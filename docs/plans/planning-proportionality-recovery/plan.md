# Plan: Planning Proportionality Recovery

**Plan status:** `Active`

**Current phase:** Milestone 3: historical-authority migration

**Next slice:** complete `PPR-C2` in the exact retained shell entrypoints that
combine active-plan history with obsolete orchestration or duplicated
plan-structure gates, preserving their non-plan behavior

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Restore a proportional planning architecture in which ordinary plans require no
unsupported transition protocol, concurrent stale-state protection is routed
only when its precise applicability conditions hold, and active plans contain
current authority rather than historical verification data.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | An ordinary written plan requires an explicit path, operation, lifecycle state, bounded work, and serial shared-authority ownership without requiring a digest or transition envelope. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A2 | A concurrent-plan-integration profile has tested inclusion and exclusion cases and applies only when outstanding proposals can become stale before integration. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A3 | Machine-protocol requirements update every affected representation and executable surface; review-only semantic policy does not acquire unnecessary tooling. | `contract` | `not-applicable` | `review-and-automated` | `pending` | pending |
| A4 | No verifier treats accepted historical narration in an active plan as canonical authority. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A5 | Migration lifecycle derives from canonical package, disposition, lifecycle, or evidence records rather than duplicated active-plan prose. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A6 | The parent and verification-engine plans contain only current decisions, milestone state, blockers, next work, acceptance state, and evidence links; displaced history remains available. | `contract` | `not-applicable` | `review-and-automated` | `pending` | pending |
| A7 | Declarative verification, the retained mixed checkpoint, scenario rescoring, and an ordinary-plan downstream pilot pass without invented transition tooling. | `system` | `downstream-repository` | `automated-and-manual` | `pending` | pending |

## Scope

### In Scope

- Generic Planning applicability, admission, lifecycle, and artifact ownership.
- A conditionally routed concurrent-plan-integration profile.
- Non-normative reference material for concrete revision mechanisms.
- Router, prompt, template, fixture, and verifier projections affected by the
  corrected contracts.
- Active-plan consumer migration and compaction of the parent and
  verification-engine plans.
- Scenario rescoring and one downstream ordinary-plan pilot.

### Out Of Scope

- A universal cryptographic transition protocol.
- A scheduler, queue, lease, journal, or distributed transaction manager.
- Requiring executable enforcement for semantic policies that remain
  review-based.
- Resuming source-index or other Bash-checker migrations before this recovery
  is accepted.
- Unrelated standards-policy changes.

## Constraints And Assumptions

### Constraints

- Generic Planning keeps explicit plan identity and operation; no scanning,
  recency, conversation-state, or latest-state fallback is introduced.
- The concurrent profile is mandatory when its applicability condition is met
  and does not apply merely because several people or agents participate.
- Diagnostics require distinguishable semantic classifications, not a specific
  serialized runtime type.
- Historical authority moves before plan prose is removed; compaction cannot
  weaken an accepted contract.
- Canonical tables derive migration status. The recovery adds no manually
  synchronized counts or duplicate status summaries.
- Active plans, Router, shared fixtures, suite registry, generated artifacts,
  and this plan remain serial integration-owner files.

### Assumptions

- Existing package, disposition, lifecycle, ledger, report, and suite records
  can own every legitimate historical claim currently read from active plans.
- Concrete revision mechanisms can remain implementation-selected unless a
  routed profile prescribes a supported machine protocol.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Keep generic Planning limited to broadly applicable plan identity, operation, lifecycle, current state, bounded work, and serial shared-authority integration. | `workflow.planning` | Unsupported universal transition protocol and ordinary-plan usability requirement | Universal revision-bound transition mechanism |
| Route concurrent integration only when two or more proposals may be prepared from the same mutable plan revision before integration and correctness depends on detecting intervening plan or shared-authority change. | Concurrent-plan-integration profile | Applicability review | Broad “multiple writers” trigger |
| Exclude serial collaboration, read-only reports, non-authorizing investigations, non-stale independent work, and one current-state integration owner with no outstanding proposals. | Concurrent-plan-integration profile | Applicability review | Participant-count inference |
| Require machine support only when a normative rule prescribes a machine protocol, concrete representation, or automated gate; otherwise update only affected distribution and enforcement surfaces. | Owning standard | Projection-completeness review | Universal tooling requirement for every normative rule |
| Keep diagnostics semantically distinguishable while allowing manual records and tools to use representations appropriate to their medium. | Owning workflow/profile | Manual and automated consumers | Mandatory serialized diagnostic representation |
| Prohibit active-plan narration from owning historical verification claims. | `workflow.planning` | Current plan and checker-consumer audit | Active plan as append-only execution database |
| Compact through authority migration and structural ownership, not a hardcoded line limit. | This plan | Derived-data and maintenance constraints | Numeric plan-size gate |
| Resume the selected source-index generalization only after this recovery is accepted. | Verification-engine plan | Dependency sequencing | Immediate option-3 implementation |

## Simplicity And Ownership Review

- Independent concepts: generic plan admission, concurrent stale-state
  protection, mechanism examples, current plan state, and historical evidence.
- Intentional coupling: Router applicability selects the concurrent profile;
  machine protocols align their templates, prompts, fixtures, and executable
  support.
- Accidental coupling risk: participant count selecting concurrency, active
  prose becoming fixture authority, or reference mechanisms becoming normative.
- Policy/state/lifecycle owners: Planning owns generic workflow; the concurrent
  profile owns stale-proposal coordination; active plans own current state;
  ledgers and reports own history; canonical tables own migration lifecycle.
- Future changes that remain independent: changing a concrete revision
  mechanism, adding a planning semantic rule, and adding a new migration suite.

## Milestones

### Milestone 0: Recovery Authority And Freeze

**Goal:** Establish one concise recovery plan and stop new verifier-migration
admissions without changing normative policy.

**Allowed write set:**

- `docs/plans/planning-proportionality-recovery/plan.md`
- `docs/plans/planning-proportionality-recovery/execution-ledger.md`
- `docs/plans/planning-proportionality-recovery/issues.md`
- `docs/plans/standards-verification-engine/plan.md`
- `plans/standards-library-effectiveness-restructure-plan.md`

**Tasks:**

- [x] Record the approved Option 3 architecture and refinements.
- [x] Freeze new verifier-migration admissions.

**Acceptance gate:**

- Recovery plan structure passes and both upstream plans identify this recovery
  as the current dependency.

**Status:** `Accepted`

### Milestone 1: Consumer And Authority Inventory

**Goal:** Account exactly for every check that consumes active-plan content and
separate current-structure checks from historical-prose dependencies.

**Allowed write set:**

- This plan directory.
- `evaluation/standards-effectiveness/` inventory and report artifacts approved
  by the slice.
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-nodes.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-edges.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-components.tsv`

**Tasks:**

- [x] Derive direct and transitive active-plan consumers.
- [x] Classify every consumed claim by semantic purpose.
- [x] Assign one canonical replacement authority or retirement disposition.
- [x] Prove exact inventory coverage without manually maintained counts.

**Acceptance gate:**

- Every historical-plan claim has exactly one reviewed disposition and no
  normative or executable file changes have begun. Generated migration
  observations are current and confer no execution, dependency, ownership, or
  acceptance authority.

**Status:** `Accepted`

### Milestone 2: Planning Contract Split

**Goal:** Correct generic Planning and introduce the precisely routed concurrent
profile and non-normative mechanism reference.

**Allowed write set:**

- `workflows/planning.md`
- `profiles/` profile path approved by Milestone 1
- `reference/` recipe path approved by Milestone 1
- `STANDARDS-ROUTER.md`
- Affected prompts, templates, fixtures, suites, metadata, and disposition files
  identified before the slice.

**Tasks:**

- [x] Remove universal mechanism requirements from generic Planning.
- [x] Add tested concurrent-profile inclusion and exclusion conditions.
- [x] Preserve semantic stale, invalid, unavailable, unsupported, conflicting,
  and dependency-blocked outcomes.
- [x] Align only affected distribution and enforcement surfaces.

**Acceptance gate:**

- Positive and negative routing scenarios pass; an ordinary plan requires no
  unsupported transition fields; no old universal protocol remains normative.

**Status:** `Accepted`

### Milestone 3: Historical-Authority Migration

**Goal:** Move every accepted historical claim out of active-plan narration and
change its consumers to canonical records.

**Allowed write set:**

- Exact consumer, suite, fixture, package, disposition, lifecycle, evidence,
  and generated paths admitted from the Milestone 1 inventory.
- This plan and ledger.

**Tasks:**

- [x] Remove all `PPR-C1` declarative active-plan checks while preserving their
  current owner, fixture, disposition, package, and decision checks.
- [x] Remove plain historical assertions from every `PPR-C2` entrypoint whose
  active-plan consumption has no orchestration or structure-gate control flow.
- [ ] Remove active-plan consumption from the remaining `PPR-C2` entrypoints
  with obsolete orchestration or duplicated plan-structure gates.
- [x] Keep shared authority under serial integration.

**Acceptance gate:**

- No checker or declarative suite depends on accepted historical narration in
  either active plan.

**Status:** `Active`

### Milestone 4: Active-Plan Compaction

**Goal:** Replace both active plans with concise current-state indexes while
preserving all displaced history through links to canonical evidence.

**Allowed write set:**

- `plans/standards-library-effectiveness-restructure-plan.md`
- `docs/plans/standards-verification-engine/plan.md`
- Their ledgers, issues, and reports when required by reviewed dispositions.
- Planning structure verification affected by compaction ownership.

**Tasks:**

- [ ] Compact milestone history into current-state tables and evidence links.
- [ ] Remove duplicated accepted-slice narratives.
- [ ] Verify displaced evidence remains reachable and authoritative.

**Acceptance gate:**

- Structural and semantic review confirms that both plans expose current
  authority without historical narration or lost evidence.

**Status:** `Planned`

### Milestone 5: Acceptance And Downstream Pilot

**Goal:** Prove the corrected architecture and resume verifier migration from a
clean, usable planning boundary.

**Allowed write set:**

- Recovery evidence and scenario results.
- A bounded downstream pilot report.
- Current-state fields in affected plans.

**Tasks:**

- [ ] Run declarative and retained mixed checkpoints.
- [ ] Rescore planning scenarios.
- [ ] Run one ordinary-plan downstream pilot without transition tooling.
- [ ] Re-admit the selected source-index generalization from fresh state.

**Acceptance gate:**

- A1 through A7 are satisfied with linked evidence.

**Status:** `Planned`

## Blockers

- `none`

## Re-Plan Triggers

- A historical-plan claim has no canonical replacement authority.
- The concurrent profile cannot express stale-state protection without a
  universally mandated mechanism.
- Profile routing overlaps generic Planning or runtime Concurrency ownership.
- Compaction would remove evidence before all consumers migrate.
- Affected distribution or enforcement surfaces cannot be derived reliably.
- Downstream ordinary-plan adoption still requires invented protocol fields.

## Concurrent Work

No writes are currently delegated. Independent consumer analysis may run
concurrently after non-overlapping report paths are declared. Shared suites,
fixtures, generated artifacts, and active plans remain serial.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Active`
