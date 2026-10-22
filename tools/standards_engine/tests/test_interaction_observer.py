"""Synthetic operator evidence; never records a real agent/model session."""
from __future__ import annotations

from contextlib import redirect_stderr
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine.interaction_observer import (
    APPLICATION_ID, InputShape, InteractionRecorder, RecorderConfig, SCHEMA_VERSION,
    report,
)
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.test_mcp import ROOT, initialize, request

MODULE = 'tools.standards_engine.standards_engine.interaction_observer'
MCP_MODULE = 'tools.standards_engine.standards_engine.mcp'


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.database = Path(self.temporary.name) / 'observations.sqlite'
        self.diagnostics = io.StringIO()

    def server(self, **options):
        with redirect_stderr(self.diagnostics):
            server = MCPServer(ROOT, purpose='authoring',
                               observation=RecorderConfig(self.database, 'synthetic', **options))
        self.addCleanup(server.close)
        return server

    def rows(self, sql):
        with sqlite3.connect(self.database) as db:
            db.row_factory = sqlite3.Row
            return [dict(row) for row in db.execute(sql)]

    def test_opt_in_does_not_change_catalog_or_results(self):
        plain = MCPServer(ROOT, purpose='authoring')
        self.addCleanup(plain.close)
        observed = self.server()
        self.assertEqual(plain.tools, observed.tools)
        for server in (plain, observed):
            initialize(server)
        # A fixed process identity makes these full public responses comparable.
        observed._runtime_identity._instance = plain._runtime_identity._instance
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
        feedback = shape.feedback({'issues': [
            {'instance_pointer': '/facts/facts/body', 'keyword': 'type', 'message': 'CREDENTIAL'},
            {'instance_pointer': '/items/8/selector', 'keyword': 'required'},
            {'instance_pointer': '/body/token', 'keyword': 'CREDENTIAL'},
        ]})
        self.assertEqual(feedback, [{'pointer': '/facts/*/*', 'keyword': 'type'},
                                    {'pointer': '/items/*/selector', 'keyword': 'required'},
                                    {'pointer': '/body/*', 'keyword': 'other'}])
        # Deep/large adversarial data is bounded without traversing unknown maps.
        projected = shape.project({'items': [{'selector': 'x' * 1_000_000}] * 100_000})
        self.assertLess(len(json.dumps(projected)), 8192)

    def test_privacy_at_real_dispatch_and_disk_boundary(self):
        server = self.server()
        initialize(server)
        secrets = ['SYNTHETIC_PASSWORD_847', 'SYNTHETIC_PROMPT_738', 'SYNTHETIC_REPO_339']
        server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {
            'expected_catalog': secrets[0], secrets[1]: secrets[2]}}, identifier=secrets[0]))
        server.dispatch(request('tools/call', {'name': secrets[1], 'arguments': {'body': secrets[2]}}))
        server.dispatch(request('initialize', {'clientInfo': {'name': secrets[0]}}))
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
                      request('tools/call', {'name': []}), request('ping', [])):
            server.dispatch(value)
        output = io.StringIO()
        serve(server, io.StringIO('{BAD JSON\n'), output)
        self.assertEqual(json.loads(output.getvalue())['error']['code'], -32700)
        self.assertEqual(server._observer.health['state'], 'healthy')
        self.assertEqual(report(self.database)['retained_starts'], 8)
        self.assertIn('parse-error', {row['outcome'] for row in self.rows('SELECT outcome FROM events')})

    def test_tool_exception_interruption_and_delivery_failure(self):
        server = self.server()
        initialize(server)
        with patch.object(AgentToolFacade, 'open_repository') as opened, redirect_stderr(io.StringIO()):
            opened.return_value.__enter__.side_effect = RuntimeError('SENSITIVE_EXCEPTION')
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
        self.assertNotIn('SENSITIVE_', self.database.read_bytes().decode(errors='ignore'))

    def test_unavailable_locked_and_failed_health_sink_preserve_responses(self):
        unavailable = Path(self.temporary.name) / 'missing' / 'db'
        with redirect_stderr(io.StringIO()):
            server = MCPServer(ROOT, purpose='authoring', observation=RecorderConfig(unavailable, 'synthetic'))
        self.addCleanup(server.close)
        self.assertEqual(server.dispatch(request('ping'))['result'], {})
        self.assertEqual(server._observer.health['state'], 'degraded')
        observed = self.server()
        with sqlite3.connect(self.database, isolation_level=None) as lock:
            lock.execute('BEGIN IMMEDIATE')
            before = time.monotonic()
            response = observed.dispatch(request('ping'))
            elapsed = time.monotonic() - before
            lock.execute('ROLLBACK')
        self.assertEqual(response['result'], {})
        self.assertEqual(observed._observer.health['reason'], 'storage-locked')
        self.assertLess(elapsed, 1, '20ms SQLite busy policy must not wait indefinitely')
        class BrokenDiagnostics:
            def write(self, value):
                raise OSError('private')
            def flush(self):
                raise OSError('private')
        recorder = InteractionRecorder(RecorderConfig(unavailable, 'synthetic'), {}, [], diagnostics=BrokenDiagnostics())
        recorder.close()
        self.assertEqual(recorder.health['state'], 'degraded')

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

    def test_migration_reopen_unsupported_corrupt_and_spoofed(self):
        server = self.server()
        server.dispatch(request('ping'))
        server.close()
        with sqlite3.connect(self.database) as db:
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], SCHEMA_VERSION)
            self.assertEqual(db.execute('PRAGMA application_id').fetchone()[0], APPLICATION_ID)
        again = self.server()
        again.dispatch(request('ping'))
        again.close()
        self.assertEqual(report(self.database)['retained_starts'], 2)
        for name, setup in (
            ('future', 'PRAGMA user_version=999'),
            ('unrelated', 'CREATE TABLE business (secret TEXT)'),
            ('spoofed', f'PRAGMA user_version=1; PRAGMA application_id={APPLICATION_ID}; CREATE TABLE sessions(id TEXT)'),
        ):
            target = Path(self.temporary.name) / name
            with sqlite3.connect(target) as db:
                db.executescript(setup)
            target.chmod(0o600)
            before = target.read_bytes()
            with redirect_stderr(io.StringIO()):
                recorder = InteractionRecorder(RecorderConfig(target, 'synthetic'), {}, [])
            self.assertEqual(recorder.health['state'], 'degraded')
            self.assertEqual(target.read_bytes(), before)
        corrupt = Path(self.temporary.name) / 'corrupt'
        corrupt.write_bytes(b'not sqlite sensitive synthetic')
        corrupt.chmod(0o600)
        before = corrupt.read_bytes()
        recorder = InteractionRecorder(RecorderConfig(corrupt, 'synthetic'), {}, [], diagnostics=io.StringIO())
        self.assertEqual(recorder.health['state'], 'degraded')
        self.assertEqual(corrupt.read_bytes(), before)

    def test_unsupported_journal_and_page_budget_never_publish_migration(self):
        for name, pragma in (('wal', 'PRAGMA journal_mode=WAL'),):
            path = Path(self.temporary.name) / name
            with sqlite3.connect(path) as db:
                db.execute(pragma)
            path.chmod(0o600)
            before = path.read_bytes()
            recorder = InteractionRecorder(RecorderConfig(path, 'synthetic', max_bytes=1024*1024),
                                           {}, [], diagnostics=io.StringIO())
            self.assertEqual(recorder.health['state'], 'degraded')
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
        self.assertEqual(first._observer.health['dropped_observations'], 1)
        first.dispatch(request('ping'))
        self.assertEqual(first._observer.health['recorded_terminals'], 1)
        summary = report(self.database)
        self.assertEqual(summary['retained_starts'], 16)
        self.assertEqual(summary['retained_terminals'], 16)

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

    def test_arbitrary_outputs_are_never_retained(self):
        server = self.server()
        initialize(server)
        secret = 'SYNTHETIC_OUTPUT_CREDENTIAL'
        result = {'structuredContent': {'body': secret, 'outcome': secret,
                  'input_feedback': {'issues': [{'instance_pointer': '/' + secret,
                                                'keyword': secret, 'message': secret}]}}, 'isError': True}
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
            payload = '{"jsonrpc":"2.0","id":"\ud800","method":"ping"}\n'
            serve(server, io.StringIO(payload), output)
            self.assertEqual(json.loads(output.getvalue())['result'], {})



class ProcessTests(unittest.TestCase):
    def test_cold_stdio_restart_bytes_identity_and_operator_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / 'observer.sqlite'
            messages = [request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {}}),
                        {'jsonrpc': '2.0', 'method': 'notifications/initialized'}, request('tools/list'),
                        request('tools/call', {'name': 'describe_input', 'arguments': {'operation': 'runtime_info'}}),
                        request('tools/call', {'name': 'runtime_info', 'arguments': {'unexpected': 'SYNTHETIC_SECRET'}}),
                        request('tools/call', {'name': 'runtime_info', 'arguments': {}})]
            payload = ''.join(json.dumps(message) + '\n' for message in messages)
            command = [sys.executable, '-m', MCP_MODULE, '--repo-root', str(ROOT), '--purpose', 'authoring',
                       '--output-schemas', 'on-demand', '--observe-database', str(database), '--observe-deployment', 'cold-test']
            identities = []
            for _ in range(2):
                process = subprocess.run(command, cwd=ROOT, input=payload, capture_output=True, text=True, timeout=30)
                self.assertEqual(process.returncode, 0, process.stderr)
                responses = [json.loads(line) for line in process.stdout.splitlines()]
                identity = responses[0]['result']['_meta']['standards-engine/runtime']
                identities.append(identity)
                with sqlite3.connect(database) as db:
                    row = db.execute('SELECT runtime FROM sessions WHERE id=?', (identity['instance_id'],)).fetchone()
                    self.assertEqual(json.loads(row[0]), identity)
                    counts = db.execute('SELECT sum(request_bytes) FROM interactions WHERE session=?', (identity['instance_id'],)).fetchone()[0]
                    notification_bytes = len((json.dumps(messages[1]) + '\n').encode())
                    self.assertEqual(counts, len(payload.encode()) - notification_bytes)
                    output_bytes = db.execute('SELECT sum(e.response_bytes) FROM events e JOIN interactions i '
                                             'ON i.id=e.interaction WHERE session=?', (identity['instance_id'],)).fetchone()[0]
                    self.assertEqual(output_bytes, len(process.stdout.encode()))
                self.assertIn('"state":"healthy"', process.stderr)
            self.assertNotEqual(identities[0]['instance_id'], identities[1]['instance_id'])
            for key in ('implementation_digest', 'schema_digest', 'catalog_digest', 'interface_version'):
                self.assertEqual(identities[0][key], identities[1][key])
            summary = report(database)
            self.assertEqual(summary['retained_starts'], 10)
            self.assertEqual(summary['retained_terminals'], 10)
            self.assertEqual({row['scope'] for row in summary['operations']}, {'stdio-flushed'})
            before = database.read_bytes()
            result = subprocess.run([sys.executable, '-m', MODULE, '--database', str(database), '--limit', '2'],
                                    cwd=ROOT, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['retained_starts'], 10)
            self.assertEqual(database.read_bytes(), before)

    def test_process_kill_leaves_unmatched_start_and_replacement_does_not_complete_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / 'observer.sqlite'
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
            process = subprocess.Popen([sys.executable, '-c', script, str(ROOT), str(database)], cwd=ROOT,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                process.stdin.write(json.dumps(request('ping')) + '\n')
                process.stdin.flush()
                self.assertIn('healthy', process.stderr.readline())
                self.assertEqual(process.stderr.readline().strip(), 'entered-domain')
                process.kill()
                process.communicate(timeout=10)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate(timeout=10)
            replacement = subprocess.run([sys.executable, '-m', MCP_MODULE, '--purpose', 'authoring',
                                          '--observe-database', str(database), '--observe-deployment', 'replacement'],
                                         cwd=ROOT, input=json.dumps(request('ping')) + '\n',
                                         text=True, capture_output=True, timeout=30)
            self.assertEqual(replacement.returncode, 0, replacement.stderr)
            summary = report(database)
            self.assertEqual(summary['retained_starts'], 2)
            self.assertEqual(summary['retained_terminals'], 1)
            self.assertEqual(summary['unmatched_starts'], 1)

    def test_concurrent_processes_and_first_open_never_overwrite_or_duplicate(self):
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / 'observer.sqlite'
            command = [sys.executable, '-m', MCP_MODULE, '--purpose', 'authoring',
                       '--observe-database', str(database), '--observe-deployment', 'concurrent']
            workers = [subprocess.Popen(command, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True) for _ in range(4)]
            try:
                outputs = []
                for worker in workers:
                    worker.stdin.write(''.join(json.dumps(request('ping', identifier=i)) + '\n' for i in range(5)))
                    worker.stdin.flush()
                for worker in workers:
                    output, errors = worker.communicate(timeout=30)
                    self.assertEqual(worker.returncode, 0, errors)
                    self.assertEqual(len(output.splitlines()), 5)
                    outputs.append(errors)
            finally:
                for worker in workers:
                    if worker.poll() is None:
                        worker.kill()
                        worker.communicate(timeout=10)
            # Contention may intentionally degrade a process after the 20ms budget.
            # A failed terminal write may leave an unmatched begin; no duplicate or
            # fabricated terminal is permitted. Domain replies still total 20.
            summary = report(database)
            self.assertGreater(summary['retained_starts'], 0)
            self.assertLessEqual(summary['retained_starts'], 20)
            self.assertLessEqual(summary['retained_terminals'], summary['retained_starts'])
            with sqlite3.connect(database) as db:
                self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
                self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
            self.assertTrue(all('healthy' in output or 'degraded' in output for output in outputs))


if __name__ == '__main__':
    unittest.main()
