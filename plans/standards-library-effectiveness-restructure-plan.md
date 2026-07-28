# Plan: Standards Library Effectiveness Restructure

## Status

**Direction:** Approved for planning.

**Current phase:** Plan created; normative standards are unchanged.

**Next slice:** Milestone 0, baseline inventory and evaluation fixtures.

This is the active implementation plan. Detailed findings, command output, and
dated execution history belong in linked reports and an execution ledger, not
in this file.

## Objective

Make the Coding Standards repository objectively more effective as reusable
guidance for unrelated downstream repositories. The revised library must:

- produce higher-quality plans and implementation procedures;
- route a task to the smallest sufficient standards set;
- distinguish mandatory rules, recommendations, profiles, and reference;
- give each normative rule one canonical owner;
- preserve objective-level acceptance through planning and implementation;
- separate active plan state from execution history;
- make compatibility, fallback, documentation, and process obligations
  proportional to real contracts and risks; and
- remain stack-agnostic at the root, with explicit profiles for specialized
  guidance.

Pantograph is evidence that the current process can produce oversized,
internally inconsistent plans whose completed milestones do not prove the
requested user outcome. It is a regression case, not the design target.
Pantograph-specific architecture, runtime policy, or no-fallback decisions must
not become universal standards.

## Success Measures

### Quality

- Plans state the requested end goal and its acceptance path.
- A milestone cannot close with evidence weaker than its acceptance criterion.
- Current decisions, owners, blockers, status, and next action are unambiguous.
- Re-planning supersedes old decisions instead of leaving multiple active
  interpretations.
- Compatibility and fallback policy follows actual authority, consumer,
  persistence, and deployment boundaries.
- Independent concerns remain independently changeable.

### Cognitive Load

- One short entry point routes each task to applicable guidance.
- Normal tasks never require reading the whole standards tree.
- Examples and tool recipes are not required context for normative compliance.
- Active plans contain current state; ledgers and reports contain history.
- Generic rules are not repeated in language or application profiles.

### Initial Quantitative Targets

Milestone 0 records exact baselines. Initial targets are:

- reduce normative duplication by at least 30% without losing mapped required
  semantics;
- route every evaluation fixture without loading the complete library;
- keep the median routed set below 25% of the normative corpus;
- assign every retained normative rule one canonical owner;
- eliminate all inventoried contradictory active rules;
- give every fixture plan one objective-level acceptance path and one next
  slice; and
- produce no broken links, ownership gaps, or unresolved precedence.

Targets may change only from recorded evidence, never to make results appear
successful.

## Baseline

The 2026-07-28 review found:

- about 11,600 Markdown lines in the repository;
- more than 10,000 lines after excluding plans, prompts, templates, indexes,
  and adoption notes;
- about 860 headings and more than 300 strong imperative phrases;
- a root quick start that directs adopters to copy and read the full library;
- additive generic and Rust guidance that can require a large combined context;
- normative rules mixed with examples, setup recipes, and tool versions;
- planning rules that require continual updates without defining rollover,
  supersession, history separation, or sufficient lifecycle states; and
- cross-layer test requirements without an equally strong plan-closure rule
  binding completion to objective-level acceptance.

The Pantograph regression case includes an approximately 75,000-line active
plan, hundreds of dated/re-plan entries, conflicting decisions, and headless
validation that preceded a usable workflow. These are evidence, not universal
size limits.

## Scope And Constraints

### In Scope

- Library information architecture and task routing.
- Normative level, applicability, ownership, and precedence metadata.
- Planning, implementation, verification, re-planning, and release workflows.
- Active-plan, execution-ledger, issue, report, and ADR ownership.
- Acceptance taxonomy for focused through user-visible and release checks.
- Contract evolution, compatibility, and fallback/degraded-mode policy.
- Proportional documentation and commit-process obligations.
- Normative deduplication and reference extraction.
- Versioning, migration, and adoption guidance.
- Repeatable before/after evaluation.

### Out Of Scope

- Retrofitting downstream repositories.
- Encoding one product's architecture as generic policy.
- Removing safety, security, accessibility, interop, or concurrency semantics
  solely to reduce document size.
- Building a documentation site unless repository navigation proves
  insufficient.

### Constraints

- Root guidance owns cross-language principles; profiles own specializations.
- Each mandatory rule needs one canonical owner and an observable reason.
- Every removed or moved rule needs a recorded
  `keep/refine/merge/move/remove` disposition.
- Old entrypoints may temporarily route readers, but cannot remain competing
  normative owners.
- Metadata must be simple enough to maintain manually.
- Automation may enforce deterministic structure, not subjective architecture.
- Work proceeds in verified, atomic documentation slices.

## Target Information Architecture

Milestone 1 freezes paths after inventory. The intended roles are:

```text
CORE-STANDARDS.md       Short universal invariants
STANDARDS-ROUTER.md     Applicability and precedence
workflows/              Planning, implementation, verification, release
profiles/               Application, boundary, and language specializations
topics/                 Optional concerns such as security and persistence
reference/              Examples, recipes, explanations, and templates
```

Every canonical module declares:

- purpose;
- level: `MUST`, `SHOULD`, `PROFILE`, or `REFERENCE`;
- applies when / does not apply when;
- prerequisites and specialization relationship;
- verification; and
- canonical owner.

The router resolves:

```text
CORE
  + one workflow
  + applicable application/boundary/language profiles
  + affected topic modules
```

Readers must not infer precedence from scattered prose.

## Plan Artifact Contract

Planning guidance will separate state from evidence:

```text
plan.md              Objective, decisions, status, milestones, next slice
execution-ledger.md  Dated slice, commit, and verification summaries
issues.md            Findings and dispositions
reports/             Investigations and detailed evidence
ADRs                 Durable architectural decisions
```

An active plan exposes its objective, objective-level acceptance path, current
phase, exactly one next slice, binding decisions, blockers, and re-plan
triggers. It links to history rather than embedding it.

Lifecycle states are `Planned`, `Active`, `Blocked`, `Implemented`,
`Verifying`, `Accepted`, `Deferred`, and `Superseded`. `Implemented` is not
complete; `Accepted` requires the named evidence.

## Evaluation Method

### Fixed Scenarios

Use neutral fixtures representing:

1. A small single-module bug fix.
2. A cross-layer desktop workflow with backend business logic and frontend
   projection.
3. A durable background worker with cancellation and restart.
4. A Rust FFI or generated-binding contract change.
5. A persisted breaking schema change with coordinated consumers.
6. A dependency and release update.
7. A hardware- or environment-gated end-to-end capability.

Each fixture declares applicable and excluded standards, required plan fields,
expected acceptance level, prohibited ownership/fallback errors, and expected
state/history artifacts.

### Comparison Rubric

| Dimension | Objective check |
| --- | --- |
| Applicability | Router selects sufficient modules without a full-tree read. |
| Objective fidelity | Plan names the externally meaningful acceptance path. |
| Ownership | Each policy, state, and lifecycle decision has one owner. |
| Complection | Independent concepts can change independently. |
| Verification | Lower-level checks cannot satisfy higher-level acceptance. |
| Legibility | Objective, status, blockers, and next slice have one entrypoint. |
| Re-planning | A new decision supersedes the old active decision. |
| Proportionality | Small work avoids unrelated plan, README, ADR, or history duties. |
| Evolution | Internal, persisted, public, and versioned contracts get the right policy. |

Run the same fixtures and rubric before and after restructuring.

## Definition Of Done

- Core, router, roles, metadata, and precedence are implemented.
- Every retained rule has one owner and an inventory disposition.
- Planning separates current state from history and uses the richer lifecycle.
- Acceptance levels have distinct meanings and closure roles.
- Contract and fallback rules follow explicit authority/consumer analysis.
- README, ADR, and commit obligations are proportional to risk.
- Examples and recipes no longer inflate mandatory context.
- All fixed scenarios improve or preserve required rubric scores.
- Quantitative targets, structural checks, and link checks pass.
- Migration guidance explains paths, precedence, and adoption.
- No downstream-specific rule leaks into universal standards.

## Milestones

### Milestone 0: Baseline And Fixtures

**Goal:** Establish reproducible evidence before changing normative guidance.

- [ ] Inventory files, normative sections, rules, links, and applicability.
- [ ] Assign rule identifiers and preliminary role/disposition.
- [ ] Record duplicates, conflicts, broad rules, and ownership gaps.
- [ ] Capture corpus, duplication, routing, and process baselines.
- [ ] Create and score the seven fixed scenarios.

**Write set:** this plan and a dedicated evaluation/report directory only.

**Gate:** Every normative section has an identifier; another reviewer can
reproduce counts, routing, and scores.

**Status:** Planned.

### Milestone 1: Architecture And Metadata

**Goal:** Freeze ownership and routing before moving rules.

- [ ] Confirm canonical paths, metadata fields, and precedence.
- [ ] Map each rule identifier to one future owner and disposition.
- [ ] Resolve conflicts and define old-entrypoint migration policy.
- [ ] Add valid/invalid routing metadata fixtures.

**Write set:** decision/report artifacts, metadata fixtures, and this plan.

**Gate:** Every retained rule has one proposed owner; scenarios route without
cycles or ambiguity.

**Status:** Planned.

### Milestone 2: Core And Router Vertical Slice

**Goal:** Prove progressive disclosure on one complete scenario.

- [ ] Implement core, router, one workflow, applicable profiles, and minimum
  topics for the selected scenario.
- [ ] Convert affected old entrypoints to non-duplicating indexes.
- [ ] Add link, applicability, ownership, and precedence checks.
- [ ] Re-run the scenario using only its routed set.

**Write set:** selected vertical path, old indexes, focused checks, and plan.

**Gate:** The scenario is correctly planned without unrelated standards, and
all retained semantics trace to inventory identifiers.

**Status:** Planned.

### Milestone 3: Planning And Implementation Lifecycle

**Goal:** Keep active plans current, bounded, and acceptance-oriented.

- [ ] Implement the plan artifact contract and richer lifecycle.
- [ ] Require one current phase, one next slice, and explicit supersession.
- [ ] Define compaction/rollover triggers.
- [ ] Bind `Accepted` to objective-level evidence.
- [ ] Update planning/implementation standards, prompts, and templates.
- [ ] Add active, blocked, accepted, and superseded fixtures.

**Write set:** planning/implementation guidance, prompts, template, fixtures,
and plan.

**Gate:** Partial or headless evidence cannot close a user-visible objective;
current status is understandable without reading history.

**Status:** Planned.

### Milestone 4: Verification And Release Acceptance

**Goal:** Give every verification level a distinct purpose.

- [ ] Consolidate focused, integration, contract, system, user-workflow,
  environment-gated, release-artifact, and manual acceptance definitions.
- [ ] Remove universal duration and CI-only assumptions.
- [ ] State that launch smoke does not prove a user feature.
- [ ] Align testing, tooling, launcher, release, and plan guidance.

**Write set:** verification workflow and affected standards/templates/fixtures.

**Gate:** Every scenario selects the expected levels; weaker evidence cannot
satisfy a stronger criterion.

**Status:** Planned.

### Milestone 5: Contracts, Compatibility, And Fallbacks

**Goal:** Base evolution behavior on real authority and consumer constraints.

- [ ] Define policies for internal, persisted, public, and independently
  versioned contracts.
- [ ] Define coordinated breaking replacement and migration expectations.
- [ ] Require authority and semantic fidelity for degraded behavior.
- [ ] Require typed unavailable/invalid/deferred outcomes when no valid
  decision can be made.
- [ ] Reconcile affected coding, architecture, interop, persistence, release,
  and profile guidance.

**Write set:** canonical evolution topic, affected indexes/profiles, fixtures,
and plan.

**Gate:** Fixtures distinguish coordinated replacement, public versioning,
persistence migration, and invalid fallback.

**Status:** Planned.

### Milestone 6: Proportional Documentation And Commit Process

**Goal:** Preserve traceability without routine low-value work.

- [ ] Require module READMEs only at meaningful boundaries.
- [ ] Use concise README profiles instead of one universal template.
- [ ] Tie README/ADR work to decision impact.
- [ ] Link accepted rationale instead of restating it in every artifact.
- [ ] Move full-history checks to milestone, pre-push, and PR boundaries while
  retaining staged-diff review per commit.
- [ ] Update traceability tooling and fixtures.

**Write set:** documentation/commit/tooling standards, templates, checks,
fixtures, and plan.

**Gate:** Small changes avoid unrelated artifacts; architectural/public changes
retain durable traceability and atomic review.

**Status:** Planned.

### Milestone 7: Role-Based Consolidation

**Goal:** Complete migration without losing mapped semantics.

- [ ] Move rules to canonical workflow/profile/topic owners.
- [ ] Replace duplicate normative passages with links.
- [ ] Move examples, recipes, and tool-version guidance to reference.
- [ ] Remove obsolete rules only after inventory and fixture review.
- [ ] Retain legacy indexes only where migration value is demonstrated.

**Write set:** one role at a time, its fixtures/indexes, migration map, and plan.

**Gate:** Every rule identifier has a final disposition; duplication target and
all structural/routing fixtures pass.

**Status:** Planned.

### Milestone 8: Pilot And Adoption

**Goal:** Prove improvement before declaring the redesign accepted.

- [ ] Re-run scenarios and compare scores/context against baseline.
- [ ] Run two independent downstream pilots with different profiles.
- [ ] Use Pantograph only as one regression audit.
- [ ] Fix material regressions in owner-bounded slices.
- [ ] Publish migration guidance and standards version information.
- [ ] Record residual limitations and future work.

**Write set:** pilot reports, migration/version artifacts, final plan status,
and separately bounded fixes.

**Gate:** Critical rubric dimensions and quantitative targets pass; pilots do
not need the full library or introduce downstream-specific root policy.

**Status:** Planned.

## Slice Procedure

For every implementation slice:

1. Inspect standards-repository status and do not start with unrelated dirty
   implementation files.
2. Name one behavior or information-architecture outcome and exact write set.
3. Identify affected rule identifiers and their dispositions.
4. State which semantics are preserved, refined, moved, or removed.
5. Add or update focused structural and scenario fixtures.
6. Run focused fixtures plus affected link/metadata checks.
7. Update milestone state here; put details in the ledger/report.
8. Review staged changes and create one atomic conventional commit.
9. Do not start the next slice with unresolved implementation files.

If evidence or history obscures current status, move it out of this plan before
continuing.

## Concurrency

Read-only inventory may run in parallel for non-overlapping standards groups.
Core, router, metadata schema, shared acceptance taxonomy, lifecycle contract,
templates, validation scripts, migration map, and this plan remain serial
integration-owner work.

Delegated work reports files reviewed, rule identifiers/dispositions,
conflicts, proposed owners, fixture effects, and out-of-scope findings. It may
not create competing core, precedence, or taxonomy rules.

## Risks And Re-Plan Triggers

| Risk or trigger | Required response |
| --- | --- |
| Reduction drops safety or correctness semantics | Stop; restore traceability and revise disposition. |
| Router needs most of the library for ordinary scenarios | Rework roles or routing before migration. |
| Rule cannot map to one owner | Resolve ownership before moving it. |
| Metadata needs subjective machine enforcement | Reduce metadata/check scope. |
| Stable links require duplicate normative owners | Use routing indexes or versioned migration, not duplication. |
| Scores fall despite lower context | Preserve quality and revise structure/targets. |
| Root guidance becomes stack/product-specific | Move specialization to a profile or project policy. |
| Shared taxonomy must change outside a slice | Stop and re-plan a serial contract slice. |
| Pilot evidence invalidates sequence or targets | Record evidence and revise milestones before continuing. |

Isolated urgent safety corrections may proceed only as separate, verified work
unrelated to this restructure.

## Commit And Completion Policy

- Shared contracts land before broad movement.
- Each commit preserves a usable entrypoint and passes affected checks.
- Rule moves include indexes and fixtures in the same commit.
- Mechanical reference extraction follows semantic ownership decisions.
- Verification logs stay out of commit messages.

Complete this plan only when all milestone gates and the definition of done are
accepted. The final summary must list accepted outcomes, deviations, remaining
follow-ups, verification evidence, and the migration/version result.
