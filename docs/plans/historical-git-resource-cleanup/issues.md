# Historical Git Resource Cleanup Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| GRC001 | Resolved by Milestone 2 | High | Current Git administration reported 385 worktree registrations, of which 384 were missing and unlocked. | Exact administrative prune completed; one live `main` worktree and zero stale registrations remain, with all non-main branch tips unchanged. |
| GRC002 | Resolved by review | High | The accepted lifecycle inventory found 12 branches with unique commits and 115 patch-equivalent but non-ancestral branches. | The 115 mapped redundant refs are retired; all 12 unique proposals are reviewed and classified as superseded by later accepted transitions. |
| GRC003 | Resolved by mapped-ref re-plan | High | Removing a mapped divergent branch requires forced ref deletion even though every source commit has one reviewed accepted replacement. | Permit `git branch -D` only for the exact accepted mapped-redundant set after all lineage, tip, checkout, publication, and uniqueness preconditions are revalidated; unique and unmapped branches remain prohibited. |
| GRC004 | Resolved by permanent retirement | High | The 12 remaining superseded branches were the last refs reaching 12 unique, unaccepted proposal commits. | Exact preconditions were revalidated and all 12 refs were permanently retired without archive refs; accepted successors and durable evidence own the useful outcomes. |
