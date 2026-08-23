from __future__ import annotations

import tempfile
import textwrap
import unittest
import json
from pathlib import Path

from tools.graph_engine.graph_engine import GraphContribution
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_metadata.standards_metadata import (
    CanonicalModuleCorpus,
    CanonicalStandardsCorpus,
    ModuleMetadata,
    PolicyUnit,
    PolicyUnitCorpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    PolicyImpactSemantics,
)
from tools.standards_engine.contracts.validate_contracts import validate

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    compile_coverage,
    derive_coverage_requirement,
    derive_coverage_view,
    load_coverage_horizon,
)


class CoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write("workflows/policy.md", "# Policy\n\n## Rule\n\nMeaning.\n")
        self.write("suites/coverage.toml", 'schema_version = 1\nid = "coverage"\nowner = "test"\n[[checks]]\nid = "input"\ntype = "text"\npath = "inputs/consumer.md"\n')
        self.write("inputs/consumer.md", "# Consumer\n")
        self.write("evidence.md", "# Reviewed coverage\n")
        self.write(
            "suite-registry.toml",
            'schema_version = 1\n[[suites]]\nid = "coverage"\npath = "suites/coverage.toml"\nrequires = []\n',
        )
        self.write("edge-sources.toml", "schema_version = 1\nsources = []\n")
        self.write(
            "catalog.toml",
            'schema_version = 1\nsource_id = "standards.policy-impact-catalog"\nedges = []\nnodes = []\ngroups = []\n',
        )
        self.write(
            "horizon.toml",
            """
            schema_version = 1
            id = "audit-horizon.policy-impact-consumers"
            provider = "standards-analysis:policy-impact-consumer-horizon"
            version = 1
            suite_registry = "suite-registry.toml"
            edge_source_registry = "edge-sources.toml"
            policy_impact_node_catalog = "catalog.toml"
            """,
        )
        self.write("attestation-sources.toml", "schema_version = 1\nsources = []\n")

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

    def compiled(self, *, relationship: bool = False) -> CompiledPolicyImpactSet:
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
                "policy-coverage/attestations/relationship.toml",
                "sha256:" + "3" * 64,
            )
        return CompiledPolicyImpactSet(
            GraphContribution((), (), ()),
            semantics,
            self.schema,
            "catalog.toml",
            ("declarations.toml",),
            ("registry.toml", "catalog.toml"),
            "sha256:" + ("4" if relationship else "5") * 64,
            "sha256:" + "6" * 64,
        )

    def test_horizon_uses_registered_suite_inputs_and_fingerprints_content(self) -> None:
        first = load_coverage_horizon(self.root, self.corpus, "horizon.toml")
        ids = {member.id for member in first.members}
        self.assertIn("suite:coverage", ids)
        self.assertIn("repository:inputs/consumer.md", ids)

        self.write("inputs/consumer.md", "# Consumer\n\nNow consumes policy.\n")
        second = load_coverage_horizon(self.root, self.corpus, "horizon.toml")
        self.assertNotEqual(first.digest, second.digest)

    def test_unrelated_relationship_state_does_not_invalidate_view(self) -> None:
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
        changed = CompiledPolicyImpactSet(
            compiled.graph,
            {unrelated.edge_id: unrelated},
            compiled.fact_schema,
            compiled.node_catalog,
            compiled.declaration_sources,
            compiled.input_sources,
            "sha256:" + "8" * 64,
            compiled.provider_contract_digest,
        )
        horizon = load_coverage_horizon(self.root, self.corpus, "horizon.toml")
        unit = self.corpus.policy_unit_corpus.units[0]

        self.assertEqual(
            derive_coverage_view(unit, compiled, horizon).handle,
            derive_coverage_view(unit, changed, horizon).handle,
        )

    def test_attestation_changes_complete_inputs_without_changing_requirement(self) -> None:
        compiled = self.compiled()
        empty = compile_coverage(
            self.root,
            self.corpus,
            compiled,
            horizon_path="horizon.toml",
            attestation_registry_path="attestation-sources.toml",
            derived_from_snapshot="snapshot:sha256:" + "a" * 64,
        )
        requirement = empty.requirements["workflow.policy.rule"]
        self.write(
            "attestations.toml",
            f"""
            schema_version = 1
            [[attestations]]
            requirement = "{requirement.handle}"
            conclusion = "complete"
            evidence = ["evidence.md"]
            explicit_exclusions = []
            rationale = "The exact registered horizon was reviewed."
            auditor_provenance = "reviewer:test"
            """,
        )
        self.write(
            "attestation-sources.toml",
            'schema_version = 1\nsources = ["attestations.toml"]\n',
        )
        resolved = compile_coverage(
            self.root,
            self.corpus,
            compiled,
            horizon_path="horizon.toml",
            attestation_registry_path="attestation-sources.toml",
            derived_from_snapshot="snapshot:sha256:" + "b" * 64,
        )
        self.assertEqual(
            requirement.handle,
            resolved.requirements["workflow.policy.rule"].handle,
        )
        self.assertEqual(
            empty.views["workflow.policy.rule"].handle,
            resolved.views["workflow.policy.rule"].handle,
        )
        self.assertIsNotNone(resolved.certificate_for("workflow.policy.rule"))
        schema_path = Path(__file__).resolve().parents[2] / "standards_engine/contracts/a1-contract.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        attestation = next(iter(resolved.attestations.values()))
        certificate = resolved.certificate_for("workflow.policy.rule")
        assert certificate is not None
        for definition, value in (
            ("CoverageAuthorityView", resolved.views["workflow.policy.rule"].as_projection()),
            ("CoverageAuditRequirement", resolved.requirements["workflow.policy.rule"].as_projection()),
            ("CoverageAttestation", attestation.as_projection()),
            ("ConsumerCoverageCertificate", certificate.as_projection()),
        ):
            validate(schema, schema["$defs"][definition], value, definition)

    def test_stale_attestation_rejects_and_relationship_location_cannot_escape(self) -> None:
        horizon = load_coverage_horizon(self.root, self.corpus, "horizon.toml")
        plain_view = derive_coverage_view(
            self.corpus.policy_units[0],
            self.compiled(),
            horizon,
        )
        relationship_view = derive_coverage_view(
            self.corpus.policy_units[0],
            self.compiled(relationship=True),
            horizon,
        )
        self.assertNotEqual(plain_view.handle, relationship_view.handle)
        self.assertNotIn("attestations", str(relationship_view.as_identity_projection()))

        requirement = derive_coverage_requirement(plain_view)
        self.write(
            "attestations.toml",
            """
            schema_version = 1
            [[attestations]]
            requirement = "coverage-requirement:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            conclusion = "complete"
            evidence = ["evidence.md"]
            explicit_exclusions = []
            rationale = "Stale fixture."
            auditor_provenance = "reviewer:test"
            """,
        )
        self.write(
            "attestation-sources.toml",
            'schema_version = 1\nsources = ["attestations.toml"]\n',
        )
        self.assertTrue(requirement.handle.startswith("coverage-requirement:"))
        with self.assertRaises(AnalysisError) as caught:
            compile_coverage(
                self.root,
                self.corpus,
                self.compiled(),
                horizon_path="horizon.toml",
                attestation_registry_path="attestation-sources.toml",
            )
        self.assertEqual(caught.exception.failure.code, "COVERAGE.STALE_ATTESTATION")


if __name__ == "__main__":
    unittest.main()
