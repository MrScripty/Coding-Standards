from __future__ import annotations

import unittest

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    ConsumerReviewObligationCause,
    DependencyCause,
    ReadingSelection,
    ReviewScope,
    RoutingBaseCause,
    RoutingRuleCause,
    compile_reading_plan,
    consumer_reading_selections,
)
from tools.standards_analysis.standards_analysis.obligations import (
    DecisionContract,
    DecisionDependency,
    DecisionFingerprint,
    Obligation,
)


WHOLE = ReviewScope("whole-artifact")
STRUCTURED = ReviewScope("structured", ("Selected",))


def authority(_target: str) -> str:
    return "projection"


def obligation(identifier: str, *, scope: ReviewScope = WHOLE) -> Obligation:
    contract = DecisionContract("decision-contract.consumer.v1", 1, ("policy-unit",))
    return Obligation(
        f"obligation:sha256:{identifier * 64}",
        "consumer-review",
        "prompt.consumer",
        scope,
        ({"kind": "policy-impact-edge"},),
        "required",
        ("consumer-disposition",),
        DecisionFingerprint(
            "consumer-review",
            contract.id,
            (
                DecisionDependency(
                    "policy-unit",
                    "workflow.test.policy",
                    f"sha256:{identifier * 64}",
                ),
            ),
        ),
        "true",
    )


class ReadingPlanCompilerTest(unittest.TestCase):
    def test_compatible_obligations_collapse_to_plural_references(self) -> None:
        first = obligation("a")
        second = obligation("b")
        left = compile_reading_plan(
            consumer_reading_selections((first, second, first)),
            authority,
        )
        right = compile_reading_plan(
            consumer_reading_selections((second, first)),
            authority,
        )

        self.assertEqual(left, right)
        self.assertEqual(len(left), 1)
        self.assertEqual(
            left[0].as_contract()["reasons"],
            [
                {
                    "kind": "consumer-review-obligation",
                    "obligation": first.id,
                },
                {
                    "kind": "consumer-review-obligation",
                    "obligation": second.id,
                },
            ],
        )

    def test_exact_scope_and_state_rules_are_mechanical(self) -> None:
        plan = compile_reading_plan(
            (
                ReadingSelection(
                    "prompt.consumer",
                    WHOLE,
                    RoutingRuleCause("router.rule", ("fact.b", "fact.a")),
                    "unresolved",
                    2,
                ),
                ReadingSelection(
                    "prompt.consumer",
                    WHOLE,
                    RoutingBaseCause("router.projection"),
                    "selected",
                    2,
                ),
                ReadingSelection(
                    "prompt.consumer",
                    STRUCTURED,
                    ConsumerReviewObligationCause(
                        "obligation:sha256:" + "c" * 64
                    ),
                    "conditional",
                    3,
                ),
            ),
            authority,
        )

        self.assertEqual(len(plan), 2)
        whole = next(item for item in plan if item.scope == WHOLE)
        self.assertEqual(whole.state, "selected")
        routing_rule = next(
            reason
            for reason in whole.as_contract()["reasons"]
            if reason["kind"] == "routing-rule"
        )
        self.assertEqual(
            routing_rule["facts"],
            ["fact.a", "fact.b"],
        )
        structured = next(item for item in plan if item.scope == STRUCTURED)
        self.assertEqual(structured.state, "conditional")

    def test_every_dependency_edge_and_direct_cause_is_retained(self) -> None:
        plan = compile_reading_plan(
            (
                ReadingSelection(
                    "core",
                    WHOLE,
                    DependencyCause("requires", "edge.parent-a", "parent.a"),
                    "selected",
                    1,
                ),
                ReadingSelection(
                    "core",
                    WHOLE,
                    DependencyCause("requires", "edge.parent-b", "parent.b"),
                    "selected",
                    1,
                ),
                ReadingSelection(
                    "core",
                    WHOLE,
                    RoutingRuleCause("router.core", ("routing.fact",)),
                    "selected",
                    2,
                ),
            ),
            lambda _target: "normative",
        )

        self.assertEqual(
            {reason["kind"] for reason in plan[0].as_contract()["reasons"]},
            {"requires", "routing-rule"},
        )
        self.assertEqual(len(plan[0].reasons), 3)

    def test_cause_changes_change_projection_and_missing_authority_rejects(self) -> None:
        base = (
            ReadingSelection(
                "core",
                WHOLE,
                RoutingBaseCause("router.projection"),
                "selected",
                0,
            ),
        )
        first = compile_reading_plan(base, lambda _target: "normative")
        second = compile_reading_plan(
            (
                *base,
                ReadingSelection(
                    "core",
                    WHOLE,
                    DependencyCause("requires", "edge.extra", "workflow.extra"),
                    "selected",
                    1,
                ),
            ),
            lambda _target: "normative",
        )
        self.assertNotEqual(first, second)

        with self.assertRaises(AnalysisError) as caught:
            compile_reading_plan(base, lambda _target: "")
        self.assertEqual(caught.exception.failure.code, "READING_PLAN.AUTHORITY")

    def test_entry_rejects_noncanonical_or_duplicate_causes(self) -> None:
        from tools.standards_analysis.standards_analysis import ReadingPlanEntry

        reasons = (
            {"kind": "routing-base", "projection": "z"},
            {"kind": "routing-base", "projection": "a"},
        )
        with self.assertRaises(AnalysisError) as caught:
            ReadingPlanEntry("core", WHOLE, "normative", reasons, "selected")
        self.assertEqual(caught.exception.failure.code, "READING_PLAN.REASONS")


if __name__ == "__main__":
    unittest.main()
