"""Storage admission and synchronous maintenance against real SQLite connections.

No-work observations must not request a writer. A positive probe is only a hint:
transactions still select the current due set and own all deletion effects.

One process runs the complete integrity/foreign-key audit of a store file once.
Later opens of that file keep the application, version and exact schema checks.

An owner that keeps a store between uses releases it after each use and
readmits it before the next. A released store holds no connection. Readmission
opens a new one, runs the statements of a later open, and reports a path that
no longer names the opened file so that the owner opens it again.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from typing import Callable
from unittest import mock

from tools.standards_snapshots.standards_snapshots import (
    AggregateChild, AggregateRecord, AggregateRoot, ChildHandle,
    FindAggregateRootsRequest, FindSnapshotsRequest, SnapshotError, SnapshotModule,
)
from tools.standards_snapshots.standards_snapshots import store as store_module
from tools.standards_snapshots.standards_snapshots.store import SQLiteSnapshotStore
from tools.standards_snapshots.tests.test_module import capture
from tools.standards_snapshots.tests.test_store import (
    _downgrade_to_version_one, _populated_version_one_store, _version_one_rows,
)

ROOT = Path(__file__).resolve().parents[3]

# A separate interpreter has no audit record. It reports the admission outcome
# of the ordinary module open path for one existing store file.
_COLD_OPEN = """
import sys
from pathlib import Path
from tools.standards_snapshots.standards_snapshots import SnapshotError, SnapshotModule
try:
    SnapshotModule.open(Path(sys.argv[1])).close()
except SnapshotError as error:
    print(error.failure.code)
else:
    print('admitted')
"""


def _begin_as_new_process() -> None:
    """Discard this process's audit record, as a newly started process has none."""
    with store_module._AUDITED_FILES_LOCK:
        store_module._AUDITED_FILES.clear()


def _file_identity(path: Path) -> tuple[int, int]:
    observed = path.lstat()
    return observed.st_dev, observed.st_ino


def _violate_foreign_key(path: Path) -> None:
    with closing(sqlite3.connect(path, isolation_level=None)) as corruptor:
        corruptor.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")


class _ObservedAdmissionStore(SQLiteSnapshotStore):
    """Record proof phases while running the unchanged real proof implementations."""

    def __init__(self, path: Path) -> None:
        self.admission_events: list[tuple[str, int, bool]] = []
        super().__init__(path)

    def _observe(self, event: str) -> None:
        self.admission_events.append((
            event,
            self._connection.execute('PRAGMA user_version').fetchone()[0],
            self._connection.in_transaction,
        ))

    def _configure(self) -> None:
        self._observe('configure')
        super()._configure()

    def _verify_integrity(self) -> None:
        self._observe('integrity')
        super()._verify_integrity()


class _BeforeWriterConnection:
    """Deterministically interleave a real competing operation, outside all locks.

    This test-only proxy is installed after store admission. The actual SQLite
    cursor, transactions, errors, triggers and data are never replaced.
    """

    def __init__(self, connection: sqlite3.Connection, action: Callable[[], None]):
        self.connection = connection
        self.action = action
        self.calls = 0

    def execute(self, statement, *args):
        if statement == 'BEGIN IMMEDIATE' and self.calls == 0:
            self.calls += 1
            self.action()
        return self.connection.execute(statement, *args)

    def __getattr__(self, name):
        return getattr(self.connection, name)


class StorageLifecycleTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / 'snapshots.sqlite3'
        self.now = 2_000_000_000
        # Audit expectations must not depend on stores opened by earlier tests,
        # whose removed files can lend their inode numbers to these fixtures.
        _begin_as_new_process()

    def events(self, path=None):
        opened = _ObservedAdmissionStore(path or self.path)
        try:
            return opened.admission_events
        finally:
            opened.close()

    def cold_open(self, path=None):
        completed = subprocess.run(
            [sys.executable, '-P', '-c', _COLD_OPEN, str(path or self.path)],
            env={**os.environ, 'PYTHONPATH': str(ROOT)},
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed.stdout.strip()

    def module(self):
        module = SnapshotModule.open(self.path, now=lambda: self.now, quarantine_seconds=10)
        self.addCleanup(module.close)
        return module

    def connection(self):
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=0.1)
        self.addCleanup(connection.close)
        return connection

    def assert_code(self, expected, call):
        with self.assertRaises(SnapshotError) as error:
            call()
        self.assertEqual(error.exception.failure.code, expected)

    def seed(self, module):
        snapshot = module.create_snapshot(capture()).snapshot
        head = AggregateRecord(
            'revision:one', 'revision', b'one', (snapshot,),
            (AggregateChild('requirement', 'one', b'child'),),
        )
        root = AggregateRoot('proposal:one', 'proposal', head.aggregate_id, (snapshot,), 1)
        module.create_aggregate_root(root, head)
        return snapshot, head, root

    def test_observations_do_not_require_writer_when_no_expiry_is_due(self):
        module = self.module()
        snapshot, head, root = self.seed(module)
        # Shorten only this test connection's timeout; the oracle is successful
        # reads/no write admission, not an elapsed-time threshold.
        module._store._connection.execute('PRAGMA busy_timeout=1')
        statements = []
        module._store._connection.set_trace_callback(statements.append)
        writer = self.connection()
        writer.execute('BEGIN IMMEDIATE')
        writer.execute('INSERT INTO purged_root_tombstones VALUES (?, ?)', ('pending', self.now))
        try:
            self.assertEqual(module.snapshot(snapshot).snapshot, snapshot)
            self.assertEqual(module.load_content(snapshot), capture())
            self.assertEqual(module.find_snapshots(FindSnapshotsRequest()).snapshots[0].snapshot, snapshot)
            self.assertEqual(module.load_aggregate(head.aggregate_id), head)
            self.assertEqual(module.load_aggregate_root(root.aggregate_id), root)
            self.assertEqual(module.find_aggregate_roots(FindAggregateRootsRequest('proposal')).roots, (root,))
            self.assertEqual(module.inspect_child(ChildHandle(head.aggregate_id, 'requirement', 'one')), b'child')
            module.maintain()
        finally:
            writer.execute('ROLLBACK')
            module._store._connection.set_trace_callback(None)
        self.assertNotIn('BEGIN IMMEDIATE', statements)
        self.assertEqual(module._store.counts()['purged_root_tombstones'], 0)

    def test_exclusive_writer_blocks_probe_with_busy_and_no_maintenance_effects(self):
        module = self.module()
        snapshot, head, root = self.seed(module)
        connection = module._store._connection
        self.assertEqual(connection.execute('PRAGMA journal_mode').fetchone(), ('delete',))
        before = module._store.counts()
        timeout = connection.execute('PRAGMA busy_timeout').fetchone()[0]
        # Shorten only the owned fixture connection; no wall-clock oracle or sleep.
        connection.execute('PRAGMA busy_timeout=1')
        statements = []
        connection.set_trace_callback(statements.append)
        writer = self.connection()
        try:
            writer.execute('BEGIN EXCLUSIVE')
            self.assertTrue(writer.in_transaction)
            with self.assertRaises(SnapshotError) as caught:
                module.maintain()
            self.assertEqual(caught.exception.failure.code, 'SNAPSHOT_STORE.BUSY')
            self.assertEqual(caught.exception.failure.kind, 'unavailable')
            self.assertIsInstance(caught.exception.__cause__, sqlite3.OperationalError)
            self.assertEqual(caught.exception.__cause__.sqlite_errorcode, sqlite3.SQLITE_BUSY)
            # The real read was attempted. No writer admission or rollback was
            # attempted by the maintenance connection after its failed probe.
            self.assertEqual(len(statements), 1, statements)
            self.assertTrue(statements[0].startswith('SELECT 1 FROM snapshot_roots '), statements)
            self.assertFalse(connection.in_transaction)
            self.assertTrue(writer.in_transaction)
        finally:
            if writer.in_transaction:
                writer.execute('ROLLBACK')
            connection.set_trace_callback(None)
            connection.execute(f'PRAGMA busy_timeout={timeout}')
        self.assertEqual(module._store.counts(), before)
        module.maintain()
        self.assertEqual(module._store.counts(), before)
        self.assertEqual(module.load_content(snapshot), capture())
        self.assertEqual(module.load_aggregate(head.aggregate_id), head)
        self.assertEqual(module.load_aggregate_root(root.aggregate_id), root)

    def test_reopening_current_store_can_read_alongside_reserved_writer(self):
        with SnapshotModule.open(self.path, now=lambda: self.now) as initial:
            snapshot = initial.create_snapshot(capture()).snapshot
        writer = self.connection()
        writer.execute('BEGIN IMMEDIATE')
        try:
            with SnapshotModule.open(self.path, now=lambda: self.now) as reopened:
                self.assertEqual(reopened.load_content(snapshot), capture())
        finally:
            writer.execute('ROLLBACK')

    def test_future_quarantine_avoids_writer_but_exact_deadline_purges(self):
        module = self.module()
        snapshot = module.create_snapshot(capture()).snapshot
        deadline = module.delete_snapshot(snapshot).purge_deadline
        statements = []
        module._store._connection.set_trace_callback(statements.append)
        self.now = deadline - 1
        self.assertEqual(module.snapshot(snapshot, include_quarantined=True).lifecycle, 'quarantined')
        self.assert_code('SNAPSHOT.QUARANTINED', lambda: module.load_content(snapshot))
        self.assertNotIn('BEGIN IMMEDIATE', statements)
        self.now = deadline
        self.assert_code('SNAPSHOT.EXPIRED', lambda: module.snapshot(snapshot, include_quarantined=True))
        self.assertEqual(statements.count('BEGIN IMMEDIATE'), 1)
        statements.clear()
        module.maintain()
        self.assertNotIn('BEGIN IMMEDIATE', statements)

    def test_negative_probe_does_not_hide_later_due_work(self):
        module = self.module()
        snapshot = module.create_snapshot(capture()).snapshot
        module.maintain()
        other = SQLiteSnapshotStore(self.path)
        self.addCleanup(other.close)
        other.delete(snapshot, now=self.now, quarantine_seconds=1)
        self.now += 1
        self.assert_code('SNAPSHOT.EXPIRED', lambda: module.undelete_snapshot(snapshot))
        self.assertEqual(module._store.counts()['content_sets'], 0)

    def test_due_work_keeps_busy_failure_without_partial_deletion(self):
        module = self.module()
        snapshot, head, root = self.seed(module)
        module.delete_snapshot(snapshot)
        self.now += 10
        before = module._store.counts()
        module._store._connection.execute('PRAGMA busy_timeout=1')
        writer = self.connection()
        writer.execute('BEGIN IMMEDIATE')
        try:
            self.assert_code('SNAPSHOT_STORE.BUSY', module.maintain)
            self.assertEqual(module._store.counts(), before)
            self.assertFalse(module._store._connection.in_transaction)
        finally:
            writer.execute('ROLLBACK')
        module.maintain()
        self.assert_code('SNAPSHOT.EXPIRED', lambda: module.snapshot(snapshot))
        self.assert_code('AGGREGATE.UNAVAILABLE', lambda: module.load_aggregate(head.aggregate_id))
        self.assert_code('AGGREGATE.ROOT_UNAVAILABLE', lambda: module.load_aggregate_root(root.aggregate_id))
        self.assertEqual(module._store.counts()['child_index'], 0)
        self.assertEqual(module._store.counts()['purged_root_tombstones'], 1)

    def test_positive_probe_rechecks_concurrent_undelete_and_requarantine(self):
        for renew in (False, True):
            with self.subTest(renew=renew):
                # Each interleaving owns a separate database and clock.
                with tempfile.TemporaryDirectory() as temporary:
                    path = Path(temporary) / 'snapshots.sqlite3'
                    with SnapshotModule.open(path, now=lambda: self.now, quarantine_seconds=1) as module:
                        snapshot = module.create_snapshot(capture()).snapshot
                        module.delete_snapshot(snapshot)
                        self.now += 1
                        other = SQLiteSnapshotStore(path)
                        try:
                            def interleave():
                                other.undelete(snapshot)
                                if renew:
                                    other.delete(snapshot, now=self.now, quarantine_seconds=20)
                            original = module._store._connection
                            proxy = _BeforeWriterConnection(original, interleave)
                            module._store._connection = proxy
                            try:
                                module.maintain()
                            finally:
                                module._store._connection = original
                            self.assertEqual(proxy.calls, 1)
                            result = module.snapshot(snapshot, include_quarantined=True)
                            self.assertEqual(result.lifecycle, 'quarantined' if renew else 'active')
                            self.assertEqual(module._store.counts()['purged_root_tombstones'], 0)
                        finally:
                            other.close()

    def test_positive_probe_rechecks_competing_purge(self):
        module = self.module()
        snapshot = module.create_snapshot(capture()).snapshot
        module.delete_snapshot(snapshot)
        self.now += 10
        other = SQLiteSnapshotStore(self.path)
        self.addCleanup(other.close)
        original = module._store._connection
        proxy = _BeforeWriterConnection(original, lambda: other.purge_expired(self.now))
        module._store._connection = proxy
        try:
            module.maintain()
        finally:
            module._store._connection = original
        self.assertEqual(proxy.calls, 1)
        self.assertEqual(module._store.counts()['purged_root_tombstones'], 1)
        self.assert_code('SNAPSHOT.EXPIRED', lambda: module.snapshot(snapshot))

    def test_guarded_selection_includes_newly_due_root_not_just_probe_result(self):
        module = self.module()
        first = module.create_snapshot(capture(b'first')).snapshot
        second = module.create_snapshot(capture(b'second')).snapshot
        module.delete_snapshot(first)
        self.now += 10
        other = SQLiteSnapshotStore(self.path)
        self.addCleanup(other.close)
        original = module._store._connection
        proxy = _BeforeWriterConnection(original, lambda: other.delete(
            second, now=self.now - 1, quarantine_seconds=1,
        ))
        module._store._connection = proxy
        try:
            module.maintain()
        finally:
            module._store._connection = original
        self.assertEqual(proxy.calls, 1)
        for snapshot in (first, second):
            self.assert_code('SNAPSHOT.EXPIRED', lambda: module.snapshot(snapshot))
        self.assertEqual(module._store.counts()['purged_root_tombstones'], 2)

    def test_probe_sql_error_retains_typed_failure_without_transaction(self):
        module = self.module()
        statements = []
        module._store._connection.set_trace_callback(statements.append)
        # Deny just the selected SQLite read; leave real execution/error adaptation.
        module._store._connection.set_authorizer(lambda action, arg1, *rest:
            sqlite3.SQLITE_DENY if action == sqlite3.SQLITE_READ and arg1 == 'snapshot_roots'
            else sqlite3.SQLITE_OK)
        try:
            self.assert_code('SNAPSHOT_STORE.INVALID_DATABASE', module.maintain)
        finally:
            module._store._connection.set_authorizer(None)
        self.assertNotIn('BEGIN IMMEDIATE', statements)
        self.assertFalse(module._store._connection.in_transaction)

    def test_new_and_current_admission_have_one_full_integrity_audit_per_process(self):
        # The creating process audits its new file, and does not audit it again.
        self.assertEqual(self.events(), [('configure', 0, False), ('integrity', 2, False)])
        for _ in range(2):
            self.assertEqual(self.events(), [('configure', 2, False)])
        # A new process audits the existing file once, before configuration.
        _begin_as_new_process()
        self.assertEqual(self.events(), [('integrity', 2, False), ('configure', 2, False)])
        for _ in range(2):
            self.assertEqual(self.events(), [('configure', 2, False)])

    def test_two_module_opens_in_one_process_audit_the_file_once(self):
        with SnapshotModule.open(self.path, now=lambda: self.now) as initial:
            snapshot = initial.create_snapshot(capture()).snapshot
        _begin_as_new_process()
        opens = []
        connect = sqlite3.connect

        def traced_connect(database, *arguments, **options):
            # Observe each store connection from before its first statement.
            connection = connect(database, *arguments, **options)
            if Path(database).resolve() == self.path.resolve():
                opens.append([])
                connection.set_trace_callback(opens[-1].append)
            return connection

        with mock.patch.object(store_module.sqlite3, 'connect', traced_connect):
            for _ in range(2):
                with SnapshotModule.open(self.path, now=lambda: self.now) as reopened:
                    self.assertEqual(reopened.load_content(snapshot), capture())
        first, second = opens
        audit = ['PRAGMA integrity_check', 'PRAGMA foreign_key_check']
        self.assertEqual([statement for statement in first if statement in audit], audit)
        # The later open omits exactly that pair and repeats every other statement.
        self.assertEqual([statement for statement in first if statement not in audit], second)
        self.assertIn('PRAGMA application_id', second)
        self.assertIn('PRAGMA user_version', second)
        self.assertTrue(any('FROM sqlite_schema' in statement for statement in second), second)

    def test_replaced_file_is_audited_again(self):
        self.assertEqual(self.events(), [('configure', 0, False), ('integrity', 2, False)])
        self.assertEqual(self.events(), [('configure', 2, False)])
        audited = _file_identity(self.path)
        # The replacement exists beside the audited file, so it has another inode.
        replacement = self.path.with_name('replacement.sqlite3')
        shutil.copyfile(self.path, replacement)
        self.assertNotEqual(_file_identity(replacement), audited)
        os.replace(replacement, self.path)
        self.assertEqual(self.events(), [('integrity', 2, False), ('configure', 2, False)])
        self.assertEqual(self.events(), [('configure', 2, False)])

    def test_corrupt_replacement_of_an_audited_file_is_rejected(self):
        SQLiteSnapshotStore(self.path).close()
        SQLiteSnapshotStore(self.path).close()
        replacement = self.path.with_name('replacement.sqlite3')
        shutil.copyfile(self.path, replacement)
        _violate_foreign_key(replacement)
        os.replace(replacement, self.path)
        self.assert_code('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', lambda: SQLiteSnapshotStore(self.path))
        # A rejected file gains no audit record: the next open audits it again.
        self.assert_code('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', lambda: SQLiteSnapshotStore(self.path))
        self.assertTrue(self.path.is_file())

    def test_later_opens_keep_application_version_and_schema_checks(self):
        for change, code in (
            ('PRAGMA application_id=1', 'SNAPSHOT_STORE.INVALID_APPLICATION'),
            ('PRAGMA user_version=3', 'SNAPSHOT_STORE.UNSUPPORTED_VERSION'),
            ('PRAGMA user_version=0', 'SNAPSHOT_STORE.INVALID_VERSION'),
            ('CREATE TABLE unexpected (value TEXT)', 'SNAPSHOT_STORE.INVALID_SCHEMA'),
            ('DROP TRIGGER child_index_no_update', 'SNAPSHOT_STORE.INVALID_SCHEMA'),
        ):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'snapshots.sqlite3'
                SQLiteSnapshotStore(path).close()
                self.assertEqual(self.events(path), [('configure', 2, False)])
                with closing(sqlite3.connect(path, isolation_level=None)) as changer:
                    changer.execute(change)
                # Same file, already audited by this process: only the audit is omitted.
                self.assert_code(code, lambda: _ObservedAdmissionStore(path))
                self.assertTrue(path.is_file())

    def test_new_process_rejects_corruption_in_a_file_audited_elsewhere(self):
        for corruption, code in (('foreign-key', 'SNAPSHOT_STORE.FOREIGN_KEY_FAILURE'),
                                 ('check', 'SNAPSHOT_STORE.INTEGRITY_FAILURE')):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'snapshots.sqlite3'
                # This process audits the file; that record stays in this process.
                SQLiteSnapshotStore(path).close()
                self.assertEqual(self.cold_open(path), 'admitted')
                with closing(sqlite3.connect(path, isolation_level=None)) as corruptor:
                    if corruption == 'foreign-key':
                        corruptor.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")
                    else:
                        corruptor.execute('PRAGMA ignore_check_constraints=ON')
                        corruptor.execute("INSERT INTO content_sets VALUES ('bad', 0)")
                self.assertEqual(self.cold_open(path), code)
                self.assertTrue(path.is_file())

    def test_version_one_keeps_preconfiguration_guarded_and_final_audits(self):
        _, record = _populated_version_one_store(self.path)
        before = _version_one_rows(self.path)
        # Building the fixture audited this same file as a current store. That
        # record must not shorten any audit of its version-one admission.
        self.assertTrue(store_module._audit_recorded(_file_identity(self.path)))
        opened = _ObservedAdmissionStore(self.path)
        try:
            self.assertEqual(opened.admission_events, [
                ('integrity', 1, False), ('configure', 1, False),
                ('integrity', 1, True), ('integrity', 2, True), ('integrity', 2, False),
            ])
            self.assertEqual(opened.load_aggregate(record.aggregate_id), record)
        finally:
            opened.close()
        self.assertEqual(_version_one_rows(self.path), before)

    def test_version_one_migration_in_a_new_process_keeps_every_audit(self):
        _populated_version_one_store(self.path)
        before = _version_one_rows(self.path)
        _begin_as_new_process()
        self.assertEqual(self.events(), [
            ('integrity', 1, False), ('configure', 1, False),
            ('integrity', 1, True), ('integrity', 2, True), ('integrity', 2, False),
        ])
        self.assertEqual(_version_one_rows(self.path), before)
        # The final destination audit is this process's audit of the migrated file.
        self.assertEqual(self.events(), [('configure', 2, False)])

    def test_other_opener_migration_keeps_destination_audit(self):
        _populated_version_one_store(self.path)
        before = _version_one_rows(self.path)

        class CompetingMigrationStore(_ObservedAdmissionStore):
            def _configure(inner):
                super()._configure()
                migrated = SQLiteSnapshotStore(inner.path)
                migrated.close()

        opened = CompetingMigrationStore(self.path)
        try:
            self.assertEqual(opened.admission_events, [
                ('integrity', 1, False), ('configure', 1, False), ('integrity', 2, False),
            ])
        finally:
            opened.close()
        self.assertEqual(_version_one_rows(self.path), before)

    def test_migration_completed_after_prepare_still_gets_final_audit(self):
        _populated_version_one_store(self.path)
        before = _version_one_rows(self.path)

        class CompetingMigrationStore(_ObservedAdmissionStore):
            def _migrate_version_one(inner):
                migrated = SQLiteSnapshotStore(inner.path)
                migrated.close()
                super()._migrate_version_one()

        opened = CompetingMigrationStore(self.path)
        try:
            self.assertEqual(opened.admission_events, [
                ('integrity', 1, False), ('configure', 1, False), ('integrity', 2, False),
            ])
        finally:
            opened.close()
        self.assertEqual(_version_one_rows(self.path), before)

    def test_competing_migration_does_not_bypass_destination_corruption(self):
        _populated_version_one_store(self.path)

        class CompetingCorruptMigrationStore(_ObservedAdmissionStore):
            def _configure(inner):
                super()._configure()
                migrated = SQLiteSnapshotStore(inner.path)
                migrated.close()
                with closing(sqlite3.connect(inner.path, isolation_level=None)) as corruptor:
                    corruptor.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")

        self.assert_code('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE',
                         lambda: CompetingCorruptMigrationStore(self.path))
        self.assertTrue(self.path.is_file())

    def test_current_corruption_is_rejected_before_persistent_configuration(self):
        for corruption, code in (('foreign-key', 'SNAPSHOT_STORE.FOREIGN_KEY_FAILURE'),
                                 ('check', 'SNAPSHOT_STORE.INTEGRITY_FAILURE')):
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'snapshots.sqlite3'
                SQLiteSnapshotStore(path).close()
                with closing(sqlite3.connect(path, isolation_level=None)) as corruptor:
                    corruptor.execute('PRAGMA journal_mode=WAL')
                    if corruption == 'foreign-key':
                        corruptor.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")
                    else:
                        corruptor.execute('PRAGMA ignore_check_constraints=ON')
                        corruptor.execute("INSERT INTO content_sets VALUES ('bad', 0)")
                # The first open by a process is the one that audits.
                _begin_as_new_process()
                self.assert_code(code, lambda: _ObservedAdmissionStore(path))
                self.assertTrue(path.is_file())
                with closing(sqlite3.connect(path)) as observed:
                    self.assertEqual(observed.execute('PRAGMA journal_mode').fetchone(), ('wal',))

    def test_postconfiguration_schema_check_is_retained(self):
        SQLiteSnapshotStore(self.path).close()

        class SchemaChangedStore(SQLiteSnapshotStore):
            def _configure(inner):
                super()._configure()
                inner._connection.execute('CREATE TABLE unexpected (value TEXT)')

        self.assert_code('SNAPSHOT_STORE.INVALID_SCHEMA', lambda: SchemaChangedStore(self.path))
        self.assertTrue(self.path.is_file())

    def test_failed_new_integrity_check_closes_and_removes_only_owned_file(self):
        connections = []

        class CorruptInitializationStore(SQLiteSnapshotStore):
            def _initialize_schema(inner):
                super()._initialize_schema()
                connections.append(inner._connection)
                inner._connection.execute('PRAGMA foreign_keys=OFF')
                inner._connection.execute("INSERT INTO content_files VALUES ('missing', 'a', X'', 0, 'digest')")

        self.assert_code('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', lambda: CorruptInitializationStore(self.path))
        self.assertFalse(self.path.exists())
        with self.assertRaises(sqlite3.ProgrammingError):
            connections[0].execute('SELECT 1')

    def test_readmission_runs_the_statements_of_a_later_open(self):
        with SnapshotModule.open(self.path, now=lambda: self.now) as initial:
            snapshot = initial.create_snapshot(capture()).snapshot
        opens = []
        connect = sqlite3.connect

        def traced_connect(database, *arguments, **options):
            connection = connect(database, *arguments, **options)
            opens.append([])
            connection.set_trace_callback(opens[-1].append)
            return connection

        with mock.patch.object(store_module.sqlite3, 'connect', traced_connect):
            kept = SnapshotModule.open(self.path, now=lambda: self.now)
            self.addCleanup(kept.close)
            kept.release()
            SnapshotModule.open(self.path, now=lambda: self.now).close()
            opened, later = opens
            self.assertEqual(opened, later)
            self.assertNotIn('PRAGMA integrity_check', later)
            for _ in range(2):
                self.assertTrue(kept.readmit())
                # A new connection: admission and the maintenance probe, statement for statement.
                self.assertEqual(opens[-1], later)
                self.assertEqual(kept.load_content(snapshot), capture())
                kept.release()
            self.assertEqual(len(opens), 4)
            # A process without an audit record audits on readmission, as on open.
            _begin_as_new_process()
            self.assertTrue(kept.readmit())
        self.assertEqual([statement for statement in opens[-1] if statement not in later],
                         ['PRAGMA integrity_check', 'PRAGMA foreign_key_check'])
        self.assertTrue(store_module._audit_recorded(_file_identity(self.path)))

    def test_released_store_holds_no_connection_and_readmission_opens_a_new_one(self):
        module = self.module()
        snapshot, head, root = self.seed(module)
        uses = (
            lambda: module.load_content(snapshot),
            lambda: module.find_snapshots(FindSnapshotsRequest(limit=10)),
            lambda: module.inspect_child(ChildHandle(head.aggregate_id, 'requirement', 'one')),
            lambda: module.create_snapshot(capture(b'another')),
            lambda: self.assert_code('AGGREGATE.UNAVAILABLE', lambda: module.load_aggregate('missing')),
            lambda: module.delete_snapshot(snapshot),
            lambda: module.undelete_snapshot(snapshot),
        )
        seen = []
        for use in uses:
            use()
            connection = module._store._connection
            self.assertFalse(any(connection is earlier for earlier in seen))
            seen.append(connection)
            module.release()
            self.assert_released(module)
            # Releasing a released store does nothing.
            module.release()
            self.assertTrue(module.readmit())
        # Readmission without a release also replaces the connection.
        connection = module._store._connection
        self.assertTrue(module.readmit())
        self.assertIsNot(module._store._connection, connection)
        with self.assertRaises(sqlite3.ProgrammingError):
            connection.execute('SELECT 1')
        self.assertEqual(module.load_aggregate_root(root.aggregate_id), root)
        # Closing a released store does nothing either.
        module.release()
        module.close()
        self.assert_released(module)

    def test_release_rolls_back_a_transaction_the_use_did_not_end(self):
        module = self.module()
        module._store._connection.execute('BEGIN IMMEDIATE')
        module._store._connection.execute(
            'INSERT INTO purged_root_tombstones VALUES (?, ?)', ('left-open', 1))
        module.release()
        observed = self.connection()
        self.assertIsNone(observed.execute(
            "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = 'left-open'").fetchone())
        self.assertFalse(self.path.with_name(self.path.name + '-journal').exists())
        self.assertTrue(module.readmit())
        self.assertEqual(module._store.counts()['purged_root_tombstones'], 0)

    def test_readmission_reads_a_file_overwritten_in_place_as_a_new_open_does(self):
        # Two stores with the same history but different content. Their change
        # counters, page counts and schema cookies are equal, which is all that
        # SQLite compares before trusting the pages a connection has read. A
        # store that kept its connection would go on answering from the old ones.
        first, second = self.path, self.path.with_name('second.sqlite3')
        snapshots = {}
        for path, content in ((first, b'first lineage'), (second, b'other lineage')):
            with SnapshotModule.open(path, now=lambda: self.now) as module:
                snapshots[path] = module.create_snapshot(capture(content)).snapshot
        self.assertEqual(first.read_bytes()[24:44], second.read_bytes()[24:44])
        self.assertEqual(first.stat().st_size, second.stat().st_size)
        kept = SnapshotModule.open(first, now=lambda: self.now)
        self.addCleanup(kept.close)
        self.assertEqual(kept.load_content(snapshots[first]), capture(b'first lineage'))
        kept.release()
        identity = _file_identity(first)
        shutil.copyfile(second, first)
        self.assertEqual(_file_identity(first), identity)
        self.assertTrue(kept.readmit())
        # Exactly what a new open of the path reads: nothing of the old content.
        self.assert_code('SNAPSHOT.UNAVAILABLE', lambda: kept.load_content(snapshots[first]))
        self.assertEqual(kept.load_content(snapshots[second]), capture(b'other lineage'))

    def test_readmission_reports_a_path_that_names_another_file_or_none(self):
        def replaced(path):
            replacement = path.with_name('replacement.sqlite3')
            shutil.copyfile(path, replacement)
            os.replace(replacement, path)

        def moved_behind_a_link(path):
            target = path.with_name('moved.sqlite3')
            os.replace(path, target)
            path.symlink_to(target)

        for change, reopened in ((replaced, 'admitted'), (Path.unlink, 'admitted'),
                                 (moved_behind_a_link, 'SNAPSHOT_STORE.UNSUPPORTED_PATH')):
            with self.subTest(change=change.__name__), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'snapshots.sqlite3'
                with SnapshotModule.open(path, now=lambda: self.now) as kept:
                    kept.create_snapshot(capture())
                    kept.release()
                    self.assertTrue(kept.readmit())
                    kept.release()
                    opened = _file_identity(path)
                    self.assertTrue(store_module._audit_recorded(opened))
                    change(path)
                    # Nothing is opened: what is at the path now is for a new open to decide.
                    connect = sqlite3.connect
                    with mock.patch.object(store_module.sqlite3, 'connect', wraps=connect) as connections:
                        self.assertFalse(kept.readmit())
                        self.assertFalse(kept.readmit())
                    connections.assert_not_called()
                    # A file that is given the opened file's inode number later
                    # has no audit record.
                    self.assertFalse(store_module._audit_recorded(opened))
                # The owner's new open is what admits, creates or refuses the path.
                if reopened == 'admitted':
                    SnapshotModule.open(path, now=lambda: self.now).close()
                else:
                    self.assert_code(reopened, lambda: SnapshotModule.open(path))

    def assert_released(self, module):
        with self.assertRaises(sqlite3.ProgrammingError):
            module._store._connection.execute('SELECT 1')
        # An exclusive transaction needs every other connection to hold no lock.
        with closing(sqlite3.connect(module._store.path, isolation_level=None, timeout=0)) as other:
            other.execute('BEGIN EXCLUSIVE')
            other.execute('ROLLBACK')

    def test_readmission_keeps_application_version_and_schema_checks(self):
        for change, code in (
            ('PRAGMA application_id=1', 'SNAPSHOT_STORE.INVALID_APPLICATION'),
            ('PRAGMA user_version=3', 'SNAPSHOT_STORE.UNSUPPORTED_VERSION'),
            ('PRAGMA user_version=0', 'SNAPSHOT_STORE.INVALID_VERSION'),
            ('CREATE TABLE unexpected (value TEXT)', 'SNAPSHOT_STORE.INVALID_SCHEMA'),
            ('DROP TRIGGER child_index_no_update', 'SNAPSHOT_STORE.INVALID_SCHEMA'),
        ):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'snapshots.sqlite3'
                with SnapshotModule.open(path, now=lambda: self.now) as kept:
                    kept.release()
                    self.assertTrue(kept.readmit())
                    kept.release()
                    with closing(sqlite3.connect(path, isolation_level=None)) as changer:
                        changer.execute(change)
                    # The code a new open of this file reports.
                    self.assert_code(code, kept.readmit)
                    self.assert_code(code, lambda: SQLiteSnapshotStore(path))
                    # A refused readmission leaves no connection behind.
                    self.assert_released(kept)

    def test_readmission_restores_the_required_profile_as_an_open_does(self):
        kept = self.module()
        kept.release()
        with closing(sqlite3.connect(self.path, isolation_level=None)) as changer:
            self.assertEqual(changer.execute('PRAGMA journal_mode=WAL').fetchone(), ('wal',))
        self.assertTrue(kept.readmit())
        with closing(sqlite3.connect(self.path)) as observed:
            self.assertEqual(observed.execute('PRAGMA journal_mode').fetchone(), ('delete',))
        kept.create_snapshot(capture())
        self.assertFalse(self.path.with_name(self.path.name + '-wal').exists())

    def test_readmission_migrates_a_version_one_file_with_every_audit(self):
        _, record = _populated_version_one_store(self.path)
        kept = _ObservedAdmissionStore(self.path)
        self.addCleanup(kept.close)
        self.assertEqual(kept.load_aggregate(record.aggregate_id), record)
        kept.release()
        # Another process returns the same file to version one between uses.
        _downgrade_to_version_one(self.path)
        before = _version_one_rows(self.path)
        del kept.admission_events[:]
        self.assertTrue(kept.readmit())
        self.assertEqual(kept.admission_events, [
            ('integrity', 1, False), ('configure', 1, False),
            ('integrity', 1, True), ('integrity', 2, True), ('integrity', 2, False),
        ])
        self.assertEqual(_version_one_rows(self.path), before)
        self.assertEqual(kept.load_aggregate(record.aggregate_id), record)
        kept.release()
        del kept.admission_events[:]
        self.assertTrue(kept.readmit())
        self.assertEqual(kept.admission_events, [('configure', 2, False)])

    def test_readmission_audits_and_rejects_a_file_without_an_audit_record(self):
        kept = SQLiteSnapshotStore(self.path)
        self.addCleanup(kept.close)
        kept.release()
        _violate_foreign_key(self.path)
        # The record of this process's audit stands: damage after it is not looked for.
        self.assertTrue(kept.readmit())
        kept.release()
        _begin_as_new_process()
        self.assert_code('SNAPSHOT_STORE.FOREIGN_KEY_FAILURE', kept.readmit)
        self.assertFalse(store_module._audit_recorded(_file_identity(self.path)))
        # A refused readmission leaves no connection behind.
        with self.assertRaises(sqlite3.ProgrammingError):
            kept._connection.execute('SELECT 1')

    def test_readmission_runs_due_maintenance_and_keeps_its_busy_failure(self):
        module = self.module()
        snapshot, head, root = self.seed(module)
        module.delete_snapshot(snapshot)
        module.release()
        self.now += 10
        writer = self.connection()
        writer.execute('BEGIN IMMEDIATE')
        try:
            self.assert_code('SNAPSHOT_STORE.BUSY', module.readmit)
            # The failed readmission left no connection behind.
            with self.assertRaises(sqlite3.ProgrammingError):
                module._store._connection.execute('SELECT 1')
            self.assertIsNotNone(writer.execute(
                'SELECT 1 FROM snapshot_roots WHERE snapshot_id = ?', (str(snapshot),)).fetchone())
        finally:
            writer.execute('ROLLBACK')
        self.assertTrue(module.readmit())
        self.assert_code('SNAPSHOT.EXPIRED', lambda: module.snapshot(snapshot))
        self.assert_code('AGGREGATE.UNAVAILABLE', lambda: module.load_aggregate(head.aggregate_id))

if __name__ == '__main__':
    unittest.main()
