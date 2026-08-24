# Plan A1 Boundary Repair VI Candidate

**Status:** `Ready for independent review`

**Implementation commit:** `2359a98740b6035a0414bfaf5427ceaa1301a1c8`

**Implementation tree:** `97c850ab718287007c1e1daac538f40869f71a1d`

**Rejected predecessor:** commit
`e7e0e1e20762f994e644f2e3c88d017d1625266c`, tree
`22c263b4f30c706b94ce3125c8f0537e5d210fe6`

## Candidate Disposition

The implementation addresses the remaining Repair V findings without changing
runtime semantics or the accepted single-state architecture:

- Generated code imports `canonical_json_bytes` through the public
  `standards_metadata` package entry point identified by the ADR.
- Const and enum differential tests cover composed/decomposed Unicode,
  Boolean supplied against integer authority, and integer supplied against
  Boolean authority.
- Unique-items differential tests continue to cover mixed Boolean/integer and
  canonically equivalent Unicode collections.

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
| Differential equality matrix | Const, enum, and unique-items decisions agree for Boolean/integer and Unicode inputs |
| Current plan catalog | Every current plan passed the strengthened checker |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Scoped Ruff and Git diff checks passed |

## Admission State

This document records a review candidate, not an acceptance. Plan A1 remains
`Verifying`, SENA-022 remains active, and objectives A2, A3, A8, and A9 remain
pending until an independent review accepts this exact boundary. Controlled
authoring Plan A2 remains inactive.
