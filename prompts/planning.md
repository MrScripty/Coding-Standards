# Planning Prompt

Create or revise an implementation plan. Do not implement source changes.

1. Read `CORE-STANDARDS.md` and use `STANDARDS-ROUTER.md`.
2. Follow `workflows/planning.md`.
3. Inspect repository status and affected code/contracts.
4. Preserve the requested objective and name its acceptance level.
5. Produce current-state artifacts from `templates/PLAN-TEMPLATE.md`.
6. Put findings in `issues.md` and detailed investigation in reports.
7. Select one coherent implementation unit. Split it only for material
   acceptance, risk, dependency, conflict, rollback, or feedback value; a plan
   may contain one milestone and one slice.
8. Delegate only non-overlapping read or write scopes with report paths.
9. Route concurrent plan integration only when multiple outstanding proposals
   can become stale before integration; do not infer it from participant count.

Stop for clarification when authoritative facts cannot support a valid plan.
Do not add fallback or compatibility behavior without an actual routed contract.
