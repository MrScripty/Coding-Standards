# Execution ledger

## 2026-09-27 — admitted implementation

User authorized the next step of the current refinement review. Bound to
`docs/plans/fact-ownership-and-working-set/plan.md`, operation `start`; Active R1.
Verified upstream head 87873de5 and source artifact SHA-256
ce045eb23445d0407caa995692871ec1df421b7aaa5014106d28741428035229. No remote source
or operator files were changed. The clean isolated checkout supplies exact base
hashes for the eventual patch.

Read Core and the executable Router; all supplied task categories were explicit
and no unanswered condition remained. Baseline material capture initially used
vars() on a slotted dataclass in the task-local instrument; it failed before source
changes. Corrected the instrument to dataclasses.asdict; this was not a product
failure. Original instrument output is retained separately.


## R1/R2 implementation and early regressions

The new canonical-owner tests first failed because RouterProjection had no record
method. The focused-transition regression failed against the original code with
one base compilation on the next status read. Both behaviors were reproduced before
production edits. Moved the exact projection into RouterProjection and coordinated
all five Engine consumers. The cache now records actual use of its exact retained
base after successful projection construction, before retaining the result; no new
capacity, store, registry or authority check was introduced.

Initial new tests exposed three test-assumption errors: Router reads require the
explicit include_routing option; focused and native revision operations legitimately
return different context stages, so each must be compared against its own cold
observation; and focused NO_EFFECT rejection is carried by workflow-result.outcome.
Corrected those tests using the existing public contracts. The cache's reported
transition miss is fixed, and capacity-pressure outcome comparison already passed.
These early logs are retained, not counted as final all-green evidence.

## Local verification outcome

Both source refinements are complete. The unchanged post-correction source passed
all 555 distinct Engine methods in four file-disjoint shards. Eleven supporting
packages ran 570 tests: 568 passed, two existing environmental skips. All 11 added
methods are included in those totals. Structural and generated-contract checks
passed. The final maintenance records do not change tested Python bytes.

The same-seed baseline/candidate comparison eliminated one base compile and one
content-ID calculation from the next focused status call, with no change to its
structured result or default limits. Native-path behavior is preserved. All 83
material records/bindings, eight catalogs and old proposal/readiness observations
were independently checked unchanged; no migration or publication occurred.

The baseline measurement clone was initially empty because a redundant branch
creation failed after --no-checkout; the task-owned clone was explicitly checked
out at the verified base before rerunning. This was an instrument setup error,
not product evidence. No code guard was weakened for any test/instrument repair.

The source remains on the original commit with only the scoped staged changes.
No source commit or remote write is claimed. Plan status is Verifying with next
slice A: unchanged supported-lock CI and independent integration review. Existing
snapshot-capture and typed-edit recommendations remain explicitly deferred.
