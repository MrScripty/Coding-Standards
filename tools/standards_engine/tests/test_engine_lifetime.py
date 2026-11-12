"""One Engine for the life of a server process, one store connection for each call.

A server opens its facade and Engine with its first store-backed tool call,
serves every later call with them and closes them when it closes. The store
connection is opened for each call, with the admission a new open runs, and
closed when the call ends: between calls the process holds no connection, lock
or open store file, and what another process did to the store is met by the
next call. An Engine is never used again after a failure nobody classified.

Tests that claim something about another process start one. The fixture owns
its repository root, database and processes; no production store is accessed.
"""
from __future__ import annotations

from contextlib import closing, redirect_stderr
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import engine as engine_module
from tools.standards_engine.standards_engine.compiled_cache import CompiledSnapshotCache
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_engine.tests import test_purpose_transport as fixture
from tools.standards_engine.tests.stdio_server import StdioServer
from tools.standards_engine.tests.test_mcp import initialize, request
from tools.standards_engine.tests.test_route_content import known_assertions
from tools.standards_snapshots.standards_snapshots import SnapshotId, SnapshotModule
from tools.standards_snapshots.standards_snapshots import store as snapshot_store

ROOT = Path(__file__).resolve().parents[3]
AUDIT_STATEMENTS = ['PRAGMA integrity_check', 'PRAGMA foreign_key_check']

# A separate interpreter, as another server or a CLI call is: it opens the
# store through the ordinary module path, commits one change and exits.
_OTHER_PROCESS = """
import sys
from pathlib import Path
from tools.standards_snapshots.standards_snapshots import SnapshotId, SnapshotModule
action, path, identifier = sys.argv[1:4]
with SnapshotModule.open(Path(path)) as store:
    snapshot = SnapshotId(identifier)
    if action == 'quarantine':
        store.delete_snapshot(snapshot)
    elif action == 'restore':
        store.undelete_snapshot(snapshot)
    else:
        print(store.create_snapshot(store.load_content(snapshot)).snapshot.value)
"""


class EngineLifetimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeTransportTest.setUpClass()
        cls.root = fixture.PurposeTransportTest.root
        cls.snapshot = fixture.PurposeTransportTest.snapshot
        cls.expected = fixture.PurposeTransportTest.expected
        cls.path = cls.root / '.standards-engine/snapshots-v1.sqlite3'

    @classmethod
    def tearDownClass(cls):
        fixture.PurposeTransportTest.tearDownClass()

    def setUp(self):
        self.opens, self.connections = [], []
        connect = self.untraced_connect = sqlite3.connect

        def traced_connect(database, *arguments, **options):
            # Observe each store connection from before its first statement.
            connection = connect(database, *arguments, **options)
            if Path(database).resolve() == self.path.resolve():
                self.opens.append([])
                self.connections.append(connection)
                connection.set_trace_callback(self.opens[-1].append)
            return connection

        patcher = mock.patch.object(snapshot_store.sqlite3, 'connect', traced_connect)
        patcher.start()
        self.addCleanup(patcher.stop)

    def server(self, purpose='application'):
        server = MCPServer(self.root, purpose=purpose)
        self.addCleanup(server.close)
        initialize(server)
        return server

    def call(self, server, operation, arguments):
        return server.dispatch(request('tools/call', {'name': operation, 'arguments': arguments}))['result']

    def read(self, server, **arguments):
        return self.call(server, 'read', {'snapshot': self.snapshot, 'target': 'core', **arguments})

    def failed_call(self, server):
        """One call that fails outside any typed outcome; return the private stderr."""
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            failed = self.read(server)
        self.assertTrue(failed['isError'])
        self.assertNotIn('structuredContent', failed)
        self.assertIn('Engine invocation failed', failed['content'][0]['text'])
        return stderr.getvalue()

    def other_process(self, action, snapshot=None):
        completed = subprocess.run(
            [sys.executable, '-P', '-c', _OTHER_PROCESS, action, str(self.path),
             (snapshot or self.snapshot)['id']],
            env={**os.environ, 'PYTHONPATH': str(ROOT)}, text=True, capture_output=True, timeout=60)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed.stdout.strip()

    def assert_no_connection(self):
        """Every store connection this process opened is closed and holds no lock."""
        for connection in self.connections:
            with self.assertRaises(sqlite3.ProgrammingError):
                connection.execute('SELECT 1')
        # An exclusive transaction is granted only when no connection holds a lock.
        with closing(self.untraced_connect(self.path, isolation_level=None, timeout=0)) as other:
            other.execute('BEGIN EXCLUSIVE')
            other.execute('ROLLBACK')

    def assert_closed(self, facade):
        with self.assertRaises(sqlite3.ProgrammingError):
            facade._engine._snapshots._store._connection.execute('SELECT 1')
        with self.assertRaisesRegex(ValueError, 'closed'):
            facade._engine._compiled_cache.require_scope(self.root, facade._engine.purpose)

    def test_several_calls_use_one_facade_and_engine_and_a_store_connection_each(self):
        server = self.server()
        self.assertIsNone(server._facade)
        # Catalog and runtime observations need no Engine and open none.
        for name in ('runtime_info', 'describe_input'):
            self.call(server, name, {} if name == 'runtime_info' else {'operation': 'read'})
        self.assertIsNone(server._facade)
        self.assertEqual(self.opens, [])
        opened = AgentToolFacade.open_repository
        with mock.patch.object(AgentToolFacade, 'open_repository', wraps=opened) as calls:
            first = self.read(server)
            facade, engine = server._facade, server._facade._engine
            self.assertEqual(len(self.opens), 1)
            self.assert_no_connection()
            for count, (operation, arguments) in enumerate((
                ('read', {'snapshot': self.snapshot, 'target': 'core'}),
                ('read_many', {'snapshot': self.snapshot, 'items': [{'target': 'core'}, {'target': 'router'}]}),
                ('route', {'snapshot': self.snapshot, 'facts': known_assertions(), 'content': {'limit': 1}}),
                ('relationship_groups', {'snapshot': self.snapshot, 'limit': 1}),
                # Typed rejections are ordinary outcomes: the Engine stays.
                ('read', {'snapshot': self.snapshot, 'target': 'not-registered'}),
                ('read', {'extra': True}),
            ), start=2):
                self.call(server, operation, arguments)
                self.assertIs(server._facade, facade)
                self.assertIs(server._facade._engine, engine)
                # Each call opened one store connection and closed it when it ended.
                self.assertEqual(len(self.opens), count)
                self.assert_no_connection()
        self.assertEqual(first['structuredContent']['content'], self.expected)
        self.assertEqual(calls.call_count, 1)
        self.assertIs(calls.call_args.kwargs['interface'], server._interface)
        # The server lends no cache: the Engine's own lives exactly as long as it does.
        self.assertNotIn('compiled_cache', calls.call_args.kwargs)
        self.assertTrue(engine._owns_compiled_cache)
        self.assertEqual(engine._compiled_cache.statistics['entries'], 1)

    def test_every_call_answers_as_a_facade_opened_for_that_call_does(self):
        cases = [
            ('read', {'snapshot': self.snapshot, 'target': 'core'}),
            ('read', {'snapshot': self.snapshot, 'target': 'core', 'detail': 'full'}),
            ('read_many', {'snapshot': self.snapshot, 'items': [{'target': 'core'}, {'target': 'router'}]}),
            ('route', {'snapshot': self.snapshot, 'facts': known_assertions(), 'content': {'limit': 1}}),
            ('relationship_groups', {'snapshot': self.snapshot, 'limit': 1}),
            ('related', {'snapshot': self.snapshot, 'target': 'core', 'groups': ['standards-requires'],
                         'direction': 'outgoing', 'transitive': False}),
            ('related', {'snapshot': self.snapshot, 'target': 'core', 'groups': ['not-a-group'],
                         'direction': 'outgoing', 'transitive': False}),
            ('read', {'snapshot': self.snapshot, 'target': 'not-registered'}),
            ('read', {'snapshot': {**self.snapshot, 'id': 'snapshot:v1:' + '0' * 8 + '-0000-4000-8000-' + '0' * 12},
                      'target': 'core'}),
            ('read', {'extra': True}),
            ('read', {'snapshot': self.snapshot, 'target': 'core'}),
        ]

        for purpose in ('application', 'authoring'):
            with self.subTest(purpose=purpose):
                kept = self.server(purpose)
                lent = CompiledSnapshotCache(self.root, purpose)
                self.addCleanup(lent.close)
                for operation, arguments in cases:
                    # What the transport did for every call before it kept its
                    # Engine: open a facade and store, lending the process's
                    # interface and cache, run the operation, and close.
                    with AgentToolFacade.open_repository(
                            self.root, purpose=purpose, interface=kept._interface,
                            compiled_cache=lent) as opened:
                        expected = getattr(opened, operation)(deepcopy(arguments))
                    answer = self.call(kept, operation, arguments)
                    self.assertEqual(answer, kept._tool_result(deepcopy(expected)), (operation, arguments))
                    self.assertEqual(json.loads(answer['content'][0]['text']), expected)
                    # A caller that alters its answer changes nothing a later call returns.
                    answer['structuredContent'].clear()
                    answer['content'].clear()
                self.assertEqual(kept._facade._engine._compiled_cache.statistics['entries'], 1)

    def test_unexpected_exception_closes_the_engine_and_the_next_call_opens_another(self):
        for purpose in ('application', 'authoring'):
            with self.subTest(purpose=purpose):
                del self.opens[:]
                server = self.server(purpose)
                first = self.read(server)
                self.assertFalse(first['isError'], first)
                failed_facade = server._facade
                with (mock.patch.object(AgentToolFacade, 'read', side_effect=RuntimeError('private diagnostic')),
                      redirect_stderr(io.StringIO()) as stderr):
                    failed = self.read(server)
                self.assertTrue(failed['isError'])
                self.assertNotIn('structuredContent', failed)
                self.assertNotIn('private diagnostic', json.dumps(failed))
                self.assertIn('RuntimeError', stderr.getvalue())
                self.assertIsNone(server._facade)
                self.assert_closed(failed_facade)
                again = self.read(server)
                self.assertEqual(again['structuredContent'], first['structuredContent'])
                self.assertIsNot(server._facade, failed_facade)
                self.assertIsNot(server._facade._engine, failed_facade._engine)
                # One connection for each of the three calls, none left open.
                self.assertEqual(len(self.opens), 3)
                self.assert_no_connection()

    def test_interruption_closes_the_engine_before_it_propagates(self):
        server = self.server()
        self.read(server)
        interrupted = server._facade
        with mock.patch.object(AgentToolFacade, 'read', side_effect=KeyboardInterrupt()):
            with self.assertRaises(KeyboardInterrupt):
                self.read(server)
        self.assertIsNone(server._facade)
        self.assert_closed(interrupted)
        self.assertFalse(self.read(server)['isError'])

    def test_unclassified_failure_behind_an_application_rejection_also_closes_the_engine(self):
        server = self.server()
        first = self.read(server)
        kept = server._facade
        # A typed failure is an ordinary outcome with the same public code.
        missing = {**self.snapshot, 'id': 'snapshot:v1:' + '0' * 8 + '-0000-4000-8000-' + '0' * 12}
        typed = self.call(server, 'read', {'snapshot': missing, 'target': 'core'})
        self.assertEqual(typed['structuredContent']['code'], 'APPLICATION.INTERNAL_UNAVAILABLE')
        self.assertIs(server._facade, kept)
        self.assertTrue(kept.reusable)
        with (mock.patch.object(StandardsEngine, '_compiled_snapshot', side_effect=RuntimeError('private diagnostic')),
              self.assertLogs('tools.standards_engine.standards_engine.context_projection', 'ERROR') as logged):
            swallowed = self.read(server)
        # The application caller sees exactly the bounded rejection it always saw.
        self.assertEqual(swallowed, {**typed, '_meta': swallowed['_meta']})
        self.assertNotIn('private diagnostic', json.dumps(swallowed) + ''.join(logged.output))
        self.assertFalse(kept.reusable)
        self.assertIsNone(server._facade)
        self.assert_closed(kept)
        self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])
        self.assertIsNot(server._facade, kept)
        self.assert_no_connection()

    def test_transaction_an_operation_left_open_is_rolled_back_not_committed(self):
        server = self.server()
        first = self.read(server)
        kept = server._facade
        read = AgentToolFacade.read

        def read_and_leave_a_transaction(facade, arguments):
            value = read(facade, arguments)
            connection = facade._engine._snapshots._store._connection
            connection.execute('BEGIN IMMEDIATE')
            connection.execute('INSERT INTO purged_root_tombstones VALUES (?, ?)', ('left-open', 1))
            return value

        with mock.patch.object(AgentToolFacade, 'read', read_and_leave_a_transaction):
            answered = self.read(server)
        self.assertEqual(answered['structuredContent'], first['structuredContent'])
        # Closing the call's connection ended the transaction without its
        # write, as closing a store opened for one call always did.
        self.assert_no_connection()
        with closing(sqlite3.connect(self.path)) as observed:
            self.assertIsNone(observed.execute(
                "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = 'left-open'").fetchone())
        self.assertFalse(self.path.with_name(self.path.name + '-journal').exists())
        self.assertIs(server._facade, kept)
        self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])

    def test_replaced_store_file_is_reopened_and_audited(self):
        with snapshot_store._AUDITED_FILES_LOCK:
            snapshot_store._AUDITED_FILES.clear()
        server = self.server('authoring')
        first = self.read(server)
        self.assertFalse(first['isError'], first)
        self.assertEqual(self.read(server), {**first, '_meta': first['_meta']})
        self.assertEqual(len(self.opens), 2)
        self.assertNotIn('PRAGMA integrity_check', self.opens[1])
        original = server._facade
        audited = (self.path.lstat().st_dev, self.path.lstat().st_ino)
        self.assertTrue(snapshot_store._audit_recorded(audited))
        retained = self.path.with_name('retained-valid-store.sqlite3')
        shutil.copyfile(self.path, retained)
        try:
            # A complete file moved into place has another inode: the Engine
            # is opened anew, and that open audits the file.
            replacement = self.path.with_name('replacement.sqlite3')
            shutil.copyfile(self.path, replacement)
            os.replace(replacement, self.path)
            self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])
            self.assertIsNot(server._facade, original)
            self.assert_closed(original)
            self.assertEqual(len(self.opens), 3)
            self.assertEqual([statement for statement in self.opens[2] if statement in AUDIT_STATEMENTS],
                             AUDIT_STATEMENTS)
            # The replaced file's inode number can go to a later replacement;
            # the audit of the file that had it is no longer on record.
            self.assertFalse(snapshot_store._audit_recorded(audited))
            # A damaged replacement is refused by that audit, at the open boundary.
            shutil.copyfile(self.path, replacement)
            with closing(sqlite3.connect(replacement, isolation_level=None)) as corruptor:
                corruptor.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")
            os.replace(replacement, self.path)
            self.assertIn('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', self.failed_call(server))
            self.assertIsNone(server._facade)
            self.assertIn('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', self.failed_call(server))
            # A removed store is created again, empty, as an open of a missing path does.
            self.path.unlink()
            missing = self.read(server)
            self.assertEqual(missing['structuredContent']['code'], 'SNAPSHOT.UNAVAILABLE', missing)
            self.assertTrue(self.path.is_file())
            with closing(sqlite3.connect(self.path)) as created:
                self.assertEqual(created.execute('SELECT count(*) FROM snapshot_roots').fetchone(), (0,))
        finally:
            os.replace(retained, self.path)
        self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])

    def test_another_process_committed_writes_are_visible_to_the_next_call(self):
        server = self.server('authoring')
        first = self.read(server)
        self.assertFalse(first['isError'], first)
        kept = server._facade
        self.other_process('quarantine')
        try:
            quarantined = self.read(server)
            self.assertEqual(quarantined['structuredContent']['code'], 'SNAPSHOT.QUARANTINED', quarantined)
        finally:
            self.other_process('restore')
        self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])
        added = {**self.snapshot, 'id': self.other_process('copy')}
        self.assertNotEqual(added, self.snapshot)
        other = self.call(server, 'read', {'snapshot': added, 'target': 'core'})
        self.assertFalse(other['isError'], other)
        self.assertEqual(other['structuredContent']['snapshot'], added)
        self.assertEqual(other['structuredContent']['content'], first['structuredContent']['content'])
        # Every observation was made by the one Engine this server opened.
        self.assertIs(server._facade, kept)

    def test_another_process_schema_or_version_change_is_met_by_the_next_call(self):
        server = self.server('authoring')
        first = self.read(server)
        for change, restore, code in (
            # A later Engine migrated the store in place; this one must stop using it.
            ('PRAGMA user_version=3', 'PRAGMA user_version=2', 'SNAPSHOT_STORE.UNSUPPORTED_VERSION'),
            ('CREATE TABLE unexpected (value TEXT)', 'DROP TABLE unexpected', 'SNAPSHOT_STORE.INVALID_SCHEMA'),
        ):
            with self.subTest(change=change):
                self.assertIsNotNone(server._facade)
                with closing(sqlite3.connect(self.path, isolation_level=None)) as other:
                    other.execute(change)
                try:
                    self.assertIn(code, self.failed_call(server))
                    self.assertIsNone(server._facade)
                    self.assertIn(code, self.failed_call(server))
                finally:
                    with closing(sqlite3.connect(self.path, isolation_level=None)) as other:
                        other.execute(restore)
                self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])

    def test_due_maintenance_under_another_writer_fails_before_the_operation_as_at_open(self):
        original = SnapshotId(self.snapshot['id'])
        # A short busy budget for this server's connection; the outcome is the same.
        with mock.patch.object(snapshot_store, 'BUSY_TIMEOUT_MS', 50):
            server = self.server('authoring')
            first = self.read(server)
            kept = server._facade
            with SnapshotModule.open(self.path) as source:
                capture = source.load_content(original)
            # Put only an additional root past its deadline, without a sleep.
            with SnapshotModule.open(self.path, now=lambda: int(time.time()) - 10,
                                     quarantine_seconds=1) as source:
                expired = source.create_snapshot(capture).snapshot
                source.delete_snapshot(expired)
            with closing(sqlite3.connect(self.path, isolation_level=None)) as writer:
                writer.execute('BEGIN IMMEDIATE')
                try:
                    # Not a typed result of the operation: the same private
                    # boundary as a store open that meets the busy writer.
                    self.assertIn('SNAPSHOT_STORE.BUSY', self.failed_call(server))
                    self.assertIsNone(server._facade)
                    self.assert_closed(kept)
                    self.assertIsNotNone(writer.execute(
                        'SELECT 1 FROM snapshot_roots WHERE snapshot_id = ?', (str(expired),)).fetchone())
                finally:
                    writer.execute('ROLLBACK')
            self.assertEqual(self.read(server)['structuredContent'], first['structuredContent'])
            with closing(sqlite3.connect(self.path)) as observed:
                self.assertIsNone(observed.execute(
                    'SELECT 1 FROM snapshot_roots WHERE snapshot_id = ?', (str(expired),)).fetchone())
                self.assertIsNotNone(observed.execute(
                    'SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = ?', (str(expired),)).fetchone())

    def test_closing_the_server_closes_the_engine_and_its_cache(self):
        server = self.server()
        self.read(server)
        facade = server._facade
        # The call's store connection is already closed; the Engine and cache are kept.
        self.assert_no_connection()
        self.assertEqual(facade._engine._compiled_cache.statistics['entries'], 1)
        server.close()
        self.assertIsNone(server._facade)
        self.assert_closed(facade)
        self.assertEqual(facade._engine._compiled_cache.statistics['entries'], 0)
        self.assertEqual(server.dispatch(request('ping'))['error']['code'], -32000)
        self.assertEqual(len(self.opens), 1)
        # End of input closes it the same way.
        served = MCPServer(self.root, purpose='application')
        initialize(served)
        self.read(served)
        facade = served._facade
        serve(served, io.StringIO(''), io.StringIO())
        self.assertIsNone(served._facade)
        self.assert_closed(facade)

    @unittest.skipUnless(os.path.isdir('/proc/self/fd'), 'needs /proc to list another process\'s descriptors')
    def test_idle_server_process_holds_no_descriptor_or_lock_on_the_store(self):
        server = StdioServer(self.root, purpose='authoring', client='lifetime-fixture')
        self.addCleanup(server.close)
        store = str(self.path.resolve())
        descriptors = Path('/proc') / str(server._process.pid) / 'fd'
        for arguments, rejected in (
            ({'snapshot': self.snapshot, 'target': 'core'}, False),
            ({'snapshot': self.snapshot, 'target': 'not-registered'}, True),
            ({'snapshot': self.snapshot, 'target': 'core'}, False),
        ):
            result = server.call('read', arguments)['result']
            self.assertEqual(result['isError'], rejected, result)
            # The server process is alive and has answered. Nothing it has open
            # is the store file, its rollback journal or a write-ahead log.
            targets = [os.readlink(entry) for entry in descriptors.iterdir()]
            self.assertTrue(targets)
            self.assertEqual([target for target in targets if target.startswith(store)], [])
            # An exclusive transaction is granted only when no other connection holds a lock.
            with closing(sqlite3.connect(self.path, isolation_level=None, timeout=0)) as other:
                other.execute('BEGIN EXCLUSIVE')
                other.execute('INSERT INTO purged_root_tombstones VALUES (?, ?)', ('idle-lock-probe', 1))
                other.execute('ROLLBACK')
        for suffix in ('-journal', '-wal', '-shm'):
            self.assertFalse(self.path.with_name(self.path.name + suffix).exists())

    def test_dispatch_from_another_thread_than_the_previous_call_works(self):
        server = self.server('authoring')
        first = self.read(server)
        self.assertFalse(first['isError'], first)
        kept = server._facade
        answers, failures = [], []

        def call():
            try:
                answers.append(self.read(server))
            except BaseException as error:
                failures.append(error)

        for _ in range(2):
            worker = threading.Thread(target=call)
            worker.start()
            worker.join()
            call()
        self.assertEqual(failures, [])
        self.assertEqual([answer['structuredContent'] for answer in answers], [first['structuredContent']] * 4)
        self.assertIs(server._facade, kept)
        self.assert_no_connection()
        # A thread that made none of the calls can close the server.
        closer = threading.Thread(target=server.close)
        closer.start()
        closer.join()
        self.assertIsNone(server._facade)
        self.assert_closed(kept)

    def test_engine_without_a_lent_cache_reuses_a_compiled_snapshot(self):
        arguments = {'snapshot': self.snapshot, 'target': 'core'}
        with AgentToolFacade.open_repository(self.root, purpose='authoring') as facade:
            engine = facade._engine
            cache = engine._compiled_cache
            self.assertTrue(engine._owns_compiled_cache)
            with (
                mock.patch.object(engine._snapshots, 'load_content', wraps=engine._snapshots.load_content) as load,
                mock.patch.object(engine_module, 'compile_policy_impact',
                                  wraps=engine_module.compile_policy_impact) as compile,
            ):
                first = facade.read(arguments)
                second = facade.read(arguments)
            self.assertEqual(first['kind'], 'compact-read-result', first)
            self.assertEqual(first, second)
            # Stored content is loaded and verified by each read; compilation runs once.
            self.assertEqual(load.call_count, 2)
            self.assertEqual(compile.call_count, 1)
            self.assertEqual((cache.statistics['misses'], cache.statistics['hits']), (1, 1))
            self.assertEqual(cache.statistics['entries'], 1)
        # The Engine closes the cache it owns.
        self.assertEqual(cache.statistics['entries'], 0)
        with self.assertRaisesRegex(ValueError, 'closed'):
            cache.require_scope(self.root, 'authoring')

    def test_store_directory_link_pointed_elsewhere_selects_a_new_open(self):
        with tempfile.TemporaryDirectory(prefix='engine-lifetime-link-') as temporary:
            root = Path(temporary) / 'repository'
            first, second = Path(temporary) / 'first', Path(temporary) / 'second'
            for directory in (root, first, second):
                directory.mkdir()
            link = root / '.standards-engine'
            link.symlink_to(first)
            with StandardsEngine.open_repository(root, purpose='authoring') as engine:
                self.assertTrue((first / 'snapshots-v1.sqlite3').is_file())
                self.assertTrue(engine.readmit())
                link.unlink()
                link.symlink_to(second)
                self.assertFalse(engine.readmit())
                self.assertFalse((second / 'snapshots-v1.sqlite3').exists())
            with StandardsEngine.open_repository(root, purpose='authoring'):
                self.assertTrue((second / 'snapshots-v1.sqlite3').is_file())

    def test_repository_root_moved_behind_a_link_selects_a_new_open(self):
        with tempfile.TemporaryDirectory(prefix='engine-lifetime-root-') as temporary:
            root, moved = Path(temporary) / 'repository', Path(temporary) / 'moved'
            stores = Path(temporary) / 'stores'
            root.mkdir()
            stores.mkdir()
            # The store directory is elsewhere, so only the root's own location changes.
            (root / '.standards-engine').symlink_to(stores)
            with StandardsEngine.open_repository(root, purpose='authoring') as engine:
                self.assertEqual(engine._repository.root, root.resolve())
                self.assertTrue(engine.readmit())
                root.rename(moved)
                root.symlink_to(moved)
                self.assertFalse(engine.readmit())
            with StandardsEngine.open_repository(root, purpose='authoring') as engine:
                self.assertEqual(engine._repository.root, moved.resolve())
                self.assertTrue(engine.readmit())


if __name__ == '__main__':
    unittest.main()
