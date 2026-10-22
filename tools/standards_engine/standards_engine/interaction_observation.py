"""Private, non-authoritative interaction evidence; no Engine or transport policy.

Every write commits synchronously. A failed recorder becomes inert until close;
its bounded stderr diagnostic cannot disclose supplied observations.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys


SCHEMA_VERSION = 1
_TABLES = {
    "sessions": """CREATE TABLE sessions (
        id INTEGER PRIMARY KEY,
        started_at TEXT NOT NULL,
        ended_at TEXT,
        interface_version INTEGER NOT NULL,
        catalog_digest TEXT NOT NULL,
        schema_digest TEXT NOT NULL,
        purpose TEXT NOT NULL,
        session_metadata_json TEXT
    )""",
    "interactions": """CREATE TABLE interactions (
        id INTEGER PRIMARY KEY,
        session_id INTEGER NOT NULL,
        sequence_number INTEGER NOT NULL,
        observed_at TEXT NOT NULL,
        request_json TEXT NOT NULL,
        response_metadata_json TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        UNIQUE (session_id, sequence_number)
    )""",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class InertInteractionRecorder:
    """The disabled boundary holds no state and performs no serialization or I/O."""
    __slots__ = ()

    def begin_session(self, interface_identity: dict, session_metadata: object = None) -> None:
        pass

    def record_request(self, request: object) -> int | None:
        return None

    def record_response_metadata(self, interaction: int | None, metadata: object) -> None:
        pass

    def close(self) -> None:
        pass


class SQLiteInteractionRecorder:
    """Own one session, its ordering, schema admission, commits and failure isolation.

    The caller supplies existing identity and opaque JSON-compatible values.
    Private interaction handles are used only to attach explicit metadata.
    """
    def __init__(self, path: Path) -> None:
        self._connection: sqlite3.Connection | None = None
        self._session: int | None = None
        self._sequence = 0
        self._failed = False
        try:
            self._connection = sqlite3.connect(path.resolve())
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._admit_schema()
        except Exception as error:
            self._disable("initialization", error)

    def _admit_schema(self) -> None:
        connection = self._connection
        version = connection.execute("PRAGMA user_version").fetchone()[0]
        objects = connection.execute(
            "SELECT name, sql FROM sqlite_master WHERE sql IS NOT NULL"
        ).fetchall()
        if version == 0 and not objects:
            # DDL and version publication are one transaction, including interruption.
            with connection:
                connection.execute("BEGIN")
                for statement in _TABLES.values():
                    connection.execute(statement)
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        elif version != SCHEMA_VERSION:
            raise ValueError("Unsupported observation schema version")
        elif {name: " ".join(sql.split()).lower() for name, sql in objects} != {
            name: " ".join(sql.split()).lower() for name, sql in _TABLES.items()
        }:
            raise ValueError("Contradictory observation schema")

    def _disable(self, operation: str, error: Exception) -> None:
        connection, self._connection = self._connection, None
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
        if not self._failed:
            self._failed = True
            try:
                print(f"Interaction observation disabled: {operation} failed "
                      f"({type(error).__name__[:64]}).", file=sys.stderr)
            except Exception:
                # Diagnostic-channel failure must also remain private and inert.
                pass

    def begin_session(self, interface_identity: dict, session_metadata: object = None) -> None:
        if self._connection is None:
            return
        try:
            if self._session is not None:
                raise ValueError("Observation session already begun")
            with self._connection:
                cursor = self._connection.execute(
                    "INSERT INTO sessions (started_at, interface_version, catalog_digest, "
                    "schema_digest, purpose, session_metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
                    (_now(), interface_identity["interface_version"],
                     interface_identity["catalog_digest"], interface_identity["schema_digest"],
                     interface_identity["purpose"],
                     None if session_metadata is None else json.dumps(session_metadata)),
                )
                self._session = cursor.lastrowid
        except Exception as error:
            self._disable("session creation", error)

    def record_request(self, request: object) -> int | None:
        if self._connection is None:
            return None
        try:
            self._sequence += 1
            with self._connection:
                cursor = self._connection.execute(
                    "INSERT INTO interactions (session_id, sequence_number, observed_at, "
                    "request_json) VALUES (?, ?, ?, ?)",
                    (self._session, self._sequence, _now(), json.dumps(request)),
                )
            return cursor.lastrowid
        except Exception as error:
            self._disable("request write", error)
            return None

    def record_response_metadata(self, interaction: int | None, metadata: object) -> None:
        if self._connection is None or interaction is None:
            return
        try:
            with self._connection:
                self._connection.execute(
                    "UPDATE interactions SET response_metadata_json = ? "
                    "WHERE id = ? AND session_id = ?",
                    (json.dumps(metadata), interaction, self._session),
                )
        except Exception as error:
            self._disable("metadata write", error)

    def close(self) -> None:
        if self._connection is None:
            return
        try:
            if self._session is not None:
                with self._connection:
                    self._connection.execute(
                        "UPDATE sessions SET ended_at = ? WHERE id = ?", (_now(), self._session)
                    )
            self._connection.close()
            self._connection = None
        except Exception as error:
            self._disable("close", error)
