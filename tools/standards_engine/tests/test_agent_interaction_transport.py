"""Cold stdio qualification of navigation and rejection feedback, without a model.

Every call replaces the process. The existing qualified-snapshot fixture keeps
production Git, standards and stores outside this transport test's write set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

from tools.standards_engine.tests import test_purpose_transport as fixture
from tools.standards_engine.tests.test_route_content import known_assertions


class AgentInteractionTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.PurposeTransportTest.setUpClass()
        cls.root = fixture.PurposeTransportTest.root
        cls.snapshot = fixture.PurposeTransportTest.snapshot

    @classmethod
    def tearDownClass(cls):
        fixture.PurposeTransportTest.tearDownClass()

    def call(self, purpose, operation, arguments, *, rejected=False, delivery="eager"):
        messages = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'interaction-fixture', 'version': '1'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
             'params': {'name': operation, 'arguments': arguments}},
        ]
        process = subprocess.run(
            [sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp',
             '--repo-root', str(self.root), '--purpose', purpose,
             '--output-schemas', delivery],
            env={**os.environ, 'PYTHONPATH': str(fixture.ROOT)}, text=True,
            input=''.join(json.dumps(value) + '\n' for value in messages),
            capture_output=True, timeout=90,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, '')
        responses = {item['id']: item for item in map(json.loads, process.stdout.splitlines())}
        self.assertNotIn('error', responses[2], responses[2])
        result = responses[2]['result']
        self.assertEqual(result['isError'], rejected, result)
        self.assertEqual(json.loads(result['content'][0]['text']), result['structuredContent'])
        return result['structuredContent']

    def test_cold_relationship_repair_and_pages_use_the_same_snapshot(self):
        for purpose in ('application', 'authoring'):
            with self.subTest(purpose=purpose):
                first = self.call(purpose, 'relationship_groups', {'snapshot': self.snapshot, 'limit': 1})
                groups = list(first['items'])
                page = first
                while 'next' in page:
                    page = self.call(purpose, 'relationship_groups', page['next'])
                    self.assertEqual(page['snapshot'], self.snapshot)
                    groups.extend(page['items'])
                self.assertEqual(len(groups), first['total'])
                invalid = self.call(purpose, 'related', {
                    'snapshot': self.snapshot, 'target': 'core', 'groups': ['plausible-but-unregistered'],
                    'direction': 'outgoing', 'transitive': False}, rejected=True)
                choices = invalid['relationship_groups']
                self.assertEqual(choices['snapshot'], self.snapshot)
                self.assertIn('standards-requires', [item['id'] for item in groups])
                repaired = self.call(purpose, 'related', {
                    'snapshot': self.snapshot, 'target': 'core', 'groups': ['standards-requires'],
                    'direction': 'outgoing', 'transitive': False})
                self.assertEqual(repaired.get('relationships', repaired.get('related', [])), [])
                if purpose == 'application':
                    self.assertNotIn(fixture.PRIVATE, json.dumps(choices))
                    self.assertNotIn('decision-provenance', [item['id'] for item in groups])

    def test_cold_compact_route_and_full_explanation_keep_uncertainty(self):
        facts = {key: value for key, value in known_assertions().items()
                 if key in ('routing.activities', 'routing.applications')}
        for purpose in ('application', 'authoring'):
            with self.subTest(purpose=purpose):
                route = self.call(purpose, 'route', {'snapshot': self.snapshot, 'facts': facts,
                                                   'content': {'limit': 1}})
                self.assertEqual(len(route['unresolved_questions']), 6)
                self.assertEqual(route['status'], 'needs-facts')
                next_page = self.call(purpose, 'route', route['content']['next'])
                self.assertEqual(next_page['snapshot'], self.snapshot)
                self.assertEqual(next_page['unresolved_questions'], route['unresolved_questions'])
                target = next_page['reading_plan'][1]['target']
                read = self.call(purpose, 'read', {'snapshot': self.snapshot, 'target': target})
                self.assertEqual(next_page['content']['items'][0], read)
                if purpose == 'authoring':
                    full = self.call(purpose, 'route', route['explanation'])
                    self.assertEqual(full['unresolved_questions'], route['unresolved_questions'])
                    self.assertEqual([item for item in full['reading_plan'] if item['state'] == 'selected'],
                                     route['reading_plan'])

    def test_cold_invalid_proposal_has_usable_discovery_continuation(self):
        invalid = self.call('authoring', 'propose', {'change_set': {}}, rejected=True)
        feedback = invalid['input_feedback']
        self.assertEqual({item['instance_pointer'] for item in feedback['issues']},
                         {'/change_set/purpose', '/change_set/edits'})
        described = self.call('authoring', 'describe_input', feedback['describe_input'])
        self.assertEqual(described['root'], 'AgentProposeCall')
        self.assertEqual(described['operation'], 'propose')
        self.assertNotIn('context', invalid)

    def test_on_demand_navigation_and_feedback_preserve_eager_results(self):
        facts = {key: value for key, value in known_assertions().items()
                 if key in ('routing.activities', 'routing.applications')}
        for purpose in ('application', 'authoring'):
            cases = [('read', {'snapshot': self.snapshot, 'target': 'core'}, False),
                     ('route', {'snapshot': self.snapshot, 'facts': facts,
                                'content': {'limit': 2}}, False),
                     ('related', {'snapshot': self.snapshot, 'target': 'core',
                                  'groups': ['unknown-group'], 'direction': 'outgoing',
                                  'transitive': False}, True)]
            for operation, arguments, rejected in cases:
                with self.subTest(purpose=purpose, operation=operation):
                    eager = self.call(purpose, operation, arguments, rejected=rejected)
                    deferred = self.call(purpose, operation, arguments, rejected=rejected,
                                         delivery='on-demand')
                    self.assertEqual(deferred, eager)
        eager = self.call('authoring', 'propose', {'change_set': {}}, rejected=True)
        deferred = self.call('authoring', 'propose', {'change_set': {}}, rejected=True,
                             delivery='on-demand')
        self.assertEqual(deferred, eager)
