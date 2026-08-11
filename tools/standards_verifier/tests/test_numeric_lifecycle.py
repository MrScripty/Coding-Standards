from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.checks.numeric_lifecycle import PACKAGES_HEADER
from standards_verifier.diagnostics import EngineError
from standards_verifier.engine import Verifier
from standards_verifier.numeric_audit import HEADER, collect_candidates, render_candidates


class NumericLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.checker = "evaluation/standards-effectiveness/verify-owner.sh"
        self.baseline = "generated/numeric-comparison-candidates.tsv"
        self.decisions = "numeric-comparison-decisions.tsv"
        self.packages = "checker-migration-packages.tsv"
        self.write(self.checker, '[[ "$count" -eq 0 ]]\n')
        self.freeze_baseline()
        self.write_packages([])
        self.write_suite()
        self.write_registry()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def freeze_baseline(self) -> None:
        candidates = collect_candidates(self.root, (self.checker,))
        self.write(self.baseline, render_candidates(candidates))
        decisions = ["candidate_id\tsemantic_class"]
        decisions.extend(
            f"{candidate.candidate_id}\tstructural-multiplicity"
            for candidate in candidates
        )
        self.write(self.decisions, "\n".join(decisions) + "\n")

    def package_row(
        self,
        number: int,
        *,
        state: str = "accepted",
        owner: str = "topics/example.md",
    ) -> tuple[str, ...]:
        return (
            str(number),
            f"P{number}",
            f"checker:{self.checker}",
            owner,
            "consolidation",
            "checker-retired",
            "-",
            "-",
            "focused",
            state,
        )

    def write_packages(self, rows: list[tuple[str, ...]]) -> None:
        lines = ["\t".join(PACKAGES_HEADER)]
        lines.extend("\t".join(row) for row in rows)
        self.write(self.packages, "\n".join(lines) + "\n")

    def write_suite(self, *, extra: str = "") -> None:
        self.write(
            "suites/numeric.toml",
            f"""
            schema_version = 1
            id = "numeric"
            owner = "test.owner"
            description = "Numeric lifecycle test"

            [[checks]]
            id = "lifecycle"
            type = "numeric_audit_lifecycle"
            baseline_path = "{self.baseline}"
            decisions_path = "{self.decisions}"
            packages_path = "{self.packages}"
            {extra}
            """,
        )

    def write_registry(self) -> None:
        self.write(
            "registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "numeric"
            path = "suites/numeric.toml"
            requires = []
            """,
        )

    def result(self):
        return Verifier(self.root, "registry.toml").run()[0]

    def retire_checker(self) -> None:
        (self.root / self.checker).unlink()

    def test_unchanged_current_candidates_pass_without_package(self) -> None:
        self.assertEqual(self.result().status, "passed")

    def test_accepted_package_authorizes_retired_checker(self) -> None:
        self.retire_checker()
        self.write_packages([self.package_row(1)])

        self.assertEqual(self.result().status, "passed")

    def test_new_candidate_is_invalid(self) -> None:
        self.write(self.checker, '[[ "$count" -eq 1 ]]\n')

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "ASSERT.NUMERIC_LIFECYCLE_NEW_CANDIDATE"
        )
        self.assertEqual(diagnostic.outcome, "invalid")

    def test_unexplained_retirement_is_unavailable(self) -> None:
        self.retire_checker()

        result = self.result()
        self.assertEqual(
            result.diagnostics[0].code, "NUMERIC_LIFECYCLE.PACKAGE_UNAVAILABLE"
        )
        self.assertEqual(result.diagnostics[0].outcome, "unavailable")
        self.assertEqual(result.exit_code, 3)

    def test_candidate_removal_while_checker_is_live_is_invalid(self) -> None:
        self.write(self.checker, "printf 'still live\\n'\n")
        self.write_packages([self.package_row(1)])

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "ASSERT.NUMERIC_LIFECYCLE_CHECKER_STILL_LIVE"
        )

    def test_ambiguous_package_is_invalid(self) -> None:
        self.retire_checker()
        self.write_packages([self.package_row(1), self.package_row(2)])

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "ASSERT.NUMERIC_LIFECYCLE_AMBIGUOUS_PACKAGE"
        )

    def test_non_accepted_package_is_invalid(self) -> None:
        self.retire_checker()
        self.write_packages([self.package_row(1, state="admitted")])

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "ASSERT.NUMERIC_LIFECYCLE_PACKAGE_STATE"
        )

    def test_empty_package_owner_is_unavailable(self) -> None:
        self.retire_checker()
        self.write_packages([self.package_row(1, owner="")])

        result = self.result()
        self.assertEqual(
            result.diagnostics[0].code, "NUMERIC_LIFECYCLE.OWNER_UNAVAILABLE"
        )
        self.assertEqual(result.exit_code, 3)

    def test_decisions_must_cover_exact_baseline_identities(self) -> None:
        self.write(self.decisions, "candidate_id\tsemantic_class\n")

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "ASSERT.NUMERIC_LIFECYCLE_DECISIONS"
        )

    def test_package_header_is_exact(self) -> None:
        self.write(self.packages, "subject\towner\n")

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(diagnostic.code, "TABLE.HEADER_CONTRACT")

    def test_unknown_configuration_field_is_invalid(self) -> None:
        self.write_suite(extra='unexpected = "value"')

        with self.assertRaises(EngineError) as raised:
            self.result()
        self.assertEqual(raised.exception.diagnostic.code, "CONFIG.UNKNOWN_FIELD")

    def test_baseline_checker_parent_traversal_is_invalid(self) -> None:
        baseline = (self.root / self.baseline).read_text(encoding="utf-8")
        self.write(self.baseline, baseline.replace(self.checker, "../verify-owner.sh"))

        diagnostic = self.result().diagnostics[0]
        self.assertEqual(
            diagnostic.code, "NUMERIC_LIFECYCLE.INVALID_CHECKER_PATH"
        )


if __name__ == "__main__":
    unittest.main()
