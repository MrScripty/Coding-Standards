# A1b Authority Closure Audit

**Recorded:** 2026-08-28

## Scope

This audit covers immutable content capture, typed object persistence,
reference-only standards views, roots-only execution closure, analysis-state
reconstruction, and the authorization/provider objects consumed by successful
transitions.

## Implemented Ownership

| Concern | Owner |
| --- | --- |
| Logical-path and raw-byte content snapshots | `standards_authority` |
| Envelope integrity, direct lookup, transactions, backup, and restore | `standards_authority` |
| Semantic construction, identity, decoding, and direct dependencies | Each domain's injected codec set |
| Standards-view and operation-contract composition | `standards_engine` |
| Analysis state, coverage claims, grants, attestations, and certificates | `standards_analysis` |

Authority and Contracts remain independent Modules. The repository stores
immutable JSON-compatible owner records in SQLite or memory; authored standards
authority remains text in Git.

## Closure Properties

- ContentSnapshot identity contains normalized logical path components and
  exact bytes only. It excludes Git lineage and filesystem metadata.
- StandardsAuthorityView contains references to owner-produced semantic
  authorities and does not acquire their lifecycle.
- Each operation selects one exact compatibility key and persists only its
  role- and side-qualified roots.
- Transitive closure is derived by traversing owner-declared direct references;
  callers cannot supply a closure or version bag.
- Analysis state stores narrow context plus dependency-valid decisions.
  Requirements, obligations, reading plans, certificates, and completion are
  deterministic projections.
- Provider and authorization authority enters state only after a successful
  transition consumes it. Deterministic no-observation stores no substitute
  authority.
- Existing state and child handles reconstruct from SQLite without live
  provider, authorization, repository files, or hidden process state.
- Missing immutable inputs, cycles, kind mismatches, unsupported platform
  capabilities, and repository corruption return distinct typed failures.

## Coverage Authority Correction

`standards_analysis.coverage_authority` is the sole v3 constructor for coverage
views, requirements, repository authorization grants, authored attestations,
and generated certificates. Repository TOML records are claims, not stored
objects and not self-authorization. They are validated against exact evidence
bytes, one registered authorization authority, and explicit revocation state.

Engine composition and static verification consume that same compiled result.
The previous v2 identity and certificate path, exports, and fallback behavior
are removed.

## Evidence

The registered `immutable-authority-closure` suite covers exact capture,
roots-only closure, owner codecs, platform/containment outcomes, durable direct
lookup, and cold reconstruction. Focused Authority, Analysis, and Engine tests
cover mutation isolation, dependency-sensitive identity, cycle rejection,
backup/restore, concurrent publication, branching transitions, authorization
failure, and cold SQLite replay.

Required-real interruption evidence and the final complete checkpoint are
recorded in `a1b-cutover-evidence.md`.

## Disposition

The implemented boundary has one immutable object repository and one semantic
constructor per domain object. No scan, caller index, complete-view analysis
record, ambient replay authority, or compatibility storage path remains.
