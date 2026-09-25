"""Existing-owner registration through the real logical compiler and metadata.

These integration tests require the complete repository and its ordinary
verification inputs. Contract-only tests live in test_registration_contract.py.
"""
from __future__ import annotations

import copy
import tomllib
import unittest

from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_engine.standards_engine.engine import StandardsEngine
from tools.standards_engine.standards_engine.logical_authoring import (
    LogicalAuthoringCompiler, LogicalProgram, StandardsChangeSet,
)
from tools.standards_engine.tests import test_logical_authoring as fixture
from tools.standards_metadata.standards_metadata import MetadataError


MODULE = "topic.registration-fixture"
EXISTING = MODULE + ".existing"
ADDED = MODULE + ".added"
EVIDENCE = {
    "id": "evidence:registration-fixture", "digest": "sha256:" + "1" * 64,
    "provider_contract": "standards-evidence", "provider_contract_version": "1",
}


def unit(identity: str, heading: str) -> dict[str, object]:
    return {"id": identity, "heading_chain": [heading], "semantic_revision": 1,
            "intent": "Identify the selected scope for explicit consumer review.",
            "aliases": [], "predecessors": [], "successors": []}


def register(identity: str = ADDED, heading: str = "Additional Scope") -> dict[str, object]:
    return {"kind": "register-policy-unit", "standard": MODULE,
            "policy_unit": unit(identity, heading)}


def change(edits: list[dict[str, object]]) -> StandardsChangeSet:
    return StandardsChangeSet.from_mapping({
        "purpose": {"summary": "Exercise existing-owner registration.",
                    "rationale": "The fixture verifies an explicit logical authoring transition.",
                    "evidence": [EVIDENCE]},
        "edits": edits,
    })


def create_owner(with_policy: bool = False) -> dict[str, object]:
    edit = fixture.LogicalAuthoringTests.new_standard_edit()
    edit["standard"].update({
        "id": MODULE, "title": "Registration Fixture", "body": (
            "## Existing Scope\n\nPreserve the existing owner's result.\n\n"
            "## Additional Scope\n\nReview the selected additional scope.\n\n"
            "## Further Scope\n\nKeep a separate ownership decision.\n"
        ),
    })
    edit["policy_units"] = [unit(EXISTING, "Existing Scope")] if with_policy else []
    if with_policy:
        edit["policy_units"][0]["aliases"] = [MODULE + ".legacy-alias"]
    return edit


def relationship(policy: str = ADDED) -> dict[str, object]:
    result = fixture.LogicalAuthoringTests.new_relationship()
    result["source_policy"] = policy
    return {"kind": "put-policy-relationship", "relationship": result}


class PolicyRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Reuse the established capture fixture, not a hand-written metadata or
        # graph implementation. Creation occurs before the registration base.
        fixture.LogicalAuthoringTests.setUpClass()
        shared = fixture.LogicalAuthoringTests
        compiler = LogicalAuthoringCompiler(StandardsEngine._compile)
        cls.owners = {}
        for populated in (False, True):
            cls.owners[populated] = compiler.compile(
                shared.base, LogicalProgram([change([create_owner(populated)])]),
                base_repository_paths=shared.repository_paths, compiled_base=shared.compiled,
            )

    def project(self, changes, *, populated=False, base=None, predecessor=None):
        base = self.owners[populated] if base is None else base
        return LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            base.source, LogicalProgram(changes), base_repository_paths=base.repository_paths,
            compiled_base=base.compiled, predecessor=predecessor,
        )

    def test_registers_on_preexisting_unmapped_owner_without_rewriting_prose(self):
        base = self.owners[False]
        before = dict(base.source.files)
        module = base.compiled.corpus.resolve_module(MODULE)
        projected = self.project([change([register()])])
        policy = projected.compiled.corpus.resolve_policy_unit(ADDED)
        self.assertEqual(policy.module, MODULE)
        self.assertEqual(policy.heading_path, ("Additional Scope",))
        self.assertEqual(policy.semantic_revision, 1)
        self.assertEqual(projected.source.read_bytes(module.path), base.source.read_bytes(module.path))
        self.assertEqual(dict(base.source.files), before)
        self.assertIn(MODULE, projected.analysis_module_ids)
        self.assertNotIn(ADDED, projected.compiled.repository_coverage.covered_subjects)
        semantic = next(value for value in projected.semantic_proposals if value["policy"] == ADDED)
        self.assertIsNone(semantic["accepted_semantic_revision"])
        self.assertEqual(semantic["proposed_semantic_revision"], 1)

    def test_existing_unit_and_alias_are_preserved_in_the_same_sidecar(self):
        base = self.owners[True]
        old = base.compiled.corpus.resolve_policy_unit(EXISTING)
        projected = self.project([change([register()])], populated=True)
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(EXISTING), old)
        added = projected.compiled.corpus.resolve_policy_unit(ADDED)
        self.assertEqual(added.source, old.source)
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(MODULE + ".legacy-alias"), old)

    def test_multiple_registrations_share_one_registered_owner_and_ignore_input_order(self):
        edits = [register(), register(MODULE + ".further", "Further Scope")]
        first = self.project([change(edits)])
        second = self.project([change(list(reversed(edits)))])
        self.assertEqual(first.source.files, second.source.files)
        self.assertEqual(first.semantic_proposals, second.semantic_proposals)
        policies = first.compiled.corpus.policy_unit_corpus.for_module(MODULE)
        self.assertEqual(len(policies), 2)
        self.assertEqual(len({policy.source for policy in policies}), 1)
        sources = tomllib.loads(first.source.read_bytes(
            "evaluation/standards-effectiveness/policy-units/registry.toml").decode())["sources"]
        self.assertEqual(sources.count(policies[0].source), 1)

    def test_same_candidate_rewrite_register_relationship_and_provenance(self):
        standard = create_owner(True)["standard"]
        standard["body"] = standard["body"].replace("Additional Scope", "Revised Additional Scope")
        rewrite = {"kind": "revise-standard", "standard": standard,
                   "scope_updates": [{"policy": EXISTING, "heading_path": ["Existing Scope"],
                                      "semantics": {"kind": "preserve", "semantic_revision": 1,
                                                    "intent": "Preserve the existing policy."}}]}
        provenance = {"kind": "put-provenance", "record": {
            "id": "provenance.registration-fixture", "subject": ADDED,
            "origin": "current-justification", "rationale": "Private fixture rationale.",
            "evidence": [EVIDENCE],
        }}
        edits = [provenance, relationship(), register(heading="Revised Additional Scope"), rewrite]
        projected = self.project([change(edits)], populated=True)
        reversed_projection = self.project([change(list(reversed(edits)))], populated=True)
        self.assertEqual(projected.source.files, reversed_projection.source.files)
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(ADDED).heading_path,
                         ("Revised Additional Scope",))
        self.assertEqual(projected.compiled.supporting.provenance[
            "provenance.registration-fixture"].subject, ADDED)
        self.assertTrue(any(value.source == ADDED for value in projected.compiled.policy_impact.semantics.values()))

    def test_registered_empty_owner_retains_tombstones(self):
        retirement = {"kind": "retire-policy-unit", "policy": EXISTING,
                      "retired_semantic_revision": 1, "successors": [],
                      "relationship_dispositions": [], "evidence": [EVIDENCE]}
        retired_base = self.project([change([retirement])], populated=True)
        tombstone = retired_base.compiled.corpus.resolve_policy_unit(EXISTING)
        projected = self.project([change([register()])], base=retired_base)
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(EXISTING), tombstone)
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(ADDED).source, tombstone.source)
        with self.assertRaises(AuthoringError):
            self.project([change([register(EXISTING)])], base=retired_base)

    def test_reserved_identity_and_module_alias_collisions_are_rejected(self):
        for identity in (EXISTING, MODULE + ".legacy-alias", MODULE):
            with self.subTest(identity=identity), self.assertRaises(AuthoringError):
                self.project([change([register(identity)])], populated=True)
        collision = register()
        collision["policy_unit"]["aliases"] = [MODULE]
        with self.assertRaises(AuthoringError):
            self.project([change([collision])], populated=True)

    def test_canonical_metadata_rejects_missing_ambiguous_and_overlapping_scopes(self):
        for heading in ("Missing Scope", "Existing Scope"):
            with self.subTest(heading=heading), self.assertRaises(MetadataError):
                self.project([change([register(heading=heading)])], populated=True)
        standard = create_owner()["standard"]
        standard["body"] += "\n## Additional Scope\n\nA duplicate heading is ambiguous.\n"
        with self.assertRaises(MetadataError):
            self.project([change([{"kind": "revise-standard", "standard": standard}, register()])])
        standard = create_owner(True)["standard"]
        standard["body"] = standard["body"].replace(
            "Preserve the existing owner's result.",
            "Preserve the existing owner's result.\n\n### Nested Scope\n\nNested text.",
        )
        nested = register()
        nested["policy_unit"]["heading_chain"] = ["Existing Scope", "Nested Scope"]
        rewrite = {"kind": "revise-standard", "standard": standard,
                   "scope_updates": [{"policy": EXISTING, "heading_path": ["Existing Scope"],
                                      "semantics": {"kind": "preserve", "semantic_revision": 1,
                                                    "intent": "Preserve fixture meaning."}}]}
        with self.assertRaises(MetadataError):
            self.project([change([rewrite, nested])], populated=True)

    def test_new_alias_conflict_is_rejected_for_the_complete_group(self):
        first, second = register(), register(MODULE + ".further", "Further Scope")
        first["policy_unit"]["aliases"] = ["registration.shared-alias"]
        second["policy_unit"]["aliases"] = ["registration.shared-alias"]
        with self.assertRaises(MetadataError):
            self.project([change([first, second])])

    def test_existing_lineage_validation_remains_authoritative(self):
        invalid = register()
        invalid["policy_unit"]["predecessors"] = [MODULE + ".unknown-predecessor"]
        with self.assertRaises(MetadataError):
            self.project([change([invalid])])

    def test_unknown_module_and_conflicting_logical_edits_are_rejected(self):
        missing = register()
        missing["standard"] = "topic.unavailable-registration-fixture"
        with self.assertRaises(AuthoringError):
            self.project([change([missing])])
        with self.assertRaises(AuthoringError):
            change([register(), register()])
        with self.assertRaises(AuthoringError):
            change([register(), {"kind": "revise-policy-unit", "policy": ADDED,
                                "title": "Additional Scope", "body": "Owned result.",
                                "semantics": {"kind": "preserve", "semantic_revision": 1,
                                              "intent": "Conflicting facet fixture."}}])

    def test_full_replay_and_incremental_successor_produce_identical_authority(self):
        prefix = (change([register()]),)
        previous = self.project(prefix)
        self.assertIsNotNone(previous._continuation)
        original = dict(previous.source.files)
        program = (*prefix, change([register(MODULE + ".further", "Further Scope"), relationship()]))
        cold = self.project(program)
        warm = self.project(program, predecessor=previous)
        self.assertEqual(warm.source.files, cold.source.files)
        self.assertEqual(warm.repository_paths, cold.repository_paths)
        self.assertEqual(warm.semantic_proposals, cold.semantic_proposals)
        self.assertEqual(warm.analysis_policy_ids, cold.analysis_policy_ids)
        self.assertEqual(warm.analysis_module_ids, cold.analysis_module_ids)
        self.assertEqual(dict(previous.source.files), original)

    def test_failed_suffix_preserves_the_predecessor_and_original_base(self):
        prefix = (change([register()]),)
        previous = self.project(prefix)
        before_base = dict(self.owners[False].source.files)
        before_prefix = dict(previous.source.files)
        failed = (*prefix, change([register(MODULE + ".further", "Missing Scope")]))
        for seed in (None, previous):
            with self.subTest(incremental=seed is not None), self.assertRaises(MetadataError):
                self.project(failed, predecessor=seed)
        self.assertEqual(dict(self.owners[False].source.files), before_base)
        self.assertEqual(dict(previous.source.files), before_prefix)

    def test_caller_mutation_cannot_rewrite_a_registered_edit(self):
        request = register()
        selected = change([request])
        expected = copy.deepcopy(selected.as_contract())
        request["policy_unit"]["heading_chain"].append("Changed")
        self.assertEqual(selected.as_contract(), expected)
        projected = self.project([selected])
        self.assertEqual(projected.compiled.corpus.resolve_policy_unit(ADDED).heading_path,
                         ("Additional Scope",))

    def test_later_preservation_keeps_original_absent_identity_semantics(self):
        program = [change([register()]), change([{
            "kind": "revise-policy-unit", "policy": ADDED, "title": "Additional Scope",
            "body": "Review the selected additional scope with its owner.",
            "semantics": {"kind": "preserve", "semantic_revision": 1,
                          "intent": "Clarify the same fixture obligation."},
        }])]
        projected = self.project(program)
        semantic = next(value for value in projected.semantic_proposals if value["policy"] == ADDED)
        self.assertIsNone(semantic["accepted_semantic_revision"])
        self.assertEqual(semantic["proposed_semantic_revision"], 1)


if __name__ == "__main__":
    unittest.main()
