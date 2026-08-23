from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = REPO_ROOT / "tools/standards_verifier"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ENGINE_ROOT))

from tools.standards_metadata.standards_metadata import load_canonical_module_corpus
from standards_verifier.graph_adapters import (
    METADATA_REQUIRES,
    METADATA_SPECIALIZES,
)
from standards_verifier.repository_graph import load_repository_registry


SOURCE_REGISTRY = "evaluation/standards-effectiveness/edge-source-registry.toml"


class RepositoryGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_repository_registry(REPO_ROOT, SOURCE_REGISTRY)

    def test_repository_composition_registers_every_migrated_group(self) -> None:
        self.assertEqual(
            set(self.registry.groups),
            {
                "policy-impact",
                "semantic",
                "standards-dependencies",
                "standards-requires",
                "standards-specializes",
                "suite-dependencies",
            },
        )

    def test_one_artifact_reports_edges_from_independent_registered_sources(self) -> None:
        groups = {group.id for group in self.registry.groups_for("workflow.implementation")}

        self.assertEqual(
            groups,
            {
                "policy-impact",
                "semantic",
                "standards-dependencies",
                "standards-requires",
            },
        )

    def test_suite_id_and_path_report_policy_and_dependency_edges(self) -> None:
        suite_id = "concurrent-plan-integration"
        suite_path = "evaluation/standards-effectiveness/suites/concurrent-plan-integration.toml"

        self.assertEqual(
            self.registry.incident(suite_id),
            self.registry.incident(suite_path),
        )
        self.assertEqual(
            {group.id for group in self.registry.groups_for(suite_id)},
            {"policy-impact", "semantic", "suite-dependencies"},
        )

    def test_existing_unregistered_artifact_returns_empty_incidence(self) -> None:
        self.assertEqual(self.registry.incident("LICENSE"), ())

    def test_every_corpus_member_resolves_by_id_and_path(self) -> None:
        corpus = load_canonical_module_corpus(REPO_ROOT)

        for module in corpus.modules:
            with self.subTest(module=module.module_id):
                self.assertEqual(self.registry.resolve(module.module_id), module.module_id)
                self.assertEqual(self.registry.resolve(module.path), module.module_id)

    def test_metadata_edges_exactly_match_canonical_document_relations(self) -> None:
        corpus = load_canonical_module_corpus(REPO_ROOT)
        expected_requires = {
            f"metadata-requires:{module.module_id}->{target}"
            for module in corpus.modules
            for target in module.requires
        }
        expected_specializes = {
            f"metadata-specializes:{module.module_id}->{target}"
            for module in corpus.modules
            for target in module.specializes
        }

        self.assertEqual(
            {edge.id for edge in self.registry.edges_for_group(METADATA_REQUIRES)},
            expected_requires,
        )
        self.assertEqual(
            {edge.id for edge in self.registry.edges_for_group(METADATA_SPECIALIZES)},
            expected_specializes,
        )

    def test_previously_unselected_normative_and_reference_aliases_resolve(self) -> None:
        aliases = (
            ("topic.performance", "topics/performance.md"),
            ("workflow.planning", "workflows/planning.md"),
            (
                "profile.workflow.concurrent-plan-integration",
                "profiles/workflows/concurrent-plan-integration.md",
            ),
            ("reference.recipes.commits", "reference/recipes/commits.md"),
        )

        for module_id, path in aliases:
            with self.subTest(module=module_id):
                self.assertEqual(self.registry.resolve(module_id), module_id)
                self.assertEqual(self.registry.resolve(path), module_id)
                self.assertEqual(
                    self.registry.incident(module_id),
                    self.registry.incident(path),
                )

    def test_canonical_cli_uses_the_complete_repository_composition(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "tools/query_edges.py"),
                "--node",
                "concurrent-plan-integration",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("policy-impact,semantic", completed.stdout)
        self.assertIn("suite-dependencies", completed.stdout)
