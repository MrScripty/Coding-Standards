from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.standards_snapshots.standards_snapshots import (
    AggregateRecord,
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


class SnapshotStoreTests(unittest.TestCase):
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
