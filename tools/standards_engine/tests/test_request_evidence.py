"""Request-local references preserve native authority, evidence and atomicity."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine import decision_batch
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.tests.test_agent_workflow import decisions, evidence, reference_change
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree
from tools.standards_engine.tests.test_review_workflow_ux import decision, topic_change

ROOT = Path(__file__).resolve().parents[3]
REFERENCE_FIELDS = {'id', 'digest', 'provider_contract', 'provider_contract_version'}


def shared(arguments):
    """Fixture client replaces exact reference objects, never production input."""
    table = {}
    names = {}

    def replace(value):
        if isinstance(value, dict):
            if set(value) == REFERENCE_FIELDS:
                key = json.dumps(value, sort_keys=True)
                if key not in names:
                    name = f'review-{len(names)}'
                    names[key] = name
                    table[name] = deepcopy(value)
                return {'evidence_ref': names[key]}
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return value

    result = replace(arguments)
    return {**result, 'evidence': table}


class RequestEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='request-evidence-')
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

    def pending(self, label, count=4):
        result = self.facade.propose({'snapshot': self.snapshot, 'change_set': topic_change(self.root, label, count)})
        self.assertEqual(result['status'], 'needs-action', result)
        return result

    def submissions(self, pending):
        return [decision(self.root, item['obligation']) for item in pending['work']['items']]

    def test_every_agent_operation_normalizes_authored_examples_to_native_types(self):
        examples = json.loads((ROOT / 'tools/standards_engine/contracts/examples/a1-examples.json').read_text())['examples']
        operations = [op for op in _contracts(ROOT).interface.operations if 'agent' in op.variants]
        self.assertEqual({op.id for op in operations}, {'propose', 'revise', 'resolve_workflow', 'resolve_many', 'review'})
        for op in operations:
            fixtures = [e['value'] for e in examples if e['definition'] == op.input_definition]
            self.assertTrue(fixtures, op.id)
            for original in fixtures:
                selected = shared(original)
                before = deepcopy(selected)
                checked = self.facade._decode_call(op.id, selected, None)
                with self.subTest(operation=op.id):
                    self.assertIs(type(checked), c.MODEL_TYPES[op.input_definition])
                    self.assertEqual(checked.as_contract(), original)
                    self.assertEqual(selected, before)

    def test_shared_batch_has_identical_analysis_and_cold_readback(self):
        pending = self.pending('same-authority')
        arguments = {'context': pending['context'], 'submissions': self.submissions(pending)}
        aliased = shared(arguments)
        original = deepcopy(aliased)
        native = self.facade.resolve_many(arguments)
        selected = self.facade.resolve_many(aliased)
        self.assertEqual(selected['status'], 'complete', selected)
        self.assertEqual(selected, native)
        self.assertEqual(aliased, original)
        self.assertLess(len(json.dumps(aliased)), len(json.dumps(arguments)))
        with AgentToolFacade.open_repository(self.root, purpose='authoring') as cold:
            self.assertEqual(cold.workflow_status({'context': selected['context']}), selected)
            # Local names from the previous request cannot be reused implicitly.
            forgotten = {k: v for k, v in aliased.items() if k != 'evidence'}
            self.assertEqual(cold.resolve_many(forgotten)['outcome'], 'invalid')
        full = self.facade.workflow_status({'context': selected['context'], 'detail': 'full'})
        self.assertNotIn('evidence_ref', json.dumps(full))
        self.assertNotIn('review-0', json.dumps(full))

    def test_propose_revise_and_review_accept_exact_shared_evidence_without_publication(self):
        created = self.facade.propose(shared({'snapshot': self.snapshot, 'change_set': reference_change(self.root, 'all-operations')}))
        self.assertEqual(created['status'], 'complete', created)
        revision = self.facade.revise(shared({'context': created['context'], 'change_set': reference_change(self.root, 'all-operations', revision=True)}))
        self.assertEqual(revision['status'], 'complete', revision)
        args = {'context': revision['context'], 'decisions': decisions(self.root)}
        with patch.object(self.engine, 'apply_proposal', side_effect=AssertionError('implicit publication')):
            aliased = self.facade.review(shared(args))
            native = self.facade.review(args)
        self.assertEqual(aliased['status'], 'ready', aliased)
        self.assertEqual(aliased, native)
        self.assertNotIn('evidence_ref', json.dumps(aliased))

    def test_single_resolution_reuses_the_ordinary_validator(self):
        pending = self.pending('single', 1)
        args = {'context': pending['context'], 'submission': self.submissions(pending)[0]}
        self.assertEqual(self.facade.resolve_workflow(shared(args)), self.facade.resolve_workflow(args))

    def test_missing_unused_nested_aliases_never_dispatch(self):
        pending = self.pending('invalid-local-table', 2)
        args = shared({'context': pending['context'], 'submissions': self.submissions(pending)})
        cases = []
        missing = deepcopy(args)
        missing['submissions'][0]['evidence'] = [{'evidence_ref': 'missing'}]
        cases.append(missing)
        unused = deepcopy(args)
        unused['evidence']['unused'] = evidence(self.root)
        cases.append(unused)
        nested = deepcopy(args)
        nested['evidence']['review-0'] = {'evidence_ref': 'review-0'}
        cases.append(nested)
        extra = deepcopy(args)
        extra['submissions'][0]['evidence'][0]['extra'] = True
        cases.append(extra)
        table_limit = deepcopy(args)
        table_limit['evidence'] = {f'e{i}': evidence(self.root) for i in range(129)}
        cases.append(table_limit)
        for case in cases:
            with self.subTest(case=cases.index(case)), patch.object(self.engine, 'resolve_many', side_effect=AssertionError('invalid request dispatched')):
                value = self.facade.resolve_many(case)
            self.assertEqual(value['outcome'], 'invalid', value)

    def test_changed_evidence_and_unsupported_provider_still_publish_nothing(self):
        pending = self.pending('live-evidence', 2)
        args = shared({'context': pending['context'], 'submissions': self.submissions(pending)})
        path = self.root / evidence(self.root)['id']
        original = path.read_bytes()
        try:
            path.write_bytes(original + b'\nChanged after submission construction.\n')
            with patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head', side_effect=AssertionError('invalid evidence published')):
                result = self.facade.resolve_many(args)
            self.assertEqual(result['code'], 'ANALYSIS.EVIDENCE_DIGEST_MISMATCH', result)
        finally:
            path.write_bytes(original)
        unknown = deepcopy(args)
        unknown['evidence']['review-0']['provider_contract'] = 'unregistered-provider'
        with patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head', side_effect=AssertionError('unsupported evidence published')):
            result = self.facade.resolve_many(unknown)
        self.assertIn(result['outcome'], ('unsupported', 'unavailable'))

    def test_expanded_batch_limit_cannot_be_bypassed(self):
        pending = self.pending('expanded-limit', 4)
        ordinary = {'context': pending['context'], 'submissions': self.submissions(pending)}
        args = shared(ordinary)
        encoded = len(json.dumps(ordinary['submissions']).encode())
        self.assertLess(len(json.dumps(args['submissions']).encode()), encoded)
        with patch.object(decision_batch, 'INPUT_BYTES', encoded - 1), \
             patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head', side_effect=AssertionError('oversized batch published')):
            result = self.facade.resolve_many(args)
        self.assertEqual(result['code'], 'WORKFLOW.INPUT_LIMIT', result)

    def test_authored_text_is_not_interpreted_as_an_evidence_reference(self):
        native = {'change_set': reference_change(self.root, 'literal-text')}
        native['change_set']['edits'][0]['standard']['body'] = '{"evidence_ref":"not-a-binding"}'
        normalized = self.facade._decode_call('propose', shared(native), None)
        self.assertEqual(normalized.as_contract(), native)

    def test_expansion_preserves_each_native_uniqueness_contract(self):
        pending = self.pending('native-uniqueness', 1)
        args = shared({'context': pending['context'], 'decisions': decisions(self.root)})
        args['evidence']['same-bytes'] = evidence(self.root)
        args['decisions'][0]['evidence'].append({'evidence_ref': 'same-bytes'})
        with patch.object(self.engine, 'review', side_effect=AssertionError('duplicate review evidence dispatched')):
            result = self.facade.review(args)
        self.assertEqual(result['outcome'], 'invalid')
        # Impact submissions intentionally do not require unique evidence arrays.
        # Preserve that native contract rather than inventing a blanket restriction.
        ordinary = {'context': pending['context'], 'submissions': self.submissions(pending)}
        ordinary['submissions'][0]['evidence'] *= 2
        normalized = self.facade._decode_call('resolve_many', shared(ordinary), None)
        self.assertEqual(normalized.as_contract(), ordinary)

    def test_foreign_work_and_denied_later_decision_cannot_use_shared_evidence_as_authority(self):
        from tools.standards_analysis.standards_analysis import AuthorizationDenied
        pending = self.pending('shared-authorization', 2)
        original = shared({'context': pending['context'], 'submissions': self.submissions(pending)})
        foreign = deepcopy(original)
        foreign['submissions'][0]['obligation']['analysis']['id'] = 'analysis:sha256:' + '0'*64
        with patch.object(self.engine, '_apply_submission', side_effect=AssertionError('foreign work authorized')):
            self.assertIn('rejected', self.facade.resolve_many(foreign)['kind'])
        authorizer = self.engine._execution_context.authorization
        ordinary = authorizer.authorize
        denied_id = original['submissions'][-1]['obligation']['child_id']

        def deny_last(request):
            return (AuthorizationDenied('Fixture denies this exact decision.')
                    if request.subject_id.endswith(denied_id) else ordinary(request))

        with patch.object(authorizer, 'authorize', side_effect=deny_last), \
             patch.object(self.engine._snapshots, 'publish_aggregate_if_root_head', side_effect=AssertionError('denied batch published')):
            result = self.facade.resolve_many(original)
        self.assertIn('rejected', result['kind'])
        self.assertEqual(self.facade.workflow_status({'context': pending['context']}),
                         {k: v for k, v in pending.items() if k != 'work'})

    def test_agent_schema_family_only_changes_evidence_positions(self):
        schema = _contracts(ROOT).schema['$defs']
        roots = [op.input_definition for op in _contracts(ROOT).interface.operations if 'agent' in op.variants]

        def refs(value):
            if isinstance(value, dict):
                if '$ref' in value:
                    yield value['$ref'].rsplit('/', 1)[-1]
                for item in value.values():
                    yield from refs(item)
            elif isinstance(value, list):
                for item in value:
                    yield from refs(item)

        def reachable(root):
            seen, pending = set(), [root]
            while pending:
                name = pending.pop()
                if name not in seen:
                    seen.add(name)
                    pending.extend(refs(schema[name]))
            return seen

        closure = set.union(*(reachable(root) for root in roots))
        family = {name for name in closure if 'EvidenceReference' in reachable(name)}

        def rewrite(value):
            if isinstance(value, dict):
                return {key: ('#/$defs/Agent' + item.rsplit('/', 1)[-1]
                              if key == '$ref' and item.rsplit('/', 1)[-1] in family
                              else rewrite(item)) for key, item in value.items()}
            if isinstance(value, list):
                return [rewrite(item) for item in value]
            return value

        for name in family - {'EvidenceReference'}:
            expected = rewrite(schema[name])
            if name in roots:
                expected['properties']['evidence'] = {'$ref': '#/$defs/RequestEvidenceTable'}
            self.assertEqual(schema['Agent' + name], expected, name)
