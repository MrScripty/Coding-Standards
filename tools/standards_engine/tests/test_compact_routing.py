"""Compact routing preserves selection and uncertainty, not default negatives."""
from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.tests.test_route_content import known_assertions

ROOT = Path(__file__).resolve().parents[3]


class CompactRoutingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = StandardsEngine.open_repository(ROOT, durable=False, purpose='authoring')
        cls.interface = AgentToolFacade.load_interface(ROOT)
        cls.facade = AgentToolFacade(cls.engine, cls.interface)
        cls.snapshot = cls.facade.routing_facts({})['snapshot']

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_two_known_facts_keep_all_six_questions_and_exact_selected_closure(self):
        facts = {k: v for k, v in known_assertions().items() if k in ('routing.activities', 'routing.applications')}
        facts['routing.activities'] = ['implementation']
        compact = self.facade.route({'snapshot': self.snapshot, 'facts': facts})
        full = self.facade.route(compact['explanation'])
        canonical = {key: {'type': 'enum-set', 'state': 'known', 'value': value} for key, value in facts.items()}
        native = self.facade.query({'snapshot': self.snapshot, 'request': {'kind': 'route', 'facts': canonical}})
        self.assertEqual(compact['kind'], 'compact-route-result')
        self.assertEqual(compact['status'], 'needs-facts')
        self.assertEqual(len(compact['unresolved_questions']), 6)
        self.assertEqual(compact['unresolved_questions'], full['unresolved_questions'])
        self.assertEqual(compact['facts'], full['facts'])
        self.assertEqual(compact['reading_plan'], [v for v in native['reading_plan'] if v['state'] == 'selected'])
        self.assertEqual(compact['reading_plan'], [v for v in full['reading_plan'] if v['state'] == 'selected'])
        self.assertEqual(compact['unresolved_policy_count'], len([v for v in full['reading_plan'] if v['state'] != 'selected']))
        self.assertNotIn('rules', compact)
        self.assertLess(len(json.dumps(compact)), len(json.dumps(full)))
        self.interface.validate('CompactRouteResult', compact)

    def test_known_empty_is_distinct_from_unknown(self):
        unknown = self.facade.route({'snapshot': self.snapshot, 'facts': {}})
        empty = self.facade.route({'snapshot': self.snapshot, 'facts': known_assertions()})
        self.assertEqual(unknown['status'], 'needs-facts')
        self.assertEqual(empty['status'], 'complete')
        self.assertEqual(empty['unresolved_questions'], [])
        self.assertEqual(empty['unresolved_policy_count'], 0)
        self.assertEqual(unknown['facts'], {})

    def test_full_explanation_and_content_paging_stay_on_the_original_snapshot(self):
        for detail in ('compact', 'full'):
            first = self.facade.route({'snapshot': self.snapshot, 'facts': known_assertions(),
                                      'detail': detail, 'content': {'limit': 1}})
            second = self.facade.route(first['content']['next'])
            self.assertEqual(first['kind'], second['kind'])
            self.assertEqual(first['snapshot'], second['snapshot'])
            self.assertEqual(first['content']['next']['detail'], detail)
            target = second['reading_plan'][1]['target']
            self.assertEqual(second['content']['items'][0], self.facade.read({'snapshot': self.snapshot, 'target': target}))
        with patch.object(self.engine, '_capture_snapshot', side_effect=AssertionError('capture')):
            compact = self.facade.route({'snapshot': self.snapshot, 'facts': {}})
            self.assertEqual(self.facade.route(compact['explanation'])['snapshot'], self.snapshot)

    def test_compact_path_does_not_build_full_rule_expressions(self):
        compiled = self.engine._compiled_snapshot(self.engine._snapshot_id(c.SnapshotHandle.from_value(self.snapshot)))
        program_type = type(compiled.router.rules[0].program)
        with patch.object(self.engine, '_compiled_snapshot', return_value=compiled), \
             patch.object(program_type, 'as_expression', side_effect=AssertionError('full explanation built')):
            value = self.facade.route({'snapshot': self.snapshot, 'facts': {}})
        self.assertEqual(value['kind'], 'compact-route-result')
