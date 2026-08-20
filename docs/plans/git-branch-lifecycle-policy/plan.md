# Plan: Git Branch And Worktree Lifecycle Policy

**Plan status:** `Accepted`

**Current phase:** Accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `9c8e1f46b919a8c62361f7261d5e93f256f3a18e`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Define proportionate branch and worktree applicability, least-transforming
integration selection, durable cherry-pick lineage, terminal resource
lifecycle, and bounded cleanup authority without making isolation or
cherry-pick universal. Demonstrate the policy through one task branch and
worktree integrated by fast-forward from an unchanged accepted base.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Commit owns ordinary branch selection, integration, lineage, terminal lifecycle, worktree cleanup, and durable evidence; Planning and the concurrent profile retain bounded specializations. | `contract` | repository | `review` | `satisfied` | Policy and exact [consumer audit](reports/consumer-audit.tsv) |
| A2 | Required positive and negative scenarios independently produce isolation, integration, terminal, lineage, and cleanup outcomes without age, count, force, ancestry, or cherry-pick fallback. | `focused` | repository | `automated` | `satisfied` | [Verification report](reports/verification.md) |
| A3 | Commit has audited policy-impact coverage, and logical/path aliases return the same exact consumers. | `integration` | repository | `automated` | `satisfied` | [Verification report](reports/verification.md) |
| A4 | Every current local branch and worktree has a non-destructive classification and later cleanup recommendation; no resource is deleted or rewritten. | `inventory` | repository | `automated-review` | `satisfied` | [Branch inventory](inventories/branches.tsv), [worktree inventory](inventories/worktrees.tsv), and [cleanup report](reports/cleanup-dispositions.tsv) |
| A5 | All focused, Python, declarative, generated, plan/link, and complete repository gates pass. | `complete` | repository | `automated` | `satisfied` | [Verification report](reports/verification.md) |
| A6 | The accepted task branch is fast-forwarded to unchanged `main`, and its clean worktree/branch receive an explicit terminal disposition. | `integration` | repository | `manual` | `satisfied` | [Verification report](reports/verification.md) and Git revision `55f42c03cb6d94ef770fc64a9907ae99991276be` |

## Scope

### In Scope

- Canonical Commit branch/worktree policy and bounded Planning, Implementation,
  concurrent-integration, Router, prompt, template, recipe, fixture, suite, and
  policy-impact projections.
- One multi-output decision fixture covering required lifecycle scenarios
  without ordered-rule masking.
- Exact current branch/worktree inventories and cleanup recommendations.
- Policy-impact support for explicit non-normative reference projections.
- One task branch/worktree and fast-forward integration demonstration.

### Out Of Scope

- Deleting branches, pruning registrations, removing worktrees, rewriting
  history, or discarding unique commits.
- M6-I17, verifier migration packages, temporary Bash graph schemas, generated
  migration topology, or checker retirement.
- A branch-management service, executable cleanup protocol, scheduler,
  arbitrary age/count thresholds, or automatic semantic inference.

## Constraints And Assumptions

### Constraints

- One serial integration owner controls all normative owners, Router, shared
  policy-impact authority, fixtures, suites, active plan, and final integration.
- Existing branch refs and worktrees are evidence inputs only; this task has no
  destructive cleanup authority.
- `main` must remain at the accepted base until fast-forward integration. A
  change makes this proposal stale and requires fresh admission.
- The temporary Bash graph and active verifier-migration authority remain
  unchanged.

### Assumptions

- Commit is the narrow existing owner for ordinary Git history and can own
  branch/worktree lifecycle without a standalone Git framework.
- The current registered Git state is sufficient for a bounded inventory;
  explicit long-lived purpose is present only when repository metadata records
  it.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Policy owner | `workflow.commit` owns ordinary branch applicability, integration mechanism, lineage, terminal state, cleanup authority, and durable evidence. | Existing history and rewrite ownership | Ad hoc worktree/cherry-pick convention |
| Specialization | Planning records isolation facts only for written plans; concurrent integration owns stale-capable proposal admission and cleanup handoff. | Existing owner boundaries | Universal plan or concurrency records |
| Mechanism | Select direct work, fast-forward, private rebase plus reverification, merge, or cherry-pick from accepted outcome and history value. | Least-transforming objective | Cherry-pick by default |
| Cleanup | Terminal evidence and ownership authorize only bounded predeclared cleanup; age/count trigger review only. | Safety objective | Ancestry, age, count, or force-delete authority |
| Impact | Audit Commit as a policy owner and model its real consumers explicitly, including non-normative reference projection. | Bounded manual audit | Link or metadata inference |
| Integration | Use one task branch/worktree, one coherent commit, and `git merge --ff-only` if `main` remains unchanged. | Task demonstration | Cherry-pick integration |

## Simplicity And Ownership Review

- Independent concepts: Git operational resources, plan state, concurrent
  proposal admission, release support contracts, and durable evidence.
- Intentional coupling: Planning and concurrent integration consume only their
  bounded Commit-owned branch decisions.
- Accidental coupling risk: treating worktree count as concurrency, ancestry as
  semantic acceptance, or branch refs as permanent evidence.
- Policy/state/lifecycle owners: Commit owns ordinary lifecycle; the integration
  owner owns task cleanup; resource owners retain unknown or unique state.
- Future changes that should remain independent: cleanup automation requires a
  separately justified executable contract and tests.

## Milestones

### Milestone 1: Branch And Worktree Lifecycle Policy

**Goal:** accept one coherent policy, all real projections, exact current
inventory, and a fast-forward lifecycle demonstration.

**Allowed write set:**

- `docs/plans/git-branch-lifecycle-policy/**`
- `CORE-STANDARDS.md` for the bounded code-branch terminology clarification
- `workflows/commit.md`
- `workflows/planning.md`
- `workflows/implementation.md`
- `profiles/workflows/concurrent-plan-integration.md`
- `workflows/release.md` only if audit evidence requires a normative correction
- `STANDARDS-ROUTER.md`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `reference/recipes/commits.md`
- `evaluation/standards-effectiveness/policy-semantic-impact.toml`
- `evaluation/standards-effectiveness/README.md`
- `evaluation/standards-effectiveness/fixtures/commit/**`
- `evaluation/standards-effectiveness/suites/commit-consolidation-dispositions.toml`
- `evaluation/standards-effectiveness/suites/plan-template-projection.toml`
- `tools/standards_verifier/standards_verifier/policy_impact.py`
- `tools/standards_verifier/tests/test_policy_impact.py`

**Tasks:**

- [x] Define proportionate applicability, branch context, least-transforming
  integration, cherry-pick lineage, terminal states, worktree lifecycle,
  cleanup authority, and durable evidence.
- [x] Update every audited projection and record exact dispositions.
- [x] Audit Commit policy impact and prove alias/owned-suite closure.
- [x] Add and pass required lifecycle decision scenarios.
- [x] Resolve accepted-review applicability, template-boundary, independent-
  outcome, documentation-impact, and code-branch terminology findings.
- [x] Correct fixture phase ordering so integration selection precedes
  replacement lineage and lifecycle-only work has no integration decision.
- [x] Integrate the completely verified policy by fast-forward and record the
  terminal resource disposition.

**Acceptance gate:** A1-A6 are satisfied, the staged write set is exact, no Git
resource is destructively cleaned, and canonical `main` is clean after
fast-forward integration.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- `main` or another shared authority changes before integration.
- Commit cannot own ordinary lifecycle without conflicting with an existing
  canonical owner.
- Policy-impact completeness requires inferred edges or dual authority.
- Acceptance requires destructive cleanup, history rewrite, M6 package work,
  or temporary Bash graph changes.
- A machine cleanup protocol becomes necessary for the requested semantic
  policy.

## Repository Isolation

One serial integration owner used
`codex/git-branch-lifecycle-policy` in `/tmp/cs-git-branch-lifecycle`, targeting
`main` at the accepted base. Expected terminal disposition is `integrated`,
followed by separately authorized removal of the clean task worktree and
redundant branch; no cleanup was performed as part of implementation. No
delegated or concurrent work occurred.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: authorized cleanup of inventoried resources
- Final status: `Accepted`
