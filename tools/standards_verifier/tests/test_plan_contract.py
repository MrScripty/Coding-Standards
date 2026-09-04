from __future__ import annotations

import sys
import unittest
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.checks.plan_contract import (  # noqa: E402
    parse_plan_contract_check,
    validate_plan,
)
from standards_verifier.diagnostics import EngineError  # noqa: E402


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPOSITORY_ROOT / "evaluation/standards-effectiveness/fixtures/plans"


class PlanContractTest(unittest.TestCase):
    def test_valid_fixtures_pass(self) -> None:
        for path in sorted(FIXTURES.glob("valid-*.md")):
            with self.subTest(path=path.name):
                self.assertIsNone(validate_plan(path.read_text(encoding="utf-8")))

    def test_invalid_fixtures_preserve_diagnostics(self) -> None:
        expected = {
            "invalid-accepted-malformed-objective-status.md": "objective A1 has invalid status satified",
            "invalid-accepted-missing-final-projections.md": "accepted plan requires both final acceptance projections",
            "invalid-accepted-pending-criterion.md": "accepted plan has unsatisfied objective A1",
            "invalid-accepted-satisfied-without-evidence.md": "satisfied objective A1 requires evidence",
            "invalid-duplicate-composed-design-probe.md": "applicable composed-design review requires Independent concepts and dimensions",
            "invalid-execution-history.md": "execution history belongs in the ledger",
            "invalid-headless-accepted.md": "accepted plan has partial acceptance",
            "invalid-incomplete-composed-design-review.md": "applicable composed-design review requires Deletion and cumulative machinery result",
            "invalid-missing-composed-design-applicability.md": "expected one ## Simplicity And Ownership Review heading",
            "invalid-missing-next.md": "expected one Next slice field",
            "invalid-objective-partial.md": "objective A1 has invalid status partial",
            "invalid-three-state.md": "invalid plan status Complete",
            "invalid-unreasoned-composed-design-exclusion.md": "not-applicable composed-design review requires a concrete Reason",
            "invalid-whitespace-composed-design-probe.md": "applicable composed-design review requires Deletion and cumulative machinery result",
            "invalid-whitespace-composed-design-reason.md": "not-applicable composed-design review requires a concrete Reason",
        }
        self.assertEqual(
            {path.name for path in FIXTURES.glob("invalid-*.md")},
            set(expected),
        )
        for name, message in expected.items():
            with self.subTest(path=name):
                content = (FIXTURES / name).read_text(encoding="utf-8")
                self.assertEqual(validate_plan(content), message)

    def test_parser_rejects_unknown_and_contradictory_configuration(self) -> None:
        with self.assertRaises(EngineError):
            parse_plan_contract_check(
                {
                    "id": "plan",
                    "type": "plan_contract",
                    "path": "plan.md",
                    "expected": "valid",
                    "unknown": True,
                },
                "suite",
            )
        with self.assertRaises(EngineError):
            parse_plan_contract_check(
                {
                    "id": "plan",
                    "type": "plan_contract",
                    "path": "plan.md",
                    "expected": "valid",
                    "message": "must fail",
                },
                "suite",
            )


if __name__ == "__main__":
    unittest.main()
