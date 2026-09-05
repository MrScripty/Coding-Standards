from __future__ import annotations

import shutil
import tempfile
import unittest
import uuid
from pathlib import Path

from tools.standards_snapshots.standards_snapshots import (
    AggregateChild,
    AggregateRecord,
    CapturedContent,
    ChildHandle,
    FindSnapshotsRequest,
    SnapshotError,
    SnapshotFile,
    SnapshotId,
    SnapshotModule,
    SnapshotPath,
)

DAY = 24 * 60 * 60


def capture(content: bytes = b"canonical") -> CapturedContent:
    return CapturedContent(
        "a" * 40,
        (
            SnapshotFile(SnapshotPath.parse("STANDARDS-ROUTER.md"), content),
            SnapshotFile(SnapshotPath.parse("topics/contracts.md"), b"contracts"),
        ),
    )


class SnapshotModuleTests(unittest.TestCase):
    def test_equal_content_with_nested_paths_can_be_recaptured_after_reopen(
        self,
    ) -> None:
        files = tuple(
            SnapshotFile(SnapshotPath.parse(path), path.encode("utf-8"))
            for path in (
                "profiles/rust.md",
                "profiles/rust/api.md",
                "profiles/rust-api.md",
                "profiles/é.md",
                "profiles/e\u0301.md",
                "profiles/é/api.md",
            )
        )
        first_capture = CapturedContent("first-revision", files)
        second_capture = CapturedContent("second-revision", reversed(files))
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            database = Path(temporary) / "snapshots.sqlite3"
            with SnapshotModule.open(database) as module:
                first = module.create_snapshot(first_capture)
            with SnapshotModule.open(database) as module:
                second = module.create_snapshot(second_capture)
                self.assertNotEqual(first.snapshot, second.snapshot)
                self.assertEqual(module.load_content(first.snapshot), first_capture)
                self.assertEqual(module.load_content(second.snapshot), second_capture)

    def test_nested_domain_values_reject_ambiguous_or_wrong_types(self) -> None:
        for operation in (
            lambda: SnapshotPath("ambiguous"),
            lambda: SnapshotFile("not-a-path", b"bytes"),  # type: ignore[arg-type]
            lambda: CapturedContent("revision", ("not-a-file",)),  # type: ignore[arg-type]
            lambda: AggregateRecord(
                "analysis:v1:invalid",
                "analysis",
                b"state",
                ("not-a-snapshot",),  # type: ignore[arg-type]
            ),
        ):
            with self.subTest(operation=operation), self.assertRaises(SnapshotError):
                operation()

    def test_equal_content_roots_have_independent_lifecycle_and_discovery(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            with SnapshotModule.open(
                Path(temporary) / "snapshots.sqlite3", now=lambda: now[0]
            ) as module:
                first = module.create_snapshot(capture())
                second = module.create_snapshot(capture())
                self.assertNotEqual(first.snapshot, second.snapshot)
                self.assertEqual(
                    module.find_snapshots(FindSnapshotsRequest()).snapshots,
                    tuple(
                        sorted(
                            (first, second),
                            key=lambda item: (item.created_at, str(item.snapshot)),
                        )
                    ),
                )

                deletion = module.delete_snapshot(first.snapshot)
                self.assertEqual(module.delete_snapshot(first.snapshot), deletion)
                self.assertEqual(
                    module.find_snapshots(FindSnapshotsRequest()).snapshots,
                    (second,),
                )
                self.assertEqual(
                    module.find_snapshots(
                        FindSnapshotsRequest(lifecycle="quarantined")
                    ).snapshots,
                    (module.snapshot(first.snapshot, include_quarantined=True),),
                )
                self.assertEqual(
                    module.undelete_snapshot(first.snapshot).lifecycle, "active"
                )
                self.assertEqual(
                    len(module.find_snapshots(FindSnapshotsRequest()).snapshots), 2
                )

    def test_multi_root_aggregate_is_unavailable_and_cascades_as_one_value(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            database = Path(temporary) / "snapshots.sqlite3"
            with SnapshotModule.open(database, now=lambda: now[0]) as module:
                first = module.create_snapshot(capture()).snapshot
                second = module.create_snapshot(capture()).snapshot
                only_second = AggregateRecord(
                    "analysis:v1:second",
                    "analysis",
                    b"second",
                    (second,),
                    (AggregateChild("requirement", "second", b"child-second"),),
                )
                both = AggregateRecord(
                    "analysis:v1:both",
                    "analysis",
                    b"both",
                    (first, second),
                    (AggregateChild("requirement", "both", b"child-both"),),
                )
                module.publish_aggregate(only_second)
                module.publish_aggregate(both)
                module.delete_snapshot(first)

                self.assertEqual(
                    module.load_aggregate(only_second.aggregate_id), only_second
                )
                self._expect(
                    "SNAPSHOT.QUARANTINED",
                    lambda: module.load_aggregate(both.aggregate_id),
                )
                module.undelete_snapshot(first)
                self.assertEqual(
                    module.inspect_child(
                        ChildHandle("analysis:v1:both", "requirement", "both")
                    ),
                    b"child-both",
                )
                module.delete_snapshot(first)
                now[0] += 7 * DAY
                module.maintain()
                self._expect(
                    "AGGREGATE.UNAVAILABLE",
                    lambda: module.load_aggregate(both.aggregate_id),
                )
                self.assertEqual(
                    module.load_aggregate(only_second.aggregate_id), only_second
                )

                module.delete_snapshot(second)
                now[0] += 7 * DAY
                module.maintain()
                self._expect("SNAPSHOT.EXPIRED", lambda: module.snapshot(first))

    def test_cold_reopen_and_closed_store_copy_reconstruct_exact_values(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            database = root / "snapshots.sqlite3"
            with SnapshotModule.open(database) as module:
                snapshot = module.create_snapshot(capture()).snapshot
                record = AggregateRecord(
                    "analysis:v1:cold",
                    "analysis",
                    b"payload",
                    (snapshot,),
                    (AggregateChild("obligation", "review", b"review"),),
                )
                module.publish_aggregate(record)
            self.assertFalse((root / "snapshots.sqlite3-wal").exists())
            self.assertFalse((root / "snapshots.sqlite3-shm").exists())

            copied = root / "moved.sqlite3"
            shutil.copyfile(database, copied)
            with SnapshotModule.open(copied) as reopened:
                self.assertEqual(reopened.load_content(snapshot), capture())
                self.assertEqual(reopened.load_aggregate(record.aggregate_id), record)
                self.assertEqual(
                    reopened.inspect_child(
                        ChildHandle(record.aggregate_id, "obligation", "review")
                    ),
                    b"review",
                )

    def test_snapshot_id_collision_rejects_without_aliasing_content(self) -> None:
        selected = SnapshotId.from_uuid(
            uuid.UUID("00000000-0000-4000-8000-000000000001")
        )
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            with SnapshotModule.open(
                Path(temporary) / "snapshots.sqlite3",
                snapshot_id_factory=lambda: selected,
            ) as module:
                module.create_snapshot(capture())
                self._expect(
                    "SNAPSHOT.ID_COLLISION", lambda: module.create_snapshot(capture())
                )
                self.assertEqual(
                    len(module.find_snapshots(FindSnapshotsRequest()).snapshots), 1
                )

    def test_expired_snapshot_id_cannot_be_reused(self) -> None:
        selected = SnapshotId.from_uuid(
            uuid.UUID("00000000-0000-4000-8000-000000000001")
        )
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            with SnapshotModule.open(
                Path(temporary) / "snapshots.sqlite3",
                now=lambda: now[0],
                snapshot_id_factory=lambda: selected,
            ) as module:
                module.create_snapshot(capture())
                module.delete_snapshot(selected)
                now[0] += 7 * DAY
                module.maintain()
                self._expect(
                    "SNAPSHOT.ID_COLLISION", lambda: module.create_snapshot(capture())
                )

    def test_keyset_pagination_uses_opaque_snapshot_continuation(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            now = [2_000_000_000]
            with SnapshotModule.open(
                Path(temporary) / "snapshots.sqlite3", now=lambda: now[0]
            ) as module:
                first = module.create_snapshot(capture(b"first"))
                now[0] += 1
                second = module.create_snapshot(capture(b"second"))
                first_page = module.find_snapshots(FindSnapshotsRequest(limit=1))
                self.assertEqual(first_page.snapshots, (first,))
                self.assertEqual(first_page.continuation, first.snapshot)
                second_page = module.find_snapshots(
                    FindSnapshotsRequest(after=first_page.continuation, limit=1)
                )
                self.assertEqual(second_page.snapshots, (second,))
                self.assertIsNone(second_page.continuation)

    @staticmethod
    def _expect(code: str, operation) -> None:  # type: ignore[no-untyped-def]
        with unittest.TestCase().assertRaises(SnapshotError) as raised:
            operation()
        if raised.exception.failure.code != code:
            raise AssertionError(
                f"expected {code}, observed {raised.exception.failure.code}"
            )


if __name__ == "__main__":
    unittest.main()
