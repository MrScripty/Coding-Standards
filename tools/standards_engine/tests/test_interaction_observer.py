"""Synthetic operator evidence; never records a real agent/model session.

Every recorder here writes to a temporary directory. Child processes get a
temporary HOME so the always-on default can never reach a developer's database.
"""
from __future__ import annotations

from contextlib import redirect_stderr
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine.interaction_observer import (
    APPLICATION_ID, DEFAULT_DATABASE_NAME, InputShape, InteractionRecorder, RecorderConfig,
    SCHEMA_VERSION, StorageRejected, TRUNCATED, default_database, report, text_report,
)
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests import stdio_server
from tools.standards_engine.tests.test_mcp import ROOT, initialize, request

MODULE = 'tools.standards_engine.standards_engine.interaction_observer'
MCP_MODULE = 'tools.standards_engine.standards_engine.mcp'
SNAPSHOT = {'kind': 'snapshot-handle', 'id': 'snapshot:v1:5e17e1a1-0000-4000-8000-000000000001', 'schema_version': 5}
ANALYSIS = {'kind': 'analysis-handle', 'id': 'analysis:sha256:' + 'ab' * 32, 'schema_version': 7}
# The request metadata Codex attaches to every tool call, with synthetic values.
CODEX_META = {
    'callId': 'exec-SENTINEL_CALL', 'threadId': 'SENTINEL_THREAD', 'sessionId': 'SENTINEL_SESSION', 'progressToken': 9,
    'x-codex-turn-metadata': {
        'session_id': 'SENTINEL_SESSION', 'thread_id': 'SENTINEL_THREAD', 'turn_id': 'SENTINEL_TURN',
        'model': 'SENTINEL_MODEL', 'thread_source': 'subagent',
        'workspaces': {'/SENTINEL/WORKSPACE': {'associated_remote_urls': {'origin': 'git@example.invalid:SENTINEL/REPO.git'}}}},
}
V1_DDL = (
    'CREATE TABLE sessions (id TEXT PRIMARY KEY, started REAL NOT NULL, runtime TEXT NOT NULL, deployment TEXT NOT NULL, catalog TEXT NOT NULL, pruned INTEGER NOT NULL DEFAULT 0)',
    'CREATE TABLE interactions (id TEXT PRIMARY KEY, session TEXT NOT NULL REFERENCES sessions(id), ordinal INTEGER NOT NULL, started REAL NOT NULL, method TEXT NOT NULL, operation TEXT NOT NULL, input_shape TEXT NOT NULL, shape_digest TEXT NOT NULL, discovery_operation TEXT, catalog_state TEXT NOT NULL, request_bytes INTEGER, scope TEXT NOT NULL, UNIQUE(session, ordinal))',
    "CREATE TABLE events (interaction TEXT PRIMARY KEY REFERENCES interactions(id) ON DELETE CASCADE, phase TEXT NOT NULL CHECK(phase IN ('end','error','incomplete')), finished REAL NOT NULL, duration_ms REAL NOT NULL, response_bytes INTEGER, outcome TEXT NOT NULL, feedback TEXT NOT NULL)",
    'CREATE INDEX interaction_age ON interactions(started)',
)


def environment(home: Path, **extra: str) -> dict:
    """A child environment whose default observation location is under `home`."""
    env = {name: value for name, value in os.environ.items()
           if name not in ('XDG_DATA_HOME', 'STANDARDS_ENGINE_OBSERVE')}
    return {**env, 'PYTHONPATH': str(ROOT), 'HOME': str(home), **extra}


def rejection(code, pointer=None, keyword='fact', **extra):
    value = {'kind': 'rejected-result', 'code': code, 'outcome': 'invalid', 'message': 'SENTINEL_MESSAGE',
             'details': {'SENTINEL_DETAIL': 'SENTINEL_DETAIL'}, 'next_operations': [], **extra}
    if pointer is not None:
        value['input_feedback'] = {'issues': [{'instance_pointer': pointer, 'keyword': keyword,
                                               'message': 'SENTINEL_MESSAGE'}], 'truncated': False}
    return value


def route_result(unresolved=('routing.topics',)):
    return {'kind': 'compact-route-result', 'status': 'needs-facts' if unresolved else 'complete', 'snapshot': SNAPSHOT,
            'summary': 'SENTINEL_SUMMARY',
            'reading_plan': [{'target': 'core', 'state': 'selected'}, {'target': 'router', 'state': 'selected'},
                             {'target': 'topic.security', 'state': 'conditional'}],
            'unresolved_questions': [{'fact': {'id': name, 'prompt': 'SENTINEL_PROMPT'}} for name in unresolved],
            'content': {'offset': 0, 'total': 2, 'items': [read_result('core')]}}


def read_result(target):
    return {'kind': 'compact-read-result', 'snapshot': SNAPSHOT, 'content': 'SENTINEL_STANDARD_TEXT',
            'policy': {'handle': {'kind': 'snapshot-child-handle', 'child_kind': 'policy', 'child_id': target}}}


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.database = Path(self.temporary.name) / 'observations.sqlite'
        self.diagnostics = io.StringIO()

    def server(self, *, advanced=False, **options):
        with redirect_stderr(self.diagnostics):
            server = MCPServer(ROOT, purpose='authoring', advanced=advanced,
                               observation=RecorderConfig(self.database, 'synthetic', **options))
        self.addCleanup(server.close)
        return server

    def rows(self, sql):
        with sqlite3.connect(self.database) as db:
            db.row_factory = sqlite3.Row
            return [dict(row) for row in db.execute(sql)]

    def call(self, server, name, arguments, value, meta=None):
        """One tool call whose Engine result is `value`; no store is opened."""
        params = {'name': name, 'arguments': arguments, **({'_meta': meta} if meta else {})}
        with patch.object(server, '_request', return_value=server._tool_result(value)):
            return server.dispatch(request('tools/call', params))

    def stored_bytes(self):
        return b''.join(path.read_bytes() for path in self.database.parent.iterdir())

    def test_recording_does_not_change_catalog_instructions_or_results(self):
        plain = MCPServer(ROOT, purpose='authoring')
        self.addCleanup(plain.close)
        observed = self.server()
        self.assertEqual(plain.tools, observed.tools)
        # A fixed process identity makes these full public responses comparable.
        observed._runtime_identity._instance = plain._runtime_identity._instance
        self.assertEqual(initialize(plain), initialize(observed))
        for message in (request('tools/list'), request('tools/call', {'name': 'runtime_info'}),
                        request('tools/call', {'name': 'describe_input', 'arguments': {'operation': 'apply'}}),
                        request('tools/call', {'name': 'runtime_info', 'arguments': {'secret': 'private'}}),
                        request('tools/call', {'name': 'missing-operation'})):
            self.assertEqual(plain.dispatch(message), observed.dispatch(message))
        result = report(self.database)
        self.assertEqual(result['retained_starts'], 6)
        self.assertEqual(result['retained_terminals'], 6)
        self.assertEqual(result['unmatched_starts'], 0)
        self.assertEqual(result['sessions'][0]['runtime']['interface_version'],
                         plain._runtime_identity.metadata()['interface_version'])
        self.assertEqual(result['sessions'][0]['runtime']['catalog_digest'],
                         plain._runtime_identity.metadata()['catalog_digest'])
        self.assertNotIn('observer', json.dumps(observed.tools))
        self.assertEqual(self.diagnostics.getvalue(), '', 'a healthy recorder is silent')

    def test_shape_and_feedback_disclose_no_values_or_dynamic_keys(self):
        schema = {'type': 'object', 'properties': {
            'body': {'type': 'object', 'properties': {'token': {'type': 'string'}}},
            'facts': {'type': 'object', 'additionalProperties': {
                'type': 'object', 'properties': {'body': {'type': 'string'}}}},
            'items': {'type': 'array', 'items': {'type': 'object', 'properties': {
                'selector': {'type': 'string'}}}},
        }}
        shape = InputShape(schema)
        value = {'body': {'token': 'CREDENTIAL'}, 'facts': {'facts': {'body': 'RAW-STANDARDS'}},
                 'items': [{'selector': 'PROMPT'}] * 100, 'SECRET-KEY': 'RAW-REPO'}
        encoded = json.dumps(shape.project(value))
        for secret in ('CREDENTIAL', 'RAW-STANDARDS', 'PROMPT', 'SECRET-KEY', 'RAW-REPO'):
            self.assertNotIn(secret, encoded)
        self.assertEqual(shape.project(value)['fields']['body'], 'redacted')
        self.assertEqual(shape.project(value)['fields']['facts']['fields'], {})
        issues = {'issues': [
            {'instance_pointer': '/facts/facts/body', 'keyword': 'type', 'message': 'CREDENTIAL'},
            {'instance_pointer': '/items/8/selector', 'keyword': 'required'},
            {'instance_pointer': '/body/token', 'keyword': 'CREDENTIAL'},
            {'instance_pointer': '/facts/routing.topics', 'keyword': 'fact'},
            {'instance_pointer': '/items/routing.topics', 'keyword': 'evidence_ref'},
        ]}
        self.assertEqual(shape.feedback(issues), [
            {'pointer': '/facts/*/*', 'keyword': 'type'}, {'pointer': '/items/*/selector', 'keyword': 'required'},
            {'pointer': '/body/*', 'keyword': 'other'}, {'pointer': '/facts/*', 'keyword': 'fact'},
            {'pointer': '/items/*', 'keyword': 'evidence_ref'}])
        # A fact name the same call already recorded may locate its own rejection;
        # the same text under any other map stays a wildcard.
        named = shape.feedback(issues, frozenset({'routing.topics'}))
        self.assertEqual([issue['pointer'] for issue in named][3:], ['/facts/routing.topics', '/items/*'])
        # Deep/large adversarial data is bounded without traversing unknown maps.
        projected = shape.project({'items': [{'selector': 'x' * 1_000_000}] * 100_000})
        self.assertLess(len(json.dumps(projected)), 8192)

    def test_navigation_values_results_sizes_and_task_identity_are_recorded(self):
        server = self.server()
        initialize(server)
        facts = {'routing.activities': ['implementation', 'testing'], 'python': True, 'task': 'p' * 300}
        items = [{'target': 'core'}, {'target': 'router', 'detail': 'full', 'include_routing': True, 'extra': 'DROPPED'}]
        calls = (
            ('route', {'facts': facts, 'content': {'limit': 1}, 'detail': 'compact'}, route_result()),
            ('read', {'snapshot': SNAPSHOT, 'target': 'core', 'detail': 'full', 'handle': {'kind': 'DROPPED'},
                      'request': {'kind': 'route', 'facts': {'DROPPED': 'DROPPED'}}, 'facts': {'DROPPED': True}},
             read_result('core')),
            ('read_many', {'snapshot': SNAPSHOT, 'items': items},
             {'kind': 'read-many-result', 'snapshot': SNAPSHOT, 'items': [read_result('core'), read_result('router')]}),
            ('related', {'snapshot': SNAPSHOT, 'target': 'core', 'groups': ['semantic'], 'direction': 'both', 'transitive': False},
             rejection('GRAPH.UNKNOWN_GROUP')),
            ('query_proposal', {'revision': {'kind': 'proposal-revision-handle', 'id': 'proposal-revision:sha256:' + 'cd' * 32},
                                'request': {'kind': 'route', 'facts': {'nested.fact': {'type': 'string', 'state': 'known', 'value': 'nested-value'}}}},
             rejection('AGGREGATE.UNAVAILABLE')),
        )
        for name, arguments, value in calls:
            self.call(server, name, arguments, value, CODEX_META)
        server.dispatch(request('tools/call', {'name': 'describe_input', 'arguments': {
            'operation': 'route', 'selector': 'RouteCall', 'limit': 2, 'expected_catalog': 'sha256:' + '0' * 64}}))
        recorded = {row['operation']: row for row in self.rows(
            'SELECT i.*,e.outcome,e.result,e.result_bytes FROM interactions i JOIN events e ON e.interaction=i.id '
            "WHERE i.method='tools/call'")}
        values = {name: json.loads(row['arguments']) for name, row in recorded.items()}
        results = {name: json.loads(row['result']) for name, row in recorded.items()}
        self.assertEqual(values['route'], {'detail': 'compact', 'content': {'limit': 1}, 'facts': {
            'routing.activities': ['implementation', 'testing'], 'python': True, 'task': 'p' * 200 + TRUNCATED}})
        self.assertEqual(results['route'], {
            'kind': 'compact-route-result', 'status': 'needs-facts', 'selected': ['core', 'router'],
            'unresolved': ['routing.topics'], 'content': {'offset': 0, 'total': 2, 'items': 1, 'targets': ['core']}})
        self.assertEqual(recorded['route']['outcome'], 'needs-facts')
        reused = values['read']['snapshot']
        self.assertRegex(reused, '^[0-9a-f]{12}$')
        self.assertEqual(values['read'], {'snapshot': reused, 'target': 'core', 'detail': 'full'})
        self.assertEqual(values['read_many'], {'snapshot': reused, 'items': [
            {'target': 'core'}, {'target': 'router', 'detail': 'full', 'include_routing': True}]})
        self.assertEqual(results['read_many'], {'kind': 'read-many-result', 'targets': ['core', 'router']})
        self.assertEqual(values['related'], {'snapshot': reused, 'target': 'core', 'groups': ['semantic'],
                                             'direction': 'both', 'transitive': False})
        self.assertEqual(results['related'], {'kind': 'rejected-result', 'code': 'GRAPH.UNKNOWN_GROUP', 'outcome': 'invalid'})
        self.assertEqual(values['query_proposal'], {'revision': {'kind': 'proposal-revision-handle'}, 'request': {
            'kind': 'route', 'facts': {'nested.fact': {'type': 'string', 'state': 'known', 'value': 'nested-value'}}}})
        self.assertEqual(values['describe_input'], {'operation': 'route', 'selector': 'RouteCall', 'limit': 2})
        self.assertEqual(recorded['describe_input']['catalog_state'], 'differs')
        # Sizes: the arguments object alone and one serialization of structuredContent.
        self.assertEqual(recorded['read']['arguments_bytes'], len(json.dumps(calls[1][1], separators=(',', ':'))))
        self.assertEqual(recorded['read']['result_bytes'], len(json.dumps(read_result('core'))))
        self.assertGreater(recorded['read']['request_bytes'], recorded['read']['arguments_bytes'])
        # Task identity: one salted hash per client thread, never the id itself.
        threads = {(row['thread'], row['origin']) for name, row in recorded.items() if name != 'describe_input'}
        self.assertEqual(len(threads), 1)
        thread, origin = threads.pop()
        self.assertRegex(thread, '^[0-9a-f]{16}$')
        self.assertEqual(origin, 'subagent')
        self.assertEqual((recorded['describe_input']['thread'], recorded['describe_input']['origin']), (None, 'unknown'))
        self.assertEqual(self.rows('SELECT client_name,client_version FROM sessions'),
                         [{'client_name': 'test', 'client_version': '1'}])
        stored = self.stored_bytes()
        for private in (b'SENTINEL', b'5e17e1a1', b'cdcdcdcd', b'DROPPED'):
            self.assertNotIn(private, stored)
        # The salt belongs to the database: another process maps the thread to the same hash.
        second = self.server()
        self.call(second, 'read', {'target': 'core'}, read_result('core'), CODEX_META)
        self.assertEqual({row['thread'] for row in self.rows('SELECT thread FROM interactions WHERE thread IS NOT NULL')}, {thread})

    def test_authoring_prose_never_reaches_disk_while_route_facts_do(self):
        server = self.server(advanced=True)
        initialize(server)
        prose = {name: f'SENTINEL_{name.upper()}' for name in (
            'body', 'title', 'summary', 'rationale', 'intent', 'heading', 'condition', 'path', 'label',
            'evidence', 'applies', 'verification', 'description', 'provenance', 'value', 'tool')}
        evidence = {'id': prose['evidence'], 'digest': 'sha256:' + 'ef' * 32, 'provider_contract': 'review-evidence',
                    'provider_contract_version': '1'}
        change_set = {'purpose': {'summary': prose['summary'], 'rationale': prose['rationale'], 'evidence': [{'evidence_ref': prose['label']}]}, 'edits': [
            {'kind': 'revise-policy-unit', 'policy': 'workflow.planning.written-plan-applicability', 'title': prose['title'], 'body': prose['body'],
             'semantics': {'kind': 'change', 'accepted_semantic_revision': 1, 'proposed_semantic_revision': 2, 'intent': prose['intent']}},
            {'kind': 'create-standard', 'requires': ['core'], 'specializes': [], 'standard': {
                'id': 'topic.recorded-identifier', 'title': prose['title'], 'body': prose['body'], 'level': 'SHOULD', 'role': 'topic',
                'applies_when': prose['applies'], 'does_not_apply_when': prose['applies'], 'verification': prose['verification']},
             'policy_units': [{'id': 'topic.recorded-identifier.unit', 'heading_chain': [prose['heading']], 'intent': prose['intent'],
                               'semantic_revision': 1, 'aliases': [], 'predecessors': [], 'successors': []}]},
            {'kind': 'put-policy-relationship', 'relationship': {
                'source_policy': 'core.application-guidance', 'consumer': 'prompts/planning.md', 'relation': 'prompt-projection',
                'evidence_owner': 'review:consumer', 'rationale': prose['rationale'], 'applicability': {'operator': 'always'}}},
            {'kind': 'register-consumer', 'consumer': 'consumer.recorded', 'artifact_kind': 'documentation', 'authority': 'projection',
             'path': prose['path']},
            {'kind': 'put-routing-rule', 'rationale': prose['rationale'], 'rule': {
                'id': 'rule.recorded', 'target': 'topic.security', 'condition': prose['condition'],
                'when': {'operator': 'equals', 'fact': 'routing.topics', 'value': prose['value']}}},
            # Prose placed in an identifier field is dropped by its shape.
            {'kind': 'audit-policy-unit', 'policy': 'SENTINEL PROSE in an identifier field', 'rationale': prose['rationale']},
        ]}
        child = {'kind': 'analysis-child-handle', 'analysis': ANALYSIS, 'child_kind': 'obligation', 'child_id': 'sha256:' + '12' * 32}
        calls = (
            ('propose', {'snapshot': SNAPSHOT, 'detail': 'full', 'change_set': change_set, 'evidence': {prose['label']: evidence}}),
            ('revise', {'context': ANALYSIS, 'change_set': change_set}),
            ('review', {'context': ANALYSIS, 'decisions': [
                {'owner': 'consumer', 'decision': 'accept', 'rationale': prose['rationale'], 'evidence': [evidence]}]}),
            ('resolve_workflow', {'context': ANALYSIS, 'submission': {
                'kind': 'coverage-attestation', 'claim': {'requirement': child, 'conclusion': 'complete', 'rationale': prose['rationale'],
                                                          'auditor_provenance': prose['provenance'], 'evidence': [evidence],
                                                          'explicit_exclusions': [evidence]}}}),
            ('recover', {'context': ANALYSIS, 'action': 'observe'}),
            ('maintain_evidence', {'kind': 'maintain-evidence', 'expected_revision': prose['value'], 'apply': False, 'evidence': [evidence],
                                   'plan': {'suite_descriptions': [{'suite': prose['label'], 'description': prose['description']}],
                                            'replacement_evidence_rationale': prose['rationale'],
                                            'consumer_registrations': [{'path': prose['path'], 'rationale': prose['rationale'],
                                                                        'artifact_kind': 'fixture', 'relation': 'fixture-projection'}]}}),
        )
        for name, arguments in calls:
            self.call(server, name, arguments, rejection('INTERFACE.INVALID_ARGUMENTS', '/change_set/purpose/' + prose['label'], 'minItems'),
                      CODEX_META)
        server.dispatch(request('tools/call', {'name': prose['tool'], 'arguments': {'body': prose['body']}}, identifier=prose['value']))
        # Route facts are kept as sent, in the focused form and inside a preview request.
        self.call(server, 'route', {'facts': {'OOV_NAME_python': True, 'task': 'OOV free text about a parser',
                                              'routing.activities': ['implementation', 'OOV_VALUE_testing']}},
                  rejection('ROUTE.INPUT_INVALID', '/facts'))
        self.call(server, 'preview_application', {'revision': {'kind': 'proposal-revision-handle', 'id': 'proposal-revision:sha256:' + '34' * 32},
                                                  'request': {'kind': 'route', 'facts': {'OOV_NESTED': {'type': 'string', 'state': 'known', 'value': 'OOV_NESTED_VALUE'}}}},
                  rejection('ROUTE.INPUT_INVALID', '/request/facts'))
        for closed in (False, True):
            stored = self.stored_bytes()  # The main file, and the write-ahead log while it exists.
            for private in (b'SENTINEL', b'abababab', b'efefefef', b'12121212', b'34343434', b'5e17e1a1'):
                self.assertNotIn(private, stored, (private, closed))
            for kept in (b'OOV_NAME_python', b'OOV free text about a parser', b'OOV_VALUE_testing', b'OOV_NESTED_VALUE',
                         b'workflow.planning.written-plan-applicability', b'topic.recorded-identifier.unit',
                         b'prompts/planning.md', b'consumer.recorded', b'revise-policy-unit', b'analysis-handle',
                         b'INTERFACE.INVALID_ARGUMENTS'):
                self.assertIn(kept, stored, (kept, closed))
            server.close()
        summary = report(self.database)
        self.assertNotIn('SENTINEL', json.dumps(summary) + text_report(summary))
        propose = json.loads(self.rows("SELECT arguments FROM interactions WHERE operation='propose'")[0]['arguments'])
        self.assertEqual(propose['change_set']['edits'][0], {
            'kind': 'revise-policy-unit', 'policy': 'workflow.planning.written-plan-applicability', 'semantics': {'kind': 'change'}})
        self.assertEqual(propose['change_set']['edits'][5], {'kind': 'audit-policy-unit'})
        self.assertEqual((propose['snapshot'], propose['detail']), ({'kind': 'snapshot-handle'}, 'full'))

    def test_privacy_at_real_dispatch_and_disk_boundary(self):
        server = self.server()
        initialize(server)
        secrets = ['SYNTHETIC_PASSWORD_847', 'SYNTHETIC_PROMPT_738', 'SYNTHETIC_REPO_339']
        server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {
            'expected_catalog': secrets[0], secrets[1]: secrets[2]}}, identifier=secrets[0]))
        server.dispatch(request('tools/call', {'name': secrets[1], 'arguments': {'body': secrets[2]}}))
        # Only the first initialize names the client; other clientInfo members are never read.
        server.dispatch(request('initialize', {'clientInfo': {'name': secrets[0], 'title': secrets[1]}}))
        server.close()
        for path in self.database.parent.iterdir():
            contents = path.read_bytes()
            for secret in secrets:
                self.assertNotIn(secret.encode(), contents)
        summary = json.dumps(report(self.database))
        for secret in secrets:
            self.assertNotIn(secret, summary)
        failures = self.rows("SELECT outcome,feedback FROM events WHERE phase='error'")
        self.assertIn('input-invalid', {row['outcome'] for row in failures})
        self.assertTrue(any('expected_catalog' in row['feedback'] for row in failures))

    def test_malformed_envelopes_and_parse_errors_do_not_disable_recorder(self):
        server = self.server()
        for value in (None, [], {}, {'method': 'ping'}, {'id': 1, 'method': [], 'jsonrpc': '2.0'},
                      request('tools/call', {'name': []}), request('ping', []),
                      request('tools/call', {'name': 'route', 'arguments': [], '_meta': []}),
                      request('tools/call', {'name': 'read_many', 'arguments': {'items': 'x', 'snapshot': []},
                                             '_meta': {'x-codex-turn-metadata': {'thread_id': [], 'thread_source': {}}}})):
            server.dispatch(value)
        output = io.StringIO()
        serve(server, io.StringIO('{BAD JSON\n'), output)
        self.assertEqual(json.loads(output.getvalue())['error']['code'], -32700)
        self.assertEqual(server._observer.health['state'], 'healthy')
        self.assertEqual(server._observer.health['lost'], 0)
        self.assertEqual(report(self.database)['retained_starts'], 10)
        self.assertIn('parse-error', {row['outcome'] for row in self.rows('SELECT outcome FROM events')})

    def test_tool_exception_interruption_and_delivery_failure(self):
        server = self.server()
        initialize(server)
        with patch.object(AgentToolFacade, 'open_repository') as opened, redirect_stderr(io.StringIO()):
            opened.return_value.apply.side_effect = RuntimeError('SENSITIVE_EXCEPTION')
            response = server.dispatch(request('tools/call', {'name': 'apply', 'arguments': {}}))
        self.assertTrue(response['result']['isError'])
        with patch.object(server, '_request', side_effect=KeyboardInterrupt('SENSITIVE_INTERRUPT')):
            with self.assertRaises(KeyboardInterrupt):
                server.dispatch(request('ping'))
        def broken(response):
            raise BrokenPipeError('SENSITIVE_PIPE')
        with self.assertRaises(BrokenPipeError):
            server._handle(request('ping'), deliver=broken, request_bytes=22)
        events = self.rows('SELECT phase,outcome,response_bytes FROM events')
        self.assertEqual([r['outcome'] for r in events], ['response', 'tool-exception', 'unknown', 'unknown'])
        self.assertEqual(sum(r['phase'] == 'incomplete' for r in events), 2)
        self.assertNotIn(b'SENSITIVE_', self.stored_bytes())

    def test_locked_database_delays_rows_but_never_drops_or_slows_a_call(self):
        observed = self.server()
        with sqlite3.connect(self.database, isolation_level=None) as lock:
            lock.execute('BEGIN IMMEDIATE')
            before = time.monotonic()
            responses = [observed.dispatch(request('ping')) for _ in range(3)]
            elapsed = time.monotonic() - before
            self.assertEqual(report(self.database)['retained_starts'], 0)
            lock.execute('ROLLBACK')
        self.assertEqual([response['result'] for response in responses], [{}, {}, {}])
        self.assertLess(elapsed, 1, 'six lock waits of 20 ms must not delay three calls materially')
        health = observed._observer.health
        self.assertEqual((health['state'], health['reason'], health['backlog']), ('degraded', 'storage-locked', 6))
        # The next call delivers the whole backlog in order.
        observed.dispatch(request('ping'))
        self.assertEqual((health['state'], health['backlog'], health['lost']), ('healthy', 0, 0))
        self.assertEqual((health['recorded_starts'], health['recorded_terminals']), (4, 4))
        self.assertEqual([row['ordinal'] for row in self.rows('SELECT ordinal FROM interactions ORDER BY started')], [1, 2, 3, 4])
        # Orderly close waits longer for a writer than a call may.
        lock = sqlite3.connect(self.database, isolation_level=None, check_same_thread=False)
        lock.execute('BEGIN IMMEDIATE')
        observed.dispatch(request('ping'))
        self.assertEqual(health['backlog'], 2)
        release = threading.Timer(0.3, lambda: (lock.execute('ROLLBACK'), lock.close()))
        release.start()
        observed.close()
        release.join()
        summary = report(self.database)
        self.assertEqual((summary['retained_starts'], summary['retained_terminals'], summary['lost_rows']), (5, 5, 0))
        notes = [json.loads(line.split(' ', 2)[2]) for line in self.diagnostics.getvalue().splitlines()]
        # One line per change of health, then the totals at close; nothing while healthy.
        self.assertEqual([(note['state'], note['reason']) for note in notes],
                         [('degraded', 'storage-locked'), ('healthy', None), ('degraded', 'storage-locked'),
                          ('healthy', None), ('healthy', None)])
        self.assertEqual((notes[-1]['recorded_starts'], notes[-1]['recorded_terminals'], notes[-1]['lost']), (5, 5, 0))

    def test_backlog_overflow_is_counted_and_the_count_is_persisted(self):
        observed = self.server()
        with patch(MODULE + '.MAX_BACKLOG', 4):
            with sqlite3.connect(self.database, isolation_level=None) as lock:
                lock.execute('BEGIN IMMEDIATE')
                for _ in range(5):
                    observed.dispatch(request('ping'))
                lock.execute('ROLLBACK')
            self.assertEqual((observed._observer.health['backlog'], observed._observer.health['lost']), (4, 6))
            observed.dispatch(request('ping'))
        # Calls 1-3 overflowed (6 rows); call 4 lost its start to the sixth call and
        # so its terminal as well (2 rows). Calls 5 and 6 are complete.
        health = observed._observer.health
        self.assertEqual((health['state'], health['lost'], health['recorded_starts'], health['recorded_terminals']),
                         ('healthy', 8, 2, 2))
        summary = report(self.database)
        self.assertEqual((summary['retained_starts'], summary['retained_terminals'], summary['lost_rows']), (2, 2, 8))
        self.assertIn('8 rows lost', text_report(summary))

    def test_unavailable_storage_reconnects_later_and_reports_what_it_never_wrote(self):
        unavailable = Path(self.temporary.name) / 'missing' / 'db'
        with redirect_stderr(io.StringIO()):
            server = MCPServer(ROOT, purpose='authoring', observation=RecorderConfig(unavailable, 'synthetic'))
        self.addCleanup(server.close)
        self.assertEqual(server.dispatch(request('ping'))['result'], {})
        health = server._observer.health
        self.assertEqual((health['state'], health['reason'], health['backlog']), ('degraded', 'storage-unavailable', 2))
        self.assertFalse(unavailable.parent.exists(), 'an operator-supplied directory is never created')
        unavailable.parent.mkdir()
        self.assertEqual(server.dispatch(request('ping'))['result'], {})
        self.assertEqual((health['state'], health['recorded_starts'], health['recorded_terminals'], health['lost']),
                         ('healthy', 2, 2, 0))
        # A process that can never write says so on stderr at close, with its count.
        class BrokenDiagnostics:
            def write(self, value):
                raise OSError('private')
            def flush(self):
                raise OSError('private')
        for diagnostics in (self.diagnostics, BrokenDiagnostics()):
            recorder = InteractionRecorder(RecorderConfig(Path(self.temporary.name) / 'absent' / 'db', 'synthetic'),
                                           {'instance_id': 'never', 'catalog_digest': 'c'}, [], diagnostics=diagnostics)
            recorder.finish(recorder.begin(request('ping'), request_bytes=1, scope='constructed'), {'result': {}})
            recorder.close()
            self.assertEqual((recorder.health['state'], recorder.health['lost']), ('degraded', 2))
        self.assertIn('"lost":2', self.diagnostics.getvalue().splitlines()[-1])

    def test_full_storage_after_domain_result_never_repeats_work(self):
        server = self.server()
        initialize(server)
        original = server._request
        calls = []
        def domain(method, params):
            calls.append(method)
            result = original(method, params)
            # Fill remaining permitted SQLite pages after the begin commit. This
            # reaches real SQLITE_FULL while inserting the terminal evidence.
            db = server._observer._connection
            db.execute('UPDATE events SET feedback=?', ('x' * 3950,))
            pages = db.execute('PRAGMA page_count').fetchone()[0]
            db.execute(f'PRAGMA max_page_count={pages}')
            return result
        with patch.object(server, '_request', side_effect=domain):
            response = server.dispatch(request('ping'))
        self.assertEqual(response['result'], {})
        self.assertEqual(calls, ['ping'])
        self.assertEqual(server._observer.health['reason'], 'storage-full')
        self.assertEqual(report(self.database)['unmatched_starts'], 1)
        # The terminal waited in the backlog; a later call reconnects and delivers it.
        server.dispatch(request('ping'))
        self.assertEqual(server._observer.health['state'], 'healthy')
        self.assertEqual(report(self.database)['unmatched_starts'], 0)

    def test_byte_cap_evicts_the_oldest_calls_instead_of_refusing_new_ones(self):
        recorder = self.server(max_bytes=1024 * 1024)._observer
        message = request('tools/call', {'name': 'route', 'arguments': {
            'facts': {f'routing.fact-{index}': ['v' * 150] * 2 for index in range(8)}}})
        for _ in range(900):
            recorder.finish(recorder.begin(message, request_bytes=1, scope='constructed'), {'result': {}}, response_bytes=1)
        health = recorder.health
        self.assertEqual((health['state'], health['lost'], health['recorded_starts']), ('healthy', 0, 900))
        self.assertGreater(health['pruned_interactions'], 0)
        retained = self.rows('SELECT min(ordinal) AS oldest,max(ordinal) AS newest,count(*) AS count FROM interactions')[0]
        self.assertEqual(retained['newest'], 900)
        self.assertEqual(retained['count'], 900 - health['pruned_interactions'])
        recorder.close()
        self.assertLessEqual(self.database.stat().st_size, 1024 * 1024)

    def test_migration_reopen_unsupported_corrupt_and_spoofed(self):
        server = self.server()
        server.dispatch(request('ping'))
        server.close()
        with sqlite3.connect(self.database) as db:
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], SCHEMA_VERSION)
            self.assertEqual(db.execute('PRAGMA application_id').fetchone()[0], APPLICATION_ID)
            self.assertEqual(db.execute('PRAGMA journal_mode').fetchone()[0], 'wal')
            self.assertRegex(db.execute("SELECT value FROM meta WHERE key='salt'").fetchone()[0], '^[0-9a-f]{32}$')
        again = self.server()
        again.dispatch(request('ping'))
        again.close()
        self.assertEqual(report(self.database)['retained_starts'], 2)
        for name, setup, reason in (
            ('future', 'PRAGMA user_version=999', 'unsupported-database-schema'),
            ('unrelated', 'CREATE TABLE business (secret TEXT)', 'unsupported-database-schema'),
            ('spoofed', f'PRAGMA user_version={SCHEMA_VERSION}; PRAGMA application_id={APPLICATION_ID}; CREATE TABLE sessions(id TEXT)',
             'invalid-database-schema'),
        ):
            target = Path(self.temporary.name) / name
            with sqlite3.connect(target) as db:
                db.executescript(setup)
            target.chmod(0o600)
            before = target.read_bytes()
            with redirect_stderr(io.StringIO()):
                recorder = InteractionRecorder(RecorderConfig(target, 'synthetic'), {}, [])
            self.assertEqual((recorder.health['state'], recorder.health['reason']), ('degraded', reason))
            self.assertEqual(target.read_bytes(), before)
        corrupt = Path(self.temporary.name) / 'corrupt'
        corrupt.write_bytes(b'not sqlite sensitive synthetic')
        corrupt.chmod(0o600)
        before = corrupt.read_bytes()
        recorder = InteractionRecorder(RecorderConfig(corrupt, 'synthetic'), {}, [], diagnostics=io.StringIO())
        self.assertEqual(recorder.health['state'], 'degraded')
        self.assertEqual(corrupt.read_bytes(), before)

    def test_schema_v1_database_is_refused_and_left_untouched(self):
        with sqlite3.connect(self.database) as db:
            db.executescript(';'.join(V1_DDL) + f';PRAGMA application_id={APPLICATION_ID};PRAGMA user_version=1;'
                             "INSERT INTO sessions VALUES('historical',1.0,'{}','codex-local','{}',0)")
        self.database.chmod(0o600)
        before = self.database.read_bytes()
        server = self.server()
        self.assertEqual(server.dispatch(request('ping'))['result'], {})
        health = server._observer.health
        self.assertEqual((health['state'], health['reason'], health['recorded_starts']),
                         ('degraded', 'unsupported-database-schema', 0))
        server.close()
        self.assertEqual(self.database.read_bytes(), before)
        self.assertEqual(sorted(path.name for path in self.database.parent.iterdir()), [self.database.name])
        with self.assertRaises(StorageRejected):
            report(self.database)
        self.assertIn('unsupported-database-schema', self.diagnostics.getvalue())

    def test_foreign_wal_store_and_page_budget_never_publish_migration(self):
        for name, pragma in (('wal', 'PRAGMA journal_mode=WAL'),):
            path = Path(self.temporary.name) / name
            with sqlite3.connect(path) as db:
                db.execute(pragma)
            path.chmod(0o600)
            before = path.read_bytes()
            recorder = InteractionRecorder(RecorderConfig(path, 'synthetic', max_bytes=1024*1024),
                                           {}, [], diagnostics=io.StringIO())
            self.assertEqual((recorder.health['state'], recorder.health['reason']), ('degraded', 'nonpristine-database'))
            self.assertEqual(path.read_bytes(), before)
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 0)
                self.assertEqual(db.execute('SELECT name FROM sqlite_master').fetchall(), [])

    def test_dropped_private_content_cannot_be_admitted_as_an_empty_recorder(self):
        secret = 'SYNTHETIC_PRIOR_STORE_SECRET'
        with sqlite3.connect(self.database) as db:
            db.execute('PRAGMA secure_delete=OFF')
            db.execute('CREATE TABLE prior_private(payload TEXT)')
            db.execute('INSERT INTO prior_private VALUES(?)', (secret,))
            db.execute('DROP TABLE prior_private')
        self.database.chmod(0o600)
        before = self.database.read_bytes()
        self.assertIn(secret.encode(), before)
        recorder = InteractionRecorder(RecorderConfig(self.database, 'synthetic'), {}, [], diagnostics=io.StringIO())
        self.assertEqual(recorder.health['reason'], 'nonpristine-database')
        self.assertEqual(self.database.read_bytes(), before)
        with sqlite3.connect(self.database) as db:
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT name FROM sqlite_master').fetchall(), [])

    def test_oversized_empty_store_is_rejected_before_migration(self):
        with sqlite3.connect(self.database) as db:
            db.execute('CREATE TABLE staging(payload BLOB)')
            db.execute('INSERT INTO staging VALUES(zeroblob(2097152))')
            db.execute('DROP TABLE staging')
        self.database.chmod(0o600)
        before = self.database.read_bytes()
        recorder = InteractionRecorder(RecorderConfig(self.database, 'synthetic', max_bytes=1048576),
                                       {}, [], diagnostics=io.StringIO())
        self.assertEqual(recorder.health['reason'], 'database-over-budget')
        self.assertEqual(self.database.read_bytes(), before)

    def test_interrupted_initial_migration_reopens_empty_source_transactionally(self):
        script = """
import os, sqlite3, sys
connection=sqlite3.connect(sys.argv[1],isolation_level=None)
connection.execute('BEGIN IMMEDIATE')
connection.execute('CREATE TABLE sessions(id TEXT PRIMARY KEY)')
os._exit(0)
"""
        process = subprocess.run([sys.executable, '-c', script, str(self.database)],
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.database.chmod(0o600)
        server = self.server()
        self.assertEqual(server._observer.health['state'], 'healthy')
        server.dispatch(request('ping'))
        self.assertEqual(report(self.database)['retained_terminals'], 1)

    def test_private_regular_file_and_no_symlink_or_hardlink(self):
        target = Path(self.temporary.name) / 'target'
        target.write_text('unchanged')
        target.chmod(0o600)
        for name in ('symlink', 'hardlink'):
            path = Path(self.temporary.name) / name
            path.symlink_to(target) if name == 'symlink' else os.link(target, path)
            recorder = InteractionRecorder(RecorderConfig(path, 'synthetic'), {}, [], diagnostics=io.StringIO())
            self.assertEqual(recorder.health['state'], 'degraded')
        self.assertEqual(target.read_text(), 'unchanged')
        public = Path(self.temporary.name) / 'public'
        public.touch()
        public.chmod(0o644)
        recorder = InteractionRecorder(RecorderConfig(public, 'synthetic'), {}, [], diagnostics=io.StringIO())
        self.assertEqual(recorder.health['reason'], 'unsafe-database-file')
        self.assertEqual(public.stat().st_mode & 0o777, 0o644)

    def test_default_location_follows_xdg_and_is_created_private(self):
        home = Path(self.temporary.name) / 'home'
        with patch.dict(os.environ, {'HOME': str(home), 'XDG_DATA_HOME': ''}):
            self.assertEqual(default_database(), home / '.local/share/standards-engine/observations' / DEFAULT_DATABASE_NAME)
            with patch.dict(os.environ, {'XDG_DATA_HOME': 'relative/ignored'}):
                self.assertEqual(default_database().parents[2], home / '.local/share')
            with patch.dict(os.environ, {'XDG_DATA_HOME': str(home / 'xdg')}):
                recorder = InteractionRecorder(RecorderConfig(), {'instance_id': 'default', 'catalog_digest': 'c'}, [],
                                               diagnostics=self.diagnostics)
                recorder.finish(recorder.begin(request('ping'), request_bytes=1, scope='constructed'), {'result': {}})
                recorder.close()
                database = home / 'xdg/standards-engine/observations' / DEFAULT_DATABASE_NAME
                self.assertEqual(default_database(), database)
        self.assertEqual(recorder.health['recorded_terminals'], 1)
        self.assertEqual(stat.S_IMODE(database.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(database.parent.stat().st_mode), 0o700)
        self.assertEqual(self.diagnostics.getvalue(), '')

    def test_count_age_and_session_retention_and_read_only_reports(self):
        # Every process-like recorder has its own session; old empty sessions must
        # disappear along with their interactions rather than accumulating forever.
        for _ in range(19):
            server = self.server(max_calls=16)
            server.dispatch(request('ping'))
            server.close()
        summary = report(self.database, limit=1)
        self.assertEqual(summary['retained_starts'], 16)
        self.assertEqual(len(self.rows('SELECT id FROM sessions')), 16)
        self.assertEqual(len(self.rows('SELECT digest FROM catalogs')), 1, 'one catalog row serves every session')
        self.assertTrue(summary['session_rows_truncated'])
        with sqlite3.connect(self.database) as db:
            db.execute('UPDATE interactions SET started=0')
        server = self.server(max_calls=16, max_age_seconds=60)
        server.dispatch(request('ping'))
        self.assertEqual(report(self.database)['retained_starts'], 1)
        self.assertEqual(server._observer.health['pruned_interactions'], 16)
        before = self.database.read_bytes()
        report(self.database)
        self.assertEqual(self.database.read_bytes(), before)
        for limit in (0, 1001):
            with self.assertRaises(ValueError):
                report(self.database, limit=limit)
        with self.assertRaises(ValueError):
            report(self.database, since_days=0)
        missing = Path(self.temporary.name) / 'absent.sqlite'
        with self.assertRaises(FileNotFoundError):
            report(missing)
        self.assertFalse(missing.exists())

    def test_retention_can_evict_inflight_evidence_without_disabling_a_live_process(self):
        first = self.server(max_calls=16)
        second = self.server(max_calls=16)
        ticket = first._observer.begin(request('ping'), request_bytes=50, scope='constructed')
        for _ in range(16):
            second.dispatch(request('ping'))
        first._observer.finish(ticket, {'result': {}}, response_bytes=14)
        self.assertEqual(first._observer.health['state'], 'healthy')
        self.assertEqual(first._observer.health['lost'], 1)
        first.dispatch(request('ping'))
        self.assertEqual(first._observer.health['recorded_terminals'], 1)
        summary = report(self.database)
        self.assertEqual(summary['retained_starts'], 16)
        self.assertEqual(summary['retained_terminals'], 16)
        self.assertEqual(summary['lost_rows'], 1)

    def test_observed_discovery_and_error_sequences_have_explicit_denominators(self):
        server = self.server()
        initialize(server)
        for name, arguments in (('describe_input', {'operation': 'runtime_info'}),
                                ('runtime_info', {'extra': 'bad'}), ('runtime_info', {}),
                                ('runtime_info', {})):
            server.dispatch(request('tools/call', {'name': name, 'arguments': arguments}))
        summary = report(self.database)
        self.assertEqual(summary['sequences'][0]['successful_responses'], 2)
        self.assertEqual(summary['sequences'][0]['preceding_errors_histogram'], {1: 1, 0: 1})
        self.assertEqual(summary['sequences'][0]['preceding_discoveries_histogram'], {1: 1, 0: 1})
        self.assertEqual(summary['failures'][0]['outcome'], 'input-invalid')

    def test_catalog_revision_report_attributes_exact_operation_schema_changes(self):
        def runtime(instance, catalog):
            return {'instance_id': instance, 'interface_version': 46, 'purpose': 'authoring',
                    'catalog_digest': catalog, 'schema_digest': 'synthetic-schema',
                    'implementation_digest': 'synthetic-source'}
        first_catalog = [{'name': 'shared', 'inputSchema': {'type': 'string'}},
                         {'name': 'retired', 'inputSchema': {}}]
        second_catalog = [{'name': 'shared', 'inputSchema': {'type': 'number'}},
                          {'name': 'added', 'inputSchema': {}}]
        for instance, digest, catalog in (('first', 'synthetic-catalog-1', first_catalog),
                                          ('second', 'synthetic-catalog-2', second_catalog)):
            recorder = InteractionRecorder(RecorderConfig(self.database, 'synthetic'),
                                           runtime(instance, digest), catalog, diagnostics=io.StringIO())
            ticket = recorder.begin(request('tools/call', {'name': 'shared', 'arguments': {}}),
                                    request_bytes=50, scope='constructed')
            recorder.finish(ticket, {'result': {}}, response_bytes=14)
            recorder.close()
        summary = report(self.database)
        self.assertEqual(summary['catalog_comparisons'], [{
            'before': 'synthetic-catalog-1', 'after': 'synthetic-catalog-2',
            'added': ['added'], 'removed': ['retired'], 'changed': ['shared']}])
        self.assertEqual({row['runtime']['implementation_digest'] for row in summary['sessions']},
                         {'synthetic-source'})

    def test_report_scope_truncation_and_bounded_scan_are_explicit(self):
        server = self.server()
        initialize(server)
        message = request('tools/call', {'name': 'runtime_info', 'arguments': {}})
        server.dispatch(message)
        server._handle(message, deliver=lambda response: 10, request_bytes=10)
        summary = report(self.database, limit=1)
        self.assertTrue(summary['operations_truncated'])
        self.assertTrue(summary['shapes_truncated'])
        self.assertEqual({row['scope'] for row in summary['sequences']}, {'constructed', 'stdio-flushed'})
        with patch(MODULE + '.MAX_SEQUENCE_SCAN', 1):
            bounded = report(self.database)
        self.assertEqual(bounded['sequence_scan_starts'], 1)
        self.assertTrue(bounded['sequence_scan_truncated'])
        self.assertIn('input_shape', summary['shapes'][0])

    def test_text_report_answers_the_interface_questions_in_a_screenful(self):
        server = self.server()
        initialize(server)
        thread = {'x-codex-turn-metadata': {'thread_id': 'thread-a', 'thread_source': 'user'}}
        self.call(server, 'route', {'facts': {}, 'content': {}}, route_result(('routing.activities', 'routing.topics')), thread)
        self.call(server, 'route', {'snapshot': SNAPSHOT, 'facts': {'routing.activities': ['implementation']}}, route_result(), thread)
        self.call(server, 'route', {'facts': {'python': True, 'task': 'write a parser test', 'routing.topics': ['security']}},
                  rejection('ROUTE.INPUT_INVALID', '/facts'), thread)
        for _ in range(2):
            self.call(server, 'route', {'facts': {'routing.activities': ['implementation', 'testing']}},
                      rejection('ROUTE.INPUT_INVALID', '/facts/routing.activities'), thread)
        for target in ('core', 'core', 'router'):
            self.call(server, 'read', {'snapshot': SNAPSHOT, 'target': target}, read_result(target), thread)
        self.call(server, 'read', {'target': 'python-standards'}, rejection('NAVIGATION.UNKNOWN_POLICY'))
        open_call = server._observer.begin(request('ping'), request_bytes=1, scope='constructed')
        summary = report(self.database)
        text = text_report(summary)
        lines = text.splitlines()
        self.assertLessEqual(len(lines), 50)
        self.assertLessEqual(max(map(len, lines)), 130)
        self.assertEqual(lines[2], '11 calls: 1 without an outcome (process ended mid-call), 0 rows lost, 0 pruned by retention')
        self.assertRegex(text, r'test 1 +authoring +\d+ +1 +11')
        usage = {row['operation']: row for row in summary['usage']}
        self.assertEqual((usage['route']['calls'], usage['route']['rejected'], usage['route']['rejection_rate']), (5, 3, 0.6))
        self.assertGreaterEqual(usage['route']['duration_max_ms'], usage['route']['duration_p90_ms'])
        self.assertGreaterEqual(usage['route']['duration_p90_ms'], usage['route']['duration_p50_ms'])
        self.assertEqual(usage['read']['result_max_bytes'],
                         max(len(json.dumps(value)) for value in (read_result('router'), rejection('NAVIGATION.UNKNOWN_POLICY'))))
        self.assertRegex(text, r'route +5 +60\.0% +[\d.]+ +[\d.]+ +[\d.]+ +[\d.]+ k?B +[\d.]+ k?B')
        self.assertIn('    2  route  ROUTE.INPUT_INVALID  /facts/routing.activities (fact)  ["implementation","testing"]', lines)
        self.assertIn('    1  read  NAVIGATION.UNKNOWN_POLICY  -  {"target":"python-standards"}', lines)
        self.assertEqual(summary['unaccepted_facts'], {
            'names': [{'name': 'python', 'count': 1}, {'name': 'task', 'count': 1}],
            'values': [{'fact': 'routing.activities', 'value': 'testing', 'count': 2}]})
        self.assertIn('  names:  python x1, task x1', lines)
        self.assertIn('  values: routing.activities=testing x2', lines)
        # Two route content pages delivered core; three reads returned core, core, router.
        self.assertIn('  core x4, router x1', lines)
        self.assertEqual(summary['repeat_reads'], {'reads': 5, 'repeats': 3, 'threads': 1, 'threads_repeating': 1,
                                                   'worst_thread_rate': 0.6})
        self.assertIn('Routes sent without a snapshot: 4 of 5 (80.0%)', lines)
        self.assertEqual(lines[-3:], ['Tool-calling threads  threads   calls   reads repeated',
                                      'main                        1       8   3 of 5 (60.0%)',
                                      'unknown                     1       1   0 of 0'])
        # The window filter drops older calls from every section.
        with sqlite3.connect(self.database) as db:
            db.execute("UPDATE interactions SET started=started-3*86400 WHERE operation='route'")
        recent = report(self.database, since_days=1)
        self.assertEqual(recent['retained_starts'], 6)
        self.assertNotIn('route', {row['operation'] for row in recent['usage']})
        self.assertIn('(last 1 days)', text_report(recent))
        server._observer.finish(open_call, {'result': {}})

    def test_arbitrary_outputs_are_never_retained(self):
        server = self.server()
        initialize(server)
        secret = 'SYNTHETIC_OUTPUT_CREDENTIAL'
        result = {'structuredContent': {'body': secret, 'outcome': secret, 'kind': secret, 'code': secret, 'status': secret,
                  'content': {'offset': secret, 'total': secret, 'items': [{'policy': {'id': secret + ' prose'}, 'content': secret}]},
                  'reading_plan': [{'target': secret + ' prose', 'state': 'selected'}],
                  'input_feedback': {'issues': [{'instance_pointer': '/' + secret,
                                                'keyword': secret, 'message': secret}]}}, 'isError': True,
                  'content': [{'type': 'text', 'text': secret}]}
        with patch.object(server, '_request', return_value=result):
            response = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {}}))
        self.assertEqual(response['result'], result)
        server.close()
        self.assertNotIn(secret.encode(), self.database.read_bytes())
        self.assertNotIn(secret, json.dumps(report(self.database)))

    def test_unencodable_text_measurement_never_changes_stdio_behavior(self):
        for observed in (False, True):
            server = self.server() if observed else MCPServer(ROOT, purpose='authoring')
            self.addCleanup(server.close)
            output = io.StringIO()
            payload = '{"jsonrpc":"2.0","id":"\ud800","method":"ping","params":{"_meta":{"threadId":"\ud800"}}}\n'
            serve(server, io.StringIO(payload), output)
            self.assertEqual(json.loads(output.getvalue())['result'], {})
        self.assertEqual(report(self.database)['retained_terminals'], 1)

    def test_no_test_or_harness_launch_can_reach_the_default_database(self):
        # Always-on recording must not follow the test suite into a developer's home.
        # In-process MCPServer construction records only when given a configuration;
        # every file that launches the server module as a process must disable
        # recording or name a database explicitly.
        launch = re.compile(r'''standards_engine\.mcp["']|standards_engine\.mcp import main''')
        guards = ('--no-observe', '--observe-database', 'STANDARDS_ENGINE_OBSERVE')
        sources = [path for folder in ('tools', 'evaluation', '.agents') for path in sorted((ROOT / folder).rglob('*.py'))]
        launchers = [path for path in sources if launch.search(path.read_text())]
        # Files that launch only through the shared server helper name no module
        # and can pass no option that turns recording back on.
        helper = Path(stdio_server.__file__).resolve()
        delegating = [path for path in sources if 'tests.stdio_server import' in path.read_text()]
        self.assertIn(helper, [path.resolve() for path in launchers])
        self.assertGreater(len(launchers) + len(delegating), 20)
        for path in launchers:
            self.assertTrue(any(guard in path.read_text() for guard in guards), path)
        with patch.object(stdio_server.subprocess, 'Popen', side_effect=OSError('launch observed')) as launched:
            with self.assertRaisesRegex(OSError, 'launch observed'):
                stdio_server.StdioServer(ROOT, purpose='application', options=('--observe-database', str(self.database)))
        self.assertEqual(launched.call_args.args[0][-1], '--no-observe', 'the helper disables recording on every launch')


class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name) / 'home'
        self.home.mkdir()
        self.database = Path(self.temporary.name) / 'observer.sqlite'

    def census(self):
        with sqlite3.connect(self.database) as db:
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
            return (db.execute('SELECT count(*) FROM interactions').fetchone()[0],
                    db.execute('SELECT count(*) FROM events').fetchone()[0],
                    db.execute('SELECT count(*) FROM (SELECT 1 FROM interactions i JOIN events e ON e.interaction=i.id '
                               'GROUP BY i.session HAVING count(*)=22)').fetchone()[0],
                    db.execute('SELECT coalesce(sum(lost),0) FROM sessions').fetchone()[0])

    def test_always_on_by_default_in_both_purposes_invisible_and_two_off_switches(self):
        messages = [request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {},
                                           'clientInfo': {'name': 'default-on-fixture', 'version': '7'}}),
                    {'jsonrpc': '2.0', 'method': 'notifications/initialized'}, request('tools/list', identifier=2),
                    request('tools/call', {'name': 'runtime_info', 'arguments': {}}, identifier=3)]
        payload = ''.join(json.dumps(message) + '\n' for message in messages)
        def run(purpose, *flags, **variables):
            process = subprocess.run([sys.executable, '-m', MCP_MODULE, '--repo-root', str(ROOT), '--purpose', purpose, *flags],
                                     cwd=ROOT, env=environment(self.home, **variables), input=payload,
                                     capture_output=True, text=True, timeout=60)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stderr, '', 'recording health is silent unless something is wrong')
            return re.sub('[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}', 'INSTANCE', process.stdout)
        silent = [run('application', '--no-observe'), run('application', STANDARDS_ENGINE_OBSERVE='off'),
                  run('application', '--observe-database', str(self.database), STANDARDS_ENGINE_OBSERVE=' OFF ')]
        self.assertEqual(list(self.home.iterdir()), [], 'both off switches leave no file or directory')
        self.assertFalse(self.database.exists())
        observed = run('application')
        self.assertEqual({observed}, set(silent), 'recording changes no protocol byte')
        run('authoring')
        default = self.home / '.local/share/standards-engine/observations' / DEFAULT_DATABASE_NAME
        self.assertEqual(stat.S_IMODE(default.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(default.parent.stat().st_mode), 0o700)
        summary = report(default)
        self.assertEqual((summary['retained_starts'], summary['retained_terminals']), (6, 6))
        self.assertEqual([(row['client'], row['purpose'], row['sessions'], row['calls']) for row in summary['clients']],
                         [('default-on-fixture 7', 'application', 1, 3), ('default-on-fixture 7', 'authoring', 1, 3)])
        self.assertEqual({row['deployment'] for row in summary['sessions']}, {'local'})
        run('application', XDG_DATA_HOME=str(self.home / 'xdg'), STANDARDS_ENGINE_OBSERVE='on')
        self.assertEqual(report(self.home / 'xdg/standards-engine/observations' / DEFAULT_DATABASE_NAME)['retained_starts'], 3)
        run('application', '--observe-database', str(self.database), '--observe-deployment', 'explicit')
        self.assertEqual(report(self.database)['sessions'][0]['deployment'], 'explicit')
        self.assertEqual(report(default)['retained_starts'], 6)

    def test_cold_stdio_restart_bytes_identity_and_operator_cli(self):
        messages = [request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {}}),
                    {'jsonrpc': '2.0', 'method': 'notifications/initialized'}, request('tools/list'),
                    request('tools/call', {'name': 'describe_input', 'arguments': {'operation': 'runtime_info'}}),
                    request('tools/call', {'name': 'runtime_info', 'arguments': {'unexpected': 'SYNTHETIC_SECRET'}}),
                    request('tools/call', {'name': 'runtime_info', 'arguments': {}})]
        payload = ''.join(json.dumps(message) + '\n' for message in messages)
        command = [sys.executable, '-m', MCP_MODULE, '--repo-root', str(ROOT), '--purpose', 'authoring',
                   '--output-schemas', 'on-demand', '--observe-database', str(self.database), '--observe-deployment', 'cold-test']
        identities = []
        for _ in range(2):
            process = subprocess.run(command, cwd=ROOT, env=environment(self.home), input=payload,
                                     capture_output=True, text=True, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stderr, '')
            responses = [json.loads(line) for line in process.stdout.splitlines()]
            identity = responses[0]['result']['_meta']['standards-engine/runtime']
            identities.append(identity)
            with sqlite3.connect(self.database) as db:
                row = db.execute('SELECT runtime FROM sessions WHERE id=?', (identity['instance_id'],)).fetchone()
                self.assertEqual(json.loads(row[0]), identity)
                counts = db.execute('SELECT sum(request_bytes) FROM interactions WHERE session=?', (identity['instance_id'],)).fetchone()[0]
                notification_bytes = len((json.dumps(messages[1]) + '\n').encode())
                self.assertEqual(counts, len(payload.encode()) - notification_bytes)
                output_bytes, result_bytes = db.execute(
                    'SELECT sum(e.response_bytes),sum(e.result_bytes) FROM events e JOIN interactions i '
                    'ON i.id=e.interaction WHERE session=?', (identity['instance_id'],)).fetchone()
                self.assertEqual(output_bytes, len(process.stdout.encode()))
                self.assertEqual(result_bytes, sum(len(response['result']['content'][0]['text']) for response in responses[2:]))
                self.assertLess(2 * result_bytes, output_bytes)
        self.assertNotEqual(identities[0]['instance_id'], identities[1]['instance_id'])
        for key in ('implementation_digest', 'schema_digest', 'catalog_digest', 'interface_version'):
            self.assertEqual(identities[0][key], identities[1][key])
        summary = report(self.database)
        self.assertEqual(summary['retained_starts'], 10)
        self.assertEqual(summary['retained_terminals'], 10)
        self.assertEqual({row['scope'] for row in summary['operations']}, {'stdio-flushed'})
        before = self.database.read_bytes()
        cli = [sys.executable, '-m', MODULE, '--database', str(self.database)]
        result = subprocess.run(cli + ['--format', 'json', '--limit', '2'], cwd=ROOT, env=environment(self.home),
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['retained_starts'], 10)
        self.assertLess(len(result.stdout), 16_000, 'no per-session schema digests in the report')
        result = subprocess.run(cli + ['--since-days', '1'], cwd=ROOT, env=environment(self.home),
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('10 calls: 0 without an outcome', result.stdout)
        self.assertRegex(result.stdout, r'runtime_info +4 +50\.0%')
        self.assertNotIn('SYNTHETIC_SECRET', result.stdout)
        self.assertEqual(self.database.read_bytes(), before)
        # Without --database the report reads the always-on location, here an empty home.
        result = subprocess.run(cli[:3], cwd=ROOT, env=environment(self.home), capture_output=True, text=True, timeout=30)
        self.assertEqual((result.returncode, result.stdout), (1, ''))
        self.assertEqual(list(self.home.iterdir()), [])

    def test_process_kill_leaves_unmatched_start_and_replacement_does_not_complete_it(self):
        script = '''
import sys, threading
from pathlib import Path
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_engine.standards_engine.interaction_observer import RecorderConfig
server=MCPServer(Path(sys.argv[1]), purpose='authoring', observation=RecorderConfig(Path(sys.argv[2]), 'kill-test'))
def blocked(method, params):
    print('entered-domain', file=sys.stderr, flush=True)
    threading.Event().wait()
server._request=blocked
serve(server,sys.stdin,sys.stdout)
'''
        process = subprocess.Popen([sys.executable, '-c', script, str(ROOT), str(self.database)], cwd=ROOT,
                                   env=environment(self.home),
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            process.stdin.write(json.dumps(request('ping')) + '\n')
            process.stdin.flush()
            self.assertEqual(process.stderr.readline().strip(), 'entered-domain')
            process.kill()
            process.communicate(timeout=10)
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=10)
        replacement = subprocess.run([sys.executable, '-m', MCP_MODULE, '--purpose', 'authoring',
                                      '--observe-database', str(self.database), '--observe-deployment', 'replacement'],
                                     cwd=ROOT, env=environment(self.home), input=json.dumps(request('ping')) + '\n',
                                     text=True, capture_output=True, timeout=30)
        self.assertEqual(replacement.returncode, 0, replacement.stderr)
        summary = report(self.database)
        self.assertEqual(summary['retained_starts'], 2)
        self.assertEqual(summary['retained_terminals'], 1)
        self.assertEqual(summary['unmatched_starts'], 1)
        self.assertIn('2 calls: 1 without an outcome', text_report(summary))

    def test_eight_recorders_creating_one_database_at_the_same_instant_lose_nothing(self):
        script = '''
import io, sys, time
from pathlib import Path
from tools.standards_engine.standards_engine.interaction_observer import InteractionRecorder, RecorderConfig
while time.time() < float(sys.argv[2]):
    pass
recorder = InteractionRecorder(RecorderConfig(Path(sys.argv[1]), 'simultaneous'), {'instance_id': sys.argv[3], 'catalog_digest': 'c'},
                               [{'name': 'runtime_info', 'inputSchema': {'type': 'object'}}], diagnostics=io.StringIO())
calls = [('initialize', {}), ('tools/list', {})] + [('tools/call', {'name': 'runtime_info', 'arguments': {}})] * 20
for identifier, (method, params) in enumerate(calls):
    ticket = recorder.begin({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params}, request_bytes=1, scope='constructed')
    recorder.finish(ticket, {'result': {}}, response_bytes=1)
recorder.close()
'''
        for attempt in range(3):
            self.database = Path(self.temporary.name) / f'simultaneous-{attempt}.sqlite'
            instant = time.time() + 1.5  # After every interpreter has imported the Engine.
            workers = [subprocess.Popen([sys.executable, '-c', script, str(self.database), str(instant), f'worker-{index}'],
                                        cwd=ROOT, env=environment(self.home), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                       for index in range(8)]
            for worker in workers:
                output, errors = worker.communicate(timeout=60)
                self.assertEqual(worker.returncode, 0, errors)
            self.assertEqual(self.census(), (176, 176, 8, 0))

    def servers(self, count=8):
        command = [sys.executable, '-m', MCP_MODULE, '--repo-root', str(ROOT), '--purpose', 'application',
                   '--output-schemas', 'on-demand', '--observe-database', str(self.database)]
        return [subprocess.Popen(command, cwd=ROOT, env=environment(self.home), stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(count)]

    def lines(self, *messages):
        return ''.join(json.dumps(message) + '\n' for message in messages)

    def collect(self, workers, responses):
        errors = []
        try:
            for worker in workers:
                output, error = worker.communicate(timeout=60)
                self.assertEqual(worker.returncode, 0, error)
                self.assertEqual(len(output.splitlines()), responses)
                errors.append(error)
        finally:
            for worker in workers:
                if worker.poll() is None:
                    worker.kill()
                    worker.communicate(timeout=10)
        return errors

    def test_eight_server_processes_started_together_record_every_call(self):
        opening = self.lines(request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {},
                                                    'clientInfo': {'name': 'fan-out', 'version': '1'}}),
                             {'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        calls = self.lines(request('tools/list', identifier=2),
                           *(request('tools/call', {'name': 'runtime_info', 'arguments': {}}, identifier=3 + index) for index in range(20)))
        # No database exists yet: all eight create it while starting.
        workers = self.servers()
        for worker in workers:
            worker.stdin.write(opening + calls)
            worker.stdin.flush()
        self.collect(workers, 22)
        self.assertEqual(self.census(), (176, 176, 8, 0))
        # Again while another connection holds the write lock for 500 ms.
        workers = self.servers()
        try:
            for worker in workers:
                worker.stdin.write(opening)
                worker.stdin.flush()
            for worker in workers:
                self.assertIn('"result"', worker.stdout.readline())
            lock = sqlite3.connect(self.database, isolation_level=None)
            lock.execute('BEGIN IMMEDIATE')
            for worker in workers:
                worker.stdin.write(calls)
                worker.stdin.flush()
            time.sleep(0.5)
            self.assertEqual(self.census()[0], 184, 'nothing is written while the lock is held')
            lock.execute('ROLLBACK')
            lock.close()
        finally:
            errors = self.collect(workers, 21)
        self.assertEqual(self.census(), (352, 352, 16, 0))
        locked = [error for error in errors if '"reason":"storage-locked"' in error]
        self.assertTrue(locked, 'the lock must have forced at least one process to use its backlog')
        for error in errors:
            if error:
                final = json.loads(error.splitlines()[-1].split(' ', 2)[2])
                self.assertEqual((final['state'], final['backlog'], final['lost']), ('healthy', 0, 0))


if __name__ == '__main__':
    unittest.main()
