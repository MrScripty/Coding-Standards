# Standards Engine A1b Implementation Candidate

**Status:** `Ready for independent content review`

**Implementation commit:** `3da674c1227a8ff6544e846a252a21a255854f49`

**Implementation tree:** `63d55780f77c7f1af64762b6363b8ba776e7fd51`

**Review subject:** The material A1b implementation content identified by the
commit and tree above. This report, review records, and lifecycle projections
are evidence about that content; adding them does not change the reviewed
subject.

## Candidate Scope

The candidate completes the C7 replacement of A1 with:

- the exact locked `jsonschema==4.26.0` and `referencing==0.37.0` dependency
  closure recorded in [dependency provenance](a1b-dependency-provenance.md);
- codepoint-preserving identity encoding v2 and owner-local semantic identity
  contracts;
- one generated v11 request/result algebra owned by Standards Contracts;
- exact path/raw-byte content snapshots and a bounded authority-envelope v1;
- one immutable SQLite schema-v1 authority repository with owner-local codecs;
- reference-only standards authority views and roots-only execution closure v2;
- four independently identified operation-authority contracts for route, read,
  related, and analysis;
- direct provider and authorization authority consumed only by successful
  analysis transitions; and
- one immutable, branchable analysis state with direct cold-process inspection
  of every advertised public object family.

The exact contract, object-kind, compatibility, role/cardinality, direct-
dependency, authority-view, execution-closure, and trust selections are
enumerated in the [C7 design](c7-design-proposal.md), [schema and domain
audit](schema-and-domain-contract-audit.md), [authority composition and
execution closure](authority-composition-and-execution-closure.md), and
[cutover evidence](a1b-cutover-evidence.md). Those records are incorporated as
candidate evidence rather than copied into another catalog.

## Corrected Review Findings

This candidate supersedes rejected implementation commit `d6117216`, tree
`8fd3b6fd9370a38952c115190069b6a288f77f2f`. The corrected boundary:

1. removes downstream codec-kind authority from Standards Authority;
2. requires domain owners to produce immutable authority-bound values;
3. checks exact qualified-root cardinality before map projection;
4. preserves side and role qualification for provider inputs;
5. places repository coverage composition behind Standards Analysis and
   removes the Verifier-to-Engine dependency;
6. moves deterministic public-contract projection generation to Standards
   Contracts and removes the former Engine generator;
7. executes every manifest-owned public root, export, and repository entrypoint
   in both admitted clean Python environments;
8. rejects aliased dynamic-import capability through the package verifier;
9. deletes the two unregistered superseded suite definitions;
10. reconstructs every advertised public object family in a genuinely fresh
    interpreter using persisted SQLite authority and public composition; and
11. removes the stale lazy dependency on the retired handwritten Engine model.

The implementation migration has no mutable relationship-count oracle.
Created, retained, and retired nodes and natural-key relationship dispositions
are recorded in [consumer dispositions](a1b-consumer-dispositions.md), the
registered relationship migration fixture, and [cutover evidence](a1b-cutover-evidence.md).

## Coverage And Generated Outputs

- The accepted and proposed policy-impact source registries compile through
  the same production path.
- Selected consumer subjects exactly equal recorded disposition subjects.
- Required coverage subjects exactly equal valid certificate subjects.
- Repository claim sources contain stable semantic selectors rather than
  generated handles or digests; Analysis derives current requirements,
  grants, attestations, and certificates.
- Generated Python contract output is fresh against the canonical v11 schema
  and interface contract.
- Every public package manifest declares its direct dependencies, public root,
  static exports, Python range, and repository entrypoints.
- Superseded validator, serializer, generator, storage, coverage, and
  compatibility paths are unreachable or deleted as required by the plan.

## Verification

The clean implementation tree passed:

| Evidence | Result |
| --- | --- |
| Standards Identity | 8 tests passed |
| Standards Contracts | 18 tests passed |
| Standards Authority | 38 package tests passed; one explicitly selected required-real case passed independently |
| Standards Applicability | 12 tests passed |
| Standards Metadata | 17 tests passed |
| Graph Engine | 37 tests passed |
| Standards Policy Impact | 9 tests passed |
| Standards Graph | 2 tests passed |
| Standards Analysis | 66 tests passed |
| Standards Engine | 33 tests passed |
| Standards Verifier | 386 tests passed |
| Clean public execution | Every manifest-owned root, export, and entrypoint passed on isolated CPython 3.11 and 3.12 |
| Required-real durability | The admitted Linux syscall-interruption oracle reached and interrupted the real SQLite synchronization boundary |
| Declarative verification | 226 of 226 registered suites passed |
| Migration verification | All 53 retained migration checkers passed without extension |
| Repository hygiene | Generated freshness, plan validation, changed-file Ruff, and diff checks passed |

The worktree was clean when the implementation commit and tree were recorded.

## Pending Independent Claims

This candidate does not self-accept:

- `A1B-A6L` remains pending independent confirmation that the implemented lock,
  artifact provenance, license and notice authority, non-bundling disposition,
  and required-real oracle match the admitted selection.
- `A1B-A11` remains pending independent Standards and Specification acceptance
  of this exact implementation content.
- The ADR remains `Proposed`, the plan remains `Active`, and A2 remains
  inactive until those claims are satisfied and final acceptance is recorded.
