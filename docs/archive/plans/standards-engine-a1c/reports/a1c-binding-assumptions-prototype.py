#!/usr/bin/env python3
"""Disposable probes for the remaining A1c binding assumptions.

This is executable design evidence, not production code. It tests the proposed
content-source protocol, aggregate lifecycle, and eight-operation workflow
without changing the accepted A1b runtime.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


class ProbeFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def expect_failure(code: str, operation: Callable[[], object]) -> None:
    try:
        operation()
    except ProbeFailure as error:
        if error.code != code:
            raise AssertionError(f"expected {code}, observed {error.code}") from error
        return
    raise AssertionError(f"expected {code}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def normalize_path(value: str) -> str:
    if "\\" in value:
        raise ProbeFailure("CONTENT.INVALID_PATH")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise ProbeFailure("CONTENT.INVALID_PATH")
    return path.as_posix()


class RecordingContentSource:
    """Exact logical-path reads with no filesystem or semantic knowledge."""

    def __init__(self, entries: Iterable[tuple[str, bytes]]) -> None:
        self._entries: dict[str, bytes] = {}
        self.requested: list[str] = []
        for raw_path, raw_content in entries:
            path = normalize_path(raw_path)
            content = bytes(raw_content)
            previous = self._entries.get(path)
            if previous is not None and previous != content:
                raise ProbeFailure("CONTENT.CONTRADICTORY_PATH")
            self._entries[path] = content

    def read_bytes(self, raw_path: str) -> bytes:
        path = normalize_path(raw_path)
        self.requested.append(path)
        try:
            return self._entries[path]
        except KeyError as error:
            raise ProbeFailure("CONTENT.UNAVAILABLE") from error

    def captured(self) -> dict[str, bytes]:
        return {path: self._entries[path] for path in sorted(set(self.requested))}


def load_document(source: RecordingContentSource, path: str) -> dict[str, Any]:
    try:
        document = json.loads(source.read_bytes(path))
    except json.JSONDecodeError as error:
        raise ProbeFailure("CONTENT.INVALID_DOCUMENT") from error
    if not isinstance(document, dict):
        raise ProbeFailure("CONTENT.INVALID_DOCUMENT")
    return document


def compile_roots(
    source: RecordingContentSource,
    roots: tuple[str, ...],
    *,
    extra_read: str | None = None,
) -> str:
    """Representative typed loaders own references; capture only records reads."""

    queue = list(roots)
    loaded: dict[str, dict[str, Any]] = {}
    while queue:
        path = normalize_path(queue.pop(0))
        if path in loaded:
            continue
        document = load_document(source, path)
        references = document.get("references", [])
        if not isinstance(references, list) or not all(
            isinstance(item, str) for item in references
        ):
            raise ProbeFailure("CONTENT.INVALID_REFERENCES")
        loaded[path] = document
        queue.extend(references)
    if extra_read is not None:
        source.read_bytes(extra_read)
    return digest([[path, loaded[path]] for path in sorted(loaded)])


@dataclass(frozen=True, slots=True)
class CaptureResult:
    files: Mapping[str, bytes]
    semantic_digest: str


def capture_and_replay(
    repository: RecordingContentSource, roots: tuple[str, ...]
) -> CaptureResult:
    first_digest = compile_roots(repository, roots)
    captured = repository.captured()
    replay = RecordingContentSource(captured.items())
    replay_digest = compile_roots(replay, roots)
    if set(replay.requested) != set(captured) or replay_digest != first_digest:
        raise ProbeFailure("CAPTURE.NONDETERMINISTIC_CLOSURE")
    return CaptureResult(captured, first_digest)


class SequenceIds:
    def __init__(self, prefix: str, start: int = 1) -> None:
        self._prefix = prefix
        self._next = start

    def __call__(self) -> str:
        value = f"{self._prefix}:v1:{self._next:04d}"
        self._next += 1
        return value


class AggregateStore:
    """Disposable relational model of A1c lifecycle ownership."""

    def __init__(
        self,
        database: Path,
        now: Callable[[], int],
        snapshot_ids: Callable[[], str],
        analysis_ids: Callable[[], str],
        purge_probe: Callable[[str], None] | None = None,
    ) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._now = now
        self._snapshot_ids = snapshot_ids
        self._analysis_ids = analysis_ids
        self._purge_probe = purge_probe
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS content_sets (
                content_id TEXT PRIMARY KEY
            ) STRICT;
            CREATE TABLE IF NOT EXISTS content_files (
                content_id TEXT NOT NULL REFERENCES content_sets(content_id)
                    ON DELETE CASCADE,
                logical_path TEXT NOT NULL,
                raw_bytes BLOB NOT NULL,
                PRIMARY KEY (content_id, logical_path)
            ) STRICT;
            CREATE TABLE IF NOT EXISTS snapshot_roots (
                snapshot_id TEXT PRIMARY KEY,
                content_id TEXT NOT NULL REFERENCES content_sets(content_id),
                source_commit TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                lifecycle TEXT NOT NULL CHECK (lifecycle IN ('active', 'quarantined')),
                purge_deadline INTEGER,
                CHECK ((lifecycle = 'active' AND purge_deadline IS NULL) OR
                       (lifecycle = 'quarantined' AND purge_deadline IS NOT NULL))
            ) STRICT;
            CREATE TABLE IF NOT EXISTS analysis_states (
                analysis_id TEXT PRIMARY KEY,
                payload BLOB NOT NULL
            ) STRICT;
            CREATE TABLE IF NOT EXISTS analysis_snapshot_dependencies (
                analysis_id TEXT NOT NULL REFERENCES analysis_states(analysis_id)
                    ON DELETE CASCADE,
                snapshot_id TEXT NOT NULL REFERENCES snapshot_roots(snapshot_id)
                    ON DELETE CASCADE,
                PRIMARY KEY (analysis_id, snapshot_id)
            ) STRICT;
            CREATE TABLE IF NOT EXISTS child_index (
                child_id TEXT PRIMARY KEY,
                analysis_id TEXT NOT NULL REFERENCES analysis_states(analysis_id)
                    ON DELETE CASCADE,
                payload BLOB NOT NULL
            ) STRICT;
            CREATE TABLE IF NOT EXISTS purged_root_tombstones (
                snapshot_id TEXT PRIMARY KEY,
                purged_at INTEGER NOT NULL
            ) STRICT;
            CREATE TRIGGER IF NOT EXISTS delete_root_analysis
            BEFORE DELETE ON snapshot_roots
            BEGIN
                DELETE FROM analysis_states WHERE analysis_id IN (
                    SELECT analysis_id FROM analysis_snapshot_dependencies
                    WHERE snapshot_id = OLD.snapshot_id
                );
            END;
            """
        )
        self.maintain()

    def close(self) -> None:
        self._connection.close()

    def create_snapshot(
        self, files: Mapping[str, bytes], source_commit: str
    ) -> dict[str, object]:
        material = [
            [normalize_path(path), bytes(files[path]).hex()] for path in sorted(files)
        ]
        content_id = (
            "content:v1:" + hashlib.sha256(canonical_bytes(material)).hexdigest()
        )
        snapshot_id = self._snapshot_ids()
        created_at = self._now()
        try:
            with self._connection:
                self._connection.execute(
                    "INSERT OR IGNORE INTO content_sets VALUES (?)", (content_id,)
                )
                for path in sorted(files):
                    normalized = normalize_path(path)
                    row = self._connection.execute(
                        "SELECT raw_bytes FROM content_files WHERE content_id = ? AND logical_path = ?",
                        (content_id, normalized),
                    ).fetchone()
                    if row is None:
                        self._connection.execute(
                            "INSERT INTO content_files VALUES (?, ?, ?)",
                            (content_id, normalized, bytes(files[path])),
                        )
                    elif bytes(row[0]) != bytes(files[path]):
                        raise ProbeFailure("SNAPSHOT.CONTENT_CONTRADICTION")
                self._connection.execute(
                    "INSERT INTO snapshot_roots VALUES (?, ?, ?, ?, 'active', NULL)",
                    (snapshot_id, content_id, source_commit, created_at),
                )
        except sqlite3.IntegrityError as error:
            raise ProbeFailure("SNAPSHOT.ID_COLLISION") from error
        return self.snapshot_summary(snapshot_id)

    def find_snapshots(
        self, lifecycle: str = "active", after: str | None = None, limit: int = 50
    ) -> tuple[dict[str, object], ...]:
        self.maintain()
        if (
            lifecycle not in ("active", "quarantined")
            or type(limit) is not int
            or limit < 1
        ):
            raise ProbeFailure("SNAPSHOT.INVALID_DISCOVERY")
        if after is None:
            rows = self._connection.execute(
                """
                SELECT snapshot_id FROM snapshot_roots
                WHERE lifecycle = ?
                ORDER BY created_at, snapshot_id LIMIT ?
                """,
                (lifecycle, limit),
            ).fetchall()
        else:
            cursor = self._connection.execute(
                "SELECT created_at, snapshot_id FROM snapshot_roots WHERE snapshot_id = ?",
                (after,),
            ).fetchone()
            if cursor is None:
                raise ProbeFailure("SNAPSHOT.INVALID_CONTINUATION")
            rows = self._connection.execute(
                """
                SELECT snapshot_id FROM snapshot_roots
                WHERE lifecycle = ?
                  AND (created_at > ? OR (created_at = ? AND snapshot_id > ?))
                ORDER BY created_at, snapshot_id LIMIT ?
                """,
                (lifecycle, cursor[0], cursor[0], cursor[1], limit),
            ).fetchall()
        return tuple(self.snapshot_summary(str(row[0])) for row in rows)

    def delete_snapshot(self, snapshot_id: str) -> dict[str, object]:
        self.maintain()
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        if row[1] == "quarantined":
            deadline = int(row[2])
        else:
            deadline = self._now() + 7 * 24 * 60 * 60
            with self._connection:
                self._connection.execute(
                    "UPDATE snapshot_roots SET lifecycle = 'quarantined', purge_deadline = ? WHERE snapshot_id = ?",
                    (deadline, snapshot_id),
                )
        return {
            "kind": "delete-snapshot-result",
            "snapshot": snapshot_id,
            "purge_deadline": deadline,
        }

    def undelete_snapshot(self, snapshot_id: str) -> dict[str, object]:
        self.maintain()
        if self._root(snapshot_id) is None:
            self._raise_missing(snapshot_id)
        with self._connection:
            self._connection.execute(
                "UPDATE snapshot_roots SET lifecycle = 'active', purge_deadline = NULL WHERE snapshot_id = ?",
                (snapshot_id,),
            )
        return {
            "kind": "undelete-snapshot-result",
            "snapshot": snapshot_id,
            "lifecycle": "active",
        }

    def store_analysis(
        self,
        snapshots: tuple[str, ...],
        decisions: Mapping[str, object],
        children: Mapping[str, object],
    ) -> str:
        for snapshot in snapshots:
            self.require_active(snapshot)
        analysis_id = self._analysis_ids()
        payload = canonical_bytes(
            {"snapshots": sorted(snapshots), "decisions": decisions}
        )
        with self._connection:
            self._connection.execute(
                "INSERT INTO analysis_states VALUES (?, ?)", (analysis_id, payload)
            )
            for snapshot in sorted(set(snapshots)):
                self._connection.execute(
                    "INSERT INTO analysis_snapshot_dependencies VALUES (?, ?)",
                    (analysis_id, snapshot),
                )
            for child_id in sorted(children):
                self._connection.execute(
                    "INSERT INTO child_index VALUES (?, ?, ?)",
                    (child_id, analysis_id, canonical_bytes(children[child_id])),
                )
        return analysis_id

    def load_analysis(self, analysis_id: str) -> dict[str, object]:
        row = self._connection.execute(
            "SELECT payload FROM analysis_states WHERE analysis_id = ?", (analysis_id,)
        ).fetchone()
        if row is None:
            raise ProbeFailure("ANALYSIS.UNAVAILABLE")
        dependencies = tuple(
            str(item[0])
            for item in self._connection.execute(
                "SELECT snapshot_id FROM analysis_snapshot_dependencies WHERE analysis_id = ? ORDER BY snapshot_id",
                (analysis_id,),
            ).fetchall()
        )
        for snapshot in dependencies:
            self.require_active(snapshot)
        return json.loads(bytes(row[0]))

    def inspect_child(self, child_id: str) -> object:
        row = self._connection.execute(
            "SELECT analysis_id, payload FROM child_index WHERE child_id = ?",
            (child_id,),
        ).fetchone()
        if row is None:
            raise ProbeFailure("INSPECTION.UNAVAILABLE")
        self.load_analysis(str(row[0]))
        return json.loads(bytes(row[1]))

    def require_active(self, snapshot_id: str) -> None:
        self.maintain()
        row = self._root(snapshot_id)
        if row is None:
            self._raise_missing(snapshot_id)
        if row[1] == "quarantined":
            raise ProbeFailure("SNAPSHOT.QUARANTINED")

    def snapshot_summary(self, snapshot_id: str) -> dict[str, object]:
        row = self._connection.execute(
            "SELECT source_commit, created_at, lifecycle, purge_deadline FROM snapshot_roots WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            self._raise_missing(snapshot_id)
        return {
            "kind": "snapshot-summary",
            "snapshot": snapshot_id,
            "source_commit": row[0],
            "created_at": row[1],
            "lifecycle": row[2],
            "purge_deadline": row[3],
        }

    def maintain(self) -> None:
        expired = self._connection.execute(
            "SELECT snapshot_id, content_id FROM snapshot_roots WHERE lifecycle = 'quarantined' AND purge_deadline <= ? ORDER BY snapshot_id",
            (self._now(),),
        ).fetchall()
        if not expired:
            return
        with self._connection:
            for snapshot_id, content_id in expired:
                self._connection.execute(
                    "INSERT INTO purged_root_tombstones VALUES (?, ?)",
                    (snapshot_id, self._now()),
                )
                self._connection.execute(
                    "DELETE FROM snapshot_roots WHERE snapshot_id = ?", (snapshot_id,)
                )
                if self._purge_probe is not None:
                    self._purge_probe(str(snapshot_id))
                self._connection.execute(
                    "DELETE FROM content_sets WHERE content_id = ? AND NOT EXISTS (SELECT 1 FROM snapshot_roots WHERE content_id = ?)",
                    (content_id, content_id),
                )

    def counts(self) -> dict[str, int]:
        tables = (
            "content_sets",
            "content_files",
            "snapshot_roots",
            "analysis_states",
            "analysis_snapshot_dependencies",
            "child_index",
            "purged_root_tombstones",
        )
        return {
            table: int(
                self._connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            )
            for table in tables
        }

    def _root(self, snapshot_id: str) -> tuple[object, ...] | None:
        return self._connection.execute(
            "SELECT snapshot_id, lifecycle, purge_deadline FROM snapshot_roots WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()

    def _raise_missing(self, snapshot_id: str) -> None:
        tombstone = self._connection.execute(
            "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = ?", (snapshot_id,)
        ).fetchone()
        raise ProbeFailure("SNAPSHOT.EXPIRED" if tombstone else "SNAPSHOT.UNAVAILABLE")


PUBLIC_RESULT_KEYS: dict[str, frozenset[str]] = {
    "create-snapshot-result": frozenset({"kind", "snapshot"}),
    "find-snapshots-result": frozenset({"kind", "snapshots", "continuation"}),
    "delete-snapshot-result": frozenset({"kind", "snapshot", "purge_deadline"}),
    "undelete-snapshot-result": frozenset({"kind", "snapshot", "lifecycle"}),
    "navigation-result": frozenset({"kind", "snapshot", "target"}),
    "pending-result": frozenset({"kind", "analysis", "work", "next"}),
    "complete-result": frozenset({"kind", "analysis", "decisions"}),
    "inspection-result": frozenset({"kind", "handle", "value"}),
}


def validate_public_result(value: Mapping[str, object]) -> None:
    kind = value.get("kind")
    if not isinstance(kind, str) or frozenset(value) != PUBLIC_RESULT_KEYS.get(kind):
        raise ProbeFailure("INTERFACE.INVALID_PROJECTION")


class Facade:
    def __init__(self, store: AggregateStore, capture: CaptureResult) -> None:
        self._store = store
        self._capture = capture

    def create_snapshot(self) -> dict[str, object]:
        summary = self._store.create_snapshot(self._capture.files, "commit-current")
        return self._result(
            {"kind": "create-snapshot-result", "snapshot": summary["snapshot"]}
        )

    def find_snapshots(
        self, after: str | None = None, limit: int = 50
    ) -> dict[str, object]:
        rows = self._store.find_snapshots(after=after, limit=limit)
        continuation = rows[-1]["snapshot"] if len(rows) == limit else None
        return self._result(
            {
                "kind": "find-snapshots-result",
                "snapshots": [row["snapshot"] for row in rows],
                "continuation": continuation,
            }
        )

    def delete_snapshot(self, snapshot: str) -> dict[str, object]:
        return self._result(self._store.delete_snapshot(snapshot))

    def undelete_snapshot(self, snapshot: str) -> dict[str, object]:
        return self._result(self._store.undelete_snapshot(snapshot))

    def query(self, snapshot: str, target: str) -> dict[str, object]:
        self._store.require_active(snapshot)
        return self._result(
            {"kind": "navigation-result", "snapshot": snapshot, "target": target}
        )

    def prepare(self, snapshot: str) -> dict[str, object]:
        analysis = self._store.store_analysis(
            (snapshot,), {}, {"requirement:v1:fact-a": {"fact": "fact-a"}}
        )
        return self._result(
            {
                "kind": "pending-result",
                "analysis": analysis,
                "work": ["requirement:v1:fact-a"],
                "next": ["provide-fact"],
            }
        )

    def resolve(self, analysis: str, decision: object) -> dict[str, object]:
        state = self._store.load_analysis(analysis)
        child = self._store.store_analysis(
            tuple(state["snapshots"]), {"fact-a": decision}, {}
        )
        return self._result(
            {
                "kind": "complete-result",
                "analysis": child,
                "decisions": {"fact-a": decision},
            }
        )

    def inspect(self, handle: str) -> dict[str, object]:
        if handle.startswith("analysis:"):
            value = self._store.load_analysis(handle)
        elif handle.startswith("requirement:"):
            value = self._store.inspect_child(handle)
        elif handle.startswith("snapshot:"):
            self._store.require_active(handle)
            value = self._store.snapshot_summary(handle)
        else:
            raise ProbeFailure("INSPECTION.UNSUPPORTED_HANDLE")
        return self._result(
            {"kind": "inspection-result", "handle": handle, "value": value}
        )

    @staticmethod
    def _result(value: dict[str, object]) -> dict[str, object]:
        validate_public_result(value)
        forbidden = {
            "content_id",
            "git_revision",
            "database_path",
            "project",
            "children",
        }
        if forbidden.intersection(value):
            raise ProbeFailure("INTERFACE.LEAKED_INTERNAL_AUTHORITY")
        return value


def probe_capture() -> dict[str, object]:
    entries = [
        (
            "roots/modules.json",
            canonical_bytes(
                {"references": ["modules/core.json", "registries/policy-units.json"]}
            ),
        ),
        (
            "modules/core.json",
            canonical_bytes({"references": ["standards/core.md"], "id": "core"}),
        ),
        (
            "standards/core.md",
            canonical_bytes({"references": [], "content": "normative bytes"}),
        ),
        (
            "registries/policy-units.json",
            canonical_bytes({"references": ["units/core.json"]}),
        ),
        ("units/core.json", canonical_bytes({"references": [], "id": "core.boundary"})),
        ("unrelated.txt", b"not requested"),
    ]
    source = RecordingContentSource(entries)
    capture = capture_and_replay(source, ("roots/modules.json",))
    assert "unrelated.txt" not in capture.files
    assert set(capture.files) == {
        "roots/modules.json",
        "modules/core.json",
        "standards/core.md",
        "registries/policy-units.json",
        "units/core.json",
    }

    expanded_entries = entries + [
        ("contracts/interface.json", canonical_bytes({"references": [], "version": 12}))
    ]
    expanded_entries[0] = (
        "roots/modules.json",
        canonical_bytes(
            {
                "references": [
                    "modules/core.json",
                    "registries/policy-units.json",
                    "contracts/interface.json",
                ]
            }
        ),
    )
    expanded = capture_and_replay(
        RecordingContentSource(expanded_entries), ("roots/modules.json",)
    )
    assert set(expanded.files) == set(capture.files) | {"contracts/interface.json"}
    assert expanded.semantic_digest != capture.semantic_digest

    expect_failure("CONTENT.INVALID_PATH", lambda: source.read_bytes("/etc/passwd"))
    expect_failure("CONTENT.INVALID_PATH", lambda: source.read_bytes("../outside"))
    expect_failure("CONTENT.UNAVAILABLE", lambda: source.read_bytes("missing.json"))
    expect_failure(
        "CONTENT.CONTRADICTORY_PATH",
        lambda: RecordingContentSource((("same", b"a"), ("same", b"b"))),
    )
    replay = RecordingContentSource(capture.files.items())
    expect_failure(
        "CONTENT.UNAVAILABLE",
        lambda: compile_roots(
            replay, ("roots/modules.json",), extra_read="ambient/extra.json"
        ),
    )
    return {
        "case": "traced-roots-only-capture",
        "status": "confirmed-with-production-parity-gate",
        "captured_paths": sorted(capture.files),
        "automatic_expansion": "contracts/interface.json",
        "semantic_digest_changed": True,
        "negative_cases": [
            "escaped-path",
            "missing-reference",
            "contradictory-path",
            "undeclared-replay-read",
        ],
    }


def probe_store_and_facade(
    capture: CaptureResult,
) -> tuple[dict[str, object], dict[str, object]]:
    now = [2_000_000_000]

    def clock() -> int:
        return now[0]

    with tempfile.TemporaryDirectory(prefix="a1c-binding-probe-") as temporary:
        database = Path(temporary) / "snapshot.sqlite3"
        store = AggregateStore(
            database, clock, SequenceIds("snapshot"), SequenceIds("analysis")
        )
        facade = Facade(store, capture)
        first = facade.create_snapshot()["snapshot"]
        second = facade.create_snapshot()["snapshot"]
        assert isinstance(first, str) and isinstance(second, str) and first != second
        assert store.counts()["content_sets"] == 1
        analysis_first = store.store_analysis(
            (first,), {"a": True}, {"child:first": {"value": 1}}
        )
        analysis_both = store.store_analysis(
            (first, second), {"b": True}, {"child:both": {"value": 2}}
        )
        analysis_second = store.store_analysis(
            (second,), {"c": True}, {"child:second": {"value": 3}}
        )
        deadline = facade.delete_snapshot(first)["purge_deadline"]
        assert facade.delete_snapshot(first)["purge_deadline"] == deadline
        expect_failure(
            "SNAPSHOT.QUARANTINED", lambda: store.load_analysis(analysis_first)
        )
        expect_failure(
            "SNAPSHOT.QUARANTINED", lambda: store.load_analysis(analysis_both)
        )
        assert store.load_analysis(analysis_second)["decisions"] == {"c": True}
        facade.undelete_snapshot(first)
        assert store.inspect_child("child:both") == {"value": 2}

        pending = facade.prepare(first)
        pending_handle = str(pending["analysis"])
        requirement = str(pending["work"][0])
        store.close()

        reopened = AggregateStore(
            database, clock, SequenceIds("unused"), SequenceIds("analysis", 100)
        )
        reopened_facade = Facade(reopened, capture)
        assert reopened_facade.inspect(pending_handle)["handle"] == pending_handle
        assert reopened_facade.inspect(requirement)["value"] == {"fact": "fact-a"}
        complete = reopened_facade.resolve(pending_handle, True)
        assert reopened_facade.inspect(str(complete["analysis"]))["value"][
            "decisions"
        ] == {"fact-a": True}
        assert reopened_facade.find_snapshots(limit=1)["continuation"] == first
        assert reopened_facade.find_snapshots(after=first)["snapshots"] == [second]

        reopened_facade.delete_snapshot(first)
        expect_failure(
            "SNAPSHOT.QUARANTINED", lambda: reopened_facade.query(first, "core")
        )
        expect_failure(
            "SNAPSHOT.QUARANTINED", lambda: reopened_facade.inspect(pending_handle)
        )
        reopened_facade.undelete_snapshot(first)
        assert reopened_facade.query(first, "core")["target"] == "core"

        reopened_facade.delete_snapshot(first)
        now[0] += 7 * 24 * 60 * 60
        reopened.maintain()
        counts_after_first_purge = reopened.counts()
        expect_failure("SNAPSHOT.EXPIRED", lambda: reopened_facade.query(first, "core"))
        expect_failure(
            "ANALYSIS.UNAVAILABLE", lambda: reopened.load_analysis(analysis_both)
        )
        assert reopened.load_analysis(analysis_second)["decisions"] == {"c": True}
        assert counts_after_first_purge["content_sets"] == 1
        assert counts_after_first_purge["child_index"] == 1
        reopened_facade.delete_snapshot(second)
        now[0] += 7 * 24 * 60 * 60
        reopened.maintain()
        final_counts = reopened.counts()
        assert final_counts["content_sets"] == 0
        assert final_counts["analysis_states"] == 0
        assert final_counts["analysis_snapshot_dependencies"] == 0
        assert final_counts["child_index"] == 0
        reopened.close()

        collision = AggregateStore(
            database, clock, lambda: "snapshot:v1:collision", SequenceIds("analysis")
        )
        collision.create_snapshot(capture.files, "commit-current")
        expect_failure(
            "SNAPSHOT.ID_COLLISION",
            lambda: collision.create_snapshot(capture.files, "commit-current"),
        )
        collision.close()

        rollback_database = Path(temporary) / "rollback.sqlite3"
        rollback_ids = SequenceIds("snapshot-rollback")
        interrupted = AggregateStore(
            rollback_database,
            clock,
            rollback_ids,
            SequenceIds("analysis-rollback"),
            purge_probe=lambda _snapshot: (_ for _ in ()).throw(
                RuntimeError("interrupt")
            ),
        )
        rollback_root = interrupted.create_snapshot(capture.files, "commit-current")[
            "snapshot"
        ]
        interrupted.delete_snapshot(str(rollback_root))
        now[0] += 7 * 24 * 60 * 60
        try:
            interrupted.maintain()
        except RuntimeError:
            pass
        else:
            raise AssertionError("expected interrupted purge")
        rollback_counts = interrupted.counts()
        assert rollback_counts["snapshot_roots"] == 1
        assert rollback_counts["purged_root_tombstones"] == 0
        interrupted.close()

    return (
        {
            "case": "sqlite-aggregate-lifecycle",
            "status": "confirmed-with-required-platform-gate",
            "multi_root_cascade": True,
            "shared_content_retained_until_last_root": True,
            "cold_reconstruction": True,
            "interrupted_purge_rolled_back": True,
            "root_collision_rejected": True,
            "final_counts": final_counts,
        },
        {
            "case": "eight-operation-workflows",
            "status": "confirmed-with-generated-contract-gate",
            "operations": [
                "create_snapshot",
                "find_snapshots",
                "delete_snapshot",
                "undelete_snapshot",
                "query",
                "prepare",
                "resolve",
                "inspect",
            ],
            "cold_coordinator_subagent_handoff": True,
            "fresh_agent_discovery": True,
            "quarantine_and_expiry_are_typed": True,
            "public_internal_leaks": [],
        },
    )


def run() -> dict[str, object]:
    capture_case = probe_capture()
    source = RecordingContentSource(
        (
            ("root.json", canonical_bytes({"references": ["core.json"]})),
            ("core.json", canonical_bytes({"references": [], "id": "core"})),
        )
    )
    capture = capture_and_replay(source, ("root.json",))
    store_case, facade_case = probe_store_and_facade(capture)
    return {
        "kind": "a1c-binding-assumptions-prototype",
        "result": "confirmed-with-production-gates",
        "cases": [capture_case, store_case, facade_case],
        "limits": [
            "representative loaders, not production loader parity",
            "local SQLite, not required-real platform evidence",
            "prototype result shapes, not generated v12 contract evidence",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
