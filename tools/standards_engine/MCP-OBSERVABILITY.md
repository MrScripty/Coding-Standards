# Operator MCP interaction observations

This optional local recorder observes the existing MCP boundary. It does not add
agent tools, modify domain outcomes or workflow authority, make model calls, retry
operations, or change the installed agent catalog. The qualification observer remains
**observer v3**, with its existing raw-event acquisition, assessment and exact-source
replay. The production recorder does not import the harness or rewrite verdicts.

The sanitized recorder selected by `--observe-database` and
`--observe-deployment` is the sole supported recording mode. The earlier raw
recorder and its `--observation-db` option are retired. Historical raw databases
retain their original schema and remain separate evidence; configure a new
dedicated database for sanitized observations.

## Configuration and authority

Recording is off unless the operator explicitly supplies **both** options below.
The commands illustrate a new operator-owned installation, not instructions to
enable an existing one without its operator's approval. Replace paths and the
nonsensitive deployment label with operator-selected values:

```sh
python3 -m tools.standards_engine.standards_engine.mcp \
  --repo-root /operator/standards --purpose authoring \
  --observe-database /operator/private-diagnostics/interactions.sqlite \
  --observe-deployment qualification-fixture
```

The database directory must already exist, be operator controlled and exclude
concurrent untrusted replacement of the directory or its ancestors. This initial
recorder supports POSIX regular local files and SQLite rollback journals only.
It refuses final-component symlinks, hardlinked files, existing group/world-readable
files, unsupported journal modes and unsupported or unrelated database schemas.
New files use mode 0600. It does not chmod existing files, create directories or
use an Engine domain database. Do not place it in a repository, tracked directory,
network share or an agent-visible artifact directory. The operator must select
appropriate disk access, encrypted storage/backup and disposal arrangements.

**Same-user filesystem access is not a security boundary.** A process with the
same OS authority can read, modify or remove the recorder database and stderr.
Tool-catalog invisibility does not create confidentiality or tamper evidence.
The recorder therefore excludes payload values regardless of filesystem modes.
The deployment label must not contain account identities, credentials or secrets.
No network exporter is included. Export/sharing requires separate operator review.

Policy defaults and valid ranges:

| Option | Default | Range / meaning |
| --- | --- | --- |
| `--observe-max-calls` | 10000 | 16–100000 retained interaction starts, across all processes |
| `--observe-max-age-seconds` | 604800 | 60–31536000 seconds since begin |
| `--observe-max-bytes` | 33554432 | 1048576–1073741824 bytes, SQLite main-file page quota |

All processes sharing a database must use the same privacy/retention policy.
Each connection enforces its configured page quota; mixed policies do not establish
a shared minimum. Rollback journals may temporarily add up to roughly another
main database's size, plus SQLite bookkeeping and bounded report/sort working space.
The directory's filesystem quota remains the final bound on all files. No WAL,
background thread, queue or telemetry write retry is introduced. Main files do not
shrink on deletion: SQLite reuses freed pages. No automatic VACUUM/rebuild occurs.

## Persisted contract and lifecycle

Schema v1 has three owners within one recorder database:

- `sessions`: exact startup runtime metadata (process instance UUID, interface,
  purpose, catalog/schema/implementation digests), deployment label and per-tool
  input/output schema digests. These bind the actually loaded source and effective
  eager/on-demand catalog. They do not prove a client refreshed its catalog.
- `interactions`: immutable begin evidence, recorder UUID, session-local ordinal,
  wall-clock begin instant, method/installed operation, sanitized input shape and
  its shape-only digest, safe discovery target, expected-catalog match state,
  request byte measurement and delivery scope. This row is the begin event.
- `events`: at most one independent end/error/incomplete observation per begin,
  with monotonic elapsed milliseconds, wall-clock finish instant, response bytes,
  fixed outcome class and sanitized validation locations/constraint keywords.

Each mutation owns `BEGIN IMMEDIATE`/commit/rollback. Schema admission is checked
under the same lock, including exact owned DDL and application ID. Zero-length new version-0
SQLite files migrate transactionally once to v1; v1 reopens without rewriting
observations. Future versions, unrelated/partial schemas and corruption are
unavailable, never deleted or replaced. Migration interruption rolls back under
SQLite recovery. Backup a stopped database before any future supported migration;
no downgrade migration or automatic restoration is currently provided.

Stdio begins are committed before dispatch. End/error evidence is committed only
after the ordinary response write and flush return. `stdio-flushed` does not prove
the client received/processed the response. The direct Python `dispatch` path uses
`constructed` scope, which proves only that a response was produced. Parsing errors
and malformed requests with responses are observed; valid notifications have no
request/response pair and are excluded. Client IDs and clientInfo are not retained.

A caught tool exception has a fixed `tool-exception` category; domain outcome may
be unknown. Typed validation rejections retain `input-invalid` plus safe field
locations. Other protocol/domain classes use fixed vocabularies, never exception
messages, tracebacks or arbitrary result codes. Transport/interruption errors
append `incomplete/unknown` if storage remains available. A killed process or a
failed terminal write leaves an unmatched begin. Reports label it unknown; startup
does not complete old calls or presume other live recorders died. Telemetry cannot
prove a domain effect did or did not commit and cannot authorize a mutation retry.

Age and count retention run transactionally on each new observed request. Expiry
is event-driven: an idle/stopped database retains expired records until recording
resumes or the operator disposes of it. Starts and their terminal evidence are
removed together; unreferenced session manifests are removed in the same
transaction. Retention can evict an in-flight call from another process. Its late
terminal is counted as dropped and recording continues; no start is recreated.
Retention can remove evidence before a later success, so history/repair denominators
are limited to retained observations. Per-session prune counters themselves expire
with their session; they are not installation-lifetime loss totals. Secure deletion
is enabled for recorder deletes; it does not erase backups, filesystem snapshots,
SQLite journal history or storage-device remnants.

## Privacy projection

No credentials/tokens, scalar input values, raw request IDs, complete prompts,
model transcripts, standards/repository bodies, domain handles or arbitrary tool
outputs are stored or hashed. Every scalar input becomes only its type.

At each structural location, only property names declared by the installed input
schema can appear. Recursive references/unions supply possible property names;
this is a disclosure projection, not another input validator. Dynamic map keys
and unknown names are removed and counted. Sensitive subtrees (`body`, `content`,
`text`, `prompt`, `message`, `rationale`, `reason`, `evidence`, `details`, `metadata`,
credentials/password/token/secret/authorization/api_key/environment/env) are replaced
by a redacted marker. Other input fields still retain no scalar values. Shapes
have at most 64 visited nodes, depth 5, four sampled array items and 8192 serialized
ASCII bytes. Truncation is explicit. Validation feedback is limited to eight
issues, depth-five schema-owned pointer components, wildcard indices/dynamic keys
and fixed constraint keywords; messages and offending values are omitted.

An input-shape digest groups structural samples, not raw values or exact semantic
variants. Two scalar variants can deliberately have the same shape. Discovery
operation values are retained only on exact installed-operation membership.
Expected catalogs become only unspecified/matches/differs. Selector values are
not retained. There is no legitimate cross-process session/task ID in the current
MCP server: reports do not infer continuation from prompts or domain handles.

## Health and recovery

Operator stderr receives fixed JSON health at recorder startup, first degradation,
retention-dropped terminal observations, and orderly close. It carries state,
fixed reason, starts/terminals recorded, observations dropped and interactions
pruned in that process. Stderr failure itself is guarded. Health is not advertised
in the agent catalog or appended to an Engine result.

Unavailable, locked (20 ms busy budget), full, unsafe, unsupported or corrupt
storage disables recording for that process and reports degraded health. Existing
begin evidence remains independent; no completion is invented. No further writes
or retries occur. The MCP operation still returns its original outcome and runs
once, including a domain result committed before the telemetry failure. A failed
start means that interaction may have no retained evidence at all. Health counters
cover attempted observations, not an exact census of lost interactions.

The operator must monitor stderr/process supervision independently of SQLite,
fix the owned storage condition and restart the MCP process to recover recording.
Preserve a corrupt/unrecognized database for diagnosis; select a separately
approved fresh path rather than silently rebuilding it. A report cannot recover
health messages that were unavailable/lost with stderr or process termination.

## Read-only inspection

```sh
python3 -m tools.standards_engine.standards_engine.interaction_observer \
  --database /operator/private-diagnostics/interactions.sqlite --limit 100
```

This operator CLI opens an existing v1 database in SQLite read-only/query-only
mode and uses one read snapshot. It never creates, migrates, prunes or modifies
observations. JSON goes only to the operator's stdout; no output file is created.
Each group/session/histogram section is bounded by `--limit` (1–1000), with explicit
truncation flags. Sequence analysis scans at most the latest 10000 retained starts;
its scan count and truncation are reported. Aggregate queries scan the bounded
retained database (at most the configured 100000 starts). Sessions show the latest
bounded set in chronological order; catalog comparisons cover those shown manifests.

The report provides operation usage, error distribution by structural input shape,
sanitized field/constraint failures, observed latency and serialized bytes with
measurement counts, sanitized shapes for successful and failed calls, session
identity and catalog additions/removals/schema changes. Totals include all retained
starts/terminals; operation/failure/shape rows identify their delivery scope and
have their own counts. An end is a non-error MCP response, not evidence the domain
workflow completed. Missing measurements are null and have separate denominators.

Sequence histograms count preceding observed errors/discoveries before a non-error
tool response, by session, delivery scope and operation. Their denominator is the
reported number of non-error responses in the bounded scan. This is a diagnostic
candidate for investigating repair loops, not proof that errors caused discovery,
that a schema was acquired before use, or that separate tasks share agent intent.
No raw trace or redacted request can be reconstructed. Bytes are JSON/stdio bytes,
not model tokens or provider billing. Preserve independent qualification evidence
for observer-v3 replay and exact behavioral assessment; do not export actual logs
with code or automatically rewrite contracts from these summaries.
