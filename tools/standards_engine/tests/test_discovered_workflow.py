"""Real workflow uses independently validated discovered input contracts.

This is a deterministic consumer, not model-visible client qualification. The
opt-in Codex harness observes that separate boundary with model-authored calls.
"""
import json
import sys
import itertools
from pathlib import Path
import subprocess
import tempfile
import unittest

from jsonschema import Draft202012Validator

from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.tests.test_agent_workflow import decisions, reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_engine.tests.test_request_evidence import shared
from tools.standards_engine.tests.test_review_workflow_ux import topic_change, decision


class DiscoveredWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='discovered-input-workflow-')
        cls.root = Path(cls.temp.name) / 'repository'
        _clone_tracked_worktree(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_discovered_shapes_drive_all_five_authoring_calls_and_preserve_decisions(self):
        for mode, delivery in itertools.product(('compatibility', 'native'), ('eager', 'on-demand')):
            with self.subTest(mode=mode, delivery=delivery):
                server = MCPServer(self.root, purpose='authoring', schema_mode=mode, output_schemas=delivery)
                self.addCleanup(server.close)
                initialize(server)
                validators = {}
                result_validator = None
                def call(operation, arguments):
                    if operation in validators:
                        validators[operation].validate(arguments)
                    selected = request('tools/call', {'name': operation, 'arguments': arguments})
                    if mode == 'native' and delivery == 'on-demand':
                        # The compact catalog path crosses real stdio and replaces
                        # its process on every call; no connection cache is needed.
                        selected['id'] = 2
                        messages = [request('initialize', {'protocolVersion': '2025-11-25',
                            'capabilities': {}, 'clientInfo': {'name': 'output-workflow', 'version': '1'}}),
                            {'jsonrpc': '2.0', 'method': 'notifications/initialized'}, selected]
                        process = subprocess.run([sys.executable, '-m',
                            'tools.standards_engine.standards_engine.mcp', '--repo-root', str(self.root),
                            '--purpose', 'authoring', '--schema-mode', mode, '--output-schemas', delivery],
                            input=''.join(json.dumps(message) + '\n' for message in messages),
                            text=True, capture_output=True, check=True)
                        self.assertEqual(process.stderr, '')
                        reply = next(json.loads(line) for line in process.stdout.splitlines()
                                     if json.loads(line).get('id') == 2)
                        self.assertNotIn('error', reply, reply)
                        output = reply['result']
                    else:
                        output = server.dispatch(selected)['result']
                    self.assertEqual(json.loads(output['content'][0]['text']), output['structuredContent'])
                    self.assertFalse(output['isError'], output)
                    value = output['structuredContent']
                    if operation in validators and result_validator is not None:
                        result_validator.validate(value)
                    return value

                # Schema acquisition uses only the published tool, never generated
                # Python types, filesystem examples or a second schema oracle.
                for operation in ('propose', 'revise', 'resolve_workflow', 'resolve_many', 'review'):
                    args = {'operation': operation, 'limit': 16}
                    documents = {}
                    while True:
                        page = call('describe_input', args)
                        documents.update({d['name']: json.loads(d['schema_json']) for d in page['records']})
                        if 'next' not in page:
                            break
                        args = page['next']
                    validators[operation] = Draft202012Validator({'$schema': page['dialect'],
                        '$ref': '#/$defs/' + page['root'], '$defs': documents})

                # All five focused actions share one canonical result algebra.
                # Retrieve it once; reuse is based on exact schema identity.
                output_args, documents = {'operation':'propose','limit':16}, {}
                while True:
                    page = call('describe_output', output_args)
                    documents.update({r['name']:json.loads(r['schema_json']) for r in page['records']})
                    if 'next' not in page:
                        break
                    output_args = page['next']
                result_validator = Draft202012Validator({**json.loads(page['root_schema_json']), '$defs':documents})
                schema_ids = {t['_meta']['standards-engine/output-schema-digest'] for t in server.tools
                              if t['name'] in validators} if delivery=='on-demand' else {page['schema_digest']}
                self.assertEqual(schema_ids,{page['schema_digest']})
                before = subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'main'])
                change = topic_change(self.root, 'discovered-' + mode + '-' + delivery, 3)
                original = call('propose', shared({'change_set': change}))
                self.assertEqual(original['status'], 'needs-action', original)
                # Add a reference artifact in a revision; the same three topic
                # decisions remain explicit and are bound to the new Analysis.
                revised = call('revise', shared({'context': original['context'],
                    'change_set': reference_change(self.root, 'discovered-extra-' + mode + '-' + delivery)}))
                self.assertEqual(revised['status'], 'needs-action', revised)
                first = decision(self.root, revised['work']['items'][0]['obligation'])
                single = call('resolve_workflow', shared({'context': revised['context'], 'submission': first}))
                self.assertEqual(single['status'], 'needs-action')
                batch_arguments = {'context': single['context'], 'submissions': [
                    decision(self.root, item['obligation']) for item in single['work']['items']]}
                self.assertEqual(len(batch_arguments['submissions']), 2)
                completed = call('resolve_many', shared(batch_arguments))
                ordinary = call('resolve_many', batch_arguments)
                self.assertEqual(completed, ordinary)
                self.assertEqual(completed['status'], 'complete')
                review_arguments = {'context': completed['context'], 'decisions': decisions(self.root)}
                ready = call('review', shared(review_arguments))
                self.assertEqual(ready, call('review', review_arguments))
                self.assertEqual(ready['status'], 'ready')
                self.assertEqual(before, subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'main']))
                server.close()
