# Coding-Standards CI efficiency: review and implementation plan

Start with [the implementation plan](plan.md). The [code review](reports/code-review.md) separates source findings, actual hosted measurements and local diagnostic evidence.

The `docs/plans/test-ci-efficiency/` subtree follows the repository's plan artifact structure. It contains the plan, execution ledger, issues, review, hosted baseline and local diagnostic reports. The ledger records M0 implementation on an isolated candidate. The 2026-10-22 cleanup found neither that temporary checkout nor its named branch in this repository; recover an exact candidate before resuming qualification. Historical reports and source identities are retained.

**Current status:** In Progress. **Exactly one next slice:** M0 — recover the recorded candidate, then obtain hosted timing artifacts and disposition the independent review. CI-A3 has historical focused candidate evidence; hosted timing, full candidate verification and final objective acceptance remain pending.

The complete hosted job log confirms Engine tests took 43m57.839s; review-evidence took only 4.501s. Start the performance investigation inside Engine rather than treating every audit finding as an equally important CI bottleneck.

Local diagnostic tests used Python 3.13.5 and a different dependency version, not CI's hash-locked Python 3.12 environment. They are diagnostic evidence only. The source bundle and full repository are not duplicated in this package.

The plan is admitted on an isolated candidate branch. Recheck the current branch/head and overlapping A1 work before integration; keep the existing plans index as a link to this plan.
