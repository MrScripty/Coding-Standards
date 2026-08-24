# Plan A1 Boundary Repair Acceptance

**Status:** `Accepted`

**Implementation commit:** `51dcd258942b0774c73ae8b620227c7ce34d1129`

**Implementation tree:** `f8d028e887f4061a1d03ad6e75b9776a5fc3966b`

**Supersedes:** the withdrawn acceptance at commit
`94b295b40bc1cef9a6281355d68115f3a98ed112`, tree
`ff032da51fcaff45533c07daa8de464065b8e55c`

## Disposition

Plan A1 is accepted at the repaired implementation boundary. The repair keeps
the accepted single-state architecture and closes SENA-021 without adding a
packet/report compatibility lifecycle or admitting controlled authoring.

The boundary establishes these corrected contracts:

- Snapshot-bound reads resolve immutable content captured from an exact Git
  tree or a digest-verified manifest, never later worktree bytes.
- Snapshot identity includes interpretation-affecting semantic contract
  versions; implementation releases remain provenance when they do not alter
  meaning.
- The canonical JSON Schema generates the Python request/result algebra and
  agent-tool definitions, and deterministic generation drift fails validation.
- Agent argument failures remain typed rejections while engine-produced
  invariant failures remain programming errors.
- Canonical serialization normalizes object keys and rejects normalization
  collisions through one metadata-owned implementation.
- Every advertised handle is inspectable, including generated consumer
  coverage certificates and the analysis-state authority chain.
- Every derived continuation binds the exact snapshot or analysis that makes
  the operation valid.
- Plan acceptance verification reconciles the plan header, all objective rows,
  milestone states, and final acceptance projection.

## Verification Evidence

The exact implementation tree passed:

| Verification surface | Result |
| --- | --- |
| `standards_analysis` | 82 tests passed |
| `standards_engine` | 39 tests passed |
| `standards_metadata` | 18 tests passed |
| `standards_applicability` | 12 tests passed |
| `standards_policy_impact` | 7 tests passed |
| `graph_engine` | 35 tests passed |
| `standards_graph` | 2 tests passed |
| `standards_verifier` | 380 tests passed |
| Canonical contract validation | 33 examples, 8 identity fixtures, 4 operation envelopes, and 143 definitions passed |
| Generated projection freshness | `generate_contract.py --check` passed |
| Declarative suite catalog | 218 of 218 suites passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Formatting and patch integrity | Ruff and Git diff checks passed |

Focused regressions cover source mutation after snapshot issuance, semantic
contract-version identity, generated projection freshness, every request and
result variant, every inspectable handle, normalized-key collision rejection,
snapshot- and analysis-bound continuations, and contradictory accepted-plan
projections.

## Boundary

This acceptance completes read-only Plan A1 navigation and analysis only.
Controlled authoring remains subject to a separately reviewed and admitted Plan
A2. Evidence-oracle policy and projection correction remain Plan B concerns,
and external-project application and upgrade baselines remain Plan C concerns.
