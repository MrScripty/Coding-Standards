"""Proposal consumer publication through real MCP processes and Git/SQLite.

Each test talks to one local stdio server process per purpose and replaces it
only where a claim is about a new process. This tests the actual wire boundary
without requiring an optional SDK or the user's installed store.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest

from tools.standards_engine.standards_engine.tools import INTERFACE_CONTRACT
from tools.standards_engine.tests.stdio_server import StdioServers
from tools.standards_engine.tests.test_agent_workflow import decisions, evidence, prepare_repository
from tools.standards_engine.tests import test_proposal_consumers as fixtures
from tools.standards_engine.tests.test_proposal_consumers import registration


def installed_interface_version(root):
    # The server announces the interface declared by the repository it serves.
    # Read that declaration instead of repeating a number that each interface
    # edition would otherwise leave stale here.
    with (root / INTERFACE_CONTRACT).open('rb') as source:
        return tomllib.load(source)['interface_schema_version']


class PublicationWorkflowCase(unittest.TestCase):
    """An isolated repository and its servers; subclasses choose how decisions are submitted."""

    prepare = staticmethod(prepare_repository)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='consumer-publication-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repository'
        self.prepare(self.root)
        self.calls = []
        self.servers = StdioServers(client='consumer-publication-test')
        self.addCleanup(self.servers.close)

    def rpc(self, method, params, purpose='authoring'):
        # One server process per purpose serves every call of a test.
        server = self.servers.server(self.root, purpose, '--advanced')
        self.assertIn(f'interface {installed_interface_version(self.root)};',
                      server.initialized['result']['instructions'])
        return server.exchange(method, params)

    def restart(self, purpose='authoring'):
        """Replace this purpose's server: its next call is answered by a new process."""
        self.servers.restart(self.root, purpose, '--advanced')

    def call(self,name,arguments,purpose='authoring',error=False):
        if name in {"propose", "revise", "analyze", "resolve_workflow", "workflow_status", "resume"}:
            arguments = {"detail": "full", **arguments}
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


class ConsumerPublicationTest(PublicationWorkflowCase):
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
        labelled=self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':F.document}})
        self.assertEqual((labelled['kind'],labelled['review_state']),('candidate-application-read-result','not-reviewed'))
        self.assertEqual(preview['review_state'],'current')
        unknown=self.call('preview_application',{'revision':revision,'request':{'kind':'read','target':'provenance.consumer-test'}},error=True)
        self.assertEqual(unknown['code'],'APPLICATION.UNKNOWN_TARGET')
        denied=self.rpc('tools/call',{'name':'preview_application','arguments':{'revision':revision,'request':{'kind':'read','target':F.owner}}},'application')
        self.assertIn('error',denied)
        # A fresh process reconstructs the draft after unrelated working-tree drift.
        (self.root/F.fixture_path).write_bytes(b'LOCAL_UNPUBLISHED_INPUT_DRIFT\n')
        self.restart()
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
        self.assertEqual(published['outcome']['checkout']['status'],'current',published)
        self.assertEqual((self.root/F.doc_path).read_bytes(),
                         subprocess.check_output(['git','show','main:'+F.doc_path],cwd=self.root))
        # Cold readback: the application process that reads starts after publication.
        self.restart('application')
        exposed=self.call('read',{'target':F.owner,'detail':'full'},purpose='application')
        self.assertEqual(exposed['content'],preview['content'])
        self.assertEqual(exposed['scope'],preview['scope'])
        self.assertEqual(exposed['requires'],preview['requires'])
        for path in (F.fixture_path,F.second_path):
            self.assertEqual(subprocess.check_output(['git','show','main:'+path],cwd=self.root),original[path])
        self.assertIn(b'Apply the owned rule.',subprocess.check_output(['git','show','main:'+F.doc_path],cwd=self.root))
        self.assertEqual(exposed['review_state'],'current')
        hidden=self.call('read',{'target':'provenance.consumer-test'},purpose='application',error=True)
        self.assertEqual(hidden['code'],'APPLICATION.UNKNOWN_TARGET')
        document=self.call('read',{'target':F.document},purpose='application')
        self.assertEqual(document['review_state'],'not-reviewed')
        self.assertIn('Apply the owned rule.',document['content'])
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
        # Cold completion: a new process holds nothing from the failed apply or its observation.
        self.restart()
        recovered = self.call("recover", {"context": ready["context"], "action": "complete-publication"})
        self.assertEqual(recovered["status"], "applied", recovered)
        self.assertEqual(recovered["outcome"]["checkout"]["status"], "current", recovered)
        self.assertEqual(recovered["outcome"]["application"], application)
        published = subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root)
        self.assertNotEqual(published, before)
        again = self.call("recover_application", {
            "kind": "recover-application", "readiness": ready["context"],
            "action": "complete-publication",
        })
        self.assertEqual(again["application"], application)
        self.assertEqual(again["checkout"]["status"], "current", again)
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "main"], cwd=self.root), published)
        exposed = self.call("read", {"target": identity}, purpose="application")
        self.assertIn("isolated workflow test reference", exposed["content"])
        self.assertEqual(local.read_bytes(), b"independent local data\n")
        self.assertNotIn("unpublished-local-note.txt", subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "main"], cwd=self.root, text=True))


if __name__ == '__main__':
    unittest.main()
