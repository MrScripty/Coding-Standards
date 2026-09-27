"""Independent semantic and boundary evidence for the native-only MCP catalog."""
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
            purpose: {t['name']: t for t in tool_catalog(cls.interface, purpose=purpose, advanced=True)}
            for purpose in ('authoring', 'application')
        }

    def test_valid_and_malformed_examples_agree_with_canonical_validator(self):
        for example in self.examples:
            if example['definition'] in ('InputContractResult', 'OutputContractResult'):
                self.assertEqual(example['value']['interface_version'],
                                 self.interface.interface.interface_schema_version)
        for operation in self.interface.interface.operations:
            for purpose in ('authoring', 'application'):
                if purpose == 'application' and 'application' not in operation.variants:
                    continue
                selected = (operation.select_variant('application') if purpose == 'application'
                            else operation.select_variant('agent') if 'agent' in operation.variants
                            else operation)
                definitions = {selected.input_definition, operation.input_definition} if purpose == 'authoring' else {selected.input_definition}
                fixtures = [e['value'] for e in self.examples if e['definition'] in definitions]
                self.assertTrue(fixtures, selected.id)
                root = self.schema['$defs'][selected.input_definition]
                canonical = Draft202012Validator({**root, '$defs': self.schema['$defs']})
                tool = self.catalogs[purpose][operation.id]
                validator = Draft202012Validator(tool['inputSchema'])
                Draft202012Validator.check_schema(tool['inputSchema'])
                Draft202012Validator.check_schema(tool['outputSchema'])
                for value in fixtures:
                    cases = [value, {**value, 'unexpected_input': True}]
                    cases.extend({k: v for k, v in value.items() if k != required}
                                 for required in root.get('required', []))
                    with self.subTest(operation=operation.id, purpose=purpose):
                        for case in cases:
                            self.assertEqual(validator.is_valid(case), canonical.is_valid(case))

    def test_recursive_expressions_keep_validation(self):
        propose = deepcopy(next(e['value'] for e in self.examples if e['definition'] == 'ProposeCall'))
        rule = deepcopy(next(e['value'] for e in self.examples if e['definition'] == 'PutRoutingRuleEdit'))
        for _ in range(12):
            rule['rule']['when'] = {'operator': 'not', 'expression': rule['rule']['when']}
        propose['change_set']['edits'] = [rule]
        validator = Draft202012Validator(self.catalogs['authoring']['propose']['inputSchema'])
        self.assertTrue(validator.is_valid(propose))
        invalid = deepcopy(propose)
        invalid['change_set']['edits'][0]['rule']['when']['expression'] = {'operator': 'invented'}
        self.assertFalse(validator.is_valid(invalid))

    def test_application_catalog_contains_no_authoring_contracts(self):
        for hidden in ('EvidenceUse', 'RequestEvidenceTable', 'AgentProposeCall', 'DecisionProvenance'):
            self.assertNotIn(hidden, json.dumps(self.catalogs['application']))

    def test_runtime_catalog_identity_tracks_output_delivery_without_store_access(self):
        from unittest.mock import patch
        from tools.standards_engine.standards_engine.tools import AgentToolFacade
        servers = [MCPServer(ROOT, purpose='authoring', output_schemas=delivery)
                   for delivery in ('eager', 'on-demand')]
        try:
            with patch.object(AgentToolFacade, 'open_repository', side_effect=AssertionError('store opened')):
                digests = []
                for server in servers:
                    initialize(server)
                    value = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {}}))['result']['structuredContent']
                    self.assertEqual(value['interface_version'], 44)
                    digests.append(value['catalog_digest'])
                self.assertNotEqual(*digests)
                other = servers[1].dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {'expected_catalog': digests[0]}}))['result']['structuredContent']
                self.assertEqual(other['action'], 'refresh-tools')
        finally:
            for server in servers:
                server.close()


class NativeOnlyBoundaryTest(unittest.TestCase):
    """Retired launch and composition arguments fail before repository work."""

    def test_removed_python_keyword_is_not_accepted(self):
        from unittest.mock import patch
        from tools.standards_engine.standards_engine.tools import AgentToolFacade
        for value in ('native', 'compatibility', None):
            with self.subTest(value=value), patch.object(
                AgentToolFacade, 'load_interface', side_effect=AssertionError('installation loaded')
            ), self.assertRaisesRegex(TypeError, 'schema_mode'):
                MCPServer(ROOT, purpose='authoring', schema_mode=value)
            with self.subTest(catalog=value), self.assertRaisesRegex(TypeError, 'schema_mode'):
                tool_catalog(None, purpose='authoring', schema_mode=value)

    def test_retired_cli_flags_reject_without_creating_paths(self):
        import os
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'untouched'
            commands = (
                ('tools.standards_engine.standards_engine.mcp', ['--repo-root', str(root), '--purpose', 'authoring']),
                ('tools.standards_engine.tests.catalog_inventory', ['--repo-root', str(root)]),
                ('tools.standards_engine.tests.codex_navigation_client', []),
                ('tools.standards_engine.tests.codex_discovery_client', ['--model', 'fixture', '--surface', 'fixture', '--evidence-dir', str(root)]),
            )
            for module, args in commands:
                for value in ('native', 'compatibility'):
                    for flags in (['--schema-mode', value], ['--schema-mode=' + value]):
                        with self.subTest(module=module, flags=flags):
                            process = subprocess.run([sys.executable, '-m', module, *args, *flags],
                                cwd=ROOT, env={**os.environ, 'PYTHONPATH': str(ROOT)},
                                input='', text=True, capture_output=True)
                            self.assertEqual(process.returncode, 2, process.stderr)
                            self.assertIn('unrecognized arguments: --schema-mode', process.stderr)
                            self.assertFalse(root.exists())

    def test_single_reference_projection_and_no_fallback_export(self):
        from tools.standards_contracts import standards_contracts
        from tools.standards_contracts.standards_contracts import schema_closure
        from tools.standards_engine.standards_engine import mcp_catalog
        from tools.standards_engine.standards_engine.context_projection import qualified_operations
        for name in ('SchemaMode', 'INPUT_CONTRACT_DESCRIPTIONS', 'input_schema', 'presented_input_schema'):
            self.assertFalse(hasattr(mcp_catalog, name), name)
        self.assertFalse(hasattr(standards_contracts, 'map_schema_children'))
        interface = _contracts(ROOT)
        projection = interface.project().agent_tools
        for purpose in ('application', 'authoring'):
            expected = {op['id']: op for op in qualified_operations(projection, purpose)}
            for delivery in ('eager', 'on-demand'):
                for tool in tool_catalog(interface, purpose=purpose, advanced=True, output_schemas=delivery):
                    self.assertEqual(tool['inputSchema'], schema_closure(
                        projection['$defs'][expected[tool['name']]['input_definition']], projection['$defs']))
                    self.assertNotIn('```json', tool['description'])
                    self.assertEqual('outputSchema' in tool, delivery == 'eager')
