# Historical Git Reachability Recovery Ledger

## 2026-08-21 - Start And Emergency Containment

- Operation: `start` at clean accepted revision
  `931a4616908bb4a87bc0527f0b4162389bf04987`.
- No verifier migration package was admitted after M6-I52.
- Verified all 11 reported detached OIDs still exist as commit objects.
- Reconstructed 208 distinct detached heads from the pre-cleanup worktree
  inventory. Exactly 147 were not reachable from any branch tip recorded in
  the corresponding pre-cleanup branch inventory.
- Created exact `refs/recovery/historical-worktrees/<short-oid>` refs for all
  208 detached heads. All 147 registration-only heads are now protected.
- No object maintenance, branch deletion, worktree mutation, history rewrite,
  or remote operation was performed.

## 2026-08-21 - Milestone 1 Acceptance

- Corrected reachability classification uses Git ancestry from every recorded
  pre-cleanup branch tip: 61 detached heads had a recorded ref ancestor and 147
  were registration-only.
- Verified all 208 exact recovery refs resolve to their recorded commit OIDs;
  the protected set includes all 11 confirmed unique registration-only heads.
- Reopened the historical cleanup plan, invalidated final acceptance, replaced
  conflicting objective/scope/criteria, and corrected the false Milestone 2
  and `git fsck --no-dangling` claims.
- Milestone 1 is accepted. Recovery refs remain protected operational state;
  their retirement is outside this plan.

## 2026-08-21 - Milestone 2 And Objective Acceptance

- Updated Commit and every changed audited projection to require an explicit
  reachable, archived, or discard-authorized commit disposition before
  worktree removal or registration pruning.
- Added reusable protected-OID verification and nine focused tests. Verified
  all 208 protected commits against exact recovery refs with zero discard
  authorizations.
- Verified logical and path Commit aliases return the same 15 policy-impact
  edges, and recorded an exact disposition for every reviewed consumer.
- Passed 35 graph-engine tests, 341 standards-verifier tests, all 199
  declarative suites, and the complete mixed checkpoint with 73 retained Bash
  checkers.
- Passed affected plan-structure checks, Markdown-link checks, generated
  freshness, and `git diff --check`.
- Accepted Milestone 2 and the recovery objective. No verifier package was
  selected or admitted; the parent plans resume at a fresh graph audit.
