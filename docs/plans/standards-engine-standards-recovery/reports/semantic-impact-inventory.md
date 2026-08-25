# Standards Recovery Semantic-Impact Inventory

## Status

This is the pre-change inventory for the standards-recovery plan. It is bound
to planning commit `3439aae9540786d9734431e633ea5b62afb50592`, tree
`0ff4af77ebe5056c9478f04bf65dd87141f573d8`.

Historical A1 behavior is reproduced from accepted commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`. That historical boundary is
distinct from both the standards comparison baseline and any later admitted
policy-implementation base.

It records proposed policy identities and the consumer families that must be
reviewed before policy mutation. It is not a coverage attestation, policy
acceptance, relationship declaration, or implementation admission.

At the planning base:

- policy-unit sources are registered only for Commit, Planning, and
  Verification;
- Verification has only `workflow.verification.acceptance-claims`;
- policy-impact declaration sources exist only for Planning and Commit;
- no accepted policy-impact relationship originates from Router, Verification,
  Contracts, Architecture, Dependencies, or a Generated Contract profile; and
- the provider-v2 horizon has not been audited for the proposed units.

Therefore every current empty impact result below is `unaudited`. It is not
evidence that the policy has no consumers.

The first admission may authorize only read-only reproduction and completion
of this pre-policy scope audit. No normative policy mutation is eligible until every
independent-horizon member and missing consumer class has a planned disposition
and a second independent review accepts the exact post-scope-audit plan tree.

Milestone 0 changes each proposed policy subject from `unaudited` to
`pre-policy-scope-audit-complete` only after the independent horizon has been
examined, every discovered consumer class is mapped, and every mapped consumer
has a planned disposition in the admitted write/read sets. This planning state
is not a coverage attestation or certificate. Final policy coverage cannot be
derived until the policy units, relationships, and horizon-affecting inputs
exist and are frozen.

## Disposition Vocabulary

Every selected consumer must receive exactly one final disposition:

- `updated`: the consumer changes and evidence identifies the exact proposed
  scope plus why it satisfies the policy impact;
- `reviewed-no-change`: the exact consumer revision and scope were reviewed and
  rationale explains why no change is required;
- `not-applicable`: resolved facts and rationale prove the policy does not
  select the consumer;
- `blocked`: required evidence, authority, or implementation is unavailable;
  any blocked consumer prevents recovery acceptance.

`pending-required` below means the implementation milestone must assign one of
the four final dispositions. It is not a completion result.

Likewise, `pre-policy-scope-audit-complete` permits policy-scope admission but
does not satisfy a final disposition or any accepted coverage claim.

## Proposed Policy Units

| Defect family | Proposed stable policy-unit ID | Owning module and exact proposed heading locator | Existing relationship state | Proposed relationship classes | Pre-policy scope-audit state |
| --- | --- | --- | --- | --- | --- |
| Evidence-oracle boundaries | `workflow.verification.evidence-oracle-boundary` | `workflow.verification`; `Evidence Oracle Boundaries` | Unit and edges absent. Existing Verification unit covers only `Acceptance Is A Set Of Claims`. | prompt, template, documentation, fixture, enforcement-suite, and checker projections | `unaudited` |
| Evidence-oracle boundaries | `workflow.verification.negative-fixture-isolation` | `workflow.verification`; `Negative Fixture Isolation` | Unit and edges absent. | planning/checker fixture and enforcement-suite projections | `unaudited` |
| Evidence-oracle boundaries | `workflow.verification.differential-evidence` | `workflow.verification`; `Property And Differential Evidence` | Unit and edges absent. | prompt, fixture, suite, and evidence-report projections | `unaudited` |
| Generated-contract semantic conformance | `topic.contracts.generated-semantic-conformance` | `topic.contracts`; `Generated Contract Semantic Conformance` | Contracts has no policy-unit source and no policy-impact declaration source. | Router, profile, Build, Tooling, prompt, generated-output, validator/generator, facade, test, and suite projections | `unaudited` |
| Generated-contract semantic conformance | `topic.contracts.schema-dialect-and-vocabulary` | `topic.contracts`; `Schema Dialect And Vocabulary` | Unit and edges absent. | profile, dependency-decision, schema declaration, validator, generator, fixture, and suite projections | `unaudited` |
| Generated-contract semantic conformance | `topic.contracts.identity-versus-instance-equality` | `topic.contracts`; `Identity And Instance Equality` | Unit and edges absent. | canonical serializer, schema validator, generated decoder, applicability-value, identity fixture, persisted-handle, and suite projections | `unaudited` |
| Immutable authority closure | `topic.architecture.immutable-authority-closure` | `topic.architecture`; `Immutable Authority Closure` | Architecture has no policy-unit source and no policy-impact declaration source. | snapshot provider/store, analysis-state store, inspection, authorization/provider view, Persistence, public-interface fixture, and suite projections | `unaudited` |
| Implementation-versus-dependency | `topic.dependencies.implementation-versus-dependency` | `topic.dependencies`; `Implementation Versus Dependency` | Dependencies has no policy-unit source and no policy-impact declaration source. | Router, planning/implementation prompt, ADR, dependency fixture, toolchain manifest, and suite projections | `unaudited` |
| Systemic-finding re-planning | `workflow.planning.systemic-finding-replan` | `workflow.planning`; `Systemic-Finding Re-Planning` | New unit absent. Neighboring `workflow.planning.replanning` currently selects `fixtures/planning/consolidation-decisions.tsv`, `planning-consolidation`, and `prompts/planning.md`; those edges do not prove coverage for the new meaning. | planning prompt, implementation prompt, plan template, issue-record, fixture, checker, and suite projections | `unaudited`; existing Planning attestations do not cover the new unit |
| Router completeness | `router.generated-contract-profile-applicability` | `router`; `Generated Contract Profile Applicability` | Router is a canonical module and an existing consumer of Planning/Commit policy, but it has no policy-unit source, no outgoing impact declaration source, and no coverage attestation. | executable Router projection, Generated Contract profile, planning/implementation prompts, routing fixtures, and Router suite | `unaudited` |
| Generated Contract profile applicability | `profile.boundary.generated-contract.applicability` | new `profile.boundary.generated-contract`; `Applicability` | Module, unit, Router rule, and edges absent. | Router prose/executable projection, routing fixtures, planning/implementation prompts, and profile owner-suite projections | `unaudited` |
| Generated Contract profile contract | `profile.boundary.generated-contract.semantic-closure` | new `profile.boundary.generated-contract`; `Semantic Closure` | Unit and edges absent. | Contracts, Verification, Build, Dependencies, generated-output, public-consumer, and suite projections | `unaudited` |

The proposed locators are exact planning bindings. Independent plan admission
must confirm that each heading expresses one coherent meaning. If implementation
needs a different locator, overlapping scope, module metadata locator, split,
merge, or additional policy unit, that is a re-plan trigger rather than a
silent identity change.

## Existing And Proposed Graph Mapping

### Existing graph at the planning base

| Proposed owner | Current declaration source | Current outgoing edges relevant to this recovery | Finding |
| --- | --- | --- | --- |
| `workflow.verification` | none | none | Missing source authority and unaudited consumers |
| `topic.contracts` | none | none | Missing source authority and unaudited consumers |
| `topic.architecture` | none | none | Missing source authority and unaudited consumers |
| `topic.dependencies` | none | none | Missing source authority and unaudited consumers |
| `workflow.planning` | `policy-impact/workflow.planning.toml` | `workflow.planning.replanning` selects the consolidation fixture, `planning-consolidation`, and `prompts/planning.md`; `workflow.planning.findings` selects the consolidation fixture and suite | Existing edges remain valid only for their exact accepted meanings; they neither authorize nor cover `workflow.planning.systemic-finding-replan` |
| `router` | none | none outgoing; Router is currently a target of Planning and Commit relationships | Missing policy-unit source, outgoing source authority, and coverage for the materially changed Router heading |
| `profile.boundary.generated-contract` | none | none | Module and source authority do not yet exist |

### Proposed source-owned declaration sets

| Declaration source | Required source units | Minimum consumer relationship inventory before cutover |
| --- | --- | --- |
| `policy-impact/workflow.verification.toml` | three Verification units | Planning and implementation prompts; plan template where an evidence field is required; verification fixtures and suites; plan-fixture checker; documentation/evidence reports that make acceptance claims |
| `policy-impact/topic.contracts.toml` | three Contracts units | Router and Generated Contract profile; Build and Tooling policy; Language Binding only under real cross-language applicability; schema generators and validators; generated public artifacts; package facades; contract fixtures and suites; canonical serializer, applicability values, and persisted-handle consumers for the equality unit |
| `policy-impact/topic.architecture.toml` | immutable-authority unit | snapshot providers and stores; analysis-state stores; inspection paths; authorization/provider views; Persistence; cold-process fixtures and suites |
| `policy-impact/topic.dependencies.toml` | implementation-versus-dependency unit | Router; planning and implementation prompts; ADR decision expectations; dependency fixtures and suites; applicable toolchain manifests |
| existing `policy-impact/workflow.planning.toml` | new systemic-finding unit | planning and implementation prompts; plan template; issue records; planning fixtures; plan checker and lifecycle suites |
| `policy-impact/router.toml` | Generated Contract profile applicability unit | executable Router projection; Generated Contract profile; planning and implementation prompts; routing fixtures and suite |
| `policy-impact/profile.boundary.generated-contract.toml` | applicability and semantic-closure units | Router projection and routing fixtures; required owner modules; generated artifacts and public consumers; profile fixture and owner suite |

All relationship applicability is initially expected to be `always` where the
consumer is an unconditional projection of the source policy. Conditional
relationships require an existing typed fact contract and reviewed predicate.
No applicability may be inferred from explanatory prose or path names.

## Consumer Audit Matrix

### Evidence-oracle boundaries

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| `prompts/planning.md` | registered projection node | Ensure plans identify claim, domain, oracle, unsupported domain, and intended negative failure | `pending-required` |
| `prompts/implement-plan.md` | registered projection node | Ensure implementation records evidence fidelity and stops on invalid oracle/systemic finding | `pending-required` |
| `templates/PLAN-TEMPLATE.md` | registered projection node | Determine the minimum explicit fields needed without duplicating Verification policy | `pending-required` |
| `workflows/documentation.md` | canonical Documentation workflow | Review durable evidence and acceptance-report projection requirements for oracle-qualified claims | `pending-required`; expected `reviewed-no-change` unless a concrete policy gap is proven |
| `evaluation/standards-effectiveness/check-plan-structure.sh` | retained Bash checker under active migration authority | Review exact current behavior without extending it; new policy enforcement belongs in Python declarative suites | `pending-required`; expected `reviewed-no-change` pending retirement |
| `evaluation/standards-effectiveness/verify-plan-fixtures.sh` | retained Bash checker under active migration authority | Review exact current behavior without extending it; new negative scenarios belong in Python declarative suites | `pending-required`; expected `reviewed-no-change` pending retirement |
| Verification fixture family | horizon member through suite inputs | Add valid/invalid oracle, freshness-only, local-agreement-only, mutation-domain, and isolated-negative cases | `pending-required` |
| Verification suites and suite registry | registered horizon/suite authority | Add enforcement suites and dependencies without copied policy prose as sole oracle | `pending-required` |
| Acceptance and candidate reports | registered documentation/reference corpus through the independent horizon | Audit claims that freshness or local agreement proves semantics and confirm Documentation-owned traceability | `pending-required`; relationship representation must be decided during audit |
| `tools/standards_verifier/**` | package consumer, read-only in this plan | Confirm existing generic suite/checker support is sufficient | `pending-required`; re-plan if update is required |

### Generated-contract semantic conformance and equality

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| `STANDARDS-ROUTER.md` | canonical Router module, not current impact node | Add Generated Contract applicability and conditional Language Binding/IPC rules | `pending-required`; missing consumer registration |
| `evaluation/standards-effectiveness/router-projection.toml` | executable Router projection | Add typed boundary fact/rule and preserve missing-fact behavior | `pending-required`; missing consumer registration |
| `profiles/boundaries/generated-contract.md` | absent | Create specialization requiring Core, Verification, Contracts, and Build; include Dependencies decision applicability | `pending-required` |
| `workflows/build.md` | canonical module | Review deterministic generation, stale output, and build authority | `pending-required`; expected `reviewed-no-change` unless a concrete gap is proven |
| `workflows/tooling.md` | canonical module | Review generator/checker selection and execution ownership | `pending-required`; expected `reviewed-no-change` unless a concrete gap is proven |
| `profiles/boundaries/language-bindings.md` | canonical profile | Confirm it applies only to genuine native/host or cross-language representation | `pending-required` |
| `profiles/applications/library.md` | canonical profile | Confirm public package producer/consumer proof remains required | `pending-required` |
| `workflows/documentation.md` | canonical Documentation workflow | Confirm generated contract decisions, supported semantics, and external-conformance limits are durably projected | `pending-required`; expected `reviewed-no-change` unless a concrete policy gap is proven |
| `topics/licensing.md` | canonical Licensing topic selected by third-party specification use | Confirm the Draft 2020-12 activity remains reference/citation only and preserve the source, version, terms authority, and resulting obligations recorded in the reference Licensing decision | `pending-required`; expected `reviewed-no-change` unless copying, adaptation, or redistribution is proposed |
| `tools/standards_engine/contracts/a1-contract.schema.json` | A1 runtime authority, read-only | Reproduce dialect/equality defect; do not correct in recovery | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| `tools/standards_engine/contracts/generate_contract.py` | A1 runtime implementation, read-only | Inventory generated closure and equality behavior for A1b | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| `tools/standards_engine/standards_engine/_generated_contract.py` | generated public artifact, read-only | Reproduce generated-model semantics and public result behavior | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| `tools/standards_engine/standards_engine/__init__.py` and `tools.py` | public facade/tool adapter, read-only | Audit actual public producer and consumer evidence | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| `tools/standards_metadata/standards_metadata/serialization.py` | identity serializer, read-only | Classify identity canonicalization separately from schema equality | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| Applicability values and persisted handles | A1 domain/state consumers, read-only | Record domain equality and migration questions for A1b without changing them | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| Contract and Generated Contract fixtures/suites | current Contracts suites plus new recovery suite | Prove freshness, shape, semantics, public path, unsupported behavior, Boolean/numeric rules, and Unicode equality separately | `pending-required` |

### Immutable authority closure

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| Snapshot providers and immutable content views | A1 packages, read-only | Inventory complete transitive authority needed by every advertised result | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| Snapshot and analysis-state stores | A1 packages, read-only | Confirm real adapter persistence and exact-handle reconstruction requirements | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| Query/read/related/inspect paths | A1 facade, read-only | Inventory every public result and child handle requiring replay | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| Authorization and provider views | A1 authority inputs, read-only | Require exact immutable authority references rather than fresh ambient configuration | `pending-required`; expected `reviewed-no-change` for recovery and A1b-owned follow-up |
| `profiles/boundaries/persistence.md` | canonical profile | Confirm reopening and store-adapter ownership | `pending-required` |
| Cold-process fixtures and suites | current A1 tests plus new declarative recovery evidence | Distinguish genuine process destruction/reconstruction from in-memory reinjection | `pending-required` |

### Implementation-versus-dependency decisions

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| `STANDARDS-ROUTER.md` and Router projection | canonical/executable route | Ensure difficult standardized semantics select Dependencies | `pending-required` |
| `prompts/planning.md` | registered projection | Require evaluated candidates, conformance support, maintenance/security ownership, and local-subset cost | `pending-required` |
| `prompts/implement-plan.md` | registered projection | Stop and re-plan when an unreviewed implementation/dependency decision appears | `pending-required` |
| ADR expectations | Architecture/Planning documentation convention | Require recorded decision evidence without creating the A1b ADR now | `pending-required` |
| Dependency fixtures and suites | registered suite authority | Add implement/adopt/unsupported/unresolved cases | `pending-required` |
| Toolchain and dependency manifests | independent horizon members where registered | Audit whether any recovery implementation adds a dependency; none is planned | `pending-required`; expected `not-applicable` unless scope changes |

### Systemic-finding re-planning

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| `prompts/planning.md` | registered projection | Require invariant-family and sibling-consumer audit before admitting another local repair | `pending-required` |
| `prompts/implement-plan.md` | registered projection | Stop implementation at a systemic finding and return to the reviewed plan | `pending-required` |
| `templates/PLAN-TEMPLATE.md` | registered projection | Expose class-level acceptance and inventory/disposition fields only where material | `pending-required` |
| `docs/plans/*/issues.md` contract | planning artifact model | Ensure issue records distinguish isolated repair from systemic re-plan trigger | `pending-required`; representation relationship must be audited |
| Planning fixtures and `planning-consolidation` | registered evidence nodes | Add duplicated authority, incomplete projection, ambient authority, public/internal leak, and invalid-oracle cases | `pending-required` |
| Retained plan Bash checkers | active migration-owned consumers | Review current behavior and record `reviewed-no-change`; enforce new recognized-status/evidence and intended-diagnostic behavior through Python declarative suites | `pending-required`; do not add relationships that would preserve retiring implementations as permanent authority |

### Generated Contract Router completeness

| Consumer | Current authority/registration | Required review | Planned disposition |
| --- | --- | --- | --- |
| Router prose boundary table | canonical Router | Add `generated-contract` observable condition | `pending-required` |
| `router.generated-contract-profile-applicability` | absent policy unit | Bind the new Router heading to stable semantic identity and audited outgoing relationships | `pending-required` |
| `routing.boundaries` fact domain and rule set | executable Router projection | Add `generated-contract` while retaining typed unresolved behavior | `pending-required` |
| `canonical-module-corpus.toml` | canonical membership manifest | Register the new Generated Contract profile exactly once so metadata and graph composition can resolve it; treat this as module-membership authority, not a Router policy-impact edge unless the semantic audit proves such a dependency | `pending-required` |
| Generated Contract positive fixture | absent | Select Core, Router, Planning, Implementation, Verification, Documentation, Build, Tooling, Architecture, Contracts, Dependencies, Library, Generated Contract, Persistence, and fact-selected Diagnostics/Security | `pending-required` |
| IPC non-applicability fixture | absent | Exclude IPC when no process or independent-deployment boundary exists | `pending-required` |
| Language Binding non-applicability fixture | absent | Exclude Language Binding when no native/host or cross-language boundary exists | `pending-required` |
| Missing-fact fixture | absent | Produce unresolved/invalid routing instead of a smaller route | `pending-required` |
| Planning and implementation prompts | registered projections | Consume Router output and unresolved facts, not a copied static module list | `pending-required` |

## Missing Or Unaudited Consumer Classes

The following are known gaps at the planning base and must be resolved before
policy mutation can be accepted:

- Canonical Router node `router` exists and is an existing impact consumer, but
  the executable `router-projection.toml` has no direct relationship and Router
  has no outgoing source authority for the new policy.
- Router has no policy-unit declaration source, outgoing impact source, or
  coverage attestation for the materially changed Generated Contract heading.
- Plan checkers are not current policy-impact nodes.
- Verification, Contracts, Architecture, and Dependencies have no declaration
  sources or coverage attestations for the proposed meanings.
- The Generated Contract profile, its policy units, Router rule, fixtures,
  suite, relationships, and attestation do not exist.
- The canonical module corpus does not contain the future Generated Contract
  profile.
- The Documentation workflow and durable acceptance-report projections have
  not been dispositioned for the new evidence and generated-contract policies.
- Licensing is applicable because Draft 2020-12 documentation is selected as
  authority; the reference-only decision is recorded, but the final audit must
  confirm that no later slice expands the activity.
- A1 package files are present in the independent repository horizon but are
  not represented as reviewed policy-impact consumers for these new units.
- Historical reports may contain acceptance-oracle claims, but their role in
  semantic coverage is not yet represented by source-owned relationships.
- Existing Planning coverage covers revision-1 units only and cannot certify
  the new systemic-finding unit.

Milestone 0 must audit the independent horizon rather than close these gaps by
listing only already-known consumers. A newly discovered consumer updates this
inventory and the planned write/read sets. After policy authority exists, the
source-owned graph declaration and final disposition report are updated and
analysis is rerun. The pre-policy audit must not be presented as accepted
policy coverage.

## Required Final Evidence

The final consumer-disposition report must include:

- base and candidate commits and trees;
- every changed policy-unit ID, locator, accepted/proposed semantic revision,
  and structural/content digest;
- exact prior and proposed relationship sets;
- all selected consumers and all independently audited horizon members;
- one final disposition and evidence reference per selected consumer;
- every added, removed, corrected, or retained relationship disposition;
- exact coverage requirement and certificate handles;
- explicit proof that no empty impact result was accepted without coverage;
- Router positive, negative, non-applicable, and unresolved cases;
- focused oracle claims and their independent authorities; and
- all reanalysis points after authoritative metadata changes.
