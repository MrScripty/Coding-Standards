from __future__ import annotations

import sqlite3
import os
import subprocess
import sys
import tempfile
import time
import unittest
import multiprocessing
import uuid
from pathlib import Path
from unittest.mock import patch

from tools.standards_authority.standards_authority import (
    AuthorityEnvelope,
    AuthorityError,
    AuthorityReference,
    AuthorityRepository,
    CodecSet,
    ContentSnapshot,
    ContentSnapshotCodec,
    MemoryObjectStore,
    SQLiteObjectStore,
    SQLiteRecovery,
    SnapshotFile,
    RepositoryPath,
    decode_envelope,
    encode_envelope,
)


class SQLiteStoreTests(unittest.TestCase):
    def test_schema_profile_idempotence_immutability_and_cold_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            envelope = AuthorityEnvelope("fixture", "opaque", (), "fixture.v1", None)
            encoded = encode_envelope(envelope)
            with SQLiteObjectStore(path) as store:
                self.assertEqual(
                    store.put_if_absent(envelope.handle, encoded), "inserted"
                )
                self.assertEqual(
                    store.put_if_absent(envelope.handle, encoded), "existing-identical"
                )
                self.assertEqual(decode_envelope(store.get(envelope.handle)), envelope)
                with self.assertRaises(sqlite3.IntegrityError):
                    store._connection.execute(
                        "UPDATE authority_objects SET envelope=x'00'"
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    store._connection.execute("DELETE FROM authority_objects")
            with SQLiteObjectStore(path) as reopened:
                self.assertEqual(reopened.get(envelope.handle), encoded)
                self.assertEqual(
                    reopened._connection.execute("PRAGMA application_id").fetchone()[0],
                    1_397_047_601,
                )
                self.assertEqual(
                    reopened._connection.execute("PRAGMA user_version").fetchone()[0], 1
                )

    def test_collision_and_missing_are_typed(self) -> None:
        store = MemoryObjectStore()
        envelope = AuthorityEnvelope("fixture", "opaque", (), "fixture.v1", None)
        store.put_if_absent(envelope.handle, encode_envelope(envelope))
        with self.assertRaises(AuthorityError) as collision:
            store.put_if_absent(envelope.handle, b"different")
        self.assertEqual(collision.exception.failure.code, "IDENTITY.COLLISION")

    def test_concurrent_identical_and_conflicting_writers_converge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            with SQLiteObjectStore(path):
                pass
            first = AuthorityEnvelope("fixture", "shared", (), "fixture.v1", "one")
            identical = self._concurrent_puts(path, (first, first))
            self.assertEqual(sorted(identical), ["existing-identical", "inserted"])
            conflict_one = AuthorityEnvelope(
                "fixture", "conflict", (), "fixture.v1", "one"
            )
            conflict_two = AuthorityEnvelope(
                "fixture", "conflict", (), "fixture.v1", "two"
            )
            conflicting = self._concurrent_puts(path, (conflict_one, conflict_two))
            self.assertEqual(sorted(conflicting), ["IDENTITY.COLLISION", "inserted"])

    @staticmethod
    def _concurrent_puts(
        path: Path, envelopes: tuple[AuthorityEnvelope, AuthorityEnvelope]
    ) -> list[str]:
        context = multiprocessing.get_context("fork")
        barrier = context.Barrier(2)
        queue = context.Queue()
        processes = [
            context.Process(
                target=_put_worker,
                args=(path, encode_envelope(envelope), barrier, queue),
            )
            for envelope in envelopes
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join(10)
            if process.is_alive():
                process.kill()
                process.join()
                raise AssertionError("coordinated writer did not terminate")
            if process.exitcode != 0:
                raise AssertionError(f"writer exited with {process.exitcode}")
        return [queue.get(timeout=1) for _ in processes]

    def test_busy_timeout_has_no_application_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            first = SQLiteObjectStore(path)
            second = SQLiteObjectStore(path)
            envelope = AuthorityEnvelope("fixture", "busy", (), "fixture.v1", None)
            readable = AuthorityEnvelope("fixture", "readable", (), "fixture.v1", None)
            try:
                first.put_if_absent(readable.handle, encode_envelope(readable))
                first._connection.execute("BEGIN IMMEDIATE")
                self.assertEqual(second.get(readable.handle), encode_envelope(readable))
                started = time.monotonic()
                with self.assertRaises(AuthorityError) as raised:
                    second.put_if_absent(envelope.handle, encode_envelope(envelope))
                elapsed = time.monotonic() - started
                self.assertEqual(raised.exception.failure.code, "STORE.BUSY")
                self.assertGreaterEqual(elapsed, 4.5)
                self.assertLess(elapsed, 6.5)
            finally:
                first._connection.execute("ROLLBACK")
                first.close()
                second.close()

    def test_backup_restore_and_cold_process_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.sqlite3"
            backup = root / "backup.sqlite3"
            restored = root / "restored.sqlite3"
            codec = ContentSnapshotCodec()
            snapshot = ContentSnapshot(
                (SnapshotFile(RepositoryPath(("file.txt",)), b"durable"),)
            )
            with SQLiteObjectStore(source) as store:
                repository = AuthorityRepository(store, (CodecSet("test", (codec,)),))
                repository.publish(codec, snapshot)
                handle = repository.resolve_reference(
                    AuthorityReference(
                        "content-snapshot",
                        codec.semantic_id(snapshot, repository),  # type: ignore[arg-type]
                    )
                ).handle
            recovery = SQLiteRecovery((CodecSet("test", (codec,)),))
            recovery.backup(source, backup)
            recovery.restore(backup, restored)
            script = (
                "from pathlib import Path; "
                "from tools.standards_authority.standards_authority import *; "
                f"s=SQLiteObjectStore(Path({str(restored)!r})); "
                "r=AuthorityRepository(s,(CodecSet('test', (ContentSnapshotCodec(),)),)); "
                f"print(r.resolve(AuthorityHandle({handle.object_kind!r}, {handle.semantic_id!r})).handle.semantic_id); "
                "s.close()"
            )
            output = subprocess.run(
                (sys.executable, "-c", script),
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            self.assertEqual(output, handle.semantic_id)
            with self.assertRaises(AuthorityError) as exists:
                recovery.restore(backup, restored)
            self.assertEqual(exists.exception.failure.code, "STORE.DESTINATION_EXISTS")

    def test_failed_restore_does_not_change_source_or_publish_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.sqlite3"
            backup = root / "backup.sqlite3"
            destination = root / "destination.sqlite3"
            codec = ContentSnapshotCodec()
            snapshot = ContentSnapshot(
                (SnapshotFile(RepositoryPath(("file.txt",)), b"retained"),)
            )
            with SQLiteObjectStore(source) as store:
                AuthorityRepository(store, (CodecSet("test", (codec,)),)).publish(
                    codec, snapshot
                )
            recovery = SQLiteRecovery((CodecSet("test", (codec,)),))
            recovery.backup(source, backup)
            bytes_before = source.read_bytes()
            corrupted = bytearray(backup.read_bytes())
            corrupted[0] ^= 0xFF
            backup.write_bytes(corrupted)
            with self.assertRaises(AuthorityError):
                recovery.restore(backup, destination)
            self.assertFalse(destination.exists())
            self.assertEqual(source.read_bytes(), bytes_before)
            with SQLiteObjectStore(source) as reopened:
                AuthorityRepository(
                    reopened, (CodecSet("test", (codec,)),)
                )._verify_all_stored()

    def test_raced_destination_is_not_overwritten_or_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.sqlite3"
            destination = root / "destination.sqlite3"
            with SQLiteObjectStore(source):
                pass
            recovery = SQLiteRecovery((CodecSet("test", ()),))
            raced_content = b"another owner created this destination"
            real_link = os.link

            def create_destination_then_link(source_path, destination_path):
                Path(destination_path).write_bytes(raced_content)
                return real_link(source_path, destination_path)

            with patch(
                "tools.standards_authority.standards_authority.recovery.os.link",
                side_effect=create_destination_then_link,
            ):
                with self.assertRaises(AuthorityError) as raised:
                    recovery.backup(source, destination)

            self.assertEqual(raised.exception.failure.code, "STORE.DESTINATION_EXISTS")
            self.assertEqual(destination.read_bytes(), raced_content)

    def test_cross_mount_recovery_rejects_before_destination_creation(self) -> None:
        shared_memory = Path("/dev/shm")
        if (
            not shared_memory.is_dir()
            or shared_memory.stat().st_dev == Path("/tmp").stat().st_dev
        ):
            self.skipTest("no distinct local mount available")
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            source = Path(temporary) / "source.sqlite3"
            with SQLiteObjectStore(source):
                pass
            destination = shared_memory / f"a1b-{uuid.uuid4().hex}.sqlite3"
            recovery = SQLiteRecovery((CodecSet("test", ()),))
            with self.assertRaises(AuthorityError) as raised:
                recovery.backup(source, destination)
            self.assertEqual(raised.exception.failure.kind, "unsupported")
            self.assertFalse(destination.exists())

    def test_newer_schema_is_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            with SQLiteObjectStore(path) as store:
                store._connection.execute("PRAGMA user_version=2")
            with self.assertRaises(AuthorityError) as raised:
                SQLiteObjectStore(path)
            self.assertEqual(raised.exception.failure.kind, "unsupported")

    def test_parallel_schema_authority_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "authority.sqlite3"
            with SQLiteObjectStore(path) as store:
                store._connection.execute("CREATE TABLE shadow_authority(value TEXT)")
            with self.assertRaises(AuthorityError) as raised:
                SQLiteObjectStore(path)
            self.assertEqual(raised.exception.failure.code, "STORE.INVALID_SCHEMA")


def _put_worker(
    path: Path,
    encoded: bytes,
    barrier: multiprocessing.synchronize.Barrier,
    queue: multiprocessing.queues.Queue,
) -> None:
    envelope = decode_envelope(encoded)
    try:
        with SQLiteObjectStore(path) as store:
            barrier.wait()
            queue.put(store.put_if_absent(envelope.handle, encoded))
    except AuthorityError as error:
        queue.put(error.failure.code)


if __name__ == "__main__":
    unittest.main()
