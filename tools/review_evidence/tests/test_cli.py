from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from tools.review_evidence.review_evidence.common import PacketError, digest
from tools.review_evidence.review_evidence.packet import _validate_staged, build
from tools.review_evidence.review_evidence.request import load_request
from tools.repository_git.repository_git import GitRepositoryError


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
            "format_version": 1,
            "repository_label": "fixture",
            "label": "review",
            "review_question": "Inspect exact changed bytes",
            "revisions": {"baseline": self.base, "candidate": self.candidate},
            "plan": {"revision": "candidate", "path": "plan.md"},
            "context": ["plan.md"],
            "comparisons": [],
            "artifacts": [],
            "claims": [],
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
            self.assertTrue(
                all(
                    ((info.external_attr >> 16) & 0o170000) == 0o100000
                    and ((info.external_attr >> 16) & 0o111) == 0
                    for info in archive.infolist()
                )
            )
            self.assertEqual(
                archive.read("source/baseline/changed.bin"), b"\x00first\xff"
            )
            self.assertEqual(
                archive.read("source/candidate/changed.bin"), b"\x00second\xff"
            )
            self.assertEqual(archive.read("source/baseline/gone.txt"), b"gone\n")
            self.assertNotIn("source/candidate/gone.txt", archive.namelist())
            self.assertEqual(archive.read("source/candidate/new.txt"), b"new\n")
            patch = archive.read("changes/baseline-candidate.patch")
            expected = subprocess.check_output(
                (
                    "git",
                    "-C",
                    str(self.repo),
                    "diff",
                    "--no-ext-diff",
                    "--no-textconv",
                    "--no-renames",
                    "--binary",
                    "--full-index",
                    "--no-color",
                    self.base,
                    self.candidate,
                    "--",
                )
            )
            self.assertEqual(patch, expected)
            manifest = json.loads(archive.read("manifest.json"))
            self.assertEqual(
                {item["path"] for item in manifest["primary"] if item["changed"]},
                {"changed.bin", "gone.txt", "new.txt"},
            )
            self.assertEqual(
                result["manifest_sha256"], digest(archive.read("manifest.json"))
            )
            self.assertEqual(
                {item["name"] for item in manifest["members"]},
                set(archive.namelist()) - {"manifest.json"},
            )
            self.assertEqual(
                manifest["revisions"]["candidate"],
                {
                    "commit": self.candidate,
                    "tree": self.git("rev-parse", "HEAD^{tree}").strip(),
                },
            )
            index = archive.read("INDEX.md").decode()
            self.assertIn("Changed primary files (3)", index)
            self.assertIn("Explicit context files (1)", index)
            self.assertIn(
                f"ZIP file members, including index and manifest: {len(archive.namelist())}",
                index,
            )
            payload_bytes = sum(
                item.file_size
                for item in archive.infolist()
                if item.filename not in {"INDEX.md", "manifest.json"}
            )
            self.assertIn(
                f"Included payload bytes, excluding index and manifest: {payload_bytes}",
                index,
            )

    def test_references_and_missing_file_are_gaps(self) -> None:
        self.request["artifacts"] = [
            {
                "id": "log",
                "role": "ci-log",
                "origin": {"kind": "local-file", "path": "ci/missing.log"},
            },
            {
                "id": "link",
                "role": "ci-reference",
                "origin": {
                    "kind": "reference",
                    "label": "run",
                    "url": "https://example.test/run",
                },
            },
        ]
        result = self.build()
        self.assertEqual(
            [item["availability"] for item in result["material_gaps"]],
            ["missing", "referenced"],
        )
        with zipfile.ZipFile(self.out) as archive:
            self.assertFalse(
                any(name.startswith("evidence/") for name in archive.namelist())
            )

    def test_no_clobber_and_hash_contradiction(self) -> None:
        self.out.write_bytes(b"keep")
        with self.assertRaises(PacketError):
            self.build()
        self.assertEqual(self.out.read_bytes(), b"keep")
        self.out.unlink()
        (self.evidence / "log.txt").write_bytes(b"actual")
        self.request["artifacts"] = [
            {
                "id": "log",
                "role": "ci-log",
                "origin": {
                    "kind": "local-file",
                    "path": "log.txt",
                    "expected_sha256": "sha256:" + "0" * 64,
                },
            }
        ]
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_publication_race_keeps_competing_file_and_cleans_staging(self) -> None:
        def race(*_: object, **__: object) -> None:
            self.out.write_bytes(b"other writer")
            raise FileExistsError("competing output")

        with patch(
            "tools.review_evidence.review_evidence.packet.os.link", side_effect=race
        ):
            with self.assertRaises(FileExistsError):
                self.build()
        self.assertEqual(self.out.read_bytes(), b"other writer")
        self.assertEqual(list(self.out.parent.glob(".review-evidence-*.zip")), [])

    def test_failed_staging_validation_never_publishes(self) -> None:
        with patch(
            "tools.review_evidence.review_evidence.packet._validate_staged",
            side_effect=PacketError("invalid", "injected"),
        ):
            with self.assertRaises(PacketError):
                self.build()
        self.assertFalse(self.out.exists())
        self.assertEqual(list(self.out.parent.glob(".review-evidence-*.zip")), [])

    def test_interrupted_staging_cleans_owned_file(self) -> None:
        with patch(
            "tools.review_evidence.review_evidence.packet._validate_staged",
            side_effect=KeyboardInterrupt,
        ):
            with self.assertRaises(KeyboardInterrupt):
                self.build()
        self.assertFalse(self.out.exists())
        self.assertEqual(list(self.out.parent.glob(".review-evidence-*.zip")), [])

    def test_cleanup_failure_reports_published_artifact(self) -> None:
        with patch(
            "tools.review_evidence.review_evidence.packet.os.unlink",
            side_effect=PermissionError("injected cleanup failure"),
        ):
            result = self.build()
        self.assertTrue(self.out.exists())
        self.assertEqual(result["status"], "built")
        self.assertEqual(result["cleanup_warning"], "owned staging file cleanup failed")
        for owned in self.out.parent.glob(".review-evidence-*.zip"):
            owned.unlink()

    def test_staged_validation_rejects_traversal_and_duplicates(self) -> None:
        for names in (
            ("../escape", "manifest.json"),
            ("same.txt", "same.txt", "manifest.json"),
        ):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(self.out, "w") as archive:
                    for name in names:
                        archive.writestr(name, b"x")
            with self.assertRaises(PacketError):
                _validate_staged(self.out)
            self.out.unlink()

    def test_unknown_claim_and_symlink_evidence_rejected(self) -> None:
        self.request["claims"] = [{"id": "C1", "artifacts": ["unknown"]}]
        with self.assertRaises(PacketError):
            self.build()
        self.request["claims"] = []
        (self.evidence / "link").symlink_to(self.repo / "changed.bin")
        self.request["artifacts"] = [
            {
                "id": "link",
                "role": "ci-log",
                "origin": {"kind": "local-file", "path": "link"},
            }
        ]
        with self.assertRaises(OSError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_symlinked_output_or_evidence_root_is_rejected(self) -> None:
        alias = self.repo.parent / "evidence-alias"
        alias.symlink_to(self.evidence, target_is_directory=True)
        self.write_request()
        with self.assertRaises(PacketError):
            build(self.repo, self.request_path, alias, self.out)
        parent_alias = self.repo.parent / "output-alias"
        parent_alias.symlink_to(self.repo.parent, target_is_directory=True)
        with self.assertRaises(PacketError):
            build(
                self.repo, self.request_path, self.evidence, parent_alias / "packet.zip"
            )
        self.assertFalse(self.out.exists())

    def test_repo_root_must_be_actual_worktree_root(self) -> None:
        child = self.repo / "child"
        child.mkdir()
        self.write_request()
        with self.assertRaises(PacketError):
            build(child, self.request_path, self.evidence, self.out)
        self.assertFalse(self.out.exists())

    def test_portable_case_collision_blocks_publication(self) -> None:
        (self.repo / "Case.txt").write_bytes(b"upper")
        (self.repo / "case.txt").write_bytes(b"lower")
        self.git("add", "Case.txt", "case.txt")
        self.git("commit", "-qm", "colliding paths")
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_unsupported_git_path_encoding_blocks_publication(self) -> None:
        raw_path = os.fsencode(self.repo) + b"/bad-\xff"
        descriptor = os.open(raw_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(b"opaque")
        self.git("add", "-A")
        self.git("commit", "-qm", "invalid path encoding")
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        with self.assertRaises(GitRepositoryError) as raised:
            self.build()
        self.assertEqual(raised.exception.failure.kind, "unsupported")
        self.assertFalse(self.out.exists())

    def test_selected_gitlink_blocks_publication_without_traversal(self) -> None:
        self.git(
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.base},nested-repository",
        )
        self.git("commit", "-qm", "gitlink")
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_request_rejects_duplicate_keys_and_unsafe_paths(self) -> None:
        self.request_path.write_text('{"format_version":1,"format_version":1}')
        with self.assertRaises(PacketError):
            load_request(self.request_path)
        self.request["context"] = ["notes:secret.txt"]
        with self.assertRaises(PacketError):
            self.build()
        self.request["context"] = ["plan.md", "absent-at-both.txt"]
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())
        self.request["context"] = ["plan.md"]
        self.request["label"] = "surrogate" + chr(0xD800)
        with self.assertRaises(PacketError):
            self.build()
        self.request["label"] = "review"
        self.request["revisions"]["candidate"] = "HEAD"
        with self.assertRaises(PacketError):
            self.build()
        self.request["revisions"]["candidate"] = self.candidate
        self.request["format_version"] = 2
        with self.assertRaises(PacketError) as raised:
            self.build()
        self.assertEqual(raised.exception.kind, "unsupported")
        self.request["format_version"] = 1
        self.request["context"] = ["/".join(["x" * 250] * 300)]
        with self.assertRaises(PacketError) as raised:
            self.build()
        self.assertEqual(raised.exception.kind, "unsupported")

    def test_roles_may_share_commit_and_empty_primary_diff(self) -> None:
        self.request["revisions"]["baseline"] = self.candidate
        self.request["revisions"]["ci"] = self.candidate
        self.request["comparisons"] = [{"revision": "ci", "scopes": ["plan.md"]}]
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            self.assertEqual(archive.read("changes/baseline-candidate.patch"), b"")
            manifest = json.loads(archive.read("manifest.json"))
            self.assertFalse(any(item["changed"] for item in manifest["primary"]))
            self.assertEqual(
                manifest["revisions"]["candidate"], manifest["revisions"]["ci"]
            )
            self.assertIn(
                "Changed primary files (0)", archive.read("INDEX.md").decode()
            )

    def test_foreign_evidence_identity_is_recorded_without_inheritance(self) -> None:
        (self.evidence / "foreign.log").write_bytes(b"foreign raw material")
        artifact = {
            "id": "foreign",
            "role": "ci-log",
            "reported_repository": "other-owner/other-repo",
            "reported_subject_revision": "a" * 40,
            "origin": {"kind": "local-file", "path": "foreign.log"},
        }
        self.request["artifacts"] = [artifact]
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            actual = json.loads(archive.read("manifest.json"))["artifacts"][0]
            self.assertEqual(
                archive.read("evidence/foreign/foreign.log"), b"foreign raw material"
            )
            self.assertIsNone(actual["subject"])
            self.assertEqual(actual["reported_repository"], "other-owner/other-repo")
            self.assertEqual(actual["reported_subject_revision"], "a" * 40)
        self.out.unlink()
        artifact["subject"] = "candidate"
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_scope_comparison_keeps_outside_changes_and_links(self) -> None:
        self.request["revisions"]["records"] = self.git("rev-parse", "HEAD").strip()
        (self.repo / "outside.txt").write_bytes(b"later record\n")
        self.git("add", ".")
        self.git("commit", "-qm", "records")
        self.request["revisions"]["records"] = self.git("rev-parse", "HEAD").strip()
        self.request["comparisons"] = [{"revision": "records", "scopes": ["plan.md"]}]
        self.request["artifacts"] = [
            {
                "id": "record",
                "role": "later-record",
                "subject": "candidate",
                "origin": {
                    "kind": "git-file",
                    "revision": "records",
                    "path": "outside.txt",
                },
            }
        ]
        self.request["claims"] = [{"id": "C1", "artifacts": ["record"]}]
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            comparison = json.loads(archive.read("comparisons/records.json"))
            self.assertTrue(comparison["equal_within_scopes"])
            self.assertEqual(comparison["differences_within_scopes"], [])
            self.assertEqual(
                comparison["differences_outside_scopes"][0]["path"], "outside.txt"
            )
            self.assertEqual(
                comparison["differences_outside_scopes"][0]["records"]["blob"],
                self.git("rev-parse", "HEAD:outside.txt").strip(),
            )
            self.assertEqual(
                archive.read("records/record/outside.txt"), b"later record\n"
            )
            index = archive.read("INDEX.md").decode()
            self.assertIn(
                "[Exact governing plan](records/governing-plan/plan.md)", index
            )
            self.assertIn("[complete path inventory](comparisons/records.json)", index)
            self.assertIn("C1: record", index)

    def test_source_symlink_and_member_limit_block_publication(self) -> None:
        (self.repo / "link.txt").symlink_to("plan.md")
        self.git("add", "link.txt")
        self.git("commit", "-qm", "symlink")
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        with self.assertRaises(PacketError):
            self.build()
        self.assertFalse(self.out.exists())
        self.request["revisions"]["candidate"] = self.candidate
        with patch("tools.review_evidence.review_evidence.packet.MEMBER_LIMIT", 5):
            with self.assertRaises(PacketError):
                self.build()
        self.assertFalse(self.out.exists())

    def test_total_limit_exact_boundary(self) -> None:
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            exact = sum(item.file_size for item in archive.infolist())
        self.out.unlink()
        with patch("tools.review_evidence.review_evidence.packet.TOTAL_LIMIT", exact):
            self.build()
        self.out.unlink()
        with patch(
            "tools.review_evidence.review_evidence.packet.TOTAL_LIMIT", exact - 1
        ):
            with self.assertRaises(PacketError):
                self.build()
        self.assertFalse(self.out.exists())

    def test_manifest_identity_ignores_output_filename(self) -> None:
        first = self.build()
        second_path = self.out.parent / "second.zip"
        second = build(self.repo, self.request_path, self.evidence, second_path)
        self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
        with (
            zipfile.ZipFile(self.out) as first_archive,
            zipfile.ZipFile(second_path) as second_archive,
        ):
            self.assertEqual(
                first_archive.read("manifest.json"),
                second_archive.read("manifest.json"),
            )

    def test_member_count_exact_boundary_includes_manifest(self) -> None:
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            exact = len(archive.infolist())
        self.out.unlink()
        with patch("tools.review_evidence.review_evidence.packet.COUNT_LIMIT", exact):
            self.build()
        self.out.unlink()
        with patch(
            "tools.review_evidence.review_evidence.packet.COUNT_LIMIT", exact - 1
        ):
            with self.assertRaises(PacketError):
                self.build()
        self.assertFalse(self.out.exists())

    def test_no_external_diff_or_textconv_execution(self) -> None:
        clean = self.build()
        with zipfile.ZipFile(self.out) as archive:
            clean_patch = archive.read("changes/baseline-candidate.patch")
        self.out.unlink()
        marker = self.repo / "executed"
        driver = self.repo / "driver.sh"
        driver.write_text(f"#!/bin/sh\ntouch '{marker}'\n")
        driver.chmod(0o755)
        (self.repo / ".gitattributes").write_text("*.bin diff=hostile\n*.txt -diff\n")
        self.git("config", "diff.hostile.command", str(driver))
        self.git("config", "diff.hostile.textconv", str(driver))
        self.git("config", "diff.external", str(driver))
        hostile = self.build()
        with zipfile.ZipFile(self.out) as archive:
            self.assertEqual(
                archive.read("changes/baseline-candidate.patch"), clean_patch
            )
        self.assertEqual(hostile["manifest_sha256"], clean["manifest_sha256"])
        self.assertFalse(marker.exists())

    def test_export_attributes_do_not_rewrite_source_bytes(self) -> None:
        (self.repo / ".gitattributes").write_bytes(
            b"new.txt export-ignore\nplan.md export-subst\n"
        )
        self.git("add", ".gitattributes")
        self.git("commit", "-qm", "attributes")
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            self.assertEqual(archive.read("source/candidate/new.txt"), b"new\n")
            self.assertEqual(
                archive.read("records/governing-plan/plan.md"), b"# Actual plan\n"
            )

    def test_missing_promisor_blob_is_never_fetched(self) -> None:
        remote = self.repo.parent / "remote.git"
        subprocess.run(
            ("git", "clone", "--bare", "-q", str(self.repo), str(remote)), check=True
        )
        self.git("remote", "add", "origin", remote.as_uri())
        self.git("config", "extensions.partialClone", "origin")
        self.git("config", "remote.origin.promisor", "true")
        blob = self.git("rev-parse", "HEAD:new.txt").strip()
        loose = self.repo / ".git" / "objects" / blob[:2] / blob[2:]
        self.assertTrue(loose.exists())
        loose.unlink()
        with self.assertRaises(GitRepositoryError):
            self.build()
        self.assertFalse(loose.exists())
        self.assertFalse(self.out.exists())

    def test_replace_ref_cannot_substitute_candidate(self) -> None:
        self.git("replace", self.candidate, self.base)
        before = self.git("show-ref", "--verify", "refs/replace/" + self.candidate)
        self.build()
        self.assertEqual(
            self.git("show-ref", "--verify", "refs/replace/" + self.candidate), before
        )
        with zipfile.ZipFile(self.out) as archive:
            self.assertEqual(
                archive.read("source/candidate/changed.bin"), b"\x00second\xff"
            )

    def test_mode_change_and_rename_are_explicit_versions(self) -> None:
        (self.repo / "changed.bin").chmod(0o755)
        (self.repo / "new.txt").rename(self.repo / "moved.txt")
        self.git("add", "-A")
        self.git("commit", "-qm", "mode and move")
        self.request["revisions"]["baseline"] = self.candidate
        self.request["revisions"]["candidate"] = self.git("rev-parse", "HEAD").strip()
        self.build()
        with zipfile.ZipFile(self.out) as archive:
            manifest = json.loads(archive.read("manifest.json"))
            by_path = {item["path"]: item for item in manifest["primary"]}
            self.assertEqual(by_path["changed.bin"]["baseline"]["mode"], "100644")
            self.assertEqual(by_path["changed.bin"]["candidate"]["mode"], "100755")
            self.assertIn("new.txt", by_path)
            self.assertNotIn("candidate", by_path["new.txt"])
            self.assertIn("moved.txt", by_path)
            self.assertNotIn("baseline", by_path["moved.txt"])
            patch_bytes = archive.read("changes/baseline-candidate.patch")
            self.assertNotIn(b"rename from", patch_bytes)
            self.assertIn(b"diff --git a/new.txt b/new.txt", patch_bytes)
            self.assertIn(b"diff --git a/moved.txt b/moved.txt", patch_bytes)

    def test_documented_command_preserves_source_and_evidence(self) -> None:
        local = self.evidence / "log.txt"
        marker = self.repo.parent / "evidence-executed"
        local.write_bytes(f"#!/bin/sh\ntouch '{marker}'\n".encode())
        self.request["artifacts"] = [
            {
                "id": "log",
                "role": "ci-log",
                "subject": "candidate",
                "origin": {
                    "kind": "local-file",
                    "path": "log.txt",
                    "expected_sha256": digest(local.read_bytes()),
                },
            }
        ]
        self.write_request()
        (self.repo / "changed.bin").write_bytes(b"dirty")
        (self.repo / "untracked.zip").write_bytes(b"external handoff")
        watched = [
            self.repo / ".git" / "index",
            self.repo / ".git" / "config",
            self.repo / ".git" / "refs" / "heads" / "master",
            self.repo / "changed.bin",
            self.repo / "untracked.zip",
            local,
        ]
        if not watched[2].exists():
            watched[2] = self.repo / ".git" / "refs" / "heads" / "main"
        before = [path.read_bytes() for path in watched]
        source_root = Path(__file__).resolve().parents[3]
        bytecode_before = {
            path: path.stat().st_mtime_ns
            for path in source_root.joinpath("tools/review_evidence").rglob("*.pyc")
        }
        command = (
            sys.executable,
            "-B",
            "-m",
            "tools.review_evidence.review_evidence",
            "build",
            "--repo-root",
            str(self.repo),
            "--request",
            str(self.request_path),
            "--evidence-root",
            str(self.evidence),
            "--output",
            str(self.out),
        )
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(source_root)},
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "built")
        self.assertEqual([path.read_bytes() for path in watched], before)
        self.assertFalse(marker.exists())
        self.assertEqual(
            {
                path: path.stat().st_mtime_ns
                for path in source_root.joinpath("tools/review_evidence").rglob("*.pyc")
            },
            bytecode_before,
        )


if __name__ == "__main__":
    unittest.main()
