# Persistent MCP interaction observability (issue 3)

Status: Accepted (local fixture qualification). Acceptance: satisfied. Operation: verify. Owner: implementation agent;
publication and merge authority remain with the parent/operator. Baseline:
`188beda1fa477d21d576c233dd8c7f4c4c267d23` (interface 46).
Canonical plan: `docs/plans/mcp-observability/plan.md`.

## Objective and authority

Implement opt-in, local, agent-invisible SQLite observations at the existing MCP
boundary. Keep domain transactions, tools, outcomes, protocol, retries, generated
contracts, normative standards and observer-v3 qualification unchanged. No model
calls, Tuldok changes, installation configuration or live telemetry collection.
The subsequent user approval permits pushing the verified feature branch and
opening a PR containing only code, synthetic tests and sanitized documentation.
Parent owns merge. No deployment or enabling on existing installations.

Private feature branch `feat/issue3-mcp-observability` in the separate clone
`/workspace/Coding-Standards`; target `main`, integration owner parent. Retain
branch/checkout for publication decision and review; no cleanup or history rewrite.
No writes to Nearwork or other mounted repositories.

## Routed owners and decisions

Core and Router select implementation, verification/oracles, planning/discovery,
proportionality, commit, documentation; library application, IPC and persistence; diagnostics,
architecture, code-design, contracts/evolution/protocols, concurrency, security,
resilience, performance and cross-platform. Python has no language profile.
No normative or generated contract changes: no generated-contract profile,
standards-authoring workflow, release or framework profile is needed.
No AGENTS.md exists in this clone or its workspace ancestors. Runtime identity
uses process UUID and exact catalog/schema/implementation digests, independent
of Git/content authority. Observer v3 remains qualification evidence and retains
its independent exact-source replay. No production dependency on test code.

## Binding design

- MCP owns request execution and response delivery. Recorder owns only sanitized
  observations, SQLite transactions, retention and health. Operator CLI reads
  that separate database; Engine stores and authorization remain untouched.
- Explicit operator CLI configuration supplies a database in an existing trusted
  directory and a deployment label. Omission creates no recorder/file. POSIX local
  regular files only; reject symlinks, nonprivate files, unrelated databases and
  unsupported schemas. The trusted directory must exclude concurrent hostile
  path replacement. Same-user agents can read files: filesystem modes are damage
  reduction, never an agent authorization boundary. Store no secrets regardless.
- Schema v1: immutable interaction starts plus independent terminal events, joined
  by generated UUID; process/session UUID and ordinal establish local chronology.
  Sessions bind runtime metadata, deployment label and per-operation schema
  digests. No client-supplied request IDs, names or paths are stored verbatim.
- Pair end/error with begin only after response write/flush in stdio. Direct
  dispatch records a constructed response (distinct delivery evidence). Parsing,
  validation, typed rejection, tool exceptions and interruption are classified
  without raw messages. Unmatched starts remain incomplete/unknown, including
  process kill and response delivery failure; never infer completion on restart.
- Bounded input shape: fixed schema-derived property names, scalar type markers,
  depth/node/array caps; redact sensitive subtrees and unknown member names.
  Never retain scalar values, arbitrary map keys, prompts, bodies, tokens,
  credentials, outputs, exception messages or client metadata. Static schema
  selector/operation names are admitted only by exact installed-catalog membership.
  Feedback retains sanitized field pointers and fixed constraint keywords only.
- No raw input digests (dictionary attacks). Shape digests identify structural
  variants only. Catalog and implementation digests identify exact source material.
  MCP has no legitimate cross-process session/task continuation in this server;
  do not invent one from prompts or domain handles. Reports state that limitation.
- Serial synchronous recorder, no queue/thread/retry. SQLite `BEGIN IMMEDIATE`
  owns each mutation and rollback. Finite busy timeout and page quota; rollback
  journal rather than unbounded WAL. Maximum retained interactions and age are
  operator policies with bounded defaults; prune starts and events atomically.
  Retention may evict unmatched observations and is explicitly reported.
- Version 0 is accepted only for a zero-length new database and migrates transactionally
  to v1. Existing v1 reopens intact; future/corrupt/unrelated databases fail open
  without replacement. No inferred migration or automatic destructive recovery.
- Recorder failure degrades once, disables further recording for that process,
  and reports a fixed nonsensitive reason plus counters on operator stderr.
  It never retries domain work or changes its return. Operator fixes storage and
  restarts to recover recording. Health is independent of the failing database.
- Read-only bounded JSON report: operation/error/shape counts, observed latency
  and bytes, incomplete counts, discovery/failed-attempt sequences before a
  later success in the same process/operation, catalog comparisons. Denominators
  and delivery scope explicit. Correlation cannot prove intent, actual repair,
  client acquisition, token usage or billing. Retained traces cannot reconstruct
  redacted requests; observer v3 remains the source-backed replay authority.

## Composed-design admission: applicable

1. Independent concerns: MCP owns execution/delivery; recorder owns privacy,
   observations and local retention; operator report owns read-only interpretation;
   RuntimeIdentity/catalog own source/contract attribution. No observer-v3 coupling.
2. Necessary interleaving: begin before dispatch, terminal after delivery, metadata
   captured at recorder construction. Accidental coupling avoided: no Engine SQL,
   tool registration, hidden model work or telemetry-driven domain decisions.
3. Composition root knows configuration, immutable runtime/catalog and close;
   dispatch/stdio know begin/finish lifecycle. Callers never own SQL or redaction.
4. Privacy changes touch recorder/tests/docs; schema revisions flow through existing
   catalog identity; delivery changes touch MCP integration; storage revisions
   touch recorder migration and CLI together. Domain changes need no recorder edits.
5. Stable runtime metadata crosses the seam; no store handles or validator internals.
   Schema property vocabulary is diagnostic disclosure authority, not validation.
6. Recorder can fail and be disabled independently; CLI reads across restart.
   MCP remains independently usable. Tests exercise both enabled and omitted paths.
7. Deleting recorder moves necessary privacy/storage/retention/lifecycle complexity
   back into MCP, so retain it. No generic adapter registry, background worker,
   second protocol, exported observer tool or migration framework is admitted.
8. Inherent complexity is bounded evidence, privacy and SQLite lifecycle; keep it
   in one production module plus its read-only reporting entrypoint, not harnesses.

## Milestones and evidence

A Accepted: design/source/privacy review; write set this plan directory only.
B Accepted: recorder and MCP integration; write set
`tools/standards_engine/standards_engine/{interaction_observer.py,mcp.py}`,
`tools/standards_engine/tests/test_interaction_observer.py`. Gate: focused
privacy, failure and outcome-preservation tests.
C Accepted: operator report, configuration and operational documentation; same
module plus `tools/standards_engine/MCP-OBSERVABILITY.md` and README link.
Gate: bounded read-only report, catalog changes, accurate denominators.
D Accepted: cold stdio/process replacement, exceptions/interruption, real unavailable,
locked/full SQLite, concurrent processes, migration/retention/privacy. Existing MCP,
runtime identity, discovery and observer-v3 tests plus full Engine suite and
contract projection check. Synthetic baseline/candidate call and byte comparison.
E Accepted: independent GPT-6.1 Sol High design/source/privacy review accepted with all seven findings resolved; staged and full branch review, local commits, authorized push and PR.
No real logs or confidential artifacts in Git. Parent owns merge. The generated
`evaluation/standards-effectiveness/generated/suite-inputs.json` is an allowed
adjacent write: refresh through the Engine after staging declared inputs; it
tracks source/README digests and is not a normative standards change.

F Accepted: repair I1 using the actual policy semantic revision from the immutable
snapshot, before entering the existing counting mocks. Write set:
`tools/standards_engine/tests/test_analysis.py`, this plan/ledger/issues, a bounded
fixture-review report and current verification evidence; generated verifier input
manifest only if its compiler requires a refresh. Gate: failing case, analysis
module and full Engine suite pass; independent review; reviewed commit/push to
existing approved PR #4 branch. Validator, normative content and both count
assertions remain unchanged. No telemetry activation or raw log publication.

Current phase: complete local qualification. Next slice: none. Blockers: none.
F evidence: targeted case passed; analysis module 23/23; full serial Engine suite
636/636; independent fixture review satisfied. I1 is resolved without changing
validator, normative content or either count assertion; historical baseline failure
remains in issues/evidence. I2 resolved through the existing Git transport; parent
opened PR #4. The verified follow-up is packaged for the explicitly approved branch
push; Git/PR refs own publication identity and parent owns hosted CI/merge.
See [verification](reports/verification.md), [fixture review](reports/fixture-review.md), [independent source/privacy review](reports/independent-review.md), [ledger](execution-ledger.md) and [issues](issues.md).
