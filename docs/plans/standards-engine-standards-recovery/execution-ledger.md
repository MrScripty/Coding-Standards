# Standards Engine Standards Recovery Execution Ledger

## 2026-08-24 - Plan Authoring Boundary

- Operation: author the standards-recovery plan only.
- Exact planning base: commit
  `3439aae9540786d9734431e633ea5b62afb50592`, tree
  `0ff4af77ebe5056c9478f04bf65dd87141f573d8`.
- Source brief:
  [Standards Recovery And Standards Engine A1b Redesign](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md).
- Routed authority: Core, Router, Planning, Verification, Documentation,
  Implementation, Commit, Contracts, Architecture, Dependencies, Build,
  Tooling, Library, Persistence, and conditional Language Binding/IPC.
- Scope result: six standards defects and their projections are in scope. A1b
  runtime redesign, all A2 work, Plan C, and historical A1 rewriting are out of
  scope.
- Inventory result: current policy-unit sources exist only for Commit,
  Planning, and Verification; current policy-impact sources exist only for
  Planning and Commit. Five proposed owners have no source declarations, and
  the new Planning meaning has no policy unit. All initial empty results are
  recorded as unaudited.
- Sequencing result: independent plan admission is the sole next slice. The
  plan is `Blocked`; no implementation operation is admitted.
- JSON Schema result: the known Draft 2020-12 equality disagreement is recorded
  as an active critical issue. This authoring slice does not reproduce or
  correct runtime behavior.
- Repository isolation: direct serial authoring in the current worktree; no
  branch or worktree was created by this plan.
- Files authored: `plan.md`, `execution-ledger.md`, `issues.md`, and
  `reports/semantic-impact-inventory.md` under this plan directory. The
  generated checker-structure inventory is refreshed because the plan must
  name exact retained checker paths and that inventory fingerprints Markdown
  inbound references.
- Verification: the focused plan-structure check and `git diff --check`
  passed. The canonical complete checkpoint passed generated-artifact
  freshness, all 218 registered declarative suites, and all 53 retained Bash
  checkers after the mechanically affected checker inventory was regenerated.
- Commit summary: `docs(planning): add standards recovery plan`; the resulting
  commit and tree are the candidate inputs for independent plan admission.

## Next Ledger Entry

The independent plan reviewer records an exact commit/tree review in
`reports/standards-recovery-plan-admission.md`. If admitted, the integration
owner updates the plan to `Planned` and names Milestone 0 reproduction as the
sole next slice. No policy or runtime file may change before that transition.

## 2026-08-24 - Independent Admission Rejection

- Reviewed candidate: commit
  `ec01ca7db9bd65cbf8c7186e6bc7cdf98879f007`, tree
  `76c2655717f6cc304b027379718760b5d5afedc0`.
- Admission result: rejected. The plan remains `Blocked`; no policy or runtime
  implementation is admitted.
- Standards findings: invalid Verification acceptance vocabulary, omitted
  canonical module-corpus write authority, conflated comparison and
  implementation bases, and incomplete issue-record fields.
- Specification findings: incomplete historical A1 repair-family reproduction,
  missing Router policy-unit/impact/coverage authority, and omitted
  Documentation workflow/acceptance-report consumer review.
- Verification context: the rejected tree remained mechanically green, but the
  existing checks did not prove the missing planning contracts.
- Repair disposition: replace all seven defective plan projections in one
  planning-only candidate, retain comparison commit `3439aae...`, require a
  later admission-bound implementation base, rerun focused and complete
  verification, and request another exact-tree review.
- Forbidden scope remains unchanged: no normative policy, A1b runtime, A2, or
  Plan C implementation.

## 2026-08-24 - Admission-Plan Repair Candidate

- Operation: repair the rejected planning boundary only.
- Comparison baseline remains commit
  `3439aae9540786d9734431e633ea5b62afb50592`, tree
  `0ff4af77ebe5056c9478f04bf65dd87141f573d8`; it is not the implementation
  checkout. A later independent admission must bind the exact planning commit
  and tree used as the implementation base.
- Acceptance contracts now use only Verification's closed evidence-kind,
  environment, and mode vocabularies. Automated and independent manual claims
  are separate objectives.
- Exact planning scope now includes canonical profile membership, a stable
  Router policy-unit/impact/coverage authority, Documentation and historical
  acceptance-report consumers, and all historical A1 repair-family
  reproductions required by the authoring brief.
- The official JSON Schema Test Suite source is pinned to commit
  `b01af8c8d50244a2eb4dd3e01073e24823aa8691` with an exact licensed fixture
  subset. Milestone 0 must reproduce the known defect; this candidate does not
  change runtime behavior.
- Issue records now bind evidence, objective relationships, owners, affected
  boundaries, dispositions, and revisit triggers.
- Verification: focused plan structure, plan fixtures, objective-vocabulary
  validation, generated-artifact freshness, `git diff --check`, all 218
  registered declarative suites, and all 53 retained Bash checkers passed.
- Lifecycle result: the plan remains `Blocked`. Independent exact-tree plan
  admission remains the sole next slice; no policy or runtime implementation
  is admitted.
