from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.engine import Verifier
from standards_verifier.model import SuiteResult


SUITE_ID = "checker-migration-packages"
SUITE_PATH = "evaluation/standards-effectiveness/suites/checker-migration-packages.toml"
MANIFEST_PATH = "evaluation/standards-effectiveness/checker-migration-packages.tsv"
DISPOSITIONS_PATH = "evaluation/standards-effectiveness/migration-python-dispositions.tsv"


class PackageManifestContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._copy(SUITE_PATH)
        self._copy(MANIFEST_PATH)
        self._copy(DISPOSITIONS_PATH)
        shutil.copytree(
            REPOSITORY_ROOT / "tools/standards_verifier/standards_verifier",
            self.root / "tools/standards_verifier/standards_verifier",
        )
        (self.root / "registry.toml").write_text(
            "schema_version = 1\n\n"
            "[[suites]]\n"
            f'id = "{SUITE_ID}"\n'
            f'path = "{SUITE_PATH}"\n'
            "requires = []\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _copy(self, relative_path: str) -> None:
        destination = self.root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY_ROOT / relative_path, destination)

    def _rows(self, path: str = MANIFEST_PATH) -> list[list[str]]:
        with (self.root / path).open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            return list(csv.reader(handle, delimiter="\t"))

    def _write_rows(self, rows: list[list[str]], path: str = MANIFEST_PATH) -> None:
        with (self.root / path).open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)

    def _result(self) -> SuiteResult:
        return Verifier(self.root, "registry.toml").run((SUITE_ID,))[0]

    def _assert_mutation(
        self,
        mutate: Callable[[list[list[str]]], None],
        code: str,
        path: str = MANIFEST_PATH,
    ) -> None:
        rows = self._rows(path)
        mutate(rows)
        self._write_rows(rows, path)

        result = self._result()

        self.assertEqual(result.status, "failed")
        self.assertIn(code, [diagnostic.code for diagnostic in result.diagnostics])

    def test_canonical_manifest_passes(self) -> None:
        self.assertEqual(self._result().status, "passed")

    def test_header_mutation_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[0].__setitem__(0, "sequence"),
            "TABLE.HEADER_CONTRACT",
        )

    def test_empty_required_value_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(3, ""),
            "ASSERT.TABLE_EMPTY_VALUE",
        )

    def test_unknown_risk_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(4, "unknown"),
            "ASSERT.TABLE_DOMAIN",
        )

    def test_unknown_state_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(9, "unknown"),
            "ASSERT.TABLE_DOMAIN",
        )

    def test_duplicate_train_order_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[2].__setitem__(0, rows[1][0]),
            "ASSERT.TABLE_DUPLICATE_KEY",
        )

    def test_duplicate_package_id_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[2].__setitem__(1, rows[1][1]),
            "ASSERT.TABLE_DUPLICATE_KEY",
        )

    def test_duplicate_subject_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[2].__setitem__(2, rows[1][2]),
            "ASSERT.TABLE_DUPLICATE_KEY",
        )

    def test_unknown_terminal_disposition_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(3, "postpone"),
            "ASSERT.TABLE_DOMAIN",
            DISPOSITIONS_PATH,
        )

    def test_empty_terminal_consumer_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(4, ""),
            "ASSERT.TABLE_EMPTY_VALUE",
            DISPOSITIONS_PATH,
        )

    def test_duplicate_terminal_subject_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[2].__setitem__(1, rows[1][1]),
            "ASSERT.TABLE_DUPLICATE_KEY",
            DISPOSITIONS_PATH,
        )

    def test_unknown_terminal_trigger_is_rejected(self) -> None:
        self._assert_mutation(
            lambda rows: rows[1].__setitem__(6, "eventually"),
            "ASSERT.TABLE_DOMAIN",
            DISPOSITIONS_PATH,
        )


if __name__ == "__main__":
    unittest.main()
