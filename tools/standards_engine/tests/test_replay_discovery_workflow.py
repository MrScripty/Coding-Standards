"""Real Engine results in a synthetic client trace; no model qualification claim."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.standards_contracts.standards_contracts import direct_schema_references, local_definition_name
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.tests.codex_discovery_client import fixture_contents
from tools.standards_engine.tests.replay_discovery_qualification import replay
from tools.standards_engine.tests.test_agent_workflow import decisions, reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_engine.tests.test_request_evidence import shared
from tools.standards_engine.tests.test_review_workflow_ux import topic_change, decision
from tools.standards_engine.tests.test_replay_discovery_qualification import TraceWriter

ROOT = Path(__file__).resolve().parents[3]


class ReplayDiscoveryWorkflowTest(unittest.TestCase):
    def test_cold_replay_of_real_discovered_workflow_preserves_evidence_and_main(self):
        self.exercise_delivery('eager')

    def test_on_demand_cold_replay_keeps_validation_without_eager_schemas(self):
        self.exercise_delivery('on-demand')

    def exercise_delivery(self, delivery):
        with tempfile.TemporaryDirectory(prefix='discovery-replay-integration-') as folder:
            evidence_dir = Path(folder) / 'original'; evidence_dir.mkdir()
            fixture = evidence_dir / 'repository'
            _clone_tracked_worktree(fixture)
            main = subprocess.check_output(['git', '-C', str(fixture), 'rev-parse', 'main'], text=True).strip()
            server = MCPServer(fixture, purpose='authoring', schema_mode='native', output_schemas=delivery)
            self.addCleanup(server.close)
            initialize(server)
            trace = TraceWriter()
            trace.rpc('thread/start', {'ephemeral': True, 'model': 'synthetic-no-model'}, {'thread': {'id': 'thread'}})
            toolmap = {tool['name']: tool for tool in server.tools}
            trace.rpc('mcpServerStatus/list', {'threadId': 'thread'}, {'data': [{'name': 'fixture', 'tools': toolmap}]})
            count = 0

            def invoke(name, arguments, *, model=True):
                nonlocal count
                count += 1
                item = {'id': str(count), 'type': 'mcpToolCall', 'server': 'fixture',
                        'tool': name, 'arguments': arguments, 'status': 'inProgress', 'error': None, 'result': None}
                if model:
                    trace.event('item/started', {'threadId': 'thread', 'turnId': 'turn', 'item': deepcopy(item)})
                result = server.dispatch(request('tools/call', {'name': name, 'arguments': arguments}))['result']
                self.assertFalse(result['isError'], result)
                if model:
                    item.update(status='completed', result=result)
                    trace.event('item/completed', {'threadId': 'thread', 'turnId': 'turn', 'item': item})
                else:
                    trace.rpc('mcpServer/tool/call', {'threadId': 'thread', 'server': 'fixture', 'tool': name,
                              'arguments': arguments}, result)
                return result['structuredContent']

            identity = server._runtime_identity.metadata()
            runtime = invoke('runtime_info', {'expected_catalog': identity['catalog_digest']}, model=False)
            trace.rpc('turn/start', {'threadId': 'thread'}, {'turn': {'id': 'turn'}})
            known = {}

            def discover(operation):
                # Retrieve the root for each operation; obtain referenced shapes
                # only when they have not already arrived through any operation.
                page = invoke('describe_input', {'operation': operation, 'limit': 1})
                queue = list(page['records'])
                while queue:
                    record = queue.pop(0)
                    definition = json.loads(record['schema_json'])
                    known[record['name']] = definition
                    for ref in sorted(direct_schema_references(definition)):
                        name = local_definition_name(ref)
                        if name in known:
                            continue
                        selected = invoke('describe_input', {'operation': operation, 'selector': name,
                            'expected_catalog': identity['catalog_digest'], 'limit': 1})
                        # Mark queued names immediately so recursive definitions
                        # cannot keep re-enqueueing each other.
                        for entry in selected['records']:
                            known[entry['name']] = json.loads(entry['schema_json'])
                            queue.append(entry)

            prefix = 'topic.discovery-abcdef123456'
            discover('propose')
            change = topic_change(fixture, prefix.removeprefix('topic.'), 3)
            for edit in change['edits']:
                title, body = fixture_contents(prefix)[edit['standard']['id']]
                edit['standard'].update(title=title, body=body)
            proposed = invoke('propose', shared({'change_set': change}))
            self.assertEqual(proposed['status'], 'needs-action')
            discover('revise')
            reference = reference_change(fixture)
            reference['edits'][0]['standard'].update(id=f'reference.{prefix}-extra', title='Discovery Reference',
                body='This is contextual test material only.')
            revised = invoke('revise', shared({'context': proposed['context'], 'change_set': reference}))
            discover('resolve_workflow')
            single = invoke('resolve_workflow', shared({'context': revised['context'],
                'submission': decision(fixture, revised['work']['items'][0]['obligation'])}))
            discover('resolve_many')
            batch = invoke('resolve_many', shared({'context': single['context'], 'submissions': [
                decision(fixture, item['obligation']) for item in single['work']['items']]}))
            self.assertEqual(batch['status'], 'complete')
            invoke('describe_output', {'operation': 'review'})
            discover('review')
            ready = invoke('review', shared({'context': batch['context'], 'decisions': decisions(fixture)}))
            self.assertEqual(ready['status'], 'ready')
            trace.event('turn/completed', {'threadId': 'thread', 'turn': {'id': 'turn', 'status': 'completed'}})
            for target in fixture_contents(prefix):
                invoke('query_proposal', {'revision': ready['revision'], 'request': {'kind': 'read', 'target': target}}, model=False)
            previous = {'status': 'failed', 'runtime': runtime, 'catalog_digest': runtime['catalog_digest'],
                'fixture_main': main, 'schema_mode': 'native', 'output_schemas': delivery, 'requested_model': 'synthetic-no-model',
                'requested_surface': 'synthetic protocol trace', 'client_version': 'test-only; no Codex'}
            (evidence_dir / 'events.jsonl').write_text(trace.text())
            (evidence_dir / 'qualification.json').write_text(json.dumps(previous))
            original = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence_dir.iterdir() if p.is_file()}
            result = replay(evidence_dir)
            self.assertEqual(result['status'], 'passed', result)
            self.assertEqual(result['readbacks_verified'], 4)
            self.assertEqual(result['previous_status'], 'failed')
            output = Path(folder) / 'corrected.json'
            process = subprocess.run([sys.executable, '-m', 'tools.standards_engine.tests.replay_discovery_qualification',
                '--evidence-dir', str(evidence_dir), '--output', str(output)], cwd=ROOT,
                env={**os.environ, 'PYTHONPATH': str(ROOT)}, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertEqual(json.loads(output.read_text()), result)
            self.assertEqual({p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in evidence_dir.iterdir() if p.is_file()}, original)
            self.assertEqual(subprocess.check_output(['git', '-C', str(fixture), 'rev-parse', 'main'], text=True).strip(), main)
