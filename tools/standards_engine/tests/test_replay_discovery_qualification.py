"""Recorded-evidence oracle tests; synthetic transcripts are not model runs."""
from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.tests.codex_discovery_client import fixture_contents
from tools.standards_engine.tests.test_model_discovery_qualification import RUNTIME, observed_fixture
from tools.standards_engine.tests.replay_discovery_qualification import (
    assess_recording, main, parse_trace, replay,
)

PREFIX = 'topic.discovery-abcdef123456'
MAIN = '1' * 40


class TraceWriter:
    """Synthetic protocol writer, independent of the replay correlation logic."""
    def __init__(self):
        self.rows = []
        self.counter = 0

    def rpc(self, method, params, result):
        self.counter += 1
        self.rows.extend([
            {'direction': 'request', 'message': {'id': self.counter, 'method': method, 'params': params}},
            {'direction': 'response', 'message': {'id': self.counter, 'result': result}}])

    def event(self, method, params):
        self.rows.append({'direction': 'response', 'message': {'method': method, 'params': params}})

    def text(self):
        return '\n'.join(json.dumps(row) for row in self.rows) + '\n'


def recording_fixture():
    catalog, items, contracts = observed_fixture()
    contracts['propose']['$defs']['FixtureCall']['properties']['change_set'] = {'type': 'object'}
    # All roots share this one synthetic definition. Update the advertised
    # records, then retrieve FixtureItem only once, before its use in the batch.
    for i, item in enumerate(items):
        if item['tool'] == 'describe_input':
            item['result']['structuredContent']['records'] = [
                {'name': k, 'schema_json': json.dumps(v)} for k, v in contracts['propose']['$defs'].items()
                if i == 0 or k != 'FixtureItem']
        if item['tool'] in ('propose', 'revise'):
            ids = [f'{PREFIX}-{i}' for i in range(3)] if item['tool'] == 'propose' else [f'reference.{PREFIX}-extra']
            item['arguments']['change_set'] = {'edits': [
                {'kind': 'create-standard', 'standard': {'id': name}} for name in ids]}
    revision = {'kind': 'synthetic-revision'}
    items[-1]['result']['structuredContent']['revision'] = revision
    for name in ('runtime_info', 'query_proposal'):
        catalog[name] = {'inputSchema': {'type': 'object'}, 'outputSchema': {'type': 'object'}}
    for name, tool in catalog.items():
        tool.update(name=name, description='Synthetic observer fixture')
    runtime = {**RUNTIME, 'installation_state': 'current', 'client_catalog_state': 'matches'}
    previous = {'status': 'failed', 'runtime': runtime, 'catalog_digest': RUNTIME['catalog_digest'],
                'fixture_main': MAIN, 'schema_mode': 'native', 'requested_model': 'synthetic-model'}
    trace = TraceWriter()
    trace.rpc('thread/start', {'ephemeral': True, 'model': 'synthetic-model'}, {'thread': {'id': 'thread'}})
    trace.rpc('mcpServerStatus/list', {'threadId': 'thread'}, {'data': [{'name': 'fixture', 'tools': catalog}]})
    trace.rpc('mcpServer/tool/call', {'threadId': 'thread', 'server': 'fixture', 'tool': 'runtime_info'},
              {'structuredContent': runtime})
    trace.rpc('turn/start', {'threadId': 'thread'}, {'turn': {'id': 'turn'}})
    for item in items:
        trace.event('item/started', {'threadId': 'thread', 'turnId': 'turn', 'item': {**item, 'result': None}})
        trace.event('item/completed', {'threadId': 'thread', 'turnId': 'turn', 'item': item})
    trace.event('turn/completed', {'threadId': 'thread', 'turn': {'id': 'turn', 'status': 'completed'}})
    for target, (title, body) in fixture_contents(PREFIX).items():
        result = {'kind': 'proposal-read-result', 'revision': revision, 'policy': {'id': target},
                  'requires': ['core'], 'specializes': [],
                  'content': f'# {title}\n\n**Standards metadata**\n\n- ID: `{target}`\n\n{body}\n'}
        trace.rpc('mcpServer/tool/call', {'threadId': 'thread', 'server': 'fixture', 'tool': 'query_proposal',
            'arguments': {'revision': revision, 'request': {'kind': 'read', 'target': target}}},
            {'structuredContent': result, '_meta': {'standards-engine/runtime': deepcopy(RUNTIME)}})
    return trace, previous, catalog, contracts


class ReplayQualificationTest(unittest.TestCase):
    def assess(self, trace, previous, catalog, contracts, observed_main=MAIN):
        calls, events = parse_trace(trace.text())
        return assess_recording(calls, events, previous, catalog, contracts, RUNTIME, observed_main)

    def test_recorded_cross_operation_reuse_passes_with_exact_readbacks(self):
        result = self.assess(*recording_fixture())
        self.assertEqual(result['status'], 'passed', result)
        self.assertEqual(result['readbacks_verified'], 4)
        self.assertEqual(result['observer_version'], 3)

    def test_readback_and_publication_checks_remain_effective(self):
        trace, previous, catalog, contracts = recording_fixture()
        trace.rows[-1]['message']['result']['structuredContent']['content'] += 'Unexpected body.'
        result = self.assess(trace, previous, catalog, contracts)
        self.assertTrue(any('Readback did not preserve' in f for f in result['failures']))
        result = self.assess(*recording_fixture(), observed_main='2' * 40)
        self.assertIn('Fixture publication occurred; the task required unchanged main.', result['failures'])

    def test_incomplete_independent_readback_is_not_a_pass(self):
        trace, previous, catalog, contracts = recording_fixture()
        trace.rows = trace.rows[:-2]
        result = self.assess(trace, previous, catalog, contracts)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['readbacks_verified'], 3)

    def test_foreign_thread_and_turn_cannot_supply_discovery(self):
        for field in ('threadId', 'turnId'):
            trace, previous, catalog, contracts = recording_fixture()
            trace.rows[8]['message']['params'][field] = 'other'
            with self.assertRaisesRegex(ValueError, 'Mixed session/turn'):
                self.assess(trace, previous, catalog, contracts)

    def test_late_discovery_does_not_satisfy_an_already_running_action(self):
        trace, previous, catalog, contracts = recording_fixture()
        # Move propose's start before the first discovery completion, while
        # keeping the final completion order unchanged.
        trace.rows.insert(9, trace.rows.pop(10))
        result = self.assess(trace, previous, catalog, contracts)
        self.assertIn('propose: used input shapes were not acquired through discovery before use.', result['failures'])

    def test_catalog_or_runtime_change_is_unavailable_not_silently_rebound(self):
        trace, previous, catalog, contracts = recording_fixture()
        expected = deepcopy(catalog); expected['propose']['description'] = 'new implementation'
        with self.assertRaisesRegex(ValueError, 'Recorded catalog differs'):
            self.assess(trace, previous, expected, contracts)
        trace, previous, catalog, contracts = recording_fixture()
        trace.rows[5]['message']['result']['structuredContent']['schema_digest'] = 'sha256:' + 'f' * 64
        with self.assertRaisesRegex(ValueError, 'Recorded runtime differs'):
            self.assess(trace, previous, catalog, contracts)

    def test_missing_call_start_and_unmatched_response_are_explicit(self):
        trace, previous, catalog, contracts = recording_fixture()
        del trace.rows[8]
        with self.assertRaisesRegex(ValueError, 'no observed start'):
            self.assess(trace, previous, catalog, contracts)
        trace, *_ = recording_fixture()
        trace.rows[1]['message']['id'] = 9876
        with self.assertRaisesRegex(ValueError, 'Unmatched'):
            parse_trace(trace.text())

    def test_ambiguous_json_and_truncated_trace_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON member'):
            parse_trace('{"direction":"request","direction":"response","message":{}}')
        with self.assertRaisesRegex(ValueError, 'Non-JSON numeric'):
            parse_trace('{"direction":"request","message":{"id":NaN}}')
        trace, *_ = recording_fixture()
        trace.rows.pop()
        with self.assertRaisesRegex(ValueError, 'unresolved RPC'):
            parse_trace(trace.text())

    def test_cli_writes_only_a_new_report_and_preserves_existing_verdicts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); evidence = root / 'evidence'; evidence.mkdir()
            previous = evidence / 'qualification.json'; previous.write_text('{"status":"failed"}')
            output = root / 'observer-v2.json'
            with patch('tools.standards_engine.tests.replay_discovery_qualification.replay', return_value={'status': 'passed'}), redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--evidence-dir', str(evidence), '--output', str(output)]), 0)
                with self.assertRaises(FileExistsError):
                    main(['--evidence-dir', str(evidence), '--output', str(output)])
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main(['--evidence-dir', str(evidence), '--output', str(previous)])
            self.assertEqual(previous.read_text(), '{"status":"failed"}')
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_missing_evidence_is_unavailable_without_model_or_store_activity(self):
        with tempfile.TemporaryDirectory() as folder, patch('subprocess.check_output') as subprocess_call:
            result = replay(Path(folder))
            self.assertEqual(result['status'], 'unavailable')
            subprocess_call.assert_not_called()


    def test_unexpected_scripted_rpc_or_notification_cannot_be_ignored(self):
        for method in ('command/exec', 'thread/resume', 'thread/fork', 'turn/steer'):
            with self.subTest(method=method):
                trace, previous, catalog, contracts = recording_fixture()
                trace.rpc(method, {}, {})
                with self.assertRaisesRegex(ValueError, 'Unexpected scripted RPC'):
                    self.assess(trace, previous, catalog, contracts)
        trace, *_ = recording_fixture()
        trace.rows.append({'direction': 'request', 'message': {'method': 'turn/interrupt', 'params': {}}})
        with self.assertRaisesRegex(ValueError, 'Unsupported client notification'):
            parse_trace(trace.text())


class NativeReplayAdmissionTest(unittest.TestCase):
    def test_retired_or_missing_presentation_is_unavailable_without_reconstruction(self):
        from tools.standards_engine.standards_engine.tools import AgentToolFacade
        for recorded in ('compatibility', None, 'invented'):
            with self.subTest(recorded=recorded), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                previous = {'status': 'passed', 'schema_mode': recorded}
                (directory / 'qualification.json').write_text(json.dumps(previous))
                (directory / 'events.jsonl').write_text('')
                before = {p.name: p.read_bytes() for p in directory.iterdir()}
                with patch.object(AgentToolFacade, 'load_interface', side_effect=AssertionError('loaded')):
                    result = replay(directory)
                self.assertEqual(result['status'], 'unavailable')
                self.assertEqual(result['previous_status'], 'passed')
                self.assertIn('original pinned tooling', result['failure'])
                self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})
