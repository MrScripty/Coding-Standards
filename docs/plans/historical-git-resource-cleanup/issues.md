# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Resolved by Milestone 2 | High | Current Git administration reported 385 worktree registrations, of which 384 were missing and unlocked. | Exact administrative prune completed; one live `main` worktree and zero stale registrations remain, with all non-main branch tips unchanged. |
| GRC002 | Partially resolved | High | The accepted lifecycle inventory found 12 branches with unique commits and 115 patch-equivalent but non-ancestral branches. | The 115 mapped redundant refs are retired with exact lineage evidence; preserve the 12 unique branches pending separate ownership and terminal review. |
| GRC003 | Resolved by mapped-ref re-plan | High | Removing a mapped divergent branch requires forced ref deletion even though every source commit has one reviewed accepted replacement. | Permit `git branch -D` only for the exact accepted mapped-redundant set after all lineage, tip, checkout, publication, and uniqueness preconditions are revalidated; unique and unmapped branches remain prohibited. |
