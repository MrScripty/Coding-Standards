# Execution ledger

> **Current disposition (2026-09-27): Accepted.** Acceptance owner reconciled the exact-source CI, preserved external verdict and plan-specific evidence. The slice is Accepted; implementation-stage pending notes below remain historical. See the [acceptance-owner decision](../typed-routing-edits/reports/acceptance-dispositions.md).

- Inspected latest upstream `6fa41c31` and verified its Actions source ZIP SHA-256
  and complete tree. Created a clean owned branch; no remote writes performed.
- Routed the task with explicit facts; all 24 selected standards were read. The
  approved design is the smallest internal handoff through existing owners, with
  capture proofs and normal durable validation unchanged.
- C1 is active. The regression first observes the original compiled-function count
  with a profiler so cache eligibility is not changed by test instrumentation.

- The initial regression reproduced three compiler calls. The first implementation
  run exposed a missing dataclass helper import, fixed immediately; the regression
  then passed with two proof calls and normal durable load/identity checks intact.
- Twelve focused cases exposed one oracle ordering assumption: FrozenContentSource
  orders path strings while CapturedContent orders path components. The expected
  value now uses the source owner's defined string ordering; no production path or
  identity semantics were changed to satisfy the test. Initial logs remain distinct
  from subsequent accepted evidence.

- The first actual-stdio fixture passed the server without its required streams;
  its launcher now passes stdin/stdout explicitly. This fixture error occurred
  before any protocol call and is not evidence of a product failure or success.
  Candidate runtime behavior remains unchanged; repeat the transport checks.
- The supported Python 3.12 provisioning attempt failed at package-host DNS.
  Keep the existing dependency lock and qualify the exact patch on CI separately.

- Independent original/candidate measurement confirmed the compile reduction but
  exposed a material memory cost: first identity learning replaced an equal cache
  key with newly loaded bytes while the retained compilation still owned the old
  bytes (about 7.58 to 12.08 million accounted bytes in this fixture). A focused
  identity-key regression failed before correction. The existing cache now keeps
  its exact retained key while adding the identity proof. No new owner, state or
  limit is added. Task-owned verification processes were explicitly stopped; their
  partial run is not acceptance evidence. The final source selection is rerun.

- The complete restarted Engine selection passed all 569 distinct methods in four
  file-disjoint shards, including all 14 new handoff/cache/stdio methods. Eleven
  supporting suites passed 568 methods with two pre-existing environment-dependent
  skips. Complete structure passed 121 checks / 73 suites. No old failed or stopped
  run is relabeled as final evidence.
- Final separate-process measurements preserve identical structured outputs while
  reducing first route/read compilation from three to two. Both identity computations
  and the durable load remain. Identity-key repair restores retained accounting to
  the original approximately 7.58 million bytes, without changing the cache limits.
- Four replacement MCP processes reopened actual baseline proposal/readiness status,
  repeated review and content readback unchanged, without migration or publication.
  All canonical schemas/operation declarations and eight catalogs are unchanged.
- C1 is implemented and the plan is Verifying. C2 is the only next slice: exact-diff
  supported-runtime CI and independent external review. The private user checkout,
  stores/configuration, remote refs and unrelated ZIPs were not changed.
