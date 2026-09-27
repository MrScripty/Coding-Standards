# Verified snapshot-capture handoff

**Plan status:** Verifying
**Acceptance status:** pending — A6 exact-diff CI and independent review
**Admission:** `verify`, source implementation and local qualification complete.
**Base:** `6fa41c3105a6d1d4a49230ad367ae83d3afc472c`, interface 44.
**Current phase:** C1 Implemented; integration acceptance pending.
**Next slice:** C2 — exact-diff supported-runtime CI and independent review.

## Objective and scope

Keep both independent live-recorded and frozen-replayed capture compilations, but
reuse their proved frozen result on the first subsequent snapshot observation.
Preserve exact schemas, result bytes, identities, store admission, fresh lifecycle
and evidence checks, resource budgets and historical reconstruction. This is one
internal capture/cache handoff, not another cache, schema API, persisted proof,
publication permission or compilation mode. Typed routing-edit work remains deferred.

The latest upstream commit and its source artifact/tree are verified. Only this
clean task-owned checkout and disposable test stores are modified. The executable
Router returned no unresolved task facts; all 24 selected standards were read.
The live operator's repository, stores, host configuration and unrelated ZIPs are
not write targets. The base workflow run is observed separately from this diff.

## Binding design and composed review

1. Engine capture owns the live recorder, independent replay, requested-path and
   semantic-signature agreement, durable snapshot admission and returned handle.
   CompiledSnapshotCache owns only bounded reusable identity/compilation material.
2. The result may be offered to that existing cache only after both proofs and
   successful snapshot publication/result construction. The same captured compiler
   function identity is associated with its result. The recording wrapper is
   replaced by the exact immutable frozen source; no Git reader or live recorder
   is retained by the successful handoff.
3. The cache entry is keyed by exact CapturedContent, not an admitted handle or an
   asserted stored content ID. Normal observation still loads/verifies durable
   bytes, compares computed identity with the stored identity, and applies its
   current lifecycle and qualification checks before compilation reuse. Capture
   handoff does not add a redundant store read or cache a permission decision.
4. Existing compiler eligibility and count/byte budgets govern retention. Disabled,
   undersized, evicted or non-stateless compiler cases use the ordinary cold path.
   No increased default, pin, second lifetime or background task is introduced.
   Adding the identity proof to a capture-seeded entry preserves its existing exact
   key, so a later equal store load does not retain a second full copy of its bytes.
5. The Engine supplies the already proved result; the cache decides retention.
   Future compilation changes alter the existing compiler-identity match. Store
   changes are checked by the snapshot owner, not inferred by the cache. Exact
   fact/material projections and canonical digest formats remain unchanged.
6. Tests isolate admission ordering, both proof passes, cache eligibility, exact
   source/result preservation, bad closure/persistence rejection, corruption,
   quarantine, eviction, code changes and fresh-process behavior. Profiler counts
   use original function identities rather than replacing the compiler with a mock.
7. The only new runtime capability is retaining a caller-proved compilation in the
   existing owner. Deleting it would restore the measured third compile. Reusing
   this retention path after ordinary cold compilation avoids a second retention
   policy. No validation framework or additional permanent module is necessary.
8. Interface 44, input/output catalogs and all persisted versions remain unchanged.
   A normal process restart loads updated Python; no configuration or state migration
   is needed. Accepted Git refs and publication/recovery authority remain separate.

## Write set and acceptance

Production: `tools/standards_engine/standards_engine/engine.py` and
`compiled_cache.py`. Tests: `tools/standards_engine/tests/test_capture_handoff.py`
`tools/standards_engine/tests/test_capture_handoff_transport.py`,
and a directly affected existing assertion only if its old work-count assumption
is demonstrated obsolete. Documentation: Engine README, this plan/ledger/issues/
verification, the plans index and the generated verifier suite-input manifest.
The prior fact-ownership/working-set plan may link to this owner of its deferred
capture slice without changing that plan's acceptance evidence. Normative policy,
contracts, locks, dependencies, host configuration and user data are excluded.

- A1: fresh cache-eligible route/read performs two independent proof compilations,
  not three, and returns exactly the cold result for the same snapshot.
- A2: closure, semantic or persistence failure does not seed the capture result;
  no recording wrapper/live source is retained by a successful handoff.
- A3: durable identity/content and lifecycle checks still run before cache reuse;
  corrupted/missing/quarantined material cannot be answered from the cache.
- A4: compiler changes, stateful adapters, resource limits, eviction, close and
  replacement processes preserve ordinary semantics and bounded lifetime.
- A5: public contracts/catalogs and baseline-produced retained observations remain
  unchanged. Generated freshness, focused/affected suites, static checks and exact
  package reconstruction pass. Measured counts are not latency or billing claims.
- A6: exact-diff supported-runtime CI and independent external review are required
  for Accepted status; unavailable execution evidence remains explicit.

C1 completes implementation and its local evidence. The next acceptance slice after
C1 is integration with supported CI and independent review. Replan if the proposed
handoff bypasses live authority or exact identity, requires extra retained state,
changes public/domain meaning, or makes capture success depend on cache retention.

## Implementation disposition

C1 is **Implemented**. Local evidence satisfies A1–A5 at the representative boundaries
described in [verification](reports/verification.md); A6 remains pending at its
integration/reviewer owners. Fourteen new methods and the complete 569-test Engine
selection passed, along with the supporting packages, contract preservation and
actual cold transport/state comparisons. The final delivery records its own focused,
structural, patch and file-hash checks. No live model run is inferred.

There is one next slice, C2. Run the unchanged supported lock on this exact diff and
obtain independent material review before Accepted status. Restart the normal MCP
process only to load new code, preserving arguments, catalogs, stores and handles.
Typed routing-edit work remains a separate deferred recommendation.
