# Migration Execution Efficiency Recovery Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| MER001 | Resolved by Milestone 1 | Medium | Ordinal component IDs rename unrelated generated node and component rows after checker retirement. | Component IDs now derive from exact sorted canonical members without changing the frozen graph schema or purpose; insertion/removal stability tests and the complete checkpoint pass. |
| MER002 | Resolved by Milestone 2 | Medium | Remaining low-risk serial checker packages still commonly use separate admission and acceptance commits plus per-package mixed checkpoints. | Verification migration now selects one of four fact-driven execution modes; low-risk serial work needs no separate admission commit, and mixed checkpoints occur at owner-wave, shared-contract, or zero-Bash boundaries. |
| MER003 | Resolved by Milestone 3 and separate cleanup | Medium | Commit policy requires worktree cleanup, but task execution left 384 prunable registrations. | Commit requires exact task-created registry evidence; the separately accepted historical cleanup leaves one canonical worktree and zero stale registrations. |
| MER004 | Resolved by authorized fast-forward backup | High | Local `main` had hundreds of commits not represented by `origin/main`. | [Backup resolution](reports/backup-risk.md) records the authorized normal push and live verification that remote `main` reached accepted cleanup revision `9cdda3de` without force or divergence. |
| MER005 | Deferred to parent Milestone 8 | Medium | Independent downstream effectiveness remains unproved. | Preserve the two-pilot acceptance requirement; do not mix pilot execution into verifier retirement. |
