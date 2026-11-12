from __future__ import annotations

import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    RouteDecision,
    load_router_projection,
)
from tools.standards_metadata.standards_metadata import load_canonical_module_corpus


REPO_ROOT = Path(__file__).resolve().parents[3]


class RouteDecisionTest(unittest.TestCase):
    """The repository Router decides a route in one place for every caller."""

    @classmethod
    def setUpClass(cls) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        cls.router = load_router_projection(REPO_ROOT, modules)

    def decide(self, **facts: object) -> RouteDecision:
        values: dict[str, object] = {}
        for definition in self.router.facts:
            value = facts.get(definition.id.removeprefix("routing."), [])
            values[definition.id] = (
                {"type": definition.type, "state": "unknown"}
                if value is None
                else {"type": definition.type, "state": "known", "value": value}
            )
        return self.router.decide(self.router.fact_schema.bind(values))

    def test_base_modules_come_first_and_true_rules_follow_in_rule_order(self) -> None:
        decision = self.decide(
            activities=["verification", "implementation"], boundaries=["generated-contract"]
        )

        self.assertEqual(decision.selected[:1], self.router.base_modules)
        self.assertEqual(
            sorted(decision.selected[1:]),
            [
                "profile.boundary.generated-contract",
                "topic.contracts.schemas",
                "workflow.implementation",
                "workflow.verification",
            ],
        )
        self.assertEqual(decision.unresolved_facts, ())
        self.assertEqual(decision.unresolved_targets, ())
        self.assertEqual(
            [(rule.target, state) for rule, state in decision.rule_states],
            [(target, "selected") for target in decision.selected[1:]],
        )

    def test_no_known_fact_selects_only_the_base(self) -> None:
        decision = self.decide()

        self.assertEqual(decision.selected, self.router.base_modules)
        self.assertEqual(decision.rule_states, ())

    def test_an_unknown_fact_leaves_its_rules_unresolved(self) -> None:
        decision = self.decide(activities=["implementation"], topics=None)

        self.assertEqual(decision.selected, ("router", "workflow.implementation"))
        self.assertEqual(decision.unresolved_facts, ("routing.topics",))
        self.assertIn("topic.architecture", decision.unresolved_targets)
        self.assertIn("topic.code-design", decision.unresolved_targets)
        self.assertNotIn("workflow.verification", decision.unresolved_targets)
        self.assertFalse(set(decision.selected) & set(decision.unresolved_targets))


if __name__ == "__main__":
    unittest.main()
