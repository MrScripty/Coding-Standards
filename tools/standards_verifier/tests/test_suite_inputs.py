from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from standards_verifier.config import parse_check as parse_registered_check
from standards_verifier.model import (
    CheckRepositoryIndexInput,
    present_inputs,
    absent_inputs,
)

from standards_verifier.diagnostics import EngineError
from standards_verifier.suite_inputs import (
    CONTRACT,
    check_suite_input_projection,
    compile_suite_input_projection,
    write_suite_input_projection,
)


class SuiteInputProjectionTest(unittest.TestCase):
    def setUp(self) -> None:
        def parse_fixture(raw, suite):
            if raw.get("type") != "fixture_inputs":
                return parse_registered_check(raw, suite)

            def inputs(context):
                return (
                    *present_inputs(
                        "content", *([raw["path"]] if "path" in raw else [])
                    ),
                    *present_inputs("required-present", *raw.get("present", [])),
                    *absent_inputs("required-absent", *raw.get("absent", [])),
                    *(
                        (CheckRepositoryIndexInput("tracked"),)
                        if "tracked" in raw
                        else ()
                    ),
                )

            return SimpleNamespace(id=raw["id"], authority_inputs=inputs)

        adapter = patch(
            "standards_verifier.config.parse_check", side_effect=parse_fixture
        )
        adapter.start()
        self.addCleanup(adapter.stop)
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write(
            "evaluation/standards-effectiveness/suite-registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "fixture"
            path = "evaluation/standards-effectiveness/suites/fixture.toml"
            requires = []
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/suites/fixture.toml",
            """
            schema_version = 1
            id = "fixture"
            owner = "test"
            description = "Typed suite input fixture."

            [[checks]]
            id = "content"
            type = "fixture_inputs"
            path = "present.md"
            required = ["present"]
            prohibited = []
            match_case = "sensitive"

            [[checks]]
            id = "state"
            type = "fixture_inputs"
            present = ["present.md"]
            absent = ["absent.md"]

            [[checks]]
            id = "tracked"
            type = "fixture_inputs"
            tracked = ["present.md"]
            """,
        )
        self.write("present.md", "present\n")
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        subprocess.run(("git", "add", "-A"), cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def test_projection_distinguishes_content_and_absence(self) -> None:
        projection = compile_suite_input_projection(self.root)

        self.assertEqual(projection["contract"], CONTRACT)
        inputs = {item["path"]: item for item in projection["files"]}
        self.assertEqual(inputs["present.md"]["state"], "present")
        self.assertTrue(inputs["present.md"]["digest"].startswith("sha256:"))
        self.assertEqual(inputs["absent.md"]["state"], "absent")
        self.assertNotIn("digest", inputs["absent.md"])
        self.assertEqual(
            [use["check"] for use in inputs["present.md"]["uses"]],
            ["content", "state"],
        )
        self.assertIsNotNone(projection["repository_index"])

    def test_missing_required_present_input_is_rejected(self) -> None:
        (self.root / "present.md").unlink()

        with self.assertRaises(EngineError) as caught:
            compile_suite_input_projection(self.root)

        self.assertEqual(caught.exception.diagnostic.code, "INPUT.UNAVAILABLE")

    def test_present_absence_assertion_is_rejected(self) -> None:
        self.write("absent.md", "unexpected\n")

        with self.assertRaises(EngineError) as caught:
            compile_suite_input_projection(self.root)

        self.assertEqual(caught.exception.diagnostic.code, "INPUT.EXPECTED_ABSENT")

    def test_contradictory_cross_check_states_are_typed(self) -> None:
        suite = "evaluation/standards-effectiveness/suites/fixture.toml"
        content = (self.root / suite).read_text(encoding="utf-8")
        self.write(
            suite,
            content
            + """

            [[checks]]
            id = "contradiction"
            type = "fixture_inputs"
            present = ["absent.md"]
            absent = ["present.md"]
            """,
        )

        with self.assertRaises(EngineError) as caught:
            compile_suite_input_projection(self.root)

        self.assertEqual(caught.exception.diagnostic.code, "INPUT.CONTRADICTORY_STATE")

    def test_freshness_binds_suite_and_input_bytes(self) -> None:
        self.assertEqual(write_suite_input_projection(self.root), 0)
        self.assertEqual(check_suite_input_projection(self.root), 0)

        self.write("present.md", "present changed\n")

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_repository_projection_covers_every_parsed_check_adapter(self) -> None:
        repository = Path(__file__).resolve().parents[3]
        projection = compile_suite_input_projection(repository)

        registry = projection["registry"]
        self.assertEqual(
            registry["path"],
            "evaluation/standards-effectiveness/suite-registry.toml",
        )
        self.assertGreater(len(projection["suites"]), 0)
        self.assertGreater(len(projection["files"]), 0)
        files = {item["path"]: item for item in projection["files"]}
        for path in (
            "tools/standards_analysis/standards_analysis/coverage_publication.py",
            "tools/standards_engine/tests/test_coverage_publication.py",
        ):
            self.assertEqual(files[path]["state"], "present")
            self.assertTrue(files[path]["uses"])

    def test_repository_index_membership_changes_projection_identity(self) -> None:
        first = compile_suite_input_projection(self.root)["repository_index"]
        self.write("tracked-later.md", "new tracked input\n")
        subprocess.run(("git", "add", "tracked-later.md"), cwd=self.root, check=True)

        second = compile_suite_input_projection(self.root)["repository_index"]

        self.assertNotEqual(first, second)

    def test_explicit_repository_paths_use_the_canonical_projection_owner(self) -> None:
        indexed = compile_suite_input_projection(self.root)["repository_index"]
        explicit = compile_suite_input_projection(
            self.root,
            repository_paths=(
                "evaluation/standards-effectiveness/suite-registry.toml",
                "evaluation/standards-effectiveness/suites/fixture.toml",
                "present.md",
            ),
        )["repository_index"]
        without_present = compile_suite_input_projection(
            self.root,
            repository_paths=(
                "evaluation/standards-effectiveness/suite-registry.toml",
                "evaluation/standards-effectiveness/suites/fixture.toml",
            ),
        )["repository_index"]

        self.assertEqual(explicit, indexed)
        self.assertNotEqual(without_present, indexed)

    def test_written_projection_rejects_stale_repository_index(self) -> None:
        self.assertEqual(write_suite_input_projection(self.root), 0)
        self.write("tracked-later.md", "new tracked input\n")
        subprocess.run(("git", "add", "tracked-later.md"), cwd=self.root, check=True)

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_written_projection_rejects_tracked_membership_removal(self) -> None:
        self.assertEqual(write_suite_input_projection(self.root), 0)
        subprocess.run(
            ("git", "rm", "--cached", "present.md"),
            cwd=self.root,
            check=True,
            capture_output=True,
        )

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_written_projection_rejects_stale_suite_definition(self) -> None:
        self.assertEqual(write_suite_input_projection(self.root), 0)
        suite = "evaluation/standards-effectiveness/suites/fixture.toml"
        content = (self.root / suite).read_text(encoding="utf-8")
        self.write(suite, content + "\n")

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_written_projection_rejects_stale_registry(self) -> None:
        self.assertEqual(write_suite_input_projection(self.root), 0)
        registry = "evaluation/standards-effectiveness/suite-registry.toml"
        content = (self.root / registry).read_text(encoding="utf-8")
        self.write(registry, content + "\n")

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_written_projection_rejects_transitive_input_mutation(self) -> None:
        self.write(
            "evaluation/standards-effectiveness/suites/fixture.toml",
            """
            schema_version = 1
            id = "fixture"
            owner = "test"
            description = "Transitive suite input fixture."

            [[checks]]
            id = "references"
            type = "markdown_links"
            members = { path = "candidates.tsv", header = ["path"], columns = ["path"], order = "source" }
            """,
        )
        self.write("candidates.tsv", "path\nconsumer.md\n")
        self.write("manifest.tsv", "path\nconsumer.md\n")
        self.write("consumer.md", "selected-marker\n")
        subprocess.run(("git", "add", "-A"), cwd=self.root, check=True)
        self.assertEqual(write_suite_input_projection(self.root), 0)

        self.write("consumer.md", "selected-marker changed\n")

        self.assertEqual(check_suite_input_projection(self.root), 2)

    def test_written_projection_is_canonical_json(self) -> None:
        write_suite_input_projection(self.root)
        path = (
            self.root / "evaluation/standards-effectiveness/generated/suite-inputs.json"
        )
        content = path.read_text(encoding="utf-8")

        self.assertEqual(
            content,
            json.dumps(json.loads(content), indent=2, sort_keys=True) + "\n",
        )


if __name__ == "__main__":
    unittest.main()
