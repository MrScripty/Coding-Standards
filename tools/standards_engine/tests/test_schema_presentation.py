"""Independent Draft validation of both public MCP schema presentations."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.tests.test_mcp import initialize, request

ROOT = Path(__file__).resolve().parents[3]


class SchemaPresentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = _contracts(ROOT)
        cls.schema = cls.interface.schema
        cls.examples = json.loads((ROOT / 'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples']
        cls.catalogs = {
            (purpose, mode): {t['name']: t for t in tool_catalog(cls.interface, purpose=purpose, advanced=True, schema_mode=mode)}
            for purpose in ('authoring', 'application') for mode in ('compatibility', 'native')
        }

    def test_valid_and_malformed_examples_agree_with_canonical_validator(self):
        for operation in self.interface.interface.operations:
            for purpose in ('authoring', 'application'):
                if purpose == 'application' and 'application' not in operation.variants:
                    continue
                selected = (operation.select_variant('application') if purpose == 'application'
                            else operation.select_variant('agent') if 'agent' in operation.variants
                            else operation)
                definitions = {selected.input_definition, operation.input_definition} if purpose == 'authoring' else {selected.input_definition}
                fixtures = [e['value'] for e in self.examples if e['definition'] in definitions]
                for value in fixtures:
                    bad_extra = {**value, 'unexpected_input': True}
                    cases = [value, bad_extra]
                    root = self.schema['$defs'][selected.input_definition]
                    cases.extend({k: v for k, v in value.items() if k != required} for required in root.get('required', []))
                    canonical = Draft202012Validator({**root, '$defs': self.schema['$defs']})
                    for mode in ('compatibility', 'native'):
                        tool = self.catalogs[(purpose, mode)][operation.id]
                        validator = Draft202012Validator(tool['inputSchema'])
                        with self.subTest(operation=operation.id, purpose=purpose, mode=mode):
                            Draft202012Validator.check_schema(tool['inputSchema'])
                            Draft202012Validator.check_schema(tool['outputSchema'])
                            for case in cases:
                                self.assertEqual(validator.is_valid(case), canonical.is_valid(case))

    def test_recursive_expressions_keep_validation_in_native_mode(self):
        propose = deepcopy(next(e['value'] for e in self.examples if e['definition'] == 'ProposeCall'))
        rule = deepcopy(next(e['value'] for e in self.examples if e['definition'] == 'PutRoutingRuleEdit'))
        for _ in range(12):
            rule['rule']['when'] = {'operator': 'not', 'expression': rule['rule']['when']}
        propose['change_set']['edits'] = [rule]
        for mode in ('compatibility', 'native'):
            validator = Draft202012Validator(self.catalogs[('authoring', mode)]['propose']['inputSchema'])
            self.assertTrue(validator.is_valid(propose))
            invalid = deepcopy(propose)
            invalid['change_set']['edits'][0]['rule']['when']['expression'] = {'operator': 'invented'}
            self.assertFalse(validator.is_valid(invalid))

    def test_native_catalog_removes_only_presentation_overhead(self):
        for purpose in ('authoring', 'application'):
            compatible = self.catalogs[(purpose, 'compatibility')]
            native = self.catalogs[(purpose, 'native')]
            self.assertEqual(set(compatible), set(native))
            self.assertLessEqual(len(json.dumps(native)), len(json.dumps(compatible)))
            if purpose == 'authoring':
                self.assertLess(len(json.dumps(native)), len(json.dumps(compatible)))
            for name, item in native.items():
                self.assertNotIn('```json', item['description'])
                self.assertEqual(item['outputSchema'], compatible[name]['outputSchema'])
                self.assertEqual(item['annotations'], compatible[name]['annotations'])
            if purpose == 'application':
                for hidden in ('EvidenceUse', 'RequestEvidenceTable', 'AgentProposeCall', 'DecisionProvenance'):
                    self.assertNotIn(hidden, json.dumps(native))

    def test_runtime_catalog_identity_tracks_explicit_mode_without_store_access(self):
        servers = [MCPServer(ROOT, purpose='authoring', schema_mode=mode)
                   for mode in ('compatibility', 'native')]
        try:
            digests = []
            for server in servers:
                initialize(server)
                value = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {}}))['result']['structuredContent']
                self.assertEqual(value['interface_version'], 40)
                digests.append(value['catalog_digest'])
            self.assertNotEqual(*digests)
            native = servers[1].dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {'expected_catalog': digests[0]}}))['result']['structuredContent']
            self.assertEqual(native['action'], 'refresh-tools')
        finally:
            for server in servers:
                server.close()
        with self.assertRaises(ValueError):
            MCPServer(ROOT, purpose='authoring', schema_mode='guessed-client')
