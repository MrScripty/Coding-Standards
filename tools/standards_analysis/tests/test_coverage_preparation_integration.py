"""Complete-checkout coverage preparation through the existing real fixture."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import coverage
from tools.standards_analysis.standards_analysis.errors import AnalysisError
from tools.standards_analysis.tests import test_coverage as fixtures
from tools.standards_metadata.standards_metadata.suite_inputs import SuiteInputManifest


class CoveragePreparationIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CoverageTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    def test_real_horizon_views_and_requirement_identity_reuse_preparation(self):
        fixture = self.fixture
        compiled = fixture.compiled(relationship=True)
        original = SuiteInputManifest._derive_dependency
        calls = []
        def observed(manifest, suite_id, definitions):
            calls.append(suite_id)
            return original(manifest, suite_id, definitions)
        with patch.object(SuiteInputManifest, "_derive_dependency", observed):
            horizon = coverage.load_coverage_horizon(fixture.root, fixture.corpus, compiled, "horizon.toml")
            result = coverage.compile_coverage_definitions(fixture.corpus, compiled, horizon)
        self.assertEqual(calls, [suite.id for suite in horizon.suite_inputs.suites])
        cold = replace(horizon, suite_inputs=replace(horizon.suite_inputs))
        reference = coverage.compile_coverage_definitions(fixture.corpus, compiled, cold)
        self.assertEqual(result.views, reference.views)
        self.assertEqual(result.requirements, reference.requirements)
        for subject, view in result.views.items():
            self.assertEqual(coverage.coverage_requirement_id(result.requirements[subject], view),
                             coverage.coverage_requirement_id(reference.requirements[subject], reference.views[subject]))

    def test_persisted_coverage_claim_tracks_relevant_inputs_not_retained_preparation(self):
        fixture = self.fixture
        fixture.write_attestations(pinned=True)
        before = fixture.load_decisions()
        self.assertIn("workflow.policy.rule", before.attestations)
        fixture.write("inputs/unrelated.md", "# Unrelated changed input\n")
        fixture.write_suite_projection()
        self.assertEqual(fixture.load_decisions().attestations, before.attestations)
        fixture.write("inputs/consumer.md", "# Relevant changed input\n")
        with self.assertRaises(AnalysisError) as error:
            fixture.definitions()
        self.assertEqual(error.exception.failure.code, "SUITE_INPUT.STALE_FILE")
        fixture.write_suite_projection()
        self.assertNotIn("workflow.policy.rule", fixture.load_decisions().attestations)


if __name__ == "__main__":
    unittest.main()
