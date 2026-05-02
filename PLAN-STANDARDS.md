# Plan Standards

How to create and execute implementation plans without duplicating existing
commit, testing, tooling, or documentation rules.

## Purpose

Define a lightweight workflow for planning and executing work so changes are
clear, sequenced, and auditable.

## Scope

This document defines:
- How to write a plan
- How to execute a plan
- When to re-plan
- What completion summary to provide
- Optional use of subagents
- Worktree hygiene during plan execution
- Concurrent worker execution rules

This document does not redefine:
- Commit formatting/history rules (see `COMMIT-STANDARDS.md`)
- Verification/test rules (see `TESTING-STANDARDS.md`)
- CI/quality gates (see `TOOLING-STANDARDS.md`)
- README/ADR traceability rules (see `DOCUMENTATION-STANDARDS.md`)
- PR traceability sections (see `templates/PULL_REQUEST_TEMPLATE.md`)

If rules overlap, the specialized standard remains authoritative.

## When a Plan Is Required

Create a written plan for:
- Any change that spans multiple files/modules
- Any change with cross-layer impact
- Any change that needs staged rollout or risk controls

Small, single-step edits may use a brief inline plan (2-4 bullets).

## Plan Inputs

Before planning, capture:
- Problem statement
- Constraints
- Assumptions
- Dependencies
- Risks
- Affected structured contracts
- Affected persisted artifacts
- Concurrency/race-risk review when work touches async state, polling, restart
  logic, or overlapping/cancellable operations
- Definition of done

## Clarifying Questions

Ask clarifying questions only when missing information would materially affect
scope, sequencing, risk, or acceptance criteria.

Guidelines:
- Ask the smallest set of essential questions.
- Use assumptions when risk is low and state them explicitly.
- If unresolved uncertainty remains high-risk, pause execution until clarified.

## Required Plan Structure

Every plan must include:
- Objective
- Scope (in scope / out of scope)
- Milestones (ordered)
- Tasks per milestone
- Verification per milestone (reference existing test/tooling standards)
- Risks and mitigations
- Re-plan triggers
- Completion criteria

When applicable, plans must also include:
- Ownership and lifecycle note for polling, timers, retries, background tasks,
  or process management. State who starts work, who stops it, how cleanup or
  cancellation happens, and how overlap/restart races are prevented.
- Public facade preservation note for large refactors. Explicitly choose
  facade-first preservation or an API-breaking rewrite, and record the
  compatibility impact.
- Concurrent worker plan when work is intended to be delegated across
  subagents or parallel implementers. Include ownership slices, write sets,
  worker report paths, integration sequence, and cleanup requirements.

Use `templates/PLAN-TEMPLATE.md`.

Store project-level plan artifacts under the documentation artifact layout
defined in `DOCUMENTATION-STANDARDS.md`:
- General implementation plans belong under `docs/plans/<plan-slug>/`.
- Large refactor plans with pass findings, sub-agent instructions, coordination
  ledgers, or implementation wave reports belong under
  `docs/refactors/<refactor-slug>/`.

## Large Refactor Plans

Large refactor plans must treat findings as a combined constraint set, not as
isolated rule violations.

When a refactor spans many standards, modules, packages, or architectural
boundaries, the plan must include:
- Standards or requirement groups reviewed
- Findings grouped by affected code area
- Overlapping constraints and how they are resolved together
- Sequenced implementation steps
- Dependencies between steps
- Verification criteria per step or milestone
- Re-plan triggers
- Any unrelated issues discovered during analysis that will not be resolved by
  the refactor

When parallel implementation is expected, large refactor plans must also include
a phased worker execution plan:
- Ownership slices with non-overlapping primary write sets
- Allowed adjacent write sets
- Read-only context
- Forbidden/shared files
- Shared contracts, public interfaces, schemas, configs, global utilities,
  fixtures, generated files, lockfiles, and integration points that must be
  handled serially or by one explicit owner
- Worker report paths
- Coordination ledger path
- Integration sequence between worker waves
- Cleanup requirements for worker branches, worktrees, or temporary clones

Validate the full plan against all standards and findings until a complete pass
produces no new required plan changes.

## Recommendations

If a clearly better approach exists, include concise recommendations with:
- What to change
- Why it is better (risk, speed, maintainability, or simplicity)
- Impact on scope/timeline

Keep recommendations actionable and limited to meaningful alternatives.

## Execution Order

Execute in this order:
1. Confirm objective, constraints, and done criteria.
2. Sequence milestones by dependency order.
3. For cross-layer features, make the first implementation milestone the
   thinnest useful vertical slice unless dependencies make that impossible.
4. Implement one logical task at a time.
5. Verify each completed logical slice using applicable existing standards.
6. Update plan status after each milestone.
7. Re-plan immediately when triggers are hit.
8. Close with a completion summary against done criteria.

## Worktree Hygiene

Before plan implementation begins, inspect the git status.

Do not begin implementation when source code, tests, configs, build files,
lockfiles, generated files, or other implementation files are dirty unless the
user explicitly allows those changes to remain in place for the plan.

Dirty implementation files must be committed, stashed, reverted by the user, or
explicitly allowed before implementation begins. Do not revert unrelated user
changes without explicit permission.

Markdown plan or documentation files may be dirty when they are part of plan
setup or explicitly allowed.

During execution, do not begin the next logical step while dirty implementation
files from the previous step remain uncommitted or unresolved. Commit each
completed logical slice before moving on. If residual dirty files are not part
of the completed step, stop and resolve ownership before continuing.

## Commit Timing During Plan Execution

Commit cadence is based on logical slices, not elapsed time:
- Commit after a logical slice is complete and verified.
- Keep commits atomic and reviewable.
- Follow existing commit/history rules in `COMMIT-STANDARDS.md`.
- Commit related code, tests, and documentation together when they belong to the
  same logical slice.
- For cross-layer feature work, prefer committing the first verified vertical
  slice before expanding shared layers horizontally.
- Keep unrelated fixes in separate commits.
- Commit compile-unblocking fixes separately when they are not part of the
  current logical slice.

This document sets timing guidance only; commit format/cleanup stays external.

## Concurrent Worker Execution

Subagents or parallel workers are optional. Use them only when work can be split
into clearly bounded, low-coupling streams.

When planning concurrent workers, record:
- Owner/agent name
- Assigned scope
- Expected output contract
- Handoff checkpoint
- Primary write set
- Allowed adjacent write set
- Read-only context
- Forbidden/shared files
- External-change escalation rule
- Worker report path

Worker scopes must not overlap in a way that can produce competing edits. Shared
contracts, public interfaces, schemas, configs, global utilities, fixtures,
generated files, lockfiles, and cross-cutting integration points must be
assigned to exactly one worker, handled in a serial step, or deferred to a later
coordination step.

When workers are allowed to commit, do not run them in the same working tree.
Use one isolated worktree or temporary clone per worker branch, created from the
same clean integration commit for the wave. Each worker may commit only inside
its assigned branch and workspace.

Workers may read broadly for context but may only edit files in their assigned
primary or allowed adjacent write set. If a required change falls outside the
write set, the worker must record it in the worker report instead of making the
edit.

Execute one worker wave at a time. After each wave:
- Read every worker report.
- Verify changed files match assigned write sets.
- Merge, rebase, or cherry-pick worker branches into the integration branch one
  at a time.
- Preserve worker atomic commits when they are clean and meaningful.
- Resolve conflicts in a separate integration commit when conflict resolution is
  not already owned by one worker slice.
- Run the wave's required verification after integration.
- Update the plan with wave status, report links, integrated branches or
  commits, verification results, deviations, and follow-up work.
- Start the next wave only from the updated, verified integration branch.

Clean up worker workspaces after integration:
- Remove worker worktrees or temporary clones after their branch is integrated
  and wave verification passes, unless they are explicitly needed for
  investigation.
- Delete local worker branches after integration when their commits are
  reachable from the integration branch and the branch is no longer needed.
- Before deleting any worker workspace, confirm there are no uncommitted changes
  in that workspace.
- If a worker branch is abandoned, preserve its Markdown report and record the
  reason in the plan before deleting the workspace.

All commit metadata requirements remain defined by `COMMIT-STANDARDS.md`.

## Re-Plan Triggers

Re-plan when any of the following occurs:
- Objective or constraints materially change
- A dependency assumption is invalidated
- A milestone misses acceptance criteria
- New risk is introduced that changes sequencing
- An unexpected issue changes scope, sequencing, compatibility impact, or
  verification strategy

When re-planning, document:
- What changed
- Why it changed
- Which milestones/tasks were updated

## Unexpected Issues During Execution

Record unexpected issues in the plan before deciding how to proceed.

Use this decision process:
- If an issue is directly related to the current plan and can be resolved safely
  in a standards-compliant way, add a new plan step, implement the fix, verify
  it, and commit it as its own atomic commit when it is meaningfully separate
  from the current step.
- If an issue is related to the plan but is not easy to resolve safely, and the
  remaining plan can continue without being adversely affected, record the
  issue, location, risk, and recommended follow-up in the plan.
- If an issue is unrelated to the plan and does not affect implementation,
  compilation, or required verification, record the issue, location, and
  recommended follow-up in the plan and continue.
- If an unrelated issue prevents compilation, testing, or required verification,
  add a new plan step for the minimal standards-compliant unblocker, implement
  only that unblocker, verify it, and commit it separately.
- If an issue changes objective, scope, sequencing, compatibility impact, or
  risk profile, stop implementation, re-evaluate the code and plan, and update
  the plan before continuing.

## Plan Updates During Execution

Keep the plan current as implementation progresses.

Plan updates must record:
- Completed steps
- Added steps
- Skipped or deferred steps, with reasons
- Unexpected issues discovered
- Verification run and results
- Deviations from the original plan
- Remaining follow-ups

Do not use the plan as a scratchpad for noisy command output. Summarize
verification results and link or reference detailed logs only when needed.

## Completion Summary

At plan close, provide:
- Completed milestones
- Deviations from original plan
- Remaining follow-ups (if any)
- Verification summary (referenced checks run)
- Traceability pointers (README/ADR/PR fields as applicable)

## Brevity Default

Plans should be concise by default:
- Use short sections and direct wording.
- Include detail only where it affects execution decisions.
- Expand depth only when explicitly requested or risk warrants it.
