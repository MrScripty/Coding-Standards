"""Typed routing values retain the existing final-context projection semantics."""
from __future__ import annotations

from copy import deepcopy
import json
import tomllib
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import logical_authoring as logical
from tools.standards_engine.standards_engine.engine import StandardsEngine
from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_analysis.standards_analysis import AnalysisError
from tools.standards_engine.tests import test_logical_authoring as fixtures


class TypedRoutingProjectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures.LogicalAuthoringTests.setUpClass()
        cls.fixture = fixtures.LogicalAuthoringTests()
        cls.base = cls.fixture.base
        cls.paths = cls.fixture.repository_paths
        cls.router = tomllib.loads(dict(cls.base.files)['evaluation/standards-effectiveness/router-projection.toml'].decode())

    def fact(self):
        return {'id': 'routing.typed-projection', 'semantic_revision': 1, 'type': 'enum-set',
                'nullable': False, 'values': ['z', 'a'], 'aliases': ['routing.typed-projection-alias'],
                'meaning': 'Synthetic typed routing.', 'prompt': 'Which synthetic route?'}

    def put_fact(self, fact):
        return {'kind': 'put-routing-fact', 'fact': fact, 'rationale': 'Explicit synthetic fact edit.'}

    def put_rule(self, rule):
        return {'kind': 'put-routing-rule', 'rule': rule, 'rationale': 'Explicit synthetic rule edit.'}

    def rule(self):
        return {**self.router['rules'][0], 'condition': 'The synthetic condition applies.'}

    def compile(self, changes, predecessor=None):
        return logical.LogicalAuthoringCompiler(StandardsEngine._compile).compile(
            self.base, logical.LogicalProgram(changes), base_repository_paths=self.paths,
            predecessor=predecessor)

    def test_typed_fact_and_rule_resolve_in_same_atomic_context(self):
        fact = self.fact()
        rule = self.rule()
        rule['when'] = {'operator': 'contains', 'fact': fact['id'], 'value': 'z'}
        change = self.fixture.change_set([self.put_rule(rule), self.put_fact(fact)])
        projected = self.compile([change])
        self.assertEqual(next(r for r in projected.compiled.router.rules if r.id == rule['id']).program.referenced_facts,
                         (fact['id'],))
        self.assertEqual(projected.analysis_module_ids, ('router',))
        records = tomllib.loads(dict(projected.source.files)['evaluation/standards-effectiveness/router-projection.toml'].decode())
        self.assertEqual(next(f for f in records['facts'] if f['id'] == fact['id'])['values'], ['z', 'a'])
        self.assertIn(rule['condition'], dict(projected.source.files)['STANDARDS-ROUTER.md'].decode())
        self.fixture.assert_suite_input_projection_is_canonical(projected)

    def test_incremental_and_full_replay_have_exact_files_and_analysis(self):
        fact, rule = self.fact(), self.rule()
        rule['when'] = {'operator': 'contains', 'fact': fact['id'], 'value': 'z'}
        first = self.fixture.change_set([self.put_fact(fact), self.put_rule(rule)])
        second = self.fixture.change_set([self.put_rule(self.rule()),
            {'kind': 'remove-routing-fact', 'fact': fact['id'], 'rationale': 'Remove unused synthetic fact.'}])
        prefix = self.compile([first])
        frozen_prefix = prefix.source.files
        suffix = self.compile([first, second], predecessor=prefix)
        full = self.compile([first, second])
        self.assertEqual(suffix.source.files, full.source.files)
        self.assertEqual(suffix.semantic_proposals, full.semantic_proposals)
        self.assertEqual(suffix.analysis_policy_ids, full.analysis_policy_ids)
        self.assertEqual(suffix.analysis_module_ids, full.analysis_module_ids)
        self.assertEqual(suffix.repository_paths, full.repository_paths)
        self.assertEqual(prefix.source.files, frozen_prefix)
        self.assertNotIn(fact['id'], {f.id for f in suffix.compiled.router.facts})

    def test_shape_normalization_does_not_compile_or_reject_unbound_references(self):
        rule = self.rule(); rule['when'] = {'operator': 'exists', 'fact': 'routing.unbound-typed'}
        with patch.object(logical, 'compile_fact_schema', side_effect=AssertionError('early fact compile')):
            change = self.fixture.change_set([self.put_rule(rule)])
        original = self.base.files
        with self.assertRaises(AnalysisError):
            self.compile([change])
        self.assertEqual(self.base.files, original)

    def test_fact_semantic_revision_and_invalid_type_still_fail_at_projection(self):
        fact = {key: self.router['facts'][0][key] for key in self.fact()}
        fact['meaning'] += ' Changed meaning.'
        parsed = self.fixture.change_set([self.put_fact(fact)])
        with self.assertRaises(AuthoringError) as caught:
            self.compile([parsed])
        self.assertEqual(caught.exception.failure.code, 'AUTHORING.INVALID_SEMANTIC_REVISION')
        bad = self.fact(); bad['type'] = 'unknown-type'
        parsed = self.fixture.change_set([self.put_fact(bad)])
        with self.assertRaises(AnalysisError):
            self.compile([parsed])

    def test_typed_edits_and_nonrouting_edits_keep_their_projection_order(self):
        standard = self.fixture.new_standard_edit()
        fact = self.fact()
        rule = {'id': 'route.typed-projection', 'target': standard['standard']['id'],
                'when': {'operator': 'contains', 'fact': fact['id'], 'value': 'z'},
                'condition': 'The typed pilot requires this new standard.'}
        first = self.compile([self.fixture.change_set([self.put_rule(rule), standard, self.put_fact(fact)])])
        second = self.compile([self.fixture.change_set([self.put_fact(fact), self.put_rule(rule), standard])])
        self.assertEqual(first.source.files, second.source.files)
        self.assertEqual(set(first.analysis_module_ids), {'router', standard['standard']['id']})
        self.fixture.assert_suite_input_projection_is_canonical(first)

    def test_duplicate_targets_and_used_fact_removal_keep_typed_failure(self):
        rule = self.rule(); rule['target'] = self.router['rules'][1]['target']
        with self.assertRaises(AuthoringError) as error:
            self.compile([self.fixture.change_set([self.put_rule(rule)])])
        self.assertEqual(error.exception.failure.code, 'AUTHORING.DUPLICATE_ROUTE_TARGET')
        with self.assertRaises(AnalysisError):
            self.compile([self.fixture.change_set([{'kind':'remove-routing-fact',
                'fact':self.router['facts'][0]['id'],'rationale':'Remove referenced field.'}])])
