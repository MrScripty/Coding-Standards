from __future__ import annotations

import hashlib
import json
import tempfile
import textwrap
import unittest
from dataclasses import replace
from pathlib import Path

from tools.graph_engine.graph_engine import GraphContribution
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_authority.standards_authority import (
    AuthorityHandle,
    AuthorityReference,
)
from tools.standards_identity.standards_identity import encode_identity_value
from tools.standards_metadata.standards_metadata import (
    CanonicalModuleCorpus,
    CanonicalStandardsCorpus,
    ModuleMetadata,
    PolicyUnit,
    PolicyUnitCorpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    PolicyImpactArtifact,
    PolicyImpactSemantics,
)

from tools.standards_analysis.standards_analysis import (
    AUTHORIZATION_GRANT_CODEC,
    AnalysisError,
    AuthorizationGrant,
    CoverageAuthorityIndex,
    compile_coverage_definitions,
    derive_coverage_view,
    load_coverage_horizon,
    load_repository_coverage_authority,
    publish_coverage_definitions,
)


class RecordingRepository:
    def __init__(self) -> None:
        self.values: list[tuple[object, object]] = []

    def publish(self, codec, value) -> AuthorityHandle:
        payload = encode_identity_value(codec.encode(value))
        semantic_id = (
            f"{codec.object_kind}:sha256:" + hashlib.sha256(payload).hexdigest()
        )
        self.values.append((codec, value))
        return AuthorityHandle(codec.object_kind, semantic_id)


class CoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write("workflows/policy.md", "# Policy\n\n## Rule\n\nMeaning.\n")
        self.write(
            "suites/coverage.toml",
            """
            schema_version = 1
            id = "coverage"
            owner = "test"

            [[checks]]
            id = "input"
            type = "text"
            path = "inputs/consumer.md"
            """,
        )
        self.write("inputs/consumer.md", "# Consumer\n")
        self.write("evidence.md", "# Reviewed coverage\n")
        self.write("authorization.md", "# Authorized reviewer\n")
        self.write(
            "suite-registry.toml",
            """
            schema_version = 1
            [[suites]]
            id = "coverage"
            path = "suites/coverage.toml"
            requires = []
            """,
        )
        self.write_suite_projection()
        self.write(
            "edge-sources.toml",
            """
            schema_version = 1
            [[sources]]
            id = "standards.policy-impact"
            kind = "provider"
            provider = "standards.policy-impact"
            """,
        )
        self.write(
            "horizon.toml",
            """
            schema_version = 1
            id = "audit-horizon.policy-impact-consumers"
            provider = "standards-analysis:policy-impact-consumer-horizon"
            version = 4
            suite_registry = "suite-registry.toml"
            suite_inputs = "suite-inputs.json"
            edge_source_registry = "edge-sources.toml"
            """,
        )
        self.write(
            "authorization-authority.toml",
            """
            schema_version = 1
            issuer_id = "issuer.test"
            issuer_semantic_revision = 1
            principal_id = "reviewer.test"
            capability = "standards.review.audit"
            authorization_evidence = ["authorization.md"]
            revocation_authority_id = "revocations.test"
            revocation_authority_semantic_revision = 1
            revocations = "revocations.toml"
            """,
        )
        self.write(
            "revocations.toml",
            """
            schema_version = 1
            authority_id = "revocations.test"
            semantic_revision = 1
            revoked_grants = []
            """,
        )

        module = ModuleMetadata(
            "workflows/policy.md",
            "workflow.policy",
            "workflow",
            "MUST",
            "policy applies",
            "not applicable",
            (),
            (),
            "coverage",
            "workflows/policy.md",
        )
        unit = PolicyUnit(
            "workflow.policy.rule",
            module.module_id,
            ("Rule",),
            1,
            (),
            (),
            (),
            module.path,
            "## Rule\n\nMeaning.\n",
            "sha256:" + "1" * 64,
            "sha256:" + "2" * 64,
            "units.toml",
        )
        self.corpus = CanonicalStandardsCorpus(
            CanonicalModuleCorpus("corpus.toml", (module.path,), (module,)),
            PolicyUnitCorpus("units-registry.toml", ("units.toml",), (unit,), ()),
        )
        self.schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "policy-impact.applicability",
                "version": 1,
                "facts": [],
            }
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_suite_projection(self) -> None:
        def digest(path: str) -> str:
            return "sha256:" + hashlib.sha256(
                (self.root / path).read_bytes()
            ).hexdigest()
        projection = {
            "schema_version": 1,
            "contract": "standards-verifier:suite-input-projection:v1",
            "registry": {
                "path": "suite-registry.toml",
                "digest": digest("suite-registry.toml"),
            },
            "suites": [
                {
                    "id": "coverage",
                    "path": "suites/coverage.toml",
                    "digest": digest("suites/coverage.toml"),
                }
            ],
            "inputs": [
                {
                    "path": "inputs/consumer.md",
                    "state": "present",
                    "digest": digest("inputs/consumer.md"),
                    "uses": [
                        {
                            "suite": "coverage",
                            "check": "input",
                            "role": "content",
                        }
                    ],
                }
            ],
        }
        target = self.root / "suite-inputs.json"
        target.write_text(
            json.dumps(projection, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def compiled(
        self,
        *,
        relationship: bool = False,
        artifact: PolicyImpactArtifact | None = None,
    ) -> CompiledPolicyImpactSet:
        semantics = {}
        if relationship:
            program = self.schema.compile({"operator": "always"})
            semantics["edge.policy.consumer"] = PolicyImpactSemantics(
                "edge.policy.consumer",
                "workflow.policy.rule",
                "consumer",
                "documentation-projection",
                program,
                None,
                None,
                "source-to-consumer",
                "suite:coverage",
                "Relationship authority.",
                "declarations.toml",
                "sha256:" + "3" * 64,
            )
        selected_artifact = artifact or PolicyImpactArtifact(
            "consumer",
            (),
            "inputs/consumer.md",
            "documentation",
            "projection",
            None,
            "sha256:" + "c" * 64,
            "catalog.toml",
        )
        return CompiledPolicyImpactSet(
            graph=GraphContribution((), (), ()),
            semantics=semantics,
            artifacts={selected_artifact.id: selected_artifact},
            relationship_kinds={},
            fact_schema=self.schema,
            node_catalog="catalog.toml",
            declaration_sources=("declarations.toml",),
            input_sources=("registry.toml", "catalog.toml"),
            declaration_digest="sha256:" + ("4" if relationship else "5") * 64,
            catalog_digest="sha256:" + "6" * 64,
            authoring_contract_digest="sha256:" + "7" * 64,
            provider_contract_digest="sha256:" + "8" * 64,
            relationship_kind_contract_version=2,
        )

    def authority_index(self) -> tuple[RecordingRepository, CoverageAuthorityIndex]:
        horizon = load_coverage_horizon(
            self.root, self.corpus, self.compiled(), "horizon.toml"
        )
        definitions = compile_coverage_definitions(
            self.corpus, self.compiled(), horizon
        )
        repository = RecordingRepository()
        index = publish_coverage_definitions(
            repository,  # type: ignore[arg-type]
            definitions,
            metadata=AuthorityReference(
                "canonical-standards-corpus",
                "canonical-standards-corpus:sha256:" + "1" * 64,
            ),
            policy_impact=AuthorityReference(
                "compiled-policy-impact", "compiled-policy-impact:sha256:" + "2" * 64
            ),
            graph=AuthorityReference(
                "standards-graph", "standards-graph:sha256:" + "3" * 64
            ),
            horizon=AuthorityReference(
                "coverage-horizon",
                "coverage-horizon:sha256:"
                + horizon.digest.removeprefix("sha256:"),
            ),
        )
        return repository, index

    def write_claim(
        self,
        *,
        principal: str = "reviewer.test",
        semantic_revision: int = 1,
        horizon_version: int = 4,
    ) -> None:
        self.write(
            "attestations.toml",
            f"""
            schema_version = 4

            [[attestations]]
            subject = "workflow.policy.rule"
            semantic_revision = {semantic_revision}
            horizon_provider = "standards-analysis:policy-impact-consumer-horizon"
            horizon_version = {horizon_version}
            relationship_kind_contract_version = 2
            applicability_language_version = 1
            coverage_evidence_contract = "coverage-evidence.v1"
            conclusion = "complete"
            evidence = ["evidence.md"]
            explicit_exclusions = []
            rationale = "The exact registered horizon was reviewed."
            auditor_provenance = "{principal}"
            """,
        )
        self.write(
            "attestation-sources.toml",
            'schema_version = 2\nsources = ["attestations.toml"]\n',
        )

    def load_claims(
        self, repository: RecordingRepository, index: CoverageAuthorityIndex
    ) -> CoverageAuthorityIndex:
        return load_repository_coverage_authority(
            self.root,
            repository,  # type: ignore[arg-type]
            index,
            attestation_registry="attestation-sources.toml",
            authorization_authority="authorization-authority.toml",
            revocations="revocations.toml",
        )

    def test_horizon_uses_registered_suite_inputs_and_fingerprints_content(self) -> None:
        first = load_coverage_horizon(
            self.root, self.corpus, self.compiled(), "horizon.toml"
        )
        ids = {member.id for member in first.members}
        self.assertIn("suite:coverage", ids)
        self.assertIn("repository:inputs/consumer.md", ids)

        self.write("inputs/consumer.md", "# Consumer\n\nNow consumes policy.\n")
        with self.assertRaises(AnalysisError) as caught:
            load_coverage_horizon(
                self.root, self.corpus, self.compiled(), "horizon.toml"
            )
        self.assertEqual(caught.exception.failure.code, "COVERAGE.SUITE_INPUT_STALE")
        self.write_suite_projection()
        second = load_coverage_horizon(
            self.root, self.corpus, self.compiled(), "horizon.toml"
        )
        self.assertNotEqual(first.digest, second.digest)

    def test_reading_authority_label_does_not_change_coverage(self) -> None:
        compiled = self.compiled()
        first = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        artifact = compiled.artifact_for("consumer")
        reading_only = load_coverage_horizon(
            self.root,
            self.corpus,
            replace(
                compiled,
                artifacts={"consumer": replace(artifact, authority="evidence")},
            ),
            "horizon.toml",
        )
        self.assertEqual(first.digest, reading_only.digest)

    def test_unrelated_relationship_does_not_change_subject_definition(self) -> None:
        compiled = self.compiled()
        program = self.schema.compile({"operator": "always"})
        unrelated = PolicyImpactSemantics(
            "edge.other.consumer",
            "workflow.other.rule",
            "consumer",
            "documentation-projection",
            program,
            None,
            None,
            "source-to-consumer",
            "suite:coverage",
            "Unrelated relationship authority.",
            "declarations.toml",
            "sha256:" + "7" * 64,
        )
        changed = replace(compiled, semantics={unrelated.edge_id: unrelated})
        horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        unit = self.corpus.policy_units[0]
        self.assertEqual(
            derive_coverage_view(unit, compiled, horizon),
            derive_coverage_view(unit, changed, horizon),
        )

    def test_repository_claim_constructs_v3_grant_attestation_and_certificate(self) -> None:
        repository, index = self.authority_index()
        subject = index.subjects["workflow.policy.rule"]
        self.write_claim()

        resolved = self.load_claims(repository, index)

        published = resolved.subjects["workflow.policy.rule"]
        self.assertIsNotNone(published.attestation)
        self.assertIsNotNone(published.certificate)
        grants = [
            value
            for codec, value in repository.values
            if codec is AUTHORIZATION_GRANT_CODEC
        ]
        self.assertEqual(len(grants), 1)
        self.assertIsInstance(grants[0], AuthorizationGrant)
        self.assertEqual(grants[0].subject_id, subject.requirement.semantic_id)

    def test_incompatible_semantic_contract_is_not_current_coverage(self) -> None:
        repository, index = self.authority_index()
        self.write_claim(semantic_revision=2)

        resolved = self.load_claims(repository, index)

        subject = resolved.subjects["workflow.policy.rule"]
        self.assertIsNone(subject.attestation)
        self.assertIsNone(subject.certificate)

    def test_wrong_principal_is_rejected(self) -> None:
        repository, index = self.authority_index()
        self.write_claim(principal="reviewer.other")
        with self.assertRaises(AnalysisError) as caught:
            self.load_claims(repository, index)
        self.assertEqual(
            caught.exception.failure.code, "COVERAGE.UNAUTHORIZED_PRINCIPAL"
        )

    def test_revoked_grant_is_rejected(self) -> None:
        repository, index = self.authority_index()
        self.write_claim()
        self.load_claims(repository, index)
        grant = next(
            value
            for codec, value in repository.values
            if codec is AUTHORIZATION_GRANT_CODEC
        )
        self.write(
            "revocations.toml",
            f"""
            schema_version = 1
            authority_id = "revocations.test"
            semantic_revision = 1
            revoked_grants = ["{grant.grant_id}"]
            """,
        )
        with self.assertRaises(AnalysisError) as caught:
            self.load_claims(RecordingRepository(), index)
        self.assertEqual(caught.exception.failure.code, "COVERAGE.AUTHORIZATION_REVOKED")

    def test_evidence_byte_change_changes_attestation_and_certificate(self) -> None:
        repository, index = self.authority_index()
        self.write_claim()
        first = self.load_claims(repository, index)
        self.write("evidence.md", "# Reviewed changed coverage\n")
        second = self.load_claims(RecordingRepository(), index)
        self.assertNotEqual(
            first.subjects["workflow.policy.rule"].attestation.reference,
            second.subjects["workflow.policy.rule"].attestation.reference,
        )
        self.assertNotEqual(
            first.subjects["workflow.policy.rule"].certificate,
            second.subjects["workflow.policy.rule"].certificate,
        )

    def test_representation_change_regenerates_proofs_without_claim_edit(self) -> None:
        self.write_claim()
        claim_source = (self.root / "attestations.toml").read_bytes()
        first_repository, first_index = self.authority_index()
        first = self.load_claims(first_repository, first_index)

        self.write("inputs/consumer.md", "# Consumer\n\n")
        self.write_suite_projection()
        second_repository, second_index = self.authority_index()
        second = self.load_claims(second_repository, second_index)

        first_subject = first.subjects["workflow.policy.rule"]
        second_subject = second.subjects["workflow.policy.rule"]
        self.assertNotEqual(first_subject.requirement, second_subject.requirement)
        self.assertNotEqual(first_subject.attestation, second_subject.attestation)
        self.assertNotEqual(first_subject.certificate, second_subject.certificate)
        self.assertEqual(
            (self.root / "attestations.toml").read_bytes(), claim_source
        )

    def test_repository_claim_rejects_generated_requirement_handle(self) -> None:
        repository, index = self.authority_index()
        self.write_claim()
        source = self.root / "attestations.toml"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                'subject = "workflow.policy.rule"',
                'subject = "workflow.policy.rule"\n'
                'requirement = "coverage-requirement:sha256:' + "9" * 64 + '"',
            ),
            encoding="utf-8",
        )
        with self.assertRaises(AnalysisError) as caught:
            self.load_claims(repository, index)
        self.assertEqual(caught.exception.failure.code, "COVERAGE.FIELDS")

    def test_v2_coverage_identity_fallback_is_absent(self) -> None:
        package = Path(__file__).resolve().parents[1] / "standards_analysis"
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(package.glob("*.py"))
        )
        self.assertNotIn("coverage-authority-view:v2", source)
        self.assertNotIn("coverage-audit-requirement:v2", source)
        self.assertNotIn("coverage-attestation:v2", source)
        self.assertNotIn("consumer-coverage-certificate:v2", source)


if __name__ == "__main__":
    unittest.main()
