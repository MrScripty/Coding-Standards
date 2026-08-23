from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    CHANGE_GRAPH_GROUPS,
    POLICY_IMPACT,
    STANDARDS_REQUIRES,
    STANDARDS_SPECIALIZES,
    AnalysisError,
    ChangeClassification,
    ChangeDescriptor,
    ChangeKind,
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
    ReviewScope,
    SemanticProposal,
    SemanticState,
    classify_changes,
)
from tools.standards_engine.contracts.validate_contracts import validate


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)
STRUCTURED = ReviewScope("structured", ("Policy",))
WHOLE = ReviewScope("whole-artifact")
DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64


def unit(
    policy_id: str = "workflow.test.policy",
    *,
    module: str = "workflow.test",
    representation: str = DIGEST_A,
    structural: str = DIGEST_B,
    revision: int = 3,
    heading: tuple[str, ...] = ("Policy",),
    predecessors: tuple[str, ...] = (),
) -> PolicyUnit:
    return PolicyUnit(
        policy_id,
        module,
        heading,
        revision,
        (),
        predecessors,
        (),
        "module.md",
        "## Policy\n\nText.\n",
        representation,
        structural,
        "units.toml",
    )


def corpus(
    *units: PolicyUnit,
    tombstones: tuple[PolicyUnitTombstone, ...] = (),
) -> PolicyUnitCorpus:
    return PolicyUnitCorpus("registry.toml", ("units.toml",), units, tombstones)


def descriptor(
    kind: ChangeKind,
    accepted: tuple[str, ...],
    proposed: tuple[str, ...],
    *,
    accepted_module: str | None = None,
    proposed_module: str | None = None,
    scope: ReviewScope = STRUCTURED,
) -> ChangeDescriptor:
    return ChangeDescriptor(
        kind,
        accepted,
        proposed,
        scope,
        accepted_module,
        proposed_module,
    )


class ChangeClassificationTest(unittest.TestCase):
    def test_implemented_graph_group_projection_matches_canonical_schema(self) -> None:
        projected = SCHEMA["x-standards-engine-contract"]["impact_graph_groups"]
        for kind, (accepted, proposed) in CHANGE_GRAPH_GROUPS.items():
            self.assertEqual(list(accepted), projected[kind.value]["accepted"])
            self.assertEqual(list(proposed), projected[kind.value]["proposed"])

    def test_semantic_modification_binds_overlay_and_exact_graph_groups(self) -> None:
        before = unit()
        after = unit(representation=DIGEST_B, structural=DIGEST_C)
        result = classify_changes(
            corpus(before),
            corpus(after),
            (
                descriptor(
                    ChangeKind.MODIFICATION,
                    (before.id,),
                    (before.id,),
                    accepted_module=before.module,
                    proposed_module=after.module,
                ),
            ),
            (
                SemanticProposal(
                    before.id,
                    3,
                    4,
                    "Clarify the policy meaning.",
                    after.structural_digest,
                ),
            ),
        )[0]

        changed = result.changed_units[0]
        self.assertEqual(changed.classification, ChangeClassification.SEMANTICALLY_CHANGED)
        self.assertEqual(changed.semantic_state, SemanticState.PROPOSED)
        self.assertEqual(changed.proposed_semantic_revision, 4)
        self.assertEqual(result.graph.accepted_seeds, (before.id,))
        self.assertEqual(result.graph.accepted_groups, (POLICY_IMPACT,))
        self.assertEqual(result.graph.proposed_seeds, (before.id,))
        self.assertEqual(result.graph.proposed_groups, (POLICY_IMPACT,))
        validate(
            SCHEMA,
            SCHEMA["$defs"]["ChangedPolicyUnit"],
            changed.as_contract(),
            "$changed_unit",
        )

    def test_representation_only_change_does_not_claim_semantic_equivalence(self) -> None:
        before = unit()
        after = unit(representation=DIGEST_C)

        changed = classify_changes(
            corpus(before),
            corpus(after),
            (descriptor(ChangeKind.MODIFICATION, (before.id,), (before.id,)),),
        )[0].changed_units[0]

        self.assertEqual(
            changed.classification,
            ChangeClassification.REPRESENTATION_ONLY_CANDIDATE,
        )
        self.assertEqual(changed.semantic_state, SemanticState.ACCEPTED_UNCHANGED)

    def test_structural_change_without_overlay_remains_unresolved(self) -> None:
        before = unit()
        after = unit(representation=DIGEST_C, structural=DIGEST_C)

        changed = classify_changes(
            corpus(before),
            corpus(after),
            (descriptor(ChangeKind.MODIFICATION, (before.id,), (before.id,)),),
        )[0].changed_units[0]

        self.assertEqual(
            changed.classification,
            ChangeClassification.POSSIBLY_SEMANTICALLY_CHANGED,
        )
        self.assertEqual(changed.semantic_state, SemanticState.UNRESOLVED)
        self.assertIsNone(changed.proposed_semantic_revision)

    def test_unchanged_unit_is_distinct_from_representation_candidate(self) -> None:
        selected = unit()

        changed = classify_changes(
            corpus(selected),
            corpus(selected),
            (descriptor(ChangeKind.MODIFICATION, (selected.id,), (selected.id,)),),
        )[0].changed_units[0]

        self.assertEqual(changed.classification, ChangeClassification.UNCHANGED)

    def test_addition_seeds_policy_and_owner_context(self) -> None:
        added = unit(revision=1)
        result = classify_changes(
            corpus(),
            corpus(added),
            (
                descriptor(
                    ChangeKind.ADDITION,
                    (),
                    (added.id,),
                    proposed_module=added.module,
                ),
            ),
            (
                SemanticProposal(
                    added.id,
                    None,
                    1,
                    "Create the policy.",
                    added.structural_digest,
                ),
            ),
        )[0]

        changed = result.changed_units[0]
        self.assertIsNone(changed.accepted_representation_digest)
        self.assertEqual(changed.proposed_semantic_revision, 1)
        self.assertEqual(result.graph.accepted_seeds, ())
        self.assertEqual(
            result.graph.proposed_seeds,
            tuple(sorted((added.id, added.module))),
        )
        self.assertEqual(
            result.graph.proposed_groups,
            (POLICY_IMPACT, STANDARDS_REQUIRES, STANDARDS_SPECIALIZES),
        )

    def test_removal_requires_tombstone_and_keeps_accepted_policy_seed(self) -> None:
        before = unit()
        tombstone = PolicyUnitTombstone(
            before.id,
            before.semantic_revision,
            (),
            "review.retirement",
            "units.toml",
        )
        result = classify_changes(
            corpus(before),
            corpus(tombstones=(tombstone,)),
            (
                descriptor(
                    ChangeKind.REMOVAL,
                    (before.id,),
                    (),
                    accepted_module=before.module,
                    scope=WHOLE,
                ),
            ),
        )[0]

        changed = result.changed_units[0]
        self.assertEqual(changed.semantic_state, SemanticState.REMOVED)
        self.assertIsNone(changed.proposed_structural_digest)
        self.assertEqual(result.graph.accepted_seeds, (before.id,))
        self.assertEqual(result.graph.accepted_groups, (POLICY_IMPACT,))
        self.assertEqual(result.graph.proposed_seeds, ())
        self.assertEqual(result.graph.proposed_groups, ())

    def test_wrong_cardinality_and_module_are_rejected(self) -> None:
        selected = unit()
        cases = (
            (
                descriptor(ChangeKind.MODIFICATION, (), (selected.id,)),
                "CHANGE.DESCRIPTOR_SHAPE",
            ),
            (
                descriptor(
                    ChangeKind.MODIFICATION,
                    (selected.id,),
                    (selected.id,),
                    accepted_module="workflow.wrong",
                ),
                "CHANGE.MODULE_MISMATCH",
            ),
        )
        for change, code in cases:
            with self.subTest(code=code), self.assertRaises(AnalysisError) as caught:
                classify_changes(corpus(selected), corpus(selected), (change,))
            self.assertEqual(caught.exception.failure.code, code)

    def test_modification_rejects_move_and_accepted_revision_mutation(self) -> None:
        before = unit()
        cases = (
            (unit(heading=("Moved",)), "CHANGE.WRONG_KIND"),
            (unit(revision=4), "CHANGE.ACCEPTED_REVISION_MUTATED"),
        )
        for after, code in cases:
            with self.subTest(code=code), self.assertRaises(AnalysisError) as caught:
                classify_changes(
                    corpus(before),
                    corpus(after),
                    (descriptor(ChangeKind.MODIFICATION, (before.id,), (before.id,)),),
                )
            self.assertEqual(caught.exception.failure.code, code)

    def test_semantic_overlay_requires_exact_next_revision_and_structure(self) -> None:
        before = unit()
        after = unit(representation=DIGEST_C, structural=DIGEST_C)
        for proposal in (
            SemanticProposal(before.id, 2, 4, "Intent.", after.structural_digest),
            SemanticProposal(before.id, 3, 5, "Intent.", after.structural_digest),
            SemanticProposal(before.id, 3, 4, "Intent.", DIGEST_A),
        ):
            with self.subTest(proposal=proposal), self.assertRaises(AnalysisError) as caught:
                classify_changes(
                    corpus(before),
                    corpus(after),
                    (descriptor(ChangeKind.MODIFICATION, (before.id,), (before.id,)),),
                    (proposal,),
                )
            self.assertEqual(caught.exception.failure.code, "CHANGE.SEMANTIC_PROPOSAL_MISMATCH")

    def test_addition_requires_semantic_overlay_and_cannot_reuse_tombstone(self) -> None:
        added = unit(revision=1)
        change = descriptor(ChangeKind.ADDITION, (), (added.id,))
        with self.assertRaises(AnalysisError) as caught:
            classify_changes(corpus(), corpus(added), (change,))
        self.assertEqual(caught.exception.failure.code, "CHANGE.SEMANTIC_PROPOSAL_REQUIRED")

        retired = PolicyUnitTombstone(added.id, 1, (), "review.old", "units.toml")
        with self.assertRaises(AnalysisError) as caught:
            classify_changes(
                corpus(tombstones=(retired,)),
                corpus(added),
                (change,),
                (SemanticProposal(added.id, None, 1, "Intent.", added.structural_digest),),
            )
        self.assertEqual(caught.exception.failure.code, "CHANGE.ADDED_ID_EXISTS")

    def test_removal_requires_exact_tombstone(self) -> None:
        before = unit()
        change = descriptor(ChangeKind.REMOVAL, (before.id,), (), scope=WHOLE)
        with self.assertRaises(AnalysisError) as caught:
            classify_changes(corpus(before), corpus(), (change,))
        self.assertEqual(caught.exception.failure.code, "CHANGE.TOMBSTONE_REQUIRED")

        retired = PolicyUnitTombstone(before.id, 2, (), "review.old", "units.toml")
        with self.assertRaises(AnalysisError) as caught:
            classify_changes(
                corpus(before),
                corpus(tombstones=(retired,)),
                (change,),
            )
        self.assertEqual(caught.exception.failure.code, "CHANGE.RETIRED_REVISION")

    def test_duplicate_change_and_orphan_proposal_are_rejected(self) -> None:
        selected = unit()
        change = descriptor(ChangeKind.MODIFICATION, (selected.id,), (selected.id,))
        with self.assertRaises(AnalysisError) as caught:
            classify_changes(corpus(selected), corpus(selected), (change, change))
        self.assertEqual(caught.exception.failure.code, "CHANGE.DUPLICATE_POLICY")

        with self.assertRaises(AnalysisError) as caught:
            classify_changes(
                corpus(selected),
                corpus(selected),
                (change,),
                (SemanticProposal("workflow.other", 1, 2, "Intent.", DIGEST_A),),
            )
        self.assertEqual(caught.exception.failure.code, "CHANGE.ORPHAN_SEMANTIC_PROPOSAL")

    def test_lifecycle_change_kinds_remain_explicitly_unavailable(self) -> None:
        selected = unit()
        for kind in (ChangeKind.MOVE, ChangeKind.SPLIT, ChangeKind.MERGE):
            with self.subTest(kind=kind), self.assertRaises(AnalysisError) as caught:
                classify_changes(
                    corpus(selected),
                    corpus(selected),
                    (descriptor(kind, (selected.id,), (selected.id,)),),
                )
            self.assertEqual(caught.exception.failure.code, "CHANGE.UNSUPPORTED_KIND")


if __name__ == "__main__":
    unittest.main()
