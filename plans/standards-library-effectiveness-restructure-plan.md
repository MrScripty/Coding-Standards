# Plan: Standards Library Effectiveness Restructure

**Plan status:** `Active`

**Current phase:** Milestone 7 verification migration

**Next slice:** fresh post-recovery graph audit; no verifier package is preselected

**Acceptance status:** `partial`

**Execution ledger:** [Milestone execution ledger](../evaluation/standards-effectiveness/execution-ledger.md)

**Issues:** [Standards effectiveness findings](../evaluation/standards-effectiveness/findings.md)

This file owns current objective, decisions, milestone state, blockers, and the
next authorized slice. Detailed execution history belongs in the linked ledger
and reports. Migration lifecycle belongs in canonical package, disposition,
owner, and generated-evidence records.

## Objective

Make the Coding Standards repository objectively more effective as reusable
guidance for unrelated downstream repositories. The revised library must:

- produce higher-quality plans and implementation procedures;
- route tasks to the smallest sufficient standards set;
- distinguish mandatory rules, recommendations, profiles, and reference;
- give each normative rule one canonical owner;
- preserve objective-level acceptance through planning and implementation;
- separate active plan state from execution history;
- make compatibility, fallback, documentation, and process obligations
  proportional to real contracts and risks; and
- remain stack-agnostic at the root, with explicit profiles for specialized
  guidance.

Pantograph remains one regression case, not the design target or a source of
universal architecture policy.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | Fixed scenarios improve or preserve every critical rubric dimension. | `satisfied` | [Baseline scores](../evaluation/standards-effectiveness/baseline-scores.md) and [current rescore](../docs/plans/planning-proportionality-recovery/reports/scenario-rescore.md) |
| A2 | Routing, ownership, duplication, disposition, and link targets pass from canonical evidence. | `partial` | [Generated owner map](../evaluation/standards-effectiveness/generated/rule-owner-map.tsv); [consolidation dispositions](../evaluation/standards-effectiveness/consolidation-dispositions.tsv) |
| A3 | Two independent downstream pilots complete without loading the full library. | `pending` | Milestone 8 |
| A4 | Migration and standards-version guidance is published. | `pending` | Milestone 8 |
| A5 | Final manual review confirms the library is stack-agnostic, routed, concise, and free of competing normative owners. | `pending` | Milestone 8 |

## Scope And Constraints

### In Scope

- Library information architecture and task routing.
- Normative level, applicability, ownership, and precedence metadata.
- Planning, implementation, verification, re-planning, and release workflows.
- Active-plan, ledger, issue, report, and ADR ownership.
- Typed acceptance for focused through user-visible and release checks.
- Contract evolution, compatibility, fallback, and degraded-mode policy.
- Proportional documentation and commit obligations.
- Normative deduplication, reference extraction, versioning, and adoption.
- Repeatable before-and-after evaluation.

### Out Of Scope

- Retrofitting downstream repositories.
- Encoding one product's architecture as generic policy.
- Removing safety, security, accessibility, interop, or concurrency semantics
  solely to reduce document size.
- Building a documentation site unless repository navigation proves
  insufficient.

### Constraints

- Root guidance owns cross-language principles; profiles own specializations.
- Each retained mandatory rule has one canonical owner and observable reason.
- Every removed or moved rule has a recorded
  `keep/refine/merge/move/remove` disposition.
- Old entrypoints may route readers only when they do not compete as normative
  owners.
- Automation enforces deterministic structure and evidence, not subjective
  architecture.
- Shared contracts and authority files integrate serially.
- Work proceeds in verified atomic slices without compatibility or fallback
  preservation of replaced standards and verification methods.

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Progressive disclosure | Route from Core through one workflow and only applicable profiles and topics. |
| Normative ownership | Every retained rule has one canonical owner; indexes link without restating rules. |
| Planning artifacts | Active plans own current state; ledgers and reports own history; ADRs own durable architectural decisions. |
| Specialization | Root guidance stays stack-agnostic; language and application details belong in profiles. |
| Reference material | Examples, recipes, and tool versions are non-normative unless explicitly promoted. |
| Acceptance model | Required evidence is a set of typed claims; proof kind, environment, and execution mode are independent dimensions. |
| Migration lifecycle | Canonical package, disposition, owner, and generated records own status; active-plan narration does not. |
| Verification migration | Bash checkers and helpers are removed with accepted Python-engine replacements; no wrappers, dual authority, compatibility parsers, or fallback remain. |
| Accelerated execution | Select proportional `serial-coherent`, `pre-admitted`, `owner-wave`, or `shared-contract` migration modes from current risk and concurrency facts. Owner-coherent packages may prepare concurrently with disjoint write sets; shared registry, evidence, Router, and plan integration remain serial. |
| Recovery dependency | The historical Git reachability recovery and the reopened cleanup plan are accepted. Obtain fresh graph evidence before selecting another verifier package rather than reusing post-M6-I52 selection facts. |
| Current efficiency recovery | The accepted efficiency recovery stabilizes temporary component identities and applies proportional serial/wave migration modes. Historical cleanup is accepted only after explicit reachability reconciliation; normal remote backup is accepted and pilots remain separately owned. |

## Current Architecture

```text
CORE-STANDARDS.md
  + one workflow
  + applicable application, boundary, and language profiles
  + affected topic modules
```

Canonical modules declare purpose, level, applicability and exclusions,
prerequisites, specialization, verification, and owner. Readers do not infer
precedence from scattered prose.

The active artifact boundary is:

```text
plan.md              current objective, decisions, milestones, blockers, next slice
execution-ledger.md  accepted execution and verification history
issues.md            findings and dispositions
reports/             detailed investigations and evidence
ADRs                 durable architecture decisions
```

Lifecycle states are `Planned`, `Active`, `Blocked`, `Implemented`,
`Verifying`, `Accepted`, `Deferred`, and `Superseded`. `Implemented` is not
complete; `Accepted` requires the named evidence.

## Milestones

| Milestone | Outcome | Status | Current evidence or next work |
| --- | --- | --- | --- |
| 0 | Baseline and fixed scenarios | `Accepted` | [Baseline report](../evaluation/standards-effectiveness/baseline-report.md), [scenario fixtures](../evaluation/standards-effectiveness/fixtures/scenarios.md) |
| 1 | Architecture, metadata, routing, and ownership | `Accepted` | [Owner map](../evaluation/standards-effectiveness/owner-map.tsv), [generated owner map](../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| 2 | Core and Router vertical slice | `Accepted` | [Core](../CORE-STANDARDS.md), [Router](../STANDARDS-ROUTER.md) |
| 3 | Planning and implementation lifecycle | `Accepted` | [Planning](../workflows/planning.md), [Implementation](../workflows/implementation.md) |
| 4 | Typed verification and release acceptance | `Accepted` | [Verification](../workflows/verification.md), [Release](../workflows/release.md) |
| 5 | Contracts, compatibility, and fallbacks | `Accepted` | [Contracts](../topics/contracts.md) |
| 6 | Proportional documentation and commit process | `Accepted` | [Documentation](../workflows/documentation.md), [Commit](../workflows/commit.md) |
| 7 | Role-based consolidation and verification migration | `Active` | M6-I59 accepted; fresh graph audit is next |
| 8 | Scenario rescore, pilots, migration publication, and final review | `Planned` | Begins after Milestone 7 and the planning recovery are accepted |

### Milestone 7 Current State

**Goal:** Complete canonical-owner migration and eliminate legacy verification
without losing mapped semantics.

**Accepted boundary:** normative owner consolidation is complete through the
recorded `7.4c3` packages. Verification migration is accepted through M6-I59
at train order 174, and no later package is admitted. The canonical package
manifest contains the exact package state; the execution ledger contains
detailed slice evidence.

**Accepted recovery boundary:** M6-I16 is accepted after one-owner final-state
proof. The [work proportionality and policy impact recovery](../docs/plans/work-proportionality-and-policy-impact/plan.md)
and [generic edge-system recovery](../docs/plans/generic-edge-system/plan.md)
are accepted. Fresh post-recovery evidence selected M6-I17 and fresh
post-M6-I17 evidence selected M6-I18; no stale package evidence was reused.

**Remaining work:**

1. Audit the fresh post-recovery graph through the verification-engine plan.
2. Continue owner-coherent Python-engine migration until no Bash verifier,
   helper, or migration launcher remains.
3. Use focused final-state evidence for each package and run the complete mixed
   checkpoint at owner-wave or shared-contract acceptance, zero-Bash closure,
   or when cumulative retained-Bash/consumer evidence cannot prove accepted
   packages independent.
4. Regenerate canonical inventories and prove exact dispositions, no source
   gaps, no normative legacy source rows, and no legacy Router routes.
5. Complete manual semantic-ownership review `D001` through `D010` before
   Milestone 7 acceptance.

**Acceptance gate:** every rule identifier has a final disposition; structural,
routing, ownership, source-closure, and no-legacy checks pass; the final Python
engine is the sole verification authority.

## Evidence Index

| Authority | Canonical artifact |
| --- | --- |
| Detailed accepted execution history | [Execution ledger](../evaluation/standards-effectiveness/execution-ledger.md) |
| Findings and resolutions | [Findings](../evaluation/standards-effectiveness/findings.md) |
| Rule ownership | [Owner map](../evaluation/standards-effectiveness/owner-map.tsv) and [generated owner map](../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| Rule dispositions | [Consolidation dispositions](../evaluation/standards-effectiveness/consolidation-dispositions.tsv) |
| Milestone 7 decomposition | [Execution decomposition](../evaluation/standards-effectiveness/milestone-7-execution-decomposition.tsv) |
| Checker migration lifecycle | [Checker migration packages](../evaluation/standards-effectiveness/checker-migration-packages.tsv) |
| Executable-edge lifecycle | [Executable edge dispositions](../evaluation/standards-effectiveness/executable-edge-dispositions.tsv) |
| Verification-engine current state | [Verification-engine plan](../docs/plans/standards-verification-engine/plan.md) and [ledger](../docs/plans/standards-verification-engine/execution-ledger.md) |
| Current recovery state | [Generic edge-system recovery](../docs/plans/generic-edge-system/plan.md) and [ledger](../docs/plans/generic-edge-system/execution-ledger.md) |

## Blockers

- `none`

## Slice Procedure

1. Confirm a clean repository and name one behavior plus exact write set.
2. Identify affected owners, identifiers, dispositions, and no-fallback impact.
3. Implement one coherent unit with focused evidence; split only when
   separation materially improves acceptance, risk, dependency, conflict,
   rollback, or feedback.
4. Run risk-proportionate checks and any required shared checkpoint.
5. Update current plan state and put execution detail in the ledger.
6. Review the staged write set and create one atomic conventional commit.

If history obscures current authority, move it to its canonical ledger or
report before continuing.

## Re-Plan Triggers

| Trigger | Required response |
| --- | --- |
| Safety or correctness semantics would be dropped | Stop, restore traceability, and revise the disposition. |
| Ordinary routing needs most of the library | Rework roles or routing before migration. |
| A rule cannot map to one owner | Resolve ownership before moving it. |
| Stable links require duplicate normative owners | Use a routing index or versioned migration, not duplication. |
| A shared taxonomy or authority contract must change outside the slice | Stop and admit a serial contract slice. |
| A checker migration needs a wrapper, retained Bash execution, compatibility parser, inferred owner, false dependency, or fallback | Stop and re-plan a canonical Python-engine replacement. |
| Active-plan compaction would remove evidence without canonical ledger, report, package, disposition, or lifecycle ownership | Stop and migrate that authority before deleting prose. |
| Pilot evidence invalidates sequence or targets | Record the evidence and revise milestones before continuing. |

## Final Acceptance

- **Objective evidence:** Pending Milestone 7 closure, Milestone 8 scenario
  comparison, two downstream pilots, migration publication, and manual review.
- **Deferred follow-ups:** None beyond milestones explicitly marked `Planned`.
- **Final status:** `Active`
