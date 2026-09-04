# Standards Recovery Discovery Admission

## Reviewed Boundary

- Result: `Approved for discovery admission`.
- Reviewed planning commit:
  `39d5210dcb32611c725052e67a918b4f88de9cc7`.
- Reviewed planning tree:
  `ef5f626c9bc2300c648fe7f3aa0d482c58d85233`.
- Comparison baseline: commit
  `3439aae9540786d9734431e633ea5b62afb50592`, tree
  `0ff4af77ebe5056c9478f04bf65dd87141f573d8`.
- Historical A1 reproduction boundary: commit
  `2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
  `97c850ab718287007c1e1daac538f40869f71a1d`.
- Review axes: repository Standards and the standards-recovery specification
  derived from the A1b authoring brief.

The reviewed worktree was clean. This report is the only repository change
authorized by the independent-review operation.

## Standards Review

No findings.

The reviewed snapshot:

- separates the reviewed planning snapshot, reviewer-owned report, constrained
  lifecycle transition, and later milestone `start`;
- records a bounded reference-only Licensing decision without incorporating
  third-party material;
- preserves rejected admission history without retaining a stale current
  instruction; and
- assigns new recovery enforcement to registered Python declarative suites
  without extending retained Bash checkers.

Standards total: zero findings.

## Specification Review

No findings.

The reviewed snapshot:

- defines exact reviewer-report and transition-commit mechanics;
- binds the accepted A1 commit and tree;
- limits Milestone 0 to historical reproduction and preliminary scope audit;
- keeps final attestations and certificates downstream of frozen policy and
  horizon authority;
- places the future systemic-finding negative scenario outside the retained
  Bash `invalid-*` fixture glob; and
- makes SR-A7 record the known A1 disagreement without requiring its correction
  during standards recovery.

Specification total: zero findings.

## Verification

Independent review confirmed:

- `HEAD` and the repository tree matched the reviewed identities;
- the worktree was clean;
- all 218 registered declarative suites passed;
- all 53 retained Bash checkers passed without extension;
- focused plan, lifecycle, Licensing, and generated-freshness checks passed;
  and
- `git diff --check` passed.

## Non-Blocking Precision Note

The reference-only Licensing decision identifies the exact Draft 2020-12 Core
and Validation URLs and selected clauses. Its `Published identity` row lists
only Core's `draft-bhutton-json-schema-01`; the corresponding Validation
publication identifies itself as
`draft-bhutton-json-schema-validation-01`.

This does not block discovery admission because the exact Validation URL and
clause are already bound. If that Licensing report is edited later, listing
both publication identifiers would improve provenance. This note does not
authorize editing it during the admission transition.

## Authorized Admission Transition

This approval authorizes one mechanical transition commit after the commit
that contains this report. The transition commit must have the report commit as
its direct parent and may change only:

- `docs/archive/plans/standards-engine-standards-recovery/plan.md`;
- `docs/archive/plans/standards-engine-standards-recovery/execution-ledger.md`; and
- `docs/archive/plans/standards-engine-standards-recovery/issues.md`.

The transition may perform only these changes:

1. Record the reviewed planning commit/tree above.
2. Record the exact commit/tree containing this admission report.
3. Set the plan and Milestone 0 to `Planned`.
4. Set the current phase to Milestone 0 ready for `start`.
5. Name Milestone 0 `start` as the sole next operation.
6. Record that the resulting transition commit is the admitted
   discovery/audit base whose exact identity must be captured by `start`.
7. Update SESR-009 and append ledger evidence only to reflect this admission
   and the still-pending `start` transition.

The transition must not change scope, tasks, write or read sets, objectives,
evidence contracts, policy, Router authority, fixtures, verifier behavior,
runtime code, A1b artifacts, A2 artifacts, or any other issue disposition.

Any additional file or semantic delta, non-direct parent, intervening commit,
or unresolved identity invalidates this approval.

## Decision

Discovery admission is approved for the exact reviewed planning snapshot. This
report does not itself transition the plan, start Milestone 0, admit policy
implementation, change A1 runtime behavior, create A1b authority, or activate
A2.

The sole next authorized operation is the constrained admission transition
above. Milestone 0 `start` becomes eligible only after that transition commit
exists and only while it remains the current `HEAD`.
