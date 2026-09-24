"""Real pipe/process failures and exact-revision retention boundaries."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.repository_git.repository_git import GitRepository, GitRepositoryError, RepositoryPath
from tools.repository_git.repository_git import repository as repo_module
from tools.repository_git.repository_git.batch import VerifiedBatchReader


class BatchReaderTest(unittest.TestCase):
    def reader(self, script: str, **options):
        reader = VerifiedBatchReader(
            (sys.executable, "-u", "-c", script), environment=dict(os.environ),
            object_limit=options.get("object_limit", 1024),
            stderr_limit=options.get("stderr_limit", 1024),
            timeout=options.get("timeout", 3),
        )
        self.addCleanup(reader.abort)
        return reader

    def assert_released(self, reader):
        self.assertIsNotNone(reader._process.poll())
        self.assertFalse(reader._worker.is_alive())
        self.assertFalse(reader._drainer.is_alive())
        self.assertTrue(reader._process.stdin.closed)
        self.assertTrue(reader._process.stdout.closed)
        self.assertTrue(reader._process.stderr.closed)

    @staticmethod
    def response(header: bytes, body: bytes):
        return ("import sys; sys.stdin.buffer.readline(); "
                f"sys.stdout.buffer.write({header + body!r}); sys.stdout.buffer.flush()")

    def test_fragmented_frames_and_one_owned_process(self):
        content = b"a\x00\n\xff"
        oid = hashlib.sha1(b"blob 4\0" + content).hexdigest()
        script = ("import sys,os\nfor line in sys.stdin.buffer:\n"
                  f" data=line.strip()+b' blob 4\\n'+{content!r}+b'\\n'\n"
                  " for byte in data: os.write(1,bytes([byte]))\n")
        reader = self.reader(script)
        pid = reader._process.pid
        for _ in range(20):
            self.assertEqual(reader.read(oid, "blob", "sha1"), content)
            self.assertEqual(reader._process.pid, pid)
        reader.close()
        reader.close()
        self.assert_released(reader)

    def test_missing_type_size_truncation_and_hash_failures(self):
        oid = "a" * 40
        cases = [
            (f"{oid} missing\n".encode(), b"", "REPOSITORY_GIT.OBJECT_UNAVAILABLE"),
            (b"contradiction\n", b"", "REPOSITORY_GIT.INVALID_OBJECT"),
            (b"x" * 257, b"", "REPOSITORY_GIT.INVALID_OBJECT"),
            (f"{oid} tree 0\n".encode(), b"\n", "REPOSITORY_GIT.TYPE_MISMATCH"),
            (f"{oid} blob 2048\n".encode(), b"", "REPOSITORY_GIT.OBJECT_LIMIT"),
            (f"{oid} blob -1\n".encode(), b"", "REPOSITORY_GIT.OBJECT_LIMIT"),
            (f"{oid} blob two\n".encode(), b"", "REPOSITORY_GIT.INVALID_OBJECT"),
            (f"{oid} blob 2\n".encode(), b"a", "REPOSITORY_GIT.INVALID_OBJECT"),
            (f"{oid} blob 2\n".encode(), b"ab!", "REPOSITORY_GIT.INVALID_OBJECT"),
            (f"{oid} blob 2\n".encode(), b"ab\n", "REPOSITORY_GIT.HASH_MISMATCH"),
        ]
        for header, body, code in cases:
            with self.subTest(code=code, header=header):
                reader = self.reader(self.response(header, body))
                with self.assertRaises(GitRepositoryError) as raised:
                    reader.read(oid, "blob", "sha1")
                self.assertEqual(raised.exception.failure.code, code)
                self.assert_released(reader)

    def test_stderr_overflow_drains_without_deadlock(self):
        reader = self.reader("import sys; sys.stdin.buffer.readline(); sys.stderr.buffer.write(b'x'*1000000); sys.stderr.flush(); sys.stdin.read()")
        with self.assertRaises(GitRepositoryError) as raised:
            reader.read("a" * 40, "blob", "sha1")
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.OUTPUT_LIMIT")
        self.assertLessEqual(len(reader._stderr), 1024)
        self.assert_released(reader)

    def test_exchange_timeout_kills_and_reaps_without_capture_deadline(self):
        reader = self.reader("import sys; sys.stdin.buffer.readline(); sys.stdin.read()", timeout=0.25)
        with self.assertRaises(GitRepositoryError) as raised:
            reader.read("a" * 40, "blob", "sha1")
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.COMMAND_TIMEOUT")
        self.assert_released(reader)

    def test_close_checks_trailing_data_and_exit_status(self):
        oid = hashlib.sha1(b"blob 0\0").hexdigest()
        for suffix, code in [("; sys.stdout.buffer.write(b'extra');sys.stdout.buffer.flush()", "REPOSITORY_GIT.INVALID_OBJECT"),
                             ("; sys.exit(7)", "REPOSITORY_GIT.COMMAND_UNAVAILABLE")]:
            reader = self.reader(self.response(f"{oid} blob 0\n".encode(), b"\n") + suffix)
            self.assertEqual(reader.read(oid, "blob", "sha1"), b"")
            with self.assertRaises(GitRepositoryError) as raised:
                reader.close()
            self.assertEqual(raised.exception.failure.code, code)
            self.assert_released(reader)

    def test_caller_interrupt_reaps_worker_and_process(self):
        reader = self.reader("import sys; sys.stdin.read()")
        original = reader._perform
        def interrupted():
            raise KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            original(interrupted)
        self.assert_released(reader)

    def test_nonzero_early_exit_retains_command_failure(self):
        reader = self.reader("import sys; sys.stdin.buffer.readline(); sys.stderr.write('stopped'); sys.exit(7)")
        with self.assertRaises(GitRepositoryError) as raised:
            reader.read("a" * 40, "blob", "sha1")
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.COMMAND_UNAVAILABLE")
        self.assert_released(reader)

    def test_shutdown_timeout_reaps_process(self):
        reader = self.reader("import sys,threading; sys.stdin.read(); threading.Event().wait()", timeout=0.25)
        with self.assertRaises(GitRepositoryError) as raised:
            reader.close()
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.COMMAND_TIMEOUT")
        self.assert_released(reader)

    def test_child_start_failure_is_typed(self):
        with patch("tools.repository_git.repository_git.batch.subprocess.Popen", side_effect=FileNotFoundError):
            with self.assertRaises(GitRepositoryError) as raised:
                self.reader("")
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.EXECUTABLE_UNAVAILABLE")


class CaptureSessionTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.root / "sub").mkdir()
        for i in range(12):
            (self.root / "sub" / f"{i}.txt").write_bytes(str(i).encode())
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.repo = GitRepository(self.root)
        self.revision = self.repo.current_revision()

    def git(self, *args):
        return subprocess.check_output(("git", "-C", str(self.root), *args))

    def test_shared_tree_is_parsed_once_and_child_ends_with_owner(self):
        with patch.object(repo_module, "_tree_entries", wraps=repo_module._tree_entries) as parse:
            with self.repo.read_session(self.revision) as session:
                for _ in range(2):
                    for i in range(12):
                        self.assertEqual(session.read_file(RepositoryPath.parse(f"sub/{i}.txt")), str(i).encode())
                reader = session._reader[1]
                self.assertEqual(parse.call_count, 2)  # root and sub tree
                raw = sum(len(item.content) for item in session._objects.values())
                self.assertGreater(session.cached_bytes, raw)
                self.assertLessEqual(session.cached_bytes, 8 * 1024 * 1024)
        self.assertIsNotNone(reader._process.returncode)
        self.assertFalse(reader._worker.is_alive())
        self.assertFalse(reader._drainer.is_alive())
        self.assertEqual(session.cached_bytes, 0)

    def test_zero_retention_keeps_batching_and_complete_validation(self):
        with self.repo.read_session(self.revision, max_cached_objects=0) as session:
            session.read_file(RepositoryPath.parse("sub/1.txt"))
            reader = session._reader[1]
            for i in range(12):
                self.assertEqual(session.read_file(RepositoryPath.parse(f"sub/{i}.txt")), str(i).encode())
                self.assertIs(session._reader[1], reader)
            self.assertEqual(session.cached_objects, 0)
            self.assertEqual(session.cached_bytes, 0)

    def test_decoded_tree_budget_and_exception_cleanup(self):
        for budget in (128, 512, 1024):
            with self.subTest(budget=budget):
                session = self.repo.read_session(self.revision, max_cached_bytes=budget)
                with self.assertRaisesRegex(RuntimeError, "consumer failed"):
                    with session:
                        for i in range(12):
                            self.assertEqual(session.read_file(RepositoryPath.parse(f"sub/{i}.txt")), str(i).encode())
                            self.assertLessEqual(session.cached_bytes, budget)
                        reader = session._reader[1]
                        raise RuntimeError("consumer failed")
                self.assertEqual(session.cached_objects, 0)
                self.assertIsNotNone(reader._process.returncode)
