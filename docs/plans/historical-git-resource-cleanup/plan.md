# Plan: Historical Git Resource Cleanup

**Plan status:** `Accepted`

**Current phase:** Accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `f3488ee3df6861bec6adfc8951b60a66939cbc93`

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
| A1 | Every current worktree registration and local branch has one reviewed ownership and terminal disposition. | `satisfied` | Current inventory and [unique-proposal review](reports/milestone-4-unique-proposal-review.md) classify `main` as retained integration authority and all 12 proposals as superseded |
| A2 | Pruned registrations are proven missing, task-independent, unlocked, and free of a live or user-owned path before mutation. | `satisfied` | [Milestone 2 report](reports/milestone-2-prune.md) and post-prune worktree inventory |
| A3 | No branch with unique, shared, published, checked-out, unknown, or unmapped replacement history is deleted. | `satisfied` | [Ancestral cleanup](reports/milestone-3-ancestral-delete.md), [replacement-lineage review](reports/milestone-3-replacement-lineage.md), and [mapped-ref retirement](reports/milestone-3-mapped-ref-retirement.md) |
| A4 | Repository state and protected commit reachability are verified before and after every accepted cleanup batch. | `satisfied` | Milestone 2, Milestone 3, and [final acceptance](reports/final-acceptance.md) verification evidence |

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
| Mapped redundant refs | `git branch -D` is authorized only for the exact 115 `candidate-delete-mapped` rows accepted at `481d8547`: every tip must remain unchanged, every source commit must retain one accepted `main` replacement and semantic-subject agreement, and no branch may be checked out, published, shared, or contain unmapped history. This deletes redundant local refs; it does not authorize history rewrite or deletion of any unique branch. |
| Superseded unique proposals | Permanently retire only the exact 12 branches and commits in `unique-proposal-dispositions.tsv` after revalidating unchanged tips, `superseded` terminal state, accepted transition commits on `main`, current registered suites, absent replaced checkers, and no checkout, upstream, remote, tag, shared consumer, or long-lived purpose. The recovery outcome is permanent retirement without an archive ref because accepted implementations and durable review evidence own the useful outcome. |
| Batch size | Group only resources sharing ownership, disposition, risk, and verification contracts; preserve exact per-resource evidence. |
| Integration owner | One serial owner controls inventory, cleanup commands, acceptance evidence, and shared Git authority. |

## Milestones

| Milestone | Goal | Status |
| --- | --- | --- |
| 1 | Refresh read-only branch/worktree facts and exact dispositions. | `Accepted` |
| 2 | Execute an explicitly authorized stale-registration cleanup batch with before/after proof. | `Accepted` |
| 3 | Review redundant branch refs separately from registrations and protect every unique or unmapped commit. | `Accepted` |
| 4 | Verify terminal repository integrity and record deferred retained resources. | `Accepted` |

## Blockers

- `none`

## Re-Plan Triggers

- A supposedly missing worktree path exists, is locked, is dirty, or has an
  owner not represented by current evidence.
- A branch contains unique commits or lacks explicit accepted-replacement
  lineage.
- Forced ref deletion is requested outside the exact accepted mapped-redundant
  set, or any mapped-ref precondition no longer holds.
- Cleanup requires history rewrite, remote mutation, or deletion outside an
  accepted exact resource set.
- Current Git state changes after a cleanup batch is admitted.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: `none`
- Final status: `Accepted`
