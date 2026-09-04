# Current Git Resource Inventory

This read-only inventory was derived after explicit plan start at accepted
revision `8cce95b27220faa3ed115542c7242464d04df225`.

- `branches.tsv` contains all 137 local branches: 10 ancestral to `main`, 115
  divergent but patch-equivalent, and 12 with unique commits.
- `worktrees.tsv` contains all 385 registrations: one live clean integration
  worktree and 384 missing, unlocked, prunable registrations.
- `stale-registration-candidates.tsv` is the exact 384-row Milestone 2 mutation
  boundary. Every path is missing and every registration is unlocked.
- `worktrees-post-prune.tsv` contains the sole retained live `main` worktree.
- `branches-post-prune.tsv` proves all branch refs survived pruning and now
  classifies 9 ancestral deletion candidates, 115 patch-equivalent mapping
  candidates, and 12 unique-commit branches requiring preservation and review.

The inventories are evidence, not implicit deletion authority. In particular,
patch equivalence does not prove accepted replacement lineage, and the 133
branches associated with stale registrations remain protected until pruning
completes and branch facts are refreshed.
