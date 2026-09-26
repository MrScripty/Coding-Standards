"""Opt-in model-visible discovery qualification in a private disposable repository.

Requires the operator's configured Codex and explicit --allow-model-turn. This
starts a real model turn, not a scripted substitution for one. Keep local logs
private. It does not edit the source repository or publish its fixture proposals.
Protocol source: openai/codex rust-v0.157.1 app-server ThreadStartParams,
TurnStartParams and ThreadItem. Unknown client event surfaces fail qualification.
"""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from jsonschema import Draft202012Validator

from tools.standards_contracts.standards_contracts import schema_closure
from tools.standards_engine.standards_engine.context_projection import qualified_operations

from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.standards_engine.runtime_identity import RuntimeIdentity
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.test_agent_workflow import evidence
from tools.standards_engine.tests.test_analysis import _clone_tracked_worktree

ROOT = Path(__file__).resolve().parents[3]
AUTHORING_OPERATIONS = ('propose', 'revise', 'resolve_workflow', 'resolve_many', 'review')


def _arguments_visible(contract: dict, arguments: object, records: dict) -> bool:
    """Check acquired definitions along the independently validated input path.

    The reference validator selects oneOf branches. Unread alternatives are not
    needed, but every named definition on the selected path must be acquired.
    This observes coverage; it does not implement instance constraint semantics.
    """
    validator = Draft202012Validator(contract)
    if not validator.is_valid(arguments):
        return False
    definitions = contract['$defs']
    seen = set()

    def observe(schema, value):
        if isinstance(schema, bool):
            return True
        if '$ref' in schema:
            name = schema['$ref'].removeprefix('#/$defs/')
            if name not in definitions or records.get(name) != definitions[name]:
                return False
            key = (name, id(value))
            if key not in seen:
                seen.add(key)
                if not observe(definitions[name], value):
                    return False
        if 'oneOf' in schema:
            choices = [choice for choice in schema['oneOf']
                       if validator.evolve(schema=choice).is_valid(value)]
            if len(choices) != 1 or not observe(choices[0], value):
                return False
        if isinstance(value, dict):
            properties = schema.get('properties', {})
            for key, item in value.items():
                child = properties.get(key, schema.get('additionalProperties', True))
                if not observe(child, item):
                    return False
        if isinstance(value, list) and 'items' in schema:
            if not all(observe(schema['items'], item) for item in value):
                return False
        return True

    return observe({'$ref': contract['$ref']}, arguments)


def assess_model_items(items: list[dict], server: str, catalog: dict, contracts: dict) -> dict:
    """Assess observed tool events, never an agent's self-reported success."""
    failures = []
    calls = []
    discovered = set()
    acquired = {}
    seen_ids = set()
    for item in items:
        if item.get('id') in seen_ids:
            failures.append('Duplicate completed item identity.')
            continue
        seen_ids.add(item.get('id'))
        kind = item.get('type')
        if kind in {'userMessage', 'agentMessage', 'reasoning', 'plan', 'contextCompaction'}:
            continue
        if kind == 'functionCallOutput' and item.get('name') == 'exec' and item.get('namespace') == 'functions':
            # Code Mode's execution wrapper is not a filesystem command. Its
            # underlying MCP calls must still be individually observed below.
            continue
        if kind != 'mcpToolCall' or item.get('server') != server:
            failures.append(f'Non-fixture or unqualified tool surface: {kind}.')
            continue
        name = item.get('tool')
        if name not in catalog:
            failures.append('Call outside the qualified catalog.')
            continue
        arguments = item.get('arguments')
        result = item.get('result') or {}
        value = result.get('structuredContent')
        calls.append((name, arguments, value))
        if item.get('status') != 'completed' or item.get('error') is not None or result.get('isError'):
            failures.append(f'{name}: client reported failure.')
        if not Draft202012Validator(catalog[name]['inputSchema']).is_valid(arguments):
            failures.append(f'{name}: invalid model-authored arguments.')
            continue
        if not isinstance(value, dict) or not Draft202012Validator(catalog[name]['outputSchema']).is_valid(value):
            failures.append(f'{name}: missing or invalid structured result.')
            continue
        if 'rejected' in value.get('kind', '') or value.get('status') in {'rejected', 'stale', 'recovery-required'}:
            failures.append(f'{name}: unresolved domain failure.')
        if name == 'describe_input':
            if value.get('kind') != 'input-contract-result' or not value.get('records'):
                failures.append('Discovery returned no input records.')
            else:
                target = arguments['operation']
                contract = contracts.get(target)
                if contract is None or value.get('root') != contract['$ref'].rsplit('/', 1)[-1]:
                    failures.append('Discovery did not identify the expected operation root.')
                    continue
                records = acquired.setdefault(target, {})
                for record in value['records']:
                    try:
                        definition = json.loads(record['schema_json'])
                    except (KeyError, TypeError, ValueError):
                        failures.append('An observed discovery record was not complete JSON.')
                        continue
                    if record['name'] not in contract['$defs'] or definition != contract['$defs'][record['name']]:
                        failures.append('An observed discovery record differed from the installed contract.')
                        continue
                    records[record['name']] = definition
                discovered.add(target)
        elif name in AUTHORING_OPERATIONS:
            if name not in discovered or not _arguments_visible(contracts[name], arguments, acquired.get(name, {})):
                failures.append(f'{name}: used input shapes were not acquired through discovery before use.')
        if name in {'apply', 'recover'}:
            failures.append('Publication/recovery is outside this fixture task.')
    counts = Counter(name for name, _, _ in calls)
    for name in AUTHORING_OPERATIONS:
        if counts[name] != 1:
            failures.append(f'{name}: expected one successful action, observed {counts[name]}.')
    actions = [name for name, _, _ in calls if name in AUTHORING_OPERATIONS]
    if actions != list(AUTHORING_OPERATIONS):
        failures.append('Required proposal/revision/single/batch/review sequence was not observed.')
    batches = [a for n, a, _ in calls if n == 'resolve_many' and isinstance(a, dict)]
    if len(batches) != 1 or len(batches[0].get('submissions', [])) < 2:
        failures.append('No multi-decision atomic batch was observed.')
    for name in ('resolve_many', 'review'):
        args = [a for n, a, _ in calls if n == name and isinstance(a, dict)]
        if len(args) != 1 or not args[0].get('evidence') or 'evidence_ref' not in json.dumps(args[0]):
            failures.append(f'{name}: request-local evidence reuse was not observed.')
    ready = [v for n, _, v in calls if n == 'review' and isinstance(v, dict)]
    if len(ready) != 1 or ready[0].get('status') != 'ready':
        failures.append('Exact review readiness was not observed.')
    return {
        'status': 'failed' if failures else 'passed', 'failures': failures,
        'calls': dict(counts), 'discovered_operations': sorted(discovered),
        'request_json_bytes': sum(len(json.dumps(a).encode()) for _, a, _ in calls),
        'result_json_bytes': sum(len(json.dumps(v).encode()) for _, _, v in calls),
        'model_visible_rendering': 'Not inferred from raw catalog; this assessment observes model behavior using discovery.',
    }


def _matches_readback(value: dict, revision: dict, target: str, title: str, body: str) -> bool:
    """Inspect the fixture's exact rendered body, not a matching summary string."""
    parts = value.get('content', '').split('\n\n', 3)
    return (value.get('kind') == 'proposal-read-result' and value.get('revision') == revision
            and value.get('policy', {}).get('id') == target and value.get('requires') == ['core']
            and value.get('specializes') == [] and len(parts) == 4
            and parts[0] == '# ' + title and parts[1] == '**Standards metadata**'
            and parts[3].strip() == body)


def scenario(server: str, fixture: Path, prefix: str) -> str:
    reference = evidence(fixture)
    return f'''Qualify input-contract discovery using only the {server} MCP tools in
this fresh session. Obtain each of the five authoring operations' argument shapes
through describe_input before using it. Select relevant definitions rather than
reading unrelated schema alternatives. Repository files, schema/example files,
shell, web, other servers and subagents are outside this task. Do not ask for
clarification or infer success from your own text; report exact unavailable outcomes.

In one proposal create three isolated test-only topic standards, with identities
{prefix}-0, {prefix}-1 and {prefix}-2. Their titles are "Discovery Test 0",
"Discovery Test 1" and "Discovery Test 2"; role topic, normative level MUST.
Each applies only during this disposable qualification, excludes all production
use, requires core, specializes nothing, and registers no policy units. All three
initial bodies are "This isolated test scope requires an explicit owner decision."
Verification is this isolated MCP workflow. Give a material purpose and rationale.

Revise that proposal once to add a non-normative reference standard named
reference.{prefix}-extra, title "Discovery Reference", role reference, level
REFERENCE, the same test-only applicability, core prerequisite and no specialization
or policy units. Its body is "This is contextual test material only."

There should be three topic impact obligations in the new analysis. As authorized
fixture owner, explicitly confirm the first in one single-decision operation,
then confirm the remaining two together in one atomic batch. Bind each decision to
the returned work and current context. Review the complete analysis with separate
consumer, impact and audit acceptances to readiness. The decisions explicitly
acknowledge the isolated scopes and absence of production impact. This task grants
fixture proposal/decision/review authority, not publication or recovery authority.
Stop at readiness. Use request-local evidence reuse for the batch and review.

The real available evidence is {reference['id']}, with exact digest
{reference['digest']}, provider {reference['provider_contract']}, version
{reference['provider_contract_version']}. It documents the actual Engine protocol
being exercised. Use it as the fixture's evidence; the isolated test owner decisions
above supply the intended semantic dispositions. Do not fabricate other evidence.
'''


async def run(arguments) -> dict:
    output = arguments.evidence_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    fixture = output / 'repository'
    _clone_tracked_worktree(fixture)
    workdir = output / 'client-workdir'
    workdir.mkdir()
    prefix = 'topic.discovery-' + uuid.uuid4().hex[:12]
    server = 'standards-discovery-' + uuid.uuid4().hex[:12]
    prompt = scenario(server, fixture, prefix)
    (output / 'task.txt').write_text(prompt)
    interface = AgentToolFacade.load_interface(fixture)
    catalog = tool_catalog(interface, purpose='authoring', schema_mode=arguments.schema_mode)
    toolmap = {tool['name']: tool for tool in catalog}
    projection = interface.project().agent_tools
    contracts = {operation['id']: schema_closure(
        {'$schema': interface.schema['$schema'], '$ref': '#/$defs/' + operation['input_definition']},
        projection['$defs']) for operation in qualified_operations(projection, 'authoring')
        if operation['id'] in toolmap}
    identity = RuntimeIdentity(fixture, 'authoring', interface, catalog).metadata()
    original_main = subprocess.check_output(['git', '-C', str(fixture), 'rev-parse', 'main'], text=True).strip()
    version = subprocess.check_output([arguments.codex, '--version'], text=True).strip()
    command = [arguments.codex, 'app-server', '--stdio']
    for option in arguments.codex_config:
        command.extend(['-c', option])
    # Run-owned fixture coordinates take precedence over operator surface choices.
    command.extend(['-c', 'analytics.enabled=false',
        '-c', f'mcp_servers.{server}.command={json.dumps(sys.executable)}',
        '-c', f'mcp_servers.{server}.args={json.dumps(["-P", "-m", "tools.standards_engine.standards_engine.mcp", "--repo-root", str(fixture), "--purpose", "authoring", "--schema-mode", arguments.schema_mode])}',
        '-c', f'mcp_servers.{server}.env.PYTHONPATH={json.dumps(str(ROOT))}'])
    events = []
    report = {'status': 'unavailable', 'client_version': version, 'requested_model': arguments.model,
              'requested_surface': arguments.surface, 'schema_mode': arguments.schema_mode,
              'catalog_digest': identity['catalog_digest'], 'fixture_main': original_main}
    process = None
    with (output/'stderr.log').open('w') as stderr, (output/'events.jsonl').open('w') as transcript:
        try:
            process = await asyncio.create_subprocess_exec(*command, cwd=workdir,
                stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                stderr=stderr, limit=16 * 1024 * 1024)
            counter = 0
            def send(value):
                transcript.write(json.dumps({'direction': 'request', 'message': value})+'\n'); transcript.flush()
                process.stdin.write((json.dumps(value)+'\n').encode())
            async def receive():
                line = await process.stdout.readline()
                if not line:
                    raise RuntimeError('Codex app-server closed before qualification completed.')
                value = json.loads(line)
                transcript.write(json.dumps({'direction': 'response', 'message': value})+'\n'); transcript.flush()
                if 'method' in value:
                    if 'id' in value:
                        send({'id': value['id'], 'error': {'code': -32601, 'message': 'Interactive approval/input is not authorized by this qualification harness.'}})
                        raise RuntimeError('Unexpected interactive client request; inspect the private transcript.')
                    events.append(value)
                return value
            async def rpc(method, params):
                nonlocal counter
                counter += 1
                send({'id': counter, 'method': method, 'params': params})
                await process.stdin.drain()
                while True:
                    value = await receive()
                    if value.get('id') == counter:
                        if 'error' in value:
                            raise RuntimeError(f'{method} failed; inspect the private transcript.')
                        return value['result']
            await rpc('initialize', {'clientInfo': {'name': 'standards-discovery-qualification', 'version': '1'}, 'capabilities': {'experimentalApi': True}})
            send({'method': 'initialized', 'params': {}})
            thread = await rpc('thread/start', {'cwd': str(workdir), 'ephemeral': True,
                'approvalPolicy': 'never', 'sandbox': 'read-only', 'model': arguments.model,
                'developerInstructions': f'This qualification permits only the {server} MCP tools. Obtain input shapes from describe_input. Stop before publication; use no filesystem, shell, web or other tools.'})
            tid = thread['thread']['id']
            inventory = await rpc('mcpServerStatus/list', {'threadId': tid})
            if any(s.get('tools') for s in inventory['data'] if s['name'] != server):
                raise RuntimeError('Disable other MCP servers for this qualification before authorizing a model turn; only the disposable fixture may expose tools.')
            observed = next(s for s in inventory['data'] if s['name'] == server)['tools']
            if set(observed) != set(toolmap):
                raise RuntimeError('Configured fixture catalog did not match the expected tool set.')
            for name in toolmap:
                for field in ('inputSchema', 'outputSchema', 'description'):
                    if observed[name][field] != toolmap[name][field]:
                        raise RuntimeError('Configured fixture catalog content did not match.')
            async def call(name, payload):
                result = await rpc('mcpServer/tool/call', {'threadId': tid, 'server': server, 'tool': name, 'arguments': payload})
                if result.get('isError'):
                    raise RuntimeError(f'{name} failed during scripted qualification observation.')
                value = result['structuredContent']
                Draft202012Validator(toolmap[name]['outputSchema']).validate(value)
                return value
            runtime = await call('runtime_info', {'expected_catalog': identity['catalog_digest']})
            if runtime['client_catalog_state'] != 'matches' or runtime['installation_state'] != 'current':
                raise RuntimeError('Fixture runtime/catalog qualification failed before the model turn.')
            report['runtime'] = runtime
            turn = await rpc('turn/start', {'threadId': tid, 'input': [{'type': 'text', 'text': prompt}]})
            turn_id = turn['turn']['id']
            while not any(e.get('method') == 'turn/completed' and e['params']['turn']['id'] == turn_id for e in events):
                await receive()
            terminal = next(e['params']['turn'] for e in events if e.get('method') == 'turn/completed' and e['params']['turn']['id'] == turn_id)
            items = [e['params']['item'] for e in events if e.get('method') == 'item/completed' and e['params'].get('turnId') == turn_id]
            report.update(assess_model_items(items, server, toolmap, contracts))
            if terminal.get('status') != 'completed':
                report['failures'].append('The real model turn did not complete successfully.')
            calls = [i for i in items if i.get('type') == 'mcpToolCall' and i.get('server') == server]
            for operation, expected_ids in [('propose', {f'{prefix}-{i}' for i in range(3)}),
                                            ('revise', {f'reference.{prefix}-extra'})]:
                selected = [i.get('arguments', {}) for i in calls if i.get('tool') == operation]
                edits = selected[0].get('change_set', {}).get('edits', []) if len(selected) == 1 else []
                if (len(edits) != len(expected_ids) or any(edit.get('kind') != 'create-standard' for edit in edits)
                    or {edit.get('standard', {}).get('id') for edit in edits} != expected_ids):
                    report['failures'].append(f'{operation}: edits did not match the isolated task write set.')
            revisions = [i['result']['structuredContent'].get('revision') for i in calls if i.get('tool') == 'review' and i.get('result', {}).get('structuredContent', {}).get('status') == 'ready']
            if len(revisions) == 1 and revisions[0] is not None:
                for target in [f'{prefix}-{i}' for i in range(3)] + [f'reference.{prefix}-extra']:
                    value = await call('query_proposal', {'revision': revisions[0], 'request': {'kind': 'read', 'target': target}})
                    (output/(target+'.json')).write_text(json.dumps(value, indent=2))
                    expected = ('This is contextual test material only.' if target.startswith('reference.') else
                                'This isolated test scope requires an explicit owner decision.')
                    title = 'Discovery Reference' if target.startswith('reference.') else 'Discovery Test ' + target.rsplit('-', 1)[-1]
                    if not _matches_readback(value, revisions[0], target, title, expected):
                        report['failures'].append('Readback did not preserve requested fixture content.')
            else:
                report['failures'].append('No exact readiness revision was available for independent readback.')
            if subprocess.check_output(['git', '-C', str(fixture), 'rev-parse', 'main'], text=True).strip() != original_main:
                report['failures'].append('Fixture publication occurred; the task required unchanged main.')
            report['status'] = 'failed' if report['failures'] else 'passed'
        except Exception as error:
            report.update(status='unavailable', failure=f'{type(error).__name__}: {error}')
        finally:
            if process is not None:
                process.stdin.close()
                # This is shutdown after completion/failure/operator cancellation,
                # not an elapsed-time deadline for an active model task.
                try:
                    await asyncio.wait_for(process.wait(), 10)
                except asyncio.TimeoutError:
                    process.terminate()
                    await process.wait()
            (output/'qualification.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-model-turn', action='store_true', help='Explicitly authorize this local qualification to use the configured model service.')
    parser.add_argument('--model', required=True)
    parser.add_argument('--surface', required=True, help='Operator-selected actual client surface, e.g. code-mode; recorded, not inferred from a catalog.')
    parser.add_argument('--evidence-dir', required=True, type=Path, help='New directory; preserves the disposable repository and private transcript.')
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--schema-mode', choices=('native', 'compatibility'), default='native')
    parser.add_argument('--codex-config', action='append', default=[], help='Explicit current-client configuration override; never written to user configuration.')
    args = parser.parse_args(argv)
    if not args.allow_model_turn:
        parser.error('--allow-model-turn is required; no model turn was started')
    if shutil.which(args.codex) is None:
        parser.error('The selected Codex executable is unavailable; actual-client qualification remains open')
    result = asyncio.run(run(args))
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
