from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.review_evidence.review_evidence.cli import PacketError, build, digest


class PacketBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.repo = root / "source"
        self.repo.mkdir()
        self.evidence = root / "evidence"
        self.evidence.mkdir()
        self.out = root / "packet.zip"
        self.request_path = root / "request.json"
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        (self.repo / "plan.md").write_bytes(b"# Actual plan\n")
        (self.repo / "changed.bin").write_bytes(b"\x00first\xff")
        (self.repo / "gone.txt").write_bytes(b"gone\n")
        self.git("add", ".")
        self.git("commit", "-qm", "baseline")
        self.base = self.git("rev-parse", "HEAD").strip()
        (self.repo / "changed.bin").write_bytes(b"\x00second\xff")
        (self.repo / "gone.txt").unlink()
        (self.repo / "new.txt").write_bytes(b"new\n")
        self.git("add", ".")
        self.git("commit", "-qm", "candidate")
        self.candidate = self.git("rev-parse", "HEAD").strip()
        self.request = {
            "format_version": 1, "repository_label": "fixture", "label": "review",
            "review_question": "Inspect exact changed bytes", "revisions": {"baseline": self.base, "candidate": self.candidate},
            "plan": {"revision": "candidate", "path": "plan.md"}, "context": ["plan.md"],
            "comparisons": [], "artifacts": [], "claims": [],
        }

    def git(self, *args: str) -> str:
        return subprocess.check_output(("git", "-C", str(self.repo), *args), text=True)

    def write_request(self) -> None:
        self.request_path.write_text(json.dumps(self.request))

    def build(self) -> dict:
        self.write_request()
        return build(self.repo, self.request_path, self.evidence, self.out)

    def test_exact_versions_and_dirty_source_preserved(self) -> None:
        (self.repo / "changed.bin").write_bytes(b"dirty worktree")
        (self.repo / "untracked.zip").write_bytes(b"not source")
        before = self.git("status", "--porcelain=v1")
        result = self.build()
        self.assertEqual(result["status"], "built")
        self.assertEqual(self.git("status", "--porcelain=v1"), before)
        with zipfile.ZipFile(self.out) as archive:
            self.assertEqual(archive.read("source/baseline/changed.bin"), b"\x00first\xff")
            self.assertEqual(archive.read("source/candidate/changed.bin"), b"\x00second\xff")
            self.assertEqual(archive.read("source/baseline/gone.txt"), b"gone\n")
            self.assertNotIn("source/candidate/gone.txt", archive.namelist())
            self.assertEqual(archive.read("source/candidate/new.txt"), b"new\n")
            patch = archive.read("changes/baseline-candidate.patch")
            expected = subprocess.check_output(("git", "-C", str(self.repo), "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--binary", "--full-index", "--no-color", self.base, self.candidate, "--"))
            self.assertEqual(patch, expected)
            manifest = json.loads(archive.read("manifest.json"))
            self.assertEqual({item["path"] for item in manifest["primary"] if item["changed"]}, {"changed.bin", "gone.txt", "new.txt"})
            self.assertEqual(result["manifest_sha256"], digest(archive.read("manifest.json")))
            self.assertEqual({item["name"] for item in manifest["members"]}, set(archive.namelist()) - {"manifest.json"})

    def test_references_and_missing_file_are_gaps(self) -> None:
        self.request["artifacts"] = [
            {"id": "log", "role": "ci-log", "origin": {"kind": "local-file", "path": "ci/missing.log"}},
            {"id": "link", "role": "ci-reference", "origin": {"kind": "reference", "label": "run", "url": "https://example.test/run"}},
        ]
        result = self.build()
        self.assertEqual([item["availability"] for item in result["material_gaps"]], ["missing", "referenced"])
        with zipfile.ZipFile(self.out) as archive:
            self.assertFalse(any(name.startswith("evidence/") for name in archive.namelist()))

    def test_no_clobber_and_hash_contradiction(self) -> None:
        self.out.write_bytes(b"keep")
        with self.assertRaises(PacketError):
            self.build()
        self.assertEqual(self.out.read_bytes(), b"keep")
        self.out.unlink()
        (self.evidence / "log.txt").write_bytes(b"actual")
        self.request["artifacts"] = [{"id": "log", "role": "ci-log", "origin": {"kind": "local-file", "path": "log.txt", "expected_sha256": "sha256:" + "0" * 64}}]
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_unknown_claim_and_symlink_evidence_rejected(self) -> None:
        self.request["claims"] = [{"id": "C1", "artifacts": ["unknown"]}]
        with self.assertRaises(PacketError):
            self.build()
        self.request["claims"] = []
        (self.evidence / "link").symlink_to(self.repo / "changed.bin")
        self.request["artifacts"] = [{"id": "link", "role": "ci-log", "origin": {"kind": "local-file", "path": "link"}}]
        with self.assertRaises(OSError):
            self.build()
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
