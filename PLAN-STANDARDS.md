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

Use `templates/PLAN-TEMPLATE.md`.

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
3. Implement one logical task at a time.
4. Verify each completed logical slice using applicable existing standards.
5. Update plan status after each milestone.
6. Re-plan immediately when triggers are hit.
7. Close with a completion summary against done criteria.

## Commit Timing During Plan Execution

Commit cadence is based on logical slices, not elapsed time:
- Commit after a logical slice is complete and verified.
- Keep commits atomic and reviewable.
- Follow existing commit/history rules in `COMMIT-STANDARDS.md`.

This document sets timing guidance only; commit format/cleanup stays external.

## Optional Subagent Use

Subagents are optional. Use them only when work can be split into clearly
bounded, low-coupling streams.

When using subagents, record:
- Owner/agent name
- Assigned scope
- Expected output contract
- Handoff checkpoint

All commit metadata requirements remain defined by `COMMIT-STANDARDS.md`.

## Re-Plan Triggers

Re-plan when any of the following occurs:
- Objective or constraints materially change
- A dependency assumption is invalidated
- A milestone misses acceptance criteria
- New risk is introduced that changes sequencing

When re-planning, document:
- What changed
- Why it changed
- Which milestones/tasks were updated

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
