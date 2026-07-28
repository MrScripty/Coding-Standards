# Standards Effectiveness Execution Ledger

## 2026-07-28: Milestone 0 Baseline And Fixtures

**Outcome:** Accepted.

**Write set:**

- `evaluation/standards-effectiveness/`
- `plans/standards-library-effectiveness-restructure-plan.md`

**Delivered:**

- frozen 40-artifact corpus manifest at baseline commit `6b4df85`;
- reproducible file metrics and 916-section inventory;
- snapshots and hashes for three ignored local-only prompts;
- seven product-neutral evaluation scenarios;
- fixed scoring rubric and 43/126 baseline score;
- ten duplicate-ownership clusters;
- thirty systemic, correctness, safety, and ownership findings; and
- preliminary role/disposition for every current guidance artifact.

**Deviations:**

- The plan assumed prompts were repository artifacts. They are ignored by
  `.gitignore`; baseline snapshots preserve evidence, and F001 assigns the
  versioning decision to Milestones 1 and 3.
- The earlier approximate imperative count used a broader search. The
  reproducible generator defines and records 352 all-corpus and 321
  normative/derived occurrences.

**Verification:**

- Baseline generator completed against the frozen commit.
- Repeated generation produced identical output content.
- Every manifest source resolved from Git or a frozen snapshot.
- Section IDs are unique and contiguous through `STD-0916`.
- Seven fixture scenarios and nine rubric dimensions are present.
- `bash -n` accepted the generator and existing traceability script.
- Markdown and staged-diff whitespace checks passed.

**Commit:** `docs(evaluation): freeze standards effectiveness baseline`

## 2026-07-28: Milestone 1 Architecture And Metadata

**Outcome:** Accepted.

**Write set:**

- `evaluation/standards-effectiveness/`
- `plans/standards-library-effectiveness-restructure-plan.md`

**Delivered:**

- six-role information architecture and canonical target paths;
- deterministic routing and precedence rules;
- one-major-version old-entrypoint migration policy;
- decision to version thin prompts and remove machine-specific local prompts;
- fixed module metadata schema;
- positive and negative metadata fixtures;
- metadata checks for fields, enums, path ownership, duplicate IDs,
  dependencies, self-dependencies, and cycles; and
- generated proposed canonical owners for all 916 section identifiers.

**Deviations:**

- File-level mapping was insufficient for the mixed architecture catalog.
  Section overrides assign contracts, IPC, documentation, diagnostics,
  persistence, resilience, and HTTP contracts to distinct proposed owners.
- A zero-heading local prompt has no section ID; it remains covered by the
  corpus-level owner map and prompt versioning decision.

**Verification:**

- Owner-map generation produced 916 unique, non-empty assignments.
- Metadata positive fixtures passed.
- Invalid level, missing owner, wrong owner, self-dependency, missing
  dependency, duplicate ID, and dependency-cycle fixtures failed as expected.
- Shell syntax and whitespace checks passed.

**Commit:** `docs(architecture): freeze standards routing contract`

## 2026-07-28: Milestone 2 Core And Router Vertical Slice

**Outcome:** Accepted.

**Scenario:** S1 small local bug fix in a Rust library.

**Write set:**

- `CORE-STANDARDS.md`
- `STANDARDS-ROUTER.md`
- `workflows/implementation.md`
- `workflows/verification.md`
- `profiles/applications/library.md`
- `profiles/languages/rust/README.md`
- affected root, coding, testing, language, and Rust entrypoints
- S1 routing fixture and verifier
- evaluation ledger/README and active plan

**Delivered:**

- concise universal Core;
- deterministic Router with inclusion and exclusion conditions;
- bounded implementation and objective-aligned verification workflows;
- library and Rust profiles;
- explicit migration authority for overlapping old entrypoints; and
- executable S1 routed-set and context-size verification.

**No-fallback/legacy result:**

- No compatibility shim or alternate behavior path was added.
- New modules are canonical for moved rules.
- Existing documents retain ownership only for rules not yet moved and state
  that boundary explicitly.
- Unknown applicability requires a routing diagnostic rather than a default.

**Deviation:**

- The first S1 verifier over-escaped a basic `sed` capture and produced an
  empty ID set. The parser was corrected before repository integration; the
  metadata contract itself had passed.

**Verification:**

- All six selected modules passed metadata validation.
- Expected and actual module IDs matched.
- Routed context measured 520/11,066 baseline lines (4.7%).
- Root README no longer requires reading every document.
- Shell syntax, whitespace, link, and staged-scope checks passed.

**Commit:** `docs(core): add first routed standards path`

## 2026-07-28: Milestone 3 Planning And Implementation Lifecycle

**Outcome:** Accepted.

**Write set:**

- planning and implementation workflows;
- Router and legacy planning entrypoint;
- plan template;
- versioned prompts and `.gitignore`;
- plan lifecycle fixtures/checks;
- evaluation README, ledger, findings, and active plan.

**Delivered:**

- separate active plan, execution ledger, issues, reports, and ADR ownership;
- `Planned`, `Active`, `Blocked`, `Implemented`, `Verifying`, `Accepted`,
  `Deferred`, and `Superseded` lifecycle;
- exactly one current phase and next slice;
- objective/evidence level comparison for acceptance;
- decision replacement, supersession, and plan compaction;
- bounded findings and delegated write-set contracts;
- concise canonical plan template;
- versioned planning, implementation, and full-review prompts; and
- positive/negative lifecycle fixtures.

**No-fallback/legacy result:**

- `PLAN-STANDARDS.md` is now a nonnormative migration index.
- The old three-state template and plan-as-history model were replaced, not
  retained as alternate behavior.
- Re-planning replaces binding decisions; it does not carry old behavior
  forward implicitly.

**Deviations:**

- The first fixture checker counted `## Objective Acceptance` as a second
  `## Objective`; exact whole-line heading matching fixed the checker before
  integration.

**Verification:**

- Planning and implementation modules passed metadata/dependency checks.
- Active, blocked, accepted, and superseded fixtures passed.
- Three-state, missing-next-slice, embedded-history, and headless-acceptance
  fixtures failed as expected.
- The canonical plan template passed the structure check.
- Shell syntax, links, whitespace, and staged-scope checks passed.

**Commit:** `docs(planning): replace append-only plan lifecycle`

## 2026-07-28: Milestone 4.1 Acceptance Claims And Plan Integration

**Outcome:** Accepted.

**Re-plan trigger:**

- Milestone 3 provisionally ranked `manual`, `environment`, and `release`
  evidence above behavior-oriented levels.
- Those values represent execution mode, environment qualification, and proof
  target rather than one comparable strength hierarchy.
- The active plan was revised before implementation to use typed claim sets.

**Write set:**

- verification and planning workflows;
- plan template and lifecycle checker/fixtures;
- acceptance claim fixtures/checker;
- evaluation README, ledger, findings, and active plan.

**Delivered:**

- canonical evidence kinds for focused, integration, contract, system,
  user-workflow, and release-artifact claims;
- independent environment and execution-mode qualifiers;
- plan acceptance states `pending`, `partial`, `blocked`, and `satisfied`;
- explicit smoke-check limits and unavailable-evidence behavior; and
- fixed scenario cases proving that every required claim must match.

**No-fallback/legacy result:**

- The scalar evidence rank was removed rather than retained as an alternate
  acceptance path.
- Supporting checks cannot substitute for missing objective claims.
- Simulated or startup-smoke evidence cannot silently stand in for required
  hardware or user-workflow evidence.

**Verification:**

- Plan lifecycle positive and negative fixtures passed.
- Canonical template and active restructure plan passed structure checks.
- All seven scenario claim cases passed.
- Startup-smoke, simulated-hardware, and manual-as-higher regressions were
  rejected as expected.
- Verification and planning metadata/dependency checks passed.
- Shell syntax, whitespace, and staged-scope checks passed.

**Commit:** `docs(verification): model acceptance as typed claims`
