from __future__ import annotations

import unittest
from dataclasses import dataclass

from tools.standards_analysis.standards_analysis.authority import (
    ANALYSIS_CODECS,
    ANALYSIS_CONTEXT_CODEC,
    ANALYSIS_ROOT_CODEC,
    AUTHORIZATION_GRANT_CODEC,
    COVERAGE_ATTESTATION_CODEC,
    COVERAGE_CERTIFICATE_CODEC,
    COVERAGE_HORIZON_CODEC,
    COVERAGE_REQUIREMENT_CODEC,
    COVERAGE_VIEW_CODEC,
    FACT_OBSERVATION_CODEC,
    FACT_REQUIREMENT_CODEC,
    PROVIDER_AUTHORITY_CODEC,
    ROUTING_PROJECTION_CODEC,
    AnalysisContextAuthority,
    AnalysisRootAuthority,
    AuthorityEvidence,
    AuthorizationGrant,
    CoverageAttestationAuthority,
    CoverageCertificateAuthority,
    CoverageHorizonAuthority,
    CoverageRequirementAuthority,
    CoverageViewAuthority,
    FactObservationAuthority,
    FactRequirementAuthority,
    ProviderAuthority,
    RoutingProjectionAuthority,
)
from tools.standards_analysis.standards_analysis.coverage import (
    CoverageHorizon,
    CoverageHorizonMember,
)
from tools.standards_analysis.standards_analysis.routing import RouterProjection
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_authority.standards_authority import (
    AuthorityReference,
    AuthorityRepository,
    CodecContext,
    CodecSet,
    ExecutionAuthorityRoot,
    MemoryObjectStore,
)
from tools.standards_authority.standards_authority.errors import AuthorityError
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)


@dataclass(frozen=True, slots=True)
class _Leaf:
    name: str


class _LeafCodec:
    payload_contract = "test-leaf.v1"
    allowed_dependency_kinds = frozenset[str]()

    def __init__(self, object_kind: str) -> None:
        self.object_kind = object_kind

    def encode(self, value: _Leaf) -> IdentityValue:
        return IdentityObject((("name", value.name),))

    def decode(self, payload: IdentityValue, context: CodecContext) -> _Leaf:
        del context
        assert type(payload) is IdentityObject
        return _Leaf(dict(payload.members)["name"])  # type: ignore[arg-type]

    def semantic_id(self, value: _Leaf, context: CodecContext) -> str:
        del context
        return hash_identity("test:leaf:v1", self.object_kind, self.encode(value))

    def direct_dependencies(self, value: _Leaf) -> tuple[AuthorityReference, ...]:
        del value
        return ()


def _projection(**values: object) -> IdentityObject:
    def identity(value: object) -> IdentityValue:
        if value is None or type(value) in {bool, int, str}:
            return value  # type: ignore[return-value]
        if isinstance(value, (tuple, list)):
            return IdentityArray(identity(item) for item in value)
        if isinstance(value, dict):
            return IdentityObject(
                (key, identity(value[key])) for key in sorted(value)
            )
        raise TypeError(type(value))

    return IdentityObject((key, identity(values[key])) for key in sorted(values))


class AnalysisAuthorityCodecTests(unittest.TestCase):
    def setUp(self) -> None:
        self.leaf_codecs = tuple(
            _LeafCodec(kind)
            for kind in (
                "canonical-standards-corpus",
                "compiled-policy-impact",
                "content-snapshot",
                "standards-graph",
                "execution-closure",
            )
        )
        self.analysis_codecs = ANALYSIS_CODECS.codecs
        self.store = MemoryObjectStore()
        self.repository = AuthorityRepository(
            self.store,
            (
                CodecSet("test-leaves", self.leaf_codecs),
                ANALYSIS_CODECS,
            ),
        )
        self.leaves = {
            codec.object_kind: self.repository.publish(codec, _Leaf(codec.object_kind))
            for codec in self.leaf_codecs
        }

    def test_complete_analysis_authority_chain_round_trips_cold(self) -> None:
        metadata = self.leaves["canonical-standards-corpus"].reference
        impact = self.leaves["compiled-policy-impact"].reference
        content = self.leaves["content-snapshot"].reference
        graph = self.leaves["standards-graph"].reference
        closure = self.leaves["execution-closure"].reference

        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "routing.test",
                "version": 1,
                "facts": [],
            }
        )
        routing = self.repository.publish(
            ROUTING_PROJECTION_CODEC,
            RoutingProjectionAuthority(
                content,
                metadata,
                RouterProjection(
                    "routing.test",
                    "test.owner",
                    "router.test",
                    ("topic.test",),
                    (),
                    (),
                    fact_schema,
                ),
            ),
        )
        horizon = self.repository.publish(
            COVERAGE_HORIZON_CODEC,
            CoverageHorizonAuthority(
                content,
                metadata,
                impact,
                graph,
                CoverageHorizon(
                    "horizon.test",
                    "provider.test",
                    1,
                    (
                        CoverageHorizonMember(
                            "consumer.test",
                            ("consumer",),
                            "sha256:" + "8" * 64,
                        ),
                    ),
                    "sha256:" + "9" * 64,
                    ("consumer.test",),
                ),
            ),
        )

        context = self.repository.publish(
            ANALYSIS_CONTEXT_CODEC,
            AnalysisContextAuthority(
                metadata,
                _projection(subjects=[{"id": "policy.one"}], changes=[], semantic_proposals=[]),
            ),
        )
        requirement = self.repository.publish(
            FACT_REQUIREMENT_CODEC,
            FactRequirementAuthority(
                context.reference,
                impact,
                _projection(
                    fact="change.review",
                    fact_semantic_revision=1,
                    fact_contract_digest="sha256:" + "1" * 64,
                    value_contract={"type": "boolean", "states": ["known"]},
                    answer_contract="fact-answer.v1",
                    evidence_contract="evidence.test",
                    authorization_capability="standards.analyze",
                ),
            ),
        )
        provider = self.repository.publish(
            PROVIDER_AUTHORITY_CODEC,
            ProviderAuthority(
                "provider.test",
                1,
                "authority-inputs.v1",
                "evidence.test",
                tuple(
                    sorted(
                        (
                            ExecutionAuthorityRoot("accepted", "metadata", metadata),
                            ExecutionAuthorityRoot("proposed", "metadata", metadata),
                            ExecutionAuthorityRoot(
                                "accepted", "policy-impact", impact
                            ),
                            ExecutionAuthorityRoot(
                                "current", "context", context.reference
                            ),
                            ExecutionAuthorityRoot(
                                "current", "requirement", requirement.reference
                            ),
                        )
                    )
                ),
            ),
        )
        evidence = AuthorityEvidence(
            "evidence.test", "1", "evidence.one", "sha256:" + "2" * 64
        )
        authorization = self.repository.publish(
            AUTHORIZATION_GRANT_CODEC,
            AuthorizationGrant(
                "issuer.test",
                1,
                "grant.one",
                "principal.test",
                "standards.analyze",
                "provide-fact",
                "fact-requirement",
                requirement.semantic_id,
                (evidence,),
                "revocation.test",
                1,
                (evidence,),
            ),
        )
        observation = self.repository.publish(
            FACT_OBSERVATION_CODEC,
            FactObservationAuthority(
                requirement.reference,
                authorization.reference,
                provider.reference,
                _projection(value={"type": "boolean", "state": "known", "value": True}, evidence=[{"id": evidence.id, "digest": evidence.digest, "provider_contract": evidence.provider_contract, "provider_contract_version": evidence.provider_contract_version}]),
            ),
        )
        coverage_view = self.repository.publish(
            COVERAGE_VIEW_CODEC,
            CoverageViewAuthority(
                metadata,
                impact,
                graph,
                horizon.reference,
                _projection(
                    subject="policy.one",
                    owner="topic.test",
                    semantic_revision=1,
                    representation_digest="sha256:" + "3" * 64,
                    structural_digest="sha256:" + "4" * 64,
                    relationship_kinds=[],
                    relationship_fingerprints=[],
                    applicability_program_digests=[],
                    fact_schema_digest="sha256:" + "5" * 64,
                    horizon={"id": "horizon.test", "digest": "sha256:" + "6" * 64},
                ),
            ),
        )
        coverage_requirement = self.repository.publish(
            COVERAGE_REQUIREMENT_CODEC,
            CoverageRequirementAuthority(
                coverage_view.reference,
                _projection(
                    subject="policy.one",
                    owner="topic.test",
                    semantic_revision=1,
                    relationship_kinds=[],
                    horizon={"id": "horizon.test", "digest": "sha256:" + "6" * 64},
                    required_evidence_contract="coverage-evidence.v1",
                ),
            ),
        )
        audit_grant = self.repository.publish(
            AUTHORIZATION_GRANT_CODEC,
            AuthorizationGrant(
                "issuer.test",
                1,
                "grant.audit",
                "principal.test",
                "standards.review.audit",
                "coverage-attestation",
                "coverage-requirement",
                coverage_requirement.semantic_id,
                (evidence,),
                "revocation.test",
                1,
                (evidence,),
            ),
        )
        attestation = self.repository.publish(
            COVERAGE_ATTESTATION_CODEC,
            CoverageAttestationAuthority(
                coverage_requirement.reference,
                audit_grant.reference,
                _projection(
                    conclusion="complete",
                    evidence=[{"id": evidence.id, "digest": evidence.digest, "provider_contract": evidence.provider_contract, "provider_contract_version": evidence.provider_contract_version}],
                    explicit_exclusions=[],
                    rationale="Complete bounded audit.",
                    auditor_provenance="reviewer:test",
                    schema_version=1,
                ),
            ),
        )
        certificate = self.repository.publish(
            COVERAGE_CERTIFICATE_CODEC,
            CoverageCertificateAuthority(
                coverage_view.reference,
                coverage_requirement.reference,
                attestation.reference,
                _projection(
                    subject="policy.one",
                    owner="topic.test",
                    semantic_revision=1,
                    horizon_digest="sha256:" + "6" * 64,
                    relationship_digest="sha256:" + "7" * 64,
                    evidence_digests=[evidence.digest],
                    provenance={"provider": "coverage.test"},
                    fact_schema_digest="sha256:" + "5" * 64,
                ),
            ),
        )
        root = self.repository.publish(
            ANALYSIS_ROOT_CODEC,
            AnalysisRootAuthority(
                closure,
                context.reference,
                (observation.reference,),
                (attestation.reference,),
                _projection(dispositions=[]),
            ),
        )

        cold = AuthorityRepository(
            self.store,
            (
                CodecSet("test-leaves", self.leaf_codecs),
                ANALYSIS_CODECS,
            ),
        )
        for handle in (
            routing,
            horizon,
            context,
            requirement,
            provider,
            authorization,
            observation,
            coverage_view,
            coverage_requirement,
            audit_grant,
            attestation,
            certificate,
            root,
        ):
            self.assertEqual(cold.resolve(handle).handle, handle)
        self.assertEqual(
            {codec.object_kind for codec in self.analysis_codecs},
            {
                handle.object_kind
                for handle in (
                    routing,
                    horizon,
                    context,
                    requirement,
                    provider,
                    authorization,
                    observation,
                    coverage_view,
                    coverage_requirement,
                    audit_grant,
                    attestation,
                    certificate,
                    root,
                )
            },
        )
        cold._verify_all_stored()
        resolved_provider = cold.resolve(provider).value
        self.assertIsInstance(resolved_provider, ProviderAuthority)
        self.assertEqual(len(resolved_provider.inputs), 5)
        self.assertEqual(
            {item.side for item in resolved_provider.inputs if item.role == "metadata"},
            {"accepted", "proposed"},
        )

    def test_authorization_rejects_action_subject_mismatch(self) -> None:
        evidence = AuthorityEvidence(
            "evidence.test", "1", "evidence.one", "sha256:" + "2" * 64
        )
        with self.assertRaises(AuthorityError) as raised:
            AuthorizationGrant(
                "issuer.test",
                1,
                "grant.one",
                "principal.test",
                "standards.analyze",
                "provide-fact",
                "coverage-requirement",
                "fact-requirement:sha256:" + "1" * 64,
                (evidence,),
                "revocation.test",
                1,
                (evidence,),
            )
        self.assertEqual(
            raised.exception.failure.code, "ANALYSIS.AUTHORIZATION_SUBJECT_MISMATCH"
        )

    def test_authorization_rejects_repeated_logical_evidence_key(self) -> None:
        first = AuthorityEvidence(
            "evidence.test", "1", "evidence.one", "sha256:" + "2" * 64
        )
        second = AuthorityEvidence(
            "evidence.test", "1", "evidence.one", "sha256:" + "3" * 64
        )
        with self.assertRaises(AuthorityError) as raised:
            AuthorizationGrant(
                "issuer.test",
                1,
                "grant.one",
                "principal.test",
                "standards.analyze",
                "provide-fact",
                "fact-requirement",
                "fact-requirement:sha256:" + "1" * 64,
                (first, second),
                "revocation.test",
                1,
                (first,),
            )
        self.assertEqual(raised.exception.failure.code, "ANALYSIS.DUPLICATE_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
