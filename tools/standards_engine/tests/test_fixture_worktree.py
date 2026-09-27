"""Disposable source fixtures must represent additions and removals together."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.tests import test_analysis as fixtures


class TrackedWorktreeFixtureTest(unittest.TestCase):
    def test_clone_preserves_the_current_tracked_write_set_including_deletion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, destination = root / "source", root / "destination"
            source.mkdir()
            def git(*arguments):
                return subprocess.check_output(["git", "-C", str(source), *arguments])
            git("init", "-q", "-b", "main")
            (source / "removed.py").write_text("old implementation\n")
            (source / "retained.py").write_text("original\n")
            git("add", ".")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-qm", "fixture base")
            git("rm", "removed.py")
            (source / "replacement.py").write_text("new implementation\n")
            (source / "retained.py").write_text("current worktree bytes\n")
            (source / "unrelated.zip").write_text("untracked user work\n")
            git("add", "replacement.py")
            before = git("status", "--porcelain=v1", "-z")
            with patch.object(fixtures, "REPO_ROOT", source):
                fixtures._clone_tracked_worktree(destination)
            self.assertFalse((destination / "removed.py").exists())
            self.assertFalse((destination / "unrelated.zip").exists())
            self.assertEqual((destination / "replacement.py").read_text(), "new implementation\n")
            self.assertEqual((destination / "retained.py").read_text(), "current worktree bytes\n")
            self.assertEqual(git("status", "--porcelain=v1", "-z"), before)
            self.assertEqual(subprocess.check_output(["git", "-C", str(destination),
                "status", "--porcelain=v1"]), b"")
