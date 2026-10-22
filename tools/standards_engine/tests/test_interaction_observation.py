from __future__ import annotations

from contextlib import chdir, redirect_stderr
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine.interaction_observation import (
    InertInteractionRecorder, SQLiteInteractionRecorder,
)
from tools.standards_engine.standards_engine.mcp import MCPServer, _response_metadata
from tools.standards_engine.tests.test_mcp import initialize, request, ROOT
from tools.standards_engine.standards_engine.tools import AgentToolFacade

IDENTITY = {"interface_version": 45, "catalog_digest": "fixture-catalog",
            "schema_digest": "fixture-schema", "purpose": "authoring"}


class InteractionObservationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="interaction-observation-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "observations.sqlite3"

    def recorder(self):
        recorder = SQLiteInteractionRecorder(self.path)
        self.addCleanup(recorder.close)
        recorder.begin_session(IDENTITY)
        return recorder

    def test_disabled_has_no_state_serialization_or_database(self):
        with (patch('sqlite3.connect', side_effect=AssertionError("database opened")),
              patch('json.dumps', side_effect=AssertionError("serialized"))):
            recorder = InertInteractionRecorder()
            recorder.begin_session(IDENTITY, object())
            self.assertIsNone(recorder.record_request(object()))
            recorder.record_response_metadata(None, object())
            recorder.close()
            self.assertFalse(hasattr(recorder, '__dict__'))
        self.assertEqual(list(Path(self.temp.name).iterdir()), [])

    def test_literal_capture_order_commits_identity_and_cold_reopen(self):
        supplied = [{"name": "unknown", "arguments": None, "extra": [False, 0, "é"]},
                    {"name": "runtime_info"}, {}]
        recorder = self.recorder()
        for invocation in supplied:
            recorder.record_request(invocation)
        # A separate reader observes committed requests before recorder close.
        with sqlite3.connect(self.path) as db:
            rows = db.execute('SELECT sequence_number, request_json, response_metadata_json '
                              'FROM interactions ORDER BY sequence_number').fetchall()
            self.assertEqual([r[0] for r in rows], [1, 2, 3])
            self.assertEqual([json.loads(r[1]) for r in rows], supplied)
            self.assertEqual([r[2] for r in rows], [None] * 3)
            self.assertEqual(db.execute('PRAGMA user_version').fetchone(), (1,))
            self.assertEqual(db.execute('SELECT interface_version,catalog_digest,schema_digest,purpose '
                                        'FROM sessions').fetchone(), tuple(IDENTITY.values()))
            self.assertIsNone(db.execute('SELECT ended_at FROM sessions').fetchone()[0])
        recorder.close()
        second = self.recorder()
        handle = second.record_request({"cold": True})
        second.record_response_metadata(handle, {"kind": "fixture"})
        second.close()
        with sqlite3.connect(self.path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM sessions').fetchone(), (2,))
            self.assertTrue(all(row[0] for row in db.execute('SELECT ended_at FROM sessions')))
            self.assertEqual([json.loads(row[0]) for row in db.execute(
                'SELECT request_json FROM interactions ORDER BY id')], supplied + [{"cold": True}])
            self.assertEqual(db.execute('SELECT sequence_number,response_metadata_json FROM interactions '
                                        'WHERE id=?', (handle,)).fetchone(), (1, '{"kind": "fixture"}'))

    def test_path_named_memory_is_a_durable_local_file(self):
        path = Path(self.temp.name) / ':memory:'
        with chdir(self.temp.name):
            recorder = SQLiteInteractionRecorder(Path(':memory:'))
        recorder.begin_session(IDENTITY)
        recorder.record_request({'retained': True})
        recorder.close()
        self.assertTrue(path.is_file())
        with sqlite3.connect(path) as db:
            self.assertEqual(db.execute('SELECT request_json FROM interactions').fetchone(), ('{"retained": true}',))

    def test_schema_constraints_are_enforced_by_real_sqlite(self):
        recorder = self.recorder()
        recorder.record_request({})
        with sqlite3.connect(self.path) as db:
            db.execute('PRAGMA foreign_keys=ON')
            columns = {row[1] for row in db.execute('PRAGMA table_info(sessions)')}
            self.assertEqual(columns, {'id', 'started_at', 'ended_at', 'interface_version',
                                      'catalog_digest', 'schema_digest', 'purpose', 'session_metadata_json'})
            self.assertEqual({row[1] for row in db.execute('PRAGMA table_info(interactions)')},
                             {'id', 'session_id', 'sequence_number', 'observed_at',
                              'request_json', 'response_metadata_json'})
            for session, sequence in ((1, 1), (999, 2)):
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute('INSERT INTO interactions (session_id,sequence_number,observed_at,request_json) '
                               'VALUES (?,?,?,?)', (session, sequence, 'fixture', '{}'))
                db.rollback()

    def test_unknown_version_and_contradictory_schema_preserve_existing_bytes(self):
        for defect in ('version', 'missing-table', 'extra-trigger', 'version-zero', 'extra-column'):
            with self.subTest(defect=defect):
                path = Path(self.temp.name) / (defect + '.sqlite3')
                recorder = SQLiteInteractionRecorder(path)
                recorder.begin_session(IDENTITY)
                recorder.record_request({'original': 'retained'})
                recorder.close()
                with sqlite3.connect(path) as db:
                    if defect == 'version':
                        db.execute('PRAGMA user_version=99')
                    elif defect == 'version-zero':
                        db.execute('PRAGMA user_version=0')
                    elif defect == 'missing-table':
                        db.execute('DROP TABLE interactions')
                    elif defect == 'extra-column':
                        db.execute('ALTER TABLE interactions ADD COLUMN foreign_content TEXT')
                    else:
                        db.execute('CREATE TRIGGER unexpected AFTER INSERT ON interactions BEGIN SELECT 1; END')
                before = path.read_bytes()
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    recorder = SQLiteInteractionRecorder(path)
                    recorder.begin_session(IDENTITY)
                    self.assertIsNone(recorder.record_request({'private': 'do-not-log'}))
                    recorder.close()
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual(len(stderr.getvalue().splitlines()), 1)
                self.assertIn('initialization failed (ValueError)', stderr.getvalue())
                self.assertNotIn('do-not-log', stderr.getvalue())

    def test_missing_parent_is_not_created_and_diagnostic_channel_failure_is_contained(self):
        path = Path(self.temp.name) / 'missing' / 'capture.sqlite3'
        with patch('sys.stderr.write', side_effect=OSError('private channel failure')):
            recorder = SQLiteInteractionRecorder(path)
            recorder.begin_session(IDENTITY)
            self.assertIsNone(recorder.record_request({}))
            recorder.close()
        self.assertFalse(path.parent.exists())

    def test_serialization_failure_is_inert_and_does_not_echo_request(self):
        recorder = self.recorder()
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertIsNone(recorder.record_request({'do-not-log': object()}))
            with patch('json.dumps', side_effect=AssertionError('must be inert')):
                self.assertIsNone(recorder.record_request({'after': True}))
                recorder.record_response_metadata(1, {'after': True})
                recorder.begin_session(IDENTITY)
                recorder.close()
        self.assertEqual(stderr.getvalue(), 'Interaction observation disabled: request write failed (TypeError).\n')
        with sqlite3.connect(self.path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM interactions').fetchone(), (0,))

    def test_each_write_failure_is_bounded_and_stops_subsequent_capture(self):
        for operation, trigger in (
            ('session creation', 'BEFORE INSERT ON sessions'),
            ('request write', 'BEFORE INSERT ON interactions'),
            ('metadata write', 'BEFORE UPDATE ON interactions'),
            ('close', 'BEFORE UPDATE ON sessions'),
        ):
            with self.subTest(operation=operation):
                path = Path(self.temp.name) / (operation + '.sqlite3')
                recorder = SQLiteInteractionRecorder(path)
                if operation != 'session creation':
                    recorder.begin_session(IDENTITY)
                handle = recorder.record_request({'before': True}) if operation in ('metadata write', 'close') else None
                with sqlite3.connect(path) as db:
                    db.execute(f"CREATE TRIGGER fail {trigger} BEGIN SELECT RAISE(ABORT, 'private-payload'); END")
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    if operation == 'session creation':
                        recorder.begin_session(IDENTITY)
                    elif operation == 'request write':
                        recorder.record_request({'private-payload': True})
                    elif operation == 'metadata write':
                        recorder.record_response_metadata(handle, {'private-payload': True})
                    else:
                        recorder.close()
                    self.assertIsNone(recorder.record_request({'after': True}))
                    recorder.record_response_metadata(handle, {})
                    recorder.close()
                self.assertEqual(stderr.getvalue(), f'Interaction observation disabled: {operation} failed (IntegrityError).\n')
                with sqlite3.connect(path) as db:
                    rows = db.execute('SELECT request_json,response_metadata_json FROM interactions').fetchall()
                    self.assertEqual(rows, [('{"before": true}', None)] if handle else [])

    def test_interface_projection_only_selects_string_identifiers(self):
        value = {'kind': 'k', 'code': 'c', 'outcome': 'o', 'status': 's',
                 'content': 'standards', 'structuredContent': {'kind': 'nested'},
                 'message': 'private', 'details': {'private': True}, 'input_feedback': 'private',
                 'continuations': ['private'], 'proposal': 'private'}
        self.assertEqual(_response_metadata(value), {'kind': 'k', 'code': 'c', 'outcome': 'o', 'status': 's'})
        self.assertEqual(_response_metadata({'kind': {'content': 'private'}, 'code': None}), {})
        self.assertEqual(_response_metadata({}), {})

    def test_capture_is_committed_before_dispatch_and_failure_does_not_change_result(self):
        server = MCPServer(ROOT, purpose='application', observation_db=self.path)
        self.addCleanup(server.close)
        initialize(server)
        supplied = {'name': 'read', 'arguments': {'private-request': 'literal'}}
        result = {'kind': 'fixture', 'content': 'not-captured', 'message': 'not-captured', 'status': 'ready'}
        def invoke(arguments):
            with sqlite3.connect(self.path) as db:
                self.assertEqual(json.loads(db.execute('SELECT request_json FROM interactions').fetchone()[0]), supplied)
                # Force response-metadata write failure after the real request commit.
                db.execute("CREATE TRIGGER fail BEFORE UPDATE ON interactions BEGIN SELECT RAISE(ABORT, 'private'); END")
            self.assertEqual(arguments, supplied['arguments'])
            return result
        stderr = io.StringIO()
        with patch.object(AgentToolFacade, 'open_repository') as opened, redirect_stderr(stderr):
            opened.return_value.__enter__.return_value.read.side_effect = invoke
            actual = server.dispatch(request('tools/call', supplied))['result']
        self.assertEqual(actual, server._tool_result(result))
        self.assertEqual(stderr.getvalue(), 'Interaction observation disabled: metadata write failed (IntegrityError).\n')
        with sqlite3.connect(self.path) as db:
            self.assertIsNone(db.execute('SELECT response_metadata_json FROM interactions').fetchone()[0])


if __name__ == '__main__':
    unittest.main()
