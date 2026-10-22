"""Real stdio and SQLite evidence; invocation literals independently own expectations."""
from __future__ import annotations

import json
import os
import select
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

from tools.standards_engine.tests import test_purpose_transport as fixture

ROOT = fixture.ROOT


def request(identifier, method, params):
    return {'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params}


def without_instance(responses):
    """Normalize only the known per-process UUID, including its text encoding."""
    initialized = next(row for row in responses if row.get('id') == 1)
    instance = initialized['result']['_meta']['standards-engine/runtime']['instance_id']
    return json.loads(json.dumps(responses).replace(instance, '<process-instance>'))


class InteractionObservationTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeTransportTest.setUpClass()
        cls.root = fixture.PurposeTransportTest.root
        cls.snapshot = fixture.PurposeTransportTest.snapshot
        cls.expected = fixture.PurposeTransportTest.expected

    @classmethod
    def tearDownClass(cls):
        fixture.PurposeTransportTest.tearDownClass()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='observation-stdio-')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def messages(self):
        invocations = [
            {'name': 'runtime_info'},
            {'name': 'unavailable', 'arguments': {'literal': [None, False, 'é']}, 'extra': True},
            {'name': 'read', 'arguments': []},
            {'arguments': None},
            {'name': 'runtime_info', 'arguments': {'unknown': 'private-request-marker'}},
            {'name': 'describe_input', 'arguments': {'operation': 'read'}},
            {'name': 'describe_output', 'arguments': {'operation': 'read'}},
            {'name': 'read', 'arguments': {'snapshot': self.snapshot, 'target': 'core', 'detail': 'full'}},
            {'name': 'read', 'arguments': {'snapshot': self.snapshot, 'target': 'provenance.fixture'}},
        ]
        messages = [request(1, 'initialize', {'protocolVersion': '2025-11-25', 'capabilities': {},
                     'clientInfo': {'name': 'observation-fixture', 'version': '1'}}),
                    {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                    request(2, 'tools/list', {}), request(3, 'ping', {})]
        messages += [request(i, 'tools/call', value) for i, value in enumerate(invocations, 10)]
        messages += [request(30, 'tools/list', {'cursor': 'invalid'}),
                     request(31, 'unsupported', {}),
                     request(32, 'tools/call', []),
                     {'jsonrpc': '2.0', 'method': 'notifications/cancelled'}]
        return messages, invocations

    def launch(self, messages, path=None, purpose='application', *options):
        command = [sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp',
                   '--repo-root', str(self.root), '--purpose', purpose, *options]
        if path is not None:
            command += ['--observation-db', str(path)]
        process = subprocess.run(command, input='bad json\n' + ''.join(json.dumps(m) + '\n' for m in messages),
                                 capture_output=True, text=True, cwd=self.directory,
                                 env={**os.environ, 'PYTHONPATH': str(ROOT)}, timeout=90)
        self.assertEqual(process.returncode, 0, process.stderr)
        return [json.loads(line) for line in process.stdout.splitlines()], process.stderr

    def test_order_identity_metadata_and_enabled_disabled_failed_invisibility(self):
        messages, invocations = self.messages()
        disabled, stderr = self.launch(messages)
        self.assertEqual(stderr, '')
        self.assertEqual(list(self.directory.iterdir()), [])
        path = self.directory / 'observations.sqlite3'
        enabled, stderr = self.launch(messages, path)
        self.assertEqual(stderr, '')
        self.assertEqual(without_instance(enabled), without_instance(disabled))
        failed, stderr = self.launch(messages, self.directory / 'missing' / 'observations.sqlite3')
        self.assertEqual(without_instance(failed), without_instance(disabled))
        self.assertEqual(stderr, 'Interaction observation disabled: initialization failed (OperationalError).\n')
        self.assertFalse((self.directory / 'missing').exists())
        responses = {v['id']: v for v in enabled}
        identity = responses[1]['result']['_meta']['standards-engine/runtime']
        self.assertEqual(responses[17]['result']['structuredContent']['content'], self.expected)
        self.assertTrue(responses[18]['result']['isError'])
        for identifier in (11, 12, 13, 30, 31, 32):
            self.assertIn('error', responses[identifier])
        with sqlite3.connect(path) as db:
            session = db.execute('SELECT interface_version,catalog_digest,schema_digest,purpose,ended_at,session_metadata_json FROM sessions').fetchall()
            self.assertEqual(len(session), 1)
            self.assertEqual(session[0][:4], tuple(identity[k] for k in ('interface_version', 'catalog_digest', 'schema_digest', 'purpose')))
            self.assertIsNotNone(session[0][4])
            self.assertIsNone(session[0][5])
            rows = db.execute('SELECT sequence_number,request_json,response_metadata_json FROM interactions ORDER BY sequence_number').fetchall()
            self.assertEqual([r[0] for r in rows], list(range(1, len(invocations) + 1)))
            self.assertEqual([json.loads(r[1]) for r in rows], invocations)
            for row, identifier in zip(rows, range(10, 19)):
                if identifier in (11, 12, 13):
                    self.assertIsNone(row[2])
                else:
                    value = responses[identifier]['result']['structuredContent']
                    expected = {k: value[k] for k in ('kind', 'code', 'outcome', 'status') if k in value}
                    self.assertEqual(json.loads(row[2]), expected)
                    self.assertNotIn(self.expected, row[2])
                    self.assertNotIn('private-request-marker', row[2])
        # Configuration and private handles never enter any result or catalog.
        public = json.dumps(enabled)
        for private in ('observation-db', str(path), 'sequence_number', 'response_metadata_json'):
            self.assertNotIn(private, public)

    def test_cold_sessions_append_and_reuse_actual_selected_identity(self):
        path = self.directory / 'observations.sqlite3'
        messages, invocations = self.messages()
        for purpose, options in (('application', ['--output-schemas', 'on-demand']),
                                 ('authoring', ['--advanced'])):
            enabled, stderr = self.launch(messages, path, purpose, *options)
            self.assertEqual(stderr, '')
            disabled, stderr = self.launch(messages, None, purpose, *options)
            self.assertEqual(stderr, '')
            self.assertEqual(without_instance(enabled), without_instance(disabled))
            identity = next(v for v in enabled if v['id'] == 1)['result']['_meta']['standards-engine/runtime']
            with sqlite3.connect(path) as db:
                session = db.execute('SELECT interface_version,catalog_digest,schema_digest,purpose FROM sessions ORDER BY id DESC LIMIT 1').fetchone()
                self.assertEqual(session, tuple(identity[k] for k in ('interface_version', 'catalog_digest', 'schema_digest', 'purpose')))
        with sqlite3.connect(path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM sessions').fetchone(), (2,))
            self.assertEqual(db.execute('SELECT COUNT(*) FROM interactions').fetchone(), (2 * len(invocations),))
            for session in (1, 2):
                self.assertEqual([row[0] for row in db.execute('SELECT sequence_number FROM interactions WHERE session_id=? ORDER BY sequence_number', (session,))], list(range(1, 10)))

    def test_real_write_failure_after_handshake_is_invisible_and_inert(self):
        path = self.directory / 'write-failure.sqlite3'
        messages, _ = self.messages()
        disabled, _ = self.launch(messages)
        command = [sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp',
                   '--repo-root', str(self.root), '--purpose', 'application',
                   '--observation-db', str(path)]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=self.directory,
                                   env={**os.environ, 'PYTHONPATH': str(ROOT)})
        try:
            # Wait for an actual initialized process, then fail its first request insert.
            process.stdin.write(('bad json\n' + json.dumps(messages[0]) + '\n').encode())
            process.stdin.flush()
            deadline = time.monotonic() + 30
            prefix_bytes = bytearray()
            while prefix_bytes.count(b'\n') < 2:
                remaining = deadline - time.monotonic()
                self.assertGreater(remaining, 0, 'MCP initialization exceeded the harness deadline')
                readable, _, _ = select.select([process.stdout], [], [], remaining)
                self.assertTrue(readable, 'MCP initialization did not produce a response')
                chunk = os.read(process.stdout.fileno(), 4096)
                self.assertTrue(chunk, 'MCP process ended before initialization')
                prefix_bytes.extend(chunk)
            prefix = [json.loads(line) for line in prefix_bytes.splitlines()]
            with sqlite3.connect(path) as db:
                db.execute("CREATE TRIGGER fail BEFORE INSERT ON interactions BEGIN SELECT RAISE(ABORT, 'private-request-marker'); END")
            output, stderr = process.communicate(''.join(json.dumps(m) + '\n' for m in messages[1:]).encode(), timeout=90)
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()
        self.assertEqual(process.returncode, 0)
        stderr = stderr.decode()
        responses = prefix + [json.loads(line) for line in output.splitlines()]
        self.assertEqual(without_instance(responses), without_instance(disabled))
        self.assertEqual(stderr, 'Interaction observation disabled: request write failed (IntegrityError).\n')
        with sqlite3.connect(path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM interactions').fetchone(), (0,))
            self.assertEqual(db.execute('SELECT COUNT(*) FROM sessions').fetchone(), (1,))
            self.assertIsNone(db.execute('SELECT ended_at FROM sessions').fetchone()[0])

    def test_unsupported_database_is_preserved_and_agent_results_match(self):
        path = self.directory / 'future.sqlite3'
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE historical (body TEXT)')
            db.execute("INSERT INTO historical VALUES ('operator-owned')")
            db.execute('PRAGMA user_version=99')
        before = path.read_bytes()
        messages, _ = self.messages()
        disabled, _ = self.launch(messages)
        failed, stderr = self.launch(messages, path)
        self.assertEqual(without_instance(failed), without_instance(disabled))
        self.assertEqual(stderr, 'Interaction observation disabled: initialization failed (ValueError).\n')
        self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
