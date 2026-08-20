from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.numeric_audit import collect_candidates, render_candidates
from standards_verifier.numeric_retirements import (
    BASELINE_PATH,
    PACKAGES_HEADER,
    PACKAGES_PATH,
    RETIREMENTS_HEADER,
    RETIREMENTS_PATH,
    check_retirements,
    record_retirements,
)


class NumericRetirementsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.checker = "evaluation/standards-effectiveness/verify-owner.sh"
        self.write(self.checker, '[[ "$count" -eq 0 ]]\n')
        candidates = collect_candidates(self.root, (self.checker,))
        self.candidate_id = candidates[0].candidate_id
        self.write(BASELINE_PATH.as_posix(), render_candidates(candidates))
        self.write_packages("admitted")
        self.write(RETIREMENTS_PATH.as_posix(), "\t".join(RETIREMENTS_HEADER) + "\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def write_packages(self, state: str) -> None:
        row = ("R1", "test.owner", "obsolete-comparison-removed", state)
        self.write(
            PACKAGES_PATH.as_posix(),
            "\t".join(PACKAGES_HEADER) + "\n" + "\t".join(row) + "\n",
        )

    def remove_candidate(self) -> None:
        self.write(self.checker, "printf 'still live\\n'\n")

    def retirement_rows(self) -> list[list[str]]:
        with (self.root / RETIREMENTS_PATH).open(encoding="utf-8") as source:
            return list(csv.reader(source, delimiter="\t"))

    def test_records_exact_derived_identity_for_admitted_package(self) -> None:
        self.remove_candidate()

        self.assertEqual(record_retirements(self.root, "R1"), 0)

        self.assertEqual(
            self.retirement_rows(),
            [list(RETIREMENTS_HEADER), [self.candidate_id, "R1"]],
        )

    def test_recording_is_idempotent(self) -> None:
        self.remove_candidate()

        self.assertEqual(record_retirements(self.root, "R1"), 0)
        self.assertEqual(record_retirements(self.root, "R1"), 0)

        self.assertEqual(len(self.retirement_rows()), 2)

    def test_new_identity_cannot_join_accepted_package(self) -> None:
        self.remove_candidate()
        self.write_packages("accepted")

        self.assertEqual(record_retirements(self.root, "R1"), 2)

    def test_unknown_package_is_unavailable(self) -> None:
        self.remove_candidate()

        self.assertEqual(record_retirements(self.root, "missing"), 3)

    def test_check_requires_exact_missing_live_coverage(self) -> None:
        self.remove_candidate()

        self.assertEqual(check_retirements(self.root), 2)

    def test_check_accepts_generated_identity_after_package_acceptance(self) -> None:
        self.remove_candidate()
        self.assertEqual(record_retirements(self.root, "R1"), 0)
        self.write_packages("accepted")

        self.assertEqual(check_retirements(self.root), 0)

    def test_check_rejects_retirement_for_present_candidate(self) -> None:
        self.write(
            RETIREMENTS_PATH.as_posix(),
            "\t".join(RETIREMENTS_HEADER)
            + "\n"
            + f"{self.candidate_id}\tR1\n",
        )
        self.write_packages("accepted")

        self.assertEqual(check_retirements(self.root), 2)


if __name__ == "__main__":
    unittest.main()
