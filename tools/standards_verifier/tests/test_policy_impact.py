from __future__ import annotations

import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ENGINE_ROOT))

from tools.graph_engine.graph_engine import EdgeRegistry

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
            """,
        )
        self.write("prompts/a.md", "# A\n")
        self.write("prompts/b.md", "# B\n")
        self.write("reference/recipes/a.md", "# A reference\n")
        self.write(
            "suites/evidence.toml",
            """
            schema_version = 1
            id = "evidence"
            owner = "test.evidence"
            """,
        )
        self.suite_paths = {"evidence": "suites/evidence.toml"}

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def manifest(
        self,
        *,
        owner_id: str = "workflow.planning",
        consumer: str = "prompts/a.md",
        relation: str = "prompt-projection",
        applicability: str = "Consumer applies when Planning changes.",
        evidence_owner: str = "suite:evidence",
        edge_id: str = "planning-consumer",
    ) -> str:
        return textwrap.dedent(
            f'''
            schema_version = 1
            source_id = "test.policy-impact"

            [[nodes]]
            id = "{owner_id}"
            aliases = ["workflows/planning.md"]
            metadata = {{ repository_path = "workflows/planning.md", policy_impact_coverage = "audited" }}

            [[nodes]]
            id = "{consumer}"
            metadata = {{ repository_path = "{consumer}" }}

            [[groups]]
            id = "policy-impact"
            purpose = "Test policy impact."
            directions = ["incoming", "outgoing"]
            transitive = false

            [[edges]]
            id = "{edge_id}"
            source = "{owner_id}"
            target = "{consumer}"
            relation = "{relation}"
            groups = ["policy-impact"]
            traversable = true
            metadata = {{ applicability = "{applicability}", evidence_owner = "{evidence_owner}" }}
            '''
        ).lstrip()

    def load(self, content: str):
        self.write("impact.toml", content)
        return load_policy_impact(self.root, "impact.toml", self.suite_paths)

    def test_adapter_queries_generic_registry_in_deterministic_consumer_order(self) -> None:
        content = self.manifest(consumer="prompts/b.md", edge_id="b")
        content = content.replace(
            "[[groups]]",
            """
            [[nodes]]
            id = "prompts/a.md"
            metadata = { repository_path = "prompts/a.md" }

            [[groups]]
            """,
            1,
        )
        content += """
        [[edges]]
        id = "a"
        source = "workflow.planning"
        target = "prompts/a.md"
        relation = "prompt-projection"
        groups = ["policy-impact"]
        traversable = true
        metadata = { applicability = "Consumer applies when Planning changes.", evidence_owner = "suite:evidence" }
        """

        impact = self.load(content)

        self.assertIsInstance(impact.registry, EdgeRegistry)
        self.assertEqual(
            [edge.consumer for edge in impact.consumers_for("workflow.planning")],
            ["prompts/a.md", "prompts/b.md"],
        )

    def test_rejects_owner_that_does_not_match_canonical_metadata(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(owner_id="workflow.unknown"))

        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_OWNER")

    def test_rejects_unknown_evidence_owner_and_invalid_consumer_relation(self) -> None:
        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(evidence_owner="suite:missing"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.EVIDENCE_OWNER")

        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(relation="template-projection"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_CONSUMER")

    def test_accepts_only_reference_markdown_for_reference_projection(self) -> None:
        impact = self.load(
            self.manifest(
                consumer="reference/recipes/a.md",
                relation="reference-projection",
            )
        )
        self.assertEqual(
            impact.consumers_for("workflow.planning")[0].consumer,
            "reference/recipes/a.md",
        )

        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest(relation="reference-projection"))
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.UNKNOWN_CONSUMER")

    def test_uncovered_owner_query_is_typed_unavailable(self) -> None:
        impact = self.load(self.manifest())

        with self.assertRaises(EngineError) as raised:
            impact.consumers_for("workflow.unknown")

        self.assertEqual(raised.exception.exit_code, 3)
        self.assertEqual(raised.exception.diagnostic.code, "POLICY_IMPACT.OWNER_NOT_AUDITED")

    def test_requires_enforcement_edge_for_every_suite_owned_by_audited_owner(self) -> None:
        self.write(
            "suites/evidence.toml",
            """
            schema_version = 1
            id = "evidence"
            owner = "workflow.planning"
            """,
        )

        with self.assertRaises(EngineError) as raised:
            self.load(self.manifest())

        self.assertEqual(
            raised.exception.diagnostic.code,
            "POLICY_IMPACT.MISSING_ENFORCEMENT_SUITE_EDGE",
        )

    def test_current_planning_graph_has_complete_alias_and_suite_closure(self) -> None:
        entries = load_registry(
            REPO_ROOT,
            "evaluation/standards-effectiveness/suite-registry.toml",
        )
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
        self.assertEqual(
            {view.edge.id for view in graph.incident("workflow.planning", ("policy-impact",))},
            {view.edge.id for view in graph.incident("workflows/planning.md", ("policy-impact",))},
        )
        planning_owned_suites = set()
        for entry in entries:
            with (REPO_ROOT / entry.path).open("rb") as handle:
                if tomllib.load(handle).get("owner") == "workflow.planning":
                    planning_owned_suites.add(entry.path)
        self.assertTrue(planning_owned_suites.issubset(consumers))

    def test_current_commit_graph_has_complete_alias_and_suite_closure(self) -> None:
        entries = load_registry(
            REPO_ROOT,
            "evaluation/standards-effectiveness/suite-registry.toml",
        )
        impact = load_registered_policy_impact(
            REPO_ROOT,
            DEFAULT_SOURCE_REGISTRY,
            {entry.id: entry.path for entry in entries},
        )
        consumers = {edge.consumer for edge in impact.consumers_for("workflow.commit")}
        graph = load_repository_registry(REPO_ROOT, DEFAULT_SOURCE_REGISTRY)

        self.assertEqual(
            consumers,
            {
                "STANDARDS-ROUTER.md",
                "workflows/implementation.md",
                "workflows/planning.md",
                "profiles/workflows/concurrent-plan-integration.md",
                "workflows/release.md",
                "prompts/planning.md",
                "prompts/implement-plan.md",
                "templates/PLAN-TEMPLATE.md",
                "reference/recipes/commits.md",
                "evaluation/standards-effectiveness/fixtures/commit/authority.tsv",
                "evaluation/standards-effectiveness/fixtures/commit/hook-bypass.tsv",
                "evaluation/standards-effectiveness/fixtures/commit/branch-lifecycle.tsv",
                "evaluation/standards-effectiveness/suites/commit-consolidation-dispositions.toml",
            },
        )
        self.assertEqual(
            {view.edge.id for view in graph.incident("workflow.commit", ("policy-impact",))},
            {view.edge.id for view in graph.incident("workflows/commit.md", ("policy-impact",))},
        )

    def test_old_policy_query_and_bespoke_graph_files_are_absent(self) -> None:
        self.assertFalse((REPO_ROOT / "tools/standards_verifier/query_policy_impact.py").exists())
        self.assertFalse(
            (
                REPO_ROOT
                / "tools/standards_verifier/standards_verifier/policy_impact_cli.py"
            ).exists()
        )
