from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_applicability.standards_applicability import (
    SUPPORTED_FACT_STATES,
    SUPPORTED_FACT_TYPES,
    SUPPORTED_OPERATORS,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


class ApplicabilityContractTest(unittest.TestCase):
    def test_runtime_domains_cover_the_public_serialized_applicability_shapes(
        self,
    ) -> None:
        definitions = json.loads(
            (
                REPO_ROOT
                / "tools/standards_engine/contracts/a1-contract.schema.json"
            ).read_text(encoding="utf-8")
        )["$defs"]
        operators = {
            definitions[item["$ref"].rsplit("/", 1)[1]]["properties"]["operator"][
                "const"
            ]
            for item in definitions["ApplicabilityExpression"]["oneOf"]
        }
        fact_types: set[str] = set()
        fact_states: set[str] = set()
        for variant in definitions["FactValue"]["oneOf"]:
            type_contract = variant["properties"]["type"]
            state_contract = variant["properties"]["state"]
            fact_types.update(type_contract.get("enum", ()))
            if "const" in type_contract:
                fact_types.add(type_contract["const"])
            fact_states.update(state_contract.get("enum", ()))
            if "const" in state_contract:
                fact_states.add(state_contract["const"])

        self.assertEqual(operators, set(SUPPORTED_OPERATORS))
        self.assertEqual(fact_types, set(SUPPORTED_FACT_TYPES))
        self.assertEqual(fact_states, set(SUPPORTED_FACT_STATES))
        self.assertIn("PolicyRelationshipInspection", definitions)
        for internal_definition in (
            "FactDeclaration",
            "ApplicabilityFactSchema",
            "ApplicabilityEvaluationResult",
            "PolicyImpactDeclaration",
            "CompiledPolicyImpactSemantics",
            "CompiledApplicabilityProgram",
        ):
            self.assertNotIn(internal_definition, definitions)

    def test_former_applicability_implementations_are_not_fallbacks(self) -> None:
        self.assertFalse(
            (
                REPO_ROOT
                / "tools/standards_analysis/standards_analysis/applicability.py"
            ).exists()
        )
        compiler = (
            REPO_ROOT
            / "tools/standards_policy_impact/standards_policy_impact/compiler.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("def _applicability(", compiler)
        self.assertNotIn("standards_analysis", compiler)


if __name__ == "__main__":
    unittest.main()
