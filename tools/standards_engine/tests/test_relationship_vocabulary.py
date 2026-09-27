"""Registered vocabulary is exact, paged and purpose-qualified, not inferred."""
from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import relationship_vocabulary as vocabulary
from tools.standards_engine.standards_engine.context_projection import ApplicationView
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.tests import test_purpose_projection as fixture
from tools.standards_snapshots.standards_snapshots import SnapshotId

ROOT = Path(__file__).resolve().parents[3]


class RelationshipVocabularyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeProjectionTest.setUpClass()
        cls.app = fixture.PurposeProjectionTest.facade
        cls.snapshot = cls.app_snapshot = fixture.PurposeProjectionTest.snapshot
        cls.author_engine = StandardsEngine.open_repository(ROOT, purpose='authoring',
                                        store_path=fixture.PurposeProjectionTest.store_path)
        cls.author = AgentToolFacade(cls.author_engine, AgentToolFacade.load_interface(ROOT))

    @classmethod
    def tearDownClass(cls):
        cls.author_engine.close()
        fixture.PurposeProjectionTest.tearDownClass()

    def page(self, facade, **arguments):
        return facade.relationship_groups({'snapshot': self.snapshot, **arguments})

    def test_pages_match_graph_records_and_only_permitted_application_groups(self):
        for facade in (self.author, self.app):
            graph = fixture.PurposeProjectionTest.compiled.graph if facade is self.author else ApplicationView(
                fixture.PurposeProjectionTest.compiled, c.SnapshotHandle.from_value(self.snapshot)).graph
            expected = [{'id': g.id, 'description': g.purpose,
                         'traversal_directions': sorted(v.value for v in g.traversal.directions),
                         'transitive': g.traversal.transitive}
                        for g in sorted(graph.groups.values(), key=lambda g: g.id)]
            items = []
            args = {'snapshot': self.snapshot, 'limit': 1}
            while True:
                result = facade.relationship_groups(args)
                self.assertEqual(result['offset'], len(items))
                self.assertEqual(result['snapshot'], self.snapshot)
                self.assertEqual(result['total'], len(expected))
                items.extend(result['items'])
                if 'next' not in result:
                    break
                args = result['next']
            self.assertEqual(items, expected)
            if facade is self.app:
                self.assertNotIn('decision-provenance', json.dumps(items))
                self.assertNotIn(fixture.PRIVATE, json.dumps(items))
            else:
                self.assertIn('decision-provenance', [i['id'] for i in items])

    def test_unknown_query_offers_same_first_page_and_choices_repair_it(self):
        for facade in (self.author, self.app):
            arguments = {'snapshot': self.snapshot, 'target': 'core', 'groups': ['plausible-but-invalid'],
                         'direction': 'outgoing', 'transitive': False}
            rejected = facade.related(arguments)
            self.assertEqual(rejected['outcome'], 'invalid')
            self.assertEqual(rejected['code'], 'GRAPH.UNKNOWN_GROUP' if facade is self.author else 'APPLICATION.UNKNOWN_GROUP')
            self.assertEqual(rejected['relationship_groups'], self.page(facade))
            chosen = next(i['id'] for i in rejected['relationship_groups']['items'] if i['id'] == 'standards-requires')
            success = facade.related({**arguments, 'groups': [chosen]})
            self.assertEqual(success['relationships'], [])  # Registered but empty remains success.
            self.assertNotIn('relationship_groups', success)
            self.assertNotIn('code', success)

    def test_hidden_target_is_not_a_way_to_read_private_application_groups(self):
        result = self.app.related({'snapshot': self.snapshot, 'target': 'provenance.fixture',
                                  'groups': ['decision-provenance'], 'direction': 'outgoing', 'transitive': False})
        self.assertEqual(result['code'], 'APPLICATION.CONTENT_UNAVAILABLE')
        self.assertNotIn('relationship_groups', result)
        self.assertNotIn(fixture.PRIVATE, json.dumps(result))

    def test_byte_bounds_whole_records_and_numeric_equivalence(self):
        for facade in (self.author, self.app):
            first = self.page(facade, limit=1)
            full = self.page(facade, limit=2)
            full_size = len(json.dumps(full).encode())
            with patch.object(vocabulary, 'GROUP_PAGE_BYTES', full_size):
                self.assertEqual(self.page(facade, limit=2), full)
            with patch.object(vocabulary, 'GROUP_PAGE_BYTES', len(json.dumps(first).encode())):
                partial = self.page(facade, limit=2)
                self.assertEqual(partial['items'], first['items'])
                self.assertEqual(partial['next']['offset'], 1)
            with patch.object(vocabulary, 'GROUP_PAGE_BYTES', 1):
                self.assertEqual(self.page(facade)['outcome'], 'unsupported')
            self.assertEqual(self.page(facade, offset=1.0, limit=1.0), self.page(facade, offset=1, limit=1))
            for args in ({'limit': 0}, {'limit': 33}, {'offset': -1}, {'offset': 0.5}, {'limit': True}, {'offset': 999}):
                self.assertEqual(self.page(facade, **args)['outcome'], 'invalid')
            final = self.page(facade, offset=first['total'])
            self.assertEqual(final['items'], [])
            self.assertNotIn('next', final)

    def test_one_compile_and_no_unanchored_continuation_capture(self):
        for facade in (self.author, self.app):
            engine = facade._engine
            with patch.object(engine, '_compiled_snapshot', wraps=engine._compiled_snapshot) as compiled:
                self.page(facade)
                self.assertEqual(compiled.call_count, 1)
            with patch.object(engine, '_capture_snapshot', side_effect=AssertionError('ambient capture')):
                self.assertEqual(facade.relationship_groups({'offset': 1})['outcome'], 'invalid')

    def test_cold_continuation_and_deleted_snapshot(self):
        first = self.page(self.author, limit=1)
        expected = self.author.relationship_groups(first['next'])
        with StandardsEngine.open_repository(ROOT, purpose='authoring',
                                            store_path=fixture.PurposeProjectionTest.store_path) as engine:
            actual = AgentToolFacade(engine, AgentToolFacade.load_interface(ROOT)).relationship_groups(first['next'])
            self.assertEqual(actual, expected)
        sid = SnapshotId(self.snapshot['id'])
        self.author_engine._snapshots.delete_snapshot(sid)
        try:
            for facade in (self.author, self.app):
                result = self.page(facade)
                self.assertIn('rejected', result['kind'])
                self.assertNotIn('items', result)
        finally:
            self.author_engine._snapshots.undelete_snapshot(sid)

    def test_final_lifecycle_failure_discards_the_vocabulary(self):
        engine = self.author_engine
        compiled = engine._compiled_snapshot(engine._snapshot_id(c.SnapshotHandle.from_value(self.snapshot)))
        original = engine._snapshots.snapshot
        count = 0
        def observe(identity):
            nonlocal count
            count += 1
            if count == 2:
                engine._snapshots.delete_snapshot(identity)
            return original(identity)
        try:
            with patch.object(engine, '_compiled_snapshot', return_value=compiled), \
                 patch.object(engine._snapshots, 'snapshot', side_effect=observe):
                result = self.page(self.author)
            self.assertIn('rejected', result['kind'])
            self.assertNotIn('items', result)
        finally:
            engine._snapshots.undelete_snapshot(SnapshotId(self.snapshot['id']))
