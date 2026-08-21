# Commit Reachability Consumer Audit

The accepted `policy-impact` query for `workflow.commit` returned 15 semantic
consumers. The path alias `workflows/commit.md` returned the same edge IDs and
canonical endpoints. No edge was inferred from a link, name, owner field, or
lexical similarity.

| Consumer | Disposition | Reason or evidence |
| --- | --- | --- |
| `evaluation/standards-effectiveness/fixtures/commit/authority.tsv` | `reviewed-no-change` | Staged review and history-rewrite authority do not decide worktree head reachability. |
| `evaluation/standards-effectiveness/fixtures/commit/branch-lifecycle.tsv` | `updated` | Adds head reachability, commit disposition, and explicit removed, archived, retained, discard, and refusal outcomes. |
| `profiles/workflows/concurrent-plan-integration.md` | `updated` | Cleanup handoff now carries Commit's reachability and disposition evidence. |
| `evaluation/standards-effectiveness/suites/commit-consolidation-dispositions.toml` | `updated` | Enforces the new inputs, outcomes, negative cases, and projections. |
| `evaluation/standards-effectiveness/README.md` | `updated` | Documents reachability-aware Commit fixture coverage. |
| `evaluation/standards-effectiveness/fixtures/commit/hook-bypass.tsv` | `reviewed-no-change` | Hook bypass authority is independent of cleanup reachability. |
| `prompts/implement-plan.md` | `updated` | Requires bounded protected-OID evidence for task-created worktree cleanup. |
| `workflows/implementation.md` | `reviewed-no-change` | It delegates cleanup and terminal lifecycle to Commit without restating the defective mechanism. |
| `templates/PLAN-TEMPLATE.md` | `updated` | Optional isolation evidence now records head OID and commit disposition when removal is authorized. |
| `prompts/planning.md` | `updated` | Cleanup planning no longer treats stale registration state as sufficient. |
| `workflows/planning.md` | `updated` | Written plans record reachability facts only when cleanup is in scope. |
| `reference/recipes/commits.md` | `updated` | Adds the non-normative executable protected-OID verification example. |
| `workflows/release.md` | `reviewed-no-change` | Release owns maintenance behavior; retained-branch lifecycle continues to delegate to Commit. |
| `STANDARDS-ROUTER.md` | `reviewed-no-change` | Existing applicability already routes branch/worktree lifecycle assessment and cleanup to Commit. |
| `evaluation/standards-effectiveness/fixtures/commit/task-worktree-terminal.tsv` | `updated` | Replaces ambiguous removal acceptance with reachable, archived, retained, authorized-discard, and refusal outcomes. |

The policy-impact manifest metadata for changed consumers was updated without
adding or inferring edges. Bounded manual review also found these non-graph
execution and historical evidence surfaces:

| Surface | Disposition | Reason or evidence |
| --- | --- | --- |
| `docs/plans/historical-git-resource-cleanup/plan.md` | `updated` | Reopens invalid acceptance and replaces conflicting objective, scope, criteria, and milestone state. |
| `docs/plans/historical-git-resource-cleanup/reports/final-acceptance.md` | `updated` | Replaces false terminal acceptance with reachability reconciliation status. |
| `docs/plans/historical-git-resource-cleanup/reports/milestone-2-prune.md` | `updated` | Corrects the meaning of `git fsck --no-dangling`. |
| `tools/standards_verifier/README.md` | `updated` | Documents the reusable Git reachability verifier contract. |
| Migration execution-mode report and active plans | `updated` | Adds a cumulative-risk checkpoint trigger, pauses migration through recovery acceptance, and resumes at a fresh graph audit without preselection. |

The semantic graph cannot prove that a plan is internally consistent or that a
Git object remains reachable. Those checks remain respectively a planning
consistency review and executable Git-state evidence.
