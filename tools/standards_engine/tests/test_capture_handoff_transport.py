"""Actual stdio processes observe the handoff and fresh-owner reconstruction.

The profiler records original compiler calls without replacing function identity.
No model, host configuration or production repository is used.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree

ROOT = Path(__file__).resolve().parents[3]

# This launcher instantiates the real server and uses its normal stdio loop.
LAUNCH = '''
import json, sys
from pathlib import Path
from tools.standards_engine.standards_engine import StandardsEngine
from tools.standards_engine.standards_engine.mcp import MCPServer, serve
from tools.standards_snapshots.standards_snapshots import SnapshotModule
counts = {'compile': 0, 'identity': 0}
functions = {StandardsEngine._compile.__code__: 'compile', SnapshotModule._content_id.__code__: 'identity'}
def observe(frame, event, value):
    if event == 'call' and frame.f_code in functions:
        counts[functions[frame.f_code]] += 1
server = MCPServer(Path(sys.argv[1]), purpose='authoring', output_schemas=sys.argv[2])
sys.setprofile(observe)
try:
    serve(server, sys.stdin, sys.stdout)
finally:
    sys.setprofile(None)
    Path(sys.argv[3]).write_text(json.dumps(counts))
'''


class CaptureHandoffTransportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='capture-handoff-transport-')
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)/'repository'
        _clone_tracked_worktree(cls.root)
        cls.initial_main = subprocess.check_output(['git','-C',str(cls.root),'rev-parse','main'],text=True)

    @contextmanager
    def process(self, delivery, label):
        statistics = Path(self.temporary.name)/(delivery+'-'+label+'.json')
        with tempfile.TemporaryFile(mode='w+') as errors:
            process = subprocess.Popen([sys.executable,'-P','-c',LAUNCH,str(self.root),delivery,str(statistics)],
                cwd=ROOT, env={**os.environ,'PYTHONPATH':str(ROOT)}, text=True,
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors)
            counter = 0
            def call(method, params=None):
                nonlocal counter
                counter += 1
                message = {'jsonrpc':'2.0','id':counter,'method':method}
                if params is not None:
                    message['params'] = params
                process.stdin.write(json.dumps(message)+'\n')
                process.stdin.flush()
                line = process.stdout.readline()
                self.assertTrue(line, 'Server closed without a response.')
                result = json.loads(line)
                self.assertNotIn('error',result,result)
                self.assertEqual(result['id'],counter)
                return result['result']
            try:
                initialized = call('initialize',{'protocolVersion':'2025-11-25','capabilities':{},
                    'clientInfo':{'name':'capture-handoff-fixture','version':'1'}})
                self.assertEqual(initialized['_meta']['standards-engine/runtime']['interface_version'],46)
                process.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
                process.stdin.flush()
                def tool(name, arguments):
                    result = call('tools/call', {'name':name,'arguments':arguments})
                    self.assertFalse(result['isError'],result)
                    self.assertEqual(json.loads(result['content'][0]['text']),result['structuredContent'])
                    return result['structuredContent']
                yield tool, statistics
            finally:
                process.stdin.close()
                try:
                    # Bounds cleanup of this disposable server after explicit EOF;
                    # not a production task-expiry policy.
                    process.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                    self.fail('Fixture server failed to close after EOF.')
                finally:
                    process.stdout.close()
                errors.seek(0)
                self.assertEqual(process.returncode,0,errors.read())

    def test_first_process_reuses_proof_and_replacement_reconstructs_exact_results(self):
        for delivery in ('eager','on-demand'):
            with self.subTest(delivery=delivery):
                with self.process(delivery,'capturing') as (call, statistics):
                    route = call('route', {'facts':{}})
                    self.assertEqual(route['kind'],'compact-route-result')
                    read_args = {'snapshot':route['snapshot'],'target':'core'}
                    read = call('read',read_args)
                    self.assertEqual(call('read',read_args),read)
                self.assertEqual(json.loads(statistics.read_text())['compile'],2)
                with self.process(delivery,'replacement') as (call, statistics):
                    self.assertEqual(call('read',read_args),read)
                    self.assertEqual(call('route',{'snapshot':route['snapshot'],'facts':{}}),route)
                self.assertEqual(json.loads(statistics.read_text())['compile'],1)
        self.assertEqual(subprocess.check_output(['git','-C',str(self.root),'rev-parse','main'],text=True),self.initial_main)
