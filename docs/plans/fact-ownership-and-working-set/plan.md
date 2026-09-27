# Canonical fact ownership and focused revision working set

**Plan status:** Verifying
**Acceptance status:** pending
**Admission:** `start`, user-authorized implementation of the next refinement from the review.
**Base:** `87873de5e1405590209dad389f7010a6b61f0bbe` (interface 44).
**Current phase:** local integrated verification complete; external acceptance pending.
**Next slice:** A — supported-runtime integration and independent acceptance review.

## Objective and scope

Separate canonical routing-material identity from agent presentation, then retain
the useful accepted-base/successor working set in the existing bounded process
cache. Preserve public results, canonical/persisted identities, actual store and
head checks, scope, byte limits, and evidence/authorization. No new MCP operation,
interface edition, persistence migration, cache capacity or storage mechanism.

The current upstream head and source artifact digest were verified. The clean,
task-owned checkout is the only source write target. Existing remote branches,
operator configuration, user stores and unrelated ZIPs remain untouched. The
executable Router selected explicit implementation, verification, planning,
documentation, build, immutable replay, contracts, architecture, performance and
boundary guidance with no unanswered conditions. Exact readings are delivery
evidence. The prior reviewed recommendations for snapshot-capture handoff and
typed routing-edit values are deferred rather than silently added to this slice.

## Binding decisions and composed-design review (applicable)

1. Produced artifact: one canonical fact-record method on the existing
   RouterProjection, its coordinated consumers, and one cache-retention correction
   in the existing CompiledSnapshotCache. Routing semantics belong to Analysis;
   current authority remains with snapshots, authoring and the Engine. Navigation
   consumes the exact canonical records without defining review material identity.
2. Required interleavings: the record's exact eight fields, ordering and empty lists
   must remain part of the existing router-material contract. Cache use requires
   caller-verified exact material; recency is only computation lifetime, never
   evidence of admission, current head, approval or publication.
3. Caller knowledge: consumers ask the RouterProjection for its fact records.
   Existing projection callers already supply the verified compiled base; no new
   keep-alive handle or retention flag is required. The cache alone owns eviction
   under its existing count/byte limits.
4. Representative changes: formatting a navigation response affects only that
   projection. Changing canonical fact fields/order is an explicitly reviewed
   router-contract change. Changing retention policy stays in compiled_cache.py;
   revision/head/evidence validity does not move into the cache.
5. Dependencies: supporting-material composition now depends on the public
   RouterProjection owner, not agent_navigation. Cache retention recognizes the
   exact compiled base object already retained; it cannot match a different base
   merely by a claimed revision or digest.
6. Independence: fact projection has literal-field and baseline-digest oracles;
   the cache change has real focused and native revision/status sequences, cold
   equivalence and failure/limit tests. Either refinement can be tested without
   changing the other or the underlying public contracts.
7. Deletion test: no new permanent module, service, registry, cache, serializer,
   validator or version is added. The old navigation-owned projection disappears
   with its direct consumers. Removing the recency adjustment would recreate the
   demonstrated transition miss, not remove a domain obligation.
8. Inherent complexity remains with the existing canonical projection and bounded
   cache. Successful successor construction makes its actual retained base recent
   before insertion, so a borrowed predecessor does not displace it by accident.
   Failure, disabled/tiny budgets and missing retained bases retain ordinary
   behavior. Historical revisions remain reconstructable after eviction.

## Milestones and write set

### R1 — canonical fact projection

**Status:** Implemented; local exact-record checks passed.

Move the exact current field/order definition into
`tools/standards_analysis/standards_analysis/routing.py` as a RouterProjection
method. Update all `fact_definitions` consumers in Engine `agent_navigation.py`,
`supporting.py`, `context_projection.py` and `engine.py` in one change. Add focused
Analysis and Engine tests for empty values, exact field/order and fresh return
values, actual binding preservation and isolation from presentation mutation.
Update the owning package documentation. No generic FactContract serialization
substitution or new digest is permitted.

### R2 — focused revision working set

**Status:** Implemented; focused and full-suite evidence passed.

Update `tools/standards_engine/standards_engine/compiled_cache.py` to recognize the
exact already-retained compiled base as used when retaining a new successful
projection. Preserve two entries / 32 MiB defaults and the existing exact keys,
function-identity checks, accounting and predecessor borrowing. Tests cover focused
and native transitions, repeats/historical reads, disabled/undersized/one-entry
caches, changed material, error paths, scope and lifecycle checks. No base pin or
unbounded operation-retention mechanism.

### V — integration evidence and delivery

**Status:** Locally verified; final delivery checks are recorded in the archive.

Run both regressions before/with changes; retain their initial failures. Execute
relevant package and Engine checks, including real cold MCP/retained-state evidence.
Record operation counts and accounted resident bytes, not guessed time/token
savings. Refresh only generated verification-input artifacts through their owner
and confirm normal generated contracts/catalogs are unchanged. Review/stage only
the explicit diff, reconstruct a base-pinned ZIP, and keep unavailable acceptance
requirements visible. Scoped source documentation, this plan/ledger/issues/report,
`docs/plans/README.md` and `suite-inputs.json` are included in the write set.

## Acceptance claims and gates

- A1: current eight-field records/order, rule facts and material bindings remain
  identical; navigation-only edits cannot redefine authoritative material.
- A2: a real fact-contract change still changes the owning material binding.
- A3: default focused revise → status avoids redundant base identity/compile work;
  native revision behavior, response equivalence, historical reads and bounded
  memory remain valid.
- A4: retained computation never bypasses current lifecycle, current-head, exact
  evidence or rejection rules, including failure and cache-disabled paths.
- A5: producer/consumer, generated freshness, independent oracles, package/static
  checks and patch reconstruction pass for this diff. Preserve normative authority,
  public/schema/state versions and unrelated source.
- A6: supported locked-runtime CI and independent external material review before
  Accepted status. Local execution alone does not qualify that environment/review.

## Blockers, exclusions and re-plan conditions

No known source-implementation blocker. Python 3.13.5 and rpds-py 2026.5.1 are
available locally, not the supported locked 3.11/3.12 environment. Actual client
credentials and independent reviewers are not available; no live-model result will
be invented. A no-behavior-change ownership/cache slice does not require changing
host configuration or rerunning an unrelated publication exercise.

Replan if identities/result semantics differ, if a cache entry can satisfy authority
without fresh checks, if the proposed retention requires extra capacity/state, or
if another owner must change the same invariant. Record independent future work in
[issues](issues.md). Verification and material deviations go in the
[execution ledger](execution-ledger.md) and [report](reports/verification.md).

## Current acceptance disposition

A1–A5 have local source, independent-oracle, complete-suite and reconstruction
evidence recorded in [verification](reports/verification.md). A6 remains pending
on the supported locked environment and independent external review. Exactly one
next slice is active for handoff: A — integration acceptance. No compatibility or
new cache mechanism is retained/introduced to compensate for unavailable review.


## Deferred capture work ownership

The separately authorized [snapshot-capture handoff](../snapshot-capture-handoff/plan.md)
now owns that deferred recommendation. It does not change this plan's earlier
scope, qualification evidence or pending acceptance. Typed routing-edit work
remains deferred and is not included in either implementation.


### Scoped continuation: typed routing edits

[Typed Routing-Edit Pilot](../typed-routing-edits/plan.md) now owns the separately
admitted routing-family experiment. It does not change the acceptance evidence
or implementation status of this fact-ownership/working-set plan. Other edit
families remain deferred; the capture handoff has its own plan.
