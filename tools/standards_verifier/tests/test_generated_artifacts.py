from __future__ import annotations

# ruff: noqa: E402 - repository package root is installed before imports.

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_ROOT))

from standards_verifier.generated_artifacts import check_generated_artifacts


class GeneratedArtifactsTest(unittest.TestCase):
    @patch("standards_verifier.generated_artifacts.check_suite_input_projection")
    @patch("standards_verifier.generated_artifacts.check_retirements")
    @patch("standards_verifier.generated_artifacts.check_graph")
    @patch("standards_verifier.generated_artifacts.check_inventory")
    def test_checks_inventory_graph_and_numeric_retirements(
        self, inventory, graph, retirements, suite_inputs
    ) -> None:
        suite_inputs.return_value = 0
        inventory.return_value = 0
        graph.return_value = 0
        retirements.return_value = 0
        root = Path("repo")

        self.assertEqual(check_generated_artifacts(root), 0)

        suite_inputs.assert_called_once_with(root)
        inventory.assert_called_once_with(root)
        graph.assert_called_once_with(root)
        retirements.assert_called_once_with(root)

    @patch("standards_verifier.generated_artifacts.check_suite_input_projection")
    @patch("standards_verifier.generated_artifacts.check_retirements")
    @patch("standards_verifier.generated_artifacts.check_graph")
    @patch("standards_verifier.generated_artifacts.check_inventory")
    def test_fails_before_retirements_when_graph_is_stale(
        self, inventory, graph, retirements, suite_inputs
    ) -> None:
        suite_inputs.return_value = 0
        inventory.return_value = 0
        graph.return_value = 2

        self.assertEqual(check_generated_artifacts(Path("repo")), 2)

        retirements.assert_not_called()

    @patch(
        "standards_verifier.generated_artifacts.check_suite_input_projection",
        return_value=2,
    )
    @patch("standards_verifier.generated_artifacts.check_inventory")
    def test_fails_before_other_artifacts_when_suite_inputs_are_stale(
        self, inventory, suite_inputs
    ) -> None:
        self.assertEqual(check_generated_artifacts(Path("repo")), 2)

        suite_inputs.assert_called_once_with(Path("repo"))
        inventory.assert_not_called()


if __name__ == "__main__":
    unittest.main()
