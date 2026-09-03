from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import tools.repository_git.repository_git.repository as repository_module

from tools.repository_git.repository_git import (
    CapturedFile,
    GitRepository,
    GitRepositoryError,
    GitRepositoryFailure,
    GitlinkRepository,
    MaterializedCandidate,
    RepositoryPath,
    RepositoryRevision,
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
            self.assertEqual(
                tuple(
                    str(path) for path in repository.revision_paths(capture.revision)
                ),
                ("nested/é.txt", "other.txt"),
            )

            (root / "other.txt").write_bytes(b"worktree mutation")
            self.assertEqual(
                repository.read_file(
                    capture.revision, RepositoryPath.parse("other.txt")
                ),
                b"other",
            )
            (root / "later.txt").write_bytes(b"later")
            self._commit(root, "next")
            self.assertNotEqual(repository.current_revision(), capture.revision)
            self.assertEqual(
                tuple(
                    str(path) for path in repository.revision_paths(capture.revision)
                ),
                ("nested/é.txt", "other.txt"),
            )
            self.assertEqual(
                tuple(
                    str(path)
                    for path in repository.revision_paths(repository.current_revision())
                ),
                ("later.txt", "nested/é.txt", "other.txt"),
            )
            self.assertEqual(
                repository.read_file(
                    capture.revision, RepositoryPath.parse("other.txt")
                ),
                b"other",
            )

    def test_branch_revision_is_independent_of_the_checked_out_head(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "value.txt").write_text("main", encoding="utf-8")
            self._commit(root, "main")
            self._git(root, "branch", "-M", "main")
            main = self._git(root, "rev-parse", "HEAD").strip()
            self._git(root, "switch", "-qc", "other")
            (root / "value.txt").write_text("other", encoding="utf-8")
            self._commit(root, "other")

            repository = GitRepository(root)

            self.assertNotEqual(repository.current_revision().oid, main)
            self.assertEqual(repository.branch_revision("main").oid, main)

    def test_candidate_is_isolated_and_published_by_expected_target(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "regular.txt").write_bytes(b"accepted\n")
            executable = root / "executable.sh"
            executable.write_bytes(b"#!/bin/sh\nexit 0\n")
            executable.chmod(0o755)
            magic = root / ":(exclude,glob)**"
            magic.write_bytes(b"accepted magic\n")
            self._commit(root, "initial")
            self._git(root, "branch", "-M", "main")
            repository = GitRepository(root)
            expected = repository.branch_revision("main")

            (root / "unrelated.txt").write_bytes(b"staged but unrelated\n")
            self._git(root, "add", "unrelated.txt")
            source_index = self._git(root, "write-tree").strip()
            source_status = self._git(root, "status", "--porcelain=v1", "-z")

            replacements = (
                CapturedFile(
                    RepositoryPath.parse(":(exclude,glob)**"),
                    b"proposed magic\n",
                ),
                CapturedFile(
                    RepositoryPath.parse("executable.sh"),
                    b"#!/bin/sh\nexit 7\n",
                ),
                CapturedFile(
                    RepositoryPath.parse("regular.txt"),
                    b"proposed\n",
                ),
            )
            forged = MaterializedCandidate(
                root,
                expected,
                RepositoryRevision("f" * 40),
            )
            with self.assertRaises(GitRepositoryError) as unissued:
                repository.publish_candidate(forged, expected)
            self.assertEqual(
                unissued.exception.failure.code,
                "REPOSITORY_GIT.INVALID_CANDIDATE",
            )
            with repository.materialize_candidate(expected, replacements) as candidate:
                self.assertEqual(candidate.expected, expected)
                self.assertEqual(
                    repository.branch_revision("main"),
                    expected,
                )
                self.assertEqual(self._git(root, "write-tree").strip(), source_index)
                self.assertEqual(
                    self._git(root, "status", "--porcelain=v1", "-z"),
                    source_status,
                )
                self.assertEqual(
                    (candidate.root / "regular.txt").read_bytes(),
                    b"proposed\n",
                )
                self.assertEqual(
                    (candidate.root / "executable.sh").read_bytes(),
                    b"#!/bin/sh\nexit 7\n",
                )
                self.assertEqual(
                    (candidate.root / ":(exclude,glob)**").read_bytes(),
                    b"proposed magic\n",
                )
                self.assertTrue(
                    (candidate.root / "executable.sh").stat().st_mode & 0o111
                )
                self.assertEqual(self._git(candidate.root, "remote"), "")
                first_revision = candidate.revision
                self.assertEqual(
                    self._git(candidate.root, "log", "-1", "--format=%B"),
                    "feat(standards): apply approved proposal\n\n",
                )

                with repository.materialize_candidate(
                    expected, replacements
                ) as repeated:
                    self.assertEqual(repeated.revision, first_revision)

                self.assertEqual(
                    repository.publish_candidate(candidate, expected),
                    "updated",
                )

            self.assertEqual(repository.branch_revision("main"), first_revision)
            self.assertEqual((root / "regular.txt").read_bytes(), b"accepted\n")
            self.assertEqual(self._git(root, "write-tree").strip(), source_index)

    def test_candidate_publication_rejects_stale_target_and_drift(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "value.txt").write_bytes(b"accepted\n")
            self._commit(root, "initial")
            self._git(root, "branch", "-M", "main")
            repository = GitRepository(root)
            expected = repository.branch_revision("main")
            replacement = CapturedFile(RepositoryPath.parse("value.txt"), b"proposed\n")

            with repository.materialize_candidate(expected, (replacement,)) as drifted:
                (drifted.root / "value.txt").write_bytes(b"unverified drift\n")
                with self.assertRaises(GitRepositoryError) as changed:
                    repository.publish_candidate(drifted, expected)
            self.assertEqual(
                changed.exception.failure.code,
                "REPOSITORY_GIT.CANDIDATE_DIVERGED",
            )
            self.assertEqual(repository.branch_revision("main"), expected)

            with repository.materialize_candidate(
                expected, (replacement,)
            ) as candidate:
                (root / "competing.txt").write_bytes(b"competing\n")
                self._commit(root, "competing")
                competing = repository.branch_revision("main")
                self.assertEqual(
                    repository.publish_candidate(candidate, expected),
                    "stale",
                )

            self.assertEqual(repository.branch_revision("main"), competing)

    def test_candidate_publication_loses_a_race_at_the_atomic_update(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "value.txt").write_bytes(b"accepted\n")
            self._commit(root, "initial")
            self._git(root, "branch", "-M", "main")
            repository = GitRepository(root)
            expected = repository.branch_revision("main")

            self._git(root, "switch", "-qc", "competing")
            (root / "competing.txt").write_bytes(b"competing\n")
            self._commit(root, "competing")
            competing = repository.current_revision()
            self._git(root, "switch", "-q", "main")
            replacement = CapturedFile(RepositoryPath.parse("value.txt"), b"proposed\n")
            original_git_command = repository_module.git_command

            with repository.materialize_candidate(
                expected, (replacement,)
            ) as candidate:
                raced = False

                def race_before_update(
                    command_root: Path,
                    arguments: tuple[str, ...],
                    **options: object,
                ):
                    nonlocal raced
                    if (
                        not raced
                        and arguments[:2] == ("update-ref", "refs/heads/main")
                        and arguments[2] == candidate.revision.oid
                    ):
                        raced = True
                        original_git_command(
                            root,
                            (
                                "update-ref",
                                "refs/heads/main",
                                competing.oid,
                                expected.oid,
                            ),
                            max_output_bytes=256,
                        )
                    return original_git_command(
                        command_root,
                        arguments,
                        **options,
                    )

                with mock.patch.object(
                    repository_module,
                    "git_command",
                    side_effect=race_before_update,
                ):
                    result = repository.publish_candidate(candidate, expected)

            self.assertTrue(raced)
            self.assertEqual(result, "stale")
            self.assertEqual(repository.branch_revision("main"), competing)

    def test_uncertain_update_preserves_recovery_required_authority(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as temporary:
            root = Path(temporary)
            self._initialize(root)
            (root / "value.txt").write_bytes(b"accepted\n")
            self._commit(root, "initial")
            self._git(root, "branch", "-M", "main")
            repository = GitRepository(root)
            expected = repository.branch_revision("main")

            self._git(root, "switch", "-qc", "competing")
            (root / "competing.txt").write_bytes(b"competing\n")
            self._commit(root, "competing")
            competing = repository.current_revision()
            self._git(root, "switch", "-q", "main")
            replacement = CapturedFile(RepositoryPath.parse("value.txt"), b"proposed\n")
            original_git_command = repository_module.git_command

            with repository.materialize_candidate(
                expected, (replacement,)
            ) as candidate:

                def interrupt_after_update(
                    command_root: Path,
                    arguments: tuple[str, ...],
                    **options: object,
                ):
                    if (
                        arguments[:2] == ("update-ref", "refs/heads/main")
                        and arguments[2] == candidate.revision.oid
                    ):
                        original_git_command(
                            root,
                            arguments,
                            **options,
                        )
                        original_git_command(
                            root,
                            (
                                "update-ref",
                                "refs/heads/main",
                                competing.oid,
                                candidate.revision.oid,
                            ),
                            max_output_bytes=256,
                        )
                        raise GitRepositoryError(
                            GitRepositoryFailure(
                                "unavailable",
                                "REPOSITORY_GIT.COMMAND_TIMEOUT",
                                "fixture command outcome is unknown",
                            )
                        )
                    return original_git_command(
                        command_root,
                        arguments,
                        **options,
                    )

                with (
                    mock.patch.object(
                        repository_module,
                        "git_command",
                        side_effect=interrupt_after_update,
                    ),
                    self.assertRaises(GitRepositoryError) as unavailable_outcome,
                ):
                    repository.publish_candidate(candidate, expected)

            self.assertEqual(
                unavailable_outcome.exception.failure.code,
                "REPOSITORY_GIT.PUBLICATION_OUTCOME_UNAVAILABLE",
            )
            self.assertEqual(repository.branch_revision("main"), competing)

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
