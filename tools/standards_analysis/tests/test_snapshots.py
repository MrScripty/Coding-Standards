from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisVersions,
    compile_snapshot,
)
from tools.standards_engine.contracts.validate_contracts import identity, validate


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


class SnapshotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ("git", "-C", str(self.root), *arguments),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def initialize_git(self) -> None:
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Test")
        (self.root / "standard.md").write_text("# Standard\n", encoding="utf-8")
        self.git("add", "standard.md")
        self.git("commit", "-qm", "base")

    def assert_contract(self, snapshot) -> None:
        validate(
            SCHEMA,
            SCHEMA["$defs"]["SnapshotInspectionResult"],
            {"kind": "snapshot-inspection-result", "snapshot": snapshot.inspection},
            "$snapshot",
        )
        definition = (
            "GitSnapshotInspection"
            if snapshot.inspection["kind"] == "git-snapshot-inspection"
            else "ManifestSnapshotInspection"
        )
        self.assertEqual(
            snapshot.handle["id"],
            identity(SCHEMA, definition, snapshot.inspection),
        )

    def test_clean_git_uses_tree_identity_and_commit_as_provenance(self) -> None:
        self.initialize_git()

        first = compile_snapshot(self.root, ("standard.md",))
        self.git("commit", "--allow-empty", "-qm", "provenance only")
        second = compile_snapshot(self.root, ("standard.md",))

        self.assertEqual(first.handle, second.handle)
        self.assertNotEqual(first.inspection["commit"], second.inspection["commit"])
        self.assert_contract(second)

    def test_clean_git_snapshot_content_is_loaded_from_the_bound_tree(self) -> None:
        self.initialize_git()
        snapshot = compile_snapshot(self.root, ("standard.md",))

        (self.root / "standard.md").write_text("# Changed later\n", encoding="utf-8")

        self.assertEqual(snapshot.contents["standard.md"], b"# Standard\n")

    def test_semantic_contract_versions_participate_in_snapshot_identity(self) -> None:
        self.initialize_git()

        first = compile_snapshot(
            self.root,
            ("standard.md",),
            versions=AnalysisVersions(metadata_api_version="1"),
        )
        second = compile_snapshot(
            self.root,
            ("standard.md",),
            versions=AnalysisVersions(metadata_api_version="2"),
        )

        self.assertNotEqual(first.handle, second.handle)

        implementation_only = compile_snapshot(
            self.root,
            ("standard.md",),
            versions=AnalysisVersions(
                metadata_api_version="1",
                analyzer_implementation_version="2",
                graph_engine_implementation_version="2",
            ),
        )
        self.assertEqual(first.handle, implementation_only.handle)

    def test_dirty_git_manifest_includes_tracked_untracked_and_ignored_files(
        self,
    ) -> None:
        self.initialize_git()
        (self.root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
        (self.root / "standard.md").write_text("# Changed\n", encoding="utf-8")
        (self.root / "untracked.txt").write_text("new\n", encoding="utf-8")
        (self.root / "ignored.txt").write_text(
            "ignored but relevant\n", encoding="utf-8"
        )

        snapshot = compile_snapshot(
            self.root,
            ("standard.md", "untracked.txt", "ignored.txt"),
        )
        entries = {entry["path"]: entry for entry in snapshot.inspection["entries"]}

        self.assertEqual(snapshot.inspection["source_kind"], "dirty-git")
        self.assertEqual(entries["standard.md"]["tracking"], "tracked")
        self.assertEqual(entries["untracked.txt"]["tracking"], "untracked")
        self.assertEqual(entries["ignored.txt"]["tracking"], "untracked")
        self.assert_contract(snapshot)

    def test_git_repository_without_tracked_files_labels_inputs_untracked(self) -> None:
        self.git("init", "-q")
        (self.root / "new.txt").write_text("new\n", encoding="utf-8")

        snapshot = compile_snapshot(self.root, ("new.txt",))

        self.assertEqual(snapshot.inspection["source_kind"], "dirty-git")
        self.assertEqual(snapshot.inspection["entries"][0]["tracking"], "untracked")
        self.assert_contract(snapshot)

    def test_ignored_file_is_manifest_input_when_explicitly_in_scope(self) -> None:
        self.initialize_git()
        (self.root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "ignore fixture")
        (self.root / "ignored.txt").write_text("relevant\n", encoding="utf-8")

        snapshot = compile_snapshot(self.root, ("ignored.txt",))

        self.assertEqual(snapshot.inspection["source_kind"], "dirty-git")
        self.assertEqual(snapshot.inspection["entries"][0]["tracking"], "untracked")
        self.assert_contract(snapshot)

    def test_untracked_file_outside_scope_does_not_change_scoped_git_snapshot(
        self,
    ) -> None:
        self.initialize_git()
        before = compile_snapshot(self.root, ("standard.md",))
        (self.root / "outside.txt").write_text("outside\n", encoding="utf-8")

        after = compile_snapshot(self.root, ("standard.md",))

        self.assertEqual(before.handle, after.handle)
        self.assertEqual(after.inspection["kind"], "git-snapshot-inspection")

    def test_manifest_identity_tracks_content_mode_and_explicit_exclusion(self) -> None:
        source = self.root / "source"
        source.mkdir()
        script = source / "run.sh"
        script.write_text("exit 0\n", encoding="utf-8")
        omitted = source / "omitted.txt"
        omitted.write_text("not analyzed\n", encoding="utf-8")

        first = compile_snapshot(
            self.root,
            ("source",),
            exclusions=(("source/omitted.txt", "generated output"),),
        )
        os.chmod(script, 0o755)
        second = compile_snapshot(
            self.root,
            ("source",),
            exclusions=(("source/omitted.txt", "generated output"),),
        )

        self.assertNotEqual(first.handle, second.handle)
        omitted_entry = next(
            entry
            for entry in second.inspection["entries"]
            if entry["path"] == "source/omitted.txt"
        )
        self.assertEqual(omitted_entry["inclusion"], "excluded")
        self.assert_contract(second)

    def test_symlinks_are_not_followed_and_escape_is_inert(self) -> None:
        outside = self.root.with_name(f"{self.root.name}-outside")
        outside.write_text("outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        (self.root / "link").symlink_to(outside)

        snapshot = compile_snapshot(self.root, ("link",))
        entry = snapshot.inspection["entries"][0]

        self.assertEqual(entry["entry_type"], "symlink")
        self.assertEqual(entry["symlink_resolution"], "inert-escape")
        self.assertEqual(entry["symlink_target"], str(outside))
        self.assert_contract(snapshot)

        outside_directory = self.root.with_name(f"{self.root.name}-outside-directory")
        outside_directory.mkdir()
        self.addCleanup(outside_directory.rmdir)
        (outside_directory / "secret").write_text("outside\n", encoding="utf-8")
        self.addCleanup((outside_directory / "secret").unlink)
        (self.root / "directory-link").symlink_to(outside_directory)
        with self.assertRaises(AnalysisError) as caught:
            compile_snapshot(self.root, ("directory-link/secret",))
        self.assertEqual(caught.exception.failure.code, "SNAPSHOT.SYMLINK_ESCAPE")

    def test_dirty_gitlink_binds_nested_snapshot_without_scanning_git_data(
        self,
    ) -> None:
        self.initialize_git()
        nested = self.root / "nested"
        nested.mkdir()
        subprocess.run(("git", "-C", str(nested), "init", "-q"), check=True)
        subprocess.run(
            ("git", "-C", str(nested), "config", "user.email", "test@example.invalid"),
            check=True,
        )
        subprocess.run(
            ("git", "-C", str(nested), "config", "user.name", "Test"),
            check=True,
        )
        (nested / "nested.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(("git", "-C", str(nested), "add", "nested.txt"), check=True)
        subprocess.run(
            ("git", "-C", str(nested), "commit", "-qm", "nested"), check=True
        )
        self.git("add", "nested")
        self.git("commit", "-qm", "gitlink")

        clean = compile_snapshot(self.root, ("nested",))
        self.assertEqual(clean.inspection["submodules"][0]["entry_type"], "gitlink")

        (nested / "nested.txt").write_text("changed\n", encoding="utf-8")
        dirty = compile_snapshot(self.root, ("nested",))
        entry = dirty.inspection["entries"][0]

        self.assertEqual(entry["entry_type"], "gitlink")
        self.assertEqual(entry["worktree_state"], "dirty")
        self.assertIn("nested_snapshot", entry)
        self.assertNotEqual(clean.handle, dirty.handle)
        self.assert_contract(dirty)

    def test_uninitialized_clean_gitlink_uses_recorded_index_identity(self) -> None:
        self.initialize_git()
        source_temp = tempfile.TemporaryDirectory()
        self.addCleanup(source_temp.cleanup)
        source = Path(source_temp.name)
        subprocess.run(("git", "-C", str(source), "init", "-q"), check=True)
        subprocess.run(
            ("git", "-C", str(source), "config", "user.email", "test@example.invalid"),
            check=True,
        )
        subprocess.run(
            ("git", "-C", str(source), "config", "user.name", "Test"),
            check=True,
        )
        (source / "nested.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(("git", "-C", str(source), "add", "nested.txt"), check=True)
        subprocess.run(
            ("git", "-C", str(source), "commit", "-qm", "nested"), check=True
        )
        nested_revision = subprocess.run(
            ("git", "-C", str(source), "rev-parse", "HEAD"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            (
                "git",
                "-C",
                str(self.root),
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-q",
                str(source),
                "nested",
            ),
            check=True,
        )
        self.git("commit", "-qm", "gitlink")
        self.git("submodule", "deinit", "-f", "--", "nested")

        snapshot = compile_snapshot(self.root, ("nested",))
        entry = snapshot.inspection["submodules"][0]

        self.assertEqual(entry["recorded_gitlink"], nested_revision)
        self.assertEqual(entry["checked_out_revision"], nested_revision)
        self.assertEqual(entry["worktree_state"], "clean")
        self.assert_contract(snapshot)

    def test_scope_and_exclusion_paths_are_strict(self) -> None:
        with self.assertRaises(AnalysisError) as caught:
            compile_snapshot(self.root, ("../outside",))
        self.assertEqual(caught.exception.failure.code, "SNAPSHOT.PATH")

        (self.root / "file").write_text("value\n", encoding="utf-8")
        with self.assertRaises(AnalysisError) as caught:
            compile_snapshot(
                self.root,
                ("file",),
                exclusions=(("missing", "not relevant"),),
            )
        self.assertEqual(caught.exception.failure.code, "SNAPSHOT.EXCLUSION_UNRESOLVED")

        self.initialize_git()
        with self.assertRaises(AnalysisError) as caught:
            compile_snapshot(self.root, ("missing",))
        self.assertEqual(caught.exception.failure.code, "SNAPSHOT.INPUT_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
