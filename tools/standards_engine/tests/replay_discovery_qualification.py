"""Reassess a stock Codex discovery transcript without running a model or Engine.

Read the original events, report, and retained fixture ref; write one new report
exclusively. The source checkout must reproduce the recorded runtime/catalog.
This is recorded-evidence assessment, not fresh client qualification or approval
of compatibility retirement. Original and independent verdicts remain untouched.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError, SchemaError

from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
from tools.standards_engine.standards_engine.runtime_identity import RuntimeIdentity
from tools.standards_engine.standards_engine.tools import AgentToolFacade
from tools.standards_engine.tests.codex_discovery_client import (
    OBSERVER_VERSION, ROOT, RUNTIME_FIELDS, _same_json, assess_model_items,
    fixture_contents, fixture_failures, input_contracts, model_observations, read_recorded_json,
)


@dataclass(frozen=True)
class RecordedCall:
    method: str
    params: dict
    result: dict
    requested_at: int
    received_at: int


def parse_trace(text: str) -> tuple[list[RecordedCall], list[tuple[int, dict]]]:
    """Correlate the single-connection stock JSONL format; preserve file order."""
    calls, events, pending, used = [], [], {}, set()
    for index, line in enumerate(text.splitlines()):
        row = read_recorded_json(line)
        if not isinstance(row, dict) or row.get('direction') not in ('request', 'response'):
            raise ValueError('Unsupported transcript envelope.')
        message = row.get('message')
        if not isinstance(message, dict):
            raise ValueError('Unsupported transcript message.')
        identifier = message.get('id')
        if identifier is not None and (isinstance(identifier, bool) or not isinstance(identifier, (int, str))):
            raise ValueError('Invalid transcript request identity.')
        if row['direction'] == 'request':
            if identifier is not None:
                if identifier in used or not isinstance(message.get('params'), dict):
                    raise ValueError('Duplicate request or missing request parameters.')
                used.add(identifier)
                pending[identifier] = (index, message)
            elif message.get('method') != 'initialized' or message.get('params', {}) != {}:
                raise ValueError('Unsupported client notification in the stock transcript.')
            continue
        if 'method' in message:
            if identifier is not None:
                raise ValueError('Interactive server request prevents automatic qualification.')
            if not isinstance(message.get('params', {}), dict):
                raise ValueError('Malformed notification parameters.')
            events.append((index, message))
            continue
        if identifier not in pending or 'error' in message or not isinstance(message.get('result'), dict):
            raise ValueError('Unmatched, failed, or malformed RPC response.')
        requested_at, request = pending.pop(identifier)
        calls.append(RecordedCall(request['method'], request['params'], message['result'], requested_at, index))
    if pending:
        raise ValueError('Transcript ended with unresolved RPC requests.')
    return calls, events


def _one(values, label):
    if len(values) != 1:
        raise ValueError(f'Expected exactly one {label} in the preserved trace.')
    return values[0]


def assess_recording(calls: list[RecordedCall], events: list[tuple[int, dict]],
                     previous: dict, catalog: dict, contracts: dict,
                     expected_runtime: dict, observed_main: str, *, output_contracts: dict | None = None) -> dict:
    """Reconstruct one fresh model turn and its independent scripted readbacks."""
    validation = output_contracts if output_contracts is not None else {
        name: tool['outputSchema'] for name, tool in catalog.items()}
    allowed_methods = {'initialize', 'thread/start', 'mcpServerStatus/list',
                       'mcpServer/tool/call', 'turn/start'}
    if any(call.method not in allowed_methods for call in calls):
        raise ValueError('Unexpected scripted RPC outside the stock qualification workflow.')
    thread = _one([c for c in calls if c.method == 'thread/start'], 'fresh thread')
    turn = _one([c for c in calls if c.method == 'turn/start'], 'model turn')
    tid = thread.result['thread']['id']
    turn_id = turn.result['turn']['id']
    if (thread.params.get('ephemeral') is not True or turn.params.get('threadId') != tid
        or thread.received_at >= turn.requested_at):
        raise ValueError('Recorded turn is not bound to the fresh thread.')
    inventory = _one([c for c in calls if c.method == 'mcpServerStatus/list'], 'catalog observation')
    servers = [s for s in inventory.result['data'] if s.get('tools')]
    server_info = _one(servers, 'exposed fixture server')
    server = server_info['name']
    if (inventory.params.get('threadId') != tid or inventory.received_at >= turn.requested_at
        or set(server_info['tools']) != set(catalog)):
        raise ValueError('Catalog preflight is missing or outside the selected thread.')
    for name, tool in catalog.items():
        for field in ('inputSchema', 'outputSchema', 'description'):
            if ((field in server_info['tools'][name]) != (field in tool) or
                not _same_json(server_info['tools'][name].get(field), tool.get(field))):
                raise ValueError('Recorded catalog differs from the selected source checkout.')
    runtime_call = _one([c for c in calls if c.method == 'mcpServer/tool/call'
                         and c.params.get('tool') == 'runtime_info'], 'runtime observation')
    runtime = runtime_call.result['structuredContent']
    if (runtime_call.params.get('server') != server or runtime_call.params.get('threadId') != tid
        or runtime_call.received_at >= turn.requested_at or runtime_call.result.get('isError')
        or runtime.get('installation_state') != 'current' or runtime.get('client_catalog_state') != 'matches'):
        raise ValueError('Runtime preflight is not current and bound before the model turn.')
    Draft202012Validator(validation['runtime_info']).validate(runtime)
    for key in RUNTIME_FIELDS:
        if key != 'instance_id' and not _same_json(runtime.get(key), expected_runtime[key]):
            raise ValueError('Recorded runtime differs from the selected source checkout.')
    if not _same_json(previous.get('runtime'), runtime) or previous.get('catalog_digest') != runtime['catalog_digest']:
        raise ValueError('Preserved report and trace have different runtime bindings.')
    if previous.get('requested_model') != thread.params.get('model'):
        raise ValueError('Preserved report and thread have different model selections.')
    endings = [(index, e) for index, e in events if e.get('method') == 'turn/completed'
               and e.get('params', {}).get('threadId') == tid
               and e['params'].get('turn', {}).get('id') == turn_id]
    ending_at, ending = _one(endings, 'completed model turn')
    for index, event in events:
        params = event.get('params', {})
        if event.get('method') in ('item/started', 'item/completed'):
            if params.get('threadId') != tid or params.get('turnId') != turn_id:
                raise ValueError('Mixed session/turn item stream is not qualified.')
            if not turn.requested_at < index < ending_at:
                raise ValueError('Item observations fall outside the selected model turn.')
    items, starts = model_observations([e for _, e in events], tid, turn_id)
    result = assess_model_items(items, server, catalog, contracts, runtime, started_before=starts, output_contracts=validation)
    if ending['params']['turn'].get('status') != 'completed':
        result['failures'].append('The recorded model turn did not complete successfully.')
    proposed = _one([i for i in items if i.get('tool') == 'propose'], 'proposal')
    identities = [e['standard']['id'] for e in proposed['arguments']['change_set']['edits']]
    matches = [re.fullmatch(r'(topic\.discovery-[0-9a-f]{12})-[012]', name) for name in identities]
    if not matches or any(m is None for m in matches):
        raise ValueError('Unsupported fixture identity; use the stock discovery scenario.')
    prefix = _one(list({m[1] for m in matches}), 'fixture prefix')
    # New reports carry these fields; older stock reports can recover them only
    # from the correlated protocol, not from caller-supplied guesses.
    for key, value in (('server', server), ('thread_id', tid), ('turn_id', turn_id), ('fixture_prefix', prefix)):
        if key in previous and previous[key] != value:
            raise ValueError('Preserved report disagrees with the trace scope.')
    readbacks = {}
    for call in calls:
        if call.method != 'mcpServer/tool/call' or call is runtime_call:
            continue
        params = call.params
        request = params.get('arguments', {}).get('request', {})
        if (call.requested_at <= ending_at or params.get('server') != server
            or params.get('threadId') != tid or params.get('tool') != 'query_proposal'
            or request.get('kind') != 'read' or request.get('target') not in fixture_contents(prefix)):
            raise ValueError('Unexpected scripted tool call; model authoring must come from observed items.')
        target = request['target']
        if target in readbacks or call.result.get('isError'):
            raise ValueError('Duplicate or failed independent readback.')
        meta = (call.result.get('_meta') or {}).get('standards-engine/runtime', {})
        if any(not _same_json(meta.get(key), runtime[key]) for key in RUNTIME_FIELDS):
            raise ValueError('Independent readback changed runtime binding.')
        value = call.result['structuredContent']
        Draft202012Validator(validation['query_proposal']).validate(value)
        if value.get('revision') != params['arguments'].get('revision'):
            raise ValueError('Readback response did not bind the requested revision.')
        readbacks[target] = value
    initial_main = previous['fixture_main']
    if not isinstance(initial_main, str) or not re.fullmatch(r'[0-9a-f]{40}', initial_main):
        raise ValueError('Missing exact initial fixture revision.')
    result['failures'].extend(fixture_failures(items, server, prefix, readbacks, initial_main, observed_main))
    result.update(status='failed' if result['failures'] else 'passed',
                  thread_id=tid, turn_id=turn_id, server=server,
                  readbacks_verified=len(readbacks), fixture_main=initial_main,
                  observed_main=observed_main, catalog_digest=runtime['catalog_digest'],
                  client_version=previous.get('client_version'), requested_model=previous.get('requested_model'),
                  requested_surface=previous.get('requested_surface'))
    return result


def replay(evidence_dir: Path) -> dict:
    """Read-only observation; no store open, tool submission, or paid model call."""
    result = {'observer_version': OBSERVER_VERSION, 'status': 'unavailable',
              'scope': 'preserved single-session evidence replay; not a new model run',
              'compatibility_retirement': 'requires supported-client and integration acceptance'}
    result['observer_sources'] = {name: 'sha256:' + hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                                  for name in ('codex_discovery_client.py', 'replay_discovery_qualification.py')}
    try:
        raw_trace = (evidence_dir / 'events.jsonl').read_bytes()
        raw_report = (evidence_dir / 'qualification.json').read_bytes()
        result['sources'] = {name: 'sha256:' + hashlib.sha256(raw).hexdigest() for name, raw in
                             (('events.jsonl', raw_trace), ('qualification.json', raw_report))}
        previous = read_recorded_json(raw_report.decode('utf-8'))
        result['previous_status'] = previous.get('status')
        mode = previous.get('schema_mode')
        if mode not in ('native', 'compatibility'):
            raise ValueError('Missing recorded schema mode.')
        interface = AgentToolFacade.load_interface(ROOT)
        delivery = previous.get('output_schemas', 'eager')
        catalog = tool_catalog(interface, purpose='authoring', schema_mode=mode, output_schemas=delivery)
        validation = {t['name']: t['outputSchema'] for t in tool_catalog(interface, purpose='authoring', schema_mode=mode)}
        expected = RuntimeIdentity(ROOT, 'authoring', interface, catalog).metadata()
        toolmap = {t['name']: t for t in catalog}
        calls, events = parse_trace(raw_trace.decode('utf-8'))
        current = subprocess.check_output(
            ['git', '-C', str(evidence_dir / 'repository'), 'rev-parse', '--verify', 'refs/heads/main'],
            text=True, stderr=subprocess.PIPE).strip()
        result.update(assess_recording(calls, events, previous, toolmap,
                                     input_contracts(interface, toolmap), expected, current, output_contracts=validation))
        result['schema_mode'] = mode
        result['output_schemas'] = delivery
        # Detect input replacement during observation instead of certifying a
        # mixture. This is hash-bound local evidence, not cryptographic attestation
        # that the caller's log was never edited before it was supplied.
        for name, digest in result['sources'].items():
            if 'sha256:' + hashlib.sha256((evidence_dir / name).read_bytes()).hexdigest() != digest:
                raise ValueError('Recorded evidence changed while it was being assessed.')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ValidationError, SchemaError, subprocess.CalledProcessError) as error:
        result.update(status='unavailable', failure=f'{type(error).__name__}: {error}')
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', type=Path, required=True, help='Original stock harness directory, including the retained fixture.')
    parser.add_argument('--output', type=Path, required=True, help='New report path; existing files are never replaced.')
    args = parser.parse_args(argv)
    if args.output.resolve().is_relative_to(args.evidence_dir.resolve()):
        parser.error('--output must be outside the original evidence directory')
    # Reserve the new output before assessment. Exclusive creation also refuses
    # existing symlinks/hardlinks, including aliases of original evidence files.
    with open(args.output, 'x', encoding='utf-8',
              opener=lambda path, flags: os.open(path, flags, 0o600)) as destination:
        result = replay(args.evidence_dir)
        destination.write(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
