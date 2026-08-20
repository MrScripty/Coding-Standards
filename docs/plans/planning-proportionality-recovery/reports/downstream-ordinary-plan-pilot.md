# Downstream Ordinary-Plan Pilot

## Pilot Boundary

- Downstream repository: Pantograph, read-only at commit
  `464d5d0bd99267ab86e5960f2abf4d930148e035`.
- Downstream condition: two unrelated proposal documents were dirty, so the
  pilot made no downstream write and did not begin a source slice.
- Candidate objective: derive one current owner-classified image-generation
  failure inventory from committed evidence and update the recovery handoff.
- Candidate scope: plan and report Markdown only; source, tests, fixtures,
  configuration, generated files, saved workflows, lockfiles, SQLite files,
  and runtime behavior were excluded.

The pilot used Pantograph only as an adopter. No Pantograph policy, design, or
repository-specific mechanism was copied into the standards library.

## Routed Guidance

| Observable condition | Selected owner |
| --- | --- |
| Any standards-governed change | Core and Router |
| Bounded documentation implementation | Implementation and Documentation workflows |
| Multi-step evidence classification and handoff | Planning workflow |
| Objective and link proof | Verification workflow |
| Multiple outstanding proposals that can become stale | Not present; Concurrent Plan Integration excluded |

No application, language, boundary, or topic profile was needed because the
pilot changed no product behavior. Backend, scheduler, runtime, frontend, and
Tauri ownership appeared only as downstream classification constraints.

## Candidate Plan

The candidate plan contained:

- explicit `Planned` status, current phase, exactly one next slice, and pending
  acceptance;
- links to a separate ledger and issue record;
- one observable objective and two typed acceptance claims;
- bounded in-scope and excluded artifacts;
- two current binding decisions with owners and supersession;
- one milestone with an exact four-path Markdown write set;
- blockers, re-plan triggers, concurrency exclusion, and final acceptance;
- no compatibility, legacy, inferred-status, or missing-evidence fallback.

The exact candidate write set was:

```text
docs/plans/current-image-generation-graphs/reports/known-failures.md
docs/plans/current-image-generation-graphs/implementation-recovery-sequence.md
docs/plans/current-image-generation-graphs/execution-ledger.md
docs/plans/current-image-generation-graphs/issues.md
```

The plan required no digest, transition identity, admission identity, revision
token, proposal actor, reconciliation record, or storage representation. Those
fields were not applicable because one current-state integration owner had no
outstanding proposal that could become stale.

## Verification

- The canonical plan-structure checker passed the 132-line candidate plan.
- Every candidate plan link resolved against its temporary downstream artifact
  directory.
- A prohibited-field search found no genericized transition-protocol fields.
- Manual review confirmed one objective, one current phase, one next slice,
  bounded work, explicit acceptance, and serial shared-authority ownership.
- Pantograph remained unchanged; the two pre-existing proposal changes were
  neither edited nor used as pilot authority.

## Result

The ordinary-plan pilot passes. An adopter can construct and validate a
standards-compliant plan from explicit identity, lifecycle, scope, ownership,
and acceptance facts without inventing transition tooling. The conditional
concurrency profile remains available without burdening the ordinary path.
