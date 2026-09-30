"""Snapshot-bound focused assertions, qualification and real cold stdio responses."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from tools.standards_applicability.standards_applicability import ApplicabilityError, FactSchema
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine, _generated_contract as c
from tools.standards_engine.standards_engine import routing_inputs
from tools.standards_engine.standards_engine.logical_authoring import _toml_inline
from tools.standards_engine.tests import test_purpose_projection as fixture
from tools.standards_engine.tests.test_routing_fact_inputs import SPECS
from tools.standards_metadata.standards_metadata import APPLICATION_CONTENT
from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotPath, SnapshotId

ROOT = Path(__file__).resolve().parents[3]
CONFIG = 'evaluation/standards-effectiveness/router-projection.toml'


class RoutingFactTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeProjectionTest.setUpClass()
        cls.temp = tempfile.TemporaryDirectory(prefix='focused-fact-transport-')
        cls.root = Path(cls.temp.name)
        for name in ('a1-contract.schema.json', 'a1-interface.toml', 'generated/agent-tools.json', 'examples/a1-examples.json'):
            relative = 'tools/standards_engine/contracts/' + name
            target = cls.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        cls.interface = AgentToolFacade.load_interface(cls.root)
        cls.engines = {p: StandardsEngine.open_repository(cls.root, purpose=p) for p in ('authoring','application')}
        cls.facades = {p: AgentToolFacade(e, cls.interface) for p,e in cls.engines.items()}
        cls.snapshots = {}
        cls.compiled = {}
        for kind in ('boolean', 'enum-set'):
            files = dict(fixture.PurposeProjectionTest.files)
            raw = tomllib.loads(files[CONFIG].decode())
            template = raw['facts'][0]
            for spec in SPECS:
                raw['facts'].append({**template, 'values':[], 'aliases':[], 'semantic_revision':1, **spec})
            raw['facts'].append({**template,'id':'routing.probe','type':kind,'values':['x'] if kind=='enum-set' else [],
                                 'aliases':['probe'],'semantic_revision':1})
            files[CONFIG] = ('\n'.join(f'{k} = {_toml_inline(v)}' for k,v in raw.items()) + '\n').encode()
            compiled = fixture.compile_files(files)
            approved = tomllib.loads(files[APPLICATION_CONTENT].decode())['entries']
            for row in approved:
                row['binding'] = compiled.materials[row['target']].binding
            files[APPLICATION_CONTENT] = ('schema_version = 1\nentries = ' + _toml_inline(approved) + '\n').encode()
            files = dict(fixture.refresh(files).files)
            cls.compiled[kind] = fixture.compile_files(files)
            cls.snapshots[kind] = cls.capture(files, kind)
            if kind == 'boolean':
                private = dict(files)
                private[APPLICATION_CONTENT] = b'schema_version = 1\nentries = []\n'
                cls.snapshots['unqualified'] = cls.capture(dict(fixture.refresh(private).files), 'unqualified')

    @classmethod
    def capture(cls, files, label):
        store = cls.engines['authoring']._snapshots
        value = store.create_snapshot(CapturedContent(label, tuple(
            SnapshotFile(SnapshotPath.parse(path), content) for path,content in files.items())))
        return cls.engines['authoring']._snapshot_handle(value.snapshot)

    @classmethod
    def tearDownClass(cls):
        for engine in cls.engines.values():
            engine.close()
        cls.temp.cleanup()
        fixture.PurposeProjectionTest.tearDownClass()

    def route(self, purpose, facts, *, snapshot='boolean', **rest):
        return self.facades[purpose].route({'snapshot':self.snapshots[snapshot], 'facts':facts, **rest})

    def cold(self, purpose, operation, args, *, error=False):
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{
            'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'fact-input-test','version':'1'}}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':operation,'arguments':args}}]
        proc=subprocess.run([sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp',
            '--repo-root',str(self.root),'--purpose',purpose,'--output-schemas','on-demand'],
            cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT)},input=''.join(json.dumps(m)+'\n' for m in messages),
            capture_output=True,text=True,check=True)
        self.assertEqual(proc.stderr,'')
        rows={m['id']:m for m in map(json.loads,proc.stdout.splitlines())}
        self.assertNotIn('error',rows[2],rows[2])
        response=rows[2]['result']
        self.assertEqual(response['isError'],error,response)
        value=response['structuredContent']
        self.assertEqual(value,json.loads(response['content'][0]['text']))
        return value

    def test_type_resolution_uses_the_selected_durable_snapshot_not_ambient_files(self):
        # A deliberately unrelated live projection cannot determine either result.
        path=self.root/CONFIG
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('unrelated live bytes')
        for purpose in self.facades:
            valid=self.route(purpose,{'probe':True})
            self.assertNotIn('code',valid)
            invalid=self.route(purpose,{'probe':True},snapshot='enum-set')
            self.assertEqual(invalid['input_feedback']['issues'][0]['message'], 'set fact value must contain unique strings')
            self.assertEqual(invalid['outcome'],'invalid')
            self.assertNotIn('code',self.route(purpose,{'probe':['x']},snapshot='enum-set'))
            invalid=self.route(purpose,{'probe':['x']})
            self.assertEqual(invalid['input_feedback']['issues'][0]['message'],'boolean fact value is invalid')

    def test_qualification_precedes_vocabulary_interpretation(self):
        with patch.object(routing_inputs,'bind_facts',side_effect=AssertionError('private vocabulary')):
            result=self.route('application',{'PRIVATE_FIELD':'PRIVATE_VALUE'},snapshot='unqualified')
        self.assertEqual(result['code'],'APPLICATION.CONTENT_UNAVAILABLE')
        self.assertNotIn('input_feedback',result)
        self.assertNotIn('PRIVATE',json.dumps(result))

    def test_single_bind_and_verified_load_per_focused_content_call(self):
        for purpose,engine in self.engines.items():
            original=FactSchema.bind
            with patch.object(FactSchema,'bind',autospec=True,side_effect=original) as bind, \
                 patch.object(engine,'_compiled_snapshot',wraps=engine._compiled_snapshot) as compiled, \
                 patch.object(engine._snapshots,'load_content',wraps=engine._snapshots.load_content) as load, \
                 patch.object(engine,'_capture_snapshot',side_effect=AssertionError('ambient capture')):
                value=self.route(purpose,{'tags':['y','x']},content={'limit':1})
            self.assertEqual(bind.call_count,1)
            self.assertEqual(compiled.call_count,1)
            self.assertEqual(load.call_count,1)
            self.assertIn('content',value)

    def test_normalized_continuations_and_explanations_roundtrip_in_cold_processes(self):
        supplied={'on':False,'tags':['y','x'],'text':None,'names':{'state':'unknown'},
                  'artifact':{'state':'known-absent'}}
        normalized={'enabled':False,'tags':['x','y'],'text':None,'names':{'state':'unknown'},
                    'artifact':{'state':'known-absent'}}
        for purpose in self.facades:
            for detail in ('compact','full'):
                first=self.route(purpose,supplied,detail=detail,content={'limit':1})
                args=first['content']['next']
                self.interface.validate('RouteCall',args)
                self.assertEqual(args['facts'],normalized)
                self.assertEqual(args['snapshot'],self.snapshots['boolean'])
                self.assertEqual(args['detail'],detail)
                actual=self.cold(purpose,'route',args)
                expected=self.facades[purpose].route(args)
                self.assertEqual(actual,expected)
                self.assertEqual(actual['reading_plan'],first['reading_plan'])
                self.assertEqual(actual['unresolved_questions'],first['unresolved_questions'])
                if purpose=='authoring':
                    self.assertEqual(first['facts'],normalized)
                    if detail=='compact':
                        self.assertEqual(first['explanation']['facts'],normalized)
                        self.assertEqual(self.cold(purpose,'route',first['explanation']),
                                         self.facades[purpose].route(first['explanation']))

    def test_canonical_queries_remain_typed_and_equal_in_meaning(self):
        canonical={'enabled':{'type':'boolean','state':'known','value':False},
                   'tags':{'type':'enum-set','state':'known','value':['x']}}
        for purpose,facade in self.facades.items():
            native=facade.query({'snapshot':self.snapshots['boolean'], 'request':{'kind':'route','facts':canonical}})
            focused=self.route(purpose,{'enabled':False,'tags':['x']})
            self.assertEqual(focused['reading_plan'],[e for e in native['reading_plan'] if e['state']=='selected'])
            if purpose=='application':
                self.assertEqual(native,focused)
            else:
                self.assertEqual([q['id'] for q in focused['unresolved_questions']],
                                 [q['id'] for q in native['unresolved_questions']])
            rejected=self.route(purpose,canonical)
            self.assertEqual(rejected['outcome'],'invalid')
            self.assertNotIn('reading_plan',rejected)

    def test_static_rejections_precede_capture_and_domain_actions(self):
        for purpose,facade in self.facades.items():
            engine=self.engines[purpose]
            for invalid in ({'facts':{'tags':{'type':'enum-set','state':'known','value':[]}}},
                            {'facts':{'enabled':1}},{'facts':{'text':{'state':'unknown','value':None}}}):
                with patch.object(engine,'_capture_snapshot',side_effect=AssertionError('capture')), \
                     patch.object(engine,'propose',side_effect=AssertionError('proposal')):
                    value=facade.route(invalid)
                self.assertEqual(value['outcome'],'invalid')
                self.assertEqual(value['input_feedback']['describe_input'],{'operation':'route'})

    def test_cold_dynamic_failures_are_typed_and_do_not_expose_unknown_keys(self):
        for purpose in self.facades:
            for values in ({'tags':'SECRET_VALUE'},{'SECRET_KEY':True},{'enabled':None}):
                response=self.cold(purpose,'route',{'snapshot':self.snapshots['boolean'],'facts':values},error=True)
                self.assertEqual(response['outcome'],'invalid')
                self.assertEqual(response['code'],'ROUTE.INPUT_INVALID' if purpose=='authoring' else 'APPLICATION.INPUT_INVALID')
                self.assertNotIn('SECRET',json.dumps(response))
                self.assertNotIn('reading_plan',response)
                self.assertNotIn('context',response)

    def test_input_discovery_and_output_schema_contain_only_the_new_focused_shape(self):
        for purpose,facade in self.facades.items():
            args={'operation':'route','limit':16};records={}
            while True:
                page=facade.describe_input(args)
                self.assertEqual(page['kind'],'input-contract-result')
                records.update({r['name']:json.loads(r['schema_json']) for r in page['records']})
                if 'next' not in page:break
                args=page['next']
            self.assertIn('RoutingFactAssertions',records)
            self.assertIn('RoutingFactAssertion',records)
            self.assertNotIn('FactValue',records)
            self.assertNotIn('FactSet',records)
            self.assertEqual(page['interface_version'],46)

    def test_schema_digest_guard_and_final_lifecycle_checks_still_apply(self):
        author=self.engines['authoring']
        bound=routing_inputs.bind_facts(self.compiled['boolean'].router.fact_schema,{})
        with self.assertRaises(ApplicabilityError) as caught:
            author._bound_routing_selection(self.compiled['enum-set'],bound)
        self.assertEqual(caught.exception.failure.field,'schema_digest')
        # Existing routed-page logic must discard a page if its lifetime ends
        # after item production, even though type binding and selection succeeded.
        from tools.standards_engine.standards_engine import agent_navigation
        original=agent_navigation.read_selected_item
        sid=SnapshotId(self.snapshots['boolean']['id'])
        def expire(*args,**kwargs):
            value=original(*args,**kwargs)
            author._snapshots.delete_snapshot(sid)
            return value
        try:
            with patch.object(agent_navigation,'read_selected_item',side_effect=expire):
                rejected=self.route('authoring',{},content={'limit':1})
            self.assertIn('rejected',rejected['kind'])
            self.assertNotIn('content',rejected)
        finally:
            author._snapshots.undelete_snapshot(sid)

    def test_unicode_collision_is_invalid_feedback_through_actual_stdio(self):
        for purpose in self.facades:
            value = self.cold(purpose, 'route', {'snapshot': self.snapshots['boolean'],
                'facts': {'names': ['e\u0301', 'é']}}, error=True)
            self.assertEqual(value['outcome'], 'invalid')
            self.assertEqual(value['input_feedback']['issues'][0]['instance_pointer'], '/facts/names')
            self.assertIn('Unicode normalization', value['input_feedback']['issues'][0]['message'])
            repaired = self.route(purpose, {'names': ['e\u0301']}, content={'limit':1})
            self.assertEqual(repaired['content']['next']['facts'], {'names':['é']})
