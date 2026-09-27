# Standards Engine

The current interface is **44**. Input contracts are native-only; `--schema-mode`
is no longer accepted. Exact input/output contracts remain available through
`describe_input` and `describe_output`. Select `--output-schemas on-demand` for the
smaller catalog; eager output delivery remains the default.

Interface 44 aligns logical graph, store-path, integer and evidence-digest boundaries.
The Digest scalar now excludes trailing data explicitly. Operation shapes and stored
workflow identities are unchanged. Restart the MCP process and refresh the client
catalog after installing the coordinated source and generated contracts; preserve
existing stores and exact workflow handles. See the
[boundary repair record](../../docs/plans/boundary-repairs/plan.md).

The versioned sections below retain implementation history.

## Purpose separation (interface 31)

Version 0.2.0 / interface 31 requires host-selected `application` or `authoring`
purpose. Application views use exact reviewed content declarations; the real
corpus intentionally starts unqualified in this code release. Authoring retains
the complete workflow and adds provenance, registered operational-aid editing
and explicit application exposure decisions. Analysis request 6 / state 7 bind
explicit preservation or change to the actual candidate semantic revision.

See [Purpose separation and code-to-content handoff](PURPOSE-SEPARATION.md) for
the supported operation map, replay guarantees, empty-corpus bootstrap and
breaking cutover. The underlying implementation description follows.

`tools/standards_engine/` is the typed composition facade for standards
navigation, immutable analysis, and controlled authoring. Callers use canonical
IDs, authored policy title/body content, explicit semantics, and opaque handles.
Repository paths, complete files, Markdown metadata envelopes, TOML/JSON
projections, SQLite records, Git refs/object IDs, and source locators remain
private Engine implementation facts unless explicitly inspected or selected
for evidence catalog maintenance.

Agents use the MCP stdio server in `standards_engine/mcp.py`. Its default catalog exposes
focused navigation and context-based authoring with generated input/output
schemas. `--advanced` exposes native operations within the configured purpose. See
[agent connection setup](../../.agents/skills/standards-engine/references/environment.md).
The existing `.agents/skills/standards-engine/scripts/invoke.py` remains the
reference/debugging transport.
`route`, `read`, and `related` accept an optional snapshot; omission captures
accepted authority and returns its handle. `read` defaults to compact exact
policy content and essential metadata; `detail: "full"` returns all relationship
rows. Native `query` remains available.

`read_many` reads a selected set using one explicit snapshot. It accepts 1–32
ordered unique items, applies the existing purpose-qualified single-read behavior,
and returns all results or one bounded rejection. Its complete JSON domain
payload is limited to 2 MiB. See [the grouped-read contract](PURPOSE-SEPARATION.md#bounded-grouped-reads).

Navigation reads immutable snapshots; proposal analysis, review, verification,
and application operate on exact revision handles. Proposal creation and
revision each carry one atomic
`StandardsChangeSet`: an evidence-backed purpose plus explicit standards-domain
edits. The common focused revision names a canonical policy unit and supplies
its title, authored body, and preserve/change semantic intent. Creation,
retirement, registered policy-unit movement, `Requires`/`Specializes` changes,
and policy-impact or broader semantic relationships use other closed edit
variants. No edit accepts paths or serialized repository files.

Focused `propose` and `revise` compose the existing creation/revision and
Analysis operations. Their `workflow-result` returns one `context` referencing
an immutable revision, analysis, or readiness record. The Engine reconstructs
all linked identities, status, and continuations from existing durable records.
`resolve_workflow` supplies a real decision/evidence submission; `review`,
`apply`, and `recover` remain explicit actions. `workflow_status` observes the
exact context, while `resume` explicitly selects the current proposal revision.
No transport context cache, mutable workflow store, or new identity scheme is
introduced. Current authorization and native atomic publication guards remain
required. Native Python/CLI operations remain supported.

Each accepted revision appends its normalized change set to an immutable
logical program and advances the durable proposal head only from its exact
expected revision; stale or invalid requests publish nothing. The Engine
privately projects that program to the fixed Markdown, TOML, and JSON
authorities and sends the result through the same compiler, Router, neutral
standards graph, and coverage owners as A1c. Discovery and revision readback
reconstruct the exact logical authority from SQLite after process replacement.
`query_proposal` reads one exact historical revision; its results and
continuations are revision-anchored projections and do not mint Snapshot or
inspection authority. A `related` query for an exact non-standard relationship
consumer returns an opaque `authoring_target` bound to the query Snapshot (or a
proposal's retained base Snapshot). Relationship edits submit that handle;
they never submit the consumer's repository locator as authoring input. The
facade owns and closes its Engine/store lifecycle when opened from a repository.

`analyze_proposal` derives normalized policy-unit changes and A1c semantic
proposals from explicit authoring intent and the compiled base/candidate, then
creates the same immutable A1c Analysis state used by `prepare` and `resolve`.
Authoring callers do not submit `semantic_proposals`; that field remains an A1c
Analysis representation. Exact revision identity participates in cold replay
without treating projected material as a Snapshot. `review_proposal` accepts
only a complete current revision analysis with no `requires-change`
disposition and three explicit evidence-backed
consumer, impact, and audit acceptances. The Engine derives the proposal head,
configured `refs/heads/main`, and Standards Verifier `complete` checkpoint,
derives an imperative proposal-specific conventional subject plus material
rationale from the explicit purpose, then publishes one immutable content-bound
readiness aggregate under an atomic proposal-head guard. `apply_proposal`
accepts only that readiness handle,
obtains current apply authorization, creates and validates a deterministic
candidate with the complete Engine-projected add, modify, relocate, and remove
topology in a private local clone, and runs the Standards Verifier `complete`
checkpoint against the exact checkout before import. Candidate identity binds
the exact parent, tree, executable decisions, and proposal-specific message.
Mechanically authored standards authorities are canonical regular,
non-executable data files; an existing non-canonical executable authority is
normalized when that authority changes. The Engine revalidates the candidate
after the external checkpoint and before durable admission. Failed-verification
results expose only bounded public code, outcome, suite, and check identifiers;
raw verifier messages and repository paths remain private. It records immutable
verified intent, advances only `refs/heads/main` with an
expected-target compare-and-swap, observes the exact candidate, and records an
immutable applied outcome before returning `applied`. Application is local and never
pushes a remote. Every failure after durable application admission returns the
application handle as
`recovery-required`. Application admission atomically records one immutable
readiness-to-application selection with the verified intent.
`recover_application(readiness)` requires separate current recovery authority,
resolves only that selection, and observes the configured canonical ref. An
existing durable outcome returns `applied` without consulting current Git; an
exact candidate at the ref records the missing outcome and returns `applied`.
An unchanged expected target, another target, or unavailable observation stays
explicitly recovery-required. Recovery never stages, verifies, imports,
publishes, retries, rolls back, or scans application records. Application does
not use the configured worktree or index as staging authority and creates no
mutable phase ledger, automatic retry, rollback, or second review lifecycle.
Routing evaluates the registered
Router projection and derives dependency closure from the neutral standards graph.
Read-only change analysis compares exact accepted and proposed authority,
derives fact requirements and impact obligations, validates evidence-backed
decisions, and projects either pending work or a complete result from one
content-addressed `AnalysisState`.

The canonical JSON Schema generates the native request/result algebra and
agent tool definitions. The optional text renderer is presentation only; no
command-string protocol or repository path is part of the agent interface.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_engine/tests
```

## Evidence and repository verification

`verify_repository` checks the working tree and can refresh its generated input
manifest. Missing inputs return typed diagnostics, including their paths.
The checkpoint validates declared structure; it does not execute the Engine's
unit tests or certify semantic completeness.

`maintain_evidence` previews or applies explicit retirements of stale claims,
checks, suites, fixtures, and registered evidence implementations. It can revise
evidence descriptions and consumer registrations. Optional
`unregister_policy_subjects` removes selected review subjects and their incident
policy relationships while preserving the standards text, module routes, and
ordinary review obligations. Certificates are pruned against the resulting
requirements. It binds an expected Git
revision and actual review evidence, verifies a candidate, and refuses to
replace independently edited working-tree files. Commit its resulting files
with the maintenance review. It neither edits normative policy nor issues a
certificate. Use the normal Engine audit publication workflow for an actual
review; `review:consumer` ownership alone creates no attestation.

## Agent Interface Acceptance

Focused tests live in `tests/test_agent_navigation.py`, `tests/test_agent_workflow.py`,
and `tests/test_mcp.py`. The real-client harness `tests/mcp_workflow_client.py`
requires the official MCP SDK in a separate client environment; it is not an
Engine dependency. From the repository root, run it with `PYTHONPATH=.` and
`--engine-python /path/to/locked-engine-python`. The default walkthrough covers
explicit review, successful application, an interrupted application, cold-process
recovery, and stale revision handling in an isolated repository. `--pending-only`
covers explicit resolution of pending normative work. Recorded acceptance and
client versions are in the [agent interface plan](../../docs/plans/standards-agent-interface/plan.md).

The optional `tests/codex_navigation_client.py` harness exercises the actual
configured Codex app-server client without starting a model turn. Run it with
the locked Engine Python; it requires `codex` on PATH and `standards-engine`
configured for this checkout. It checks exact reference-preserving authoring contracts and follows
focused route/read continuations with exact snapshot reuse in an ephemeral
client thread. It does not modify standards or apply proposals.


### Completing admitted publication

The interface-35 recovery contract distinguishes observation from explicit
completion. Carry the original readiness into `recover`. Select `observe` for
receipt reconciliation, or `complete-publication` on an authorized Git-writable
host to verify and re-establish the exact admitted candidate. Current permissions,
proposal head, candidate identity and expected-target CAS remain required. The
existing application and store are preserved. See [the recovery contract](PURPOSE-SEPARATION.md#admitted-publication-recovery-interface-35)
and [implementation evidence](../../docs/plans/admitted-publication-recovery/verification.md).

## Review workflow and deployment identity

Interface 36 supports atomic final-state decision batches with `resolve_many`,
compact focused results and paged `workflow_details`. `runtime_info` reports the
actual running process, interface and catalog, including installation drift.
The shared Router parser selects canonical table destinations independently of
display headings. [The current contract](PURPOSE-SEPARATION.md#routing-and-review-workflow-interface-36)
records limits, evidence, publication and restart semantics. These changes leave
normative meaning, review authority and retained user state with their existing owners.

## Agent interface efficiency

Interface 39 supports `route` with `content: {}` for immediate bounded exact
guidance and request-local evidence reuse in the five focused authoring inputs.
Interface 43 retains those capabilities with native-only input presentation and
explicit input/output discovery. Existing workflow
results, retained contexts and explicit review/publication gates remain unchanged.
See [the contract](PURPOSE-SEPARATION.md#agent-interface-efficiency-interface-39),
[the implementation plan](../../docs/plans/agent-interface-efficiency/plan.md), and
[agent setup](../../.agents/skills/standards-engine/references/environment.md).

Run the focused evidence with:

```bash
PYTHONPATH=. python3 -m unittest tools.standards_engine.tests.test_schema_presentation \
  tools.standards_engine.tests.test_route_content tools.standards_engine.tests.test_request_evidence
PYTHONPATH=. python3 -m tools.standards_engine.tests.agent_efficiency_trace
```

The trace uses disposable repositories, real cold MCP stdio calls and explicit
fixture-owned decisions. It compares selection-plus-read to composed routing and
inline to shared evidence, verifies exact outcomes and stops before publication.
Use the supported locked environment for release qualification.


## Catalog and transport ownership

`mcp_catalog.tool_catalog` builds tool definitions from an already compiled
interface plus explicit purpose, focused/advanced selection and output delivery.
It performs no installation loading, store access or connection management. MCP
and CLI composition load the interface; `mcp.py` owns protocol and stdio lifetime.
Schema locations and reference closure belong to the contracts package. Input
schemas are the exact reference-preserving closure of the selected declaration;
there is no recursive inliner, size-based representation selector, input-mode enum,
or embedded schema fallback. The unused structural mapper was removed with its
only production caller; schema traversal and validation remain independent owners.

Interface 43 removes `schema_mode` from Python composition APIs and `--schema-mode`
from launch and live qualification commands. Both old flag values fail explicitly.
Remove the argument pair before restarting the server; preserve the independent
`--output-schemas` choice. See [native-only cutover](PURPOSE-SEPARATION.md#native-only-input-cutover-interface-43)
and [the active implementation record](../../docs/plans/native-only-mcp/plan.md).
The earlier [schema cleanup record](../../docs/plans/schema-projection-cleanup/plan.md)
remains evidence of its original revision, not an alternate live configuration.

## Bounded input-contract discovery (interface 40)

`describe_input` exposes the exact compiled input contract for an operation in the
running catalog, including request-local evidence variants. Flat arguments select
an operation, an optional returned definition name, a catalog digest and a page.
Whole JSON schema records and exact continuations are result data, not another
validator or a schema-dependent authoring request. The service has no repository,
snapshot, evidence or workflow state access. MCP and CLI invoke it before opening
the Engine; direct facade callers share full-catalog identity with `runtime_info`.

The discovery owner uses the existing structural-reference traversal and the
existing runtime catalog digest. The generated interface remains the schema
source and validation authority. All public descriptions advertise discovery,
including every focused authoring operation. Native input presentation and
explicit discovery are the supported path. Agent evidence-reference variants,
native domain request types and retained-state versions remain unchanged.

See [the operation contract](PURPOSE-SEPARATION.md#input-contract-discovery-interface-40)
and [model-visible qualification](tests/INPUT-DISCOVERY-QUALIFICATION.md).


## Agent Interaction Quality (Interface 41)

Focused authoring routing defaults to `compact-route-result`: selected guidance,
all unanswered questions, unresolved-policy count, and an exact full `explanation`
request. Full route and native query preserve existing explanations. Relationship
IDs/meanings are available through `relationship_groups`; unknown focused queries
return the same bounded vocabulary page. Input-invalid requests carry safe field
feedback and an input-discovery continuation before domain effects.

See [the interface contract](PURPOSE-SEPARATION.md#agent-interaction-quality-interface-41)
and [the implementation/qualification record](../../docs/plans/agent-interaction-quality/plan.md).
Restart/reconnect for the coordinated catalog update. Persisted handles and mutation
contracts are unchanged. The native-only cutover below changes only presentation
and launch/composition promises.

## Output-contract delivery

Interface 42 adds `describe_output` and host-selected
`--output-schemas eager|on-demand`. Eager remains the default. A qualified client may
select on-demand to omit repeated full output schemas from its initial catalog,
while exact, catalog-bound output contracts remain available in bounded pages.
Canonical request/result validation and the actual structured tool results do not
change. There is no additional discovery call required after ordinary successes.

Use the [output delivery contract](PURPOSE-SEPARATION.md#output-contract-delivery-interface-42)
and [implementation verification](../../docs/plans/output-contract-delivery/verification.md).
The catalog inventory reports schema and digest-metadata bytes separately. Use the
updated no-model and opt-in model harnesses on the actual host before adopting the
smaller catalog. Preserve stores and handles across restart/reconnect.

## Immutable-work reuse (interface unchanged: 44)

The process-owned compilation cache also retains exact captured-content identity
proofs. Identity and compilation for one capture share one LRU entry and the existing
byte budget. The Snapshot codec still defines identity, and every read reloads actual
bytes, verifies file integrity and checks the stored identity and current lifecycle.

Focused authoring operations reuse canonical revision decoding through
`ProposalMaterials`; the single record is released on success or exceptional exit.
Every access still loads the aggregate and current root. Revision heads, evidence,
authorization and publication decisions are not cached. Retained revisions are built
only by the canonical decoder with immutable edit values; exported JSON maps are fresh.

Restart installed MCP processes to load the optimization. All existing public schemas,
input/output catalogs, flags, IDs and stores remain unchanged. No reset or migration
is needed. Measurements and remaining qualification are in
[the implementation record](../../docs/plans/immutable-work-reuse/reports/verification.md).


## Fact-material ownership and revision working sets

The Analysis-owned `RouterProjection` supplies canonical routing fact records to
both supporting-material binding and agent navigation. Navigation no longer owns
the representation that determines a router material digest. Existing records,
bindings and external interfaces remain unchanged.

The existing bounded compilation cache treats the exact accepted base as used
when retaining a successfully constructed proposal projection, including when an
operation borrowed that base without another cache lookup. With the normal budget,
this favors the base and successor over a computational predecessor. It does not
pin a base, add cache entries beyond either bound, or turn a cached product into
admission/current-head/authorization evidence. Historical revisions can still be
reconstructed and disabled/undersized caches preserve results. See the
[implementation record](../../docs/plans/fact-ownership-and-working-set/plan.md).


## Verified snapshot-capture handoff

Successful capture still compiles the live recorded source and the frozen replay
independently and checks both path closure and semantic signature before durable
snapshot publication. After admission it offers that proved frozen compilation
to the existing bounded process cache, without retaining the recording wrapper.
The first snapshot operation can reuse the result instead of compiling it again.

This is computation reuse, not a stored proof or lifecycle decision. Every later
observation still loads and verifies durable content and applies its normal current
lifecycle, evidence and purpose checks. Cache limits, compiler-identity matching,
eviction and cold/restart reconstruction remain unchanged. No API, catalog, state
format, capacity or registration flag changes. See the
[capture-handoff plan](../../docs/plans/snapshot-capture-handoff/plan.md) and evidence.
