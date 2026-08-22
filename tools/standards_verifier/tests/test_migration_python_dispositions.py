from __future__ import annotations

import csv
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.engine import Verifier


HEADER = (
    "subject_kind",
    "subject",
    "path",
    "disposition",
    "current_consumer",
    "post_zero_consumer",
    "terminal_trigger",
    "evidence_owner",
    "rationale",
)


class MigrationPythonDispositionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write(
            "package/worker.py",
            'MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"\n',
        )
        self.write(
            "package/check.py",
            'MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"\n'
            'MIGRATION_CHECK_KINDS = ("temporary_check",)\n',
        )
        self.write_rows(
            [
                HEADER,
                self.row("module", "standards_verifier.worker", "package/worker.py"),
                self.row("module", "standards_verifier.check", "package/check.py"),
                self.row("check-kind", "temporary_check", "package/check.py"),
            ]
        )
        self.write(
            "suite.toml",
            """
            schema_version = 1
            id = "migration"
            owner = "test.migration"
            description = "Migration Python dispositions fixture"

            [[checks]]
            id = "dispositions"
            type = "migration_python_dispositions"
            path = "dispositions.tsv"
            package_path = "package"
            terminal_trigger = "zero-bash-accepted"
            """,
        )
        self.write(
            "registry.toml",
            "schema_version = 1\n\n"
            "[[suites]]\n"
            'id = "migration"\n'
            'path = "suite.toml"\n'
            "requires = []\n",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    @staticmethod
    def row(kind: str, subject: str, path: str) -> tuple[str, ...]:
        return (
            kind,
            subject,
            path,
            "delete",
            "current",
            "none",
            "zero-bash-accepted",
            "owner",
            "temporary candidate",
        )

    def write_rows(self, rows) -> None:
        with (self.root / "dispositions.tsv").open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)

    def rows(self):
        with (self.root / "dispositions.tsv").open("r", encoding="utf-8", newline="") as handle:
            return list(csv.reader(handle, delimiter="\t"))

    def result(self):
        return Verifier(self.root, "registry.toml").run(("migration",))[0]

    def test_declared_candidates_match_dispositions(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_deleting_module_disposition_fails(self) -> None:
        rows = [row for row in self.rows() if row[1] != "standards_verifier.worker"]
        self.write_rows(rows)
        self.assertIn(
            "ASSERT.MIGRATION_PYTHON_DISPOSITION",
            [item.code for item in self.result().diagnostics],
        )

    def test_deleting_check_kind_disposition_fails(self) -> None:
        rows = [row for row in self.rows() if row[1] != "temporary_check"]
        self.write_rows(rows)
        self.assertIn(
            "ASSERT.MIGRATION_PYTHON_DISPOSITION",
            [item.code for item in self.result().diagnostics],
        )

    def test_undeclared_disposition_fails(self) -> None:
        rows = self.rows()
        rows.append(list(self.row("module", "standards_verifier.stale", "package/stale.py")))
        self.write_rows(rows)
        self.assertIn(
            "ASSERT.MIGRATION_PYTHON_CANDIDATE",
            [item.code for item in self.result().diagnostics],
        )

    def test_candidate_path_mismatch_fails(self) -> None:
        rows = self.rows()
        rows[1][2] = "package/other.py"
        self.write_rows(rows)
        self.assertIn(
            "ASSERT.MIGRATION_PYTHON_PATH",
            [item.code for item in self.result().diagnostics],
        )


if __name__ == "__main__":
    unittest.main()
