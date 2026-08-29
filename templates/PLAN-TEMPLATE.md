# Plan: [Short Outcome]

**Plan status:** `Planned`

**Current phase:** [Milestone or phase]

**Next slice:** [Exactly one slice or `none` for terminal status]

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

State the externally meaningful outcome and who or what observes it.

## Objective Acceptance

State the exact claims that close the objective. Add rows when the objective
requires independent proof kinds.

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | [Externally meaningful result] | `focused` | `not-applicable` | `automated` | `pending` | [Link or pending] |

## Scope

### In Scope

- [Owned result]

### Out Of Scope

- [Explicit exclusion]

## Constraints And Assumptions

### Constraints

- [Constraint that affects decisions]

### Assumptions

- [Assumption and validation owner]

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| [Current decision] | [Owner] | [Reason/source] | [Prior decision or none] |

## Evidence And Oracle Plan

Use when acceptance depends on generated output, multiple implementations,
external contracts, persisted authority, or negative fixtures. Remove this
section when none applies.

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| [Claim] | [Freshness, shape, semantics, public path, external conformance, or other] | [Exact oracle] | [Authority or not applicable] | [Boundary] | [Exact diagnostic or not applicable] |

Do not treat freshness as semantic correctness, agreement between local
implementations as external conformance, in-process reconstruction as
cold-process evidence, or any fixture failure as proof of its intended claim.

## Systemic Finding Audit

Use when a defect reveals a repeated invariant, duplicated authority, missing
projection, ambient-state dependency, or public/internal boundary leak. Remove
this section when the finding is demonstrably isolated.

- Invariant family:
- Sibling producers and consumers:
- Authority and projection inventory:
- Consumer dispositions:
- Scope or sequencing replacement:

## Simplicity And Ownership Review

**Applicability:** `applicable` or `not-applicable`

Every nonterminal written plan keeps this field. If `not-applicable`, replace
the probe below with `**Reason:** [Concrete reason]`. If `applicable`, answer
every probe with current artifact evidence.

- Independent concepts and dimensions:
- State, identity, value, time, policy, and mechanism:
  - Canonical authority scope and referenced authorities:
  - Version and identity-invalidation scopes:
- Caller and composition-root knowledge:
- Representative change paths and forced owners:
- Stable Interfaces versus hidden knowledge:
- Independent evolution, testing, failure, and replacement:
- Necessary complexity and containment:
- Deletion and cumulative machinery result:

## Milestones

A plan may contain one milestone and one implementation slice when that is the
complete coherent change. Add or split milestones only when separation
materially improves independent acceptance, risk containment, dependency
ordering, conflict isolation, rollback, or feedback. File count, layer count,
line count, and commit cadence do not decide milestone or slice count.

Milestones do not prescribe Git commit count, parentage, direct-child chains,
exact-HEAD admission, or standalone lifecycle commits. Bind review to material
content and update lifecycle state with the coherent outcome or evidence that
caused it. The Commit workflow owns commit boundaries.

### Milestone 0: [Name]

**Goal:** [One useful result]

**Allowed write set:**

- `[path]`

**Tasks:**

- [ ] [Task]

**Acceptance gate:**

- [Evidence and level]

**Status:** `Planned`

## Blockers

- `none`

## Re-Plan Triggers

- [Fact or failure that invalidates a decision, scope, sequence, or gate]
- [Material replacement, cumulative machinery, or observed propagation that
  requires a new composed-design decision]

## Concurrent Work

Use only when work is independent.

| Owner | Primary write set | Adjacent write set | Forbidden/shared | Output/report | Integration order |
| --- | --- | --- | --- | --- | --- |
| [Owner] | [Paths] | [Paths or none] | [Paths] | [Contract and report] | [Order] |

When the
[Concurrent Plan Integration profile](../profiles/workflows/concurrent-plan-integration.md)
applies, record the selected revision mechanism and admitted revision, proposal
actor, scope, write set, prerequisites, intended outcome and state,
verification contract, and integration owner. Omit those fields when the
profile does not apply. Do not add digest or transition-envelope fields merely
because work is delegated.

## Repository Isolation

When material repository isolation is part of the plan, record its purpose,
responsible owner, target branch, visibility or long-lived status, integration
owner, and expected terminal disposition. Record an admitted base only when
stale-state coordination makes it relevant. Omit repository-isolation fields
and remove this section for direct serial work. Do not require a branch merely
because a written plan exists or because work is delegated.

For each worktree created by the plan, record its exact path and terminal
outcome. If removal is authorized, record the exact head OID, its reachability,
and its retained, archived, or discard-authorized commit disposition. Final
evidence confirms that its registry entry is absent after safe removal and its
protected-OID postcondition holds, or records an explicit retained-resource
contract with its purpose, owner, and next disposition. This evidence is scoped
to plan-created paths and does not authorize repository-wide pruning.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Planned`
