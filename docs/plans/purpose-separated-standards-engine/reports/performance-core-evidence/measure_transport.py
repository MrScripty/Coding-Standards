"""Observe unchanged CLI/MCP contracts in an explicitly disposable checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--store', type=Path, required=True)
p.add_argument('--snapshot', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--confirm-disposable', action='store_true', required=True)
a = p.parse_args()
root = a.repo.resolve()
snapshot = json.loads(a.snapshot.read_text())
target = root / '.standards-engine' / 'snapshots-v1.sqlite3'
target.parent.mkdir(exist_ok=True)
# Measurements supply a closed store. Exclusive creation preserves any existing
# installation; the caller selects a new disposable checkout for another run.
with a.store.open('rb') as source, target.open('xb') as output:
    shutil.copyfileobj(source, output)
env = {**os.environ, 'PYTHONPATH': str(root), 'PYTHONDONTWRITEBYTECODE': '1'}
rows = []

def observe(name, action):
    start = time.perf_counter()
    value = action()
    rows.append({'operation': name, 'wall_s': time.perf_counter() - start,
                 'result_digest': hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()})
    return value

payload = {'snapshot': snapshot, 'request': {'kind': 'read', 'target': 'workflow.planning'}}
cli = [sys.executable, '-P', str(root / '.agents/skills/standards-engine/scripts/invoke.py'),
       '--purpose', 'authoring', '--repo-root', str(root), 'query']

def cli_read():
    result = subprocess.run(cli, input=json.dumps(payload), text=True, capture_output=True,
                            cwd=root, env=env, check=True)
    value = json.loads(result.stdout)
    assert value['kind'] == 'read-result', value
    return value

for i in range(3):
    observe('cold_cli_read', cli_read)

for i in range(2):
    start = time.perf_counter()
    with a.output.with_suffix(f'.mcp-{i}.stderr').open('w') as errors:
        proc = subprocess.Popen([sys.executable, '-P', '-m',
            'tools.standards_engine.standards_engine.mcp', '--purpose', 'authoring',
            '--repo-root', str(root)], cwd=root, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=errors, text=True, bufsize=1)
        def rpc(message):
            proc.stdin.write(json.dumps(message) + '\n')
            proc.stdin.flush()
            response = json.loads(proc.stdout.readline())
            assert 'error' not in response, response
            return response['result']
        try:
            rpc({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'performance-probe', 'version': '1'}}})
            rows.append({'operation': 'cold_mcp_initialize', 'wall_s': time.perf_counter() - start})
            proc.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
            proc.stdin.flush()
            tools = rpc({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}})
            assert len(tools['tools']) == 15
            for j in range(3):
                value = observe('mcp_explicit_read', lambda: rpc({
                    'jsonrpc': '2.0', 'id': j + 3, 'method': 'tools/call', 'params': {
                    'name': 'read', 'arguments': {'snapshot': snapshot, 'target': 'workflow.planning'}}}))
                assert not value.get('isError', False), value
                assert value['structuredContent']['kind'] == 'compact-read-result'
            if i == 0:
                value = observe('mcp_implicit_capture_read', lambda: rpc({
                    'jsonrpc': '2.0', 'id': 20, 'method': 'tools/call', 'params': {
                    'name': 'read', 'arguments': {'target': 'workflow.planning'}}}))
                assert not value.get('isError', False), value
        finally:
            proc.stdin.close()
            proc.wait()
            proc.stdout.close()
        assert proc.returncode == 0

a.output.write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps(rows, indent=2))
