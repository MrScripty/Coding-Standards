"""Cold stdio qualification of navigation and rejection feedback, without a model.

Each test uses one server process per purpose and catalog delivery, and replaces
it where a continuation must be honoured by a process that did not issue it. The
existing qualified-snapshot fixture keeps production Git, standards and stores
outside this transport test's write set.
"""
from __future__ import annotations

import json
import unittest

from tools.standards_engine.tests import test_purpose_transport as fixture
from tools.standards_engine.tests.stdio_server import StdioServers
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

    def setUp(self):
        self.servers = StdioServers(client='interaction-fixture')
        self.addCleanup(self.servers.close)

    def call(self, purpose, operation, arguments, *, rejected=False, delivery="eager"):
        # One server process per purpose and catalog delivery serves every call of a test.
        server = self.servers.server(self.root, purpose, '--output-schemas', delivery)
        response = server.call(operation, arguments)
        self.assertNotIn('error', response, response)
        result = response['result']
        self.assertEqual(result['isError'], rejected, result)
        self.assertEqual(json.loads(result['content'][0]['text']), result['structuredContent'])
        return result['structuredContent']

    def replace_server(self, purpose, delivery="eager"):
        """End this purpose's server: its next call is answered by a new process."""
        self.servers.restart(self.root, purpose, '--output-schemas', delivery)

    def test_cold_relationship_repair_and_pages_use_the_same_snapshot(self):
        for purpose in ('application', 'authoring'):
            with self.subTest(purpose=purpose):
                first = self.call(purpose, 'relationship_groups', {'snapshot': self.snapshot, 'limit': 1})
                groups = list(first['items'])
                page = first
                # Cold: a process that did not issue the continuations follows them.
                self.replace_server(purpose)
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
                # Cold: a process that did not route honours the page and explanation continuations.
                self.replace_server(purpose)
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
        # Cold: a process that did not reject the proposal answers its discovery continuation.
        self.replace_server('authoring')
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
