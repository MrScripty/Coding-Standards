# Plan: Standards Engine A1b Contract And Authority Foundations

**Plan status:** `Blocked`

**Current phase:** Planning admission

**Next slice:** Independent exact-tree review of this plan, its proposed ADR,
and its two planning reports

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Replace A1's duplicated contract semantics and fragmented immutable-authority
storage with one dependency-backed contract compiler, three explicit equality
domains, one narrow immutable authority repository, and one generated public
request/result algebra. Preserve the four-operation read-only Standards Engine
and immutable analysis kernel while making every issued handle reproducible in
a cold process. Complete the coordinated replacement and independent exact-tree
acceptance before any A2 review or implementation begins.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1B-A1 | The exact selected Draft 2020-12 implementation passes every applicable case from the pinned official external suite through the production contract adapter. | `contract` | `required-real` | `automated` | `pending` | Pending Milestone 1 and final acceptance |
| A1B-A2 | Every public operation request and result has one complete reachable schema closure, generated models preserve it, stale projections fail, and unsupported reachable semantics reject. | `contract` | `not-applicable` | `automated` | `pending` | Pending Milestone 1 and Milestone 3 |
| A1B-A3 | Draft instance equality, applicability value equality, and NFC identity canonicalization pass independent domain-specific fixtures without one domain deciding another. | `focused` | `not-applicable` | `automated` | `pending` | Pending Milestone 1 |
| A1B-A4 | Snapshot, analysis, and navigation roots reconstruct every advertised operation and handle in a genuinely fresh process after source and provider mutation. | `system` | `representative` | `automated` | `pending` | Pending Milestone 2 and Milestone 3 |
| A1B-A5 | Public `query`, `prepare`, `resolve`, and `inspect` accept and return only generated v11 contract values; internal domain models and dependency exceptions cannot cross the facade. | `integration` | `not-applicable` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A6 | The selected dependency closure is exact, hash-checked, provenance- and license-reviewed, supported on the admitted Python environments, and free of unresolved blocking security findings. | `release-artifact` | `representative` | `automated` | `pending` | Pending Milestone 0 and final review |
| A1B-A7 | No old validator, generated keyword interpreter, metadata-owned identity implementation, snapshot compiler, analysis-state store, compatibility reader/writer, or old-version fallback remains reachable. | `integration` | `not-applicable` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A8 | Existing routing, policy-impact, analysis, coverage, reading, rendering, and inspection behavior remains valid except for the declared version and external-conformance corrections. | `integration` | `not-applicable` | `automated` | `pending` | Pending broad checkpoint |
| A1B-A9 | All focused package tests, registered declarative suites, retained migration checkers, generated freshness, plan checks, and diff hygiene pass without mutable catalog-count assertions. | `integration` | `not-applicable` | `automated` | `pending` | Pending final checkpoint |
| A1B-A10 | An independent reviewer accepts one clean implementation commit and tree and confirms every claim, migration deletion, consumer disposition, and exclusion. | `contract` | `not-applicable` | `manual` | `pending` | Pending final acceptance report |

## Scope

### In Scope

- A stdlib-only `standards_identity` Module owning the existing identity format.
- A `standards_contracts` Module owning the admitted schema profile, Draft
  execution, reachable closure, diagnostics, model construction, and build-time
  projections.
- Adoption and exact resolution of `jsonschema` 4.26.0 and the directly used
  `referencing` Interface.
- A `standards_authority` Module owning typed immutable snapshot, analysis, and
  navigation roots with in-memory and directory adapters.
- Contract version 11 and handle version 4 coordinated replacement.
- Owner-qualified child handles and complete cold-process inspection.
- Migration of every repository-controlled public consumer and deletion of all
  superseded implementations.
- Registered Python verification, official external conformance, dependency
  and licensing evidence, coverage reconciliation, and exact-tree acceptance.

### Out Of Scope

- A2 authoring, mutation, proposal heads, canonical application, or recovery.
- A compatibility layer, old-state converter, dual reader/writer, or version-10
  fallback.
- Changes to policy meaning, policy-unit declarations, policy-impact
  relationships, relationship kinds, generic graph semantics, or routing
  policy.
- A general content-addressed DAG, garbage collection, remote storage, mutable
  indexes, arbitrary object types, or streaming snapshots.
- Runtime remote schema retrieval, custom vocabularies, format assertion, or
  validator keyword overrides.
- Copied third-party source, wheels, or official test corpus.
- New or extended Bash verification.
- Plan C external-project baselines.

## Constraints And Assumptions

### Constraints

- This plan is unavailable while `Blocked`. Planning admission must complete
  before `start` or any implementation edit.
- The accepted standards-recovery boundary is the comparison base, not the
  eventual implementation base.
- Public version replacement is atomic. Old and new implementations may coexist
  only inside pre-cutover equivalence tests on an unaccepted implementation
  branch; they are never parallel runtime authorities.
- Every dependency is resolved through the accepted lock. No test, build, or
  runtime path installs or selects an ambient alternate dependency.
- Generated freshness and semantic correctness are separate gates.
- Coverage attestations are renewed only after schema, suites, registrations,
  and all other horizon-affecting inputs are frozen.
- Mutable repository totals are not acceptance oracles. Tests assert stable
  identities, closure invariants, and selected semantics.

### Assumptions

- [Consumer and state inventory](reports/consumer-and-state-inventory.md) found
  no external consumer and no retained A1 persisted state. Discovery of either
  invalidates the coordinated no-compatibility cutover.
- The bounded repository snapshot remains small enough for atomic bundle
  storage. The inventory-base tracked tree is under 10 MB; the authority tests
  must measure the actual admitted capture before relying on this assumption.
- The selected dependency closure supports Python 3.11 and 3.12 on the admitted
  Linux verification environments. Milestone 0 owns proof.
- Existing applicability NFC semantics and identity format version 1 are
  intentional and remain unchanged.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Preserve A1's four-operation read-only facade and immutable analysis kernel. | Accepted A1 architecture | [A1 ADR](../../decisions/standards-engine-navigation-analysis.md) | None |
| Add one deep contract compiler over `jsonschema.Draft202012Validator`; generated models are representations, not validators. | Contracts and Dependencies | [Proposed A1b ADR](../../decisions/standards-engine-a1b.md), [dependency decision](reports/dependency-and-dialect-decision.md) | Local validator plus generated second interpreter |
| Keep JSON Schema equality, applicability equality, and identity canonicalization separate. | Contracts, Applicability, Identity | [Proposed A1b ADR](../../decisions/standards-engine-a1b.md) | Identity bytes as schema equality |
| Move unchanged NFC identity format version 1 into `standards_identity`; expose no generic equality helper. | Identity | Existing identity fixtures and design review | Metadata-owned cross-package serialization |
| Store three typed immutable roots through one `standards_authority` Interface; use bounded snapshot bundles initially. | Architecture and Persistence | [Consumer and state inventory](reports/consumer-and-state-inventory.md), [Proposed A1b ADR](../../decisions/standards-engine-a1b.md) | Split snapshot/state/cache ownership |
| Use one coordinated v11/handle-v4 cutover with typed unsupported old versions and no conversion. | Contracts and Planning | Consumer/state inventory | Incremental compatibility migration |
| Run the exact official external conformance corpus from temporary storage; do not copy it into the repository. | Verification and Licensing | [Dependency decision](reports/dependency-and-dialect-decision.md) | Local implementations as each other's only oracle |
| Keep A2 inactive through independent A1b acceptance. | Planning | Accepted standards recovery | Direct progression to authoring |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Generated files are current | Freshness | Deterministic projection `--check` | Canonical contract source and compiler | None within admitted profile | Stale generated output diagnostic |
| Generated closure is complete | Shape and reachability | Reachability compiler plus public-operation fixtures | Canonical public-operation declarations | Unreachable public definitions and unsupported reachable keywords | Contract-compilation failure naming definition and keyword |
| Draft semantics are correct | External conformance | Production adapter over applicable official-suite cases | Exact official JSON Schema Test Suite revision | Excluded vocabularies and formats recorded explicitly | Official negative case rejects at expected keyword/path |
| Equality domains are separated | Semantics and identity | Domain-specific differential and identity fixtures | Draft rules, Applicability contract, and identity contract respectively | Cross-domain coercion | Composed/decomposed Unicode differs for schema but preserves existing identity fixture |
| Cold reconstruction is complete | Persistence/system | Fresh process given only authority-store path and handle | Persisted root and exact bytes | Unavailable external authority | Missing closure returns unavailable; identity contradiction returns invalid |
| Public algebra is exhaustive | Public integration | Real facade and tool operations using exported generated types | Canonical public operation closure | Internal-only domain types | Unhandled internal result remains programming error |
| Dependency is reproducible | Dependency/release | Hash-checked isolated install and import/conformance smoke | Lock, package index artifacts, provenance and licenses | Unsupported target artifact | Missing or mismatched artifact blocks installation |
| Negative fixtures reach their target | Diagnostic isolation | Otherwise-valid fixtures plus exact code/path assertion | Owning contract and typed diagnostic | Unrelated precondition failure | Harness rejects a failure at the wrong diagnostic |

## Systemic Finding Audit

- **Invariant family:** external contract semantics, public projection closure,
  identity serialization, and immutable handle authority.
- **Sibling producers and consumers:** canonical schema, local validator,
  generator, generated models, tool definitions, facade adapters, metadata and
  analysis serializers, snapshot providers, state stores, navigation caches,
  inspection paths, package tests, registered suites, and verifier adapters.
- **Authority and projection inventory:**
  [consumer-and-state-inventory.md](reports/consumer-and-state-inventory.md).
- **Consumer dispositions:** every repository-controlled consumer is `updated`
  or `reviewed-no-change`; no blocked or omitted consumer is allowed at final
  acceptance.
- **Scope or sequencing replacement:** one coordinated public cutover follows
  independently testable foundation Modules; local example repairs are
  prohibited.

## Simplicity And Ownership Review

- **Independent concepts:** standardized schema semantics, A1 identity,
  applicability values, immutable storage, domain analysis, and public facade.
- **Intentional coupling:** the contract compiler uses identity only for
  contract/program identity; the authority repository uses compiled root
  contracts; the facade composes both with domain modules.
- **Accidental coupling risk:** generated validation logic, metadata-owned
  serialization, store enumeration, live repository reads, dependency exception
  leakage, and duplicated public/internal models.
- **Policy/state/lifecycle owners:** canonical schema declares wire shape;
  `standards_contracts` executes it; `standards_identity` owns identity bytes;
  `standards_authority` owns persistence; domain modules own meaning and state
  transitions; A2 alone will own mutable authoring lifecycles.
- **Future independence:** a dependency update should not change domain rules;
  storage layout should not change handles; identity changes require an explicit
  identity version; A2 should compose immutable A1b results without adding
  mutable behavior below this seam.

## Planning And Admission Boundary

The planning comparison base is commit
`c4408363752b10060f631247f3e2f1fa26eae003`, tree
`84477150bd368a168dd04da3770de55c23bbb817`.

Admission uses four distinct identities:

1. this planning candidate commit and tree;
2. a reviewer-owned `reports/a1b-plan-admission.md` commit whose sole change is
   the admission report binding that candidate;
3. a mechanical transition commit whose only changes are lifecycle fields in
   `plan.md`, `issues.md`, and `execution-ledger.md`; and
4. that transition commit as the exact implementation base accepted by
   `start`.

The reviewer report does not self-authorize and is not part of the tree it
reviews. The transition may set this plan to `Planned`, clear the admission
blocker, and identify Milestone 0 as the next slice only when review reports no
blocking Standards or Specification finding. No implementation file may change
in the report or transition commits.

## Milestones

### Milestone 0: Dependency And Identity Foundations

**Goal:** Establish reproducible dependency, licensing, and identity foundations
without changing accepted A1 runtime behavior.

**Allowed write set:**

- `tools/standards_identity`
- `tools/standards_contracts/pyproject.toml`
- `tools/standards_contracts/requirements.lock`
- `tools/standards_contracts/README.md`
- `tools/standards_contracts/tests/test_dependency_resolution.py`
- `docs/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md`
- `docs/plans/standards-engine-a1b/plan.md`
- `docs/plans/standards-engine-a1b/issues.md`
- `docs/plans/standards-engine-a1b/execution-ledger.md`

**Tasks:**

- [ ] Resolve and hash-lock the exact dependency closure for admitted Python
  environments.
- [ ] Record provenance, license authority, supported-target, and security
  dispositions.
- [ ] Implement `standards_identity` with existing identity format version 1 and
  differential byte fixtures copied from authority, not regenerated
  expectations.
- [ ] Prove no existing A1 runtime import changes in this milestone.

**Acceptance gate:** A1B-A3 identity half and A1B-A6 pass; package tests and
broad baseline remain green.

**Status:** `Planned`

### Milestone 1: Contract Compiler And Projection

**Goal:** Implement one deep contract compiler and build-time projection path,
including external conformance, without switching the public facade yet.

**Allowed write set:**

- `tools/standards_contracts`
- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- `tools/standards_engine/contracts/identity-fixtures.json`
- `tools/standards_engine/contracts/generated/agent-tools.json`
- `tools/standards_engine/standards_engine/_generated_contract.py`
- `tools/standards_engine/tests/test_generated_contract.py`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/a1b-contract-conformance.toml`
- `evaluation/standards-effectiveness/fixtures/contracts/a1b`
- `docs/plans/standards-engine-a1b/reports/a1b-contract-profile-audit.md`
- `docs/plans/standards-engine-a1b/plan.md`
- `docs/plans/standards-engine-a1b/issues.md`
- `docs/plans/standards-engine-a1b/execution-ledger.md`

**Tasks:**

- [ ] Compile the exact supported keyword, annotation, reference, and reachable
  public-operation profile.
- [ ] Adapt Draft validator errors to stable typed diagnostics.
- [ ] Generate immutable public models and per-operation tool closures without
  embedded keyword execution.
- [ ] Reproduce the accepted A1 Unicode defect, then prove corrected Draft
  behavior separately from preserved A1 identity behavior.
- [ ] Run applicable official external-suite cases through the production
  adapter and keep the corpus outside the repository.
- [ ] Reject unsupported reachable semantics and unreachable public
  definitions.

**Acceptance gate:** A1B-A1, A1B-A2 compiler half, and A1B-A3 pass; freshness
and semantic gates are reported separately.

**Status:** `Planned`

### Milestone 2: Immutable Authority Repository

**Goal:** Implement three typed immutable roots and prove atomic capture and
cold reconstruction independently of the accepted facade.

**Allowed write set:**

- `tools/standards_authority`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/a1b-authority-reconstruction.toml`
- `evaluation/standards-effectiveness/fixtures/architecture/a1b-authority`
- `docs/plans/standards-engine-a1b/reports/a1b-authority-closure-audit.md`
- `docs/plans/standards-engine-a1b/plan.md`
- `docs/plans/standards-engine-a1b/issues.md`
- `docs/plans/standards-engine-a1b/execution-ledger.md`

**Tasks:**

- [ ] Implement typed snapshot, analysis, and navigation roots plus in-memory
  and directory adapters behind one Interface.
- [ ] Capture bounded snapshot bundles atomically and issue no handle on partial
  failure.
- [ ] Verify collision detection, path/symlink/nested-source behavior, durable
  publication, missing closure, identity contradiction, and unsupported root
  versions.
- [ ] Prove fresh-process reconstruction after source, provider, and process
  mutation using only store path and handle.
- [ ] Prove caches are disposable and enumeration is absent from the public or
  internal repository Interface.

**Acceptance gate:** A1B-A4 foundation evidence passes on in-memory and real
directory adapters.

**Status:** `Planned`

### Milestone 3: Coordinated V11 Runtime Cutover

**Goal:** Switch every repository-controlled producer and consumer atomically,
delete superseded authorities, and preserve A1 behavior.

**Allowed write set:**

- `tools/standards_engine`
- `tools/standards_analysis`
- `tools/standards_metadata`
- `tools/standards_policy_impact`
- `tools/standards_graph`
- `tools/standards_verifier`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/a1b-public-cutover.toml`
- `evaluation/standards-effectiveness/fixtures/contracts/a1b`
- `evaluation/standards-effectiveness/fixtures/architecture/a1b-authority`
- `evaluation/standards-effectiveness/policy-coverage/attestations`
- `docs/plans/standards-engine-a1b/reports/a1b-consumer-dispositions.md`
- `docs/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`
- `docs/plans/standards-engine-a1b/plan.md`
- `docs/plans/standards-engine-a1b/issues.md`
- `docs/plans/standards-engine-a1b/execution-ledger.md`
- `docs/decisions/standards-engine-a1b.md`

**Tasks:**

- [ ] Advance interface, result, analysis, snapshot, navigation, and analysis
  handle contracts exactly as defined by the ADR; retain unaffected identity
  domains.
- [ ] Move identity consumers to `standards_identity` and remove the old owner
  without a compatibility re-export.
- [ ] Make the facade use generated v11 inputs/results and exhaustive domain
  adapters.
- [ ] Move snapshot capture and all state/navigation persistence to
  `standards_authority`; remove store scans and process-local artifact
  authority.
- [ ] Add owner-qualified child handles and cold inspection for every
  advertised variant.
- [ ] Delete old validators, generated keyword walkers, snapshot compiler,
  analysis stores, aliases, and fallbacks in the same change.
- [ ] Reconcile every consumer disposition and renew only mechanically stale
  coverage attestations after the horizon is frozen.

**Acceptance gate:** A1B-A2, A1B-A4, A1B-A5, A1B-A7, and A1B-A8 pass; all old
versions reject as unsupported and no compatibility path remains.

**Status:** `Planned`

### Milestone 4: Exact-Tree Acceptance

**Goal:** Freeze one clean implementation tree, run complete evidence, and
obtain independent acceptance.

**Allowed write set:**

- `docs/plans/standards-engine-a1b/reports/a1b-implementation-candidate.md`
- `docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`
- `docs/plans/standards-engine-a1b/plan.md`
- `docs/plans/standards-engine-a1b/issues.md`
- `docs/plans/standards-engine-a1b/execution-ledger.md`
- `docs/decisions/standards-engine-a1b.md`

The reviewer-owned final acceptance report is a sole-change direct child of the
candidate it reviews. The later mechanical lifecycle transition may update only
the plan, issues, ledger, and ADR status and must identify both exact trees.

**Tasks:**

- [ ] Freeze and record the implementation commit/tree, dependency resolution,
  conformance corpus revision, generated outputs, consumer dispositions,
  coverage identities, and complete verification.
- [ ] Obtain independent Standards and Specification review against the exact
  tree.
- [ ] Accept only with no blocked consumer or claim and a clean worktree.
- [ ] Mark the ADR Accepted and this plan Accepted through the constrained
  transition.

**Acceptance gate:** A1B-A1 through A1B-A10 are satisfied.

**Status:** `Planned`

## Blockers

- `A1B-006`: independent planning admission has not yet accepted this exact
  plan and ADR tree.

## Re-Plan Triggers

- Any external consumer, independently deployed tool contract, or retained A1
  state invalidates the no-compatibility decision.
- Any remote reference, custom vocabulary, format assertion, validator
  override, unsupported recursive projection, or pattern incompatibility is
  required by reachable public schema.
- Any machine annotation lacks a closed representation and named executable
  owner.
- The locked dependency closure cannot satisfy a supported Python environment,
  has an unresolved blocking security/license issue, or cannot be reproduced
  without ambient state.
- Snapshot capture is not bounded enough for atomic bundle publication or
  requires streaming.
- Cold reconstruction requires source paths, Git objects, provider capability,
  store enumeration, process caches, or fresh authorization.
- A systemic finding identifies an unreviewed sibling producer or consumer.
- A proposed fix changes policy meaning, relationship authority, generic graph
  behavior, A2 mutable state, or another path outside the active milestone
  write set.
- Focused or broad verification reveals a pre-existing invalid oracle whose
  repair has a different owner.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `A2 remains inactive until this plan is independently accepted`
- Final status: `Blocked`

