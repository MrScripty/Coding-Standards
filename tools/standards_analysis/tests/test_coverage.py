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
from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    compile_coverage_definitions,
    coverage_requirement_id,
    derive_coverage_requirement,
    derive_coverage_view,
    load_coverage_horizon,
    load_repository_coverage_decisions,
)
from tools.standards_analysis.standards_analysis.keys import analysis_identity
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
        self.write(
            "suites/unrelated.toml",
            """
            schema_version = 1
            id = "unrelated"
            owner = "test"
            description = "Unrelated coverage input."
            checks = [{ id = "input", type = "text" }]
            """,
        )
        self.write("inputs/unrelated.md", "# Unrelated\n")
        self.write(
            "suite-registry.toml",
            """
            schema_version = 1
            [[suites]]
            id = "coverage"
            path = "suites/coverage.toml"
            requires = []

            [[suites]]
            id = "unrelated"
            path = "suites/unrelated.toml"
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
            version = 6
            suite_registry = "suite-registry.toml"
            suite_inputs = "suite-inputs.json"
            edge_source_registry = "edge-sources.toml"
            """,
        )
        self.write("evidence/review.md", "Reviewed coverage.\n")
        self.write("evidence/authorization.md", "Authorized reviewer.\n")
        self.write(
            "authorization.toml",
            """
            schema_version = 1
            issuer_id = "issuer.coverage"
            issuer_semantic_revision = 1
            principal_id = "principal.coverage"
            capability = "standards.review.audit"
            authorization_evidence = ["evidence/authorization.md"]
            revocation_authority_id = "authority.revocations"
            revocation_authority_semantic_revision = 1
            revocations = "revocations.toml"
            """,
        )
        self.write(
            "revocations.toml",
            """
            schema_version = 1
            authority_id = "authority.revocations"
            semantic_revision = 1
            revoked_grants = []
            """,
        )
        self.write(
            "attestation-sources.toml",
            """
            schema_version = 2
            sources = ["attestations.toml"]
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
            "contract": "standards-metadata:suite-input-manifest:v1",
            "registry": {
                "path": "suite-registry.toml",
                "digest": digest("suite-registry.toml"),
            },
            "suites": [
                {
                    "id": "coverage",
                    "path": "suites/coverage.toml",
                    "digest": digest("suites/coverage.toml"),
                    "requires": [],
                },
                {
                    "id": "unrelated",
                    "path": "suites/unrelated.toml",
                    "digest": digest("suites/unrelated.toml"),
                    "requires": [],
                },
            ],
            "files": [
                {
                    "path": "inputs/consumer.md",
                    "state": "present",
                    "digest": digest("inputs/consumer.md"),
                    "uses": [
                        {"suite": "coverage", "check": "input", "role": "content"}
                    ],
                },
                {
                    "path": "inputs/unrelated.md",
                    "state": "present",
                    "digest": digest("inputs/unrelated.md"),
                    "uses": [
                        {"suite": "unrelated", "check": "input", "role": "content"}
                    ],
                }
            ],
            "repository_index": None,
        }
        (self.root / "suite-inputs.json").write_text(
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
            semantics["edge.policy.consumer"] = PolicyImpactSemantics(
                "edge.policy.consumer",
                "workflow.policy.rule",
                "consumer",
                "documentation-projection",
                self.schema.compile({"operator": "always"}),
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

    def definitions(self):
        compiled = self.compiled(relationship=True)
        horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        return compile_coverage_definitions(self.corpus, compiled, horizon)

    def write_attestations(
        self,
        *,
        requirement_id: str | None = None,
        principal: str = "principal.coverage",
        duplicate: bool = False,
        pinned: bool = False,
        exclusions: tuple[str, ...] = (),
    ) -> None:
        definitions = self.definitions()
        current_requirement = coverage_requirement_id(
            definitions.requirements["workflow.policy.rule"],
            definitions.views["workflow.policy.rule"],
        )

        def evidence_value(path):
            if not pinned:
                return json.dumps(path)
            fields = {
                "id": path,
                "digest": "sha256:"
                + hashlib.sha256((self.root / path).read_bytes()).hexdigest(),
                "provider_contract": "repository-content",
                "provider_contract_version": "1",
            }
            return (
                "{ "
                + ", ".join(
                    f"{key} = {json.dumps(value)}" for key, value in fields.items()
                )
                + " }"
            )

        claim = f"""
            [[attestations]]
            requirement_id = "{requirement_id or current_requirement}"
            conclusion = "complete"
            evidence = [{evidence_value("evidence/review.md")}]
            explicit_exclusions = [{", ".join(evidence_value(path) for path in exclusions)}]
            rationale = "The bounded horizon was reviewed."
            auditor_provenance = "{principal}"
        """
        self.write(
            "attestations.toml",
            f"schema_version = {6 if pinned else 5}\n"
            + claim
            + (claim if duplicate else ""),
        )

    def load_decisions(self):
        return load_repository_coverage_decisions(
            self.root,
            self.definitions(),
            attestation_registry="attestation-sources.toml",
            authorization_authority="authorization.toml",
            revocations="revocations.toml",
        )

    def test_horizon_fingerprints_registered_content(self) -> None:
        first = load_coverage_horizon(
            self.root, self.corpus, self.compiled(), "horizon.toml"
        )

        self.write("inputs/consumer.md", "# Consumer\n\nNow consumes policy.\n")
        self.write_suite_projection()
        content_changed = load_coverage_horizon(
            self.root, self.corpus, self.compiled(), "horizon.toml"
        )
        self.assertNotEqual(first.digest, content_changed.digest)

    def test_unrelated_suite_input_preserves_subject_requirement(self) -> None:
        compiled = self.compiled(relationship=True)
        first_horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        unit = self.corpus.policy_units[0]
        first_view = derive_coverage_view(unit, compiled, first_horizon)
        first_requirement = coverage_requirement_id(
            derive_coverage_requirement(first_view), first_view
        )

        self.write("inputs/unrelated.md", "# Unrelated changed\n")
        self.write_suite_projection()
        second_horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        second_view = derive_coverage_view(unit, compiled, second_horizon)
        second_requirement = coverage_requirement_id(
            derive_coverage_requirement(second_view), second_view
        )

        self.assertNotEqual(first_horizon.digest, second_horizon.digest)
        self.assertEqual(first_requirement, second_requirement)

    def test_selected_suite_input_changes_subject_requirement(self) -> None:
        compiled = self.compiled(relationship=True)
        first_horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        unit = self.corpus.policy_units[0]
        first_view = derive_coverage_view(unit, compiled, first_horizon)
        first_requirement = coverage_requirement_id(
            derive_coverage_requirement(first_view), first_view
        )

        self.write("inputs/consumer.md", "# Consumer changed\n")
        self.write_suite_projection()
        second_horizon = load_coverage_horizon(
            self.root, self.corpus, compiled, "horizon.toml"
        )
        second_view = derive_coverage_view(unit, compiled, second_horizon)
        second_requirement = coverage_requirement_id(
            derive_coverage_requirement(second_view), second_view
        )

        self.assertNotEqual(first_requirement, second_requirement)

    def test_reading_authority_label_does_not_change_coverage(self) -> None:
        compiled = self.compiled()
        first = load_coverage_horizon(self.root, self.corpus, compiled, "horizon.toml")
        artifact = compiled.artifact_for("consumer")
        reading_only = load_coverage_horizon(
            self.root,
            self.corpus,
            replace(compiled, artifacts={"consumer": replace(artifact, authority="evidence")}),
            "horizon.toml",
        )
        self.assertEqual(first.digest, reading_only.digest)

    def test_unrelated_relationship_does_not_change_subject_definition(self) -> None:
        compiled = self.compiled()
        unrelated = PolicyImpactSemantics(
            "edge.other.consumer",
            "workflow.other.rule",
            "consumer",
            "documentation-projection",
            self.schema.compile({"operator": "always"}),
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

    def test_selected_relationship_changes_only_its_subject_requirement(self) -> None:
        without_relationship = self.compiled()
        with_relationship = self.compiled(relationship=True)
        first_horizon = load_coverage_horizon(
            self.root, self.corpus, without_relationship, "horizon.toml"
        )
        second_horizon = load_coverage_horizon(
            self.root, self.corpus, with_relationship, "horizon.toml"
        )
        unit = self.corpus.policy_units[0]
        first = derive_coverage_requirement(
            derive_coverage_view(unit, without_relationship, first_horizon)
        )
        second = derive_coverage_requirement(
            derive_coverage_view(unit, with_relationship, second_horizon)
        )

        self.assertNotEqual(first, second)
        definitions = compile_coverage_definitions(
            self.corpus, with_relationship, second_horizon
        )
        self.assertEqual(tuple(definitions.requirements), (unit.id,))

    def test_current_repository_attestation_is_validated_and_loaded(self) -> None:
        self.write_attestations()

        decisions = self.load_decisions()

        self.assertEqual(decisions.covered_subjects, {"workflow.policy.rule"})
        attestation = decisions.attestations["workflow.policy.rule"]
        authorization_id = attestation["authorization_id"]
        self.assertIn(authorization_id, decisions.authorization_records)
        self.assertEqual(
            decisions.input_sources,
            tuple(sorted(decisions.input_sources)),
        )
        self.assertTrue(
            {
                "attestation-sources.toml",
                "attestations.toml",
                "authorization.toml",
                "revocations.toml",
                "evidence/review.md",
                "evidence/authorization.md",
            }.issubset(decisions.input_sources)
        )

    def test_pinned_attestation_rejects_changed_review_or_exclusion_bytes(self):
        for changed in ("evidence/review.md", "evidence/exclusion.md"):
            with self.subTest(changed=changed):
                self.write("evidence/review.md", "Reviewed evidence.\n")
                self.write("evidence/exclusion.md", "Reviewed exclusion.\n")
                self.write_attestations(
                    pinned=True, exclusions=("evidence/exclusion.md",)
                )
                decisions = self.load_decisions()
                self.assertEqual(decisions.covered_subjects, {"workflow.policy.rule"})
                self.assertIn("evidence/exclusion.md", decisions.input_sources)
                self.write(changed, "Changed after review.\n")
                with self.assertRaises(AnalysisError) as caught:
                    self.load_decisions()
                self.assertEqual(
                    caught.exception.failure.code, "ANALYSIS.EVIDENCE_DIGEST_MISMATCH"
                )

    def test_pinned_attestation_remains_bound_to_its_requirement(self):
        self.write_attestations(pinned=True, requirement_id="sha256:" + "0" * 64)
        self.assertFalse(self.load_decisions().covered_subjects)

    def test_pinned_attestation_rejects_unknown_provider(self):
        self.write_attestations(pinned=True)
        path = self.root / "attestations.toml"
        path.write_text(
            path.read_text().replace(
                'provider_contract = "repository-content"',
                'provider_contract = "unknown"',
            )
        )
        with self.assertRaises(AnalysisError) as caught:
            self.load_decisions()
        self.assertEqual(caught.exception.failure.code, "COVERAGE.EVIDENCE")

    def test_stale_repository_attestation_is_not_current_coverage(self) -> None:
        self.write_attestations(requirement_id="sha256:" + "0" * 64)

        decisions = self.load_decisions()

        self.assertFalse(decisions.covered_subjects)

    def test_selected_input_change_stales_exact_repository_attestation(self) -> None:
        self.write_attestations()

        self.write("inputs/consumer.md", "# Consumer changed\n")
        self.write_suite_projection()

        self.assertFalse(self.load_decisions().covered_subjects)

    def test_unrelated_input_change_preserves_exact_repository_attestation(
        self,
    ) -> None:
        self.write_attestations()

        self.write("inputs/unrelated.md", "# Unrelated changed\n")
        self.write_suite_projection()

        self.assertEqual(
            self.load_decisions().covered_subjects,
            {"workflow.policy.rule"},
        )

    def test_repository_attestation_rejects_malformed_requirement_id(self) -> None:
        self.write_attestations(requirement_id="not-a-requirement")

        with self.assertRaises(AnalysisError) as caught:
            self.load_decisions()

        self.assertEqual(caught.exception.failure.code, "COVERAGE.REQUIREMENT_ID")

    def test_duplicate_current_repository_attestations_are_rejected(self) -> None:
        self.write_attestations(duplicate=True)

        with self.assertRaises(AnalysisError) as caught:
            self.load_decisions()

        self.assertEqual(caught.exception.failure.code, "COVERAGE.DUPLICATE_SUBJECT")

    def test_repository_attestation_requires_authorized_principal(self) -> None:
        self.write_attestations(principal="principal.other")

        with self.assertRaises(AnalysisError) as caught:
            self.load_decisions()

        self.assertEqual(
            caught.exception.failure.code,
            "COVERAGE.UNAUTHORIZED_PRINCIPAL",
        )

    def test_repository_coverage_grant_can_be_revoked_without_identity_cycle(self) -> None:
        self.write_attestations()
        definitions = self.definitions()
        requirement_id = coverage_requirement_id(
            definitions.requirements["workflow.policy.rule"],
            definitions.views["workflow.policy.rule"],
        )
        grant = analysis_identity(
            "coding-standards:repository-coverage-grant-key:v1",
            "coverage-grant",
            {
                "issuer": "issuer.coverage",
                "principal": "principal.coverage",
                "requirement": requirement_id,
                "capability": "standards.review.audit",
            },
        )
        self.write(
            "revocations.toml",
            f"""
            schema_version = 1
            authority_id = "authority.revocations"
            semantic_revision = 1
            revoked_grants = ["{grant}"]
            """,
        )

        with self.assertRaises(AnalysisError) as caught:
            self.load_decisions()

        self.assertEqual(
            caught.exception.failure.code,
            "COVERAGE.AUTHORIZATION_REVOKED",
        )


if __name__ == "__main__":
    unittest.main()
