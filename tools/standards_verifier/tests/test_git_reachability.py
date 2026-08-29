from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tools.standards_verifier.standards_verifier.entrypoints import (
    git_reachability_main,
)
from tools.standards_verifier.standards_verifier.git_reachability import (
    ReachabilityError,
    verify_manifest,
)


class GitReachabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Verifier Test")
        self.git("config", "user.email", "verifier@example.invalid")
        self.first = self.commit("first")
        self.second = self.commit("second")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip()

    def commit(self, content: str) -> str:
        (self.root / "value.txt").write_text(content, encoding="utf-8")
        self.git("add", "value.txt")
        self.git("commit", "-qm", content)
        return self.git("rev-parse", "HEAD")

    def manifest(self, rows: list[tuple[str, str, str, str]], name: str = "protected.tsv") -> Path:
        path = self.root / name
        lines = ["oid\tcommit_disposition\treference\tauthority"]
        lines.extend("\t".join(row) for row in rows)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path.relative_to(self.root)

    def assert_code(self, expected: str, rows: list[tuple[str, str, str, str]]) -> None:
        with self.assertRaises(ReachabilityError) as raised:
            verify_manifest(self.root, self.manifest(rows))
        self.assertEqual(raised.exception.code, expected)

    def test_retained_ref_accepts_an_ancestor(self) -> None:
        records = verify_manifest(
            self.root,
            self.manifest([(self.first, "retained", "refs/heads/master", "none")]),
        )
        self.assertEqual(records[0].oid, self.first)

    def test_archived_ref_must_resolve_to_exact_commit(self) -> None:
        self.git("update-ref", "refs/recovery/example", self.first)
        verify_manifest(
            self.root,
            self.manifest([(self.first, "archived", "refs/recovery/example", "none")]),
        )
        self.assert_code(
            "GIT_REACHABILITY.ARCHIVE_MISMATCH",
            [(self.second, "archived", "refs/recovery/example", "none")],
        )

    def test_unknown_reference_is_distinct(self) -> None:
        self.assert_code(
            "GIT_REACHABILITY.UNKNOWN_REFERENCE",
            [(self.first, "retained", "refs/heads/missing", "none")],
        )

    def test_malformed_reference_is_invalid(self) -> None:
        self.assert_code(
            "GIT_REACHABILITY.INVALID_REFERENCE",
            [(self.first, "retained", "refs/heads/bad..name", "none")],
        )

    def test_retained_ref_rejects_unreachable_commit(self) -> None:
        self.git("checkout", "-qb", "other", self.first)
        other = self.commit("other")
        self.assert_code(
            "GIT_REACHABILITY.UNREACHABLE",
            [(self.second, "retained", "refs/heads/other", "none")],
        )
        self.assertNotEqual(other, self.second)

    def test_discard_requires_exact_authority_record(self) -> None:
        verify_manifest(
            self.root,
            self.manifest([(self.first, "discard-authorized", "none", "plan:exact-row")]),
        )
        self.assert_code(
            "GIT_REACHABILITY.INVALID_DISCARD",
            [(self.first, "discard-authorized", "none", "none")],
        )

    def test_duplicate_oid_is_rejected(self) -> None:
        self.assert_code(
            "GIT_REACHABILITY.DUPLICATE_OID",
            [
                (self.first, "retained", "refs/heads/master", "none"),
                (self.first, "archived", "refs/recovery/example", "none"),
            ],
        )

    def test_malformed_oid_is_rejected(self) -> None:
        self.assert_code(
            "GIT_REACHABILITY.INVALID_OID",
            [("abc", "retained", "refs/heads/master", "none")],
        )

    def test_legacy_ref_suffix_dispositions_are_rejected(self) -> None:
        for disposition in ("retained-ref", "archived-ref"):
            with self.subTest(disposition=disposition):
                self.assert_code(
                    "GIT_REACHABILITY.INVALID_DISPOSITION",
                    [(self.first, disposition, "refs/heads/master", "none")],
                )

    def test_manifest_path_cannot_escape_repository(self) -> None:
        with self.assertRaises(ReachabilityError) as raised:
            verify_manifest(self.root, Path("../outside.tsv"))
        self.assertEqual(raised.exception.code, "GIT_REACHABILITY.PATH_ESCAPE")

    def test_repository_identity_ignores_ambient_git_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as outside_directory:
            outside = Path(outside_directory)
            manifest = outside / "protected.tsv"
            manifest.write_text(
                "oid\tcommit_disposition\treference\tauthority\n"
                f"{self.first}\tretained\trefs/heads/master\tnone\n",
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {
                    "GIT_DIR": str(self.root / ".git"),
                    "GIT_INDEX_FILE": str(self.root / ".git" / "index"),
                },
            ):
                with self.assertRaises(ReachabilityError) as raised:
                    verify_manifest(outside, Path("protected.tsv"))
        self.assertEqual(raised.exception.code, "GIT_REACHABILITY.NOT_REPOSITORY")

    def test_unavailable_git_is_a_typed_reachability_failure(self) -> None:
        rows = [(self.first, "retained", "refs/heads/master", "none")]
        with patch(
            "tools.standards_authority.standards_authority.git_index.subprocess.run",
            side_effect=FileNotFoundError("git unavailable"),
        ):
            with self.assertRaises(ReachabilityError) as raised:
                verify_manifest(self.root, self.manifest(rows))
        self.assertEqual(raised.exception.code, "GIT_REACHABILITY.GIT_UNAVAILABLE")

    def test_public_entrypoint_renders_unavailable_git_failure(self) -> None:
        manifest = self.manifest(
            [(self.first, "retained", "refs/heads/master", "none")]
        )
        stderr = StringIO()
        with (
            patch(
                "tools.standards_authority.standards_authority.git_index.subprocess.run",
                side_effect=FileNotFoundError("git unavailable"),
            ),
            redirect_stderr(stderr),
        ):
            result = git_reachability_main(
                (
                    "--repository",
                    str(self.root),
                    "--manifest",
                    str(manifest),
                ),
                default_repo_root=self.root,
            )
        self.assertEqual(result, 2)
        self.assertTrue(
            stderr.getvalue().startswith("GIT_REACHABILITY.GIT_UNAVAILABLE:")
        )
