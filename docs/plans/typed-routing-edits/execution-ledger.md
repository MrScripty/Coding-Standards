# Execution ledger

2026-09-27: admitted `start` against the latest main commit `cbf9cdd2`. Its capture
handoff is already integrated. Verified source tree and Actions archive digest;
created independent baseline and candidate checkouts. The Router returned 24
selected modules and no unanswered applicability. No source mutation to user or
remote resources. Local Python is 3.13.5/rpds-py 2026.5.1; use the unchanged locked
supported CI for environment acceptance.

Design choice: keep authored declarations distinct from compiled semantic facts
and bound programs. Reusing a compiled FactContract here would normalize metadata
and validate dependent facts too early. The pilot owns value retention and typed
edit dispatch only; schema validation and applicability remain at existing owners.

- The original serialization regression failed for all four JSON-backed routing
  variants; the candidate passes with no inner JSON decoder call. Ten focused
  representation tests and six projection tests pass. The 31 original logical
  authoring tests also passed in that initial focused selection (47 total).
- An independent baseline/candidate run on the same baseline authority matched
  23 scenarios exactly: eight successful projections and fifteen rejections.
  Normalized records, map/array order, facets, revision IDs, aggregate hashes,
  every projected file hash, semantic signatures and failure stage/code/message
  match. The baseline produced real retained routing proposal/revision/readiness
  records for cold candidate readback.

- Review identified Python's boolean/integer equality as an ambiguity for the new
  declaration values. Authored equality now compares scalar types as well as values,
  preserving the former canonical-JSON distinction without introducing a semantic
  evaluator. A direct regression covers true, one, null and mutable nested input.
- The actual retained baseline workflow uses all four routing edit forms in two
  revisions, reaches readiness with real fixture evidence, and remains unpublished.
  Warm-status instrumentation observes 52 inner routing JSON decodes at the baseline
  and zero with typed values, with identical structured status. Measurements are
  operation counts and bounded inner-serialization timings, not end-to-end latency.

- Final composition review keeps routing parse checks in logical_authoring.py,
  where their validation primitives already belong. The new routing_edits.py
  depends only on standard-library value types; no reverse import into the logical
  compiler remains. The initial Engine campaign was stopped before acceptance and
  is retained separately; the complete selection is restarted on the frozen source.

- The final frozen production run passed all 589 Engine methods in four disjoint
  shards, including 20 new typed-routing methods. Supporting packages passed 568
  tests with two existing environment-dependent skips. Full baseline/candidate
  differential and eight real replacement-process observations passed. Runtime
  files remain exactly the hashes recorded before the final suite.
- A measured 400 standalone routing serializations now make zero inner JSON loads;
  a warm retained status still serializes 52 edit records but no longer decodes
  52 inner payload strings. Exact structured status is preserved. Timing samples
  are not claimed as general latency, memory or model-cost improvements.
- T1 source implementation is complete; plan moves to Verifying with one next
  slice, T2 locked CI and independent review. Current docs and verification inputs
  are finalized, followed by a focused rerun and structural/freshness checks.
  No public interface, store, operator configuration or remote ref changed.
