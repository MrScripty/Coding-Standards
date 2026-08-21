# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Resolved by Milestone 2 | High | Current Git administration reported 385 worktree registrations, of which 384 were missing and unlocked. | Exact administrative prune completed; one live `main` worktree and zero stale registrations remain, with all non-main branch tips unchanged. |
| GRC002 | Open | High | The accepted lifecycle inventory found 12 branches with unique commits and 115 patch-equivalent but non-ancestral branches. | Preserve every remaining ref while reconstructing explicit source-to-accepted replacement mappings; patch equivalence alone does not authorize deletion. |
