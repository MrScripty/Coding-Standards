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

Apply the bounded-local exclusion before the written-plan triggers. A change
with a clear objective, exact write set, regression check, and acceptance path
may proceed directly even when it touches a public, generated, persistence,
process, language, or user-interface boundary. State its write set inline; an
exact write set does not require a plan artifact.

Create a written plan when the change introduces material sequencing,
independently owned contract, migration, coordination, rollout, risk, or
acceptance complexity that must remain stable during implementation. A boundary
or file category alone does not satisfy this condition. Parallel work requires
a plan only when ownership, dependency, integration, or stale-state coordination
is material.

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
- objective acceptance claims;
- current acceptance status;
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

`Implemented` is not complete. `Accepted` requires every objective acceptance
claim to be satisfied.

Exactly one current phase is identified. Multiple independent milestones may be
implemented, but the active plan still names one next integration slice.

## Explicit Plan Admission

An implementation invocation that uses a written plan supplies one canonical
repository-relative `plan.md` path and one explicit operation. Do not discover
an active plan by scanning, recency, conventional location, conversation state,
or a repository-global pointer.

Planning owns these admission decisions:

- `start` accepts only `Planned` and transitions it to `Active`;
- `continue` accepts only `Active` without changing that state; and
- `verify` accepts `Implemented` or `Verifying`, transitioning `Implemented` to
  `Verifying` when objective verification begins.

`Blocked` and `Deferred` are `unavailable`; report the blocker or revisit
authority. `Accepted`, `Superseded`, and operation/state contradictions are
`invalid`. Missing plan identity, operation, lifecycle facts, or required linked
artifacts are `unavailable`. Security owns containment and traversal or symlink
escape rejection; unsupported filesystem representation routes conditionally
through Cross-Platform. Never infer the operation or treat a next slice as
execution authority.

## Concurrent Integration Routing

Ordinary planning does not require a revision digest, transition envelope, or
reconciliation identity. Apply the
[Concurrent Plan Integration profile](../profiles/workflows/concurrent-plan-integration.md)
only when two or more proposals may be prepared from the same mutable plan
revision before integration and correctness depends on detecting whether plan
or shared-authority state changed before a proposal is integrated.

Do not select the profile merely because several people or agents participate.
Serial collaboration, read-only investigations, non-authorizing reports,
independent work whose admission facts cannot become stale, and one integration
owner working from current state with no outstanding proposals remain under
this workflow alone.

When the profile applies, it owns proposal revision checks, stale-state
classification, compatibility, and reconciliation. This workflow continues to
own plan lifecycle and artifact boundaries. Shared authority remains a serial
integration-owner write in either case.

## Repository Isolation In Written Plans

A written plan does not require a branch or worktree by default. When material
review, concurrency, experimentation, release maintenance, risk containment,
or repository controls make isolation part of the accepted approach, record
the branch or worktree purpose, responsible owner, target branch, integration
owner, visibility or long-lived status, and expected terminal disposition.
Record an admitted base or revision only when stale-state coordination makes it
relevant.

Commit owns ordinary branch selection, integration mechanism, history, and
terminal cleanup. This workflow records only plan-level facts needed to keep
scope, ownership, sequencing, or acceptance stable. File count, commit count,
plan existence, delegation, and participant count do not independently require
repository isolation.

## Policy Projection Completeness

A normative change updates every affected distribution and enforcement surface.
Before changing an audited policy owner, query the neutral repository graph's
`policy-impact` edge group from the owner's logical ID or repository-path alias
and review every returned consumer. Audit and add explicit edges for a
previously uncovered owner before its next normative change. One registered
source declares each edge; the neutral graph engine derives bidirectional
indexes and exposes the same declaration from either endpoint without owning
policy semantics. Group membership does not copy an edge, domain validation
remains group-specific, and traversal requires explicit permission. The graph
manifest owns current semantic relations; a change report owns change-specific
dispositions. Do not infer missing semantic consumers from hyperlinks, lexical
similarity, routing prerequisites, suite ownership, or another graph; correct
the authoritative declaration explicitly.

When a rule prescribes a machine protocol, concrete representation, or
automated gate, its applicable prompts, templates, fixtures, and executable
support agree before the rule becomes mandatory. Do not require a template,
prompt, fixture, or executable mechanism for a semantic policy that does not
use that surface.

Diagnostic outcomes must remain semantically distinguishable. A manual process
may record classifications in prose or a table; a tool may use typed values.
Planning does not require one serialized diagnostic representation.

## Acceptance Claims

Follow [the verification workflow](verification.md). Record each required claim
with:

- stable identifier and observable criterion;
- evidence kind;
- required environment;
- execution mode;
- `pending`, `blocked`, or `satisfied` status; and
- evidence link when satisfied.

The plan-level acceptance status is:

| Status | Meaning |
| --- | --- |
| `pending` | No required claim is satisfied yet. |
| `partial` | Some claims are satisfied and at least one remains pending. |
| `blocked` | At least one required claim cannot currently be run. |
| `satisfied` | Every required claim is satisfied. |

Evidence kinds, environment requirements, and execution modes are independent.
Do not treat manual, environment-qualified, or artifact evidence as higher
positions in one hierarchy.

## Milestones And Slices

Order milestones by dependency. For each milestone record:

- one goal;
- one coherent implementation unit;
- exact allowed write set;
- semantics or contracts preserved/replaced;
- focused tests or fixtures;
- objective-relevant verification gate;
- re-plan conditions; and
- lifecycle state.

Select one coherent implementation unit. Split it only when separation
materially improves independent acceptance, risk containment, dependency
ordering, conflict isolation, rollback, or feedback. A bounded change that can
be understood and verified as a whole is one slice regardless of how many files
or layers it touches. Do not split work merely to minimize diff size or satisfy
a preferred commit cadence.

A written plan may contain one milestone and one implementation slice, and the
complete requested change may be that slice. Prefer thin vertical milestones
only when separation produces useful acceptance, risk reduction, or dependency
ordering. For cross-layer work that benefits from separation, prefer a real
vertical path before horizontal expansion. Do not substitute a headless path
when the objective is user-facing. File count, layer count, line count, and
commit cadence do not decide slice count.

## Current State, Not History

Keep `plan.md` concise and current:

- replace old binding decisions when re-planning;
- mark the old decision `Superseded` in the ledger or ADR history;
- move dated implementation detail and command output to the ledger/report;
- remove completed task narration when milestone state and evidence link are
  sufficient; and
- compact the plan when history obscures objective, blockers, or next slice.

Automated verification may inspect current plan structure and current authority.
It must not use accepted historical narration in an active plan as migration,
behavior, or lifecycle authority. Canonical package, disposition, lifecycle,
and evidence records own those claims; the ledger and reports retain history.
Perform this ownership review at completed-wave boundaries without using an
arbitrary line-count trigger.

Do not append a new interpretation beside an old active interpretation.

## Re-Planning

Stop and re-plan when:

- objective, authority, ownership, or constraints change;
- required facts invalidate a decision;
- a milestone misses its acceptance gate;
- compatibility, migration, security, data, or lifecycle risk changes;
- a directly affected file outside the stated write set changes objective,
  ownership, contract, risk, or acceptance scope;
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
outside their declared ownership. The serial integration owner may perform
predeclared terminal cleanup for clean branches and worktrees created by the
governed task after Commit-required terminal evidence is recorded. This does
not grant general destructive authority or permit force-removing unknown,
dirty, locked, user-owned, or uniquely committed resources.

## Completion

A plan is accepted only when:

- all non-deferred milestones are `Accepted` or `Superseded`;
- plan acceptance status is `satisfied`;
- every objective acceptance claim has matching evidence;
- unresolved follow-ups have owners and triggers;
- implementation files are resolved;
- the ledger contains final verification and commit summaries; and
- the active plan links to the final evidence.

After acceptance, retain the plan as a concise decision/result index. The
ledger and reports preserve history.
