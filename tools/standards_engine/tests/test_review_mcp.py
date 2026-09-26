"""Cold MCP review batching with real candidate publication and recovery."""
from __future__ import annotations

from tools.standards_engine.tests import test_consumer_publication as fixture
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_agent_workflow import evidence


class BatchedPublicationTests(fixture.ConsumerPublicationTest):
    def setUp(self):
        # The predecessor walkthrough remains a single-decision/full-detail test;
        # this subclass drives its same public workflows through compact batches.
        import tempfile
        from pathlib import Path
        self.temp = tempfile.TemporaryDirectory(prefix='batched-publication-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repository'
        _clone_tracked_worktree(self.root)
        self.calls = []
        self.batch_count = 0

    def call(self, name, arguments, purpose='authoring', error=False):
        if name in {'propose', 'revise', 'analyze', 'resolve_workflow', 'resolve_many', 'workflow_status', 'resume'}:
            arguments = {**arguments, 'detail': 'compact'}
        return super().call(name, arguments, purpose, error)

    def complete(self, workflow):
        seen = set()
        while workflow.get('status') == 'needs-action':
            identity = workflow['context']['id']
            self.assertNotIn(identity, seen); seen.add(identity)
            self.assertEqual(workflow['outcome']['kind'], 'workflow-analysis-summary')
            self.assertEqual(workflow['outcome']['pending_facts'], 0)
            # Mutations provide the first page. A resumed lightweight status
            # deliberately requires one initial read, then uses the same paging.
            page = workflow.get('work')
            if page is None:
                page = self.call('workflow_details', {
                    'analysis': workflow['context'], 'section': 'pending_obligations',
                })
                self.assertEqual(page['kind'], 'workflow-details-result', page)
            else:
                self.assertEqual(page['kind'], 'workflow-work-page', page)
            self.assertEqual(page['section'], 'pending_obligations')
            total = page['total']
            work = list(page['items'])
            if 'next' in page:
                request = {'analysis': workflow['context'], **page['next']}
                while True:
                    page = self.call('workflow_details', request)
                    work.extend(page['items'])
                    if 'next' not in page:
                        break
                    request = page['next']
            self.assertEqual(len(work), total)
            self.assertTrue(work)
            submissions = []
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
                submissions.append(submission)
            workflow = self.call('resolve_many', {'context':workflow['context'], 'submissions':submissions})
            self.batch_count += 1
        self.assertEqual(workflow['status'], 'complete', workflow)
        self.assertGreater(self.batch_count, 0)
        return workflow
