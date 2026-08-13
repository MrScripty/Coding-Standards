from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def write_path_state_suite(
        self,
        *,
        present: object | None = None,
        absent: object | None = ("retired/a.md", "retired/b.md"),
        check_type: str = "path_state",
        extra: str = "",
    ) -> str:
        states = ""
        if present is not None:
            states += f"present = {json.dumps(present)}\n"
        if absent is not None:
            states += f"absent = {json.dumps(absent)}\n"
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Path state test"

            [[checks]]
            id = "paths"
            type = {json.dumps(check_type)}
            {states}
            {extra}
            """,
        )
        return suite_path

    def write_heading_policy_suite(
        self,
        *,
        path: str = "docs/index.md",
        level: str = "2",
        required: object = ("Migrated",),
        prohibited: object = (),
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Markdown heading policy test"

            [[checks]]
            id = "headings"
            type = "markdown_headings"
            path = {json.dumps(path)}
            level = {level}
            required = {json.dumps(required)}
            prohibited = {json.dumps(prohibited)}
            {extra}
            """,
        )
        return suite_path

    def write_section_text_suite(
        self,
        *,
        path: str = "docs/index.md",
        heading: str = "## Selected",
        required: object = ("required text",),
        prohibited: object = (),
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Markdown section text test"

            [[checks]]
            id = "section"
            type = "markdown_section_text"
            path = {json.dumps(path)}
            heading = {json.dumps(heading)}
            required = {json.dumps(required)}
            prohibited = {json.dumps(prohibited)}
            {extra}
            """,
        )
        return suite_path

    def write_heading_cardinality_suite(
        self,
        *,
        path: str = "docs/index.md",
        level: str = "2",
        cardinality: object = "single",
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Markdown heading cardinality test"

            [[checks]]
            id = "heading-cardinality"
            type = "markdown_heading_cardinality"
            path = {json.dumps(path)}
            level = {level}
            cardinality = {json.dumps(cardinality)}
            {extra}
            """,
        )
        return suite_path

    def write_git_index_suite(
        self,
        *,
        tracked: object = ("docs/tracked.md",),
        extra: str = "",
    ) -> str:
        suite_path = "suites/files.toml"
        self.write(
            suite_path,
            f"""
            schema_version = 1
            id = "files"
            owner = "test.owner"
            description = "Git index path test"

            [[checks]]
            id = "git-index"
            type = "git_index_paths"
            tracked = {json.dumps(tracked)}
            {extra}
            """,
        )
        return suite_path

    def initialize_git_index(self, *paths: str) -> None:
        subprocess.run(
            ["git", "init", "-q"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "add", "--", *paths],
            cwd=self.root,
            check=True,
        )

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

    def test_markdown_headings_applies_literals_to_every_selected_heading(self) -> None:
        self.write(
            "docs/index.md",
            """
            # Index
            ## First Migrated
            prose
            ### Nested
            ## Second Migrated
            """,
        )

        result = self.result(
            self.write_heading_policy_suite(prohibited=["Legacy"])
        )

        self.assertEqual(result.status, "passed")

    def test_markdown_headings_reports_each_required_and_prohibited_violation(self) -> None:
        self.write(
            "docs/index.md",
            "## Missing marker\n## Legacy Migrated\n## Also missing\n",
        )

        result = self.result(
            self.write_heading_policy_suite(prohibited=["Legacy"])
        )

        self.assertEqual(
            [(item.code, item.row) for item in result.diagnostics],
            [
                ("ASSERT.MARKDOWN_HEADING_REQUIRED", 1),
                ("ASSERT.MARKDOWN_HEADING_PROHIBITED", 2),
                ("ASSERT.MARKDOWN_HEADING_REQUIRED", 3),
            ],
        )

    def test_markdown_headings_requires_nonempty_level_selection(self) -> None:
        self.write("docs/index.md", "# Migrated\n### Migrated\n")

        result = self.result(self.write_heading_policy_suite())

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.MARKDOWN_HEADING_SELECTION",
        )

    def test_markdown_headings_ignores_heading_syntax_inside_fences(self) -> None:
        self.write(
            "docs/index.md",
            (
                "## Real Migrated\n"
                "```markdown\n## Not migrated\n```\n"
                "~~~text\n## Also not migrated\n~~~~\n"
            ),
        )

        result = self.result(self.write_heading_policy_suite())

        self.assertEqual(result.status, "passed")

    def test_markdown_headings_recognizes_only_atx_heading_syntax(self) -> None:
        self.write(
            "docs/index.md",
            "## Migrated\n  ## Indented Migrated\n##NoSpace\n####### TooMany\n",
        )

        result = self.result(self.write_heading_policy_suite())

        self.assertEqual(result.status, "passed")

    def test_markdown_headings_invalid_utf8_and_missing_input_are_typed(self) -> None:
        target = self.root / "docs/index.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"## Migrated\n\xff")
        result = self.result(self.write_heading_policy_suite())
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

        target.unlink()
        result = self.result(self.write_heading_policy_suite())
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_markdown_headings_rejects_escaping_paths(self) -> None:
        external = Path(self.external_dir.name)
        (external / "index.md").write_text("## Migrated\n", encoding="utf-8")
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for path in ("/tmp/index.md", "../index.md", "escape/index.md"):
            with self.subTest(path=path):
                result = self.result(self.write_heading_policy_suite(path=path))
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_markdown_headings_rejects_configuration_errors(self) -> None:
        cases = (
            ({"level": "0"}, "CONFIG.HEADING_LEVEL"),
            ({"level": "7"}, "CONFIG.HEADING_LEVEL"),
            ({"level": "true"}, "CONFIG.HEADING_LEVEL"),
            ({"level": '"2"'}, "CONFIG.HEADING_LEVEL"),
            ({"required": []}, "CONFIG.EMPTY_CHECK"),
            ({"required": [""]}, "CONFIG.STRING_LIST"),
            ({"required": ["x", "x"]}, "CONFIG.STRING_LIST"),
            (
                {"required": ["x"], "prohibited": ["x"]},
                "CONFIG.CONTRADICTORY_TEXT",
            ),
            ({"path": ""}, "CONFIG.PATH"),
            ({"extra": 'pattern = "Migrated"'}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code, options=options):
                suite = self.write_heading_policy_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_markdown_heading_cardinality_accepts_semantic_boundaries(self) -> None:
        cases = (
            ("empty", "# Root\n", "empty"),
            ("single", "# Root\n## One\n", "single"),
            ("nonempty-one", "## One\n", "nonempty"),
            ("nonempty-many", "## One\n## Two\n", "nonempty"),
        )
        for name, content, cardinality in cases:
            with self.subTest(name=name):
                self.write("docs/index.md", content)
                result = self.result(
                    self.write_heading_cardinality_suite(
                        cardinality=cardinality
                    )
                )
                self.assertEqual(result.status, "passed")

    def test_markdown_heading_cardinality_reports_semantic_states(self) -> None:
        cases = (
            ("## One\n", "empty", "single"),
            ("## One\n## Two\n", "empty", "multiple"),
            ("# Root\n", "single", "empty"),
            ("## One\n## Two\n", "single", "multiple"),
            ("# Root\n", "nonempty", "empty"),
        )
        for content, expected, observed in cases:
            with self.subTest(expected=expected, observed=observed):
                self.write("docs/index.md", content)
                result = self.result(
                    self.write_heading_cardinality_suite(
                        cardinality=expected
                    )
                )
                self.assertEqual(result.exit_code, 1)
                diagnostic = result.diagnostics[0]
                self.assertEqual(
                    diagnostic.code,
                    "ASSERT.MARKDOWN_HEADING_CARDINALITY",
                )
                self.assertEqual(diagnostic.expected, expected)
                self.assertEqual(diagnostic.observed, observed)

    def test_markdown_heading_cardinality_isolates_level_and_fences(self) -> None:
        self.write(
            "docs/index.md",
            (
                "# Root\n"
                "```markdown\n## Fenced one\n## Fenced two\n```\n"
                "### Nested\n"
                "## Real\n"
            ),
        )

        result = self.result(self.write_heading_cardinality_suite())

        self.assertEqual(result.status, "passed")

    def test_markdown_heading_cardinality_invalid_utf8_and_missing_are_typed(
        self,
    ) -> None:
        target = self.root / "docs/index.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"## Heading\n\xff")
        result = self.result(self.write_heading_cardinality_suite())
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

        target.unlink()
        result = self.result(self.write_heading_cardinality_suite())
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_markdown_heading_cardinality_rejects_escaping_paths(self) -> None:
        external = Path(self.external_dir.name)
        (external / "index.md").write_text("## Heading\n", encoding="utf-8")
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for path in ("/tmp/index.md", "../index.md", "escape/index.md"):
            with self.subTest(path=path):
                result = self.result(
                    self.write_heading_cardinality_suite(path=path)
                )
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_markdown_heading_cardinality_rejects_configuration_errors(
        self,
    ) -> None:
        cases = (
            ({"level": "0"}, "CONFIG.HEADING_LEVEL"),
            ({"level": "7"}, "CONFIG.HEADING_LEVEL"),
            ({"level": "true"}, "CONFIG.HEADING_LEVEL"),
            ({"level": '"2"'}, "CONFIG.HEADING_LEVEL"),
            ({"cardinality": ""}, "CONFIG.HEADING_CARDINALITY"),
            ({"cardinality": "multiple"}, "CONFIG.HEADING_CARDINALITY"),
            ({"cardinality": 1}, "CONFIG.HEADING_CARDINALITY"),
            ({"path": ""}, "CONFIG.PATH"),
            ({"extra": "count = 1"}, "CONFIG.UNKNOWN_FIELD"),
            ({"extra": 'mode = "single"'}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code, options=options):
                suite = self.write_heading_cardinality_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

        for missing, code in (
            ("path", "CONFIG.PATH"),
            ("level", "CONFIG.HEADING_LEVEL"),
            ("cardinality", "CONFIG.HEADING_CARDINALITY"),
        ):
            with self.subTest(missing=missing):
                fields = {
                    "path": 'path = "docs/index.md"',
                    "level": "level = 2",
                    "cardinality": 'cardinality = "single"',
                }
                del fields[missing]
                suite_path = "suites/files.toml"
                self.write(
                    suite_path,
                    f"""
                    schema_version = 1
                    id = "files"
                    owner = "test.owner"
                    description = "Missing field"

                    [[checks]]
                    id = "heading-cardinality"
                    type = "markdown_heading_cardinality"
                    {fields.get("path", "")}
                    {fields.get("level", "")}
                    {fields.get("cardinality", "")}
                    """,
                )
                self.write_registry(suite_path)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_git_index_paths_accepts_present_and_deleted_tracked_paths(self) -> None:
        tracked = ("docs/tracked file.md", "docs/caf\u00e9.md")
        for path in tracked:
            self.write(path, "tracked\n")
        self.initialize_git_index(*tracked)
        (self.root / tracked[1]).unlink()

        result = self.result(self.write_git_index_suite(tracked=tracked))

        self.assertEqual(result.status, "passed")

    def test_git_index_paths_distinguishes_untracked_worktree_state(self) -> None:
        self.write("docs/present.md", "untracked\n")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

        result = self.result(
            self.write_git_index_suite(
                tracked=("docs/present.md", "docs/absent.md")
            )
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            [(item.path, item.observed) for item in result.diagnostics],
            [
                ("docs/present.md", "present-untracked"),
                ("docs/absent.md", "absent-untracked"),
            ],
        )

    def test_git_index_paths_requires_exact_membership(self) -> None:
        self.write("docs/prompt-long.md", "tracked\n")
        self.initialize_git_index("docs/prompt-long.md")

        result = self.result(
            self.write_git_index_suite(tracked=("docs/prompt.md",))
        )

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.diagnostics[0].observed, "absent-untracked")

    @patch("standards_verifier.checks.git_index_paths.subprocess.run")
    def test_git_index_paths_uses_one_fixed_index_read(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            [],
            0,
            stdout=b"docs/a.md\0docs/b.md\0",
            stderr=b"",
        )
        with patch.dict(
            os.environ,
            {"GIT_DIR": "/outside", "GIT_INDEX_FILE": "/outside/index"},
        ):
            result = self.result(
                self.write_git_index_suite(tracked=("docs/a.md", "docs/b.md"))
            )

        self.assertEqual(result.status, "passed")
        run.assert_called_once()
        arguments, options = run.call_args
        self.assertEqual(
            arguments[0],
            ["git", "-C", str(self.root), "ls-files", "-z", "--full-name"],
        )
        self.assertFalse(options["check"])
        self.assertTrue(options["capture_output"])
        self.assertNotIn("GIT_DIR", options["env"])
        self.assertNotIn("GIT_INDEX_FILE", options["env"])

    def test_git_index_paths_types_git_and_output_failures(self) -> None:
        cases = (
            (FileNotFoundError("missing"), "GIT.UNAVAILABLE", 3),
            (
                subprocess.CompletedProcess([], 128, stdout=b"", stderr=b"fatal"),
                "GIT.INDEX_UNAVAILABLE",
                3,
            ),
            (
                subprocess.CompletedProcess([], 0, stdout=b"docs/a.md", stderr=b""),
                "GIT.INDEX_OUTPUT",
                2,
            ),
            (
                subprocess.CompletedProcess([], 0, stdout=b"docs/\xff.md\0", stderr=b""),
                "GIT.INDEX_UTF8",
                2,
            ),
            (
                subprocess.CompletedProcess([], 0, stdout=b"docs/a.md\0\0", stderr=b""),
                "GIT.INDEX_OUTPUT",
                2,
            ),
        )
        for effect, code, exit_code in cases:
            with self.subTest(code=code):
                with patch(
                    "standards_verifier.checks.git_index_paths.subprocess.run",
                    side_effect=effect if isinstance(effect, Exception) else None,
                    return_value=None if isinstance(effect, Exception) else effect,
                ):
                    result = self.result(self.write_git_index_suite())
                self.assertEqual(result.exit_code, exit_code)
                self.assertEqual(result.diagnostics[0].code, code)

    def test_git_index_paths_types_non_repository_root(self) -> None:
        result = self.result(self.write_git_index_suite())

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "GIT.INDEX_UNAVAILABLE")

    def test_git_index_paths_rejects_configuration_errors(self) -> None:
        cases = (
            ({"tracked": []}, "CONFIG.STRING_LIST"),
            ({"tracked": [""]}, "CONFIG.STRING_LIST"),
            ({"tracked": ["docs/a.md", "docs/a.md"]}, "CONFIG.STRING_LIST"),
            ({"tracked": ["/docs/a.md"]}, "PATH.OUTSIDE_REPOSITORY"),
            ({"tracked": ["../docs/a.md"]}, "PATH.OUTSIDE_REPOSITORY"),
            ({"tracked": ["."]}, "CONFIG.GIT_INDEX_PATH"),
            ({"tracked": ["docs/./a.md"]}, "CONFIG.GIT_INDEX_PATH"),
            ({"tracked": ["docs//a.md"]}, "CONFIG.GIT_INDEX_PATH"),
            ({"extra": 'command = "git"'}, "CONFIG.UNKNOWN_FIELD"),
            ({"extra": 'flags = ["--cached"]'}, "CONFIG.UNKNOWN_FIELD"),
            ({"extra": 'repository = "."'}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code, options=options):
                suite = self.write_git_index_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_markdown_section_text_selects_through_nested_headings(self) -> None:
        self.write(
            "docs/index.md",
            """
            # Index
            outside prohibited
            ## Selected
            required text
            ### Nested
            nested text
            ## Next
            prohibited
            """,
        )

        result = self.result(
            self.write_section_text_suite(
                required=["required text", "nested text"],
                prohibited=["prohibited"],
            )
        )

        self.assertEqual(result.status, "passed")

    def test_markdown_section_text_stops_at_higher_heading(self) -> None:
        self.write(
            "docs/index.md",
            "## Selected\nrequired text\n# Next\nprohibited\n",
        )

        result = self.result(
            self.write_section_text_suite(prohibited=["prohibited"])
        )

        self.assertEqual(result.status, "passed")

    def test_markdown_section_text_ignores_fenced_heading_boundaries(self) -> None:
        self.write(
            "docs/index.md",
            (
                "```markdown\n## Selected\n```\n"
                "## Selected\nrequired text\n"
                "~~~markdown\n# Not a boundary\n~~~\n"
                "still selected\n## Next\n"
            ),
        )

        result = self.result(
            self.write_section_text_suite(required=["still selected"])
        )

        self.assertEqual(result.status, "passed")

    def test_markdown_section_text_requires_one_exact_start_heading(self) -> None:
        for content, observed in (
            ("## Other\nrequired text\n", "absent"),
            (
                "## Selected\nrequired text\n## Selected\nrequired text\n",
                "2 matches",
            ),
        ):
            with self.subTest(observed=observed):
                self.write("docs/index.md", content)
                result = self.result(self.write_section_text_suite())
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "ASSERT.MARKDOWN_SECTION_SELECTION",
                )
                self.assertEqual(result.diagnostics[0].observed, observed)

    def test_markdown_section_text_reports_literal_failures_in_order(self) -> None:
        self.write("docs/index.md", "## Selected\nprohibited text\n")

        result = self.result(
            self.write_section_text_suite(
                required=["first missing", "second missing"],
                prohibited=["prohibited text"],
            )
        )

        self.assertEqual(
            [(item.code, item.expected, item.observed) for item in result.diagnostics],
            [
                ("ASSERT.MARKDOWN_SECTION_REQUIRED", "first missing", "absent"),
                ("ASSERT.MARKDOWN_SECTION_REQUIRED", "second missing", "absent"),
                ("ASSERT.MARKDOWN_SECTION_PROHIBITED", "absent", "prohibited text"),
            ],
        )

    def test_markdown_section_text_invalid_utf8_and_missing_input_are_typed(
        self,
    ) -> None:
        target = self.root / "docs/index.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"## Selected\nrequired text\n\xff")
        result = self.result(self.write_section_text_suite())
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

        target.unlink()
        result = self.result(self.write_section_text_suite())
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_markdown_section_text_rejects_escaping_paths(self) -> None:
        external = Path(self.external_dir.name)
        (external / "index.md").write_text(
            "## Selected\nrequired text\n", encoding="utf-8"
        )
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for path in ("/tmp/index.md", "../index.md", "escape/index.md"):
            with self.subTest(path=path):
                result = self.result(self.write_section_text_suite(path=path))
                self.assertEqual(result.exit_code, 2)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_markdown_section_text_rejects_configuration_errors(self) -> None:
        cases = (
            ({"heading": ""}, "CONFIG.MARKDOWN_HEADING"),
            ({"heading": "Selected"}, "CONFIG.MARKDOWN_HEADING"),
            ({"heading": "####### Selected"}, "CONFIG.MARKDOWN_HEADING"),
            ({"heading": "## Selected\ntext"}, "CONFIG.MARKDOWN_HEADING"),
            ({"required": []}, "CONFIG.EMPTY_CHECK"),
            ({"required": [""]}, "CONFIG.STRING_LIST"),
            ({"required": ["x", "x"]}, "CONFIG.STRING_LIST"),
            (
                {"required": ["x"], "prohibited": ["x"]},
                "CONFIG.CONTRADICTORY_TEXT",
            ),
            ({"path": ""}, "CONFIG.PATH"),
            ({"extra": 'pattern = "required"'}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code, options=options):
                suite = self.write_section_text_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_path_state_accepts_present_and_absent_paths(self) -> None:
        self.write("present/file.md", "present\n")
        (self.root / "present/directory").mkdir()
        (self.root / "present/link").symlink_to("file.md")

        result = self.result(
            self.write_path_state_suite(
                present=[
                    "present/file.md",
                    "present/directory",
                    "present/link",
                ]
            )
        )

        self.assertEqual(result.status, "passed")

    def test_path_state_reports_missing_present_paths_unavailable(self) -> None:
        (self.root / "present").mkdir()
        (self.root / "present/broken").symlink_to("missing.md")
        for path in ("present/missing.md", "present/broken"):
            with self.subTest(path=path):
                result = self.result(
                    self.write_path_state_suite(
                        present=[path],
                        absent=None,
                    )
                )
                self.assertEqual(result.exit_code, 3)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "INPUT.UNAVAILABLE",
                )
                self.assertEqual(
                    result.diagnostics[0].outcome,
                    "unavailable",
                )

    def test_path_state_rejects_entries_required_absent(self) -> None:
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
                result = self.result(
                    self.write_path_state_suite(absent=[path])
                )
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(
                    result.diagnostics[0].code,
                    "ASSERT.PATH_PRESENT",
                )

    def test_path_state_reports_each_entry_required_absent(self) -> None:
        self.write("present/a.md", "a\n")
        self.write("present/b.md", "b\n")

        result = self.result(
            self.write_path_state_suite(
                absent=["present/a.md", "present/b.md"]
            )
        )

        self.assertEqual(
            [diagnostic.path for diagnostic in result.diagnostics],
            ["present/a.md", "present/b.md"],
        )

    def test_path_state_rejects_escaping_paths_in_both_states(self) -> None:
        external = Path(self.external_dir.name)
        (self.root / "escape").symlink_to(external, target_is_directory=True)
        for field in ("present", "absent"):
            for path in (
                "/tmp/retired.md",
                "../retired.md",
                "escape/retired.md",
            ):
                with self.subTest(field=field, path=path):
                    options = {field: [path]}
                    if field == "present":
                        options["absent"] = None
                    result = self.result(
                        self.write_path_state_suite(**options)
                    )
                    self.assertEqual(result.exit_code, 2)
                    self.assertEqual(
                        result.diagnostics[0].code,
                        "PATH.OUTSIDE_REPOSITORY",
                    )

    def test_path_state_rejects_configuration_errors(self) -> None:
        cases = (
            ({"present": None, "absent": None}, "CONFIG.EMPTY_CHECK"),
            ({"absent": []}, "CONFIG.STRING_LIST"),
            ({"absent": ["a.md", "a.md"]}, "CONFIG.STRING_LIST"),
            (
                {"present": ["a.md"], "absent": ["a.md"]},
                "CONFIG.CONTRADICTORY_PATH_STATE",
            ),
            ({"extra": "allow_broken = true"}, "CONFIG.UNKNOWN_FIELD"),
        )
        for options, code in cases:
            with self.subTest(code=code):
                suite = self.write_path_state_suite(**options)
                self.write_registry(suite)
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, "registry.toml")
                self.assertEqual(raised.exception.diagnostic.code, code)

    def test_absent_paths_type_is_rejected(self) -> None:
        suite = self.write_path_state_suite(check_type="absent_paths")
        self.write_registry(suite)

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, "registry.toml")

        self.assertEqual(
            raised.exception.diagnostic.code,
            "CONFIG.UNKNOWN_CHECK",
        )


if __name__ == "__main__":
    unittest.main()
