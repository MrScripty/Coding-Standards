# Standards Engine A2 Contracts

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

## Focused Agent Navigation

Interface version 26 adds `route`, `read`, and `related` with direct domain
arguments and an optional `snapshot`. Omission captures new accepted authority
for that call; a supplied handle is used exactly. Every successful result
returns the effective snapshot. Native `query` remains available.

`read` defaults to `compact-read-result`: exact content, policy authority,
prerequisites, specialization, requested coverage/routing detail, and
continuations, without the complete `related` projection. `detail: "full"`
returns the native `read-result`. Both share the same snapshot semantics.

## Public Operations

| Operation | Input | Success result | Expected rejection |
| --- | --- | --- | --- |
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
