from __future__ import annotations

import hashlib
import unittest

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    AuthorizationDenied,
    AuthorizationRequest,
    EvidenceContractKey,
    EvidenceReference,
    FactProviderContract,
    ProviderInputRole,
    ProviderNoObservation,
    ResolvedEvidence,
    construct_authorization_record,
)


def _reference(identifier: str) -> EvidenceReference:
    content = identifier.encode("utf-8")
    return EvidenceReference(
        identifier,
        "sha256:" + hashlib.sha256(content).hexdigest(),
        "repository-content",
        "1",
    )


AUTHORITY_CONTRACT = AuthorizationAuthorityContract(
    "issuer.test",
    1,
    "principal.test",
    "authorization-grant.v1",
    (EvidenceContractKey("repository-content", "1"),),
    "revocation.test",
    1,
    "authorization-revocation.v1",
    (EvidenceContractKey("repository-content", "1"),),
)


class AllowingAuthorizer:
    contract = AUTHORITY_CONTRACT

    def __init__(self, *, subject: str | None = None) -> None:
        self.subject = subject

    def authorize(self, request):
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id if self.subject is None else self.subject,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (ResolvedEvidence(_reference("authorization"), b"authorization"),),
            (ResolvedEvidence(_reference("revocation"), b"revocation"),),
            "not-revoked",
            "allow",
        )


class DenyingAuthorizer:
    contract = AUTHORITY_CONTRACT

    def authorize(self, request):
        del request
        return AuthorizationDenied("The exact capability was denied.")


class EmptyProvider:
    def __init__(self, identifier: str) -> None:
        self.contract = FactProviderContract(
            identifier,
            1,
            "analysis-provider-input.v1",
            "fact-evidence.v1",
            (ProviderInputRole("current", "requirement"),),
        )

    def observe(self, request):
        del request
        return ProviderNoObservation()


class AnalysisTrustTest(unittest.TestCase):
    def test_authorization_record_is_canonical_and_exactly_bound(self) -> None:
        evidence = _reference("submission")
        request = AuthorizationRequest(
            "provide-fact",
            "fact-requirement",
            "requirement.one",
            "standards.analyze",
            (evidence,),
        )
        context = AnalysisExecutionContext(AllowingAuthorizer())

        first = construct_authorization_record(context, request)
        second = construct_authorization_record(context, request)

        self.assertEqual(first, second)
        self.assertEqual(first.subject_id, request.subject_id)
        self.assertEqual(first.reference["capability"], request.capability)

    def test_authorization_context_mismatch_is_rejected(self) -> None:
        request = AuthorizationRequest(
            "coverage-attestation",
            "coverage-requirement",
            "requirement.one",
            "standards.review.audit",
            (_reference("submission"),),
        )

        with self.assertRaises(AnalysisError) as caught:
            construct_authorization_record(
                AnalysisExecutionContext(AllowingAuthorizer(subject="other")),
                request,
            )

        self.assertEqual(
            caught.exception.failure.code,
            "ANALYSIS.AUTHORIZATION_CONTEXT_MISMATCH",
        )

    def test_denied_and_missing_authority_remain_distinct(self) -> None:
        request = AuthorizationRequest(
            "provide-fact",
            "fact-requirement",
            "requirement.one",
            "standards.analyze",
            (_reference("submission"),),
        )
        cases = (
            (AnalysisExecutionContext(DenyingAuthorizer()), "ANALYSIS.UNAUTHORIZED"),
            (AnalysisExecutionContext(), "ANALYSIS.AUTHORIZATION_UNAVAILABLE"),
        )
        for context, expected in cases:
            with self.subTest(expected=expected), self.assertRaises(
                AnalysisError
            ) as caught:
                construct_authorization_record(context, request)
            self.assertEqual(caught.exception.failure.code, expected)

    def test_evidence_content_must_match_its_digest(self) -> None:
        with self.assertRaises(AnalysisError) as caught:
            ResolvedEvidence(_reference("expected"), b"different")
        self.assertEqual(
            caught.exception.failure.code,
            "ANALYSIS.EVIDENCE_DIGEST_MISMATCH",
        )

    def test_execution_contract_view_is_order_independent(self) -> None:
        first = EmptyProvider("provider.first")
        second = EmptyProvider("provider.second")

        left = AnalysisExecutionContext(
            AllowingAuthorizer(), (second, first)
        ).contract_view()
        right = AnalysisExecutionContext(
            AllowingAuthorizer(), (first, second)
        ).contract_view()

        self.assertEqual(left, right)
        self.assertEqual(
            [item["id"] for item in left["providers"]],
            ["provider.first", "provider.second"],
        )

    def test_duplicate_provider_identity_is_rejected(self) -> None:
        with self.assertRaises(AnalysisError) as caught:
            AnalysisExecutionContext(
                providers=(EmptyProvider("provider.same"), EmptyProvider("provider.same"))
            )
        self.assertEqual(caught.exception.failure.code, "ANALYSIS.DUPLICATE_PROVIDER")


if __name__ == "__main__":
    unittest.main()
