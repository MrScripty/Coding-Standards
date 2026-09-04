# Plan A1 Boundary Repair V Candidate

**Status:** `Rework required`

**Review outcome:** The candidate was not accepted. Generated code imported the
canonical serializer through an internal metadata module instead of the
documented package entry point, and const/enum differential evidence covered
Unicode normalization but not Boolean/integer type distinctions. Runtime
behavior was correct; the remaining defects were public-boundary discipline
and durable evidence completeness. This report remains historical candidate
evidence only.

**Implementation commit:** `e7e0e1e20762f994e644f2e3c88d017d1625266c`

**Implementation tree:** `22c263b4f30c706b94ce3125c8f0537e5d210fe6`

**Rejected predecessor:** commit
`3d389dd7f73f48c21d80570331c8058737f941db`, tree
`6fcbfed114dcfd768186f8610c0792e220657b32`

## Candidate Disposition

The implementation addresses the remaining Repair IV findings without
changing the accepted single-state architecture:

- Generated const, enum, and `uniqueItems` checks use
  `standards_metadata`'s canonical serializer rather than a second equality
  implementation or Python membership semantics.
- Mixed integer and Boolean values retain distinct canonical representations.
  Canonically equivalent composed and decomposed Unicode share one normalized
  representation.
- Differential regressions exercise canonical validation and generated model
  construction with the same values and require matching decisions.
- The plan fixture harness compares its complete captured output with the exact
  expected fixture path and diagnostic text. Additional or merely containing
  output no longer satisfies the oracle.

## Verification Evidence

| Verification surface | Result |
| --- | --- |
| `standards_analysis` | 82 tests passed |
| `standards_engine` | 45 tests passed |
| `standards_metadata` | 18 tests passed |
| `standards_applicability` | 12 tests passed |
| `standards_policy_impact` | 7 tests passed |
| `graph_engine` | 35 tests passed |
| `standards_graph` | 2 tests passed |
| `standards_verifier` | 380 tests passed |
| Canonical contract validation | 33 examples, 8 identity fixtures, 4 operation envelopes, and 143 definitions passed |
| Generated projection freshness | `generate_contract.py --check` passed |
| Differential equality regressions | Canonical and generated const, enum, and unique-items decisions agree for Boolean/integer and Unicode inputs |
| Plan regressions | Otherwise-valid fixtures produced exactly one complete expected diagnostic line |
| Current plan catalog | Every current plan passed the strengthened checker |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Scoped Ruff and Git diff checks passed |

## Admission State

This document records a review candidate, not an acceptance. Plan A1 remains
`Verifying`, SENA-022 remains active, and objectives A2, A3, A8, and A9 remain
pending until an independent review accepts this exact boundary. Controlled
authoring Plan A2 remains inactive.
