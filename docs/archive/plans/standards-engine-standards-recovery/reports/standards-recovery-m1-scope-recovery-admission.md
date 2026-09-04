# Standards Recovery Milestone 1 Scope-Recovery Admission

## Reviewed Boundary

- Result: `Approved for Milestone 1 scope-recovery admission`.
- Reviewed candidate commit:
  `7a571ed26a132056368ef465d6041910c5a6ed48`.
- Reviewed candidate tree:
  `b1bd7994e9ab3ec8298b57755a285cdf2a72e9f6`.
- Admitted Milestone 1 start boundary: commit
  `e96da5eb3cccc22fb5c2293af65800cc69006ebf`, tree
  `b3d058001d9d61608bf518033bfe3e120bf8aac4`.
- Review axes: repository Standards and the exact one-path M1
  protected-consumer scope-recovery specification in SESR-025.

The reviewed worktree was clean. This report is the only repository change
authorized by the independent-review operation.

## Standards Review

No findings.

Independent review confirmed:

- the replan records the trigger, replaces the active mutation-boundary
  decision, and explicitly marks the former classification `Superseded`;
- the plan and Milestone 1 remain `Blocked` before any protected-consumer
  mutation;
- the proposed transfer names exactly one focused test and no runtime
  implementation path;
- `routing.boundaries` advances to semantic revision 2 with its expanded value
  domain; and
- the admission reuses the established exact-candidate, reviewer-report,
  mechanical-transition, and exact-head `start` lifecycle.

Standards total: zero findings.

## Specification Review

No findings.

Independent review confirmed:

- `tools/standards_analysis/tests/test_routing.py` is the sole protected
  consumer requiring source modification;
- the repair removes both incidental global cardinality assertions rather than
  replacing 38 with 39;
- the focused test will assert the stable boundary fact ID, semantic revision,
  enum member, rule ID, target, referenced fact, and compiled `contains`
  expression;
- successful projection loading plus the existing target-drift mutation test
  retain global Router target-closure evidence;
- registered M1 fixtures, not the focused loader test, own positive, absent,
  unresolved, IPC, Language Binding, and required-module behavior; and
- stale pre-change coverage after canonical-corpus mutation remains expected
  intermediate unavailability until Milestone 2 and does not authorize another
  test transfer.

Specification total: zero findings.

## Closure Evidence

The proposed mutation boundary transfers exactly
`tools/standards_analysis/tests/test_routing.py` from `R` to `W`. The path was
already an exact member of `E`, so `S`, `E`, and `W union R` remain unchanged;
`W intersect R` remains empty after the transfer. Every other admitted write,
suite-derived, exact non-registry, protected-consumer, and generated-inventory
rule remains unchanged.

The consumer's final disposition is `updated`: the targeted assertion change
is required to preserve the stable Router fact/rule contract without retaining
an incidental catalog-count oracle.

## Verification

Independent review confirmed:

- `HEAD` and the repository tree matched the reviewed identities;
- the worktree was clean;
- all 18 metadata and policy-unit tests passed;
- 81 of 82 Standards Analysis tests passed;
- the sole failure was the admitted protected assertion
  `AssertionError: 39 != 38`;
- generated freshness and dependency-graph checks passed;
- plan structure and lifecycle fixtures passed;
- the `metadata-fixtures` and `s1-routing` suites passed; and
- `git diff --check` passed.

The expected focused failure is the exact output this admission authorizes M1
to repair after transition and `start`. It is not a green acceptance claim.

## Authorized Admission Transition

This approval authorizes one mechanical transition commit after the commit
that contains this report. The transition commit must have the report commit as
its direct parent and may change only:

- `docs/archive/plans/standards-engine-standards-recovery/plan.md`;
- `docs/archive/plans/standards-engine-standards-recovery/execution-ledger.md`; and
- `docs/archive/plans/standards-engine-standards-recovery/issues.md`.

The transition may perform only these changes:

1. Record the reviewed candidate commit/tree above.
2. Record the exact commit/tree containing this admission report.
3. Set the plan and Milestone 1 to `Planned`.
4. Set the current phase to M1 scope recovery ready for `start`.
5. Name M1 scope-recovery `start` as the sole next operation.
6. Require `start` to capture the resulting transition commit/tree before
   changing to `Active`.
7. Update SESR-009 and SESR-025 and append ledger evidence only to reflect this
   admission and the still-pending `start` transition.

The transition must not change normative policy, Router authority, the focused
test, scope, tasks, evidence, any other closure member, generated artifacts,
runtime code, A1b artifacts, A2 artifacts, or any other issue disposition.

Any additional file or semantic delta, non-direct parent, intervening commit,
or unresolved identity invalidates this approval.

## Decision

Milestone 1 scope-recovery admission is approved for the exact reviewed
candidate. This report does not itself transition or start Milestone 1, modify
the protected test, register semantic relationships, change A1 runtime
behavior, create A1b authority, or activate A2.

The sole next authorized operation is the constrained lifecycle transition
above. M1 scope-recovery `start` becomes eligible only after that transition
commit exists and only while it remains the current `HEAD`.
