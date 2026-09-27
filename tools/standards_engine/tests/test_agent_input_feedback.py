"""Field feedback is safe, discoverable and returned before domain effects."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.tests.test_mcp import initialize, request

ROOT = Path(__file__).resolve().parents[3]


class AgentInputFeedbackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = StandardsEngine.open_repository(ROOT, durable=False, purpose='authoring')
        cls.interface = _contracts(ROOT)
        cls.facade = AgentToolFacade(cls.engine, cls.interface)

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_empty_proposal_names_fields_and_never_dispatches_or_captures(self):
        arguments = {'change_set': {}}
        with patch.object(self.engine, 'propose', side_effect=AssertionError('domain mutation')), \
             patch.object(self.engine, 'create_snapshot', side_effect=AssertionError('snapshot')):
            result = self.facade.propose(arguments)
        self.assertEqual(arguments, {'change_set': {}})
        self.assertEqual(result['code'], 'INTERFACE.INVALID_ARGUMENTS')
        feedback = result['input_feedback']
        self.assertEqual([i['instance_pointer'] for i in feedback['issues']],
                         ['/change_set/purpose', '/change_set/edits'])
        self.assertEqual(feedback['describe_input'], {'operation': 'propose'})
        discovery = self.facade.describe_input(feedback['describe_input'])
        self.assertEqual(discovery['operation'], 'propose')
        self.assertEqual(discovery['kind'], 'input-contract-result')
        self.interface.validate('RejectedResult', result)

    def test_all_five_authoring_operations_expose_their_own_help_without_dispatch(self):
        for name in ('propose', 'revise', 'resolve_workflow', 'resolve_many', 'review'):
            with self.subTest(operation=name), patch.object(self.engine, name, side_effect=AssertionError('mutation')):
                result = getattr(self.facade, name)({})
                self.assertEqual(result['input_feedback']['describe_input'], {'operation': name})
                self.assertTrue(result['input_feedback']['issues'])
                self.interface.validate('RejectedResult', result)

    def test_empty_edits_have_an_exact_minimum_constraint(self):
        example = next(e['value'] for e in json.loads((ROOT / 'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples'] if e['definition'] == 'ProposeCall')
        arguments = deepcopy(example)
        arguments['change_set']['edits'] = []
        with patch.object(self.engine, 'propose', side_effect=AssertionError('mutation')):
            result = self.facade.propose(arguments)
        issue = next(i for i in result['input_feedback']['issues'] if i['instance_pointer'] == '/change_set/edits')
        self.assertEqual(issue['keyword'], 'minItems')
        self.assertEqual(issue['message'], 'Satisfy minItems = 1.')

    def test_non_object_arguments_have_help_without_echo(self):
        result = self.facade.propose('SECRET_VALUE')
        self.assertEqual(result['input_feedback']['describe_input'], {'operation': 'propose'})
        self.assertNotIn('SECRET', json.dumps(result))

    def test_application_feedback_is_purpose_qualified_and_disabled_operations_stay_hidden(self):
        with StandardsEngine.open_repository(ROOT, durable=False, purpose='application') as engine:
            facade = AgentToolFacade(engine, self.interface)
            result = facade.related({})
            self.assertEqual(result['kind'], 'application-rejected-result')
            self.assertEqual(result['input_feedback']['describe_input'], {'operation': 'related'})
            self.assertEqual(facade.propose({})['code'], 'APPLICATION.OPERATION_UNAVAILABLE')
            self.assertNotIn('input_feedback', facade.propose({}))
            self.interface.validate('ApplicationRejectedResult', result)

    def test_mcp_envelope_is_error_and_metadata_observers_use_safe_feedback(self):
        for purpose in ('authoring', 'application'):
            server = MCPServer(ROOT, purpose=purpose, schema_mode='native')
            self.addCleanup(server.close)
            initialize(server)
            for operation, arguments in (('runtime_info', {'expected_catalog': 'SECRET'}),
                                         ('describe_input', {}), ('related', {})):
                result = server.dispatch(request('tools/call', {'name': operation, 'arguments': arguments}))['result']
                self.assertTrue(result['isError'], result)
                value = result['structuredContent']
                self.assertEqual(value['input_feedback']['describe_input'], {'operation': operation})
                self.assertNotIn('SECRET', json.dumps(value))
                self.assertEqual(json.loads(result['content'][0]['text']), value)

    def test_request_evidence_binding_errors_keep_specific_safe_feedback(self):
        from tools.standards_engine.tests.test_request_evidence import shared
        example = next(e['value'] for e in json.loads((ROOT / 'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples'] if e['definition'] == 'ProposeCall')
        args = shared(deepcopy(example))
        name = next(iter(args['evidence']))
        args['evidence']['UNUSED_SECRET_NAME'] = args['evidence'][name]
        result = self.facade.propose(args)
        issue = result['input_feedback']['issues'][0]
        self.assertEqual(issue['instance_pointer'], '/evidence')
        self.assertEqual(issue['message'], 'Every request evidence entry must be explicitly used.')
        self.assertNotIn('UNUSED_SECRET_NAME', json.dumps(result))
        args['evidence'].pop(name)
        result = self.facade.propose(args)
        issue = result['input_feedback']['issues'][0]
        self.assertTrue(issue['instance_pointer'].endswith('/evidence_ref'))
        self.assertEqual(issue['message'], 'An evidence_ref does not name an entry in this request.')

    def test_unsupported_handle_does_not_echo_arbitrary_version_payload(self):
        result = self.facade.read({'snapshot': {'kind': 'snapshot-handle', 'schema_version': 'SECRET_VERSION'}, 'target': 'core'})
        self.assertEqual(result['code'], 'INTERFACE.UNSUPPORTED_VERSION')
        self.assertNotIn('SECRET_VERSION', json.dumps(result))
