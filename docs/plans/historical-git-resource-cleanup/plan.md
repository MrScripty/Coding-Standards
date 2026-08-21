# Plan: Historical Git Resource Cleanup

**Plan status:** `Active`

**Current phase:** Milestone 2 stale-registration cleanup

**Next slice:** prune exactly the 384 missing unlocked registrations in the accepted candidate inventory

**Acceptance status:** `pending`

**Accepted base:** `8cce95b27220faa3ed115542c7242464d04df225`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Classify and, only under separately accepted authority, retire redundant local
Git worktree registrations and branch refs without deleting unknown resources,
discarding unique commits, rewriting shared history, or treating age, count,
ancestry, or patch equivalence as deletion authority.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Every current worktree registration and local branch has one reviewed ownership and terminal disposition. | `partial` | Current inventories classify all resources; branch terminal review follows registration cleanup |
| A2 | Pruned registrations are proven missing, task-independent, unlocked, and free of a live or user-owned path before mutation. | `pending` | Milestone 2 execution report |
| A3 | No branch with unique, shared, published, checked-out, unknown, or unmapped replacement history is deleted. | `pending` | Branch disposition review |
| A4 | Repository state and protected commit reachability are verified before and after every accepted cleanup batch. | `pending` | Verification reports |

## Scope

### In Scope

- Read-only refresh of local branch and worktree inventories.
- Exact ownership, reachability, patch-equivalence, checked-out, lock, path,
  dirtiness, and unique-commit classifications.
- Separately accepted cleanup batches for unambiguous stale registrations or
  redundant refs.
- Before/after reachability, registry, and repository-integrity evidence.

### Out Of Scope

- Cleanup during plan creation or without an explicit `start` operation.
- Force-removing dirty, locked, unknown, user-owned, or uniquely committed
  worktrees.
- Deleting unique or unmapped branch history, rewriting shared history, or
  inferring acceptance from ancestry or patch equivalence.
- Verifier migration, temporary Bash graph changes, remote publication, or
  downstream pilots.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Current authority | Refresh Git facts after `start`; the prior lifecycle-policy inventories are historical evidence, not current cleanup authority. |
| Safe default | Unknown or contradictory ownership, path, lock, reachability, mapping, or retained-purpose facts refuse cleanup. |
| Registration boundary | Administrative pruning and filesystem worktree removal are distinct operations with distinct evidence. |
| Branch boundary | Ancestry and patch equivalence may trigger review but cannot authorize deletion without terminal ownership and replacement lineage. |
| Batch size | Group only resources sharing ownership, disposition, risk, and verification contracts; preserve exact per-resource evidence. |
| Integration owner | One serial owner controls inventory, cleanup commands, acceptance evidence, and shared Git authority. |

## Milestones

| Milestone | Goal | Status |
| --- | --- | --- |
| 1 | Refresh read-only branch/worktree facts and exact dispositions. | `Accepted` |
| 2 | Execute an explicitly authorized stale-registration cleanup batch with before/after proof. | `Planned` |
| 3 | Review redundant branch refs separately from registrations and protect every unique or unmapped commit. | `Planned` |
| 4 | Verify terminal repository integrity and record deferred retained resources. | `Planned` |

## Blockers

- `none`

## Re-Plan Triggers

- A supposedly missing worktree path exists, is locked, is dirty, or has an
  owner not represented by current evidence.
- A branch contains unique commits or lacks explicit accepted-replacement
  lineage.
- Cleanup requires force, history rewrite, remote mutation, or deletion outside
  an accepted exact resource set.
- Current Git state changes after a cleanup batch is admitted.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Planned`
