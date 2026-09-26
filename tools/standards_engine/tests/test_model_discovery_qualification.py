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
    AUTHORING_OPERATIONS, _arguments_visible, _matches_readback, assess_model_items, main,
)

ROOT = Path(__file__).resolve().parents[3]


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
    contracts = {name: {'$ref': '#/$defs/FixtureCall', '$defs': definitions} for name in names}
    events = []
    def add(name, args, value):
        events.append({'id': str(len(events)), 'type': 'mcpToolCall', 'server': 'fixture',
            'tool': name, 'arguments': args, 'status': 'completed', 'error': None,
            'result': {'structuredContent': value, 'isError': False}})
    for name in AUTHORING_OPERATIONS:
        add('describe_input', {'operation': name}, {'kind': 'input-contract-result', 'root': 'FixtureCall', 'records': [{'name': key, 'schema_json': json.dumps(value)} for key, value in definitions.items()]})
        args = {'evidence': {'review': {}}, 'evidence_ref': 'review'}
        if name == 'resolve_many':
            args['submissions'] = [{}, {}]
        add(name, args, {'kind': 'workflow-result', 'status': 'ready' if name == 'review' else 'complete'})
    return catalog, events, contracts


class ModelDiscoveryQualificationTest(unittest.TestCase):
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
