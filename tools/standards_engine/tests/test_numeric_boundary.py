"""Schema-valid integral numbers reach domain authoring through the public facade."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.standards_engine.standards_engine import AgentToolFacade, SnapshotHandle
from tools.standards_engine.tests.test_agent_workflow import evidence
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree, _section_body
from tools.standards_engine.tests.test_request_evidence import shared

ROOT = Path(__file__).resolve().parents[3]
POLICY = 'workflow.planning.written-plan-applicability'


class NumericBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='numeric-boundary-')
        cls.root = Path(cls.temporary.name) / 'repository'
        _clone_tracked_worktree(cls.root)
        cls.facade = AgentToolFacade.open_repository(cls.root, purpose='authoring')
        capture = cls.facade.create_snapshot({'kind': 'create-snapshot'})
        assert capture['kind'] == 'create-snapshot-result', capture
        cls.snapshot = capture['snapshot']['snapshot']
        engine = cls.facade._engine
        compiled = engine._compiled_snapshot(engine._snapshot_id(SnapshotHandle.from_value(cls.snapshot)))
        cls.unit = compiled.corpus.resolve_policy_unit(POLICY)
        title = cls.unit.heading_path[-1]
        # The edit sends a heading and body, not the original module separator.
        cls.expected_content = f"## {title}\n\n{_section_body(cls.unit.content, title)}\n"
        cls.main_before = cls.main()

    @classmethod
    def tearDownClass(cls):
        cls.facade.close()
        cls.temporary.cleanup()

    @classmethod
    def main(cls):
        return subprocess.check_output(['git', '-C', str(cls.root), 'rev-parse', 'main'])

    def change(self, kind='preserve', numeric=float):
        revision = self.unit.semantic_revision
        semantics = {'kind': kind, 'intent': 'Isolated numeric boundary fixture.'}
        if kind == 'preserve':
            semantics['semantic_revision'] = numeric(revision)
        else:
            semantics.update(accepted_semantic_revision=numeric(revision),
                             proposed_semantic_revision=numeric(revision + 1))
        return {'purpose': {'summary': 'Verify numeric representation',
                'rationale': 'Disposable request; preserve the accepted repository.',
                'evidence': [evidence(self.root)]},
            'edits': [{'kind': 'revise-policy-unit', 'policy': POLICY,
                'title': self.unit.heading_path[-1],
                'body': _section_body(self.unit.content, self.unit.heading_path[-1]),
                'semantics': semantics}]}

    def test_both_semantic_revision_variants_reach_proposals_with_inline_or_shared_evidence(self):
        for kind in ('preserve', 'change'):
            for share in (False, True):
                with self.subTest(kind=kind, shared=share):
                    args = {'snapshot': self.snapshot, 'change_set': self.change(kind)}
                    expected = {'snapshot': self.snapshot, 'change_set': self.change(kind, int)}
                    if share:
                        args = shared(args)
                    before = deepcopy(args)
                    self.assertEqual(self.facade._decode_call('propose', args).as_contract(), expected)
                    result = self.facade.propose(args)
                    self.assertEqual(result['kind'], 'workflow-result', result)
                    self.assertIn(result['status'], ('needs-action', 'complete'), result)
                    read = self.facade.query_proposal({'revision': result['revision'],
                        'request': {'kind': 'read', 'target': POLICY}})
                    self.assertEqual(read['content'], self.expected_content)
                    self.assertEqual(args, before)
                    self.assertIs(type(before.get('change_set', {})['edits'][0]['semantics'][
                        'semantic_revision' if kind == 'preserve' else 'proposed_semantic_revision']), float)
        self.assertEqual(self.main(), self.main_before)

    def test_invalid_numeric_and_digest_requests_create_no_draft(self):
        before = self.facade.find_proposals({'kind': 'find-proposals'})
        for value in (True, False, 0, -1, 1.5, '1', float('inf'), float('nan')):
            args = {'snapshot': self.snapshot, 'change_set': self.change()}
            args['change_set']['edits'][0]['semantics']['semantic_revision'] = value
            result = self.facade.propose(args)
            self.assertEqual(result['kind'], 'rejected-result', result)
            self.assertEqual(result['code'], 'INTERFACE.INVALID_ARGUMENTS', result)
            self.assertNotIn('proposal', result)
        args = {'snapshot': self.snapshot, 'change_set': self.change()}
        args['change_set']['purpose']['evidence'][0]['digest'] += '\n'
        result = self.facade.propose(args)
        self.assertEqual(result['code'], 'INTERFACE.INVALID_ARGUMENTS', result)
        self.assertTrue(any(i['keyword'] == 'maxLength' for i in result['input_feedback']['issues']))
        self.assertEqual(self.facade.find_proposals({'kind': 'find-proposals'}), before)
        self.assertEqual(self.main(), self.main_before)

    def cold_call(self, operation, arguments, rejected=False):
        messages = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'boundary-regression', 'version': '1'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                'params': {'name': operation, 'arguments': arguments}},
        ]
        result = subprocess.run([sys.executable, '-P', '-m',
            'tools.standards_engine.standards_engine.mcp', '--repo-root', str(self.root),
            '--purpose', 'authoring', '--output-schemas', 'on-demand', '--advanced'],
            input=''.join(json.dumps(m) + '\n' for m in messages), text=True,
            capture_output=True, env={**os.environ, 'PYTHONPATH': str(ROOT)}, timeout=90)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        reply = json.loads(result.stdout.splitlines()[-1])['result']
        self.assertEqual(reply['isError'], rejected, reply)
        self.assertEqual(json.loads(reply['content'][0]['text']), reply['structuredContent'])
        return reply['structuredContent']

    def test_cold_stdio_accepts_integral_revisions_and_retains_rejection_without_effects(self):
        args = shared({'snapshot': self.snapshot, 'change_set': self.change()})
        # Schema-constrained handle versions are normalized on the same path.
        args['snapshot']['schema_version'] = float(args['snapshot']['schema_version'])
        result = self.cold_call('propose', args)
        self.assertEqual(result['kind'], 'workflow-result', result)
        self.assertIn(result['status'], ('needs-action', 'complete'))
        read = self.cold_call('query_proposal', {'revision': result['revision'],
            'request': {'kind': 'read', 'target': POLICY}})
        self.assertEqual(read['content'], self.expected_content)
        before = self.cold_call('find_proposals', {'kind': 'find-proposals'})
        args['change_set']['edits'][0]['semantics']['semantic_revision'] = 1.5
        invalid = self.cold_call('propose', args, rejected=True)
        self.assertEqual(invalid['code'], 'INTERFACE.INVALID_ARGUMENTS')
        self.assertEqual(self.cold_call('find_proposals', {'kind': 'find-proposals'}), before)
        self.assertEqual(self.main(), self.main_before)
