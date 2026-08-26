# Plan: Standards Engine A1b Contract And Authority Foundations

**Plan status:** `Blocked`

**Current phase:** Replacement planning admission

**Next slice:** Independent exact-tree Standards and Specification review of
replacement planning candidate C3, including canonical entrypoint execution,
Authority contract validation, and coverage-source closure

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Replace A1's duplicated contract semantics, generic normalized identity
serialization, and fragmented immutable-authority storage with one
dependency-backed contract compiler, one codepoint-preserving identity encoder,
one direct immutable authority-object repository, and one generated public
request/result algebra. Preserve the four-operation read-only Standards Engine
and immutable analysis kernel while making every issued handle directly
resolvable in a cold process. Complete independent exact-tree acceptance before
any A2 review or implementation begins.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1B-A1 | The canonical schema is checked and every accepted instance is validated through the exact selected `jsonschema.Draft202012Validator`; known A1 equality and pattern regressions pass through that production adapter without a repository keyword interpreter. | `contract` | `not-applicable` | `automated` | `pending` | Pending Milestone 1 and atomic cutover |
| A1B-A2 | Every public operation request and result has one complete reachable schema closure, generated models preserve it, stale projections fail, and unsupported reachable projection semantics reject. | `contract` | `not-applicable` | `automated` | `pending` | Pending Milestones 1 and 3 |
| A1B-A3 | JSON Schema validation, applicability equality, identity encoding, and domain ordering/deduplication pass owner-specific fixtures without one domain deciding another. | `focused` | `not-applicable` | `automated` | `pending` | Pending Milestones 0, 1, and 3 |
| A1B-A4 | Every advertised snapshot, analysis, navigation, policy, relationship, coverage, context, requirement, and observation handle directly reconstructs its typed object in a fresh process after source and process mutation; durable publication and cleanup pass on Linux ext4. | `system` | `required-real` | `automated` | `pending` | Pending Milestones 2 and 3 |
| A1B-A5 | Public `query`, `prepare`, `resolve`, and `inspect` accept and return only generated v11 contract values; internal domain models and dependency exceptions cannot cross the facade. | `integration` | `not-applicable` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A6 | The selected external dependency closure is exact, hash-checked, reproducible on Linux x86-64 with glibc 2.17 or newer for CPython 3.11 and 3.12, imports from an isolated install, and is free of unresolved blocking security findings. | `release-artifact` | `required-real` | `automated` | `pending` | Pending Milestone 0 |
| A1B-A6I | Every Engine Module manifest exactly declares its production direct imports, Python range, public import root, and repository entrypoints; package roots expose one statically resolvable `__all__`; all production cross-Module and entrypoint imports resolve through those roots and exports; private, alternate-root, star, dynamic, or unowned imports reject; and every public export and exact entrypoint executes in both clean environments with only the admitted external lock. | `integration` | `required-real` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A6P | Before implementation starts, an independent planning review accepts the selected package provenance, license authorities, intended use, compatibility, and current non-bundling disposition. | `release-artifact` | `not-applicable` | `manual` | `pending` | Pending plan-admission report |
| A1B-A6L | Final independent review proves the implemented exact lock and provenance match the admitted selection and introduce no changed license or notice obligation. | `release-artifact` | `not-applicable` | `manual` | `pending` | Pending final acceptance review |
| A1B-A7 | No old validator, generated keyword interpreter, generic NFC identity encoder, snapshot compiler, split state store, owner map, scan, compatibility path, or old-version fallback remains reachable. | `integration` | `not-applicable` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A8 | Accepted and proposed policy-impact catalogs compile; every changed implementation node and relationship has a disposition; selected consumers equal disposition subjects; required coverage subjects equal valid certificate subjects. | `integration` | `not-applicable` | `automated` | `pending` | Pending Milestone 3 |
| A1B-A9 | Existing routing, analysis, coverage, reading, rendering, and inspection behavior remains valid except for declared contract, handle, identity, and storage replacements. | `integration` | `not-applicable` | `automated` | `pending` | Pending broad checkpoint |
| A1B-A10 | All focused package tests, registered declarative suites, retained migration checkers, generated freshness, plan checks, and diff hygiene pass without mutable catalog-count assertions. | `integration` | `not-applicable` | `automated` | `pending` | Pending final checkpoint |
| A1B-A11 | One clean implementation commit and tree has a reviewer-owned acceptance record confirming every claim, migration deletion, consumer disposition, and exclusion. | `release-artifact` | `not-applicable` | `manual` | `pending` | Pending final acceptance report |

## Scope

### In Scope

- A stdlib-only `standards_identity` Module owning identity encoding v2 and
  domain-separated hashing.
- A `standards_contracts` Module owning contract loading, the projection
  profile, local references, reachability, diagnostics, model construction, and
  build-time projections.
- `jsonschema==4.26.0` as the sole Draft validator and direct use of
  `referencing==0.37.0`.
- A `standards_authority` Module directly storing the closed set of public
  inspectable objects through in-memory and directory adapters, using
  `standards_contracts` as the sole validator for embedded v11 definitions.
- Contract v11, request v3, result projection v3, analysis contract/schema 7/4,
  public handle v4, authority envelope v1, and identity encoding v2.
- The exact proposed v11 public schema and interface contract in
  `reports/a1-contract-v11.schema.json` and `reports/a1-interface-v11.toml`.
- Domain-owned ordering, deduplication, normalization, and identity records.
- Complete repository-controlled consumer migration and deletion of
  superseded implementations.
- Supplemental node-catalog and source-owned relationship migration for
  created, retained, and retired implementation artifacts.
- Registered Python verification, dependency and licensing evidence, coverage
  reconciliation, and exact-tree acceptance.
- Manifest-owned public import roots and repository entrypoints,
  initializer-owned static export closure, and one AST-backed verifier contract
  for every governed production cross-Module import.

### Out Of Scope

- A2 authoring, mutation, proposal heads, canonical application, or recovery.
- A compatibility layer, old-state converter, dual reader/writer, old-contract
  fallback, or identity migration tool.
- Implementing JSON or JSON Schema, overriding validator behavior, copying or
  running the complete official JSON Schema corpus, or claiming independent
  Draft certification.
- Changes to normative policy meaning, relationship-kind semantics, generic
  graph behavior, or routing policy. Adding policy-unit projections for exact
  existing headings and updating implementation consumer nodes/relationships
  are in scope.
- A general content-addressed DAG, public enumeration, garbage collection,
  remote storage, mutable indexes, arbitrary object types, or streaming
  snapshots.
- Runtime remote schema retrieval, custom vocabularies, format assertion, or
  dynamic references.
- New or extended Bash verification.
- Plan C external-project baselines.

## Constraints And Assumptions

### Constraints

- This plan is unavailable while `Blocked`. The exact admission and start
  chain must complete before any implementation edit.
- The accepted standards-recovery boundary is the comparison base. The direct
  start-transition child is the implementation base.
- Foundation Modules may be implemented and tested only against private staging
  fixtures. They may not modify or become dependencies of accepted production
  A1 before the atomic Milestone 3 cutover.
- Milestones 0 through 2 are ordered working-tree checkpoints inside one
  implementation transaction. They are not committed or accepted separately.
  Milestone 3 produces the first implementation commit and includes every
  foundation, production consumer, catalog/relationship migration, and final
  coverage update.
- Public replacement is atomic. Old and new production authorities never
  coexist in an accepted runtime.
- Dependency installation and verification use the accepted hash-checked lock.
  Ambient alternate packages are not evidence.
- Generated freshness and semantic correctness are separate gates.
- Coverage attestations are renewed only after every horizon-affecting input is
  frozen.
- Mutable repository totals are not acceptance oracles.

### Assumptions

- [Consumer and state inventory](reports/consumer-and-state-inventory.md) found
  no external consumer and no retained A1 persisted state.
- The bounded repository snapshot remains small enough for atomic object
  publication; Milestone 2 measures the admitted capture.
- The reviewed dependency resolution supports Linux x86-64 with glibc 2.17 or
  newer for CPython 3.11 and 3.12; Milestone 0 reproduces both exact native
  wheel tags. Other targets are unsupported.
- The durable authority adapter supports Linux ext4 only in A1b. The in-memory
  adapter remains repository-neutral; another durable filesystem requires a
  separate capability and durability decision.
- Existing applicability NFC semantics are domain-owned and remain unchanged
  after byte-level dependency proof.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Preserve the four-operation read-only facade and immutable analysis kernel. | Accepted A1 architecture | [A1 ADR](../../decisions/standards-engine-navigation-analysis.md) | None |
| Use `jsonschema.Draft202012Validator` as the sole Draft validator behind one deep project adapter. | Contracts and Dependencies | [A1b ADR](../../decisions/standards-engine-a1b.md), [dependency decision](reports/dependency-and-dialect-decision.md) | Local validator and generated keyword interpreter |
| Keep schema validation, applicability equality, identity encoding, and domain ordering separate. | Owning domain Modules | [Schema/domain audit](reports/schema-and-domain-contract-audit.md) | Generic serializer as cross-domain semantics |
| Use codepoint-preserving identity encoding v2; domain Modules own typed identity records and any semantic normalization. | Identity and domain owners | [Identity/version matrix](reports/identity-version-object-matrix.md) | Recursive NFC identity encoding v1 |
| Directly store every inspectable object through one closed acyclic immutable authority Interface; delegate embedded v11 definition validation to Contracts; keep readers lock-free; serialize writers through non-authoritative publication coordination; make same-ID publication idempotent by content identity; and expose explicit interruption outcomes. | Architecture, Persistence, Contracts, Concurrency, and Resilience | [Authority-object contracts](reports/authority-object-contracts.md), [identity/version matrix](reports/identity-version-object-matrix.md), [consumer inventory](reports/consumer-and-state-inventory.md) | Three-root storage plus owner maps, scans, caches, or duplicated schema interpretation |
| Support one exact Linux ext4 durable-store contract with filesystem-aware identity, handle-relative mutation, explicit aliases, and typed unsupported outcomes. | Cross-Platform and Security | [A1b ADR](../../decisions/standards-engine-a1b.md), [authority-object contracts](reports/authority-object-contracts.md), [migration plan](reports/policy-impact-migration-plan.md) | Operating-system-name inference and path-based validation/use |
| Remove all schema `x-standards-engine-*` annotations; use one closed interface contract and domain-owned executable contracts. | Contracts and domain owners | [Schema/domain audit](reports/schema-and-domain-contract-audit.md) | Mixed machine prose in public schema |
| Build isolated foundations, then perform one atomic production v11 cutover. | Planning and integration owner | This plan | Partial schema/generated production cutover |
| Migrate implementation catalog and policy-impact relationships in the atomic cutover. | Policy Impact and coverage owners | [Migration plan](reports/policy-impact-migration-plan.md) | Treating implementation artifact changes as incidental paths |
| Keep `policy-impact-registry.toml` as the sole closed declaration-source membership authority and register every admitted source explicitly. | Policy Impact | [Migration plan](reports/policy-impact-migration-plan.md) | Filesystem discovery or policy-unit-derived relationship registration |
| Make each Engine Module manifest own one public import root and its repository entrypoints; make the root's closed `__all__` expression own exported names; require entrypoints to call canonical-root adapters; and enforce all three with one AST-backed Standards Verifier contract plus safe-path execution. | Dependencies and Verification | [Dependency decision](reports/dependency-and-dialect-decision.md), [consumer inventory](reports/consumer-and-state-inventory.md) | Root-only smoke, script-directory imports, generator-only checks, implicit Python child-module loading, and copied package or symbol allowlists |
| Keep A2 inactive through independent A1b acceptance. | Planning | Accepted standards recovery | Direct progression to authoring |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Generated files are current | Freshness | Deterministic projection `--check` | Canonical schema, interface contract, and compiler | Semantic correctness | Stale generated output diagnostic |
| Contract adapter is correct | External-contract adapter | Production adapter regressions and schema self-check | Selected validator API and canonical contract | Independent Draft re-certification | Exact keyword/path diagnostic |
| Projection closure is complete | Public shape | Reachability compiler and public-operation fixtures | Canonical v11 schema and closed interface contract | Constructs outside the admitted projection profile | Unsupported reachable construct or unreachable public definition |
| Identity is representation preserving | Content identity | Exact codepoint fixtures and domain identity records | Identity v2 contract | Domain semantic equality | NFC-equivalent inputs remain distinct unless owner normalizes |
| Domain equality/order is local | Domain semantics | Applicability and analysis owner fixtures | Each domain contract | Generic identity-byte ordering or equality | Generic identity bytes cannot decide semantic equality or order |
| Cold reconstruction is complete | Persisted authority | Fresh process with store path and handle only | Persisted object envelope and dependencies | In-process caches or unavailable durable filesystem | Missing is unavailable; contradiction is invalid |
| Public algebra is exhaustive | Public path | Real facade/tool calls using exported generated types | Public operation closure | Internal domain values crossing the facade | Unhandled domain result is a programming error |
| External dependency is reproducible | Release artifact | Hash-checked isolated install and dependency import smoke | Reviewed lock, artifact hashes, provenance, licenses | Unreviewed platform, Python, wheel, or source build | Missing or mismatched artifact blocks installation |
| Internal Module closure is exact | Source-tree integration | AST-derived production-import/manifest equality, root-export resolution, governed-source ownership, and isolated root/export/entrypoint execution | Manifest-owned requirements, roots, repository entrypoints, package `__all__`, and reviewed checkout | Independently published or installed local distributions | Missing, transitive-only, unused, ambient, alternate-root, undeclared, private-child, root-plus-private-child, star, dynamic, or unowned production import fails |
| Policy-impact migration is complete | Semantic consumers | Accepted/proposed compile, exact admitted-source registration, and exact disposition equality | Closed policy-impact registry, compiled relationship authority, and independent horizon | Empty impact without certified coverage | Unregistered source, unmapped node, edge, consumer, or coverage subject blocks |
| Negative fixture reaches intended rule | Negative evidence | Otherwise-valid fixture and exact diagnostic assertion | Owning typed diagnostic | Failure at another precondition | Failure at another precondition rejects the test |

A1b does not use agreement between local implementations as external Draft
conformance and does not run the complete upstream corpus.

## Systemic Finding Audit

- **Invariant families:** contract validation and projection, identity encoding,
  semantic ordering/deduplication, immutable object resolution, package
  dependency/public-export closure, and implementation-consumer coverage.
- **Inventories:** [schema/domain audit](reports/schema-and-domain-contract-audit.md),
  [identity/version matrix](reports/identity-version-object-matrix.md),
  [authority-object contracts](reports/authority-object-contracts.md),
  [consumer/state inventory](reports/consumer-and-state-inventory.md), and
  [policy-impact migration](reports/policy-impact-migration-plan.md).
- **Required disposition:** every repository-controlled implementation,
  representation, relationship, and selected consumer is `updated`,
  `reviewed-no-change`, or `not-applicable` with rationale. Any blocked,
  missing, or unaudited item blocks cutover.
- **Empty impact rule:** an empty result is not evidence of no impact without a
  valid independent coverage certificate.

## Planning And Admission Boundary

The comparison base is commit
`c4408363752b10060f631247f3e2f1fa26eae003`, tree
`84477150bd368a168dd04da3770de55c23bbb817`.

The rejected candidate `f41037bf71deddba36056b27d418fe767a7cfb62`,
tree `042f97101d50df79dcac0b029aa1b9324cf8b881`, is `Superseded`
by the replacement candidate created from this plan revision.

The later candidate `44de7dff9c83f08b24225c82ad1b6a974f6655a9`,
tree `24925cfce1d87f69bfde78d9f060eddae6963308`, is also
`Superseded`. Its review found that two admitted relationship files were absent
from the closed relationship-source registry and that successful imports did
not prove use of public package boundaries.

Candidate C-prime `ecdf5a55588d18d068a513d910959ccbd9c65f71`, tree
`ec19cb2c02a67f96229176302d5dbcd3f4964022`, is `Superseded` by C2.
Its review found that module-path equality still permitted Python's implicit
`from public_root import private_child` loading and that the systemic migration
did not disposition every affected package artifact and existing private-import
consumer.

Candidate C2 `c2aea75c85800aec6ac00fcc3b2690f8629845ab`, tree
`19074828c41ac1c2d8814578f08604106112ad1c`, is `Superseded` by C3.
Its Specification review passed. Its Standards review found that Verifier-local
entrypoints still depended on ambient alternate-root imports, Authority's v11
shape-validation dependency was undeclared, the coverage attestation-source
registry was absent from the cutover write set, and the active Router evidence
omitted Commit.

Admission and start require this direct-child chain:

1. **C3:** clean replacement planning candidate containing no implementation
   and superseding every rejected candidate named above;
2. **R:** reviewer-owned `reports/a1b-plan-admission.md` as the sole change,
   binding C3, explicitly accepting the dependency provenance/licensing
   disposition in A1B-A6P, and reporting no blocking Standards or
   Specification finding;
3. **T:** mechanical admission transition as the direct child of R, changing
   only lifecycle fields in `plan.md` and `issues.md` plus one append-only
   transition record in `execution-ledger.md`, setting A1B-A6P to `satisfied`
   with R as evidence and setting the plan to `Planned`; and
4. **S:** `start` transition as the direct child of T, changing only those
   lifecycle fields plus one append-only ledger record, setting the plan and
   Milestone 0 to `Active`.

S is the exact clean implementation base. Any intervening commit, extra file,
dirty worktree, identity mismatch, or review finding invalidates the chain.
Neither R nor T starts implementation.

## Milestones

### Milestone 0: Dependency And Identity Foundation

**Goal:** Reproduce the reviewed lock and implement identity encoding v2 in an
isolated Module without changing accepted A1 production imports or behavior.

**Allowed write set:**

- `tools/standards_identity/`
- `tools/standards_contracts/pyproject.toml`
- `tools/standards_contracts/requirements.lock`
- `tools/standards_contracts/README.md`
- `tools/standards_contracts/tests/test_dependency_resolution.py`
- `docs/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [ ] Reproduce the exact dependency names, versions, target wheels, and hashes.
- [ ] Record authoritative provenance, license files, supported targets,
  security results, and install command.
- [ ] Implement identity encoding v2, domain hashing, immutable typed inputs,
  and exact codepoint/invalid-value fixtures.
- [ ] Prove no accepted A1 production import or output changes.

**Acceptance gate:** Identity foundation and A1B-A6 pass; isolated package
tests and the accepted broad baseline remain green. A1B-A6L remains a distinct
manual exact-lock final-acceptance claim; A1B-A6P must already be satisfied
before start. Record the checkpoint in the ledger working tree, but do not
commit it separately.

**Status:** `Blocked`

### Milestone 1: Isolated Contract Compiler

**Goal:** Implement the contract adapter and projection compiler against the
exact admitted machine-readable v11 schema and interface contract without
changing the production schema, generated output, or facade.

**Allowed write set:**

- `tools/standards_contracts/`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [ ] Implement schema self-check, retrieval-free local registry, stable errors,
  reachable closure, and projection-profile admission.
- [ ] Compile the admitted `reports/a1-interface-v11.toml` and
  `reports/a1-contract-v11.schema.json` without rewriting or extending their
  public algebra. Any required shape change is a re-plan trigger.
- [ ] Generate staging immutable Python and agent-tool projections without a
  keyword interpreter or default injection.
- [ ] Prove known A1 Boolean/integer, Unicode, `pattern`, and `uniqueItems`
  behavior through the production-intended adapter.
- [ ] Reject unsupported projection constructs and unreachable public roots.

**Acceptance gate:** A1B-A1, the isolated half of A1B-A2, and contract portions
of A1B-A3 pass while every accepted production A1 artifact remains byte
identical. Record the checkpoint in the ledger working tree, but do not commit
it separately.

**Status:** `Planned`

### Milestone 2: Isolated Authority Repository

**Goal:** Implement the closed direct-object repository and prove atomic
publication and cold reconstruction independently of the accepted facade.

**Allowed write set:**

- `tools/standards_authority/`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [ ] Implement the envelope, closed object-kind registry, typed handles,
  in-memory adapter, and directory adapter.
- [ ] Implement authority-owned Git-tree and mutable-manifest capture adapters,
  exact scope/path/symlink/nested-source handling, and two-pass source-change
  rejection.
- [ ] Store and resolve every root and child kind from the identity matrix
  directly by handle.
- [ ] Verify same-directory create-only hard-link publication, collision
  detection, missing objects, binary and empty snapshot entries,
  Base64/digest/length contradiction, kind mismatch, unsupported versions,
  file/directory flush, store ownership/mode enforcement, symlink rejection,
  and unsupported-filesystem rejection.
- [ ] Prove the required-real ext4 contract with spaces, canonical root
  descriptor equality, rejection of `.`, `..`, repeated-separator, final
  symlink, and intermediate-symlink aliases, case-sensitive distinct names,
  writable-mount detection, and typed unknown-filesystem outcomes. Walk every
  configured absolute-path component from a trusted `/` descriptor using
  directory-relative no-follow opens; exercise concurrent parent-component
  replacement without redirecting authority and rewalk the complete path
  before returning success.
- [ ] Prove overlapping writers serialize without changing identity,
  different-ID independence after publication, same-ID idempotence,
  same-ID contradictory collision, interruption before publication,
  interruption after publication before acknowledgement, retry
  reconciliation, crash-released publication lock, next-writer abandoned
  staging cleanup, normal-path terminal cleanup, and fresh-process reopening.
- [ ] Prove fresh-process reconstruction using only persisted objects and
  handles after source and process mutation.
- [ ] Prove no enumeration, owner map, root scan, cache index, or ambient
  provider authority is needed.

**Acceptance gate:** The isolated half of A1B-A4 passes on both adapters.
Record the checkpoint in the ledger working tree, but do not commit it
separately.

**Status:** `Planned`

### Milestone 3: Atomic V11 Production Cutover

**Goal:** Switch every production producer, semantic registration, and consumer
in one replacement boundary; delete all superseded authority.

**Allowed write set:**

- `tools/standards_identity/`
- `tools/standards_contracts/`
- `tools/standards_authority/`
- `tools/standards_applicability/`
- `tools/standards_metadata/`
- `tools/graph_engine/`
- `tools/standards_policy_impact/`
- `tools/standards_graph/`
- `tools/standards_analysis/`
- `tools/standards_engine/`
- `tools/standards_verifier/`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-impact-registry.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-units/dependencies.toml`
- `evaluation/standards-effectiveness/policy-units/registry.toml`
- `evaluation/standards-effectiveness/policy-units/cross-platform.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.cross-platform.toml`
- `evaluation/standards-effectiveness/policy-units/security.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.security.toml`
- `evaluation/standards-effectiveness/policy-impact/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-coverage/horizons.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/a1b-contract-conformance.toml`
- `evaluation/standards-effectiveness/suites/a1b-authority-reconstruction.toml`
- `evaluation/standards-effectiveness/suites/a1b-public-cutover.toml`
- `evaluation/standards-effectiveness/fixtures/contracts/a1b/`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1b/`
- `evaluation/standards-effectiveness/fixtures/architecture/a1b-authority/`
- `tools/query_edges.py`
- `tools/verify_git_reachability.py`
- `docs/plans/standards-engine-a1b/reports/a1b-contract-profile-audit.md`
- `docs/plans/standards-engine-a1b/reports/a1b-authority-closure-audit.md`
- `docs/plans/standards-engine-a1b/reports/a1b-consumer-dispositions.md`
- `docs/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [ ] Promote the exact admitted planning schema and interface contract
  byte-for-byte to their canonical production paths; generate the complete
  public Python and agent-tool algebra.
- [ ] Advance every identity and public contract in the identity/version matrix
  and use domain-owned typed keys for ordering and deduplication.
- [ ] Route all public validation through `standards_contracts` and all public
  object persistence/inspection through `standards_authority`. Authority must
  use the Contracts named-definition adapter for every embedded v11 value and
  own its envelope, closed stored-payload records, identity, dependency-kind,
  object-local, and DAG validation.
- [ ] Exhaustively adapt domain requests and outcomes at the facade.
- [ ] Accept coverage claims as input, validate evidence and trusted execution
  authorization, and construct stored coverage attestations only inside the
  analysis kernel.
- [ ] Update every manifest in the closed Module dependency table with exact
  direct requirements, the admitted Python range, one public source-tree import
  root, and its repository entrypoint scripts. Require each public-root
  `__init__.py` to define exactly one statically resolvable `__all__` through the
  closed literal-and-local-star export profile. Derive imports with Python AST,
  require exact manifest equality and source ownership, and reject imports
  below another Module's root, root-form names absent from resolved `__all__`,
  cross-Module star imports, or literal/dynamic import bypasses.
- [ ] Derive all governed production Python from manifest roots and repository
  entrypoints, and reject tracked non-test Python under `tools/` that has no
  manifest owner. Assign the canonical graph query and Git-reachability scripts
  to the Standards Verifier manifest. Replace ambient or alternate-root imports
  in every exact Verifier entrypoint with canonical-root adapters.
- [ ] Execute every manifest-owned public root, every resolved export, and every
  exact repository entrypoint in clean CPython 3.11 and 3.12 environments after
  installing only the admitted external lock. Use safe-path mode from outside
  the checkout with the checkout root as the sole `PYTHONPATH`; mutating
  entrypoints operate only on isolated repository fixtures.
- [ ] Make generated imports a closed compiler prelude, verify their AST in
  focused compiler tests, and independently reject otherwise-valid generated
  and handwritten-facade fixtures for both `from public_root.private_child`
  and `from public_root import private_child`. Require the intended rule's exact
  diagnostic and prove that exported root names remain accepted.
- [ ] Delete old validators, generated keyword walkers, generic NFC serializer,
  snapshot compiler, split stores, owner maps, scans, aliases, and fallbacks.
- [ ] Register the Cross-Platform and Security declaration files explicitly in
  the closed policy-impact registry. Compile accepted and proposed
  catalogs/relationships; require every admitted declaration source and natural
  key to appear in migration evidence; and record every node, edge, and
  selected-consumer disposition without fixed cardinality assertions.
- [ ] Reject an otherwise-valid migration fixture whose admitted relationship
  source is absent from the closed registry with the exact migration-completeness
  diagnostic; the relationship compiler remains responsible only for compiling
  its registered closed input.
- [ ] Freeze all horizon inputs, derive requirements, renew stale attestations
  through the existing authorization/evidence path, register the new
  owner-local Cross-Platform and Security attestation files in the closed
  attestation-source registry, and compile certificates.
- [ ] Prove exact selected-consumer/disposition and
  requirement/certificate equality.

**Acceptance gate:** Every automated objective claim passes. Final manual
A1B-A6L and A1B-A11 remain pending exact-tree acceptance.
Any required path outside this write set, any substantive ADR change, blocked
disposition, or horizon change after attestation is a re-plan trigger. The
admitted ADR remains byte-identical and `Proposed` throughout Milestone 3;
Milestone 4 alone may change its status after exact-tree acceptance.

Milestone 3 creates the first implementation commit after start. Its parent is
the clean start-transition commit S; no foundation-only implementation commit
may intervene.

**Status:** `Planned`

### Milestone 4: Exact-Tree Acceptance

**Goal:** Freeze one clean implementation tree, run complete evidence, and
obtain independent acceptance.

**Allowed write set:**

- `docs/plans/standards-engine-a1b/reports/a1b-implementation-candidate.md`
- `docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger
- ADR status only in `docs/decisions/standards-engine-a1b.md`

The final reviewer report is a sole-change direct child of the implementation
candidate. A later mechanical acceptance transition may update only the
declared lifecycle fields and must identify both exact trees.

**Tasks:**

- [ ] Record the exact implementation commit/tree, dependency resolution,
  generated outputs, identity versions, object kinds, node/edge/consumer
  dispositions, coverage identities, and complete verification.
- [ ] Obtain independent Standards and Specification review against that exact
  tree.
- [ ] Accept only with no blocked claim or consumer and a clean worktree.
- [ ] Mark the ADR and plan Accepted through the constrained transition.

**Acceptance gate:** Every objective acceptance claim is satisfied.

**Status:** `Planned`

## Blockers

- `A1B-006`: independent planning admission has not accepted this replacement
  candidate and its direct-child transition chain.

## Re-Plan Triggers

- Any external consumer or retained A1 state invalidates the no-compatibility
  decision.
- Any reachable public contract requires excluded validator configuration or
  unsupported projection semantics.
- Implementation reveals that either admitted machine-readable v11 contract
  artifact requires a field, variant, version, or operation-shape change.
- The exact dependency resolution cannot satisfy an admitted environment or
  has a blocking provenance, license, or security result.
- An identity consumer cannot express its semantic normalization, ordering, or
  deduplication through an owning typed contract.
- An inspectable value cannot use the closed direct-object repository without
  scans, mutable indexes, or ambient authority.
- Bounded atomic snapshot publication is invalidated by measured size,
  streaming requirements, or missing ext4 hard-link/flush/lock behavior.
- A systemic sibling, semantic consumer, relationship, horizon input, or
  required source path falls outside the admitted inventory or write set.
- A required relationship declaration cannot be registered through the closed
  policy-impact registry, or relationship membership requires path inference.
- A production cross-Module import cannot be expressed through one
  manifest-owned public root and statically resolved export, or requires runtime
  import discovery.
- A repository entrypoint cannot execute from outside the checkout through its
  manifest-owned canonical root without script-directory or ambient imports.
- A foundation milestone changes accepted production A1 before Milestone 3.
- A proposed correction changes normative policy meaning, relationship-kind or
  generic graph semantics, A2 behavior, or another owner outside scope.
- Focused or broad verification reveals a pre-existing invalid oracle whose
  repair has a different owner.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `A2 remains inactive until A1b is independently accepted`
- Final status: `Blocked`
