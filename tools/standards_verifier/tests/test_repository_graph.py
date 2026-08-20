from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_ROOT = REPO_ROOT / "tools/standards_verifier"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ENGINE_ROOT))

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
