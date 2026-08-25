# Plan: Standards Engine Standards Recovery

**Plan status:** `Active`

**Current phase:** Milestone 1 live-authority cardinality test implementation

**Next slice:** replace the four admitted live-authority cardinality oracles,
run their focused suites, and commit the test-only prerequisite independently

**Acceptance status:** `partial`

**Planning comparison baseline:** commit
`3439aae9540786d9734431e633ea5b62afb50592`, tree
`0ff4af77ebe5056c9478f04bf65dd87141f573d8`

**Historical A1 reproduction boundary:** commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`

**Reviewed discovery planning snapshot:** commit
`39d5210dcb32611c725052e67a918b4f88de9cc7`, tree
`ef5f626c9bc2300c648fe7f3aa0d482c58d85233`

**Discovery admission transition:** report commit
`2deb5439c5493522a5fb390096994524cf0a556b`, tree
`c1ef4a940c0f08bcd81d70f2d2517d09cb2b7d86`

**Admitted discovery/audit base:** commit
`3082cd9432371071d63d4d6084c9eb15731e6495`, tree
`32e06eef2dddf3e3e235bda7e28c3916fc18c761`

**Reviewed M0 recovery candidate:** commit
`a1dd7b562d84263cca4d0e8ad34770c2effbc7e7`, tree
`4b46dfbaa44e486d3291f1d679d2ab777c1f5b51`

**M0 recovery admission:** report commit
`048f6a75512ba89efbf042f07ef8b8dda3baa337`, tree
`5747e25c8d176e90444aa7b69200cc576f58c2b4`

**Admitted M0 recovery base:** commit
`4788fd816d20ccbbea7004ad04bd3a099c78e68a`, tree
`44b2b7fef3d8a489ba91ca40276b211979da3c00`

**Reviewed policy-implementation candidate:** commit
`ce667c699f0b658949df628e60d1113c9695fdf3`, tree
`5d68ba1e58096520416d5711f391239074dd5714`

**Policy-implementation admission:** report commit
`2adc885202cadd668b8d0ba66bbd9f1f0015d414`, tree
`1ecfa9f8be664576a1521b82bf7bfca78643f168`

**Admitted policy-implementation base:** commit
`59ecd309ae85db9d1f194ca3b49a23e79df51c62`, tree
`669b9d98b3c4baccc96e5bac29ceee06e532dda0`

**Reviewed M1 scope-recovery candidate:** commit
`7a571ed26a132056368ef465d6041910c5a6ed48`, tree
`b1bd7994e9ab3ec8298b57755a285cdf2a72e9f6`

**M1 scope-recovery admission:** report commit
`d4376c3e410841676a0a8d3711254067f875d493`, tree
`db23d1a417dd1fa4322b078d71bc6d377ca210d1`

**Reviewed M1 cardinality-recovery candidate:** commit
`882335b276a9e74024e60060b863c225f6299e91`, tree
`83e7b7e1614e52b822d9182cbceca95ecc43bf8c`

**M1 cardinality-recovery admission:** report commit
`5b1d3fb3677702c97837697570ba91975421ec94`, tree
`189ae67bdd47672bd6637cab7ba14d992aa58471`

**Admitted M1 cardinality-recovery base:** commit
`0bc6343edc90b279733e6a956acefbc9d8b67fcd`, tree
`acd0f113fad64d759b8b38c6799ed891165a5f2d`

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
| SR-A7 | Recovery distinguishes local agreement from external conformance, records the accepted A1 boundary's known nonconformance against independent authority, and assigns runtime correction to A1b without claiming A1 conformance. | `contract` | `not-applicable` | `automated` | `pending` | Pending conformance-classification and known-nonconformance evidence |
| SR-A8 | Schema instance equality and content-identity canonicalization are exercised as separate contracts. | `contract` | `not-applicable` | `automated` | `pending` | Pending equality-domain fixtures |
| SR-A9 | Immutable authority reconstruction succeeds through a genuinely fresh public process and remains unaffected by post-capture source mutation. | `system` | `not-applicable` | `automated` | `pending` | Pending cold-process reconstruction evidence |
| SR-A10 | Every negative fixture satisfies unrelated preconditions and proves the exact intended diagnostic or failure point. | `focused` | `not-applicable` | `automated` | `pending` | Pending isolated negative-fixture evidence |
| SR-A11 | The generated closure, public result, semantic-version identity, and JSON Schema equality repair families are reproduced and recorded without changing A1 runtime behavior. | `contract` | `not-applicable` | `automated` | `satisfied` | [Historical reproductions](reports/historical-a1-repair-reproductions.md) and [equality reproduction](reports/json-schema-instance-equality-reproduction.md) |
| SR-A12 | Immutable reads and cold reconstruction are reproduced through their real public process boundaries without changing A1 runtime behavior. | `system` | `not-applicable` | `automated` | `satisfied` | [Historical reproductions](reports/historical-a1-repair-reproductions.md) records passing public boundaries and the exact unsupported child-handle domain |
| SR-A13 | Every historical acceptance-oracle failure is reproduced at its intended failure point without changing A1 runtime behavior. | `focused` | `not-applicable` | `automated` | `satisfied` | [Historical reproductions](reports/historical-a1-repair-reproductions.md#exact-negative-diagnostics) |
| SR-A14 | One clean candidate commit and tree pass focused recovery checks and all current registered verification. | `integration` | `not-applicable` | `automated` | `pending` | Pending exact-tree candidate report |
| SR-A15 | An independent reviewer accepts the exact standards candidate, its final consumer coverage and dispositions, and every objective claim with no blocked consumer. | `integration` | `not-applicable` | `manual` | `pending` | Pending independent standards-recovery acceptance report |

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
  suite registrations, and Python-verifier declarative support required by the
  new policy.
- Reproduction and durable recording of every historical A1 repair family,
  including the existing JSON Schema equality disagreement, before any later
  A1b correction.
- A reference-only Licensing decision for the selected Draft 2020-12
  specification authority; no third-party content is incorporated.
- Independent plan admission and independent exact-tree standards acceptance.

### Out Of Scope

- Any A1b runtime redesign, contract compiler, validator replacement,
  immutable authority repository, public result-algebra migration, handle
  migration, or compatibility implementation.
- Any production edit under `tools/standards_engine/`, `tools/standards_analysis/`,
  `tools/standards_applicability/`, `tools/standards_policy_impact/`,
  `tools/standards_metadata/`, `tools/standards_graph/`, or
  `tools/graph_engine/`.
- Any test edit under those package trees except these exact test-only recovery
  paths listed in the active Milestone 1 `W`:
  `tools/standards_analysis/tests/test_routing.py`,
  `tools/standards_policy_impact/tests/test_compiler.py`,
  `tools/standards_verifier/tests/test_policy_impact.py`,
  `tools/standards_engine/tests/test_navigation.py`, and
  `tools/standards_engine/tests/test_analysis.py`. This narrow exception does
  not authorize runtime, fixture, contract, or package-interface changes.
- Correcting the JSON Schema equality defect during the reproduction slice or
  as an incidental standards-recovery change.
- Vendoring an external JSON or JSON Schema corpus, adding a third-party
  dependency, or adding JSON-specific standards or permanent verifier machinery.
- Adding a Bash checker or extending a retained Bash checker. The active
  verification-engine migration owns retirement of that surface.
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
- Discovery and policy admissions are pre-milestone transitions, not milestone
  tasks. Each independent report binds one reviewed snapshot and authorizes one
  exact mechanical lifecycle transition. The resulting transition commit is
  the implementation base; `start` records its exact commit and tree before
  changing the plan from `Planned` to `Active`.
- No implementation invocation is admitted while this plan is `Blocked`.
  Writing an independent admission report and applying its authorized
  plan/ledger/issues lifecycle transition are governance operations outside the
  milestones. Any additional transition delta invalidates admission.
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
- Registered declarative suites executed by the Python standards verifier can
  enforce the new standards without changing A1 runtime packages or adding to
  the Bash surface. A missing Python capability requires coordination with the
  active verification-engine migration and a write-set re-plan.
- The historical equality reproduction uses existing accepted A1 inputs, a
  temporary invocation outside repository authority, and the normative Draft
  2020-12 Core section 4.2.2 and Validation section 6.4.3. No upstream test
  corpus, executable, dependency, or copied test vector enters the repository.
- The selected specification is third-party documentation. Its exact identity,
  source, terms authority, reference-only use, and resulting obligations are
  recorded in the
  [reference Licensing decision](reports/draft-2020-12-reference-licensing-decision.md).

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Standards recovery precedes A1b planning; A1b acceptance precedes any separate A2 review. | This plan | [Authoring brief, required sequence](../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md#1-required-sequence) | Any assumption that accepted A1 immediately admits A2 |
| The six defects form one standards outcome, but reproduction is isolated from the coordinated policy cutover so the current JSON Schema defect is recorded before correction. | This plan | User direction and brief sections 5.1-5.6 | Incidental runtime correction during standards work |
| New normative meanings receive distinct stable heading-scoped policy units; the existing `workflow.planning.replanning` unit is not broadened to hide systemic-finding semantics. | Normative document owners and policy-unit sidecars | [Semantic-impact inventory](reports/semantic-impact-inventory.md) | Module-level or convenient-heading impact authority |
| The generic Generated Contract profile applies to program-consumed generated representations; Language Binding specializes it only for a real native/host or cross-language boundary. | Router and Contracts | Authoring brief section 5.2 | Stretching Language Binding over unrelated generation |
| Schema instance equality, domain-value equality, and content-identity canonicalization are separate authority domains. This recovery establishes the policy distinction but does not implement A1b semantics. | Contracts | Authoring brief sections 3 and 6.3 | Reusing identity serialization as schema equality |
| Independent evidence must prove the claimed property; freshness, local agreement, literal matching, mutation detection, and cold-process replay remain distinct claims. | Verification | Authoring brief section 5.1 | One undifferentiated green-check oracle |
| The accepted A1 JSON Schema disagreement is one bounded historical reproduction, not a new repository focus. Existing A1 inputs and directly applicable normative specification clauses determine the expected result; no external test corpus is incorporated. | Verification | Draft 2020-12 Core section 4.2.2 and Validation section 6.4.3 | Vendored JSON Schema fixtures, a new dependency, or JSON-specific recovery policy |
| Selecting Draft 2020-12 as reference authority invokes Licensing even though no file is copied. The accepted activity is citation and comparison only, with provenance retained and no incorporated or redistributed third-party content. | Licensing | [Reference-only Licensing decision](reports/draft-2020-12-reference-licensing-decision.md) | Treating no-copy use as Licensing non-applicability |
| Recovery enforcement uses registered Python declarative suites and adds no Bash checker or Bash-checker behavior. | Verification-engine migration | [Active verification-engine plan](../standards-verification-engine/plan.md) | Temporary Bash enforcement or duplicate migration authority |
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

### Audit State Distinction

`pre-policy-scope-audit-complete` means the independent horizon was examined
against one planned policy meaning, every discovered consumer class was mapped,
and the proposed write/read sets contain a planned disposition for each. It is
planning evidence only. It does not assert that a not-yet-created policy unit,
relationship set, or horizon snapshot has accepted semantic coverage.

Final coverage exists only after the policy authority and horizon-affecting
inputs are frozen, an exact coverage requirement is derived, an authorized
attestation is accepted, and a certificate validates against that exact state.
Pre-policy scope audit records cannot satisfy SR-A3, SR-A4, or final acceptance.

## Required Projection Matrix

| Projection | Required agreement |
| --- | --- |
| `STANDARDS-ROUTER.md` | States observable Generated Contract applicability, owner closure, IPC and Language Binding conditions, and unresolved-fact behavior. |
| Normative standards and profiles | Own the six policy families without duplicate semantics; the new profile specializes application mechanics without replacing Contracts, Verification, Build, or Dependencies. |
| Policy-unit declarations | Bind every new or materially changed heading to one active stable ID, exact locator, owner, and reviewed semantic revision. |
| Semantic graph | Source each policy-impact relationship from the owning policy unit; record typed applicability and independently audited coverage. |
| `prompts/planning.md` and `prompts/implement-plan.md` | Require routed owners, class-level replanning for systemic findings, explicit oracle claims, and complete consumer dispositions without copying a static standards list. |
| `templates/PLAN-TEMPLATE.md` | Provides only the fields necessary to record systemic invariant audits, independent evidence, impact dispositions, and re-plan triggers. |
| Behavioral fixtures | Exercise applicability and non-applicability, intended negative failures, external-conformance classification, semantic mutation, and cold-process reconstruction claims. |
| Executable verification | Enforces Router projection, policy ownership, policy-unit/graph consistency, exact negative diagnostics, independent oracle provenance, and complete registered verification. |

## Historical A1 Repair Reproduction Matrix

Milestone 0 records current behavior for every family below. A passing current
regression proves the repaired behavior remains present; the Unicode equality
case records the still-failing external contract. No result authorizes runtime
changes in this plan.

| Repair family | Required reproduction | Independent or higher-fidelity boundary | Insufficient evidence |
| --- | --- | --- | --- |
| Generated public closure | Exercise fields, types, defaults, requiredness, minimum/other constraints, discriminants, nested request/submission variants, complete result variants, and generated native classes from the canonical schema. | Existing accepted A1 contract and public entry points; mutation of each represented semantic feature must affect generated/runtime acceptance, with limitations recorded for later A1b design. | Field-name equality or generator freshness alone. |
| Public result and package ownership | Call public `prepare` and `resolve`, assert exported generated result classes, exhaust every result conversion, preserve engine programming errors, and verify documented public imports. | Actual package facade and agent-tool adapter, with import inspection across package boundaries. | Constructing generated classes directly or injecting internal result objects. |
| Immutable snapshot reads | Capture a snapshot, mutate source files, then repeat whole-module read and policy inspection through the old handle and compare the complete result. | Captured immutable content through the public engine. | Policy-unit-only reads or handle-string equality. |
| Cold reconstruction | Persist analysis and authority inputs, destroy process state, create a fresh public engine, then inspect the analysis plus every advertised context, requirement, observation, disposition, and certificate handle. | Separate process with only declared persisted authority. | Reusing an in-memory store or injecting private authorizations, providers, graph state, or caches. |
| Semantic-version identity | Hold repository bytes constant while changing each interpretation-affecting contract version, then verify the owning snapshot or analysis identity changes; vary implementation provenance separately and verify identity stability. | Domain-specific identity fixtures derived from the accepted contract-version list. | Displayed version fields that do not participate in identity. |
| Equality and validation | Reproduce the accepted A1 Boolean/integer and Unicode behavior through canonical and generated public entry points, including the known disagreement, without adding permanent JSON-specific fixtures. | Existing accepted A1 inputs and directly applicable Draft 2020-12 specification clauses recorded in the reproduction report. | Agreement between canonical and generated local implementations. |
| Acceptance oracles | Recreate malformed negative fixtures, substring diagnostics, incomplete differential matrices, copied expected literals, freshness-only checks, and sampled mutation claims; then demonstrate the intended stronger check. | Otherwise-valid fixtures, exact diagnostics, complete named matrices, and explicit claim/domain/oracle/unsupported-domain records. | Any nonzero exit, matching substring, or a subject-derived expected value. |

## Pre-Milestone Admission Transitions

Admission is governance over a plan, not implementation of a milestone. The
repository-local report necessarily changes the tree after the reviewed
snapshot, so admission uses an explicitly authorized two-commit transition.

### Discovery Admission

1. An independent reviewer evaluates one exact `Blocked` planning snapshot and
   authors only
   `reports/standards-recovery-discovery-admission.md`. The report binds the
   reviewed commit/tree and either rejects it or authorizes the mechanical
   transition below.
2. If accepted, the integration owner creates one transition commit whose
   parent is the admission-report commit and whose only changed files are
   `plan.md`, `execution-ledger.md`, and `issues.md`. The transition records the
   reviewed snapshot and admission-report commit/tree, sets the plan and
   Milestone 0 to `Planned`, and names Milestone 0 `start` as the sole next
   operation. It may not change scope, tasks, write sets, objectives, or
   evidence contracts.
3. That transition commit is the admitted discovery/audit base. `start` is
   valid only when it is the current `HEAD`; the `start` transition records its
   exact commit/tree in the ledger before creating the `Active` state.

Any intervening commit, additional transition delta, or inability to resolve
the reviewed/report parent chain invalidates admission and requires another
review. No milestone operation occurs while the plan is `Blocked`.

### Milestone 0 Recovery Admission

If Milestone 0 discovers that required evidence changes a generated artifact
outside its admitted write set, Milestone 0 returns to `Blocked` and uses a
distinct recovery admission. This admission is narrower than policy admission:

1. An independent reviewer evaluates one exact blocked M0 replan snapshot and
   authors only
   `reports/standards-recovery-m0-recovery-admission.md`. The report binds the
   reviewed commit/tree and either rejects the replan or authorizes the exact
   generated-evidence closure below. It must link to the authoritative issue
   and reproduction evidence rather than duplicate retained-checker names.
2. If accepted, the integration owner creates one mechanical transition commit
   whose parent is the admission-report commit and whose only changed files are
   `plan.md`, `execution-ledger.md`, and `issues.md`. It records the reviewed
   snapshot and report commit/tree, sets the plan and Milestone 0 to `Planned`,
   and names M0 recovery `start` as the sole next operation. It may not change
   scope, evidence, write sets, objectives, or policy authority.
3. `start` records that exact transition commit/tree and sets the plan and
   Milestone 0 to `Active`. The only newly admitted repository output is the
   mechanically regenerated structure inventory already named in the M0 write
   set.
4. After all documentation inputs are final, regeneration must change only the
   single affected retained-harness inventory record. Only its total and
   documentation inbound counts and corresponding file lists may change. Its
   source, mechanism, executable-reference, contract-reference,
   helper-dependency, and verifier-dependency fields must remain identical;
   every other inventory record, every checker source, and every generated
   dependency-graph artifact must remain byte-identical.
5. The expected current count delta is total inbound `12` to `13` and
   documentation inbound `4` to `5`, with the historical-reproduction report
   as the sole added inbound file. These counts are supporting evidence; the
   field-level structural invariant is authoritative.

No inventory regeneration, policy-admission review, normative policy mutation,
A1b runtime work, or A2 work is permitted before this transition completes.

### Policy-Implementation Admission

After Milestone 0 satisfies its gate, the plan becomes `Blocked` on policy
admission. The same protocol applies: an independent reviewer authors only
`reports/standards-recovery-policy-admission.md` against the exact post-scope-audit
snapshot; a separate mechanical transition commit may change only `plan.md`,
`execution-ledger.md`, and `issues.md`, mark Milestone 0 `Accepted`, set the plan
and Milestone 1 to `Planned`, and name Milestone 1 `start`. That transition
commit is the admitted policy-implementation base, and `start` records its exact
identity. It may not change the audited consumer map, policy write set, or
acceptance contracts.
The report may accept only when every planned policy subject is
`pre-policy-scope-audit-complete`, no planned disposition is blocked, the exact
Milestone 1 write set and protected mapped-consumer closure cover all mapped
consumers, and Python-only fixture execution does not expand retained Bash
behavior. The reviewer must mechanically resolve the 36 suite IDs selected by
the pre-policy scope audit through the canonical suite registry at the reviewed
tree; copied suite-definition or input lists are not admission authority.

### Milestone 1 Scope-Recovery Admission

If an admitted M1 policy change proves that one protected mapped consumer must
change, M1 returns to `Blocked` and uses this bounded scope-recovery protocol:

1. Commit the exact blocked in-progress proposal and replan records before
   modifying the protected consumer. The candidate must identify the failing
   consumer, exact failure, proposed `R` to `W` transfer, and unchanged
   remainder of the admitted closure.
2. An independent reviewer authors only
   `reports/standards-recovery-m1-scope-recovery-admission.md`. The report
   binds that exact commit/tree and may authorize only the one-path transfer of
   `tools/standards_analysis/tests/test_routing.py` from `R` to `W`.
3. If accepted, the integration owner creates one mechanical transition commit
   whose parent is the admission-report commit and whose only changed files are
   `plan.md`, `execution-ledger.md`, and `issues.md`. It records the reviewed
   snapshot and report commit/tree, sets the plan and Milestone 1 to `Planned`,
   and names M1 scope-recovery `start` as the sole next operation. It may not
   change policy, scope, tasks, evidence, or any other closure member.
4. `start` is valid only while that transition is current `HEAD`. It records
   the transition commit/tree, returns the plan and Milestone 1 to `Active`,
   and authorizes modification of only the transferred test beyond paths in
   the originally admitted `W`.
5. The test must remove global fact/rule count assertions and instead verify
   the stable `routing.boundaries` revision/domain and
   `route.boundary.generated-contract` source expression, referenced fact, and
   target. Existing loader closure and target-drift evidence remains unchanged;
   public routing behavior belongs to the registered M1 route fixtures.

The new canonical module changes coverage inputs, so Standards Engine
navigation may remain unavailable against pre-change attestations until the
planned Milestone 2 coverage renewal. That expected intermediate outcome does
not authorize navigation-test mutation or another `R` to `W` transfer. Any
different protected-consumer failure still triggers a separate re-plan.

### Milestone 1 Live-Authority Cardinality Recovery Admission

The source-owned relationship batch exposed a systemic oracle defect in four
protected tests: they assert fixed cardinalities of the mutable repository
authority. Milestone 1 returns to `Blocked` and uses this bounded recovery
protocol before relationship registration continues:

1. Commit the exact blocked proposal and replan records without modifying any
   newly transferred test. The candidate must inventory every live-repository
   cardinality assertion in scope, distinguish it from fixed synthetic-fixture
   cardinality, and specify the semantic replacement.
2. An independent reviewer authors only
   `reports/standards-recovery-m1-cardinality-recovery-admission.md`. The report
   binds that exact commit/tree and may authorize only these transfers from
   `R` to `W`:
   - `tools/standards_policy_impact/tests/test_compiler.py`
   - `tools/standards_verifier/tests/test_policy_impact.py`
   - `tools/standards_engine/tests/test_navigation.py`
   - `tools/standards_engine/tests/test_analysis.py`
3. If accepted, the integration owner creates one mechanical transition commit
   whose parent is the admission-report commit and whose only changed files are
   `plan.md`, `execution-ledger.md`, and `issues.md`. It records the reviewed
   snapshot and report commit/tree, sets the plan and Milestone 1 to `Planned`,
   and names cardinality recovery `start` as the sole next operation. It may
   not change policy, relationships, tasks, evidence, or any other closure
   member.
4. `start` is valid only while that transition is current `HEAD`. It records
   the transition commit/tree, returns the plan and Milestone 1 to `Active`,
   and authorizes modification of only the four transferred tests beyond the
   originally admitted `W`.
5. The compiler test must compare the complete edge-ID and semantics-ID sets
   and retain targeted relationship semantics without asserting their size.
   The verifier test must retain named consumer and suite-owner closure checks
   for both Planning and Commit without asserting either consumer total. The
   navigation test must prove direct and dependency causes are present and
   deduplicated without asserting a repository-topology count or threshold.
   The analysis test must compare dependent-program identities and flattened
   policy-impact reason edge IDs with the compiler-derived relationship set for
   the selected policy, without asserting fan-out or obligation totals.
6. Fixed cardinalities remain permitted only where the test constructs and
   owns the complete bounded fixture and the cardinality is itself the claimed
   behavior. Generated inventory counts remain derived evidence, not copied
   acceptance oracles.

After this test-only prerequisite passes its focused suites, commit it
independently and resume relationship registration. Any additional
live-authority cardinality oracle or protected consumer requiring mutation is a
new re-plan trigger.

## Milestones

### Milestone 0: Historical Reproduction And Pre-Policy Scope Audit

**Goal:** Reproduce the accepted A1 boundary and complete the independent
pre-policy scope audit without changing policy, verifier behavior, or A1 runtime.

**Allowed write set:**

- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/pre-policy-scope-audit.md` (new)
- `docs/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md` (new)
- `docs/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md` (new)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`

**Tasks:**

- [x] Bind every reproduction to accepted A1 commit
  `2359a98740b6035a0414bfaf5427ceaa1301a1c8` and tree
  `97c850ab718287007c1e1daac538f40869f71a1d`.
- [x] Reproduce the known A1 schema-equality disagreement using only existing
  accepted A1 inputs and a temporary invocation; cite the exact normative
  specification clauses and add no external corpus, dependency, or permanent
  JSON-specific fixture.
- [x] Reproduce the complete generated-contract closure family: field names,
  types, defaults, requiredness, constraints, nested variants, result shapes,
  and generated native result ownership.
- [x] Reproduce the public-result boundary family: analysis-domain result
  leakage, exhaustive public conversion, documented public imports, internal
  package imports, and typed engine-error ownership.
- [x] Reproduce the immutable-read family: whole-module reads and inspection
  after source mutation must remain bound to captured authority.
- [x] Reproduce the cold-reconstruction family for analysis state and every
  advertised child handle through a fresh public engine without private cache,
  provider, authorization, or in-memory-store injection.
- [x] Reproduce the semantic-version identity family: interpretation-affecting
  contract versions change the correct snapshot or analysis identity while
  implementation-only releases do not.
- [x] Reproduce the acceptance-oracle family: otherwise-invalid negative
  fixtures, substring-only diagnostics, incomplete Boolean/integer and Unicode
  differential matrices, generated freshness standing in for semantics, and
  two local implementations serving as each other's only oracle.
- [x] Record commands, versions, exact inputs, expected and actual outcomes,
  claimed property, independent oracle, and unsupported domain for every
  historical family without changing runtime code.
- [x] Enumerate every independent-horizon member relevant to each proposed
  policy unit, review every known missing consumer class, and record its planned
  `updated`, `reviewed-no-change`, `not-applicable`, or `blocked` disposition.
- [x] Record current policy-impact results and independently enumerate the
  horizon for every proposed owner, complete the pre-policy scope-audit report,
  and mark every planned policy subject `pre-policy-scope-audit-complete`
  before policy admission.
- [x] Record A1b planning and all A2 work as unavailable while recovery remains
  incomplete.
- [x] Obtain independent M0 recovery admission for the exact blocked replan
  candidate and apply only its authorized mechanical lifecycle transition.
- [x] After all documentation inputs are final, regenerate the admitted
  structure inventory through its existing generator.
- [x] Prove the generated delta satisfies the field-level structural invariant
  in the M0 recovery-admission contract; checker sources and generated
  dependency-graph artifacts remain byte-identical.
- [x] Run focused freshness and plan checks, then one complete declarative and
  retained-checker checkpoint from the final M0 tree.
- [x] After every Milestone 0 criterion passes, set the plan to `Blocked` on the
  separate policy-implementation admission transition; do not mutate normative
  policy.

**Acceptance gate:** Every historical repair family has a reproducible result
from the accepted A1 boundary; the bounded schema-equality disagreement is
recorded against normative specification authority; every planned policy
subject is `pre-policy-scope-audit-complete` with all known horizon members and
missing consumer classes mapped to planned dispositions; generated structure
inventory is fresh and satisfies the admitted field-level delta invariant; no
final coverage, external corpus, policy, verifier behavior, or A1 runtime
changed.

**Status:** `Accepted`

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
- `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-missing-audit.md` (new)
- `evaluation/standards-effectiveness/suites/standards-recovery-routing.toml` (new)
- `evaluation/standards-effectiveness/suites/evidence-oracle-boundaries.toml` (new)
- `evaluation/standards-effectiveness/suites/generated-contract-semantic-conformance.toml` (new)
- `evaluation/standards-effectiveness/suites/immutable-authority-closure.toml` (new)
- `evaluation/standards-effectiveness/suites/implementation-versus-dependency.toml` (new)
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml` (new)
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `tools/standards_analysis/tests/test_routing.py`
- `tools/standards_policy_impact/tests/test_compiler.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_engine/tests/test_navigation.py`
- `tools/standards_engine/tests/test_analysis.py`
- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md` (new)

**Protected mapped-consumer closure:**

The authoritative closure is derived rather than copied into this plan:

- `W` is the exact Milestone 1 allowed write set above.
- `S` is every suite definition and every registered input mechanically
  resolved from the 36 stable suite IDs selected under `Selected Existing
  Suites` in the pre-policy scope audit, using the canonical suite registry at
  the admitted implementation base.
- `E` is the exact non-registry consumer list under `Exact Non-Registry
  Consumers` in the pre-policy scope audit. It contains no wildcard.
- `R = (S union E) - W` is the protected mapped-consumer closure.

Policy admission must prove that every selected suite still resolves to its
admitted definition and inputs, every pre-existing path in `W union R` resolves
at the reviewed tree, each absent `W` path is explicitly marked `(new)` with an
existing parent, `W intersect R` is empty, and the mapped consumers are exactly
`W union R`. The expanded `S` paths may appear in admission evidence, but the
suite registry and selected suite IDs remain their sole authority.

`R` is an audit and mutation-protection boundary, not a restriction on
incidental repository reading. Its members require review and a disposition,
may not be modified without replanning, and remain in final impact coverage.
Only `W` authorizes mutation. If a protected consumer requires a semantic
update rather than a `reviewed-no-change` or `not-applicable` disposition, stop
and re-plan its exact write set. Runtime-package edits remain unavailable.

**Tasks:**

- [x] Add exact, non-overlapping normative headings for all proposed policy
  units in the semantic-impact inventory.
- [x] Update the focused Router projection test to assert the admitted
  `routing.boundaries` revision/domain and Generated Contract rule ID, target,
  referenced fact, and `contains` expression; remove incidental global fact
  and rule cardinality assertions and do not change Router runtime
  implementation.
- [ ] Replace live-repository policy-impact and navigation cardinality oracles
  with semantic identity, exact projection-set agreement, Planning and Commit
  owner closure, cause-presence/deduplication, and compiler-derived analysis
  dependency/reason set assertions; preserve bounded synthetic-fixture
  cardinality tests.
- [ ] Add the Generated Contract profile and route it from observable schema,
  generator, and program-consumer facts; preserve conditional IPC and Language
  Binding selection.
- [ ] Add the new profile to the canonical module corpus and prove that module
  discovery, graph composition, Router output, and metadata closure all resolve
  the same canonical ID.
- [ ] Give the materially changed Router heading its own stable policy unit,
  source-owned impact declaration, mapped consumer set, and coverage subject
  rather than treating Router prose as an unowned projection.
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
- [ ] Register Python declarative suites for every recovery behavior and keep
  generation freshness separate from semantic correctness; add or extend no
  Bash checker.
- [ ] After M1 suite definitions, registered inputs, and documentation are
  final, regenerate the existing checker structure inventory mechanically.
  Permit changes only to inbound-reference count and file-list fields of the
  checker rows explicitly selected by the pre-policy audit. Checker sources,
  source/mechanism fields, executable and dependency fields, generated graph
  artifacts, and every unrelated inventory row must remain unchanged.
- [ ] Run prior/current graph comparison after each metadata batch and update
  the disposition report for every selected consumer.
- [ ] Reject any missing consumer or unresolved final coverage subject rather
  than accepting an empty result.

**Acceptance gate:** Every policy heading resolves exactly once; Router prose
and executable projection agree; current and proposed graph comparison has no
unexplained edge change; every selected consumer has one non-blocked
disposition; focused suites separately prove SR-A6 through SR-A10;
protected runtime paths remain unchanged; the generated checker inventory is
fresh and satisfies its field-level M1 delta contract; all affected declarative
and static verification passes.

**Status:** `Active`

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
| Generated semantic correctness | Mutation and behavioral cases checked against a normative specification, mature independent implementation, or independently reviewed executable specification. | Two local implementations agreeing is consistency only. |
| Schema instance equality | Selected Draft 2020-12 dialect/vocabulary oracle using codepoint-based string equality and schema data-model rules. | Identity canonicalization bytes and Python equality are not schema equality. |
| Content identity | Domain-separated canonical serialization fixtures for the explicitly named identity contract. | Schema instance equality does not define identity normalization. |
| Immutable authority closure | Capture, persist, destroy process state, reconstruct in a genuinely fresh process through public adapters, and compare complete results after source mutation. | Reusing an in-memory store, injected private cache, or live repository path is not cold reconstruction. |
| Negative fixture | Otherwise-valid fixture plus exact diagnostic identity or exact complete diagnostic line for the intended failure. | Nonzero exit or any matching substring is not sufficient. |

## Blockers

- Milestone 0 is accepted and Milestone 1 started from the exact admitted
  transition base. Only the admitted M1 write set and protected-consumer
  contract are active; runtime, A1b, and A2 work remain unavailable.
- The JSON Schema equality disagreement is independently reproduced and remains
  intentionally unresolved for A1b.
- A1b planning, A1b runtime work, and A2 are blocked by independent acceptance
  of this standards recovery; A2 remains blocked further by independent A1b
  acceptance.

## Re-Plan Triggers

- Independent admission rejects or materially changes the six-policy scope,
  consumer inventory, oracle selection, sequence, or write sets.
- Either admission omits the reviewed snapshot, reviewer-report commit/tree,
  authorized transition delta, or resulting implementation base; the parent
  chain differs; or `start` does not record the exact current transition base.
  The comparison baseline remains `3439aae...` and the historical A1
  reproduction boundary remains `2359a987...`.
- A proposed policy locator is missing, duplicated, overlapping, or cannot
  express one coherent semantic unit.
- Impact analysis discovers a required consumer outside `W union R`, a
  protected consumer requires modification, an `E` wildcard appears, or a
  selected suite no longer resolves to its admitted definition and inputs.
- M1 suite or documentation changes stale generated checker evidence outside
  the admitted inbound-reference fields, alter an unrelated inventory row,
  change a checker source/dependency field, or modify a generated dependency
  graph artifact.
- An empty impact result lacks current independent coverage, or the horizon is
  unable to discover consumers omitted from both the graph and node catalog.
- A new or changed permanent relationship, node registration, suite input,
  policy unit, fact contract, provider, or horizon member invalidates an
  already-reviewed impact result or attestation.
- Existing relation kinds, policy-unit schemas, Router projections, or Python
  declarative-suite capabilities cannot represent or enforce the new policy.
  Coordinate any required Python-verifier change with the active migration plan
  and re-plan its exact shared write set; never add a Bash fallback.
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

- Acceptance status: `partial`
- Deferred follow-ups: A1b planning and ADR are gated by this recovery; A2 is
  gated by independently accepted A1b; Plan C remains inactive.
- Final status: `Active`
