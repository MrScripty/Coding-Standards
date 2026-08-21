# Historical Git Resource Cleanup Ledger

No cleanup operation is admitted or executed. Plan creation records only the
accepted base and the requirement for a fresh read-only inventory after an
explicit `start` operation.

## 2026-08-21 - Start And Milestone 1 Acceptance

- Operation: `start` at accepted clean revision
  `8cce95b27220faa3ed115542c7242464d04df225`.
- Refreshed all 137 local branches and 385 registered worktrees from Git rather
  than reusing the historical lifecycle-policy snapshot.
- Classified one live clean integration worktree and 384 missing, unlocked,
  prunable registrations. The exact candidate table contains those 384 paths
  and no live path.
- Ten branch tips are ancestral to `main`; 115 divergent branches are
  patch-equivalent; 12 contain unique commits. Stale registrations still mark
  133 branches as checked out, so no branch deletion is admitted yet.
- Milestone 1 is accepted as read-only evidence. Milestone 2 may prune only
  the exact registration candidates; branch refs and commits remain protected.

## 2026-08-21 - Milestone 2 Acceptance

- Confirmed the dry-run prune set matched the accepted 384 missing, unlocked
  registration candidates; no live path or locked record was eligible.
- Ran Git's administrative worktree prune. No filesystem path, branch ref,
  tag, remote ref, or commit was removed.
- Post-prune evidence contains one live clean `main` worktree and zero stale
  registrations. All 136 non-main branch names and tips match pre-prune
  evidence exactly; `main` moved only through the Milestone 1 evidence commit.
- `git fsck --no-dangling` and clean-status checks pass. Milestone 2 is
  accepted.
- Branch review now exposes nine ancestral deletion candidates, 115 divergent
  patch-equivalent mapping candidates, and 12 branches with unique commits.

## 2026-08-21 - Milestone 3 Ancestral Branch Batch

- Revalidated the exact nine admitted branch names and tips against the
  accepted post-prune inventory immediately before mutation.
- Confirmed every admitted tip was an ancestor of current `main`, no admitted
  branch was checked out, and no additional ref was in the command write set.
- Deleted the nine refs with non-force `git branch -d`; no force deletion,
  commit rewrite, remote mutation, or filesystem worktree removal occurred.
- Post-mutation evidence records 128 local branches: `main`, 115 divergent
  patch-equivalent branches awaiting replacement-lineage review, and 12
  branches with unique commits retained for explicit review.
- One live worktree, zero prunable registrations, clean status, and
  `git fsck --no-dangling` passed. Milestone 3 remains active because
  patch-equivalent and unique branch terminal dispositions are unresolved.

## 2026-08-21 - Milestone 3 Replacement-Lineage Review

- Reconstructed explicit lineage for all 127 remaining non-main branches
  without mutating refs or commits.
- All 118 source commits across 115 patch-equivalent branches resolve by stable
  patch identity to exactly one accepted `main` commit. Their semantic commit
  subjects also agree: 117 exactly and one by accepted-subject prefix.
- Recorded each source branch, source tip, source commit, accepted replacement,
  mapping cardinality, semantic-subject relation, reconstructed-lineage mode,
  and verification classification in durable TSV evidence.
- The 12 unique proposal branches each retain one unmapped commit and remain
  protected for separate ownership and terminal review.
- The mapped branches are not Git ancestors of `main`; physical ref deletion
  therefore requires `git branch -D`. Because the active plan names force as a
  re-plan trigger, no mapped branch deletion is admitted.

## 2026-08-21 - Mapped Redundant-Ref Re-Plan

- Operation: `continue` from clean accepted revision
  `481d8547d11c9910cb137e5a293f1bfade61547b`.
- Accepted a narrow distinction between forced removal of an evidence-backed
  redundant local ref and prohibited force deletion that could discard unique,
  shared, published, checked-out, unknown, or unmapped history.
- Admitted only the 115 `candidate-delete-mapped` rows in the accepted lineage
  inventory. Each current tip must match, every source commit must retain one
  reviewed accepted replacement, and no upstream or remote branch may exist.
- The 12 `retain-lineage-review` branches remain outside the write set and keep
  full protection for their unique commits.

## 2026-08-21 - Milestone 3 Mapped Ref Retirement

- Regenerated lineage against current `main` and obtained byte-for-byte
  agreement with both accepted lineage artifacts before mutation.
- Revalidated all 115 exact branch tips, 118 unique accepted replacements,
  semantic-subject relations, zero ambiguous or unmapped source commits, zero
  merge commits, absent upstreams, absent matching origin refs, and a sole
  checked-out `main` worktree.
- Removed exactly the 115 admitted redundant local refs with `git branch -D`.
  No unique branch, remote ref, tag, commit, or worktree was included.
- Post-deletion evidence records 13 local branches: `main` and the 12 protected
  unique proposals. One live worktree, zero prunable registrations, clean
  status, and `git fsck --no-dangling` pass.
- Milestone 3 is accepted. Milestone 4 may inspect the 12 unique proposals but
  has no authority to delete or rewrite them.

## 2026-08-21 - Milestone 4 Unique Proposal Review

- Inspected the exact 12 retained branches and their one unique commit each
  without mutating refs, commits, remotes, tags, or worktrees.
- Every proposal added one declarative verifier suite and removed its matching
  Bash checker. For every proposal, current accepted `main` contains exactly
  one later commit that owns both artifact transitions.
- Confirmed all 12 current suites exist and are registered, all 12 proposed
  Bash checkers are absent, and every superseding commit is reachable from
  `main`.
- Classified all 12 proposal branches as `superseded`, not integrated: their
  exact unique patches were never accepted and must not be relabeled as
  replacement lineage.
- Permanent retirement would discard the last branch refs reaching those 12
  unique commits. The required exact destructive authority is a re-plan
  trigger, so all refs remain present.
