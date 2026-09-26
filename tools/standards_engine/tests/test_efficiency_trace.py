"""The supported CLI carries optimized requests across real process replacement."""
from __future__ import annotations

import unittest

from tools.standards_engine.tests.agent_efficiency_trace import measure


class EfficiencyTraceTest(unittest.TestCase):
    def test_cold_stdio_preserves_authority_and_reduces_targeted_interaction_costs(self):
        result = measure()
        self.assertEqual(result['model_turns'], 0)
        self.assertEqual(len(result['routing']), 4)
        for route in result['routing']:
            self.assertTrue(route['exact_content_equal'])
            self.assertEqual(route['separate']['call_count'], 2)
            self.assertEqual(route['composed']['call_count'], 1)
        for evidence in result['evidence']:
            self.assertTrue(evidence['exact_analysis_and_readiness_equal'])
            self.assertTrue(evidence['previous_request_alias_rejected'])
            self.assertTrue(evidence['cold_readback'])
            self.assertLess(evidence['shared']['argument_bytes'], evidence['inline']['argument_bytes'])
            self.assertEqual(evidence['shared']['result_bytes'], evidence['inline']['result_bytes'])
            self.assertFalse(evidence['published'])
