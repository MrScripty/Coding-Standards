# Batched capture and bounded multi-read — implementation and evidence

**Status:** implemented and locally verified. Supported installed qualification and
independent review remain separate.

**Branch:** `implementation/purpose-separated-standards-engine`

**Base:** `bac7dc3dc39fbf519429ea91bff1e02e65925299`

**Implementation commit:** `3d92a78b`

**Evidence date:** September 24, 2026.

## Outcome and scope

The user selected faster fresh capture and a grouped-read API from the consumer
performance investigation. The [admission](performance-capture-multiread/admission.md)
records the owner boundaries, scope, applicable standards and unchanged promises.
This increment implements those two changes. Proposal-projection caching,
selective compilation, decoder optimization, standards rewriting and test-runner
parallelism remain separate concerns.

Repository Git owns the batch process, frame validation, decoded-tree reuse and
session cleanup. Engine navigation owns a bounded same-snapshot reading set.
Canonical Engine schemas own the interface shape, with regenerated native models,
tool definitions and examples. Existing purpose, store, snapshot, authorization,
publication and recovery owners retain their contracts.

## Capture pipeline

`RevisionReadSession` keeps one active `git cat-file --batch` child and reuses
verified object bytes and decoded immutable tree tables. Switching to an explicit
mapped repository closes the preceding child and opens the selected repository;
the cache key still includes repository, object ID, type and hash algorithm.
There is no global process or repository cache.

Each object miss validates header framing, type, bounded declared size, complete
body framing and the actual object hash. Mode and path traversal checks remain
active on every file resolution. One-shot reads and the batch transport use the
same object-verification functions. A failed exchange closes its stream and does
not retry the operation.

One pipe-exchange worker and one bounded stderr drain belong to the child. Each
exchange retains the existing Git command timeout, including pipe writes; it is
not a whole-capture deadline. Normal closure checks trailing output and exit,
then reaps the child and joins workers. Failure or caller interruption aborts the
owned process (its process group on POSIX), reaps it, and releases streams/workers.
These failure paths were exercised on Linux; Windows execution is not claimed.

Raw object payload and decoded-tree allocations share the existing 8 MiB /
1,024-entry LRU budget. Tree tables are immutable views over validated built-in
structures, with conservative allocation accounting. Oversized tables remain
uncached and eviction changes cost only. The budget is not a total process-RSS or
transient-read-memory limit; existing individual object limits still apply.

Accepted `main` is resolved once. Its exact revision supplies the recorded pass.
The session closes before the independent frozen compiler pass. Both requested
path closure and semantic signatures are compared before snapshot publication.
Old explicit snapshots continue reading captured bytes, independent of new main.

## Multi-read interface

Engine interface **32** adds `read_many` to the native facade, focused MCP catalog
and generated reference CLI. Other owned version domains remain unchanged.
Each request supplies an explicit snapshot and **1–32 ordered item specifications**.
Exact duplicate specifications reject. Each item has a target and optional detail;
authoring additionally permits the existing coverage/routing read options.

```python
result = facade.read_many({
    "snapshot": snapshot,  # The exact handle returned by route or read.
    "items": [
        {"target": "core"},
        {"target": "workflow.implementation"},
        {"target": "workflow.verification", "detail": "full"},
    ],
})
```

The entire ordered set succeeds or one bounded rejection returns. A failed item,
invalid option, unavailable dependency or lifecycle change returns no preceding
item content. Single-item projection and focused continuations are shared with
ordinary reads; the API does not expand the requested set automatically.

The complete domain result is limited to **2 MiB under default JSON encoding**
(ASCII escaping and default separators). This includes the result envelope and
item values, but not protocol framing, pretty-printing or MCP's duplicated
structured/text encodings. Over-budget results reject without truncation; callers
can select fewer items or narrower policy scopes.

One complete durable content and identity validation supplies the operation.
Snapshot lifecycle is observed before each item and before final return. Current
host purpose and ordinary exposure/dependency rules still govern every projection.
A new independent request performs its own full integrity check, even with a warm
compiled cache. This scope introduces no new cross-call cache or mutable session.

`read_many` is a named operation, not a new `query`/`query_proposal` request variant.
It requires a snapshot rather than implicitly capturing main. Existing single-read
and capture semantics remain unchanged. Reconnect the client and restart the MCP
server to load the new interface; authoring focused discovery adds one tool and
application discovery adds the corresponding restricted variant. Official SDK and
configured-client harnesses were updated to exercise it.

## Measured performance

Capture compared baseline/candidate code against the same accepted fixture at
`bac7dc3d`: **437 files, 3,757,063 source bytes and a 4,530,176-byte temporary store**.
Three serial samples per implementation excluded fixture preparation and Engine
construction. Attribution counters ran separately from those timing samples.
Both implementations returned the exact same source revision and content ID:

`snapshot-content:sha256:99a23add9dfa4f48711c1945dc0d133cf00dc44808f2ac9cfc00481690dc49f3`

| Capture observation | Baseline | Candidate |
| --- | ---: | ---: |
| Median capture | 2.001 s | 0.661 s |
| Range | 1.981–2.233 s | 0.658–0.695 s |
| Git processes | 529 | 3 |
| `cat-file` processes | 527 | 1 |
| Tree parses | 3,872 | 89 |
| Full compiler passes | 2 | 2 |
| Logical source reads | 1,140 | 1,140 |
| Peak accounted session bytes | 3,793,805 | 4,007,360 |
| Peak retained object entries | 527 | 527 |
| Retained bytes/entries after close | 0 / 0 | 0 / 0 |

Capture is **3.03x faster (67.0% less elapsed time)** in this comparison. Parsed
reuse accounts for approximately 209 KiB more retained session data; it remains
inside the existing budget. Full process memory was not measured.

Multi-read used real MCP subprocesses and six selected real module bodies over
one synthetic qualified snapshot. The fixture has **437 files / 3,757,909 bytes**;
its approvals are benchmark-only records, not qualification of real standards.
Every comparison used the same snapshot, implementation, server, purpose and
ordered items. An initial explicit read warmed existing compilation. Five paired
comparisons per purpose alternated six-call/grouped-call ordering.

| Actual warm stdio workload | Six separate reads | One `read_many` | Speedup |
| --- | ---: | ---: | ---: |
| Application purpose, median | 1.051 s | 0.183 s | 5.76x |
| Application range | 1.041–1.083 s | 0.177–0.219 s | — |
| Authoring purpose, median | 1.115 s | 0.249 s | 4.47x |
| Authoring range | 1.099–1.151 s | 0.240–0.266 s | — |
| Complete durable loads, each purpose | 6 | 1 | — |

All ordered item values matched exactly. Structured MCP content and its text JSON
were independently compared. The selected item payload is about 93–94 KB. This is
the completed public API, not the earlier experimental kernel. Capture/init and
model tool-selection latency are outside the grouped-read timings. Sample counts
support medians/ranges, not p95/p99 or an installed-client/full-suite speed claim.
Baseline and candidate use identical executable bytes and dependency versions;
local configuration limits are recorded below.

[Comparison CSV](performance-capture-multiread/comparison.csv),
[capture baseline](performance-capture-multiread/capture-baseline.json),
[capture candidate](performance-capture-multiread/capture-candidate.json) and
[multi-read observations](performance-capture-multiread/multiread-stdio.json)
retain exact inputs, counts and observations. Inclusive work is not added twice.

## Correctness evidence

The full serial Engine discovery run passed **211 tests**. Eleven supporting
package suites ran **450 tests: 449 passed and one existing interpreter-dependent
skip**. Combined, this is **661 tests run, 660 passed and one skipped**.
The Engine runner itself was serial; supporting suites used a separate process
during its early execution. These are correctness results, not paired suite-speed
measurements.

Twelve new Repository Git tests cover fragmented binary frames, one-process reuse,
missing/type/size/truncation/hash failures, oversized stderr, exchange/shutdown
timeouts, nonzero exit, startup failure, caller interruption, tree reuse, bounds
and cleanup. Existing real Git SHA-256, corruption, gitlink and cache cases remain.

Twelve new Engine tests cover ordered equality and one durable load, all existing
single-read result kinds, 1/32 limits, duplicate/invalid/privileged input, hidden
items and whole-request rejection, exact result-budget boundaries, quarantine
between items and after the final item, warm-cache corruption, cold reopening,
purpose-specific schema discovery, and actual CLI/two-fresh-MCP-process output.
Existing publication, authorization, main advancement, independent replay and
cold-recovery tests passed without relaxing assertions or changing capture.

After the full run, one MCP set-literal formatting correction preserved its parsed
AST. All **13 MCP tests and 12 multi-read tests** then passed against that exact
final code in the qualified disposable candidate context. A trial rerun from the
source checkout encountered `SUPPORT.UNSUPPORTED_CAPTURE` because its preserved
accepted main still has the older contract. The corrected rerun used the documented
disposable candidate main; production capture was not changed to accommodate it.

The [verification inventory](performance-capture-multiread/verification.json) and
[source binding](performance-capture-multiread/source-binding.json) identify exact
scopes. The final structural checkpoint is recorded separately in
[structural evidence](performance-capture-multiread/structural.json). Its expected
population is **73 suites / 121 checks**; it proves declared structure and generated
freshness rather than functional correctness or semantic standards quality.

## Qualification and delivery limits

Local execution used isolated **Python 3.13.5**, outside supported 3.11/3.12, with
`rpds-py 2026.5.1` rather than locked `2026.6.3`. Other core package versions and
executable hashes are in [environment](performance-capture-multiread/environment.json).
The official MCP SDK, configured Codex executable and independent reviewer were
unavailable. Supported locked-environment, official SDK/configured-client and
independent review qualification remain required for this new interface/capture
implementation. Real raw MCP results are not substituted for those claims.

Normative standards, reference and operational guidance content, dependency locks,
identity framing, persisted state and SQLite policy remain unchanged. Only the
new read API advances its wire interface. The source checkout keeps real accepted
main at `366c1d9`; disposable clones own their candidate main for qualification.
The user's installed store, archived proposals and Codex configuration were not
accessed or modified. Delivery is a Git CLI commit bundle/patch and complete changed
files; application and merging into main remain explicit operator actions.

## Reproduction

Run the included drivers from the supported environment with separate baseline
and candidate implementation checkouts and a common fixture checkout whose local
main points to `bac7dc3d`. They write only disposable repositories/stores and the
chosen evidence file.

```bash
python measure_capture.py --source /path/to/base --fixture /path/to/common-fixture --output capture-base.json --repeats 3
python measure_capture.py --source /path/to/candidate --fixture /path/to/common-fixture --output capture-candidate.json --repeats 3
python measure_read_many.py --source /path/to/candidate --fixture /path/to/common-fixture --output reads.json --repeats 5
```

[Capture driver](performance-capture-multiread/measure_capture.py) and
[grouped-read driver](performance-capture-multiread/measure_read_many.py) retain
validation assertions, corpus identity, alternating order and separate attribution.
The new API does not infer approvals for real application content.
