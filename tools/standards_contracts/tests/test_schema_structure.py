"""Hand-authored structural oracles for the admitted schema-location family."""
from __future__ import annotations

from copy import deepcopy
import unittest

from tools.standards_contracts.standards_contracts import ContractError
from tools.standards_contracts.standards_contracts.schema_structure import (
    direct_schema_references, referenced_definitions,
    schema_children, schema_closure, schema_nodes,
)


class SchemaStructureTest(unittest.TestCase):
    def test_only_declared_schema_positions_are_walked(self):
        data = {"$ref": "#/$defs/Data", "properties": {"fake": {"type": "integer"}}}
        root = {
            "properties": {"$ref": {"$ref": "#/$defs/Property"}},
            "$defs": {"Local": {"$ref": "#/$defs/Definition"}},
            "items": {"$ref": "#/$defs/Item"},
            "additionalProperties": False,
            "oneOf": [{"$ref": "#/$defs/Variant"}, True],
            "allOf": [{"$ref": "#/$defs/Sibling"}],
            "const": data, "enum": [data], "default": data,
        }
        self.assertEqual([path for path, _ in schema_children(root)], [
            ("properties", "$ref"), ("$defs", "Local"), ("items",),
            ("additionalProperties",), ("oneOf", 0), ("oneOf", 1), ("allOf", 0),
        ])
        self.assertEqual(list(direct_schema_references(root)), [
            "#/$defs/Property", "#/$defs/Definition", "#/$defs/Item",
            "#/$defs/Variant", "#/$defs/Sibling",
        ])
        self.assertEqual(len(list(schema_nodes(root))), 6)

    def test_reference_closure_terminates_cycles_and_keeps_literal_data(self):
        definitions = {
            "Node": {"type": "object", "properties": {"next": {"$ref": "#/$defs/Node"}},
                     "default": {"$ref": "#/$defs/Unused"}},
            "Unused": {"type": "integer"},
        }
        root = {"allOf": [{"$ref": "#/$defs/Node"}], "const": {"$ref": "#/$defs/Missing"}}
        self.assertEqual(set(referenced_definitions(root, definitions)), {"Node"})
        original = deepcopy(definitions)
        output = schema_closure(root, definitions)
        output["$defs"]["Node"]["properties"].clear()
        self.assertEqual(definitions, original)
        self.assertEqual(output["const"], root["const"])

    def test_reference_failures_are_explicit_without_retrieval(self):
        for reference, code in (("#/$defs/Missing", "CONTRACT.UNRESOLVABLE_REFERENCE"),
                                ("https://example.invalid/schema", "CONTRACT.UNSUPPORTED_REFERENCE"),
                                ("#/properties/name", "CONTRACT.UNSUPPORTED_REFERENCE")):
            with self.subTest(reference=reference), self.assertRaises(ContractError) as caught:
                schema_closure({"$ref": reference}, {})
            self.assertEqual(caught.exception.failure.code, code)
