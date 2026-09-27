"""Diagnostic semantics against the independent validator, not another validator."""
from __future__ import annotations

from dataclasses import asdict
import json
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts import ContractError, ContractRuntime
from tools.standards_contracts.standards_contracts.validation_feedback import MAX_FEEDBACK_BYTES


def runtime_for(call):
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
              '$id': 'https://fixture.local/feedback', '$defs': {'Call': call},
              '$ref': '#/$defs/Call'}
    return ContractRuntime(schema, {}), Draft202012Validator(schema)


def object_schema(properties, required):
    return {'type': 'object', 'properties': properties, 'required': required,
            'additionalProperties': False}


class ValidationFeedbackTest(unittest.TestCase):
    def rejected(self, schema, value):
        runtime, independent = runtime_for(schema)
        self.assertFalse(independent.is_valid(value))
        with self.assertRaises(ContractError) as caught:
            runtime.validate('Call', value)
        return caught.exception.failure

    def test_missing_fields_are_individual_locations_not_duplicate_root_errors(self):
        schema = object_schema({'task': object_schema({'title': {'type': 'string'},
                            'edits': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}},
                            ['title', 'edits'])}, ['task'])
        result = self.rejected(schema, {'task': {}})
        self.assertEqual([(i.instance_pointer, i.keyword) for i in result.input_issues],
                         [('/task/title', 'required'), ('/task/edits', 'required')])
        self.assertFalse(result.issues_truncated)

    def test_disjoint_tag_reports_only_the_selected_branch_without_accepting_it(self):
        schema = object_schema({'action': {'oneOf': [
            object_schema({'kind': {'const': 'add'}, 'value': {'type': 'integer'}}, ['kind', 'value']),
            object_schema({'kind': {'const': 'remove'}, 'target': {'type': 'string'}}, ['kind', 'target']),
        ]}}, ['action'])
        result = self.rejected(schema, {'action': {'kind': 'add', 'value': 'SECRET'}})
        self.assertTrue(result.causes)  # The original validator failure tree is retained.
        self.assertEqual([(i.instance_pointer, i.keyword) for i in result.input_issues],
                         [('/action/value', 'type')])
        self.assertNotIn('SECRET', json.dumps([asdict(i) for i in result.input_issues]))

    def test_missing_or_ambiguous_discriminator_is_not_guessed(self):
        schema = {'oneOf': [object_schema({'kind': {'const': 'a'}}, ['kind']),
                            object_schema({'kind': {'const': 'b'}}, ['kind'])]}
        result = self.rejected(schema, {})
        self.assertEqual([i.keyword for i in result.input_issues], ['oneOf'])
        self.assertEqual(result.input_issues[0].instance_pointer, '')

    def test_array_constraints_and_escaping_are_preserved(self):
        schema = object_schema({'x/y~z': {'type': 'array', 'items': {'type': 'integer'}, 'minItems': 1}}, ['x/y~z'])
        result = self.rejected(schema, {'x/y~z': []})
        self.assertEqual(result.input_issues[0].instance_pointer, '/x~1y~0z')
        self.assertEqual(result.input_issues[0].message, 'Satisfy minItems = 1.')
        self.assertTrue(result.input_issues[0].location_exact)

    def test_dynamic_keys_and_submitted_values_are_redacted(self):
        schema = object_schema({'evidence': {'type': 'object', 'additionalProperties':
                                object_schema({'digest': {'type': 'integer'}}, ['digest'])}}, ['evidence'])
        result = self.rejected(schema, {'evidence': {'SECRET_KEY': {'digest': 'SECRET_VALUE'}}})
        issue = result.input_issues[0]
        self.assertEqual(issue.instance_pointer, '/evidence/*/digest')
        self.assertFalse(issue.location_exact)
        self.assertNotIn('SECRET', json.dumps(asdict(issue)))
        extra = self.rejected(object_schema({'known': {'type': 'string'}}, []), {'SECRET': 'SECRET'})
        self.assertEqual(extra.input_issues[0].keyword, 'additionalProperties')
        self.assertNotIn('SECRET', json.dumps(asdict(extra.input_issues[0])))

    def test_item_and_byte_bounds_have_explicit_truncation(self):
        schema = object_schema({f'field{i}': {'type': 'string'} for i in range(30)},
                               [f'field{i}' for i in range(30)])
        result = self.rejected(schema, {})
        self.assertEqual(len(result.input_issues), 8)
        self.assertTrue(result.issues_truncated)
        names = ['界' * 400 + str(i) for i in range(8)]
        result = self.rejected(object_schema({n: {'type': 'string'} for n in names}, names), {})
        self.assertLessEqual(len(json.dumps([asdict(i) for i in result.input_issues]).encode()), MAX_FEEDBACK_BYTES)
        self.assertTrue(result.issues_truncated)

    def test_oversized_pointer_is_explicitly_non_exact(self):
        key = 'x' * 600
        result = self.rejected(object_schema({key: {'type': 'integer'}}, [key]), {key: 'bad'})
        self.assertEqual(result.input_issues[0].instance_pointer, '')
        self.assertFalse(result.input_issues[0].location_exact)

    def test_success_never_builds_feedback_and_acceptance_matches_independent_validator(self):
        schema = object_schema({'value': {'type': 'integer', 'minimum': 0}}, ['value'])
        runtime, validator = runtime_for(schema)
        for value in ({}, {'value': False}, {'value': -1}, {'value': '1'},
                      {'value': 0}, {'value': 1.0}, {'value': 5, 'extra': 2}):
            try:
                runtime.validate('Call', value)
                accepted = True
            except ContractError:
                accepted = False
            self.assertEqual(accepted, validator.is_valid(value))
        with patch('tools.standards_contracts.standards_contracts.runtime.validation_feedback',
                   side_effect=AssertionError('valid path must not construct diagnostics')):
            runtime.validate('Call', {'value': 2})
