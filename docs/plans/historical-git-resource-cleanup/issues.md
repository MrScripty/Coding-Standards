# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Open | High | Current Git administration reports 385 worktree registrations, of which 384 are prunable. | Refresh exact facts after plan start; do not prune from this historical count. |
| GRC002 | Open | High | The accepted lifecycle inventory found branches with unique and patch-equivalent but non-ancestral commits. | Preserve every ref until current reachability, ownership, replacement lineage, and terminal disposition are reviewed. |
