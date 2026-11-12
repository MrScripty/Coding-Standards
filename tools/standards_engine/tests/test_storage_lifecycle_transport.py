"""Cold MCP reads coexist with a reserved writer only when no purge is due.

One server process audits its store once, on its first call; a newly started
process audits again and still rejects a corrupt store. Each test therefore
starts a new server process exactly where its claim is about a cold start.

The fixture owns its database, evidence and processes. Publication, authorization
and interpreter timing are not simulated; no production store is accessed.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import time
import unittest
from contextlib import closing
from pathlib import Path
from unittest import mock

from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.tests import test_agent_interaction_transport as transport
from tools.standards_engine.tests.stdio_server import StdioServer, StdioServers
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_engine.tests.test_route_content import known_assertions
from tools.standards_snapshots.standards_snapshots import (
    AggregateChild, AggregateRecord, AggregateRoot, ChildHandle,
    SnapshotError, SnapshotId, SnapshotModule,
)
from tools.standards_snapshots.standards_snapshots import store as snapshot_store

AUDIT_STATEMENTS = ('PRAGMA integrity_check', 'PRAGMA foreign_key_check')


class StorageLifecycleTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        transport.fixture.PurposeTransportTest.setUpClass()
        cls.root = transport.fixture.PurposeTransportTest.root
        cls.snapshot = transport.fixture.PurposeTransportTest.snapshot
        cls.path = cls.root / '.standards-engine/snapshots-v1.sqlite3'

    @classmethod
    def tearDownClass(cls):
        transport.fixture.PurposeTransportTest.tearDownClass()

    def setUp(self):
        self.servers = StdioServers(client='interaction-fixture')
        self.addCleanup(self.servers.close)

    def call(self, purpose, operation, arguments, *, rejected=False):
        return transport.AgentInteractionTransportTest.call(
            self, purpose, operation, arguments, rejected=rejected, delivery='on-demand',
        )

    def cold_open_failure(self):
        """Run one cold authoring read whose store open fails; return its private stderr."""
        # Open-time failure retains the existing MCP private-stderr
        # boundary (no structured result), not an invented tool outcome.
        server = StdioServer(self.root, purpose='authoring', options=('--output-schemas', 'on-demand'),
                             client='storage-open-fixture', silent=False)
        try:
            failed = server.call('read', {'snapshot': self.snapshot, 'target': 'core'})['result']
        finally:
            errors = server.close()
        self.assertTrue(failed['isError'])
        self.assertNotIn('structuredContent', failed)
        self.assertIn('Engine invocation failed', failed['content'][0]['text'])
        return errors

    def test_one_server_process_audits_its_store_once_across_calls(self):
        # The fixture built this store inside the test process. Discard that
        # record so the server below starts as a newly launched process does.
        with snapshot_store._AUDITED_FILES_LOCK:
            snapshot_store._AUDITED_FILES.clear()
        opens = []
        connect = sqlite3.connect

        def traced_connect(database, *arguments, **options):
            connection = connect(database, *arguments, **options)
            if Path(database).resolve() == self.path.resolve():
                opens.append([])
                connection.set_trace_callback(opens[-1].append)
            return connection

        server = MCPServer(self.root, purpose='application')
        self.addCleanup(server.close)
        initialize(server)
        arguments = {'snapshot': self.snapshot, 'target': 'core'}
        with mock.patch.object(snapshot_store.sqlite3, 'connect', traced_connect):
            results = [
                server.dispatch(request('tools/call', {'name': 'read', 'arguments': arguments},
                                        identifier))['result']
                for identifier in (2, 3, 4)
            ]
        for result in results:
            self.assertFalse(result['isError'], result)
            self.assertEqual(result['structuredContent']['content'],
                             transport.fixture.PurposeTransportTest.expected)
        # Every call still opens and closes its own store connection.
        self.assertEqual(len(opens), 3)
        self.assertEqual([[statement for statement in statements if statement in AUDIT_STATEMENTS]
                          for statements in opens], [list(AUDIT_STATEMENTS), [], []])
        for statements in opens:
            self.assertIn('PRAGMA application_id', statements)
            self.assertIn('PRAGMA user_version', statements)
            self.assertTrue(any('FROM sqlite_schema' in statement for statement in statements))

    def test_cold_server_process_rejects_a_corrupt_store_on_its_first_call(self):
        retained = self.path.with_name('retained-valid-store.sqlite3')
        shutil.copyfile(self.path, retained)
        try:
            with closing(sqlite3.connect(self.path, isolation_level=None)) as corruptor:
                corruptor.execute(
                    "INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")
            self.assertIn('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', self.cold_open_failure())
        finally:
            os.replace(retained, self.path)
        recovered = self.call('authoring', 'read', {'snapshot': self.snapshot, 'target': 'core'})
        self.assertEqual(recovered['content'], transport.fixture.PurposeTransportTest.expected)

    def test_cold_agent_observations_match_while_another_process_holds_writer(self):
        cases = [
            ('read', {'snapshot': self.snapshot, 'target': 'core'}),
            ('read_many', {'snapshot': self.snapshot, 'items': [
                {'target': 'core'}, {'target': 'router'}]}),
            ('route', {'snapshot': self.snapshot, 'facts': known_assertions(), 'content': {'limit': 1}}),
            ('relationship_groups', {'snapshot': self.snapshot, 'limit': 1}),
        ]
        expected = {(purpose, operation): self.call(purpose, operation, arguments)
                    for purpose in ('application', 'authoring')
                    for operation, arguments in cases}
        with closing(sqlite3.connect(self.path, isolation_level=None)) as writer:
            writer.execute('BEGIN IMMEDIATE')
            writer.execute('INSERT INTO purged_root_tombstones VALUES (?, ?)', ('uncommitted-test', 1))
            try:
                for purpose in ('application', 'authoring'):
                    # Cold: a process started under the held writer audits and opens the store.
                    self.servers.restart(self.root, purpose, '--output-schemas', 'on-demand')
                    for operation, arguments in cases:
                        with self.subTest(purpose=purpose, operation=operation):
                            self.assertEqual(self.call(purpose, operation, arguments),
                                             expected[purpose, operation])
            finally:
                writer.execute('ROLLBACK')
            self.assertIsNone(writer.execute(
                "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = 'uncommitted-test'"
            ).fetchone())

    def test_cold_due_maintenance_keeps_busy_then_expires_all_dependents_atomically(self):
        original = SnapshotId(self.snapshot['id'])
        with SnapshotModule.open(self.path) as source:
            capture = source.load_content(original)
        # Put only the additional fixture root past its deadline, without a sleep.
        with SnapshotModule.open(self.path, now=lambda: int(time.time()) - 10,
                                 quarantine_seconds=1) as source:
            expired = source.create_snapshot(capture).snapshot
            head = AggregateRecord('revision:expired-transport', 'revision', b'head', (expired,),
                                   (AggregateChild('requirement', 'one', b'child'),))
            root = AggregateRoot('proposal:expired-transport', 'proposal', head.aggregate_id,
                                 (expired,), 1)
            source.create_aggregate_root(root, head)
            source.delete_snapshot(expired)
        with closing(sqlite3.connect(self.path, isolation_level=None)) as writer:
            writer.execute('BEGIN IMMEDIATE')
            try:
                self.assertIn('SNAPSHOT_STORE.BUSY', self.cold_open_failure())
                self.assertIsNotNone(writer.execute(
                    'SELECT 1 FROM snapshot_roots WHERE snapshot_id = ?', (str(expired),)
                ).fetchone())
                self.assertIsNotNone(writer.execute(
                    'SELECT 1 FROM aggregate_records WHERE aggregate_id = ?', (head.aggregate_id,)
                ).fetchone())
            finally:
                writer.execute('ROLLBACK')
        recovered = self.call('authoring', 'read', {'snapshot': self.snapshot, 'target': 'core'})
        self.assertEqual(recovered['content'], transport.fixture.PurposeTransportTest.expected)
        with SnapshotModule.open(self.path) as source:
            for operation, code in (
                (lambda: source.snapshot(expired), 'SNAPSHOT.EXPIRED'),
                (lambda: source.load_aggregate(head.aggregate_id), 'AGGREGATE.UNAVAILABLE'),
                (lambda: source.load_aggregate_root(root.aggregate_id), 'AGGREGATE.ROOT_UNAVAILABLE'),
                (lambda: source.inspect_child(ChildHandle(head.aggregate_id, 'requirement', 'one')),
                 'AGGREGATE.UNAVAILABLE'),
            ):
                with self.subTest(code=code), self.assertRaises(SnapshotError) as error:
                    operation()
                self.assertEqual(error.exception.failure.code, code)
            self.assertEqual(source.load_content(original), capture)
            self.assertEqual(source._store.counts()['purged_root_tombstones'], 1)
            self.assertEqual(source._store.counts()['content_sets'], 1)


if __name__ == '__main__':
    unittest.main()
