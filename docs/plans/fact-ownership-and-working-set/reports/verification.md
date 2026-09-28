# Canonical fact ownership and focused working-set verification

> **Current disposition (2026-09-27): Accepted.** The exact-source locked Python 3.12 workflow passed, the independent external reviewer recommended this slice as satisfied, and the acceptance owner dispositioned its findings. The earlier local-only/pending status below is historical. See the [acceptance-owner decision](../../typed-routing-edits/reports/acceptance-dispositions.md).

**Status: Verifying.** Both source refinements and local acceptance checks are
complete. Exact-diff supported-runtime CI and independent external review remain
required for Accepted status. Base:
`87873de5e1405590209dad389f7010a6b61f0bbe`, source tree
`be94d23e7cdcd6383f588ab8d332146d587debcf`. The public Engine stays at **interface 44**.

## Scope, standards and admission

The user authorized the review's next targeted refinement. R1 moves the canonical
routing-fact projection to its existing domain owner; R2 fixes the demonstrated
focused revision cache transition. Snapshot-capture result handoff and typed routing
edit families remain explicitly deferred. No public operation, output/input mode,
store, dependency, authorization rule, or workflow state is added or removed.

Current upstream head was checked before implementation. Its retained source ZIP
was verified against SHA-256
`ce045eb23445d0407caa995692871ec1df421b7aaa5014106d28741428035229` and checked out in a
clean owned workspace. The executable Router was run with explicit task facts,
returned no unanswered conditions, and all 24 selected documents were read. The plan
records the eight-part composed-design review, owners, scope and acceptance gates.
The operator's repository, configuration, stores and unrelated ZIPs were not edited.

## R1: canonical routing facts have their domain owner

`RouterProjection.fact_definitions()` now owns the existing ordered eight-field
representation. It preserves `id`, semantic revision, type, nullable, values,
aliases, meaning and prompt in the same insertion order, including empty values
and aliases. This is not replaced with the wider `FactContract.as_contract()`
serialization. Returned dictionaries/lists are independent of the immutable domain
projection and may be safely used by presentation code.

Supporting-material composition imports the public RouterProjection owner and no
longer imports agent navigation. Agent facts, application facts/questions, full
routing explanations and routing-enriched reads consume the same domain method.
The former navigation-owned projection is deleted. No new module, registry,
serializer framework or canonical identity format is introduced.

Independent tests use literal field expectations and raw canonical TOML rather
than deriving every expected result from the method under test. They cover empty
collections, canonical normalization, tuple and field order, aliases and independent
return values. In a controlled public-navigation change, display order/prompt/aliases
change without changing material bindings or the compiled semantic signature. A
real source fact-contract change still changes the router binding without altering
unrelated materials. The old navigation dependency is absent.

A separate original-code process captured exact baseline fact records and all **83**
content materials. Candidate loading of the same captured source produced identical
records and materials, including every binding. This is stronger than checking only
a freshly calculated expected digest within the candidate implementation.

## R2: successful projection construction keeps the useful bounded working set

The existing cache records actual use of the exact retained compiled base after a
successful projection construction and before retaining its result. This covers an
operation-local borrowed base that skipped another cache lookup. It adjusts the
existing LRU order; it neither inserts an absent base nor pins an entry. The normal
working set is the accepted base and useful successor, rather than a predecessor
accidentally taking priority over the base it depends on.

The default remains **two entries and 32 MiB**. Existing exact capture/program keys,
compiler identity, counted resident-size policy, eviction, and disabled/oversized
behavior remain unchanged. Cached material is still computation, not proof that a
prospective revision was admitted, current, reviewed or published. Root/content/
lifecycle/evidence checks remain with their existing owners and historical revisions
remain readable after computational eviction.

The new tests exercise a real seeded proposal with focused and lower-level native
revision paths. They compare each path with its own cold observation rather than
confusing their intentionally different context stages. Counts use profiler code
identity on the original methods, not wrappers that would change cache eligibility.
Tests also cover repeats, historical reads/stale status, one-entry/zero-entry/tiny
budgets, exact cold-result equivalence, rejected no-effect revisions, unchanged main
and release of retained entries on owner close.

Existing full-suite cases retain fresh authorization/evidence on hits, corrupt
base/revision rejection, hash collisions, codec/compiler changes, quarantine/purge,
store replacement, unsuccessful replay, publication recovery, and both capture
proof passes. This change does not admit snapshot-capture handoff or collapse the
independent review/application replay boundary.

## Measured operation-count effect

The performance instrument copied one baseline-produced store for each scenario,
kept the same 32 MiB budget, and ran the original and new implementations separately.
It checked exact structured status equality and preserved main. The table concerns
the **first status immediately after successor construction**, not every workflow
operation and not an end-to-end latency benchmark.

| Path / retained-entry limit | Original base compiles / content-ID computations | Candidate | Original accounted bytes | Candidate accounted bytes |
| --- | ---: | ---: | ---: | ---: |
| Focused `revise`, default 2 | 1 / 1 | **0 / 0** | 16,524,186 | 15,843,645 |
| Native `revise_proposal`, default 2 | 0 / 0 | **0 / 0** | 15,844,049 | 15,844,029 |
| Focused `revise`, diagnostic 3 | 0 / 0 | 0 / 0 | 24,104,643 | 24,104,647 |
| Native `revise_proposal`, diagnostic 3 | 0 / 0 | 0 / 0 | 24,105,251 | 24,105,223 |

Here, native names the lower-level `revise_proposal` operation, not an alternate
MCP input presentation mode. Default focused retention changes from
predecessor+successor to snapshot+successor.
The small accounting differences between separately constructed equivalent objects
are not process RSS. All compared domain results are identical, subsequent repeated
status calls are warm, and the larger diagnostic capacity is not a new default.
A separate actual MCP dispatch probe, with the normal per-call facade/store opens,
also retains two entries after focused revise and performs zero base compile and
content-ID computations on the next status. It verifies equal repeated results and
unchanged main. That probe is JSON-RPC dispatch, not an additional stdio or model
qualification claim.

No latency, allocation-wide, billed-token or production-database speedup is inferred
from these call counts or from concurrently executed local tests.

## Verification results

| Check | Result |
| --- | --- |
| Complete Engine selection, four file-disjoint shards | **555 passed; no failures/errors/skips** |
| Eleven complete supporting packages | **568 passed; 2 skips (570 executions)** |
| New focused regression methods | **11 passed**, included in the above totals; repeated in the final post-record check |
| Structural verifier | **121 checks across 73 suites passed** |
| Generated contract freshness | Passed; canonical/generated public artifacts unchanged |
| Exact current/baseline catalog comparison | All eight purpose/scope/output-delivery combinations byte-identical |
| Original stored proposal/readiness via four replacement MCP processes | Status, review and readback unchanged |

The complete Engine run used the stable production and test-source version after
its focused test corrections. Each current test ID appears in exactly one shard;
selection, success IDs, commands and final result counts are retained. Final report
and ledger edits are maintenance-only. The delivery's final static/structural
checks cover those records and the regenerated input manifest. Repeated targeted
executions are not added to unique-test totals.

The supporting packages are Analysis 125, Contracts 81 (one skip), Identity 16,
Applicability 12, Metadata 43, Policy Impact 10, Graph 41, Standards Graph 2,
Snapshots 40, Repository Git 32 (one skip), and Verifier 168. The skips are the
existing supported-interpreter environment check and a permission test unsuitable
under the container's root user. Neither is counted as a pass.

The baseline owner tests failed before implementation because the domain method did
not exist; the baseline focused working-set test independently reproduced the extra
compile. Early added tests then needed three consumer corrections: routing-enriched
reads require `include_routing`, native/focused revision contexts have different
stages, and focused NO_EFFECT is a nested workflow outcome. These were corrected
against existing contracts, without production workarounds. Original logs remain
separate from final acceptance evidence.

Two task-only instrument setup errors were also corrected: a slotted material
requires dataclass extraction rather than vars(), and an empty no-checkout clone
needed its actual tree checked out before import. These are not reported as product
failures. The evidence inventory identifies all such diagnostic runs.

## Contract and retained-state preservation

All **326** schema definitions and **40** operation declarations remain unchanged,
as do generated Python models, interface 44, request/state versions, handles,
readiness/recovery representations and dependency pins. Eight complete tool arrays
match baseline bytes in both purposes, focused/advanced scope and eager/on-demand
delivery. Ninety-one protected normative/contract/CI/lock files were independently
compared unchanged; complete-tree patch reconstruction protects all other baseline
paths as well.

An untouched baseline implementation created a real proposal and readiness in a
separate fixture store. Four fresh candidate native/on-demand stdio processes read
proposal status, readiness status, repeated review and exact proposal content.
StructuredContent and its text JSON copy equal the baseline results; main is unchanged.
No store migration, reset or publication occurred. This is actual transport and
stored-state evidence, not a live model session or a claim about a user's private
production store.

## Environment, limitations and integration

Local checks used CPython 3.13.5, Linux, jsonschema 4.26.0 and rpds-py 2026.5.1.
The unchanged supported lock requires Python 3.11/3.12 and rpds-py 2026.6.3. An attempt
to obtain Python 3.12 failed because external DNS was unavailable; the lock was not
relaxed. Run the exact diff through supported CI before acceptance. Implementation
self-review and independent test oracles do not substitute for the required external
material review. No actual Codex/model turn was run; this internal refinement does
not change agent contracts or demand a new host configuration.

Apply the entire base-pinned delivery with additions, changed source and generated
suite inputs coordinated. Preserve unrelated work and all existing workflow stores.
Restart any long-running MCP processes to load changed Python code; there are no
new flags, catalog edition changes or data-migration steps. No remote push, source
publication or external configuration write was performed here.

The plan is Verifying, R1/R2 implemented, with supported-runtime/integration review
as the remaining acceptance slice. Snapshot-capture handoff and typed routing-edit
work remain separate deferred recommendations, not hidden unfinished parts of this
implementation. Exact fresh-base reconstruction, file hashes, modes and ZIP integrity
are recorded in DELIVERY/reconstruction.json and the delivery manifest.
