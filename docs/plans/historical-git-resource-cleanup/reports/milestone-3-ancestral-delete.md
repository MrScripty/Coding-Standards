# Milestone 3 Ancestral Branch Cleanup

## Authorized Batch

The accepted post-prune inventory identified exactly nine non-checked-out task
branches whose tips were already ancestors of `main`. Immediately before
mutation, each branch still resolved to its accepted tip and each tip remained
an ancestor of current `main`.

| Branch | Accepted tip |
| --- | --- |
| `codex/7.4b8s-row-6-decomposition` | `11c0acf2935fabb577b4f6a9fccf2d1742854b87` |
| `codex/7.4b8t-native-artifact-loading` | `1473f49845b2858b6d08f08629282758fbe8348b` |
| `codex/7.4b8u-native-artifact-release` | `7c60fcab9e9d991e9e8adabbaae1d4354d66c0bf` |
| `codex/7.4b8v-platform-evidence` | `ca622cc12fcd3fe6ebebdaa12d8f150c3573a22c` |
| `codex/git-branch-lifecycle-policy` | `55f42c03cb6d94ef770fc64a9907ae99991276be` |
| `codex/standards-7.4b8i` | `5b7adab6a1f054128b4683afc2cb0c79273edd6e` |
| `codex/standards-7.4b8j` | `3a870ba8890701ca614bb4f91139e4970f327d60` |
| `codex/standards-7.4b8k` | `4b4329f3f53c78aad6d67bb20890b42d9a63db5e` |
| `codex/ve057-impl` | `454d80461fa937d969e03b506349bfef5d73c2ec` |

## Result

The refs were deleted using non-force `git branch -d`. The operation removed
branch names only; it did not rewrite history, mutate remotes, remove filesystem
worktrees, or discard commits not already reachable from `main`.

Postconditions:

- local branches: 128;
- deleted refs: exactly the nine authorized names;
- worktree registrations: 1;
- prunable registrations: 0;
- remaining divergent patch-equivalent branches: 115;
- remaining branches with unique commits: 12;
- repository integrity: `git fsck --no-dangling` passed;
- repository worktree: clean before evidence updates.

The [post-deletion inventory](../inventories/branches-post-ancestral-delete.tsv)
is the current mapping-review input. It does not authorize deleting a
patch-equivalent branch without explicit source-to-accepted lineage, and it
does not authorize deleting any branch with unique commits.

## Verification

- cleanup-plan structure check: passed;
- report and plan link targets: present;
- exact deleted-ref absence: passed for all nine names;
- branch and worktree inventory regeneration: passed;
- `git fsck --no-dangling`: passed;
- `git diff --check`: passed before staging.
