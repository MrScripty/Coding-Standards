# Planning Workflow

**Standards metadata**

- ID: `workflow.planning`
- Role: `workflow`
- Level: `MUST`
- Applies when: Work requires sequencing, shared decisions, migration, delegation, or acceptance across multiple boundaries.
- Does not apply when: A bounded local change has an obvious write set, regression check, and acceptance path.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Active-plan structure fixtures and objective-level acceptance review.
- Canonical owner: `workflows/planning.md`

## When A Written Plan Is Required

Create a written plan when any condition applies:

- multiple slices have ordering or migration dependencies;
- a change crosses process, language, persistence, generated, public, or
  user-interface boundaries;
- ownership, lifecycle, concurrency, rollout, or compatibility decisions must
  remain stable during implementation;
- required acceptance cannot be completed in the current environment;
- parallel workers need bounded write sets; or
- failure would create material security, data, release, or operational risk.

A small local change may use an inline checklist when objective, write set,
regression test, and acceptance are unambiguous.

## Artifact Model

Store a planned effort under one directory:

```text
docs/plans/<plan-slug>/
  plan.md
  execution-ledger.md
  issues.md
  reports/
```

- `plan.md` owns current objective, binding decisions, status, milestones,
  blockers, and exactly one next slice.
- `execution-ledger.md` owns dated slice, verification, deviation, and commit
  summaries.
- `issues.md` owns discovered issues and their dispositions.
- `reports/` owns investigations and detailed evidence.
- ADRs own durable architecture decisions that outlive the plan.

Do not duplicate the same decision in multiple active owners. Link instead.

## Required Active-Plan Fields

An active plan states:

- plan status;
- objective and scope;
- objective acceptance criterion and acceptance level;
- current evidence level;
- constraints and assumptions that affect decisions;
- binding decisions and owners;
- current phase;
- exactly one next slice or `none` for terminal status;
- milestones with goals, write sets, gates, and lifecycle states;
- blockers;
- re-plan triggers; and
- links to ledger, issues, reports, and ADRs.

Use [the plan template](../templates/PLAN-TEMPLATE.md).

## Lifecycle

| State | Meaning |
| --- | --- |
| `Planned` | Approved direction; implementation has not started. |
| `Active` | The current phase or slice is being implemented. |
| `Blocked` | A named dependency or required fact prevents progress. |
| `Implemented` | Source work is complete; objective acceptance is pending. |
| `Verifying` | Objective-level acceptance is running or awaiting environment. |
| `Accepted` | The named acceptance evidence passed. |
| `Deferred` | Work is intentionally excluded with owner and revisit trigger. |
| `Superseded` | A newer binding decision or plan replaces this item. |

`Implemented` is not complete. `Accepted` requires evidence at least as strong
as the objective's acceptance level.

Exactly one current phase is identified. Multiple independent milestones may be
implemented, but the active plan still names one next integration slice.

## Acceptance Levels

Until the verification taxonomy migration completes, plans use:

`focused`, `integration`, `contract`, `system`, `user-workflow`,
`environment`, `release`, or `manual`.

Name the level required by the objective, not the easiest available check.
Lower-level checks may reduce risk but cannot close a higher-level criterion.

## Milestones And Slices

Order milestones by dependency. For each milestone record:

- one goal;
- smallest useful vertical result;
- exact allowed write set;
- semantics or contracts preserved/replaced;
- focused tests or fixtures;
- objective-relevant verification gate;
- re-plan conditions; and
- lifecycle state.

For cross-layer work, prefer a thin real vertical path before horizontal
expansion. Do not substitute a headless path when the objective is user-facing.

## Current State, Not History

Keep `plan.md` concise and current:

- replace old binding decisions when re-planning;
- mark the old decision `Superseded` in the ledger or ADR history;
- move dated implementation detail and command output to the ledger/report;
- remove completed task narration when milestone state and evidence link are
  sufficient; and
- compact the plan when history obscures objective, blockers, or next slice.

Do not append a new interpretation beside an old active interpretation.

## Re-Planning

Stop and re-plan when:

- objective, authority, ownership, or constraints change;
- required facts invalidate a decision;
- a milestone misses its acceptance gate;
- compatibility, migration, security, data, or lifecycle risk changes;
- implementation requires files outside the approved write set;
- a lower-fidelity check was being used for a higher-fidelity objective; or
- a new dependency changes sequencing.

Re-planning must:

1. record the trigger and evidence in the ledger;
2. replace the binding decision in the active plan;
3. mark the prior decision or milestone `Superseded`;
4. update downstream milestones, gates, and next slice; and
5. obtain clarification when no standards-compliant decision is supported.

Do not preserve rejected behavior as a fallback unless a real contract requires
it and the routed contract guidance permits it.

## Findings

Record each discovered issue in `issues.md` with:

- ID, severity, and evidence;
- relationship to the objective;
- owner and affected boundary;
- fix-now, defer, or re-plan disposition;
- verification needed; and
- revisit trigger when deferred.

Fix an issue in the current slice only when it is inside the write set and
required for that slice's acceptance. Otherwise defer it explicitly.

## Concurrent Work

Delegate only independent work with non-overlapping primary write sets. Record:

- owner;
- primary and allowed-adjacent write sets;
- read-only context;
- forbidden/shared files;
- output and verification contract;
- report path;
- escalation rule; and
- serial integration order.

Core contracts, schemas, generated artifacts, lockfiles, shared fixtures,
workflow files, and active plans remain serial unless assigned to one explicit
owner.

Workers may not delete branches, worktrees, user changes, or shared history
without explicit authority.

## Completion

A plan is accepted only when:

- all non-deferred milestones are `Accepted` or `Superseded`;
- objective evidence meets the named level;
- unresolved follow-ups have owners and triggers;
- implementation files are resolved;
- the ledger contains final verification and commit summaries; and
- the active plan links to the final evidence.

After acceptance, retain the plan as a concise decision/result index. The
ledger and reports preserve history.
