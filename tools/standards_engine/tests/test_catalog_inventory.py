from pathlib import Path
import json
import unittest

from tools.standards_engine.tests.catalog_inventory import measure_catalog
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog

ROOT = Path(__file__).resolve().parents[3]


class CatalogInventoryTest(unittest.TestCase):
    def test_counts_are_explicit_about_characters_bytes_and_framing(self):
        tools = [{'name': 'test', 'description': 'é', 'inputSchema': {'type': 'object'}}]
        report = measure_catalog(tools)
        self.assertEqual(report['description_characters'], 1)
        self.assertEqual(report['description_utf8_bytes'], 2)
        self.assertEqual(report['serialized_catalog_json_bytes'], len(json.dumps(tools).encode()))
        self.assertEqual(report, measure_catalog({'jsonrpc': '2.0', 'id': 1, 'result': {'tools': tools}}))
        self.assertEqual(report['output_schema_json_bytes'], 0)

    def test_native_omits_embedded_fallback_and_application_stays_focused(self):
        interface = AgentToolFacade.load_interface(ROOT)
        compatible = tool_catalog(interface, purpose='authoring')
        native = tool_catalog(interface, purpose='authoring', schema_mode='native')
        application = tool_catalog(interface, purpose='application', schema_mode='native')
        self.assertGreater(measure_catalog(compatible)['description_characters'],
                           measure_catalog(native)['description_characters'] * 3)
        self.assertFalse(any('```json' in t['description'] for t in native))
        self.assertTrue(any('```json' in t['description'] for t in compatible))
        self.assertNotIn('propose', {t['name'] for t in application})
        self.assertIn('relationship_groups', {t['name'] for t in application})

    def test_unknown_host_renderings_and_duplicate_names_are_not_guessed(self):
        for value in ({'data': 'host-rendered'}, [{'name': 'test'}],
                      [{'name': 'a', 'inputSchema': {}}] * 2):
            with self.assertRaises(ValueError):
                measure_catalog(value)
