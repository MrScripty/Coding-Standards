# Milestone 3 Mapped Redundant-Ref Retirement

## Authorized Set

The accepted lineage inventory identified exactly 115 local branches whose
complete source history had one reviewed accepted replacement per source
commit. The narrow re-plan authorized forced ref deletion only for those
`candidate-delete-mapped` rows.

Immediately before mutation:

- the regenerated lineage artifacts matched accepted evidence byte for byte;
- all 115 branch tips matched their accepted identities;
- all 118 source commits retained exactly one accepted `main` replacement;
- all semantic-subject relations remained accepted;
- no source commit was ambiguous, unmapped, or a merge;
- no candidate had an upstream or matching `origin` ref;
- no candidate was checked out; and
- the canonical worktree was clean.

## Result

`git branch -D` removed exactly the 115 mapped redundant local refs. This used
Git's force flag because replacement commits are patch-equivalent rather than
ancestors of the source tips. It did not rewrite commits or mutate remote refs,
tags, worktrees, or the 12 branches containing unique commits.

Postconditions:

- local branches: 13;
- retained integration branch: `main`;
- retained unique proposal branches: 12;
- deleted mapped redundant refs: 115;
- worktree registrations: 1;
- prunable registrations: 0;
- repository integrity: `git fsck --no-dangling` passed;
- repository worktree: clean before evidence updates.

The [post-deletion inventory](../inventories/branches-post-mapped-delete.tsv)
contains only current retained branch authority. Historical source-to-accepted
lineage remains in the accepted mapping artifacts; redundant branch refs are
not retained as an evidence database.

## Verification

- exact mapped-ref absence: passed for all 115 accepted names;
- exact unique-tip preservation: passed for all 12 protected names;
- branch and worktree inventory regeneration: passed;
- `git fsck --no-dangling`: passed;
- cleanup-plan structure check: passed;
- `git diff --check`: passed.
