# Milestone 2 Stale-Registration Prune

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
- repository integrity: `git fsck --no-dangling` passed;
- repository worktree: clean before evidence updates.

The post-prune branch inventory is the current Milestone 3 review input. It
does not authorize deletion of patch-equivalent or unique branches.
