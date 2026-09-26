"""Review decisions exercise the real domain and SQLite boundary."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, AnalysisHandle
from tools.standards_engine.tests.test_agent_workflow import evidence, reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree


def topic_change(root: Path, label: str, count: int = 4):
    change = reference_change(root, label)
    template = change['edits'][0]
    change['edits'] = []
    for index in range(count):
        edit = deepcopy(template)
        edit['standard'].update(id=f'topic.{label}-{index}', role='topic', level='MUST')
        change['edits'].append(edit)
    return change


def decision(root, item):
    return {'kind': 'impact-disposition', 'obligation': item['handle'],
            'fingerprint': item['fingerprint'], 'result': 'confirmed',
            'rationale': 'The isolated fixture owner explicitly accepts this scope.',
            'evidence': [evidence(root)]}


class ReviewWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='review-workflow-ux-')
        cls.root = Path(cls.temp.name) / 'repository'
        _clone_tracked_worktree(cls.root)
        cls.facade = AgentToolFacade.open_repository(cls.root, purpose='authoring')
        cls.engine = cls.facade._engine
        captured = cls.facade.create_snapshot({'kind': 'create-snapshot'})
        assert captured['kind'] == 'create-snapshot-result', captured
        cls.snapshot = captured['snapshot']['snapshot']

    @classmethod
    def tearDownClass(cls):
        cls.facade.close()
        cls.temp.cleanup()

    def proposed(self, label, count=4):
        result = self.facade.propose({'snapshot': self.snapshot, 'change_set': topic_change(self.root, label, count)})
        self.assertEqual(result['status'], 'needs-action', result)
        return result

    def work(self, result):
        page = self.facade.workflow_details({'analysis': result['context'], 'section': 'pending_obligations'})
        self.assertEqual(page['kind'], 'workflow-details-result', page)
        return [item['obligation'] for item in page['items']]

    def test_compact_default_and_complete_observation_bound_pages(self):
        proposed = self.proposed('compact')
        full = self.facade.workflow_status({'context': proposed['context'], 'detail': 'full'})
        self.assertEqual(full['outcome']['kind'], 'pending-result')
        self.assertEqual(proposed['outcome']['kind'], 'workflow-analysis-summary')
        self.assertEqual(proposed['outcome']['required_obligations'], 4)
        status = self.facade.workflow_status({'context': proposed['context']})
        self.assertLess(len(json.dumps(status)), len(json.dumps(full)) / 2)
        self.assertEqual(proposed['work']['total'], 4)
        self.assertNotIn('work', status)
        arguments = {'analysis': proposed['context'], 'section': 'pending_obligations', 'limit': 1}
        items = []
        while True:
            page = self.facade.workflow_details(arguments)
            self.assertEqual(page['kind'], 'workflow-details-result', page)
            items.extend(item['obligation'] for item in page['items'])
            if 'next' not in page:
                break
            arguments = page['next']
        self.assertEqual(items, full['outcome']['obligations'])
        for invalid in ({**arguments, 'observation': 'sha256:' + '0'*64},
                        {key: value for key, value in arguments.items() if key != 'observation'}):
            result = self.facade.workflow_details(invalid)
            self.assertEqual(result['code'], 'WORKFLOW.OBSERVATION_CHANGED')
            self.assertNotIn('items', result)

    def test_batch_and_serial_decisions_have_identical_final_authority(self):
        original = self.proposed('equivalence')
        submitted = [decision(self.root, item) for item in self.work(original)]
        original_copy = deepcopy(submitted)
        with patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head',
                          wraps=self.engine._snapshots.publish_aggregate_if_root_head) as publish:
            batched = self.facade.resolve_many({'context': original['context'], 'submissions': submitted})
            self.assertEqual(publish.call_count, 1)
        self.assertEqual(submitted, original_copy)
        self.assertEqual(batched['status'], 'complete', batched)
        serial = original
        for _ in submitted:
            item = self.work(serial)[0]
            serial = self.facade.resolve_workflow({'context': serial['context'], 'submission': decision(self.root, item)})
        self.assertEqual(serial['context'], batched['context'])
        self.assertEqual(self.engine._load_analysis(AnalysisHandle.from_value(original['context'])).dispositions, ())
        with AgentToolFacade.open_repository(self.root, purpose='authoring') as cold:
            self.assertEqual(cold.workflow_status({'context': batched['context']}), batched)
        # Repeating the exact original request yields the same immutable authority;
        # it does not start a review/publication or duplicate disposition records.
        repeated = self.facade.resolve_many({'context': original['context'], 'submissions': submitted})
        self.assertEqual(repeated['context'], batched['context'])
        records = self.facade.workflow_details({'analysis': batched['context'], 'section': 'dispositions'})
        self.assertEqual(records['total'], 4)

    def test_historical_pages_survive_evidence_edits_but_decisions_revalidate(self):
        original = self.proposed('historical-evidence', 4)
        first = self.facade.workflow_details({
            'analysis': original['context'],
            'section': 'pending_obligations',
            'limit': 1,
        })
        self.assertEqual(first['kind'], 'workflow-details-result', first)
        submitted = decision(self.root, first['items'][0]['obligation'])
        evidence_path = self.root / 'tools/standards_engine/README.md'
        original_bytes = evidence_path.read_bytes()
        try:
            evidence_path.write_bytes(original_bytes + b'\nEvidence changed after paging.\n')
            with patch.object(
                self.engine._snapshots, 'publish_aggregate_if_root_head',
                wraps=self.engine._snapshots.publish_aggregate_if_root_head,
            ) as publish:
                second = self.facade.workflow_details(first['next'])
                self.assertEqual(second['kind'], 'workflow-details-result', second)
                self.assertEqual(second['observation'], first['observation'])
                self.assertEqual(second['analysis'], original['context'])
                self.assertEqual(second['offset'], 1)
                rejected = self.facade.resolve_many({
                    'context': original['context'], 'submissions': [submitted],
                })
                self.assertEqual(rejected['kind'], 'rejected-result', rejected)
                self.assertEqual(rejected['code'], 'ANALYSIS.EVIDENCE_DIGEST_MISMATCH')
                publish.assert_not_called()
        finally:
            evidence_path.write_bytes(original_bytes)
        self.assertEqual(self.facade.workflow_status({'context': original['context']}),
                         {key: value for key, value in original.items() if key != 'work'})

    def test_single_full_and_compact_batch_remain_workload_options(self):
        for count in (1, 4):
            with self.subTest(decisions=count):
                original = self.facade.propose({
                    'snapshot': self.snapshot,
                    'change_set': topic_change(self.root, f'options-{count}', count),
                    'detail': 'full',
                })
                self.assertEqual(original['outcome']['kind'], 'pending-result', original)
                submitted = [decision(self.root, item) for item in original['outcome']['obligations']]
                self.assertEqual(len(submitted), count)
                batched = self.facade.resolve_many({
                    'context': original['context'], 'submissions': submitted,
                })
                self.assertEqual(batched['status'], 'complete', batched)
                self.assertEqual(batched['outcome']['kind'], 'workflow-analysis-summary')
                serial = original
                for _ in submitted:
                    # Full results already expose actionable work: no page call is needed.
                    obligation = next(item for item in serial['outcome']['obligations']
                                      if item['state'] == 'required')
                    serial = self.facade.resolve_workflow({
                        'context': serial['context'],
                        'submission': decision(self.root, obligation),
                        'detail': 'full',
                    })
                self.assertEqual(serial['status'], 'complete', serial)
                self.assertEqual(serial['outcome']['kind'], 'complete-result')
                self.assertEqual(serial['context'], batched['context'])
                full_batch = self.facade.resolve_many({
                    'context': original['context'], 'submissions': submitted,
                    'detail': 'full',
                })
                self.assertEqual(full_batch, serial)

    def test_bad_last_decision_leaves_no_partial_analysis(self):
        original = self.proposed('invalid-last')
        submitted = [decision(self.root, item) for item in self.work(original)]
        submitted[-1]['fingerprint']['dependencies'][0]['digest'] = 'sha256:' + '0'*64
        with patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head',
                          wraps=self.engine._snapshots.publish_aggregate_if_root_head) as publish:
            result = self.facade.resolve_many({'context': original['context'], 'submissions': submitted})
            self.assertEqual(result['kind'], 'rejected-result', result)
            self.assertEqual(result['details']['submission_index'], 3)
            publish.assert_not_called()
        self.assertEqual(self.facade.workflow_status({'context': original['context']}),
                         {key: value for key, value in original.items() if key != 'work'})

    def test_duplicates_foreign_and_unknown_handles_reject_before_authorization(self):
        original = self.proposed('invalid-handles')
        valid = decision(self.root, self.work(original)[0])
        foreign = deepcopy(valid)
        foreign['obligation']['analysis']['id'] = 'analysis:sha256:' + '0'*64
        unknown = deepcopy(valid)
        unknown['obligation']['child_id'] = 'sha256:' + '0'*64
        for values in ([valid, valid], [foreign], [unknown]):
            with patch.object(self.engine, '_apply_submission', side_effect=AssertionError('early authorization')):
                result = self.facade.resolve_many({'context': original['context'], 'submissions': values})
                self.assertEqual(result['kind'], 'rejected-result', result)

    def test_stale_head_at_final_write_rejects_without_partial_batch(self):
        original = self.proposed('head-race')
        submitted = [decision(self.root, item) for item in self.work(original)]
        ordinary = self.engine._snapshots.publish_aggregate_if_root_head
        def race(*args):
            revised = self.facade.revise({'context': original['context'],
                                         'change_set': reference_change(self.root, 'head-race-added')})
            self.assertEqual(revised['kind'], 'workflow-result', revised)
            return ordinary(*args)
        with patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head', side_effect=race):
            result = self.facade.resolve_many({'context': original['context'], 'submissions': submitted})
        self.assertEqual(result['code'], 'WORKFLOW.STALE_CONTEXT', result)
        self.assertEqual(self.facade.workflow_status({'context': original['context']})['status'], 'stale')

    def test_limits_and_application_purpose(self):
        original = self.proposed('limits')
        valid = decision(self.root, self.work(original)[0])
        for values in ([], [valid]*129):
            result = self.facade.resolve_many({'context': original['context'], 'submissions': values})
            self.assertEqual(result['kind'], 'rejected-result')
        oversized = deepcopy(valid)
        oversized['rationale'] = 'x' * (256 * 1024)
        result = self.facade.resolve_many({'context': original['context'], 'submissions': [oversized]})
        self.assertEqual(result['code'], 'WORKFLOW.INPUT_LIMIT')
        for limit in (0, 17):
            self.assertEqual(self.facade.workflow_details({'analysis': original['context'],
                'section': 'obligations', 'limit': limit})['kind'], 'rejected-result')
        with AgentToolFacade.open_repository(self.root, purpose='application') as application:
            self.assertEqual(application.resolve_many({'context': original['context'], 'submissions': [valid]})['code'],
                             'APPLICATION.OPERATION_UNAVAILABLE')
            self.assertEqual(application.workflow_details({'analysis': original['context'], 'section': 'obligations'})['code'],
                             'APPLICATION.OPERATION_UNAVAILABLE')

    def test_denied_later_authorization_and_bad_evidence_leave_no_partial_state(self):
        from tools.standards_analysis.standards_analysis import AuthorizationDenied
        original = self.proposed('authorization')
        submissions = [decision(self.root, item) for item in self.work(original)]
        bad = deepcopy(submissions)
        bad[-1]['evidence'][0]['digest'] = 'sha256:' + '0'*64
        authorizer = self.engine._execution_context.authorization
        ordinary = authorizer.authorize
        denied_id = submissions[-1]['obligation']['child_id']
        def deny_last(request):
            return AuthorizationDenied('Fixture denies this exact decision.') if request.subject_id.endswith(denied_id) else ordinary(request)
        for values, adapter in ((bad, ordinary), (submissions, deny_last)):
            with patch.object(authorizer, 'authorize', side_effect=adapter), patch.object(
                    self.engine._snapshots, 'publish_aggregate_if_root_head',
                    wraps=self.engine._snapshots.publish_aggregate_if_root_head) as publish:
                result = self.facade.resolve_many({'context': original['context'], 'submissions': values})
                self.assertEqual(result['kind'], 'rejected-result', result)
                publish.assert_not_called()
        self.assertEqual(self.facade.workflow_status({'context': original['context']}),
                         {key: value for key, value in original.items() if key != 'work'})

    def test_page_payload_limit_preserves_complete_items(self):
        from tools.standards_engine.standards_engine import workflow_presentation
        original = self.proposed('page-size')
        with patch.object(workflow_presentation, 'PAGE_BYTES', 1):
            rejected = self.facade.workflow_details({'analysis': original['context'], 'section': 'pending_obligations'})
        self.assertEqual(rejected['code'], 'WORKFLOW.RESULT_LIMIT')
        self.assertNotIn('items', rejected)
        self.assertEqual(len(self.work(original)), 4)

    def test_page_continuation_binds_the_original_context_and_section(self):
        original = self.proposed('page-context')
        first = self.facade.workflow_details({'analysis': original['context'], 'section': 'obligations', 'limit': 1})
        self.assertIn('next', first)
        complete = self.facade.resolve_many({'context': original['context'],
            'submissions': [decision(self.root, item) for item in self.work(original)]})
        for replacement in ({'analysis': complete['context']}, {'section': 'pending_obligations'}):
            later = self.facade.workflow_details({**first['next'], **replacement})
            self.assertEqual(later['code'], 'WORKFLOW.OBSERVATION_CHANGED', later)
            self.assertNotIn('items', later)
        # The unchanged historical context remains readable after its successor.
        history = self.facade.workflow_details(first['next'])
        self.assertEqual(history['kind'], 'workflow-details-result', history)
        self.assertEqual(history['observation'], first['observation'])

    def test_fact_decision_uses_original_context_and_reveals_work_in_next_round(self):
        import subprocess
        from tools.standards_verifier.standards_verifier import write_suite_input_projection
        from tools.standards_engine.tests.test_proposal_consumers import ConsumerCompilerTests
        with tempfile.TemporaryDirectory(prefix='review-fact-') as temporary:
            root = Path(temporary) / 'repository'
            _clone_tracked_worktree(root)
            path = root / 'evaluation/standards-effectiveness/policy-impact-facts.toml'
            path.write_text('''schema_version = 1
id = "policy-impact.applicability"
[[facts]]
id = "changed"
semantic_revision = 1
type = "boolean"
nullable = false
aliases = []
meaning = "Whether the selected consumer is affected."
context_kind = "standards-change"
answer_contract = "fact-value.v1"
evidence_contract = "evidence-reference.v1"
authorization_capability = "standards.analyze"
prompt = "Is the selected consumer affected?"
''')
            write_suite_input_projection(root)
            subprocess.run(['git','add','--all'], cwd=root, check=True)
            subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                            '-c','commit.gpgsign=false','commit','--quiet','-m','test: declare a conditional fact'],cwd=root,check=True)
            with AgentToolFacade.open_repository(root, purpose='authoring') as facade:
                change = reference_change(root, 'conditional')
                owner = ConsumerCompilerTests.owner_edit()
                relation = ConsumerCompilerTests.relation('workflow.planning', 'normative-consumer')
                relation['relationship']['applicability'] = {'operator':'equals','fact':'changed','value':True}
                change['edits'] = [owner, relation]
                original = facade.propose({'change_set':change})
                self.assertEqual(original['kind'],'workflow-result',original)
                self.assertEqual(original['outcome']['pending_facts'],1,original)
                page = facade.workflow_details({'analysis':original['context'],'section':'fact_requirements'})
                self.assertEqual(original['work']['section'], 'fact_requirements')
                self.assertEqual(original['work']['items'], page['items'])
                self.assertEqual(original['work']['observation'], page['observation'])
                fact = {'kind':'provide-fact','requirement':original['work']['items'][0]['requirement']['handle'],
                        'value':{'type':'boolean','state':'known','value':True},'evidence':[evidence(root)]}
                result = facade.resolve_many({'context':original['context'],'submissions':[fact]})
                self.assertEqual(result['kind'],'workflow-result',result)
                self.assertEqual(result['outcome']['pending_facts'],0)
                self.assertEqual(result['work']['section'], 'pending_obligations')
                successor_page = facade.workflow_details({
                    'analysis': result['context'], 'section': result['work']['section']})
                self.assertEqual(result['work']['items'], successor_page['items'])
                self.assertEqual(result['work']['observation'], successor_page['observation'])
                serial = facade.resolve_workflow({'context': original['context'], 'submission': fact})
                self.assertEqual(serial['context'], result['context'], serial)
                records = facade.workflow_details({'analysis':result['context'],'section':'fact_observations'})
                self.assertEqual(records['total'],1,records)
                self.assertEqual(records['items'][0]['value']['value'],True)
                self.assertEqual(facade.workflow_details({'analysis':original['context'],'section':'fact_requirements'})['total'],1)
