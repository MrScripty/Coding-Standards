"""Proposal consumer publication through real MCP processes and Git/SQLite.

Every tool call reconnects a cold local stdio process. This tests the actual
wire boundary without requiring an optional SDK or the user's installed store.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.standards_engine.tests.test_agent_workflow import ROOT, decisions, evidence, prepare_repository
from tools.standards_engine.tests import test_proposal_consumers as fixtures
from tools.standards_engine.tests.test_proposal_consumers import registration


class ConsumerPublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='consumer-publication-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repository'
        prepare_repository(self.root)
        self.calls = []

    def rpc(self, method, params, purpose='authoring'):
        messages=[
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{
                'protocolVersion':'2025-11-25','capabilities':{},
                'clientInfo':{'name':'consumer-publication-test','version':'1'}}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':method,'params':params},
        ]
        process=subprocess.run(
            [sys.executable,'-P','-m','tools.standards_engine.standards_engine.mcp',
             '--repo-root',str(self.root),'--purpose',purpose,'--advanced'],
            input=''.join(json.dumps(m)+'\n' for m in messages),text=True,capture_output=True,
            env={**os.environ,'PYTHONPATH':str(ROOT)},timeout=180,
        )
        self.assertEqual(process.returncode,0,process.stderr)
        self.assertEqual(process.stderr,'')
        responses={row['id']:row for row in map(json.loads,process.stdout.splitlines())}
        self.assertIn('interface 35;',responses[1]['result']['instructions'])
        return responses[2]

    def call(self,name,arguments,purpose='authoring',error=False):
        self.calls.append(name)
        response=self.rpc('tools/call',{'name':name,'arguments':arguments},purpose)
        self.assertNotIn('error',response,response)
        result=response['result']
        self.assertEqual(result['isError'],error,result)
        self.assertEqual(json.loads(result['content'][0]['text']),result['structuredContent'])
        return result['structuredContent']

    def change(self,edits):
        return {'purpose':{'summary':'Qualify proposal consumer publication.',
                           'rationale':'This isolated repository owns the synthetic review evidence.',
                           'evidence':[evidence(self.root)]},'edits':edits}

    def complete(self,workflow):
        seen=set()
        while workflow.get('status')=='needs-action':
            identity=json.dumps(workflow['context'],sort_keys=True)
            self.assertNotIn(identity,seen);seen.add(identity)
            outcome=workflow['outcome']
            self.assertFalse(outcome.get('fact_requirements'),outcome)
            operations=[n for n in outcome['next_operations'] if n['operation']=='resolve']
            self.assertTrue(operations,outcome)
            selected=next((n for n in operations if n['request_kind']=='consumer-disposition'),operations[0])
            kind=selected['request_kind']
            if kind=='coverage-attestation':
                submission={'kind':kind,'claim':{
                    'requirement':selected['work'],'conclusion':'complete',
                    'evidence':[evidence(self.root)],'explicit_exclusions':[],
                    'rationale':'This fixture explicitly owns the selected synthetic consumer horizon.',
                    'auditor_provenance':'Isolated MCP test; not a standards-content audit.',
                }}
            else:
                self.assertIn(kind,{'consumer-disposition','impact-disposition'})
                obligation=next(o for o in outcome['obligations'] if o['handle']==selected['work'])
                submission={'kind':kind,'obligation':selected['work'],
                    'result':'reviewed-no-change' if kind=='consumer-disposition' else 'confirmed',
                    'fingerprint':obligation['fingerprint'],'evidence':[evidence(self.root)],
                    'rationale':'The isolated fixture confirms this exact declared consumer/owner change.'}
            workflow=self.call('resolve_workflow',{'context':workflow['context'],'submission':submission})
        self.assertEqual(workflow.get('status'),'complete',workflow)
        return workflow

    def test_same_candidate_registration_preview_review_publication_and_cold_readback(self):
        F=fixtures.ConsumerCompilerTests
        catalog=self.rpc('tools/list',{})['result']['tools']
        self.assertIn('preview_application',{t['name'] for t in catalog})
        self.assertIn('register-consumer',json.dumps(next(t for t in catalog if t['name']=='propose')['inputSchema']))
        self.assertNotIn('preview_application',{t['name'] for t in self.rpc('tools/list',{},'application')['result']['tools']})
        before=subprocess.check_output(['git','rev-parse','main'],cwd=self.root)
        original={p:(self.root/p).read_bytes() for p in (F.fixture_path,F.second_path,F.doc_path)}
        edits=F().initial_edits()
        # A published reference shares positive wording; hidden rationale stays editorial.
        (self.root/F.fixture_path).write_bytes(b'UNPUBLISHED_BEFORE_CAPTURE_DRIFT\n')
        workflow=self.call('propose',{'change_set':self.change(edits)})
        (self.root/F.fixture_path).write_bytes(original[F.fixture_path])
        self.assertIn(workflow.get('status'),{'needs-action','complete'},workflow)
        revision=workflow['revision']
        self.assertEqual(subprocess.check_output(['git','rev-parse','main'],cwd=self.root),before)
        for path,content in original.items():self.assertEqual((self.root/path).read_bytes(),content)
        author=self.call('query_proposal',{'revision':revision,'request':{'kind':'read','target':F.document}})
        self.assertEqual(author['role'],'documentation');self.assertIn('Apply the owned rule.',author['content'])
        preview=self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':F.owner,'detail':'full'}})
        self.assertEqual(preview['kind'],'candidate-application-read-result')
        self.assertEqual(preview['revision'],revision)
        self.assertNotIn('snapshot',preview);self.assertNotIn('handle',preview['policy'])
        self.assertNotIn('AUTHORING_PRIVATE_8159',json.dumps(preview))
        hidden=self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':F.document}},error=True)
        self.assertEqual(hidden['code'],'APPLICATION.CONTENT_UNAVAILABLE')
        denied=self.rpc('tools/call',{'name':'preview_application','arguments':{'revision':revision,'request':{'kind':'read','target':F.owner}}},'application')
        self.assertIn('error',denied)
        # A fresh process reconstructs the draft after unrelated working-tree drift.
        (self.root/F.fixture_path).write_bytes(b'LOCAL_UNPUBLISHED_INPUT_DRIFT\n')
        rebuilt=self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':F.owner,'detail':'full'}})
        self.assertEqual(rebuilt,preview)
        (self.root/F.fixture_path).write_bytes(original[F.fixture_path])
        bad=self.call('revise',{'context':workflow['context'],'change_set':self.change([
            registration('fixture.duplicate-consumer-path',F.fixture_path)])},error=True)
        status=self.call('workflow_status',{'context':workflow['context']})
        self.assertEqual(status['revision'],revision)
        self.assertEqual(subprocess.check_output(['git','rev-parse','main'],cwd=self.root),before)
        complete=self.complete(status)
        ready=self.call('review',{'context':complete['context'],'decisions':decisions(self.root)})
        self.assertEqual(ready['status'],'ready',ready)
        verified=self.call('verify_proposal',{'kind':'verify-proposal','revision':revision,'readiness':ready['context']})
        self.assertTrue(verified['verification']['passed'],verified)
        published=self.call('apply',{'context':ready['context']})
        self.assertEqual(published['status'],'applied',published)
        exposed=self.call('read',{'target':F.owner,'detail':'full'},purpose='application')
        self.assertEqual(exposed['content'],preview['content'])
        self.assertEqual(exposed['scope'],preview['scope'])
        self.assertEqual(exposed['requires'],preview['requires'])
        for path in (F.fixture_path,F.second_path):
            self.assertEqual(subprocess.check_output(['git','show','main:'+path],cwd=self.root),original[path])
        self.assertIn(b'Apply the owned rule.',subprocess.check_output(['git','show','main:'+F.doc_path],cwd=self.root))
        self.call('read',{'target':'provenance.consumer-test'},purpose='application',error=True)
        self.call('read',{'target':F.document},purpose='application',error=True)
        self.assertEqual(self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':F.owner,'detail':'full'}}),preview)
        self.assertNotEqual(subprocess.check_output(['git','rev-parse','main'],cwd=self.root),before)

    def test_failed_publication_observe_and_explicit_cold_completion(self):
        from tools.standards_engine.tests.test_agent_workflow import reference_change
        change = reference_change(self.root, "recovery-publication")
        change["edits"][0]["requires"] = []
        identity = change["edits"][0]["standard"]["id"]
        change["edits"].append({"kind": "approve-application-content", "target": identity})
        change["edits"].append({"kind": "audit-policy-unit", "policy": "workflow.commit.commit-message",
                                "rationale": "Qualify deterministic reconstruction of a reviewed coverage receipt."})
        proposed = self.call("propose", {"change_set": change})
        complete = self.complete(proposed)
        ready = self.call("review", {"context": complete["context"], "decisions": decisions(self.root)})
        self.assertEqual(ready["status"], "ready", ready)
        before = subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root)
        lock = self.root / ".git/refs/heads/main.lock"
        lock.write_bytes(b"owned by this isolated recovery test\n")
        failed = self.call("apply", {"context": ready["context"]})
        self.assertEqual(failed["status"], "recovery-required", failed)
        application = failed["outcome"]["application"]
        diagnostic = failed["outcome"]["details"]
        self.assertEqual(diagnostic["git_operation"], "update-ref")
        self.assertEqual(diagnostic["git_stderr_excerpt"], "File exists")
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root), before)
        observed = self.call("recover", {"context": ready["context"], "action": "observe"})
        self.assertEqual(observed["outcome"]["code"], "APPLICATION.RECOVERY_TARGET_UNCERTAIN")
        self.assertEqual(observed["outcome"]["application"], application)
        # Only the test owner releases its synthetic lock; the Engine never does.
        lock.unlink()
        local = self.root / "unpublished-local-note.txt"
        local.write_bytes(b"independent local data\n")
        recovered = self.call("recover", {"context": ready["context"], "action": "complete-publication"})
        self.assertEqual(recovered["status"], "applied", recovered)
        self.assertEqual(recovered["outcome"]["application"], application)
        published = subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root)
        self.assertNotEqual(published, before)
        again = self.call("recover_application", {
            "kind": "recover-application", "readiness": ready["context"],
            "action": "complete-publication",
        })
        self.assertEqual(again["application"], application)
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root), published)
        exposed = self.call("read", {"target": identity}, purpose="application")
        self.assertIn("isolated workflow test reference", exposed["content"])
        self.assertEqual(local.read_bytes(), b"independent local data\n")
        self.assertNotIn("unpublished-local-note.txt", subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "main"], cwd=self.root, text=True))


if __name__ == '__main__':
    unittest.main()
