from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisVersions,
    ApplicabilityQuestion,
    ChangeDescriptor,
    ChangeKind,
    ConsumerDispositionSubmission,
    CoverageAttestation,
    CoverageAttestationSubmission,
    CoverageEvidence,
    EvidenceReference,
    FactAnswerSubmission,
    ImpactDispositionSubmission,
    ReadingPlanEntry,
    ReviewScope,
    build_pending_packet,
    classify_changes,
)
from tools.standards_analysis.standards_analysis.obligations import (
    DecisionContract,
    DecisionDependency,
    DecisionFingerprint,
    Obligation,
)
from tools.standards_engine.contracts.validate_contracts import validate
from tools.standards_metadata.standards_metadata import PolicyUnit, PolicyUnitCorpus


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)
BASE = {
    "kind": "snapshot-handle",
    "id": "snapshot:sha256:" + "a" * 64,
    "schema_version": 1,
}
PROPOSED = {
    "kind": "snapshot-handle",
    "id": "snapshot:sha256:" + "b" * 64,
    "schema_version": 1,
}
SCOPE = ReviewScope("whole-artifact")


def unit(representation: str) -> PolicyUnit:
    return PolicyUnit(
        "workflow.test.policy",
        "workflow.test",
        ("Policy",),
        1,
        (),
        (),
        (),
        "module.md",
        "## Policy\n\nText.\n",
        "sha256:" + representation * 64,
        "sha256:" + "c" * 64,
        "units.toml",
    )


def change():
    before = unit("a")
    after = unit("b")
    return classify_changes(
        PolicyUnitCorpus("units/registry.toml", (), (before,), ()),
        PolicyUnitCorpus("units/registry.toml", (), (after,), ()),
        (
            ChangeDescriptor(
                ChangeKind.MODIFICATION,
                (before.id,),
                (after.id,),
                SCOPE,
            ),
        ),
    )[0]


def fingerprint() -> DecisionFingerprint:
    contract = DecisionContract(
        "decision-contract.test.v1",
        1,
        ("policy-unit",),
    )
    return DecisionFingerprint(
        "consumer-review",
        contract.id,
        (
            DecisionDependency(
                "policy-unit",
                "workflow.test.policy",
                "sha256:" + "d" * 64,
            ),
        ),
    )


def obligation(identifier: str = "e") -> Obligation:
    return Obligation(
        "obligation:sha256:" + identifier * 64,
        "consumer-review",
        "workflow.consumer",
        SCOPE,
        (
            {
                "kind": "policy-impact-edge",
                "source": "workflow.test.policy",
                "edge": "edge.test",
                "relation": "normative-consumer",
                "evidence_owner": "suite.test",
                "traces": [
                    {
                        "id": "impact-trace:sha256:" + "1" * 64,
                        "graph": "proposed",
                        "applicability": "true",
                    }
                ],
            },
        ),
        "required",
        ("consumer-disposition",),
        fingerprint(),
        "true",
    )


class PendingPacketTest(unittest.TestCase):
    def test_packet_is_schema_valid_and_derives_next_operations(self) -> None:
        question = ApplicabilityQuestion(
            "question.applicability.changed",
            "changed",
            "Was the policy changed?",
        )
        selected_obligation = obligation()
        packet = build_pending_packet(
            BASE,
            PROPOSED,
            (change(),),
            (selected_obligation,),
            (question,),
            (
                ReadingPlanEntry(
                    "workflow.consumer",
                    SCOPE,
                    "normative",
                    {
                        "kind": "policy-impact-edge",
                        "source": "workflow.test.policy",
                        "edge": "edge.test",
                        "relation": "normative-consumer",
                        "evidence_owner": "suite.test",
                        "traces": [
                            {
                                "id": "impact-trace:sha256:" + "1" * 64,
                                "graph": "proposed",
                                "applicability": "true",
                            }
                        ],
                    },
                    "selected",
                ),
            ),
            summary="One review remains.",
        )

        value = packet.as_contract()
        validate(SCHEMA, SCHEMA["$defs"]["PendingPacket"], value, "$packet")
        self.assertEqual(
            value["next_operations"],
            [
                {
                    "operation": "resolve",
                    "request_kind": "consumer-disposition",
                    "target": "workflow.consumer",
                    "obligation_id": selected_obligation.id,
                },
                {
                    "operation": "resolve",
                    "request_kind": "fact-answer",
                    "target": question.id,
                },
            ],
        )

    def test_packet_identity_is_order_independent_but_snapshot_bound(self) -> None:
        first = obligation("e")
        second = obligation("f")
        left = build_pending_packet(BASE, PROPOSED, (change(),), (first, second))
        right = build_pending_packet(
            BASE,
            PROPOSED,
            (change(),),
            (second, first),
            summary="Display text does not own identity.",
        )
        changed_snapshot = build_pending_packet(
            BASE,
            {**PROPOSED, "id": "snapshot:sha256:" + "9" * 64},
            (change(),),
            (first, second),
        )

        self.assertEqual(left.id, right.id)
        self.assertNotEqual(left.id, changed_snapshot.id)
        self.assertNotIn("summary", left.as_contract())
        self.assertEqual(
            right.as_contract()["summary"],
            "Display text does not own identity.",
        )

    def test_duplicate_or_empty_work_is_rejected(self) -> None:
        with self.assertRaises(AnalysisError) as caught:
            build_pending_packet(BASE, PROPOSED, (change(),), ())
        self.assertEqual(caught.exception.failure.code, "PACKET.NO_OUTSTANDING_WORK")

        selected = obligation()
        with self.assertRaises(AnalysisError) as caught:
            build_pending_packet(BASE, PROPOSED, (change(),), (selected, selected))
        self.assertEqual(caught.exception.failure.code, "PACKET.DUPLICATE_OBLIGATION")

    def test_typed_dispositions_require_evidence_and_match_schema(self) -> None:
        evidence = EvidenceReference(
            "review.consumer",
            "sha256:" + "1" * 64,
            "1",
        )
        consumer = ConsumerDispositionSubmission(
            obligation().id,
            "reviewed-no-change",
            "The consumer remains correct.",
            (evidence,),
            fingerprint(),
        )
        impact = ImpactDispositionSubmission(
            obligation().id,
            "confirmed",
            "The impact remains applicable.",
            (evidence,),
            fingerprint(),
        )

        validate(
            SCHEMA,
            SCHEMA["$defs"]["ConsumerDispositionSubmission"],
            consumer.as_contract(),
            "$consumer",
        )
        validate(
            SCHEMA,
            SCHEMA["$defs"]["ImpactDispositionSubmission"],
            impact.as_contract(),
            "$impact",
        )
        with self.assertRaises(AnalysisError) as caught:
            ConsumerDispositionSubmission(
                obligation().id,
                "reviewed-no-change",
                "Missing evidence.",
                (),
                fingerprint(),
            )
        self.assertEqual(caught.exception.failure.code, "SUBMISSION.EVIDENCE_REQUIRED")

    def test_fact_and_coverage_submissions_match_schema(self) -> None:
        evidence = EvidenceReference(
            "fact.changed",
            "sha256:" + "2" * 64,
            "1",
        )
        fact = FactAnswerSubmission(
            "question.applicability.changed",
            {"type": "boolean", "state": "known", "value": True},
            (evidence,),
        )
        attestation = CoverageAttestation(
            "coverage-attestation:sha256:" + "3" * 64,
            "coverage-requirement:sha256:" + "4" * 64,
            "complete",
            (CoverageEvidence("audit.review", "sha256:" + "5" * 64),),
            (),
            "The bounded consumer horizon was reviewed.",
            "reviewer.authorized",
            1,
            "attestations/test.toml",
        )
        coverage = CoverageAttestationSubmission(obligation().id, attestation)

        validate(
            SCHEMA,
            SCHEMA["$defs"]["FactAnswerSubmission"],
            fact.as_contract(),
            "$fact",
        )
        validate(
            SCHEMA,
            SCHEMA["$defs"]["CoverageAttestationSubmission"],
            coverage.as_contract(),
            "$coverage",
        )

    def test_blocked_work_has_no_derived_resolution_operation(self) -> None:
        selected = obligation()
        blocked = Obligation(
            selected.id,
            selected.kind,
            selected.target,
            selected.scope,
            selected.reasons,
            "blocked",
            selected.permitted_submissions,
            selected.fingerprint,
            selected.applicability,
        )

        packet = build_pending_packet(BASE, PROPOSED, (change(),), (blocked,))

        self.assertEqual(packet.next_operations, ())

    def test_implementation_versions_do_not_change_packet_identity(self) -> None:
        left = build_pending_packet(
            BASE,
            PROPOSED,
            (change(),),
            (obligation(),),
            provenance=AnalysisVersions(analyzer_implementation_version="one"),
        )
        right = build_pending_packet(
            BASE,
            PROPOSED,
            (change(),),
            (obligation(),),
            provenance=AnalysisVersions(analyzer_implementation_version="two"),
        )
        self.assertEqual(left.id, right.id)


if __name__ == "__main__":
    unittest.main()
