from __future__ import annotations

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
from standards_verifier.paths import contained_file


class DerivedEvidenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry = "registry.toml"
        self.write("checks/live.sh", "#!/usr/bin/env bash\n")
        self.write(
            "subjects.tsv",
            "scope\tsubjects\n"
            "selected\tchecker:checks/live.sh,suite:derived\n",
        )
        self.write(
            "keys.tsv",
            "kind\tsource\n"
            "selected\tlanguages/README.md\n"
            "selected\tsecurity/README.md\n",
        )
        self.write(
            "records.tsv",
            "source\tdisposition\n"
            "languages/README.md\tmove\n"
            "languages/README.md\tindex\n"
            "security/README.md\tmove\n"
            "unrelated/README.md\tmove\n",
        )
        self.write(
            "literals.tsv",
            "kind\tpath\n"
            "former\tlanguages/README.md\n"
            "former\tsecurity/README.md\n",
        )
        self.write("docs/commit.md", "# Commit\n")
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\n"
            "selected\tmove\tdocs/commit.md\n"
            "selected\tremove\tnone\n"
            "ignored\tmove\tmissing.md\n",
        )
        self.write("ROUTER.md", "Canonical modules only.\n")
        self.write_registry()
        self.write_suite()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_registry(self) -> None:
        self.write(
            self.registry,
            """
            schema_version = 1

            [[suites]]
            id = "derived"
            path = "suites/derived.toml"
            requires = []
            """,
        )

    def write_suite(
        self,
        *,
        subject_columns: str = '["subjects"]',
        subject_extra: str = "",
        path_columns: str = '["target"]',
        path_extra: str = "",
        path_source_extra: str = "",
        coverage_extra: str = "",
        absence_extra: str = "",
    ) -> None:
        self.write(
            "suites/derived.toml",
            f"""
            schema_version = 1
            id = "derived"
            owner = "test.owner"
            description = "Derived evidence suite"

            [[checks]]
            id = "subjects"
            type = "repository_subjects"
            {subject_extra}
            [checks.subjects]
            path = "subjects.tsv"
            header = ["scope", "subjects"]
            columns = {subject_columns}
            order = "source"
            where = {{ field = "scope", op = "eq", value = "selected" }}
            split = {{ field = "subjects", delimiter = "," }}

            [[checks]]
            id = "paths"
            type = "repository_paths"
            {path_extra}
            [checks.paths]
            path = "paths.tsv"
            header = ["scope", "disposition", "target"]
            columns = {path_columns}
            order = "source"
            where = {{ all = [
              {{ field = "scope", op = "eq", value = "selected" }},
              {{ field = "disposition", op = "ne", value = "remove" }},
            ] }}
            {path_source_extra}

            [[checks]]
            id = "coverage"
            type = "key_coverage"
            {coverage_extra}
            [checks.keys]
            path = "keys.tsv"
            header = ["kind", "source"]
            columns = ["source"]
            order = "source"
            where = {{ field = "kind", op = "eq", value = "selected" }}
            [checks.records]
            path = "records.tsv"
            header = ["source", "disposition"]
            columns = ["source"]
            order = "source"

            [[checks]]
            id = "absence"
            type = "table_text_absence"
            path = "ROUTER.md"
            {absence_extra}
            [checks.literals]
            path = "literals.tsv"
            header = ["kind", "path"]
            columns = ["path"]
            order = "source"
            where = {{ field = "kind", op = "eq", value = "former" }}
            """,
        )

    def run_suite(self):
        return Verifier(self.root, self.registry).run()[0]

    def test_all_derived_evidence_contracts_pass(self) -> None:
        result = self.run_suite()

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.check_count, 4)

    def test_repository_paths_rejects_empty_projection(self) -> None:
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tremove\tnone\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.REPOSITORY_PATHS_EMPTY")

    def test_repository_paths_accepts_repeated_values(self) -> None:
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\n"
            "selected\tmove\tdocs/commit.md\n"
            "selected\tmove\tdocs/commit.md\n",
        )

        with patch(
            "standards_verifier.checks.derived_evidence.contained_file",
            wraps=contained_file,
        ) as contained_file_spy:
            result = self.run_suite()

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.check_count, 4)
        path_calls = [
            call
            for call in contained_file_spy.call_args_list
            if call.kwargs["check"] == "paths"
        ]
        self.assertEqual(len(path_calls), 1)

    def test_repository_paths_rejects_empty_value(self) -> None:
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tmove\t\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.DERIVED_VALUE_EMPTY")

    def test_repository_paths_reports_missing_file_unavailable(self) -> None:
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tmove\tmissing.md\n",
        )

        result = self.run_suite()

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_repository_paths_rejects_directory(self) -> None:
        (self.root / "directory").mkdir()
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tmove\tdirectory\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "INPUT.NOT_FILE")

    def test_repository_paths_rejects_absolute_and_traversal_paths(self) -> None:
        for path in ("/tmp/outside.md", "../outside.md"):
            with self.subTest(path=path):
                self.write(
                    "paths.tsv",
                    "scope\tdisposition\ttarget\n"
                    f"selected\tmove\t{path}\n",
                )

                result = self.run_suite()

                self.assertEqual(
                    result.diagnostics[0].code,
                    "PATH.OUTSIDE_REPOSITORY",
                )

    def test_repository_paths_rejects_symlink(self) -> None:
        (self.root / "docs/link.md").symlink_to("commit.md")
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tmove\tdocs/link.md\n",
        )

        result = self.run_suite()

        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.REPOSITORY_PATH_SYMLINK",
        )

    def test_repository_paths_rejects_symlink_escape(self) -> None:
        (self.root / "docs/external").symlink_to("/tmp")
        self.write(
            "paths.tsv",
            "scope\tdisposition\ttarget\nselected\tmove\tdocs/external/file.md\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_repository_paths_rejects_malformed_table(self) -> None:
        self.write("paths.tsv", "wrong\theader\nselected\tmove\n")

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "TABLE.HEADER_CONTRACT")

    def test_repository_subject_rejects_unknown_type(self) -> None:
        self.write("subjects.tsv", "scope\tsubjects\nselected\tpath:checks/live.sh\n")

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.REPOSITORY_SUBJECT_TYPE")

    def test_repository_subject_reports_unregistered_suite_unavailable(self) -> None:
        self.write("subjects.tsv", "scope\tsubjects\nselected\tsuite:missing\n")

        result = self.run_suite()

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.SUITE_UNAVAILABLE")

    def test_repository_subject_reports_missing_checker_unavailable(self) -> None:
        self.write("subjects.tsv", "scope\tsubjects\nselected\tchecker:missing.sh\n")

        result = self.run_suite()

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_repository_subject_rejects_checker_path_escape(self) -> None:
        self.write("subjects.tsv", "scope\tsubjects\nselected\tchecker:../outside.sh\n")

        result = self.run_suite()

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.diagnostics[0].code, "PATH.OUTSIDE_REPOSITORY")

    def test_repository_subject_rejects_checker_symlink(self) -> None:
        (self.root / "checks/link.sh").symlink_to("live.sh")
        self.write("subjects.tsv", "scope\tsubjects\nselected\tchecker:checks/link.sh\n")

        result = self.run_suite()

        self.assertEqual(
            result.diagnostics[0].code,
            "ASSERT.REPOSITORY_SUBJECT_SYMLINK",
        )

    def test_repository_subject_rejects_duplicate_projection(self) -> None:
        self.write(
            "subjects.tsv",
            "scope\tsubjects\nselected\tsuite:derived,suite:derived\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.DERIVED_VALUE_DUPLICATE")

    def test_key_coverage_reports_uncovered_key(self) -> None:
        self.write(
            "records.tsv",
            "source\tdisposition\nlanguages/README.md\tmove\n",
        )

        result = self.run_suite()

        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.KEY_COVERAGE_MISSING")
        self.assertEqual(diagnostic.expected, "security/README.md")

    def test_key_coverage_allows_multiple_and_unrelated_records(self) -> None:
        result = self.run_suite()

        self.assertEqual(result.status, "passed")

    def test_key_coverage_rejects_duplicate_derived_keys(self) -> None:
        self.write(
            "keys.tsv",
            "kind\tsource\n"
            "selected\tlanguages/README.md\n"
            "selected\tlanguages/README.md\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.DERIVED_VALUE_DUPLICATE")

    def test_key_coverage_reports_missing_record_table_unavailable(self) -> None:
        (self.root / "records.tsv").unlink()

        result = self.run_suite()

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_table_text_absence_reports_derived_literal(self) -> None:
        self.write("ROUTER.md", "Route through languages/README.md.\n")

        result = self.run_suite()

        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.code, "ASSERT.TABLE_TEXT_PRESENT")
        self.assertEqual(diagnostic.observed, "languages/README.md")

    def test_table_text_absence_rejects_invalid_utf8(self) -> None:
        (self.root / "ROUTER.md").write_bytes(b"\xff")

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "INPUT.INVALID_UTF8")

    def test_table_text_absence_reports_missing_target_unavailable(self) -> None:
        (self.root / "ROUTER.md").unlink()

        result = self.run_suite()

        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.diagnostics[0].code, "INPUT.UNAVAILABLE")

    def test_table_text_absence_rejects_duplicate_literals(self) -> None:
        self.write(
            "literals.tsv",
            "kind\tpath\n"
            "former\tlanguages/README.md\n"
            "former\tlanguages/README.md\n",
        )

        result = self.run_suite()

        self.assertEqual(result.diagnostics[0].code, "ASSERT.DERIVED_VALUE_DUPLICATE")

    def test_checks_reject_unknown_fields(self) -> None:
        for field in (
            "subject_extra",
            "path_extra",
            "coverage_extra",
            "absence_extra",
        ):
            with self.subTest(field=field):
                self.write_suite(**{field: "fallback = true"})
                with self.assertRaises(EngineError) as raised:
                    Verifier(self.root, self.registry)
                self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_projection_must_select_one_column(self) -> None:
        self.write_suite(subject_columns='["scope", "subjects"]')

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(
            raised.exception.diagnostic.code,
            "CONFIG.REPOSITORY_SUBJECTS_WIDTH",
        )

    def test_repository_path_projection_must_select_one_column(self) -> None:
        self.write_suite(path_columns='["scope", "target"]')

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(
            raised.exception.diagnostic.code,
            "CONFIG.REPOSITORY_PATHS_WIDTH",
        )

    def test_repository_path_source_rejects_unknown_fields(self) -> None:
        self.write_suite(path_source_extra="fallback = true")

        with self.assertRaises(EngineError) as raised:
            Verifier(self.root, self.registry)

        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")


if __name__ == "__main__":
    unittest.main()
