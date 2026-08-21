# Historical Git Reachability Recovery Acceptance

## Outcome

The recovery is accepted. Exact recovery refs protect all 208 detached heads
reconstructed from the historical worktree inventory. The set includes all 147
heads that had no recorded branch-tip ancestor and all 11 confirmed unique
heads reported after pruning.

The historical cleanup plan is accepted only after reconciliation. Its prior
claim that `git fsck --no-dangling` proved continued reachability remains
invalid; the repaired terminal state is proven by the protected-OID manifest
and exact refs.

## Policy And Verification

- Commit policy now refuses worktree or registration cleanup unless the exact
  head is reachable from a retained ref, protected by a verified archive ref,
  or covered by explicit discard authority.
- Fixtures distinguish removed-reachable, removed-archived,
  retained-protected, discard-authorized, and refusal outcomes.
- The Python protected-OID verifier validates retained and archive refs without
  mutating repository state or falling back to object-integrity output.
- Migration policy now has a cumulative evidence trigger for the mixed
  checkpoint without restoring a per-package checkpoint cadence.

## Acceptance Evidence

- 208 protected commits verified against 208 exact recovery refs;
- 35 graph-engine tests passed;
- 341 standards-verifier tests passed;
- all 199 declarative suites passed;
- complete mixed checkpoint passed with 73 retained Bash checkers;
- Commit logical and path aliases returned the same 15 policy-impact edges;
- affected plan structure, links, generated freshness, and `git diff --check`
  passed.

No verifier package was selected or admitted. Recovery-ref retirement remains
separate future work requiring durable archive review and explicit authority.
