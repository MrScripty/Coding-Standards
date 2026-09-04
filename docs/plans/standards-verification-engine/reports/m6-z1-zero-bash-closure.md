# M6-Z1 Zero-Bash Closure

**Status:** `Accepted`

**Date:** 2026-09-03

## Boundary

M6-Z1 closes the Bash-to-Python verification migration after M6-I126 removed
the final Bash helper. Standards Engine applications `fc22c42a` and
`9790e576` first retired the three migration-launcher projections and five
migration-only module projections without changing current standards policy.

The terminal implementation then:

- removes the remaining baseline, owner-map, and metadata Bash launchers;
- removes the temporary inventory, dependency graph, edge-disposition,
  numeric-lifecycle, execution-train, and migration-Python machinery;
- removes their launchers, tests, suites, generated observations, lifecycle
  tables, and orphan supplemental catalog nodes;
- reduces the row-35 suite to its five permanent policy checks;
- makes `--complete` run the immutable registered Python catalog directly; and
- exposes the same complete result through text, JSON, and the library API,
  with no subprocess phase, session token, adapter, compatibility path, or
  fallback.

Historical ledgers and reports remain historical evidence. They do not keep a
deleted migration path live or make it current authority.

## Final State

- Registered Python suites: 271.
- Bash verifiers, helpers, and launchers in the migration scope: 0.
- Temporary Bash graph and migration lifecycle suites: absent.
- Complete-mode meanings: one Python catalog execution, represented in text or
  JSON.
- Current coverage: all 51 dependency-local requirements have renewed IDs and
  complete authorized attestations.

## Verification

| Check | Result |
| --- | --- |
| Verifier unit suite | 349 tests passed |
| Complete text mode | 271 selected, 271 passed, 0 failed, 0 blocked |
| Complete JSON mode | 271 results with the same passing summary |
| Migration-scope shell inventory | No `.sh` path under `evaluation/standards-effectiveness` or `tools/standards_verifier` |
| Repository Git regression suite | 11 tests passed |
| Neutral graph regression suite | 37 tests passed |
| Standards Engine regression suite | 68 tests passed from the accepted `HEAD` |
| Canonical suite-input projection | Fresh after terminal documentation and attestation renewal |

The acceptance gate is satisfied: the Python engine is the sole verification
authority, and no wrapper, transitive Bash execution, arbitrary command action,
dual authority, compatibility representation, or fallback remains.
