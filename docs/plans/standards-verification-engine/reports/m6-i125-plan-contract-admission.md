# M6-I125 Plan Contract Admission

## Decision

Admit `verify-plan-fixtures.sh` at train order 240 as a `shared-contract`
package owned by `workflow.planning`. The package may add one strict
`plan_contract` check kind to the existing `planning-consolidation` suite and
delete the Bash verifier after parity and complete mixed evidence pass.

## Fresh Selection Evidence

The post-M6-I124 generated graph contains 1 Bash verifier, 2 executable nodes,
15 conservative edges, and 2 components. The 55-line verifier is the sole
executable root and invokes the 226-line `check-plan-structure.sh` helper.
Nine repository artifacts refer to the verifier; the helper also remains a
declared Standards Engine policy projection.

## Owned Contract

The typed check will consume one repository-contained Markdown plan and
preserve:

- the exact plan, acceptance, milestone, objective, and final-projection
  lifecycle domains and their cross-field consistency;
- required plan fields and headings, objective table structure, satisfied
  evidence, and accepted-plan closure;
- the prohibition on execution history in the active plan; and
- applicability, concrete reasons, and each composed-design probe required by
  the planning contract.

The check exposes typed diagnostics and repository-contained file inputs. It
does not execute commands, accept callbacks, infer compatibility behavior, or
retain Bash as fallback.

## Two-Stage Helper Boundary

M6-I125 deletes only `verify-plan-fixtures.sh`. It retains
`check-plan-structure.sh` as a non-executed policy projection because two
current Standards Engine relationships name that artifact. The retained
helper is not an alternate execution path: all plan fixtures move to the
typed suite in this package.

Deleting the verifier makes the frozen Bash verifier graph header-only. From
that stable state, a fresh Standards Engine proposal can move the two policy
relationships to the registered `planning-consolidation` suite without making
the generated graph stale during candidate verification. A subsequent
package will delete the relationship-free helper.

## Dependency And History Transfer

The verifier's executable and helper dependency edges receive explicit
`external-owned-artifact` dispositions during this package because the helper
remains an Engine-declared projection. Accepted historical independent-gate
records that select the plan verifier transfer to `suite:planning-consolidation`
without rewriting their historical source or target identities.

## Frozen Write Set

The canonical package-manifest row owns the exact implementation write set. It
covers the typed check and direct tests, parser registration, three affected
suites, package and edge authority, generated graph and suite-input evidence,
the eleven affected dependency-local coverage-attestation sources, verifier
documentation, both recovery plans and ledgers, the active verifier plan,
checker inventory, parent plan, this admission report, and deletion of the Bash
verifier. The suite changes renew 50 of 51 current coverage identities while
leaving the unrelated requirement stable.

## Acceptance Evidence

Acceptance requires:

1. canonical Bash/Python success parity for all four valid fixtures and exact
   diagnostic parity for all fifteen invalid fixtures;
2. rejecting mutations for lifecycle, required-field, objective,
   applicability, reason, and composed-design-probe behavior;
3. direct Python unit tests for the typed check and strict parser contract;
4. focused planning, evidence-boundary, systemic-replanning, package, edge,
   numeric-lifecycle, and retained-helper checks;
5. exact 50/50 dependency-local coverage renewal, generated graph and
   suite-input freshness, all verifier,
   repository-Git, and graph tests, all registered suites, the retained helper,
   and the complete mixed checkpoint; and
6. staged-scope, sensitive-content, whitespace, source-unchanged, and removed-
   path review.
