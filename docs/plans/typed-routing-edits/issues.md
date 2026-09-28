# Issues and gates

- Q1 — resolved: the pilot is integrated at `7d563f03` on GitHub `main`.
  Exact-commit [workflow run 36358571883](https://github.com/MrScripty/Coding-Standards/actions/runs/36358571883)
  passed the repository's Python 3.12 hash-locked installation, all twelve
  package selections and complete structural verifier. Python 3.11 is supported
  by package metadata and lock but is not an entry in the current CI workflow.
- Q2 — reviewer: independent external review is required before Accepted status;
  a fresh internal read-only architecture review found no implementation blocker,
  but is not a substitute. External reviewer/acceptance owner remains to be assigned.
- Q3 — pilot boundary: other StructuredEdit families remain unchanged. Do not
  generalize to every edit or build a second expression interpreter without a
  separately demonstrated need and admission.

- Q4 — resolved before the final run: composition review moved all original parse
  checks to their existing logical-authoring owner; the new value module imports
  only stdlib and contains no compiler/validator dependency. The stopped initial
  campaign is preserved separately, not treated as a successful full selection.
- Q5 — deferred advisory from fresh review: private float comparison treats
  negative and positive zero as equal. The identity codec rejects floats and
  applicability has no numeric operand path; no valid-workflow failure was
  demonstrated. Do not widen this pilot without new evidence.
- Q2 remains the sole unsatisfied pilot acceptance gate, not a demonstrated
  defect. Q3 remains the scope boundary. See reports/verification.md for evidence
  and the preceding-slice reconciliation.
