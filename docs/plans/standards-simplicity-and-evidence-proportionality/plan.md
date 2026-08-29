# Plan: Standards Simplicity And Evidence Proportionality

**Plan status:** `Planned`

**Current phase:** Normative implementation has not started

**Next slice:** Re-query the current policy-impact and verifier-migration graphs,
confirm the shared-authority write set is free, and admit Milestone 0 against
that fresh baseline.

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Revise the project-agnostic Coding Standards so they apply the repository's
complection principle to the composed artifact, admit permanent validation and
evidence from explicit risk and necessity, scale authority and version
machinery to actual consumer promises, and bound systemic replanning. Project
the revised rules through every applicable policy-graph consumer with the
smallest sufficient enforcement portfolio.

This plan implements standards recommendations derived from the accepted
[A1/A1b audit](../standards-engine-a1-a1b-audit/plan.md) and the source-backed
[*Simple Made Easy* conformance audit](../standards-engine-a1-a1b-audit/reports/simple-made-easy-complection-conformance.md).
It does not design A1c or modify the Standards Engine implementation.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SEP-A1 | Core and Architecture distinguish simple from easy, test the resulting composition after introducing a boundary, and require an artifact-level review of caller knowledge, composition-root knowledge, representative change Locality, necessary complexity, cumulative machinery, and deletion results. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A2 | Every written plan records whether composed-design review applies; applicable material plans contain the required probes, replacement plans cannot silently lose them, and one expanded simplicity suite rejects nominal decomposition whose parts remain interleaved. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A3 | Verification admits permanent evidence, validation, integrity, and hash mechanisms from a reachable failure, material consequence, adequate oracle, proof boundary, marginal value, cost, and retention trigger rather than from possibility or existing machinery alone. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A4 | Contracts distinguishes external, adversarial, operational, contained-programming, and escaping/corrupting failures; intact proof-bearing values are not revalidated and contained internal defects may use immediate failure and diagnostics when the scoped risk does not require recovery machinery. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A5 | Immutable authority closure and version scopes are proportional to stated consumer, lifetime, reconstruction, overlap, deployment, persistence, and migration promises while preserving non-ambient reconstruction and independent scopes where those promises require them. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A6 | Systemic replanning has authority- and reachability-based stopping rules, accepts deletion and smaller Interfaces as repairs, compares the revised composition with the original objective, and established dependencies or proof tools are preferred unless a local semantic product is justified and owned. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A7 | Every existing relationship of every revised policy unit has an explicit disposition; every new unit and applicable consumer is registered; current repository-specific implementation projections are reviewed without changing A1b or treating it as general policy authority. | `integration` | `not-applicable` | `automated` | `pending` | [Planned graph dispositions](reports/policy-impact-dispositions.tsv) |
| SEP-A8 | Dependency-local policy/evidence invalidation is either accepted from a bounded prototype with completeness and stale-authority counterexamples, or rejected with a documented no-change decision; it is not made normative from the audit hypothesis alone. | `focused` | `not-applicable` | `automated` | `pending` | pending |
| SEP-A9 | The complete standards, prompt, template, fixture, suite, graph, generated-input, and documentation checks pass, and the generated standalone HTML matches the accepted policy-unit and relationship manifests. | `integration` | repository-supported verification environments | `automated` | `pending` | [Planned graph visualization](reports/standards-graph-change-visualization.html) |

## Scope

### In Scope

- Project-agnostic normative changes to Core, Architecture, Contracts,
  Dependencies, Planning, and Verification, plus Security, Resilience,
  Diagnostics, Documentation, and Release only where they consume the scoped
  risk, detection, recovery, evidence-lifecycle, or exact-identity decision.
- Fine-grained policy units and source-owned policy-impact relationships for
  every added or revised rule.
- Planning and implementation prompts, the plan template, structural plan
  validation, decision fixtures, declarative suites, suite registration, and
  generated verification inputs needed to make the rules operational.
- A bounded prototype of dependency-local policy/evidence invalidation before
  deciding whether to revise Projection Completeness.
- A deterministic, standalone HTML visualization of the current graph and the
  reviewed proposed delta.

### Out Of Scope

- A1c requirements, package structure, Interfaces, persistence, versions,
  validation paths, tests, or implementation.
- Changes to accepted A1 or A1b runtime code, tests, schemas, or contracts.
- Python verifier architecture or implementation changes; the active verifier
  recovery and Bash-retirement plans own those decisions.
- Retirement or replacement of any retained Bash checker. This plan may make
  an existing fixture a declarative-suite projection, but the active verifier
  migration owns checker retirement and terminal lifecycle evidence.
- Declaring individual existing tests, checkers, validators, hashes, or
  contracts redundant without a separate claim-level disposition.
- Reproducing Hickey's transcript or turning his language and technology
  examples into project-specific mandates.
- Rewriting historical accepted plans solely to satisfy a new planning field.

## Constraints And Assumptions

### Constraints

- Normative wording must remain applicable across unrelated repositories and
  technologies. A1/A1b are evidence, not the scope of the rule.
- Counts locate accumulated cost but never decide simplicity, necessity, or
  removal.
- Tests, types, schemas, freshness checks, coverage, and formal review may prove
  selected correctness claims; none is evidence that the design is simple.
- A new permanent check requires a stronger reason than “the value could be
  wrong.” Existing checks are retained until a claim-level review proves a
  smaller portfolio preserves the selected claims.
- Shared suite registry, policy graph, generated suite inputs, and verifier
  contracts are serial integration-owner writes. Re-query them before every
  implementation slice that touches shared authority.
- Each normative owner and every affected consumer change atomically in one
  accepted slice. Do not leave mandatory prose ahead of its applicable prompt,
  template, fixture, suite, or graph projection.

### Assumptions

- Commit `351e7852` is the accepted evidence baseline for this plan.
- Existing A1b implementation projections under Immutable Authority Closure
  and Version Scope remain applicable to A1b's accepted durable promises; the
  plan records them as reviewed-no-change unless fresh evidence contradicts
  that fact.
- The active verification migration may change suite and graph baselines before
  this plan starts; therefore the committed inventory is planning evidence, not
  admission authority for a later write.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Keep standards changes and A1c design as separate efforts. No A1c choice can become a normative example or implementation projection in this plan. | Planning | User direction and accepted audit scope | Any combined standards/A1c implementation proposal |
| Add one Core simplicity/complection unit and one Architecture composed-design admission unit; do not create one policy unit per audit recommendation. | Core and Architecture | [Recommendation consolidation](reports/recommendation-consolidation.md) | Parallel S1/S2/C1-C4 rules |
| Require every written plan to state `applicable` or `not-applicable` for composed-design review. Require the full artifact probe only when applicable and a reason when not applicable. | Planning | A1b replacement commit `44de7dff` removed the applicable review without detection | Optional template-only simplicity review |
| Expand `core-simplicity` to evaluate post-boundary composition and update existing Planning projection enforcement. Add only one new evidence-necessity suite and extend `contract-invariants` for proof lifetime/failure classification. | Verification | Evidence-lifecycle and enforcement-cost findings | One new suite for every recommendation |
| Locate scoped correctness-risk and evidence necessity together in Verification; Security continues to own adversarial threat semantics and Contracts owns proof construction and failure behavior. | Verification, Security, Contracts | S3-S5 and C5 consolidation | A universal security threat model for internal code |
| Preserve non-ambient closure and independent version promises, but derive their machinery from stated lifetimes and actual consumer compatibility rather than from the mere presence of a handle, artifact, or version field. | Architecture and Contracts | S6-S7 | Unconditional maximal closure or umbrella versioning |
| Keep dependency-local invalidation conditional until a prototype proves completeness, stale-edge detection, and stable unaffected evidence. | Planning | S9 is medium-high confidence and explicitly calls for a prototype | Immediate normative adoption of a proposed invalidation algebra |
| The policy-impact manifest, not the visualization or this plan, is final relationship authority. The generator must fail if a revised owner's current edges lack dispositions. | Planning | Policy Projection Completeness | Hand-maintained diagram as graph authority |
| Generate in `planning` state against the pre-change graph, `transition` state after each accepted owner-coherent milestone, and `accepted` state after resolving every conditional row. Transition and accepted modes reconstruct the fixed before-topology from the reviewed delta rather than treating a partially or fully changed graph as a new baseline. | Planning | Inspectable-history objective and generator lifecycle review | A live-only visualization that becomes unverifiable after the first implementation slice |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Composed design is less complected | Architecture | Artifact probe and representative semantic change paths | Actual Interface/dependency/change facts | Unbuilt speculative variants | Module count or ownership labels used as verdict |
| Evidence mechanism is necessary | Verification | Reachable failure, consequence, oracle, overlap, and proof-substitution record | Contract, threat/risk model, defect history, or mutation evidence | Hypothetical failures with no material consequence | “Could be wrong” treated as permanent-test authority |
| Validation belongs at this Seam | Contracts | Input authority, proof lifetime, mutation path, and escaping consequence | Producer/consumer and persistence/trust facts | Unchecked dynamic mutation not inspected | Type annotation alone treated as proof across deserialization |
| Closure/version machinery is proportionate | Architecture/Contracts | Stated consumer lifetime and compatibility promise | Public, persisted, deployment, and reconstruction contracts | Hypothetical consumers | Existing handle/version field treated as maximal promise |
| Local invalidation is complete | Policy graph | Prototype mutations of changed edge, removed consumer, provider revision, and unrelated subject | Current graph compiler and accepted coverage semantics | Unmodeled external evidence stores | Unrelated evidence remains stable only because a stale edge was missed |
| Projection set is complete | Policy impact | Source-owned graph query plus one disposition per current and planned edge | Registered unit and node catalogs | Unregistered semantic consumers | Link search substituted for graph declaration |

## Systemic Finding Audit

- Invariant family: standards-wide simplicity, verification proportionality,
  proof lifetime, promise scope, and replanning admission.
- Sibling producers and consumers: Core, Architecture, Contracts, Dependencies,
  Security, Resilience, Diagnostics, Planning, Implementation, Verification,
  Documentation, Release, applicable profiles, prompts, template, checker,
  fixtures, suites, suite registry, graph catalogs/declarations, and generated
  inputs.
- Authority and projection inventory: [current owner inventory](reports/current-policy-consumer-inventory.tsv),
  [planned unit changes](reports/planned-policy-units.tsv), and
  [planned catalog nodes](reports/planned-node-catalog-additions.tsv), and
  [edge dispositions](reports/policy-impact-dispositions.tsv).
- Consumer dispositions: every current edge of a revised owner is `update`,
  `reviewed-no-change`, or `conditional-update`; every new edge is `add` or
  `conditional-add`.
- Scope or sequencing replacement: if the live graph differs, stop and
  regenerate the inventory before normative edits. If the local-invalidation
  prototype fails, retain Projection Completeness revision 1 and record the
  rejected hypothesis rather than expanding the implementation.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts: composed-design admission; evidence/risk admission;
  proof lifetime and failure classification; promise proportionality;
  bounded replanning; graph projection and visualization.
- What/who/how/when/where/why interleavings: normative meaning stays in its
  owner; Planning records admission; Verification decides evidence; Contracts
  owns proof/failure; the graph records consumption; the HTML only presents
  graph data.
- Caller and composition-root knowledge: adopters need only routed normative
  Modules. The plan integration owner must coordinate shared graph, suite, and
  generated-input writes serially.
- Representative change path: adding the contained-internal-failure rule
  changes Contracts, its consuming profiles/prompts/template, one existing
  fixture family and suite, policy units/catalog/relationships, and generated
  suite inputs; it does not change A1b runtime code.
- Stable Interfaces versus hidden knowledge: TSV manifests are the planning
  Interface to the visualization; the generator reads authoritative current
  TOML directly and does not duplicate graph semantics.
- Necessary versus incidental complexity: five normative families and one
  conditional prototype replace twelve parallel proposals. Existing suites are
  expanded where they already own the decision family; one new suite is added
  only because no current owner decides evidence necessity.
- Deletion result: removing the HTML leaves normative meaning intact; removing
  edge dispositions makes complete impact review unprovable; removing the new
  evidence unit leaves S3/S5/S11 without an owner; removing separate Contracts
  proof ownership would mix evidence selection with value validity.
- Cumulative machinery: one Core unit, one Architecture unit, two existing
  Contracts headings promoted to units, one Verification unit, one new suite,
  no new verifier framework, and no new A1/A1b runtime mechanism.
- Future independent changes: A1c design, verifier migration, and any later
  evidence-portfolio retirement remain separate plans.

## Milestones

### Milestone 0: Fresh Admission And Conditional Prototype

**Goal:** Reconcile the committed plan with the live graph and decide the
dependency-local invalidation hypothesis before it can change normative text.

**Allowed write set:**

- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/current-policy-consumer-inventory.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/dependency-local-invalidation-prototype.py`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/dependency-local-invalidation-prototype.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/generate-standards-graph-visualization.py`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

No normative owner, graph declaration, suite registry, generated input, or
verifier source is writable in Milestone 0.

**Tasks:**

- [ ] Query all current relationships for every proposed revised owner.
- [ ] Reconcile additions, removals, concurrent changes, and shared write sets.
- [ ] Prototype changed-edge, removed-consumer, provider-revision, missing-edge,
  and unrelated-subject cases using current graph semantics.
- [ ] Record an accept-with-exact-algebra or reject-with-no-change decision.

**Acceptance gate:** The live inventory is complete, shared-authority ownership
is clear, SEP-A8 has a reproducible decision, and any accepted P1 implementation
has replaced Milestone 4's initial no-normative-write set with exact paths
before that milestone can be admitted.

**Status:** `Planned`

### Milestone 1: Composed Simplicity Admission

**Goal:** Make simple/easy/complection and post-boundary composition enforceable
through Core, Architecture, and Planning.

**Allowed write set:**

- `CORE-STANDARDS.md`
- `topics/architecture.md`
- `workflows/planning.md`
- `workflows/implementation.md`
- `workflows/verification.md`
- `profiles/applications/library.md`
- `profiles/boundaries/generated-contract.md`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `prompts/full-codebase-standards-refactor.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/check-plan-structure.sh`
- `evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/consolidation-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/template-projection-decisions.tsv`
- `evaluation/standards-effectiveness/suites/core-simplicity.toml`
- `evaluation/standards-effectiveness/suites/planning-consolidation.toml`
- `evaluation/standards-effectiveness/suites/plan-template-projection.toml`
- `evaluation/standards-effectiveness/policy-units/registry.toml`
- `evaluation/standards-effectiveness/policy-units/core.toml`
- `evaluation/standards-effectiveness/policy-units/architecture.toml`
- `evaluation/standards-effectiveness/policy-units/planning.toml`
- `evaluation/standards-effectiveness/policy-impact-registry.toml`
- `evaluation/standards-effectiveness/policy-impact/core.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-1-composed-simplicity-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

**Tasks:**

- [ ] Define simple, easy, complex/complected, and compose without technology
  mandates or cardinality rules.
- [ ] Add the post-boundary composition, artifact, representative-change,
  cumulative machinery, and deletion probes.
- [ ] Treat one hypothetical Adapter as a Seam-shape probe and normally require
  two current real variants before permanent generality, while permitting an
  independently justified public contract or invariant to supply the reason.
- [ ] Require composed-design applicability and applicable answers in written
  plans and replacement designs.
- [ ] Replace `core-simplicity`'s separation bias with composition outcomes and
  verify plan projection with the existing Planning suites.
- [ ] Register units, artifacts, and every applicable relationship atomically.

**Acceptance gate:** SEP-A1 and SEP-A2 pass, every Milestone 1 edge has its
planned final disposition, `--state transition --check` passes after
regeneration, and the general standards make no A1c choice.

**Status:** `Planned`

### Milestone 2: Evidence, Risk, And Proof Lifetime

**Goal:** Admit permanent correctness machinery from explicit failure and risk
facts while preserving real trust, persistence, and external boundaries.

**Allowed write set:**

- `topics/contracts.md`
- `topics/dependencies.md`
- `topics/diagnostics.md`
- `topics/resilience.md`
- `topics/security.md`
- `workflows/planning.md`
- `workflows/implementation.md`
- `workflows/verification.md`
- `workflows/documentation.md`
- `workflows/release.md`
- `profiles/boundaries/generated-contract.md`
- `profiles/boundaries/ipc.md`
- `profiles/boundaries/language-bindings.md`
- `profiles/boundaries/persistence.md`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/fixtures/contracts/invariant-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/dependencies/implementation-versus-dependency-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/verification/evidence-necessity-and-risk-decisions.tsv`
- `evaluation/standards-effectiveness/suites/contract-invariants.toml`
- `evaluation/standards-effectiveness/suites/implementation-versus-dependency.toml`
- `evaluation/standards-effectiveness/suites/evidence-necessity-and-risk.toml`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/policy-units/contracts.toml`
- `evaluation/standards-effectiveness/policy-units/dependencies.toml`
- `evaluation/standards-effectiveness/policy-units/verification.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.verification.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-2-evidence-and-proof-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

**Tasks:**

- [ ] Add the unified evidence-necessity, correctness-risk, marginal-value,
  exact-byte purpose, and retirement decision.
- [ ] Require the admission to compare types, construction, static analysis, a
  deeper Interface check, existing evidence, normal failure, and trace-led
  debugging before adding permanent machinery.
- [ ] Classify failure sources and consequences before selecting validation or
  recovery machinery.
- [ ] Make proof lifetime explicit and preserve direct use of intact validated
  representations.
- [ ] Register the existing Validation Proof Lifetime fixture unchanged under
  `contract-invariants`; its retained Bash consumer owns the current schema and
  16-row shape until the verifier migration retires that checker.
- [ ] Require custom semantic tooling to justify why an established dependency
  or proof tool cannot cover the reachable material failure.
- [ ] Exercise arbitrary input, durable corruption, contained internal error,
  escaping internal error, subsumed regression, justified defense in depth,
  and incidental-byte cases.
- [ ] Register units, artifacts, and every applicable relationship atomically.

**Acceptance gate:** SEP-A3 and SEP-A4 plus the established-tooling portion of
SEP-A6 pass with one coherent evidence suite and the extended Contracts suite;
`--state transition --check` passes after regeneration, and no individual
existing checker is removed by inference.

**Status:** `Planned`

### Milestone 3: Promise Proportionality And Bounded Correction

**Goal:** Scale closure, compatibility, and systemic search to real promises
and reachable consequences.

**Allowed write set:**

- `topics/architecture.md`
- `topics/contracts.md`
- `workflows/planning.md`
- `workflows/release.md`
- `profiles/applications/library.md`
- `profiles/boundaries/generated-contract.md`
- `profiles/boundaries/ipc.md`
- `profiles/boundaries/language-bindings.md`
- `profiles/boundaries/persistence.md`
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/fixtures/architecture/immutable-authority-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/contracts/version-scope-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-missing-audit.md`
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-replan-decisions.tsv`
- `evaluation/standards-effectiveness/suites/a1b-authority-reconstruction.toml`
- `evaluation/standards-effectiveness/suites/contract-authority-scope.toml`
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml`
- `evaluation/standards-effectiveness/policy-units/architecture.toml`
- `evaluation/standards-effectiveness/policy-units/contracts.toml`
- `evaluation/standards-effectiveness/policy-units/planning.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.planning.toml`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-3-promise-and-replanning-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

**Tasks:**

- [ ] Revise closure admission from the promised handle and reconstruction
  lifetime without weakening genuine cold replay.
- [ ] Add actual-consumer and cumulative migration/test cost to version-scope
  admission without restoring an umbrella version.
- [ ] Add authority/reachability stopping rules, deletion/smaller-Interface
  remedies, and composition comparison to systemic replanning.
- [ ] Reconfirm every A1b implementation projection as reviewed-no-change or
  change the graph disposition from fresh evidence; do not edit A1b.

**Acceptance gate:** SEP-A5 and SEP-A6 pass and all current implementation
projections have explicit evidence-backed dispositions;
`--state transition --check` passes after regeneration.

**Status:** `Planned`

### Milestone 4: Conditional Projection-Local Invalidation

**Goal:** Implement only the Milestone 0 invalidation result that was proved.

**Allowed write set:**

- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-4-projection-invalidation-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

This initial set authorizes the rejected-prototype/no-normative-change path. If
Milestone 0 accepts the prototype, it must re-plan this milestone with exact
normative, fixture, suite, graph, and generated-input paths before any such
file is writable. Generic verifier Python is not an admissible expansion here.

**Tasks:**

- [ ] If accepted, revise Projection Completeness and its declarative evidence
  to the exact dependency-local algebra.
- [ ] If rejected, retain semantic revision 1 and record `reviewed-no-change`
  for its current relationship; resolve the planning manifests from
  `conditional-revise`/`conditional-update` to `retain`/`reviewed-no-change`.
- [ ] Prove changed/missing consumers invalidate while unrelated subjects stay
  stable only when their deciding authority did not change.

**Acceptance gate:** SEP-A8 is satisfied without a stale-edge or global-renewal
fallback and without crossing verifier ownership; the resolved manifests pass
`--state transition --check` after regeneration.

**Status:** `Planned`

### Milestone 5: Integrated Graph And Standards Acceptance

**Goal:** Verify the complete normative system and publish the accepted graph
delta without creating a second authority.

**Allowed write set:**

- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/current-policy-consumer-inventory.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/generate-standards-graph-visualization.py`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/final-acceptance.md`

Milestone 5 is verification and plan-state reconciliation only. A discovered
normative, routing, suite, graph, or generated-input change returns to its
owning milestone and exact write set.

**Tasks:**

- [ ] Re-query every revised unit and prove one final disposition per consumer.
- [ ] Resolve every conditional unit/edge row, verify registered suite-input
  freshness, and regenerate the standalone HTML with `--state accepted` from
  the accepted manifests and reviewed before/after delta.
- [ ] Run focused suites, graph/compiler checks, plan checks, all-suites
  verification, link checks, and diff hygiene.
- [ ] Reconcile this plan, ledger, issues, graph data, and visualization to the
  same accepted state.

**Acceptance gate:** SEP-A1 through SEP-A9 are satisfied, no unresolved or
unconnected graph change remains, and all applicable repository checks pass.

**Status:** `Planned`

## Blockers

- `none` for planning. Normative implementation must wait until the active
  verifier migration exposes a non-overlapping serial shared-authority slice.

## Re-Plan Triggers

- The live policy graph differs from the committed counts or contains a new
  consumer of a proposed revised owner.
- The verifier migration has an admitted slice touching the suite registry,
  policy graph, generated suite inputs, or another shared write in this plan.
- The local-invalidation prototype cannot preserve both complete affected-edge
  detection and stable unrelated evidence.
- A proposed rule can only be expressed through A1/A1b-specific nouns,
  guarantees, or implementation artifacts.
- The enforcement design adds another suite, checker, registry, or serialized
  contract without a unique claim not owned by the planned portfolio.
- A current implementation projection no longer consumes the revised promise,
  or a missing consumer is discovered.
- Final change propagation materially exceeds the composed-design review.

## Concurrent Work

Read-only investigations with disjoint report outputs may run concurrently.
Normative owners, policy-unit registries, node catalogs, relationship
declarations, suite registry, generated suite inputs, plan/ledger state, and
final integration remain serial integration-owner writes. Do not begin a
concurrent normative slice while the verifier migration owns any shared
artifact.

## Repository Isolation

Direct serial work in the current repository is the planned mode. If concurrent
external work makes isolation material, record the responsible owner, target
branch, integration owner, visibility, and expected terminal disposition
before creating a worktree. No isolation is currently required.

## Final Acceptance

- Acceptance status: `pending`
- Final status: `Planned`
- Required final evidence: accepted objective rows, milestone gates, exact
  final policy-impact query, complete suite/checker results, generated-input
  freshness, HTML `--state accepted --check`, link validation, and clean diff
  hygiene.
