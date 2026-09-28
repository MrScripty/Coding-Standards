# Verified snapshot-capture handoff — implementation verification

> **Current disposition (2026-09-27): Accepted.** The exact-source locked Python 3.12 workflow passed, the independent external reviewer recommended this slice as satisfied, and the acceptance owner dispositioned its findings. The earlier local-only/pending status below is historical. See the [acceptance-owner decision](../../typed-routing-edits/reports/acceptance-dispositions.md).

**Status: Verifying.** Source implementation and local evidence are complete.
Supported locked-runtime CI for the exact diff and independent external material
review remain acceptance requirements. Baseline:
`6fa41c3105a6d1d4a49230ad367ae83d3afc472c`, tree
`8ec12dc319e4da76605b08cbcd602ae6b9c12389`. The Engine remains **interface 44**.

## Scope, standards and admission

The latest main revision was resolved through the connected GitHub repository
before source changes. Its Actions source archive was verified against SHA-256
`fa626806f85fb49e3216b747c1d40d146add2f369e5d795d4729b070efbdca0a` and the complete
checkout tree was checked. This is a patch to that actual revision, not a
reconstruction from an earlier implementation package. A separate baseline clone
and task-owned fixture stores preserve original-code comparisons.

The user authorized the capture handoff only. The executable Router received
explicit task facts, returned no unresolved conditions, and all 24 selected
standards were read. The plan records the composed-design ownership review,
write set, acceptance cases and remaining gates. Typed routing-edit work stays
deferred. Normative standards, public contracts, dependency locks, approvals,
accepted Git refs, host configuration, user stores and unrelated ZIPs are unchanged.

## Production design

Only two existing production files change: `engine.py` and `compiled_cache.py`.
The Engine binds the same actual compiler function before both independent capture
passes. It still records/compiles the live source, freezes it, compiles an independent
recorded replay, and compares requested paths and semantic signatures. A closure,
semantic or storage admission failure cannot offer this result to the cache.

After successful snapshot admission and normal result construction, the proved
second compilation is retained through the existing CompiledSnapshotCache owner.
Its mutable RecordingContentSource wrapper is replaced with the exact immutable
FrozenContentSource only when the compilation actually belongs to that replay.
The cache retains neither a Git reader nor the mutable recorder. Compiler adapters
which do not provide this exact source proof keep their ordinary cold behavior.

The new cache method `retain_verified` is the shared retention path for ordinary
cold compilation and this capture handoff. It uses the existing exact CapturedContent
key, compiler-function identity, two-entry/32 MiB defaults, byte accounting and LRU
policy. It adds no second cache, pin, increased limit, persistent proof or server
mode. Disabled, undersized or ineligible cases simply use normal reconstruction.

The normal snapshot observation path is unchanged: it loads captured material from
the store, checks its bytes and lifecycle, computes or safely reuses the identity,
and compares it with the current stored identity before compilation reuse. A seeded
compilation is not evidence of a current snapshot, permission, successful publication
or evidence validity. Store corruption, quarantine and expiry still reject before
an answer can be obtained from the cache.

## Measured work and retention

Original and candidate code ran separately against the same accepted baseline
source and deterministic test-owned snapshot identities. The profiler counts
original function code identities, avoiding mock wrappers that would change cache
eligibility. Structured results were compared exactly.

| First implicit-snapshot observation | Original | Candidate |
| --- | ---: | ---: |
| Route compiler calls | 3 | **2** |
| Read compiler calls | 3 | **2** |
| Content-identity computations, either operation | 2 | **2** |
| Durable content loads, either operation | 1 | **1** |
| Further compiler/identity work on an immediate repeat | 0 / 0 | **0 / 0** |

The two remaining compiler calls are the separate live and frozen proof passes.
There is no third reconstruction on a cache-eligible first route/read. Subsequent
explicit observations retain the existing warm behavior. Each output equals its
baseline counterpart, not merely another candidate-generated expected value.

The first handoff implementation exposed an important retention problem: the first
identity observation replaced an equal cache key with newly loaded bytes while the
retained compilation still held the original capture bytes. Accounted retained
material grew from about 7.58 to 12.08 million bytes in that experiment. The issue
was reproduced by an identity-key regression before repair.

The existing cache now preserves its already-retained exact key when extending an
identity proof. This shares the captured byte set without changing exact equality,
codec/compiler checks or eviction. Final route accounting was **7,583,246 original
versus 7,581,967 candidate bytes**; read accounting was **7,583,206 versus 7,581,943**.
Small accounting differences between separately compiled equivalent objects are
not process RSS or an additional memory-saving claim. The relevant result is that
the new handoff does not retain a second full equal byte set.

These are verified operation counts and existing cache accounting—not end-to-end
latency, production throughput, allocation-wide, model-token or billing claims.

## Deciding acceptance tests

Fourteen new methods (13 handoff/cache tests and one real transport test) cover:

- Successful admission before retention; both proof passes; exact frozen content,
  independent semantic signature and release of live readers/recorders.
- Closure/semantic mismatch and admission failure without seeding; retry success.
- Unchanged durable loads/identity checks, wrong stored identity, altered SQL bytes
  with updated per-file digests, quarantine and expiry rejection before cache reuse.
- Disabled/tiny/one-entry budgets, eviction, owner close, stateless/foreign-source
  compilers and compiler changes during admission, with exact cold-result equality.
- Preservation of the retained capture key while adding the first identity proof.
- Real MCP stdio in eager and on-demand delivery: two first-process proof compiles,
  one replacement-process cold reconstruction, equal structured/text results,
  unchanged accepted main and no publication.

These cases complement existing immutable-identity, cache collision, evidence,
working-set, state-reuse, storage and publication/recovery tests; they do not
replace them. No new test framework or production profiling mechanism was added.

| Check | Result |
| --- | --- |
| Complete Engine selection, four file-disjoint shards | **569 passed; no failures, errors or skips** |
| Eleven complete supporting-package suites | **568 passed; 2 existing environment-dependent skips** |
| New handoff/cache/stdio regression methods | **14 passed**, included in the Engine total |
| Complete registered structural checkpoint | **121 checks across 73 suites passed** |
| Generated contract freshness and source preservation | Passed; canonical/generated artifacts and all eight catalogs unchanged |
| Baseline retained workflow via four replacement MCP processes | Exact status, repeated review, readback and accepted main preserved |

The final complete Engine selection ran after all production and test-source
repairs, including the identity-key sharing correction. Each current test ID occurs
in exactly one shard and has one passing entry in that run. Original partial and
failed exploratory runs are retained separately, not combined into a claimed
passing selection. The final report and plan-status edits are maintenance-only.
A final focused rerun, regenerated suite-input manifest and static/structural checks
cover the delivered records; their separate logs do not add to unique-test totals.

The supporting package counts are Identity 16, Applicability 12, Graph 41, Standards
Graph 2, Snapshots 40, Repository Git 32 (one skip), Metadata 43, Policy Impact 10,
Contracts 81 (one skip), Analysis 125, and Verifier 168. The skips are the existing
supported-interpreter check and a permission check unsuitable under the container's
root user. Neither is counted as a pass. All exact test selections, pass IDs,
commands, exit codes and scope qualifications are retained in delivery evidence.


## Evidence history and limits

The new first-read regression failed against the original code with three compiler
calls, then passed with two after implementation. An early candidate run exposed a
missing dataclass import, which was fixed. One test expected CapturedContent's
component ordering where the source owner defines string ordering; the test oracle
was corrected without changing path or identity semantics. The first stdio launcher
omitted required streams and failed before protocol work; its fixture was corrected.
Those logs are retained separately from final passes.

The identity-key allocation regression identified the concrete memory cost above.
The task-owned initial broad verification was explicitly stopped to repair it, and
the complete Engine selection was restarted on the corrected source. Its partial
logs do not contribute to final acceptance counts. No production validator or
lifecycle rule was weakened to make any test pass.

## Contract and stored-state preservation

All **326 canonical schema definitions**, **40 operation declarations**, generated
models, interface 44, request/state versions and dependency pins are unchanged.
All eight purpose/scope/output-delivery tool arrays are byte-identical to the base.
Ninety-one protected normative/contract/CI/lock files are independently verified
unchanged. Whole-tree patch reconstruction additionally protects other baseline
paths. No arguments, new tool, catalog-mode or data-migration step is introduced.

An original-code process created a real proposal and readiness in a separate store.
Four fresh candidate on-demand MCP processes independently reopened proposal status,
readiness status, repeated review and exact proposal content. StructuredContent and
its matching text JSON equal the original results; accepted main is unchanged.
This is actual transport/retained-data evidence, not a live model session or a claim
about the user's private production database.

## Environment, integration and remaining acceptance

Local execution uses CPython 3.13.5, Linux, jsonschema 4.26.0 and rpds-py 2026.5.1.
The repository's supported lock remains CPython 3.11/3.12 with rpds-py 2026.6.3.
An attempt to provision 3.12 failed at package-host DNS; the lock was not relaxed.
The observed baseline GitHub workflow is not candidate CI. Exact-diff supported
CI and independent external review are still required before marking Accepted.
Implementation self-review and independent test oracles are not an external review.

Apply the complete base-pinned patch, with new tests and generated verification
inputs tracked together. Preserve unrelated source and ZIP changes. Restart a
long-running MCP process to load new Python code after settling in-flight
publication/recovery with its owner; registration arguments and catalogs do not
change. Preserve every existing store, snapshot and workflow handle. No remote
push, source commit, user configuration edit, model run or standards publication
was performed in this task.

C1 is Implemented and the plan is Verifying; its next slice is exact-diff integration
with supported-runtime CI and independent review. The typed edit-family pilot is
not part of this implementation. DELIVERY contains the exact patch, base/new hashes,
file modes, read-only preflight, logs and fresh-baseline reconstruction evidence.
