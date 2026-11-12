"""Always-on operator observations. Never an Engine store or an agent tool.

The recorder owns sanitization, SQLite transactions, retention and fail-open
health. Caller values are persisted only through the explicit allow-lists below.
A row that cannot be written waits in a bounded in-memory backlog. A missing
terminal event means unknown outcome; a recorder never manufactures a completion.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
from itertools import islice
import json
import math
import os
from pathlib import Path
import re
import secrets
import sqlite3
import stat
import sys
import time
from typing import Iterable, TextIO
import uuid

SCHEMA_VERSION = 2
APPLICATION_ID = 0x53454F42  # SEOB, separate from every Engine domain database.
DEFAULT_DATABASE_NAME = 'interactions-v2.sqlite3'
DEFAULT_DEPLOYMENT = 'local'
DEFAULT_MAX_CALLS = 10_000
DEFAULT_MAX_AGE_SECONDS = 7 * 24 * 60 * 60
DEFAULT_MAX_BYTES = 32 * 1024 * 1024
BUSY_TIMEOUT_MS = 20      # Lock wait per begin/finish; the backlog delivers later.
OPEN_TIMEOUT_MS = 250     # Lock wait at process start, before any request is served.
CLOSE_TIMEOUT_MS = 5_000  # Lock wait for the last delivery at orderly close.
LOCK_POLL_SECONDS = 0.0005
MAX_BACKLOG = 1_000
MAX_SHAPE_NODES = 64
MAX_SHAPE_DEPTH = 5
MAX_SHAPE_BYTES = 8 * 1024
MAX_ARRAY_ITEMS = 4
MAX_VALUE_CHARS = 200
MAX_VALUE_ITEMS = 32
MAX_VALUE_DEPTH = 3
MAX_VALUE_NODES = 512
MAX_ARGUMENT_BYTES = 8 * 1024
MAX_RESULT_IDS = 128
MAX_FEEDBACK_ISSUES = 8
MAX_FEEDBACK_POINTER_CHARS = 512
MAX_THREAD_CHARS = 256
MAX_REPORT_ROWS = 1000
MAX_SEQUENCE_SCAN = 10_000
TEXT_ROWS = 10
TRUNCATED = '[truncated]'
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
    'fact', 'evidence_ref',  # The Engine's own fixed keywords.
})
OUTCOMES = frozenset({'invalid', 'unsupported', 'unavailable', 'unauthorized', 'stale',
                      'rejected', 'recovery-required', 'needs-action', 'needs-facts',
                      'requires-change', 'complete', 'ready', 'draft', 'applied'})

# Values that may be persisted, by operation. A name absent from these lists is
# never stored as a value; it remains a type in input_shape.
_PAGE = ('limit', 'offset')
_READ = ('target', 'detail', 'include_coverage', 'include_routing')
_RELATED = ('target', 'direction', 'transitive', 'groups')
_DESCRIBE = ('operation', 'selector', *_PAGE)
# Navigation: values exactly as sent. Structured members (snapshot, read_many
# items, route content and facts, handles, nested requests) are projected by
# navigation_values() for the operations named here.
NAVIGATION = {
    'read': _READ, 'read_many': (), 'route': ('detail',), 'routing_facts': (),
    'related': _RELATED, 'relationship_groups': _PAGE, 'inspect': (),
    'describe_input': _DESCRIBE, 'describe_output': _DESCRIBE, 'runtime_info': (),
    'query': (), 'query_proposal': (), 'preview_application': (),
}
HANDLES = {'inspect': 'handle', 'query_proposal': 'revision', 'preview_application': 'revision'}
REQUESTS = {'route': ('kind',), 'read': ('kind', *_READ), 'related': ('kind', *_RELATED)}
# Every other operation is authoring: only these names, and only values shaped
# like a canonical identifier, an enum word, a boolean or a small integer.
IDENTIFIER_FIELDS = frozenset({
    'kind', 'child_kind', 'detail', 'action', 'section', 'result', 'decision', 'owner',
    'disposition', 'relation', 'artifact_kind', 'authority', 'level', 'role', 'origin',
    'lifecycle', 'direction',
    'id', 'policy', 'standard', 'consumer', 'target', 'source_policy', 'subject',
    'evidence_owner', 'after_policy', 'rule', 'fact', 'requires', 'specializes',
    'successors', 'predecessors', 'groups',
    'limit', 'offset', 'apply', 'transitive',
})
IDENTIFIER = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}')
OPAQUE = re.compile(r'[0-9a-fA-F]{16}|[0-9a-f]{8}-[0-9a-f]{4}-')  # Digests, handle ids, UUIDs.
RESULT_KIND = re.compile(r'[a-z][a-z0-9-]{0,63}')
RESULT_CODE = re.compile(r'[A-Z][A-Z0-9_]{0,31}(\.[A-Z][A-Z0-9_]{0,47}){1,3}')


SCHEMA_DDL = (
    'CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)',
    'CREATE TABLE catalogs (digest TEXT PRIMARY KEY, tools TEXT NOT NULL)',
    'CREATE TABLE sessions (id TEXT PRIMARY KEY, started REAL NOT NULL, runtime TEXT NOT NULL, deployment TEXT NOT NULL, catalog TEXT NOT NULL REFERENCES catalogs(digest), client_name TEXT, client_version TEXT, pruned INTEGER NOT NULL DEFAULT 0, lost INTEGER NOT NULL DEFAULT 0)',
    'CREATE TABLE interactions (id TEXT PRIMARY KEY, session TEXT NOT NULL REFERENCES sessions(id), ordinal INTEGER NOT NULL, started REAL NOT NULL, method TEXT NOT NULL, operation TEXT NOT NULL, input_shape TEXT NOT NULL, shape_digest TEXT NOT NULL, discovery_operation TEXT, catalog_state TEXT NOT NULL, request_bytes INTEGER, scope TEXT NOT NULL, arguments TEXT NOT NULL, arguments_bytes INTEGER, thread TEXT, origin TEXT NOT NULL, UNIQUE(session, ordinal))',
    "CREATE TABLE events (interaction TEXT PRIMARY KEY REFERENCES interactions(id) ON DELETE CASCADE, phase TEXT NOT NULL CHECK(phase IN ('end','error','incomplete')), finished REAL NOT NULL, duration_ms REAL NOT NULL, response_bytes INTEGER, outcome TEXT NOT NULL, feedback TEXT NOT NULL, result TEXT NOT NULL, result_bytes INTEGER)",
    'CREATE INDEX interaction_age ON interactions(started)',
)


def default_database() -> Path:
    """${XDG_DATA_HOME:-~/.local/share}/standards-engine/observations/<name>."""
    base = os.environ.get('XDG_DATA_HOME', '')
    base = Path(base) if os.path.isabs(base) else Path.home() / '.local' / 'share'
    return base / 'standards-engine' / 'observations' / DEFAULT_DATABASE_NAME


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


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and abs(value) < 2 ** 53


def _identifier(value: object) -> bool:
    """A canonical identifier or enum word. Prose, digests and handle ids never match."""
    return isinstance(value, str) and bool(IDENTIFIER.fullmatch(value)) and not OPAQUE.search(value)


def _identifiers(values: Iterable[object]) -> list:
    return [value for value in islice(values, MAX_RESULT_IDS) if _identifier(value)]


def _label(value: object) -> str | None:
    """A client's self-reported name or version: bounded printable ASCII."""
    return re.sub(r'[^ -~]', '?', value)[:64] if isinstance(value, str) and value else None


def _sent(value: object, depth: int = 0) -> object:
    """A caller value as sent, bounded. Cut strings and containers carry a marker."""
    if isinstance(value, str):
        return value if len(value) <= MAX_VALUE_CHARS else value[:MAX_VALUE_CHARS] + TRUNCATED
    if value is None or isinstance(value, bool) or _number(value):
        return value
    if isinstance(value, list) and depth < MAX_VALUE_DEPTH:
        kept = [_sent(item, depth + 1) for item in value[:MAX_VALUE_ITEMS]]
        return kept + [TRUNCATED] if len(value) > MAX_VALUE_ITEMS else kept
    if isinstance(value, dict) and depth < MAX_VALUE_DEPTH:
        kept = {_sent(str(name)): _sent(item, depth + 1)
                for name, item in islice(value.items(), MAX_VALUE_ITEMS)}
        if len(value) > MAX_VALUE_ITEMS:
            kept[TRUNCATED] = len(value) - MAX_VALUE_ITEMS
        return kept
    return {'type': _kind(value)}


def _pick(value: object, names: tuple[str, ...]) -> dict:
    """Allow-listed members as sent. A non-object keeps only its type."""
    if not isinstance(value, dict):
        return {'type': _kind(value)}
    return {name: _sent(value[name]) for name in names if name in value}


def _snapshot(handle: object) -> str:
    """Reuse is visible through a short stable hash; the handle id is not kept."""
    identity = handle.get('id') if isinstance(handle, dict) else None
    if not isinstance(identity, str):
        return 'malformed'
    return hashlib.sha256(identity.encode('utf-8', 'replace')).hexdigest()[:12]


def navigation_values(operation: str, arguments: dict) -> dict:
    """The recorded values of one navigation call, from its explicit allow-list."""
    values = _pick(arguments, NAVIGATION[operation])
    if 'snapshot' in arguments:
        values['snapshot'] = _snapshot(arguments['snapshot'])
    handle = HANDLES.get(operation)
    if handle in arguments:
        values[handle] = _pick(arguments[handle], ('kind', 'child_kind'))
    if operation == 'read_many' and isinstance(arguments.get('items'), list):
        values['items'] = [_pick(item, _READ) for item in arguments['items'][:MAX_VALUE_ITEMS]]
    if operation == 'route':
        if 'content' in arguments:
            values['content'] = _pick(arguments['content'], _PAGE)
        if 'facts' in arguments:
            # Names and values exactly as sent: invented facts are the signal.
            values['facts'] = _sent(arguments['facts'])
    request = arguments.get('request')
    if operation in ('query', 'query_proposal', 'preview_application') and isinstance(request, dict):
        kind = request.get('kind')
        values['request'] = _pick(request, REQUESTS.get(kind if isinstance(kind, str) else '', ('kind',)))
        if 'facts' in request:
            values['request']['facts'] = _sent(request['facts'])
    return values


def _recorded_facts(values: dict) -> dict:
    """Route facts inside a recorded arguments object, top-level or in a nested request."""
    request = values.get('request')
    facts = values.get('facts', request.get('facts') if isinstance(request, dict) else None)
    return facts if isinstance(facts, dict) else {}


def _bounded(values: dict) -> dict:
    """Whole-object cap: an oversized projection keeps its scalars and says so."""
    if len(_json(values)) <= MAX_ARGUMENT_BYTES:
        return values
    return {'truncated': True, **{name: value for name, value in values.items()
                                  if not isinstance(value, (dict, list))}}


def _thread(meta: object) -> tuple[str | None, str]:
    """Client thread id (hashed with the database salt before storage) and origin.

    Codex supplies both in x-codex-turn-metadata. No other _meta member is read,
    so workspace paths, repository URLs, models and turn ids never reach storage.
    """
    meta = meta if isinstance(meta, dict) else {}
    turn = meta.get('x-codex-turn-metadata')
    turn = turn if isinstance(turn, dict) else {}
    candidates = (turn.get('thread_id'), meta.get('threadId'), turn.get('session_id'), meta.get('sessionId'))
    identity = next((value[:MAX_THREAD_CHARS] for value in candidates
                     if isinstance(value, str) and value), None)
    source = turn.get('thread_source')
    origin = {'user': 'main', 'subagent': 'subagent'}.get(source, 'unknown') if isinstance(source, str) else 'unknown'
    return identity, origin


def _returned(read: object) -> object:
    """The canonical id a read result is about, wherever that result kind keeps it."""
    if not isinstance(read, dict):
        return None
    policy = read.get('policy')
    if isinstance(policy, dict):
        handle = policy.get('handle')
        return policy.get('id') or (handle.get('child_id') if isinstance(handle, dict) else None)
    return read.get('canonical_id')


def result_summary(value: dict) -> dict:
    """Engine-produced identifiers and counts from structuredContent; never text."""
    summary = {}
    for name, pattern in (('kind', RESULT_KIND), ('code', RESULT_CODE)):
        if isinstance(value.get(name), str) and pattern.fullmatch(value[name]):
            summary[name] = value[name]
    for name in ('status', 'outcome'):
        if isinstance(value.get(name), str) and value[name] in OUTCOMES:
            summary[name] = value[name]
    plan, questions, page = value.get('reading_plan'), value.get('unresolved_questions'), value.get('content')
    if isinstance(plan, list):
        summary['selected'] = _identifiers(entry.get('target') for entry in plan
                                           if isinstance(entry, dict) and entry.get('state') == 'selected')
    if isinstance(questions, list):
        summary['unresolved'] = _identifiers(question['fact'].get('id') for question in questions
                                             if isinstance(question, dict) and isinstance(question.get('fact'), dict))
    if isinstance(page, dict):  # A route's content page. A read's content is text and is not inspected.
        items = page.get('items') if isinstance(page.get('items'), list) else []
        summary['content'] = {**{name: page[name] for name in ('offset', 'total') if _number(page.get(name))},
                              'items': len(items), 'targets': _identifiers(map(_returned, items))}
    reads = value['items'] if isinstance(value.get('items'), list) else [value]
    targets = _identifiers(map(_returned, reads))
    if targets:
        summary['targets'] = targets
    return summary


class InputShape:
    """Disclosure projections of one operation's input, not a second validator.

    Static property names come only from the installed schema. Unknown names
    disappear before SQLite sees anything. Sensitive children are not traversed
    even if their properties occur elsewhere in the schema.
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
        """Value-free structure: every scalar becomes only its type."""
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

    def identifiers(self, value: object) -> dict:
        """Authoring calls: identifiers and enums at schema-declared, allow-listed names.

        The walk follows project(): dynamic keys and sensitive subtrees are never
        entered, nor are evidence references under their other name. A string
        survives only if it has the shape of an identifier, so prose placed in an
        identifier field is dropped like any body or rationale.
        """
        budget = MAX_VALUE_NODES
        def visit(item, nodes, name, depth):
            nonlocal budget
            budget -= 1
            if budget <= 0 or depth > 2 * MAX_SHAPE_DEPTH:
                return None
            if isinstance(item, dict):
                properties, kept = self._properties(nodes), {}
                for key, child in islice(item.items(), MAX_SHAPE_NODES):
                    if (key in properties and key.lower() not in SENSITIVE_FIELDS
                            and key != 'explicit_exclusions'):
                        found = visit(child, properties[key], key, depth + 1)
                        if found is not None and found != {} and found != []:
                            kept[key] = found
                return kept
            if isinstance(item, list):
                children = self._items(nodes)
                found = [visit(child, children, name, depth + 1) for child in item[:MAX_VALUE_ITEMS]]
                return [entry for entry in found if entry is not None and entry != {} and entry != []]
            if name in IDENTIFIER_FIELDS and (isinstance(item, bool) or _number(item) or _identifier(item)):
                return item
            return None
        found = visit(value, [self.schema], '', 0)
        return found if isinstance(found, dict) else {}

    def feedback(self, value: object, names: frozenset = frozenset()) -> list[dict]:
        """Validation locations. `names` are route fact names this call already recorded."""
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
                    known = bool(safe) and safe[-1] == 'facts' and name in names
                    safe.append(name.replace('~', '~0').replace('/', '~1') if known else '*')
                    nodes = items if part.isdecimal() else []
            keyword = issue.get('keyword')
            result.append({'pointer': '/' + '/'.join(safe) if safe else '',
                           'keyword': keyword if isinstance(keyword, str) and keyword in CONSTRAINTS else 'other'})
        return result


@dataclass(frozen=True)
class RecorderConfig:
    database: Path | None = None  # None selects default_database().
    deployment: str = DEFAULT_DEPLOYMENT
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
    facts: frozenset = frozenset()


class StorageRejected(Exception):
    """Fixed operator code; never includes paths, SQL or payloads."""


def _busy(error: Exception) -> bool:
    return (isinstance(error, sqlite3.Error) and getattr(error, 'sqlite_errorcode', 0) & 255
            in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED))


def _deadline(wait_ms: int) -> float:
    return time.monotonic() + wait_ms / 1000


def _locked(db: sqlite3.Connection, deadline: float, statement: str = 'BEGIN IMMEDIATE') -> sqlite3.Cursor:
    """Run a statement that needs the write lock, polling until the deadline.

    SQLite's own busy handler backs off in steps of up to 25 ms, far coarser than
    a lock that other recorders hold for microseconds, so connections use none.
    """
    while True:
        try:
            return db.execute(statement)
        except sqlite3.OperationalError as error:
            if not _busy(error) or time.monotonic() >= deadline:
                raise
            time.sleep(LOCK_POLL_SECONDS)


class InteractionRecorder:
    def __init__(self, config: RecorderConfig, runtime: dict, catalog: list[dict],
                 *, diagnostics: TextIO | None = None) -> None:
        self.config = config
        self.runtime = dict(runtime)
        self._diagnostics = diagnostics if diagnostics is not None else sys.stderr
        self._connection: sqlite3.Connection | None = None
        self._salt = b''
        self._pages = 0
        self._active: dict[str, Observation] = {}
        self._backlog: deque[tuple[str, tuple]] = deque()
        self._unsaved_lost = 0
        self._started = time.time()
        self._client: tuple[str | None, str | None] = (None, None)
        self._sequence = 0
        self._closed = False
        self._silent = True
        self.health = {'state': 'starting', 'reason': None, 'recorded_starts': 0,
                       'recorded_terminals': 0, 'backlog': 0, 'lost': 0,
                       'pruned_interactions': 0}
        self._shapes = {tool['name']: InputShape(tool['inputSchema']) for tool in catalog}
        self._catalog = _json({tool['name']: {
            'input_digest': _digest(tool['inputSchema']),
            'output_digest': (tool.get('_meta', {}).get('standards-engine/output-schema-digest')
                              or _digest(tool.get('outputSchema'))),
        } for tool in catalog})
        try:
            self._connection = self._open(_deadline(OPEN_TIMEOUT_MS))
            self._note('healthy')
        except Exception as error:
            self._degrade(error)

    def _emit(self) -> None:
        self._silent = False
        try:
            print('standards-engine observer ' + _json(self.health), file=self._diagnostics, flush=True)
        except Exception:
            # Operator stderr can itself be broken. Never change a domain result.
            pass

    def _note(self, state: str, reason: str | None = None) -> None:
        """Operator stderr only when health changes; a healthy recorder is silent."""
        previous = (self.health['state'], self.health['reason'])
        self.health.update(state=state, reason=reason, backlog=len(self._backlog))
        if previous != (state, reason) and 'degraded' in (previous[0], state):
            self._emit()

    def _degrade(self, error: Exception) -> None:
        """Keep the backlog. Reconnect on a later call unless the database was only busy."""
        reason = 'storage-unavailable'
        if isinstance(error, StorageRejected):
            reason = str(error)
        elif _busy(error):
            reason = 'storage-locked'
        elif isinstance(error, sqlite3.Error):
            reason = {sqlite3.SQLITE_FULL: 'storage-full', sqlite3.SQLITE_CORRUPT: 'storage-corrupt',
                      sqlite3.SQLITE_NOTADB: 'storage-corrupt'}.get(
                          getattr(error, 'sqlite_errorcode', 0) & 255, 'storage-error')
        if reason != 'storage-locked' and self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
        self._note('degraded', reason)

    def _lose(self, rows: int) -> None:
        self.health['lost'] += rows
        self._unsaved_lost += rows

    def _open(self, deadline: float) -> sqlite3.Connection:
        if os.name != 'posix':
            raise StorageRejected('unsupported-filesystem')
        path = self.config.database
        if path is None:
            # Only the default location is created. An operator-supplied directory
            # must already exist; existing paths and permissions are never changed.
            path = default_database()
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # O_NOFOLLOW protects the final component.
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            info = os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_nlink != 1:
                raise StorageRejected('unsafe-database-file')
        finally:
            os.close(descriptor)
        db = sqlite3.connect(path, timeout=0, isolation_level=None)
        try:
            db.execute('PRAGMA foreign_keys=ON')
            _locked(db, deadline)
            try:
                # Reject unsupported capabilities before publishing a migration.
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
                    # Simultaneous creators queue on this lock: the first publishes
                    # the whole schema in one commit and the rest find it complete.
                    if info.st_size != 0 or path.stat().st_size != 0:
                        raise StorageRejected('nonpristine-database')
                    for statement in SCHEMA_DDL:
                        db.execute(statement)
                    db.execute("INSERT INTO meta VALUES('salt',?)", (secrets.token_hex(16),))
                    db.execute(f'PRAGMA application_id={APPLICATION_ID}')
                    db.execute(f'PRAGMA user_version={SCHEMA_VERSION}')
                elif version != SCHEMA_VERSION or app != APPLICATION_ID:
                    # Includes schema v1: historical evidence, never migrated or deleted.
                    raise StorageRejected('unsupported-database-schema')
                actual = {row[0]: row[1] for row in db.execute(
                    "SELECT name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'")}
                expected = {statement.split()[2]: statement for statement in SCHEMA_DDL}
                if actual != expected:
                    raise StorageRejected('invalid-database-schema')
                salt = bytes.fromhex(db.execute("SELECT value FROM meta WHERE key='salt'").fetchone()[0])
                _locked(db, deadline, 'COMMIT')
            except BaseException:
                db.execute('ROLLBACK')
                raise
            # WAL keeps the write lock to microseconds (no fsync per commit) and lets
            # a report read while servers write. Idempotent for every later opener.
            if _locked(db, deadline, 'PRAGMA journal_mode=WAL').fetchone()[0] != 'wal':
                raise StorageRejected('unsupported-journal-mode')
            db.execute('PRAGMA synchronous=NORMAL')
            db.execute('PRAGMA secure_delete=ON')
        except BaseException:
            db.close()
            raise
        self._salt, self._pages = salt, pages
        return db

    def _pseudonym(self, thread: str | None) -> str | None:
        if thread is None:
            return None
        return hmac.new(self._salt, thread.encode('utf-8', 'replace'), 'sha256').hexdigest()[:16]

    def _write(self, db: sqlite3.Connection) -> tuple[Counter, int, int]:
        """One transaction: prune to policy, then store the whole backlog in order."""
        session, now = self.runtime['instance_id'], time.time()
        starts = sum(kind == 'start' for kind, _ in self._backlog)
        pruned = 0
        if starts:
            pruned = db.execute('DELETE FROM interactions WHERE started < ?',
                                (now - self.config.max_age_seconds,)).rowcount
            count = db.execute('SELECT count(*) FROM interactions').fetchone()[0]
            excess = max(0, count + starts - self.config.max_calls)
            used = db.execute('PRAGMA page_count').fetchone()[0] - db.execute('PRAGMA freelist_count').fetchone()[0]
            if used > self._pages - self._pages // 16:
                # The byte cap bounds retention like the count cap: a nearly full file
                # gives up its oldest sixteenth instead of refusing new observations.
                excess = max(excess, count // 16 + starts)
            if excess:
                pruned += db.execute('DELETE FROM interactions WHERE id IN '
                                     '(SELECT id FROM interactions ORDER BY started,id LIMIT ?)', (excess,)).rowcount
        if pruned:
            # A session that only carries a loss count stays until it ages out.
            db.execute('DELETE FROM sessions WHERE id != ? AND (lost = 0 OR started < ?) AND NOT EXISTS '
                       '(SELECT 1 FROM interactions WHERE session=sessions.id)',
                       (session, now - self.config.max_age_seconds))
            db.execute('DELETE FROM catalogs WHERE digest NOT IN (SELECT catalog FROM sessions)')
        catalog = _digest(self._catalog)
        db.execute('INSERT OR IGNORE INTO catalogs VALUES(?,?)', (catalog, self._catalog))
        db.execute('INSERT OR IGNORE INTO sessions(id,started,runtime,deployment,catalog) VALUES(?,?,?,?,?)',
                   (session, self._started, _json(self.runtime), self.config.deployment, catalog))
        recorded = Counter()
        for kind, row in self._backlog:
            if kind == 'start':
                recorded[kind] += db.execute(
                    'INSERT OR IGNORE INTO interactions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (*row[:-2], self._pseudonym(row[-2]), row[-1])).rowcount
            else:
                # Retention or a backlog overflow may have removed this start. Do
                # not recreate it or claim a terminal event was retained.
                recorded[kind] += db.execute(
                    'INSERT OR IGNORE INTO events SELECT ?,?,?,?,?,?,?,?,? WHERE EXISTS '
                    '(SELECT 1 FROM interactions WHERE id=?)', (*row, row[0])).rowcount
        orphans = len(self._backlog) - starts - recorded['end']
        db.execute('UPDATE sessions SET client_name=?,client_version=?,pruned=pruned+?,lost=lost+? WHERE id=?',
                   (*self._client, pruned, self._unsaved_lost + orphans, session))
        return recorded, pruned, orphans

    def _flush(self, wait_ms: int) -> None:
        """Deliver the backlog, or keep all of it for a later call. Never raises."""
        if not self._backlog and not self._unsaved_lost:
            return
        deadline = _deadline(wait_ms)
        try:
            if self._connection is None:
                self._connection = self._open(deadline)
            db = self._connection
            _locked(db, deadline)
            try:
                recorded, pruned, orphans = self._write(db)
                db.execute('COMMIT')
            except BaseException:
                try:
                    db.execute('ROLLBACK')
                except sqlite3.Error:
                    pass
                raise
        except Exception as error:
            self._degrade(error)
            return
        self._backlog.clear()
        self._unsaved_lost = 0
        self.health['recorded_starts'] += recorded['start']
        self.health['recorded_terminals'] += recorded['end']
        self.health['pruned_interactions'] += pruned
        self.health['lost'] += orphans
        self._note('healthy')

    def _record(self, kind: str, row: tuple) -> None:
        if len(self._backlog) >= MAX_BACKLOG:
            # Bounded memory: the oldest waiting row gives way and is counted.
            self._backlog.popleft()
            self._lose(1)
        self._backlog.append((kind, row))
        self._flush(BUSY_TIMEOUT_MS)

    def begin(self, message: object, *, request_bytes: int | None, scope: str,
              parse_error: bool = False) -> Observation | None:
        if self._closed:
            return None
        # Notifications have no response pair. Invalid envelopes and parse errors do.
        if (isinstance(message, dict) and 'id' not in message and not parse_error
                and message.get('jsonrpc') == '2.0' and isinstance(message.get('method'), str)):
            return None
        try:
            params = message.get('params', {}) if isinstance(message, dict) else {}
            params = params if isinstance(params, dict) else {}
            method = message.get('method') if isinstance(message, dict) else None
            method = method if isinstance(method, str) and method in METHODS else 'invalid-json' if parse_error else 'other'
            name = params.get('name')
            operation = name if method == 'tools/call' and isinstance(name, str) and name in self._shapes else 'other'
            arguments = params.get('arguments', {})
            shape, values, arguments_bytes = {}, {}, None
            if operation in self._shapes:
                shape = self._shapes[operation].project(arguments)
                if operation not in NAVIGATION:
                    values = self._shapes[operation].identifiers(arguments)
                elif isinstance(arguments, dict):
                    values = navigation_values(operation, arguments)
                values = _bounded(values)
                try:
                    arguments_bytes = len(json.dumps(arguments, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
                except Exception:
                    pass
            discovery = arguments.get('operation') if isinstance(arguments, dict) else None
            discovery = discovery if operation in {'describe_input', 'describe_output'} and isinstance(discovery, str) and discovery in self._shapes else None
            expected = arguments.get('expected_catalog') if isinstance(arguments, dict) else None
            catalog_state = ('unspecified' if expected is None else 'matches'
                             if expected == self.runtime['catalog_digest'] else 'differs')
            if method == 'initialize' and self._client == (None, None):
                client = params.get('clientInfo')
                client = client if isinstance(client, dict) else {}
                self._client = (_label(client.get('name')), _label(client.get('version')))
            thread, origin = _thread(params.get('_meta'))
            observation = Observation(str(uuid.uuid4()), time.monotonic(), operation,
                                      frozenset(_recorded_facts(values)))
            self._sequence += 1
            row = (observation.identity, self.runtime['instance_id'], self._sequence, time.time(),
                   method, operation, _json(shape), _digest(shape), discovery, catalog_state,
                   request_bytes, scope, _json(values), arguments_bytes, thread, origin)
            self._active[observation.identity] = observation
            self._record('start', row)
            return observation
        except Exception:
            self._lose(1)
            self._note('degraded', 'recorder-error')
            return None

    def finish(self, observation: Observation | None, response: object = None,
               *, response_bytes: int | None = None, incomplete: bool = False) -> None:
        if observation is None:
            return
        self._active.pop(observation.identity, None)
        try:
            phase, outcome, feedback, summary, result_bytes = 'end', 'response', [], {}, None
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
                        summary = result_summary(value)
                        if 'structuredContent' in result:
                            try:
                                # One serialization: the text copy the transport already made.
                                result_bytes = len(result['content'][0]['text'].encode('utf-8'))
                            except Exception:
                                pass
                        if observation.operation in self._shapes:
                            feedback = self._shapes[observation.operation].feedback(
                                value.get('input_feedback'), observation.facts)
                            if 'input_feedback' in value:
                                phase, outcome = 'error', 'input-invalid'
            self._record('end', (observation.identity, phase, time.time(),
                                 max(0, (time.monotonic() - observation.started) * 1000),
                                 response_bytes, outcome, _json(feedback), _json(summary), result_bytes))
        except Exception:
            self._lose(1)
            self._note('degraded', 'recorder-error')

    def close(self) -> None:
        if self._closed:
            return
        for observation in tuple(self._active.values()):
            self.finish(observation, incomplete=True)
        self._closed = True
        self._flush(CLOSE_TIMEOUT_MS)
        if self._backlog:
            # The process is ending: nothing can deliver these rows any more.
            # Save the count if the database can still be reached at all.
            self._lose(len(self._backlog))
            self._backlog.clear()
            self._flush(BUSY_TIMEOUT_MS)
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
        self.health['backlog'] = 0
        if not self._silent or self.health['lost']:
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


def _percentile(values: list, fraction: float):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(fraction * len(ordered)) - 1)] if ordered else None


def _top(counter: Counter, limit: int, *names: str) -> list[dict]:
    """Most common keys as rows; ties break on the key so reports are stable."""
    rows = sorted(counter.items(), key=lambda item: (-item[1], _json(item[0])))[:limit]
    return [{**dict(zip(names, key if isinstance(key, tuple) else (key,))), 'count': count}
            for key, count in rows]


def _fact_values(value: object) -> list[str]:
    """The vocabulary words inside one routing fact value as sent."""
    if isinstance(value, dict):  # Native typed form {type, state, value}.
        value = value.get('value')
    return [item for item in (value if isinstance(value, list) else [value]) if isinstance(item, str)]


def _usage(db: sqlite3.Connection, since: float, limit: int) -> dict:
    """What agents asked for and what came back, from the recorded values."""
    sessions = {}
    for row in db.execute('SELECT id,runtime,client_name,client_version FROM sessions'):
        runtime = json.loads(row['runtime'])
        sessions[row['id']] = (' '.join(filter(None, (row['client_name'], row['client_version']))) or 'unknown',
                               runtime.get('purpose'), runtime.get('interface_version'))
    clients, calls, rejected = {}, Counter(), Counter()
    durations, sizes = {}, {}
    rejections, read_targets, origins, tool_calls = Counter(), Counter(), {}, Counter()
    reads, accepted, declared, refused = {}, {}, set(), []
    routes = without_snapshot = 0
    for row in db.execute(
            'SELECT i.session,i.method,i.operation,i.arguments,i.thread,i.origin,e.phase,e.outcome,'
            'e.feedback,e.duration_ms,e.result,e.result_bytes FROM interactions i LEFT JOIN events e '
            'ON e.interaction=i.id WHERE i.started >= ? ORDER BY i.started,i.id', (since,)):
        client = clients.setdefault(sessions.get(row['session'], ('unknown', None, None)), [set(), 0])
        client[0].add(row['session'])
        client[1] += 1
        thread = row['thread'] or 'process:' + row['session']
        if row['method'] == 'tools/call':
            origins[thread] = row['origin']
            tool_calls[thread] += 1
        operation = row['operation'] if row['method'] == 'tools/call' else row['method']
        calls[operation] += 1
        if row['duration_ms'] is not None:
            durations.setdefault(operation, []).append(row['duration_ms'])
        if row['result_bytes'] is not None:
            sizes.setdefault(operation, []).append(row['result_bytes'])
        arguments = json.loads(row['arguments'])
        result = json.loads(row['result']) if row['result'] else {}
        facts = _recorded_facts(arguments)
        if row['operation'] == 'route':
            routes += 1
            without_snapshot += 'snapshot' not in arguments
        if row['phase'] == 'end':
            declared.update(result.get('unresolved', ()))
            for name, value in facts.items():
                accepted.setdefault(name, set()).update(_fact_values(value))
            delivered = result.get('targets', []) + result.get('content', {}).get('targets', [])
            read_targets.update(delivered)
            if delivered:
                reads.setdefault(thread, Counter()).update(delivered)
        elif row['phase'] == 'error' and row['method'] == 'tools/call':
            rejected[operation] += 1
            issue = (json.loads(row['feedback']) or [{}])[0]
            # The offending value is whatever the validation pointer names in the
            # recorded arguments; without a pointer, everything recorded but the snapshot.
            value = arguments
            for part in issue.get('pointer', '').split('/')[1:]:
                part = part.replace('~1', '/').replace('~0', '~')
                inner = (value.get(part) if isinstance(value, dict)
                         else value[int(part)] if isinstance(value, list) and part.isdecimal() and int(part) < len(value)
                         else None)
                if inner is None:
                    break
                value = inner
            if value is arguments:
                value = {name: item for name, item in arguments.items() if name != 'snapshot'}
            rejections[(operation, result.get('code') or row['outcome'], issue.get('pointer', ''),
                        issue.get('keyword', ''), _json(value)[:MAX_VALUE_CHARS])] += 1
            if issue.get('keyword') == 'fact':
                pointed = issue['pointer'].rpartition('/facts/')[2].replace('~1', '/').replace('~0', '~')
                refused.append((facts, pointed if '/facts/' in issue['pointer'] else None))
    # Out-of-vocabulary is inferred, never looked up: a name or value counts when
    # the server refused its route and never accepted or asked for it in this window.
    names, values = Counter(), Counter()
    for facts, pointed in refused:
        names.update(name for name in facts if name not in accepted and name not in declared)
        for name in ([pointed] if pointed in facts else []):
            values.update((name, word) for word in _fact_values(facts[name])
                          if word not in accepted.get(name, ()))
    repeats = {thread: sum(seen.values()) - len(seen) for thread, seen in reads.items()}
    total_reads = sum(sum(seen.values()) for seen in reads.values())
    threads = {}
    for thread, origin in origins.items():
        entry = threads.setdefault(origin, {'origin': origin, 'threads': 0, 'calls': 0, 'reads': 0, 'repeats': 0})
        entry['threads'] += 1
        entry['calls'] += tool_calls[thread]
        entry['reads'] += sum(reads.get(thread, {}).values())
        entry['repeats'] += repeats.get(thread, 0)
    return {
        'clients': [{'client': key[0], 'purpose': key[1], 'interface_version': key[2],
                     'sessions': len(value[0]), 'calls': value[1]}
                    for key, value in sorted(clients.items(), key=lambda item: (-item[1][1], _json(item[0])))][:limit],
        'usage': [{'operation': operation, 'calls': count, 'rejected': rejected[operation],
                   'rejection_rate': rejected[operation] / count,
                   'duration_p50_ms': _percentile(durations.get(operation, []), 0.5),
                   'duration_p90_ms': _percentile(durations.get(operation, []), 0.9),
                   'duration_max_ms': max(durations.get(operation, []), default=None),
                   'result_p50_bytes': _percentile(sizes.get(operation, []), 0.5),
                   'result_max_bytes': max(sizes.get(operation, []), default=None)}
                  for operation, count in sorted(calls.items(), key=lambda item: (-item[1], item[0]))][:limit],
        'rejections': _top(rejections, limit, 'operation', 'code', 'pointer', 'keyword', 'value'),
        'unaccepted_facts': {'names': _top(names, limit, 'name'), 'values': _top(values, limit, 'fact', 'value')},
        'read_targets': _top(read_targets, limit, 'target'),
        'repeat_reads': {'reads': total_reads, 'repeats': sum(repeats.values()), 'threads': len(reads),
                         'threads_repeating': sum(count > 0 for count in repeats.values()),
                         'worst_thread_rate': max((count / sum(reads[thread].values())
                                                   for thread, count in repeats.items() if count), default=0.0)},
        'routes': {'calls': routes, 'without_snapshot': without_snapshot},
        'threads': [threads[origin] for origin in sorted(threads)],
    }


def report(database: Path, *, limit: int = 100, since_days: float | None = None) -> dict:
    if not 1 <= limit <= MAX_REPORT_ROWS:
        raise ValueError('report limit must be in 1..1000')
    if since_days is not None and not 0 < since_days <= 3650:
        raise ValueError('since_days must be in 0..3650')
    since = time.time() - since_days * 24 * 60 * 60 if since_days is not None else 0.0
    db = open_report(database)
    db.row_factory = sqlite3.Row
    try:
        db.execute('BEGIN')  # One consistent read snapshot, including denominators.
        total, first, last = db.execute('SELECT count(*),min(started),max(started) FROM interactions '
                                        'WHERE started >= ?', (since,)).fetchone()
        terminals = db.execute('SELECT count(*) FROM events e JOIN interactions i ON i.id=e.interaction '
                               'WHERE i.started >= ?', (since,)).fetchone()[0]
        lost, pruned = db.execute('SELECT coalesce(sum(lost),0),coalesce(sum(pruned),0) FROM sessions').fetchone()
        operations = [dict(row) for row in db.execute(
            'SELECT i.scope,i.method,i.operation,count(*) AS starts,count(e.interaction) AS terminals,'
            'sum(CASE WHEN e.phase=\'error\' THEN 1 ELSE 0 END) AS errors,'
            'sum(CASE WHEN e.interaction IS NULL OR e.phase=\'incomplete\' THEN 1 ELSE 0 END) AS incomplete,'
            'sum(i.request_bytes) AS request_bytes,count(i.request_bytes) AS request_measurements,'
            'sum(i.arguments_bytes) AS arguments_bytes,count(i.arguments_bytes) AS arguments_measurements,'
            'sum(e.response_bytes) AS response_bytes,count(e.response_bytes) AS response_measurements,'
            'sum(e.result_bytes) AS result_bytes,count(e.result_bytes) AS result_measurements,'
            'count(e.duration_ms) AS duration_measurements,'
            'avg(e.duration_ms) AS observed_duration_ms FROM interactions i LEFT JOIN events e '
            'ON e.interaction=i.id WHERE i.started >= ? GROUP BY i.scope,i.method,i.operation '
            'ORDER BY starts DESC,i.scope,i.method,i.operation LIMIT ?', (since, limit + 1))]
        operations_truncated = len(operations) > limit
        operations = operations[:limit]
        failures = [dict(row) for row in db.execute(
            'SELECT i.scope,i.operation,i.shape_digest,e.outcome,e.feedback,count(*) AS count FROM interactions i '
            'JOIN events e ON e.interaction=i.id WHERE e.phase=\'error\' AND i.started >= ? '
            'GROUP BY i.scope,i.operation,i.shape_digest,e.outcome,e.feedback ORDER BY count DESC,i.scope,i.operation,i.shape_digest,e.outcome,e.feedback LIMIT ?', (since, limit + 1))]
        failures_truncated = len(failures) > limit
        failures = failures[:limit]
        shapes = [dict(row) for row in db.execute(
            'SELECT i.scope,i.operation,i.shape_digest,i.input_shape,count(*) AS starts,'
            'sum(CASE WHEN e.phase=\'error\' THEN 1 ELSE 0 END) AS errors FROM interactions i '
            'LEFT JOIN events e ON e.interaction=i.id WHERE i.method=\'tools/call\' AND i.started >= ? '
            'GROUP BY i.scope,i.operation,i.shape_digest,i.input_shape '
            'ORDER BY starts DESC,i.scope,i.operation,i.shape_digest LIMIT ?', (since, limit + 1))]
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
            'FROM interactions i LEFT JOIN events e ON e.interaction=i.id WHERE i.started >= ? '
            'ORDER BY i.started DESC,i.id DESC LIMIT ?) ORDER BY session,ordinal', (since, MAX_SEQUENCE_SCAN)):
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
        # Each distinct catalog is stored once; compare them in order of first use.
        revisions = {}
        for session in sessions:
            revisions.setdefault(session['runtime'].get('catalog_digest'), session['catalog'])
        tools = {digest: json.loads(db.execute('SELECT tools FROM catalogs WHERE digest=?', (digest,)).fetchone()[0])
                 for digest in set(revisions.values())}
        comparisons = []
        digests = list(revisions)
        for before, after in zip(digests, digests[1:]):
            left, right = tools[revisions[before]], tools[revisions[after]]
            comparisons.append({'before': before, 'after': after,
                                'added': sorted(right.keys() - left.keys()),
                                'removed': sorted(left.keys() - right.keys()),
                                'changed': sorted(name for name in left.keys() & right.keys() if left[name] != right[name])})
        return {'schema_version': SCHEMA_VERSION, 'since_days': since_days,
                'first_start': first, 'last_start': last, 'retained_starts': total,
                'retained_terminals': terminals,
                'unmatched_starts': total - terminals,
                'lost_rows': lost, 'pruned_interactions': pruned,
                **_usage(db, since, limit),
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
                           'Sequence denominator is end responses per session/scope/operation in the bounded scan. '
                           'A thread is a hashed client thread id, or the server process when the client sent none. '
                           'Unaccepted facts are inferred from refused routes, not checked against a vocabulary. '
                           'Retention can remove prior attempts; lost_rows and pruned_interactions cover retained sessions. '
                           'Bytes are serialized JSON/stdio bytes, never tokens or billing. '
                           'Recorded requests cannot be replayed; use independent qualification evidence.'}}
    finally:
        db.close()


def _stamp(seconds: float | None) -> str:
    return datetime.fromtimestamp(seconds, timezone.utc).strftime('%Y-%m-%d %H:%M') if seconds else '-'


def _amount(value: float | None, unit: str = '') -> str:
    if value is None:
        return '-'
    if unit == 'B':
        return (f'{value} B' if value < 1000 else f'{value / 1000:.1f} kB' if value < 1_000_000
                else f'{value / 1_000_000:.1f} MB')
    return f'{value:.1f}' if value < 10 else f'{value:.0f}'


def _share(part: int, whole: int) -> str:
    return f'{part} of {whole} ({100 * part / whole:.1f}%)' if whole else '0 of 0'


def text_report(summary: dict) -> str:
    """About a screenful for a person; the JSON form holds every row."""
    window = f'last {summary["since_days"]:g} days' if summary['since_days'] else 'all retained'
    lines = [
        f'Standards Engine MCP observations, schema v{summary["schema_version"]} ({window})',
        f'{_stamp(summary["first_start"])} to {_stamp(summary["last_start"])} UTC',
        f'{summary["retained_starts"]} calls: {summary["unmatched_starts"]} without an outcome '
        f'(process ended mid-call), {summary["lost_rows"]} rows lost, '
        f'{summary["pruned_interactions"]} pruned by retention',
        '', f'{"Client":<34}{"purpose":<13}{"interface":>9}{"sessions":>10}{"calls":>8}']
    lines += [f'{row["client"][:33]:<34}{row["purpose"] or "-":<13}{row["interface_version"] or "-":>9}'
              f'{row["sessions"]:>10}{row["calls"]:>8}' for row in summary['clients'][:TEXT_ROWS]]
    lines += ['', f'{"Operation":<22}{"calls":>7}{"rejected":>10}{"p50 ms":>9}{"p90 ms":>9}{"max ms":>9}'
                  f'{"p50 result":>12}{"max result":>12}']
    lines += [f'{row["operation"][:21]:<22}{row["calls"]:>7}{100 * row["rejection_rate"]:>9.1f}%'
              f'{_amount(row["duration_p50_ms"]):>9}{_amount(row["duration_p90_ms"]):>9}'
              f'{_amount(row["duration_max_ms"]):>9}{_amount(row["result_p50_bytes"], "B"):>12}'
              f'{_amount(row["result_max_bytes"], "B"):>12}' for row in summary['usage'][:2 * TEXT_ROWS]]
    lines += ['', 'Top rejections (count, operation, code, where, value sent)']
    lines += [f'{row["count"]:>5}  {row["operation"]}  {row["code"]}  '
              f'{row["pointer"] or "-"}{" (" + row["keyword"] + ")" if row["keyword"] else ""}  {row["value"][:70]}'
              for row in summary['rejections'][:TEXT_ROWS]] or ['  none']
    facts = summary['unaccepted_facts']
    lines += ['', 'Route facts the server refused and never accepted in this window',
              '  names:  ' + (', '.join(f'{row["name"][:40]} x{row["count"]}' for row in facts['names'][:TEXT_ROWS]) or 'none'),
              '  values: ' + (', '.join(f'{row["fact"][:40]}={row["value"][:40]} x{row["count"]}'
                                        for row in facts['values'][:TEXT_ROWS]) or 'none'),
              '', 'Most-read targets (read, read_many and route content)',
              '  ' + (', '.join(f'{row["target"]} x{row["count"]}' for row in summary['read_targets'][:TEXT_ROWS]) or 'none')]
    repeats, routes = summary['repeat_reads'], summary['routes']
    lines += ['', f'Reads repeating a target within one thread: {_share(repeats["repeats"], repeats["reads"])}; '
                  f'{repeats["threads_repeating"]} of {repeats["threads"]} reading threads repeated '
                  f'(worst {100 * repeats["worst_thread_rate"]:.1f}%)',
              f'Routes sent without a snapshot: {_share(routes["without_snapshot"], routes["calls"])}',
              '', f'{"Tool-calling threads":<22}{"threads":>7}{"calls":>8}   reads repeated']
    lines += [f'{row["origin"]:<22}{row["threads"]:>7}{row["calls"]:>8}   {_share(row["repeats"], row["reads"])}'
              for row in summary['threads']]
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Read-only operator MCP observation report; no agent tools.')
    parser.add_argument('--database', type=Path, help='Defaults to the always-on recording location.')
    parser.add_argument('--format', choices=('text', 'json'), default='text')
    parser.add_argument('--since-days', type=float, help='Only calls started within this many days.')
    parser.add_argument('--limit', type=int, default=100, help='Rows per section in the JSON form.')
    arguments = parser.parse_args()
    try:
        summary = report(arguments.database or default_database(), limit=arguments.limit,
                         since_days=arguments.since_days)
    except (OSError, RuntimeError, sqlite3.Error, StorageRejected, ValueError):
        print('Observation report unavailable; check database access and schema.', file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True, indent=2) if arguments.format == 'json' else text_report(summary))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
