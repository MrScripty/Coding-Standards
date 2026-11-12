"""The shared server helper still fails a test for everything the per-call launches did."""
from __future__ import annotations

import unittest

from tools.standards_engine.tests.stdio_server import StdioServer, StdioServers
from tools.standards_engine.tests.test_mcp import ROOT, installation_root


def instance(server):
    return server.initialized['result']['_meta']['standards-engine/runtime']['instance_id']


class StdioServerTest(unittest.TestCase):
    def test_one_process_answers_every_call_and_exits_cleanly(self):
        server = StdioServer(installation_root(self), purpose='application', client='helper-test')
        self.addCleanup(server.close)
        self.assertEqual(server.exchange('ping')['result'], {})
        results = [server.call('runtime_info', {})['result'] for _ in range(2)]
        self.assertEqual([result['structuredContent']['instance_id'] for result in results], [instance(server)] * 2)
        self.assertEqual(server.close(), '')
        self.assertEqual(server._process.returncode, 0)
        self.assertEqual(server.close(), '', 'closing again is harmless')

    def test_stderr_fails_the_call_that_caused_it_unless_the_test_expects_it(self):
        root = installation_root(self)
        store = root / '.standards-engine/snapshots-v1.sqlite3'
        store.parent.mkdir()
        store.write_bytes(b'not a database')
        server = StdioServer(root, purpose='authoring')
        with self.assertRaisesRegex(AssertionError, 'wrote to stderr during tools/call'):
            server.call('read', {'target': 'core'})
        with self.assertRaisesRegex(AssertionError, 'wrote to stderr'):
            server.close()
        expected = StdioServer(root, purpose='authoring', silent=False)
        self.assertTrue(expected.call('read', {'target': 'core'})['result']['isError'])
        self.assertIn('Traceback', expected.close())

    def test_a_process_that_ends_early_fails_with_its_diagnostics(self):
        with self.assertRaisesRegex(AssertionError, "exited before answering initialize: (?s:.*)invalid choice: 'neither'"):
            StdioServer(ROOT, purpose='neither')
        server = StdioServer(installation_root(self), purpose='application')
        server._process.kill()
        server._process.wait()
        with self.assertRaises(AssertionError):
            server.exchange('ping')
        with self.assertRaisesRegex(AssertionError, 'exited with status'):
            server.close()

    def test_one_process_per_launch_until_restart_and_close_ends_them_all(self):
        root = installation_root(self)
        servers = StdioServers(client='helper-test')
        self.addCleanup(servers.close)
        first = servers.server(root, 'application')
        self.assertIs(servers.server(root, 'application'), first)
        other = servers.server(root, 'application', '--output-schemas', 'on-demand')
        self.assertNotEqual(instance(other), instance(first))
        servers.restart(root, 'application')
        self.assertEqual(first._process.returncode, 0)
        replacement = servers.server(root, 'application')
        self.assertNotEqual(instance(replacement), instance(first))
        servers.close()
        self.assertEqual([server._process.returncode for server in (other, replacement)], [0, 0])


if __name__ == '__main__':
    unittest.main()
