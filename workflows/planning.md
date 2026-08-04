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

## Revision-Bound Transitions

`planning-admission-v1` identifies authoritative current plan state. Digest the
exact bytes of the selected `plan.md` and linked `issues.md` in canonical
repository-relative path order using explicit presence markers and
length-delimited path and content fields. Record the supported cryptographic
algorithm with the scheme. Do not normalize content or use Git identity,
timestamps, filesystem metadata, inferred paths, or the append-only ledger as
digest input.

Each proposal has a deterministic `planning-transition-v1` identity over its
scheme and algorithm, canonical plan path, explicit operation and actor, prior
admission identity, exact affected scope and bounded write set, canonically
ordered prerequisite transition identities, intended semantic outcome and plan
state, intended resulting admission identity, and verification contract. Empty
and absent values remain distinct. Actor identity records responsibility; it
does not confer plan, resource, or integration ownership.

Missing required identity facts are `unavailable`; malformed framing, ordering,
identity, scope, operation, or outcome is `invalid`; an unavailable supported
digest or conditional-update mechanism is `unsupported`. A changed admission
identity is stale `invalid`. Do not retry, merge, overwrite, or select latest
state automatically.

## Concurrent Preparation And Serial Integration

Transitions may be prepared or implemented concurrently only when their
admitted bases are current, prerequisites are satisfied, affected scopes and
write sets are compatible, semantic outcomes do not conflict, verification
contracts remain valid, and no shared-authority write overlaps. Disjoint files
alone do not prove compatibility. Return typed transition identities, affected
scopes, and failed invariants for stale, overlapping, contradictory,
under-specified, or dependency-blocked proposals.

One designated integration owner serially changes active plans, ledgers,
routers, shared contracts, lockfiles, generated artifacts, and other declared
shared authority. Compare `planning-admission-v1` immediately before mutation
or staging and again immediately before authoritative integration. Either
mismatch invalidates admission and requires a new decision from fresh state.
This is optimistic revision validation, not atomic multi-file replacement.

The coherent transition contains plan and issue changes, ledger evidence, the
operation, prior and resulting revisions, resulting state and next slice,
integration owner, and verification result. Recompute the resulting digest
after integration. State/evidence disagreement blocks normal admission.

The integration owner explicitly reconciles disagreement by selecting
`complete-transition`, `restore-prior-state`, or `supersede-transition` against
fresh current state and both revision gates. Reconciliation has a separate
deterministic identity referencing the failed transition, observed revisions,
selected remedy and authority, intended result, and verification contract. It
never reuses the failed admission or chooses from timestamps, file precedence,
or apparent completeness.

Do not introduce reservations, leases, queues, heartbeats, scheduling,
state-only commits, recovery journals, transaction managers, duplicate
execution, or persistent coordination lifecycle as generic fallback. Such a
mechanism requires measured downstream need and a separate plan.

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
- plan acceptance status is `satisfied`;
- every objective acceptance claim has matching evidence;
- unresolved follow-ups have owners and triggers;
- implementation files are resolved;
- the ledger contains final verification and commit summaries; and
- the active plan links to the final evidence.

After acceptance, retain the plan as a concise decision/result index. The
ledger and reports preserve history.
