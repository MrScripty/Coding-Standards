#!/usr/bin/env python3
"""Disposable A1c snapshot-aggregate design probe.

This executable report is not production code. It exercises the selected
product workflows against a temporary SQLite model and exits nonzero when a
required state transition or ownership invariant fails.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import sqlite3
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

DAY_SECONDS = 24 * 60 * 60
DEFAULT_QUARANTINE_SECONDS = 7 * DAY_SECONDS


class SnapshotFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class Capture:
    source_commit: str
    canonical_bytes: bytes


class CanonicalSource:
    """Internal Adapter: callers cannot select a revision or raw bytes."""

    def __init__(self, capture: Capture) -> None:
        self.capture = capture
        self.available = True
        self.calls = 0

    def current(self) -> Capture:
        self.calls += 1
        if not self.available:
            raise SnapshotFailure("CANONICAL.UNAVAILABLE")
        return self.capture


class SequenceIds:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.next_value = 1

    def __call__(self) -> str:
        value = f"{self.prefix}:{self.next_value:04d}"
        self.next_value += 1
        return value


@dataclass(frozen=True, slots=True)
class SnapshotSummary:
    handle: str
    lifecycle: Literal["active", "quarantined"]
    source_commit: str
    content_id: str
    created_at: int
    purge_deadline: int | None


@dataclass(frozen=True, slots=True)
class ChildHandle:
    snapshot: str
    child: str


class SnapshotModule:
    """Candidate deep Module shared by both public Interface alternatives."""

    def __init__(
        self,
        database: Path,
        source: CanonicalSource,
        now: Callable[[], int],
        snapshot_ids: Callable[[], str],
        *,
        quarantine_seconds: int = DEFAULT_QUARANTINE_SECONDS,
    ) -> None:
        if type(quarantine_seconds) is not int or quarantine_seconds <= 0:
            raise SnapshotFailure("CONFIG.INVALID_QUARANTINE_DURATION")
        self._source = source
        self._now = now
        self._snapshot_ids = snapshot_ids
        self._quarantine_seconds = quarantine_seconds
        self._connection = sqlite3.connect(database)
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._create_schema()
        self._maintenance()

    def close(self) -> None:
        self._connection.close()

    def create_snapshot(self) -> SnapshotSummary:
        capture = self._source.current()
        content_id = "content:sha256:" + hashlib.sha256(
            capture.canonical_bytes
        ).hexdigest()
        snapshot_id = self._snapshot_ids()
        created_at = self._now()
        with self._connection:
            existing = self._connection.execute(
                "SELECT canonical_bytes FROM canonical_content WHERE content_id = ?",
                (content_id,),
            ).fetchone()
            if existing is None:
                self._connection.execute(
                    "INSERT INTO canonical_content VALUES (?, ?)",
                    (content_id, capture.canonical_bytes),
                )
            elif bytes(existing[0]) != capture.canonical_bytes:
                raise SnapshotFailure("SNAPSHOT.CONTENT_ID_CONTRADICTION")
            self._connection.execute(
                """
                INSERT INTO snapshot_roots(
                    snapshot_id, content_id, source_commit, created_at,
                    lifecycle, purge_deadline
                ) VALUES (?, ?, ?, ?, 'active', NULL)
                """,
                (snapshot_id, content_id, capture.source_commit, created_at),
            )
        return self._summary(snapshot_id)

    def find_snapshots(
        self, lifecycle: Literal["active", "quarantined"] = "active"
    ) -> tuple[SnapshotSummary, ...]:
        self._maintenance()
        rows = self._connection.execute(
            """
            SELECT snapshot_id FROM snapshot_roots
            WHERE lifecycle = ? ORDER BY created_at, snapshot_id
            """,
            (lifecycle,),
        ).fetchall()
        return tuple(self._summary(str(row[0])) for row in rows)

    def delete_snapshot(self, snapshot_id: str) -> int:
        self._maintenance()
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        lifecycle = str(row[4])
        if lifecycle == "quarantined":
            return int(row[5])
        deadline = self._now() + self._quarantine_seconds
        with self._connection:
            self._connection.execute(
                """
                UPDATE snapshot_roots
                SET lifecycle = 'quarantined', purge_deadline = ?
                WHERE snapshot_id = ? AND lifecycle = 'active'
                """,
                (deadline, snapshot_id),
            )
        return deadline

    def undelete_snapshot(self, snapshot_id: str) -> SnapshotSummary:
        self._maintenance()
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        if str(row[4]) == "active":
            return self._summary(snapshot_id)
        with self._connection:
            self._connection.execute(
                """
                UPDATE snapshot_roots
                SET lifecycle = 'active', purge_deadline = NULL
                WHERE snapshot_id = ?
                """,
                (snapshot_id,),
            )
        return self._summary(snapshot_id)

    def add_analysis(
        self, snapshot_id: str, analysis_id: str, children: dict[str, object]
    ) -> tuple[ChildHandle, ...]:
        self.require_active(snapshot_id)
        payload = json.dumps(
            {"children": children}, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        with self._connection:
            self._connection.execute(
                "INSERT INTO aggregate_records VALUES (?, ?, 'analysis', ?)",
                (snapshot_id, analysis_id, payload),
            )
            for child_id in sorted(children):
                self._connection.execute(
                    "INSERT INTO child_index VALUES (?, ?, ?)",
                    (snapshot_id, child_id, analysis_id),
                )
        return tuple(ChildHandle(snapshot_id, child) for child in sorted(children))

    def inspect_child(self, handle: ChildHandle) -> object:
        self.require_active(handle.snapshot)
        row = self._connection.execute(
            """
            SELECT aggregate_records.payload
            FROM child_index
            JOIN aggregate_records USING (snapshot_id, aggregate_id)
            WHERE child_index.snapshot_id = ? AND child_index.child_id = ?
            """,
            (handle.snapshot, handle.child),
        ).fetchone()
        if row is None:
            raise SnapshotFailure("INSPECTION.UNKNOWN_CHILD")
        payload = json.loads(bytes(row[0]).decode("utf-8"))
        return payload["children"][handle.child]

    def require_active(self, snapshot_id: str) -> SnapshotSummary:
        self._maintenance()
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        if str(row[4]) == "quarantined":
            raise SnapshotFailure("SNAPSHOT.QUARANTINED")
        return self._summary(snapshot_id)

    def state(self) -> dict[str, object]:
        roots = self._connection.execute(
            """
            SELECT snapshot_id, content_id, source_commit, created_at,
                   lifecycle, purge_deadline
            FROM snapshot_roots ORDER BY snapshot_id
            """
        ).fetchall()
        return {
            "content_count": self._count("canonical_content"),
            "snapshot_count": self._count("snapshot_roots"),
            "aggregate_count": self._count("aggregate_records"),
            "child_index_count": self._count("child_index"),
            "tombstone_count": self._count("purged_snapshots"),
            "roots": [
                {
                    "handle": row[0],
                    "content_id": row[1],
                    "source_commit": row[2],
                    "created_at": row[3],
                    "lifecycle": row[4],
                    "purge_deadline": row[5],
                }
                for row in roots
            ],
        }

    def _maintenance(self) -> None:
        expired = self._connection.execute(
            """
            SELECT snapshot_id, content_id FROM snapshot_roots
            WHERE lifecycle = 'quarantined' AND purge_deadline <= ?
            ORDER BY snapshot_id
            """,
            (self._now(),),
        ).fetchall()
        if not expired:
            return
        with self._connection:
            for snapshot_id, content_id in expired:
                self._connection.execute(
                    "INSERT INTO purged_snapshots VALUES (?, ?)",
                    (snapshot_id, self._now()),
                )
                self._connection.execute(
                    "DELETE FROM snapshot_roots WHERE snapshot_id = ?",
                    (snapshot_id,),
                )
                self._connection.execute(
                    """
                    DELETE FROM canonical_content
                    WHERE content_id = ? AND NOT EXISTS (
                        SELECT 1 FROM snapshot_roots WHERE content_id = ?
                    )
                    """,
                    (content_id, content_id),
                )

    def _summary(self, snapshot_id: str) -> SnapshotSummary:
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        return SnapshotSummary(
            handle=str(row[0]),
            content_id=str(row[1]),
            source_commit=str(row[2]),
            created_at=int(row[3]),
            lifecycle=str(row[4]),  # type: ignore[arg-type]
            purge_deadline=None if row[5] is None else int(row[5]),
        )

    def _root(self, snapshot_id: str) -> tuple[object, ...] | None:
        return self._connection.execute(
            """
            SELECT snapshot_id, content_id, source_commit, created_at,
                   lifecycle, purge_deadline
            FROM snapshot_roots WHERE snapshot_id = ?
            """,
            (snapshot_id,),
        ).fetchone()

    def _raise_missing(self, snapshot_id: str) -> None:
        tombstone = self._connection.execute(
            "SELECT 1 FROM purged_snapshots WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()
        if tombstone is not None:
            raise SnapshotFailure("SNAPSHOT.EXPIRED")
        raise SnapshotFailure("SNAPSHOT.UNAVAILABLE")

    def _count(self, table: str) -> int:
        allowed = {
            "canonical_content",
            "snapshot_roots",
            "aggregate_records",
            "child_index",
            "purged_snapshots",
        }
        if table not in allowed:
            raise AssertionError(table)
        return int(self._connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0])

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS canonical_content (
                content_id TEXT PRIMARY KEY,
                canonical_bytes BLOB NOT NULL
            ) STRICT;
            CREATE TABLE IF NOT EXISTS snapshot_roots (
                snapshot_id TEXT PRIMARY KEY,
                content_id TEXT NOT NULL REFERENCES canonical_content(content_id),
                source_commit TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                lifecycle TEXT NOT NULL CHECK (lifecycle IN ('active', 'quarantined')),
                purge_deadline INTEGER,
                CHECK (
                    (lifecycle = 'active' AND purge_deadline IS NULL) OR
                    (lifecycle = 'quarantined' AND purge_deadline IS NOT NULL)
                )
            ) STRICT;
            CREATE TABLE IF NOT EXISTS aggregate_records (
                snapshot_id TEXT NOT NULL REFERENCES snapshot_roots(snapshot_id) ON DELETE CASCADE,
                aggregate_id TEXT NOT NULL,
                aggregate_kind TEXT NOT NULL,
                payload BLOB NOT NULL,
                PRIMARY KEY (snapshot_id, aggregate_id)
            ) STRICT;
            CREATE TABLE IF NOT EXISTS child_index (
                snapshot_id TEXT NOT NULL,
                child_id TEXT NOT NULL,
                aggregate_id TEXT NOT NULL,
                PRIMARY KEY (snapshot_id, child_id),
                FOREIGN KEY (snapshot_id, aggregate_id)
                    REFERENCES aggregate_records(snapshot_id, aggregate_id)
                    ON DELETE CASCADE
            ) STRICT;
            CREATE TABLE IF NOT EXISTS purged_snapshots (
                snapshot_id TEXT PRIMARY KEY,
                purged_at INTEGER NOT NULL
            ) STRICT;
            """
        )


class ExplicitSnapshotInterface:
    def __init__(self, module: SnapshotModule) -> None:
        self._module = module

    def create_snapshot(self) -> SnapshotSummary:
        return self._module.create_snapshot()

    def find_snapshots(
        self, lifecycle: Literal["active", "quarantined"] = "active"
    ) -> tuple[SnapshotSummary, ...]:
        return self._module.find_snapshots(lifecycle)

    def delete_snapshot(self, snapshot: str) -> int:
        return self._module.delete_snapshot(snapshot)

    def undelete_snapshot(self, snapshot: str) -> SnapshotSummary:
        return self._module.undelete_snapshot(snapshot)


class TaggedSnapshotInterface:
    def __init__(self, module: SnapshotModule) -> None:
        self._module = module

    def snapshots(self, request: dict[str, object]) -> object:
        kind = request.get("kind")
        if kind == "create":
            return self._module.create_snapshot()
        if kind == "find":
            return self._module.find_snapshots(str(request.get("lifecycle", "active")))  # type: ignore[arg-type]
        if kind == "delete":
            return self._module.delete_snapshot(str(request["snapshot"]))
        if kind == "undelete":
            return self._module.undelete_snapshot(str(request["snapshot"]))
        raise SnapshotFailure("SNAPSHOT.UNSUPPORTED_REQUEST")


def expect_failure(code: str, action: Callable[[], object]) -> None:
    try:
        action()
    except SnapshotFailure as error:
        if error.code != code:
            raise AssertionError(f"expected {code}, observed {error.code}") from error
        return
    raise AssertionError(f"expected {code}")


def run() -> dict[str, object]:
    now = [2_000_000_000]

    def clock() -> int:
        return now[0]

    source = CanonicalSource(Capture("commit-current", b"canonical standards"))
    ids = SequenceIds("snapshot")
    cases: dict[str, object] = {}

    with tempfile.TemporaryDirectory(prefix="a1c-snapshot-prototype-") as temporary:
        database = Path(temporary) / "PROTOTYPE-snapshot-store.sqlite3"
        module = SnapshotModule(database, source, clock, ids)
        explicit = ExplicitSnapshotInterface(module)

        assert tuple(inspect.signature(explicit.create_snapshot).parameters) == ()
        first = explicit.create_snapshot()
        second = explicit.create_snapshot()
        assert first.handle != second.handle
        assert first.content_id == second.content_id
        assert source.calls == 2
        assert module.state()["content_count"] == 1
        cases["same-content-isolation"] = module.state()

        first_children = module.add_analysis(
            first.handle,
            "analysis:first",
            {"requirement:first": {"fact": "change.requires_review"}},
        )
        second_children = module.add_analysis(
            second.handle,
            "analysis:second",
            {"requirement:second": {"fact": "change.affects_docs"}},
        )
        assert module.inspect_child(first_children[0])["fact"] == "change.requires_review"
        assert module.inspect_child(second_children[0])["fact"] == "change.affects_docs"
        cases["child-inspection"] = module.state()

        deadline = explicit.delete_snapshot(first.handle)
        assert explicit.delete_snapshot(first.handle) == deadline
        assert tuple(item.handle for item in explicit.find_snapshots()) == (second.handle,)
        assert tuple(
            item.handle for item in explicit.find_snapshots("quarantined")
        ) == (first.handle,)
        expect_failure(
            "SNAPSHOT.QUARANTINED", lambda: module.inspect_child(first_children[0])
        )
        assert module.inspect_child(second_children[0])["fact"] == "change.affects_docs"
        cases["quarantined-discovery"] = module.state()

        restored = explicit.undelete_snapshot(first.handle)
        assert restored.lifecycle == "active"
        assert module.inspect_child(first_children[0])["fact"] == "change.requires_review"
        cases["undelete"] = module.state()

        explicit.delete_snapshot(first.handle)
        module.close()
        source.available = False
        reopened = SnapshotModule(database, source, clock, ids)
        assert reopened.inspect_child(second_children[0])["fact"] == "change.affects_docs"
        assert source.calls == 2
        cases["cold-reopen"] = reopened.state()

        now[0] += DEFAULT_QUARANTINE_SECONDS + 1
        assert tuple(item.handle for item in reopened.find_snapshots()) == (second.handle,)
        expect_failure(
            "SNAPSHOT.EXPIRED", lambda: reopened.undelete_snapshot(first.handle)
        )
        state = reopened.state()
        assert state["content_count"] == 1
        assert state["snapshot_count"] == 1
        assert state["aggregate_count"] == 1
        assert state["tombstone_count"] == 1
        cases["expiry-and-shared-content"] = state

        reopened.delete_snapshot(second.handle)
        now[0] += DEFAULT_QUARANTINE_SECONDS + 1
        assert reopened.find_snapshots() == ()
        final_state = reopened.state()
        assert final_state["content_count"] == 0
        assert final_state["snapshot_count"] == 0
        assert final_state["aggregate_count"] == 0
        assert final_state["child_index_count"] == 0
        assert final_state["tombstone_count"] == 2
        cases["transactional-purge"] = final_state
        reopened.close()

        interface_source = CanonicalSource(
            Capture("commit-interface", b"interface comparison")
        )
        explicit_module = SnapshotModule(
            Path(temporary) / "explicit.sqlite3",
            interface_source,
            clock,
            SequenceIds("explicit"),
        )
        tagged_module = SnapshotModule(
            Path(temporary) / "tagged.sqlite3",
            interface_source,
            clock,
            SequenceIds("tagged"),
        )
        explicit_result = ExplicitSnapshotInterface(explicit_module).create_snapshot()
        tagged_result = TaggedSnapshotInterface(tagged_module).snapshots({"kind": "create"})
        assert isinstance(tagged_result, SnapshotSummary)
        assert explicit_result.content_id == tagged_result.content_id
        cases["interface-parity"] = {
            "explicit_public_methods": [
                "create_snapshot",
                "find_snapshots",
                "delete_snapshot",
                "undelete_snapshot",
            ],
            "tagged_public_method": "snapshots",
            "shared_internal_module": "SnapshotModule",
            "behavior_equal": True,
        }
        explicit_module.close()
        tagged_module.close()

        expect_failure(
            "CONFIG.INVALID_QUARANTINE_DURATION",
            lambda: SnapshotModule(
                Path(temporary) / "invalid.sqlite3",
                interface_source,
                clock,
                SequenceIds("invalid"),
                quarantine_seconds=0,
            ),
        )
        cases["invalid-config-rejected"] = True

    return {
        "prototype": "a1c-snapshot-aggregate",
        "status": "pass",
        "cases": cases,
        "limitations": [
            "single-process authorization is represented only by separate methods",
            "canonical bytes are a bounded stand-in for the complete corpus capture",
            "tombstone retention policy remains a design question",
            "Windows and macOS behavior is not proved by this Linux experiment",
            "change-set authoring remains outside A1c",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
