"""Qualification checker tests use synthetic events, not claimed model evidence."""
from copy import deepcopy
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine.context_projection import Purpose
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.codex_discovery_client import (
    AUTHORING_OPERATIONS, _arguments_visible, _matches_readback, assess_model_items as _assess_model_items, main, model_observations,
)

ROOT = Path(__file__).resolve().parents[3]
DIALECT = 'https://json-schema.org/draft/2020-12/schema'
RUNTIME = {'instance_id': 'fixture-instance', 'purpose': 'authoring',
           'catalog_digest': 'sha256:' + 'a' * 64, 'schema_digest': 'sha256:' + 'b' * 64,
           'implementation_digest': 'sha256:' + 'c' * 64, 'interface_version': 40}


def assess_model_items(items, server, catalog, contracts, **kwargs):
    return _assess_model_items(items, server, catalog, contracts, RUNTIME, **kwargs)


def observed_fixture():
    # Deliberately permissive schemas isolate event/completion checks. Production
    # schema conformance is independently tested in test_input_discovery and the
    # real workflow test; these events are never published as client acceptance.
    names = (*AUTHORING_OPERATIONS, 'describe_input', 'apply', 'recover')
    catalog = {name: {'inputSchema': {'type': 'object'}, 'outputSchema': {'type': 'object'}} for name in names}
    definition = {'type': 'object', 'properties': {
        'evidence': {'type': 'object'}, 'evidence_ref': {'type': 'string'},
        'submissions': {'type': 'array', 'items': {'$ref': '#/$defs/FixtureItem'}}},
        'additionalProperties': False}
    definitions = {'FixtureCall': definition, 'FixtureItem': {'type': 'object'}}
    contracts = {name: {'$schema': DIALECT, '$ref': '#/$defs/FixtureCall', '$defs': definitions} for name in names}
    events = []
    def add(name, args, value):
        events.append({'id': str(len(events)), 'type': 'mcpToolCall', 'server': 'fixture',
            'tool': name, 'arguments': args, 'status': 'completed', 'error': None,
            'result': {'structuredContent': value, 'isError': False,
                       '_meta': {'standards-engine/runtime': deepcopy(RUNTIME)}}})
    for name in AUTHORING_OPERATIONS:
        add('describe_input', {'operation': name}, {'kind': 'input-contract-result', 'root': 'FixtureCall', 'operation': name,
            'purpose': 'authoring', 'catalog_digest': RUNTIME['catalog_digest'],
            'interface_version': 40, 'dialect': DIALECT, 'records': [{'name': key, 'schema_json': json.dumps(value)} for key, value in definitions.items()]})
        args = {'evidence': {'review': {}}, 'evidence_ref': 'review'}
        if name == 'resolve_many':
            args['submissions'] = [{}, {}]
        add(name, args, {'kind': 'workflow-result', 'status': 'ready' if name == 'review' else 'complete'})
    return catalog, events, contracts


class ModelDiscoveryQualificationTest(unittest.TestCase):
    def test_exact_output_definition_can_supply_shared_input_knowledge(self):
        from tools.standards_engine.standards_engine.contract_discovery import output_schema_digest
        catalog, items, contracts = observed_fixture()
        for item in items:
            if item['tool']=='describe_input':
                item['result']['structuredContent']['records']=[r for r in item['result']['structuredContent']['records'] if r['name']!='FixtureItem']
        root={'type':'object','properties':{'shared':{'$ref':'#/$defs/FixtureItem'}}}
        schema={**root,'$defs':{'FixtureItem':{'type':'object'}}}
        catalog['review']['outputSchema']=schema
        catalog['describe_output']={'inputSchema':{'type':'object'},'outputSchema':{'type':'object'}}
        out=deepcopy(items[0]);out.update(id='output-discovery',tool='describe_output',arguments={'operation':'review'})
        out['result']['structuredContent']={'kind':'output-contract-result','purpose':'authoring',
            'catalog_digest':RUNTIME['catalog_digest'],'interface_version':40,'operation':'review',
            'schema_digest':output_schema_digest(schema),'root_schema_json':json.dumps(root),
            'records':[{'name':'FixtureItem','schema_json':'{"type":"object"}'}]}
        result=assess_model_items([out]+items,'fixture',catalog,contracts)
        self.assertEqual(result['status'],'passed',result)
        out['result']['structuredContent']['records'][0]['schema_json']='{"type":"string"}'
        self.assertEqual(assess_model_items([out]+items,'fixture',catalog,contracts)['status'],'failed')

    def test_on_demand_results_use_independent_observer_validation(self):
        catalog, items, contracts = observed_fixture()
        validation = {name: tool.pop('outputSchema') for name, tool in catalog.items()}
        result = assess_model_items(items, 'fixture', catalog, contracts, output_contracts=validation)
        self.assertEqual(result['status'], 'passed', result)
        changed = deepcopy(items)
        changed[-1]['result']['structuredContent'] = 'invalid-result'
        result = assess_model_items(changed, 'fixture', catalog, contracts, output_contracts=validation)
        self.assertEqual(result['status'], 'failed', result)

    def test_on_demand_observation_requires_explicit_output_validation(self):
        catalog, items, contracts = observed_fixture()
        for tool in catalog.values():
            tool.pop('outputSchema')
        with self.assertRaises((KeyError, ValueError)):
            assess_model_items(items, 'fixture', catalog, contracts)

    def test_complete_observed_sequence_passes_but_self_report_does_not(self):
        catalog, events, contracts = observed_fixture()
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertEqual(result['status'], 'passed', result)
        self.assertGreater(result['request_json_bytes'], 0)
        self.assertEqual(result['calls']['describe_input'], 5)
        self.assertEqual(assess_model_items([{'id': '1', 'type': 'agentMessage', 'text': 'All checks passed.'}], 'fixture', catalog, contracts)['status'], 'failed')

    def test_missing_discovery_foreign_tools_and_unrecognized_surfaces_fail(self):
        catalog, base, contracts = observed_fixture()
        for extra in ({'id': 'other', 'type': 'commandExecution'},
                      {'id': 'other', 'type': 'fileChange'},
                      {'id': 'other', 'type': 'webSearch'},
                      {'id': 'other', 'type': 'unrecognizedFutureClientSurface'}):
            self.assertEqual(assess_model_items(base+[extra], 'fixture', catalog, contracts)['status'], 'failed')
        self.assertEqual(assess_model_items(base[1:], 'fixture', catalog, contracts)['status'], 'failed')
        changed = deepcopy(base); changed[1]['server'] = 'production'
        self.assertEqual(assess_model_items(changed, 'fixture', catalog, contracts)['status'], 'failed')

    def test_repair_calls_invalid_shapes_and_publication_fail(self):
        catalog, base, contracts = observed_fixture()
        cases = []
        cases.append(base + [{**base[1], 'id': 'retry'}])
        bad = deepcopy(base); bad[1]['result']['isError'] = True; cases.append(bad)
        bad = deepcopy(base); bad[1]['result']['structuredContent']['status'] = 'rejected'; cases.append(bad)
        bad = deepcopy(base); bad[1]['arguments'] = 'not structured'; cases.append(bad)
        bad = deepcopy(base); bad[-1]['result']['structuredContent']['status'] = 'complete'; cases.append(bad)
        bad = deepcopy(base); bad[-3]['arguments']['submissions'] = [{}]; cases.append(bad)
        bad = deepcopy(base); bad[-1]['arguments'].pop('evidence'); cases.append(bad)
        cases.append(base + [{**base[1], 'id': 'publication', 'tool': 'apply'}])
        for case in cases:
            self.assertEqual(assess_model_items(case, 'fixture', catalog, contracts)['status'], 'failed')

    def test_used_definitions_are_required_but_unrelated_union_choices_are_not(self):
        definitions = {
            'Choice': {'oneOf': [{'$ref': '#/$defs/Alpha'}, {'$ref': '#/$defs/Beta'}]},
            'Alpha': {'type': 'object', 'properties': {'kind': {'const': 'alpha'},
                      'value': {'$ref': '#/$defs/Text'}}, 'required': ['kind', 'value']},
            'Beta': {'type': 'object', 'properties': {'kind': {'const': 'beta'}}, 'required': ['kind']},
            'Text': {'type': 'string', 'minLength': 1},
        }
        contract = {'$ref': '#/$defs/Choice', '$defs': definitions}
        value = {'kind': 'alpha', 'value': 'observed'}
        selected = {name: definition for name, definition in definitions.items() if name != 'Beta'}
        self.assertTrue(_arguments_visible(contract, value, selected))
        selected.pop('Text')
        self.assertFalse(_arguments_visible(contract, value, selected))
        self.assertFalse(_arguments_visible(contract, value, {'Text': definitions['Text']}))
        # Replacing unread definitions by false could select a different branch
        # of nested oneOf. Coverage follows the original valid branch instead.
        nested = {'Choice': {'oneOf': [{'$ref': '#/$defs/Alpha'}, {'$ref': '#/$defs/Other'}]},
                  'Alpha': {'type': 'integer'}, 'Other': {'oneOf': [
                      {'$ref': '#/$defs/Beta'}, {'$ref': '#/$defs/Gamma'}]},
                  'Beta': {'type': 'integer'}, 'Gamma': {'type': 'integer'}}
        self.assertFalse(_arguments_visible({'$ref': '#/$defs/Choice', '$defs': nested}, 1,
            {key: nested[key] for key in ('Choice', 'Other', 'Beta')}))
        catalog, events, contracts = observed_fixture()
        events[0]['result']['structuredContent']['records'] = [
            record for record in events[0]['result']['structuredContent']['records'] if record['name'] != 'FixtureCall']
        self.assertEqual(assess_model_items(events, 'fixture', catalog, contracts)['status'], 'failed')
        catalog, events, contracts = observed_fixture()
        events[0]['result']['structuredContent']['records'][0]['schema_json'] = '{}'
        self.assertEqual(assess_model_items(events, 'fixture', catalog, contracts)['status'], 'failed')

    def test_readback_checks_body_identity_and_revision_not_summary_text(self):
        revision = {'kind': 'fixture-revision'}
        value = {'kind': 'proposal-read-result', 'revision': revision, 'policy': {'id': 'fixture'},
                 'requires': ['core'], 'specializes': [],
                 'content': '# Title\n\n**Standards metadata**\n\n- ID: `fixture`\n\nExact body.\n'}
        self.assertTrue(_matches_readback(value, revision, 'fixture', 'Title', 'Exact body.'))
        wrong = {**value, 'content': value['content'].replace('Exact body.', 'Different body.'), 'summary': 'Exact body.'}
        self.assertFalse(_matches_readback(wrong, revision, 'fixture', 'Title', 'Exact body.'))
        self.assertFalse(_matches_readback(value, {'kind': 'another-revision'}, 'fixture', 'Title', 'Exact body.'))

    def test_model_turn_requires_explicit_permission_and_executable(self):
        args = ['--model', 'operator-model', '--surface', 'code-mode', '--evidence-dir', '/unused-test-directory']
        with redirect_stderr(io.StringIO()), patch('asyncio.run') as run:
            with self.assertRaises(SystemExit):
                main(args)
            run.assert_not_called()
            with patch('shutil.which', return_value=None), self.assertRaises(SystemExit):
                main([*args, '--allow-model-turn'])
            run.assert_not_called()

    def test_native_facade_identity_and_discovery_share_the_actual_full_catalog(self):
        interface = AgentToolFacade.load_interface(ROOT)
        engine = SimpleNamespace(purpose=Purpose.AUTHORING, _repository=SimpleNamespace(root=ROOT))
        facade = AgentToolFacade(engine, interface)
        runtime = facade.runtime_info({})
        discovered = facade.describe_input({'operation': 'query'})
        self.assertEqual(discovered['kind'], 'input-contract-result')
        self.assertEqual(runtime['catalog_digest'], discovered['catalog_digest'])
        self.assertEqual(facade.describe_input({'operation': 'query', 'selector': discovered['root'],
            'expected_catalog': runtime['catalog_digest']})['kind'], 'input-contract-result')


class SharedDiscoveryQualificationTest(unittest.TestCase):
    def shared_fixture(self):
        catalog, events, contracts = observed_fixture()
        # Acquire the batch element once during propose. Later operations still
        # discover their root; common definitions do not need retransmission.
        for event in events[2:]:
            if event['tool'] == 'describe_input':
                event['result']['structuredContent']['records'] = [
                    r for r in event['result']['structuredContent']['records']
                    if r['name'] != 'FixtureItem']
        return catalog, events, contracts

    def test_prior_shared_definition_is_usable_by_later_operation(self):
        catalog, events, contracts = self.shared_fixture()
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertEqual(result['status'], 'passed', result)
        self.assertEqual(result['observer_version'], 2)
        self.assertEqual(result['calls']['describe_input'], 5)

    def test_never_discovered_shared_definition_is_rejected_at_use(self):
        catalog, events, contracts = self.shared_fixture()
        events[0]['result']['structuredContent']['records'].pop()
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertIn('resolve_many: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_later_discovery_cannot_retroactively_satisfy_a_call(self):
        catalog, events, contracts = self.shared_fixture()
        record = events[0]['result']['structuredContent']['records'].pop()
        events[-2]['result']['structuredContent']['records'].append(record)
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertIn('resolve_many: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_same_name_changed_definition_is_not_credited(self):
        catalog, events, contracts = self.shared_fixture()
        events[0]['result']['structuredContent']['records'][-1]['schema_json'] = '{"type":"string"}'
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertIn('An observed discovery record differed from the installed contract.', result['failures'])
        self.assertIn('resolve_many: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_foreign_source_purpose_catalog_or_instance_is_not_credited(self):
        catalog, events, contracts = self.shared_fixture()
        for key in RUNTIME:
            with self.subTest(field=key):
                altered = deepcopy(events)
                altered[0]['result']['_meta']['standards-engine/runtime'][key] = 'foreign'
                result = assess_model_items(altered, 'fixture', catalog, contracts)
                self.assertIn('Tool result did not match the qualified runtime/source/purpose/catalog.', result['failures'])

    def test_discovery_envelope_must_match_the_operation_and_catalog(self):
        catalog, events, contracts = self.shared_fixture()
        for key in ('root', 'operation', 'dialect', 'purpose', 'catalog_digest', 'interface_version'):
            with self.subTest(field=key):
                altered = deepcopy(events)
                altered[0]['result']['structuredContent'][key] = 'different'
                result = assess_model_items(altered, 'fixture', catalog, contracts)
                self.assertIn('Discovery did not identify the expected operation root.', result['failures'])

    def test_shared_definition_cache_never_survives_an_assessment(self):
        catalog, events, contracts = self.shared_fixture()
        self.assertEqual(assess_model_items(events, 'fixture', catalog, contracts)['status'], 'passed')
        events[0]['result']['structuredContent']['records'].pop()
        self.assertEqual(assess_model_items(events, 'fixture', catalog, contracts)['status'], 'failed')

    def test_compaction_requires_reacquisition_not_assumed_memory(self):
        catalog, events, contracts = self.shared_fixture()
        events.insert(2, {'id': 'compacted', 'type': 'contextCompaction'})
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertIn('resolve_many: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_boolean_and_number_literal_definitions_are_distinct(self):
        contract = {'$ref': '#/$defs/Flag', '$defs': {'Flag': {'const': True}}}
        self.assertFalse(_arguments_visible(contract, True, {'Flag': {'const': 1}}))

    def test_key_order_is_not_a_definition_change(self):
        contract = {'$ref': '#/$defs/Text', '$defs': {'Text': {'type': 'string', 'minLength': 1}}}
        self.assertTrue(_arguments_visible(contract, 'text', {'Text': {'minLength': 1, 'type': 'string'}}))

    def test_discovery_completing_after_action_start_does_not_count(self):
        catalog, items, contracts = self.shared_fixture()
        # Root for propose completes at index zero. A proposal already started
        # before that completion must not be credited with its later arrival.
        starts = {i['id']: n for n, i in enumerate(items)}
        starts[items[1]['id']] = 0
        result = assess_model_items(items, 'fixture', catalog, contracts, started_before=starts)
        self.assertIn('propose: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_observations_keep_one_thread_and_turn_and_require_call_start(self):
        _, items, _ = self.shared_fixture()
        events = []
        for item in items:
            for method in ('item/started', 'item/completed'):
                events.append({'method': method, 'params': {'threadId': 'thread', 'turnId': 'turn', 'item': item}})
        foreign = deepcopy(events[0]); foreign['params']['threadId'] = 'other'
        selected, starts = model_observations([foreign, *events], 'thread', 'turn')
        self.assertEqual(selected, items)
        self.assertEqual(starts, {i['id']: n for n, i in enumerate(items)})
        with self.assertRaisesRegex(ValueError, 'no observed start'):
            model_observations(events[1:], 'thread', 'turn')
        with self.assertRaisesRegex(ValueError, 'duplicate started'):
            model_observations([events[0], *events], 'thread', 'turn')


    def test_started_tools_require_matching_terminal_observations(self):
        _, items, _ = self.shared_fixture()
        def event(method, item):
            return {'method': method, 'params': {'threadId': 'thread', 'turnId': 'turn', 'item': item}}
        with self.assertRaisesRegex(ValueError, 'no completed observation'):
            model_observations([event('item/started', items[0])], 'thread', 'turn')
        with self.assertRaisesRegex(ValueError, 'completion identity differs'):
            model_observations([event('item/started', items[0]),
                event('item/completed', {**items[0], 'tool': 'apply'})], 'thread', 'turn')
        with self.assertRaisesRegex(ValueError, 'completion identity differs'):
            model_observations([event('item/started', items[0]),
                event('item/completed', {'id': items[0]['id'], 'type': 'agentMessage'})], 'thread', 'turn')

    def test_duplicate_schema_members_are_not_credited(self):
        catalog, events, contracts = self.shared_fixture()
        events[0]['result']['structuredContent']['records'][-1]['schema_json'] = '{"type":"string","type":"object"}'
        result = assess_model_items(events, 'fixture', catalog, contracts)
        self.assertIn('An observed discovery record was not complete JSON.', result['failures'])
        self.assertEqual(result['status'], 'failed')
