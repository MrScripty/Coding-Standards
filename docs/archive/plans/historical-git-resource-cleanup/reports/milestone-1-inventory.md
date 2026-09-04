# Milestone 1 Inventory Acceptance

## Current Facts

| Resource | Total | Classification |
| --- | ---: | --- |
| Worktree registrations | 385 | 1 live and retained; 384 missing, unlocked, and candidate-prunable |
| Local branches | 137 | 1 integration branch; 3 immediately unassociated ancestral candidates; 133 held by stale registrations |
| Branch ancestry | 137 | 10 ancestral; 127 divergent |
| Divergent branch patches | 127 | 115 patch-equivalent; 12 with unique commits |

## Accepted Mutation Boundary

Milestone 2 may run Git's administrative prune only against the state captured
by `stale-registration-candidates.tsv`. Before mutation, all 384 records must
still be reported prunable, missing, and unlocked. Any changed path or lock
state invalidates the batch.

The batch may not remove a filesystem path, branch ref, tag, remote ref, or
commit. Acceptance requires:

- one live `main` worktree remains at the canonical repository path;
- no stale registration remains;
- all 137 local branch refs retain their exact pre-prune tips; and
- protected commit reachability is unchanged.
