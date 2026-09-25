"""Exact continuation input/material matching, independent of repository I/O."""
from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
import unittest

from tools.standards_engine.standards_engine.projection_continuation import (
    ProjectionContinuation,
    ProjectionInputs,
)


def compiler_one(source: object) -> object:
    return source


def compiler_two(source: object) -> object:
    return source


class ProjectionContinuationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inputs = ProjectionInputs(
            (("base.md", b"accepted"),), "snapshot:original",
            ("base.md", "not-read.md"), ("change-1", "change-2"),
            (compiler_one,),
        )
        self.material = (("base.md", b"projected"), ("created.md", b"new"))
        self.paths = ("base.md", "created.md", "not-read.md")
        self.proof = ProjectionContinuation(self.inputs, self.material, self.paths)
        self.successor = replace(self.inputs, change_sets=(*self.inputs.change_sets, "change-3"))

    def length(self, successor: ProjectionInputs) -> int:
        return self.proof.prefix_length(
            successor, projected_files=self.material, repository_paths=self.paths,
        )

    def test_exact_prefix_supports_one_or_multiple_appended_changes(self) -> None:
        self.assertEqual(self.length(self.successor), 2)
        self.assertEqual(self.length(replace(
            self.successor, change_sets=(*self.successor.change_sets, "change-4"),
        )), 2)

    def test_each_supported_history_length_matches_only_its_exact_prefix(self) -> None:
        for length in (1, 4, 12, 32):
            with self.subTest(length=length):
                prefix = replace(self.inputs, change_sets=tuple(str(i) for i in range(length)))
                successor = replace(prefix, change_sets=(*prefix.change_sets, "new"))
                self.assertEqual(prefix.prefix_length(successor), length)
                self.assertEqual(prefix.prefix_length(replace(
                    successor, change_sets=("changed", *successor.change_sets[1:]),
                )), 0)

    def test_same_shorter_or_reordered_program_is_not_a_successor(self) -> None:
        for program in ((), ("change-1",), self.inputs.change_sets,
                        ("change-2", "change-1", "change-3")):
            with self.subTest(program=program):
                self.assertEqual(self.length(replace(self.inputs, change_sets=program)), 0)

    def test_empty_program_does_not_supply_continuation(self) -> None:
        self.assertEqual(replace(self.inputs, change_sets=()).prefix_length(self.successor), 0)

    def test_changed_base_bytes_or_file_membership_replays(self) -> None:
        for files in ((("base.md", b"new accepted bytes"),),
                      (("renamed.md", b"accepted"),),
                      (*self.inputs.base_files, ("extra.md", b"more"))):
            with self.subTest(files=files):
                self.assertEqual(self.length(replace(self.successor, base_files=files)), 0)

    def test_changed_snapshot_identity_replays_even_with_equal_bytes(self) -> None:
        for snapshot in (None, "snapshot:other"):
            with self.subTest(snapshot=snapshot):
                self.assertEqual(self.length(replace(self.successor, base_snapshot=snapshot)), 0)

    def test_repository_membership_outside_captured_files_is_bound(self) -> None:
        self.assertEqual(self.length(replace(
            self.successor, base_repository_paths=("base.md",),
        )), 0)
        self.assertEqual(self.length(replace(
            self.successor, base_repository_paths=(*self.inputs.base_repository_paths, "new.md"),
        )), 0)

    def test_installed_compiler_identity_is_bound(self) -> None:
        self.assertEqual(self.length(replace(self.successor, implementation=(compiler_two,))), 0)

    def test_changed_projected_bytes_replay(self) -> None:
        self.assertEqual(self.proof.prefix_length(
            self.successor, projected_files=(("base.md", b"forged"),),
            repository_paths=self.paths,
        ), 0)

    def test_changed_projected_membership_replays(self) -> None:
        self.assertEqual(self.proof.prefix_length(
            self.successor, projected_files=self.material, repository_paths=("base.md",),
        ), 0)

    def test_canonical_program_snapshot_does_not_follow_caller_mutation(self) -> None:
        change = {"purpose": {"evidence": [{"id": "evidence:original"}]}}
        original = json.dumps(change, sort_keys=True)
        prefix = replace(self.inputs, change_sets=(original,))
        change["purpose"]["evidence"][0]["id"] = "evidence:mutated"
        successor = replace(prefix, change_sets=(json.dumps(change, sort_keys=True), "new"))
        self.assertEqual(prefix.change_sets, (original,))
        self.assertEqual(prefix.prefix_length(successor), 0)

    def test_material_and_provenance_are_immutable_and_copies_are_independent(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.proof.repository_paths = ()  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            self.inputs.change_sets = ()  # type: ignore[misc]
        working = dict(self.material)
        working["base.md"] = b"successor only"
        del working["created.md"]
        self.assertEqual(self.proof.projected_files, self.material)
        self.assertEqual(self.length(self.successor), 2)


if __name__ == "__main__":
    unittest.main()
