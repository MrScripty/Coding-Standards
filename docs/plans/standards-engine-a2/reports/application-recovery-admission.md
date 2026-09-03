# Application Recovery Admission

**Status:** `Accepted for Milestone 7 implementation`

**Exact base:** `992bd115017df53d41e413b0303d2ab92a1d0c0f`

## Question And Boundary

After `apply_proposal` has durably admitted a verified application but its
caller loses the response, can a caller holding only the readiness handle
rediscover the same application and establish the terminal result without
changing accepted apply semantics or adding a scan, mutable phase state, Git
retry, rollback, or guessed history?

The pre-run pass threshold allowed at most one new public operation and one
small immutable selection per admitted application. It allowed no table or
store-version change, generic aggregate enumeration, mutable application
state, retry loop, caller-supplied Git fact, or recovery Git write. Recovery
could write only the already-defined immutable applied outcome after observing
the exact candidate.

The routed standards set was CORE and Router, then Implementation,
Verification, Development Proportionality, Planning, Commit, Documentation,
Build, Contracts, Dependencies, Resilience, Architecture, Security,
Cross-platform, the Generated Contract and Persistence boundary profiles, and
the Library application profile. Release was assessed as an internal
coordinated contract evolution with no release artifact. No dependency change
was admitted.

## Design It Twice Comparison

Three candidates were compared in sequence:

1. A discovery operation followed by recovery would require generic aggregate
   enumeration or another index and two calls on the ordinary path. It was
   rejected as unused machinery.
2. Repeating `apply_proposal(readiness)` would change the accepted operation's
   meaning and could resume candidate materialization, verification, import,
   or Git publication. It was rejected as semantically unsafe.
3. One explicit `recover_application(readiness)` operation plus one immutable
   readiness-to-application selection preserved apply semantics and allowed a
   direct cold lookup. It was selected for the minimum viable tests.

The selected design keeps Authoring as the deep Module. The public Interface
contains only the readiness handle. The immutable selection is the private
seam from readiness to the content-bound application. The existing Snapshot
Module remains the persistence Adapter and Repository Git remains the target
observation Adapter. The selection and verified intent are admitted atomically
under the existing proposal-head guard; no second owner or mutable lifecycle is
introduced.

## Prototype Evidence

The disposable logic prototype is preserved at signed commit
`78033d3d65bdb003c57fa44940061a0df220c8a1` and
`refs/archive/a2-prototypes/application-recovery-logic`. Its single HTML file
exercised ten guided states under a Node DOM stub. All ten passed: admitted
candidate, existing outcome, unchanged target, different target, unavailable
observation, missing/corrupt selection, corrupt outcome, and denied,
unavailable, or unsupported authority. Every case performed zero Git writes;
only exact candidate observation wrote one outcome.

The real Git and SQLite MVT is preserved at signed commit
`685badf5dddb872aeaf5666e646dd8bdd2dc8479` and
`refs/archive/a2-prototypes/application-recovery-selection-mvt`. It passed
identically on Linux CPython 3.11 and 3.12. An interruption between the two
admission writes exposed neither record; a conflicting application rolled
back; cold recovery after a real expected-old-object ref transition resolved
the same content-bound application; recovery and duplicate recovery performed
zero Git writes and zero duplicate outcome writes. The immutable selection
payload was 218 bytes and store schema v2 was unchanged.

Both prototype worktrees and their temporary branches were removed after the
archive refs were verified. Neither prototype source was merged or copied into
the production branch.

## Decision

The design passes the four required dimensions:

- Effectiveness: readiness alone recovers the exact admitted application
  across process replacement and lost response.
- Efficiency: one operation, one 218-byte immutable selection, one lookup, and
  no scan, table, store migration, or repeated verification/publication.
- Correctness: admission is atomic; authority is current; a durable outcome is
  historical authority; without it, only the exact candidate proves applied.
  The expected target remains uncertain, another target is diverged, and an
  unavailable observation remains unavailable.
- Standards compliance: the design follows existing A1c/A2 ownership and
  generated-contract seams, adds no dependency or standards-graph member, and
  stops investigation at a reversible production slice with no unresolved
  irreversible or high-consequence design issue.

Milestone 7 may therefore add the one generated operation and capability,
atomic guarded aggregate-set publication, immutable selection and exact
decoder, target observation, facade/renderer projections, focused tests, and
the mechanically required generated evidence. Recovery must never require the
current proposal head, because admission already proved it; possession of a
readiness handle grants no authority. Existing pre-Milestone-7 applications
without a selection receive typed `APPLICATION.NOT_ADMITTED`; no scan fallback
or compatibility migration is justified by the current coordinated internal
consumer inventory.

## Limits And Re-plan Triggers

The prototypes did not prove the complete generated facade, current production
authorizer, real Engine close/reopen path, corrupt production decoder, or full
repository checkpoint. Focused production and repository verification own
those claims. Re-plan if recovery needs to stage or publish Git, if more than
one application can be selected for a readiness, if a retained external store
requires old-intent discovery, if the canonical target is no longer the fixed
local `refs/heads/main`, or if recovery needs a second persistence owner.
