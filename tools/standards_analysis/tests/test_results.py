from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisVersions,
    AuthorizationReference,
    ChangeDescriptor,
    ChangeKind,
    ConsumerDispositionSubmission,
    CoverageAttestation,
    CoverageAttestationSubmission,
    CoverageDecision,
    CoverageEvidence,
    EvidenceReference,
    ImpactDispositionSubmission,
    ProvideFactSubmission,
    ReadingPlanEntry,
    ReviewScope,
    build_analysis_context,
    build_fact_requirement,
    build_pending_result,
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
ANALYSIS = {
    "kind": "analysis-handle",
    "id": "analysis:sha256:" + "8" * 64,
    "schema_version": 3,
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
    contract = DecisionContract("decision-contract.test.v1", 1, ("policy-unit",))
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


def fact_requirement():
    schema = compile_fact_schema(
        {
            "kind": "applicability-fact-schema",
            "id": "facts.result",
            "version": 1,
            "facts": [
                {
                    "id": "change.requires-review",
                    "semantic_revision": 1,
                    "type": "boolean",
                    "nullable": False,
                    "aliases": [],
                    "meaning": "Whether the change requires review.",
                    "context_kind": "standards-change",
                    "answer_contract": "fact-value.v1",
                    "evidence_contract": "evidence-reference.v1",
                    "authorization_capability": "standards.analyze",
                    "prompt": "Does the change require review?",
                }
            ],
        }
    )
    return build_fact_requirement(
        schema.resolve("change.requires-review"),
        build_analysis_context((change(),)),
        ("proposed:edge.test",),
    )


class PendingResultTest(unittest.TestCase):
    def test_projection_is_schema_valid_and_derives_next_operations(self) -> None:
        requirement = fact_requirement()
        selected = obligation()
        result = build_pending_result(
            ANALYSIS,
            (change(),),
            (selected,),
            (requirement,),
            (
                ReadingPlanEntry(
                    "workflow.consumer",
                    SCOPE,
                    "normative",
                    (
                        {
                            "kind": "consumer-review-obligation",
                            "obligation": selected.id,
                        },
                    ),
                    "selected",
                ),
            ),
            context=build_analysis_context((change(),)),
            summary="One review remains.",
        )

        value = result.as_contract()
        validate(SCHEMA, SCHEMA["$defs"]["PendingResult"], value, "$result")
        self.assertEqual(result.handle, ANALYSIS)
        self.assertEqual(
            value["next_operations"],
            [
                {
                    "operation": "resolve",
                    "request_kind": "consumer-disposition",
                    "target": "workflow.consumer",
                    "obligation_id": selected.id,
                    "analysis": ANALYSIS,
                },
                {
                    "operation": "resolve",
                    "request_kind": "provide-fact",
                    "target": requirement.fact,
                    "requirement_id": requirement.id,
                    "analysis": ANALYSIS,
                },
            ],
        )

    def test_projection_has_no_identity_independent_of_analysis(self) -> None:
        selected = obligation()
        left = build_pending_result(
            ANALYSIS,
            (change(),),
            (selected,),
            (),
            (),
            context=build_analysis_context((change(),)),
        )
        right = build_pending_result(
            ANALYSIS,
            (change(),),
            (selected,),
            (),
            (),
            context=build_analysis_context((change(),)),
            provenance=AnalysisVersions(analyzer_implementation_version="two"),
            summary="Display-only text.",
        )

        self.assertEqual(left.id, right.id)
        self.assertEqual(left.handle, right.handle)
        self.assertNotIn("summary", left.as_contract())
        self.assertEqual(right.as_contract()["summary"], "Display-only text.")

    def test_duplicate_or_empty_work_is_rejected(self) -> None:
        context = build_analysis_context((change(),))
        with self.assertRaises(AnalysisError) as caught:
            build_pending_result(ANALYSIS, (change(),), (), (), (), context=context)
        self.assertEqual(caught.exception.failure.code, "RESULT.NO_OUTSTANDING_WORK")

        selected = obligation()
        with self.assertRaises(AnalysisError) as caught:
            build_pending_result(
                ANALYSIS,
                (change(),),
                (selected, selected),
                (),
                (),
                context=context,
            )
        self.assertEqual(
            caught.exception.failure.code,
            "RESULT.DUPLICATE_OBLIGATION",
        )

    def test_typed_submissions_and_coverage_decision_match_schema(self) -> None:
        evidence = EvidenceReference(
            "review.consumer",
            "sha256:" + "1" * 64,
            "repository-content",
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
        requirement = fact_requirement()
        fact = ProvideFactSubmission(
            requirement.handle,
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
            2,
            "attestations/test.toml",
        )
        coverage = CoverageAttestationSubmission(obligation().id, attestation)
        authorization = AuthorizationReference(
            "authorization.audit",
            "standards.review.audit",
            "sha256:" + "6" * 64,
        )

        for definition, value in (
            ("ConsumerDispositionSubmission", consumer.as_contract()),
            ("ImpactDispositionSubmission", impact.as_contract()),
            ("ProvideFactSubmission", fact.as_contract()),
            ("CoverageAttestationSubmission", coverage.as_contract()),
            (
                "CoverageDecision",
                CoverageDecision(attestation, authorization).as_contract(),
            ),
        ):
            validate(SCHEMA, SCHEMA["$defs"][definition], value, "$submission")

        with self.assertRaises(AnalysisError) as caught:
            ConsumerDispositionSubmission(
                obligation().id,
                "reviewed-no-change",
                "Missing evidence.",
                (),
                fingerprint(),
            )
        self.assertEqual(caught.exception.failure.code, "SUBMISSION.EVIDENCE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
