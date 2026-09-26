"""Schema keywords have meaning at schema positions, not inside JSON literals."""
from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

from tools.standards_contracts.standards_contracts import ContractError, compile_contracts
from tools.standards_contracts.tests.schema_location_fixtures import inputs


class SchemaLocationsTest(unittest.TestCase):
    def test_literal_annotations_do_not_create_reference_dependencies(self):
        for keyword, annotation in (
            ("default", {"$ref": "#/$defs/Missing", "$id": "literal", "unknown": True}),
            ("const", {"$ref": "https://example.invalid/not-a-reference"}),
            ("enum", [{"$ref": "#/$defs/Missing"}, {"oneOf": [{"$ref": "#/$defs/Other"}]}]),
        ):
            with self.subTest(keyword=keyword):
                schema, interface = inputs()
                schema["$defs"]["RuntimeInfoCall"]["properties"]["payload"] = {keyword: annotation}
                compiled = compile_contracts(schema, interface)
                self.assertEqual(compiled.schema, schema)
                projected = compiled.project().agent_tools
                self.assertEqual(projected["$defs"]["RuntimeInfoCall"]["properties"]["payload"],
                                 {keyword: annotation})

    def test_annotation_reference_does_not_make_an_unused_definition_reachable(self):
        schema, interface = inputs()
        schema["$defs"]["Unused"] = {"type": "string"}
        schema["$defs"]["RuntimeInfoCall"]["default"] = {"$ref": "#/$defs/Unused"}
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.UNREACHABLE_DEFINITION")

    def test_missing_real_reference_and_unknown_schema_keyword_still_reject(self):
        for field, code in (({"$ref": "#/$defs/Missing"}, "CONTRACT.UNRESOLVABLE_REFERENCE"),
                            ({"$ref": "https://example.invalid/remote"}, "CONTRACT.UNSUPPORTED_REFERENCE"),
                            ({"allOf": [{"type": "string"}]}, "CONTRACT.UNSUPPORTED_PROJECTION")):
            schema, interface = inputs()
            schema["$defs"]["RuntimeInfoCall"]["properties"]["payload"] = field
            with self.subTest(code=code), self.assertRaises(ContractError) as caught:
                compile_contracts(schema, interface)
            self.assertEqual(caught.exception.failure.code, code)

    def test_generated_python_preserves_literal_wire_field_names(self):
        schema, interface = inputs()
        fields = ["$ref", "$defs", "123", "", "a.b", "a-b", "class", "µ", "__private"]
        root = schema["$defs"]["RuntimeInfoCall"]
        root["properties"].update({name: {"type": "string"} for name in fields})
        compiled = compile_contracts(schema, interface)
        source = compiled.project().python_source
        module = types.ModuleType("schema_location_generated")
        with patch.dict(sys.modules, {module.__name__: module}):
            exec(compile(source, "schema_location_generated.py", "exec"), module.__dict__)
            value = {name: "literal field value" for name in fields}
            result = module.RuntimeInfoCall.from_value(value)
            self.assertEqual(result.as_contract(), value)
            self.assertEqual(module.RuntimeInfoCall.from_value({}).as_contract(), {})
            with self.assertRaises(ContractError):
                module.RuntimeInfoCall.from_value({"$ref": 1})
            self.assertEqual(result.__contract_fields__["a-b"], "a_b")
            self.assertEqual(result.__contract_fields__["class"], "class_")

    def test_escaped_field_collisions_are_rejected(self):
        schema, interface = inputs()
        schema["$defs"]["RuntimeInfoCall"]["properties"].update(
            {"$ref": {"type": "string"}, "field_24726566": {"type": "string"}})
        with self.assertRaises(ContractError) as caught:
            compile_contracts(schema, interface)
        self.assertEqual(caught.exception.failure.code, "CONTRACT.UNSUPPORTED_PROJECTION")
