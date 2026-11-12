"""Routed exact content across review labels, paging and lifecycle boundaries."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import agent_navigation
from tools.standards_engine.standards_engine.mcp import MCPServer
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.tests.test_mcp import initialize, request
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

    def test_unapproved_later_target_is_delivered_with_its_label_on_its_own_page(self):
        facts = known_assertions()
        facts['routing.activities'] = ['implementation']
        value = self.route(self.app, facts=facts, content={'limit': 1})
        self.assertEqual(value['kind'], 'application-route-result', value)
        labels = {entry['target']: entry['review_state'] for entry in value['reading_plan']}
        self.assertEqual(labels['workflow.implementation'], 'not-reviewed')
        items = list(value['content']['items'])
        while 'next' in value['content']:
            value = self.app.route(value['content']['next'])
            items.extend(value['content']['items'])
        self.assertEqual({item['policy']['id']: item['review_state'] for item in items}, labels)
        self.assertEqual(items, [self.app.read({'snapshot': self.snapshot, 'target': target}) for target in labels])
        self.assertNotIn(fixture.PRIVATE, json.dumps(items))

    def test_exact_byte_limit_partial_pages_and_oversized_record(self):
        for facade in (self.author, self.app):
            application = facade is self.app

            def budget(size):
                # Authoring pages keep the transport bound; application pages use the host budget.
                return (patch.object(facade._engine, '_route_page_bytes', size) if application
                        else patch.object(agent_navigation, 'ROUTE_CONTENT_RESULT_BYTES', size))

            first = self.route(facade, content={'limit': 1})
            full = self.route(facade, content={'limit': 2})
            full_bytes = len(json.dumps(full).encode('utf-8'))
            with budget(full_bytes):
                self.assertEqual(self.route(facade, content={'limit': 2}), full)
            first_bytes = len(json.dumps(first).encode('utf-8'))
            self.assertLess(first_bytes, full_bytes)
            with budget(first_bytes):
                partial = self.route(facade, content={'limit': 2})
                self.assertEqual(partial['content']['items'], first['content']['items'])
                self.assertEqual(partial['content']['next']['content']['offset'], 1)
                self.assertLessEqual(len(json.dumps(partial).encode('utf-8')), first_bytes)
            with budget(1):
                oversized = self.route(facade)
            if application:
                # One whole item is returned alone rather than rejected or clipped.
                self.assertEqual(oversized['content']['items'], first['content']['items'])
                self.assertEqual(oversized['content']['next']['content'], {'offset': 1, 'limit': 8})
                with budget(1):
                    last = self.app.route(oversized['content']['next'])
                self.assertEqual(first['content']['items'] + last['content']['items'], full['content']['items'])
                self.assertNotIn('next', last['content'])
            with patch.object(agent_navigation, 'ROUTE_CONTENT_RESULT_BYTES', 1):
                rejected = self.route(facade)
            self.assertEqual(rejected['outcome'], 'unsupported')
            self.assertNotIn('content', rejected)
            if not application:
                self.assertEqual(oversized, rejected)
            # The explicit non-composed operation remains available.
            self.assertIn('reading_plan', facade.route({'snapshot': self.snapshot, 'facts': known_assertions()}))

    def test_application_page_budget_default_and_host_configuration(self):
        self.assertEqual(agent_navigation.ROUTE_PAGE_BYTES, 40 * 1024)
        self.assertEqual(self.app._engine.route_page_bytes, agent_navigation.ROUTE_PAGE_BYTES)
        # The default holds both fixture items; each returned page stays within it.
        default = self.route(self.app)
        self.assertEqual(len(default['content']['items']), 2)
        self.assertLessEqual(len(json.dumps(default).encode('utf-8')), agent_navigation.ROUTE_PAGE_BYTES)
        first = self.route(self.app, content={'limit': 1})
        configured = len(json.dumps(first).encode('utf-8'))
        self.assertGreaterEqual(configured, agent_navigation.ROUTE_PAGE_MIN_BYTES)
        with StandardsEngine.open_repository(
                ROOT, purpose='application', store_path=fixture.PurposeProjectionTest.store_path,
                route_page_bytes=configured) as engine:
            self.assertEqual(engine.route_page_bytes, configured)
            page = self.route(AgentToolFacade(engine, _contracts(ROOT)))
        self.assertEqual(page, {**first, 'content': {**first['content'], 'next': {
            **first['content']['next'], 'content': {'offset': 1, 'limit': 8}}}})
        # The same budget never shortens an authoring page.
        with StandardsEngine.open_repository(
                ROOT, purpose='authoring', store_path=fixture.PurposeProjectionTest.store_path,
                route_page_bytes=agent_navigation.ROUTE_PAGE_MIN_BYTES) as engine:
            self.assertEqual(self.route(AgentToolFacade(engine, _contracts(ROOT))), self.route(self.author))

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


class RoutePageBudgetOptionTest(unittest.TestCase):
    def test_budget_range_is_closed_and_whole(self):
        admit = agent_navigation.admit_route_page_bytes
        self.assertEqual(admit(None), agent_navigation.ROUTE_PAGE_BYTES)
        for value in (agent_navigation.ROUTE_PAGE_MIN_BYTES, 50_000, agent_navigation.ROUTE_CONTENT_RESULT_BYTES):
            self.assertEqual(admit(value), value)
        for value in (0, -1, agent_navigation.ROUTE_PAGE_MIN_BYTES - 1,
                      agent_navigation.ROUTE_CONTENT_RESULT_BYTES + 1, True, 40960.0, '40960'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                admit(value)
        with self.assertRaises(ValueError):
            MCPServer(ROOT, purpose='application', route_page_bytes=1)

    def test_server_passes_its_budget_to_every_call(self):
        for configured in (None, 50_000):
            server = MCPServer(ROOT, purpose='application', route_page_bytes=configured)
            self.addCleanup(server.close)
            initialize(server)
            with patch.object(AgentToolFacade, 'open_repository') as opened:
                opened.return_value.__enter__.return_value.route.return_value = {'kind': 'fixture'}
                server.dispatch(request('tools/call', {'name': 'route', 'arguments': {'facts': {}}}))
            self.assertEqual(opened.call_args.kwargs['route_page_bytes'],
                             configured or agent_navigation.ROUTE_PAGE_BYTES)

    def test_launch_option_is_validated_before_serving(self):
        def launch(*arguments):
            return subprocess.run(
                [sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp', '--no-observe',
                 '--repo-root', str(ROOT), *arguments],
                input='', text=True, capture_output=True, env={**os.environ, 'PYTHONPATH': str(ROOT)}, timeout=90)
        accepted = launch('--purpose', 'application', '--route-page-bytes', '50000')
        self.assertEqual((accepted.returncode, accepted.stdout, accepted.stderr), (0, '', ''))
        for purpose, value, reason in (('application', '100', 'from 8192 to 2097152'),
                                       ('application', '9999999', 'from 8192 to 2097152'),
                                       ('application', 'large', 'invalid int value'),
                                       ('authoring', '50000', 'applies to the application purpose')):
            with self.subTest(purpose=purpose, value=value):
                refused = launch('--purpose', purpose, '--route-page-bytes', value)
                self.assertEqual(refused.returncode, 2)
                self.assertEqual(refused.stdout, '')
                self.assertIn(reason, refused.stderr)
