from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.standards_snapshots.standards_snapshots import (
    AggregateChild,
    AggregateRecord,
    ChildHandle,
    FindSnapshotsRequest,
    SnapshotError,
    SnapshotModule,
)
from tools.standards_snapshots.standards_snapshots.store import SQLiteSnapshotStore
from tools.standards_snapshots.tests.test_module import DAY, capture


class _InterruptedPurgeStore(SQLiteSnapshotStore):
    def _purge_stage(self, stage: str, snapshot_id: str) -> None:
        if stage == "after-root-delete":
            raise RuntimeError(f"interrupted {snapshot_id}")


class _InterruptedMigrationStore(SQLiteSnapshotStore):
    interrupted_connection: sqlite3.Connection | None = None

    def _migration_stage(self, stage: str) -> None:
        if stage == "before-commit":
            type(self).interrupted_connection = self._connection
            raise RuntimeError("interrupted migration")


class _FailedInitializationStore(SQLiteSnapshotStore):
    def _initialize_schema(self) -> None:
        raise RuntimeError("failed initialization")


_VERSION_ONE_TABLES = (
    "content_sets",
    "content_files",
    "snapshot_roots",
    "aggregate_records",
    "aggregate_snapshot_dependencies",
    "child_index",
    "purged_root_tombstones",
)


def _downgrade_to_version_one(path: Path) -> None:
    connection = sqlite3.connect(path, isolation_level=None)
    connection.executescript(
        "BEGIN IMMEDIATE;\n"
        "DROP TRIGGER aggregate_root_dependencies_no_update;\n"
        "DROP TRIGGER aggregate_roots_no_material_update;\n"
        "DROP TRIGGER aggregate_root_tombstones_no_update;\n"
        "DROP TABLE aggregate_root_snapshot_dependencies;\n"
        "DROP TABLE aggregate_roots;\n"
        "DROP TABLE aggregate_root_tombstones;\n"
        "DROP TRIGGER delete_root_aggregate;\n"
        "CREATE TRIGGER delete_root_aggregate\n"
        "BEFORE DELETE ON snapshot_roots\n"
        "BEGIN\n"
        "    DELETE FROM aggregate_records WHERE aggregate_id IN (\n"
        "        SELECT aggregate_id FROM aggregate_snapshot_dependencies\n"
        "        WHERE snapshot_id = OLD.snapshot_id\n"
        "    );\n"
        "END;\n"
        "PRAGMA user_version=1;\n"
        "COMMIT;"
    )
    connection.close()


def _version_one_rows(path: Path) -> dict[str, tuple[tuple[object, ...], ...]]:
    connection = sqlite3.connect(path)
    try:
        return {
            table: tuple(
                sorted(
                    connection.execute(f"SELECT * FROM {table}").fetchall(),
                    key=repr,
                )
            )
            for table in _VERSION_ONE_TABLES
        }
    finally:
        connection.close()


def _populated_version_one_store(path: Path) -> tuple[object, AggregateRecord]:
    now = [2_000_000_000]
    with SnapshotModule.open(path, now=lambda: now[0], quarantine_seconds=1) as module:
        expired = module.create_snapshot(capture(b"expired")).snapshot
        module.delete_snapshot(expired)
        now[0] += 1
        module.maintain()

        active = module.create_snapshot(capture(b"active")).snapshot
        quarantined = module.create_snapshot(capture(b"quarantined")).snapshot
        record = AggregateRecord(
            "analysis:v1:migration",
            "analysis",
            b"state",
            (active,),
            (AggregateChild("requirement", "migration", b"child"),),
        )
        module.publish_aggregate(record)
        module.delete_snapshot(quarantined)
    _downgrade_to_version_one(path)
    return active, record


class SnapshotStoreTests(unittest.TestCase):
    def test_version_one_store_migrates_transactionally_without_changing_a1c_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            path = Path(temporary) / "snapshots.sqlite3"
            active, record = _populated_version_one_store(path)
            before = _version_one_rows(path)
            self.assertTrue(all(before.values()))

            with SnapshotModule.open(path) as migrated:
                self.assertEqual(migrated.load_content(active), capture(b"active"))
                self.assertEqual(migrated.load_aggregate(record.aggregate_id), record)
                self.assertEqual(
                    migrated.inspect_child(
                        ChildHandle(record.aggregate_id, "requirement", "migration")
                    ),
                    b"child",
                )
                self.assertEqual(
                    migrated._store._connection.execute(
                        "PRAGMA user_version"
                    ).fetchone(),
                    (2,),
                )
            self.assertEqual(_version_one_rows(path), before)

    def test_interrupted_version_one_migration_rolls_back_every_change(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            path = Path(temporary) / "snapshots.sqlite3"
            _populated_version_one_store(path)
            before = _version_one_rows(path)

            with self.assertRaisesRegex(RuntimeError, "interrupted migration"):
                _InterruptedMigrationStore(path)
            interrupted = _InterruptedMigrationStore.interrupted_connection
            self.assertIsNotNone(interrupted)
            assert interrupted is not None
            with self.assertRaises(sqlite3.ProgrammingError):
                interrupted.execute("SELECT 1")

            connection = sqlite3.connect(path)
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone(), (1,))
            self.assertIsNone(
                connection.execute(
                    "SELECT 1 FROM sqlite_schema WHERE name = 'aggregate_roots'"
                ).fetchone()
            )
            connection.close()
            self.assertEqual(_version_one_rows(path), before)

            with SnapshotModule.open(path) as migrated:
                self.assertEqual(
                    migrated._store._connection.execute(
                        "PRAGMA user_version"
                    ).fetchone(),
                    (2,),
                )

    def test_invalid_version_one_authority_is_not_migrated(self) -> None:
        for corruption in ("schema", "integrity"):
            with (
                self.subTest(corruption=corruption),
                tempfile.TemporaryDirectory(dir="/tmp") as temporary,
            ):
                path = Path(temporary) / "snapshots.sqlite3"
                _populated_version_one_store(path)
                connection = sqlite3.connect(path, isolation_level=None)
                if corruption == "schema":
                    connection.executescript(
                        "DROP TRIGGER child_index_no_update;"
                        "CREATE TRIGGER child_index_no_update "
                        "BEFORE UPDATE ON child_index BEGIN "
                        "SELECT RAISE(ABORT, 'different'); END;"
                    )
                else:
                    connection.execute("PRAGMA foreign_keys=OFF")
                    content_id = connection.execute(
                        "SELECT content_id FROM snapshot_roots LIMIT 1"
                    ).fetchone()[0]
                    connection.execute(
                        "DELETE FROM content_sets WHERE content_id = ?", (content_id,)
                    )
                connection.close()

                with self.assertRaises(SnapshotError):
                    SQLiteSnapshotStore(path)

                connection = sqlite3.connect(path)
                self.assertEqual(
                    connection.execute("PRAGMA user_version").fetchone(), (1,)
                )
                self.assertIsNone(
                    connection.execute(
                        "SELECT 1 FROM sqlite_schema WHERE name = 'aggregate_roots'"
                    ).fetchone()
                )
                connection.close()

    def test_invalid_existing_store_is_not_configured_before_rejection(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            path = Path(temporary) / "unrelated.sqlite3"
            connection = sqlite3.connect(path)
            self.assertEqual(
                connection.execute("PRAGMA journal_mode=WAL").fetchone(), ("wal",)
            )
            connection.execute("CREATE TABLE unrelated (value TEXT)")
            connection.close()

            with self.assertRaises(SnapshotError) as rejected:
                SQLiteSnapshotStore(path)
            self.assertEqual(
                rejected.exception.failure.code,
                "SNAPSHOT_STORE.INVALID_APPLICATION",
            )

            connection = sqlite3.connect(path)
            self.assertEqual(
                connection.execute("PRAGMA journal_mode").fetchone(), ("wal",)
            )
            connection.close()

    def test_failed_new_store_initialization_removes_owned_staging_file(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            path = Path(temporary) / "snapshots.sqlite3"
            with self.assertRaisesRegex(RuntimeError, "failed initialization"):
                _FailedInitializationStore(path)
            self.assertFalse(path.exists())

    def test_snapshot_material_rows_reject_updates(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            store = SQLiteSnapshotStore(Path(temporary) / "snapshots.sqlite3")
            module = SnapshotModule(store)
            snapshot = module.create_snapshot(capture()).snapshot
            for statement in (
                "UPDATE content_sets SET file_count = 3",
                "UPDATE content_files SET raw_bytes = X'00'",
                "UPDATE snapshot_roots SET source_revision = 'replacement'",
            ):
                with (
                    self.subTest(statement=statement),
                    self.assertRaises(sqlite3.IntegrityError),
                ):
                    store._connection.execute(statement)
            self.assertEqual(module.load_content(snapshot), capture())
            module.close()

    def test_interrupted_purge_rolls_back_root_aggregate_and_tombstone(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            path = Path(temporary) / "snapshots.sqlite3"
            store = _InterruptedPurgeStore(path)
            module = SnapshotModule(store, now=lambda: now[0])
            snapshot = module.create_snapshot(capture()).snapshot
            record = AggregateRecord(
                "analysis:v1:rollback", "analysis", b"state", (snapshot,)
            )
            module.publish_aggregate(record)
            module.delete_snapshot(snapshot)
            now[0] += 7 * DAY
            with self.assertRaisesRegex(RuntimeError, "interrupted"):
                module.maintain()
            self.assertEqual(store.counts()["purged_root_tombstones"], 0)
            module.close()

            with SnapshotModule.open(path, now=lambda: now[0] - 1) as reopened:
                summary = reopened.snapshot(snapshot, include_quarantined=True)
                self.assertEqual(summary.lifecycle, "quarantined")

    def test_equal_content_roots_share_content_until_the_last_root_expires(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            store = SQLiteSnapshotStore(Path(temporary) / "snapshots.sqlite3")
            module = SnapshotModule(store, now=lambda: now[0])
            first = module.create_snapshot(capture()).snapshot
            second = module.create_snapshot(capture()).snapshot
            self.assertEqual(store.counts()["content_sets"], 1)

            module.delete_snapshot(first)
            now[0] += 7 * DAY
            module.maintain()
            self.assertEqual(store.counts()["content_sets"], 1)

            module.delete_snapshot(second)
            now[0] += 7 * DAY
            module.maintain()
            self.assertEqual(store.counts()["content_sets"], 0)
            module.close()

    def test_aggregate_publication_is_idempotent_but_contradiction_rejects(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            with SnapshotModule.open(Path(temporary) / "snapshots.sqlite3") as module:
                snapshot = module.create_snapshot(capture()).snapshot
                record = AggregateRecord(
                    "analysis:v1:stable", "analysis", b"one", (snapshot,)
                )
                self.assertEqual(module.publish_aggregate(record), "inserted")
                self.assertEqual(module.publish_aggregate(record), "existing-identical")
                with self.assertRaises(SnapshotError) as raised:
                    module.publish_aggregate(
                        AggregateRecord(
                            "analysis:v1:stable", "analysis", b"two", (snapshot,)
                        )
                    )
                self.assertEqual(
                    raised.exception.failure.code, "AGGREGATE.ID_COLLISION"
                )

    def test_invalid_database_and_unsupported_path_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            relative = Path("relative.sqlite3")
            with self.assertRaises(SnapshotError) as relative_error:
                SnapshotModule.open(relative)
            self.assertEqual(
                relative_error.exception.failure.code, "SNAPSHOT_STORE.RELATIVE_PATH"
            )

            invalid = root / "invalid.sqlite3"
            invalid.write_bytes(b"not sqlite")
            with self.assertRaises(SnapshotError) as invalid_error:
                SnapshotModule.open(invalid)
            self.assertEqual(invalid_error.exception.failure.kind, "invalid")

            target = root / "target.sqlite3"
            sqlite3.connect(target).close()
            link = root / "link.sqlite3"
            os.symlink(target, link)
            with self.assertRaises(SnapshotError) as link_error:
                SnapshotModule.open(link)
            self.assertEqual(link_error.exception.failure.kind, "unsupported")

    def test_quarantined_root_blocks_new_aggregate_publication(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            with SnapshotModule.open(Path(temporary) / "snapshots.sqlite3") as module:
                snapshot = module.create_snapshot(capture()).snapshot
                module.delete_snapshot(snapshot)
                with self.assertRaises(SnapshotError) as raised:
                    module.publish_aggregate(
                        AggregateRecord(
                            "analysis:v1:blocked", "analysis", b"state", (snapshot,)
                        )
                    )
                self.assertEqual(raised.exception.failure.code, "SNAPSHOT.QUARANTINED")
                self.assertEqual(
                    module.find_snapshots(FindSnapshotsRequest()).snapshots,
                    (),
                )


if __name__ == "__main__":
    unittest.main()
