"""Opt-in operator observations. Never an Engine store or an agent tool.

The recorder owns sanitization, SQLite transactions, retention and fail-open
health. No caller-supplied scalar is persisted. A missing terminal event means
unknown outcome; restarting a recorder never manufactures a completion.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import sys
import time
from typing import TextIO
import uuid

SCHEMA_VERSION = 1
APPLICATION_ID = 0x53454F42  # SEOB, separate from every Engine domain database.
DEFAULT_MAX_CALLS = 10_000
DEFAULT_MAX_AGE_SECONDS = 7 * 24 * 60 * 60
DEFAULT_MAX_BYTES = 32 * 1024 * 1024
BUSY_TIMEOUT_MS = 20
MAX_SHAPE_NODES = 64
MAX_SHAPE_DEPTH = 5
MAX_SHAPE_BYTES = 8 * 1024
MAX_ARRAY_ITEMS = 4
MAX_FEEDBACK_ISSUES = 8
MAX_FEEDBACK_POINTER_CHARS = 512
MAX_REPORT_ROWS = 1000
MAX_SEQUENCE_SCAN = 10_000
METHODS = frozenset({'initialize', 'tools/list', 'tools/call', 'ping'})
SENSITIVE_FIELDS = frozenset({
    'body', 'content', 'text', 'prompt', 'message', 'rationale', 'reason',
    'evidence', 'details', 'metadata', 'credentials', 'password', 'token',
    'secret', 'authorization', 'api_key', 'environment', 'env',
})
CONSTRAINTS = frozenset({
    'type', 'required', 'additionalProperties', 'enum', 'const', 'oneOf',
    'anyOf', 'allOf', 'not', 'minimum', 'maximum', 'minItems', 'maxItems',
    'minLength', 'maxLength', 'pattern', 'format', 'uniqueItems',
})
OUTCOMES = frozenset({'invalid', 'unsupported', 'unavailable', 'stale',
                      'rejected', 'recovery-required', 'needs-action',
                      'requires-change', 'complete', 'ready'})


SCHEMA_DDL = (
    'CREATE TABLE sessions (id TEXT PRIMARY KEY, started REAL NOT NULL, runtime TEXT NOT NULL, deployment TEXT NOT NULL, catalog TEXT NOT NULL, pruned INTEGER NOT NULL DEFAULT 0)',
    'CREATE TABLE interactions (id TEXT PRIMARY KEY, session TEXT NOT NULL REFERENCES sessions(id), ordinal INTEGER NOT NULL, started REAL NOT NULL, method TEXT NOT NULL, operation TEXT NOT NULL, input_shape TEXT NOT NULL, shape_digest TEXT NOT NULL, discovery_operation TEXT, catalog_state TEXT NOT NULL, request_bytes INTEGER, scope TEXT NOT NULL, UNIQUE(session, ordinal))',
    "CREATE TABLE events (interaction TEXT PRIMARY KEY REFERENCES interactions(id) ON DELETE CASCADE, phase TEXT NOT NULL CHECK(phase IN ('end','error','incomplete')), finished REAL NOT NULL, duration_ms REAL NOT NULL, response_bytes INTEGER, outcome TEXT NOT NULL, feedback TEXT NOT NULL)",
    'CREATE INDEX interaction_age ON interactions(started)',
)


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def _digest(value: object) -> str:
    return 'sha256:' + hashlib.sha256(_json(value).encode()).hexdigest()


def serialized_bytes(value: object) -> int:
    """JSON representation bytes, not tokens; avoid retaining a second payload."""
    return sum(len(part.encode('utf-8')) for part in json.JSONEncoder().iterencode(value))


def _kind(value: object) -> str:
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, str):
        return 'string'
    if isinstance(value, (int, float)):
        return 'number'
    return 'object' if isinstance(value, dict) else 'array' if isinstance(value, list) else 'unknown'


class InputShape:
    """Value-free disclosure projection, not a second input validator.

    Static property names come only from the installed schema. Unknown names and
    every scalar value disappear before SQLite sees anything. Sensitive children
    are not traversed even if their properties occur elsewhere in the schema.
    """
    def __init__(self, schema: dict) -> None:
        self.schema = schema
        self.definitions = schema.get('$defs', {})

    def _expanded(self, nodes: list[dict]) -> list[dict]:
        result, pending, seen = [], list(nodes), set()
        while pending:
            node = pending.pop()
            if not isinstance(node, dict) or id(node) in seen:
                continue
            seen.add(id(node))
            result.append(node)
            reference = node.get('$ref', '')
            if reference.startswith('#/$defs/'):
                pending.append(self.definitions.get(reference[len('#/$defs/'):], {}))
            for union in ('oneOf', 'anyOf', 'allOf'):
                pending.extend(node.get(union, []))
        return result

    def _properties(self, nodes: list[dict]) -> dict[str, list[dict]]:
        properties: dict[str, list[dict]] = {}
        for node in self._expanded(nodes):
            for name, child in node.get('properties', {}).items():
                properties.setdefault(name, []).append(child)
        return properties

    def _items(self, nodes: list[dict]) -> list[dict]:
        return [node['items'] for node in self._expanded(nodes)
                if isinstance(node.get('items'), dict)]

    def project(self, value: object) -> dict:
        budget = MAX_SHAPE_NODES
        def visit(item, nodes, depth):
            nonlocal budget
            budget -= 1
            if depth >= MAX_SHAPE_DEPTH or budget <= 0:
                return {'type': _kind(item), 'truncated': True}
            if isinstance(item, dict):
                properties = self._properties(nodes)
                fields, unknown, examined = {}, 0, 0
                for name, child in item.items():
                    if examined >= MAX_SHAPE_NODES or budget <= 0:
                        break
                    examined += 1
                    if name not in properties:
                        unknown += 1
                        continue
                    fields[name] = ('redacted' if name.lower() in SENSITIVE_FIELDS
                                    else visit(child, properties[name], depth + 1))
                return {'type': 'object', 'fields': fields,
                        'unknown_fields': unknown, 'truncated': len(item) > examined}
            if isinstance(item, list):
                values, children = [], self._items(nodes)
                for child in item[:MAX_ARRAY_ITEMS]:
                    if budget <= 0:
                        break
                    values.append(visit(child, children, depth + 1))
                return {'type': 'array', 'items': values,
                        'truncated': len(item) > len(values)}
            return {'type': _kind(item)}
        shape = visit(value, [self.schema], 0)
        if len(_json(shape)) > MAX_SHAPE_BYTES:
            return {'type': _kind(value), 'truncated': True}
        return shape

    def feedback(self, value: object) -> list[dict]:
        if not isinstance(value, dict) or not isinstance(value.get('issues'), list):
            return []
        result = []
        for issue in value['issues'][:MAX_FEEDBACK_ISSUES]:
            if not isinstance(issue, dict):
                continue
            pointer = issue.get('instance_pointer', '')
            parts = pointer[:MAX_FEEDBACK_POINTER_CHARS].split('/', MAX_SHAPE_DEPTH + 1)[1:MAX_SHAPE_DEPTH + 1] if isinstance(pointer, str) else []
            safe, nodes = [], [self.schema]
            for part in parts:
                name = part.replace('~1', '/').replace('~0', '~')
                properties, items = self._properties(nodes), self._items(nodes)
                if name in properties:
                    # Emit the canonical schema name/escaping, not caller text.
                    safe.append(name.replace('~', '~0').replace('/', '~1'))
                    nodes = [] if name.lower() in SENSITIVE_FIELDS else properties[name]
                else:
                    safe.append('*')
                    nodes = items if part.isdecimal() else []
            keyword = issue.get('keyword')
            result.append({'pointer': '/' + '/'.join(safe) if safe else '',
                           'keyword': keyword if isinstance(keyword, str) and keyword in CONSTRAINTS else 'other'})
        return result


@dataclass(frozen=True)
class RecorderConfig:
    database: Path
    deployment: str
    max_calls: int = DEFAULT_MAX_CALLS
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS
    max_bytes: int = DEFAULT_MAX_BYTES

    def __post_init__(self):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', self.deployment):
            raise ValueError('deployment must be a nonsensitive label of 1-64 characters')
        if not 16 <= self.max_calls <= 100_000:
            raise ValueError('max_calls must be in 16..100000')
        if not 60 <= self.max_age_seconds <= 365 * 24 * 60 * 60:
            raise ValueError('max_age_seconds must be in 60..31536000')
        if not 1024 * 1024 <= self.max_bytes <= 1024 * 1024 * 1024:
            raise ValueError('max_bytes must be in 1 MiB..1 GiB')


@dataclass(frozen=True)
class Observation:
    identity: str
    started: float
    operation: str


class StorageRejected(Exception):
    """Fixed operator code; never includes paths, SQL or payloads."""


class InteractionRecorder:
    def __init__(self, config: RecorderConfig, runtime: dict, catalog: list[dict],
                 *, diagnostics: TextIO | None = None) -> None:
        self.config = config
        self.runtime = dict(runtime)
        self._diagnostics = diagnostics if diagnostics is not None else sys.stderr
        self._connection: sqlite3.Connection | None = None
        self._active: dict[str, Observation] = {}
        self._sequence = 0
        self._closed = False
        self.health = {'state': 'starting', 'reason': None, 'recorded_starts': 0,
                       'recorded_terminals': 0, 'dropped_observations': 0,
                       'pruned_interactions': 0}
        self._shapes = {tool['name']: InputShape(tool['inputSchema']) for tool in catalog}
        self._catalog = {tool['name']: {
            'input_digest': _digest(tool['inputSchema']),
            'output_digest': (tool.get('_meta', {}).get('standards-engine/output-schema-digest')
                              or _digest(tool.get('outputSchema'))),
        } for tool in catalog}
        try:
            self._open()
            self.health['state'] = 'healthy'
            self._emit()
        except Exception as error:
            self._degrade(error)

    def _emit(self) -> None:
        try:
            print('standards-engine observer ' + _json(self.health), file=self._diagnostics, flush=True)
        except Exception:
            # Operator stderr can itself be broken. Never change a domain result.
            pass

    def _degrade(self, error: Exception) -> None:
        reason = 'storage-unavailable'
        if isinstance(error, StorageRejected):
            reason = str(error)
        elif isinstance(error, sqlite3.Error):
            reason = {sqlite3.SQLITE_BUSY: 'storage-locked', sqlite3.SQLITE_LOCKED: 'storage-locked',
                      sqlite3.SQLITE_FULL: 'storage-full', sqlite3.SQLITE_CORRUPT: 'storage-corrupt',
                      sqlite3.SQLITE_NOTADB: 'storage-corrupt'}.get(
                          getattr(error, 'sqlite_errorcode', 0) & 255, 'storage-error')
        self.health.update(state='degraded', reason=reason)
        self.health['dropped_observations'] += 1
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
        self._emit()

    def _open(self) -> None:
        path = self.config.database
        if os.name != 'posix':
            raise StorageRejected('unsupported-filesystem')
        # The operator owns the existing directory; no recursive mkdir or changes
        # to existing paths/permissions. O_NOFOLLOW protects the final component.
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            info = os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_nlink != 1:
                raise StorageRejected('unsafe-database-file')
        finally:
            os.close(descriptor)
        db = sqlite3.connect(path, timeout=BUSY_TIMEOUT_MS / 1000, isolation_level=None)
        self._connection = db
        db.execute('PRAGMA foreign_keys=ON')
        db.execute(f'PRAGMA busy_timeout={BUSY_TIMEOUT_MS}')
        db.execute('BEGIN IMMEDIATE')
        try:
            # Reject unsupported capabilities before publishing a migration.
            if db.execute('PRAGMA journal_mode').fetchone()[0] != 'delete':
                raise StorageRejected('unsupported-journal-mode')
            pages = self.config.max_bytes // db.execute('PRAGMA page_size').fetchone()[0]
            if db.execute('PRAGMA page_count').fetchone()[0] > pages:
                raise StorageRejected('database-over-budget')
            db.execute(f'PRAGMA max_page_count={pages}')
            version = db.execute('PRAGMA user_version').fetchone()[0]
            app = db.execute('PRAGMA application_id').fetchone()[0]
            tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            if version == 0 and app == 0 and not tables:
                # Table absence cannot prove privacy: dropped SQLite content may
                # remain in freelist pages or sqlite_master slack. Only a truly
                # new zero-length source is admitted; never wipe/reuse old bytes.
                if info.st_size != 0 or path.stat().st_size != 0:
                    raise StorageRejected('nonpristine-database')
                for statement in SCHEMA_DDL:
                    db.execute(statement)
                db.execute(f'PRAGMA application_id={APPLICATION_ID}')
                db.execute(f'PRAGMA user_version={SCHEMA_VERSION}')
            elif version != SCHEMA_VERSION or app != APPLICATION_ID:
                raise StorageRejected('unsupported-database-schema')
            actual = {row[0]: row[1] for row in db.execute(
                "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
            expected = {statement.split()[2]: statement for statement in SCHEMA_DDL}
            if actual != expected:
                raise StorageRejected('invalid-database-schema')
            db.execute('COMMIT')
        except BaseException:
            db.execute('ROLLBACK')
            raise
        db.execute('PRAGMA synchronous=FULL')
        db.execute('PRAGMA secure_delete=ON')

    def _transaction(self, action):
        db = self._connection
        if db is None:
            self.health['dropped_observations'] += 1
            return False
        try:
            db.execute('BEGIN IMMEDIATE')
            action(db)
            db.execute('COMMIT')
            return True
        except Exception as error:
            try:
                db.execute('ROLLBACK')
            except sqlite3.Error:
                pass
            self._degrade(error)
            return False

    def begin(self, message: object, *, request_bytes: int | None, scope: str,
              parse_error: bool = False) -> Observation | None:
        if self._closed:
            return None
        if self._active:
            self._degrade(StorageRejected('overlapping-recorder-call'))
            return None
        # Notifications have no response pair. Invalid envelopes and parse errors do.
        if (isinstance(message, dict) and 'id' not in message and not parse_error
                and message.get('jsonrpc') == '2.0' and isinstance(message.get('method'), str)):
            return None
        if self._connection is None:
            self.health['dropped_observations'] += 1
            return None
        try:
            params = message.get('params', {}) if isinstance(message, dict) else {}
            params = params if isinstance(params, dict) else {}
            method = message.get('method') if isinstance(message, dict) else None
            method = method if isinstance(method, str) and method in METHODS else 'invalid-json' if parse_error else 'other'
            name = params.get('name')
            operation = name if method == 'tools/call' and isinstance(name, str) and name in self._shapes else 'other'
            shape = self._shapes[operation].project(params.get('arguments', {})) if operation in self._shapes else {}
            arguments = params.get('arguments', {})
            discovery = arguments.get('operation') if isinstance(arguments, dict) else None
            discovery = discovery if operation in {'describe_input', 'describe_output'} and isinstance(discovery, str) and discovery in self._shapes else None
            expected = arguments.get('expected_catalog') if isinstance(arguments, dict) else None
            catalog_state = ('unspecified' if expected is None else 'matches'
                             if expected == self.runtime['catalog_digest'] else 'differs')
            now = time.time()
            observation = Observation(str(uuid.uuid4()), time.monotonic(), operation)
            self._sequence += 1
            pruned = 0
            def write(db):
                nonlocal pruned
                db.execute('INSERT OR IGNORE INTO sessions(id,started,runtime,deployment,catalog) VALUES(?,?,?,?,?)',
                           (self.runtime['instance_id'], now, _json(self.runtime), self.config.deployment, _json(self._catalog)))
                pruned += db.execute('DELETE FROM interactions WHERE started < ?',
                                     (now - self.config.max_age_seconds,)).rowcount
                excess = db.execute('SELECT max(0,count(*)-?) FROM interactions',
                                    (self.config.max_calls - 1,)).fetchone()[0]
                if excess:
                    pruned += db.execute('DELETE FROM interactions WHERE id IN '
                                         '(SELECT id FROM interactions ORDER BY started,id LIMIT ?)', (excess,)).rowcount
                db.execute('DELETE FROM sessions WHERE id != ? AND NOT EXISTS '
                           '(SELECT 1 FROM interactions WHERE session=sessions.id)', (self.runtime['instance_id'],))
                db.execute('UPDATE sessions SET pruned=pruned+? WHERE id=?', (pruned, self.runtime['instance_id']))
                db.execute('INSERT INTO interactions VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                           (observation.identity, self.runtime['instance_id'], self._sequence, now,
                            method, operation, _json(shape), _digest(shape), discovery, catalog_state,
                            request_bytes, scope))
            if not self._transaction(write):
                return None
            self.health['recorded_starts'] += 1
            self.health['pruned_interactions'] += pruned
            self._active[observation.identity] = observation
            return observation
        except Exception as error:
            self._degrade(error)
            return None

    def finish(self, observation: Observation | None, response: object = None,
               *, response_bytes: int | None = None, incomplete: bool = False) -> None:
        if observation is None:
            return
        self._active.pop(observation.identity, None)
        try:
            phase, outcome, feedback = 'end', 'response', []
            if incomplete:
                phase, outcome = 'incomplete', 'unknown'
            elif isinstance(response, dict):
                result = response.get('result', {})
                if 'error' in response:
                    phase = 'error'
                    code = response['error'].get('code')
                    outcome = {-32700: 'parse-error', -32600: 'invalid-envelope',
                               -32601: 'unsupported-method', -32602: 'invalid-parameters',
                               -32000: 'not-ready'}.get(code, 'protocol-error')
                elif isinstance(result, dict):
                    value = result.get('structuredContent', {})
                    if result.get('isError'):
                        phase, outcome = 'error', 'tool-exception' if not value else 'rejected'
                    if isinstance(value, dict):
                        if isinstance(value.get('outcome'), str) and value['outcome'] in OUTCOMES:
                            outcome = value['outcome']
                        elif isinstance(value.get('status'), str) and value['status'] in OUTCOMES:
                            outcome = value['status']
                        if observation.operation in self._shapes:
                            feedback = self._shapes[observation.operation].feedback(value.get('input_feedback'))
                            if 'input_feedback' in value:
                                phase, outcome = 'error', 'input-invalid'
            evicted = False
            def write(db):
                nonlocal evicted
                # Retention in another process may have evicted this start. Do not
                # recreate it or claim a terminal event was retained.
                if not db.execute('SELECT 1 FROM interactions WHERE id=?', (observation.identity,)).fetchone():
                    evicted = True
                    return
                db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?)',
                           (observation.identity, phase, time.time(),
                            max(0, (time.monotonic() - observation.started) * 1000),
                            response_bytes, outcome, _json(feedback)))
            if self._transaction(write):
                if evicted:
                    self.health['dropped_observations'] += 1
                    self._emit()
                else:
                    self.health['recorded_terminals'] += 1
        except Exception as error:
            self._degrade(error)

    def close(self) -> None:
        if self._closed:
            return
        for observation in tuple(self._active.values()):
            self.finish(observation, incomplete=True)
        self._closed = True
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception as error:
                self._degrade(error)
            self._connection = None
        self._emit()


def open_report(database: Path) -> sqlite3.Connection:
    """Operator-only, read-only connection. Never creates/migrates a database."""
    db = sqlite3.connect(database.resolve(strict=True).as_uri() + '?mode=ro', uri=True,
                         timeout=BUSY_TIMEOUT_MS / 1000, isolation_level=None)
    try:
        if (db.execute('PRAGMA application_id').fetchone()[0] != APPLICATION_ID
                or db.execute('PRAGMA user_version').fetchone()[0] != SCHEMA_VERSION):
            raise StorageRejected('unsupported-database-schema')
        db.execute('PRAGMA query_only=ON')
        return db
    except BaseException:
        db.close()
        raise


def report(database: Path, *, limit: int = 100) -> dict:
    if not 1 <= limit <= MAX_REPORT_ROWS:
        raise ValueError('report limit must be in 1..1000')
    db = open_report(database)
    db.row_factory = sqlite3.Row
    try:
        db.execute('BEGIN')  # One consistent read snapshot, including denominators.
        total = db.execute('SELECT count(*) FROM interactions').fetchone()[0]
        terminals = db.execute('SELECT count(*) FROM events').fetchone()[0]
        operations = [dict(row) for row in db.execute(
            'SELECT i.scope,i.method,i.operation,count(*) AS starts,count(e.interaction) AS terminals,'
            'sum(CASE WHEN e.phase=\'error\' THEN 1 ELSE 0 END) AS errors,'
            'sum(CASE WHEN e.interaction IS NULL OR e.phase=\'incomplete\' THEN 1 ELSE 0 END) AS incomplete,'
            'sum(i.request_bytes) AS request_bytes,count(i.request_bytes) AS request_measurements,'
            'sum(e.response_bytes) AS response_bytes,count(e.response_bytes) AS response_measurements,'
            'count(e.duration_ms) AS duration_measurements,'
            'avg(e.duration_ms) AS observed_duration_ms FROM interactions i LEFT JOIN events e '
            'ON e.interaction=i.id GROUP BY i.scope,i.method,i.operation ORDER BY starts DESC,i.scope,i.method,i.operation LIMIT ?', (limit + 1,))]
        operations_truncated = len(operations) > limit
        operations = operations[:limit]
        failures = [dict(row) for row in db.execute(
            'SELECT i.scope,i.operation,i.shape_digest,e.outcome,e.feedback,count(*) AS count FROM interactions i '
            'JOIN events e ON e.interaction=i.id WHERE e.phase=\'error\' '
            'GROUP BY i.scope,i.operation,i.shape_digest,e.outcome,e.feedback ORDER BY count DESC,i.scope,i.operation,i.shape_digest,e.outcome,e.feedback LIMIT ?', (limit + 1,))]
        failures_truncated = len(failures) > limit
        failures = failures[:limit]
        shapes = [dict(row) for row in db.execute(
            'SELECT i.scope,i.operation,i.shape_digest,i.input_shape,count(*) AS starts,'
            'sum(CASE WHEN e.phase=\'error\' THEN 1 ELSE 0 END) AS errors FROM interactions i '
            'LEFT JOIN events e ON e.interaction=i.id WHERE i.method=\'tools/call\' '
            'GROUP BY i.scope,i.operation,i.shape_digest,i.input_shape '
            'ORDER BY starts DESC,i.scope,i.operation,i.shape_digest LIMIT ?', (limit + 1,))]
        shapes_truncated = len(shapes) > limit
        shapes = shapes[:limit]
        for shape in shapes:
            shape['input_shape'] = json.loads(shape['input_shape'])
        for failure in failures:
            failure['feedback'] = json.loads(failure['feedback'])
        sessions = [dict(row) for row in db.execute(
            'SELECT * FROM (SELECT * FROM sessions ORDER BY started DESC,id DESC LIMIT ?) ORDER BY started,id', (limit,))]
        for session in sessions:
            session['runtime'] = json.loads(session['runtime'])
            session['catalog'] = json.loads(session['catalog'])
        # Chronology within a process only: these are observed attempts, not proof
        # of agent intent, a repair relation, or an acquired definition.
        pending = Counter()
        discoveries = Counter()
        success_counts = Counter()
        failure_histograms = {}
        discovery_histograms = {}
        scanned = 0
        for row in db.execute(
            'SELECT * FROM (SELECT i.session,i.ordinal,i.scope,i.operation,i.discovery_operation,e.phase '
            'FROM interactions i LEFT JOIN events e ON e.interaction=i.id '
            'ORDER BY i.started DESC,i.id DESC LIMIT ?) ORDER BY session,ordinal', (MAX_SEQUENCE_SCAN,)):
            scanned += 1
            scope = row['scope']
            key = (row['session'], scope, row['operation'])
            if row['discovery_operation'] and row['phase'] == 'end':
                discoveries[(row['session'], scope, row['discovery_operation'])] += 1
            elif row['operation'] not in {'other', 'describe_input', 'describe_output'}:
                if row['phase'] == 'error':
                    pending[key] += 1
                elif row['phase'] == 'end':
                    success_counts[scope] += 1
                    failure_histograms.setdefault(scope, Counter())[pending.pop(key, 0)] += 1
                    discovery_histograms.setdefault(scope, Counter())[discoveries.pop(key, 0)] += 1
        sequences = []
        for scope, successes in sorted(success_counts.items()):
            errors = failure_histograms[scope]
            discovery = discovery_histograms[scope]
            sequences.append({'scope': scope, 'successful_responses': successes,
                              'preceding_errors_histogram': dict(sorted(errors.items())[:limit]),
                              'preceding_discoveries_histogram': dict(sorted(discovery.items())[:limit]),
                              'histograms_truncated': len(errors) > limit or len(discovery) > limit})
        revisions = {}
        for session in sessions:
            revisions.setdefault(session['runtime']['catalog_digest'], session['catalog'])
        comparisons = []
        digests = list(revisions)
        for before, after in zip(digests, digests[1:]):
            left, right = revisions[before], revisions[after]
            comparisons.append({'before': before, 'after': after,
                                'added': sorted(right.keys() - left.keys()),
                                'removed': sorted(left.keys() - right.keys()),
                                'changed': sorted(name for name in left.keys() & right.keys() if left[name] != right[name])})
        return {'schema_version': SCHEMA_VERSION, 'retained_starts': total,
                'retained_terminals': terminals,
                'unmatched_starts': total - terminals,
                'operations': operations, 'operations_truncated': operations_truncated,
                'failures': failures, 'failures_truncated': failures_truncated, 'shapes': shapes,
                'shapes_truncated': shapes_truncated, 'sessions': sessions,
                'session_rows_truncated': db.execute('SELECT count(*) FROM sessions').fetchone()[0] > limit,
                'catalog_comparisons': comparisons,
                'sequences': sequences, 'sequence_scan_starts': scanned,
                'sequence_scan_truncated': total > scanned,
                'limits': {'group_rows': limit, 'sequence_scan_limit': MAX_SEQUENCE_SCAN,
                           'meaning': 'Retained observations only; unmatched or incomplete outcomes are unknown. '
                           'End means response produced/delivered per scope, not domain completion. '
                           'Sequence denominator is end responses per session/scope/operation in the bounded scan. No cross-process '
                           'continuation or intent is inferred. Retention can remove prior attempts. '
                           'Bytes are serialized JSON/stdio bytes, never tokens or billing. '
                           'Redacted requests cannot be replayed; use independent qualification evidence.'}}
    finally:
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description='Read-only operator MCP observation report; no agent tools.')
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--limit', type=int, default=100)
    arguments = parser.parse_args()
    try:
        print(json.dumps(report(arguments.database, limit=arguments.limit), sort_keys=True, indent=2))
    except (OSError, sqlite3.Error, StorageRejected, ValueError):
        print('Observation report unavailable; check database access and schema.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
