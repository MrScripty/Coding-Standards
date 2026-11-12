# MCP interaction recording

Every Standards Engine MCP server process records how its tools are used, so the
interface can be improved from what agents actually send and receive. Recording is
always on, keeps about seven days, and is invisible to the agent.

- **Always on.** No flag is needed, in either purpose, for any client.
- **Invisible.** Recording adds no tool, catalog entry or instruction text and
  changes no result. It never raises into a request. A recording problem is
  reported only on the server's stderr.
- **No dropped records.** A call that cannot be written at once waits in memory
  and is written by a later call or when the process closes.
- **Seven days.** Older calls are removed automatically.

This is the only MCP recorder. The qualification observer remains **observer v3**
with its own raw-event evidence and exact-source replay; the recorder neither
imports that harness nor rewrites its verdicts.

## Where the file is

```text
${XDG_DATA_HOME:-~/.local/share}/standards-engine/observations/interactions-v2.sqlite3
```

The server creates that directory with mode 0700 if it is missing and the file with
mode 0600. Existing directories and permissions are never changed.

| Launch option | Default | Meaning |
| --- | --- | --- |
| `--observe-database PATH` | the file above | Record somewhere else. The directory must already exist; it is not created. |
| `--observe-deployment LABEL` | `local` | A nonsensitive label stored with each server process. |
| `--observe-max-calls N` | 10000 | 16–100000 calls kept, across all processes. |
| `--observe-max-age-seconds N` | 604800 (7 days) | 60–31536000 seconds since a call began. |
| `--observe-max-bytes N` | 33554432 (32 MiB) | 1048576–1073741824 bytes of database file. |
| `--no-observe` | recording on | Do not record this process. |

## Turning it off

Either of these stops recording for a server process. Nothing is created or opened.

```sh
python3 -m tools.standards_engine.standards_engine.mcp --purpose application --no-observe
STANDARDS_ENGINE_OBSERVE=off python3 -m tools.standards_engine.standards_engine.mcp --purpose application
```

The environment variable wins over every `--observe-*` option. Tests and harnesses
that start a server pass `--no-observe`, set the variable, or name a temporary
`--observe-database`, so they never write to a developer's own file; a test
enforces this. Constructing
`MCPServer` directly in Python records only when it is given a `RecorderConfig`.

## What is recorded

One row per server process (`sessions`), one per request (`interactions`) and one
per response (`events`). Notifications are not recorded.

**Per server process**

- A random process id, start time, purpose, interface version and the catalog,
  schema and implementation digests the process actually loaded.
- The deployment label, and the client name and version from `initialize`
  `clientInfo` (for example `codex-mcp-client 0.163.0`).
- Per-tool input and output schema digests, stored once per distinct catalog.
- How many calls this process pruned, and how many rows it lost (see below).

**Per request**

- Time, order within the process, method, installed operation name, and whether the
  response was written to stdio or only constructed.
- `input_shape`: the argument structure with every value replaced by its type.
- `arguments`: the values listed in the next section, and nothing else.
- `request_bytes` (the whole JSON-RPC line, client metadata included) and
  `arguments_bytes` (the `arguments` object alone).
- `expected_catalog` as `matches`, `differs` or `unspecified`; the operation a
  `describe_input`/`describe_output` call asked about.
- `thread`: a 16-hex-digit keyed hash of the client's thread or session id, when
  the request metadata carries one, and `origin`: `main`, `subagent` or `unknown`.
  Codex supplies both. A client that sends neither is recorded with no thread and
  `unknown`; reports then treat the server process as the thread.

**Per response**

- Time, duration, `response_bytes` (the whole line) and `result_bytes` (one
  serialization of `structuredContent`; the line carries that payload twice).
- An outcome word: the result's own `outcome` or `status` (`complete`,
  `needs-facts`, `needs-action`, `requires-change`, `ready`, `draft`, `applied`,
  `stale`, `rejected`, `recovery-required`, `invalid`, `unavailable`, `unsupported`,
  `unauthorized`), or `input-invalid`, `tool-exception`, a protocol error class,
  `response`, or `unknown` for an interrupted call.
- Where input validation failed: schema field names and the constraint keyword.
- `result`: `kind`, `status`, `code` and `outcome`; for a route, the selected
  target IDs, the IDs of facts still unresolved, and the content page's offset,
  total, item count and item IDs; for reads, the target IDs returned.

### Argument values that are kept

Values are kept only for names on an explicit list per operation. Any other
argument appears only as a type in `input_shape`. Strings are cut at 200
characters, and lists and fact maps at 32 entries, with a `[truncated]` marker. A
whole `arguments` object over 8 KB keeps only its top-level scalars and
`truncated`.

| Operation | Kept as sent |
| --- | --- |
| `read` | `target`, `detail`, `include_coverage`, `include_routing` |
| `read_many` | the same four names for each item |
| `route` | `detail`; `content.limit` and `content.offset`; every fact name and value |
| `related` | `target`, `direction`, `transitive`, `groups` |
| `relationship_groups` | `limit`, `offset` |
| `describe_input`, `describe_output` | `operation`, `selector`, `limit`, `offset` |
| `inspect` | the handle's `kind` and `child_kind` |
| `query`, `query_proposal`, `preview_application` | the nested request's `kind`, the `read`/`related` names above, and route facts; the revision handle's `kind` |
| `routing_facts`, `runtime_info` | nothing beyond the snapshot note below |

A supplied `snapshot` is recorded as a 12-hex-digit hash of its id, so reuse of
one snapshot is visible without keeping the handle.

**Route facts are kept exactly as the agent sent them**, including names and
values the routing vocabulary does not contain. An agent that invents a fact such
as `python`, or passes a sentence as a `task` fact, is the most useful signal this
recording has, so up to 200 characters of that text are stored.

Every other operation is an authoring operation (`propose`, `revise`,
`resolve_workflow`, `resolve_many`, `review`, `apply`, `recover`, `analyze`,
`workflow_status`, `workflow_details`, `resume`, `maintain_evidence` and the
advanced native operations). For these, a value is kept only when all of the
following hold:

- its name is declared by the installed input schema at that position;
- it is not inside `body`, `content`, `text`, `prompt`, `message`, `rationale`,
  `reason`, `evidence`, `explicit_exclusions`, `details`, `metadata` or a
  credential-like field;
- its name is one of: `kind`, `child_kind`, `detail`, `action`, `section`,
  `result`, `decision`, `owner`, `disposition`, `relation`, `artifact_kind`,
  `authority`, `level`, `role`, `origin`, `lifecycle`, `direction`, `id`, `policy`,
  `standard`, `consumer`, `target`, `source_policy`, `subject`, `evidence_owner`,
  `after_policy`, `rule`, `fact`, `requires`, `specializes`, `successors`,
  `predecessors`, `groups`, `limit`, `offset`, `apply`, `transitive`;
- it is a boolean, a small number, or a string shaped like a canonical identifier
  (letters, digits and `._:/-`, no spaces) that contains no digest, UUID or other
  long hexadecimal run.

So an edit is recorded as, for example,
`{"kind":"revise-policy-unit","policy":"workflow.planning.written-plan-applicability"}`
and a handle as `{"kind":"analysis-handle"}`.

### What is never recorded

- Standards text, bodies, titles, summaries, rationales, intents, headings,
  conditions, evidence text, file paths, or any other prose in an authoring call.
- Result content: no standard text, messages, details or summaries.
- Handle ids, digests, request ids and progress tokens.
- Raw thread, session or turn ids, model names, workspace paths, repository URLs,
  or anything else in request `_meta`.
- Argument names the installed schema does not declare (they are counted), other
  than route fact names.
- Tool names the server does not install, exception messages and tracebacks.
- Credentials or tokens, under any name.

## The seven-day window

Each new call first removes calls that began more than seven days ago, then the
oldest calls beyond the count limit. When the file is within one sixteenth of its
byte limit the oldest sixteenth of calls is removed as well, so a full file never
stops new recording. A call and its response are removed together, and a server
process row goes when its last call does (one that carries a loss count stays
until it is seven days old).

Removal happens only while something is recording: an idle file keeps its last
contents until the next call. Deleted rows are overwritten in the file
(`secure_delete`), but backups, filesystem snapshots and storage remnants are
outside the recorder's reach. The file does not shrink; freed space is reused.

## No dropped records, and what can still be lost

Each request is written before it is dispatched and each response after it has
been delivered. If the database is busy or unavailable, the row stays in an
in-memory backlog of at most 1,000 rows and the call proceeds:

- A busy database is waited for at most 20 ms per attempt, and 250 ms once at
  process start. The backlog is written by the next request or response, and at
  orderly close with a wait of up to 5 seconds.
- Recording is never switched off. After any other storage error the connection
  is reopened on a later call.
- Several processes creating the file at the same instant all succeed: the first
  publishes the whole schema in one commit and the others find it complete.

What cannot be recovered, and how it shows:

| Situation | Effect | Visible as |
| --- | --- | --- |
| Process killed during a call | The request has no response row. | "without an outcome" in the report |
| Backlog over 1,000 rows | The oldest waiting rows are dropped. | `lost` on the process row and in the report |
| A response whose request row was already pruned or dropped | The response is not stored. | counted in the same `lost` |
| Database unreachable until the process ends | Its rows are never written. | stderr only: nothing can be stored |
| Process killed while rows are waiting | The waiting rows are gone. | not visible |

In ordinary use the write takes well under a millisecond, so the last two cases
need a database that stays locked or broken for the life of a process.

## Storage

The database uses SQLite write-ahead logging. That is what keeps recording out of
the way: a commit holds the write lock for microseconds instead of the several
milliseconds a synced rollback journal needs, and reading a report never blocks a
server. For the person reading the data it means:

- While any server is running there are three files: the database, `-wal` and
  `-shm`. Recent calls may exist only in `-wal`. Read through SQLite (the report
  does) or copy all three; do not copy the database file alone.
- The file must be on a local filesystem. Network shares are not supported.
- After an operating-system crash or power loss the last few commits may be
  missing. A killed or crashed server process loses nothing that was committed.
- `-wal` is usually a few megabytes on top of the byte limit and is removed when
  the last server closes.

The recorder accepts only a new empty file or its own schema v2. It refuses
symlinks, hardlinked files, files readable by group or others, unrelated SQLite
files, files larger than the byte limit, and other schema versions, and leaves
them untouched. That includes schema v1 files written by earlier releases: they
are historical evidence, are never migrated or deleted, and are no longer written
because the default file name is new.

**Same-user file access is not a security boundary.** Any process running as the
same user can read or change the recording. The thread hash key is stored in the
same database: it keeps raw client ids out of the file and out of shared reports,
but it does not hide a thread from someone who holds both the file and the id. Do
not put the file in a repository or an agent-visible directory, and review a
report before sharing it: route facts can contain agent-written text.

## Health messages

A healthy recorder writes nothing. When recording changes state, one line goes to
the server's stderr:

```text
standards-engine observer {"backlog":6,"lost":0,"pruned_interactions":0,"reason":"storage-locked","recorded_starts":2,"recorded_terminals":2,"state":"degraded"}
```

`degraded` means rows are waiting in memory for the stated reason; it does not mean
recording stopped. A line with `healthy` follows when they have been written, and a
final line is written at close if anything was reported or lost. Reasons are fixed
words: `storage-locked`, `storage-unavailable`, `storage-full`, `storage-corrupt`,
`storage-error`, `unsafe-database-file`, `unsupported-database-schema`,
`invalid-database-schema`, `nonpristine-database`, `database-over-budget`,
`unsupported-journal-mode`, `unsupported-filesystem` and `recorder-error`. Paths,
SQL and payloads never appear.

## Reading the recording

```sh
python3 -m tools.standards_engine.standards_engine.interaction_observer
python3 -m tools.standards_engine.standards_engine.interaction_observer --since-days 2
python3 -m tools.standards_engine.standards_engine.interaction_observer --format json --limit 100
```

`--database PATH` reads another file. The command opens the database read-only,
uses one consistent snapshot and never creates, changes or prunes a recording.
SQLite may leave an empty `-wal` and a `-shm` file beside a database it has read.

The default output is about one screen of text:

- calls by client, purpose and interface version;
- per operation: calls, share rejected, p50/p90/max duration and p50/max result
  size;
- the most frequent rejections with their code, the field that failed and the
  value that was sent;
- route fact names and values the server refused and never accepted in the window;
- the most-read targets, counting `read`, `read_many` and route content pages;
- how often a thread read a target it had already read;
- routes sent without a snapshot;
- threads, tool calls and repeated reads for main agents, subagents and clients
  that identify neither;
- calls without an outcome, rows lost and calls pruned.

`--format json` gives every section in full, plus the structural input shapes,
the latest server processes, catalog differences between them and the
error-then-success sequences. `--limit` (1–1000) bounds the rows per section and
truncation is flagged.

How to read it:

- "Refused and never accepted" is inferred from the recording, not checked against
  a vocabulary: a fact name counts when its route was rejected for a fact and the
  server neither accepted that name nor listed it as an unresolved fact in the
  window. A value counts when the rejection points at its fact and that value was
  never accepted.
- A thread is the hashed client thread, or the server process when the client sent
  none. Repeat reads are counted within a thread.
- An unmatched call has an unknown outcome. The recording cannot show whether a
  mutation committed and must not be used to decide a retry.
- Bytes are serialized JSON, not model tokens or billing.
- Recorded requests cannot be replayed. Keep qualification evidence for that.
