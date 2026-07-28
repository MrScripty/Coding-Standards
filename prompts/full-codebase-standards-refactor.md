# Full-Codebase Standards Review Prompt

Create an implementation-ready standards refactor plan. This is planning and
analysis only; do not edit source, tests, config, generated artifacts, or
lockfiles.

1. Route applicable standards with `STANDARDS-ROUTER.md`.
2. Follow `workflows/planning.md`.
3. Inventory affected areas and review standards as a combined constraint set.
4. Record findings with evidence, severity, owner, disposition, and acceptance.
5. Separate policy, mechanism, state, lifecycle, transport, persistence, UI,
   and diagnostics where they change independently.
6. Build dependency-ordered vertical slices with exact write sets.
7. Define non-overlapping delegated analysis or implementation scopes only when
   useful; shared contracts and plan artifacts remain serial.
8. Recheck the complete plan against every finding and routed standard.

Write `plan.md`, `execution-ledger.md`, `issues.md`, and reports under one
`docs/plans/<plan-slug>/` directory. Preserve the requested objective and name
the evidence that will accept it.
