from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_applicability.standards_applicability import (
    LANGUAGE_VERSION,
    SUPPORTED_FACT_STATES,
    SUPPORTED_FACT_TYPES,
    SUPPORTED_OPERATORS,
    Truth,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


class ApplicabilityContractTest(unittest.TestCase):
    def test_runtime_semantics_exactly_cover_canonical_serialized_domains(self) -> None:
        schema = json.loads(
            (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json")
            .read_text(encoding="utf-8")
        )
        definitions = schema["$defs"]
        expression_refs = definitions["ApplicabilityExpression"]["oneOf"]
        operators = {
            definitions[item["$ref"].rsplit("/", 1)[1]]["properties"]["operator"][
                "const"
            ]
            for item in expression_refs
        }
        fact_types = set(definitions["FactDeclaration"]["properties"]["type"]["enum"])
        states = set(
            definitions["FactValue"]["oneOf"][-1]["properties"]["state"]["enum"]
        ) | {"known"}
        truths = set(
            definitions["ApplicabilityEvaluationResult"]["properties"]["truth"][
                "enum"
            ]
        )

        self.assertEqual(operators, set(SUPPORTED_OPERATORS))
        self.assertEqual(fact_types, set(SUPPORTED_FACT_TYPES))
        self.assertEqual(states, set(SUPPORTED_FACT_STATES))
        self.assertEqual(truths, {item.value for item in Truth})
        self.assertEqual(
            definitions["CompiledApplicabilityProgram"]["properties"][
                "language_version"
            ]["const"],
            LANGUAGE_VERSION,
        )
        self.assertNotIn(
            "minItems",
            definitions["ApplicabilityFactSchema"]["properties"]["facts"],
        )

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
