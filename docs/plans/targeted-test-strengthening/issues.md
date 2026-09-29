# Targeted Test Strengthening — Issues

## T-01 — Packaging acceptance is a separate prerequisite

The current packaging source is implemented and its exact-source CI is successful,
but its acceptance record remains Verifying. Preserve that record; deliver this
isolated test-only preparation without treating it as packaging acceptance. The
integration/acceptance owner reconciles the preceding gate before integrating this
next slice. No new packaging repair is called for by this work.

## T-02 — Supported candidate environment and independent review

Local Python 3.13.5 with rpds-py 2026.5.1 is not the hash-locked Python 3.12 CI
qualification. The task-owned toolchain download failed on DNS. Keep locks unchanged;
run the existing workflow on the integrated candidate and obtain independent review.
Current baseline CI is not evidence for the added tests.

## T-03 — Scope limits

The equality/hash and float-zero observations, dynamic import analysis, broader
storage tuning and additional typed-edit families remain deferred. Tests here
establish only their named finite mutation population and actual SQLite case.
No new production defect has been demonstrated by the initial checks.

## Final source disposition

All five selected gaps have implemented tests and sampled-fault detection evidence.
No production defect was demonstrated and no production repair is included. T-01
and T-02 remain integration/acceptance conditions, not failing local tests. T-03
remains an explicit scope limit. Source is ready for the separate candidate CI
and reviewer/owner decision once the preceding packaging gate is reconciled.
