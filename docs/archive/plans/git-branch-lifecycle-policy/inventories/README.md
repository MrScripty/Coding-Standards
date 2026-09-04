# Git Resource Inventory

The inventory is a read-only snapshot of local Git state at accepted base
`9c8e1f46b919a8c62361f7261d5e93f256f3a18e` after creation of the governed task
branch and worktree.

- [branches.tsv](branches.tsv) contains all 137 local branches: 10 ancestral to
  `main`, 115 divergent but patch-equivalent, and 12 with unique commits.
- [worktrees.tsv](worktrees.tsv) contains all 353 registrations: 298 prunable
  missing paths and 55 existing paths, of which 44 are clean and 11 dirty.
- [cleanup-dispositions.tsv](../reports/cleanup-dispositions.tsv) gives every
  resource one non-destructive recommendation requiring separate authority.

`ancestral` means Git can reach the branch tip from `main`. `patch-equivalent`
means `git cherry main <branch>` reports every divergent commit as equivalent;
it does not itself prove accepted lineage or authorize deletion. `unique` means
at least one divergent patch has no equivalent on `main`. Registered checked-out
state includes prunable registrations until Git administration is explicitly
pruned. No branch name is treated as a long-lived contract; only recorded
purpose metadata qualifies.
