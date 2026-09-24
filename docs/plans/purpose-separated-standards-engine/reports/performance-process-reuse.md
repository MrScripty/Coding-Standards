# Process-owned interface and immutable-compilation reuse

**Status:** implemented and locally verified; installed supported qualification and
independent implementation review remain separate.

**Branch:** `implementation/purpose-separated-standards-engine`

**Base:** `b81a5aae2eb72fb976b0570a4dab76d30e531fe4`

## Objective and admission

Improve repeated explicit-snapshot MCP interactions by retaining the installed
API contract and a small amount of pure compiled snapshot material. Preserve the
per-call Engine, facade and SQLite lifetime, all required content verification,
current lifecycle/authorization observations, and exact publication/recovery.

The [bounded admission](performance-process-reuse/admission.md) records the
applicable standards, write set and composed-design decisions. Interface reuse
was implemented first: its intermediate local measurements reduced repeated
reads from about 0.676 to 0.371 seconds. Full standards compilation still occupied
about 0.196 seconds, justifying the second, bounded mechanism. Those exploratory
observations are retained separately from the final comparisons below.

Code and implementation evidence are the only changed concerns. Normative
standards, operational prompts/templates, public Engine schemas, supported
versions, dependency locks, Identity-v2, Git object verification and SQLite
settings remain unchanged. Git batching, selective compilation, test-runner
parallelism, persisted caches and shared cache services are outside this scope.

## Design and ownership

### Installed interface

`AgentToolFacade.load_interface` prepares the canonical installed schema and
interface once. The MCP server owns it for its code-installation lifetime and
passes it to each newly opened facade. Discovery is projected from the same
compiled contract used for invocation. Request decoding and result validation
still run on every call; this is preparation reuse, not validation removal.

The standalone facade remains an independent cold consumer. Embedders may supply
a prepared interface explicitly when they own its fixed implementation lifetime.
The returned catalog is independent data, so a caller cannot mutate subsequent
discovery results. Replacing installed code or the API schema requires restart;
ordinary accepted-standards publication does not change the installed API.

### Compiled snapshot material

`CompiledSnapshotCache` is a small Engine-owned mechanism. The MCP process owns
its lifetime and supplies it explicitly; the Engine retains no implicit global
cache. It is fixed to a repository root and purpose and uses an exact capture plus
the installed compiler function as the key. Capture equality includes the sorted
paths, bytes and source revision. A Python hash collision cannot conflate keys.
Public snapshot IDs and response provenance are reconstructed for each request.

`_compiled_snapshot` first performs the existing `SnapshotModule.load_content`.
That method still checks current lifecycle and verifies the complete durable
content. Only the successfully verified capture reaches compilation lookup. The
cache returns pure compiled input, never an earlier response or live access
result. Snapshot-bound attestations and exposure declarations remain historical
input; they do not acquire new authorization authority.

Equal already-verified material from separate stores may share pure compilation
inside the same trusted owner. Store-specific lifecycle, handles, integrity and
result envelopes are still observed in the current call. Missing, replaced,
quarantined, purged or corrupt storage cannot be answered from retained material.

The full compiler remains the only compiler. Misses compile frozen captured
bytes; failures are not retained. Stateful or closure-based compiler adapters
remain valid cold callers. Capture's live and frozen passes call the compiler
independently, compare closure/signatures and publish only afterward. Neither
pass consults this cache. Proposal construction independently compiles changed
candidates; this increment adds no cross-call proposal-projection cache.

### Bounds, concurrency and lifetime

The cache admits at most **two entries and 32 MiB of accounted retained data**.
A bounded LRU chooses entries; oversized or unaccountable valid material uses
ordinary verified computation. Both entry pressure and byte pressure are tested.

Accounting includes captured bytes, reachable Python containers, compiled models,
patterns and mapping tables. It counts shared objects once inside an entry and
conservatively counts inter-entry sharing separately. Path value caches are
materialized before measuring. Unknown mapping/native backing allocations and
closure state make an entry ineligible rather than pretending their size is known.
Imported implementation code and fixed-size cache bookkeeping are outside the
entry budget. It is not a total RSS or transient-compiler memory guarantee.

MCP retains serial dispatch. Each tool call opens and closes a real Engine/facade
and store. Independent MCP processes own separate fixed-purpose caches; this
change does not make a SQLite connection or one Engine concurrently callable.
The public result constructors and graph/source interfaces retain read-only
ownership; caller-visible data is constructed afresh. Stream EOF and stream
failure release the owner interface, catalog and cache. Closing a borrowing
Engine releases its store without clearing the server-owned cache.

Removing either mechanism restores a correct cold computation. Necessary state
is contained by its actual lifetime owner; neither mechanism is a durable
correctness dependency or a second authority for standards, identity or policy.

## Measured behavior

Final comparisons use the same executable, dependency set, host and fixed source
at `b81a5aae`, with no other test jobs running. Each implementation has three
serial sequences, each beginning with a new server. A prepared persisted snapshot
selects **436 files / 3,747,165 source bytes** and the same content ID on both sides:

`snapshot-content:sha256:48852a7cf384b41ea39182169465521e22aef3addc6f3d77cd39ccdb8c784ae5`

Fixture creation and initial snapshot capture are outside the operation timings.
These are local authoring-purpose observations, not an installed Codex benchmark
or a claim that the real application content has been qualified. Three samples
provide medians/ranges rather than p95/p99 service levels. Fresh processes do not
imply cold operating-system caches.

### Actual stdio process and request latency

| Observation | Baseline median | Candidate median | Interpretation |
| --- | ---: | ---: | --- |
| Process start through MCP initialization | 0.319 s | 0.584 s | +0.265 s: interface preparation now happens once at startup |
| First explicit-snapshot read after initialization | 0.617 s | 0.393 s | 1.57x faster; includes cold compilation/admission |
| Repeated read | 0.610 s | 0.172 s | 3.55x faster |
| Read another policy in the same snapshot | 0.615 s | 0.169 s | 3.63x faster |
| Another repeated read | 0.618 s | 0.175 s | 3.53x faster |
| Startup plus first read, summed per sequence | 0.938 s | 0.979 s | About 0.041 s slower; single-use startup is not the target gain |
| Startup plus all four reads, summed per sequence | 2.787 s | 1.496 s | 46.3% lower elapsed time / 1.86x throughput for this sequence |

Totals are formed per run before taking their median; they are not sums of
separately chosen medians. Raw subprocess outputs were asserted through the
actual newline-delimited MCP transport and both result encodings remain intact.

### In-process MCP dispatch attribution

| Observation | Baseline median | Candidate median |
| --- | ---: | ---: |
| Server construction and initialization | 0.006 s | 0.276 s |
| First read | 0.633 s | 0.391 s |
| Repeated read | 0.669 s | 0.178 s |
| Different policy | 0.615 s | 0.166 s |
| Full-detail read | 0.618 s | 0.180 s |
| Route using an explicit snapshot | 0.811 s | 0.367 s |

Across three five-call sequences, interface compilation falls **15 to 3** and
full standards compilation **15 to 3**. Complete durable content loading remains
**15 to 15**, with median spans of approximately **0.154 and 0.153 seconds**.
Thus the principal remaining warm-read cost is still the required content check.
Inclusive spans are not added to manufacture an overall speedup.

Every candidate sequence admits one entry, records four hits and one miss, and
retains about **6.47 MB** of accounted data (6,465,001 to 6,465,033 bytes). That is
well within the entry and byte bounds. End-of-sequence Linux RSS medians are about
61.2 MB before and 64.4 MB after. Those single-process observations include the
interpreter, installed interface, allocator retention and transient results; they
are not the cache-owned size or a portable upper bound.

The [comparison CSV](performance-process-reuse/comparison.csv), raw
[baseline](performance-process-reuse/final-baseline.json) and
[candidate](performance-process-reuse/final-candidate.json) dispatch observations,
and [baseline](performance-process-reuse/final-stdio-baseline.json) and
[candidate](performance-process-reuse/final-stdio-candidate.json) stdio observations
retain all sample ranges and count data.

## Correctness evidence and failure rules

The new regressions exercise actual stores and existing owned interfaces:

| Boundary | Evidence |
| --- | --- |
| Interface preparation versus validation | One preparation per server; malformed requests still reject; discovery/runtime use the same contract; restarted server detects changed schema |
| Every new request | Full durable load on each call, including cache hits; response mutations do not affect later output |
| Storage state | Warm reads reject quarantine, purge, missing/replaced stores and corrupted complete content before cache lookup |
| Purpose and repository | Trusted scope mismatch rejected before store open; application catalog remains restricted; existing publication scenario uses separate purpose caches |
| Current authority | Quarantine during review authorization prevents readiness; original live-evidence rejection also passes under warm recovery validation |
| Accepted main | Advancing main yields a new capture with two compiler passes; old snapshot remains readable after its working-tree source disappears |
| Cold process | Two actual fresh stdio servers reproduce the same exact historical result |
| Bounds and failures | Disabled retention, entry/byte eviction, oversized/unknown-size state, stateful compiler and failed compilation preserve cold-path behavior |
| Cleanup | EOF/write failure closes the owner; borrower close retains cache but closes store |
| Publication and recovery | Existing coordinated publication/provenance assertions pass with warmed purpose-isolated caches; unchanged audit/recovery assertions pass with a warmed first owner and a cold second owner/store |

The extra [warm recovery run](performance-process-reuse/warm-recovery.json) retains
all original assertions: actual review and candidate verification, rejection of
evidence changed after review, interrupted application, recovery, and readback
from an independent database. It observes ten first-owner cache hits. The second
owner starts cold, and both caches release their entries on completion. It is a
correctness observation, not a paired recovery performance claim.

## Test execution and qualification limits

The full serial Engine discovery run passed **199 tests**. Eleven supporting
package suites ran **438 tests**, with **one existing interpreter-dependent skip**.
Together those runs cover **637 distinct tests: 636 passed and one skipped**.

After that full run, accounting was tightened to exclude arbitrary Mapping
implementations with unknown backing allocations, and the existing bound test
added a byte-pressure case. All **21 new regression tests were then rerun and
passed** on the final code. The production source hashes of that final candidate
match this delivery; the distinction between the full run and final focused
rerun is retained in [verification](performance-process-reuse/verification.json)
and [source binding](performance-process-reuse/source-binding.json). No assertion
was removed or failure accepted as debt. The full-run duration is not a paired
suite-performance measurement and should not be compared with the user's host.

The structural checkpoint is run separately against the final source and again
after the delivery commit. Its expected population is the existing **73 suites /
121 checks**. Actual outcomes are in [structural evidence](performance-process-reuse/structural.json).
These checks establish structure and generated freshness, not functional or
semantic acceptance. Existing real publication checks remain active inside tests.

The environment is isolated Python **3.13.5**, outside the declared 3.11/3.12
range; local `rpds-py` **2026.5.1** differs from the locked **2026.6.3**. Baseline and
candidate use identical executables and dependencies. The dependency lock and
supported versions are unchanged. Changed code parses with the 3.11 grammar;
that is not execution on 3.11. See the [environment](performance-process-reuse/environment.json).

Official SDK/configured Codex qualification and independent implementation review
were not available here. Real raw stdio, native/facade tests and the narrower
existing authorization/publication fixtures are reported for their actual claims.
Run the supported locked environment and relevant installed-client qualification
before accepting this increment. The older increment's review does not transfer.

## Reproduction and delivery

Use one common fixture checkout at `b81a5aae` and separate baseline/candidate
implementation checkouts. The scripts create their own temporary Git fixture
with local accepted main at the fixture commit and preserve the source checkout.
Run each implementation serially with the same supported Python/environment:

```bash
python measure_mcp.py --source /path/to/implementation --fixture /path/to/baseline --output /path/to/dispatch.json --repeats 3
python measure_stdio.py --source /path/to/implementation --fixture /path/to/baseline --output /path/to/stdio.json --repeats 3
python validate_warm_recovery.py --source /path/to/disposable-candidate --output /path/to/recovery.json
```

The scripts are retained beside this report. Instrumentation counts the same
boundaries on each implementation. Its compiler wrapper is stateless, so it
preserves the actual retention admission rule. Raw qualification logs are included
in the ZIP outside the source replacement tree. The exact Git CLI commit/tree,
file hashes, patch and bundle are identified by the delivery manifest. Use one
application method, then restart the installed MCP server for the new code.
The user's accepted main, live store, archived proposals and configuration remain
outside the write set. No remote publication or normative-content migration is
part of this delivery.
