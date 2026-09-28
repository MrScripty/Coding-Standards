from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.repository_git.repository_git import GitRepository, GitRepositoryError, RepositoryPath, RepositoryRevision


class ReviewMetadataTests(unittest.TestCase):
    def test_exact_modes_and_commit_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args: str) -> str:
                return subprocess.check_output(("git", "-C", str(root), *args), text=True).strip()
            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.test")
            (root / "regular.txt").write_bytes(b"regular")
            executable = root / "script.sh"
            executable.write_bytes(b"#!/bin/sh\n")
            executable.chmod(0o755)
            git("add", ".")
            git("commit", "-qm", "fixture")
            revision = RepositoryRevision(git("rev-parse", "HEAD"))
            entries = GitRepository(root).revision_entries(revision, local_only=True)
            self.assertEqual(entries[RepositoryPath.parse("regular.txt")][0], "100644")
            self.assertEqual(entries[RepositoryPath.parse("script.sh")][0], "100755")
            self.assertEqual(entries[RepositoryPath.parse("regular.txt")][1], git("rev-parse", "HEAD:regular.txt"))
            with self.assertRaises(GitRepositoryError):
                GitRepository(root).revision_entries(RepositoryRevision(git("rev-parse", "HEAD^{tree}")), local_only=True)


if __name__ == "__main__":
    unittest.main()
