from __future__ import annotations

import unittest
import shutil
import tempfile
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    ApplicabilityEvaluator,
    FactDefinition,
    Truth,
    load_router_projection,
)
from tools.standards_metadata.standards_metadata import load_canonical_module_corpus


REPO_ROOT = Path(__file__).resolve().parents[3]


class ApplicabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = ApplicabilityEvaluator(
            (
                FactDefinition("enabled", "boolean"),
                FactDefinition("mode", "enum", values=("a", "b")),
                FactDefinition("tags", "enum-set", values=("x", "y")),
                FactDefinition("optional", "string", nullable=True),
            )
        )

    @staticmethod
    def fact(value_type: str, value: object) -> dict[str, object]:
        return {"type": value_type, "state": "known", "value": value}

    def test_all_supported_operators_use_three_valued_logic(self) -> None:
        facts = self.evaluator.validate_facts(
            {
                "enabled": self.fact("boolean", True),
                "mode": self.fact("enum", "a"),
                "tags": self.fact("enum-set", ["x"]),
                "optional": self.fact("string", None),
            }
        )
        expressions = (
            ({"operator": "equals", "fact": "enabled", "value": True}, Truth.TRUE),
            ({"operator": "in", "fact": "mode", "values": ["a", "b"]}, Truth.TRUE),
            ({"operator": "contains", "fact": "tags", "value": "x"}, Truth.TRUE),
            ({"operator": "exists", "fact": "mode"}, Truth.TRUE),
            ({"operator": "equals", "fact": "optional", "value": None}, Truth.TRUE),
            (
                {
                    "operator": "all",
                    "expressions": [
                        {"operator": "equals", "fact": "enabled", "value": True},
                        {"operator": "contains", "fact": "tags", "value": "y"},
                    ],
                },
                Truth.FALSE,
            ),
            (
                {
                    "operator": "any",
                    "expressions": [
                        {"operator": "contains", "fact": "tags", "value": "y"},
                        {"operator": "equals", "fact": "mode", "value": "a"},
                    ],
                },
                Truth.TRUE,
            ),
            (
                {
                    "operator": "not",
                    "expression": {"operator": "equals", "fact": "enabled", "value": False},
                },
                Truth.TRUE,
            ),
        )
        for expression, expected in expressions:
            with self.subTest(expression=expression):
                self.assertIs(self.evaluator.evaluate(expression, facts), expected)

        unknown = self.evaluator.evaluate(
            {"operator": "equals", "fact": "enabled", "value": True},
            {},
        )
        self.assertIs(unknown, Truth.UNKNOWN)

    def test_invalid_configuration_and_values_reject_instead_of_becoming_unknown(self) -> None:
        invalid = (
            {"operator": "missing", "fact": "enabled"},
            {"operator": "equals", "fact": "undeclared", "value": True},
            {"operator": "contains", "fact": "enabled", "value": True},
        )
        for expression in invalid:
            with self.subTest(expression=expression), self.assertRaises(AnalysisError):
                self.evaluator.evaluate(expression, {})
        with self.assertRaises(AnalysisError):
            self.evaluator.validate_facts(
                {"mode": {"type": "enum", "state": "known", "value": "outside"}}
            )

    def test_repository_router_projection_resolves_registered_modules(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)

        self.assertEqual(projection.owner, "router")
        self.assertEqual(projection.base_modules, ("router",))
        self.assertEqual(len(projection.facts), 7)
        self.assertEqual(len(projection.rules), 38)

    def test_router_projection_rejects_target_drift_from_router_tables(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evaluation/standards-effectiveness").mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "STANDARDS-ROUTER.md", root / "STANDARDS-ROUTER.md")
            projection = root / "evaluation/standards-effectiveness/router-projection.toml"
            shutil.copy2(
                REPO_ROOT / "evaluation/standards-effectiveness/router-projection.toml",
                projection,
            )
            text = projection.read_text(encoding="utf-8")
            marker = '\n[[rules]]\nid = "route.topic.security"'
            projection.write_text(text.split(marker, 1)[0] + "\n", encoding="utf-8")

            with self.assertRaises(AnalysisError) as caught:
                load_router_projection(root, modules)
            self.assertEqual(caught.exception.failure.code, "ROUTER_PROJECTION.INVALID")


if __name__ == "__main__":
    unittest.main()
