from __future__ import annotations

import unittest
from tools.standards_contracts.standards_contracts import ContractError, compile_contracts
from support import canonical_inputs


class ReviewContractTests(unittest.TestCase):
    def test_array_submissions_have_exact_capability_coverage(self):
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)
        batch = next(op for op in compiled.interface.operations if op.id == 'resolve_many')
        self.assertEqual(set(batch.capability_by_submission), {
            'provide-fact', 'consumer-disposition', 'impact-disposition', 'coverage-attestation'})
        raw = next(op for op in interface['operations'] if op['id'] == 'resolve_many')
        del raw['capability_by_submission']['coverage-attestation']
        with self.assertRaises(ContractError):
            compile_contracts(schema, interface)

    def test_numeric_maximum_is_retained_and_executed(self):
        schema, interface = canonical_inputs()
        compiled = compile_contracts(schema, interface)
        page = {'analysis': {'kind': 'analysis-handle', 'id': 'analysis:sha256:'+'a'*64, 'schema_version': 7},
                'section': 'obligations', 'limit': 16}
        compiled.validate('WorkflowDetailsCall', page)
        page['limit'] = 17
        with self.assertRaises(ContractError):
            compiled.validate('WorkflowDetailsCall', page)
        self.assertEqual(compiled.project().agent_tools['$defs']['WorkflowDetailsCall']['properties']['limit']['maximum'], 16)
