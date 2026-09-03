from __future__ import annotations

import time
import uuid
from collections.abc import Callable
from pathlib import Path

from tools.standards_identity.standards_identity import (
    frame_path_byte_set,
    hash_identity,
)

from .errors import invalid
from .model import (
    AdvanceAggregateRootResult,
    AggregateRecord,
    AggregateRoot,
    AggregateRootPage,
    CapturedContent,
    ChildHandle,
    DeleteSnapshotResult,
    FindSnapshotsRequest,
    FindAggregateRootsRequest,
    PutResult,
    SnapshotId,
    SnapshotPage,
    SnapshotSummary,
)
from .store import SQLiteSnapshotStore

DEFAULT_QUARANTINE_SECONDS = 7 * 24 * 60 * 60


class SnapshotModule:
    def __init__(
        self,
        store: SQLiteSnapshotStore,
        *,
        now: Callable[[], int] | None = None,
        snapshot_id_factory: Callable[[], SnapshotId] | None = None,
        quarantine_seconds: int = DEFAULT_QUARANTINE_SECONDS,
    ) -> None:
        if type(quarantine_seconds) is not int or quarantine_seconds < 1:
            raise invalid(
                "SNAPSHOT.INVALID_QUARANTINE_DURATION",
                "quarantine duration must be a positive integer",
            )
        self._store = store
        self._now = now or (lambda: int(time.time()))
        self._snapshot_id_factory = snapshot_id_factory or (
            lambda: SnapshotId.from_uuid(uuid.uuid4())
        )
        self._quarantine_seconds = quarantine_seconds
        self.maintain()

    @classmethod
    def open(
        cls,
        path: Path,
        *,
        now: Callable[[], int] | None = None,
        snapshot_id_factory: Callable[[], SnapshotId] | None = None,
        quarantine_seconds: int = DEFAULT_QUARANTINE_SECONDS,
    ) -> SnapshotModule:
        store = SQLiteSnapshotStore(path)
        try:
            return cls(
                store,
                now=now,
                snapshot_id_factory=snapshot_id_factory,
                quarantine_seconds=quarantine_seconds,
            )
        except Exception:
            store.close()
            raise

    def close(self) -> None:
        self._store.close()

    def __enter__(self) -> SnapshotModule:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def create_snapshot(self, capture: CapturedContent) -> SnapshotSummary:
        selected = self._snapshot_id_factory()
        if type(selected) is not SnapshotId:
            raise invalid(
                "SNAPSHOT.INVALID_ID_FACTORY",
                "snapshot ID factory must return an exact SnapshotId",
            )
        return self._store.publish_snapshot(
            selected, self._content_id(capture), capture, self._time()
        )

    def snapshot(
        self, snapshot: SnapshotId, *, include_quarantined: bool = False
    ) -> SnapshotSummary:
        self.maintain()
        return self._store.snapshot(snapshot, include_quarantined=include_quarantined)

    def find_snapshots(self, request: FindSnapshotsRequest) -> SnapshotPage:
        self.maintain()
        return self._store.find(request)

    def load_content(self, snapshot: SnapshotId) -> CapturedContent:
        self.maintain()
        content_id, capture = self._store.load_content(snapshot)
        if self._content_id(capture) != content_id:
            raise invalid(
                "SNAPSHOT.CONTENT_ID_MISMATCH",
                "stored path and byte material does not match its content ID",
            )
        return capture

    def delete_snapshot(self, snapshot: SnapshotId) -> DeleteSnapshotResult:
        self.maintain()
        return self._store.delete(
            snapshot,
            now=self._time(),
            quarantine_seconds=self._quarantine_seconds,
        )

    def undelete_snapshot(self, snapshot: SnapshotId) -> SnapshotSummary:
        self.maintain()
        return self._store.undelete(snapshot)

    def publish_aggregate(self, record: AggregateRecord) -> PutResult:
        self.maintain()
        return self._store.publish_aggregate(record)

    def create_aggregate_root(self, root: AggregateRoot, head: AggregateRecord) -> None:
        self.maintain()
        self._store.create_aggregate_root(root, head)

    def find_aggregate_roots(
        self, request: FindAggregateRootsRequest
    ) -> AggregateRootPage:
        self.maintain()
        return self._store.find_aggregate_roots(request)

    def load_aggregate_root(self, aggregate_id: str) -> AggregateRoot:
        self.maintain()
        return self._store.load_aggregate_root(aggregate_id)

    def advance_aggregate_root(
        self,
        aggregate_id: str,
        expected_head_id: str,
        head: AggregateRecord,
    ) -> AdvanceAggregateRootResult:
        self.maintain()
        return self._store.advance_aggregate_root(aggregate_id, expected_head_id, head)

    def load_aggregate(self, aggregate_id: str) -> AggregateRecord:
        self.maintain()
        return self._store.load_aggregate(aggregate_id)

    def inspect_child(self, handle: ChildHandle) -> bytes:
        self.maintain()
        return self._store.inspect_child(
            handle.aggregate_id, handle.kind, handle.child_id
        )

    def maintain(self) -> None:
        self._store.purge_expired(self._time())

    def _time(self) -> int:
        observed = self._now()
        if type(observed) is not int or observed < 0:
            raise invalid(
                "SNAPSHOT.INVALID_TIME", "clock must return a nonnegative integer"
            )
        return observed

    @staticmethod
    def _content_id(capture: CapturedContent) -> str:
        material = frame_path_byte_set(
            (item.path.components, item.content) for item in capture.files
        )
        return hash_identity(
            "coding-standards:snapshot-content:v1", "snapshot-content", material
        )


__all__ = ("DEFAULT_QUARANTINE_SECONDS", "SnapshotModule")
