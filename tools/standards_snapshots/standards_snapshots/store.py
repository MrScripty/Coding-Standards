from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

from .errors import SnapshotError, invalid, unavailable, unsupported
from .model import (
    AdvanceAggregateRootResult,
    AggregateChild,
    AggregateRecord,
    AggregateRoot,
    AggregateRootPage,
    CapturedContent,
    DeleteSnapshotResult,
    FindAggregateRootsRequest,
    FindSnapshotsRequest,
    PutResult,
    SnapshotId,
    SnapshotFile,
    SnapshotPage,
    SnapshotPath,
    SnapshotSummary,
)

APPLICATION_ID = 0x43534131
USER_VERSION = 2
BUSY_TIMEOUT_MS = 5_000


def _root_reference(value: object, description: str) -> None:
    if type(value) is not str or not value:
        raise invalid(
            "AGGREGATE.INVALID_ROOT_REFERENCE", f"{description} must be nonempty"
        )
    if "\0" in value or any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise invalid(
            "AGGREGATE.INVALID_ROOT_REFERENCE",
            f"{description} must contain Unicode scalar values without NUL",
        )


_SCHEMA = """
CREATE TABLE content_sets (
    content_id TEXT COLLATE BINARY PRIMARY KEY,
    file_count INTEGER NOT NULL CHECK (file_count > 0)
) STRICT, WITHOUT ROWID;
CREATE TABLE content_files (
    content_id TEXT COLLATE BINARY NOT NULL REFERENCES content_sets(content_id)
        ON DELETE CASCADE,
    logical_path TEXT COLLATE BINARY NOT NULL,
    raw_bytes BLOB NOT NULL,
    byte_length INTEGER NOT NULL CHECK (byte_length >= 0),
    sha256 TEXT COLLATE BINARY NOT NULL,
    PRIMARY KEY (content_id, logical_path),
    CHECK (typeof(raw_bytes) = 'blob'),
    CHECK (length(raw_bytes) = byte_length)
) STRICT, WITHOUT ROWID;
CREATE TABLE snapshot_roots (
    snapshot_id TEXT COLLATE BINARY PRIMARY KEY,
    content_id TEXT COLLATE BINARY NOT NULL REFERENCES content_sets(content_id),
    source_revision TEXT COLLATE BINARY NOT NULL,
    created_at INTEGER NOT NULL CHECK (created_at >= 0),
    lifecycle TEXT COLLATE BINARY NOT NULL
        CHECK (lifecycle IN ('active', 'quarantined')),
    purge_deadline INTEGER,
    CHECK ((lifecycle = 'active' AND purge_deadline IS NULL) OR
           (lifecycle = 'quarantined' AND purge_deadline IS NOT NULL))
) STRICT, WITHOUT ROWID;
CREATE TABLE aggregate_records (
    aggregate_id TEXT COLLATE BINARY PRIMARY KEY,
    aggregate_kind TEXT COLLATE BINARY NOT NULL,
    payload BLOB NOT NULL,
    CHECK (typeof(payload) = 'blob')
) STRICT, WITHOUT ROWID;
CREATE TABLE aggregate_snapshot_dependencies (
    aggregate_id TEXT COLLATE BINARY NOT NULL REFERENCES aggregate_records(aggregate_id)
        ON DELETE CASCADE,
    snapshot_id TEXT COLLATE BINARY NOT NULL REFERENCES snapshot_roots(snapshot_id)
        ON DELETE CASCADE,
    PRIMARY KEY (aggregate_id, snapshot_id)
) STRICT, WITHOUT ROWID;
CREATE TABLE aggregate_roots (
    aggregate_id TEXT COLLATE BINARY PRIMARY KEY,
    aggregate_kind TEXT COLLATE BINARY NOT NULL,
    head_aggregate_id TEXT COLLATE BINARY NOT NULL
        REFERENCES aggregate_records(aggregate_id),
    created_at INTEGER NOT NULL CHECK (created_at >= 0),
    sequence INTEGER NOT NULL UNIQUE CHECK (sequence > 0)
) STRICT, WITHOUT ROWID;
CREATE TABLE aggregate_root_snapshot_dependencies (
    aggregate_id TEXT COLLATE BINARY NOT NULL REFERENCES aggregate_roots(aggregate_id)
        ON DELETE CASCADE,
    snapshot_id TEXT COLLATE BINARY NOT NULL REFERENCES snapshot_roots(snapshot_id)
        ON DELETE CASCADE,
    PRIMARY KEY (aggregate_id, snapshot_id)
) STRICT, WITHOUT ROWID;
CREATE TABLE aggregate_root_tombstones (
    aggregate_id TEXT COLLATE BINARY PRIMARY KEY,
    aggregate_kind TEXT COLLATE BINARY NOT NULL,
    purged_at INTEGER NOT NULL CHECK (purged_at >= 0)
) STRICT, WITHOUT ROWID;
CREATE TABLE child_index (
    aggregate_id TEXT COLLATE BINARY NOT NULL REFERENCES aggregate_records(aggregate_id)
        ON DELETE CASCADE,
    child_kind TEXT COLLATE BINARY NOT NULL,
    child_id TEXT COLLATE BINARY NOT NULL,
    payload BLOB NOT NULL,
    PRIMARY KEY (aggregate_id, child_kind, child_id),
    CHECK (typeof(payload) = 'blob')
) STRICT, WITHOUT ROWID;
CREATE TABLE purged_root_tombstones (
    snapshot_id TEXT COLLATE BINARY PRIMARY KEY,
    purged_at INTEGER NOT NULL CHECK (purged_at >= 0)
) STRICT, WITHOUT ROWID;
CREATE TRIGGER delete_root_aggregate
BEFORE DELETE ON snapshot_roots
BEGIN
    INSERT INTO aggregate_root_tombstones
        SELECT roots.aggregate_id, roots.aggregate_kind, tombstones.purged_at
        FROM aggregate_roots roots
        JOIN aggregate_root_snapshot_dependencies dependencies
            ON dependencies.aggregate_id = roots.aggregate_id
        JOIN purged_root_tombstones tombstones
            ON tombstones.snapshot_id = dependencies.snapshot_id
        WHERE dependencies.snapshot_id = OLD.snapshot_id;
    DELETE FROM aggregate_roots WHERE aggregate_id IN (
        SELECT aggregate_id FROM aggregate_root_snapshot_dependencies
        WHERE snapshot_id = OLD.snapshot_id
    );
    DELETE FROM aggregate_records WHERE aggregate_id IN (
        SELECT aggregate_id FROM aggregate_snapshot_dependencies
        WHERE snapshot_id = OLD.snapshot_id
    );
END;
CREATE TRIGGER content_sets_no_update
BEFORE UPDATE ON content_sets BEGIN
    SELECT RAISE(ABORT, 'content sets are immutable');
END;
CREATE TRIGGER content_files_no_update
BEFORE UPDATE ON content_files BEGIN
    SELECT RAISE(ABORT, 'content files are immutable');
END;
CREATE TRIGGER snapshot_material_no_update
BEFORE UPDATE OF snapshot_id, content_id, source_revision, created_at ON snapshot_roots
BEGIN
    SELECT RAISE(ABORT, 'snapshot material is immutable');
END;
CREATE TRIGGER aggregate_records_no_update
BEFORE UPDATE ON aggregate_records BEGIN
    SELECT RAISE(ABORT, 'aggregate records are immutable');
END;
CREATE TRIGGER aggregate_dependencies_no_update
BEFORE UPDATE ON aggregate_snapshot_dependencies BEGIN
    SELECT RAISE(ABORT, 'aggregate dependencies are immutable');
END;
CREATE TRIGGER aggregate_roots_no_material_update
BEFORE UPDATE OF aggregate_id, aggregate_kind, created_at, sequence ON aggregate_roots BEGIN
    SELECT RAISE(ABORT, 'aggregate root material is immutable');
END;
CREATE TRIGGER aggregate_root_dependencies_no_update
BEFORE UPDATE ON aggregate_root_snapshot_dependencies BEGIN
    SELECT RAISE(ABORT, 'aggregate root dependencies are immutable');
END;
CREATE TRIGGER aggregate_root_tombstones_no_update
BEFORE UPDATE ON aggregate_root_tombstones BEGIN
    SELECT RAISE(ABORT, 'aggregate root tombstones are immutable');
END;
CREATE TRIGGER child_index_no_update
BEFORE UPDATE ON child_index BEGIN
    SELECT RAISE(ABORT, 'aggregate children are immutable');
END;
"""

# Content identity of the accepted v1 sqlite_schema rows, including DDL bodies.
_VERSION_1_SCHEMA_SHA256 = (
    "1a1a831376cf67bcabbb2ebb231845bcff6e549b950bebbc83ce1df84dac5d83"
)

_MIGRATION_1_TO_2 = (
    """CREATE TABLE aggregate_roots (
    aggregate_id TEXT COLLATE BINARY PRIMARY KEY,
    aggregate_kind TEXT COLLATE BINARY NOT NULL,
    head_aggregate_id TEXT COLLATE BINARY NOT NULL
        REFERENCES aggregate_records(aggregate_id),
    created_at INTEGER NOT NULL CHECK (created_at >= 0),
    sequence INTEGER NOT NULL UNIQUE CHECK (sequence > 0)
) STRICT, WITHOUT ROWID""",
    """CREATE TABLE aggregate_root_snapshot_dependencies (
    aggregate_id TEXT COLLATE BINARY NOT NULL REFERENCES aggregate_roots(aggregate_id)
        ON DELETE CASCADE,
    snapshot_id TEXT COLLATE BINARY NOT NULL REFERENCES snapshot_roots(snapshot_id)
        ON DELETE CASCADE,
    PRIMARY KEY (aggregate_id, snapshot_id)
) STRICT, WITHOUT ROWID""",
    """CREATE TABLE aggregate_root_tombstones (
    aggregate_id TEXT COLLATE BINARY PRIMARY KEY,
    aggregate_kind TEXT COLLATE BINARY NOT NULL,
    purged_at INTEGER NOT NULL CHECK (purged_at >= 0)
) STRICT, WITHOUT ROWID""",
    "DROP TRIGGER delete_root_aggregate",
    """CREATE TRIGGER delete_root_aggregate
BEFORE DELETE ON snapshot_roots
BEGIN
    INSERT INTO aggregate_root_tombstones
        SELECT roots.aggregate_id, roots.aggregate_kind, tombstones.purged_at
        FROM aggregate_roots roots
        JOIN aggregate_root_snapshot_dependencies dependencies
            ON dependencies.aggregate_id = roots.aggregate_id
        JOIN purged_root_tombstones tombstones
            ON tombstones.snapshot_id = dependencies.snapshot_id
        WHERE dependencies.snapshot_id = OLD.snapshot_id;
    DELETE FROM aggregate_roots WHERE aggregate_id IN (
        SELECT aggregate_id FROM aggregate_root_snapshot_dependencies
        WHERE snapshot_id = OLD.snapshot_id
    );
    DELETE FROM aggregate_records WHERE aggregate_id IN (
        SELECT aggregate_id FROM aggregate_snapshot_dependencies
        WHERE snapshot_id = OLD.snapshot_id
    );
END""",
    """CREATE TRIGGER aggregate_roots_no_material_update
BEFORE UPDATE OF aggregate_id, aggregate_kind, created_at, sequence ON aggregate_roots BEGIN
    SELECT RAISE(ABORT, 'aggregate root material is immutable');
END""",
    """CREATE TRIGGER aggregate_root_dependencies_no_update
BEFORE UPDATE ON aggregate_root_snapshot_dependencies BEGIN
    SELECT RAISE(ABORT, 'aggregate root dependencies are immutable');
END""",
    """CREATE TRIGGER aggregate_root_tombstones_no_update
BEFORE UPDATE ON aggregate_root_tombstones BEGIN
    SELECT RAISE(ABORT, 'aggregate root tombstones are immutable');
END""",
)


@lru_cache(maxsize=1)
def _expected_schema_definition() -> tuple[tuple[str, str, str, str], ...]:
    connection = sqlite3.connect(":memory:", isolation_level=None)
    try:
        connection.executescript(_SCHEMA)
        return tuple(
            (str(kind), str(name), str(table), str(sql))
            for kind, name, table, sql in connection.execute(
                "SELECT type, name, tbl_name, sql FROM sqlite_schema "
                "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
            ).fetchall()
        )
    finally:
        connection.close()


class SQLiteSnapshotStore:
    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path) or not path.is_absolute():
            raise invalid(
                "SNAPSHOT_STORE.RELATIVE_PATH", "SQLite path must be an absolute Path"
            )
        self.path = path
        existed = path.exists() or path.is_symlink()
        created_identity: tuple[int, int] | None = None
        if existed:
            observed = path.lstat()
            if not stat.S_ISREG(observed.st_mode):
                raise unsupported(
                    "SNAPSHOT_STORE.UNSUPPORTED_PATH",
                    "SQLite path must be one regular non-symlink file",
                )
        else:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            flags |= getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            try:
                descriptor = os.open(path, flags, 0o600)
                observed = os.fstat(descriptor)
                created_identity = (observed.st_dev, observed.st_ino)
                os.close(descriptor)
            except OSError as error:
                raise unavailable("SNAPSHOT_STORE.UNAVAILABLE", str(error)) from error
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(
                path, isolation_level=None, timeout=BUSY_TIMEOUT_MS / 1000
            )
            self._connection = connection
            self._connection.enable_load_extension(False)
            if existed:
                self._verify_existing_authority()
                self._configure()
                self._prepare_existing_schema()
            else:
                self._configure()
                self._initialize_schema()
            self._verify_integrity()
        except Exception as error:
            self._cleanup_failed_open(connection, created_identity)
            if isinstance(error, SnapshotError):
                raise
            if isinstance(error, sqlite3.DatabaseError):
                raise invalid("SNAPSHOT_STORE.INVALID_DATABASE", str(error)) from error
            if isinstance(error, OSError):
                raise unavailable("SNAPSHOT_STORE.UNAVAILABLE", str(error)) from error
            raise

    def close(self) -> None:
        self._connection.close()

    def _cleanup_failed_open(
        self,
        connection: sqlite3.Connection | None,
        created_identity: tuple[int, int] | None,
    ) -> None:
        if connection is not None:
            connection.close()
        if created_identity is None:
            return
        try:
            observed = self.path.lstat()
            if (
                stat.S_ISREG(observed.st_mode)
                and not self.path.is_symlink()
                and (observed.st_dev, observed.st_ino) == created_identity
            ):
                self.path.unlink()
        except FileNotFoundError:
            pass

    @contextmanager
    def _transaction(self, *, write: bool) -> Iterator[None]:
        try:
            self._connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            yield
            self._connection.execute("COMMIT")
        except SnapshotError:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise
        except sqlite3.DatabaseError as error:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise self._adapt(error) from error
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise

    def publish_snapshot(
        self,
        snapshot: SnapshotId,
        content_id: str,
        capture: CapturedContent,
        created_at: int,
    ) -> SnapshotSummary:
        began = False
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            began = True
            existing_files = self._content_files(content_id)
            submitted_files = tuple(
                (str(item.path), item.content) for item in capture.files
            )
            if existing_files:
                if existing_files != submitted_files:
                    raise invalid(
                        "SNAPSHOT.CONTENT_ID_COLLISION",
                        "one content ID identifies contradictory path bytes",
                    )
            else:
                self._connection.execute(
                    "INSERT INTO content_sets VALUES (?, ?)",
                    (content_id, len(submitted_files)),
                )
                for logical_path, raw_bytes in submitted_files:
                    self._connection.execute(
                        "INSERT INTO content_files VALUES (?, ?, ?, ?, ?)",
                        (
                            content_id,
                            logical_path,
                            sqlite3.Binary(raw_bytes),
                            len(raw_bytes),
                            hashlib.sha256(raw_bytes).hexdigest(),
                        ),
                    )
            if self._connection.execute(
                "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = ?",
                (str(snapshot),),
            ).fetchone():
                raise invalid(
                    "SNAPSHOT.ID_COLLISION",
                    "generated snapshot ID identifies an expired root",
                )
            try:
                self._connection.execute(
                    "INSERT INTO snapshot_roots VALUES (?, ?, ?, ?, 'active', NULL)",
                    (str(snapshot), content_id, capture.source_revision, created_at),
                )
            except sqlite3.IntegrityError as error:
                raise invalid(
                    "SNAPSHOT.ID_COLLISION", "generated snapshot ID already exists"
                ) from error
            self._connection.execute("COMMIT")
            began = False
        except SnapshotError:
            if began:
                self._connection.execute("ROLLBACK")
            raise
        except sqlite3.DatabaseError as error:
            if began:
                self._connection.execute("ROLLBACK")
            raise self._adapt(error) from error
        return self.snapshot(snapshot, include_quarantined=True)

    def snapshot(
        self, snapshot: SnapshotId, *, include_quarantined: bool = False
    ) -> SnapshotSummary:
        try:
            row = self._connection.execute(
                "SELECT lifecycle, source_revision, created_at, purge_deadline "
                "FROM snapshot_roots WHERE snapshot_id = ?",
                (str(snapshot),),
            ).fetchone()
        except sqlite3.DatabaseError as error:
            raise self._adapt(error) from error
        if row is None:
            self._raise_missing(snapshot)
        lifecycle = str(row[0])
        if lifecycle == "quarantined" and not include_quarantined:
            raise unavailable(
                "SNAPSHOT.QUARANTINED", f"snapshot {snapshot} is quarantined"
            )
        return SnapshotSummary(
            snapshot,
            lifecycle,  # type: ignore[arg-type]
            str(row[1]),
            int(row[2]),
            None if row[3] is None else int(row[3]),
        )

    def find(self, request: FindSnapshotsRequest) -> SnapshotPage:
        parameters: tuple[object, ...]
        if request.after is None:
            where = "lifecycle = ?"
            parameters = (request.lifecycle, request.limit + 1)
        else:
            cursor = self._connection.execute(
                "SELECT created_at, snapshot_id FROM snapshot_roots WHERE snapshot_id = ?",
                (str(request.after),),
            ).fetchone()
            if cursor is None:
                raise invalid(
                    "SNAPSHOT.INVALID_CONTINUATION",
                    "discovery continuation no longer identifies a retained root",
                )
            where = (
                "lifecycle = ? AND "
                "(created_at > ? OR (created_at = ? AND snapshot_id > ?))"
            )
            parameters = (
                request.lifecycle,
                int(cursor[0]),
                int(cursor[0]),
                str(cursor[1]),
                request.limit + 1,
            )
        try:
            rows = self._connection.execute(
                f"SELECT snapshot_id FROM snapshot_roots WHERE {where} "
                "ORDER BY created_at, snapshot_id LIMIT ?",
                parameters,
            ).fetchall()
        except sqlite3.DatabaseError as error:
            raise self._adapt(error) from error
        selected = rows[: request.limit]
        summaries = tuple(
            self.snapshot(SnapshotId(str(row[0])), include_quarantined=True)
            for row in selected
        )
        continuation = summaries[-1].snapshot if len(rows) > request.limit else None
        return SnapshotPage(summaries, continuation)

    def load_content(self, snapshot: SnapshotId) -> tuple[str, CapturedContent]:
        with self._transaction(write=False):
            self.snapshot(snapshot)
            root = self._connection.execute(
                "SELECT content_id, source_revision FROM snapshot_roots "
                "WHERE snapshot_id = ?",
                (str(snapshot),),
            ).fetchone()
            assert root is not None
            content_id = str(root[0])
            expected_count = self._connection.execute(
                "SELECT file_count FROM content_sets WHERE content_id = ?",
                (content_id,),
            ).fetchone()
            if expected_count is None:
                raise invalid(
                    "SNAPSHOT_STORE.INVALID_CONTENT",
                    "snapshot content set is unavailable",
                )
            files = self._content_files(content_id)
            if int(expected_count[0]) != len(files):
                raise invalid(
                    "SNAPSHOT_STORE.INVALID_CONTENT",
                    "snapshot content file count is contradictory",
                )
            result = (
                content_id,
                CapturedContent(
                    str(root[1]),
                    (
                        SnapshotFile(SnapshotPath.parse(path), content)
                        for path, content in files
                    ),
                ),
            )
        return result

    def delete(
        self, snapshot: SnapshotId, *, now: int, quarantine_seconds: int
    ) -> DeleteSnapshotResult:
        with self._transaction(write=True):
            summary = self.snapshot(snapshot, include_quarantined=True)
            if summary.lifecycle == "quarantined":
                assert summary.purge_deadline is not None
                result = DeleteSnapshotResult(snapshot, summary.purge_deadline)
            else:
                deadline = now + quarantine_seconds
                self._connection.execute(
                    "UPDATE snapshot_roots SET lifecycle = 'quarantined', purge_deadline = ? "
                    "WHERE snapshot_id = ?",
                    (deadline, str(snapshot)),
                )
                result = DeleteSnapshotResult(snapshot, deadline)
        return result

    def undelete(self, snapshot: SnapshotId) -> SnapshotSummary:
        with self._transaction(write=True):
            self.snapshot(snapshot, include_quarantined=True)
            self._connection.execute(
                "UPDATE snapshot_roots SET lifecycle = 'active', purge_deadline = NULL "
                "WHERE snapshot_id = ?",
                (str(snapshot),),
            )
            result = self.snapshot(snapshot)
        return result

    def purge_expired(self, now: int) -> None:
        began = False
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            began = True
            expired = self._connection.execute(
                "SELECT snapshot_id, content_id FROM snapshot_roots "
                "WHERE lifecycle = 'quarantined' AND purge_deadline <= ? "
                "ORDER BY snapshot_id",
                (now,),
            ).fetchall()
            for raw_snapshot, content_id in expired:
                snapshot_id = str(raw_snapshot)
                self._connection.execute(
                    "INSERT INTO purged_root_tombstones VALUES (?, ?)",
                    (snapshot_id, now),
                )
                self._connection.execute(
                    "DELETE FROM snapshot_roots WHERE snapshot_id = ?", (snapshot_id,)
                )
                self._purge_stage("after-root-delete", snapshot_id)
                self._connection.execute(
                    "DELETE FROM content_sets WHERE content_id = ? AND NOT EXISTS "
                    "(SELECT 1 FROM snapshot_roots WHERE content_id = ?)",
                    (content_id, content_id),
                )
            self._connection.execute("COMMIT")
            began = False
        except SnapshotError:
            if began:
                self._connection.execute("ROLLBACK")
            raise
        except sqlite3.DatabaseError as error:
            if began:
                self._connection.execute("ROLLBACK")
            raise self._adapt(error) from error
        except Exception:
            if began:
                self._connection.execute("ROLLBACK")
            raise

    def publish_aggregate(self, record: AggregateRecord) -> PutResult:
        began = False
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            began = True
            for snapshot in record.snapshots:
                self.snapshot(snapshot)
            result = self._publish_aggregate_unchecked(record)
            self._connection.execute("COMMIT")
            began = False
        except SnapshotError:
            if began:
                self._connection.execute("ROLLBACK")
            raise
        except sqlite3.DatabaseError as error:
            if began:
                self._connection.execute("ROLLBACK")
            raise self._adapt(error) from error
        return result

    def create_aggregate_root(self, root: AggregateRoot, head: AggregateRecord) -> None:
        if root.head_id != head.aggregate_id or root.snapshots != head.snapshots:
            raise invalid(
                "AGGREGATE.INVALID_ROOT_HEAD",
                "initial aggregate root and head must have identical dependencies",
            )
        with self._transaction(write=True):
            for snapshot in root.snapshots:
                self.snapshot(snapshot)
            if self._connection.execute(
                "SELECT 1 FROM aggregate_root_tombstones WHERE aggregate_id = ?",
                (root.aggregate_id,),
            ).fetchone():
                raise invalid(
                    "AGGREGATE.ROOT_ID_COLLISION",
                    "generated aggregate root ID identifies an expired root",
                )
            self._publish_aggregate_unchecked(head)
            sequence = int(
                self._connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) + 1 FROM aggregate_roots"
                ).fetchone()[0]
            )
            try:
                self._connection.execute(
                    "INSERT INTO aggregate_roots VALUES (?, ?, ?, ?, ?)",
                    (
                        root.aggregate_id,
                        root.kind,
                        root.head_id,
                        root.created_at,
                        sequence,
                    ),
                )
            except sqlite3.IntegrityError as error:
                raise invalid(
                    "AGGREGATE.ROOT_ID_COLLISION",
                    "generated aggregate root ID already exists",
                ) from error
            for snapshot in root.snapshots:
                self._connection.execute(
                    "INSERT INTO aggregate_root_snapshot_dependencies VALUES (?, ?)",
                    (root.aggregate_id, str(snapshot)),
                )

    def find_aggregate_roots(
        self, request: FindAggregateRootsRequest
    ) -> AggregateRootPage:
        with self._transaction(write=False):
            if request.after is None:
                cursor_sql = ""
                parameters: tuple[object, ...] = (request.kind, request.limit + 1)
            else:
                cursor = self._connection.execute(
                    "SELECT sequence FROM aggregate_roots "
                    "WHERE aggregate_id = ? AND aggregate_kind = ?",
                    (request.after, request.kind),
                ).fetchone()
                if cursor is None:
                    raise invalid(
                        "AGGREGATE.INVALID_ROOT_CONTINUATION",
                        "aggregate root continuation is unavailable",
                    )
                cursor_sql = "AND sequence > ? "
                parameters = (
                    request.kind,
                    int(cursor[0]),
                    request.limit + 1,
                )
            rows = self._connection.execute(
                "SELECT aggregate_id FROM aggregate_roots "
                "WHERE aggregate_kind = ? "
                "AND NOT EXISTS ("
                "SELECT 1 FROM aggregate_root_snapshot_dependencies dependencies "
                "JOIN snapshot_roots roots ON roots.snapshot_id = dependencies.snapshot_id "
                "WHERE dependencies.aggregate_id = aggregate_roots.aggregate_id "
                "AND roots.lifecycle != 'active') "
                f"{cursor_sql}ORDER BY sequence LIMIT ?",
                parameters,
            ).fetchall()
            selected = rows[: request.limit]
            roots = tuple(self._load_root_unchecked(str(row[0])) for row in selected)
        continuation = roots[-1].aggregate_id if len(rows) > request.limit else None
        return AggregateRootPage(roots, continuation)

    def load_aggregate_root(self, aggregate_id: str) -> AggregateRoot:
        _root_reference(aggregate_id, "aggregate root ID")
        with self._transaction(write=False):
            root = self._load_root_unchecked(aggregate_id)
            for snapshot in root.snapshots:
                self.snapshot(snapshot)
        return root

    def advance_aggregate_root(
        self,
        aggregate_id: str,
        expected_head_id: str,
        head: AggregateRecord,
    ) -> AdvanceAggregateRootResult:
        _root_reference(aggregate_id, "aggregate root ID")
        _root_reference(expected_head_id, "expected aggregate root head ID")
        if type(head) is not AggregateRecord:
            raise invalid(
                "AGGREGATE.INVALID_ROOT_HEAD",
                "aggregate root head must be an exact AggregateRecord",
            )
        with self._transaction(write=True):
            root = self._load_root_unchecked(aggregate_id)
            for snapshot in root.snapshots:
                self.snapshot(snapshot)
            if root.snapshots != head.snapshots:
                raise invalid(
                    "AGGREGATE.INVALID_ROOT_HEAD",
                    "aggregate root and replacement head must have identical dependencies",
                )
            if root.head_id != expected_head_id:
                return "stale"
            self._publish_aggregate_unchecked(head)
            self._advance_root_stage("after-record-publish", aggregate_id)
            updated = self._connection.execute(
                "UPDATE aggregate_roots SET head_aggregate_id = ? "
                "WHERE aggregate_id = ? AND head_aggregate_id = ?",
                (head.aggregate_id, aggregate_id, expected_head_id),
            )
            if updated.rowcount != 1:
                raise invalid(
                    "AGGREGATE.INVALID_ROOT_CAS",
                    "aggregate root head changed outside its owning transaction",
                )
            self._advance_root_stage("after-root-update", aggregate_id)
        return "advanced"

    def load_aggregate(self, aggregate_id: str) -> AggregateRecord:
        with self._transaction(write=False):
            record = self._load_aggregate_unchecked(aggregate_id)
            for snapshot in record.snapshots:
                self.snapshot(snapshot)
        return record

    def inspect_child(self, aggregate_id: str, kind: str, child_id: str) -> bytes:
        with self._transaction(write=False):
            record = self._load_aggregate_unchecked(aggregate_id)
            for snapshot in record.snapshots:
                self.snapshot(snapshot)
            row = self._connection.execute(
                "SELECT payload FROM child_index WHERE aggregate_id = ? "
                "AND child_kind = ? AND child_id = ?",
                (aggregate_id, kind, child_id),
            ).fetchone()
            if row is None:
                raise unavailable(
                    "INSPECTION.UNAVAILABLE", "aggregate child is unavailable"
                )
            result = bytes(row[0])
        return result

    def counts(self) -> dict[str, int]:
        tables = (
            "content_sets",
            "content_files",
            "snapshot_roots",
            "aggregate_records",
            "aggregate_snapshot_dependencies",
            "aggregate_roots",
            "aggregate_root_snapshot_dependencies",
            "aggregate_root_tombstones",
            "child_index",
            "purged_root_tombstones",
        )
        return {
            table: int(
                self._connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            )
            for table in tables
        }

    def _load_aggregate_unchecked(self, aggregate_id: str) -> AggregateRecord:
        try:
            row = self._connection.execute(
                "SELECT aggregate_kind, payload FROM aggregate_records WHERE aggregate_id = ?",
                (aggregate_id,),
            ).fetchone()
            if row is None:
                raise unavailable(
                    "AGGREGATE.UNAVAILABLE",
                    f"aggregate {aggregate_id!r} is unavailable",
                )
            snapshots = tuple(
                SnapshotId(str(item[0]))
                for item in self._connection.execute(
                    "SELECT snapshot_id FROM aggregate_snapshot_dependencies "
                    "WHERE aggregate_id = ? ORDER BY snapshot_id",
                    (aggregate_id,),
                ).fetchall()
            )
            children = tuple(
                AggregateChild(str(item[0]), str(item[1]), bytes(item[2]))
                for item in self._connection.execute(
                    "SELECT child_kind, child_id, payload FROM child_index "
                    "WHERE aggregate_id = ? ORDER BY child_kind, child_id",
                    (aggregate_id,),
                ).fetchall()
            )
        except sqlite3.DatabaseError as error:
            raise self._adapt(error) from error
        return AggregateRecord(
            aggregate_id, str(row[0]), bytes(row[1]), snapshots, children
        )

    def _load_root_unchecked(self, aggregate_id: str) -> AggregateRoot:
        row = self._connection.execute(
            "SELECT aggregate_kind, head_aggregate_id, created_at "
            "FROM aggregate_roots WHERE aggregate_id = ?",
            (aggregate_id,),
        ).fetchone()
        if row is None:
            raise unavailable(
                "AGGREGATE.ROOT_UNAVAILABLE",
                f"aggregate root {aggregate_id!r} is unavailable",
            )
        snapshots = tuple(
            SnapshotId(str(item[0]))
            for item in self._connection.execute(
                "SELECT snapshot_id FROM aggregate_root_snapshot_dependencies "
                "WHERE aggregate_id = ? ORDER BY snapshot_id",
                (aggregate_id,),
            ).fetchall()
        )
        return AggregateRoot(
            aggregate_id, str(row[0]), str(row[1]), snapshots, int(row[2])
        )

    def _publish_aggregate_unchecked(self, record: AggregateRecord) -> PutResult:
        existing = self._connection.execute(
            "SELECT aggregate_kind, payload FROM aggregate_records WHERE aggregate_id = ?",
            (record.aggregate_id,),
        ).fetchone()
        if existing is None:
            self._connection.execute(
                "INSERT INTO aggregate_records VALUES (?, ?, ?)",
                (record.aggregate_id, record.kind, sqlite3.Binary(record.payload)),
            )
            for snapshot in record.snapshots:
                self._connection.execute(
                    "INSERT INTO aggregate_snapshot_dependencies VALUES (?, ?)",
                    (record.aggregate_id, str(snapshot)),
                )
            for child in record.children:
                self._connection.execute(
                    "INSERT INTO child_index VALUES (?, ?, ?, ?)",
                    (
                        record.aggregate_id,
                        child.kind,
                        child.child_id,
                        sqlite3.Binary(child.payload),
                    ),
                )
            return "inserted"
        if self._load_aggregate_unchecked(record.aggregate_id) == record:
            return "existing-identical"
        raise invalid(
            "AGGREGATE.ID_COLLISION",
            "one aggregate ID identifies contradictory material",
        )

    def _content_files(self, content_id: str) -> tuple[tuple[str, bytes], ...]:
        try:
            rows = self._connection.execute(
                "SELECT logical_path, raw_bytes, byte_length, sha256 FROM content_files "
                "WHERE content_id = ? ORDER BY logical_path",
                (content_id,),
            ).fetchall()
        except sqlite3.DatabaseError as error:
            raise self._adapt(error) from error
        selected: list[tuple[str, bytes]] = []
        for path, raw, length, expected_digest in rows:
            content = bytes(raw)
            if (
                len(content) != length
                or hashlib.sha256(content).hexdigest() != expected_digest
            ):
                raise invalid(
                    "SNAPSHOT_STORE.INVALID_CONTENT",
                    "stored content bytes are contradictory",
                )
            selected.append((str(path), content))
        return tuple(selected)

    def _raise_missing(self, snapshot: SnapshotId) -> None:
        tombstone = self._connection.execute(
            "SELECT 1 FROM purged_root_tombstones WHERE snapshot_id = ?",
            (str(snapshot),),
        ).fetchone()
        if tombstone:
            raise unavailable("SNAPSHOT.EXPIRED", f"snapshot {snapshot} has expired")
        raise unavailable("SNAPSHOT.UNAVAILABLE", f"snapshot {snapshot} is unavailable")

    def _configure(self) -> None:
        observed_mode = self._connection.execute(
            "PRAGMA journal_mode=DELETE"
        ).fetchone()[0]
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._connection.execute("PRAGMA trusted_schema=OFF")
        self._connection.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
        observed = {
            "journal_mode": str(observed_mode).lower(),
            "synchronous": self._connection.execute("PRAGMA synchronous").fetchone()[0],
            "foreign_keys": self._connection.execute("PRAGMA foreign_keys").fetchone()[
                0
            ],
            "trusted_schema": self._connection.execute(
                "PRAGMA trusted_schema"
            ).fetchone()[0],
            "busy_timeout": self._connection.execute("PRAGMA busy_timeout").fetchone()[
                0
            ],
        }
        expected = {
            "journal_mode": "delete",
            "synchronous": 2,
            "foreign_keys": 1,
            "trusted_schema": 0,
            "busy_timeout": BUSY_TIMEOUT_MS,
        }
        if observed != expected:
            raise unsupported(
                "SNAPSHOT_STORE.UNSUPPORTED_PROFILE",
                f"required SQLite profile differs: {observed!r}",
            )

    def _initialize_schema(self) -> None:
        try:
            self._connection.executescript(
                "BEGIN IMMEDIATE;\n"
                f"PRAGMA application_id={APPLICATION_ID};\n"
                f"PRAGMA user_version={USER_VERSION};\n"
                f"{_SCHEMA}\n"
                "COMMIT;"
            )
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise
        self._verify_schema()

    def _prepare_existing_schema(self) -> None:
        application_id = self._connection.execute("PRAGMA application_id").fetchone()[0]
        user_version = self._connection.execute("PRAGMA user_version").fetchone()[0]
        if application_id != APPLICATION_ID:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_APPLICATION",
                f"expected application {APPLICATION_ID}, observed {application_id}",
            )
        if user_version == 1:
            self._migrate_version_one()
        self._verify_schema()

    def _verify_existing_authority(self) -> None:
        application_id = self._connection.execute("PRAGMA application_id").fetchone()[0]
        user_version = self._connection.execute("PRAGMA user_version").fetchone()[0]
        if application_id != APPLICATION_ID:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_APPLICATION",
                f"expected application {APPLICATION_ID}, observed {application_id}",
            )
        if user_version > USER_VERSION:
            raise unsupported(
                "SNAPSHOT_STORE.UNSUPPORTED_VERSION",
                f"unsupported schema version {user_version}",
            )
        if user_version == 1:
            self._verify_version_one_schema()
            self._verify_integrity()
            return
        if user_version != USER_VERSION:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_VERSION",
                f"expected schema version 1 or {USER_VERSION}, observed {user_version}",
            )
        self._verify_schema()
        self._verify_integrity()

    def _migrate_version_one(self) -> None:
        with self._transaction(write=True):
            application_id = self._connection.execute(
                "PRAGMA application_id"
            ).fetchone()[0]
            user_version = self._connection.execute("PRAGMA user_version").fetchone()[0]
            if application_id != APPLICATION_ID:
                raise invalid(
                    "SNAPSHOT_STORE.INVALID_APPLICATION",
                    f"expected application {APPLICATION_ID}, observed {application_id}",
                )
            if user_version == USER_VERSION:
                self._verify_schema()
                return
            if user_version != 1:
                raise invalid(
                    "SNAPSHOT_STORE.INVALID_VERSION",
                    f"expected schema version 1, observed {user_version}",
                )
            self._verify_version_one_schema()
            self._verify_integrity()
            for statement in _MIGRATION_1_TO_2:
                self._connection.execute(statement)
            self._migration_stage("after-schema")
            self._connection.execute(f"PRAGMA user_version={USER_VERSION}")
            self._verify_schema()
            self._verify_integrity()
            self._migration_stage("before-commit")

    def _verify_schema(self) -> None:
        application_id = self._connection.execute("PRAGMA application_id").fetchone()[0]
        user_version = self._connection.execute("PRAGMA user_version").fetchone()[0]
        if application_id != APPLICATION_ID:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_APPLICATION",
                f"expected application {APPLICATION_ID}, observed {application_id}",
            )
        if user_version > USER_VERSION:
            raise unsupported(
                "SNAPSHOT_STORE.UNSUPPORTED_VERSION",
                f"unsupported schema version {user_version}",
            )
        if user_version != USER_VERSION:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_VERSION",
                f"expected schema version {USER_VERSION}, observed {user_version}",
            )
        if self._schema_definition() != _expected_schema_definition():
            raise invalid("SNAPSHOT_STORE.INVALID_SCHEMA", "SQLite schema differs")

    def _verify_version_one_schema(self) -> None:
        encoded = json.dumps(
            self._schema_definition(), ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        observed = hashlib.sha256(encoded).hexdigest()
        if observed != _VERSION_1_SCHEMA_SHA256:
            raise invalid(
                "SNAPSHOT_STORE.INVALID_SCHEMA",
                f"SQLite v1 schema digest differs: {observed}",
            )

    def _schema_definition(self) -> tuple[tuple[str, str, str, str], ...]:
        return tuple(
            (str(kind), str(name), str(table), str(sql))
            for kind, name, table, sql in self._connection.execute(
                "SELECT type, name, tbl_name, sql FROM sqlite_schema "
                "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
            ).fetchall()
        )

    def _verify_integrity(self) -> None:
        if self._connection.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise invalid(
                "SNAPSHOT_STORE.INTEGRITY_FAILURE", "SQLite integrity check failed"
            )
        if self._connection.execute("PRAGMA foreign_key_check").fetchall():
            raise invalid(
                "SNAPSHOT_STORE.FOREIGN_KEY_FAILURE", "foreign key check failed"
            )

    def _purge_stage(self, stage: str, snapshot_id: str) -> None:
        del stage, snapshot_id

    def _migration_stage(self, stage: str) -> None:
        del stage

    def _advance_root_stage(self, stage: str, aggregate_id: str) -> None:
        del stage, aggregate_id

    @staticmethod
    def _adapt(error: sqlite3.DatabaseError) -> SnapshotError:
        code = getattr(error, "sqlite_errorcode", None)
        if code in {sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED}:
            return unavailable(
                "SNAPSHOT_STORE.BUSY",
                f"SQLite remained busy for {BUSY_TIMEOUT_MS} ms",
            )
        if code in {
            sqlite3.SQLITE_READONLY,
            sqlite3.SQLITE_CANTOPEN,
            sqlite3.SQLITE_IOERR,
        }:
            return unavailable("SNAPSHOT_STORE.UNAVAILABLE", str(error))
        return invalid("SNAPSHOT_STORE.INVALID_DATABASE", str(error))


__all__ = (
    "APPLICATION_ID",
    "BUSY_TIMEOUT_MS",
    "SQLiteSnapshotStore",
    "USER_VERSION",
)
