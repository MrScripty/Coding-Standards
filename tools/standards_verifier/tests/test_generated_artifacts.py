from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.generated_artifacts import check_generated_artifacts


class GeneratedArtifactsTest(unittest.TestCase):
    @patch("standards_verifier.generated_artifacts.check_retirements")
    @patch("standards_verifier.generated_artifacts.check_graph")
    @patch("standards_verifier.generated_artifacts.check_inventory")
    def test_checks_inventory_graph_and_numeric_retirements(
        self, inventory, graph, retirements
    ) -> None:
        inventory.return_value = 0
        graph.return_value = 0
        retirements.return_value = 0
        root = Path("repo")

        self.assertEqual(check_generated_artifacts(root), 0)

        inventory.assert_called_once_with(root)
        graph.assert_called_once_with(root)
        retirements.assert_called_once_with(root)

    @patch("standards_verifier.generated_artifacts.check_retirements")
    @patch("standards_verifier.generated_artifacts.check_graph")
    @patch("standards_verifier.generated_artifacts.check_inventory")
    def test_fails_before_retirements_when_graph_is_stale(
        self, inventory, graph, retirements
    ) -> None:
        inventory.return_value = 0
        graph.return_value = 2

        self.assertEqual(check_generated_artifacts(Path("repo")), 2)

        retirements.assert_not_called()


if __name__ == "__main__":
    unittest.main()
