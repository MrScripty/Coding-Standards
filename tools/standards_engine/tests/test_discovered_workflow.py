"""Real workflow uses independently validated discovered input contracts.

This is a deterministic consumer, not model-visible client qualification. The
opt-in Codex harness observes that separate boundary with model-authored calls.
"""
import json
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
        for mode in ('compatibility', 'native'):
            with self.subTest(mode=mode):
                server = MCPServer(self.root, purpose='authoring', schema_mode=mode)
                self.addCleanup(server.close)
                initialize(server)
                validators = {}
                def call(operation, arguments):
                    if operation in validators:
                        validators[operation].validate(arguments)
                    output = server.dispatch(request('tools/call', {'name': operation, 'arguments': arguments}))['result']
                    self.assertFalse(output['isError'], output)
                    return output['structuredContent']

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

                before = subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'main'])
                change = topic_change(self.root, 'discovered-' + mode, 3)
                original = call('propose', shared({'change_set': change}))
                self.assertEqual(original['status'], 'needs-action', original)
                # Add a reference artifact in a revision; the same three topic
                # decisions remain explicit and are bound to the new Analysis.
                revised = call('revise', shared({'context': original['context'],
                    'change_set': reference_change(self.root, 'discovered-extra-' + mode)}))
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
