from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from standards_verifier.diagnostics import EngineError
from standards_verifier.suite_inputs import (
    CONTRACT,
    check_suite_input_projection,
    compile_suite_input_projection,
    write_suite_input_projection,
)


class SuiteInputProjectionTest(unittest.TestCase):
    def setUp(self) -> None:
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
            type = "text"
            path = "present.md"
            required = ["present"]
            prohibited = []
            match_case = "sensitive"

            [[checks]]
            id = "state"
            type = "path_state"
            present = ["present.md"]
            absent = ["absent.md"]
            """,
        )
        self.write("present.md", "present\n")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def test_projection_distinguishes_content_and_absence(self) -> None:
        projection = compile_suite_input_projection(self.root)

        self.assertEqual(projection["contract"], CONTRACT)
        inputs = {item["path"]: item for item in projection["inputs"]}
        self.assertEqual(inputs["present.md"]["state"], "present")
        self.assertTrue(inputs["present.md"]["digest"].startswith("sha256:"))
        self.assertEqual(inputs["absent.md"]["state"], "absent")
        self.assertNotIn("digest", inputs["absent.md"])
        self.assertEqual(
            [use["check"] for use in inputs["present.md"]["uses"]],
            ["content", "state"],
        )

    def test_missing_required_present_input_is_rejected(self) -> None:
        (self.root / "present.md").unlink()

        with self.assertRaises(EngineError) as caught:
            compile_suite_input_projection(self.root)

        self.assertEqual(caught.exception.diagnostic.code, "INPUT.UNAVAILABLE")

    def test_present_absence_assertion_is_rejected(self) -> None:
        self.write("absent.md", "unexpected\n")

        with self.assertRaises(ValueError) as caught:
            compile_suite_input_projection(self.root)

        self.assertIn("suite input must be absent", str(caught.exception))

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
        self.assertGreater(len(projection["inputs"]), 0)

    def test_written_projection_is_canonical_json(self) -> None:
        write_suite_input_projection(self.root)
        path = (
            self.root
            / "evaluation/standards-effectiveness/generated/suite-inputs.json"
        )
        content = path.read_text(encoding="utf-8")

        self.assertEqual(
            content,
            json.dumps(json.loads(content), indent=2, sort_keys=True) + "\n",
        )


if __name__ == "__main__":
    unittest.main()
