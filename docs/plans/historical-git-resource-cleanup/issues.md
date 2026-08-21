# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Admitted for Milestone 2 | High | Current Git administration reports 385 worktree registrations, of which 384 are missing and unlocked. | Prune only the exact accepted candidate paths, then prove the sole live worktree remains and branch/commit refs are unchanged. |
| GRC002 | Open | High | The accepted lifecycle inventory found branches with unique and patch-equivalent but non-ancestral commits. | Preserve every ref until current reachability, ownership, replacement lineage, and terminal disposition are reviewed. |
