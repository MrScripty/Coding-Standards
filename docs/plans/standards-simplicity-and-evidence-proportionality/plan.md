# Plan: Standards Simplicity And Evidence Proportionality

**Plan status:** `Accepted`

**Current phase:** Milestone 5 accepted

**Next slice:** `none`

**Acceptance status:** `satisfied`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Revise the project-agnostic Coding Standards so they apply the repository's
complection principle to the composed artifact, admit permanent validation and
evidence from explicit risk and necessity, scale authority and version
machinery to actual consumer promises, and bound systemic replanning. Project
the revised rules through every applicable standards-to-standards impact edge
and use the smallest sufficient repository conformance-evidence portfolio. The standards
library does not enforce itself on adopters: each adopter chooses whether and
how to use review, existing tools, custom tooling, or no automation for a given
claim.

This plan implements standards recommendations derived from the accepted
[A1/A1b audit](../standards-engine-a1-a1b-audit/plan.md) and the source-backed
[*Simple Made Easy* conformance audit](../standards-engine-a1-a1b-audit/reports/simple-made-easy-complection-conformance.md).
The remaining-milestone replan also uses the accepted
[A1c final evidence](../standards-engine-a1c/reports/a1c-final-acceptance.md)
to challenge earlier assumptions. It does not design A1c or modify the
Standards Engine implementation.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SEP-A1 | Core and Architecture distinguish simple from easy, test the resulting composition after introducing a boundary, and require an artifact-level review of caller knowledge, composition-root knowledge, representative change Locality, necessary complexity, cumulative machinery, and deletion results. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 acceptance](reports/milestone-1-composed-simplicity-acceptance.md) |
| SEP-A2 | Every nonterminal written plan governed by the revised standard records whether composed-design review applies; applicable material plans contain the required probes, replacement plans cannot silently lose them, and one expanded simplicity suite rejects nominal decomposition whose parts remain interleaved. Historical terminal plans are not rewritten. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 acceptance](reports/milestone-1-composed-simplicity-acceptance.md) |
| SEP-A3 | Verification admits permanent evidence, validation, integrity, and hash mechanisms from a reachable failure, material consequence, adequate oracle, proof boundary, marginal value, cost, and retention trigger rather than from possibility or existing machinery alone. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-evidence-and-proof-acceptance.md) |
| SEP-A4 | Contracts distinguishes external, adversarial, operational, contained-programming, and escaping/corrupting failures; intact proof-bearing values are not revalidated and contained internal defects may use immediate failure and diagnostics when the scoped risk does not require recovery machinery. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 2 acceptance](reports/milestone-2-evidence-and-proof-acceptance.md) |
| SEP-A5 | Immutable authority closure and version scopes are proportional to stated consumer, lifetime, reconstruction, overlap, deployment, persistence, and migration promises while preserving non-ambient reconstruction and independent scopes where those promises require them. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 3 acceptance](reports/milestone-3-promise-and-replanning-acceptance.md) |
| SEP-A6 | Systemic replanning has authority- and reachability-based stopping rules, accepts deletion and smaller Interfaces as repairs, compares the revised composition with the original objective, and established dependencies or proof tools are preferred unless a local semantic product is justified and owned. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 2](reports/milestone-2-evidence-and-proof-acceptance.md) and [Milestone 3](reports/milestone-3-promise-and-replanning-acceptance.md) |
| SEP-A7 | Every revised policy unit has an explicit disposition for each potentially affected standard reachable through the standards impact graph; every new standard-to-standard relationship is registered, and no application implementation is treated as an impact-graph consumer. | `integration` | `not-applicable` | `automated` | `satisfied` | [Accepted graph dispositions](reports/policy-impact-dispositions.tsv) and [final acceptance](reports/final-acceptance.md) |
| SEP-A8 | Dependency-local policy/evidence invalidation is either accepted from a bounded prototype with completeness and stale-authority counterexamples, or rejected with a documented no-change decision; it is not made normative from the audit hypothesis alone. | `focused` | `not-applicable` | `automated` | `satisfied` | [No-change decision and implementation prototype](reports/dependency-local-invalidation-prototype.md) |
| SEP-A9 | The complete standards, prompt, template, fixture, suite, graph, generated-input, and documentation checks pass, and the generated standalone HTML matches the accepted policy-unit and relationship manifests. | `integration` | repository-supported verification environments | `automated` | `satisfied` | [Final acceptance](reports/final-acceptance.md) and [accepted graph visualization](reports/standards-graph-change-visualization.html) |

The `automated` modes above describe how this repository may demonstrate that
its own standards text, projections, and evidence remain coherent. They are
not a requirement that an adopting repository install this repository's
checks, and they do not make the written standards an enforcement harness.

## Scope

### In Scope

- Project-agnostic normative changes to Core, Architecture, Contracts,
  Dependencies, Planning, and Verification. Security, Resilience, Diagnostics,
  Documentation, Release, boundary profiles, prompts, and the plan template are
  reviewed as consumers but change only if their existing owner-local wording
  conflicts with a revised rule.
- Fine-grained policy units and source-owned standards-impact relationships for
  every added or revised rule. These relationships point to other standards
  that an agent must inspect; they do not predict or test effects on adopter
  software.
- Planning and implementation prompts, the plan template, structural plan
  validation, decision fixtures, declarative suites, suite registration, and
  generated verification inputs selected as proportionate conformance evidence
  for this repository's own standards changes.
- Project-agnostic wording that leaves adopters free to use manual review,
  established tools, locally justified tools, or no automation according to
  the claim and risk they have actually admitted.
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
- A universal enforcement harness, a requirement to run Coding Standards'
  repository-local suites, or a guarantee that a written rule will be
  remembered or re-read at a particular time.

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
- Normative requirements state expected decisions and outcomes; they cannot
  guarantee recollection, invocation, or enforcement. An adopter owns any
  mechanism that it chooses to use to obtain those properties.

### Assumptions

- Commit `351e7852` remains the fixed historical A1/A1b audit baseline. The
  accepted A1c Linux implementation is effectiveness evidence for challenging
  the audit recommendations, not a node or consumer in the standards impact
  graph and not a replacement for that historical comparison.
- Standards-impact traversal follows relationships between normative standards.
  Repository fixtures, suites, prompts, templates, generated inputs, and code
  may supply conformance or delivery evidence, but they do not represent
  standards that could be affected by another standard's meaning.
- The active verification migration may change suite and graph baselines before
  this plan starts; therefore the committed inventory is planning evidence, not
  admission authority for a later write.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Keep standards changes, standards-impact traversal, and A1c effectiveness evaluation separate. A1c choices cannot become normative examples, general rules, or impact-graph consumers, and no A1c source is writable here. | Planning | User direction and accepted audit scope | Any combined standards/A1c implementation proposal or use of adopter software as a standards-impact node |
| Add one Core simplicity/complection unit and one Architecture composed-design admission unit; do not create one policy unit per audit recommendation. | Core and Architecture | [Recommendation consolidation](reports/recommendation-consolidation.md) | Parallel S1/S2/C1-C4 rules |
| Require every nonterminal written plan governed by the revised standard to state `applicable` or `not-applicable` for composed-design review. Require the full artifact probe only when applicable and a reason when not applicable; do not rewrite historical terminal plans. | Planning | A1b replacement commit `44de7dff` removed the applicable review without detection | Optional template-only simplicity review |
| Deepen the existing `workflow.verification.acceptance-claims` owner and `acceptance-claims` suite for evidence admission and retention; do not add a parallel Verification policy unit or suite. A dedicated decision fixture may be added inside that existing suite. Extend `contract-invariants` only for the Contracts-owned failure decision. | Verification | Existing claim-selection, gate, cost, oracle, coverage, and diagnosis rules already own most of N2/N3; the missing semantics are marginal value, retention, and contained-failure classification | The parallel `evidence-necessity-and-risk` policy/suite proposal and automatic new-suite creation |
| Retain Validation Proof Lifetime prose as sufficient and register the existing heading as a standards-graph owner. A1c's repeated validation remains audit evidence outside the graph; do not repeat the rule to compensate for one application's failure to apply it. | Contracts | Existing text already requires direct use of an intact proof-bearing representation and new proof only after representation loss, mutation, contract change, or a new authority boundary | A redundant normative rewrite of Validation Proof Lifetime |
| The standards specify decisions and outcomes, not adoption-time enforcement. Repository suites, fixtures, checkers, and graph checks are internal conformance evidence; adopters choose their own manual or automated mechanism, if any. | Standards-library scope | User direction and standard-isolation principle | Any wording that requires adopters to install this repository's tooling or claims that prose can enforce its own use |
| Locate scoped correctness-risk and evidence necessity together in Verification; Security continues to own adversarial threat semantics and Contracts owns proof construction and failure behavior. | Verification, Security, Contracts | S3-S5 and C5 consolidation | A universal security threat model for internal code |
| Preserve non-ambient closure and independent version promises, but derive their machinery from stated lifetimes and actual consumer compatibility rather than from the mere presence of a handle, artifact, or version field. | Architecture and Contracts | S6-S7 | Unconditional maximal closure or umbrella versioning |
| Retain Projection Completeness at revision 1. The bounded prototype is evidence for a separately owned Coding Standards coverage-implementation review, not authority for a project-agnostic normative revision whose known concrete consumer is excluded from this plan. | Planning | [Milestone 0 no-change decision and prototype](reports/dependency-local-invalidation-prototype.md) | The unresolved P1 hypothesis and any attempt to encode repository-specific coverage machinery as general policy |
| The normative-standard subset of the policy-impact manifest, not the visualization or this plan, is final standards-impact relationship authority. Conformance projections are separate evidence metadata and application implementation projections do not determine standards impact. | Planning | User clarification of impact-graph purpose and Policy Projection Completeness | Hand-maintained diagram as graph authority or use of downstream software as standards-impact evidence |
| Generate in `planning` state against the pre-change graph, `transition` state after each accepted owner-coherent milestone, and `accepted` state after resolving every conditional row. Transition and accepted modes reconstruct the fixed before-topology from the reviewed delta rather than treating a partially or fully changed graph as a new baseline. | Planning | Inspectable-history objective and generator lifecycle review | A live-only visualization that becomes unverifiable after the first implementation slice |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Composed design is less complected | Architecture | Artifact probe and representative semantic change paths | Actual Interface/dependency/change facts | Unbuilt speculative variants | Module count or ownership labels used as verdict |
| Evidence mechanism is necessary | Verification | Reachable failure, consequence, oracle, overlap, and proof-substitution record | Contract, threat/risk model, defect history, or mutation evidence | Hypothetical failures with no material consequence | “Could be wrong” treated as permanent-test authority |
| Validation belongs at this Seam | Contracts | Input authority, proof lifetime, mutation path, and escaping consequence | Producer/consumer and persistence/trust facts | Unchecked dynamic mutation not inspected | Type annotation alone treated as proof across deserialization |
| Closure/version machinery is proportionate | Architecture/Contracts | Stated consumer lifetime and compatibility promise | Public, persisted, deployment, and reconstruction contracts | Hypothetical consumers | Existing handle/version field treated as maximal promise |
| Local invalidation is complete | Policy graph | Prototype mutations of changed edge, removed consumer, provider revision, and unrelated subject | Current graph compiler and accepted coverage semantics | Unmodeled external evidence stores | Unrelated evidence remains stable only because a stale edge was missed |
| Standards-impact set is complete | Policy impact | Source-owned graph query plus one disposition per potentially affected standard | Registered normative policy units and their standard-to-standard relationships | Undeclared semantic relationship between standards | Application code, conformance evidence, or link search substituted for standards-impact traversal |
| Repository conformance evidence is proportionate | Verification | Unique deciding claim, marginal value over an existing suite or review, and lifecycle cost | Accepted normative owner and existing conformance portfolio | An adopter's chosen enforcement arrangement | A new checker or suite admitted merely because automation is possible |

## Systemic Finding Audit

- Invariant family: standards-wide simplicity, verification proportionality,
  proof lifetime, promise scope, and replanning admission.
- Potentially affected standards: Core, Architecture, Contracts, Dependencies,
  Security, Resilience, Diagnostics, Planning, Implementation, Verification,
  Documentation, Release, applicable normative profiles, and the Router.
- Separate repository conformance surfaces: prompts, template, checker,
  fixtures, suites, suite registry, graph declarations, and generated inputs.
  These may need coordinated updates, but they are not standards-impact
  consumers.
- Authority and impact inventory: [current owner inventory](reports/current-policy-consumer-inventory.tsv),
  [planned unit changes](reports/planned-policy-units.tsv), and
  [planned catalog nodes](reports/planned-node-catalog-additions.tsv), and
  [edge dispositions](reports/policy-impact-dispositions.tsv).
- Standards-impact dispositions: every potentially affected standard is
  `update` or `reviewed-no-change`; each relationship is retained or added even
  when inspection finds that no text edit is needed, because its purpose is to
  route the next standards change back to that standard.
- Conformance dispositions: fixtures, suites, prompts, templates, and generated
  inputs are reviewed under their own ownership and acceptance claims. They do
  not satisfy the standards-impact traversal, and no A1c file receives a graph
  disposition.
- Scope or sequencing replacement: if the live graph differs, stop and
  regenerate the inventory before normative edits. Projection Completeness and
  its current declarative relationship are retained. The local-invalidation
  prototype is separately owned implementation-design evidence and does not
  authorize a normative or verifier change in this plan.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: composed-design admission; evidence/risk admission;
  proof lifetime and failure classification; promise proportionality;
  bounded replanning; graph projection and visualization.
- State, identity, value, time, policy, and mechanism: normative meaning stays in its
  owner; Planning records admission; Verification decides evidence; Contracts
  owns proof/failure; the graph records consumption; the HTML only presents
  graph data.
- Caller and composition-root knowledge: adopters need only routed normative
  Modules. The plan integration owner must coordinate shared graph, suite, and
  generated-input writes serially.
- Representative change paths and forced owners: adding the contained-internal-failure rule
  changes Contracts, its invariant fixture and existing suite, policy-unit and
  graph declarations, and generated suite inputs. Potentially affected
  standards such as Verification, Security, Resilience, Diagnostics, and
  boundary profiles are inspected through graph edges; prompts and the template
  are separate conformance surfaces; application runtime code is outside the graph.
- Stable Interfaces versus hidden knowledge: TSV manifests are the planning
  Interface to the visualization; the generator reads authoritative current
  TOML directly and does not duplicate graph semantics.
- Independent evolution, testing, failure, and replacement: A1c effectiveness
  evaluation, verifier migration, adopter enforcement choices, and any later
  evidence-portfolio retirement remain
  separate plans and can evolve, fail, or be replaced independently.
- Necessary complexity and containment: five normative families and one
  bounded prototype disposition replace twelve parallel proposals. The
  prototype rejected a sixth normative family in this plan. Existing policy
  owners and suites are deepened rather than layered; no new suite or parallel
  Verification policy owner is planned.
- Deletion and cumulative machinery result: removing the HTML leaves normative meaning intact; removing
  edge dispositions makes complete impact review unprovable; removing the
  Acceptance Claims refinement leaves S3/S5/S11 without an owner; removing
  separate Contracts proof ownership would mix evidence selection with value
  validity. The cumulative normative addition remains the accepted Core and
  Architecture units plus registration of two existing Contracts headings;
  pending work revises existing Verification, Architecture, Contracts,
  Dependencies, and Planning owners. There is no new suite, verifier framework,
  adopter enforcement requirement, or A1/A1b/A1c runtime mechanism.

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
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/recommendation-consolidation.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/dependency-local-invalidation-prototype.py`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/dependency-local-invalidation-prototype.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/generate-standards-graph-visualization.py`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

No normative owner, graph declaration, suite registry, generated input, or
verifier source is writable in Milestone 0.

**Tasks:**

- [x] Query all current relationships for every proposed revised owner.
- [x] Reconcile additions, removals, concurrent changes, and shared write sets.
- [x] Prototype changed-edge, removed-consumer, provider-revision, missing-edge,
  and unrelated-consumer cases using current graph semantics.
- [x] Record an accept-with-exact-algebra or reject-with-no-change decision.

**Acceptance gate:** The live inventory is complete, shared-authority ownership
is clear, SEP-A8 has a reproducible decision, and P1 is either admitted with a
complete owner-coherent write set or closed with an explicit no-change
disposition before later milestones can be admitted.

**Acceptance:** The live graph remains 47 policy units and 387 relationships;
all planned owner inventories reconcile; no post-`M6-I72` migration package is
admitted; and the executable prototype demonstrates a bounded implementation
candidate across all required mutations. P1 is rejected as a normative change
in this plan because its known concrete coverage consumer is excluded;
Projection Completeness remains at revision 1. The stale generated suite-input
repository-index digest is recorded for the first later shared-authority slice
rather than changed outside Milestone 0's write set.

**Status:** `Accepted`

### Milestone 1: Composed Simplicity Admission

**Goal:** Make simple/easy/complection and post-boundary composition explicit
through Core, Architecture, and Planning, with proportionate conformance
evidence for this repository.

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
- `evaluation/standards-effectiveness/verify-plan-fixtures.sh`
- `evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/consolidation-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/template-projection-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/plans/valid-active.md`
- `evaluation/standards-effectiveness/fixtures/plans/valid-blocked.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-execution-history.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-missing-next.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-objective-partial.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-missing-composed-design-applicability.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-incomplete-composed-design-review.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-unreasoned-composed-design-exclusion.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-whitespace-composed-design-reason.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-whitespace-composed-design-probe.md`
- `evaluation/standards-effectiveness/fixtures/plans/invalid-duplicate-composed-design-probe.md`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1b/relationship-migration.tsv`
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
- `evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml`
- `evaluation/standards-effectiveness/policy-coverage/authorization-authority.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/core.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/router.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.cross-platform.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.security.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-nodes.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-edges.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-components.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-1-composed-simplicity-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`
- `docs/plans/standards-verification-engine/plan.md`
- `docs/plans/standards-verification-engine/execution-ledger.md`
- `docs/plans/python-verification-engine-recovery/plan.md`
- `docs/plans/python-verification-engine-recovery/execution-ledger.md`

The plan-fixture paths are part of the structural checker's actual contract:
valid nonterminal lifecycle fixtures must project the new required field,
existing negative fixtures must still reach their intended diagnostics, and
dedicated negative fixtures must prove missing, incomplete, whitespace-only,
duplicated, and unreasoned decisions are rejected with exact diagnostics. The two current active plans
also adopt the field with owner-coordinated ledger records; historical terminal
plans are not rewritten. The coverage paths are also mandatory. Milestone 1 changes the
global provider-v5 horizon, so every current attestation must bind the current
review evidence; changed/new owners also need matching semantic revisions, and
the repository authorization authority must bind this user-authorized review.
These are current infrastructure obligations, not new general standards.

**Tasks:**

- [x] Define simple, easy, complex/complected, and compose without technology
  mandates or cardinality rules.
- [x] Add the post-boundary composition, artifact, representative-change,
  cumulative machinery, and deletion probes.
- [x] Treat a hypothetical Adapter only as a Seam-shape probe. Permanent
  generality requires a current independent reason: materially distinct real
  implementations are evidence, while a separately owned public contract,
  trust/deployment/lifecycle boundary, or enforceable invariant may suffice.
- [x] Require composed-design applicability and applicable answers in written
  plans and replacement designs.
- [x] Replace `core-simplicity`'s separation bias with composition outcomes and
  verify plan projection with the existing Planning suites.
- [x] Register units, artifacts, and every applicable relationship atomically.

**Acceptance gate:** SEP-A1 and SEP-A2 pass, every Milestone 1 edge has its
planned final disposition, `--state transition --check` passes after
regeneration, and the general standards make no A1c choice.

**Acceptance:** [Milestone 1 evidence](reports/milestone-1-composed-simplicity-acceptance.md)
records the accepted normative meaning, fixtures, 49-unit/407-relationship
repository projection closure, full current provider-v5 coverage renewal, current-plan migration,
generated-input and checker-evidence refreshes, closed migration renewal, and
transition visualization. The ownership-locality refinement keeps Core to
definitions, Architecture to admission, and downstream standards and prompts
to their local consequences. The change introduces no A1c decision or A1/A1b
runtime mechanism.

**Status:** `Accepted`

### Milestone 2: Evidence, Risk, And Proof Lifetime

**Goal:** Admit permanent correctness machinery from explicit failure and risk
facts while preserving real trust, persistence, and external boundaries.

**Allowed write set:**

- `topics/contracts.md`
- `topics/dependencies.md`
- `workflows/verification.md`
- `evaluation/standards-effectiveness/fixtures/contracts/invariant-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/contracts/validation-proof-lifetime-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/dependencies/implementation-versus-dependency-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/verification/evidence-necessity-and-risk-decisions.tsv`
- `evaluation/standards-effectiveness/suites/acceptance-claims.toml`
- `evaluation/standards-effectiveness/suites/contract-invariants.toml`
- `evaluation/standards-effectiveness/suites/implementation-versus-dependency.toml`
- `evaluation/standards-effectiveness/policy-units/contracts.toml`
- `evaluation/standards-effectiveness/policy-units/dependencies.toml`
- `evaluation/standards-effectiveness/policy-units/verification.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.verification.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/relationship-migration.tsv`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-node-catalog-additions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-2-evidence-and-proof-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

The existing `acceptance-claims` suite gains one decision check over the new
evidence-necessity fixture. This deepens its claim-selection ownership without
changing the suite registry or creating a parallel suite. Repository
conformance evidence remains optional to adopters.

The A1c-named relationship-migration fixture is admitted only as a mechanical
renewal of this repository's frozen full-projection compatibility evidence. It
does not make A1c, application code, or conformance artifacts standards-impact
consumers, and it does not authorize inspection or modification of A1c.

**Tasks:**

- [x] Re-query the standards impact graph for every current N2, N3, and N5-D
  normative neighbor before admission. Inspect each potentially affected
  standard and record `update` or `reviewed-no-change`; do not query application
  code or treat conformance artifacts as standards-impact consumers.
- [x] Revise the existing Acceptance Claims owner with the smallest permanent-
  evidence admission rule: reachable failure, material consequence, adequate
  oracle, proof boundary, marginal value over existing evidence, lifecycle
  cost, exact-byte purpose when applicable, and a retention/removal trigger.
  Do not create a second Verification owner or repeat the procedure in
  Security, Resilience, Diagnostics, Documentation, or Release.
- [x] Require the admission to compare types, construction, static analysis, a
  deeper Interface check, existing evidence, normal failure, and trace-led
  debugging before adding permanent machinery.
- [x] Refine Invariant Contracts only where current wording over-prescribes one
  failure mechanism. Classify contained programming defects separately from
  arbitrary or adversarial input, operational failure, escaping invalid state,
  and authoritative-state corruption; permit immediate failure and diagnosis
  when no public or recovery contract requires more machinery.
- [x] Retain Validation Proof Lifetime prose unchanged and register the existing
  heading as a first-class policy owner. It already requires direct use of the
  same intact proof-bearing representation, rejects type annotations as proof,
  and requires new proof after representation loss, mutation, contract change,
  or a new authority boundary.
- [x] Register the existing Validation Proof Lifetime fixture unchanged under
  `contract-invariants`; its retained Bash consumer owns the current schema and
  16-row shape until the verifier migration retires that checker.
- [x] Require a standardized semantic reimplementation to justify why an
  established dependency cannot cover the reachable material failure. Permit
  thin adapters and domain-specific products when they own distinct local
  semantics. Apply this decision when a tool is created, materially extended,
  or renewed; do not make it a retroactive automatic-deletion rule.
- [x] Extend `acceptance-claims` with the dedicated evidence-necessity decision
  fixture. Do not add a new suite, registry row, plan-template section, or
  copied downstream decision procedure.
- [x] Exercise arbitrary input, durable corruption, contained internal error,
  escaping internal error, subsumed regression, justified defense in depth,
  and incidental-byte cases.
- [x] Register policy units and every applicable standards-to-standards impact
  relationship atomically. Register repository conformance artifacts through
  their separate suite, fixture, and generated-input authorities.

**Acceptance gate:** SEP-A3 and SEP-A4 plus the established-tooling portion of
SEP-A6 pass through the existing Acceptance Claims, Contracts, and Dependencies
owners and suites; Validation Proof Lifetime has no redundant normative edit;
`--state transition --check` passes after regeneration; no individual existing
checker is removed by inference; and no wording requires an adopter to use any
Coding Standards checker or suite.

**Acceptance:** [Milestone 2 evidence](reports/milestone-2-evidence-and-proof-acceptance.md)
records the accepted normative meaning, the 51-unit/100-relationship standards
impact graph, separate 445-relationship repository projection, proportionate
suite and fixture evidence, and the A1c-free graph boundary.

**Status:** `Accepted`

### Milestone 3: Promise Proportionality And Bounded Correction

**Goal:** Scale closure, compatibility, and systemic search to real promises
and reachable consequences.

**Allowed write set:**

- `topics/architecture.md`
- `topics/contracts.md`
- `workflows/planning.md`
- `evaluation/standards-effectiveness/fixtures/architecture/immutable-authority-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/contracts/version-scope-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-missing-audit.md`
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-replan-decisions.tsv`
- `evaluation/standards-effectiveness/suites/contract-authority-scope.toml`
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml`
- `evaluation/standards-effectiveness/policy-units/architecture.toml`
- `evaluation/standards-effectiveness/policy-units/contracts.toml`
- `evaluation/standards-effectiveness/policy-units/planning.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.planning.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/relationship-migration.tsv`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `docs/plans/standards-simplicity-and-evidence-proportionality/plan.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/execution-ledger.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/issues.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/planned-policy-units.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-3-promise-and-replanning-acceptance.md`
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/standards-graph-change-visualization.html`

The existing `contract-authority-scope` suite already owns Architecture
authority-scope and Contracts version-scope decisions. It gains the generic
immutable-closure fixture instead of introducing an Architecture suite seam.

The A1c-named relationship-migration fixture is writable only for the
mechanical closed-set renewal described by SEP-019. That repository
compatibility artifact does not make A1c or any application implementation a
standards-impact consumer.

**Tasks:**

- [x] Restore project-agnostic executable ownership for
  `immutable-authority-decisions.tsv`. Its current `a1c-snapshot-lifecycle`
  evidence owner does not consume that fixture and decides A1c-specific
  snapshot behavior. Extend `contract-authority-scope`, which already decides
  generic Architecture authority and Contracts version scope; do not add a new
  suite or catalog node.
- [x] Revise closure admission from the promised handle and reconstruction
  lifetime without weakening genuine cold replay. Distinguish semantic closure
  completeness from a requirement for separately persisted identity, codec,
  handle, version, allocation ordinal, and lifecycle objects: a complete
  aggregate may carry the whole admitted closure.
- [x] Separate version roles before adding machinery: a fail-closed current-
  format discriminator, identity-domain revision, overlapping compatibility
  version, migration version, and allocation ordinal are not interchangeable.
  Require a compatibility matrix only for combinations actually promised to
  supported consumers. Do not infer historical readers or cross-engine
  migration merely from the presence of several version fields; the A1c
  observation remains effectiveness evidence outside the standards graph.
- [x] Add authority/reachability stopping rules, deletion/smaller-Interface
  remedies, and composition comparison to systemic replanning. A newly
  discovered semantic consumer, owner, risk, or public promise expands the
  audit; a newly discovered implementation file within an already admitted
  owner does not by itself expand the design. Stop when the owner and reachable
  consumer population are dispositioned.
- [x] Retain existing Release, profile, prompt, and template prose unless direct
  comparison proves a conflict. Their existing actual-consumer, overlap,
  dependency, and systemic-family wording already consumes the revised owners;
  graph them as reviewed-no-change rather than copying the new procedures.
- [x] Re-query every potentially affected standard in the Architecture,
  Contracts, and Planning impact neighborhoods and record `update` or
  `reviewed-no-change`. Preserve the relationship when no text edit is needed
  so the graph continues to route future standards changes; do not add
  application implementation projections.

**Acceptance gate:** SEP-A5 and SEP-A6 pass and all potentially affected
standards have explicit evidence-backed dispositions; the generic authority
fixture has an evidence owner that actually decides it; version-role examples
do not imply unsupported compatibility; and `--state transition --check`
passes after regeneration.

**Acceptance:** [Milestone 3 evidence](reports/milestone-3-promise-and-replanning-acceptance.md)
records the proportional closure, separated version roles, bounded replanning,
15 inspected standards routes, 51-unit/108-relationship standards graph, and
project-agnostic evidence ownership.

**Status:** `Accepted`

### Milestone 4: Projection-Local Invalidation Disposition

**Goal:** Close P1 without conflating project-agnostic standards with the
repository-specific coverage implementation that motivated the hypothesis.

**Allowed write set:** None after Milestone 0 acceptance. The decision artifacts
and executable prototype are owned by Milestone 0.

**Tasks:**

- [x] Retain `workflow.planning.projection-completeness` at semantic revision 1.
- [x] Retain its current `policy-semantic-impact` relationship as
  reviewed-no-change.
- [x] Preserve the bounded prototype as evidence for a separately scoped Coding
  Standards coverage-implementation audit.
- [x] Demonstrate local dependency mutations, a shared-protocol mutation,
  missing-disposition blocking, and the global-horizon over-invalidation
  counterexample without changing normative or verifier authority.

**Acceptance gate:** SEP-A8 is satisfied by a documented no-normative-change
decision; no Planning rule, declarative suite, graph declaration, coverage
attestation, generated input, or generic verifier source changes for P1.

**Status:** `Accepted`

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

- [x] Re-query every revised policy unit's standards-to-standards neighborhood
  and prove one final `update` or `reviewed-no-change` disposition per
  potentially affected standard. Do not count application implementation,
  fixture, suite, prompt, template, or generated-artifact projections as
  standards-impact coverage.
- [x] Verify that each standards-impact relationship identifies a real reason
  the target standard could require inspection when the source changes. A
  matching noun, application behavior, or conformance dependency is not
  sufficient.
- [x] Verify no conditional unit/edge row remains, verify registered suite-input
  freshness, and regenerate the standalone HTML with `--state accepted` from
  the accepted manifests and reviewed before/after delta.
- [x] Run focused suites, graph/compiler checks, plan checks, all-suites
  verification, link checks, and diff hygiene.
- [x] Reconcile this plan, ledger, issues, graph data, and visualization to the
  same accepted state.

**Acceptance gate:** SEP-A1 through SEP-A9 are satisfied, no unresolved or
unconnected graph change remains, every generic rule has project-agnostic
deciding evidence, and all applicable repository checks pass. Any discovered
normative or relationship defect returns to Milestone 2 or 3 instead of being
patched inside final verification.

**Acceptance:** [Final acceptance](reports/final-acceptance.md) records the
accepted graph, milestone evidence, repository checks, and deferred out-of-
scope implementation work.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- The normative standards graph contains a new potentially affected standard
  or a revised relationship meaning.
- The verifier migration has an admitted slice touching the suite registry,
  policy graph, generated suite inputs, or another shared write in this plan.
- Fresh project-agnostic evidence establishes a Projection Completeness gap
  independent of this repository's coverage implementation.
- A proposed rule can only be expressed through A1/A1b/A1c-specific nouns,
  guarantees, or implementation artifacts.
- The repository conformance design adds another suite, checker, registry, or serialized
  contract without a unique claim not owned by the planned portfolio.
- A proposal assigns enforcement to the written standards, requires adopters to
  run this repository's tooling, or spreads another owner's decision procedure
  through otherwise isolated standards.
- A standards-to-standards relationship is missing, misleading, or no longer
  routes to a potentially affected standard.
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

- Acceptance status: `satisfied`
- Deferred follow-ups: repository-specific dependency-local coverage redesign
  and implementation-projection rationale repair remain separately owned.
- Final status: `Accepted`
