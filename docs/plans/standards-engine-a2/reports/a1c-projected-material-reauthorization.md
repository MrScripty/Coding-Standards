# A1c Projected-Material Reauthorization

**Status:** `authorized for design validation; production unavailable`

## Authority And Exact Scope

On 2026-09-01, after reviewing the terminal A2-P2R evidence and the proposed
corrective design, the user explicitly selected the narrow A1c evolution that
allows one immutable projected proposal revision to participate in Analysis
identity and cold replay. This is product authority to re-plan and validate the
change. It is not authority to edit canonical Engine source, generated public
contracts, persisted stores, or the accepted A1c ADR before the predeclared
design evidence passes.

The selected correction replaces only the snapshot-only proposed-material
assumption. The target A1c rule is:

> One immutable `AnalysisState` contains an accepted snapshot root and one
> exact immutable proposed-material reference. Proposed material is either an
> accepted snapshot or a projected proposal revision. A projected proposal
> revision is not snapshot authority. Its exact reference participates in
> analysis identity, dependency closure, and cold replay.

The current accepted implementation and ADR remain runtime authority until an
accepted validation result admits a coordinated cutover. The future ADR must
record the exact supersession rather than rewriting the earlier acceptance as
though it had always used projected-material identity.

## Domain Model

| Term | Meaning | Owner | Explicit exclusion |
| --- | --- | --- | --- |
| `ProposalRevision` | An immutable content-bound authoring value rooted in one retained snapshot and containing exact normalized non-Git mutations, semantic proposals, and material contract identities. | Authoring | Mutable proposal head, snapshot, Git commit, or accepted canonical authority |
| `ProposedMaterialRef` | A closed Analysis-owned value identifying the exact proposed material used by one immutable analysis. | Analysis | Generic authority envelope, caller-selected resolver, or broad version bag |
| `SnapshotMaterialRef` | The `ProposedMaterialRef` variant that names one exact accepted snapshot root. | Analysis and Snapshot | Content hash used as lifecycle identity |
| `ProjectedRevisionMaterialRef` | The `ProposedMaterialRef` variant that names one exact `ProposalRevision` and its required base snapshot relationship. | Analysis and Authoring | Synthetic `SnapshotHandle`, mutable current-head lookup, or independently persisted analysis state |
| material-resolution seam | The private location where Analysis obtains immutable content for compilation from either snapshot or projected-revision material. | Analysis composition root | Public storage Interface or caller-visible Adapter selection |

The material-resolution seam is justified for validation by two required
behaviors: the accepted snapshot Adapter and the proposed projected-revision
Adapter. Both must feed the same compiler and Analysis kernel. P2R2 must reject
the seam if the second Adapter does not carry distinct material-resolution
behavior or if the variation leaks through the public Interface. The candidate
seam remains private to the deep Analysis Module; callers and generated
contracts do not select an Adapter or construct a `ProposedMaterialRef`.

## Selected Composition

- Existing A1c `prepare` behavior maps its exact proposed `SnapshotHandle` to
  `SnapshotMaterialRef` and otherwise preserves its public operation and typed
  result behavior.
- A candidate explicit A2 `analyze_proposal` operation accepts an opaque
  immutable revision handle and optional prior analysis handle. The Authoring
  composition root resolves the revision and constructs the private
  `ProjectedRevisionMaterialRef`; the caller supplies no changes, semantic
  proposals, content digest, repository fact, store fact, or resolver choice.
- `AnalysisState` retains normalized changes and semantic proposals as exact
  analysis inputs, but their authoritative source for projected material is
  the immutable revision. Construction and replay reject any mismatch rather
  than treating the copies as independent authority.
- Analysis identity includes the exact proposed-material reference. Two
  byte-distinct proposal revisions therefore cannot share one analysis
  identity merely because their base root and declared change descriptors are
  equal.
- Cold replay resolves the exact stored revision, verifies its base and
  identity material, reconstructs projected content through the existing
  compiler path, and revalidates retained decisions. It never substitutes a
  current proposal head, repository state, caller injection, or snapshot.
- The proposal revision remains a typed dependent record inside the one
  snapshot lifecycle aggregate and one SQLite owner. Analysis remains the only
  analysis authority; Authoring owns revision and head state, not analysis
  results.

The candidate public operation name and exact generated request/result shapes
remain subject to P4R after projected-material identity passes. This record
does not select tagged dispatch, overload an existing A1c operation, or expose
the private material value through the public Interface.

## Preserved A1c Decisions

This reauthorization does not reopen:

- immutable snapshots and unique opaque lifecycle roots;
- non-Git proposal changes and the prohibition on proposal-as-snapshot;
- one Analysis Module, one `AnalysisState`, and deterministic projections;
- one SQLite-backed aggregate owner and atomic snapshot-dependent lifecycle;
- immutable, explicitly addressed analysis and readiness evidence;
- dependency-local coverage identity and independent completeness authority;
- opaque handles, typed uncertainty, and no ambient or current-state fallback;
- the current eight A1c operation roots and their behavior;
- agent-owned semantic judgment;
- Linux CPython 3.11 and 3.12 as the only accepted platform claim; or
- explicit authority and verification before canonical publication.

Mutable current-head resolution, invocation-only material, a synthetic
proposal snapshot, field or semantic-proposal salting, a composite external
analysis handle, and a second authoring-analysis state remain rejected.

## Version And Compatibility Obligations

The selected correction changes material identity and persisted state shape.
Contracts and Analysis must allocate distinct next versions for each role that
actually changes: AnalysisState current format, analysis identity domain,
handle schema, public generated contract, and store schema. Values are not
copied into a coordinated version bag and are not bumped when their owned
promise is unchanged.

Before a version or migration behavior is selected, a fresh inventory must
identify current producers, facade consumers, retained stores, independently
deployed engines, and supported overlap. If no real compatibility consumer
exists, use coordinated replacement and exact typed rejection of obsolete
state. If a supported retained consumer exists, admit one explicit migration
with transactional interruption evidence. Do not add speculative dual readers,
aliases from old to new analysis handles, silent reinterpretation, or fallback
to the current repository.

## Required Pre-Canonical Evidence

A2-P2R2 must decide the selected identity and replay design before P4R, P5, an
ADR amendment, or production planning. It must demonstrate:

1. two byte-distinct revisions over one base with identical declared analysis
   changes produce distinct canonical state bytes and analysis handles;
2. cold-process replay after proposal-head movement resolves the exact original
   revision through one Analysis authority;
3. snapshot-backed A1c analysis behavior remains unchanged;
4. missing, wrong-base, tampered, quarantined, expired, and purged revision
   dependencies reach exact typed outcomes without substitution;
5. real SQLite close/reopen and aggregate lifecycle preserve the exact revision
   dependency and never create independent retention;
6. the selected reference adds only bounded identity and resolver work rather
   than full-corpus-per-analysis storage; and
7. the complete oracle runs under dependency-complete Linux CPython 3.11 and
   3.12 environments and passes current standards, generated, package, plan,
   diff, and Commit checks.

Only a passing result admits an ADR and implementation re-plan. A failed
identity, replay, lifecycle, or single-authority invariant rejects the selected
representation and returns to the product owner; it does not reopen one of the
already rejected alternatives as fallback.
