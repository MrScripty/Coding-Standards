# Work Proportionality And Policy Impact Recovery Execution Ledger

## 2026-08-20: Recovery Admission

- Operation: `start`.
- Accepted base: `68b52ba05587d3c8278aed82ee5b16202a024462`.
- Preconditions: canonical `main` was clean; M6-I16 was accepted in both active
  plans and the package manifest; no M6-I17 package was admitted.
- Trigger: slice proportionality remains ambiguous, and no permanent reviewed
  semantic-impact relation identifies policy consumers and projections.
- Residual defect: `workflows/implementation.md` unconditionally consumes
  concurrent-only transition identity, revision, compatibility, and
  reconciliation decisions for ordinary written plans.
- Decision: freeze verifier-package migration and accept the semantic-impact
  foundation before correcting proportionality and residual projections.
- Scope: planning authority only; no normative policy, verifier mechanics,
  suite, fixture, or generated evidence changed in this admission.
- Verification:
  - recovery, verification-engine, and parent plan structure passed;
  - `planning-admission` passed three checks;
  - `planning-consolidation` passed four checks;
  - `plan-template-projection` passed three checks; and
  - `git diff --check` passed.
- Result: recovery authority is active. Milestone 1 is the only admitted next
  slice, and M6-I17 remains unadmitted.

## 2026-08-20: Semantic Consumer/Impact Foundation

- Operation: `continue`.
- Boundary: permanent current policy structure lives in the strict semantic
  impact manifest; this recovery report and ledger own only acceptance evidence.
- Coverage: `workflow.planning` is explicitly audited. Uncovered owners are
  typed `unavailable` and must be audited before their next normative change.
- Mechanics: added one reusable `policy_impact` check and one read-only TSV
  reverse query. Canonical metadata resolves policy owners; the suite registry
  resolves enforcement consumers and evidence owners.
- No inference: hyperlinks, lexical similarity, standards `Requires`, and the
  temporary Bash checker graph create no semantic edge.
- Query result: every required Planning normative consumer, Router, prompt,
  template, planning/concurrent fixture, and enforcement suite is returned;
  [the review report](reports/planning-impact-foundation.md) records the exact
  artifact set.
- Negative evidence: duplicate edges, unknown owners and consumers, empty
  applicability, malformed relations, path escape, and missing files are
  rejected; direct tests also cover owner-metadata mismatch, unknown evidence
  owners, deterministic ordering, and unaudited-owner queries.
- Verification:
  - focused impact suite passed two checks;
  - all 315 Python tests passed;
  - all 164 registered declarative suites passed;
  - generated evidence remained current at 109 retained Bash checkers, 113
    nodes, 683 edges, and 113 components;
  - recovery plan structure, affected Markdown links, and `git diff --check`
    passed; and
  - the complete mixed checkpoint passed all 109 retained Bash checkers.
- Result: Milestone 1 accepted. Milestone 2 is the only admitted next slice;
  M6-I17 remains unadmitted.
