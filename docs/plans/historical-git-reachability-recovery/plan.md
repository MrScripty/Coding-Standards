# Plan: Historical Git Reachability Recovery

**Plan status:** `Accepted`

**Current phase:** Accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `931a4616908bb4a87bc0527f0b4162389bf04987`

**Operation:** `start`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Recover commit reachability lost by historical worktree-registration pruning,
replace the contradictory cleanup acceptance with truthful authority, and make
future worktree cleanup refuse any mutation that lacks an explicit retained,
archived, or discard-authorized commit disposition.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Every detached head that relied only on a historical worktree registration is protected by an exact recovery ref or equivalent verified archive. | `satisfied` | [Protected-head inventory](inventories/protected-detached-heads.tsv), [protected OID manifest](inventories/protected-oids.tsv), and [reconciliation report](reports/reachability-reconciliation.md) |
| A2 | The historical cleanup plan and reports no longer claim that registration pruning preserved reachability or that contradictory unique-commit exclusions remained active. | `satisfied` | Reconciled plan, ledger, issues, and reports |
| A3 | Commit policy requires a retained ref, verified archive/recovery ref, or exact discard authority before pruning can remove a detached head's reachability root. | `satisfied` | Commit owner and exact audited projections |
| A4 | Decision fixtures distinguish head reachability, commit disposition, and explicit removed, retained, archived, refused, and discard-authorized outcomes. | `satisfied` | Commit fixtures and `commit-consolidation-dispositions` suite |
| A5 | Cleanup verification compares an explicit protected-OID set before and after mutation; object-integrity output is not treated as reachability proof. | `satisfied` | Reusable Python verifier, tests, and [reconciliation report](reports/reachability-reconciliation.md) |
| A6 | Migration remains paused until focused, declarative, Python, and mixed-checkpoint evidence accepts this shared-contract recovery. | `satisfied` | Parent plans, [execution ledger](execution-ledger.md), and [final acceptance](reports/final-acceptance.md) |

## Scope

### In Scope

- Recovery refs and exact evidence for detached historical worktree heads.
- Reconciliation of the historical cleanup plan's objective, scope, claims,
  milestones, ledger, issues, and reports.
- Commit worktree lifecycle policy and its audited semantic consumers.
- Reusable Python verification of protected commit OIDs against retained refs.
- A risk-based cumulative trigger for the migration mixed checkpoint.

### Out Of Scope

- `git gc`, `git prune`, aggressive maintenance, or deletion of recovery refs.
- Resuming or admitting another Bash-verifier migration package.
- Deleting branches, refs, worktrees, objects, or unique commits.
- Reconstructing historical branch contents beyond the evidence needed to
  protect and classify the recorded detached heads.
- General Git administration frameworks or inferred semantic relationships.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Emergency containment | Protect every detached head recorded in the pre-cleanup lifecycle inventory, including every registration-only head; broader protection is acceptable and may not be removed by this recovery. |
| Reachability authority | An explicit protected-OID set and exact retained or recovery refs prove preservation. `git fsck --no-dangling` proves neither continued reachability nor cleanup safety. |
| Terminal outcomes | Use explicit `removed-reachable`, `removed-archived`, `retained-protected`, `discard-authorized`, and refusal outcomes; registration state alone cannot authorize cleanup. |
| Safe default | Unknown ownership, reachability, commit disposition, or archive evidence produces a typed refusal or unavailable result without fallback. |
| Consumer audit | Use the accepted policy-impact graph for Commit, then manually review the bounded cleanup surfaces because semantic edges do not prove internal plan consistency or Git reachability. |
| Integration ownership | One serial owner controls recovery refs, active plans, Commit policy, shared verifier mechanics, suite authority, and acceptance state. |

## Milestones

| Milestone | Goal | Exact write set | Verification | Status |
| --- | --- | --- | --- | --- |
| 1 | Protect detached heads and reconcile historical cleanup authority. | `refs/recovery/historical-worktrees/*`; this plan directory; `docs/plans/historical-git-resource-cleanup/*`; parent active plans | exact protected-OID/ref comparison; plan structure; links; clean status | `Accepted` |
| 2 | Enforce reachability-aware worktree lifecycle and executable evidence. | `workflows/commit.md`; audited Commit projections; Commit fixtures and suite; smallest reusable Python Git-reachability tool and tests; migration execution-mode report; this plan and parent plans | focused tool tests; Commit and policy-impact suites; all Python tests; all declarative suites; generated freshness; complete mixed checkpoint; `git diff --check` | `Accepted` |

## Blockers

- `none`

## Re-Plan Triggers

- A recorded detached head no longer exists as a commit object.
- Recovery requires deleting, rewriting, or replacing an existing ref.
- The protected set cannot be reconstructed deterministically from accepted
  historical evidence.
- A Commit consumer outside the audited graph and bounded manual audit changes
  the normative write set materially.
- Reachability verification requires a domain-specific dependency in generic
  graph or verifier infrastructure.
- Acceptance would preserve contradictory cleanup claims, dual policy, or a
  fallback cleanup path.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: historical recovery-ref retirement requires separate authority after durable archive review
- Final status: `Accepted`
