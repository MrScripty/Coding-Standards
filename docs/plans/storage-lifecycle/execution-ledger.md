# Execution ledger

> **Current disposition (2026-09-27): Accepted.** Acceptance owner reconciled the exact-source CI, preserved external verdict and plan-specific evidence. The slice is Accepted; implementation-stage pending notes below remain historical. See the [acceptance-owner decision](../typed-routing-edits/reports/acceptance-dispositions.md).

## 2026-09-27 — Admission

User selected audit stage Storage lifecycle. Admitted `start` at `docs/plans/storage-lifecycle/plan.md`. Verified GitHub head `0f24bac9b5bf773e9981bc027d6afd409607e89e` and Actions source ZIP SHA-256 `bf2d8b356ca8cd7be6b1eb3f730bd0f107d83ee2e856a204644804777adbf454`. The source clone is clean, on private branch `implementation/storage-lifecycle`, with main held at the verified source. No operator store/configuration is mounted.

Executed Router with explicit facts (25 selected modules, zero unresolved questions) and exact policy readback. Baseline snapshot suite: 23 passed. Source inspection confines production changes to one store file; no snapshot module or Engine signature change is required. The no-migration path repeats full integrity/foreign-key checks; the purge path acquires a writer before looking for due work.

Supported Python provisioning was attempted in a private directory and failed at DNS resolution. Lock and system environment remain unchanged; supported runtime qualification is still required.

## Regression-led implementation

Three targeted regressions reproduced the old no-work BUSY outcome, duplicate
current-store full audit, and writer admission before a failing probe. Added the
short-lived, explicitly closed existence query and preserved the under-guard due
selection. The private admission method now returns its verified source version;
only a current-version admission omits the redundant final full audit. Original
migration checks and new-store checks remain unchanged.

The first expanded snapshot suite exposed one new test expecting the aggregate
record error for an aggregate root. The actual root error is
`AGGREGATE.ROOT_UNAVAILABLE`; the fixture assertion was corrected without changing
production diagnostics. Final snapshot selection: 40 passed (17 added methods).

Two initial cold-MCP test commands exceeded their execution-tool call limits while
running the first test; neither completed verdict is counted. The same tests are
run under an owned job process with complete captured results. No production timeout
or SQLite busy-budget setting was changed.

## Final local verification and scope review

The first complete cold-MCP attempt exposed a new test's incorrect assumption that
store-open failure returns structured domain data. The established transport emits
generic public failure text and exact private stderr; the test now checks that
boundary. No MCP runtime change was made. A later interrupted single-test command
had no completed verdict and is not counted.

Held runtime and test source fixed for the complete final campaign: 547
Engine tests passed in four file-disjoint selections, with zero failures or skips.
The eleven supporting suites executed 567 tests: 565 passed and two environment
skips. The root-inapplicable permission case separately passed under nobody.
The 19 new lifecycle methods are included in these totals. Final documentation
and generated input hashes were finalized after the campaign and verified again.

Baseline/candidate current-store benchmarks used six counterbalanced paired samples
per source at each of 0/8/32/64 MiB synthetic aggregate payload. At 64 MiB median open
decreased from 83.08 to 42.01 ms. The default-busy contention reproduction changed
from a 5.009-second BUSY rejection to a successful 0.264 ms active read. Full audit
semantics and genuine-due BUSY remain; these are local observations, not a deployment
latency promise. Instruments, raw samples and row equality are in delivery evidence.

Real old/new processes reopened baseline-created snapshots, Analysis and readiness
unchanged. Actual evidence corruption rejected with ANALYSIS.EVIDENCE_DIGEST_MISMATCH;
restored bytes reproduced readiness. Accepted main did not advance. All eight
catalogs, public schemas, generated contracts, locks and SQLite schema/migration
hashes are unchanged. Production changes remain 22 added and 5 removed lines in
one store owner; no new runtime module, option, cache or migration was added.

Status is Verifying, acceptance partial. Supported locked CI and independent
material review remain required. No commits, pushes, merges, production-store
changes or host configuration edits were made. Source ZIP reconstruction is
recorded under DELIVERY; the next slice is integration qualification only.
