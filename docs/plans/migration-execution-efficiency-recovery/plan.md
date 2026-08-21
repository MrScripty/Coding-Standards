# Plan: Migration Execution Efficiency Recovery

**Plan status:** `Accepted`

**Current phase:** Accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Accepted base:** `28da602e078043d56dff37c0c44f46bfa7ad8424`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Reduce the cost, churn, and resource leakage of the remaining Bash-verifier
migration without weakening exact ownership, no-fallback replacement, focused
semantic evidence, serial shared-authority integration, or wave-boundary
acceptance.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Removing one unrelated checker does not renumber unaffected component identities. | `satisfied` | Migration-graph stability tests and regenerated node/component projections |
| A2 | Low-risk serial packages may be admitted and accepted coherently without a mandatory separate admission commit. | `satisfied` | [Migration execution modes](reports/migration-execution-modes.md) and verification-engine plan |
| A3 | Owner-coherent waves use focused member evidence and one mixed checkpoint at the actual wave or shared-contract boundary. | `satisfied` | [Migration execution modes](reports/migration-execution-modes.md) and parent plan |
| A4 | Task-created worktrees have a terminal registry postcondition without authorizing global or historical cleanup. | `satisfied` | Commit owner, prompt/template projections, and task-worktree terminal fixture |
| A5 | Historical branch/worktree cleanup, remote backup, and downstream pilots retain separate owners and authority. | `satisfied` | [Historical cleanup plan](../historical-git-resource-cleanup/plan.md), [backup risk](reports/backup-risk.md), and parent Milestone 8 |

## Scope

### In Scope

- Stable value semantics for the frozen temporary checker's component identity
  fields; columns and graph purpose remain unchanged.
- Verification-engine execution modes proportional to risk and concurrency.
- Focused member checks plus wave/shared-contract mixed checkpoints.
- Task-owned worktree terminal evidence and prompt/template projection.
- A non-destructive historical Git-resource cleanup plan and backup-risk report.

### Out Of Scope

- M6-I44 implementation or re-admission.
- Any later verifier package.
- Migration of the temporary Bash graph into the neutral graph engine.
- Bash graph schema expansion, semantic ownership inference, or AST parsing.
- Deleting branches, pruning historical worktree registrations, discarding
  commits, pushing refs, or running downstream pilots.
- Changes to generic Planning proportionality or concurrent-profile
  applicability, which already express the intended policy.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Recovery ownership | This plan serially owns shared generator, migration-procedure, Commit projection, and acceptance changes until accepted. |
| Component identity | Derive a deterministic component ID from the exact sorted canonical member set; declaration order and unrelated members cannot change it. |
| Frozen graph boundary | Preserve columns, edge discovery, component membership, wave calculation, and temporary deletion-lifecycle purpose. |
| Serial low-risk mode | Permit one admission-plus-implementation commit only when no proposal is outstanding, the owner and complete write set are current, no shared engine/schema/policy contract changes, and focused final-state evidence is available. |
| Pre-admitted mode | Retain separate admission when stale proposals, unresolved consumers, uncertain ownership, shared contracts, safety risk, or re-plan evidence require a stable intermediate decision. |
| Owner-wave mode | Group packages only when owner, dependency set, semantic contract, verification family, and integration order are compatible; run focused evidence per member and one mixed checkpoint at wave close. |
| Worktree evidence | Check only task-created paths at terminal acceptance. Historical or unknown resources require separate inventory and authority. |
| Backup and pilots | Record current risk and existing acceptance ownership; do not publish or claim pilot completion without separate execution authority. |

## Milestones

| Milestone | Goal | Exact write set | Verification | Status |
| --- | --- | --- | --- | --- |
| 1 | Make temporary component identities diff-stable. | `tools/standards_verifier/standards_verifier/migration_graph.py`; `tools/standards_verifier/tests/test_migration_graph.py`; `tools/standards_verifier/README.md`; generated checker node/component artifacts; this plan and ledger | focused graph tests; insertion/deletion stability probe; all verifier tests; generated freshness; complete checkpoint | `Accepted` |
| 2 | Make remaining package execution proportional. | verification-engine and parent active plans; this plan, ledger, issues, and execution-mode report | plan structure; package authority; all declarative suites; procedure scenario review | `Accepted` |
| 3 | Enforce task-owned worktree terminal evidence and separate historical cleanup. | Commit workflow and audited projections; Commit suite; policy-impact disposition report; historical cleanup plan; this plan, ledger, issues, and reports | policy-impact query; Commit and projection suites; graph/verifier tests; all declarative suites; complete checkpoint | `Accepted` |

## Current Evidence

- Canonical Planning already permits one coherent slice and does not require a
  separate commit cadence.
- Commit already makes isolation conditional and requires terminal cleanup.
- Current Git state has 385 worktree registrations: one live and 384 prunable;
  no destructive cleanup is authorized by this plan.
- Current local `main` is 736 commits ahead of `origin/main`; publication is
  not authorized by this plan.
- The temporary graph has 86 nodes and 86 singleton components, so ordinal
  component IDs rename unrelated rows after most checker deletions.
- M6-I44 remains admitted and blocked by VE086. It does not resume until this
  recovery is accepted and receives fresh re-admission evidence.

## Blockers

- `none`

## Re-Plan Triggers

- Stable component identity requires changing graph columns or accepted edge
  semantics rather than only value identity.
- A current consumer treats ordinal component IDs as canonical authority.
- Combined serial acceptance cannot preserve exact package, edge, source, and
  mutation evidence.
- Wave batching combines different owners, dependency sets, semantic outcomes,
  or unresolved consumer transitions.
- Worktree terminal enforcement requires global pruning, a stored mutable
  registration count, or destructive automation.
- Any milestone would resume M6-I44 or alter a later package before recovery
  acceptance.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: remote backup authorization; historical cleanup
  execution; two independent downstream pilots
- Final status: `Accepted`
