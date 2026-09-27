"""Output delivery changes catalog transmission, not canonical result semantics."""
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tomllib
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts import compile_contracts, referenced_definitions
from tools.standards_engine.standards_engine import contract_discovery as discovery
from tools.standards_engine.standards_engine.context_projection import qualified_operations
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.standards_engine.runtime_identity import RuntimeIdentity
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.test_mcp import initialize, request

ROOT = Path(__file__).resolve().parents[3]


def independent_digest(schema):
    return 'sha256:' + hashlib.sha256(json.dumps(schema, sort_keys=True,
        ensure_ascii=True, separators=(',', ':')).encode()).hexdigest()


class OutputDeliveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = AgentToolFacade.load_interface(ROOT)
        cls.examples = json.loads((ROOT/'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples']

    def server(self, purpose='authoring', mode='native', delivery='on-demand', advanced=False):
        server = MCPServer(ROOT, purpose=purpose, schema_mode=mode,
                           output_schemas=delivery, advanced=advanced)
        self.addCleanup(server.close)
        initialize(server)
        return server

    def call(self, server, arguments, name='describe_output'):
        result = server.dispatch(request('tools/call', {'name': name, 'arguments': arguments}))['result']
        value = result['structuredContent']
        self.assertEqual(json.loads(result['content'][0]['text']), value)
        self.assertEqual(result['isError'], value['kind'].endswith('rejected-result'))
        return value

    def collect(self, server, args):
        first, docs = None, {}
        while True:
            page = self.call(server, args)
            self.assertEqual(page['kind'], 'output-contract-result', page)
            self.assertLessEqual(len(json.dumps(page).encode()), discovery.DISCOVERY_RESULT_BYTES)
            first = first or page
            for record in page['records']:
                self.assertNotIn(record['name'], docs)
                docs[record['name']] = json.loads(record['schema_json'])
            if 'next' not in page:
                break
            self.assertTrue(page['records'])
            self.assertEqual(page['next']['offset'], page['offset']+len(page['records']))
            self.assertEqual(page['next']['expected_catalog'], first['catalog_digest'])
            args = page['next']
        self.assertEqual(len(docs), first['total'])
        return first, docs

    def test_catalog_delivery_omits_only_output_advertisements_and_binds_them(self):
        for purpose, mode, advanced in itertools.product(('authoring', 'application'), ('native','compatibility'), (False, True)):
            eager = tool_catalog(self.interface, purpose=purpose, schema_mode=mode, advanced=advanced)
            lean = tool_catalog(self.interface, purpose=purpose, schema_mode=mode, advanced=advanced, output_schemas='on-demand')
            self.assertEqual(len(eager), len(lean))
            for before, after in zip(eager, lean):
                self.assertEqual(before['name'], after['name'])
                self.assertEqual(before['inputSchema'], after['inputSchema'])
                self.assertEqual(before['annotations'], after['annotations'])
                self.assertNotIn('outputSchema', after)
                self.assertEqual(after['_meta'][discovery.OUTPUT_SCHEMA_DIGEST_KEY], independent_digest(before['outputSchema']))
            self.assertLess(len(json.dumps(lean)), len(json.dumps(eager)))
        with self.assertRaises(ValueError):
            tool_catalog(self.interface, purpose='application', output_schemas='automatic')

    def test_every_result_algebra_reconstructs_in_both_purposes_and_deliveries(self):
        validated = set()
        for purpose, mode, delivery in itertools.product(('application','authoring'), ('native','compatibility'), ('eager','on-demand')):
            server = self.server(purpose, mode, delivery, True)
            for op in qualified_operations(self.interface.project().agent_tools, purpose):
                with self.subTest(purpose=purpose, mode=mode, delivery=delivery, operation=op['id']):
                    page, docs = self.collect(server, {'operation':op['id'], 'limit':16})
                    expected_root = {'type':'object', 'oneOf':[{'$ref':'#/$defs/'+n} for n in op['result_definitions']]}
                    self.assertEqual(json.loads(page['root_schema_json']), expected_root)
                    expected_defs = referenced_definitions(expected_root, self.interface.schema['$defs'])
                    self.assertEqual(docs, expected_defs)
                    schema = {**expected_root, '$defs':docs}
                    self.assertEqual(page['schema_digest'], independent_digest(schema))
                    if page['schema_digest'] in validated:
                        continue
                    validated.add(page['schema_digest'])
                    validator = Draft202012Validator(schema)
                    validator.check_schema(schema)
                    for sample in self.examples:
                        if sample['definition'] in op['result_definitions']:
                            validator.validate(sample['value'])
                    self.assertFalse(validator.is_valid({'kind':'not-an-admitted-result'}))

    def test_output_discovery_input_is_small_flat_and_read_only(self):
        server = self.server()
        tool = next(t for t in server.tools if t['name']=='describe_output')
        self.assertTrue(tool['annotations']['readOnlyHint'])
        self.assertLess(len(json.dumps(tool['inputSchema'])),1800)
        self.assertEqual(tool['inputSchema']['required'],['operation'])
        for field in tool['inputSchema']['properties'].values():
            self.assertIn(field.get('type'),('string','integer'))
        with patch.object(AgentToolFacade,'open_repository',side_effect=AssertionError('store opened')), \
             patch.object(Path,'read_bytes',side_effect=AssertionError('file read')):
            page = self.call(server, {'operation':'review'})
        self.assertEqual(page['kind'],'output-contract-result')

    def test_scopes_reject_hidden_operations_and_foreign_selections(self):
        server = self.server('application')
        for op in ('propose','review','apply_proposal'):
            self.assertEqual(self.call(server, {'operation':op})['code'], 'OUTPUT_DISCOVERY.OPERATION_UNAVAILABLE')
        first = self.call(server, {'operation':'read'})
        self.assertEqual(self.call(server, {'operation':'read', 'selector':'AgentProposeCall',
            'expected_catalog':first['catalog_digest']})['code'], 'OUTPUT_DISCOVERY.SELECTION_INVALID')
        author = self.server()
        self.assertEqual(self.call(author, {'operation':'apply_proposal'})['code'], 'OUTPUT_DISCOVERY.OPERATION_UNAVAILABLE')

    def test_stale_and_unbound_selections_and_numeric_boundaries(self):
        server = self.server()
        first = self.call(server, {'operation':'read'})
        for args, code in (
            ({'operation':'read','offset':1},'SELECTION_INVALID'),
            ({'operation':'read','selector':first['roots'][0]},'SELECTION_INVALID'),
            ({'operation':'read','expected_catalog':'sha256:'+'0'*64},'CATALOG_CHANGED'),
            ({'operation':'read','limit':1.5},'INVALID_ARGUMENTS'),
            ({'operation':'read','limit':True},'INVALID_ARGUMENTS'),
            ({'operation':'read','unexpected':'secret'},'INVALID_ARGUMENTS'),
            ({'operation':'read','offset':10000,'expected_catalog':first['catalog_digest']},'SELECTION_INVALID')):
            self.assertEqual(self.call(server,args)['code'], 'OUTPUT_DISCOVERY.'+code)
        self.assertEqual(self.call(server, {'operation':'read','limit':1.0})['records'],
                         self.call(server, {'operation':'read','limit':1})['records'])
        last = self.call(server, {'operation':'read','offset':first['total'],'expected_catalog':first['catalog_digest']})
        self.assertEqual(last['records'],[]); self.assertNotIn('next',last)
        other = self.server(delivery='eager')
        self.assertEqual(self.call(other, {'operation':'read','expected_catalog':first['catalog_digest']})['code'], 'OUTPUT_DISCOVERY.CATALOG_CHANGED')

    def test_whole_record_boundaries_and_selected_closure(self):
        server=self.server()
        page=self.call(server,{'operation':'read','limit':1})
        bound=len(json.dumps(page).encode())
        with patch.object(discovery,'DISCOVERY_RESULT_BYTES',bound):
            self.assertEqual(self.call(server,{'operation':'read','limit':1}),page)
        with patch.object(discovery,'DISCOVERY_RESULT_BYTES',bound-1):
            result=self.call(server,{'operation':'read','limit':1})
            self.assertEqual(result['code'],'OUTPUT_DISCOVERY.RESULT_LIMIT')
            self.assertNotIn('records',result)
        selected,docs=self.collect(server,{'operation':'read','selector':'Digest',
                                  'expected_catalog':page['catalog_digest']})
        self.assertEqual(set(docs),{'Digest'})
        self.assertEqual(selected['schema_digest'],page['schema_digest'])
        self.assertEqual(selected['roots'],page['roots'])

    def test_output_only_change_changes_omitted_schema_catalog_identity(self):
        schema=deepcopy(self.interface.schema)
        schema['$defs']['RuntimeInfoResult']['description']='Output-only fixture contract change.'
        changed=compile_contracts(schema,tomllib.loads((ROOT/'tools/standards_engine/contracts/a1-interface.toml').read_text()))
        original=tool_catalog(self.interface,purpose='authoring',schema_mode='native',output_schemas='on-demand')
        modified=tool_catalog(changed,purpose='authoring',schema_mode='native',output_schemas='on-demand')
        before={t['name']:t for t in original}; after={t['name']:t for t in modified}
        self.assertEqual(before['runtime_info']['inputSchema'],after['runtime_info']['inputSchema'])
        self.assertNotEqual(before['runtime_info']['_meta'],after['runtime_info']['_meta'])
        first=RuntimeIdentity(ROOT,'authoring',self.interface,original).metadata()['catalog_digest']
        second=RuntimeIdentity(ROOT,'authoring',changed,modified).metadata()['catalog_digest']
        self.assertNotEqual(first,second)
        service=discovery.ContractDiscovery(changed,purpose='authoring',operation_names=after,catalog_digest=second)
        self.assertEqual(service.invoke({'operation':'runtime_info','expected_catalog':first},direction='output')['code'], 'OUTPUT_DISCOVERY.CATALOG_CHANGED')

    def test_returned_documents_do_not_mutate_later_observations(self):
        server=self.server()
        args={'operation':'read','limit':2}
        first=self.call(server,args); expected=deepcopy(first)
        first['records'][0]['schema_json']='{}'; first['roots'].clear()
        self.assertEqual(self.call(server,args),expected)
        self.assertEqual(args,{'operation':'read','limit':2})
        server.close()
        result=server.dispatch(request('tools/call',{'name':'describe_output','arguments':args}))
        self.assertEqual(result['error']['message'],'The server is closed.')

    def test_shared_workflow_schemas_have_one_digest(self):
        server=self.server()
        digests={self.call(server,{'operation':op})['schema_digest'] for op in
                 ('propose','revise','resolve_workflow','resolve_many','review','apply','recover','resume')}
        self.assertEqual(len(digests),1)

    def test_input_and_output_discovery_have_distinct_scope_without_store_changes(self):
        server=self.server()
        output=self.call(server,{'operation':'review'})
        incoming=self.call(server,{'operation':'review'},'describe_input')
        self.assertEqual(incoming['root'],'AgentReviewCall')
        self.assertNotIn('schema_digest',incoming)
        result=self.call(server,{'operation':'review','selector':'AgentReviewCall',
            'expected_catalog':output['catalog_digest']})
        self.assertEqual(result['code'],'OUTPUT_DISCOVERY.SELECTION_INVALID')

    def test_stdio_omission_and_cold_output_continuation(self):
        def run(call):
            init=request('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'output-test','version':'1'}})
            messages=[init,{'jsonrpc':'2.0','method':'notifications/initialized'},request('tools/list',identifier=2),
                      request('tools/call',{'name':'describe_output','arguments':call},identifier=3)]
            process=subprocess.run([sys.executable,'-m','tools.standards_engine.standards_engine.mcp',
                '--repo-root',str(ROOT),'--purpose','authoring','--schema-mode','native','--output-schemas','on-demand'],
                input=''.join(json.dumps(x)+'\n' for x in messages),capture_output=True,text=True,cwd=ROOT,check=True)
            replies=[json.loads(x) for x in process.stdout.splitlines()]
            self.assertTrue(all('outputSchema' not in t for t in replies[1]['result']['tools']))
            return replies[2]['result']['structuredContent']
        first=run({'operation':'review','limit':1}); second=run(first['next'])
        self.assertEqual(first['schema_digest'],second['schema_digest'])
        self.assertEqual(first['catalog_digest'],second['catalog_digest'])
        self.assertEqual(second['offset'],1)
        self.assertNotEqual(first['records'][0]['name'],second['records'][0]['name'])


if __name__=='__main__':
    unittest.main()
