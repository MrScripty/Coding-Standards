"""Cold MCP reads coexist with a reserved writer only when no purge is due.

The fixture owns its database, evidence and processes. Publication, authorization
and interpreter timing are not simulated; no production store is accessed.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time
import unittest
from contextlib import closing

from tools.standards_engine.tests import test_agent_interaction_transport as transport
from tools.standards_engine.tests.test_route_content import known_facts
from tools.standards_snapshots.standards_snapshots import (
    AggregateChild, AggregateRecord, AggregateRoot, ChildHandle,
    SnapshotError, SnapshotId, SnapshotModule,
)


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

    def call(self, purpose, operation, arguments, *, rejected=False):
        return transport.AgentInteractionTransportTest.call(
            self, purpose, operation, arguments, rejected=rejected, delivery='on-demand',
        )

    def test_cold_agent_observations_match_while_another_process_holds_writer(self):
        cases = [
            ('read', {'snapshot': self.snapshot, 'target': 'core'}),
            ('read_many', {'snapshot': self.snapshot, 'items': [
                {'target': 'core'}, {'target': 'router'}]}),
            ('route', {'snapshot': self.snapshot, 'facts': known_facts(), 'content': {'limit': 1}}),
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
                # Open-time failure retains the existing MCP private-stderr
                # boundary (no structured result), not an invented tool outcome.
                messages = [
                    {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                        'protocolVersion': '2025-11-25', 'capabilities': {},
                        'clientInfo': {'name': 'storage-busy-fixture', 'version': '1'}}},
                    {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {
                        'name': 'read', 'arguments': {'snapshot': self.snapshot, 'target': 'core'}}},
                ]
                process = subprocess.run(
                    [sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp',
                     '--repo-root', str(self.root), '--purpose', 'authoring',
                     '--output-schemas', 'on-demand'],
                    env={**os.environ, 'PYTHONPATH': str(transport.fixture.ROOT)},
                    input=''.join(json.dumps(message) + '\n' for message in messages),
                    text=True, capture_output=True, timeout=90,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertIn('SNAPSHOT_STORE.BUSY', process.stderr)
                failed = next(json.loads(line)['result'] for line in process.stdout.splitlines()
                              if json.loads(line).get('id') == 2)
                self.assertTrue(failed['isError'])
                self.assertNotIn('structuredContent', failed)
                self.assertIn('Engine invocation failed', failed['content'][0]['text'])
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
