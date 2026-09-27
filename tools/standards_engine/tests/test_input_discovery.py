"""Schema discovery is independent of renderer, purpose-private state and mutation."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts import (
    compile_contracts, referenced_definitions,
)
from tools.standards_engine.standards_engine import contract_discovery as discovery
from tools.standards_engine.standards_engine.context_projection import qualified_operations
from tools.standards_engine.standards_engine.contract_discovery import ContractDiscovery
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.test_mcp import initialize, request

ROOT = Path(__file__).resolve().parents[3]


class InputDiscoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = AgentToolFacade.load_interface(ROOT)
        cls.definitions = cls.interface.schema['$defs']
        cls.examples = json.loads((ROOT / 'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples']

    def server(self, purpose='authoring', mode='native', advanced=False):
        server = MCPServer(ROOT, purpose=purpose, schema_mode=mode, advanced=advanced)
        self.addCleanup(server.close)
        initialize(server)
        return server

    def call(self, server, arguments):
        result = server.dispatch(request('tools/call', {'name': 'describe_input', 'arguments': arguments}))['result']
        value = result['structuredContent']
        self.assertEqual(json.loads(result['content'][0]['text']), value)
        schema = next(t['outputSchema'] for t in server.tools if t['name'] == 'describe_input')
        Draft202012Validator(schema).validate(value)
        self.assertEqual(result['isError'], value['kind'] == 'input-contract-rejected-result')
        return value

    def collect(self, server, arguments):
        records = {}
        first = None
        while True:
            result = self.call(server, arguments)
            self.assertEqual(result['kind'], 'input-contract-result', result)
            first = first or result
            self.assertLessEqual(len(json.dumps(result).encode()), discovery.DISCOVERY_RESULT_BYTES)
            for record in result['records']:
                self.assertNotIn(record['name'], records)
                records[record['name']] = json.loads(record['schema_json'])
            if 'next' not in result:
                break
            self.assertTrue(result['records'])
            self.assertEqual(result['next']['offset'], result['offset'] + len(result['records']))
            self.assertEqual(result['next']['expected_catalog'], result['catalog_digest'])
            arguments = result['next']
        self.assertEqual(len(records), first['total'])
        return first, records

    def test_flat_discovery_schema_and_early_guidance_cover_every_published_tool(self):
        for purpose in ('application', 'authoring'):
            for mode in ('compatibility', 'native'):
                server = self.server(purpose, mode, True)
                tool = next(t for t in server.tools if t['name'] == 'describe_input')
                shape = tool['inputSchema']
                self.assertEqual(shape['required'], ['operation'])
                self.assertLess(len(json.dumps(shape).encode()), 1800)
                for field in shape['properties'].values():
                    self.assertIn(field.get('type'), ('string', 'integer'))
                    self.assertNotIn('oneOf', field)
                self.assertTrue(tool['annotations']['readOnlyHint'])
                for item in server.tools:
                    if item['name'] != 'describe_input':
                        self.assertIn(f'describe_input(operation="{item["name"]}")', item['description'][:250])

    def test_every_published_input_can_be_reconstructed_and_independently_validated(self):
        for purpose in ('application', 'authoring'):
            for mode in ('compatibility', 'native'):
                server = self.server(purpose, mode, True)
                operations = qualified_operations(self.interface.project().agent_tools, purpose)
                for operation in operations:
                    with self.subTest(purpose=purpose, mode=mode, operation=operation['id']):
                        result, records = self.collect(server, {'operation': operation['id'], 'limit': 16})
                        root = operation['input_definition']
                        expected = {root: self.definitions[root], **referenced_definitions(self.definitions[root], self.definitions)}
                        self.assertEqual(records, expected)
                        self.assertEqual(result['root'], root)
                        validator = Draft202012Validator({'$schema': result['dialect'], '$ref': f'#/$defs/{root}', '$defs': records})
                        validator.check_schema(validator.schema)
                        examples = [x['value'] for x in self.examples if x['definition'] == root]
                        self.assertTrue(examples, root)
                        for example in examples:
                            validator.validate(example)
                        # The rediscovered contract retains closed top-level fields.
                        self.assertFalse(validator.is_valid({'unknown-fixture-field': True}))

    def test_first_page_reveals_choices_and_selection_avoids_unrelated_edits(self):
        server = self.server()
        overview = self.call(server, {'operation': 'propose'})
        documents = {x['name']: json.loads(x['schema_json']) for x in overview['records']}
        self.assertIn('AgentStandardEdit', documents)
        self.assertEqual(documents['AgentStandardEdit'], self.definitions['AgentStandardEdit'])
        selected, records = self.collect(server, {'operation': 'propose',
            'selector': 'RevisePolicyUnitEdit', 'expected_catalog': overview['catalog_digest']})
        self.assertEqual(selected['selector'], 'RevisePolicyUnitEdit')
        self.assertNotIn('CreateStandardEdit', records)
        self.assertEqual(records['RevisePolicyUnitEdit'], self.definitions['RevisePolicyUnitEdit'])
        self.assertLess(len(records), overview['total'])

    def test_all_five_authoring_operations_expose_shared_evidence_and_nested_variants(self):
        server = self.server()
        for operation in ('propose', 'revise', 'resolve_workflow', 'resolve_many', 'review'):
            first, records = self.collect(server, {'operation': operation})
            self.assertIn('RequestEvidenceTable', records)
            self.assertEqual(records['EvidenceReference'], self.definitions['EvidenceReference'])
            self.assertEqual(records[first['root']]['properties']['evidence'], {'$ref': '#/$defs/RequestEvidenceTable'})
        _, records = self.collect(server, {'operation': 'resolve_many'})
        self.assertIn('AgentSubmission', records)
        for variant in self.definitions['AgentSubmission']['oneOf']:
            self.assertIn(variant['$ref'].rsplit('/', 1)[-1], records)

    def test_recursive_definition_closure_terminates_and_preserves_reference_semantics(self):
        server = self.server()
        overview = self.call(server, {'operation': 'propose'})
        result, records = self.collect(server, {'operation': 'propose', 'selector': 'ApplicabilityExpression',
                                                 'expected_catalog': overview['catalog_digest'], 'limit': 1})
        self.assertLess(len(records), 32)
        schema = {'$schema': result['dialect'], '$defs': records, '$ref': '#/$defs/ApplicabilityExpression'}
        validator = Draft202012Validator(schema)
        value = {'operator': 'always'}
        for _ in range(12):
            value = {'operator': 'not', 'expression': value}
        validator.validate(value)
        self.assertFalse(validator.is_valid({'operator': 'not', 'expression': {'operator': 'invented'}}))

    def test_selection_and_paging_require_matching_catalog(self):
        server = self.server()
        first = self.call(server, {'operation': 'propose'})
        for arguments, code in [
            ({'operation': 'propose', 'offset': 1}, 'SELECTION_INVALID'),
            ({'operation': 'propose', 'selector': first['root']}, 'SELECTION_INVALID'),
            ({'operation': 'propose', 'expected_catalog': 'sha256:' + '0'*64}, 'CATALOG_CHANGED'),
            ({'operation': 'propose', 'selector': 'ApplyProposalResult', 'expected_catalog': first['catalog_digest']}, 'SELECTION_INVALID'),
            ({'operation': 'propose', 'offset': first['total'] + 1, 'expected_catalog': first['catalog_digest']}, 'SELECTION_INVALID'),
        ]:
            result = self.call(server, arguments)
            self.assertEqual(result['code'], 'INPUT_DISCOVERY.' + code)
        different = self.server(advanced=True)
        result = self.call(different, first['next'])
        self.assertEqual(result['code'], 'INPUT_DISCOVERY.CATALOG_CHANGED')

    def test_purpose_and_actual_catalog_bound_visibility(self):
        for purpose, advanced, name in [('application', True, 'propose'), ('authoring', False, 'apply_proposal')]:
            server = self.server(purpose, advanced=advanced)
            hidden = self.call(server, {'operation': name})
            unknown = self.call(server, {'operation': 'not-a-tool'})
            self.assertEqual(hidden, unknown)
            self.assertNotIn(name, hidden['message'])
        server = self.server('application')
        first, records = self.collect(server, {'operation': 'read'})
        self.assertEqual(first['root'], 'ApplicationReadCall')
        self.assertNotIn('ReadCall', records)
        self.assertEqual(self.call(server, {'operation': 'read', 'selector': 'ReadCall',
            'expected_catalog': first['catalog_digest']})['code'], 'INPUT_DISCOVERY.SELECTION_INVALID')

    def test_invalid_inputs_have_bounded_typed_outcomes(self):
        server = self.server()
        for arguments in ({}, {'operation': 4}, {'operation': 'read', 'extra': True},
                          {'operation': 'read', 'limit': 0}, {'operation': 'read', 'limit': 17},
                          {'operation': 'read', 'offset': -1}, {'operation': 'read', 'offset': 0.5},
                          {'operation': 'read', 'limit': True}, {'operation': 'read', 'expected_catalog': 'bad'},
                          {'operation': 'read', 'selector': '../../secret'}, {'operation': 'read', 'selector': ''}):
            result = self.call(server, arguments)
            self.assertEqual(result['code'], 'INPUT_DISCOVERY.INVALID_ARGUMENTS', arguments)
            self.assertLess(len(json.dumps(result)), 1000)

    def test_whole_number_json_encodings_and_terminal_offset(self):
        server = self.server()
        first = self.call(server, {'operation': 'read', 'limit': 1.0})
        self.assertEqual(len(first['records']), 1)
        nxt = dict(first['next'], offset=1.0)
        self.assertEqual(self.call(server, nxt)['offset'], 1)
        terminal = dict(nxt, offset=float(first['total']))
        result = self.call(server, terminal)
        self.assertEqual(result['records'], [])
        self.assertNotIn('next', result)

    def test_exact_byte_bound_and_byte_pressure_preserve_whole_records(self):
        server = self.server()
        first = self.call(server, {'operation': 'propose', 'limit': 1})
        bound = len(json.dumps(first).encode())
        with patch.object(discovery, 'DISCOVERY_RESULT_BYTES', bound):
            result = self.call(server, {'operation': 'propose', 'limit': 1})
            self.assertEqual(result, first)
        with patch.object(discovery, 'DISCOVERY_RESULT_BYTES', bound - 1):
            self.assertEqual(self.call(server, {'operation': 'propose', 'limit': 1})['code'], 'INPUT_DISCOVERY.RESULT_LIMIT')
        # Include an explicit continuation of the same length as the 1-record form.
        with patch.object(discovery, 'DISCOVERY_RESULT_BYTES', bound):
            result = self.call(server, {'operation': 'propose', 'limit': 8})
            self.assertEqual(result['records'], first['records'])
            self.assertEqual(result['next']['offset'], 1)
            self.assertLessEqual(len(json.dumps(result).encode()), bound)

    def test_literal_reference_data_is_returned_unchanged_and_not_discoverable_as_a_reference(self):
        import tomllib
        schema = self.interface.schema
        definition = schema['$defs']['RuntimeInfoCall']
        definition['default'] = {'$ref': '#/$defs/NotARealDefinition', 'const': {'$ref': 'https://invalid.example/'}}
        definition['properties']['$ref'] = {'type': 'string', 'enum': ['#/$defs/AlsoLiteral']}
        configuration = tomllib.loads((ROOT/'tools/standards_engine/contracts/a1-interface.toml').read_text())
        interface = compile_contracts(schema, configuration)
        service = ContractDiscovery(interface, purpose='application',
            operation_names=['runtime_info'], catalog_digest='sha256:'+'1'*64)
        result = service.invoke({'operation': 'runtime_info'})
        found = json.loads(result['records'][0]['schema_json'])
        self.assertEqual(found, definition)
        self.assertEqual(result['total'], 2)

    def test_discovery_has_no_store_filesystem_or_git_access_and_keeps_owned_values_private(self):
        server = self.server()
        with patch.object(AgentToolFacade, 'open_repository', side_effect=AssertionError('store access')), \
             patch.object(Path, 'read_text', side_effect=AssertionError('filesystem access')), \
             patch('subprocess.run', side_effect=AssertionError('process access')):
            first = self.call(server, {'operation': 'propose'})
            copy = deepcopy(first)
            first['records'][0]['schema_json'] = 'mutated caller data'
            self.assertEqual(self.call(server, {'operation': 'propose'}), copy)
        server.close()
        self.assertIn('error', server.dispatch(request('tools/call', {'name': 'describe_input', 'arguments': {'operation': 'propose'}})))

    def test_semantically_identical_key_order_has_identical_pages(self):
        import tomllib
        from tools.standards_engine.standards_engine.runtime_identity import RuntimeIdentity

        def reordered(value):
            if isinstance(value, dict):
                return {key: reordered(child) for key, child in reversed(list(value.items()))}
            if isinstance(value, list):
                return [reordered(child) for child in value]
            return value

        configuration = tomllib.loads((ROOT/'tools/standards_engine/contracts/a1-interface.toml').read_text())
        alternative = compile_contracts(reordered(self.interface.schema), configuration)
        catalogs = [tool_catalog(interface, purpose='authoring', schema_mode='native')
                    for interface in (self.interface, alternative)]
        identities = [RuntimeIdentity(ROOT, 'authoring', interface, catalog).metadata()['catalog_digest']
                      for interface, catalog in zip((self.interface, alternative), catalogs)]
        self.assertEqual(identities[0], identities[1])
        services = [ContractDiscovery(interface, purpose='authoring',
                    operation_names=[tool['name'] for tool in catalog], catalog_digest=digest)
                    for interface, catalog, digest in zip((self.interface, alternative), catalogs, identities)]
        arguments = {'operation': 'propose', 'limit': 3}
        while True:
            pages = [service.invoke(arguments) for service in services]
            self.assertEqual(pages[0], pages[1])
            if 'next' not in pages[0]:
                break
            arguments = pages[0]['next']

    def test_cold_stdio_and_cli_work_without_git_or_standards_store(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in ('tools/standards_engine/contracts/a1-interface.toml',
                             'tools/standards_engine/contracts/a1-contract.schema.json',
                             'tools/standards_engine/contracts/generated/agent-tools.json'):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, path)
            environment = {**os.environ, 'PYTHONPATH': str(ROOT)}
            def cold(arguments):
                messages = [request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'discovery-fixture', 'version': '1'}}),
                            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                            request('tools/call', {'name': 'describe_input', 'arguments': arguments}, identifier=2)]
                process = subprocess.run([sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp', '--repo-root', str(root), '--purpose', 'authoring', '--advanced'],
                    input=''.join(json.dumps(m)+'\n' for m in messages), capture_output=True, text=True, env=environment, timeout=60)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stderr, '')
                result = json.loads(process.stdout.splitlines()[-1])['result']
                self.assertFalse(result['isError'], result)
                return result
            first = cold({'operation': 'propose', 'limit': 1})
            second = cold(first['structuredContent']['next'])
            self.assertNotEqual(first['_meta']['standards-engine/runtime']['instance_id'], second['_meta']['standards-engine/runtime']['instance_id'])
            self.assertEqual(second['structuredContent']['offset'], 1)
            process = subprocess.run([sys.executable, '-P', str(ROOT / '.agents/skills/standards-engine/scripts/invoke.py'), '--repo-root', str(root), '--purpose', 'authoring', 'describe_input'],
                input=json.dumps({'operation': 'propose', 'limit': 1}), capture_output=True, text=True, env=environment, timeout=60)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout), first['structuredContent'])
            # The reference CLI lists/invokes the full purpose-qualified surface;
            # discovery must include its native operations rather than a hidden
            # focused-MCP subset. This remains a store-free observation.
            native = subprocess.run(process.args,
                input=json.dumps({'operation': 'apply_proposal'}), capture_output=True,
                text=True, env=environment, timeout=60)
            self.assertEqual(native.returncode, 0, native.stderr)
            self.assertEqual(json.loads(native.stdout)['root'], 'ApplyProposalCall')
            self.assertFalse((root / '.git').exists())
            self.assertFalse((root / '.standards-engine').exists())
