"""Literal semantic oracles and canonical-vs-focused binding differentials."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import json
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_applicability.standards_applicability import (
    ApplicabilityError, FactSchema, Truth, compile_fact_schema,
)
from tools.standards_applicability.tests.test_applicability import declaration
from tools.standards_contracts.standards_contracts import ContractError, schema_closure
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine.routing_inputs import bind_facts, fact_assertions, binding_rejection
from tools.standards_engine.standards_engine.tools import AgentToolFacade

ROOT = Path(__file__).resolve().parents[3]
SPECS = [
    {'id': 'enabled', 'type': 'boolean', 'nullable': False, 'aliases': ['on']},
    {'id': 'mode', 'type': 'enum', 'nullable': False, 'values': ['x', 'y'], 'aliases': []},
    {'id': 'text', 'type': 'string', 'nullable': True, 'aliases': []},
    {'id': 'names', 'type': 'string-set', 'nullable': False, 'aliases': []},
    {'id': 'tags', 'type': 'enum-set', 'nullable': True, 'values': ['x', 'y'], 'aliases': []},
    {'id': 'artifact', 'type': 'canonical-id', 'nullable': False, 'aliases': []},
]


class RoutingFactInputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = AgentToolFacade.load_interface(ROOT)
        cls.definitions = cls.interface.schema['$defs']
        cls.assertion_validator = Draft202012Validator(schema_closure(
            cls.definitions['RoutingFactAssertions'], cls.definitions))
        cls.canonical_validator = Draft202012Validator(schema_closure(cls.definitions['FactSet'], cls.definitions))
        cls.schema = compile_fact_schema(declaration(SPECS))

    def test_all_six_types_and_states_match_final_canonical_validity(self):
        values = (True, False, None, '', 'x', 'unknown', 'known-absent', 'x.y', [], ['x'],
                  ['y', 'x'], ['x', 'x'], [''], 0, 1, 1.5, {}, {'state': 'known-absent'},
                  {'state': 'unknown'}, {'state': 'known'}, {'state': 'unknown', 'value': None})
        successes = 0
        for definition in SPECS:
            for raw in values:
                name = definition['id']
                focused = {name: raw}
                canonical = {name: {'type': definition['type'], **raw} if isinstance(raw, dict)
                             else {'type': definition['type'], 'state': 'known', 'value': raw}}
                def observe(validator, data, binder):
                    if not validator.is_valid(data):
                        return None
                    try:
                        return {k: v.as_contract() for k, v in binder(data).canonical_values.items()}
                    except ApplicabilityError:
                        return None
                with self.subTest(fact=name, raw=raw):
                    old = observe(self.canonical_validator, canonical, self.schema.bind)
                    new = observe(self.assertion_validator, focused, lambda data: bind_facts(self.schema, data))
                    self.assertEqual(old is not None, new is not None)
                    if new is not None:
                        successes += 1
                        self.assertEqual(old, new)
                        # Actual generated decode is a second boundary, not just a
                        # hand-built schema validator used by this differential.
                        decoded = c.RouteCall.from_value({'facts': focused}).as_contract()['facts']
                        self.assertEqual(fact_assertions(bind_facts(self.schema, decoded)),
                                         fact_assertions(bind_facts(self.schema, focused)))
        self.assertEqual(successes, 33)

    def test_literal_state_and_exists_semantics(self):
        cases = [({}, 'text', {}, Truth.UNKNOWN),
                 ({'enabled': False}, 'enabled', {'enabled': {'type':'boolean','state':'known','value':False}}, Truth.TRUE),
                 ({'names': []}, 'names', {'names': {'type':'string-set','state':'known','value':[]}}, Truth.TRUE),
                 ({'text': None}, 'text', {'text': {'type':'string','state':'known','value':None}}, Truth.TRUE),
                 ({'text': {'state':'known-absent'}}, 'text', {'text': {'type':'string','state':'known-absent'}}, Truth.FALSE),
                 ({'text': {'state':'unknown'}}, 'text', {'text': {'type':'string','state':'unknown'}}, Truth.UNKNOWN)]
        for data, name, expected, truth in cases:
            with self.subTest(data=data):
                bound = bind_facts(self.schema, data)
                self.assertEqual({k:v.as_contract() for k,v in bound.canonical_values.items()}, expected)
                result = self.schema.compile({'operator':'exists','fact':name}).evaluate(bound)
                self.assertIs(result.truth, truth)
                self.assertEqual(result.unresolved_facts, (name,) if truth is Truth.UNKNOWN else ())
                self.assertEqual(fact_assertions(bound), data)
        self.assertEqual(fact_assertions(bind_facts(self.schema, {'text':'unknown'})), {'text':'unknown'})

    def test_binding_once_preserves_alias_collision_and_normalization(self):
        original = FactSchema.bind
        with patch.object(FactSchema, 'bind', autospec=True, side_effect=original) as bind:
            facts = bind_facts(self.schema, {'on':True, 'tags':['y','x'], 'text':'e\u0301'})
            self.assertEqual(bind.call_count, 1)
        self.assertEqual(fact_assertions(facts), {'enabled': True, 'tags':['x','y'], 'text':'é'})
        for values in ({'enabled':True,'on':True},{'enabled':False,'on':{'state':'unknown'}}):
            with self.assertRaises(ApplicabilityError) as caught:
                bind_facts(self.schema, values)
            self.assertEqual(caught.exception.failure.message, 'a fact and its alias cannot both be supplied')
            self.assertEqual(caught.exception.failure.code, 'APPLICABILITY.INVALID')

    def test_returned_containers_are_independent_and_input_not_mutated(self):
        data = {'tags':['y','x'],'text':{'state':'unknown'}}
        before = deepcopy(data)
        bound = bind_facts(self.schema, data)
        first = fact_assertions(bound)
        first['tags'].append('foreign')
        first['text']['state'] = 'known-absent'
        self.assertEqual(fact_assertions(bound), {'tags':['x','y'],'text':{'state':'unknown'}})
        self.assertEqual(data, before)
        data['tags'].append('foreign')
        self.assertEqual(fact_assertions(bound)['tags'], ['x','y'])

    def test_static_grammar_rejects_old_envelopes_numbers_and_arbitrary_objects(self):
        for value in ({'type':'string','state':'known','value':'x'}, {'state':'known'},
                      {'state':'unknown','value':None},{'arbitrary':False},1,1.0,[],[1]):
            # The empty array is valid common syntax; the snapshot rejects it
            # specifically for a string fact.
            if value == []:
                self.assertTrue(self.assertion_validator.is_valid({'text':value}))
                continue
            with self.subTest(value=value), self.assertRaises(ContractError):
                c.RouteCall.from_value({'facts':{'text':value}})
        with self.assertRaises(ContractError):
            c.RouteCall.from_value({})
        c.RouteCall.from_value({'facts':{}})

    def test_dynamic_rejections_are_safe_and_precisely_located(self):
        cases = [({'tags':'SECRET'}, '/facts/tags', True, 'set fact value must contain unique strings'),
                 ({'enabled':None}, '/facts/enabled', True, 'fact is not nullable'),
                 ({'mode':'SECRET'}, '/facts/mode', True, 'enum fact value is outside its domain'),
                 ({'UNKNOWN_SECRET':True}, '/facts', False, 'fact is not declared by the applicability schema')]
        for values, pointer, exact, message in cases:
            with self.subTest(values=values), self.assertRaises(ApplicabilityError) as caught:
                bind_facts(self.schema, values)
            for purpose in ('authoring','application'):
                result = binding_rejection(purpose, self.schema, values, caught.exception).as_contract()
                self.assertEqual(result['outcome'], 'invalid')
                self.assertEqual(result['code'], 'ROUTE.INPUT_INVALID' if purpose=='authoring' else 'APPLICATION.INPUT_INVALID')
                self.assertEqual(result['input_feedback']['issues'], [{'instance_pointer':pointer,
                    'location_exact':exact,'keyword':'fact','message':message}])
                self.assertEqual(result['input_feedback']['describe_input'], {'operation':'route'})
                self.assertNotIn('SECRET',json.dumps(result))

    def test_resolution_errors_precede_later_binding_pass_without_fabricating_facts(self):
        with self.assertRaises(ApplicabilityError) as caught:
            bind_facts(self.schema, {'tags':'bad','UNKNOWN':False})
        self.assertEqual(caught.exception.failure.field, 'UNKNOWN')
        self.assertEqual(caught.exception.failure.message, 'fact is not declared by the applicability schema')
        with self.assertRaises(ApplicabilityError) as caught:
            bind_facts(self.schema, {'tags':'bad','mode':'bad'})
        self.assertEqual(caught.exception.failure.field, 'tags')

    def test_normalized_set_collisions_fail_the_focused_contract_without_changing_native_binding(self):
        value = {'names': ['e\u0301', 'é']}
        c.RouteCall.from_value({'facts': value})  # Distinct raw strings are static-valid.
        native = self.schema.bind({'names': {'type': 'string-set', 'state': 'known', 'value': value['names']}})
        self.assertEqual(native.canonical_values['names'].value, ('é', 'é'))
        with self.assertRaises(ContractError) as caught:
            bind_facts(self.schema, value)
        result = binding_rejection('authoring', self.schema, value, caught.exception).as_contract()
        self.assertEqual(result['code'], 'ROUTE.INPUT_INVALID')
        self.assertEqual(result['input_feedback']['issues'][0]['instance_pointer'], '/facts/names')
        self.assertIn('Unicode normalization', result['input_feedback']['issues'][0]['message'])
        self.assertEqual(fact_assertions(bind_facts(self.schema, {'names': ['e\u0301']})), {'names':['é']})

    def test_feedback_pointer_is_bounded_and_escapes_registered_names(self):
        for name, pointer, exact in (('a/b~c', '/facts/a~1b~0c', True), ('a' * 600, '/facts', False)):
            schema = compile_fact_schema(declaration([{'id':name,'type':'boolean','nullable':False,'aliases':[]}]))
            data = {name: 'not-a-boolean'}
            with self.assertRaises(ApplicabilityError) as caught:
                bind_facts(schema, data)
            result = binding_rejection('authoring', schema, data, caught.exception).as_contract()
            issue = result['input_feedback']['issues'][0]
            self.assertEqual(issue['instance_pointer'], pointer)
            self.assertEqual(issue['location_exact'], exact)
