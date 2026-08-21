# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Resolved by Milestone 2 | High | Current Git administration reported 385 worktree registrations, of which 384 were missing and unlocked. | Exact administrative prune completed; one live `main` worktree and zero stale registrations remain, with all non-main branch tips unchanged. |
| GRC002 | Partially resolved | High | The accepted lifecycle inventory found 12 branches with unique commits and 115 patch-equivalent but non-ancestral branches. | Explicit replacement lineage is now recorded for all 115 mapped branches; preserve the 12 unique branches pending separate review. |
| GRC003 | Re-plan required | High | Removing a mapped divergent branch requires forced ref deletion even though every source commit has one reviewed accepted replacement. | Do not delete the 115 refs until the plan distinguishes evidence-backed redundant-ref deletion from prohibited force removal that could discard unique or unknown history. |
