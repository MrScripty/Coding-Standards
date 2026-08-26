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
10. Record branch or worktree facts only when material isolation is part of the
    plan; a written plan, delegation, or multi-file change does not require a
    branch by itself. If cleanup is in scope, include Commit's head-reachability
    and commit-disposition evidence rather than assuming a stale registration
    is safe to prune.
11. For each acceptance claim, identify the deciding oracle and distinguish
    freshness, local agreement, semantic correctness, public-path behavior,
    and external conformance. A generated artifact or second local
    implementation is not an independent semantic oracle.
12. When standardized or difficult semantics are material, evaluate an
    established dependency against the maintained local subset, conformance,
    security, maintenance, and unsupported-domain costs before choosing an
    implementation owner.
13. When one defect reveals a repeated invariant failure, stop the local
    repair. Inventory the invariant family, sibling producers and consumers,
    authority projections, and required dispositions before revising scope.
14. Before one artifact becomes canonical for several concerns, record its
    owned responsibility, referenced authorities, independent change axes, and
    lifecycle owners. Scope each version and identity invalidation to a proven
    compatibility promise; file, schema, generator, build, or release
    co-location is not that proof.

Stop for clarification when authoritative facts cannot support a valid plan.
Do not add fallback or compatibility behavior without an actual routed contract.
