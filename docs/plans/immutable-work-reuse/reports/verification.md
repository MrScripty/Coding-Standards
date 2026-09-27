# Immutable-work reuse: implementation verification

**Status: Verifying; acceptance partial.** Source implementation and local checks are
complete. Supported locked-runtime CI and independent material review remain pending.
Base: `e384fffdcf73e43b2f784619f4812e135f5f3393`; Engine interface **44**, unchanged.
This is the audit's F01/F08 implementation, not the storage-maintenance or API stages.

## Implemented result and ownership

A process-owned snapshot-cache entry now contains the exact captured material and its
optional identity and compilation products. The existing two-entry/32 MiB accounted-data
budget, LRU, repository/purpose admission and close lifecycle govern both products. There
is no separate identity registry, global memo or additional cache budget. Replacing an
entry correctly subtracts its earlier accounting; oversized and disabled retention still
compute normally. Calculator/compiler identity is checked separately from captured-value
equality. Closure functions, bound methods and callable objects calculate cold. Eligible
plain functions must still satisfy the trusted pure-codec/compiler contract; Python function
shape alone does not establish purity of arbitrary code. Only successful pure computations
are retained. A successful identity calculation may survive a separate failed
compilation, but compilation failures themselves are never cached.

The Snapshot package owns the identity codec and the comparison with the currently loaded
stored content ID. Its small `ContentIdentityReuse` protocol accepts the complete capture
and that codec; it does not depend on Engine internals. Every access still performs the
ordinary store read, per-file byte/digest checks and snapshot lifecycle maintenance. The
returned calculation, even on a hit, is compared with the newly loaded stored identity.
No identity-v2 encoding, hash algorithm, source label, timestamp or expected-ID shortcut
was substituted. Cold and standalone callers retain the original calculation path.

Authoring owns the canonical aggregate-to-revision decoder. `RevisionDecoding` holds at
most one exact aggregate and its validated immutable revision. Record kind, identity,
payload, snapshot memberships and children all participate in equality. The existing
`ProposalMaterials` owner composes and clears that slot with its base/projection material.
Each revision access still reloads its aggregate and current root and validates membership;
current heads, lifecycle, authorizations, evidence and publication admission are not memoized.
The former summary-only decode in `current_revision` is removed while both root observations
and their validation remain. Analysis binding/evaluation and decision composition carry
this operation-local reuse explicitly. Nested public operations have independent owners.

The measured Analysis-context `workflow_status` decodes its one exact revision once per
operation rather than five times. A subsequent operation decodes again. Readiness,
selected-application and recovery readers retain their existing independent cold checks;
this is not a claim that every possible status or multi-revision operation decodes once.
A read-only scope probe recorded three decodes for a readiness-context observation; no
extra publication/recovery rewrite was introduced just to meet a count target.

## Standards and source scope

The executable Router selected 23 applicable modules with no unresolved facts. Exact
readback is retained in delivery evidence. The admitted plan covers immutable identity
proofs, operation-local material, ownership, corruption, lifecycle, performance and
verification. Source changes remain in Snapshot, the existing Engine cache/operation
owners, their direct test consumers and documentation. Public schemas, all operation
declarations, dependency locks, policy text, application approvals, production stores,
remote refs and unrelated user files remain untouched.

F15 interface-table preparation, F02/F03 purge/integrity work, F09 working-set policy,
F10/F14 domain refactors, F16 capture seeding and routing-API changes are deliberately
outside this implementation. No task timeout, background service or automatic retry was
introduced. Runtime and test source were held fixed during the complete selection; the
single test-adapter correction and touched-source formatting were followed by focused
reverification before final measurements.

## Final measurements

Workload: one baseline-produced snapshot containing **480 files /
4,465,881 captured bytes**, a Core read, a Core+Router batch, and the status
of one complete reference proposal. Baseline and candidate execute against the exact same
isolated repository, snapshot, Analysis and store. The candidate never publishes its main.

The boundary is a complete in-process MCP `tools/call` dispatch, including actual per-call
SQLite admission, durable reads, domain evaluation and result construction. It excludes
client/network/model time and outer OS-process startup. Actual replacement stdio processes
are used separately for semantic and retained-state checks. No live Codex or paid model
turn is used. This is a local server-workload comparison, not a billing or p95/p99 claim.

### Warm calls

Two counterbalanced source orders (baseline→candidate, candidate→baseline) supply 18
unprofiled samples per source and operation, after each operation's warm-up. Functional
campaigns and other implementation tests had finished before these final measurements.
Profiling calls are separate from the timing samples. Complete structured response hashes
match across every source/run comparison; raw samples are retained.

| Operation | Baseline median | Candidate median | Baseline range | Candidate range | Speedup |
| --- | ---: | ---: | ---: | ---: | ---: |
| `read` | 203.11 ms | 35.43 ms | 198.71–211.74 ms | 33.99–37.33 ms | 5.73× |
| `read_many` | 210.67 ms | 42.63 ms | 206.83–228.44 ms | 41.10–44.91 ms | 4.94× |
| `workflow_status` | 312.59 ms | 70.01 ms | 305.99–443.41 ms | 67.30–84.92 ms | 4.47× |

Both requested mechanisms contribute to the combined status improvement; its speedup is
not attributed to revision decoding alone. The earlier audit's single-mechanism prototypes
are not substituted for these final implementation observations.

### Cold cache/owner observations

Five alternating baseline/candidate pairs use replacement Python processes and fresh MCP
server/cache owners. The table measures each owner's first explicit-snapshot dispatch.
Interpreter import time is excluded; server construction/initialization time is recorded
separately in the raw data. Cold here does not claim a cold operating-system page cache.

| Operation | Baseline median | Candidate median | Baseline range | Candidate range | Speedup |
| --- | ---: | ---: | ---: | ---: | ---: |
| `read` | 404.83 ms | 403.12 ms | 397.03–446.04 ms | 400.35–430.47 ms | 1.00× |
| `workflow_status` | 886.05 ms | 822.64 ms | 868.82–952.37 ms | 818.96–869.82 ms | 1.08× |

Cold reads remain approximately unchanged in this sample. The optimization primarily
benefits repeated calls rather than avoiding the first required identity proof or compile.

### Resource tradeoff

The defaults remain two retained entries and 32 MiB of accounted data, shared with draft
projections. In the final warm sample, the candidate accounts for
**7,566,478 bytes** after the read and
**15,811,745 bytes** after
status, versus 7,566,185 and
15,811,440 in the baseline.
The identity bookkeeping adds a small amount of retained data; it does not create another
retention allowance. Active operation material, bounded LRU bookkeeping and interpreter
allocations remain outside this accounting; it is not a process-RSS measurement. Cache
close clears both products and their accounted bytes; operation exit clears decoded records
on both success and failure.

## Test and preservation evidence

| Check | Observed result |
| --- | --- |
| Complete Engine selection | 545 methods: 544 passed; one stale test-adapter error |
| Final affected Engine rerun | **67 passed**, including the corrected adapter |
| Reconciled current Engine coverage | **545 distinct current test IDs observed passing** |
| New regression methods | **22**, included above; an additional child-membership subcase is included |
| Contracts/compiler package | **80 passed; one supported-environment check skipped** |
| Other ten supporting packages | **468 passed; one root-dependent permission check skipped** |
| Skipped permission case rerun as unprivileged `nobody` | **Passed** |
| Generated-contract freshness | Passed |
| Registered structural checkpoint during final runtime refresh | **121 checks across 73 suites passed** |
| All eight purpose/scope/output-delivery catalogs | Byte-identical to baseline |
| Canonical schemas, interface, examples, generated models and dependency lock | Byte-identical to baseline |
| Real baseline/candidate replacement processes | Equal reads, Analysis/readiness status, repeated review and exact readback |
| Changed evidence after a warm read | Exact `ANALYSIS.EVIDENCE_DIGEST_MISMATCH` rejection; restoration recovers identical readiness |

The complete Engine campaign used four file-disjoint selections (139, 125, 121 and 160
methods). The failing case injected a competing revision using a test adapter whose
signature did not accept the new internal `decoding` argument. Its signature now forwards
that argument into the real owner; the exact `AUTHORING.REVISION_STALE` assertion and
subsequent stale-context observation remain and pass. Production guards were not relaxed.
This is complete-selection coverage plus a successful final rerun, **not** a claim of one
uninterrupted all-green full-suite run. Initial logs and the reconciled ID list are retained.

The new regressions cover exact separately loaded captures, Python hash collisions,
incorrect stored IDs, rewritten durable bytes with recomputed per-file digests, quarantine
and purge, codec/compiler changes, disabled/oversized/evicted retention, failed computation,
close, actual record/root reads, changed heads, changed record payload/membership/children,
immutable semantic maps, operation cleanup, and real warm/cold stdio equivalence. Existing
reuse, authoring and integration tests additionally cover store replacement, fresh
permissions, nested reentry, atomic decisions, publication and recovery.

A successful identity proof is now a legitimate cache entry even if compilation fails.
The old compilation-failure assertion was updated to distinguish that independent product
from a cached failure; repeated compilation is still required and asserted.

The retained-state instrument initially expected a bare rejection from focused review,
which correctly returns a workflow envelope. Its assertion was corrected to inspect the
nested exact diagnostic; no Engine code was changed for it. A final-check command also
initially passed `durable=False` to the facade instead of the owning Engine constructor;
it was corrected to use an explicitly disposable Engine and existing authorizer. These
instrument/invocation failures are retained separately and do not count as test passes.

## Remaining acceptance and installation

Local environment: CPython **3.13.5**, Linux x86-64, jsonschema **4.26.0**, rpds-py
**2026.5.1**, four CPU-equivalents of container quota and 4 GiB memory limit. Other
process/host load is not controlled. The supported locked environment is Python 3.11/3.12
with the unchanged repository lock. Run the existing locked CI on the integrated diff and
obtain independent material review before marking the plan Accepted. The local dependency,
contract, system and performance evidence does not replace those separate claims.

No public interface edition or catalog change is necessary; **interface 44 remains**.
Apply all delivered source, tests and generated verification inputs together. Restart the
MCP process to use the new implementation, reconnect normally and preserve its current
native-only launch arguments and output-delivery choice. Preserve every store, snapshot,
proposal, Analysis, readiness and recovery handle. Current evidence/lifecycle can still
legitimately invalidate an action; the cache does not preserve revoked authority.

The ZIP supplies complete repository-relative files, a base-pinned patch, a read-only
per-file baseline checker, source hashes/modes and verification instruments/logs. The final
post-report generated/structural checks and clean-base patch reconstruction are recorded
in `DELIVERY/evidence/final-artifact-checks.json` and `DELIVERY/reconstruction.json`.
The package performs no automatic commit, push, reset, production publication or config edit.
