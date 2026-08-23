from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    Truth,
    compile_fact_schema,
)


def declaration(facts: list[dict[str, object]] | None = None) -> dict[str, object]:
    return {
        "kind": "applicability-fact-schema",
        "id": "test.applicability",
        "version": 1,
        "facts": facts or [],
    }


class ApplicabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = compile_fact_schema(
            declaration(
                [
                    {
                        "id": "enabled",
                        "type": "boolean",
                        "nullable": False,
                        "aliases": ["on"],
                    },
                    {
                        "id": "mode",
                        "type": "enum",
                        "nullable": False,
                        "values": ["a", "b"],
                        "aliases": [],
                    },
                    {
                        "id": "tags",
                        "type": "enum-set",
                        "nullable": False,
                        "values": ["x", "y"],
                        "aliases": [],
                    },
                    {
                        "id": "optional",
                        "type": "string",
                        "nullable": True,
                        "aliases": [],
                    },
                ]
            )
        )

    @staticmethod
    def known(value_type: str, value: object) -> dict[str, object]:
        return {"type": value_type, "state": "known", "value": value}

    def test_empty_schema_compiles_fact_free_always(self) -> None:
        schema = compile_fact_schema(declaration())
        program = schema.compile({"operator": "always"})

        self.assertEqual(program.referenced_facts, ())
        self.assertIs(program.evaluate(schema.bind({})).truth, Truth.TRUE)

    def test_every_operator_and_fact_state_uses_three_valued_logic(self) -> None:
        facts = self.schema.bind(
            {
                "on": self.known("boolean", True),
                "mode": self.known("enum", "a"),
                "tags": self.known("enum-set", ["x"]),
                "optional": self.known("string", None),
            }
        )
        cases = (
            ({"operator": "equals", "fact": "enabled", "value": True}, Truth.TRUE),
            ({"operator": "in", "fact": "mode", "values": ["b", "a"]}, Truth.TRUE),
            ({"operator": "contains", "fact": "tags", "value": "x"}, Truth.TRUE),
            ({"operator": "exists", "fact": "optional"}, Truth.TRUE),
            (
                {
                    "operator": "not",
                    "expression": {
                        "operator": "equals",
                        "fact": "mode",
                        "value": "b",
                    },
                },
                Truth.TRUE,
            ),
        )
        for expression, truth in cases:
            with self.subTest(expression=expression):
                self.assertIs(self.schema.compile(expression).evaluate(facts).truth, truth)

        absent = self.schema.bind(
            {"mode": {"type": "enum", "state": "known-absent"}}
        )
        unknown = self.schema.bind({"mode": {"type": "enum", "state": "unknown"}})
        exists = self.schema.compile({"operator": "exists", "fact": "mode"})
        self.assertIs(exists.evaluate(absent).truth, Truth.FALSE)
        self.assertEqual(exists.evaluate(unknown).unresolved_facts, ("mode",))

    def test_unknown_facts_are_reported_only_when_material(self) -> None:
        unknown_enabled = {
            "operator": "equals",
            "fact": "enabled",
            "value": True,
        }
        false_mode = {"operator": "equals", "fact": "mode", "value": "b"}
        facts = self.schema.bind({"mode": self.known("enum", "a")})

        all_result = self.schema.compile(
            {"operator": "all", "expressions": [unknown_enabled, false_mode]}
        ).evaluate(facts)
        any_result = self.schema.compile(
            {"operator": "any", "expressions": [unknown_enabled, false_mode]}
        ).evaluate(facts)

        self.assertIs(all_result.truth, Truth.FALSE)
        self.assertEqual(all_result.unresolved_facts, ())
        self.assertIs(any_result.truth, Truth.UNKNOWN)
        self.assertEqual(any_result.unresolved_facts, ("enabled",))

    def test_aliases_normalize_and_conflicting_inputs_reject(self) -> None:
        program = self.schema.compile(
            {"operator": "equals", "fact": "on", "value": True}
        )
        self.assertEqual(program.as_expression()["fact"], "enabled")
        with self.assertRaises(ApplicabilityError):
            self.schema.bind(
                {
                    "enabled": self.known("boolean", True),
                    "on": self.known("boolean", True),
                }
            )

    def test_schema_and_program_digests_are_stable_and_schema_bound(self) -> None:
        repeated = compile_fact_schema(
            declaration(
                [
                    {
                        "id": "optional",
                        "type": "string",
                        "nullable": True,
                        "aliases": [],
                    },
                    {
                        "id": "tags",
                        "type": "enum-set",
                        "nullable": False,
                        "values": ["y", "x"],
                        "aliases": [],
                    },
                    {
                        "id": "mode",
                        "type": "enum",
                        "nullable": False,
                        "values": ["b", "a"],
                        "aliases": [],
                    },
                    {
                        "id": "enabled",
                        "type": "boolean",
                        "nullable": False,
                        "aliases": ["on"],
                    },
                ]
            )
        )
        expression = {"operator": "equals", "fact": "enabled", "value": True}
        self.assertEqual(self.schema.digest, repeated.digest)
        self.assertEqual(
            self.schema.compile(expression).dependency_digest,
            repeated.compile(expression).dependency_digest,
        )
        other = compile_fact_schema({**declaration(), "id": "other"})
        with self.assertRaises(ApplicabilityError):
            self.schema.compile(expression).evaluate(other.bind({}))
        with self.assertRaises(ApplicabilityError) as caught:
            self.schema.compile(expression, language_version=99)
        self.assertEqual(caught.exception.failure.outcome, "unsupported")

    def test_invalid_schema_expression_and_values_reject(self) -> None:
        invalid_expressions = (
            {"operator": "missing"},
            {"operator": "equals", "fact": "missing", "value": True},
            {"operator": "contains", "fact": "enabled", "value": True},
            {"operator": "in", "fact": "mode", "values": ["outside"]},
        )
        for expression in invalid_expressions:
            with self.subTest(expression=expression), self.assertRaises(
                ApplicabilityError
            ):
                self.schema.compile(expression)
        with self.assertRaises(ApplicabilityError):
            self.schema.bind({"mode": self.known("enum", "outside")})
        with self.assertRaises(ApplicabilityError):
            compile_fact_schema(
                declaration(
                    [
                        {
                            "id": "one",
                            "type": "boolean",
                            "nullable": False,
                            "aliases": ["same"],
                        },
                        {
                            "id": "same",
                            "type": "boolean",
                            "nullable": False,
                            "aliases": [],
                        },
                    ]
                )
            )

    def test_every_fact_type_binds_through_one_schema(self) -> None:
        schema = compile_fact_schema(
            declaration(
                [
                    {"id": "b", "type": "boolean", "nullable": False, "aliases": []},
                    {"id": "e", "type": "enum", "nullable": False, "values": ["x"], "aliases": []},
                    {"id": "s", "type": "string", "nullable": False, "aliases": []},
                    {"id": "ss", "type": "string-set", "nullable": False, "aliases": []},
                    {"id": "es", "type": "enum-set", "nullable": False, "values": ["x"], "aliases": []},
                    {"id": "id", "type": "canonical-id", "nullable": False, "aliases": []},
                ]
            )
        )
        facts = schema.bind(
            {
                "b": self.known("boolean", True),
                "e": self.known("enum", "x"),
                "s": self.known("string", "value"),
                "ss": self.known("string-set", ["value"]),
                "es": self.known("enum-set", ["x"]),
                "id": self.known("canonical-id", "workflow.test"),
            }
        )
        self.assertEqual(tuple(facts.canonical_values), ("b", "e", "es", "id", "s", "ss"))

    def test_all_any_and_not_cover_the_complete_truth_table(self) -> None:
        expressions = {
            Truth.TRUE: {"operator": "always"},
            Truth.FALSE: {"operator": "equals", "fact": "enabled", "value": False},
            Truth.UNKNOWN: {"operator": "equals", "fact": "mode", "value": "a"},
        }
        facts = self.schema.bind({"enabled": self.known("boolean", True)})
        expected_all = {
            (Truth.TRUE, Truth.TRUE): Truth.TRUE,
            (Truth.TRUE, Truth.FALSE): Truth.FALSE,
            (Truth.TRUE, Truth.UNKNOWN): Truth.UNKNOWN,
            (Truth.FALSE, Truth.TRUE): Truth.FALSE,
            (Truth.FALSE, Truth.FALSE): Truth.FALSE,
            (Truth.FALSE, Truth.UNKNOWN): Truth.FALSE,
            (Truth.UNKNOWN, Truth.TRUE): Truth.UNKNOWN,
            (Truth.UNKNOWN, Truth.FALSE): Truth.FALSE,
            (Truth.UNKNOWN, Truth.UNKNOWN): Truth.UNKNOWN,
        }
        expected_any = {
            pair: (
                Truth.TRUE
                if Truth.TRUE in pair
                else Truth.UNKNOWN
                if Truth.UNKNOWN in pair
                else Truth.FALSE
            )
            for pair in expected_all
        }
        for pair, expected in expected_all.items():
            children = [expressions[item] for item in pair]
            with self.subTest(operator="all", pair=pair):
                result = self.schema.compile(
                    {"operator": "all", "expressions": children}
                ).evaluate(facts)
                self.assertIs(result.truth, expected)
            with self.subTest(operator="any", pair=pair):
                result = self.schema.compile(
                    {"operator": "any", "expressions": children}
                ).evaluate(facts)
                self.assertIs(result.truth, expected_any[pair])
        expected_not = {
            Truth.TRUE: Truth.FALSE,
            Truth.FALSE: Truth.TRUE,
            Truth.UNKNOWN: Truth.UNKNOWN,
        }
        for value, expected in expected_not.items():
            result = self.schema.compile(
                {"operator": "not", "expression": expressions[value]}
            ).evaluate(facts)
            self.assertIs(result.truth, expected)

    def test_runtime_module_imports_only_the_standard_library(self) -> None:
        root = Path(__file__).resolve().parents[1] / "standards_applicability"
        for source in root.glob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported = {item.name.partition(".")[0] for item in node.names}
                    self.assertLessEqual(imported, sys.stdlib_module_names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    self.assertIn(str(node.module).partition(".")[0], sys.stdlib_module_names)


if __name__ == "__main__":
    unittest.main()
