from __future__ import annotations

# ruff: noqa: E402 - the standalone verifier package root precedes local imports.

import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier
from standards_verifier.model import CheckContext


class BaselineMarkdownHeadingsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("docs/source.md", "# Removed heading\n\nBody.\n")
        self.git("init", "-q")
        self.git("config", "user.email", "fixtures@example.invalid")
        self.git("config", "user.name", "Verifier Fixtures")
        self.git("add", "-A")
        self.git("commit", "-qm", "baseline")
        self.baseline = self.git("rev-parse", "HEAD").strip()
        self.write("docs/source.md", "# Current heading\n\nBody.\n")
        self.write_evidence()
        self.write_suite()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ("git", *arguments),
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout

    def write_evidence(
        self,
        *,
        dispositions: str = "",
        expected: str = "STD-0001\tdeferred\trecorded gap\n",
        inventory_line: str = "1",
        summary: str | None = None,
    ) -> None:
        self.write(
            "evidence/inventory.tsv",
            "id\tpath\tline\tlevel\ttarget_role\tdisposition\theading\n"
            f"STD-0001\tdocs/source.md\t{inventory_line}\t1\ttopic\trefine\t"
            "Removed heading\n",
        )
        self.write(
            "evidence/dispositions.tsv",
            "id\tsource\ttarget\tdisposition\trationale\n" + dispositions,
        )
        self.write(
            "evidence/expected.tsv",
            "id\tclassification\treason\n" + expected,
        )
        self.write(
            "evidence/summary.tsv",
            summary
            if summary is not None
            else f"metric\tvalue\nbaseline_commit\t{self.baseline}\n",
        )

    def write_suite(self, *, extra: str = "", classifications: str = "") -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "source-gaps"
            path = "suites/source-gaps.toml"
            requires = []
            """,
        )
        selected = classifications or 'deferred = "absent"\nretained = "present"'
        self.write(
            "suites/source-gaps.toml",
            f"""
            schema_version = 1
            id = "source-gaps"
            owner = "test.owner"
            description = "Baseline Markdown heading test"

            [[checks]]
            id = "headings"
            type = "baseline_markdown_headings"
            inventory = "evidence/inventory.tsv"
            dispositions = "evidence/dispositions.tsv"
            expected = "evidence/expected.tsv"
            summary = "evidence/summary.tsv"
            {extra}
            [checks.classifications]
            {selected}
            """,
        )

    def result(self):
        return Verifier(self.root, "registry.toml").run()[0]

    def test_accepts_exact_absent_gap(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_accepts_disposed_heading_without_expected_gap(self) -> None:
        self.write_evidence(
            dispositions=(
                "STD-0001\tdocs/source.md\tdocs/current.md\trefine\treconciled\n"
            ),
            expected="",
        )

        self.assertEqual(self.result().status, "passed")

    def test_rejects_unrecorded_undisposed_heading(self) -> None:
        self.write_evidence(expected="")

        result = self.result()

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.diagnostics[0].code, "ASSERT.BASELINE_HEADING_UNRECORDED"
        )

    def test_rejects_expected_gap_that_is_not_observed(self) -> None:
        self.write_evidence(inventory_line="2")

        result = self.result()

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.diagnostics[0].code, "ASSERT.BASELINE_HEADING_NOT_OBSERVED"
        )

    def test_checks_current_heading_state_from_classification(self) -> None:
        self.write_evidence(expected="STD-0001\tretained\tmust remain\n")

        result = self.result()

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].code, "ASSERT.BASELINE_HEADING_STATE")
        self.assertEqual(result.diagnostics[0].expected, "present")
        self.assertEqual(result.diagnostics[0].observed, "absent")

        self.write("docs/source.md", "# Current heading\n\n# Removed heading\n")
        self.assertEqual(self.result().status, "passed")

    def test_rejects_unknown_expected_classification(self) -> None:
        self.write_evidence(expected="STD-0001\tunknown\tinvalid class\n")

        result = self.result()
        self.assertEqual(
            result.diagnostics[0].code, "INPUT.BASELINE_HEADING_EVIDENCE"
        )

    def test_rejects_invalid_baseline_authority(self) -> None:
        self.write_evidence(summary="metric\tvalue\nbaseline_commit\tnot-an-oid\n")

        result = self.result()
        self.assertEqual(
            result.diagnostics[0].code, "INPUT.BASELINE_HEADING_EVIDENCE"
        )

    def test_types_missing_git_repository(self) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            outside = Path(outside_dir)
            for path in ("registry.toml", "suites", "evidence", "docs"):
                source = self.root / path
                target = outside / path
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    target.write_bytes(source.read_bytes())
            result = Verifier(outside, "registry.toml").run()[0]

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(
            result.diagnostics[0].code, "REPOSITORY_GIT.COMMAND_UNAVAILABLE"
        )

    def test_rejects_unknown_fields_and_invalid_classification_maps(self) -> None:
        cases = (
            ('command = "git"', "", "CONFIG.UNKNOWN_FIELD"),
            ("", 'deferred = "unknown"', "CONFIG.BASELINE_HEADING_CLASSIFICATIONS"),
            ("", "", None),
        )
        for extra, classifications, code in cases:
            if code is None:
                continue
            with self.subTest(extra=extra, classifications=classifications):
                self.write_suite(extra=extra, classifications=classifications)
                with self.assertRaises(EngineError) as raised:
                    self.result()
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_suite_input_authority_is_bounded(self) -> None:
        verifier = Verifier(self.root, "registry.toml")
        verifier.run()
        catalog = verifier.catalog
        suite = catalog.suite("source-gaps")
        declarations = suite.checks[0].authority_inputs(
            CheckContext(self.root, suite.id, catalog)
        )

        self.assertEqual(len(declarations), 5)
        self.assertEqual(
            sorted(item.role for item in declarations),
            [
                "baseline-authority",
                "disposition-authority",
                "expected-gap-authority",
                "heading-inventory",
                "markdown-source-membership",
            ],
        )


if __name__ == "__main__":
    unittest.main()
