"""Canonical routing records are domain data, not a navigation rendering choice."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import json
import tomllib
import unittest

from tools.standards_analysis.standards_analysis import RouterProjection, load_router_projection
from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_metadata.standards_metadata import load_canonical_module_corpus

ROOT = Path(__file__).resolve().parents[3]


class CanonicalRoutingRecordsTest(unittest.TestCase):
    def test_exact_fields_empty_values_aliases_and_record_order(self):
        schema = compile_fact_schema({
            'kind': 'applicability-fact-schema', 'id': 'routing.records.fixture', 'version': 2,
            'facts': [{
                'id': 'routing.enabled', 'semantic_revision': 1, 'type': 'boolean',
                'nullable': False, 'values': [], 'aliases': ['routing.old-enabled'],
                'meaning': 'A known enabled state.', 'prompt': 'Is it enabled?',
                'context_kind': 'task-route', 'answer_contract': 'fact-value.v1',
                'evidence_contract': 'evidence-reference.v1',
                'authorization_capability': 'standards.analyze',
            }],
        })
        projection = RouterProjection('fixture', 'router', 'STANDARDS-ROUTER.md',
                                      ('router',), schema.definitions, (), schema)
        # The literal is the established eight-field contract, not copied from
        # the implementation's projection or the wider FactContract serializer.
        expected = [{'id': 'routing.enabled', 'semantic_revision': 1, 'type': 'boolean',
                     'nullable': False, 'values': [], 'aliases': ['routing.old-enabled'],
                     'meaning': 'A known enabled state.', 'prompt': 'Is it enabled?'}]
        self.assertEqual(projection.fact_definitions(), expected)
        self.assertEqual(json.dumps(projection.fact_definitions()), json.dumps(expected))
        self.assertNotIn('values', schema.definitions[0].semantic_projection())
        self.assertNotEqual(projection.fact_definitions()[0], schema.definitions[0].as_contract())

    def test_repository_records_preserve_canonical_normalization_and_order(self):
        projection = load_router_projection(ROOT, load_canonical_module_corpus(ROOT))
        raw = tomllib.loads((ROOT/'evaluation/standards-effectiveness/router-projection.toml').read_text())
        fields = ('id', 'semantic_revision', 'type', 'nullable', 'values', 'aliases', 'meaning', 'prompt')
        expected = [{key: sorted(fact[key]) if key in ('values', 'aliases') else fact[key]
                     for key in fields} for fact in sorted(raw['facts'], key=lambda f: f['id'])]
        self.assertEqual(json.dumps(projection.fact_definitions()), json.dumps(expected))
        reversed_projection = replace(projection, facts=tuple(reversed(projection.facts)))
        self.assertEqual(reversed_projection.fact_definitions(), list(reversed(expected)))

    def test_returned_records_do_not_mutate_the_canonical_projection(self):
        projection = load_router_projection(ROOT, load_canonical_module_corpus(ROOT))
        expected = projection.fact_definitions()
        changed = projection.fact_definitions()
        changed.reverse()
        changed[0]['meaning'] = 'presentation only'
        changed[0]['values'].append('not-a-domain-value')
        changed[0]['aliases'].append('not-a-domain-alias')
        self.assertEqual(projection.fact_definitions(), expected)
