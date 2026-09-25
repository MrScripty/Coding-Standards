from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import FrozenInstanceError, asdict, field, make_dataclass
import unittest
from unittest.mock import patch
from types import MappingProxyType

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts.errors import ContractError
from tools.standards_contracts.standards_contracts.runtime import (
    ContractRuntime, FrozenMap, MISSING, model_as_contract,
)


DIALECT = "https://json-schema.org/draft/2020-12/schema"


def record(tag: object, *, name: str = "kind", required: bool = True) -> dict:
    return {
        "type": "object",
        "properties": {name: tag, "value": {"type": "integer"},
                       "note": {"type": "string", "default": "annotation only"}},
        "required": [name, "value"] if required else ["value"],
        "additionalProperties": False,
    }


def schema_for(*variants: object, definitions: dict | None = None) -> dict:
    return {"$schema": DIALECT, "$id": "https://coding-standards.local/tests/unions",
            "$defs": {**(definitions or {}), "Choice": {"oneOf": list(variants)}}}


def models_for(schema: dict) -> dict:
    """Small test models keep type identity and optionality observable."""
    models = {}
    for name, node in schema["$defs"].items():
        properties = node.get("properties", {})
        if node.get("type") != "object" or not properties:
            continue
        required = node.get("required", [])
        members = [(key, object) for key in properties if key in required]
        members.extend((key, object, field(default=MISSING))
                       for key in properties if key not in required)
        models[name] = make_dataclass(name, members, frozen=True, slots=True,
                                     namespace={"__definition__": name,
                                                "__contract_fields__": MappingProxyType(
                                                    {key: key for key in properties})})
    return models


@contextmanager
def construction_observations(runtime: ContractRuntime):
    """Count conversion work separately from the unchanged root validator."""
    counts = {"roots": 0, "branches": 0}
    validating = False
    original_validate = runtime.validate
    original_is_valid = Draft202012Validator.is_valid

    def validate(definition, value):
        nonlocal validating
        counts["roots"] += 1
        validating = True
        try:
            return original_validate(definition, value)
        finally:
            validating = False

    def is_valid(validator, *args, **kwargs):
        if not validating:
            counts["branches"] += 1
        return original_is_valid(validator, *args, **kwargs)

    with patch.object(runtime, "validate", side_effect=validate), \
            patch.object(Draft202012Validator, "is_valid", is_valid):
        yield counts


class UnionDecodingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = schema_for(
            {"$ref": "#/$defs/Alpha"}, {"$ref": "#/$defs/Beta"},
            definitions={"Alpha": record({"const": "alpha"}),
                         "Beta": record({"enum": ["beta", "b"]})},
        )
        self.models = models_for(self.schema)
        self.runtime = ContractRuntime(self.schema, self.models)

    def test_const_and_enum_select_generated_types_without_branch_validation(self):
        for tag, name in (("alpha", "Alpha"), ("beta", "Beta"), ("b", "Beta")):
            value = {"kind": tag, "value": 7}
            with self.subTest(tag=tag), construction_observations(self.runtime) as counts:
                decoded = self.runtime.decode("Choice", value)
                self.assertIs(type(decoded), self.models[name])
                self.assertEqual(model_as_contract(decoded), value)
                self.assertIs(decoded.note, MISSING)
                self.assertEqual(counts, {"roots": 1, "branches": 0})
            with self.assertRaises(FrozenInstanceError):
                decoded.value = 8

    def test_inline_variants_use_the_same_selector(self):
        runtime = ContractRuntime(schema_for(record({"const": "a"}),
                                             record({"const": "b"})), {})
        with construction_observations(runtime) as counts:
            result = runtime.decode("Choice", {"kind": "a", "value": 1})
        self.assertIsInstance(result, FrozenMap)
        self.assertEqual(dict(result), {"kind": "a", "value": 1})
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_array_and_map_values_construct_all_tagged_items(self):
        schema = deepcopy(self.schema)
        schema["$defs"].update({
            "Choices": {"type": "array", "items": {"$ref": "#/$defs/Choice"}},
            "ChoiceMap": {"type": "object", "additionalProperties": {"$ref": "#/$defs/Choice"}},
        })
        runtime = ContractRuntime(schema, self.models)
        values = [{"kind": "alpha", "value": 1}, {"kind": "b", "value": 2}]
        with construction_observations(runtime) as counts:
            array = runtime.decode("Choices", values)
            mapping = runtime.decode("ChoiceMap", dict(zip(("a", "b"), values)))
        self.assertEqual([model_as_contract(item) for item in array], values)
        self.assertEqual([model_as_contract(item) for item in mapping.values()], values)
        self.assertIsInstance(array, tuple)
        self.assertEqual(counts, {"roots": 2, "branches": 0})

    def test_normalize_model_keeps_one_root_proof_and_optional_defaults(self):
        schema = deepcopy(self.schema)
        schema["$defs"]["Envelope"] = {
            "type": "object", "required": ["choice"],
            "properties": {"choice": {"$ref": "#/$defs/Choice"},
                           "note": {"type": "string", "default": "annotation only"}},
            "additionalProperties": False,
        }
        models = models_for(schema)
        runtime = ContractRuntime(schema, models)
        envelope = models["Envelope"]({"kind": "alpha", "value": 3})
        with construction_observations(runtime) as counts:
            runtime.normalize_model(envelope)
        self.assertIs(type(envelope.choice), models["Alpha"])
        self.assertIs(envelope.note, MISSING)
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_recursive_object_boundary_and_reference_alias(self):
        schema = schema_for(
            {"$ref": "#/$defs/LeafAlias"}, {"$ref": "#/$defs/Branch"},
            definitions={
                "LeafAlias": {"$ref": "#/$defs/Leaf"},
                "Leaf": record({"const": "leaf"}),
                "Branch": {"type": "object", "required": ["kind", "children"],
                           "properties": {"kind": {"const": "branch"},
                                          "children": {"type": "array", "items": {"$ref": "#/$defs/Choice"}}},
                           "additionalProperties": False},
            },
        )
        models = models_for(schema)
        runtime = ContractRuntime(schema, models)
        value = {"kind": "leaf", "value": 1}
        for _ in range(8):
            value = {"kind": "branch", "children": [value]}
        with construction_observations(runtime) as counts:
            result = runtime.decode("Choice", value)
        self.assertEqual(model_as_contract(result), value)
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_second_required_field_can_disambiguate_overlapping_first_field(self):
        variants = [record({"const": "same"}), record({"const": "same"})]
        for variant, tag in zip(variants, ("left", "right")):
            variant["properties"]["side"] = {"const": tag}
            variant["required"].append("side")
        runtime = ContractRuntime(schema_for(*variants), {})
        with construction_observations(runtime) as counts:
            decoded = runtime.decode("Choice", {"kind": "same", "side": "right", "value": 1})
        self.assertEqual(decoded["side"], "right")
        self.assertEqual(counts["branches"], 0)

    def test_exact_unicode_strings_and_empty_tag(self):
        runtime = ContractRuntime(schema_for(*(record({"const": tag})
                                               for tag in ("", "\u00e9", "e\u0301"))), {})
        with construction_observations(runtime) as counts:
            for tag in ("", "\u00e9", "e\u0301"):
                self.assertEqual(runtime.decode("Choice", {"kind": tag, "value": 1})["kind"], tag)
        self.assertEqual(counts, {"roots": 3, "branches": 0})

    def test_schema_ownership_isolated_between_runtimes_and_from_caller_mutation(self):
        changed = deepcopy(self.schema)
        changed["$defs"]["Alpha"]["properties"]["kind"]["const"] = "changed"
        other = ContractRuntime(changed, self.models)
        self.schema["$defs"]["Alpha"]["properties"]["kind"]["const"] = "poison"
        changed["$defs"].clear()
        with construction_observations(self.runtime) as first:
            self.assertEqual(self.runtime.decode("Choice", {"kind": "alpha", "value": 1}).kind, "alpha")
        with construction_observations(other) as second:
            self.assertEqual(other.decode("Choice", {"kind": "changed", "value": 2}).kind, "changed")
        self.assertEqual(first["branches"], 0)
        self.assertEqual(second["branches"], 0)

    def test_decoded_mutation_does_not_change_later_selection(self):
        value = {"kind": "alpha", "value": 1}
        result = self.runtime.decode("Choice", value)
        value["kind"] = "b"
        object.__setattr__(result, "kind", "corrupted test instance")
        decoded = self.runtime.decode("Choice", value)
        self.assertIs(type(decoded), self.models["Beta"])
        self.assertEqual(decoded.kind, "b")

    def test_mapping_input_and_readonly_nested_values(self):
        with construction_observations(self.runtime) as counts:
            decoded = self.runtime.decode("Choice", MappingProxyType({"kind": "alpha", "value": 4}))
        self.assertEqual(decoded.value, 4)
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_invalid_inputs_have_exact_root_diagnostics_before_construction(self):
        values = [
            {"kind": "unknown", "value": 1}, {"value": 1},
            {"kind": "alpha", "value": "wrong"}, {"kind": "alpha", "value": True},
            {"kind": "alpha", "value": 1, "extra": 0},
            {"kind": ["alpha"], "value": 1}, {"kind": "alpha", "value": float("nan")},
            {1: "invalid key"}, None, b"bytes",
        ]
        for value in values:
            with self.subTest(value=value):
                with self.assertRaises(ContractError) as direct:
                    self.runtime.validate("Choice", value)
                with construction_observations(self.runtime) as counts:
                    with self.assertRaises(ContractError) as decoded:
                        self.runtime.decode("Choice", value)
                self.assertEqual(asdict(decoded.exception.failure), asdict(direct.exception.failure))
                self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_nested_invalid_branch_keeps_error_causes_and_pointers(self):
        schema = deepcopy(self.schema)
        schema["$defs"]["List"] = {"type": "array", "items": {"$ref": "#/$defs/Choice"}}
        runtime = ContractRuntime(schema, self.models)
        value = [{"kind": "alpha", "value": 0}, {"kind": "b", "value": "bad"}]
        with self.assertRaises(ContractError) as expected:
            runtime.validate("List", value)
        with self.assertRaises(ContractError) as actual:
            runtime.decode("List", value)
        self.assertEqual(actual.exception.failure, expected.exception.failure)
        self.assertEqual(actual.exception.failure.instance_pointer, "/1")
        self.assertTrue(actual.exception.failure.causes)

    def assert_fallback(self, schema: dict, value: object, expected: object) -> None:
        runtime = ContractRuntime(schema, {})
        with construction_observations(runtime) as counts:
            result = runtime.decode("Choice", value)
        self.assertEqual(result, expected)
        self.assertEqual(counts["roots"], 1)
        self.assertGreater(counts["branches"], 0)

    def test_overlapping_string_tags_retain_general_branch_selection(self):
        left, right = record({"const": "same"}), record({"const": "same"})
        right["properties"]["value"] = {"type": "string"}
        value = {"kind": "same", "value": 4}
        self.assert_fallback(schema_for(left, right), value, value)

    def test_untagged_branch_and_optional_tag_retain_general_selection(self):
        left = record({"const": "left"})
        for right in (record({"const": "right"}, required=False),
                      record({"type": "string"})):
            with self.subTest(right=right):
                # Only the right branch accepts this input.
                value = {"kind": "right", "value": 1}
                self.assert_fallback(schema_for(left, right), value, value)

    def test_non_object_and_mixed_enum_tags_retain_general_selection(self):
        self.assert_fallback(schema_for(record({"const": "left"}), {"type": "null"}), None, None)
        value = {"kind": 1, "value": 2}
        self.assert_fallback(schema_for(record({"const": "left"}), record({"enum": ["right", 1]})), value, value)

    def test_boolean_number_and_structured_constants_use_json_equality(self):
        for value in (True, 1, 1.0):
            self.assert_fallback(schema_for({"const": True}, {"const": 1}), value, value)
        for value in ([1, 2], {"a": 1}):
            self.assert_fallback(schema_for({"const": [1, 2]}, {"const": {"a": 1}}), value, value)
        ambiguous = ContractRuntime(schema_for({"const": 1}, {"const": 1.0}), {})
        with self.assertRaises(ContractError):
            ambiguous.decode("Choice", 1)

    def test_discriminant_requires_explicit_object_type(self):
        left, right = record({"const": "left"}), record({"const": "right"})
        del left["type"]
        self.assert_fallback(schema_for(left, right), "not an object", "not an object")

    def test_ref_siblings_and_referenced_tag_keep_general_selection(self):
        schema = deepcopy(self.schema)
        schema["$defs"]["Choice"]["oneOf"][0]["description"] = "Retain reference interpretation"
        value = {"kind": "alpha", "value": 1}
        self.assert_fallback(schema, value, value)
        schema = deepcopy(self.schema)
        schema["$defs"]["Tag"] = {"const": "alpha"}
        schema["$defs"]["Alpha"]["properties"]["kind"] = {"$ref": "#/$defs/Tag"}
        self.assert_fallback(schema, value, value)

    def test_ambiguous_union_rejects_even_when_one_tag_matches(self):
        variants = [record({"const": "same"}), record({"enum": ["same", "other"]})]
        runtime = ContractRuntime(schema_for(*variants), {})
        with construction_observations(runtime) as counts:
            with self.assertRaises(ContractError) as caught:
                runtime.decode("Choice", {"kind": "same", "value": 1})
        self.assertEqual(caught.exception.failure.keyword, "oneOf")
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_nested_resource_scope_keeps_the_existing_reference_path(self):
        left, right = record({"const": "left"}), record({"const": "right"})
        left["$id"] = "https://coding-standards.local/tests/child"
        value = {"kind": "left", "value": 1}
        self.assert_fallback(schema_for(left, right), value, value)

    def test_annotations_that_look_like_schemas_are_not_traversed(self):
        schema = deepcopy(self.schema)
        schema["$defs"]["Alpha"]["default"] = {
            "$id": "https://example.invalid/not-a-resource",
            "oneOf": [{"$ref": "#/$defs/Missing"}],
        }
        runtime = ContractRuntime(schema, self.models)
        with construction_observations(runtime) as counts:
            result = runtime.decode("Choice", {"kind": "alpha", "value": 3})
        self.assertEqual(result.value, 3)
        self.assertEqual(counts, {"roots": 1, "branches": 0})

    def test_missing_reference_is_not_resolved_during_selector_planning(self):
        ContractRuntime(schema_for({"$ref": "#/$defs/Missing"}, record({"const": "other"})), {})

    def test_reference_cycle_does_not_create_a_planning_loop(self):
        schema = schema_for({"$ref": "#/$defs/Loop"}, record({"const": "other"}),
                            definitions={"Loop": {"$ref": "#/$defs/Loop"}})
        # A cycle cannot identify a construction branch; actual validation stays
        # with the existing reference owner and is not invoked by this check.
        ContractRuntime(schema, {})


if __name__ == "__main__":
    unittest.main()
