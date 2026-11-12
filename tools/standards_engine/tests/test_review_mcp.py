"""Compact review batching over real MCP stdio, up to the reviewed candidate.

The full-detail, single-decision walkthroughs in test_consumer_publication own
publication, recovery and cold readback of a reviewed candidate. This module
owns only what differs before review: compact results, paged work and batches.
"""
from __future__ import annotations

from tools.standards_engine.tests import test_consumer_publication as fixture
from tools.standards_engine.tests import test_proposal_consumers as consumers
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_agent_workflow import decisions, evidence


class BatchedPublicationTests(fixture.PublicationWorkflowCase):
    prepare = staticmethod(_clone_tracked_worktree)

    def call(self, name, arguments, purpose='authoring', error=False):
        if name in {'propose', 'revise', 'analyze', 'resolve_workflow', 'resolve_many', 'workflow_status', 'resume'}:
            arguments = {**arguments, 'detail': 'compact'}
        return super().call(name, arguments, purpose, error)

    def paged_work(self, workflow, limit):
        """Read all pending work of a compact result through explicit detail pages."""
        request = {'analysis': workflow['context'], 'section': 'pending_obligations', 'limit': limit}
        work, pages = [], 0
        while True:
            page = self.call('workflow_details', request)
            self.assertEqual(page['kind'], 'workflow-details-result', page)
            self.assertEqual(page['section'], 'pending_obligations')
            self.assertLessEqual(len(page['items']), limit)
            work.extend(page['items'])
            pages += 1
            if 'next' not in page:
                break
            request = page['next']
        self.assertEqual(len(work), page['total'])
        self.assertGreater(pages, 1, 'the limit must force at least one continuation')
        return work

    def submissions(self, work):
        submitted = []
        for item in work:
            obligation = item['obligation']
            kind = obligation['permitted_submissions'][0]
            if kind == 'coverage-attestation':
                submission = {'kind':kind,'claim':{
                    'requirement':item['work'], 'conclusion':'complete',
                    'evidence':[evidence(self.root)], 'explicit_exclusions':[],
                    'rationale':'The fixture owns and reviewed the complete declared consumer horizon.',
                    'auditor_provenance':'Isolated MCP batch test, not a real content audit.'}}
            else:
                self.assertIn(kind, {'consumer-disposition', 'impact-disposition'})
                submission = {'kind':kind, 'obligation':item['work'],
                    'result':'reviewed-no-change' if kind=='consumer-disposition' else 'confirmed',
                    'fingerprint':obligation['fingerprint'], 'evidence':[evidence(self.root)],
                    'rationale':'Explicit review of this isolated consumer or scope.'}
            submitted.append(submission)
        return submitted

    def test_compact_results_paged_work_and_batches_complete_a_reviewable_workflow(self):
        F = consumers.ConsumerCompilerTests
        proposed = self.call('propose', {'change_set': self.change(F().initial_edits())})
        self.assertEqual(proposed['status'], 'needs-action', proposed)
        self.assertEqual(proposed['outcome']['kind'], 'workflow-analysis-summary')
        self.assertEqual(proposed['outcome']['pending_facts'], 0)
        # A mutation supplies the first page of its work with the compact summary.
        inline = proposed['work']
        self.assertEqual((inline['kind'], inline['section']), ('workflow-work-page', 'pending_obligations'), inline)
        self.assertGreater(inline['total'], 3)
        partial = self.call('resolve_many', {'context': proposed['context'],
                                             'submissions': self.submissions(inline['items'][:2])})
        self.assertEqual(partial['status'], 'needs-action', partial)
        self.assertEqual(partial['work']['kind'], 'workflow-work-page', partial)
        self.assertEqual(partial['work']['total'], inline['total'] - 2)
        # A rejected compact revision leaves the workflow where the batch left it.
        self.call('revise', {'context': partial['context'], 'change_set': self.change([
            consumers.registration('fixture.duplicate-consumer-path', F.fixture_path)])}, error=True)
        # A resumed lightweight status deliberately carries no work: the client
        # reads it once, in pages, and each continuation is used exactly as issued.
        status = self.call('workflow_status', {'context': partial['context']})
        self.assertEqual((status['status'], status['revision']), ('needs-action', proposed['revision']))
        self.assertEqual(status['outcome']['kind'], 'workflow-analysis-summary')
        self.assertNotIn('work', status)
        work = self.paged_work(status, limit=2)
        self.assertEqual(work[:len(partial['work']['items'])], partial['work']['items'])
        complete = self.call('resolve_many', {'context': status['context'], 'submissions': self.submissions(work)})
        self.assertEqual(complete['status'], 'complete', complete)
        self.assertEqual(complete['outcome']['kind'], 'workflow-analysis-summary')
        self.assertNotIn('work', complete)
        self.assertEqual(self.calls.count('resolve_many'), 2)
        ready = self.call('review', {'context': complete['context'], 'decisions': decisions(self.root)})
        self.assertEqual(ready['status'], 'ready', ready)
