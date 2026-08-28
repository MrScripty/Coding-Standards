from __future__ import annotations

import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from tools.standards_contracts.standards_contracts import (
    ContractError,
    compile_contracts,
)

from support import canonical_inputs, mutated_definition


class ContractSemanticsTest(unittest.TestCase):
    def assert_agrees(
        self,
        definition: str,
        replacement: dict[str, object],
        cases: tuple[tuple[object, bool], ...],
    ) -> None:
        schema, interface = mutated_definition(definition, replacement)
        compiled = compile_contracts(schema, interface)
        registry = Registry().with_resource(
            schema["$id"], Resource.from_contents(schema)
        )
        direct = Draft202012Validator(schema, registry=registry).evolve(
            schema=schema["$defs"][definition]
        )
        for value, expected in cases:
            with self.subTest(definition=definition, value=value):
                self.assertEqual(direct.is_valid(value), expected)
                try:
                    compiled.validate(definition, value)
                except ContractError as error:
                    actual = False
                    self.assertEqual(error.failure.code, "CONTRACT.INVALID_INSTANCE")
                    self.assertNotIn("jsonschema", error.failure.message)
                else:
                    actual = True
                self.assertEqual(actual, expected)

    def test_json_equality_domains_use_the_selected_validator(self) -> None:
        self.assert_agrees(
            "NonEmptyString",
            {"const": 1},
            ((1, True), (True, False), (1.0, True)),
        )
        self.assert_agrees(
            "NonEmptyString",
            {"enum": [True]},
            ((True, True), (1, False), (1.0, False)),
        )
        self.assert_agrees(
            "NonEmptyString",
            {"const": "\u00e9"},
            (("\u00e9", True), ("e\u0301", False)),
        )
        self.assert_agrees(
            "NonEmptyString",
            {"const": {"a": 1, "b": 2}},
            (({"b": 2, "a": 1}, True), ({"a": 1, "b": 3}, False)),
        )
        self.assert_agrees(
            "NonEmptyString",
            {"const": [1, 2]},
            (([1, 2], True), ([2, 1], False)),
        )

        all_json_types = (
            (None, "different"),
            (False, True),
            (3, 4),
            (3.5, 4.5),
            ("text", "other"),
            ([1, "x"], ["x", 1]),
            ({"a": 1}, {"a": 2}),
        )
        for selected, different in all_json_types:
            with self.subTest(keyword="const", selected=selected):
                self.assert_agrees(
                    "NonEmptyString",
                    {"const": selected},
                    ((selected, True), (different, False)),
                )
            with self.subTest(keyword="enum", selected=selected):
                self.assert_agrees(
                    "NonEmptyString",
                    {"enum": [selected]},
                    ((selected, True), (different, False)),
                )

    def test_unique_items_covers_every_json_value_family(self) -> None:
        cases = (
            ([None, None], False),
            ([None, False], True),
            ([True, 1], True),
            ([1, 1.0], False),
            (["\u00e9", "e\u0301"], True),
            ([[1, 2], [1, 2]], False),
            ([[1, 2], [2, 1]], True),
            ([{"a": 1, "b": 2}, {"b": 2, "a": 1}], False),
        )
        self.assert_agrees(
            "FactSet",
            {"type": "array", "items": {}, "uniqueItems": True},
            cases,
        )

    def test_primitive_composition_object_array_string_and_number_keywords(
        self,
    ) -> None:
        scenarios = (
            ("NonEmptyString", {"type": "null"}, ((None, True), (False, False))),
            ("NonEmptyString", {"type": "boolean"}, ((False, True), (0, False))),
            (
                "NonEmptyString",
                {"type": "integer"},
                ((2, True), (2.0, True), (2.5, False)),
            ),
            ("NonEmptyString", {"type": "number"}, ((2, True), (2.5, True))),
            (
                "NonEmptyString",
                {"oneOf": [{"type": "string"}, {"const": "x"}]},
                (("y", True), ("x", False), (1, False)),
            ),
            (
                "FactSet",
                {
                    "type": "object",
                    "required": ["value"],
                    "properties": {"value": {"type": "integer"}},
                    "additionalProperties": False,
                },
                (({"value": 1}, True), ({}, False), ({"value": 1, "x": 2}, False)),
            ),
            (
                "FactSet",
                {"type": "array", "items": {"type": "string"}, "minItems": 1},
                ((["x"], True), ([], False), ([1], False)),
            ),
            (
                "NonEmptyString",
                {"type": "string", "minLength": 2, "pattern": "^[a-z]+$"},
                (("ab", True), ("a", False), ("a1", False)),
            ),
            (
                "NonEmptyString",
                {"type": "number", "minimum": 2},
                ((2, True), (2.5, True), (1.99, False)),
            ),
        )
        for definition, replacement, cases in scenarios:
            self.assert_agrees(definition, replacement, cases)

    def test_adapter_rejects_values_outside_strict_json_before_validation(self) -> None:
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)
        for value in (float("nan"), float("inf"), b"bytes", {1: "invalid key"}):
            with self.subTest(value=value), self.assertRaises(ContractError) as caught:
                compiled.validate("ScalarValue", value)
            self.assertEqual(
                caught.exception.failure.code, "CONTRACT.INVALID_JSON_VALUE"
            )

    def test_validation_failures_have_stable_nested_pointers(self) -> None:
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)
        with self.assertRaises(ContractError) as caught:
            compiled.validate(
                "QueryCall",
                {
                    "view": {
                        "kind": "standards-authority-view-handle",
                        "id": "invalid",
                        "schema_version": 4,
                    },
                    "request": {"kind": "route", "facts": {}},
                },
            )
        selected = caught.exception.failure
        self.assertEqual(selected.code, "CONTRACT.INVALID_INSTANCE")
        self.assertEqual(selected.definition, "QueryCall")
        self.assertTrue(selected.instance_pointer.startswith("/view"))
        self.assertIsNotNone(selected.keyword)


if __name__ == "__main__":
    unittest.main()
