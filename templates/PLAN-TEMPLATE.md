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

## Simplicity And Ownership Review

Use for cross-layer, stateful, contract-heavy, concurrent, or refactor work.

- Independent concepts:
- Intentional coupling:
- Accidental coupling risk:
- Policy/state/lifecycle owners:
- Future changes that should remain independent:

## Milestones

A plan may contain one milestone and one implementation slice when that is the
complete coherent change. Add or split milestones only when separation
materially improves independent acceptance, risk containment, dependency
ordering, conflict isolation, rollback, or feedback. File count, layer count,
line count, and commit cadence do not decide milestone or slice count.

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
classification. Final evidence confirms that its registry entry is absent
after safe removal or records an explicit retained-resource contract with its
purpose, owner, and next disposition. This evidence is scoped to plan-created
paths and does not authorize repository-wide pruning.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Planned`
