# Plan: Standards Library Effectiveness Restructure

**Plan status:** `Active`

**Current phase:** Milestone 7 source-closure correction after semantic review

**Next slice:** admit the Engine-owned legacy-index correction for the 27-source
manifest population, including its supported semantic edit and consumer scope

**Acceptance status:** `partial`

**Composed-design review:** `not-applicable` to the current review/re-plan
slice: it records ownership findings without changing Engine composition.
Reassess when admitting any required Engine capability change.

**Execution ledger:** [Milestone execution ledger](execution-ledger.md)

**Issues:** [Standards effectiveness findings](issues.md)

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
| A1 | Fixed scenarios improve or preserve every critical rubric dimension. | `satisfied` | [Baseline scores](../../../evaluation/standards-effectiveness/baseline-scores.md) and [current rescore](../../archive/plans/planning-proportionality-recovery/reports/scenario-rescore.md) |
| A2 | Routing, ownership, duplication, disposition, and link targets pass from canonical evidence. | `pending` | [Current semantic review and inventory reconciliation](reports/milestone-7-semantic-ownership-review.md); historical dispositions do not prove current source closure |
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
| 0 | Baseline and fixed scenarios | `Accepted` | [Baseline report](../../../evaluation/standards-effectiveness/baseline-report.md), [scenario fixtures](../../../evaluation/standards-effectiveness/fixtures/scenarios.md) |
| 1 | Architecture, metadata, routing, and ownership | `Accepted` | [Owner map](../../../evaluation/standards-effectiveness/owner-map.tsv), [generated owner map](../../../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| 2 | Core and Router vertical slice | `Accepted` | [Core](../../../CORE-STANDARDS.md), [Router](../../../STANDARDS-ROUTER.md) |
| 3 | Planning and implementation lifecycle | `Accepted` | [Planning](../../../workflows/planning.md), [Implementation](../../../workflows/implementation.md) |
| 4 | Typed verification and release acceptance | `Accepted` | [Verification](../../../workflows/verification.md), [Release](../../../workflows/release.md) |
| 5 | Contracts, compatibility, and fallbacks | `Accepted` | [Contracts](../../../topics/contracts.md) |
| 6 | Proportional documentation and commit process | `Accepted` | [Documentation](../../../workflows/documentation.md), [Commit](../../../workflows/commit.md) |
| 7 | Role-based consolidation and verification migration | `Active` | D001–D010 reviewed; legacy authority and navigation findings require correction before acceptance |
| 8 | Scenario rescore, pilots, migration publication, and final review | `Planned` | Begins after Milestone 7 and the planning recovery are accepted |

### Milestone 7 Current State

**Goal:** Complete canonical-owner migration and eliminate legacy verification
without losing mapped semantics.

**Accepted boundary:** the recorded `7.4c3` packages remain historical evidence,
but their source-closure conclusion is superseded by the
[current semantic review](reports/milestone-7-semantic-ownership-review.md).
Legacy Tooling and Rust Bindings still contain competing instructions;
other retained entrypoints need purity or route correction. Verification
migration remains accepted through M6-Z1:
the complete command is Python-only, and no Bash verifier, helper, launcher, or
temporary migration model remains. The execution ledger and terminal report
contain detailed slice evidence.

**Accepted recovery boundary:** M6-I16 is accepted after one-owner final-state
proof. The [work proportionality and policy impact recovery](../../archive/plans/work-proportionality-and-policy-impact/plan.md)
and [generic edge-system recovery](../../archive/plans/generic-edge-system/plan.md)
are accepted. Fresh post-recovery evidence selected M6-I17 and fresh
post-M6-I17 evidence selected M6-I18; no stale package evidence was reused.

**Remaining work:**

1. Admit and implement the bounded source correction described in the
   [review](reports/milestone-7-semantic-ownership-review.md#corrective-slice-and-acceptance),
   through supported Engine-owned semantic operations and consumer review.
2. Recheck the affected D001–D010 findings and prove pure navigation and valid
   destinations across all 27 retained entrypoints.
3. Preserve frozen baseline inventories. Reconcile historical ID dispositions
   separately from current canonical membership, registered routing, actual
   source contents, and current structural checks. Do not regenerate frozen
   corpus classifications or revive retired migration/prose gates.

**Current blocker:** Milestone 7 acceptance is held by M7-OWN-01 through
M7-OWN-04 in [issues.md](issues.md#2026-09-05-semantic-ownership-review).
The next corrective admission can proceed; no external dependency blocks it.

**Acceptance gate:** every frozen identifier has a final disposition; live
structural and routing checks pass; manual review establishes single ownership
and navigation-only legacy sources with valid destinations. The Python
checkpoint owns registered structural verification, not prose conformance.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: routing, normative ownership,
  verification migration, downstream pilots, and publication remain separate
  milestones with distinct acceptance evidence.
- State, identity, value, time, policy, and mechanism: canonical rule identity
  and policy values stay in standards-owned records; package timing and
  mechanism migration stay in lifecycle manifests and the engine plan.
- Caller and composition-root knowledge: the Router composes the smallest
  applicable standards set, while the verification engine composes registered
  suites without moving policy into orchestration.
- Representative change paths and forced owners: a checker migration changes
  its owner-coherent suite, exact lifecycle records, and generated evidence
  without forcing unrelated normative modules to change.
- Stable Interfaces versus hidden knowledge: metadata, routing, dispositions,
  and suite contracts expose typed authority rather than relying on headings,
  filenames, or scattered plan narration.
- Independent evolution, testing, failure, and replacement: standards owners,
  reference material, migration packages, declarative checks, and pilots carry
  separate evidence and can fail without inheriting each other's authority.
- Necessary complexity and containment: temporary Bash graph evidence and
  mixed execution were contained to the verification migration and removed at
  the accepted zero-Bash boundary.
- Deletion and cumulative machinery result: each accepted slice deleted its
  replaced Bash authority, and the remaining migration machinery disappeared
  at zero-Bash closure rather than becoming permanent infrastructure.

## Evidence Index

| Authority | Canonical artifact |
| --- | --- |
| Detailed accepted execution history | [Execution ledger](execution-ledger.md) |
| Findings and resolutions | [Findings](issues.md) |
| Rule ownership | [Owner map](../../../evaluation/standards-effectiveness/owner-map.tsv) and [generated owner map](../../../evaluation/standards-effectiveness/generated/rule-owner-map.tsv) |
| Rule dispositions | [Consolidation dispositions](../../../evaluation/standards-effectiveness/consolidation-dispositions.tsv) |
| Milestone 7 decomposition | [Execution decomposition](../../../evaluation/standards-effectiveness/milestone-7-execution-decomposition.tsv) |
| Verification migration lifecycle | [Verification-engine plan](../../archive/plans/standards-verification-engine/plan.md), [ledger](../../archive/plans/standards-verification-engine/execution-ledger.md), and [M6-Z1 closure](../../archive/plans/standards-verification-engine/reports/m6-z1-zero-bash-closure.md) |
| Migration-Python terminal lifecycle | [Recovery plan](../../archive/plans/python-verification-engine-recovery/plan.md) and [ledger](../../archive/plans/python-verification-engine-recovery/execution-ledger.md) |
| Current recovery state | [Generic edge-system recovery](../../archive/plans/generic-edge-system/plan.md) and [ledger](../../archive/plans/generic-edge-system/execution-ledger.md) |
| Accepted engine recovery | [Python verification engine design recovery](../../archive/plans/python-verification-engine-recovery/plan.md) |

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
