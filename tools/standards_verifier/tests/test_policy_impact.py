from __future__ import annotations

import tempfile
import textwrap
import tomllib
import unittest
from dataclasses import replace
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ENGINE_ROOT))

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_analysis.standards_analysis import compile_coverage
from tools.standards_metadata.standards_metadata import (
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    PolicyImpactError,
    compile_policy_impact,
)

from standards_verifier.config import load_registry
from standards_verifier.diagnostics import EngineError
from standards_verifier.policy_impact import (
    DEFAULT_SOURCE_REGISTRY,
    load_policy_impact,
    load_registered_policy_impact,
)
from standards_verifier.repository_graph import load_repository_registry


class PolicyImpactTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write(
            "workflows/planning.md",
            """
            # Planning Workflow

            **Standards metadata**

            - ID: `workflow.planning`
            - Role: `workflow`
            - Level: `MUST`
            - Applies when: Planned work requires stable sequencing.
            - Does not apply when: Work is bounded and local.
            - Requires: `none`
            - Specializes: `none`
            - Verification: Policy impact fixtures.
            - Canonical owner: `workflows/planning.md`

            ## Fixture Policy

            Fixture policy meaning.
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/canonical-module-corpus.toml",
            'schema_version = 1\nmembers = ["workflows/planning.md"]\n',
        )
        for path in (
            "prompts/a.md",
            "prompts/b.md",
            "reference/recipes/a.md",
            "evaluation/README.md",
        ):
            self.write(path, "# Fixture\n")
        self.write("evaluation/not-documentation.tsv", "value\n")
        self.write(
            "suites/evidence.toml",
            'schema_version = 1\nid = "evidence"\nowner = "test.evidence"\n',
        )
        self.suite_paths = {"evidence": "suites/evidence.toml"}
        self.write(
            "evaluation/standards-effectiveness/policy-units/registry.toml",
            """
            schema_version = 1
            sources = ["evaluation/standards-effectiveness/policy-units/planning.toml"]
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/policy-units/planning.toml",
            """
            schema_version = 1

            [[policy_unit]]
            id = "workflow.planning.fixture-policy"
            module = "workflow.planning"
            heading_path = ["Fixture Policy"]
            semantic_revision = 1
            """,
        )
        self.write_fixture_authority()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_fixture_authority(self) -> None:
        self.write(
            "catalog.toml",
            """
            schema_version = 1
            source_id = "standards.policy-impact-catalog"
            edges = []

            [[nodes]]
            id = "prompt-a"
            metadata = { repository_path = "prompts/a.md" }

            [[nodes]]
            id = "prompt-b"
            metadata = { repository_path = "prompts/b.md" }

            [[nodes]]
            id = "reference-a"
            metadata = { repository_path = "reference/recipes/a.md" }

            [[nodes]]
            id = "documentation"
            metadata = { repository_path = "evaluation/README.md" }

            [[nodes]]
            id = "not-documentation"
            metadata = { repository_path = "evaluation/not-documentation.tsv" }

            [[nodes]]
            id = "evidence"
            aliases = ["suites/evidence.toml"]
            metadata = { repository_path = "suites/evidence.toml", suite_id = "evidence" }

            [[groups]]
            id = "policy-impact"
            purpose = "Fixture policy impact."
            directions = ["incoming", "outgoing"]
            transitive = false

            [[groups]]
            id = "semantic"
            purpose = "Fixture semantics."
            directions = ["incoming", "outgoing"]
            transitive = false
            """,
        )
        self.write(
            "facts.toml",
            'schema_version = 1\nid = "policy-impact.applicability"\nfacts = []\n',
        )
        self.write(
            "evaluation/standards-effectiveness/suite-registry.toml",
            """
            schema_version = 1

            [[suites]]
            id = "evidence"
            path = "suites/evidence.toml"
            requires = []
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/edge-source-registry.toml",
            "schema_version = 1\nsources = []\n",
        )
        self.write(
            "evaluation/standards-effectiveness/policy-coverage/horizons.toml",
            """
            schema_version = 1
            id = "audit-horizon.policy-impact-consumers"
            provider = "standards-analysis:policy-impact-consumer-horizon"
            version = 2
            suite_registry = "evaluation/standards-effectiveness/suite-registry.toml"
            edge_source_registry = "evaluation/standards-effectiveness/edge-source-registry.toml"
            policy_impact_node_catalog = "catalog.toml"
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml",
            "schema_version = 1\nsources = []\n",
        )
        self.write("coverage-evidence.md", "# Reviewed fixture coverage\n")

    @staticmethod
    def relationship(
        consumer: str = "prompt-a",
        relation: str = "prompt-projection",
        *,
        source: str = "workflow.planning.fixture-policy",
        evidence: str = "suite:evidence",
    ) -> str:
        return textwrap.dedent(
            f"""
            [[relationships]]
            source = "{source}"
            consumer = "{consumer}"
            relation = "{relation}"
            applicability = {{ operator = "always" }}
            evidence_owner = "{evidence}"
            rationale = "Fixture relationship."
            """
        )

    def load(self, *relationships: str, owner: str = "workflow.planning"):
        self.write(
            "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml",
            "schema_version = 1\nsources = []\n",
        )
        self.write(
            "declarations.toml",
            (
                f'schema_version = 1\nowner = "{owner}"\n'
                + ("".join(relationships) if relationships else "relationships = []\n")
            ),
        )
        self.write(
            "registry.toml",
            """
            schema_version = 1
            source_id = "standards.policy-impact"
            node_catalog = "catalog.toml"
            fact_catalog = "facts.toml"
            declaration_sources = ["declarations.toml"]
            """,
        )
        try:
            corpus = load_canonical_standards_corpus(self.root)
            compiled = compile_policy_impact(self.root, corpus, "registry.toml")
            coverage = compile_coverage(self.root, corpus, compiled)
        except PolicyImpactError:
            pass
        else:
            requirement = coverage.requirements["workflow.planning.fixture-policy"]
            self.write(
                "coverage-attestations.toml",
                f"""
                schema_version = 1

                [[attestations]]
                requirement = "{requirement.handle}"
                conclusion = "complete"
                evidence = ["coverage-evidence.md"]
                explicit_exclusions = []
                rationale = "Every registered fixture horizon member was reviewed."
                auditor_provenance = "test:policy-impact"
                """,
            )
            self.write(
                "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml",
                'schema_version = 1\nsources = ["coverage-attestations.toml"]\n',
            )
        return load_policy_impact(self.root, "registry.toml", self.suite_paths)

    def test_adapter_queries_compiled_registry_in_deterministic_consumer_order(self) -> None:
        impact = self.load(
            self.relationship("prompt-b"),
            self.relationship("prompt-a"),
        )

        self.assertIsInstance(impact.registry, EdgeRegistry)
        self.assertEqual(
            [edge.consumer for edge in impact.consumers_for("workflow.planning")],
            ["prompts/a.md", "prompts/b.md"],
        )
        self.assertEqual(
            impact.consumers_for("workflow.planning")[0]
            .applicability_program.as_expression(),
            {"operator": "always"},
        )

    def test_rejects_unknown_owner_and_evidence_owner(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(
                self.relationship(source="workflow.unknown"),
                owner="workflow.unknown",
            )
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_OWNER")

        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship(evidence="suite:missing"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.EVIDENCE_OWNER")

    def test_relation_specific_consumer_validation_remains_downstream(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship("prompt-a", "template-projection"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_CONSUMER")

        reference = self.load(self.relationship("reference-a", "reference-projection"))
        self.assertEqual(reference.consumers_for("workflow.planning")[0].consumer, "reference/recipes/a.md")

        documentation = self.load(
            self.relationship("documentation", "documentation-projection")
        )
        self.assertEqual(documentation.consumers_for("workflow.planning")[0].consumer, "evaluation/README.md")

        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship("not-documentation", "documentation-projection"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_CONSUMER")

    def test_uncovered_owner_query_is_typed_unavailable(self) -> None:
        impact = self.load(self.relationship())
        with self.assertRaises(EngineError) as raised:
            impact.consumers_for("workflow.unknown")
        self.assertEqual(raised.exception.exit_code, 3)
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.OWNER_NOT_AUDITED")

    def test_successful_empty_impact_requires_current_coverage_certificate(self) -> None:
        covered = self.load()
        self.assertEqual(covered.consumers_for("workflow.planning"), ())

        uncovered = replace(
            covered,
            coverage=replace(covered.coverage, certificates={}),
        )
        with self.assertRaises(EngineError) as raised:
            uncovered.consumers_for("workflow.planning")
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.OWNER_NOT_AUDITED",
        )

    def test_requires_enforcement_edge_for_every_suite_owned_by_covered_owner(self) -> None:
        self.write(
            "suites/evidence.toml",
            'schema_version = 1\nid = "evidence"\nowner = "workflow.planning"\n',
        )
        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship())
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.MISSING_ENFORCEMENT_SUITE_EDGE",
        )

    def test_current_planning_graph_has_complete_alias_and_suite_closure(self) -> None:
        entries = load_registry(REPO_ROOT, "evaluation/standards-effectiveness/suite-registry.toml")
        impact = load_registered_policy_impact(
            REPO_ROOT,
            DEFAULT_SOURCE_REGISTRY,
            {entry.id: entry.path for entry in entries},
        )
        consumers = {edge.consumer for edge in impact.consumers_for("workflow.planning")}
        graph = load_repository_registry(REPO_ROOT, DEFAULT_SOURCE_REGISTRY)

        self.assertEqual(len(consumers), 24)
        self.assertTrue(
            {
                "prompts/full-codebase-standards-refactor.md",
                "evaluation/standards-effectiveness/fixtures/planning/full-review-prompt-decisions.tsv",
                "evaluation/standards-effectiveness/suites/full-review-prompt-entrypoint.toml",
            }.issubset(consumers)
        )
        self.assertEqual(graph.outgoing("workflow.planning", ("policy-impact",)), ())
        self.assertEqual(
            graph.incident("workflow.planning", ("policy-impact",)),
            graph.incident("workflows/planning.md", ("policy-impact",)),
        )
        planning_owned_suites = set()
        for entry in entries:
            with (REPO_ROOT / entry.path).open("rb") as handle:
                if tomllib.load(handle).get("owner") == "workflow.planning":
                    planning_owned_suites.add(entry.path)
        self.assertTrue(planning_owned_suites.issubset(consumers))

    def test_current_commit_graph_has_complete_alias_and_suite_closure(self) -> None:
        entries = load_registry(REPO_ROOT, "evaluation/standards-effectiveness/suite-registry.toml")
        impact = load_registered_policy_impact(
            REPO_ROOT,
            DEFAULT_SOURCE_REGISTRY,
            {entry.id: entry.path for entry in entries},
        )
        consumers = {edge.consumer for edge in impact.consumers_for("workflow.commit")}
        graph = load_repository_registry(REPO_ROOT, DEFAULT_SOURCE_REGISTRY)

        self.assertEqual(len(consumers), 15)
        self.assertEqual(graph.outgoing("workflow.commit", ("policy-impact",)), ())
        self.assertEqual(
            graph.incident("workflow.commit", ("policy-impact",)),
            graph.incident("workflows/commit.md", ("policy-impact",)),
        )

    def test_old_policy_query_and_bespoke_graph_files_are_absent(self) -> None:
        self.assertFalse((REPO_ROOT / "tools/standards_verifier/query_policy_impact.py").exists())
        self.assertFalse((REPO_ROOT / "tools/standards_verifier/standards_verifier/policy_impact_cli.py").exists())


if __name__ == "__main__":
    unittest.main()
