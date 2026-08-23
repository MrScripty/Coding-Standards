from __future__ import annotations

import unittest
from pathlib import Path

from tools.graph_engine.graph_engine import Direction
from tools.standards_graph.standards_graph import (
    METADATA_REQUIRES,
    METADATA_SPECIALIZES,
    metadata_dependency_registry,
    standards_navigation_registry,
)
from tools.standards_metadata.standards_metadata import load_canonical_standards_corpus


REPO_ROOT = Path(__file__).resolve().parents[3]


class MetadataGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_canonical_standards_corpus(REPO_ROOT)

    def test_metadata_projection_preserves_groups_aliases_and_transitive_order(self) -> None:
        registry = metadata_dependency_registry(REPO_ROOT, self.corpus.modules)

        self.assertEqual(registry.resolve("workflows/planning.md"), "workflow.planning")
        self.assertIn(METADATA_REQUIRES, registry.groups)
        self.assertIn(METADATA_SPECIALIZES, registry.groups)
        closure = registry.traverse_group(
            "workflow.planning",
            METADATA_REQUIRES,
            Direction.OUTGOING,
            transitive=True,
        )
        self.assertIn("core", closure.nodes)

    def test_navigation_registry_combines_metadata_and_policy_impact_once(self) -> None:
        registry = standards_navigation_registry(REPO_ROOT, self.corpus)

        groups = {group.id for group in registry.groups_for("workflow.planning")}
        self.assertIn(METADATA_REQUIRES, groups)
        self.assertIn("policy-impact", groups)
        self.assertEqual(len(registry.edges), len(set(registry.edges)))
        self.assertIn("workflow.planning.plan-admission", registry.nodes)
        self.assertTrue(
            registry.outgoing(
                "workflow.planning.plan-admission",
                ("policy-impact",),
            )
        )
        self.assertEqual(
            registry.outgoing("workflow.planning", ("policy-impact",)),
            (),
        )


if __name__ == "__main__":
    unittest.main()
