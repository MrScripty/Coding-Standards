# Plan A1 Boundary Repair IV Candidate

**Status:** `Rework required`

**Review outcome:** The candidate was not accepted. Generated validation still
used a second equality implementation for constants and enums and ordinary
Python membership for `uniqueItems`, producing canonical disagreements for
mixed Boolean/integer values and canonically equivalent Unicode. The plan
fixture harness also matched diagnostic fragments rather than the complete
emitted line. This report remains historical candidate evidence only.

**Implementation commit:** `3d389dd7f73f48c21d80570331c8058737f941db`

**Implementation tree:** `6fcbfed114dcfd768186f8610c0792e220657b32`

**Rejected predecessor:** commit
`8ed8ba0beba5dd16c0a2da50655952842ab61c85`, tree
`eaeac78739468fc2c79241f6a7830e54986d2f95`

## Candidate Disposition

The implementation addresses the remaining Repair III findings without
changing the accepted single-state architecture:

- Generated constants and enums use type-sensitive canonical equality. A
  Boolean cannot satisfy an integer constant or enum value merely because
  Python considers the values equal.
- Generated pattern validation uses JSON Schema search semantics rather than
  requiring the pattern to match the complete string.
- Native `StandardsEngine.prepare` and `StandardsEngine.resolve` return the
  generated public `PendingResult` and `CompleteResult` classes. Conversion
  validates the complete domain projection through the generated decoder.
- The missing-evidence and invalid-objective-status fixtures are otherwise
  valid plans, and their harness requires the exact intended diagnostics.
- Current ADR prose uses immutable analysis-state and result terminology;
  packet and report terminology remains only where explicitly historical.

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
| Plan regressions | Otherwise-valid fixtures produced the exact missing-evidence and invalid-status diagnostics |
| Current plan catalog | Every current plan passed the strengthened checker |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Scoped Ruff and Git diff checks passed |

Focused regressions reject Boolean values for integer constants, preserve JSON
Schema pattern search behavior, and prove that native prepare and terminal
resolve operations return the exported generated result classes. The plan
fixture harness now fails if either regression is rejected before reaching its
claimed objective diagnostic.

## Admission State

This document records a review candidate, not an acceptance. Plan A1 remains
`Verifying`, SENA-022 remains active, and objectives A2, A3, A8, and A9 remain
pending until an independent review accepts this exact boundary. Controlled
authoring Plan A2 remains inactive.
