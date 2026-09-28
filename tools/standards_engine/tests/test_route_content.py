"""Routed exact content across qualification, paging and lifecycle boundaries."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import agent_navigation
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.tests import test_purpose_projection as fixture
from tools.standards_snapshots.standards_snapshots import SnapshotId

ROOT = Path(__file__).resolve().parents[3]


def known_facts():
    return {'routing.' + key: {'type': 'enum-set', 'state': 'known', 'value': []}
            for key in ('activities', 'workflow-profiles', 'applications', 'boundaries',
                        'languages', 'frameworks', 'topics', 'details')}


def known_assertions():
    """Focused inputs; known_facts intentionally remains a canonical-query fixture."""
    return {'routing.' + key: [] for key in (
        'activities', 'workflow-profiles', 'applications', 'boundaries',
        'languages', 'frameworks', 'topics', 'details')}


class RouteContentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeProjectionTest.setUpClass()
        cls.app = fixture.PurposeProjectionTest.facade
        cls.snapshot = fixture.PurposeProjectionTest.snapshot
        cls.author_engine = StandardsEngine.open_repository(
            ROOT, purpose='authoring', store_path=fixture.PurposeProjectionTest.store_path)
        cls.author = AgentToolFacade(cls.author_engine, _contracts(ROOT))

    @classmethod
    def tearDownClass(cls):
        cls.author_engine.close()
        fixture.PurposeProjectionTest.tearDownClass()

    def route(self, facade, **extra):
        return facade.route({'snapshot': self.snapshot, 'facts': known_assertions(), 'content': {}, **extra})

    def test_pages_equal_exact_reads_and_preserve_unknown_facts(self):
        for facade in (self.author, self.app):
            for facts in ({}, known_assertions()):
                plain = facade.route({'snapshot': self.snapshot, 'facts': facts})
                targets = list(dict.fromkeys(i['target'] for i in plain['reading_plan'] if i['state'] == 'selected'))
                expected = [facade.read({'snapshot': self.snapshot, 'target': t}) for t in targets]
                arguments = {'snapshot': self.snapshot, 'facts': facts, 'content': {'limit': 1}}
                original = deepcopy(arguments)
                items = []
                while True:
                    value = facade.route(arguments)
                    self.assertEqual(value['snapshot'], self.snapshot)
                    self.assertEqual(value['reading_plan'], plain['reading_plan'])
                    self.assertEqual(value['unresolved_questions'], plain['unresolved_questions'])
                    if facade is self.app:
                        self.assertEqual(value['status'], plain['status'])
                        self.assertNotIn(fixture.PRIVATE, json.dumps(value))
                    page = value['content']
                    self.assertEqual(page['offset'], len(items))
                    self.assertEqual(page['total'], len(targets))
                    items.extend(page['items'])
                    if 'next' not in page:
                        break
                    arguments = page['next']
                    self.assertEqual(arguments['facts'], facts)
                self.assertEqual(items, expected)
                self.assertEqual(original, {'snapshot': self.snapshot, 'facts': facts, 'content': {'limit': 1}})
                self.assertEqual(value['next_operations'], [])

    def test_one_verified_input_and_no_capture_for_each_composed_call(self):
        for facade in (self.author, self.app):
            engine = facade._engine
            with patch.object(engine, '_compiled_snapshot', wraps=engine._compiled_snapshot) as compiled, \
                 patch.object(engine._snapshots, 'load_content', wraps=engine._snapshots.load_content) as load, \
                 patch.object(engine, '_capture_snapshot', side_effect=AssertionError('ambient capture')):
                value = self.route(facade)
            self.assertEqual(len(value['content']['items']), 2)
            self.assertEqual(compiled.call_count, 1)
            self.assertEqual(load.call_count, 1)

    def test_unqualified_later_target_blocks_even_a_one_item_application_page(self):
        facts = known_assertions()
        facts['routing.activities'] = ['implementation']
        value = self.route(self.app, facts=facts, content={'limit': 1})
        self.assertEqual(value['code'], 'APPLICATION.CONTENT_UNAVAILABLE')
        self.assertNotIn('content', value)
        self.assertNotIn(fixture.PRIVATE, json.dumps(value))

    def test_exact_byte_limit_partial_pages_and_oversized_record(self):
        for facade in (self.author, self.app):
            first = self.route(facade, content={'limit': 1})
            full = self.route(facade, content={'limit': 2})
            full_bytes = len(json.dumps(full).encode('utf-8'))
            with patch.object(agent_navigation, 'ROUTE_CONTENT_RESULT_BYTES', full_bytes):
                self.assertEqual(self.route(facade, content={'limit': 2}), full)
            first_bytes = len(json.dumps(first).encode('utf-8'))
            self.assertLess(first_bytes, full_bytes)
            with patch.object(agent_navigation, 'ROUTE_CONTENT_RESULT_BYTES', first_bytes):
                partial = self.route(facade, content={'limit': 2})
                self.assertEqual(partial['content']['items'], first['content']['items'])
                self.assertEqual(partial['content']['next']['content']['offset'], 1)
                self.assertLessEqual(len(json.dumps(partial).encode('utf-8')), first_bytes)
            with patch.object(agent_navigation, 'ROUTE_CONTENT_RESULT_BYTES', 1):
                rejected = self.route(facade)
            self.assertEqual(rejected['outcome'], 'unsupported')
            self.assertNotIn('content', rejected)
            # The explicit non-composed operation remains available.
            self.assertIn('reading_plan', facade.route({'snapshot': self.snapshot, 'facts': known_assertions()}))

    def test_schema_whole_numbers_normalize_before_slicing(self):
        for facade in (self.author, self.app):
            for offset in (0, 1):
                expected = self.route(facade, content={"offset": offset, "limit": 1})
                self.assertEqual(self.route(facade, content={"offset": float(offset), "limit": 1.0}),
                                 expected)
            for content in ({"offset": 0.5}, {"limit": 1.5}):
                self.assertEqual(self.route(facade, content=content)["outcome"], "invalid")

    def test_invalid_selections_reject_and_nonzero_offsets_never_capture(self):
        for facade in (self.author, self.app):
            engine = facade._engine
            for content in ({'limit': 0}, {'limit': 33}, {'limit': True}, {'offset': -1},
                            {'offset': '1'}, {'unknown': True}, {'offset': 999}):
                with self.subTest(purpose=engine.purpose, selection=content):
                    value = self.route(facade, content=content)
                    self.assertEqual(value['outcome'], 'invalid', value)
            with patch.object(engine, '_capture_snapshot', side_effect=AssertionError('capture')):
                value = facade.route({'facts': {}, 'content': {'offset': 1}})
            self.assertEqual(value['outcome'], 'invalid')
            ended = self.route(facade, content={'offset': 2})
            self.assertEqual(ended['content'], {'offset': 2, 'total': 2, 'items': []})

    def test_midpage_or_final_lifecycle_loss_discards_all_items(self):
        for facade in (self.author, self.app):
            engine = facade._engine
            for at in (1, 2):
                ordinary = agent_navigation.read_selected_item
                calls = 0

                def read(*args, **kwargs):
                    nonlocal calls
                    value = ordinary(*args, **kwargs)
                    calls += 1
                    if calls == at:
                        engine._snapshots.delete_snapshot(SnapshotId(self.snapshot['id']))
                    return value

                try:
                    with patch.object(agent_navigation, 'read_selected_item', side_effect=read):
                        value = self.route(facade)
                    self.assertIn('rejected', value['kind'])
                    self.assertNotIn('content', value)
                finally:
                    engine._snapshots.undelete_snapshot(SnapshotId(self.snapshot['id']))

    def test_continuation_reopens_without_process_state(self):
        first = self.route(self.author, content={'limit': 1})
        expected = self.author.route(first['content']['next'])
        with StandardsEngine.open_repository(ROOT, purpose='authoring',
                                            store_path=fixture.PurposeProjectionTest.store_path) as engine:
            self.assertEqual(AgentToolFacade(engine, _contracts(ROOT)).route(first['content']['next']), expected)

    def test_source_projection_failure_returns_no_successful_prefix(self):
        original = self.author_engine._read
        calls = 0

        def read(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                return self.author_engine._reject('FIXTURE.READ_UNAVAILABLE', 'unavailable', 'Fixture read unavailable.')
            return original(*args, **kwargs)

        with patch.object(self.author_engine, '_read', side_effect=read):
            value = self.route(self.author)
        self.assertEqual(value['code'], 'FIXTURE.READ_UNAVAILABLE')
        self.assertNotIn('content', value)
