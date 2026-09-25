# Exact draft-projection reuse — implementation and evidence

**Status:** implemented and locally verified; supported installed qualification and independent review remain separate.

**Branch:** `implementation/purpose-separated-standards-engine`
**Source base:** `2dd2ce1b`, the latest delivered capture/multi-read increment.
**Implementation commit:** `443d38e1`; existing test-spy adaptation: `68eb97c0`.
**Evidence date:** September 24, 2026.

## Target selection and bounded scope

The largest measured remaining consumer delay was repeated reconstruction of an
unchanged draft's complete edit history. The baseline at this source, after the
capture and multi-read improvements, still spent about 2.55 seconds on a twelve-edit
draft read and 2.66 seconds on status. Each read rebuilt twelve manifests and
compiled the final candidate. This outweighed the earlier approximately 0.1-second
schema-decoder opportunity. The [admission](performance-proposal-reuse/admission.md)
records the scope, applicable standards and owner boundaries.

This increment retains the pure projection of an exact immutable proposal revision
inside the existing bounded compilation cache. It improves repeated draft navigation
and workflow analysis, rather than changing test workloads or standards content.
Incremental successor construction, schema-decoder changes, public API changes and
additional cache services are outside the scope. A new revision still performs
complete replay from its original accepted base.

The remote branch observed at task start was `bac7dc3d`. The newer capture/multi-read
work was present in the previous delivered ZIP, not in that remote observation.
This implementation preserves and builds on that delivery. The new package supplies
both an incremental patch from `2dd2ce1b` and a cumulative patch/bundle from `bac7dc3d`.
No remote ref, real accepted main, installed store or Codex configuration was changed.

## Design and ownership

### One shared bounded retention owner

`CompiledSnapshotCache` now admits a tagged mix of accepted-snapshot compilation
and exact draft projections under its existing **two-entry / 32 MiB** total budget.
There is no second unbounded proposal map. Entries compete under the existing LRU;
disabled retention, unaccountable state, oversized entries and eviction use ordinary
full reconstruction with the same behavior.

The draft key binds exact frozen base bytes and paths, the existing canonical
encoding of the entire revision identity material, and the installed replay recipe.
Revision material includes the original base snapshot, repository membership,
proposal identity, ordinal and complete logical program. Neither the mutable head
nor a caller-supplied digest substitutes for that material. Logical Authoring exposes
a replay identity only for its exact stateless installed owner; changed recipes
miss, and stateful/closure-based adaptations remain cold consumers.

The cache returns shared read-only compiled/source structures. Its semantic-intent
maps are copied at admission and again for each hit, preserving operation ownership.
Current result envelopes and continuations are constructed afresh. The new regression
suite verifies mutations to caller results and intent maps cannot poison later reads.

### Validation remains before reuse

`query_proposal` reads and validates the actual stored revision and root first.
The first proposal material access in every public operation performs the existing
complete base-content load and identity verification before lookup. Subsequent uses
inside that operation retain its existing lifecycle observations.

The private Engine projection helper accepts an explicit reuse selection. Draft
navigation and the existing `ProposalMaterials` workflow path select it. Review,
physical candidate verification, application and recovery keep their fresh existing
replay paths. Their permissions, verification, conditional writes and observation
semantics do not depend on the cache.

Every status request still evaluates its current decision state. Current proposal
head, lifecycle, evidence and authorization checks remain at their existing
boundaries. A cached prospective revision after a failed conditional publication
is computation only: consumers still require a real stored revision/root.

### Failure, history and lifetime behavior

| Event | Behavior |
| --- | --- |
| Accepted main advances | New captures observe the new revision; an existing draft keeps its original base. |
| Exact old draft requested after later revisions | Return that historical material; current status may be stale. |
| Process replacement or cache disabled | Load and verify durable inputs, then replay normally. |
| Base quarantine/purge/corruption or revision corruption | Current validation rejects before retained material can answer. |
| Store missing/replaced | The current store must supply the actual revision and valid base. |
| Evidence or permission changes | Existing live checks decide; no result or decision is cached. |
| New prospective revision fails publication | Retention grants no stored identity, readiness or application status. |
| Compiler failure | Return the normal failure; retain no failed projection. |
| Owner closes | Release snapshot and draft entries together. |

The existing capture still performs two independent compiles and compares frozen
closure/signatures. The new implementation adds no persistence format, compatibility
branch, cross-purpose exposure, transport lifetime or shared SQLite connection.

## Measured consumer gain

The final paired workloads use the same host, isolated executable and core
dependencies, and one fixed disposable source/store at `2dd2ce1b`. The captured
corpus has **438 files / 3,796,413 source bytes**, with content identity:

`snapshot-content:sha256:7fe09d2cadb34a547b52362239268dd86ab43ed9c679b9768e20644a87e1ec5b`

The synthetic non-normative reference has real stored revisions with 1, 4 and 12
change sets. Queries and status request exact retained revisions; the first two
statuses are correctly stale after later revisions, while the twelfth is complete.
Both implementations return exactly equal complete values for the same requests.
Preparation and initial snapshot capture are excluded from operation timings.

### Repeated in-process MCP dispatch

Each history length has three repeated query/status observations after its initial
cold projection. Lower-level counters instrument loaders and manifest/compiler
owners without replacing the installed compiler recipe used by retention.

| Change sets | Operation | Baseline median | Candidate median | Speedup |
| --- | --- | ---: | ---: | ---: |
| 1 | `query_proposal` | 0.587 s | 0.203 s | 2.90x |
| 1 | `workflow_status` | 0.714 s | 0.305 s | 2.34x |
| 4 | `query_proposal` | 1.195 s | 0.187 s | 6.39x |
| 4 | `workflow_status` | 1.264 s | 0.288 s | 4.40x |
| 12 | `query_proposal` | 2.648 s | 0.189 s | 14.04x |
| 12 | `workflow_status` | 2.807 s | 0.284 s | 9.87x |

On twelve-edit warm queries, manifest rebuilds fall **12 to 0** and full compiler
calls **1 to 0**. Complete durable loads stay **1 to 1** for every independent call.
Status keeps **one fresh decision evaluation** per call. The same observations
hold at the shorter history lengths. This is removal of repeated derivation, not
removal of the material integrity proof or of decision evaluation.

### Real MCP subprocesses

Three new server sequences per implementation alternate baseline/candidate order.
Each contains initialization and three draft-read/status pairs for the same
stored twelve-edit revision. The first draft read includes cold reconstruction;
the repeated rows aggregate six observations from three process sequences.
Structured responses and JSON text encodings are compared exactly.

| Actual stdio operation | Baseline median | Candidate median | Speedup |
| --- | ---: | ---: | ---: |
| MCP initialization | 0.616 s | 0.626 s | 0.98x |
| First draft read, cold projection | 2.817 s | 2.801 s | 1.01x |
| Repeated query_proposal | 2.596 s | 0.192 s | 13.49x |
| Repeated workflow_status | 2.705 s | 0.287 s | 9.44x |

Startup plus three query/status pairs takes a median 16.800 s before and 4.685 s after (72.1% less elapsed time). Totals are formed per sequence before aggregation.

Cold reconstruction and admission still have a cost. These changes are intended
for repeated inspection/status and reuse of already-derived prospective material,
not an assertion that first construction or every new revision becomes constant
cost. Reading the stored program, forming an exact key and evaluating current
status still depend on the material and decision scope.

The representative base plus projection retains at most **13,616,068 accounted
bytes** in two entries, with no eviction in the measured sequences. The total
budget remains 32 MiB. This is conservative cache-owned accounting, not process
RSS or transient compiler-memory measurement. Bounds and close behavior are
verified separately. No full-suite or installed Codex speedup is inferred.

[Comparison CSV](performance-proposal-reuse/comparison.csv),
[baseline counts](performance-proposal-reuse/baseline-final.json),
[candidate counts](performance-proposal-reuse/candidate-final.json),
[actual stdio observations](performance-proposal-reuse/stdio-final.json) and
[sequence totals](performance-proposal-reuse/sequence-totals.json) retain samples,
ranges, output hashes and exact interpretation. Sample sizes establish local
medians/ranges rather than tail-latency guarantees. No test jobs ran concurrently
with the final comparisons. Fresh processes do not imply cold OS caches.

## Correctness evidence

The full discovered Engine campaign ran **232 tests**. It found one old instrumentation
callback that did not accept the new private `reuse` keyword. Its entire eleven-test
module passed after forwarding that keyword; all original independence assertions
remain. The twenty-one new projection-reuse regressions were also rerun successfully
against the final source. Production runtime bytes are unchanged across that fixture
repair. Thus all **232 distinct Engine tests have passing evidence**, rather than
one falsely reported all-green initial run.

The eleven supporting suites ran **450 tests: 449 passed and one existing
interpreter-dependent skip**. Combined unique population: **682 tests**, with passing
evidence for **681** and one skip. Qualification logs retain the initial failure
and both complete corrected/final module reruns.

The added regressions cover exact output and operation counts, fresh status,
historical/stale heads, caller mutation, current base and revision integrity,
quarantine/purge, missing/replaced stores, shared bounds and failure cleanup,
compiler-recipe changes, unpublished prospective records, main advancement and
cold readback, invalid evidence, authorization-triggered quarantine, independent
review replay, purpose restriction, two-pass capture and fresh stdio processes.
Existing multi-read, capture, publication and recovery tests remain in the full
population. An additional unchanged real audit/recovery scenario passed with a
warm first cache and cold independent second store; its original live-evidence,
interrupted-publication and readback assertions remain intact.

[Verification inventory](performance-proposal-reuse/verification.json),
[warm recovery](performance-proposal-reuse/warm-recovery-final.json) and
[source binding](performance-proposal-reuse/source-binding.json) distinguish the
observations. The separate [structural checkpoint](performance-proposal-reuse/structural.json)
passed **73 suites / 121 checks** against the final source. Structure and freshness
do not certify prose quality or independent implementation review. A post-commit
check is retained separately in the delivery evidence.

## Qualification limits and handoff

The environment is isolated Python **3.13.5**, outside supported 3.11/3.12, with
`rpds-py 2026.5.1` rather than locked `2026.6.3`. Other exact versions and executable
identity are in [environment](performance-proposal-reuse/environment.json).
Python 3.11 grammar parsing is supporting syntax evidence, not execution there.
Official SDK/configured-client and independent review were unavailable; the new
increment requires its own supported qualification rather than inheriting a prior
revision's review. Actual raw MCP execution is reported for what it proves.

Normative standards, reference/operational guidance, public Engine wire schemas,
persisted formats and locks remain unchanged from `2dd2ce1b`. The earlier delivered
capture/multi-read changes remain intact. This increment is not global acceptance
of the standards-content migration or of every proposed optimization.

## Reproduction

Use the supported locked environment with separate baseline (`2dd2ce1b`) and
candidate implementations. Create one disposable common workload from the baseline;
its private local main is the baseline candidate, not the user's accepted branch.
The workload directory must be new. Drivers write only their selected fixtures and
measurement files. Run sequentially:

```bash
python measure_proposals.py --source /path/to/baseline --fixture /tmp/draft-probe/repo --output /tmp/prepared.json --prepare
python measure_proposals.py --source /path/to/baseline --fixture /tmp/draft-probe/repo --output baseline.json --repeats 3
python measure_proposals.py --source /path/to/candidate --fixture /tmp/draft-probe/repo --output candidate.json --repeats 3
python measure_proposal_stdio.py --baseline /path/to/baseline --candidate /path/to/candidate --fixture /tmp/draft-probe/repo --output stdio.json --repeats 3
```

[Dispatch/history driver](performance-proposal-reuse/measure_proposals.py) and
[stdio driver](performance-proposal-reuse/measure_proposal_stdio.py) assert expected
results; the final comparison additionally checks baseline/candidate output hashes.
The ZIP includes exact Git CLI commits, incremental/cumulative patches, a bundle,
application instructions and file checksums. Use one application method and restart
the MCP process for the new installed recipe and empty initial cache.
