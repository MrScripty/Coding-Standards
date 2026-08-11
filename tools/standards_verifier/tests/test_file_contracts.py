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


class FileContractsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.external_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.external_dir.cleanup()
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self, suite_path: str) -> None:
        self.write(
            "registry.toml",
            f"""
            schema_version = 1

            [[suites]]
            id = "files"
            path = {json.dumps(suite_path)}
            requires = []
            """,
        )

    def write_structure_suite(
        self,
        *,
        path: str = "docs/index.md",
        headings: object = ("# Index", "## Routes"),
        maximum_lines: str = "4",
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Markdown structure test"

            [[checks]]
            id = "structure"
            type = "markdown_structure"
            path = {json.dumps(path)}
            headings = {json.dumps(headings)}
            maximum_lines = {maximum_lines}
            {extra}
            """,
        )
        return suite_path

    def write_absent_suite(
        self,
        *,
        paths: object = ("retired/a.md", "retired/b.md"),
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Absent paths test"

            [[checks]]
            id = "retired"
            type = "absent_paths"
            paths = {json.dumps(paths)}
            {extra}
            """,
        )
        return suite_path

    def result(self, suite_path: str):
        self.write_registry(suite_path)
        return Verifier(self.root, "registry.toml").run()[0]

    def test_markdown_structure_accepts_exact_headings_at_line_limit(self) -> None:
        self.write("docs/index.md", "# Index\nintro\n## Routes\nroute\n")

        result = self.result(self.write_structure_suite())

        self.assertEqual(result.status, "passed")

    def test_markdown_structure_accepts_newline_count_below_limit(self) -> None:
        self.write("docs/index.md", "# Index\n## Routes")

        result = self.result(self.write_structure_suite(maximum_lines="2"))

        self.assertEqual(result.status, "passed")

    def test_markdown_structure_rejects_heading_order_extra_and_missing(self) -> None:
        cases = (
            "## Routes\n# Index\n",
            "# Index\n## Extra\n## Routes\n",
            "# Index\n",
        )
        for content in cases:
            with self.subTest(content=content):
                self.write("docs/index.md", content)
                result = self.result(self.write_structure_suite())
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "ASSERT.MARKDOWN_HEADINGS",
                )

    def test_markdown_structure_rejects_line_limit_excess(self) -> None:
        self.write("docs/index.md", "# Index\nintro\n## Routes\nroute\nextra\n")

        result = self.result(self.write_structure_suite())

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].code, "ASSERT.LINE_LIMIT")

    def test_markdown_structure_reports_all_contract_failures(self) -> None:
        self.write("docs/index.md", "# Wrong\na\nb\nc\nd\n")

        result = self.result(self.write_structure_suite())

        self.assertEqual(
            [diagnostic.code for diagnostic in result.diagnostics],
            ["ASSERT.MARKDOWN_HEADINGS", "ASSERT.LINE_LIMIT"],
        )

    def test_markdown_structure_invalid_utf8_is_invalid(self) -> None:
        target = self.root / "docs/index.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"# Index\n\xff")

        result = self.result(self.write_structure_suite())

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

    def test_markdown_structure_missing_source_is_unavailable(self) -> None:
        result = self.result(self.write_structure_suite())

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_markdown_structure_rejects_escaping_paths(self) -> None:
        external = Path(self.external_dir.name)
        (external / "index.md").write_text("# Index\n## Routes\n", encoding="utf-8")
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for path in ("/tmp/index.md", "../index.md", "escape/index.md"):
            with self.subTest(path=path):
                result = self.result(self.write_structure_suite(path=path))
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_markdown_structure_rejects_malformed_headings(self) -> None:
        for headings, code in (
            ([], "CONFIG.MARKDOWN_HEADINGS"),
            (["Index"], "CONFIG.MARKDOWN_HEADINGS"),
            (["# Index", "# Index"], "CONFIG.DUPLICATE_VALUE"),
        ):
            with self.subTest(headings=headings):
                suite = self.write_structure_suite(headings=headings)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_markdown_structure_requires_positive_integer_limit(self) -> None:
        for value in ("0", "-1", "true"):
            with self.subTest(value=value):
                suite = self.write_structure_suite(maximum_lines=value)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(
                    raised.exception.diagnostic.code,
                    "CONFIG.POSITIVE_INTEGER",
                )

    def test_markdown_structure_rejects_empty_path_and_unknown_field(self) -> None:
        for options, code in (
            ({"path": ""}, "CONFIG.PATH"),
            ({"extra": 'normalization = "none"'}, "CONFIG.UNKNOWN_FIELD"),
        ):
            with self.subTest(code=code):
                suite = self.write_structure_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_absent_paths_accepts_missing_paths(self) -> None:
        result = self.result(self.write_absent_suite())

        self.assertEqual(result.status, "passed")

    def test_absent_paths_rejects_present_file_directory_and_symlinks(self) -> None:
        self.write("present/file.md", "present\n")
        (self.root / "present/directory").mkdir()
        (self.root / "present/link").symlink_to("file.md")
        (self.root / "present/broken").symlink_to("missing.md")
        for path in (
            "present/file.md",
            "present/directory",
            "present/link",
            "present/broken",
        ):
            with self.subTest(path=path):
                result = self.result(self.write_absent_suite(paths=[path]))
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "ASSERT.PATH_PRESENT",
                )

    def test_absent_paths_reports_each_present_path(self) -> None:
        self.write("present/a.md", "a\n")
        self.write("present/b.md", "b\n")

        result = self.result(
            self.write_absent_suite(paths=["present/a.md", "present/b.md"])
        )

        self.assertEqual(
            [diagnostic.path for diagnostic in result.diagnostics],
            ["present/a.md", "present/b.md"],
        )

    def test_absent_paths_rejects_escaping_paths(self) -> None:
        external = Path(self.external_dir.name)
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for path in ("/tmp/retired.md", "../retired.md", "escape/retired.md"):
            with self.subTest(path=path):
                result = self.result(self.write_absent_suite(paths=[path]))
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_absent_paths_rejects_configuration_errors(self) -> None:
        cases = (
            ({"paths": []}, "CONFIG.STRING_LIST"),
            ({"paths": ["a.md", "a.md"]}, "CONFIG.STRING_LIST"),
            ({"extra": "allow_broken = true"}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code):
                suite = self.write_absent_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)


if __name__ == "__main__":
    unittest.main()
