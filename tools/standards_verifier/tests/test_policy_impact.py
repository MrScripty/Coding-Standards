from __future__ import annotations

# ruff: noqa: E402 - repository package roots must be installed before imports.

import os
import subprocess
import tempfile
import sys
import textwrap
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ENGINE_ROOT))

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_metadata.standards_metadata import (
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (
    DEFAULT_AUTHORING_CONTRACT,
    compile_policy_impact,
)

from standards_verifier.diagnostics import EngineError
from standards_verifier.checks.policy_impact_migration import (
    _changed_production_paths,
    _materialized_tree,
)
from standards_verifier.model import CheckContext, SuiteCatalog
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
            schema_version = 2
            source_id = "standards.policy-impact-catalog"

            [[nodes]]
            id = "prompt-a"
            metadata = { repository_path = "prompts/a.md", artifact_kind = "prompt", authority = "projection" }

            [[nodes]]
            id = "prompt-b"
            metadata = { repository_path = "prompts/b.md", artifact_kind = "prompt", authority = "projection" }

            [[nodes]]
            id = "documentation"
            metadata = { repository_path = "evaluation/README.md", artifact_kind = "documentation", authority = "projection" }

            [[nodes]]
            id = "not-documentation"
            metadata = { repository_path = "evaluation/not-documentation.tsv", artifact_kind = "fixture", authority = "evidence" }

            [[nodes]]
            id = "evidence"
            aliases = ["suites/evidence.toml"]
            metadata = { repository_path = "suites/evidence.toml", artifact_kind = "enforcement-suite", suite_id = "evidence", authority = "evidence" }
            """,
        )
        self.write(
            "contract.toml",
            (REPO_ROOT / DEFAULT_AUTHORING_CONTRACT).read_text(encoding="utf-8"),
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
            """
            schema_version = 1

            [[sources]]
            id = "standards.policy-impact"
            kind = "provider"
            provider = "standards.policy-impact"
            """,
        )
        self.write(
            "evaluation/standards-effectiveness/policy-coverage/horizons.toml",
            """
            schema_version = 1
            id = "audit-horizon.policy-impact-consumers"
            provider = "standards-analysis:policy-impact-consumer-horizon"
            version = 3
            suite_registry = "evaluation/standards-effectiveness/suite-registry.toml"
            edge_source_registry = "evaluation/standards-effectiveness/edge-source-registry.toml"
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
                f'schema_version = 2\nowner = "{owner}"\n'
                + ("".join(relationships) if relationships else "relationships = []\n")
            ),
        )
        self.write(
            "registry.toml",
            """
            schema_version = 2
            source_id = "standards.policy-impact"
            authoring_contract = "contract.toml"
            node_catalog = "catalog.toml"
            fact_catalog = "facts.toml"
            suite_registry = "evaluation/standards-effectiveness/suite-registry.toml"
            declaration_sources = ["declarations.toml"]
            """,
        )
        return load_policy_impact(self.root, "registry.toml", self.suite_paths)

    def test_adapter_queries_compiled_registry_in_deterministic_consumer_order(
        self,
    ) -> None:
        impact = self.load(
            self.relationship("prompt-b"),
            self.relationship("prompt-a"),
        )

        self.assertIsInstance(impact.registry, EdgeRegistry)
        self.assertEqual(
            [
                edge.consumer
                for edge in impact.declared_consumers_for("workflow.planning")
            ],
            ["prompts/a.md", "prompts/b.md"],
        )
        self.assertEqual(
            impact.declared_consumers_for("workflow.planning")[
                0
            ].applicability_program.as_expression(),
            {"operator": "always"},
        )

    def test_rejects_unknown_owner_and_evidence_owner(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(
                self.relationship(source="workflow.unknown"),
                owner="workflow.unknown",
            )
        self.assertEqual(
            raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_OWNER"
        )

        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship(evidence="suite:missing"))
        self.assertEqual(
            raised.exception.diagnostic.code, "POLICY_IMPACT.EVIDENCE_OWNER"
        )

    def test_registered_loader_translates_compiler_failure(self) -> None:
        default_registry = (
            "evaluation/standards-effectiveness/policy-impact-registry.toml"
        )
        self.write(
            default_registry,
            """
            schema_version = 2
            source_id = "standards.policy-impact"
            authoring_contract = "contract.toml"
            node_catalog = "catalog.toml"
            fact_catalog = "facts.toml"
            suite_registry = "evaluation/standards-effectiveness/suite-registry.toml"
            declaration_sources = ["declarations.toml"]
            """,
        )
        self.write(
            "declarations.toml",
            'schema_version = 2\nowner = "workflow.planning"\nrelationships = []\n',
        )
        contract = self.root / "contract.toml"
        contract.write_text(
            contract.read_text(encoding="utf-8").replace(
                'evidence_owner_rule = "required-registered-suite"',
                'evidence_owner_rule = "optional"',
            ),
            encoding="utf-8",
        )

        with self.assertRaises(EngineError) as raised:
            load_registered_policy_impact(
                self.root,
                "evaluation/standards-effectiveness/edge-source-registry.toml",
                self.suite_paths,
                suite="fixture-suite",
                check="fixture-check",
            )
        diagnostic = raised.exception.diagnostic
        self.assertEqual(diagnostic.code, "POLICY_IMPACT.UNSUPPORTED_CONTRACT")
        self.assertEqual(diagnostic.suite, "fixture-suite")
        self.assertEqual(diagnostic.check, "fixture-check")
        self.assertEqual(diagnostic.field, "evidence_owner_rule")

    def test_compiler_owns_relation_target_compatibility(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.relationship("prompt-a", "template-projection"))
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.INCOMPATIBLE_TARGET",
        )

        documentation = self.load(
            self.relationship("documentation", "documentation-projection")
        )
        self.assertEqual(
            documentation.declared_consumers_for("workflow.planning")[0].consumer,
            "evaluation/README.md",
        )

        with self.assertRaises(EngineError) as raised:
            self.load(
                self.relationship("not-documentation", "documentation-projection")
            )
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.INCOMPATIBLE_TARGET",
        )

    def test_uncovered_owner_query_is_typed_unavailable(self) -> None:
        impact = self.load(self.relationship())
        with self.assertRaises(EngineError) as raised:
            impact.consumers_for("workflow.unknown")
        self.assertEqual(raised.exception.exit_code, 3)
        self.assertEqual(
            raised.exception.diagnostic.code, "POLICY_IMPACT.OWNER_NOT_AUDITED"
        )

    def test_custom_manifest_has_no_implicit_coverage_authority(self) -> None:
        uncovered = self.load()
        self.assertEqual(uncovered.declared_consumers_for("workflow.planning"), ())
        with self.assertRaises(EngineError) as raised:
            uncovered.consumers_for("workflow.planning")
        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.OWNER_NOT_AUDITED",
        )

    def test_registered_loader_consumes_engine_coverage_authority(self) -> None:
        covered = load_registered_policy_impact(
            REPO_ROOT,
            DEFAULT_SOURCE_REGISTRY,
            {},
        )
        self.assertIn("workflow.planning", covered.covered_owners)

    def test_current_planning_graph_has_explicit_consumer_and_alias_closure(
        self,
    ) -> None:
        corpus = load_canonical_standards_corpus(REPO_ROOT)
        compiled = compile_policy_impact(REPO_ROOT, corpus)
        graph = load_repository_registry(REPO_ROOT, DEFAULT_SOURCE_REGISTRY)
        consumers = {
            compiled.artifact_for(semantics.consumer).repository_path
            if semantics.consumer in compiled.artifacts
            else graph.nodes[semantics.consumer].metadata["repository_path"]
            for semantics in compiled.semantics.values()
            if corpus.policy_unit_corpus.active_by_id(semantics.source).module
            == "workflow.planning"
        }

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

    def test_current_commit_graph_has_complete_alias_and_suite_closure(self) -> None:
        corpus = load_canonical_standards_corpus(REPO_ROOT)
        compiled = compile_policy_impact(REPO_ROOT, corpus)
        graph = load_repository_registry(REPO_ROOT, DEFAULT_SOURCE_REGISTRY)
        consumers = {
            compiled.artifact_for(semantics.consumer).repository_path
            if semantics.consumer in compiled.artifacts
            else graph.nodes[semantics.consumer].metadata["repository_path"]
            for semantics in compiled.semantics.values()
            if corpus.policy_unit_corpus.active_by_id(semantics.source).module
            == "workflow.commit"
        }

        self.assertIn(
            "evaluation/standards-effectiveness/suites/commit-consolidation-dispositions.toml",
            consumers,
        )
        self.assertEqual(graph.outgoing("workflow.commit", ("policy-impact",)), ())
        self.assertEqual(
            graph.incident("workflow.commit", ("policy-impact",)),
            graph.incident("workflows/commit.md", ("policy-impact",)),
        )

    def test_old_policy_query_and_bespoke_graph_files_are_absent(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "tools/standards_verifier/query_policy_impact.py").exists()
        )
        self.assertFalse(
            (
                REPO_ROOT
                / "tools/standards_verifier/standards_verifier/policy_impact_cli.py"
            ).exists()
        )

    @patch(
        "standards_verifier.checks.policy_impact_migration.staged_name_status"
    )
    def test_copied_production_source_does_not_retire_its_source(
        self, staged_name_status: Mock
    ) -> None:
        staged_name_status.return_value = (
            "C100",
            "tools/source.py",
            "tools/copied.py",
            "R100",
            "tools/old.py",
            "tools/renamed.py",
        )
        context = CheckContext(Path("."), "fixture", SuiteCatalog.empty())

        current, retired = _changed_production_paths(
            context, "migration", "a" * 40
        )

        self.assertEqual(
            current,
            frozenset({"tools/copied.py", "tools/renamed.py"}),
        )
        self.assertEqual(retired, frozenset({"tools/old.py"}))
        staged_name_status.assert_called_once_with(
            Path("."), "a" * 40, ("tools",)
        )

    def test_accepted_tree_materialization_ignores_ambient_git_overrides(
        self,
    ) -> None:
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        self.write("tools/current.py", "value = 1\n")
        subprocess.run(("git", "add", "-A"), cwd=self.root, check=True)
        tree = subprocess.run(
            ("git", "write-tree"),
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        context = CheckContext(self.root, "fixture", SuiteCatalog.empty())

        with patch.dict(
            os.environ,
            {"GIT_DIR": "/unavailable", "GIT_INDEX_FILE": "/unavailable/index"},
        ):
            with _materialized_tree(context, "migration", tree) as materialized:
                self.assertEqual(
                    (Path(materialized) / "tools/current.py").read_text(
                        encoding="utf-8"
                    ),
                    "value = 1\n",
                )


if __name__ == "__main__":
    unittest.main()
