# Milestone 2 Stale-Registration Prune

## Retrospective Correction

This milestone is not accepted as originally reported. Missing paths, unlocked
registrations, and unchanged branch refs did not prove that detached heads
would remain reachable after their worktree registration was pruned. A stale
registration can itself be the only administrative reachability root.

The reported `git fsck --no-dangling` result established object integrity while
suppressing dangling-object output. It was not a before/after reachability
comparison. Current reconciliation uses an explicit protected-OID set instead.

## Authorized Batch

The accepted candidate table named 384 worktree registrations. Immediately
before mutation, every candidate path was still missing, every registration
was still reported prunable, and none was locked. The only live worktree was
the canonical clean `main` worktree and was outside the batch.

## Result

`git worktree prune --verbose` removed exactly the stale administrative
registrations. It did not remove filesystem paths or branch refs.

Postconditions:

- worktree registrations: 1;
- prunable registrations: 0;
- retained worktree: canonical repository path on `main`;
- non-main branch refs and tips: all 136 unchanged;
- local branches: 137;
- repository object integrity: the historical `git fsck --no-dangling` command
  passed but did not establish continued reachability;
- repository worktree: clean before evidence updates.

The post-prune branch inventory was the Milestone 3 review input. It did not
authorize deletion of patch-equivalent or unique branches and did not account
for detached heads whose only root was the removed registration. Milestone 2
remains in reconciliation until every reconstructed head has an accepted commit
disposition and verified protection.
