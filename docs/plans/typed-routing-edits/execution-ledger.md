# Execution ledger

> **Current disposition (2026-09-27): Accepted.** Acceptance owner reconciled the exact-source CI, preserved external verdict and pilot claims. The pilot is Accepted; implementation-stage pending notes below remain historical. See the [acceptance-owner decision](reports/acceptance-dispositions.md).

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

2026-09-27, T2 integration reconciliation: the exact pilot commit is
`7d563f032267d8d96fd45675147b9de7206a7cac`, tree
`fa5722c82a2cb6cd260e5cef8001137bbd1e412b`, directly after `cbf9cdd2`.
GitHub `main` contains that commit; there is no pilot PR or task branch. The
repository's Python 3.12 hash-locked [CI run 36358571883](https://github.com/MrScripty/Coding-Standards/actions/runs/36358571883)
passed on the exact commit: all twelve package selections and the complete
structural verifier. A separate clean-checkout run on the same tree used Python
3.12.3 with all six runtime packages at the unchanged lock's versions. It passed
589 Engine and 570 supporting tests, with no skips, plus 73 structural suites
and 121 checks. These are repeated executions of the same tests, not additional
distinct tests; the earlier Python 3.13 campaign remains separate. A fresh
read-only internal reviewer found no A1–A5 blocker and one
non-blocking float-zero advisory. This is not the required external review;
acceptance remains blocked pending that reviewer and finding disposition.

The five preceding source slices are integrated, each has a successful
exact-source GitHub workflow run, and each still records an external material
review requirement. Their plans are not silently marked Accepted. The
[sequence reconciliation](reports/verification.md#sequence-reconciliation) binds
their commit/run pairs. No additional implementation slice is admitted; the
sequence's acceptance closure waits for the outstanding reviews.

Documentation-only closure check: changing `docs/plans/README.md` made its
generated suite-input digest stale. Recompiled the manifest in an isolated
copy of the exact candidate plus the planned record edits; the resulting diff
changes only that index digest. The complete structural checkpoint then passed
73 suites / 121 checks. This record update does not change the source revision
covered by the successful hosted CI run.
