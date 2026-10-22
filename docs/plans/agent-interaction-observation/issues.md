# Issues

## O-I1 — Existing mutable standards evidence prevents current-tree qualification

- Severity: known external verification finding; nonblocking for O1 by explicit user disposition.
- Evidence: `test_purpose_projection.PurposeProjectionTest.setUpClass` raises `ANALYSIS.EVIDENCE_DIGEST_MISMATCH` while compiling existing coverage evidence, before the observation transport test starts. A diagnostic probe retaining the original exception identified `docs/plans/standards-library-effectiveness/plan.md` as the first mismatched evidence reference. The original worktree already contained Router/Security/Concurrency and coverage/evaluation changes at O1 admission.
- Owner: existing standards-maintenance work; its evidence owner must reconcile changed source and retained coverage receipts through their authorized publication path.
- Boundary: standards coverage authority, outside observation's allowed write set.
- Disposition: preserve changes; qualify an isolated candidate from baseline `149ba317e9397519bc181a048ecf76aef129a69c` with only O1 source applied. This proves candidate behavior but does not accept the combined dirty worktree.
- Current-tree recheck: canonical suite-input regeneration and freshness passed. The complete verifier exited 2 with 73 selected suites, 72 passed and 1 failed (`policy-semantic-impact`, `ANALYSIS.EVIDENCE_DIGEST_MISMATCH`); retained log `/tmp/observation-original-complete.log`.
- User disposition (2026-10-01): “that doesnt matter”. The finding does not block O1 acceptance; accept the verified isolated observation source and preserve the failed combined-tree result.
- Verification/revisit: after the owning work reconciles its evidence, run the complete locked workflow and verifier on the combined candidate. No receipt rewriting, evidence deletion or domain migration is authorized by O1.

## O-I2 — publication fixture inherited now-approved baseline content

- Severity: required verification gate obstruction; baseline reproduction confirmed.
- Evidence: candidate `/tmp/observation-candidate-process-reuse.log` and clean baseline `/tmp/observation-baseline-process-reuse.log` both fail with `KeyError: code` at the same Security-content assertion.
- Owner: supporting publication fixture, consumed by the existing MCP runtime-cache qualification.
- Disposition: fix-now within the explicitly extended test-only write set; establish the fixture's empty approval precondition and retain its exact observable workflow assertions.
- Verification: both direct consumers passed (2 tests), independent fixture review found no material findings, and the final full Engine run passed all 625 tests. All 13 locked workflow groups (1,255 tests) and all 73 registered verifier suites passed on the isolated source.
- Final disposition: resolved; no weakened assertions or production changes.
