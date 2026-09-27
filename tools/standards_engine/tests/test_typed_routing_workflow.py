"""Real unpublished routing workflows use typed edits across replacement processes."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_agent_workflow import decisions, evidence
from tools.standards_engine.tests.test_mcp import request
from tools.standards_engine.tests.test_request_evidence import shared

ROOT = Path(__file__).resolve().parents[3]


class TypedRoutingWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='typed-routing-workflow-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)/'repository'
        _clone_tracked_worktree(cls.root)
        cls.main = subprocess.check_output(['git','-C',str(cls.root),'rev-parse','main'])
        cls.router = tomllib.loads((cls.root/'evaluation/standards-effectiveness/router-projection.toml').read_text())

    def call(self, operation, arguments, delivery='on-demand', *, error=False):
        messages = [request('initialize', {'protocolVersion':'2025-11-25','capabilities':{},
                    'clientInfo':{'name':'typed-routing-test','version':'1'}}),
                    {'jsonrpc':'2.0','method':'notifications/initialized'},
                    request('tools/call', {'name':operation,'arguments':arguments}, 2)]
        run = subprocess.run([sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp',
              '--repo-root',str(self.root),'--purpose','authoring','--output-schemas',delivery],
              input=''.join(json.dumps(v)+'\n' for v in messages),text=True,capture_output=True,check=True,
              cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT)})
        self.assertEqual(run.stderr, '')
        reply = next(json.loads(line) for line in run.stdout.splitlines() if json.loads(line).get('id')==2)
        self.assertNotIn('error', reply, reply)
        result = reply['result']
        self.assertEqual(result['isError'], error, result)
        self.assertEqual(json.loads(result['content'][0]['text']), result['structuredContent'])
        return result['structuredContent']

    def change(self, edits):
        return {'purpose':{'summary':'Typed routing integration fixture',
            'rationale':'Verify exact unpublished authoring and old/new process readback.',
            'evidence':[evidence(self.root)]}, 'edits':edits}

    def settle(self, result, delivery):
        # Each bounded step consumes the actual work returned by the Engine. This
        # is test fixture authorization only, not production approval evidence.
        for _ in range(40):
            if result['status']=='complete':
                return result
            self.assertEqual(result['status'], 'needs-action', result)
            full = self.call('workflow_status', {'context':result['context'],'detail':'full'}, delivery)
            outcome = full['outcome']
            self.assertFalse(outcome.get('fact_requirements'), outcome)
            choices = [v for v in outcome['next_operations'] if v['operation']=='resolve']
            self.assertTrue(choices, outcome)
            selected = next((v for v in choices if v['request_kind']=='consumer-disposition'),choices[0])
            kind = selected['request_kind']
            if kind=='coverage-attestation':
                submission = {'kind':kind,'claim':{'requirement':selected['work'],'conclusion':'complete',
                    'evidence':[evidence(self.root)],'explicit_exclusions':[],
                    'rationale':'The synthetic fixture explicitly reviews this routing scope.',
                    'auditor_provenance':'Test-only routing qualification, not a production standards audit.'}}
            else:
                self.assertIn(kind, ('consumer-disposition','impact-disposition'))
                obligation = next(v for v in outcome['obligations'] if v['handle']==selected['work'])
                submission = {'kind':kind,'obligation':selected['work'],
                    'result':'reviewed-no-change' if kind=='consumer-disposition' else 'confirmed',
                    'fingerprint':obligation['fingerprint'],'evidence':[evidence(self.root)],
                    'rationale':'Fixture owner confirms only this synthetic routing change.'}
            result = self.call('resolve_workflow', shared({'context':result['context'],'submission':submission}), delivery)
        self.fail('No terminal outcome in the bounded synthetic work selection.')

    def test_all_four_edits_replay_through_readiness_with_shared_evidence(self):
        for delivery in ('eager','on-demand'):
            with self.subTest(delivery=delivery):
                fact = {'id':'routing.typed-'+delivery,'semantic_revision':1,'type':'enum-set',
                        'nullable':False,'values':['a'],'aliases':[],'meaning':'Synthetic selection.',
                        'prompt':'Use this synthetic selection?'}
                rule = {**self.router['rules'][0], 'condition':'The synthetic typed condition applies.',
                        'when':{'operator':'contains','fact':fact['id'],'value':'a'}}
                proposed = self.call('propose', shared({'change_set':self.change([
                    {'kind':'put-routing-fact','fact':fact,'rationale':'Declare a synthetic fact.'},
                    {'kind':'put-routing-rule','rule':rule,'rationale':'Use the same-set fact.'}])}),delivery)
                revision = proposed['revision']
                preview = self.call('query_proposal', {'revision':revision,'request':{'kind':'read','target':'router'}},delivery)
                self.assertIn(rule['condition'],preview['content'])
                revised = self.call('revise', shared({'context':proposed['context'],'change_set':self.change([
                    {'kind':'remove-routing-fact','fact':fact['id'],'rationale':'Remove the unused fact.'},
                    {'kind':'remove-routing-rule','rule':rule['id'],'rationale':'Remove its last reference.'}])}),delivery)
                complete = self.settle(revised, delivery)
                review = shared({'context':complete['context'],'decisions':decisions(self.root)})
                ready = self.call('review',review,delivery)
                self.assertEqual(ready['status'],'ready',ready)
                self.assertEqual(self.call('review',review,delivery),ready)
                self.assertEqual(self.call('review',{'context':complete['context'],'decisions':decisions(self.root)},delivery),ready)
                read = self.call('query_proposal',{'revision':ready['revision'],'request':{'kind':'read','target':'router'}},delivery)
                self.assertNotIn(rule['condition'],read['content'])
                self.assertNotEqual(read['content'],preview['content'])
                self.assertEqual(self.call('query_proposal',{'revision':revision,'request':{'kind':'read','target':'router'}},delivery),preview)
                self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'rev-parse','main']),self.main)

    def test_semantic_failure_does_not_create_a_proposal(self):
        with AgentToolFacade.open_repository(self.root,purpose='authoring') as facade:
            before = facade.find_proposals({'kind':'find-proposals'})
        rule = {**self.router['rules'][0], 'condition':'Synthetic unknown reference.',
                'when':{'operator':'exists','fact':'routing.missing-typed-fact'}}
        rejected = self.call('propose',{'change_set':self.change([
            {'kind':'put-routing-rule','rule':rule,'rationale':'Test unavailable reference.'}])},error=True)
        self.assertIn('rejected',rejected['kind'])
        with AgentToolFacade.open_repository(self.root,purpose='authoring') as facade:
            self.assertEqual(facade.find_proposals({'kind':'find-proposals'}),before)
        self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'rev-parse','main']),self.main)

    def test_shared_evidence_references_and_schema_validation_remain_before_edits(self):
        args = {'change_set':self.change([{'kind':'remove-routing-rule','rule':self.router['rules'][0]['id'],
                                         'rationale':'Test a malformed input.'}])}
        args['change_set']['edits'][0]['extra'] = 'not-a-member'
        invalid = self.call('propose', args, error=True)
        self.assertEqual(invalid['code'],'INTERFACE.INVALID_ARGUMENTS')
        self.assertIn('input_feedback',invalid)
        self.assertNotIn('context',invalid)
        self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'rev-parse','main']),self.main)
