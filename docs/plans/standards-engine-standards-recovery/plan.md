# Plan: Standards Engine Standards Recovery

**Plan status:** `Blocked`

**Current phase:** re-planning after independent admission rejection

**Next slice:** revise the plan to separate reproduction/consumer-audit admission
from policy implementation admission, resolve Verification-engine and Licensing
authority, bind the accepted A1 boundary, and request another exact-tree review;
implementation remains unavailable

**Acceptance status:** `pending`

**Planning comparison baseline:** commit
`3439aae9540786d9734431e633ea5b62afb50592`, tree
`0ff4af77ebe5056c9478f04bf65dd87141f573d8`

**Admitted implementation base:** `pending`; the independent plan-admission
record must bind the exact reviewed planning commit and tree before `start`

**Admission review:** `rejected`; see
[standards-recovery-plan-admission.md](reports/standards-recovery-plan-admission.md)

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Semantic-impact inventory:**
[semantic-impact-inventory.md](reports/semantic-impact-inventory.md)

**Authoring brief:**
[Standards Recovery And Standards Engine A1b Redesign](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md)

## Objective

Recover the standards authority needed to govern a later Standards Engine A1b
redesign. The accepted outcome makes evidence-oracle boundaries,
generated-contract semantic conformance, immutable authority closure,
implementation-versus-dependency decisions, systemic-finding re-planning, and
Generated Contract routing explicit and mutually consistent across normative
policy, semantic metadata, agent entry points, fixtures, and executable
verification.

This plan changes standards and their projections only. It does not design or
implement A1b runtime behavior, reopen historical A1 acceptance, or activate
controlled authoring Plan A2.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SR-A1 | Each of the six defect families has normative policy with stable policy-unit identities, exact locators, and no overlapping ownership. | `contract` | `not-applicable` | `automated` | `pending` | Pending locator, metadata, and ownership checks |
| SR-A2 | Router prose and executable projection select the Generated Contract profile and all required owners for applicable tasks, preserve explicit non-applicability for IPC and Language Binding, and return unresolved or invalid when required facts are missing. | `user-workflow` | `not-applicable` | `automated` | `pending` | Pending Router applicability and non-applicability fixtures |
| SR-A3 | Prior and proposed semantic graphs are compared, every changed policy unit has mechanically valid coverage, and no empty impact result is accepted without a valid certificate. | `integration` | `not-applicable` | `automated` | `pending` | Pending graph comparison and coverage-certificate checks |
| SR-A4 | Every selected consumer has exactly one current `updated`, `reviewed-no-change`, `not-applicable`, or `blocked` disposition supported by reviewed evidence. | `integration` | `not-applicable` | `manual` | `pending` | Pending independent consumer-disposition review |
| SR-A5 | Normative documents and profiles, policy-unit declarations, policy-impact relationships, prompts, templates, behavioral fixtures, and executable verifier support agree at one exact tree. | `integration` | `not-applicable` | `automated` | `pending` | Pending coordinated projection evidence |
| SR-A6 | Generated freshness and generated semantic correctness are proved by separate checks. | `contract` | `not-applicable` | `automated` | `pending` | Pending freshness and semantic-conformance evidence |
| SR-A7 | Local implementation agreement and external conformance are proved separately against an official or independently accepted oracle. | `contract` | `not-applicable` | `automated` | `pending` | Pending external-conformance evidence |
| SR-A8 | Schema instance equality and content-identity canonicalization are exercised as separate contracts. | `contract` | `not-applicable` | `automated` | `pending` | Pending equality-domain fixtures |
| SR-A9 | Immutable authority reconstruction succeeds through a genuinely fresh public process and remains unaffected by post-capture source mutation. | `system` | `not-applicable` | `automated` | `pending` | Pending cold-process reconstruction evidence |
| SR-A10 | Every negative fixture satisfies unrelated preconditions and proves the exact intended diagnostic or failure point. | `focused` | `not-applicable` | `automated` | `pending` | Pending isolated negative-fixture evidence |
| SR-A11 | The generated closure, public result, semantic-version identity, and JSON Schema equality repair families are reproduced and recorded without changing A1 runtime behavior. | `contract` | `not-applicable` | `automated` | `pending` | Pending historical contract-reproduction reports |
| SR-A12 | Immutable reads and cold reconstruction are reproduced through their real public process boundaries without changing A1 runtime behavior. | `system` | `not-applicable` | `automated` | `pending` | Pending historical authority-reproduction report |
| SR-A13 | Every historical acceptance-oracle failure is reproduced at its intended failure point without changing A1 runtime behavior. | `focused` | `not-applicable` | `automated` | `pending` | Pending historical oracle-reproduction report |
| SR-A14 | One clean candidate commit and tree pass focused recovery checks and all current registered verification. | `integration` | `not-applicable` | `automated` | `pending` | Pending exact-tree candidate report |
| SR-A15 | An independent reviewer accepts the exact standards candidate, its complete consumer audit, and every objective claim with no blocked consumer. | `integration` | `not-applicable` | `manual` | `pending` | Pending independent standards-recovery acceptance report |

## Scope

### In Scope

- Evidence-oracle policy in Verification, including negative-fixture isolation
  and property/differential evidence contracts.
- Generated-contract semantic-conformance policy in Contracts and one generic
  Generated Contract boundary profile.
- Immutable authority-closure policy in Architecture.
- Implementation-versus-dependency policy in Dependencies.
- Systemic-finding re-planning policy in Planning.
- Router applicability, non-applicability, unresolved-fact behavior, and the
  executable Router projection for Generated Contract work.
- Stable policy-unit declarations, source-owned policy-impact declarations,
  independent consumer-coverage audit, attestations, and change-specific
  dispositions for every changed unit.
- Planning and implementation prompts, the plan template, behavioral fixtures,
  suite registrations, and executable verifier/checker support required by the
  new policy.
- Reproduction and durable recording of every historical A1 repair family,
  including the existing JSON Schema equality disagreement, before any later
  A1b correction.
- Independent plan admission and independent exact-tree standards acceptance.

### Out Of Scope

- Any A1b runtime redesign, contract compiler, validator replacement,
  immutable authority repository, public result-algebra migration, handle
  migration, or compatibility implementation.
- Any edit under `tools/standards_engine/`, `tools/standards_analysis/`,
  `tools/standards_applicability/`, `tools/standards_policy_impact/`,
  `tools/standards_metadata/`, `tools/standards_graph/`, or
  `tools/graph_engine/`.
- Correcting the JSON Schema equality defect during the reproduction slice or
  as an incidental standards-recovery change.
- Controlled authoring, change sessions, proposal mutation, semantic
  acceptance, repository apply, rollback, or recovery from Plan A2.
- External-project baselines or Plan C.
- Rewriting the historical A1 plan, acceptance report, or accepted tree.
- Creating the A1b plan or superseding ADR before this recovery is independently
  accepted.

## Constraints And Assumptions

### Constraints

- Commit `3439aae9540786d9734431e633ea5b62afb50592` is the immutable comparison
  baseline for the brief, prior-state inventory, and policy-impact comparison.
  It is not the implementation checkout after planning commits are added.
- The independent admission report must bind one later exact planning commit
  and tree as the implementation base. `start` is unavailable until that value
  replaces `pending`; implementation from any other base requires re-planning
  and a refreshed current-state inventory.
- No implementation invocation is admitted while this plan is `Blocked`.
  Independent admission must bind the reviewed commit and tree, confirm the
  bounded write sets, and transition the plan to `Planned` before `start` is
  valid.
- Policy authority and every required projection are one coordinated outcome.
  No milestone may accept prose-only policy or executable behavior without its
  normative owner.
- Every authoritative metadata change requires prior/current impact analysis.
  Newly discovered permanent consumers are declared, coverage is re-audited,
  and analysis is rerun from the changed tree before work continues.
- An empty policy-impact result is unresolved until an independent horizon and
  valid attestation prove complete consumer discovery for that exact policy
  state.
- Attestation renewal occurs only after all policy units, relationships,
  Router metadata, node registrations, suites, and horizon-affecting inputs are
  frozen.
- Independent acceptance evidence cannot be authored solely by the
  implementation owner and cannot use two local implementations as the only
  external-conformance oracle.
- A2 remains inactive through standards recovery and through subsequent A1b
  planning, implementation, migration, and independent acceptance.

### Assumptions

- Existing policy-unit heading locators can represent each proposed unit after
  the named headings are added. Duplicate, ambiguous, overlapping, or
  non-resolving locators trigger re-planning before policy mutation.
- Existing policy-impact relation kinds and the provider-v2 independent audit
  horizon can represent the required consumers without runtime changes. A need
  for a new relation kind, provider behavior, or compiler capability is a
  re-plan trigger.
- Declarative suites and existing Bash checker adapters can enforce the new
  standards without changing A1 runtime packages. This must be proven during
  the implementation milestone rather than assumed at acceptance.
- The external executable oracle is the official
  `json-schema-org/JSON-Schema-Test-Suite` at commit
  `b01af8c8d50244a2eb4dd3e01073e24823aa8691`. Milestone 0 vendors the exact
  upstream `LICENSE` and Draft 2020-12 `const.json`, `enum.json`,
  `uniqueItems.json`, `pattern.json`, and `type.json` files, records their
  digests, and executes only the subset supported by current A1 declarations.
  The normative equality oracle remains Draft 2020-12 Core section 4.2.2 and
  Validation section 6.4.3. Focused Unicode vectors not present upstream must
  identify the specification rule that determines each expected result.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Standards recovery precedes A1b planning; A1b acceptance precedes any separate A2 review. | This plan | [Authoring brief, required sequence](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md#1-required-sequence) | Any assumption that accepted A1 immediately admits A2 |
| The six defects form one standards outcome, but reproduction is isolated from the coordinated policy cutover so the current JSON Schema defect is recorded before correction. | This plan | User direction and brief sections 5.1-5.6 | Incidental runtime correction during standards work |
| New normative meanings receive distinct stable heading-scoped policy units; the existing `workflow.planning.replanning` unit is not broadened to hide systemic-finding semantics. | Normative document owners and policy-unit sidecars | [Semantic-impact inventory](reports/semantic-impact-inventory.md) | Module-level or convenient-heading impact authority |
| The generic Generated Contract profile applies to program-consumed generated representations; Language Binding specializes it only for a real native/host or cross-language boundary. | Router and Contracts | Authoring brief section 5.2 | Stretching Language Binding over unrelated generation |
| Schema instance equality, domain-value equality, and content-identity canonicalization are separate authority domains. This recovery establishes the policy distinction but does not implement A1b semantics. | Contracts | Authoring brief sections 3 and 6.3 | Reusing identity serialization as schema equality |
| Independent evidence must prove the claimed property; freshness, local agreement, literal matching, mutation detection, and cold-process replay remain distinct claims. | Verification | Authoring brief section 5.1 | One undifferentiated green-check oracle |
| External schema conformance uses a pinned official corpus and normative specification, retained with upstream licensing; local focused vectors may extend coverage but cannot replace that oracle. | Verification and Licensing | JSON Schema Test Suite commit `b01af8c8d50244a2eb4dd3e01073e24823aa8691` and Draft 2020-12 | Unpinned network content or two local implementations as sole oracle |
| Current and proposed impact results are evidence inputs, not completeness proof. Coverage and per-consumer dispositions are mandatory. | Planning and coverage authority | `workflows/planning.md` projection-completeness policy | Treating zero edges as no impact |

## Simplicity And Ownership Review

- Independent concepts: normative policy meaning; Router applicability;
  policy-unit identity; semantic consumer relationships; coverage attestation;
  behavioral evidence; A1b runtime design.
- Intentional coupling: a normative change and its Router, graph, prompt,
  template, fixture, and verifier projections are accepted together.
- Accidental coupling risk: using current A1 packages to implement recovery
  policy, deriving impact from paths or prose, treating the node catalog as the
  only audit horizon, or allowing copied expected literals to validate their
  own source.
- Policy/state/lifecycle owners: canonical Markdown owns policy; policy-unit
  sidecars own semantic identity; source-owned policy-impact declarations own
  consumer relationships; coverage attestations own audited completeness;
  this plan owns sequencing and dispositions.
- Future changes that should remain independent: A1b contract/compiler and
  storage design, A2 controlled authoring, and Plan C external baselines.

## Semantic Impact Control

The pre-change mapping is recorded in
[semantic-impact-inventory.md](reports/semantic-impact-inventory.md). For each
policy unit, implementation must preserve this control loop:

1. Resolve the stable policy-unit ID and exact heading locator in the accepted
   base.
2. Record current graph relationships and current coverage state.
3. Materialize the proposed policy, policy unit, relationships, and projections
   in one candidate tree.
4. Compare prior and proposed graphs and retain every selected consumer.
5. Audit the independent horizon for missing consumers and add every permanent
   relationship through its source-owned declaration.
6. Assign exactly one disposition to each selected consumer.
7. Rerun analysis after every authority-metadata change.
8. Freeze the final horizon, renew attestations once, generate certificates,
   and verify that no consumer is missing, duplicated, stale, or blocked.

The initial inventory records no accepted relationships for the proposed new
units. That is an unaudited starting condition, not evidence of no impact.

## Required Projection Matrix

| Projection | Required agreement |
| --- | --- |
| `STANDARDS-ROUTER.md` | States observable Generated Contract applicability, owner closure, IPC and Language Binding conditions, and unresolved-fact behavior. |
| Normative standards and profiles | Own the six policy families without duplicate semantics; the new profile specializes application mechanics without replacing Contracts, Verification, Build, or Dependencies. |
| Policy-unit declarations | Bind every new or materially changed heading to one active stable ID, exact locator, owner, and reviewed semantic revision. |
| Semantic graph | Source each policy-impact relationship from the owning policy unit; record typed applicability and independently audited coverage. |
| `prompts/planning.md` and `prompts/implement-plan.md` | Require routed owners, class-level replanning for systemic findings, explicit oracle claims, and complete consumer dispositions without copying a static standards list. |
| `templates/PLAN-TEMPLATE.md` | Provides only the fields necessary to record systemic invariant audits, independent evidence, impact dispositions, and re-plan triggers. |
| Behavioral fixtures | Exercise applicability and non-applicability, intended negative failures, external conformance, semantic mutation, and cold-process reconstruction claims. |
| Executable verification | Enforces Router projection, policy ownership, policy-unit/graph consistency, exact negative diagnostics, independent oracle provenance, and complete registered verification. |

## Historical A1 Repair Reproduction Matrix

Milestone 0 records current behavior for every family below. A passing current
regression proves the repaired behavior remains present; the Unicode equality
case records the still-failing external contract. No result authorizes runtime
changes in this plan.

| Repair family | Required reproduction | Independent or higher-fidelity boundary | Insufficient evidence |
| --- | --- | --- | --- |
| Generated public closure | Exercise fields, types, defaults, requiredness, minimum/other constraints, discriminants, nested request/submission variants, complete result variants, and generated native classes from the canonical schema. | Canonical schema plus pinned official keyword cases for the supported subset; mutation of each represented semantic feature must affect generated/runtime acceptance. | Field-name equality or generator freshness alone. |
| Public result and package ownership | Call public `prepare` and `resolve`, assert exported generated result classes, exhaust every result conversion, preserve engine programming errors, and verify documented public imports. | Actual package facade and agent-tool adapter, with import inspection across package boundaries. | Constructing generated classes directly or injecting internal result objects. |
| Immutable snapshot reads | Capture a snapshot, mutate source files, then repeat whole-module read and policy inspection through the old handle and compare the complete result. | Captured immutable content through the public engine. | Policy-unit-only reads or handle-string equality. |
| Cold reconstruction | Persist analysis and authority inputs, destroy process state, create a fresh public engine, then inspect the analysis plus every advertised context, requirement, observation, disposition, and certificate handle. | Separate process with only declared persisted authority. | Reusing an in-memory store or injecting private authorizations, providers, graph state, or caches. |
| Semantic-version identity | Hold repository bytes constant while changing each interpretation-affecting contract version, then verify the owning snapshot or analysis identity changes; vary implementation provenance separately and verify identity stability. | Domain-specific identity fixtures derived from the accepted contract-version list. | Displayed version fields that do not participate in identity. |
| Equality and validation | Exercise Boolean/integer type distinctions, Unicode codepoint distinctions, `const`, `enum`, `uniqueItems`, and regular-expression search semantics through canonical and generated public entry points. | Draft 2020-12 specification plus pinned official test corpus; focused Unicode vectors cite the exact normative rule. | Agreement between canonical and generated local implementations. |
| Acceptance oracles | Recreate malformed negative fixtures, substring diagnostics, incomplete differential matrices, copied expected literals, freshness-only checks, and sampled mutation claims; then demonstrate the intended stronger check. | Otherwise-valid fixtures, exact diagnostics, complete named matrices, and explicit claim/domain/oracle/unsupported-domain records. | Any nonzero exit, matching substring, or a subject-derived expected value. |

## Milestones

### Milestone 0: Reproduction And Frozen Admission Baseline

**Goal:** Establish a reviewed, reproducible defect and impact baseline without
changing policy or A1 runtime behavior.

**Allowed write set:**

- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`
- `docs/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-plan-admission.md`
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/LICENSE` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/const.json` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/enum.json` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/pattern.json` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/type.json` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/fixtures/contracts/json-schema-test-suite-b01af8c8/uniqueItems.json` (new, byte-identical upstream file)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`

**Tasks:**

- [ ] Obtain independent plan admission bound to the exact planning commit and
  tree; confirm scope, write sets, consumer audit, independent oracles, and the
  absence of A1b/A2 implementation.
- [ ] Transition this plan from `Blocked` to `Planned`, then admit `start` for
  this milestone from the reviewed boundary.
- [ ] Reproduce current `const`, `enum`, and `uniqueItems` behavior for composed
  and decomposed Unicode strings and compare it with the pinned Draft 2020-12
  contract or official test corpus.
- [ ] Retrieve the six admitted upstream files from exact commit
  `b01af8c8d50244a2eb4dd3e01073e24823aa8691`, preserve their bytes and license,
  record source and SHA-256 digests, and reject any fetch or digest mismatch.
- [ ] Reproduce the complete generated-contract closure family: field names,
  types, defaults, requiredness, constraints, nested variants, result shapes,
  and generated native result ownership.
- [ ] Reproduce the public-result boundary family: analysis-domain result
  leakage, exhaustive public conversion, documented public imports, internal
  package imports, and typed engine-error ownership.
- [ ] Reproduce the immutable-read family: whole-module reads and inspection
  after source mutation must remain bound to captured authority.
- [ ] Reproduce the cold-reconstruction family for analysis state and every
  advertised child handle through a fresh public engine without private cache,
  provider, authorization, or in-memory-store injection.
- [ ] Reproduce the semantic-version identity family: interpretation-affecting
  contract versions change the correct snapshot or analysis identity while
  implementation-only releases do not.
- [ ] Reproduce the acceptance-oracle family: otherwise-invalid negative
  fixtures, substring-only diagnostics, incomplete Boolean/integer and Unicode
  differential matrices, generated freshness standing in for semantics, and
  two local implementations serving as each other's only oracle.
- [ ] Record commands, versions, exact inputs, expected and actual outcomes,
  claimed property, independent oracle, and unsupported domain for every
  historical family without changing runtime code.
- [ ] Re-run current policy-impact and coverage analysis for every proposed
  policy owner and replace any incomplete inventory row before normative edits.
- [ ] Record A1b planning and all A2 work as unavailable while recovery remains
  incomplete.

**Acceptance gate:** Independent plan-admission report accepts the exact plan
tree and binds it as the implementation base; every historical repair family
has a reproducible current-state result, the JSON Schema disagreement is
reproducible through both current public and canonical validation paths against
an independent oracle, no file outside the allowed write set changed, and no
runtime behavior was corrected.

**Status:** `Blocked` pending independent plan admission

### Milestone 1: Coordinated Standards Authority Cutover

**Goal:** Introduce the six policy families and all required routing,
semantic-graph, agent, template, fixture, and enforcement projections as one
coherent candidate authority.

**Allowed write set:**

- `workflows/verification.md`
- `topics/contracts.md`
- `topics/architecture.md`
- `topics/dependencies.md`
- `workflows/planning.md`
- `profiles/boundaries/generated-contract.md` (new)
- `STANDARDS-ROUTER.md`
- `evaluation/standards-effectiveness/canonical-module-corpus.toml`
- `evaluation/standards-effectiveness/router-projection.toml`
- `evaluation/standards-effectiveness/policy-units/registry.toml`
- `evaluation/standards-effectiveness/policy-units/router.toml` (new)
- `evaluation/standards-effectiveness/policy-units/verification.toml`
- `evaluation/standards-effectiveness/policy-units/contracts.toml` (new)
- `evaluation/standards-effectiveness/policy-units/architecture.toml` (new)
- `evaluation/standards-effectiveness/policy-units/dependencies.toml` (new)
- `evaluation/standards-effectiveness/policy-units/planning.toml`
- `evaluation/standards-effectiveness/policy-units/generated-contract.toml` (new)
- `evaluation/standards-effectiveness/policy-impact-registry.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-impact/router.toml` (new)
- `evaluation/standards-effectiveness/policy-impact/workflow.verification.toml` (new)
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml` (new)
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml` (new)
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml` (new)
- `evaluation/standards-effectiveness/policy-impact/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-impact/profile.boundary.generated-contract.toml` (new)
- `prompts/planning.md`
- `prompts/implement-plan.md`
- `templates/PLAN-TEMPLATE.md`
- `evaluation/standards-effectiveness/fixtures/routing/generated-contract-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/routing/generated-contract-routes.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/verification/evidence-oracle-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/contracts/generated-contract-conformance-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/architecture/immutable-authority-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/dependencies/implementation-versus-dependency-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-replan-decisions.tsv` (new)
- `evaluation/standards-effectiveness/fixtures/plans/invalid-systemic-finding-missing-audit.md` (new)
- `evaluation/standards-effectiveness/suites/standards-recovery-routing.toml` (new)
- `evaluation/standards-effectiveness/suites/evidence-oracle-boundaries.toml` (new)
- `evaluation/standards-effectiveness/suites/generated-contract-semantic-conformance.toml` (new)
- `evaluation/standards-effectiveness/suites/immutable-authority-closure.toml` (new)
- `evaluation/standards-effectiveness/suites/implementation-versus-dependency.toml` (new)
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml` (new)
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/check-plan-structure.sh`
- `evaluation/standards-effectiveness/verify-plan-fixtures.sh`
- `evaluation/standards-effectiveness/verify-standards-recovery.sh` (new)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md` (new)

**Read-only required consumers:**

- `workflows/build.md`
- `workflows/documentation.md`
- `workflows/tooling.md`
- `topics/licensing.md`
- `workflows/implementation.md`
- `profiles/applications/library.md`
- `profiles/boundaries/language-bindings.md`
- `profiles/boundaries/ipc.md`
- `profiles/boundaries/persistence.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-acceptance.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-ii-candidate.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-iii-candidate.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-iv-candidate.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-v-candidate.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-vi-candidate.md`
- `docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`
- `tools/standards_engine/**`
- `tools/standards_analysis/**`
- `tools/standards_applicability/**`
- `tools/standards_metadata/**`
- `tools/standards_policy_impact/**`
- `tools/standards_graph/**`
- `tools/standards_verifier/**`

If a read-only consumer requires a semantic update rather than a
`reviewed-no-change` or `not-applicable` disposition, stop and re-plan its exact
write set. Runtime-package edits are not admitted by this plan.

**Tasks:**

- [ ] Add exact, non-overlapping normative headings for all proposed policy
  units in the semantic-impact inventory.
- [ ] Add the Generated Contract profile and route it from observable schema,
  generator, and program-consumer facts; preserve conditional IPC and Language
  Binding selection.
- [ ] Add the new profile to the canonical module corpus and prove that module
  discovery, graph composition, Router output, and metadata closure all resolve
  the same canonical ID.
- [ ] Give the materially changed Router heading its own stable policy unit,
  source-owned impact declaration, complete consumer audit, and coverage
  subject rather than treating Router prose as an unowned projection.
- [ ] Register every policy unit and compile source-owned relationships to all
  reviewed projections and evidence consumers.
- [ ] Update Planning and implementation prompts and the plan template to
  consume routed authority and systemic-finding/independent-evidence policy.
- [ ] Review the Documentation workflow and durable acceptance-report
  projections explicitly; update no Documentation policy unless the audit
  triggers a write-set re-plan.
- [ ] Add positive, negative, non-applicable, unresolved, semantic-mutation,
  and cold-process behavioral fixtures.
- [ ] Ensure every negative fixture satisfies unrelated preconditions and
  asserts the exact intended diagnostic, not generic failure.
- [ ] Add executable checker and suite support using an independent oracle when
  the claim is external conformance; generation freshness remains a separate
  check.
- [ ] Run prior/current graph comparison after each metadata batch and update
  the disposition report for every selected consumer.
- [ ] Reject any remaining missing or unaudited consumer rather than accepting
  an empty result.

**Acceptance gate:** Every policy heading resolves exactly once; Router prose
and executable projection agree; current and proposed graph comparison has no
unexplained edge change; every selected consumer has one non-blocked
disposition; focused suites separately prove SR-A6 through SR-A10;
forbidden runtime paths remain unchanged; all affected declarative and static
verification passes.

**Status:** `Blocked` by Milestone 0

### Milestone 2: Coverage Freeze And Exact-Tree Acceptance

**Goal:** Freeze the complete semantic authority, renew coverage exactly once,
and obtain independent acceptance of one clean standards-recovery tree.

**Allowed write set:**

- `evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/router.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.contracts.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.architecture.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml` (new)
- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-candidate.md` (new)
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md` (new, independent reviewer owned)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`

**Tasks:**

- [ ] Freeze policy, Router, registry, relationship, suite, node-catalog, and
  all other horizon-affecting inputs before attestation work.
- [ ] Derive final coverage requirements mechanically from the frozen candidate
  and obtain authorized attestations for every changed policy unit.
- [ ] Generate certificates, rerun impact analysis, and prove exact equality
  between required coverage subjects and valid certificate subjects.
- [ ] Prove every selected consumer has exactly one current, non-blocked
  disposition and that no missing consumer remains in the independent horizon.
- [ ] Run focused recovery checks, complete registered declarative suites,
  retained Bash checkers, verifier tests, link checks, plan checks, generated
  freshness checks, and `git diff --check` from one clean tree.
- [ ] Record one candidate commit and tree without claiming acceptance.
- [ ] Obtain independent Standards and specification review of that exact tree;
  only the independent acceptance record may satisfy SR-A15.
- [ ] Mark this recovery `Accepted` only after all objective rows are satisfied.
  Then, and only then, a separate A1b plan and superseding ADR may be authored.

**Acceptance gate:** One independent report accepts the exact clean candidate
commit and tree; all SR-A1 through SR-A15 claims have matching evidence; every
non-deferred milestone is accepted; no consumer is blocked; no A1b or A2
implementation exists.

**Status:** `Blocked` by Milestone 1

## Verification Strategy

The recovery uses separate evidence lanes. Passing one lane cannot satisfy a
different claim:

| Claim | Required oracle | Explicit non-proof |
| --- | --- | --- |
| Generated freshness | Regenerate and compare exact generated output to the checked-in projection. | Fresh output does not prove complete traversal or correct semantics. |
| Generated semantic correctness | Mutation and behavioral cases checked against an official corpus, mature independent implementation, or independently reviewed executable specification. | Two local implementations agreeing is consistency only. |
| Schema instance equality | Selected Draft 2020-12 dialect/vocabulary oracle using codepoint-based string equality and schema data-model rules. | Identity canonicalization bytes and Python equality are not schema equality. |
| Content identity | Domain-separated canonical serialization fixtures for the explicitly named identity contract. | Schema instance equality does not define identity normalization. |
| Immutable authority closure | Capture, persist, destroy process state, reconstruct in a genuinely fresh process through public adapters, and compare complete results after source mutation. | Reusing an in-memory store, injected private cache, or live repository path is not cold reconstruction. |
| Negative fixture | Otherwise-valid fixture plus exact diagnostic identity or exact complete diagnostic line for the intended failure. | Nonzero exit or any matching substring is not sufficient. |

## Blockers

- Independent plan admission rejected the current plan and semantic inventory.
  No implementation operation is available; the exact findings are recorded in
  [the admission report](reports/standards-recovery-plan-admission.md).
- The JSON Schema equality disagreement remains intentionally unresolved until
  Milestone 0 records an independent reproduction.
- A1b planning, A1b runtime work, and A2 are blocked by independent acceptance
  of this standards recovery; A2 remains blocked further by independent A1b
  acceptance.

## Re-Plan Triggers

- Independent admission rejects or materially changes the six-policy scope,
  consumer inventory, oracle selection, sequence, or write sets.
- The independent admission record does not bind its exact reviewed planning
  commit and tree as the implementation base, or implementation begins from a
  different tree. The comparison baseline remains
  `3439aae9540786d9734431e633ea5b62afb50592` and is not replaced by admission.
- A proposed policy locator is missing, duplicated, overlapping, or cannot
  express one coherent semantic unit.
- Impact analysis discovers a required consumer outside Milestone 1's write or
  explicit read-only sets, or a read-only consumer requires modification.
- An empty impact result lacks current independent coverage, or the horizon is
  unable to discover consumers omitted from both the graph and node catalog.
- A new or changed permanent relationship, node registration, suite input,
  policy unit, fact contract, provider, or horizon member invalidates an
  already-reviewed impact result or attestation.
- Existing relation kinds, policy-unit schemas, Router projections,
  declarative suites, or verifier/checker adapters cannot represent or enforce
  the new policy without a runtime package change.
- The Draft 2020-12 defect cannot be reproduced independently, the chosen
  external oracle is unavailable or ambiguous, or a local implementation is
  being used as its own only oracle.
- A negative fixture fails before the intended condition or cannot expose an
  exact diagnostic.
- A finding reveals another member of the same invariant family that is not in
  the inventory; stop local repair, expand the systemic audit, and obtain plan
  review before continuing.
- Generated Contract applicability requires a second static routing authority
  or cannot be represented by the Router's existing typed facts and rules.
- A third-party dependency or a decision to implement standardized semantics
  becomes necessary during recovery. That decision belongs to later A1b
  planning under the recovered Dependencies policy.
- Any A1b runtime, migration, persisted-state, contract-version, handle-version,
  or A2 authoring requirement enters the implementation scope.
- A milestone misses its acceptance gate, a lower-fidelity check is proposed
  for a higher-fidelity claim, or an independent reviewer cannot accept the
  exact tree.

## Concurrent Work

No concurrent implementation is admitted. Normative documents, Router
authority, policy-unit registries, semantic-graph declarations, coverage
attestations, shared prompts/templates, suite registry, active plan, and final
candidate commit remain serial integration-owner writes. Independent reviewers
may inspect immutable candidate trees and author only their named review report.

## Subsequent A1b Planning Gate

Only after Milestone 2 is independently accepted may a separate A1b plan and
superseding ADR be created. That planning phase must, at minimum:

- evaluate a mature Draft 2020-12 validator against an explicitly bounded local
  implementation option;
- define JSON Schema instance equality, A1 domain-value equality, and identity
  canonicalization separately;
- design one contract-compilation module and one immutable authority
  repository;
- inventory every public consumer and persisted A1 state;
- decide coordinated contract, schema, result, snapshot, state, and handle
  version migration; and
- preserve one public result algebra behind the Standards Engine facade.

This gate authorizes planning only. A1b implementation still requires its own
admitted plan and superseding ADR. A2 remains inactive until A1b implementation,
migration, and independent exact-tree acceptance are complete.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: A1b planning and ADR are gated by this recovery; A2 is
  gated by independently accepted A1b; Plan C remains inactive.
- Final status: `Blocked`
