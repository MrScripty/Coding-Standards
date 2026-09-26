"""Exercise literal-data preservation through actual catalog and CLI owners."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts import compile_contracts
from tools.standards_contracts.tests.schema_location_fixtures import inputs
from tools.standards_engine.standards_engine.mcp_catalog import input_schema, tool_catalog

ROOT = Path(__file__).resolve().parents[3]


class CatalogSchemaLocationsTest(unittest.TestCase):
    def test_public_catalog_preserves_literal_fields_and_constraints_in_both_modes(self):
        for keyword, payload in (("const", {"$ref": "#/$defs/Text"}),
                                 ("enum", [{"$ref": "#/$defs/Text"}, {"$ref": "literal"}])):
            schema, interface = inputs()
            root = schema["$defs"]["RuntimeInfoCall"]
            root["properties"].update({"$ref": {"type": "string"}, "payload": {keyword: payload}})
            before = deepcopy(schema)
            compiled = compile_contracts(schema, interface)
            for purpose in ("authoring", "application"):
                for mode in ("compatibility", "native"):
                    with self.subTest(keyword=keyword, purpose=purpose, mode=mode):
                        tool = tool_catalog(compiled, purpose=purpose, schema_mode=mode)[0]
                        projected = tool["inputSchema"]
                        Draft202012Validator.check_schema(projected)
                        self.assertEqual(projected["properties"]["payload"], {keyword: payload})
                        original = Draft202012Validator({**root, "$defs": schema["$defs"]})
                        validator = Draft202012Validator(projected)
                        for instance, expected in (({}, True), ({"$ref": "ordinary data"}, True),
                            ({"payload": {"$ref": "#/$defs/Text"}}, True),
                            ({"payload": {"type": "string", "minLength": 1}}, False),
                            ({"$ref": 1}, False), ({"unknown": True}, False)):
                            self.assertEqual(original.is_valid(instance), expected)
                            self.assertEqual(validator.is_valid(instance), expected)
            self.assertEqual(schema, before)

    def test_default_annotation_is_preserved_and_never_injects_a_value(self):
        schema, interface = inputs()
        annotation = {"$ref": "#/$defs/Missing", "oneOf": [{"$ref": "literal"}]}
        root = schema["$defs"]["RuntimeInfoCall"]
        root["properties"]["payload"] = {"default": annotation}
        compiled = compile_contracts(schema, interface)
        for mode in ("compatibility", "native"):
            tool = tool_catalog(compiled, purpose='authoring', schema_mode=mode)[0]
            self.assertEqual(tool["inputSchema"]["properties"]["payload"]["default"], annotation)
            self.assertTrue(Draft202012Validator(tool["inputSchema"]).is_valid({}))

    def test_cli_closure_matches_schema_locations(self):
        spec = importlib.util.spec_from_file_location("schema_cli_probe", ROOT / ".agents/skills/standards-engine/scripts/invoke.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        root = {"type": "object", "properties": {"$ref": {"$ref": "#/$defs/Text"}},
                "default": {"$ref": "#/$defs/Missing"}, "additionalProperties": False}
        contract = {"$defs": {"Text": {"type": "string"}}}
        result = module._schema_closure(contract, {"input_schema": root})
        self.assertEqual(result, {"input_schema": root, "$defs": contract["$defs"]})

    def test_recursive_siblings_and_literal_annotations_preserve_constraints(self):
        definitions = {"Node": {"type": "object", "properties": {
            "$ref": {"type": "string"}, "children": {"type": "array", "items": {"$ref": "#/$defs/Node"}}},
            "additionalProperties": False, "default": {"$ref": "#/$defs/Missing"}}}
        root = {"$ref": "#/$defs/Node", "required": ["$ref"]}
        projected = input_schema(root, definitions)
        validator = Draft202012Validator(projected)
        for instance, expected in (({"$ref": "a", "children": [{"$ref": "b"}]}, True),
                                   ({"$ref": "a", "children": [{}]}, True),
                                   ({}, False), ({"$ref": "a", "children": [{"$ref": 2}]}, False)):
            self.assertEqual(Draft202012Validator({**root, "$defs": definitions}).is_valid(instance), expected)
            self.assertEqual(validator.is_valid(instance), expected)

    def test_catalog_builder_requires_no_filesystem_or_transport(self):
        schema, interface = inputs()
        compiled = compile_contracts(schema, interface)
        before = compiled.schema
        with patch.object(Path, "read_text", side_effect=AssertionError("filesystem access")):
            first = tool_catalog(compiled, purpose="authoring")
            first[0]["inputSchema"]["properties"]["name"].clear()
            second = tool_catalog(compiled, purpose="authoring")
        self.assertEqual(compiled.schema, before)
        self.assertEqual(second[0]["inputSchema"]["properties"]["name"],
                         {"type": "string", "minLength": 1})

    def test_literal_values_survive_each_supported_container(self):
        literal = {"$ref": "#/$defs/NotASchema", "properties": {"$id": ["literal"]}}
        wrappers = (
            (lambda s: s, lambda v: v),
            (lambda s: {"type": "object", "properties": {"$ref": s},
                        "required": ["$ref"], "additionalProperties": False}, lambda v: {"$ref": v}),
            (lambda s: {"type": "array", "items": s, "minItems": 1}, lambda v: [v]),
            (lambda s: {"type": "object", "additionalProperties": s}, lambda v: {"key": v}),
            (lambda s: {"oneOf": [s, {"type": "null"}]}, lambda v: v),
        )
        for keyword in ("const", "enum"):
            constraint = {keyword: [literal] if keyword == "enum" else literal, "default": literal}
            for index, (wrap, instance) in enumerate(wrappers):
                with self.subTest(keyword=keyword, wrapper=index):
                    original = wrap(constraint)
                    projected = input_schema(original, {})
                    self.assertEqual(projected, {**original, "$defs": {}})
                    for value, expected in ((instance(literal), True), (instance({"$ref": "different"}), False)):
                        self.assertEqual(Draft202012Validator(original).is_valid(value), expected)
                        self.assertEqual(Draft202012Validator(projected).is_valid(value), expected)
