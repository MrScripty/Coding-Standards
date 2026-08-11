from __future__ import annotations

import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.numeric_audit import (
    HEADER,
    NumericAuditDiagnostic,
    check_snapshot,
    collect_candidates,
    render_candidates,
    write_snapshot,
)


class NumericAuditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.evaluation = self.root / "evaluation/standards-effectiveness"
        self.evaluation.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_bytes(self, path: str, content: bytes) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target

    def write(self, path: str, content: str) -> Path:
        return self.write_bytes(path, content.encode("utf-8"))

    def checker(self, name: str, content: str) -> str:
        path = f"evaluation/standards-effectiveness/verify-{name}.sh"
        self.write(path, content)
        return path

    def snapshot_path(self) -> Path:
        return self.root / "snapshot.tsv"

    def test_collects_only_comparisons_with_numeric_literals(self) -> None:
        checker = self.checker(
            "owner",
            "#!/usr/bin/env bash\n"
            "[[ \"$count\" -eq 0 ]]\n"
            "awk '$1 == 44 && count > 1 && name == expected' file\n"
            "[[ \"$actual\" == \"expected\" ]]\n",
        )

        candidates = collect_candidates(self.root, (checker,))

        self.assertEqual(len(candidates), 3)
        self.assertEqual(
            [(item.matcher, item.operator, item.numeric_literals) for item in candidates],
            [
                ("shell-numeric", "-eq", ("0",)),
                ("symbolic-numeric", "==", ("44",)),
                ("symbolic-numeric", ">", ("1",)),
            ],
        )

    def test_candidate_identity_ignores_unrelated_line_shifts(self) -> None:
        checker = self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")
        first = collect_candidates(self.root, (checker,))[0]
        self.write(checker, "# inserted\n[[ \"$count\" -eq 0 ]]\n")

        second = collect_candidates(self.root, (checker,))[0]

        self.assertEqual(first.candidate_id, second.candidate_id)
        self.assertNotEqual(first.line, second.line)

    def test_repeated_expression_has_unique_stable_occurrences(self) -> None:
        checker = self.checker(
            "owner",
            "[[ \"$count\" -eq 0 ]]\n[[ \"$count\" -eq 0 ]]\n",
        )

        candidates = collect_candidates(self.root, (checker,))

        self.assertEqual(len({item.candidate_id for item in candidates}), 2)

    def test_render_has_exact_header_and_derived_rows(self) -> None:
        checker = self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")

        content = render_candidates(collect_candidates(self.root, (checker,)))
        rows = list(csv.reader(io.StringIO(content), delimiter="\t"))

        self.assertEqual(tuple(rows[0]), HEADER)
        self.assertEqual(rows[1][1], checker)
        self.assertEqual(rows[1][6], "0")

    def test_write_then_check_is_idempotent(self) -> None:
        self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")
        output = Path("snapshot.tsv")

        self.assertEqual(write_snapshot(self.root, output), 0)
        self.assertEqual(write_snapshot(self.root, output), 0)
        self.assertEqual(check_snapshot(self.root, output), 0)

    def test_write_rejects_changed_existing_baseline(self) -> None:
        checker = self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")
        output = Path("snapshot.tsv")
        self.assertEqual(write_snapshot(self.root, output), 0)
        self.write(checker, "[[ \"$count\" -eq 1 ]]\n")

        self.assertEqual(write_snapshot(self.root, output), 2)

    def test_check_reports_missing_snapshot_as_unavailable(self) -> None:
        self.assertEqual(check_snapshot(self.root, Path("missing.tsv")), 3)

    def test_check_rejects_malformed_header(self) -> None:
        self.write("snapshot.tsv", "wrong\theader\n")

        self.assertEqual(check_snapshot(self.root, Path("snapshot.tsv")), 2)

    def test_check_rejects_duplicate_candidate_identity(self) -> None:
        checker = self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")
        content = render_candidates(collect_candidates(self.root, (checker,)))
        rows = content.splitlines()
        self.write("snapshot.tsv", "\n".join((rows[0], rows[1], rows[1])) + "\n")

        self.assertEqual(check_snapshot(self.root, Path("snapshot.tsv")), 2)

    def test_collect_rejects_duplicate_checker_scope(self) -> None:
        checker = self.checker("owner", "[[ \"$count\" -eq 0 ]]\n")

        with self.assertRaises(NumericAuditDiagnostic) as context:
            collect_candidates(self.root, (checker, checker))

        self.assertEqual(context.exception.code, "NUMERIC_AUDIT.DUPLICATE_CHECKER")

    def test_collect_reports_missing_source_as_unavailable(self) -> None:
        with self.assertRaises(NumericAuditDiagnostic) as context:
            collect_candidates(self.root, ("missing.sh",))

        self.assertEqual(context.exception.outcome, "unavailable")
        self.assertEqual(context.exception.exit_code, 3)

    def test_collect_rejects_invalid_utf8(self) -> None:
        checker = "evaluation/standards-effectiveness/verify-owner.sh"
        self.write_bytes(checker, b"[[ \"$count\" -eq 0 ]]\n\xff")

        with self.assertRaises(NumericAuditDiagnostic) as context:
            collect_candidates(self.root, (checker,))

        self.assertEqual(context.exception.code, "NUMERIC_AUDIT.INVALID_UTF8")

    def test_collect_rejects_symlink_escape(self) -> None:
        outside = Path(self.temp_dir.name).parent / "outside-numeric-audit.sh"
        outside.write_text("[[ \"$count\" -eq 0 ]]\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        checker = self.evaluation / "verify-owner.sh"
        checker.symlink_to(outside)

        with self.assertRaises(NumericAuditDiagnostic) as context:
            collect_candidates(
                self.root,
                ("evaluation/standards-effectiveness/verify-owner.sh",),
            )

        self.assertEqual(
            context.exception.code,
            "NUMERIC_AUDIT.PATH.OUTSIDE_REPOSITORY",
        )

    def test_snapshot_path_rejects_parent_escape(self) -> None:
        self.assertEqual(write_snapshot(self.root, Path("../snapshot.tsv")), 2)
        self.assertEqual(check_snapshot(self.root, Path("../snapshot.tsv")), 2)


if __name__ == "__main__":
    unittest.main()
