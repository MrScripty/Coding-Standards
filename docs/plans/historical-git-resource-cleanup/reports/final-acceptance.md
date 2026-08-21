# Historical Git Resource Cleanup Acceptance Reconciliation

## Acceptance Status

Accepted after explicit reachability reconciliation. The prior acceptance was
invalid because administrative pruning removed the only recorded reachability
root for 147 detached heads, including at least 11 heads already classified as
unique, without first proving an alternate root. That historical proof cannot
be reconstructed retroactively.

The defect is now contained and reconciled: exact recovery refs protect all
208 reconstructed detached heads, including all 147 registration-only heads,
and a reusable verifier checks the authoritative protected-OID manifest. This
acceptance does not restate the original prune as safe; it accepts the repaired
terminal state and the corrected authority.

## Final State

The cleanup produced this current operational state:

- local branches: 1;
- retained branch: `main`;
- worktree registrations: 1;
- retained worktree: the canonical repository worktree;
- prunable registrations: 0;
- retained historical task branches: 0.

The authoritative current snapshots are:

- [final branch inventory](../inventories/branches-final.tsv);
- [final worktree inventory](../inventories/worktrees-final.tsv).

## Accepted Cleanup Outcomes

| Resource class | Count | Outcome |
| --- | ---: | --- |
| Missing unlocked worktree registrations | 384 | Administratively pruned without filesystem deletion |
| Branch tips already ancestral to `main` | 9 | Retired with non-force deletion |
| Divergent branches with explicit accepted replacement lineage | 115 | Retired after exact mapped-ref authorization |
| Unique migration proposals superseded by accepted implementations | 12 | Permanently retired after exact destructive authority |

No dirty or live worktree was removed. No remote ref, tag, or commit history
was rewritten. However, pruning stale registrations removed administrative
reachability roots for detached commits before equivalent refs or archives were
established. That defect invalidates the prior reachability and acceptance
claims.

## Verification

- `main` is the sole local branch;
- the canonical worktree is the sole registered worktree;
- no registration is prunable;
- all 12 superseded proposal refs are absent;
- all accepted superseding commits remain ancestors of `main`;
- all 12 current declarative suites remain present and registered;
- all 12 replaced Bash checkers remain absent;
- the historical `git fsck --no-dangling` result proves object integrity only;
  it does not prove continued reachability and is not accepted as cleanup
  evidence;
- cleanup-plan structure passes;
- all report and inventory link targets exist;
- `git diff --check` passes.

The [historical Git reachability recovery](../../historical-git-reachability-recovery/plan.md)
accepted exact protected-OID evidence. Verifier migration may resume only from
a fresh graph audit; no package was selected from pre-recovery evidence.
