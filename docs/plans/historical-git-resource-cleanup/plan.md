# Plan: Historical Git Resource Cleanup

**Plan status:** `Accepted`

**Current phase:** Accepted after reachability reconciliation

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `f3488ee3df6861bec6adfc8951b60a66939cbc93`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Classify local Git worktree registrations and branch refs, retire only exact
resource sets under separately accepted authority, preserve detached commit
reachability before removing an administrative root, and record any exact
authorized unique-commit retirement without treating age, count, ancestry, or
patch equivalence as deletion authority.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Every mutated resource set has an exact recorded outcome, and any unproven historical ownership or task-independence precondition is explicitly classified rather than retroactively accepted. | `satisfied` | Corrected Milestone 2 evidence and [reachability reconciliation](../historical-git-reachability-recovery/reports/reachability-reconciliation.md) |
| A2 | Every detached head whose worktree registration is removed remains reachable from a retained ref, is protected by a recovery/archive ref, or has exact discard authority. | `satisfied` | [Reachability recovery](../historical-git-reachability-recovery/plan.md) protects and verifies all 208 reconstructed detached heads |
| A3 | No unique, shared, published, checked-out, unknown, or unmapped commit is discarded except the exact 12 superseded proposal commits covered by recorded destructive authority. | `satisfied` | [Unique-proposal review](reports/milestone-4-unique-proposal-review.md), exact disposition table, and accepted retirement authority |
| A4 | Repository state and an explicit protected-OID set are compared before and after every accepted cleanup batch that can remove a reachability root. | `satisfied` | Prior evidence is explicitly rejected; the recovery manifest and reusable verifier prove every reconstructed detached head now has an exact recovery ref |

## Scope

### In Scope

- Read-only refresh of local branch and worktree inventories.
- Exact ownership, reachability, patch-equivalence, checked-out, lock, path,
  dirtiness, and unique-commit classifications.
- Separately accepted cleanup batches for unambiguous stale registrations or
  redundant refs.
- Before/after protected-OID, registry, and repository-integrity evidence.
- Exact destructive retirement of the 12 superseded proposal commits after
  separate authority named every branch and commit.

### Out Of Scope

- Cleanup during plan creation or without an explicit `start` operation.
- Force-removing dirty, locked, unknown, user-owned, or uniquely committed
  worktrees.
- Deleting any unique or unmapped branch history outside the exact separately
  authorized 12-commit superseded-proposal set, rewriting shared history, or
  inferring acceptance from ancestry or patch equivalence.
- Verifier migration, temporary Bash graph changes, remote publication, or
  downstream pilots.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Current authority | Refresh Git facts after `start`; the prior lifecycle-policy inventories are historical evidence, not current cleanup authority. |
| Safe default | Unknown or contradictory ownership, path, lock, reachability, mapping, or retained-purpose facts refuse cleanup. |
| Registration boundary | Administrative pruning and filesystem worktree removal are distinct operations with distinct evidence. |
| Detached-head boundary | A stale registration may be the only reachability root for its detached head. Before pruning, retain an existing ref, create and verify a recovery/archive ref, or record exact unique-commit discard authority. |
| Branch boundary | Ancestry and patch equivalence may trigger review but cannot authorize deletion without terminal ownership and replacement lineage. |
| Mapped redundant refs | `git branch -D` is authorized only for the exact 115 `candidate-delete-mapped` rows accepted at `481d8547`: every tip must remain unchanged, every source commit must retain one accepted `main` replacement and semantic-subject agreement, and no branch may be checked out, published, shared, or contain unmapped history. This deletes redundant local refs; it does not authorize history rewrite or deletion of any unique branch. |
| Superseded unique proposals | Permanently retire only the exact 12 branches and commits in `unique-proposal-dispositions.tsv` after revalidating unchanged tips, `superseded` terminal state, accepted transition commits on `main`, current registered suites, absent replaced checkers, and no checkout, upstream, remote, tag, shared consumer, or long-lived purpose. The recovery outcome is permanent retirement without an archive ref because accepted implementations and durable review evidence own the useful outcome. |
| Batch size | Group only resources sharing ownership, disposition, risk, and verification contracts; preserve exact per-resource evidence. |
| Integration owner | One serial owner controls inventory, cleanup commands, acceptance evidence, and shared Git authority. |

## Milestones

| Milestone | Goal | Status |
| --- | --- | --- |
| 1 | Refresh read-only branch/worktree facts and exact dispositions. | `Accepted` |
| 2 | Execute an explicitly authorized stale-registration cleanup batch and reconcile the missing historical reachability proof. | `Accepted` |
| 3 | Review redundant branch refs separately from registrations and protect every unique or unmapped commit. | `Accepted` |
| 4 | Verify terminal repository integrity, protected commit reachability, and deferred retained resources. | `Accepted` |

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

- Acceptance status: `satisfied` after explicit reachability reconciliation
- Deferred follow-ups: recovery-ref retirement requires separate authority
- Final status: `Accepted`
