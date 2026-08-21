# Migration Execution Efficiency Recovery Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| MER001 | Resolved by Milestone 1 | Medium | Ordinal component IDs rename unrelated generated node and component rows after checker retirement. | Component IDs now derive from exact sorted canonical members without changing the frozen graph schema or purpose; insertion/removal stability tests and the complete checkpoint pass. |
| MER002 | Resolved by Milestone 2 | Medium | Remaining low-risk serial checker packages still commonly use separate admission and acceptance commits plus per-package mixed checkpoints. | Verification migration now selects one of four fact-driven execution modes; low-risk serial work needs no separate admission commit, and mixed checkpoints occur at owner-wave, shared-contract, or zero-Bash boundaries. |
| MER003 | Resolved by Milestone 3 | Medium | Commit policy requires worktree cleanup, but task execution has left 384 prunable registrations. | Commit now requires exact task-created registry evidence, and the separate historical cleanup plan remains `Planned` without mutation authority. |
| MER004 | Open; separate authority required | High | Local `main` has hundreds of commits not represented by the locally recorded `origin/main`. | [Backup risk](reports/backup-risk.md) records the exact accepted observation and requests separate publication or backup authority before migration resumes. |
| MER005 | Deferred to parent Milestone 8 | Medium | Independent downstream effectiveness remains unproved. | Preserve the two-pilot acceptance requirement; do not mix pilot execution into verifier retirement. |
