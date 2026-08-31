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
8. Keep Git topology out of the plan. Do not prescribe commit count, parentage,
   direct-child chains, exact-HEAD admission, or standalone lifecycle commits.
   Bind review to material content, collect one review round before revising,
   and leave coherent commit boundaries to the Commit workflow.
9. Delegate only non-overlapping read or write scopes with report paths.
10. Route concurrent plan integration only when multiple outstanding proposals
   can become stale before integration; do not infer it from participant count.
11. Record branch or worktree facts only when material isolation is part of the
    plan; a written plan, delegation, or multi-file change does not require a
    branch by itself. If cleanup is in scope, include Commit's head-reachability
    and commit-disposition evidence rather than assuming a stale registration
    is safe to prune.
12. For each acceptance claim, identify the deciding oracle and distinguish
    freshness, local agreement, semantic correctness, public-path behavior,
    and external conformance. A generated artifact or second local
    implementation is not an independent semantic oracle.
13. When standardized or difficult semantics are material, evaluate an
    established dependency against the maintained local subset, conformance,
    security, maintenance, and unsupported-domain costs before choosing an
    implementation owner.
14. When one defect reveals a repeated invariant failure, stop the local
    repair. Identify the canonical owner and bound the authorities,
    representations, and reachable consumers that can violate the class-level
    claim. Inspect sibling operations only when they share that authority,
    reachable failure, or consumer promise. Consider deletion, consolidation,
    a smaller Interface, stronger construction or type proof, and replacement
    of overlapping evidence. Expand only for a new semantic owner, reachable
    consumer, material risk, or public or persistence promise; stop when the
    bounded population has evidence-backed dispositions.
15. Before one artifact becomes canonical for several concerns, record its
    owned responsibility, referenced authorities, independent change axes, and
    lifecycle owners. Classify each version-like value as current-format,
    identity-domain, compatibility, migration, or allocation authority. Record
    its promise, consumers, supported overlap, and consequences; share a value
    only when those facts coincide. Invalidate semantic identity only for a
    material meaning change. File, schema, generator, build, or release
    co-location proves none of these relationships.
16. Record composed-design review as `applicable` or `not-applicable` for every
    nonterminal written plan. Follow Planning's record requirements and use the
    Architecture admission when the review applies; otherwise record the
    concrete reason it does not apply.
17. Re-run the applicable admission after a material replacement rather than
    inheriting the prior result.

Stop for clarification when authoritative facts cannot support a valid plan.
Do not add fallback or compatibility behavior without an actual routed contract.
