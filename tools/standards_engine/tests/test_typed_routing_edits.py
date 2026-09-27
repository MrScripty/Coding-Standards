"""The pilot changes internal representation, not the serialized edit contract."""
from __future__ import annotations

from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import logical_authoring as logical


def routing_edits():
    fact = {'id': 'routing.typed-pilot', 'semantic_revision': 1, 'type': 'enum-set',
            'nullable': False, 'values': ['z', 'a'], 'aliases': ['routing.typed-alias'],
            'meaning': 'A test selection.', 'prompt': 'Which value?'}
    rule = {'id': 'route.typed-pilot', 'target': 'topic.code-design',
            'when': {'operator': 'all', 'expressions': [
                {'operator': 'contains', 'fact': fact['id'], 'value': 'z'},
                {'operator': 'not', 'expression': {'operator': 'always'}}]},
            'condition': 'Work selects the typed pilot.'}
    return [{'kind': 'put-routing-fact', 'fact': fact, 'rationale': 'Declare selection.'},
            {'kind': 'remove-routing-fact', 'fact': fact['id'], 'rationale': 'Remove selection.'},
            {'kind': 'put-routing-rule', 'rule': rule, 'rationale': 'Route selection.'},
            {'kind': 'remove-routing-rule', 'rule': rule['id'], 'rationale': 'Remove route.'}]


class TypedRoutingEditsTest(unittest.TestCase):
    def test_routing_serialization_requires_no_inner_json_decode(self):
        for raw in routing_edits():
            with self.subTest(kind=raw['kind']):
                expected = json.loads(json.dumps(raw, sort_keys=True, ensure_ascii=False))
                edit = logical._edit(raw)
                with patch.object(logical.json, 'loads', side_effect=AssertionError('routing payload decoded')):
                    self.assertEqual(edit.as_contract(), expected)
                    self.assertEqual(edit.facet[-1], raw['fact']['id'] if isinstance(raw.get('fact'), dict)
                                     else raw['rule']['id'] if isinstance(raw.get('rule'), dict)
                                     else raw.get('fact', raw.get('rule')))

    def test_four_edit_variants_derive_their_discriminator_and_facet(self):
        from dataclasses import fields
        from tools.standards_engine.standards_engine import routing_edits as typed
        variants = (typed.PutRoutingFact, typed.RemoveRoutingFact,
                    typed.PutRoutingRule, typed.RemoveRoutingRule)
        for raw, cls in zip(routing_edits(), variants):
            with self.subTest(kind=raw['kind']):
                edit = logical._edit(raw)
                self.assertIs(type(edit), cls)
                self.assertNotIsInstance(edit, logical.StructuredEdit)
                self.assertEqual(edit.kind, raw['kind'])
                self.assertEqual({f.name for f in fields(edit)},
                                 {'fact' if 'fact' in raw else 'rule', 'rationale'})
                self.assertFalse(hasattr(edit, 'payload'))
                with self.assertRaises(TypeError):
                    cls(**{**{f.name: getattr(edit, f.name) for f in fields(edit)}, 'kind': 'contradictory'})

    def test_fact_and_rule_declarations_are_deeply_detached_and_immutable(self):
        from dataclasses import FrozenInstanceError
        for raw in (routing_edits()[0], routing_edits()[2]):
            with self.subTest(kind=raw['kind']):
                expected = deepcopy(raw)
                edit = logical._edit(raw)
                value = edit.fact if 'fact' in raw else edit.rule
                with self.assertRaises(FrozenInstanceError):
                    value.id = 'routing.changed'
                if 'fact' in raw:
                    raw['fact']['values'].append('new')
                    self.assertIsInstance(value.values, tuple)
                    with self.assertRaises(TypeError):
                        value.values[0] = 'new'
                else:
                    raw['rule']['when']['expressions'][0]['value'] = 'new'
                    with self.assertRaises(TypeError):
                        value.when['operator'] = 'changed'
                    with self.assertRaises(TypeError):
                        value.when['expressions'][0]['value'] = 'changed'
                wire = edit.as_contract()
                self.assertEqual(wire, expected)
                if 'fact' in wire:
                    wire['fact']['values'].append('changed')
                else:
                    wire['rule']['when']['expressions'][0]['value'] = 'changed'
                self.assertEqual(edit.as_contract(), expected)

    def test_complete_canonical_map_order_and_authored_array_order_match(self):
        for raw in routing_edits():
            expected = json.loads(json.dumps(raw, sort_keys=True, ensure_ascii=False))
            value = logical._edit(raw).as_contract()
            self.assertEqual(json.dumps(value, ensure_ascii=False), json.dumps(expected, ensure_ascii=False))
        fact = logical._edit(routing_edits()[0])
        self.assertEqual(fact.as_contract()['fact']['values'], ['z', 'a'])

    def test_expression_data_is_preserved_not_normalized_or_evaluated(self):
        expressions = [
            {'operator': 'always'},
            {'operator': 'equals', 'fact': 'routing.not-yet-declared', 'value': None},
            {'operator': 'in', 'fact': 'routing.future', 'values': [1, True, '1', None]},
            {'operator': 'future-operator', 'extension': {'$ref': 'literal', 'a': [{'z': 3, 'b': False}]}},
        ]
        for expression in expressions:
            raw = routing_edits()[2]
            raw['rule']['when'] = expression
            with patch.object(logical, 'compile_fact_schema', side_effect=AssertionError('early semantics')):
                edit = logical._edit(raw)
            self.assertEqual(edit.as_contract(), raw)
            self.assertEqual(json.dumps(edit.as_contract(), sort_keys=True), json.dumps(raw, sort_keys=True))

    def test_semantic_fact_fields_remain_unbound_until_projection(self):
        for field, value in (('type', 'future-type'), ('nullable', 'not-a-boolean'),
                             ('values', ['duplicate', 'duplicate']), ('aliases', ['not a semantic ID']),
                             ('type', {'nested': ['not a scalar']})):
            raw = routing_edits()[0]
            raw['fact'][field] = value
            with patch.object(logical, 'compile_fact_schema', side_effect=AssertionError('early semantics')):
                edit = logical._edit(raw)
            self.assertEqual(edit.as_contract(), raw)
            if isinstance(value, dict):
                value['nested'].append('mutated')
                self.assertNotEqual(edit.as_contract(), raw)

    def test_original_parse_checks_and_error_owner_remain(self):
        cases = []
        raw = routing_edits()[0]; raw.pop('rationale'); cases.append((raw, 'AUTHORING.INVALID_ARGUMENTS'))
        raw = routing_edits()[0]; raw['fact']['semantic_revision'] = 1.0; cases.append((raw, 'AUTHORING.INVALID_SEMANTIC_REVISION'))
        raw = routing_edits()[0]; raw['fact']['semantic_revision'] = True; cases.append((raw, 'AUTHORING.INVALID_SEMANTIC_REVISION'))
        raw = routing_edits()[0]; raw['fact']['meaning'] = ' '; cases.append((raw, 'AUTHORING.INVALID_ARGUMENTS'))
        raw = routing_edits()[2]; raw['rule']['condition'] = 'two\nlines'; cases.append((raw, 'AUTHORING.INVALID_ARGUMENTS'))
        raw = routing_edits()[2]; raw['rule']['when'] = []; cases.append((raw, 'AUTHORING.INVALID_ARGUMENTS'))
        raw = routing_edits()[3]; raw['rule'] = '../unknown'; cases.append((raw, 'AUTHORING.INVALID_CANONICAL_ID'))
        for raw, code in cases:
            with self.subTest(raw=raw), self.assertRaises(logical.AuthoringError) as error:
                logical._edit(raw)
            self.assertEqual(error.exception.failure.code, code)

    def test_facet_conflicts_and_change_set_order_are_unchanged(self):
        from tools.standards_engine.tests.test_logical_authoring import _EVIDENCE
        purpose = {'summary': 'Typed pilot', 'rationale': 'Exercise only the authored value.', 'evidence': [_EVIDENCE]}
        edits = routing_edits()
        for pair in (edits[:2], edits[2:]):
            with self.assertRaises(logical.AuthoringError) as error:
                logical.StandardsChangeSet.from_mapping({'purpose': purpose, 'edits': pair})
            self.assertEqual(error.exception.failure.code, 'AUTHORING.DUPLICATE_EDIT')
        valid = [edits[0], edits[2]]
        first = logical.StandardsChangeSet.from_mapping({'purpose': purpose, 'edits': valid})
        second = logical.StandardsChangeSet.from_mapping({'purpose': purpose, 'edits': valid[::-1]})
        self.assertEqual(first.as_contract(), second.as_contract())
        self.assertEqual([logical._canonical_json(e.as_contract()) for e in first.edits],
                         sorted(logical._canonical_json(e) for e in valid))

    def test_routing_classification_and_module_attribution_need_no_serialization(self):
        from tools.standards_engine.standards_engine.routing_edits import PutRoutingFact, PutRoutingRule
        from tools.standards_engine.tests.test_logical_authoring import _EVIDENCE
        change = logical.StandardsChangeSet.from_mapping({'purpose': {'summary': 'Pilot', 'rationale': 'Test', 'evidence': [_EVIDENCE]},
                                                         'edits': [routing_edits()[0], routing_edits()[2]]})
        with patch.object(PutRoutingFact, 'as_contract', side_effect=AssertionError('classification serialized')), \
             patch.object(PutRoutingRule, 'as_contract', side_effect=AssertionError('classification serialized')):
            self.assertEqual([logical._edit_kind(e) for e in change.edits], ['put-routing-fact', 'put-routing-rule'])
            self.assertEqual(logical._analysis_module_ids(logical.LogicalProgram((change,))), ('router',))

    def test_other_structured_edit_families_keep_their_existing_representation(self):
        raw = {'kind': 'audit-policy-unit', 'policy': 'topic.example', 'rationale': 'Review coverage.'}
        edit = logical._edit(raw)
        self.assertIs(type(edit), logical.StructuredEdit)
        self.assertEqual(edit.as_contract(), raw)
        self.assertIsInstance(edit.payload, str)

    def test_authored_equality_preserves_boolean_integer_and_null_distinctions(self):
        raw = routing_edits()[2]
        raw['rule']['when'] = {'operator': 'equals', 'fact': 'routing.future', 'value': True}
        boolean = logical._edit(raw)
        raw['rule']['when']['value'] = 1
        integer = logical._edit(raw)
        self.assertNotEqual(boolean, integer)
        raw['rule']['when']['value'] = None
        self.assertNotEqual(logical._edit(raw), integer)
        self.assertEqual(logical._edit(deepcopy(raw)), logical._edit(raw))
        first = routing_edits()[0]
        second = deepcopy(first); second['fact']['nullable'] = 0
        self.assertNotEqual(logical._edit(first), logical._edit(second))
        with self.assertRaises(TypeError):
            logical._edit(raw).rule.when['value'] = False
