"""Proposal-local registration, captured input and candidate-view regressions."""
from __future__ import annotations

from pathlib import Path
import unittest

from tools.standards_engine.standards_engine.logical_authoring import StandardsChangeSet
from tools.standards_engine.standards_engine.mcp import tool_catalog

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = {"id": "evidence:consumer-test", "digest": "sha256:" + "1" * 64,
            "provider_contract": "standards-evidence", "provider_contract_version": "1"}


def change(edits):
    return StandardsChangeSet.from_mapping({"purpose": {
        "summary": "Register selected consumer material.",
        "rationale": "The isolated fixture proves proposal-local consumer discovery.",
        "evidence": [EVIDENCE]}, "edits": edits})


def registration(identity="fixture.consumer-test", path="tools/tests/consumer.py", kind="fixture"):
    return {"kind": "register-consumer", "consumer": identity, "path": path,
            "artifact_kind": kind, "authority": "evidence" if kind == "fixture" else "projection"}


class ConsumerInterfaceTests(unittest.TestCase):
    def test_registration_edit_is_admitted(self):
        result = change([registration()])
        self.assertEqual(result.edits[0].as_contract()["kind"], "register-consumer")

    def test_authoring_catalog_exposes_candidate_preview(self):
        authoring = {item["name"] for item in tool_catalog(ROOT, purpose="authoring")}
        self.assertIn("preview_application", authoring)
        application = {item["name"] for item in tool_catalog(ROOT, purpose="application")}
        self.assertNotIn("preview_application", application)


class ConsumerInputTests(unittest.TestCase):
    def test_public_schema_excludes_private_capture_and_accepts_documentation(self):
        from tools.standards_contracts.standards_contracts import ContractError
        from tools.standards_engine.standards_engine import _generated_contract as c
        public = registration('documentation.authoring', '.agents/skills/example/references/authoring.md', 'documentation')
        self.assertEqual(c.RegisterConsumerEdit.from_value(public).as_contract(), public)
        with self.assertRaises(ContractError):
            c.RegisterConsumerEdit.from_value({**public, 'source': {'snapshot': 'private', 'content': ''}})

    def test_invalid_paths_types_and_disguised_code_are_rejected(self):
        from tools.standards_engine.standards_engine.authoring import AuthoringError
        for fields in ({'path': '../outside'}, {'path': '/absolute'}, {'path': 'tools//file.py'},
                       {'path': 'tools/./file.py'}, {'artifact_kind': []}, {'authority': []},
                       {'artifact_kind': 'documentation', 'path': 'tools/file.py'}):
            with self.subTest(fields=fields), self.assertRaises(AuthoringError):
                change([{**registration(), **fields}])

    def test_binding_is_owned_and_requires_original_membership(self):
        from tools.standards_engine.standards_engine.consumer_authoring import bind_sources
        from tools.standards_engine.standards_engine.authoring import AuthoringError
        from unittest.mock import Mock
        reader = Mock(return_value=b'original\x00binary')
        path = 'tools/tests/consumer.py'
        bound = bind_sources(change([registration()]), 'snapshot:test', (path,), reader)
        reader.assert_called_once_with(path)
        with self.assertRaises(AuthoringError):
            bind_sources(bound, 'snapshot:test', (path,), reader)
        with self.assertRaises(AuthoringError):
            bind_sources(change([registration()]), 'snapshot:test', (), reader)
        reader.assert_called_once_with(path)

    def test_capture_is_snapshot_bound_and_conflicting_bytes_are_rejected(self):
        from tools.standards_engine.standards_engine.consumer_authoring import bind_sources, captured_sources
        from tools.standards_engine.standards_engine.logical_authoring import LogicalProgram
        from tools.standards_engine.standards_engine.authoring import AuthoringError
        path = 'tools/tests/consumer.py'
        bound = bind_sources(change([registration()]), 'snapshot:test', (path,), lambda _: b'original')
        self.assertEqual(captured_sources(LogicalProgram([bound]), 'snapshot:test', {}, (path,)), ((path,b'original'),))
        for snapshot, originals, members in [('different',{},(path,)), ('snapshot:test',{path:b'changed'},(path,)), ('snapshot:test',{},())]:
            with self.subTest(snapshot=snapshot, originals=originals), self.assertRaises(AuthoringError):
                captured_sources(LogicalProgram([bound]),snapshot, originals,members)


class ConsumerCompilerTests(unittest.TestCase):
    """Real metadata, graph, coverage and logical replay over captured authority."""
    snapshot = 'snapshot:consumer-fixture'
    fixture_path = 'tools/standards_engine/tests/test_navigation.py'
    second_path = 'tools/standards_analysis/tests/test_routing.py'
    doc_path = '.agents/skills/standards-engine/references/authoring.md'
    policy = 'topic.consumer-fixture.owned'
    owner = 'topic.consumer-fixture'
    document = 'documentation.consumer-fixture'

    @classmethod
    def setUpClass(cls):
        from tools.standards_engine.tests.test_logical_authoring import LogicalAuthoringTests
        LogicalAuthoringTests.setUpClass()
        cls.base = LogicalAuthoringTests.base
        cls.compiled = LogicalAuthoringTests.compiled
        cls.paths = LogicalAuthoringTests.repository_paths
        for path in (cls.fixture_path, cls.second_path, cls.doc_path):
            assert path in cls.paths and path not in dict(cls.base.files), path

    def bound(self, edits):
        from tools.standards_engine.standards_engine.consumer_authoring import bind_sources
        return bind_sources(change(edits), self.snapshot, self.paths, lambda path: (ROOT/path).read_bytes())

    def project(self, changes, predecessor=None):
        from tools.standards_engine.standards_engine.logical_authoring import LogicalAuthoringCompiler, LogicalProgram
        from tools.standards_engine.standards_engine.engine import StandardsEngine
        return LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base, LogicalProgram(changes), base_snapshot=self.snapshot,
            base_repository_paths=self.paths, compiled_base=self.compiled, predecessor=predecessor,
        )

    @classmethod
    def owner_edit(cls):
        from tools.standards_engine.tests.test_logical_authoring import LogicalAuthoringTests
        from tools.standards_engine.tests.test_policy_registration import unit
        edit = LogicalAuthoringTests.new_standard_edit()
        edit['standard'].update(id=cls.owner,title='Consumer Fixture',body='## Owned Scope\n\nObserve the owned outcome.\n')
        edit['policy_units']=[unit(cls.policy,'Owned Scope')]
        edit['requires']=[]
        return edit

    @classmethod
    def relation(cls, consumer, kind):
        return {'kind':'put-policy-relationship','relationship':{
            'source_policy':cls.policy,'consumer':consumer,'relation':kind,
            'applicability':{'operator':'always'},'source_scope':None,'consumer_scope':None,
            'evidence_owner':'review:consumer','rationale':'The selected fixture consumes this rule.'}}

    def initial_edits(self):
        return [self.owner_edit(),
                registration('fixture.first', self.fixture_path),
                registration('fixture.second', self.second_path),
                registration(self.document, self.doc_path, 'documentation'),
                self.relation('fixture.first','fixture-projection'),
                self.relation('fixture.second','fixture-projection'),
                self.relation(self.document,'documentation-projection'),
                {'kind':'revise-operational-artifact','target':self.document,
                 'title':'Correct Consumer Guidance','body':'Apply the owned rule.\n'},
                {'kind':'put-provenance','record':{'id':'provenance.consumer-test','subject':self.policy,
                 'origin':'current-justification','rationale':'AUTHORING_PRIVATE_8159','evidence':[]}},
                {'kind':'approve-application-content','target':self.owner}]

    def test_draft_policy_consumers_documentation_and_provenance_compile_together(self):
        result=self.project([self.bound(self.initial_edits())])
        self.assertEqual(result.compiled.corpus.resolve_policy_unit(self.policy).module,self.owner)
        self.assertEqual(len([s for s in result.compiled.policy_impact.semantics.values() if s.source==self.policy]),3)
        self.assertEqual(result.compiled.materials[self.document].role,'documentation')
        self.assertEqual(result.source.read_bytes(self.doc_path),b'# Correct Consumer Guidance\n\nApply the owned rule.\n')
        self.assertEqual(result.source.read_bytes(self.fixture_path),(ROOT/self.fixture_path).read_bytes())
        self.assertEqual(result.compiled.supporting.exposure_state(self.document,result.compiled.materials[self.document].binding),'unreviewed')
        self.assertNotIn(self.policy,result.compiled.repository_coverage.covered_subjects)
        self.assertEqual(set(result.repository_paths)-set(self.paths),
                         set(dict(result.source.files))-set(dict(self.base.files))-{self.fixture_path,self.second_path,self.doc_path})
        self.assertNotIn(self.doc_path,dict(self.base.files))

    def test_cold_and_incremental_replay_preserve_bound_source_and_candidate(self):
        first=self.bound(self.initial_edits())
        previous=self.project([first]);before=dict(previous.source.files)
        second=change([{'kind':'approve-application-content','target':self.document}])
        warm=self.project([first,second],predecessor=previous)
        cold=self.project([first,second])
        self.assertEqual(warm.source.files,cold.source.files)
        self.assertEqual(warm.captured_consumer_files,cold.captured_consumer_files)
        self.assertEqual(warm.analysis_policy_ids,cold.analysis_policy_ids)
        self.assertEqual(dict(previous.source.files),before)
        # Published original input is retained independently of the edited file.
        self.assertEqual(dict(cold.captured_consumer_files)[self.doc_path],(ROOT/self.doc_path).read_bytes())
        self.assertNotEqual(dict(cold.captured_consumer_files)[self.doc_path],cold.source.read_bytes(self.doc_path))

    def test_failed_successor_and_duplicate_file_leave_prefix_unchanged(self):
        from tools.standards_engine.standards_engine.authoring import AuthoringError
        first=self.bound(self.initial_edits());previous=self.project([first]);before=dict(previous.source.files)
        bad=self.bound([registration('fixture.duplicate-path',self.fixture_path)])
        with self.assertRaises(AuthoringError) as error:
            self.project([first,bad],predecessor=previous)
        self.assertEqual(error.exception.failure.code,'AUTHORING.CONSUMER_PATH_EXISTS')
        self.assertEqual(dict(previous.source.files),before)

    def test_registers_consumers_after_policy_was_created_in_an_earlier_draft(self):
        first=change([self.owner_edit()])
        previous=self.project([first])
        second=self.bound([registration('fixture.later',self.fixture_path),
                           self.relation('fixture.later','fixture-projection')])
        warm=self.project([first,second],predecessor=previous)
        cold=self.project([first,second])
        self.assertEqual(warm.source.files,cold.source.files)
        self.assertNotIn('fixture.later',previous.compiled.policy_impact.artifacts)
        self.assertIn('fixture.later',warm.compiled.policy_impact.artifacts)
        self.assertEqual(warm.compiled.corpus.resolve_policy_unit(self.policy),
                         previous.compiled.corpus.resolve_policy_unit(self.policy))

    def test_existing_canonical_identity_and_artifact_alias_are_not_rebound(self):
        from tools.standards_engine.standards_engine.authoring import AuthoringError
        for identity in ['core',next(iter(self.compiled.policy_impact.artifacts))]:
            with self.subTest(identity=identity),self.assertRaises(AuthoringError):
                self.project([self.bound([registration(identity,self.fixture_path)])])

    def test_candidate_view_uses_same_qualification_without_published_handles(self):
        from tools.standards_engine.standards_engine.context_projection import ApplicationView, preview_application
        from tools.standards_engine.standards_engine import _generated_contract as c
        result=self.project([self.bound(self.initial_edits())])
        revision=c.ProposalRevisionHandle.from_value({'kind':'proposal-revision-handle',
                   'id':'proposal-revision:sha256:'+'1'*64,'schema_version':1})
        snapshot=c.SnapshotHandle.from_value({'kind':'snapshot-handle','id':'snapshot:v1:00000000-0000-4000-8000-000000000001','schema_version':5})
        value=ApplicationView(result.compiled,revision).read(self.owner,'full').as_contract()
        normal=ApplicationView(result.compiled,snapshot).read(self.owner,'full').as_contract()
        self.assertEqual(value['content'],normal['content'])
        self.assertEqual(value['requires'],normal['requires'])
        self.assertEqual(value['kind'],'candidate-application-read-result')
        self.assertNotIn('snapshot',value);self.assertNotIn('handle',value['policy'])
        import json
        self.assertNotIn('AUTHORING_PRIVATE_8159',json.dumps(value))
        self.assertNotIn('fixture.first',json.dumps(value))
        for target in [self.document,'provenance.consumer-test','fixture.first']:
            call=c.PreviewApplicationCall.from_value({'revision':revision.as_contract(),'request':{'kind':'read','target':target}})
            denied=preview_application(None,result.compiled,call).as_contract()
            self.assertEqual(denied['kind'],'candidate-application-rejected-result')
            self.assertEqual(denied['revision'],revision.as_contract())


class CandidateProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools.standards_engine.tests import test_purpose_projection as fixture
        from tools.standards_engine.standards_engine import _generated_contract as c
        fixture.PurposeProjectionTest.setUpClass()
        cls.fixture=fixture
        cls.state=fixture.PurposeProjectionTest
        cls.revision=c.ProposalRevisionHandle.from_value({
            'kind':'proposal-revision-handle','id':'proposal-revision:sha256:'+'2'*64,'schema_version':1})

    @classmethod
    def tearDownClass(cls):
        cls.state.tearDownClass()

    def preview(self,request,compiled=None):
        from tools.standards_engine.standards_engine.context_projection import preview_application
        from tools.standards_engine.standards_engine import _generated_contract as c
        return preview_application(self.state.engine,compiled or self.state.compiled,
            c.PreviewApplicationCall.from_value({'revision':self.revision.as_contract(),'request':request})).as_contract()

    def test_route_questions_and_selected_content_share_application_semantics(self):
        import json
        candidate=self.preview({'kind':'route','facts':{}})
        published=self.state.facade.route({'snapshot':self.state.snapshot,'facts':{}})
        for field in ('status','reading_plan','unresolved_questions'):
            self.assertEqual(candidate[field],published[field])
        self.assertEqual(candidate['kind'],'candidate-application-route-result')
        self.assertNotIn(self.fixture.PRIVATE,json.dumps(candidate))
        self.assertTrue(candidate['next_operations'])
        for operation in candidate['next_operations']:
            self.assertEqual(operation['operation'],'preview_application')
            self.assertEqual(operation['revision'],self.revision.as_contract())
            self.assertEqual(self.preview(operation['request'])['kind'],'candidate-application-read-result')

    def test_related_result_uses_revision_bound_continuations(self):
        request={'kind':'related','target':'router','groups':['standards-requires'],
                 'direction':'outgoing','transitive':False}
        candidate=self.preview(request)
        published=self.state.facade.related({'snapshot':self.state.snapshot,**{k:v for k,v in request.items() if k!='kind'}})
        self.assertEqual(candidate['relationships'],[
            {k:v for k,v in relation.items() if k!='handle'} for relation in published['relationships']])
        self.assertEqual(candidate['kind'],'candidate-application-related-result')
        self.assertTrue(candidate['next_operations'])
        self.assertTrue(all(op['operation']=='preview_application' for op in candidate['next_operations']))

    def test_stale_exposure_is_rejected_without_partial_candidate_content(self):
        files=dict(self.state.files)
        files['CORE-STANDARDS.md']+=b'\nUNAPPROVED_NEW_MATERIAL\n'
        compiled=self.fixture.compile_files(files)
        for request in ({'kind':'read','target':'core'}, {'kind':'route','facts':{}}):
            result=self.preview(request,compiled)
            self.assertEqual(result['code'],'APPLICATION.CONTENT_UNAVAILABLE')
            self.assertEqual(result['revision'],self.revision.as_contract())
            self.assertNotIn('content',result)


if __name__ == '__main__':
    unittest.main()
