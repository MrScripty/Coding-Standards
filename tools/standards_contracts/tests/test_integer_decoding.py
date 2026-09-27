"""Integer representation follows schema locations, not incidental JSON values."""
from __future__ import annotations

from copy import deepcopy
import sys
import types
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator
from tools.standards_contracts.standards_contracts import ContractError, ContractRuntime, compile_contracts
from tools.standards_contracts.tests.schema_location_fixtures import inputs

DIALECT = 'https://json-schema.org/draft/2020-12/schema'


def runtime_for(root, definitions=None):
    schema = {'$schema': DIALECT, '$id': 'https://coding-standards.local/tests/integers',
              '$defs': {'Value': root, **(definitions or {})}}
    return ContractRuntime(schema, {}), schema


class IntegerDecodingTest(unittest.TestCase):
    def test_integral_values_become_exact_ints_without_losing_large_integers(self):
        runtime, schema = runtime_for({'type': 'integer'})
        oracle = Draft202012Validator(schema['$defs']['Value'])
        for value in (0, -3, 3.0, -0.0, 1e20, 2**300 + 1):
            with self.subTest(value=value):
                self.assertTrue(oracle.is_valid(value))
                decoded = runtime.decode('Value', value)
                self.assertIs(type(decoded), int)
                self.assertEqual(decoded, value)

    def test_invalid_numbers_are_rejected_before_conversion(self):
        runtime, _ = runtime_for({'type': 'integer', 'minimum': 1, 'maximum': 5})
        for value in (True, False, 0, 0.0, 5.5, 6.0, '2', None, float('inf'), float('-inf'), float('nan')):
            with self.subTest(value=value), self.assertRaises(ContractError) as caught:
                runtime.decode('Value', value)
            self.assertEqual(caught.exception.failure.outcome, 'invalid')
        for value in (1.0, 5.0):
            self.assertIs(type(runtime.decode('Value', value)), int)

    def test_number_untyped_and_literal_values_are_not_coerced(self):
        literal = {'value': 1.0, '$ref': 'not a schema', 'nested': [2.0]}
        for schema in ({}, {'type': 'number'}, {'const': 1.0}, {'enum': [1.0]},
                       {'type': ['number', 'integer', 'null']}):
            runtime, _ = runtime_for(schema)
            self.assertIs(type(runtime.decode('Value', 1.0)), float)
        for schema in ({'const': literal}, {'enum': [literal]}, {'default': {'type': 'integer'}}):
            before = deepcopy(schema)
            runtime, _ = runtime_for(schema)
            value = runtime.decode('Value', literal)
            self.assertIs(type(value['value']), float)
            self.assertEqual(value, literal)
            self.assertEqual(schema, before)

    def test_all_structural_locations_use_their_integer_schema(self):
        leaf = {'type': 'integer'}
        wrappers = (
            (leaf, 2.0, lambda v: v),
            ({'$ref': '#/$defs/Integer'}, 2.0, lambda v: v),
            ({'type': 'array', 'items': leaf}, [2.0], lambda v: v[0]),
            ({'type': 'object', 'additionalProperties': leaf}, {'key': 2.0}, lambda v: v['key']),
            ({'type': 'object', 'properties': {'value': leaf}, 'required': ['value'],
              'additionalProperties': False}, {'value': 2.0}, lambda v: v['value']),
            ({'oneOf': [leaf, {'type': 'string'}]}, 2.0, lambda v: v),
            ({'type': ['integer', 'null']}, 2.0, lambda v: v),
            ({'$ref': '#/$defs/Number', 'type': 'integer'}, 2.0, lambda v: v),
        )
        for root, value, inspect in wrappers:
            with self.subTest(root=root):
                runtime, _ = runtime_for(root, {'Integer': leaf, 'Number': {'type': 'number'}})
                before = deepcopy(value)
                self.assertIs(type(inspect(runtime.decode('Value', value))), int)
                self.assertEqual(value, before)
        runtime, _ = runtime_for({'type': ['integer', 'null']})
        self.assertIsNone(runtime.decode('Value', None))

    def test_recursive_inline_union_properties_are_decoded_without_literal_coercion(self):
        node = {'type': 'object', 'properties': {
            'kind': {'const': 'node'}, 'count': {'type': 'integer'},
            'literal': {}, 'children': {'type': 'array', 'items': {'$ref': '#/$defs/Node'}}},
            'required': ['kind', 'count', 'children'], 'additionalProperties': False}
        runtime, _ = runtime_for({'oneOf': [node, {'type': 'null'}]}, {'Node': node})
        value = {'kind': 'node', 'count': 1.0, 'literal': 7.0, 'children': [
            {'kind': 'node', 'count': 2.0, 'children': []}]}
        decoded = runtime.decode('Value', value)
        self.assertIs(type(decoded['count']), int)
        self.assertIs(type(decoded['children'][0]['count']), int)
        self.assertIs(type(decoded['literal']), float)
        self.assertIs(type(value['count']), float)

    def test_generated_from_value_and_constructor_share_normalization(self):
        schema, interface = inputs()
        schema['$defs']['RuntimeInfoCall']['properties'].update({
            'count': {'type': 'integer', 'minimum': 1},
            'payload': {'type': 'object', 'properties': {'count': {'type': 'integer'}},
                        'additionalProperties': False},
            'unchanged': {'type': 'number'},
            'optional': {'type': 'integer', 'default': 4.0},
        })
        schema['$defs']['RuntimeInfoCall']['properties']['composed'] = {
            '$ref': '#/$defs/AnyScalar', 'oneOf': [{'type': 'integer'}, {'type': 'string'}]}
        schema['$defs']['AnyScalar'] = {}
        compiled = compile_contracts(schema, interface)
        module = types.ModuleType('_integer_projection_fixture')
        with patch.dict(sys.modules, {module.__name__: module}):
            exec(compile(compiled.project().python_source, '<integer-test>', 'exec'), module.__dict__)
            args = {'count': 3.0, 'payload': {'count': 2.0}, 'unchanged': 5.0, 'composed': 8.0}
            for model in (module.RuntimeInfoCall.from_value(args), module.RuntimeInfoCall(**args)):
                self.assertIs(type(model.count), int)
                self.assertIs(type(model.composed), int)
                self.assertIs(type(model.payload['count']), int)
                self.assertIs(type(model.unchanged), float)
                self.assertNotIn('optional', model.as_contract())
                self.assertEqual(model.as_contract(), args)
                compiled.validate('RuntimeInfoCall', model.as_contract())
            self.assertIs(type(args['count']), float)
            self.assertIs(type(args['payload']['count']), float)

    def test_nullable_implicit_and_composed_containers_keep_integer_constraints(self):
        integer_field = {"properties": {"count": {"type": "integer"}}}
        wrappers = (
            ({**integer_field, "type": ["object", "null"]}, {"count": 2.0}, lambda v: v["count"]),
            ({"type": ["array", "null"], "items": {"type": "integer"}}, [2.0], lambda v: v[0]),
            (integer_field, {"count": 2.0}, lambda v: v["count"]),
            ({"items": {"type": "integer"}}, [2.0], lambda v: v[0]),
            ({**integer_field, "$ref": "#/$defs/Anything"}, {"count": 2.0}, lambda v: v["count"]),
            ({"$ref": "#/$defs/Anything", "oneOf": [{"type": "integer"}, {"type": "string"}]},
             2.0, lambda v: v),
            ({**integer_field, "oneOf": [{"required": ["count"]}, {"type": "null"}]},
             {"count": 2.0}, lambda v: v["count"]),
        )
        for root, value, inspect in wrappers:
            with self.subTest(root=root):
                runtime, _ = runtime_for(root, {"Anything": {}})
                self.assertIs(type(inspect(runtime.decode("Value", value))), int)
                original = (value["count"] if isinstance(value, dict) else
                            value[0] if isinstance(value, list) else value)
                self.assertIs(type(original), float)
        for root in (integer_field, {"items": {"type": "integer"}}):
            runtime, _ = runtime_for(root)
            self.assertIs(type(runtime.decode("Value", 2.0)), float)
        runtime, _ = runtime_for({"type": ["object", "null"], **integer_field})
        self.assertIsNone(runtime.decode("Value", None))

    def test_boolean_item_schema_keeps_untyped_numbers_and_false_rejects(self):
        runtime, _ = runtime_for({"type": "array", "items": True})
        self.assertIs(type(runtime.decode("Value", [1.0])[0]), float)
        runtime, _ = runtime_for({"type": "array", "items": False})
        with self.assertRaises(ContractError):
            runtime.decode("Value", [1.0])
        self.assertEqual(runtime.decode("Value", []), ())

    def test_unique_items_validation_precedes_numeric_normalization(self):
        runtime, _ = runtime_for({'type': 'array', 'items': {'type': 'integer'}, 'uniqueItems': True})
        with self.assertRaises(ContractError) as caught:
            runtime.decode('Value', [1, 1.0])
        self.assertEqual(caught.exception.failure.keyword, 'uniqueItems')
        self.assertEqual(runtime.decode('Value', [1.0, 2.0]), (1, 2))
