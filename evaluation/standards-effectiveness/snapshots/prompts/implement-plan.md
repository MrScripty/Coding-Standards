## Intent

Implement the provided plan completely while preserving an auditable history of
the work. Treat the plan as the source of truth for scope, sequence, acceptance
criteria, and risk controls, but update it when implementation reveals facts
that materially change the safest path forward.

## Standards

Follow:
- `PLAN-STANDARDS.md` for execution order, worktree hygiene, plan updates,
  unexpected issue handling, concurrent worker execution, re-plan triggers, and
  completion summaries.
- `COMMIT-STANDARDS.md` for atomic commit format, commit grouping, commit
  messages, and agent metadata.
- Any domain-specific standards referenced by the plan.

## Preflight

1. Read the full plan before editing files.
2. Read the standards referenced by the plan.
3. Inspect the current git status.
4. Apply the worktree hygiene rules from `PLAN-STANDARDS.md`.
   - Do not begin implementation with dirty implementation files unless the user
     explicitly allows them.
   - Do not revert or overwrite unrelated existing changes without explicit
     permission.
5. Confirm the plan has an objective, ordered steps or milestones, verification
   criteria, and completion criteria.
   - If missing details can be inferred safely, record the assumption in the
     plan and continue.
   - If they cannot be inferred safely, record the gap in the plan and pause for
     clarification.

## Process

1. Implement the plan in order, one logical step at a time.
2. After each logical step:
   - Run the verification required for that step.
   - Update the plan with status, notes, and verification results.
   - Commit the completed step using `COMMIT-STANDARDS.md`.
3. Do not begin the next step until dirty implementation files from the previous
   step are committed or resolved according to `PLAN-STANDARDS.md`.
4. Commit code, tests, and documentation together when they belong to the same
   logical step.
5. Keep unrelated fixes and compile-unblocking changes in separate commits.
6. Do not include verification commands, test output, or tool logs in commit
   messages.

## Concurrent Workers

If the plan includes parallel implementation waves or concurrent worker
instructions, follow the concurrent worker execution rules in
`PLAN-STANDARDS.md`.

In particular:
- Execute one worker wave at a time.
- Validate non-overlapping write sets before launching workers.
- Give each worker one complete prompt with scope, write boundaries, validation
  expectations, report path, and escalation rules.
- Use one isolated worktree or temporary clone per committing worker branch.
- Integrate worker branches one at a time into the verified integration branch.
- Read worker reports and update the plan before launching dependent waves.
- Clean up worker worktrees, temporary clones, and local branches when they are
  no longer needed.

## Unexpected Issues

When implementation reveals an unexpected issue, record it in the plan before
deciding how to proceed. Follow the unexpected issue decision process in
`PLAN-STANDARDS.md`.

Continue only when the safe path is clear. If the issue changes the plan's
objective, scope, sequencing, compatibility impact, or risk profile, stop,
re-evaluate the code and plan, update the plan, and pause for clarification if
needed.

## Completion

When all plan steps are complete:

1. Run the plan's final verification criteria.
2. Update the plan with a completion summary.
3. Confirm there are no uncommitted changes that belong to the implementation.
4. Report:
   - Completed steps
   - Commits made
   - Verification summary
   - Deviations from the plan
   - Follow-ups that remain
