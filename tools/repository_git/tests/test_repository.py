from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.repository_git.repository_git import (
    GitRepository,
    GitRepositoryError,
    GitlinkRepository,
    RepositoryPath,
    git_output,
    indexed_paths,
    sanitized_git_environment,
    staged_name_status,
)


class GitRepositoryTests(unittest.TestCase):
    def test_current_capture_is_exact_after_worktree_and_head_change(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "nested").mkdir()
            (root / "nested" / "é.txt").write_bytes(b"exact\x00bytes")
            (root / "other.txt").write_bytes(b"other")
            self._commit(root, "initial")

            repository = GitRepository(root)
            capture = repository.capture_current(
                (
                    RepositoryPath.parse("other.txt"),
                    RepositoryPath.parse("nested/é.txt"),
                )
            )
            self.assertEqual(
                [(str(item.path), item.content) for item in capture.files],
                [("nested/é.txt", b"exact\x00bytes"), ("other.txt", b"other")],
            )

            (root / "other.txt").write_bytes(b"worktree mutation")
            self.assertEqual(
                repository.read_file(
                    capture.revision, RepositoryPath.parse("other.txt")
                ),
                b"other",
            )
            self._commit(root, "next")
            self.assertNotEqual(repository.current_revision(), capture.revision)
            self.assertEqual(
                repository.read_file(
                    capture.revision, RepositoryPath.parse("other.txt")
                ),
                b"other",
            )

    def test_path_and_object_failures_are_typed(self) -> None:
        for raw in ("", "/absolute", "../outside", "a//b", ".git/config"):
            with self.subTest(raw=raw), self.assertRaises(GitRepositoryError) as raised:
                RepositoryPath.parse(raw)
            self.assertEqual(raised.exception.failure.kind, "invalid")

        with self.assertRaises(GitRepositoryError) as relative:
            GitRepository(Path("relative"))
        self.assertEqual(relative.exception.failure.code, "REPOSITORY_GIT.INVALID_ROOT")
        with self.assertRaises(GitRepositoryError) as components:
            RepositoryPath("ambiguous")
        self.assertEqual(
            components.exception.failure.code, "REPOSITORY_GIT.INVALID_PATH"
        )

        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "target").write_bytes(b"target")
            os.symlink("target", root / "link")
            self._commit(root, "fixture")
            repository = GitRepository(root)
            revision = repository.current_revision()

            with self.assertRaises(GitRepositoryError) as missing:
                repository.read_file(revision, RepositoryPath.parse("absent"))
            self.assertEqual(missing.exception.failure.kind, "unavailable")
            self.assertEqual(
                missing.exception.failure.code, "REPOSITORY_GIT.OBJECT_UNAVAILABLE"
            )

            with self.assertRaises(GitRepositoryError) as symlink:
                repository.read_file(revision, RepositoryPath.parse("link"))
            self.assertEqual(symlink.exception.failure.kind, "unsupported")
            self.assertEqual(
                symlink.exception.failure.code, "REPOSITORY_GIT.NON_REGULAR_FILE"
            )

    def test_explicit_gitlink_repository_is_traversed(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            nested = root / "nested"
            parent = root / "parent"
            nested.mkdir()
            parent.mkdir()
            self._initialize(nested)
            self._initialize(parent)
            (nested / "file.txt").write_bytes(b"nested")
            self._commit(nested, "nested")
            nested_revision = self._git(nested, "rev-parse", "HEAD").strip()
            self._git(
                parent,
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{nested_revision},vendor",
            )
            self._git(parent, "commit", "-qm", "parent")

            repository = GitRepository(
                parent,
                (GitlinkRepository(RepositoryPath.parse("vendor"), nested),),
            )
            capture = repository.capture_current(
                (RepositoryPath.parse("vendor/file.txt"),)
            )
            self.assertEqual(capture.files[0].content, b"nested")

            unmapped = GitRepository(parent)
            with self.assertRaises(GitRepositoryError) as raised:
                unmapped.capture_current((RepositoryPath.parse("vendor/file.txt"),))
            self.assertEqual(
                raised.exception.failure.code, "REPOSITORY_GIT.GITLINK_UNMAPPED"
            )

    def test_index_observations_are_exact_and_nul_delimited(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "a.txt").write_bytes(b"a")
            (root / "é.txt").write_bytes(b"e")
            self._commit(root, "initial")
            self.assertEqual(indexed_paths(root), ("a.txt", "é.txt"))

            (root / "a.txt").write_bytes(b"changed")
            self._git(root, "add", "a.txt")
            self.assertEqual(
                staged_name_status(root, "HEAD", ("a.txt",)), ("M", "a.txt")
            )

    def test_environment_and_output_are_bounded(self) -> None:
        original = dict(os.environ)
        try:
            os.environ["GIT_DIR"] = "/hostile"
            os.environ["git_config"] = "/hostile-lower"
            os.environ["PRESERVED"] = "yes"
            selected = sanitized_git_environment()
        finally:
            os.environ.clear()
            os.environ.update(original)

        self.assertNotIn("GIT_DIR", selected)
        self.assertNotIn("git_config", selected)
        self.assertEqual(selected["PRESERVED"], "yes")
        self.assertEqual(selected["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(selected["GIT_CONFIG_NOSYSTEM"], "1")

        with self.assertRaises(GitRepositoryError) as raised:
            git_output(Path.cwd(), ("version",), max_output_bytes=2)
        self.assertEqual(raised.exception.failure.kind, "unsupported")
        self.assertEqual(raised.exception.failure.code, "REPOSITORY_GIT.OUTPUT_LIMIT")

        with self.assertRaises(GitRepositoryError) as invalid_argument:
            git_output(Path.cwd(), ("version\0invalid",))
        self.assertEqual(
            invalid_argument.exception.failure.code,
            "REPOSITORY_GIT.INVALID_COMMAND",
        )

    @classmethod
    def _initialize(cls, root: Path) -> None:
        cls._git(root, "init", "-q")
        cls._git(root, "config", "user.email", "test@example.invalid")
        cls._git(root, "config", "user.name", "Test")

    @classmethod
    def _commit(cls, root: Path, message: str) -> None:
        cls._git(root, "add", "-A")
        cls._git(root, "commit", "-qm", message)

    @staticmethod
    def _git(root: Path, *arguments: str) -> str:
        return subprocess.run(
            ("git", "-C", str(root), *arguments),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout


if __name__ == "__main__":
    unittest.main()
