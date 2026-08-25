# Standards Recovery Pre-Policy Scope Audit

**Status:** `pre-policy-scope-audit-complete`

**Audit base commit:**
`6f3c52a05f86e76b5fd14d54e534c864e46f6ca3`

**Audit base tree:**
`c98a2be6ef73632ae0ac5a411d8f32c34df8b7f6`

## Purpose And Limits

This report establishes the planned consumer map and bounded write/read sets
before any policy exists. It is not a coverage attestation, certificate,
semantic acceptance, consumer disposition, or policy-implementation
admission. Final coverage is possible only after policy units, relationships,
suite inputs, and all other horizon-affecting authority are frozen.

## Independent Horizon

The current provider-v2 horizon was loaded from the audit base through
`load_canonical_standards_corpus()` and `load_coverage_horizon()`.

```text
provider  standards-analysis:policy-impact-consumer-horizon
version   2
digest    sha256:35ed5271ffb9573eb1ae4dd6949debd9f6aad011bb9d0b43dbbfba9eb5b077e9
members   856
inputs    583
```

| Typed role | Count | Audit treatment |
| --- | ---: | --- |
| canonical module | 58 | Every module was classified by owner/applicability; selected modules are enumerated below |
| policy unit | 29 | Existing Planning and Verification neighbors were reviewed; Commit units do not own or project the proposed meanings |
| edge-source registration | 5 | All affect graph completeness and remain required audit authority |
| edge-source manifest | 1 | The complete policy-impact node catalog was reviewed |
| registered suite | 218 | Suites were classified by owner and input domain; selected suites are enumerated below |
| suite definition | 218 | Follows the selected suite classification |
| registered-suite input | 355 | Exact selected inputs follow their consuming suite and policy family |
| supplemental policy-impact node | 27 | Every node was classified; selected projections/evidence are enumerated below |

Counts overlap where one repository member has more than one role. The exact
horizon digest and role counts provide reconciliation for the full set; the
lists below enumerate every member selected as relevant. Non-selected members
are `not-applicable` at the planning level because their registered owner and
input domain concern unrelated language, release, frontend, accessibility,
concurrency, or other policy semantics. This does not create a final consumer
disposition.

## Current Impact Results

Read-only `policy-impact` outgoing queries for `workflow.verification`,
`topic.contracts`, `topic.architecture`, `topic.dependencies`,
`workflow.planning`, and `router` each returned only the TSV header. The future
Generated Contract profile does not exist. These empty module-level results
are recorded as missing authority, not proof of no impact.

## Selected Canonical Modules And Profiles

| Member | Selected policy family | Planned disposition |
| --- | --- | --- |
| `STANDARDS-ROUTER.md` | Generated Contract, dependency decision, Router completeness | `updated` |
| `workflows/verification.md` | evidence oracles | `updated` |
| `topics/contracts.md` | generated semantics, dialect, equality | `updated` |
| `topics/architecture.md` | immutable authority closure | `updated` |
| `topics/dependencies.md` | implementation-versus-dependency | `updated` |
| `workflows/planning.md` | systemic-finding re-planning | `updated` |
| `profiles/boundaries/generated-contract.md` | Generated Contract applicability and semantic closure | `updated` (new) |
| `workflows/build.md` | generated-output authority | `reviewed-no-change` unless policy drafting proves a gap |
| `workflows/tooling.md` | generator and verifier selection | `reviewed-no-change` unless policy drafting proves a gap |
| `workflows/documentation.md` | durable evidence and conformance-limit projection | `reviewed-no-change` unless policy drafting proves a gap |
| `workflows/implementation.md` | implementation entrypoint and evidence transport | `reviewed-no-change` |
| `topics/licensing.md` | reference-only Draft 2020-12 selection | `reviewed-no-change`; reopen on incorporation or redistribution |
| `profiles/applications/library.md` | public package/independent consumer boundary | `reviewed-no-change` |
| `profiles/boundaries/persistence.md` | immutable store reopening | `reviewed-no-change` |
| `profiles/boundaries/language-bindings.md` | only genuine cross-language representation | `not-applicable` unless Router facts select it |
| `profiles/boundaries/ipc.md` | only process or independent deployment boundary | `not-applicable` unless Router facts select it |

Core, Diagnostics, and Security remain routed dependencies selected by facts;
the recovery does not change their policy. The other canonical modules have no
semantic ownership or projection of the six proposed policy families.

## Existing Policy Units

The 29 current units are 13 Commit units, 15 Planning units, and one
Verification unit. The selected neighbors are:

- `workflow.verification.acceptance-claims` for claim identity and evidence
  set compatibility;
- `workflow.planning.replanning`, `workflow.planning.findings`,
  `workflow.planning.projection-completeness`, and
  `workflow.planning.acceptance-claims` for non-overlap with the new systemic
  unit.

The new headings own narrower semantics and do not revise those units. All
other existing units are not selected as consumers or sources of the proposed
meanings. Locator and overlap validation remains a Milestone 1 gate.

## Selected Projections And Templates

| Member | Reason | Planned disposition |
| --- | --- | --- |
| `prompts/planning.md` | projects oracle, dependency, systemic, and Router requirements | `updated` |
| `prompts/implement-plan.md` | projects stop/re-plan and evidence requirements | `updated` |
| `templates/PLAN-TEMPLATE.md` | records only material audit and evidence fields | `updated` |
| `prompts/full-codebase-standards-refactor.md` | delegates systemic standards review to Router and Planning | `reviewed-no-change` |
| `templates/PULL_REQUEST_TEMPLATE.md` | projects selected Verification claims and explicitly rejects template completion as evidence | `reviewed-no-change` |

The last two were missing from the initial read-only set and are added by this
audit. Other registered templates are illustrative or concern unrelated
configuration and do not project the proposed policy.

## Selected Existing Suites

Current suites selected for review are grouped below. Their definitions and
registered inputs are selected with them.

| Consumer class | Existing suite IDs | Planned disposition |
| --- | --- | --- |
| Verification/oracles | `acceptance-claims`, `verification-quality-gates`, `verification-ownership`, `testing-acceptance-paths`, `testing-focused-design`, `testing-gates-diagnosis`, `testing-coverage-documentation` | `reviewed-no-change`; new recovery suite/fixtures are `updated` |
| Contracts/generated semantics | `contract-artifact-selection`, `contract-boundary-proof`, `contract-invariants`, `contract-planning-boundary`, `contract-semantic-preservation`, `testing-persisted-contract-artifacts` | `reviewed-no-change`; new conformance suite/fixtures are `updated` |
| Architecture/immutable authority | `architecture-data-authority-pattern`, `architecture-durable-workflow-pattern`, `architecture-owner-contract`, `persistence-owner-contract` | `reviewed-no-change`; new closure suite/fixtures are `updated` |
| Dependencies | `dependencies-owner-contract`, `dependencies-population`, `dependency-audit-lineage`, `dependency-standards-consolidation`, `coding-dependency-route` | `reviewed-no-change`; new decision suite/fixtures are `updated` |
| Planning/systemic findings | `planning-admission`, `planning-consolidation`, `policy-semantic-impact`, `plan-template-projection`, `full-review-prompt-entrypoint`, `plan-implementation-entrypoint` | `reviewed-no-change`; new systemic suite/fixtures are `updated` |
| Router/profile | `root-index-closure`, `language-index-closure`, `coding-dependency-route`, `router-legacy-route-closure` | `reviewed-no-change`; new Router suite/fixtures are `updated` |
| Supporting read-only owners | `build-owner-contract`, `tooling-owner-contract`, `documentation-traceability-policy`, `implementation-change-evidence`, `licensing-owner-contract` | `reviewed-no-change` |

The remaining registered suites and inputs have owners and decision domains
outside the six policy families. Security and Diagnostics suites remain
conditionally routed evidence, not projections of the new Router rule.

## Missing Current Horizon Members

The independent audit found that the current horizon does not yet contain:

- either retained plan checker;
- `router-projection.toml` or the canonical module corpus manifest as member
  artifacts;
- any A1/A1b package source or package test;
- any historical A1 acceptance/candidate report; or
- the future profile, policy units, declarations, fixtures, and suites.

This is expected current state, not an empty-impact success. Milestone 1 must
make every permanent selected consumer an exact graph node and/or registered
Python-suite input. The new suites must name exact relevant checker, report,
runtime, and test paths so provider v2 fingerprints them. A wildcard package
label or report directory is not sufficient. No retained Bash checker behavior
may be extended.

The exact read-only runtime families are the Standards Engine contract/schema,
generator, canonical validator, generated result algebra, public facade,
snapshot/analysis stores, inspection paths, applicability evaluator,
policy-impact compiler, metadata serializer/corpus, graph composition,
verifier adapter, and their focused accepted A1 tests. Their recovery
disposition is `reviewed-no-change`; runtime correction belongs to A1b. If
Milestone 1 cannot register these exact consumers without changing a read-only
package, that is a re-plan trigger.

## Policy Subject Reconciliation

| Subject | Planned consumer map | State |
| --- | --- | --- |
| `workflow.verification.evidence-oracle-boundary` | prompts, plan/PR templates, Documentation, reports, verifier suites, fixtures, retained checker review | `pre-policy-scope-audit-complete` |
| `workflow.verification.negative-fixture-isolation` | plan fixture/checker boundary, planning fixtures, Python suite | `pre-policy-scope-audit-complete` |
| `workflow.verification.differential-evidence` | contract/equality fixtures, mutation evidence, reports, Python suites | `pre-policy-scope-audit-complete` |
| `topic.contracts.generated-semantic-conformance` | Router/profile, Build/Tooling, public/generated package boundary, tests/suites | `pre-policy-scope-audit-complete` |
| `topic.contracts.schema-dialect-and-vocabulary` | profile, dependency decision, schema/validator/generator, fixtures/suites | `pre-policy-scope-audit-complete` |
| `topic.contracts.identity-versus-instance-equality` | serializer, validator, decoder, applicability values, handles, fixtures/suites | `pre-policy-scope-audit-complete` |
| `topic.architecture.immutable-authority-closure` | snapshot/state stores, inspection, authority views, Persistence, cold tests/suites | `pre-policy-scope-audit-complete` |
| `topic.dependencies.implementation-versus-dependency` | Router, prompts, ADR expectation, dependency fixtures/suites, manifests | `pre-policy-scope-audit-complete` |
| `workflow.planning.systemic-finding-replan` | all three planning entrypoints, implementation prompt, template, issues, fixtures/suites | `pre-policy-scope-audit-complete` |
| `router.generated-contract-profile-applicability` | Router projection, profile, prompts, routing fixtures/suite | `pre-policy-scope-audit-complete` |
| `profile.boundary.generated-contract.applicability` | Router, route fixtures, prompts, profile owner suite | `pre-policy-scope-audit-complete` |
| `profile.boundary.generated-contract.semantic-closure` | required canonical owners, generated/public consumers, profile fixture/suite | `pre-policy-scope-audit-complete` |

No planned disposition is `blocked`. This state is one prerequisite for later
policy admission, but it does not authorize policy-admission review or policy
implementation. Those remain unavailable until M0 recovery is independently
admitted, the generated inventory is refreshed and verified, and the complete
Milestone 0 gate passes.
