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

Interface schema version 19 adds explicit recovery of an already admitted
proposal application. It does not retry application or change the previously
admitted proposal operations, the eight A1c operations, or their request and
result promises. Request contract version 4 and result projection version 5
are unchanged. Snapshot handles remain at schema version 5; Analysis handles
remain at version 6; proposal, proposal-revision, readiness, and application
handles remain at schema version 1. Unsupported well-formed compatibility
keys return `unsupported`; there is no old-version parser or fallback.

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
records, and opaque mutable aggregate heads. Proposal revisions remain
immutable; only their proposal root selects a head. Verified application
intents, readiness-to-application selections, and applied outcomes are
immutable snapshot-dependent aggregates, not mutable roots. Application
admission writes the content-bound intent and its one-per-readiness selection
atomically. Recovery follows that selection, requires current recovery
authorization, and observes the fixed canonical target; it does not scan
aggregates, stage content, verify again, publish Git, or infer success from an
unchanged target. `repository_git` captures exact object bytes from the current
canonical `HEAD`; subsequent reads, inspections, and cold reconstruction
resolve the retained snapshot and never substitute the live worktree. During
application it also owns isolated candidate materialization and the exact
canonical ref compare-and-swap. Equal captured bytes may share internal
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
