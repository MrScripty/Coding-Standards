from __future__ import annotations

import hashlib
import os
import sqlite3
import tempfile
from collections.abc import Iterable
from pathlib import Path

from .errors import invalid, unavailable, unsupported
from .model import CodecSet, RecoveryReceipt
from .repository import AuthorityRepository
from .store import SQLiteObjectStore


class SQLiteRecovery:
    def __init__(self, codec_sets: Iterable[CodecSet]) -> None:
        self._codec_sets = tuple(codec_sets)

    def backup(self, source: Path, absent_destination: Path) -> RecoveryReceipt:
        return self._copy_verified(source, absent_destination)

    def restore(self, backup: Path, absent_destination: Path) -> RecoveryReceipt:
        return self._copy_verified(backup, absent_destination)

    def _copy_verified(self, source: Path, destination: Path) -> RecoveryReceipt:
        _validate_locations(source, destination)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            suffix=".unpublished",
            dir=destination.parent,
        )
        os.close(descriptor)
        unpublished = Path(temporary_name)
        try:
            with SQLiteObjectStore(source, read_only=True) as source_store:
                AuthorityRepository(source_store, self._codec_sets)._verify_all_stored()
                destination_connection = sqlite3.connect(
                    unpublished, isolation_level=None, timeout=5.0
                )
                try:
                    source_store._connection.backup(destination_connection)
                finally:
                    destination_connection.close()
            source_digest = _file_digest(source)
            with SQLiteObjectStore(unpublished) as destination_store:
                AuthorityRepository(
                    destination_store, self._codec_sets
                )._verify_all_stored()
            destination_digest = _file_digest(unpublished)
            try:
                os.link(unpublished, destination)
            except FileExistsError as error:
                raise invalid(
                    "STORE.DESTINATION_EXISTS",
                    "recovery destination must remain absent until publication",
                ) from error
            except OSError as error:
                raise unavailable("STORE.PUBLICATION_UNAVAILABLE", str(error)) from error
        except Exception:
            raise
        finally:
            _remove_unpublished(unpublished)
        return RecoveryReceipt(
            str(source), str(destination), source_digest, destination_digest
        )


def default_store_path(repository_root: Path) -> Path:
    if not repository_root.is_absolute():
        raise invalid("STORE.RELATIVE_ROOT", "repository root must be absolute")
    return repository_root / ".standards-engine" / "authority.sqlite3"


def verify_sqlite_capabilities() -> tuple[str, tuple[str, ...]]:
    if sqlite3.sqlite_version_info < (3, 31, 0):
        raise unsupported(
            "STORE.SQLITE_VERSION_UNSUPPORTED",
            f"SQLite {sqlite3.sqlite_version} is older than 3.31.0",
        )
    if sqlite3.threadsafety != 3:
        raise unsupported(
            "STORE.SQLITE_THREADSAFETY_UNSUPPORTED",
            f"sqlite3.threadsafety must be 3, observed {sqlite3.threadsafety}",
        )
    connection = sqlite3.connect(":memory:")
    try:
        options = tuple(
            row[0] for row in connection.execute("PRAGMA compile_options").fetchall()
        )
    finally:
        connection.close()
    if "THREADSAFE=1" not in options:
        raise unsupported(
            "STORE.SQLITE_COMPILE_OPTIONS_UNSUPPORTED", "THREADSAFE=1 is required"
        )
    return sqlite3.sqlite_version, options


def _validate_locations(source: Path, destination: Path) -> None:
    if not source.is_absolute() or not destination.is_absolute():
        raise invalid("STORE.RELATIVE_PATH", "recovery paths must be absolute")
    if not source.is_file():
        raise unavailable("STORE.SOURCE_UNAVAILABLE", f"{source} is unavailable")
    if destination.exists():
        raise invalid("STORE.DESTINATION_EXISTS", "recovery destination must be absent")
    try:
        if source.parent.stat().st_dev != destination.parent.stat().st_dev:
            raise unsupported(
                "STORE.CROSS_MOUNT_RECOVERY",
                "source and destination must be on one admitted local mount",
            )
    except OSError as error:
        raise unavailable("STORE.LOCATION_UNAVAILABLE", str(error)) from error


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise unavailable("STORE.LOCATION_UNAVAILABLE", str(error)) from error
    return digest.hexdigest()


def _remove_unpublished(path: Path) -> None:
    for candidate in (
        path,
        Path(f"{path}-journal"),
        Path(f"{path}-wal"),
        Path(f"{path}-shm"),
    ):
        try:
            candidate.unlink(missing_ok=True)
        except OSError:
            pass


__all__ = ("SQLiteRecovery", "default_store_path", "verify_sqlite_capabilities")
