# Plan: Standards Library Effectiveness Restructure

## Status

**Direction:** Approved and active.

**Plan status:** `Active`

**Current phase:** Accelerated Milestone 7 execution train accepted; the first
dependency-ready trust-boundary cluster is next.

**Next slice:** Milestone 7.4b8a Security validation cluster.

**Acceptance status:** `partial`

**Execution ledger:** [Milestone execution ledger](../evaluation/standards-effectiveness/execution-ledger.md)

**Issues:** [Standards effectiveness findings](../evaluation/standards-effectiveness/findings.md)

**Evidence:** [Milestone 0 evaluation](../evaluation/standards-effectiveness/README.md)

**Milestone 7 decomposition:** [Rolling owner-and-correctness waves](../evaluation/standards-effectiveness/milestone-7-decomposition.md)

**F018 decomposition:** [Runtime proof and action-specific IPC decoding](../evaluation/standards-effectiveness/milestone-7-f018-decomposition.md)

**F022/F023 decomposition:** [Foreign memory, unsafe contracts, ABI classification, and checked conversion](../evaluation/standards-effectiveness/milestone-7-f022-f023-decomposition.md)

**Remaining trust/lifecycle re-plan:** [Generic concurrency and Rust async dependency bridge](../evaluation/standards-effectiveness/milestone-7-trust-lifecycle-replan.md)

**Rust Async decomposition:** [Four owner-bounded specialization slices](../evaluation/standards-effectiveness/milestone-7-rust-async-decomposition.md)

**F025/F026 decomposition:** [Dependent Rust binding and security lifecycle slices](../evaluation/standards-effectiveness/milestone-7-f025-f026-decomposition.md)

**Independent trust-boundary re-plan:** [Six proposed-owner groups and corrected Rust wire-representation next slice](../evaluation/standards-effectiveness/milestone-7-independent-trust-replan.md)

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

## Objective Acceptance

- The fixed scenarios improve or preserve every critical rubric dimension.
- Quantitative routing, ownership, duplication, and link targets pass.
- Two independent downstream pilots complete without loading the full library.
- Migration and standards-version guidance is published.
- A final manual review confirms that the library is stack-agnostic, routed,
  concise, and free of competing normative owners.

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

- 12,088 Markdown lines in the reproducible baseline corpus;
- 11,066 normative or operationally derived lines;
- 1,015 headings and 352 strong imperative occurrences;
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

## Binding Decisions

| Decision | Binding direction |
| --- | --- |
| Progressive disclosure | Route from Core through one workflow and only applicable profiles/topics. |
| Normative ownership | Every retained rule has one canonical owner; indexes link without restating rules. |
| Planning artifacts | Active state remains in the plan; history, findings, reports, and durable decisions have separate owners. |
| Specialization | Root guidance stays stack-agnostic; language and application details belong in profiles. |
| Reference material | Examples, recipes, and tool versions are non-normative reference unless explicitly promoted. |
| Prompts | Repository prompts are versioned thin entrypoints into canonical standards. |
| Downstream evidence | Pantograph is one regression case, not a source of universal policy. |
| Acceptance model | Required evidence is a set of typed claims; proof kind, environment, and execution mode are independent dimensions, not a scalar hierarchy. |

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

- [x] Inventory files, normative sections, rules, links, and applicability.
- [x] Assign rule identifiers and preliminary role/disposition.
- [x] Record duplicates, conflicts, broad rules, and ownership gaps.
- [x] Capture corpus, duplication, routing, and process baselines.
- [x] Create and score the seven fixed scenarios.

**Write set:** this plan and a dedicated evaluation/report directory only.

**Gate:** Every normative section has an identifier; another reviewer can
reproduce counts, routing, and scores.

**Status:** `Accepted`

### Milestone 1: Architecture And Metadata

**Goal:** Freeze ownership and routing before moving rules.

- [x] Confirm canonical paths, metadata fields, and precedence.
- [x] Map each rule identifier to one future owner and disposition.
- [x] Resolve conflicts and define old-entrypoint migration policy.
- [x] Add valid/invalid routing metadata fixtures.

**Write set:** decision/report artifacts, metadata fixtures, and this plan.

**Gate:** Every retained rule has one proposed owner; scenarios route without
cycles or ambiguity.

**Status:** `Accepted`

### Milestone 2: Core And Router Vertical Slice

**Goal:** Prove progressive disclosure on one complete scenario.

- [x] Implement core, router, one workflow, applicable profiles, and minimum
  topics for the selected scenario.
- [x] Convert affected old entrypoints to non-duplicating indexes.
- [x] Add link, applicability, ownership, and precedence checks.
- [x] Re-run the scenario using only its routed set.

**Write set:** selected vertical path, old indexes, focused checks, and plan.

**Gate:** The scenario is correctly planned without unrelated standards, and
all retained semantics trace to inventory identifiers.

**Status:** `Accepted`

### Milestone 3: Planning And Implementation Lifecycle

**Goal:** Keep active plans current, bounded, and acceptance-oriented.

- [x] Implement the plan artifact contract and richer lifecycle.
- [x] Require one current phase, one next slice, and explicit supersession.
- [x] Define compaction/rollover triggers.
- [x] Bind `Accepted` to objective-level evidence.
- [x] Update planning/implementation standards, prompts, and templates.
- [x] Add active, blocked, accepted, and superseded fixtures.

**Write set:** planning/implementation guidance, prompts, template, fixtures,
and plan.

**Gate:** Partial or headless evidence cannot close a user-visible objective;
current status is understandable without reading history.

**Status:** `Accepted`

### Milestone 4: Verification And Release Acceptance

**Goal:** Give every verification level a distinct purpose.

- [x] Replace the scalar evidence hierarchy with typed acceptance claims.
- [x] Bind plan acceptance to complete claim sets and explicit satisfaction
  state.
- [x] Add scenario fixtures for kind, environment, mode, and smoke limits.
- [x] Consolidate focused, integration, contract, system, user-workflow,
  and release-artifact evidence definitions.
- [x] Remove universal duration and CI-only assumptions.
- [x] State that launch smoke does not prove a user feature.
- [x] Align testing, tooling, launcher, release, and plan guidance.

**Write set:** verification workflow and affected standards/templates/fixtures.

**Gate:** Every scenario selects the expected claims; incomplete or unrelated
evidence cannot satisfy a criterion.

**Slices:**

1. Canonical acceptance claims, plan integration, and scenario fixtures.
2. Testing, tooling, launcher, and release migration to the canonical owner.

**Status:** `Accepted`

### Milestone 5: Contracts, Compatibility, And Fallbacks

**Goal:** Base evolution behavior on real authority and consumer constraints.

- [x] Define the contract classification and decision record.
- [x] Add coordinated, persisted, public, distributed, generated, and degraded
  outcome fixtures.
- [x] Define policies for internal, persisted, public, and independently
  versioned contracts.
- [x] Define coordinated breaking replacement and migration expectations.
- [x] Require authority and semantic fidelity for degraded behavior.
- [x] Require typed unavailable/invalid/deferred outcomes when no valid
  decision can be made.
- [x] Reconcile affected coding, architecture, interop, persistence, release,
  and profile guidance.

**Write set:** canonical evolution topic, affected indexes/profiles, fixtures,
and plan.

**Gate:** Fixtures distinguish coordinated replacement, public versioning,
persistence migration, and invalid fallback.

**Slices:**

1. Canonical contract topic, routing, decision fixtures, and typed outcomes.
2. Remove or replace conflicting architecture, coding, persistence, interop,
   release, and binding rules.

**Status:** `Accepted`

### Milestone 6: Proportional Documentation And Commit Process

**Goal:** Preserve traceability without routine low-value work.

- [x] Require module READMEs only at meaningful boundaries.
- [x] Use concise README profiles instead of one universal template.
- [x] Tie README/ADR work to decision impact.
- [x] Link accepted rationale instead of restating it in every artifact.
- [x] Move full-history checks to milestone, pre-push, and PR boundaries while
  retaining staged-diff review per commit.
- [x] Update traceability tooling and fixtures.

**Write set:** documentation/commit/tooling standards, templates, checks,
fixtures, and plan.

**Gate:** Small changes avoid unrelated artifacts; architectural/public changes
retain durable traceability and atomic review.

**Slices:**

1. Canonical documentation workflow, profiles, templates, and decision
   fixtures.
2. Explicit staged/PR diff modes and boundary-linked ADR enforcement.
3. History-rewrite authority, hook scheduling, and milestone acceptance.

**Status:** `Accepted`

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

**Slices:**

1. Commit workflow, recipe reference, legacy index, and frozen-ID dispositions.
2. Documentation consolidation, decomposed into:
   - `7.2a` (`Accepted`): comment, Markdown, API, and algorithm reference
     material;
   - `7.2b` (`Accepted`): artifact layout, ADR, and project-README workflow
     policy; and
   - `7.2c1` (`Accepted`): establish `workflows/release.md` with release
     applicability, versioning, changelog, contract-evolution, and acceptance
     boundaries;
   - `7.2c2` (`Accepted`): migrate documentation-owned changelog identifiers
     and close the legacy documentation index.
3. Owner-bounded topic/profile consolidation with correctness fixes, including:
   - `7.3a` (`Accepted`): release artifact and packaging policy;
   - `7.3b1` (`Accepted`): pipeline mechanics
     (`STD-0552`-`STD-0560`);
   - `7.3b2` (`Accepted`): maintenance and channel policy
     (`STD-0561`-`STD-0565`);
   - `7.3b3` (`Accepted`): hosted publication and asset presentation
     (`STD-0566`-`STD-0574`);
   - `7.3b4` (`Accepted`): language-profile routing and release checklist
     (`STD-0575`-`STD-0576`);
   - `7.3c` (`Accepted`): release rollback and recovery policy
     (`STD-0577`-`STD-0581`); and
   - `7.3d` (`Accepted`): non-normative release tools, examples, and recipes
     (`STD-0541`-`STD-0542`).
4. `7.4a` (`Accepted`): decompose the remaining 698 frozen identifiers across
   33 source files into reviewable owner-bounded and correctness-ordered
   implementation slices without moving normative rules.
5. Execute the rolling waves defined by `7.4a`, beginning with:
   - `7.4b1` (`Accepted`): canonical filesystem containment and platform
     path-identity contracts (`STD-0289`-`STD-0293`,
     `STD-0584`-`STD-0587`);
   - `7.4b2a` (`Accepted`): decompose action-specific untrusted payload
     validation finding `F018` into two serial owner-bounded slices;
   - `7.4b2a1` (`Accepted`): make the decomposition checker enforce valid
     disposition-backed lifecycle handoffs across both implementation slices;
   - `7.4b2b` (`Accepted`): canonical generic runtime-decoding proof
     (`STD-0051`-`STD-0054`); and
   - `7.4b2c` (`Accepted`): canonical action-specific IPC decoding and Security
     trust-boundary linkage (`STD-0063`-`STD-0068`,
     `STD-0592`-`STD-0595`), including removal of duplicate lifecycle ownership
     from the prerequisite runtime-decoding checker; and
   - `7.4b3a` (`Accepted`): decompose critical checked-conversion, C-ABI,
     allocation, initialization, provenance, lifetime, size, and unsafe-
     contract findings `F022` and `F023` across 34 frozen identifiers and six
     serial owner-bounded slices;
   - `7.4b3b` (`Accepted`): canonical generic foreign-boundary contract
     (`STD-0465`-`STD-0472`);
   - `7.4b3c` (`Accepted`): canonical generic language-binding contract
     (`STD-0483`-`STD-0486`);
   - `7.4b3d` (`Accepted`): Rust foreign-memory proof
     (`STD-0752`-`STD-0756`);
     - integration review finding (`Resolved`): the first decision fixture gave
       missing evidence precedence over concrete malformed input; concrete
       invalidity now wins, while independently missing proof returns typed
       `unavailable`;
   - `7.4b3e` (`Accepted`): Rust checked boundary arithmetic (`STD-0823`);
     - integration review finding (`Resolved`): the first focused checker
       matched a sentence across a Markdown line boundary; the assertion now
       selects a stable semantic phrase instead of formatting;
     - coverage review finding (`Resolved`): the initial fixture named
       multiplication overflow but omitted addition overflow; both arithmetic
       paths now have explicit rejection decisions;
   - `7.4b3f` (`Accepted`): Rust unsafe proof and caller contracts
     (`STD-0843`-`STD-0848`); and
   - `7.4b3g` (`Accepted`): Rust binding representation and checked conversion
     (`STD-0772`-`STD-0775`, `STD-0794`-`STD-0796`,
      `STD-0801`-`STD-0803`).
     - coverage review finding (`Resolved`): the first focused fixture omitted
       generated wrappers and opaque-handle ownership failure; both categories
       now have explicit decisions;
     - integration review finding (`Resolved`): the first decision derivation
       required host execution for a representation already classified
       incompatible; unsupported now remains distinct unless a concrete
       fallback violation requires typed `invalid`;
     - verification review finding (`Resolved`): the first legacy-pattern
       regular expression over-escaped table separators and produced a false
       positive; exact forbidden strings now make each rejection deterministic
       and independently diagnosable;
   - `7.4b4a` (`Accepted`): supersede the premature final-closure handoff,
     audit 90 remaining trust-boundary identifiers, and insert the 26-identifier
     generic Concurrency/Rust Async lifecycle bridge required by `F025` and
     `F026`;
     - verification review finding (`Resolved`): initial report assertions
       selected prose across Markdown line boundaries and assumed filename link
       labels; the focused checker now selects stable line-local semantic
       fragments and link targets;
     - checker review finding (`Resolved`): the first group-fixture variable
       collided with Bash's special `GROUPS` array and resolved to the process
       group ID; the checker now uses an ordinary file-path variable;
     - lifecycle review finding (`Resolved`): the first checker modeled only
       the pre-implementation group counts; it now accepts only zero or all
       nine next-slice dispositions and derives the corresponding owner and
       active-plan handoff;
   - `7.4b4b` (`Accepted`): establish generic Concurrency ownership
     (`STD-0263`-`STD-0268`, `STD-0270`-`STD-0272`) and resolve `F019`;
     - generic policy now distinguishes immutable access from shared mutable
       invariants, prohibits externally controlled behavior under locks, and
       selects coordination from the invariant without mandating one lock or
       message architecture;
     - async and lifecycle work now requires nonblocking execution, explicit
       completion/failure ownership, and cancellation propagation;
     - missing coordination or lifecycle capability returns the operation's
       typed outcome without unprotected mutation, detached work, discarded
       errors, ignored cancellation, synchronous waiting, or a
       language-specific universal mechanism;
   - `7.4b4c` (`Accepted`): decompose the nine Rust Async identifiers into
     applicability, owned runtime lifecycle, blocking/mutex, and
     cancellation/observability slices; record `F045`; and fully specify only
     the first implementation slice;
   - `7.4b4d` (`Accepted`): establish the Rust Async profile and contract-driven
     sync/async boundary (`STD-0717`-`STD-0718`);
     - integration review finding (`Resolved`): the initial focused checker
       required the repository-relative profile path inside the Rust profile
       index, whose correct local link is `async.md`; routing assertions now
       distinguish root, legacy, and local-index link forms;
   - `7.4b4e` (`Accepted`): specialize runtime, tracked-task, and graceful-
     shutdown ownership (`STD-0719`-`STD-0721`);
     - verification review finding (`Resolved`): the first lifecycle assertion
       crossed a Markdown line boundary, and the affected foundation checker
       required its transition marker after the concerns became active; stable
       line-local text and an explicit ownership transition now satisfy both
       contracts without duplicating policy;
     - re-plan trigger (`Resolved`): the affected foundation checker also hard-
       codes `7.4b4e` as the next slice; changing that lifecycle assertion is
       now narrowly authorized, and sequencing remains owned by the canonical
       Rust Async decomposition checker;
     - full-regression re-plan trigger (`Resolved`): the generic concurrency
       checker hard-codes historical slice `7.4b4c` as the current next slice,
       while the new lifecycle checker would repeat that defect for `7.4b4f`;
       both mutable assertions are removed while the canonical decomposition
       checker retains sequencing ownership;
   - `7.4b4f` (`Accepted`): specialize blocking-work isolation and mutex
     selection (`STD-0722`-`STD-0723`);
     - integration finding (`Resolved`): focused evidence and the foundation
       transition marker initially crossed Markdown line boundaries; stable
       line-local wording now preserves both checker contracts;
   - `7.4b4g` (`Accepted`): specialize cancellation safety and lifecycle
     observability (`STD-0724`-`STD-0725`);
     - re-plan trigger (`Resolved`): the prior blocking/mutex checker owned the
       temporary `F045` partial-resolution row and failed when the final Rust
       Async slice resolves the finding; only that mutable assertion is removed
       and the final checker owns the resolved state;
     - handoff trigger (`Resolved`): the dependent Rust Security and Rust
       Language Bindings remainder for `F025`/`F026` is decomposed by
       `7.4b5a` before implementation;
   - `7.4b5a` (`Accepted`): decompose ten dependent Rust binding and security
     identifiers into five serial owner-bounded slices;
     - scope review keeps accepted `STD-0802` as dependency evidence without
       disposing it twice and excludes unrelated callback, packaging,
       generation, queue, and panic sections;
     - ownership review assigns host adaptation to the Rust binding profile,
       runtime/task lifecycle to the accepted Rust Async owner, generic
       filesystem authority to Security, and Rust mechanisms to the Rust
       Security profile;
     - checker review finding (`Resolved`): the parent trust/lifecycle checker
       still required historical slice `7.4b4d` to be "now" implementation-
       ready; that mutable assertion is removed, stable accepted-state and
       decomposition linkage remain, and current sequencing belongs only to
       the new decomposition checker;
   - `7.4b5b` (`Accepted`): make the Rust binding core/adapter boundary
     framework-independent (`STD-0759`, `STD-0760`, `STD-0790`, `STD-0791`);
     - domain behavior and types remain usable without a binding framework,
       generated host code, or foreign runtime;
     - adapters depend on core contracts, while binding dependencies, optional
       features, procedural macros, and generated input remain adapter/package
       scoped;
     - fifteen focused decisions reject coupled annotations, reverse
       dependencies, missing framework-free core verification, hand-edited
       generated output, layer merging, and alternate-framework fallback;
     - re-plan trigger (`Resolved`): the parent trust/lifecycle checker treated
       its accepted 90-ID/42-binding snapshot as current after dispositions;
       it now preserves that fixture as baseline evidence and derives current
       counts only from exact serial `F025`/`F026` dispositions;
     - full-suite re-plan trigger (`Resolved`): the accepted Rust Async
       lifecycle checker owned temporary `7.4b4e` statuses for `F025` and
       `F026`; those two mutable assertions are removed while all lifecycle
       behavior, disposition, legacy, and decomposition evidence remains;
   - `7.4b5c` (`Accepted`): make binding handle and async adaptation consume the
     selected runtime/lifecycle capability without retaining request inputs or
     owning an alternate runtime (`STD-0798`-`STD-0800`);
     - host handles own only their declared adapter or domain-object reference;
       runtime construction, sharing, task tracking, cancellation, and
       shutdown remain composition/lifecycle responsibilities;
     - composition-owned runtime capability may remain loaded and shared
       across calls or workflow runs without ownership transfer;
     - every call receives fresh input, cancellation, result, and failure
       state, including when a persistence or keep-alive hint retains runtime
       capability;
     - 22 focused decisions reject binding/request-owned runtimes, retained
       prior request state, synchronous driving, runtime creation, blocking,
       detached work, missing task ownership, and alternate-runtime or
       alternate-binding fallback;
     - `F025` is resolved by exact dispositions for `STD-0798` through
       `STD-0800`, bounded legacy replacement, and focused plus affected
       regression evidence;
   - `7.4b5d` (`Accepted`): canonicalize explicit typed executor delegation
     without catch-all fallback (`STD-0781`);
     - successful local completion is terminal, and only the composite
       contract's exact typed unsupported variant is eligible for one selected
       next executor;
     - delegation passes only the current call's validated input and remains
       scoped or registered with the selected lifecycle owner;
     - validation, execution, cancellation, resource, lifecycle, and
       unavailable-capability outcomes retain their original typed result;
     - 25 focused decisions reject catch-all recovery, delegation after other
       failures, retained/default input, retry, alternate-executor, and
       detached-work fallback;
   - `7.4b5e` (`Accepted`): preserve validated filesystem authority through the
     Rust operation (`STD-0822`);
     - canonical identity and containment are validation facts, while held or
       handle-relative authority preserves the validated object through use
       when concurrent mutation is possible;
     - immediate revalidation is valid only when the threat model excludes
       concurrent mutation for the complete validation/use interval;
     - 19 focused decisions reject stale/plain paths, lexical checks,
       concurrent revalidation, unanchored creation, alternate roots, and
       weaker-mechanism fallback while preserving typed outcomes;
     - `F026` remains partial only for lifecycle-owned listener work; and
   - `7.4b5f` (`Accepted`): bind listener admission, spawned work, outcomes,
     and shutdown to explicit owners (`STD-0825`);
     - listener exposure follows the service contract without a universal
       address;
     - admission capacity is owned and acquired before acceptance;
     - accepted connection work is registered with the Rust Async lifecycle
       owner, which observes success, failure, panic, and cancellation;
     - shutdown closes admission, signals cancellation, drains tracked work,
       and returns typed overload, unsupported, unavailable, or incomplete
       outcomes as applicable;
     - 26 focused decisions reject broad-bind, default-capacity, accept-first,
       detached, discarded-outcome, leaf-logging, open-admission,
       unsafe-force-abort, and alternate-runtime fallback; and
     - `F026` is resolved;
     - re-plan trigger (`Resolved`): the accepted filesystem-authority checker
       owned the temporary partial `F026` status; that mutable assertion is
       removed so the listener lifecycle checker solely owns final resolution.
   - `7.4b6` (`Accepted`): re-audit the independent trust-boundary remainder,
     confirm current owners and correctness dependencies, and activate exactly
     one owner-bounded slice without normative movement;
     - 80 undisposed trust-boundary identifiers remain across seven owner
       groups;
     - all generic owners exist; only the Rust Cross-Platform specialization
       owner remains missing in this subset;
     - unresolved `F016` and its adjacent network transport sections are the
       highest-priority active-wave correctness group;
     - the planning slice changes no normative standard, legacy section, final
       disposition, generated artifact, configuration, or downstream file;
       and
   - `7.4b7a` (`Accepted`): replace generic listener exposure, admission,
     shutdown, and liveness defaults with a contract-selected network
     transport owner (`STD-0596`-`STD-0600`);
     - exposure follows the declared service and deployment contract;
     - admission capacity is owned and acquired before accepting work;
     - accepted work registers with the selected lifecycle owner, which
       observes success, failure, and cancellation;
     - shutdown closes admission before cancellation and drain, with typed
       incomplete outcomes and force only under explicit interruption-safe
       authority;
     - liveness follows protocol semantics and resource risk rather than a
       fixed mechanism or timeout;
     - 32 focused decisions reject broad/default binding, default capacity,
       accept-first, detached/discarded/leaf-owned work, open admission,
       unsafe termination, fixed timeout/liveness, and alternate-mechanism
       fallback;
     - `F016` is resolved; and
     - re-plan trigger (`Resolved`): the historical trust/lifecycle checker
       retains frozen baseline evidence while the independent checker solely
       owns mutable independent-trust counts and owner state.
   - `7.4b7b` (`Accepted`): re-measure the 608-ID global remainder and 75-ID
     independent trust subset, then activate exactly one owner-bounded slice
     after accepted pre-slice review without normative movement;
     - the seven current owner groups contain 7 Security, 15 Cross-Platform,
       10 Interop, 5 Rust Cross-Platform, 1 Rust Interop, 3 Rust Security, and
       34 Rust Language Binding identifiers;
     - the nine-section generic Cross-Platform target/isolation group is the
       highest-priority dependency-first slice;
     - fixed product targets, Strategy/Factory, one-platform-per-file,
       runtime-only selection, and best-effort stubs are recorded as `F046`;
     - native loading, CI, Security closure, Interop, Rust specializations,
       binding packaging/generation, bounded queues, and panic remain outside
       the activated write set; and
     - the planning slice changes no normative or legacy standard, final
       disposition, generated artifact, configuration, or downstream file.
   - `7.4b7c` (`Accepted`): replace generic target, isolation, mechanism, and
     degradation defaults with a contract-selected Cross-Platform owner
     (`STD-0280`-`STD-0288`);
     - target support and evidence derive from explicit project/product/release
       contracts;
     - platform mechanics use the smallest cohesive boundary and mechanisms
       selected from language, toolchain, artifact, and deployment facts;
     - required behavior preserves semantics with typed invalid, unsupported,
       and unavailable outcomes;
     - 25 focused decisions reject fixed targets/tiers, Strategy/Factory,
       one-file-per-platform, runtime/compile-only selection, stubs, omission,
       alternate mechanisms, and weaker evidence; and
     - `F046` is resolved.
   - `7.4b7d` (`Accepted`): re-measure the 599-ID global remainder and 66-ID
     independent trust subset, then activate exactly one owner-bounded slice
     without normative movement;
     - the current groups contain 7 Security, 6 Cross-Platform, 10 Interop, 5
       Rust Cross-Platform, 1 Rust Interop, 3 Rust Security, and 34 Rust
       Language Binding identifiers;
     - the five-section Rust Cross-Platform group is the smallest
       dependency-ready slice that closes a declared missing owner;
     - fixed target triples, best-effort support, universal module/trait
       layout, numeric inline-`cfg` thresholds, and named substitute tools are
       recorded as `F047`;
     - residual cross-role owner-map conflicts and the 34-ID binding
       decomposition requirement are recorded as `F048`; and
     - the planning slice changes no normative or legacy standard, final
       disposition, generated artifact, configuration, or downstream file.
   - `7.4b7e` (`Accepted`): establish the Rust Cross-Platform specialization
     with contract-selected targets, configuration boundaries, and evidence
     (`STD-0726`-`STD-0730`);
     - target triples, support claims, artifacts, and evidence derive from the
       selected target contract;
     - `cfg`, build scripts, features, composition, dispatch, and code
       placement follow Rust/toolchain/artifact/deployment facts;
     - compile, link, package, integration, and runtime evidence remain
       distinct;
     - 30 focused decisions reject fixed triples, best-effort support,
       universal layouts, numeric thresholds, substitute tools, alternate
       targets, and weaker evidence; and
     - `F047` is resolved.
   - `7.4b7f` (`Accepted`): re-measure the 594-ID global remainder and 61-ID
     independent trust subset, then correct and activate exactly one
     owner-bounded subset of `F048` without normative movement;
     - six active owner groups remain after Rust Cross-Platform acceptance;
     - `STD-0473` is one coherent provider-governed event-registration
       lifecycle that conditionally consumes Concurrency-owned work rules only
       when callback-created work can outlive invocation, while the other nine
       generic Interop IDs remain mixed-role;
     - destruction-linked cleanup and incomplete callback/release semantics
       are recorded as `F049`; and
     - the planning slice changes no normative or legacy standard, final
       disposition, generated artifact, configuration, or downstream file.
   - `7.4b7f1` (`Accepted`): correct the event-registration implementation
     contract after rejected pre-transfer verification;
     - keep Concurrency selection conditional on callback-created work that
       can outlive invocation rather than adding an unconditional metadata
       dependency;
     - derive ordering and repeated/concurrent behavior from provider facts;
     - require lifecycle-phase-aware outcomes and independent delivery/work
       dimensions;
     - prove unrelated legacy content through staged diff and run the complete
       suite with fail-fast shell behavior; and
     - change no normative, legacy, disposition, generated, implementation-
       checker, parent-decomposition, source, configuration, or downstream
       file;
     - full-suite finding (`Resolved`): fail-fast verification exposed that the
       executor-delegation checker still requires the superseded partial
       `F026` state; the live `f497517` baseline fails identically, and `F050`
       assigns a verification-only repair before normative work.
   - `7.4b7f2` (`Accepted`): replace only the stale temporary `F026` status
     assertion in the executor-delegation checker with the accepted resolved
     state, preserve all behavioral and disposition evidence, and restore a
     green fail-fast complete suite without normative movement.
   - `7.4b7g` (`Accepted`): replace the event-subscription default with an
     explicit Interop registration lifecycle contract (`STD-0473`) that owns
     provider registration/delivery/unregistration/release/shutdown behavior
     and conditionally routes only outliving callback-created work to
     Concurrency;
     - provider delivery mode and local callback-work lifetime remain
       independent;
     - provider contracts select repeated/concurrent unregistration outcomes
       and valid delivery, quiescence, release, and shutdown order;
     - lifecycle phase distinguishes pre-registration `unavailable` from
       active-resource incomplete cleanup;
     - review findings (`Resolved`): fallback attempts preserve the root phase
       diagnostic; evidence records complete selected and observed lifecycle
       sequences with quiescence before release and ties repeated/concurrent
       outcomes to selected provider contracts;
     - 43 focused decisions reject destruction/finalizer/garbage-collection
       cleanup, carry-forward input, detached work, stale registration,
       arbitrary-thread retry, alternate events, assumed idempotence,
       universal ordering, and false cleanup success;
     - `STD-0473` has one exact disposition and `F049` is resolved.
   - `7.4b7h` (`Accepted`): re-measure the 593-ID global and 60-ID independent
     trust remainder, correct the next residual owner boundary, and activate
     exactly one dependency-ready implementation slice without normative
     movement;
     - the 61-ID group fixture is a frozen baseline that includes accepted
       `STD-0473`; its count is no longer mislabeled as entirely remaining;
     - independent review rejects a six-ID Security proposal because it still
       mixes Core, Contracts, Security, implementation structure, and
       decomposable validation rules;
     - `STD-0757` is corrected from Rust Interop to Rust Language Binding
       ownership because it defines a serialized Rust/host representation;
     - the selected owner and its Contracts, generic Language Binding, Rust,
       and Verification prerequisites already exist;
     - implicit Serde shape, casing, tagging, generation, and producer-only
       evidence assumptions are recorded as `F051`; and
     - review findings (`Resolved`): planning requires zero premature
       dispositions, current audit counts are unambiguous, missing Rust API
       and Tooling owners are fixture-verified, and the report link names the
       current handoff;
     - the planning slice changes no normative or legacy standard, final
       disposition, generated artifact, configuration, or downstream file.
   - `7.4b7i` (`Accepted`): establish the Rust Language Binding contract for a
     selected Serde schema, complete attribute-derived wire shape, consumer
     agreement, typed outcomes, and native/host evidence for `STD-0757`;
     - the canonical contract derives effective tags, content, names, casing,
       optionality, variants, and fields from the selected schema, serializer,
       and applicable Serde attributes;
     - native/host agreement and typed invalid, unsupported, and unavailable
       outcomes replace implicit defaults and producer-only evidence;
     - the legacy Serde section is a bounded canonical link, and `F051` is
       resolved with one exact Rust Language Binding disposition.
   - `7.4b7j` (`Accepted`): re-measure the 592-ID global remainder across 28
     sources and 27 owners, plus the 59-ID independent-trust remainder;
     correct exactly one next owner boundary; and activate only one
     dependency-ready implementation slice without normative movement;
     - accepted baseline IDs are fixture-owned rather than encoded as
       owner-specific checker subtraction;
     - `STD-0824` is selected for Rust Security because external-input queue
       resource limits, overload outcomes, retention/rejection semantics, and
       telemetry are one cohesive operation contract;
     - `STD-0821` remains index closure and `STD-0826` remains blocked on the
       missing Rust API owner; and
     - `F052` records the legacy queue's fixed-capacity and drop-oldest
       assumptions without selected operation facts or typed outcomes.
   - `7.4b7k` (`Accepted`): establish the Rust Security contract for selected
     external-input queue resource limits, overload behavior, telemetry, typed
     outcomes, and operation evidence for `STD-0824`; fixed capacity,
     drop-oldest, silent discard, alternate mechanism, prior-input, and weaker
     evidence fallbacks are rejected, and `F052` is resolved.
   - `7.4b7l` (`Accepted`): re-measure the 591-ID global and 58-ID independent
     trust remainders and correct exactly one next owner boundary without
     normative movement;
     - `STD-0583` and `STD-0601` are one Contracts-owned proof-lifetime
       contract, while Security retains untrusted-input consequences;
     - `STD-0821` remains final index closure and `STD-0826` remains blocked on
       the missing Rust API owner; and
     - `F053` records the unsafe absolute validate-once/trust-internally rule.
   - `7.4b7m` (`Accepted`): establish the Contracts-owned validation
     proof-lifetime contract for `STD-0583` and `STD-0601`, including explicit
     proof invalidation and no stale/raw-input fallback;
     - authority follows the intact validated representation rather than
       validation history;
     - changed contracts, unchecked mutation, representation loss, and new
       applicable boundaries require current proof; and
     - 16 focused decisions resolve `F053`.
   - `7.4b7n` (`Accepted`): replace alternating planning/implementation
     commits with the verified 589-ID execution train;
     - 47 contiguous source/owner clusters cover every remaining identifier
       exactly once across five dependency waves;
     - each cluster requires a bounded pre-slice review, one atomic commit,
       focused evidence, and serial updates to shared planning records;
     - separate planning-only commits occur only when a declared re-plan
       trigger fires;
     - the complete checker suite runs at five wave checkpoints and whenever a
       shared contract, checker infrastructure, routing, metadata, or generated
       artifact changes; and
     - non-overlapping owner-specific drafts may proceed in parallel, while
       shared contracts, fixtures, dispositions, plans, and ledgers remain
       serial integration-owner work.
   - `7.4b8a` (`Planned`): review and, when the owner boundary is accepted,
     implement the `STD-0588`-`STD-0591` Security validation cluster in one
     atomic slice; a failed owner review triggers manifest correction instead
     of preserving the proposed move.
6. `7.4c` (`Planned`): perform final legacy-index review, disposition closure,
   and duplication verification only after the rolling remainder reaches zero
   and every required canonical owner exists.

**Status:** `Active`

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

**Status:** `Planned`

## Blockers

- None.

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

## Re-Plan Triggers

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

## Final Acceptance

- **Objective evidence:** Pending Milestone 8 scenario comparison, downstream
  pilots, migration publication, and manual review.
- **Deferred follow-ups:** None beyond milestones explicitly marked `Planned`.
- **Final status:** `Active`
