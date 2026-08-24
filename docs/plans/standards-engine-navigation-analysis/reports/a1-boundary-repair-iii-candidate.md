# Plan A1 Boundary Repair III Candidate

**Status:** `Rework required`

**Review outcome:** The candidate was not accepted. Generated constants and
enums used Python equality, patterns used full-match semantics, native analysis
operations still returned domain result classes, and the new negative plan
fixtures did not prove their intended objective diagnostics. This report
remains historical candidate evidence only.

**Implementation commit:** `8ed8ba0beba5dd16c0a2da50655952842ab61c85`

**Implementation tree:** `eaeac78739468fc2c79241f6a7830e54986d2f95`

**Rejected predecessor:** commit
`714ba23fb5186b549ab44865d36c77509dbf654a`, tree
`d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b`

## Candidate Disposition

The implementation addresses the remaining SENA-022 findings without changing
the accepted single-state architecture:

- One schema traversal closes over every public operation input and result,
  then generates concrete immutable Python models for that complete closure.
  Results no longer use arbitrary mapping wrappers.
- The generated decoder enforces the schema assertions used by A1, including
  required and additional object properties, exact `oneOf` selection, string
  constraints, array constraints, constants, enums, and integer minimums.
  Direct model construction and `from_value` use the same decoder.
- Analysis-state inspection returns the generated `AnalysisState` model.
- Pure reprojection binds exact snapshot authorities plus authorization and
  provider authority views stored in immutable state. It does not depend on
  fresh engine execution authority and does not invoke providers.
- A4 through A7 cite still-valid milestone evidence. Objective status is
  limited to `pending`, `blocked`, or `satisfied`, and satisfaction requires
  evidence. Retired packet and report domains are historical rather than
  current ADR authority.

## Verification Evidence

| Verification surface | Result |
| --- | --- |
| `standards_analysis` | 82 tests passed |
| `standards_engine` | 43 tests passed |
| `standards_metadata` | 18 tests passed |
| `standards_applicability` | 12 tests passed |
| `standards_policy_impact` | 7 tests passed |
| `graph_engine` | 35 tests passed |
| `standards_graph` | 2 tests passed |
| `standards_verifier` | 380 tests passed |
| Canonical contract validation | 33 examples, 8 identity fixtures, 4 operation envelopes, and 143 definitions passed |
| Generated projection freshness | `generate_contract.py --check` passed |
| Current plan catalog | Every current plan passed the strengthened checker |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Scoped Ruff and Git diff checks passed |

Focused regressions reject semantic revision zero and incomplete route results,
prove result type/required changes alter generated output, verify concrete
generated analysis-state results, inspect public cold contexts without
execution authority, retain cold requirement and observation inspection, and
reject partial or unevidenced objective satisfaction.

## Admission State

This document records a review candidate, not an acceptance. Plan A1 remains
`Verifying`, SENA-022 remains active, and objectives A2, A3, A8, and A9 remain
pending until an independent review accepts a superseding exact boundary.
Controlled authoring Plan A2 remains inactive.
