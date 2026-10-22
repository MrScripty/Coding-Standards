# Plan: Agent Interaction Observation

**Plan status:** `Accepted`

**Current phase:** O1 — private agent-interaction capture

**Next slice:** O1

**Acceptance status:** `accepted`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Add an optional, private observation layer at the Standards Engine's agent-facing interface so maintainers can collect empirical evidence about how agents actually use that interface.

When observation is enabled, each agent-interface invocation is recorded in session order in a SQLite database together with the exact existing identity of the interface presented to that session. The interface may additionally attach a deliberately bounded subset of response metadata that is useful for later analysis.

Observation is not part of the agent contract. Enabling, disabling, succeeding, or failing to record an observation must not change anything visible to the agent.

The resulting database is evidence only. The recorder does not interpret requests, classify failures, identify hotspots, infer intent, evaluate efficiency, or analyze workflows.

## Execution Admission

- Repository: Coding-Standards.
- Canonical plan: `docs/plans/agent-interaction-observation/plan.md`.
- Operation: `start`, explicitly selected by the user on 2026-10-01.
- Adopted standards revision: `149ba317e9397519bc181a048ecf76aef129a69c`, with the current working-tree Router and Security clarifications preserved.
- Scope: O1 allowed write set below. Unrelated existing changes remain owned by their original work.
- No installed MCP configuration, dependency installation, publication or domain migration is authorized by this operation.

## Standards Routing

Apply:

- Core Standards
- Standards Router
- Implementation
- Verification
- Development Proportionality
- Planning
- Documentation
- Persistence boundary profile
- Contracts, including persisted-state evolution
- Diagnostics
- Security
- Architecture
- Code Design and Ownership

No IPC-contract change is selected because the MCP protocol and agent-visible message contract are unchanged.

No Generated Contract change is selected because no tool definition, input schema, output schema, or generated agent contract changes.

No Library profile is selected for this slice. The design preserves a transport-neutral recorder boundary, but no independently distributed reusable package is introduced until another real consumer requires one.

No Performance claim is introduced. If observation overhead later becomes material enough to require a budget or optimization, route that work separately through Performance with measured evidence.

## Current Design Observations

The inspected baseline is commit `149ba317e9397519bc181a048ecf76aef129a69c`, interface **45**.

Current relevant ownership:

- `tools/standards_engine/standards_engine/mcp.py` owns synchronous MCP stdio lifecycle and agent-facing dispatch.
- MCP requests execute serially.
- `MCPServer._request()` already separates `tools/call` from transport lifecycle operations.
- `RuntimeIdentity` already owns:
  - `interface_version`
  - `catalog_digest`
  - `schema_digest`
  - runtime instance and implementation identity
- The catalog digest already reflects the actual purpose/tool catalog presented to the client.
- Python's standard library already supplies `sqlite3`; no new runtime dependency is required.
- Existing Engine/domain APIs do not need to know that observation exists.

These facts are sufficient to implement the bounded first slice without a proxy, background service, queue, analytics framework, or new public contract.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| O-A1 | With observation enabled, a real MCP session produces one SQLite session record and an ordered interaction record for every `tools/call` presented to the agent-interface boundary, preserving the supplied invocation data. | system | representative | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A2 | Each recorded session identifies the actual existing interface version, catalog digest, schema digest, and purpose used for that session without introducing a second interface-identity authority. | integration | representative | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A3 | Enabled and disabled recording produce identical agent-visible MCP catalogs, schemas, initialization data apart from ordinary candidate implementation identity, tool results, protocol errors, and workflow behavior. Recording state and observation identifiers are never exposed. | system | representative | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A4 | The interface can attach only its explicitly selected response metadata to an interaction; ordinary response bodies, standards text, messages, details, and structured result content are not persisted. | focused | not-applicable | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A5 | Recorder initialization or write failure does not alter the agent-facing operation outcome. The recorder becomes inert for the affected session and reports only a bounded operator-side diagnostic that contains no recorded request body. | integration | representative | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A6 | Disabled observation opens or creates no observation database and performs no observation serialization or writes beyond the no-op call boundary. | focused | not-applicable | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A7 | Observation records survive close and cold reopen through the real SQLite adapter; unsupported observation database schema versions are not silently reinterpreted or migrated. | contract | representative | automated | satisfied | [isolated candidate evidence](reports/verification.md) |
| O-A8 | Interface 45's agent-visible contract files, generated tool catalog semantics, request/result versions, and existing Standards Engine stores remain unchanged. No migration of domain state occurs. | contract | supported locked runtime | automated | satisfied | [isolated locked candidate](reports/verification.md) |
| O-A9 | Independent review confirms the implemented composition preserves the one-way private observation boundary, minimal machinery, persistence ownership, and agent invisibility. | integration/review | independent reviewer | manual | satisfied | [isolated candidate evidence](reports/independent-review.md) |

## Scope

### In Scope

- A small transport-neutral interaction-recorder contract inside the Standards Engine implementation.
- SQLite-backed and disabled/no-op recorder implementations.
- One observation session per MCP server session.
- Existing interface identity attached to each observation session.
- Ordered persistence of agent tool invocations.
- Optional opaque response metadata supplied explicitly by the agent-interface implementation.
- One optional MCP launch configuration selecting the observation database.
- Recorder failure isolation from agent-visible behavior.
- Focused and real-stdio verification.
- Technical documentation for enabling/disabling observation and understanding the database's ownership and limitations.

### Out Of Scope

- MCP proxying.
- Monitoring internal Standards Engine API calls.
- Monitoring Snapshot, Analysis, Authoring, Git, verification, or other domain execution.
- Recording raw stdio bytes or the JSON-RPC transport envelope.
- Recording `ping`, `tools/list`, or other transport lifecycle traffic as agent tool interactions.
- Determining whether a request is valid, malformed, unsupported, successful, failed, redundant, efficient, or confused.
- Semantic analysis of requests or responses.
- Hotspot detection, path analysis, statistics, dashboards, reports, visualization, or recommendation generation.
- Model reasoning-token measurement.
- Full response persistence.
- Standards-text persistence merely because it appeared in a response.
- A generic field-selection language or response-projection framework.
- Background writers, queues, worker threads, network telemetry, remote export, or telemetry services.
- Automatic retention, rotation, cleanup, upload, or synchronization.
- A reusable external package before another actual consumer requires one.
- Changes to normative Coding Standards content.
- Changes to the MCP tool catalog or agent-visible schemas.
- Changes to existing Standards Engine domain SQLite stores.

## Constraints And Assumptions

### Constraints

1. Observation is a private one-way side channel:

   ```text
   Agent <──── normal interface ────> MCP adapter
                                      │
                                      │ private observations
                                      ▼
                                   Recorder
                                      │
                                      ▼
                                   SQLite

   Recorder ──X──> agent response
   ```

2. Nothing produced by the recorder may participate in constructing an MCP result.

3. Recorder availability is not a prerequisite for Standards Engine availability.

4. The database records observations, not interpretations.

5. Existing `RuntimeIdentity` values remain the canonical interface identity. Do not compute a duplicate schema/catalog identity.

6. The first implementation uses the Python standard library `sqlite3`.

7. Observation is explicitly configurable and disabled when no observation database is selected.

8. The observation database is not domain authority and cannot be used by the Engine to make standards, authorization, routing, workflow, or publication decisions.

9. Request capture intentionally preserves agent-supplied interface data. Because that data may contain repository or user material, observation is opt-in, local, and not exported by this feature.

### Assumptions

| Assumption | Decision affected | Validation | Owner / stopping condition |
| --- | --- | --- | --- |
| `tools/call` is the correct current MCP boundary for logical agent invocations. | Hook placement | Exercise valid and invalid-shaped `tools/call` requests through real `MCPServer`; confirm capture precedes tool-name/argument interpretation. | MCP owner; re-plan only if another agent-facing entry path bypasses this boundary. |
| Existing runtime identity is sufficient to identify the interface actually presented. | Session schema | Compare stored values with the same running `RuntimeIdentity.metadata()` and catalog. | Runtime Identity owner; stop when exact equality is demonstrated. |
| A synchronous local SQLite insert is sufficient for the first observation use without additional scheduling machinery. | Persistence mechanism | Run representative stdio tests; do not create a latency claim. | Observation owner; re-plan if measured interference materially affects agent behavior or a performance budget is introduced. |
| One optional bounded response-metadata object is sufficient. | Response observation API | Implement the currently selected projection and inspect resulting rows. | MCP interface owner; add structure only when a real second requirement cannot fit the opaque JSON field. |

## Binding Decisions

### D1 — Observe the agent-interface invocation, not MCP transport

The first integration point is the existing `tools/call` path in `MCPServer._request()`.

After the request has reached the `tools/call` branch but **before** tool-name or argument interpretation rejects or transforms it, pass the invocation supplied by the agent to the recorder.

Record the structured logical invocation, not the original newline-delimited JSON-RPC bytes.

Conceptually:

```text
JSON-RPC transport
      │
      ▼
tools/call selected
      │
      ├──── record agent invocation
      │
      ▼
existing name/argument checks
      │
      ▼
existing Engine dispatch
```

The recorder does not know whether later code accepts or rejects that invocation.

Transport-specific initialization, ping, listing, framing and JSON parsing remain MCP concerns.

### D2 — Reuse existing interface identity

Do not add another hashing mechanism.

At session creation, persist the existing values owned by `RuntimeIdentity`:

- `interface_version`
- `catalog_digest`
- `schema_digest`
- `purpose`

The catalog and schema digests identify the actual agent-visible interface and schema set. `RuntimeIdentity` remains their single authority.

The observation implementation must not independently inspect contract files to derive competing digests.

Interface 45 remains unchanged unless unrelated current integration has already advanced it before implementation. Reconcile against the current integrated edition rather than forcing the baseline number.

### D3 — Keep the recorder contract generic and small

Add one internal module, provisionally:

`tools/standards_engine/standards_engine/interaction_observation.py`

It owns:

- observation-session lifecycle;
- interaction sequence allocation;
- serialization of supplied observation values;
- SQLite schema/version admission;
- durable writes;
- disabled behavior;
- recorder-side failure containment.

The minimum conceptual API is:

```python
begin_session(interface_identity, session_metadata=None)
record_request(request) -> private interaction handle
record_response_metadata(interaction, metadata)
close()
```

The interaction handle is private implementation data. It is never added to an MCP message or Engine value.

Recorder mutator methods return no information that can influence an agent response.

Do not add:

- a recorder registry;
- middleware framework;
- observer event hierarchy;
- generic hook bus;
- callback graph;
- analytics interface;
- provider abstraction;
- telemetry SDK;
- plugin system.

The existence of a possible future native-harness adapter does not justify that machinery now.

### D4 — SQLite is a separate observation store

Use a dedicated SQLite file, separate from every existing Standards Engine domain store.

Initial durable schema:

```sql
PRAGMA user_version = 1;

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    interface_version INTEGER NOT NULL,
    catalog_digest TEXT NOT NULL,
    schema_digest TEXT NOT NULL,
    purpose TEXT NOT NULL,
    session_metadata_json TEXT
);

CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL,
    sequence_number INTEGER NOT NULL,
    observed_at TEXT NOT NULL,
    request_json TEXT NOT NULL,
    response_metadata_json TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    UNIQUE (session_id, sequence_number)
);
```

Use SQLite's existing transaction semantics. Enable foreign keys.

Do not introduce a separate schema-version table unless implementation evidence shows `PRAGMA user_version` is insufficient.

For a new empty database, create exact schema version 1.

For a non-empty observation database with an unsupported version or contradictory schema, do not guess compatibility and do not add a migration framework. Observation becomes unavailable for that recorder instance while ordinary MCP operation continues.

Cold reopening must preserve previously recorded rows.

### D5 — Record requests before downstream interpretation

For each `tools/call`, insert and commit the observation before the existing logical tool dispatch.

The stored `request_json` represents the agent-supplied logical invocation at that boundary.

Do not:

- normalize it into a domain request;
- classify it;
- replace missing values with inferred semantic defaults for observation purposes;
- add validation results;
- add success/failure labels;
- add error categories.

The observer's only derived information is session identity, timestamp, and sequence number required to preserve ordering.

This ordering means an interaction can legitimately have:

```text
request_json = present
response_metadata_json = NULL
```

including when execution never reaches a point where the interface chooses to attach response metadata.

That is an observation, not a recorder-generated conclusion.

### D6 — Response metadata is explicitly projected by the interface

The recorder never receives the complete MCP response and never decides what part of a response matters.

The MCP/interface implementation may call:

```python
record_response_metadata(interaction, metadata)
```

with a small JSON-compatible object it explicitly selected.

For the initial Coding Standards integration, retain only existing top-level structured-result identifiers when present:

- `kind`
- `code`
- `outcome`
- `status`

Do not synthesize absent fields.

Do not persist through this projection:

- `content`
- `structuredContent`
- standards text
- `message`
- `details`
- `input_feedback`
- explanations
- continuations
- proposal contents
- arbitrary nested result data

Protocol/transport errors that do not produce one of the selected structured Engine values do not require invented observation metadata. Their request remains recorded.

Keep this projection as a small MCP-owned function or equivalent local code. Do not build a declarative selector language, annotation system, configuration schema, or generic response projector.

### D7 — Observation is invisible to the agent

This is a required invariant, not a convenience.

Recording must not:

- add a tool;
- remove a tool;
- alter a tool description;
- alter input or output schemas;
- change catalog selection;
- alter `initialize`;
- add response fields;
- add observation IDs;
- reveal the database path;
- reveal whether recording is enabled;
- alter existing Engine results or diagnostics;
- convert recorder failure into MCP failure;
- require any agent acknowledgement or cooperation.

The same candidate build with recording enabled or disabled must expose the same agent-facing interface and behavior.

Existing `implementation_digest` may change because source code changed. Recording configuration itself does not change the catalog or schema identity.

### D8 — Configuration is one optional database path

Add one host-side option:

```text
--observation-db PATH
```

Semantics:

- omitted → observation disabled;
- supplied → attempt to open the dedicated SQLite recorder at that path.

Do not add a redundant `--enable-observation` boolean.

Do not expose this setting through the MCP catalog or runtime tool results.

Do not automatically create missing parent directory trees. The operator selects an admissible destination whose parent exists.

The initial source change does not edit a user's installed MCP registration. Qualification launches an explicitly configured disposable process. Deployment configuration can enable the feature after the source is accepted.

### D9 — Disabled behavior uses an inert recorder

The MCP composition root selects one implementation once:

```text
no observation path
    → inert recorder

observation path
    → SQLite recorder
```

Normal request handling calls the same recorder contract in either case.

The disabled recorder:

- opens no database;
- creates no files;
- serializes no request JSON;
- retains no session or interaction state.

Do not scatter configuration checks through individual tools.

### D10 — Recorder failure is contained and operator-visible only

SQLite initialization or write failure must not alter the current agent-facing operation.

On the first recorder failure:

1. contain the exception inside the observation owner;
2. stop subsequent observation work for that recorder instance;
3. issue at most one bounded operator-side diagnostic through the existing private stderr channel;
4. do not include request or response payload contents in that diagnostic;
5. continue ordinary MCP execution.

Do not retry writes indefinitely, switch databases, recreate an existing database, delete observation state, or silently claim recording remains active.

The diagnostic is operational evidence only. It is never inserted into the MCP result.

### D11 — Observation state has no authority over domain state

No Engine, Snapshot, Analysis, Authoring, verification, routing, authorization, or publication code may read the observation database.

Dependency direction is:

```text
MCP composition
   ├──► Engine facade
   └──► Interaction recorder ──► SQLite
```

and never:

```text
Engine ──► observation state
observation state ──► Engine decision
```

This preserves deletion: removing the recorder integration and launch option restores the prior product behavior without migrating or translating domain data.

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Exact request capture | Agent boundary | Literal request fixture compared with SQLite JSON | Original invocation fixture | Raw wire-byte identity | Any normalized/omitted supplied request field |
| Session ordering | Observation persistence | Explicit known call sequence and SQLite ordered rows | Fixture order | Cross-process/global ordering | Duplicate or non-monotonic sequence |
| Interface identity | Runtime identity | Stored values equal current `RuntimeIdentity.metadata()` fields | Existing RuntimeIdentity owner | New identity semantics | Observation-computed competing digest |
| Agent invisibility | MCP system | Enabled/disabled response/catalog comparison | Existing MCP contract fixtures | Timing equivalence | Any observation field or changed protocol/result |
| Selective response metadata | Interface projection | Response fixture with retained and prohibited fields | Literal selected-key expectation | Full response reconstruction | Standards/body/detail field persisted |
| Disabled mode | Composition | Temp directory remains unchanged | Filesystem observation | Future native adapter | Database/file created while disabled |
| Recorder failure isolation | MCP + persistence | Injected SQLite failure plus exact MCP result comparison | Existing MCP expected result | Guarantee that data was recorded after failure | Changed agent result or leaked recorder diagnostic |
| Durability | Persistence | Close and cold reopen real SQLite database | SQLite adapter | Cross-version migration | Missing prior rows or silent unknown-version reinterpretation |

Do not use the observation database itself as the only oracle proving that observation is correct. Fixtures retain the original expected request/order independently.

No performance benchmark is an acceptance gate for this slice because no latency or throughput claim is made.

## Security And Data Handling

The feature intentionally records agent-supplied requests, which may contain repository material or other sensitive context.

Therefore:

- recording is explicit rather than implicitly always-on;
- the database remains local to the selected path;
- no upload, network export, synchronization, or remote telemetry exists;
- the recorder does not create additional copies of full responses;
- response projection retains only the selected metadata fields;
- recorder diagnostics never echo captured request/response contents;
- the observation database is not committed to the repository by this feature;
- automatic retention policy is not introduced without a real operational requirement.

Stopping future capture requires disabling the observation path. Historical database deletion/retention remains an operator-owned file lifecycle in this first slice rather than introducing cleanup machinery.

Re-plan if automatic retention, shared databases, remote collection, multi-user access, or exported analysis becomes required.

## Simplicity And Ownership Review

**Applicability:** `applicable`

### Independent concepts and dimensions

Three concerns exist:

1. **Agent interface:** owns what the agent can call and what the agent receives.
2. **Observation selection:** the interface owns which invocation and optional response metadata are observationally relevant.
3. **Observation persistence:** the recorder owns session ordering and durable SQLite representation.

Analysis of those observations is deliberately outside all three.

### State, identity, value, time, policy, and mechanism

- Agent/domain state remains in its existing owners.
- Observation state is separate non-authoritative evidence.
- Interface identity comes from existing `RuntimeIdentity`.
- Sequence number owns only order inside one observation session.
- Timestamps describe observation time; they establish no domain ordering or success.
- Response selection policy stays at the interface boundary.
- SQLite mechanics stay inside the recorder.

#### Canonical authority scope and referenced authorities

- `RuntimeIdentity`: interface/catalog/schema identity.
- MCP adapter: agent-interface invocation and selected response metadata.
- Interaction recorder: observation persistence.
- Existing Engine modules: all domain semantics.

#### Version roles and owned promises

- Agent interface version remains owned by the existing interface contract.
- Observation database schema has independent local version 1.
- Observation schema version never becomes an agent-interface version.
- No existing Standards Engine database version changes.

#### Supported compatibility overlaps and consumer matrix

The only initial observation-store consumer is offline maintainer/analysis work.

No older observation-store format exists.

No compatibility reader or migration is justified.

#### Material identity-invalidation effects

A changed catalog or schema naturally changes the existing digest stored with future sessions. Historical sessions retain their original digest.

No observation identifier participates in domain identity.

### Caller and composition-root knowledge

`MCPServer` knows only:

- the selected recorder;
- current interface identity;
- the invocation being passed through the agent boundary;
- the explicitly selected response metadata.

It does not know SQLite table layout.

The recorder knows nothing about MCP tools, Standards operations, validation, routing, proposals, or errors.

### Representative change paths and forced owners

**New response metadata is desired:** change the MCP-owned projection and its test; do not change SQLite semantics.

**Observation database representation changes:** change the recorder schema/version and persistence tests; do not change MCP schemas.

**A new agent-interface adapter is later required:** adapt that boundary to the existing recorder contract; do not introduce MCP as an intermediate.

**Agent tools change:** existing catalog/schema digests identify the new interface automatically; observation code does not duplicate those definitions.

**Analytics requirements change:** query/process the SQLite data outside runtime capture; do not add analysis to the recorder.

### Stable Interfaces versus hidden knowledge

The recorder accepts opaque JSON-compatible observations and existing identity values. It does not reach into MCP catalogs or Engine result types.

The MCP adapter does not know SQL.

No common "telemetry model" mirrors Standards Engine domain models.

### Independent evolution, testing, failure, and replacement

Recorder persistence can be tested using literal observations without running the Engine.

MCP invisibility can be tested with an inert/spying recorder without inspecting SQL internals.

SQLite failure can disable observation without changing Engine behavior.

The whole observation implementation can be deleted without migrating domain state.

### Necessary complexity and containment

Necessary complexity is limited to:

- one recorder boundary;
- one disabled implementation;
- one SQLite implementation;
- two tables;
- one independent observation schema version;
- one optional CLI path;
- one small response metadata projection.

No proxy, daemon, queue, analytics framework, retention service, generalized middleware layer, or reusable external package is admitted.

### Deletion and cumulative machinery result

Deleting:

- `interaction_observation.py`,
- the MCP hook,
- the CLI option,
- observation tests/documentation

restores the prior architecture. No Engine API, tool contract, generated schema, or existing durable state depends on observation.

The new boundary therefore contains its own incidental complexity rather than distributing SQLite or observation policy throughout the MCP and Engine.

## Milestones

### O1 — Private SQLite interaction observation

**Goal:** deliver the complete usable observation path from real MCP tool invocation to queryable SQLite evidence while preserving exact agent-visible behavior.

**Allowed write set:**

Production:

- `tools/standards_engine/standards_engine/interaction_observation.py` — new recorder owner.
- `tools/standards_engine/standards_engine/mcp.py` — composition, `tools/call` observation hook, optional response metadata projection, launch configuration.

Tests:

- `tools/standards_engine/tests/test_interaction_observation.py` — recorder, SQLite schema, disabled path, cold reopen, unsupported schema, failure containment.
- `tools/standards_engine/tests/test_interaction_observation_transport.py` — real stdio session ordering, interface identity, request capture, metadata selection, enabled/disabled invisibility.
- Directly affected existing MCP/runtime tests only when a current assertion must recognize the new host-side CLI option or injected recorder seam.
- `tools/standards_engine/tests/test_supporting_workflow.py` — explicit empty application-approval fixture precondition, admitted to unblock the required workflow gate used by the existing MCP runtime-cache test. Production behavior and existing workflow assertions remain unchanged.

Documentation and plan records:

- `tools/standards_engine/README.md` — concise operator configuration and observation-boundary contract.
- `docs/plans/agent-interaction-observation/plan.md`
- `docs/plans/agent-interaction-observation/execution-ledger.md`
- `docs/plans/agent-interaction-observation/issues.md`
- `docs/plans/agent-interaction-observation/reports/` as evidence is produced.
- `docs/plans/README.md` — link-only active-work index update.
- `evaluation/standards-effectiveness/generated/suite-inputs.json` only through its existing owning regeneration path when repository freshness requires it.

**Explicitly excluded from the write set:**

- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/contracts/a1-contract.schema.json`
- generated agent-tool contracts
- `_generated_contract.py`
- Standards content
- existing Snapshot/Analysis/Authoring database schemas
- agent skill instructions unless implementation evidence demonstrates a real operator-facing configuration dependency
- installed user MCP configuration

A discovered direct test/document consumer inside the same invariant may be added to the write set with a ledger entry. A new semantic owner, public contract, persistence format, or agent-visible behavior requires re-planning.

### Tasks

- [x] Inspect current repository state and reconcile the baseline before editing.
- [x] Add the recorder module with SQLite and inert implementations.
- [x] Define exact observation SQLite schema v1 and cold-open admission.
- [x] Reuse `RuntimeIdentity` interface/catalog/schema identity without modification.
- [x] Add optional `--observation-db PATH` composition.
- [x] Begin one observation session for the MCP session without exposing its identity.
- [x] Record each `tools/call` invocation before tool-specific interpretation.
- [x] Preserve interaction ordering with a recorder-owned sequence number.
- [x] Add the bounded MCP-owned response metadata projection.
- [x] Ensure metadata/request capture results never flow into MCP response construction.
- [x] Contain recorder errors and make the recorder inert after first persistence failure.
- [x] Add focused SQLite tests.
- [x] Add real-stdio enabled/disabled equivalence and ordering tests.
- [x] Verify existing MCP/catalog/runtime identity tests.
- [x] Run generated freshness and affected structural checks.
- [x] Run the repository's supported locked CI for the changed material.
- [x] Obtain independent review against O-A1–O-A9.
- [x] Record evidence and dispositions in the plan artifacts.

**Acceptance gate:** O-A1 through O-A9 satisfied on the coherent candidate, with exact-source locked verification and independent review.

**Status:** `Accepted`

## Blockers

`none` for O1.

The user explicitly dismissed O-I1 as material to this work on 2026-10-01. O1 is accepted against the verified isolated source: all O-A1–O-A9, 1,255 tests, 73 complete-verifier suites and independent review. The combined original tree's unrelated evidence mismatch remains recorded; its verifier result is still a failure and no historical evidence is rewritten. Installed configuration remains outside this operation's admitted scope.

## Re-Plan Triggers

Re-plan if implementation evidence shows any of the following:

- agent invocations materially bypass the selected `tools/call` boundary;
- capturing the invocation requires changing the public MCP/tool contract;
- another real integration requires materially different observation semantics rather than the same opaque recorder contract;
- the observation store requires concurrent writers, remote access, or a service lifecycle;
- a real consumer requires cross-version database migration or compatibility;
- response observation requires a general projection/selection language rather than a small explicit interface-owned projection;
- recording overhead becomes material enough to require a performance budget or asynchronous mechanism;
- automatic retention, rotation, redaction, encryption, upload, or multi-user access becomes a product requirement;
- recorder state must influence Engine behavior;
- implementation requires changes to existing domain persistence;
- observation machinery spreads into multiple Engine/domain owners rather than remaining contained.

Do not re-plan merely because another directly affected test or documentation file must enter the bounded write set.

## Final Acceptance

Acceptance requires:

1. real ordered observations in SQLite;
2. existing interface identity attached without duplicate authority;
3. bounded optional response metadata only;
4. no full-response capture;
5. exact agent-facing invisibility with observation enabled, disabled, and failed;
6. no public interface/version/schema change;
7. no domain-state migration;
8. current locked verification passing;
9. independent review with all material findings dispositioned.

After acceptance, enable observation in the intended MCP launch configuration with an explicit local database path and begin collecting empirical usage evidence.

Analytics, interface-quality conclusions, and future interface redesign are separate consumers of that evidence and are not part of this plan.

- Acceptance status: `accepted`
- Deferred follow-ups: MCP proxy, native-harness adapter, analytics/query tooling, automatic retention
- Final status: `Accepted`
