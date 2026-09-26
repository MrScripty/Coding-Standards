# Standards Engine Contracts

Interface 38 is the current focused workflow result contract. Pending mutations
return a bounded first work page and relative continuations; status reads stay
lightweight. The canonical schema, generated models and examples change together.
Existing request/state/handle versions remain unchanged. Restart and reconnect
supported clients without deleting their state. See
[the current contract](../PURPOSE-SEPARATION.md#actionable-workflow-results-interface-38).

The following notes describe earlier interface increments.

## Current contract: interface 36


Interface 36 adds `resolve_many`, `workflow_details`, and `runtime_info`.
Focused workflow calls select compact Analysis summaries by default and accept
`detail: full` for complete diagnostic results. Batched submissions keep the
existing per-variant capability contract, current evidence checks and explicit
publication boundary. Detail pages use observation-bound continuation arguments,
record-count and payload bounds. Runtime identity is available to both purposes
without standards-store access. See [the full workflow contract](../PURPOSE-SEPARATION.md#routing-and-review-workflow-interface-36).



Interface 35 adds an explicit `action` to `recover` and `recover_application`.
Omission or `observe` reconciles an existing applied candidate without Git
writes. `complete-publication` is a deliberate request to re-establish the same
admitted candidate at its exact expected target. It requires current recovery
and application permission, a current reviewed proposal, exact reconstruction,
and complete verification before the existing Git compare-and-swap. It never
creates a replacement application or changes the candidate selected by readiness.
A repeated recovery of an already-applied readiness returns that same outcome.

Recovery-required results may include scalar `details`: `cause_code`,
`cause_outcome`, and `git_operation`, `git_exit_code`, `git_reason`, and
`git_stderr_excerpt` for a failed command. The excerpt is a recognized fixed
phrase, not arbitrary stderr or a path. Unrecognized output is `unclassified`.
A permission-denied observation identifies Git's error, not its host-level cause.
`APPLICATION.RECOVERY_BLOCKED` preserves an admission whose current completion
prerequisite failed. The original readiness/application/store formats are unchanged.

Required host purpose selects application or authoring operation variants. The
canonical interface declares each variant's exact input/result roots, and the
compiler generates their shared schema authority. Application projections have
closed result fields and bounded errors; their catalogs omit authoring schemas.

New logical edits maintain decision provenance, registered prompt/template
content, and exact application exposure. Whole-standard revisions can explicitly
update all registered scopes through `scope_updates`. Analysis request 6 /
result-state 7 accept explicit equal-revision preservation or next-revision
semantic change against the actual compiled candidate. Older Analysis records
are not reinterpreted. Unchanged Snapshot/storage primitives retain their own
versions. See [the implementation contract](../PURPOSE-SEPARATION.md).

Interface 34 adds proposal-local `register-consumer` and authoring-only
`preview_application`. A registration names a canonical consumer ID, an existing
tracked repository path, artifact kind and evidence/projection authority. The
Engine binds exact original-revision bytes privately before admitting the edit;
callers supply no captured bytes. Relationships may select candidate consumer
IDs, including registrations in the same change set. Registry declarations,
relationships and coverage reviews retain separate meanings.

Registered Markdown documentation, including hidden-directory skill references,
can use `revise-operational-artifact` alongside prompts and templates. That edit
accepts a canonical registered ID or returned exact target. Fixture and source
consumers do not acquire an editing capability.

`preview_application` accepts an exact proposal revision and one application
read/route/related request. It applies normal exposure and prerequisite checks,
returns explicitly candidate-bound results, and provides preview-only
continuations. It is absent from ordinary application catalogs. Preflight still
checks structure rather than returning an application view. Preview does not
certify coverage, accept review, issue exposure approval or publish the draft.

Consumer capture uses the existing immutable revision aggregate; snapshot/store
and unrelated handle versions are unchanged. Restart the installed MCP process
and reconnect its client after updating the Engine. Initialization reports the
installed interface and purpose. Read the new tool and edit schemas rather than
inferring a live update from files on disk.

The version notes below document earlier design increments, not supported
compatibility paths or the current purpose-less launch contract.

This directory owns the serialized public shape of the Standards Engine
interface. Runtime policy meaning, identity construction, persistence,
repository loading, and controlled-authoring behavior belong to their domain
Modules.

## Authority

[`a1-contract.schema.json`](a1-contract.schema.json) is the sole public JSON
shape authority. It uses JSON Schema Draft 2020-12. The selected
`standards_contracts` dependency validates instances and compiles the reachable
public definition closure; this package does not implement JSON Schema
keywords.

[`a1-interface.toml`](a1-interface.toml) owns operation roots, accepted result
families, capabilities, and independent request/result compatibility versions.
It contains no domain identity fields or runtime state machine.

The compiler produces these disposable projections:

- [`../standards_engine/_generated_contract.py`](../standards_engine/_generated_contract.py)
- [`generated/agent-tools.json`](generated/agent-tools.json)

Files under [`examples/`](examples/) are reviewed authored fixtures. Each
example names one reachable schema definition and supplies one value. They do
not define fields, defaults, variants, identity, or runtime semantics.

## Grouped Reading (Interface 32)

`read_many` declares authoring and application operation variants. Both require
an explicit snapshot and 1–32 unique ordered read items. Each item uses the
corresponding single-read options without a separate snapshot. Success returns
that snapshot and ordered single-read result objects; failures return one normal
purpose-qualified rejection and no item results. The Engine additionally enforces
a 2 MiB serialized domain-result bound (documented in PURPOSE-SEPARATION.md).

This public addition changes the interface version and generated projections;
Snapshot, Analysis, identity and store contracts keep their independent versions.
The schema/compiler remain the sole shape authority. Transport catalogs expose
one additional focused operation; existing query variants retain their scope.

## Focused Agent Navigation

Interface version 30 adds `rewrite-navigation-index` to the proposal edit
algebra. `read(target="navigation-indexes")` lists registered entrypoint
handles; reading a listed ID returns its captured content. The typed
`navigation-indexes-result` carries exact snapshot or proposal `authority`,
entrypoint handles, and canonical destination selections. It is navigation
material, not a normative standard or coverage attestation.

The Engine resolves source locations from its navigation registration and
renders links from explicit canonical IDs. Index-only changes produce mandatory
impact-review obligations bound to accepted/proposed index representation and
selected destination authority. Existing review, readiness, verification,
local application, and recovery apply. Older snapshots without registrations
retain ordinary reads but cannot author indexes; no current-worktree authority
is inserted into them. No handle format or policy semantic revision changes.

Optional `retargets` explicitly pair registered legacy entrypoint handles with
selected canonical destinations. The Engine updates matching required-link
declarations for the edited index atomically and binds those declarations into
snapshot/review authority. Unrelated assertions remain enforced. Unused,
duplicated, stale, or unselected retargets reject the candidate.

The default MCP catalog retains its existing tools; discovery uses `read` and
authoring uses `propose`/`revise`. There is no raw Markdown or path write input.

Registered section-route inventories are captured with the index and preserved
when rewriting for explicitly selected canonical owners. Their declarations
and owner content are bound into review evidence. Missing required owners and
required non-standard artifact routes reject the rewrite. This renderer
behavior adds no public operation, edit variant, or contract shape.

Interface version 26 adds `route`, `read`, and `related` with direct domain
arguments and an optional `snapshot`. Omission captures new accepted authority
for that call; a supplied handle is used exactly. Every successful result
returns the effective snapshot. Native `query` remains available.

`read` defaults to `compact-read-result`: exact content, policy authority,
prerequisites, specialization, requested coverage/routing detail, and
continuations, without the complete `related` projection. `detail: "full"`
returns the native `read-result`. Both share the same snapshot semantics.

Interface version 27 adds `routing_facts` and a focused `agent-route-result`.
The latter retains the native reading plan, with canonicalized supplied facts,
exact evaluated rule expressions/states, and fact-typed unresolved questions.
Native `query` route results retain their existing shape. Vocabulary discovery
uses the same fact projection as full Router reads and introduces no new fact
semantics. `known-absent`, unknown, nullable values, and collection values retain
the applicability owner's meanings.

## Focused Authoring Context

Interface version 28 adds `propose`, `revise`, `analyze`, `resolve_workflow`,
`review`, `apply`, `recover`, `workflow_status`, and `resume`. `WorkflowContext`
is a union of existing immutable revision, analysis, and readiness handles.
The Engine derives the linked state; clients cannot submit conflicting handle
combinations. No new handle version or workflow persistence is introduced.

`WorkflowResult` preserves a native `outcome` when applicable and returns the
current context, exact proposal/revision, status, and bound continuations with
remaining caller input names. Existing native schemas define those inputs.
The context does not grant authorization or select a newer revision. Old Analysis
branches retain their existing immutable branch semantics. Stale revisions need
explicit `resume`; readiness retains exact review and application identity.

`propose`/`revise` stop after analysis. Rejection after creation preserves the
revision context. Review and application are never implicit. Recovery-required
permits only recovery with the same readiness. Native atomic guards protect
review and publication even if the head changes after a continuation is shown.
Terminal native application/recovery outcomes are preserved without a secondary
store read that could obscure the already-established outcome.

The default MCP catalog contains 15 focused tools. `--advanced` exposes all 32
native and focused operations; the Python facade and reference CLI keep their
existing advanced capabilities. Schema generation remains the single shape
owner for both catalogs.

## Client Presentation And Focused Continuations

Interface version 29 adds `FocusedQueryNextOperation`. Focused navigation
projects native query continuations to `route`, `read`, or `related`, retaining
snapshot, target, and request kind. Native `query` keeps its native continuation
names; native and focused results share the expanded continuation union.
No request, domain identity, analysis replay, or persistence version changes.

MCP input schemas expand canonical references inline until recursion, then keep
the recursive reference and its complete definition closure. This makes the
containing authoring objects and all edit variants explicit to clients without
weakening canonical validation or imposing a recursive expression depth cap.
Reference siblings retain conjunction semantics. Output schemas keep their
existing reference closures. This is transport presentation, not new domain
schema authority. Reconnect clients after updating the advertised catalog.

The restarted client can still abbreviate nested fields even with inline
schemas (`edits: Array<unknown>` and purpose evidence). For `propose`, `revise`,
and `resolve_workflow`, MCP descriptions therefore include the exact canonical
input schema and complete reachable definition closure as JSON. This preserves
field visibility independently of the client's type renderer, without a separate
discovery operation, hand-authored field list, changed validator, or recursive
limit. The additional description text is intentional authoring overhead.

## Public Operations

| Operation | Input | Success result | Expected rejection |
| --- | --- | --- | --- |
| `route` | `RouteCall` | `AgentRouteResult` | `RejectedResult` |
| `read` | `ReadCall` | `CompactReadResult` or `ReadResult` | `RejectedResult` |
| `related` | `RelatedCall` | `RelatedResult` | `RejectedResult` |
| `routing_facts` | `RoutingFactsCall` | `RoutingFactsResult` | `RejectedResult` |
| `propose` | `ProposeCall` | `WorkflowResult` | `RejectedResult` |
| `revise` | `ReviseCall` | `WorkflowResult` | `RejectedResult` |
| `analyze` | `AnalyzeCall` | `WorkflowResult` | `RejectedResult` |
| `resolve_many` | `ResolveManyCall` | `WorkflowResult` | `RejectedResult` |
| `workflow_details` | `WorkflowDetailsCall` | `WorkflowDetailsResult` | `RejectedResult` |
| `runtime_info` | `RuntimeInfoCall` | `RuntimeInfoResult` | Purpose-qualified rejection |
| `resolve_workflow` | `ResolveWorkflowCall` | `WorkflowResult` | `RejectedResult` |
| `review` | `ReviewCall` | `WorkflowResult` | `RejectedResult` |
| `apply` | `ApplyCall` | `WorkflowResult` | `RejectedResult` |
| `recover` | `RecoverCall` | `WorkflowResult` | `RejectedResult` |
| `workflow_status` | `WorkflowStatusCall` | `WorkflowResult` | `RejectedResult` |
| `resume` | `ResumeCall` | `WorkflowResult` | `RejectedResult` |
| `create_snapshot` | `CreateSnapshotCall` | `CreateSnapshotResult` | `RejectedResult` |
| `find_snapshots` | `FindSnapshotsCall` | `FindSnapshotsResult` | `RejectedResult` |
| `delete_snapshot` | `DeleteSnapshotCall` | `DeleteSnapshotResult` | `RejectedResult` |
| `undelete_snapshot` | `UndeleteSnapshotCall` | `UndeleteSnapshotResult` | `RejectedResult` |
| `query` | `QueryCall` | `QueryResult` | `RejectedResult` |
| `prepare` | `PrepareCall` | `PendingResult` or `CompleteResult` | `RejectedResult` |
| `resolve` | `ResolveCall` | `PendingResult` or `CompleteResult` | `RejectedResult` |
| `inspect` | `InspectCall` | `InspectionResult` | `RejectedResult` |
| `create_proposal` | `CreateProposalCall` | `CreateProposalResult` | `RejectedResult` |
| `find_proposals` | `FindProposalsCall` | `FindProposalsResult` | `RejectedResult` |
| `revise_proposal` | `ReviseProposalCall` | `ReviseProposalResult` | `RejectedResult` |
| `query_proposal` | `QueryProposalCall` | `QueryProposalResult` | `RejectedResult` |
| `analyze_proposal` | `AnalyzeProposalCall` | `PendingResult` or `CompleteResult` | `RejectedResult` |
| `review_proposal` | `ReviewProposalCall` | `ReviewProposalResult` | `RejectedResult` |
| `apply_proposal` | `ApplyProposalCall` | `ApplyProposalResult` or `ApplicationRecoveryRequiredResult` | `RejectedResult` |
| `recover_application` | `RecoverApplicationCall` | `RecoverApplicationResult` or `ApplicationRecoveryRequiredResult` | `RejectedResult` |
| `maintain_evidence` | `MaintainEvidenceCall` | `MaintainEvidenceResult` | `RejectedResult` |
| `verify_repository` | `VerifyRepositoryCall` | `VerifyRepositoryResult` | `RejectedResult` |
| `verify_proposal` | `VerifyProposalCall` | `VerifyProposalResult` | `RejectedResult` |

Interface schema version 24 adds `audit-policy-unit` edits for publishing
coverage reviews through the configured Engine audit authority. The edit names
a registered policy and rationale; it requests review and publication without
altering standards text. Current certificates need no renewal. Analysis and
review must complete before `verify_proposal` can check an audit proposal;
supply its optional `readiness` handle. The result echoes that readiness.
Application publishes the exact reviewed receipt with the candidate, using the
existing verification, local publication, and recovery lifecycle. Subsequent
coverage reads include the retained auditor's issuer, principal, and
authorization ID. A caller's provenance text does not determine audit authority.

Version 22 added optional `include_coverage` to `read` requests
through both `query` and `query_proposal`. The result lists the registered policy
units in that read scope, their current requirement identities, and whether the
captured repository has a current attestation. An empty list means no registered
units, not complete coverage. This read does not include Analysis-local claims
or certify the quality of the standard. Use Analysis to obtain review obligations
and submit evidence for an exact requirement.

Version 21 added routing rule/fact edits and explicit
verification operations. Routing edits are atomic with standards edits: the
Engine maintains readable selection rows, compiles expressions against the
final fact schema, checks target uniqueness, and refreshes derived verification
inputs. Fact revisions advance when their meaning or value domain changes;
question wording alone preserves the revision. New topic and workflow IDs may
name nested detail pages.

A Router `read` request may set `include_routing: true` to return exact authored
fact and rule definitions suitable for edits. This works through `query` for a
Snapshot and `query_proposal` for a draft. The option is omitted from ordinary
reads, keeping navigation concise.

`verify_proposal` runs the full application checkpoint on a private candidate
for an exact revision and returns its report without publication or review
admission. `verify_repository` checks the working tree; its explicit
`refresh_verification_inputs` option rebuilds the derived suite-input manifest
under `standards.verify` authorization. Neither operation marks semantic review
complete. Callers must inspect `verification.passed` and failures.

The local facade resolves `repository-content` version 1 evidence IDs as
repository-relative file paths and checks their exact bytes against the supplied
digest. Its own authorization/revocation statements use `local-statement`
version 1, under local authority revision 2. Missing documents and unsupported
providers produce typed outcomes; identifiers never substitute for file content.

Interface schema version 20 replaced repository-shaped authoring mutations
with one atomic `StandardsChangeSet` on each `create_proposal` and
`revise_proposal` call. A change set contains one evidence-backed purpose and
an unordered, non-empty set of closed standards-domain edits. Callers provide
canonical standards and policy-unit IDs, authored title/body content, explicit
semantic intent, relationships, rationale, and evidence. They do not provide
repository paths, complete files, metadata envelopes, serialization formats,
database identities, Git refs, or object IDs.

When an existing relationship endpoint is not a standard or policy-unit ID,
an exact `related` query returns a Snapshot-bound opaque `authoring_target`.
Callers use that handle in relationship edits; the Engine alone resolves its
private consumer identity.

Each accepted revision appends its normalized change set to an immutable
logical program rooted at the exact base Snapshot. The Engine privately owns
Markdown metadata envelopes, TOML and JSON projections, SQLite persistence,
and local Git candidate mechanics. It derives structural digests and A1c
`SemanticProposal` records from the compiled candidate and the caller's
explicit semantic intent. `semantic_proposals` therefore remains part of the
A1c Analysis contract, but is not an authoring input in Interface version 20.

The proposal operations and eight A1c operation roots are otherwise unchanged.
The exact module-change variant advances the Analysis request contract to 5
and result/state contract to 6. Snapshot handles
remain at schema version 5; Analysis handles remain at version 6; proposal,
proposal-revision, readiness, and application handles remain at schema version
1. Unsupported well-formed compatibility keys return `unsupported`; there is
no version 19 authoring parser or fallback.

Trusted provider and authorization context is injected by the Engine
composition root. Caller-authored requests cannot grant capabilities or supply
trusted standards-change facts.

## Identity And Authority

The schema governs representation only. `standards_identity` owns exact
identity-v2 framing and codepoint-preserving encoding. Each domain Module owns
its material record, ordering, deduplication, semantic identity, and direct
authority references. Schema annotations, generated classes, builds, and
release versions do not acquire domain authority.

`standards_snapshots` stores immutable captured content, immutable dependent
records, and opaque mutable aggregate heads in SQLite. Proposal revisions
remain immutable; only their proposal root selects a head. The revision
aggregate stores normalized logical change-set history rather than repository
files or Git material. Verified application
intents, readiness-to-application selections, and applied outcomes are
immutable snapshot-dependent aggregates, not mutable roots. Application
admission writes the content-bound intent and its one-per-readiness selection
atomically. Recovery follows that selection, requires current recovery
authorization, and observes the fixed canonical target; it does not scan
aggregates, stage content, verify again, publish Git, or infer success from an
unchanged target. `repository_git` captures exact object bytes from the current
canonical `HEAD`; subsequent reads, inspections, and cold reconstruction
resolve the retained snapshot and never substitute the live worktree. During
application it also owns isolated add, modify, relocate, and remove candidate
materialization, canonical non-executable mode for mechanically authored
standards authorities, deterministic imperative commit identity from validated
proposal purpose, and the exact canonical ref compare-and-swap. Application
verifies the exact candidate before publishing it locally and includes no
remote push. Equal
captured bytes may share internal
storage, but each public snapshot has an independent opaque identity and
lifecycle.

An `AnalysisHandle` is the sole A1 analysis identity. Pending and complete
results are deterministic projections of immutable state. Resolution creates
an independent child state; A1 has no mutable head, global supersession, or
temporal packet staleness.

## Verification

From the repository root, run:

```text
PYTHONPATH=. python3 -P -m tools.standards_contracts.standards_contracts.projection --check
```

The check compiles the canonical schema and interface through
`standards_contracts`, compares both generated projections byte-for-byte, and
validates every authored example through the same production contract runtime.
Generated freshness is not semantic conformance evidence by itself; the
registered contract suite separately exercises the selected Draft validator,
public behavior, identity equality, and unsupported-profile outcomes.

Evidence catalog maintenance accepts explicit retirements and consumer updates.
Use `apply: false` to inspect the verified candidate and `apply: true` to write
that candidate's evidence changes to the working tree. It binds an expected Git
revision, verifies supplied review evidence, and refuses to overwrite changed
paths. It never certifies completeness or publishes a Git ref. Normative edits
continue to use proposals; commit evidence maintenance with its review record.
