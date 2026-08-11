from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier


class ReferenceInventoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.external_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write("candidates.tsv", "path\ndocs/a.md\ndocs/b.md\n")
        self.write("manifest.tsv", "path\ndocs/a.md\n")
        self.write("docs/a.md", "contains README.md route\n")
        self.write("docs/b.md", "other content\n")
        self.write_suite()
        self.write_registry()

    def tearDown(self) -> None:
        self.external_dir.cleanup()
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self) -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "inventory"
            path = "suites/inventory.toml"
            requires = []
            """,
        )

    def write_suite(self, *, extra: str = "", candidate_column: str = "path") -> None:
        self.write(
            "suites/inventory.toml",
            f"""
            schema_version = 1
            id = "inventory"
            owner = "test.owner"
            description = "Reference inventory test"

            [[checks]]
            id = "references"
            type = "reference_inventory"
            candidates_path = "candidates.tsv"
            candidates_header = ["path"]
            candidate_path_column = {json.dumps(candidate_column)}
            manifest_path = "manifest.tsv"
            manifest_header = ["path"]
            manifest_path_column = "path"
            literal = "README.md"
            {extra}
            """,
        )

    def result(self):
        return Verifier(self.root, "registry.toml").run()[0]

    def test_exact_literal_inventory_passes(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_missing_manifest_member_is_invalid(self) -> None:
        self.write("manifest.tsv", "path\n")
        diagnostic = self.result().diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.REFERENCE_INVENTORY")
        self.assertEqual(diagnostic.observed, "docs/a.md")

    def test_extra_manifest_member_is_invalid(self) -> None:
        self.write("manifest.tsv", "path\ndocs/a.md\ndocs/b.md\n")
        diagnostic = self.result().diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.REFERENCE_INVENTORY")
        self.assertEqual(diagnostic.expected, "docs/a.md,docs/b.md")

    def test_duplicate_candidate_path_is_invalid(self) -> None:
        self.write("candidates.tsv", "path\ndocs/a.md\ndocs/a.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "TABLE.DUPLICATE_PATH")

    def test_duplicate_manifest_path_is_invalid(self) -> None:
        self.write("manifest.tsv", "path\ndocs/a.md\ndocs/a.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "TABLE.DUPLICATE_PATH")

    def test_missing_candidate_file_is_unavailable(self) -> None:
        self.write("candidates.tsv", "path\ndocs/missing.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")
        self.assertEqual(result.diagnostics[0].outcome, "unavailable")

    def test_invalid_utf8_candidate_is_invalid(self) -> None:
        (self.root / "docs/a.md").write_bytes(b"\xff")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

    def test_candidate_escape_is_invalid(self) -> None:
        self.write("candidates.tsv", "path\n../outside.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_manifest_member_escape_is_invalid(self) -> None:
        self.write("manifest.tsv", "path\n../outside.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_symlink_escape_is_invalid(self) -> None:
        external = Path(self.external_dir.name) / "outside.md"
        external.write_text("README.md\n", encoding="utf-8")
        (self.root / "escape.md").symlink_to(external)
        self.write("candidates.tsv", "path\nescape.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_unknown_field_is_invalid(self) -> None:
        self.write_suite(extra='unexpected = "value"')
        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_path_column_must_belong_to_header(self) -> None:
        self.write_suite(candidate_column="missing")
        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.TABLE_COLUMN")

    def test_table_header_must_match_exactly(self) -> None:
        self.write("candidates.tsv", "file\ndocs/a.md\n")
        result = self.result()
        self.assertEqual(result.diagnostics[0].code, "TABLE.HEADER_CONTRACT")

    def test_literal_must_be_non_empty(self) -> None:
        suite = self.root / "suites/inventory.toml"
        suite.write_text(
            suite.read_text(encoding="utf-8").replace(
                'literal = "README.md"', 'literal = ""'
            ),
            encoding="utf-8",
        )
        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.STRING")


if __name__ == "__main__":
    unittest.main()
