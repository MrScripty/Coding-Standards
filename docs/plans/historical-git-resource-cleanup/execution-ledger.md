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
