"""Runtime observations remain independent of Git, stores and content authority."""
from __future__ import annotations

from contextlib import ExitStack
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import RuntimeIdentity
from tools.standards_engine.standards_engine.mcp import MCPServer, tool_catalog
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.test_mcp import ROOT, initialize, request


class RuntimeIdentityTests(unittest.TestCase):
    def test_catalog_and_response_metadata_bind_one_running_process(self):
        with ExitStack() as stack:
            server = MCPServer(ROOT, purpose='authoring')
            stack.callback(server.close)
            initial = initialize(server)['result']
            catalog = server.dispatch(request('tools/list'))['result']
            with patch.object(AgentToolFacade, 'open_repository', side_effect=AssertionError('store access')):
                response = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {}}))['result']
            value = response['structuredContent']
            for result in (initial, catalog, response):
                self.assertEqual(result['_meta']['standards-engine/runtime']['instance_id'], value['instance_id'])
                self.assertEqual(result['_meta']['standards-engine/runtime']['catalog_digest'], value['catalog_digest'])
            self.assertEqual(value['interface_version'], 38)
            self.assertEqual(value['installation_state'], 'current')
            self.assertEqual(value['action'], 'reuse')
            self.assertFalse(initial['capabilities']['tools']['listChanged'])
            self.assertEqual(json.loads(response['content'][0]['text']), value)
            self.assertNotIn(str(ROOT), json.dumps(value))
            mismatch = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {
                'expected_catalog': 'sha256:'+'0'*64}}))['result']['structuredContent']
            self.assertEqual(mismatch['client_catalog_state'], 'differs')
            self.assertEqual(mismatch['action'], 'refresh-tools')
            matched = server.dispatch(request('tools/call', {'name': 'runtime_info', 'arguments': {
                'expected_catalog': value['catalog_digest']}}))['result']['structuredContent']
            self.assertEqual(matched['client_catalog_state'], 'matches')
            error = server.dispatch(request('tools/call', {'name': 'retired-fixture-operation'}))['error']
            self.assertEqual(error['data']['instance_id'], value['instance_id'])
            self.assertIn('refresh', error['message'])

    def test_disk_drift_and_unavailable_installation_keep_startup_identity(self):
        # One controlled installed input isolates drift from unrelated concurrent
        # source edits. Real process tests independently exercise the full inventory.
        with tempfile.TemporaryDirectory(dir=ROOT, prefix='.runtime-input-') as temporary:
            path = Path(temporary) / 'runtime.py'
            path.write_text('initial runtime fixture\n')
            interface = AgentToolFacade.load_interface(ROOT)
            with patch('tools.standards_engine.standards_engine.runtime_identity._implementation_files', return_value=(path,)):
                service = RuntimeIdentity(ROOT, 'authoring', interface, [])
                before = service.invoke({})
                path.write_text('replaced runtime fixture\n')
                changed = service.invoke({})
                self.assertEqual(changed['installation_state'], 'restart-required')
                self.assertEqual(changed['action'], 'restart-and-reconnect')
                self.assertEqual(changed['implementation_digest'], before['implementation_digest'])
                self.assertEqual(changed['instance_id'], before['instance_id'])
                path.unlink()
                self.assertEqual(service.invoke({})['installation_state'], 'unavailable')

    def test_content_edits_do_not_require_runtime_restart(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in ('tools/standards_engine/contracts/a1-interface.toml',
                             'tools/standards_engine/contracts/a1-contract.schema.json'):
                target = root / relative; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            interface = AgentToolFacade.load_interface(root)
            service = RuntimeIdentity(root, 'application', interface, [])
            before = service.invoke({})
            (root / 'CORE-STANDARDS.md').write_text('independent content revision')
            after = service.invoke({})
            self.assertEqual(before, after)
            self.assertFalse((root / '.standards-engine').exists())
            invalid = service.invoke({'purpose': 'authoring'})
            self.assertEqual(invalid['kind'], 'application-rejected-result')
            self.assertNotIn(str(root), json.dumps(invalid))

    def test_actual_mcp_and_cli_observe_without_a_git_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in ('tools/standards_engine/contracts/a1-interface.toml',
                             'tools/standards_engine/contracts/a1-contract.schema.json',
                             'tools/standards_engine/contracts/generated/agent-tools.json'):
                target = root / relative; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            messages = [request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {},
                         'clientInfo': {'name': 'runtime-fixture', 'version': '1'}}),
                        {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                        request('tools/call', {'name': 'runtime_info', 'arguments': {}}, identifier=2)]
            environment = {**os.environ, 'PYTHONPATH': str(ROOT)}
            mcp = subprocess.run([sys.executable, '-P', '-m', 'tools.standards_engine.standards_engine.mcp',
                    '--repo-root', str(root), '--purpose', 'application'],
                input=''.join(json.dumps(item)+'\n' for item in messages), text=True, capture_output=True,
                env=environment, timeout=60)
            self.assertEqual(mcp.returncode, 0, mcp.stderr)
            self.assertEqual(mcp.stderr, '')
            result = json.loads(mcp.stdout.splitlines()[-1])['result']['structuredContent']
            self.assertEqual(result['kind'], 'runtime-info-result')
            cli = subprocess.run([sys.executable, '-P', str(ROOT / '.agents/skills/standards-engine/scripts/invoke.py'),
                    '--repo-root', str(root), '--purpose', 'application', 'runtime_info'],
                input='{}', text=True, capture_output=True, env=environment, timeout=60)
            self.assertEqual(cli.returncode, 0, cli.stderr)
            observed = json.loads(cli.stdout)
            self.assertNotEqual(result['instance_id'], observed['instance_id'])
            self.assertEqual(result['catalog_digest'], observed['catalog_digest'])
            self.assertFalse((root / '.git').exists())
            self.assertFalse((root / '.standards-engine').exists())
            catalog = {item['name'] for item in tool_catalog(root, purpose='application')}
            self.assertIn('runtime_info', catalog)
            self.assertNotIn('resolve_many', catalog)
            self.assertNotIn('workflow_details', catalog)
