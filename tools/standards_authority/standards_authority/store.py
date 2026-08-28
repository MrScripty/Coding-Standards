from __future__ import annotations

import os
import sqlite3
import stat
from pathlib import Path
from typing import Protocol

from .errors import AuthorityError, invalid, unavailable, unsupported
from .model import MAX_ENVELOPE_BYTES, AuthorityHandle, PutResult
from .envelope import encode_storage_key

APPLICATION_ID = 1_397_047_601
USER_VERSION = 1
BUSY_TIMEOUT_MS = 5_000

_TABLE_SQL = """CREATE TABLE authority_objects (
    handle TEXT COLLATE BINARY PRIMARY KEY,
    envelope BLOB NOT NULL,
    CHECK (typeof(handle) = 'text'),
    CHECK (typeof(envelope) = 'blob')
) WITHOUT ROWID"""
_UPDATE_TRIGGER_SQL = """CREATE TRIGGER authority_objects_no_update
BEFORE UPDATE ON authority_objects
BEGIN
    SELECT RAISE(ABORT, 'authority object rows are immutable');
END"""
_DELETE_TRIGGER_SQL = """CREATE TRIGGER authority_objects_no_delete
BEFORE DELETE ON authority_objects
BEGIN
    SELECT RAISE(ABORT, 'authority object rows are immutable');
END"""


class ObjectStore(Protocol):
    def get(self, handle: AuthorityHandle) -> bytes: ...

    def put_if_absent(self, handle: AuthorityHandle, envelope: bytes) -> PutResult: ...


class MemoryObjectStore:
    def __init__(self) -> None:
        self._rows: dict[str, bytes] = {}

    def get(self, handle: AuthorityHandle) -> bytes:
        key = encode_storage_key(handle)
        try:
            envelope = self._rows[key]
        except KeyError as error:
            raise unavailable(
                "AUTHORITY.OBJECT_UNAVAILABLE", f"object {key!r} is unavailable"
            ) from error
        if len(envelope) > MAX_ENVELOPE_BYTES:
            raise unsupported(
                "AUTHORITY.ENVELOPE_TOO_LARGE", "stored envelope exceeds the bound"
            )
        return envelope

    def put_if_absent(self, handle: AuthorityHandle, envelope: bytes) -> PutResult:
        if type(envelope) is not bytes:
            raise invalid("STORE.INVALID_ENVELOPE", "stored envelope must be bytes")
        if len(envelope) > MAX_ENVELOPE_BYTES:
            raise unsupported(
                "AUTHORITY.ENVELOPE_TOO_LARGE", "submitted envelope exceeds the bound"
            )
        key = encode_storage_key(handle)
        existing = self._rows.get(key)
        if existing is None:
            self._rows[key] = envelope
            return "inserted"
        if existing != envelope:
            raise invalid(
                "IDENTITY.COLLISION",
                "one authority handle identified contradictory envelope bytes",
            )
        return "existing-identical"

    def _all_rows(self) -> tuple[tuple[str, bytes], ...]:
        return tuple(sorted(self._rows.items()))


class SQLiteObjectStore:
    def __init__(self, path: Path, *, read_only: bool = False) -> None:
        if not path.is_absolute():
            raise invalid("STORE.RELATIVE_PATH", "SQLite store path must be absolute")
        self.path = path
        existed = path.exists()
        if read_only and not existed:
            raise unavailable("STORE.UNAVAILABLE", "read-only store is absent")
        if not existed:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            try:
                descriptor = os.open(
                    path,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
                    0o600,
                )
                os.close(descriptor)
            except OSError as error:
                raise unavailable("STORE.UNAVAILABLE", str(error)) from error
        else:
            observed = path.lstat()
            if not stat.S_ISREG(observed.st_mode):
                raise unsupported(
                    "STORE.UNSUPPORTED_DATABASE_PATH",
                    "SQLite store must be one regular non-symlink file",
                )
        try:
            target = f"file:{path}?mode=ro" if read_only else str(path)
            connection = sqlite3.connect(
                target,
                isolation_level=None,
                timeout=BUSY_TIMEOUT_MS / 1000,
                uri=read_only,
            )
            connection.enable_load_extension(False)
            self._connection = connection
            self._read_only = read_only
            self._configure()
            if existed:
                self._verify_schema()
            else:
                self._initialize_schema()
            self._verify_integrity()
        except AuthorityError:
            raise
        except sqlite3.DatabaseError as error:
            raise invalid("STORE.INVALID_DATABASE", str(error)) from error
        except OSError as error:
            raise unavailable("STORE.UNAVAILABLE", str(error)) from error

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> SQLiteObjectStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def get(self, handle: AuthorityHandle) -> bytes:
        key = encode_storage_key(handle)
        try:
            row = self._connection.execute(
                "SELECT typeof(envelope), length(envelope) "
                "FROM authority_objects WHERE handle = ?",
                (key,),
            ).fetchone()
        except sqlite3.DatabaseError as error:
            raise self._adapt_database_error(error) from error
        if row is None:
            raise unavailable(
                "AUTHORITY.OBJECT_UNAVAILABLE", f"object {key!r} is unavailable"
            )
        storage_type, length = row
        if storage_type != "blob":
            raise invalid("STORE.INVALID_ROW", "stored envelope is not a BLOB")
        if type(length) is not int or length > MAX_ENVELOPE_BYTES:
            raise unsupported(
                "AUTHORITY.ENVELOPE_TOO_LARGE", "stored envelope exceeds the bound"
            )
        try:
            envelope = self._connection.execute(
                "SELECT envelope FROM authority_objects WHERE handle = ?", (key,)
            ).fetchone()[0]
        except sqlite3.DatabaseError as error:
            raise self._adapt_database_error(error) from error
        if type(envelope) is not bytes or len(envelope) != length:
            raise invalid("STORE.INVALID_ROW", "stored envelope BLOB is contradictory")
        return envelope

    def put_if_absent(self, handle: AuthorityHandle, envelope: bytes) -> PutResult:
        if self._read_only:
            raise unsupported(
                "STORE.READ_ONLY", "read-only recovery source cannot publish objects"
            )
        if type(envelope) is not bytes:
            raise invalid("STORE.INVALID_ENVELOPE", "stored envelope must be bytes")
        if len(envelope) > MAX_ENVELOPE_BYTES:
            raise unsupported(
                "AUTHORITY.ENVELOPE_TOO_LARGE", "submitted envelope exceeds the bound"
            )
        key = encode_storage_key(handle)
        began = False
        try:
            self._publication_stage("before-begin")
            self._connection.execute("BEGIN IMMEDIATE")
            began = True
            self._publication_stage("after-begin")
            row = self._connection.execute(
                "SELECT envelope FROM authority_objects WHERE handle = ?", (key,)
            ).fetchone()
            if row is None:
                self._connection.execute(
                    "INSERT INTO authority_objects(handle, envelope) VALUES (?, ?)",
                    (key, sqlite3.Binary(envelope)),
                )
                result: PutResult = "inserted"
                self._publication_stage("after-insert")
            elif row[0] == envelope:
                result = "existing-identical"
            else:
                raise invalid(
                    "IDENTITY.COLLISION",
                    "one authority handle identified contradictory envelope bytes",
                )
            self._publication_stage("before-commit")
            self._connection.execute("COMMIT")
            began = False
            self._publication_stage("after-commit")
        except AuthorityError:
            if began:
                self._connection.execute("ROLLBACK")
            raise
        except sqlite3.DatabaseError as error:
            if began:
                self._connection.execute("ROLLBACK")
            raise self._adapt_database_error(error) from error
        if self.get(handle) != envelope:
            raise invalid(
                "STORE.PUBLICATION_CONTRADICTION",
                "published row did not reproduce the submitted envelope",
            )
        return result

    def _publication_stage(self, stage: str) -> None:
        """Test seam for deterministic process interruption around publication."""
        del stage

    def _configure(self) -> None:
        required = {
            "journal_mode": "delete",
            "synchronous": 3,
            "locking_mode": "normal",
            "trusted_schema": 0,
        }
        observed: dict[str, object] = {}
        observed["journal_mode"] = self._connection.execute(
            "PRAGMA journal_mode=DELETE"
        ).fetchone()[0]
        self._connection.execute("PRAGMA synchronous=EXTRA")
        observed["synchronous"] = self._connection.execute(
            "PRAGMA synchronous"
        ).fetchone()[0]
        observed["locking_mode"] = self._connection.execute(
            "PRAGMA locking_mode=NORMAL"
        ).fetchone()[0]
        self._connection.execute("PRAGMA trusted_schema=OFF")
        observed["trusted_schema"] = self._connection.execute(
            "PRAGMA trusted_schema"
        ).fetchone()[0]
        self._connection.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
        timeout = self._connection.execute("PRAGMA busy_timeout").fetchone()[0]
        if timeout != BUSY_TIMEOUT_MS:
            raise unsupported("STORE.UNSUPPORTED_BUSY_TIMEOUT", repr(timeout))
        for name, expected in required.items():
            actual = observed[name]
            if type(expected) is str:
                matches = type(actual) is str and actual.lower() == expected
            else:
                matches = actual == expected
            if not matches:
                raise unsupported(
                    "STORE.UNSUPPORTED_PROFILE",
                    f"required {name}={expected!r}, observed {actual!r}",
                )

    def _initialize_schema(self) -> None:
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            self._connection.execute(f"PRAGMA application_id={APPLICATION_ID}")
            self._connection.execute(f"PRAGMA user_version={USER_VERSION}")
            self._connection.execute(_TABLE_SQL)
            self._connection.execute(_UPDATE_TRIGGER_SQL)
            self._connection.execute(_DELETE_TRIGGER_SQL)
            self._connection.execute("COMMIT")
            self._verify_schema()
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise

    def _verify_schema(self) -> None:
        application_id = self._connection.execute("PRAGMA application_id").fetchone()[0]
        user_version = self._connection.execute("PRAGMA user_version").fetchone()[0]
        if application_id != APPLICATION_ID:
            raise invalid(
                "STORE.INVALID_APPLICATION_ID",
                f"expected {APPLICATION_ID}, observed {application_id}",
            )
        if user_version > USER_VERSION:
            raise unsupported(
                "STORE.UNSUPPORTED_SCHEMA_VERSION", f"unsupported schema {user_version}"
            )
        if user_version != USER_VERSION:
            raise invalid(
                "STORE.INVALID_SCHEMA_VERSION",
                f"expected schema {USER_VERSION}, observed {user_version}",
            )
        rows = self._connection.execute(
            "SELECT type, name, sql FROM sqlite_schema "
            "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
        ).fetchall()
        expected = [
            ("table", "authority_objects", _TABLE_SQL),
            ("trigger", "authority_objects_no_delete", _DELETE_TRIGGER_SQL),
            ("trigger", "authority_objects_no_update", _UPDATE_TRIGGER_SQL),
        ]
        if rows != expected:
            raise invalid("STORE.INVALID_SCHEMA", "SQLite schema-v1 differs")

    def _verify_integrity(self) -> None:
        result = self._connection.execute("PRAGMA integrity_check").fetchall()
        if result != [("ok",)]:
            raise invalid("STORE.INTEGRITY_FAILURE", repr(result))

    def _all_rows(self) -> tuple[tuple[str, bytes], ...]:
        rows = self._connection.execute(
            "SELECT handle, envelope FROM authority_objects ORDER BY handle"
        ).fetchall()
        return tuple((handle, bytes(envelope)) for handle, envelope in rows)

    @staticmethod
    def _adapt_database_error(error: sqlite3.DatabaseError) -> AuthorityError:
        code = getattr(error, "sqlite_errorcode", None)
        if code in {sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED}:
            return unavailable("STORE.BUSY", "SQLite writer remained busy for 5000 ms")
        if code in {
            sqlite3.SQLITE_READONLY,
            sqlite3.SQLITE_CANTOPEN,
            sqlite3.SQLITE_IOERR,
        }:
            return unavailable("STORE.UNAVAILABLE", str(error))
        return invalid("STORE.INVALID_DATABASE", str(error))


__all__ = (
    "APPLICATION_ID",
    "BUSY_TIMEOUT_MS",
    "MemoryObjectStore",
    "ObjectStore",
    "SQLiteObjectStore",
    "USER_VERSION",
)
