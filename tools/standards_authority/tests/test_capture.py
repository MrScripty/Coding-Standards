from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.standards_authority.standards_authority import (
    AuthorityError,
    CaptureRequest,
    GitCaptureSource,
    GitlinkSource,
    NativeCaptureSource,
    RepositoryPath,
)


class _MutatingCapture(NativeCaptureSource):
    def __init__(self, root: Path, target: Path) -> None:
        super().__init__(root)
        self._target = target

    def _after_first_pass(self) -> None:
        self._target.write_bytes(b"changed")


class CaptureTests(unittest.TestCase):
    def test_git_and_native_capture_produce_equal_snapshots(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            (root / "nested").mkdir()
            (root / "nested" / "é.txt").write_bytes(b"exact\x00bytes")
            (root / "other.txt").write_bytes(b"other")
            self._git(root, "init", "-q")
            self._git(root, "config", "user.email", "test@example.invalid")
            self._git(root, "config", "user.name", "Test")
            self._git(root, "add", "nested/é.txt", "other.txt")
            self._git(root, "commit", "-qm", "fixture")
            request = CaptureRequest(
                (
                    RepositoryPath(("other.txt",)),
                    RepositoryPath(("nested", "é.txt")),
                )
            )
            git_snapshot = GitCaptureSource(root, "HEAD").capture(request)
            native_snapshot = NativeCaptureSource(root).capture(request)
            self.assertEqual(git_snapshot, native_snapshot)
            os.chmod(root / "other.txt", 0o755)
            os.utime(root / "other.txt", None)
            self.assertEqual(
                NativeCaptureSource(root).capture(request), native_snapshot
            )
            self._git(root, "add", "other.txt")
            self._git(root, "commit", "-qm", "mode-only")
            self.assertEqual(
                GitCaptureSource(root, "HEAD").capture(request), git_snapshot
            )
            (root / "other.txt").write_bytes(b"worktree mutation")
            self.assertEqual(
                GitCaptureSource(root, "HEAD").capture(request), git_snapshot
            )

    def test_native_endpoint_change_rejects_without_result(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            target = root / "file.txt"
            target.write_bytes(b"initial")
            request = CaptureRequest((RepositoryPath(("file.txt",)),))
            with self.assertRaises(AuthorityError) as raised:
                _MutatingCapture(root, target).capture(request)
            self.assertEqual(raised.exception.failure.code, "CAPTURE.SOURCE_CHANGED")

    def test_native_symlink_rejects(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            (root / "target").write_bytes(b"x")
            os.symlink("target", root / "link")
            request = CaptureRequest((RepositoryPath(("link",)),))
            with self.assertRaises(AuthorityError) as raised:
                NativeCaptureSource(root).capture(request)
            self.assertEqual(raised.exception.failure.kind, "unsupported")

    def test_explicit_gitlink_is_flattened_without_boundary_identity(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            nested = root / "nested-repository"
            parent = root / "parent-repository"
            nested.mkdir()
            parent.mkdir()
            (nested / "file.txt").write_bytes(b"nested")
            for repository in (nested, parent):
                self._git(repository, "init", "-q")
                self._git(repository, "config", "user.email", "test@example.invalid")
                self._git(repository, "config", "user.name", "Test")
            self._git(nested, "add", "file.txt")
            self._git(nested, "commit", "-qm", "nested")
            nested_oid = subprocess.run(
                ("git", "-C", str(nested), "rev-parse", "HEAD"),
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            self._git(
                parent,
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{nested_oid},vendor",
            )
            self._git(parent, "commit", "-qm", "parent")
            request = CaptureRequest((RepositoryPath(("vendor", "file.txt")),))
            snapshot = GitCaptureSource(
                parent,
                "HEAD",
                (GitlinkSource(RepositoryPath(("vendor",)), nested),),
            ).capture(request)
            self.assertEqual(snapshot.files[0].content, b"nested")
            self.assertEqual(snapshot.files[0].path.components, ("vendor", "file.txt"))

    def test_missing_and_corrupt_git_objects_have_distinct_failures(self) -> None:
        for corruption, expected_kind in (
            ("missing", "unavailable"),
            ("corrupt", "invalid"),
        ):
            with (
                self.subTest(corruption=corruption),
                tempfile.TemporaryDirectory(dir="/tmp") as temporary,
            ):
                root = Path(temporary)
                (root / "file.txt").write_bytes(b"content")
                self._git(root, "init", "-q")
                self._git(root, "config", "user.email", "test@example.invalid")
                self._git(root, "config", "user.name", "Test")
                self._git(root, "add", "file.txt")
                self._git(root, "commit", "-qm", "fixture")
                oid = subprocess.run(
                    ("git", "-C", str(root), "rev-parse", "HEAD"),
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                ).stdout.strip()
                object_path = root / ".git" / "objects" / oid[:2] / oid[2:]
                if corruption == "missing":
                    object_path.unlink()
                else:
                    os.chmod(object_path, 0o600)
                    object_path.write_bytes(b"not a Git object")
                request = CaptureRequest((RepositoryPath(("file.txt",)),))
                with self.assertRaises(AuthorityError) as raised:
                    GitCaptureSource(root, "HEAD").capture(request)
                self.assertEqual(raised.exception.failure.kind, expected_kind)

    @staticmethod
    def _git(root: Path, *arguments: str) -> None:
        subprocess.run(("git", "-C", str(root), *arguments), check=True)


if __name__ == "__main__":
    unittest.main()
