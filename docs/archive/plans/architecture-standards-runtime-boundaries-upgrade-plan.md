# Plan: Architecture Standards Runtime Boundaries Upgrade

## Objective

Upgrade the standards library so it gives clearer, stack-agnostic guidance for
monorepo package boundaries, executable shared contracts, composition roots,
long-lived realtime workflow systems, and test placement strategy.

## Scope

### In Scope

- Add a monorepo package roles pattern to the standards.
- Add executable contract guidance for shared schemas at process, network, and
  storage boundaries.
- Add a composition root plus service contract module pattern.
- Add a realtime workflow systems pattern covering idempotency, replay,
  projections, and failure reconciliation.
- Relax testing guidance so colocated tests are explicitly allowed when used
  consistently.
- Update cross-references so the new guidance is discoverable from the repo
  README and affected standards documents.

### Out of Scope

- Rewriting the full standards library around one specific architecture style.
- Adding framework-specific DI guidance for Effect, React, Nest, Spring, etc.
- Mandating monorepos for all downstream projects.
- Retrofitting downstream repositories that already copied older standards.
- Adding new automation/scripts unless gaps appear during standards updates.

## Inputs

### Problem

The current standards capture the right high-level ideas around layering,
contracts, and backend-owned state, but they are less concrete than the better
parts of `t3code` in the areas of package role boundaries, runtime-validated
contracts, composition roots, and resilient orchestration/event-flow design.
The testing standard is also stricter than many healthy TypeScript monorepos by
implying a `tests/`-mirror structure rather than allowing consistent colocated
tests.

### Constraints

- Standards must remain stack-agnostic and reusable outside TypeScript.
- New rules must describe roles and responsibilities, not force specific folder
  names or frameworks.
- Guidance must stay concise enough to copy into real projects without turning
  into architecture theory.
- Existing standards should be extended rather than duplicated.

### Assumptions

- `ARCHITECTURE-PATTERNS.md` remains the main home for cross-layer design
  patterns.
- `CODING-STANDARDS.md` remains the home for repo/file organization rules.
- `TESTING-STANDARDS.md` remains the home for test placement and verification
  guidance.
- A small README update is sufficient for discoverability; no new top-level
  standards document is required.

### Dependencies

- `ARCHITECTURE-PATTERNS.md`
- `CODING-STANDARDS.md`
- `TESTING-STANDARDS.md`
- `README.md`
- `PLAN-STANDARDS.md` for plan structure

### Risks

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| New sections duplicate existing layering guidance | Medium | Add focused subsections and cross-references instead of parallel doctrine. |
| Package-role guidance drifts into stack-specific folder prescriptions | Medium | Phrase rules in terms of responsibilities, allowed contents, and dependency direction. |
| Realtime workflow guidance becomes too advanced for simpler projects | Medium | Mark it as an optional pattern for systems with durable commands/events/process restarts. |
| Relaxing test placement guidance reduces consistency | Medium | Require one declared strategy per repo or package and show acceptable patterns. |
| Standards become harder to skim | Medium | Keep examples short and place detail only where it changes design decisions. |

## Clarifying Questions (Only If Needed)

- None at this time.

## Definition of Done

- The standards explicitly describe monorepo package roles and dependency rules.
- The standards distinguish shared compile-time types from executable boundary
  contracts with runtime validation guidance.
- The standards describe a composition root pattern and service contract module
  split without tying it to one DI library.
- The standards include a reusable pattern for resilient realtime workflow
  systems with commands, events, projections, replay, and reconciliation.
- The testing standards explicitly allow colocated tests as a first-class option
  when the repo stays consistent.
- Cross-references and top-level README text make the new guidance discoverable.

## Milestones

### Milestone 1: Add Monorepo Package Roles Guidance

**Goal:** Make package boundaries enforce architectural intent, not just folder
organization.

**Tasks:**
- [x] Add a "Monorepo Package Roles" section to `ARCHITECTURE-PATTERNS.md` or
      `CODING-STANDARDS.md` with generic role categories such as app,
      contracts, domain/core, shared utilities, and tooling/config.
- [x] Define allowed contents, forbidden contents, and dependency direction for
      each role.
- [x] Add a short example showing why cross-app imports of implementation
      details are worse than depending on a shared contracts package.
- [x] Cross-reference the section from `README.md`.

**Verification:**
- Manual review to confirm the guidance is stack-agnostic and does not require a
  specific monorepo tool.
- Manual consistency check against existing layering rules in
  `ARCHITECTURE-PATTERNS.md` and `CODING-STANDARDS.md`.

**Status:** Complete

### Milestone 2: Add Executable Contracts Guidance

**Goal:** Make the standards explicit that cross-boundary contracts should often
be runtime-checked artifacts, not only compile-time interfaces.

**Tasks:**
- [x] Extend `ARCHITECTURE-PATTERNS.md` with an "Executable Contracts" section
      covering request/response payloads, IPC messages, persisted artifacts, and
      shared IDs/enums.
- [x] Clarify when plain shared types are sufficient and when runtime-validated
      schemas are preferable.
- [x] Add guidance for preserving semantic compatibility, defaults, and branded
      identifiers across boundaries.
- [x] Add a concise note or cross-reference in `SECURITY-STANDARDS.md` or
      `CODING-STANDARDS.md` only if needed to avoid duplicated validation rules.

**Verification:**
- Manual review to confirm the new section complements existing immutable and
  structured producer-consumer contract guidance rather than restating it.
- Check examples stay technology-neutral.

**Status:** Complete

### Milestone 3: Add Composition Root and Service Contract Pattern

**Goal:** Show how to keep wiring concerns separate from service interfaces and
implementations.

**Tasks:**
- [x] Add a section to `ARCHITECTURE-PATTERNS.md` describing a composition root
      that assembles infrastructure and service implementations at the app
      boundary.
- [x] Define a service contract module pattern: public interface/facade in one
      module, concrete implementation in another, with consumers depending on
      the contract.
- [x] Add rules for where lifecycle ownership belongs for processes, sockets,
      timers, or background workers.
- [x] Add a small coding cross-reference if folder/module placement needs to be
      reinforced in `CODING-STANDARDS.md`.

**Verification:**
- Manual review to confirm the pattern works for DI frameworks and for manual
  constructor/wiring approaches.
- Confirm the lifecycle guidance does not conflict with existing single-owner
  stateful flow rules.

**Status:** Complete

### Milestone 4: Add Realtime Workflow Systems Pattern

**Goal:** Give durable guidance for systems that process commands/events across
restarts, reconnects, and partial failures.

**Tasks:**
- [x] Add an optional "Realtime Workflow Systems" section to
      `ARCHITECTURE-PATTERNS.md`.
- [x] Cover command idempotency, append-only event storage, read-model
      projections, replay/bootstrap, and reconciliation after failed dispatch.
- [x] Add guidance for separating transport concerns from orchestration/domain
      workflow concerns.
- [x] Add verification guidance or cross-references in `TESTING-STANDARDS.md`
      for replay, dedupe, recovery, and cross-layer acceptance checks.

**Verification:**
- Manual review to ensure the section is framed as an optional pattern for
  systems that need it, not a default requirement for CRUD apps.
- Manual cross-check with `CONCURRENCY-STANDARDS.md` and current
  cross-layer acceptance guidance.

**Status:** Complete

### Milestone 5: Relax and Clarify Test Placement Strategy

**Goal:** Allow healthy colocated test structures without losing consistency.

**Tasks:**
- [x] Update `TESTING-STANDARDS.md` so "mirror source structure" becomes one
      valid strategy rather than the implied default for every repo.
- [x] Add explicit acceptable strategies: colocated tests, separate `tests/`
      trees, or hybrid patterns with package-level consistency.
- [x] Define selection criteria for each strategy based on language, tooling,
      package count, and module discoverability.
- [x] Preserve existing cross-layer acceptance expectations while clarifying that
      placement is separate from verification depth.

**Verification:**
- Manual review to confirm the standard still demands consistency and clear
  conventions rather than arbitrary placement.
- Confirm examples do not contradict existing unit/integration/e2e guidance.

**Status:** Complete

### Milestone 6: Cross-Reference and Editorial Pass

**Goal:** Keep the standards library coherent after the additions.

**Tasks:**
- [x] Update `README.md` document descriptions if any standard now covers
      meaningfully broader ground.
- [x] Add or tighten cross-links between architecture, coding, testing,
      concurrency, and security standards where the new sections overlap.
- [x] Run a final editorial pass to remove duplicated wording and keep the new
      material concise.

**Verification:**
- Manual consistency pass across all touched docs.
- Markdown preview or direct read-through to confirm headings and references are
  navigable.

**Status:** Complete

## Execution Notes

Update during implementation:
- 2026-03-07: Plan created from comparison of the standards repo against
  `/media/jeremy/OrangeCream/Linux Software/t3code`.
- 2026-03-07: Milestone 1 architecture guidance drafted in
  `ARCHITECTURE-PATTERNS.md`; README cross-reference deferred to final
  editorial pass.
- 2026-03-07: Milestone 2 executable contract guidance added to
  `ARCHITECTURE-PATTERNS.md`; no extra coding/security cross-reference needed.
- 2026-03-07: Milestone 3 composition root guidance added to
  `ARCHITECTURE-PATTERNS.md` with a supporting cross-reference in
  `CODING-STANDARDS.md`.
- 2026-03-07: Milestone 4 realtime workflow architecture guidance added to
  `ARCHITECTURE-PATTERNS.md`; testing-specific follow-through deferred to the
  testing milestone.
- 2026-03-07: Milestones 4 and 5 completed in `TESTING-STANDARDS.md` with test
  placement strategy guidance plus replay/recovery verification expectations.
- 2026-03-07: Milestones 1 and 6 closed with README discoverability updates and
  a final cross-reference/editorial pass.

## Commit Cadence Notes

- Commit after each completed milestone or after a tightly related pair of small
  milestones if the changes are easier to review together.
- Keep document-only commits atomic and traceable by topic.
- Follow `COMMIT-STANDARDS.md` for commit formatting and history cleanup.

## Optional Subagent Assignment

| Owner/Agent | Scope | Output Contract | Handoff Checkpoint |
| ----------- | ----- | --------------- | ------------------ |
| N/A | N/A | N/A | N/A |

## Re-Plan Triggers

- A new section clearly belongs in a new standards document rather than an
  existing one.
- Cross-document duplication grows beyond a small amount of shared terminology.
- During drafting, one milestone reveals that another should be merged or split
  for clarity.
- Review shows the new guidance is no longer stack-agnostic.

## Recommendations (Only If Better Option Exists)

- Recommendation: Implement milestones 1-4 in `ARCHITECTURE-PATTERNS.md` first,
  then adjust `CODING-STANDARDS.md`, `TESTING-STANDARDS.md`, and `README.md`.
  This keeps the core design vocabulary stable before editing supporting docs
  and reduces rewrite churn.

## Completion Summary

### Completed

- Milestone 1: Added monorepo package role guidance and README discoverability.
- Milestone 2: Added executable boundary contract guidance.
- Milestone 3: Added composition root and service contract guidance.
- Milestone 4: Added durable realtime workflow guidance and related verification expectations.
- Milestone 5: Updated testing standards to allow colocated, mirrored, and hybrid placement strategies.
- Milestone 6: Completed cross-reference and editorial pass across touched documents.

### Deviations

- None.

### Follow-Ups

- None.

### Verification Summary

- Manual review against `PLAN-STANDARDS.md`.
- Manual comparison against current standards documents and the referenced
  `t3code` design patterns.
- Manual read-through of `README.md`, `ARCHITECTURE-PATTERNS.md`,
  `CODING-STANDARDS.md`, and `TESTING-STANDARDS.md` for consistency.

### Traceability Links

- Module README updated: N/A
- ADR added/updated: N/A
- PR notes completed per `templates/PULL_REQUEST_TEMPLATE.md`: Pending future
  PR creation

## Brevity Note

The plan stays concise and expands only where sequencing, scope, or risks would
materially affect implementation.
