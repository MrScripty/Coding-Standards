# Plan A1 Boundary Repair II Candidate

**Status:** `Rework required`

**Review outcome:** The candidate was not accepted. Generated models omitted
numeric constraints and concrete result shapes, while cold child-artifact
inspection depended on execution authority not carried by the immutable state.
The implementation remains historical candidate evidence only.

**Implementation commit:** `714ba23fb5186b549ab44865d36c77509dbf654a`

**Implementation tree:** `d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b`

**Base and withdrawn acceptance commit:**
`b8f52240572962dd4393ff2d05b245a0c7f822a9`

**Base and withdrawn acceptance tree:**
`626c761fab2d5c5885d627f402c7b392bab12039`

## Candidate Disposition

The implementation resolves the SENA-022 findings while preserving the
accepted single-state architecture:

- Whole-module read and policy inspection content comes from the immutable
  snapshot content view. A post-issuance source mutation cannot change either
  result while retaining the same snapshot handle.
- Advertised context, fact-requirement, and fact-observation handles are
  reconstructed from persisted immutable analysis states. A fresh engine can
  inspect each handle without an instance-local artifact cache.
- The canonical JSON Schema now generates Python types, defaults, constants,
  discriminated unions, nested request and submission variants, decoding,
  exports, and agent-tool schemas. Semantic schema mutations change the
  generated projection, and stale generated output fails `--check`.
- The agent facade validates operation envelopes and delegates native object
  construction to the generated decoder. It no longer maintains a parallel
  request, change, fingerprint, evidence, or submission parser.
- Accepted-plan checking parses every objective row, rejects unknown or
  missing statuses, requires at least one objective, and requires both final
  projections. The ADR consistently uses snapshot identity version 2.

## Verification Evidence

| Verification surface | Result |
| --- | --- |
| `standards_analysis` | 82 tests passed |
| `standards_engine` | 41 tests passed |
| `standards_metadata` | 18 tests passed |
| `standards_applicability` | 12 tests passed |
| `standards_policy_impact` | 7 tests passed |
| `graph_engine` | 35 tests passed |
| `standards_graph` | 2 tests passed |
| `standards_verifier` | 380 tests passed |
| Canonical contract validation | 33 examples, 8 identity fixtures, 4 operation envelopes, and 143 definitions passed |
| Generated projection freshness | `generate_contract.py --check` passed |
| Accepted-plan fixtures | Valid and invalid lifecycle fixtures passed |
| Current plan catalog | Every current plan passed the strengthened checker |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Scoped Ruff and Git diff checks passed |

Focused regression evidence includes complete inspection equality after source
mutation, cold-engine reconstruction of all three advertised analysis child
artifact kinds, generated field/type/default/discriminant/submission coverage,
semantic generator mutation checks, malformed objective status rejection, and
missing accepted final-projection rejection.

## Admission State

This document records a review candidate, not an acceptance. Plan A1 remains
`Verifying`, SENA-022 remains active, and objectives A2, A3, A8, and A9 remain
pending until an independent review accepts a superseding exact boundary.
Controlled authoring Plan A2 remains inactive.
