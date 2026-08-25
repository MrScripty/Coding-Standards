# Plan: Systemic Finding Without Audit

**Plan status:** `Blocked`

**Current phase:** systemic-finding replan

**Next slice:** complete the missing invariant-family and consumer audit

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Repair a repeated generated-contract validation failure.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Every affected consumer preserves the invariant | `contract` | `not-applicable` | `automated` | `pending` | Pending audit |

## Scope

### In Scope

- One observed validator.

### Out Of Scope

- Sibling consumers not yet inventoried.

## Milestones

### Milestone 0: Local Repair

**Goal:** Repair the first observed validator.

**Allowed write set:**

- `validator.py`

**Tasks:**

- [ ] Change the first observed implementation.

**Acceptance gate:**

- One local test passes.

**Status:** `Blocked`

## Re-Plan Triggers

- Discovery of another affected consumer.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Blocked`
