# Plan: Standards Engine Policy-Impact Authority V2

**Plan status:** `Active`

**Current phase:** Milestone 1 coverage freeze and certification

**Next slice:** freeze the v2 authority and certify current coverage

**Acceptance status:** `pending`

**Planning base:** commit
`cb6abdb89afaa4fca25706cd42f621a8c762480f`, tree
`24328086a11f9370a615ff62254de9aa1d825931`

**Admission boundary:** candidate commit
`f18bef01cf109d8dc38241a1b88297c98095655d`, tree
`dda284f6e82ea66ad11dbddc2d7584d6dfea1ece`; reviewer report commit
`95e5a389b8328f57eadc11fe650c418049a87fd1`, tree
`83f502a19463616105cc7c272d0bb904ba946ac1`

**Prior implementation base:** admission-transition commit
`fd9efe8198f787c9dd99255bf95e74d84b55baa2`, tree
`9668c0b73c72e849311bddf6a83affcec9f82685`; `Superseded` for
fixture-scope authorization by the replan triggered at commit
`6e3f784353f44cf8566b493442ef2b722a622286`, tree
`79951ad72664962cfebc6b4a2cb11210f23be7ba`

**Fixture-scope admission boundary:** candidate commit
`a38e1c5da05e28cb876d57a4ca868ce9e65a4870`, tree
`d34b95cb81a3279b30792d0c224bbc11a31a1681`; reviewer report commit
`e84e8442ddb4cef766b6e7a64f84d068f466e154`, tree
`130da772e45faddb5a6c737c5cf9afe6073f57dc`

**Renewed implementation base:** fixture-scope admission-transition commit
`ec0d7bc7abaf44e88ee99cb23c65962ba3c25a79`, tree
`4b07fdb87c0e958eb321e114171d1ac68d8820dc`

**Public-consumer admission boundary:** candidate commit
`9dd2dd1c660de9efb75522ff21a44fe844398c4f`, tree
`fcf91257f00b1d9aeb8fdb3e70a2fad06db460ce`; reviewer report commit
`1bb79e125a1362e1b666122efc78ce9a5599fe67`, tree
`2e3bc506c53f68467923b129068a163635d668bf`

**Current implementation base:** public-consumer admission-transition commit
`95cb97babff778497857e9e6be44ddc81e446564`, tree
`1d85875000ddbf75256a4ec85e12fffcf196e04f`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**ADR:**
[Standards Engine Policy-Impact Authority V2](../../decisions/standards-engine-policy-impact-authority-v2.md)

**Relationship migration:**
[relationship-migration.tsv](reports/relationship-migration.tsv)

**Artifact-kind inventory:**
[artifact-kind-inventory.tsv](reports/artifact-kind-inventory.tsv)

**Systemic consumers:**
[systemic-consumer-inventory.md](reports/systemic-consumer-inventory.md)

**Coverage transition provenance:**
[coverage-transition-provenance.tsv](reports/coverage-transition-provenance.tsv)

**State/version inventory:**
[persisted-state-and-version-inventory.md](reports/persisted-state-and-version-inventory.md)

## Objective

Restore one typed authority for policy-impact validity and projection. The
accepted result compiles supplemental artifact identity, relationship kinds,
relation/target compatibility, graph topology, policy semantics, provenance,
and coverage fingerprints in `standards_policy_impact`; gives downstream
Modules one immutable result; and exposes only operation-shaped relationship
inspection through public A1 version 10.

This plan is a recovery-enabling prerequisite. It does not implement the
broader A1b equality, general contract-compiler, immutable authority repository,
or result-algebra redesign, and it does not activate A2.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PIA2-A1 | One internal v2 contract owns every supplemental artifact kind, relationship kind, graph group, propagation rule, evidence rule, and exact allowed target class. | `contract` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) compiler contract evidence |
| PIA2-A2 | Every catalog node has one explicit admitted artifact kind, path changes do not change classification, and every relationship target is compatible by typed identity rather than path inference. | `integration` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) catalog and compatibility evidence |
| PIA2-A3 | The migration inventory's exact old identity set is dispositioned to its exact replacement set; implementation consumers use `implementation-projection`, genuine references remain references, and no permanent mutable-total assertion is introduced. | `contract` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) exact inventory-derived set comparison |
| PIA2-A4 | Graph edges and policy semantic records have equal identity sets, and graph composition uses the policy-impact provider for supplemental nodes, groups, and edges with no separate catalog source. | `integration` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) graph composition evidence |
| PIA2-A5 | Verifier and coverage consume the compiled authority; no catalog TOML parsing or relation/path compatibility switch remains outside `standards_policy_impact`. | `integration` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) dependency and behavior evidence |
| PIA2-A6 | A1 v10 public closure is reachable from the four operations, excludes `PolicyImpactDeclaration` and `CompiledPolicyImpactSemantics`, and returns typed operation-shaped relationship semantics. | `contract` | `not-applicable` | `automated` | `satisfied` | [M0 candidate](reports/authority-cutover-candidate.md) generated and operation-closure evidence |
| PIA2-A7 | Old v9 handles and states are explicitly unsupported; v10 query, prepare, resolve, inspect, persistence, and genuine cold-process reconstruction use the accepted version identities with no compatibility fallback. | `system` | `not-applicable` | `automated` | `pending` | Pending migration and cold-process evidence |
| PIA2-A8 | One post-freeze certification pass derives current subjects and requirements mechanically and proves exact active-policy-unit/requirement/attestation/certificate equality, with no stale, duplicate, extra, missing, or blocked subject. Predecessor presence remains generated migration provenance and cannot change certification behavior or identity. | `integration` | `not-applicable` | `automated` | `pending` | Pending coverage-freeze evidence |
| PIA2-A9 | One clean candidate passes focused package tests, generated freshness, registered declarative suites, the complete Python checkpoint, retained migration checks, and diff validation. | `integration` | `not-applicable` | `automated` | `pending` | Pending exact-tree candidate report |
| PIA2-A10 | An independent reviewer accepts the exact candidate against repository Standards and this specification with no unresolved consumer. | `integration` | `not-applicable` | `manual` | `pending` | Pending independent acceptance report |

## Scope

### In Scope

- One internal serialized policy-impact authoring contract and compiler-owned
  target compatibility.
- Explicit supplemental artifact kinds and a single compiled graph/semantic/
  coverage authority.
- Reclassification of every inventoried implementation relationship and
  preservation of genuine reference relationships.
- Removal of separate catalog graph loading, verifier path inference, and
  coverage raw-catalog parsing.
- Public A1 v10 operation closure, relationship inspection, version migration,
  generated outputs, examples, rendering, and public adapters.
- Explicit unsupported outcomes for v9 handles and persisted state.
- Post-freeze coverage horizon versioning, one exact current-coverage
  certification pass, generated predecessor-transition provenance, and
  exact-tree prerequisite acceptance.
- Required updates to the blocked standards-recovery plan and evidence.

### Out Of Scope

- JSON Schema instance-equality correction or validator/dependency selection.
- A general contract-compilation Module beyond the existing A1 generator.
- A new immutable content or analysis-state repository.
- Unrelated public result-algebra redesign.
- Normative standards prose, policy-unit identity, locator, or semantic-revision
  changes.
- New applicability operators, graph traversal semantics, evidence providers,
  authorization rules, or generic graph-engine behavior.
- A compatibility loader, dual v9/v10 runtime, edge alias, or state relabeling.
- A2 controlled authoring and Plan C external baselines.
- New or extended Bash verification.

## Constraints And Assumptions

### Constraints

- Historical A1 v9 acceptance remains unchanged. This is a prospective
  coordinated replacement, not a rewrite of accepted evidence.
- No implementation starts while this plan is `Blocked`. The independent
  admission report and its authorized mechanical lifecycle transition are
  governance operations outside the milestones.
- Runtime, catalog, declaration, public contract, and generated projections
  switch atomically. The predecessor and replacement loaders may coexist only
  inside equivalence or rejection tests, never as accepted runtime authority.
- All eight registered relationship declaration sources migrate from source
  schema version 1 to version 2 in that replacement. Five change only their
  schema version; three also apply the admitted relation reclassification. No
  version 1 declaration is accepted after cutover.
- Coverage attestations are authored only after contract, catalog,
  declarations, suites, provider, and horizon inputs are frozen.
- Renewal and initial establishment are not coverage semantic categories.
  Certification uses one evidence, authorization, identity, validation, and
  certificate path for every current requirement. Predecessor presence is
  generated audit provenance and is never a certification input.
- The migration inventory is finite historical evidence. Runtime and tests
  assert identities, semantic properties, and set equality rather than mutable
  catalog totals.
- No source path, suffix, directory, exception fallback, or literal allowlist
  may determine artifact or relationship compatibility.
- The suite registry and canonical metadata corpus remain upstream authorities;
  this plan does not copy their membership into a second manifest.
- A2 remains inactive until this prerequisite, standards recovery, and later
  A1b implementation each receive their own independent acceptance.

### Assumptions

- The seven artifact kinds in the proposed ADR classify every current
  supplemental node without ambiguity. A target needing another independently
  meaningful kind is a re-plan trigger.
- Existing `GraphContribution` can carry the compiled catalog nodes, groups,
  and edges without graph-engine changes.
- No retained production state requires conversion. Discovery of supported
  persisted state outside tests triggers a migration re-plan before version
  cutover.
- Operation-shaped inspection can preserve all caller-required meaning without
  exposing repository authoring or compiler internals. A public caller needing
  those internal shapes triggers interface review.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| `standards_policy_impact` compiles all policy-impact nodes, groups, edges, semantics, compatibility, provenance, and coverage fingerprints from one internal v2 contract and eight source-schema-v2 declaration inputs. | Proposed ADR | Systemic audit and independent options review | Split compiler/catalog/verifier/coverage authority and source-schema-v1 declarations |
| Supplemental nodes author one explicit artifact kind; canonical modules retain metadata-owned roles; reading/evidence authority remains separate. | Proposed ADR | [Artifact-kind inventory](reports/artifact-kind-inventory.tsv) | Path-derived or authority-derived target classification |
| `implementation-projection` identifies implementation consumers; `reference-projection` remains limited to canonical reference modules. | Proposed ADR | [Relationship migration](reports/relationship-migration.tsv) | Broad reference semantics |
| The compiler emits one graph contribution containing catalog nodes/groups and relationship edges. | Proposed ADR | Current duplicate `ManifestSource` composition | Separate catalog graph provider |
| Public v10 contains only operation-reachable definitions and an operation-shaped policy relationship inspection. | Proposed ADR | Four-operation public Interface audit | Public repository declarations and compiler semantics |
| Version 9 values are unsupported under v10; no compatibility runtime or state converter is introduced. | Proposed ADR | [State/version inventory](reports/persisted-state-and-version-inventory.md) | Implicit interpretation or relabeling of old state |
| Canonical metadata owns current coverage-subject membership, coverage compilation owns current requirements, and exact predecessor certificate presence is a generated non-authoritative transition projection. | Proposed ADR | [Coverage transition provenance](reports/coverage-transition-provenance.tsv) | Authored subject/lifecycle inventory and renewal-versus-initial behavior |
| Source-owned declarations define the relationship set; the compiler validates each supplied relationship; the independent horizon and authorized coverage audit decide missing-consumer completeness. Suite ownership does not infer policy-impact consumers. | Proposed ADR and canonical Planning | Fixture-scope systemic review | Owner-wide enforcement-suite inference in the verifier and its missing-edge fixture |
| Broader A1b work remains separately planned after standards recovery. | Standards-recovery sequence | A1b authoring brief | Pulling independent equality/storage/result redesign into this prerequisite |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Internal authoring contract freshness | Freshness | Compiler loads exact v2 contract and registered inputs | Contract fixture mutations | Does not prove semantic compatibility | Stale or unsupported version diagnostic |
| Relation/target validity | Semantics | Compiler's typed compatibility table | Exact artifact and relation fixture matrix | Paths and verifier agreement are non-proof | Typed incompatible-target diagnostic |
| Migration completeness | Identity | Mechanical old/new identity-set comparison against the admitted inventory | Independent candidate review | Mutable edge totals are non-proof | Missing, extra, or incorrectly retained identity |
| Public closure | Public contract | Generator reachability from four operation roots plus canonical validation | Public facade tests | Generated freshness alone is non-proof | Removed internal definition reachable from a public operation |
| Version migration | Persisted/public contract | Public old-version rejection and v10 reconstruction | Fresh-process test with persisted immutable inputs | In-process cache replay is non-proof | Typed unsupported result for v9 |
| Coverage closure | Audit | Derived active-unit/requirement/attestation/certificate subject equality | Authorized post-freeze attestations and independent horizon | Predecessor presence and empty graph results are non-proof | Stale, duplicate, extra, missing, or blocked subject diagnostic |
| Coverage transition provenance | Migration provenance | Exact predecessor snapshot compilation joined to the current canonical active-unit set | Bound predecessor requirement, attestation, and certificate identities | Does not define certification behavior or identity | Missing current subject or incorrect predecessor-presence projection |

The transition projection is deterministic migration evidence, not an authored
coverage inventory. Its inputs are the exact predecessor commit/tree named in
the ADR and the candidate's canonical active policy-unit corpus. Generation
compiles predecessor coverage through the accepted public package Interfaces,
left-joins certificates by canonical policy-unit ID, emits absent predecessor
identities as `-`, and sorts rows by policy-unit ID. Every row repeats the
predecessor commit/tree so the artifact cannot be interpreted against mixed or
ambient historical authority.

## Systemic Finding Audit

- Invariant family: a policy-impact relation is valid only when its source,
  relationship kind, target role, applicability, evidence owner, and graph
  projection all resolve under one contract.
- Canonical owner: `standards_policy_impact`.
- Sibling representations: internal kind table, catalog manifest, graph source
  registration, declaration files, public schema enums, generated Python/tools,
  verifier dispatch, coverage horizon projection, engine inspection, tests,
  attestations, and persisted analysis versions.
- Consumer dispositions: compiler `replace`; graph composition `replace`;
  verifier `consume`; coverage `consume`; Standards Engine `adapt`; declarations
  `migrate`; catalog `type`; generated projections `regenerate`; attestations
  `certify-current`; predecessor state `project-as-provenance`; historical A1
  evidence `retain`.
- Scope replacement: the Router-only repair and its one-file admission are
  superseded. No local repair resumes until this class-level plan is accepted.

## Simplicity And Ownership Review

- Independent concepts: canonical metadata identity, policy-impact authoring,
  generic graph traversal, applicability execution, public agent contract,
  analysis decisions, and coverage attestation.
- Intentional coupling: catalog types, relationship kinds, compatibility,
  compiled graph facts, semantics, and coverage fingerprints change together
  because they are projections of one authority.
- Accidental coupling removed: repository path taxonomy, public/internal enum
  duplication, raw catalog reparsing, separate graph source registration, and
  verifier-owned semantic validation.
- Module depth: callers receive one immutable compiled set; parsing,
  validation, compatibility, projection, identity, and diagnostics remain
  behind that Interface.
- Future independent work: JSON Schema equality, mature validator selection,
  general contract compilation, immutable authority storage, A2 authoring.

## Pre-Milestone Admission

1. Commit this blocked governance candidate with the proposed ADR, exact
   inventories, and the standards-recovery supersession records. It contains no
   implementation or authority-data migration.
2. An independent reviewer authors only
   `reports/policy-impact-authority-v2-admission.md`, binding the exact candidate
   commit/tree and reviewing Standards, specification, write sets, migration,
   versioning, and exclusions.
3. If accepted, one mechanical transition commit whose direct parent contains
   that report may change only this `plan.md`, this `execution-ledger.md`, this
   `issues.md`,
   `docs/decisions/standards-engine-policy-impact-authority-v2.md`, and
   `docs/decisions/standards-engine-navigation-analysis.md`. It may only record
   candidate/report identities, mark PIA2-005 resolved, accept the proposed
   ADR, add the predecessor ADR's scoped supersession notice, and move this plan
   and Milestone 0 from `Blocked` to `Planned`.
4. `start` is valid only while that transition is current `HEAD`. It records
   the exact transition commit/tree and moves the plan and Milestone 0 to
   `Active` before any implementation file changes.
5. Any semantic plan or ADR change after review requires a new candidate and
   admission. The report itself does not authorize implementation.

## Milestone 0 Fixture-Scope Recovery Admission

1. Preserve the interrupted implementation outside the governance candidate.
   Commit only this plan, its ledger, and its issue record from clean replan
   base commit `6e3f784353f44cf8566b493442ef2b722a622286`, tree
   `79951ad72664962cfebc6b4a2cb11210f23be7ba`.
2. An independent reviewer authors only
   `reports/policy-impact-fixture-replan-admission.md`, binding the exact
   governance candidate commit/tree and reviewing the corrected fixture
   closure, supersession, exclusions, and preserved architecture.
3. If accepted, one mechanical transition commit whose direct parent contains
   that report may change only this `plan.md`, this `execution-ledger.md`,
   and this `issues.md`. It records the candidate/report identities and moves
   this plan and Milestone 0 from `Blocked` to `Planned`. PIA2-007 remains
   active until implementation produces its exact fixture and inference-removal
   evidence.
4. `start` is valid only while that transition is current `HEAD`. It records
   the exact transition commit/tree, establishes the renewed implementation
   base, and moves this plan and Milestone 0 to `Active` before the preserved
   implementation is restored.
5. The admission authorizes only the six nested declaration-fixture paths
   added below, deletion of the obsolete fixture pair, and removal of current
   owner-wide suite-inference claims and tests. It does not reopen the accepted
   ADR, production relationship inventory, public-v10 scope, coverage design,
   A1b, or A2.

## Milestone 0 Public-Contract Consumer Recovery Admission

1. Preserve the interrupted implementation outside the governance candidate.
   Commit only this plan, its ledger, and its issue record from clean replan
   base commit `67773d0f3341359d4fb8f0d3996ceceaafebb808`, tree
   `4b7ae0c5397279e1952b887277a077fa8e44035a`.
2. An independent reviewer authors only
   `reports/policy-impact-public-consumer-replan-admission.md`, binding the exact
   governance candidate commit/tree and reviewing the one-file write-set
   correction, public operation closure, exclusions, and preserved architecture.
3. If accepted, one mechanical transition commit whose direct parent contains
   that report may change only this `plan.md`, this `execution-ledger.md`, and
   this `issues.md`. It records the candidate/report identities and moves this
   plan and Milestone 0 from `Blocked` to `Planned`. PIA2-008 remains active
   until implementation produces its exact conformance evidence.
4. `start` is valid only while that transition is current `HEAD`. It records
   the exact transition commit/tree, establishes the renewed implementation
   base, and moves this plan and Milestone 0 to `Active` before the preserved
   implementation is restored.
5. The admission authorizes only
   `tools/standards_engine/tests/test_applicability_contract.py`. The test must
   compare runtime applicability language authority with the operation-reachable
   `CoverageAuthorityView.applicability_language_version`; it must not retain or
   recreate a public compiled-program type. The ADR, public-v10 shapes, A1b,
   and A2 remain unchanged.

## Milestones

### Milestone 0: Coordinated Authority And Public Contract Cutover

**Goal:** Replace every split policy-impact validity/projection path and switch
the public facade atomically to v10, leaving coverage completion as the only
expected intermediate blocker.

**Allowed write set:**

- `tools/standards_policy_impact/contracts/policy-impact-authoring-v2.toml` (new)
- `tools/standards_policy_impact/README.md`
- `tools/standards_policy_impact/standards_policy_impact/__init__.py`
- `tools/standards_policy_impact/standards_policy_impact/compiler.py`
- `tools/standards_policy_impact/standards_policy_impact/model.py`
- `tools/standards_policy_impact/tests/test_compiler.py`
- `tools/standards_graph/README.md`
- `tools/standards_graph/standards_graph/__init__.py`
- `tools/standards_graph/standards_graph/repository.py`
- `tools/standards_graph/tests/test_metadata_graph.py`
- `tools/standards_analysis/standards_analysis/coverage.py`
- `tools/standards_analysis/standards_analysis/resolution.py`
- `tools/standards_analysis/standards_analysis/snapshots.py`
- `tools/standards_analysis/tests/test_coverage.py`
- `tools/standards_analysis/tests/test_impact.py`
- `tools/standards_analysis/tests/test_results.py`
- `tools/standards_analysis/tests/test_snapshots.py`
- `tools/standards_verifier/README.md`
- `tools/standards_verifier/standards_verifier/policy_impact.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- `tools/standards_engine/contracts/generate_contract.py`
- `tools/standards_engine/contracts/generated/agent-tools.json`
- `tools/standards_engine/contracts/identity-fixtures.json`
- `tools/standards_engine/contracts/validate_contracts.py`
- `tools/standards_engine/contracts/README.md`
- `tools/standards_engine/standards_engine/__init__.py`
- `tools/standards_engine/standards_engine/_generated_contract.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/standards_engine/rendering.py`
- `tools/standards_engine/standards_engine/tools.py`
- `tools/standards_engine/tests/test_analysis.py`
- `tools/standards_engine/tests/test_applicability_contract.py`
- `tools/standards_engine/tests/test_generated_contract.py`
- `tools/standards_engine/tests/test_navigation.py`
- `tools/standards_engine/tests/test_rendering.py`
- `evaluation/standards-effectiveness/policy-impact-registry.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/edge-source-registry.toml`
- `evaluation/standards-effectiveness/policy-coverage/horizons.toml`
- `evaluation/standards-effectiveness/policy-impact/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-impact/router.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.commit.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-impact/workflow.verification.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/duplicate-edge.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/duplicate-edge.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/malformed-relation.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/malformed-relation.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/missing-applicability.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/missing-applicability.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/missing-enforcement-suite-edge.toml` (delete)
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/missing-enforcement-suite-edge.toml` (delete)
- `evaluation/standards-effectiveness/fixtures/policy-impact/missing-file.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/path-escape.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/unknown-consumer.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/unknown-consumer.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/unknown-owner.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/declarations/unknown-owner.toml`
- `evaluation/standards-effectiveness/suites/policy-semantic-impact.toml`
- `docs/plans/standards-engine-policy-impact-authority-v2/plan.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/execution-ledger.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/issues.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/reports/authority-cutover-candidate.md` (new)

**Tasks:**

- [x] Add the v2 internal contract and compile the typed catalog, groups,
  relationships, semantics, provenance, and coverage projection once.
- [x] Migrate all eight registered relationship declaration sources to source
  schema version 2 in the same cutover. Apply relation changes only to the three
  files named by the migration inventory; reject every version 1 source after
  cutover and provide no compatibility loader.
- [x] Require explicit artifact kinds and typed relation/target compatibility;
  add complete positive and negative contract matrices.
- [x] Migrate the seven retained declarative verifier cases through the
  production registry/declaration Interface. Delete the obsolete owner-wide
  suite-inference fixture pair and remove current documentation or tests that
  infer policy-impact consumers from suite ownership.
- [x] Reclassify the admitted migration identities and prove exact old/new set
  equality without a global relationship count.
- [x] Remove the separate catalog graph source, verifier path dispatch, and
  coverage raw-catalog parser; update consumers to use the compiled authority.
- [x] Cut public schema, generated Python/tools, examples, engine adapters,
  inspection, rendering, and versions to v10 in one replacement.
- [x] Prove v9 unsupported outcomes through all four operations and persisted
  state. The existing genuine v10 cold-process reconstruction remains pending
  execution until Milestone 1 supplies current coverage.
- [x] Run focused package and contract checks. Record all expected stale
  coverage subjects; any non-coverage failure blocks completion.

**Acceptance gate:** All focused tests and public contract checks pass; exact
migration and graph/semantic set comparisons pass; repository search finds no
parallel catalog parser or path classifier; the only permitted complete
checkpoint blocker is post-cutover stale or missing coverage.

**Status:** `Implemented`

### Milestone 1: Coverage Freeze And Prerequisite Acceptance

**Goal:** Freeze the v2 authority, certify the exact mechanically derived
current coverage set through one path, prove the full repository boundary, and
independently accept the prerequisite.

**Allowed write set:**

- `evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/router.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.contracts.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.architecture.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml` (new)
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml` (new)
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_engine/tests/test_navigation.py`
- `tools/standards_engine/tests/test_analysis.py`
- `docs/plans/standards-engine-policy-impact-authority-v2/plan.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/execution-ledger.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/issues.md`
- `docs/plans/standards-engine-policy-impact-authority-v2/reports/certify-current-coverage.md` (new)
- `docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-candidate.md` (new)
- `docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md` (new, independent reviewer owned)
- `docs/plans/standards-engine-standards-recovery/plan.md`
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`
- `docs/plans/standards-engine-standards-recovery/issues.md`
- `docs/plans/standards-engine-standards-recovery/reports/semantic-impact-inventory.md`
- `docs/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md`

**Tasks:**

- [ ] Freeze contract, catalog, declarations, suites, provider, and horizon
  before authoring any attestation.
- [ ] Derive current subjects from the frozen canonical metadata corpus and
  current requirements from coverage compilation; obtain one authorized
  complete attestation for every current requirement through the same
  certification Interface.
- [ ] Generate certificates and prove exact active-policy-unit, requirement,
  attestation, and certificate subject equality.
- [ ] Reproduce the admitted transition-provenance projection from predecessor
  commit `4baa63118a72fd0c185fc1d950dc149ab0c1808c`, tree
  `5a4d6d6786fa7a6ca8b373ca221a8eb1c90fa995`, and the frozen current
  canonical corpus. Require byte-identical output; any current-subject change is
  a re-plan trigger. Do not consume this projection during certification.
- [ ] Finish the already admitted mutable-total test replacements using semantic
  identity and cause-set assertions after coverage is valid.
- [ ] Run all focused suites, generated checks, registered declarative suites,
  complete Python checkpoint, retained migration checks, and diff validation.
- [ ] Commit one clean candidate and obtain independent Standards/specification
  acceptance bound to its exact commit and tree.
- [ ] On acceptance, mark this plan accepted and return standards recovery to a
  separately admitted final-acceptance slice. Do not activate A1b or A2.

**Acceptance gate:** PIA2-A1 through PIA2-A10 are satisfied; the active policy
unit, requirement, attestation, and certificate subject sets are equal with one
record per subject; transition provenance reproduces exactly but does not
influence certification; no consumer is blocked; and an independent report
accepts one exact clean candidate.

**Status:** `Active`

## Blockers

- The standards-recovery plan remains blocked and provides no implementation
  fallback while this prerequisite is unresolved.

## Re-Plan Triggers

- A supplemental node cannot be represented by the admitted artifact-kind
  contract without conflating independently changing meanings.
- A relationship needs different propagation, traversal, evidence, scope, or
  compatibility semantics than the v2 contract represents.
- `GraphContribution` cannot carry the complete compiled node/group/edge view
  without generic graph-engine behavior changes.
- A public operation genuinely requires repository authoring or compiler
  internals removed from v10.
- Supported persisted production state exists or a retained consumer requires
  migration rather than explicit unsupported handling.
- A version change in the inventory is either insufficient to prevent old
  interpretation or broader than the changed semantic contract.
- Any affected source or consumer falls outside the exact milestone write set.
- Coverage inputs change after attestation work begins.
- Verification reveals another raw catalog parser, path classifier, public
  internal type, or compatibility authority outside the systemic inventory.
- A broader A1b, A2, security, dependency, or licensing decision becomes
  necessary.
- An independent reviewer rejects the plan, ADR, candidate, migration, or
  acceptance evidence.

## Concurrent Work

No concurrent implementation is admitted. The internal contract, catalog,
declarations, public schema, generated outputs, active plans, and coverage
attestations are shared serial authority. Independent reviewers inspect an
immutable candidate and author only the report named by the applicable
admission or acceptance protocol.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: broader A1b work remains blocked by standards recovery;
  A2 remains blocked by independently accepted A1b.
- Final status: `Active`
