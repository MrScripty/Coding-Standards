# Plan: Standards Engine Navigation And Analysis

**Plan status:** `Accepted`

**Current phase:** Plan A1 accepted

**Next slice:** none within Plan A1; Plan A2 remains inactive until separately
reviewed and admitted

**Acceptance status:** `satisfied`

**Accepted implementation boundary:** commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`; evidence in
[A1 final acceptance](reports/a1-final-acceptance.md)

**Rejected repair V implementation boundary:** commit
`e7e0e1e20762f994e644f2e3c88d017d1625266c`, tree
`22c263b4f30c706b94ce3125c8f0537e5d210fe6`; evidence in
[A1 boundary repair V candidate](reports/a1-boundary-repair-v-candidate.md)

**Rejected repair IV implementation boundary:** commit
`3d389dd7f73f48c21d80570331c8058737f941db`, tree
`6fcbfed114dcfd768186f8610c0792e220657b32`; evidence in
[A1 boundary repair IV candidate](reports/a1-boundary-repair-iv-candidate.md)

**Rejected repair III implementation boundary:** commit
`8ed8ba0beba5dd16c0a2da50655952842ab61c85`, tree
`eaeac78739468fc2c79241f6a7830e54986d2f95`; evidence in
[A1 boundary repair III candidate](reports/a1-boundary-repair-iii-candidate.md)

**Rejected repair II implementation boundary:** commit
`714ba23fb5186b549ab44865d36c77509dbf654a`, tree
`d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b`; evidence in
[A1 boundary repair II candidate](reports/a1-boundary-repair-ii-candidate.md)

**Withdrawn candidate implementation boundary:** commit
`51dcd258942b0774c73ae8b620227c7ce34d1129`, tree
`f8d028e887f4061a1d03ad6e75b9776a5fc3966b`

**Withdrawn repaired acceptance boundary:** commit
`b8f52240572962dd4393ff2d05b245a0c7f822a9`, tree
`626c761fab2d5c5885d627f402c7b392bab12039`

**Withdrawn acceptance boundary:** commit
`94b295b40bc1cef9a6281355d68115f3a98ed112`, tree
`ff032da51fcaff45533c07daa8de464065b8e55c`

**Recovery boundary:** commit
`13a9f48b95ed7532f480e4604d9dfa23443e8f43`, tree
`c27a1e2bbf52244c5b30eb1d21381be6e5c86d68`

**Implementation base:** commit
`c7d23dfa55a9558b929e6b838d7ea0563981a1ef`, tree
`5e9c4eb211ee0a67039b0ec11142db9b106243ae`

**Implementation admission:** operation `continue` accepted for Milestones 3
and 4 from the recorded implementation base and accepted replans;
implementation remains bounded by the current milestone and exact next slice

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Development brief:**
[Standards Engine Navigation and Analysis](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md)

## Objective

Provide one agent-facing, typed Standards Engine that lets a caller discover,
retrieve, and navigate canonical standards without repository paths, then
compare supplied accepted and proposed standards snapshots and resolve every
deterministically selected impact obligation into a complete read-only analysis
result. The engine must expose uncertainty and authority explicitly, preserve
one source for canonical metadata and schemas, and leave semantic acceptance,
repository mutation, and external-project application outside A1.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Every canonical corpus member, module ID, alias, document path, `Requires` edge, and `Specializes` edge is loaded through one neutral metadata API, and every inventoried consumer uses that API without a parallel production loader. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 acceptance](reports/milestone-1-neutral-metadata-cutover.md) |
| A2 | Clean Git, dirty/non-Git, untracked-file, file-mode, symlink, submodule, exclusion, interpretation-affecting semantic-contract version, and integrity-closure inputs produce deterministic immutable snapshot identities under the accepted serialization contract; implementation releases that preserve those contracts remain provenance. | `contract` | `not-applicable` | `automated` | `satisfied` | [A1 final acceptance](reports/a1-final-acceptance.md) |
| A3 | A typed agent can route from structured facts, receive canonical IDs, read canonical content, navigate declared relations, and inspect advertised handles through follow-up requests bound to the same immutable snapshot or analysis without supplying repository paths. | `user-workflow` | `not-applicable` | `automated` | `satisfied` | [A1 final acceptance](reports/a1-final-acceptance.md) |
| A4 | Policy-unit identity, accepted and proposed semantic state, move, split, merge, retirement, successor, alias, and unmapped normative-change rules preserve identity and produce the required typed outcomes without treating structure as semantic proof. | `contract` | `not-applicable` | `automated` | `satisfied` | [Lifecycle impact evidence](reports/milestone-3-lifecycle-impact-selection.md) |
| A5 | Modification, addition, removal, move, split, and merge select deterministic seeds, traverse the accepted/proposed relation union through the existing graph engine, retain unknown applicability, and generate every required scoped obligation. | `integration` | `not-applicable` | `automated` | `satisfied` | [Consumer-obligation recovery](reports/milestone-3-consumer-obligation-recovery.md) |
| A6 | Derived coverage requirements plus authorized attestations generate deterministic reusable certificates, reject stale or unaudited coverage, and never infer successful empty impact from absent edges or convert unknown applicability into true. | `contract` | `not-applicable` | `automated` | `satisfied` | [Coverage identity cutover](reports/milestone-3-coverage-identity-cutover.md) |
| A7 | `prepare` and iterative `resolve` return a `CompleteResult` only when final reached consumer-obligation IDs equal valid disposition IDs, derived fact-requirement IDs equal valid observation requirement IDs, and every other obligation, authorization, and coverage condition is resolved. | `integration` | `not-applicable` | `automated` | `satisfied` | [Single-state implementation evidence](reports/milestone-4-single-state-acceptance.md) |
| A8 | One canonical interface schema mechanically governs Python types, defaults, discriminants, nested request and submission variants, JSON validation, agent-tool definitions, examples, identity-bearing serialization, result variants, derived `next_operations`, and text rendering; projection drift fails verification. | `contract` | `not-applicable` | `automated` | `satisfied` | [A1 final acceptance](reports/a1-final-acceptance.md) |
| A9 | Representative modification, addition, and removal changes complete through the real typed agent adapter; move, split, and merge behavioral fixtures pass; focused package tests and affected broad repository verification pass from one recorded clean tree. | `user-workflow` | `not-applicable` | `automated` | `satisfied` | [A1 final acceptance](reports/a1-final-acceptance.md) |

## Scope

### In Scope

- A neutral `tools/standards_metadata/` package for canonical corpus and module
  metadata access.
- A `tools/standards_analysis/` package for snapshot comparison, policy-unit
  impact, applicability, audit coverage, analysis states, reading plans, and decision
  reuse.
- A standard-library-only `tools/standards_applicability/` package for compiled
  fact schemas, immutable programs, bound fact sets, three-valued evaluation,
  unresolved-fact reporting, and typed applicability failures.
- A `tools/standards_engine/` composition façade exposing the typed Python and
  agent-tool contracts.
- Snapshot-bound `query`, `prepare`, `resolve`, and `inspect` operations.
- Canonical interface schemas, domain-separated serialization, immutable
  handles, and typed result families.
- A mechanically generated or validated executable projection of Router-owned
  routing decisions.
- Policy-unit declarations and coverage attestations that reference canonical module IDs
  without redefining IDs, aliases, paths, membership, `Requires`, or
  `Specializes`.
- Adaptation of the verifier and repository graph composition to consume the
  neutral metadata API.
- Deterministic text rendering as a non-authoritative projection of typed
  results.
- Real typed-agent route/read and prepare/resolve acceptance fixtures.

### Out Of Scope

- Controlled authoring, change sessions, proposal storage, repository writes,
  semantic acceptance, canonical application, rollback, or recovery.
- Evidence-oracle policy and the 27 central-README projection dispositions in
  future Plan B.
- External project baselines, project bindings, or standards-upgrade analysis
  in future Plan C.
- A GUI, custom command language, or agent parsing of formatted prose.
- Automated judgment of arbitrary prose meaning or lexical inference of
  authoritative relationships.
- A replacement or policy-aware fork of `tools/graph_engine/`.
- Direct agent edits to graph, policy-unit, audit, registry, or generated data.
- A performance or resource-use claim without separate routed Performance
  authority and accepted measurements.
- New third-party dependencies in the currently planned work; a demonstrated
  requirement triggers re-planning and Dependencies routing.

## Routed Standards

| Module | Applicability to this plan |
| --- | --- |
| `core` and `router` | Universal authority, explicit scope, ownership, typed outcomes, and routed selection. |
| `workflow.planning` | Multiple dependent contracts, migrations, acceptance claims, and explicit admission are material. |
| `workflow.implementation` | Python, schemas, fixtures, documentation, and generated projections will change after admission. |
| `workflow.verification` | Public contracts, impact completeness, security, and agent workflows require named evidence. |
| `workflow.documentation` | New durable module boundaries, a public typed contract, and a cross-boundary decision require READMEs and an ADR. |
| `workflow.tooling` | A repository development tool and its agent adapters, schemas, and verification orchestration are created. |
| `workflow.commit` | Tooling requires commit-boundary and integration discipline; this plan does not itself authorize a commit. |
| `topic.architecture` | New metadata, analysis, and façade modules change authority, composition, and dependency direction. |
| `topic.contracts` | Typed requests/results, schemas, serialized identities, generated projections, and independent tool consumers form contracts. |
| `topic.diagnostics` | Stable rejection codes, safe context, exception separation, and text projection are affected. |
| `topic.security` | Typed requests and capability context authorize reads, reviews, evidence use, and filesystem access. |
| `topic.cross-platform` | Snapshot identity includes paths, modes, symlinks, Unicode, submodules, and filesystem-specific behavior. |
| `profile.boundary.persistence` | Snapshot construction reads durable Git and filesystem state and must preserve exact source identity and failure semantics. |

Performance is not selected because this plan makes no latency, throughput,
memory, or optimization acceptance claim. Concurrent Plan Integration is not
selected for the current serial planning slice because there is one integration
owner and no outstanding A1 proposals. It must be routed if multiple mutable
plan or shared-authority proposals can become stale before integration.

## Constraints And Assumptions

### Constraints

- Canonical standards documents and their metadata remain authority for module
  identity, document path, aliases, `Requires`, and `Specializes`.
- `standards_metadata` loads, validates, and projects canonical facts; it does
  not redefine them or depend on the verifier or analyzer.
- `standards_applicability` depends only on the Python standard library and
  owns executable applicability semantics without loading repository files or
  defining serialized A1 shapes.
- `standards_analysis` depends on neutral applicability, metadata, compiled
  policy-impact, and graph contracts; it owns policy-specific analysis without
  adding policy meaning to the graph.
- `standards_engine` is the composition root. Lower packages do not depend on
  it or form cycles.
- The existing graph engine remains repository-neutral and supplies its
  accepted named-group and traversal mechanics.
- Every public query and returned navigation handle is bound to one immutable
  snapshot identity.
- A1 compares externally supplied accepted and proposed snapshots. It never
  promotes proposed semantic state or authorizes a repository mutation.
- A proposed semantic revision is carried in the analysis request overlay, not
  written into accepted policy-unit authority.
- Canonical schema authority is singular. Python types, JSON validation,
  agent-tool definitions, examples, and text rendering are generated or
  mechanically validated projections.
- Identity-bearing serialization is versioned, deterministic, Unicode-defined,
  and domain-separated. Timestamps, summaries, formatting, and derived next
  operations do not affect identity.
- Accepted and proposed graph relations are queried as a union so removal of an
  edge cannot hide a former consumer.
- Valid missing facts produce `unknown`; malformed or unsupported expressions
  are invalid. Conservative review selection never changes `unknown` to true.
- Any changed normative content outside exactly one valid policy-unit locator
  creates a mandatory conservative whole-artifact obligation.
- The complete `AnalysisSnapshot` binds every analysis input, including
  repository-local attestations. A narrower `CoverageAuthorityView` binds only
  typed inputs capable of changing consumer discovery. Committing an
  attestation therefore changes the complete analysis input without changing
  the narrower requirement it answers.
- Consumer coverage is bounded by a mechanically derived requirement, an
  authorized attestation, and a generated certificate over an independent
  registered audit horizon. Coverage certificates never own change-specific
  dispositions. An unaudited empty edge result is not success.
- Coverage projection exclusions are based on typed artifact roles, never an
  ignored directory. Attestations, their source registrations, certificates,
  analysis results, timestamps, summaries, and dispositions do not enter the
  coverage view; relationship authority cannot escape projection by location.
- Coverage identity binds the target semantic payload and relationship state,
  not the transient `proposed` or `accepted` label. Promotion of identical
  reviewed content and relationships preserves applicable coverage.
- `CompleteResult.status` is derived from exact obligation,
  disposition, fact-requirement, observation, authorization, evidence, and
  coverage invariants.
- Shared schemas, metadata authority, registries, plans, and generated outputs
  have one serial integration owner.
- No A1 implementation slice may overlap an admitted verifier-migration write
  set. The active verifier plan remains authority for its own migration and
  must be consulted immediately before each shared-file slice.

### Assumptions

- The accepted Router tables and routing fixtures can be projected or
  mechanically validated without creating a second routing decision table.
- Existing graph traversal is sufficient once the policy adapter supplies the
  correct groups, seeds, scopes, and applicability; a missing generic graph
  operation triggers re-planning rather than local traversal duplication.
- The canonical corpus manifest and edge-source registry can derive the full
  standards integrity closure after adding registered policy-unit, audit, and
  schema sources.
- Initial policy-unit coverage may be partial because every uncovered or
  unresolved normative change produces a mandatory whole-artifact obligation.
- Markdown, TOML, and TSV adapters can provide the required read-only
  structural scopes; unsupported finer analysis remains explicit whole-artifact
  review scope.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Product boundary | A1 contains navigation and read-only analysis only. Controlled authoring requires a later independently admitted brief and plan. | [Development brief](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#plan-a1-navigation-and-analysis) | Earlier combined A1/A2 direction |
| Module direction | `standards_engine` composes accepted lower Modules; `standards_applicability` is standard-library-only; policy-impact and analysis consume its compiled schemas and programs; analysis, verifier, and repository graph composition consume compiled policy-impact authority. | [Architecture decision](../../../decisions/standards-engine-navigation-analysis.md) | Applicability owned by analysis, verifier ownership of neutral metadata discovery, and the pre-Milestone-3 graph-manifest edge authority |
| Metadata authority | The corpus provider owns membership only; canonical documents own IDs, aliases, paths, `Requires`, and `Specializes`; neutral code only loads, validates, and projects them. | [Brief neutral metadata](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#6-neutral-metadata-module) | Suite-selection-dependent discovery and duplicate catalogs |
| Public interface | Typed requests and typed results are authoritative. Text is a derived optional rendering, not an input command language. | [Brief public interface](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#8-public-interface) | Prose command examples as interface authority |
| Snapshot binding | Canonical tool requests carry an immutable snapshot handle; every result and follow-up handle preserves it. Native Python may offer a snapshot-bound convenience view only. | [Brief navigation](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#14-navigation) | Ambient current-tree navigation |
| Policy identity | Policy-unit sidecars own stable unit ID, canonical module reference, module-relative locator, and accepted semantic revision; document path derives from canonical metadata. Policy-impact relationships originate from policy units, while modules remain navigation and document identities. | [Policy-unit source replan](reports/milestone-3-policy-unit-source-replan.md) | Paths, headings, line numbers, migration IDs, or module revisions as semantic identity |
| Proposal state | A1 carries proposed semantic state only in `AnalysisRequest.semantic_proposals`; a `CompleteResult` proves analysis completion for its exact analysis handle but is not apply-eligible. | [Brief A1 proposal state](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#a1-proposal-state) | Proposed state represented as accepted authority |
| Impact completeness | Change-type adapters select explicit seeds and the accepted/proposed relation union, then use the existing graph engine. Unmapped normative change creates a mandatory obligation. | [Brief impact contract](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#change-type-impact-contract) | Current-graph-only traversal and optional whole-artifact selection |
| Applicability | The A1 JSON Schema owns serialized shapes. `standards_applicability` owns executable operator semantics, fact contracts, compilation, normalization, type checking, truth tables, unresolved-fact reporting, reverse dependencies, and domain-separated identity. Adapters load declarations; analysis owns requirements and diagnostics. | [Applicability ownership replan](reports/milestone-3-applicability-ownership-replan.md), [fact-authority replan](reports/milestone-4-fact-authority-replan.md) | Analysis-owned evaluator, policy-impact private parsing, Boolean coercion, verifier-predicate reuse, or question authority |
| Coverage authority | Exact authority references and accepted coverage decisions in `AnalysisState` own reproducibility while `CoverageAuthorityView` contains only typed consumer-discovery dependencies. Analysis derives an exact requirement from that view; an authorized attestation approves the requirement; and a generated reusable certificate binds view, requirement, attestation, evidence, and contract digests. The state owns change-specific dispositions; `CompleteResult` projects the certificates used. | [Coverage identity replan](reports/milestone-3-coverage-identity-replan.md) | Report-dependent certificates, permanent audited flags, snapshot-bound requirement identity, and copied projection dispositions |
| Audit horizon | `audit-horizon.policy-impact-consumers` version 1 derives typed members and content fingerprints from canonical modules, policy units, registered graph providers, every registered suite and its declared repository inputs, plus the policy-impact node catalog as a supplement. Existing policy-impact declarations and nodes are not sufficient horizon authority. | [Coverage identity replan](reports/milestone-3-coverage-identity-replan.md#audit-horizon) | `policy-impact-declarations:v1` and any horizon derived only from relationships under audit |
| Completion | Analysis completion is mechanically derived from the final reached-obligation set and exact valid disposition set plus every other typed obligation. | [Brief report invariant](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#exact-completedanalysisreport-invariant) | Authored or unchecked complete flags |
| Consumer review aggregation | Applicable policy-impact traces compile into one obligation per exact `(consumer, scope, review-contract)` key. One canonical aggregate derives plural typed reasons, required evidence owners, and the decision fingerprint; unknown traces remain separate applicability work. | [Consumer-obligation recovery](reports/milestone-3-consumer-obligation-replan.md) | Singular source/reason obligations, one review per edge, or reading-plan impact reinterpretation |
| Reading-plan projection | Reading plans are derived navigation over consumer obligations, Router selections, and dependency edges. One compiler collapses exact target/scope keys, unions typed cause references, derives authority from canonical target metadata, and applies deterministic state and ordering rules without traversing policy-impact relationships. Reading-plan compilation semantics advance the analysis contract to version 2; the coordinated public/interface identities advance to interface 5, navigation 2, packet 3, and report 2. | [Milestone 4 reading-plan replan](reports/milestone-4-reading-plan-replan.md) | Singular reasons, fake routing facts, one-parent dependency provenance, or reading-plan policy-impact interpretation |
| Coverage projection for reading authority | The complete node catalog remains an `AnalysisSnapshot` input. Audit-horizon provider version 2 removes only the typed reading-only `nodes[].metadata.authority` field from that catalog's coverage fingerprint and retains every other current or future field. Horizon-affecting implementation freezes before one final reviewed attestation renewal. | [Milestone 4 horizon projection replan](reports/milestone-4-horizon-projection-replan.md) | Opaque whole-manifest coverage fingerprints, path inference, broad ignored directories, or repeated mid-slice attestation renewal |
| Analysis state and reuse | A missing canonical fact in one derived `AnalysisContext` creates one `FactRequirement`. One normalized content-addressed `AnalysisState` is the sole analysis identity; a caller supplies at most one prior analysis handle and the engine revalidates every dependency-valid decision. Pending and complete results are projections. Raw facts, hidden sessions, packet/report identities, temporal staleness, and caller-coordinated decision lists are prohibited. | [Fact-authority replan](reports/milestone-4-fact-authority-replan.md), [single-state replan](reports/milestone-4-packet-supersession-replan.md) | Raw analysis facts, hidden mutable sessions, individual observation lists, packet/report identities, mutable A1 heads, question IDs plus echoed fingerprints, relationship-specific fact-answer obligations, generic fact-answer dispositions, topology-bound fact identity, or prompt-bound reuse |
| Agent evidence | A1 acceptance requires real typed route/read and iterative prepare/resolve workflows, not schema inspection alone. | [Brief agent evidence](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#24-required-a1-agent-evidence) | Interface usability inferred from declarations |
| Canonical schema | JSON Schema Draft 2020-12 plus documented Standards Engine annotations is the sole A1 machine contract; generated Python and agent-tool projections must pass deterministic conformance. | [Architecture decision](../../../decisions/standards-engine-navigation-analysis.md) and [Milestone 0 review](reports/milestone-0-architecture-contract-review.md) | Independent Python, JSON, tool, example, identity, or renderer contracts |
| Snapshot bootstrap | A trusted source provider issues the initial opaque snapshot handle; caller operations remain explicitly handle-bound and cannot fall back to ambient current state. | [Architecture decision](../../../decisions/standards-engine-navigation-analysis.md#public-interface) | Caller repository paths or implicit current-tree lookup |
| Impact graph groups | Use `policy-impact`; add `standards-requires` and `standards-specializes` only for additions and cross-module moves. Do not select `semantic` or `standards-dependencies` for A1 impact composition. | [Architecture decision](../../../decisions/standards-engine-navigation-analysis.md#graph-composition) | Broad semantic traversal or combined dependency provenance |
| Policy-impact authority | Module-owned typed declaration files contain relationships whose sources are active policy units in that module. They compile once into neutral graph topology and typed semantics. Canonical modules, nodes, and generic groups remain independent upstream authorities. | [Policy-unit source replan](reports/milestone-3-policy-unit-source-replan.md) | Module-source edges, edge-ID semantics sidecars, and policy strings in generic graph metadata |
| Policy-unit loading | Sidecars own policy-unit facts; `standards_metadata` loads and validates them with canonical modules as one immutable corpus and produces their derived digests. `standards_graph` owns policy-unit node projection; analysis owns only change interpretation. | [Policy-unit ownership replan](reports/milestone-3-policy-unit-ownership-replan.md) | Analysis-owned sidecar parsing or metadata-to-graph dependencies |
| Policy-impact identity | The compiler derives one ID from the unique `(source, relation, consumer)` natural key and the cutover records every old-to-new mapping. | [Milestone 3 authority replan](reports/milestone-3-policy-impact-applicability-replan.md#edge-identity) | Exact authored IDs for policy-impact edges only |

Milestone 0 must select the canonical schema representation, contract-version
policy, exact source/projection mechanism, exact graph groups used by each
change-type rule, policy-unit and audit declaration schemas, authorization
context boundary, and package entry points. Those choices are not inferred from
examples in the brief.

## Simplicity And Ownership Review

- Independent concepts: canonical metadata discovery, neutral graph mechanics,
  standards-specific analysis, public façade and tool transport, and human text
  projection.
- Intentional coupling: analysis consumes immutable metadata and graph views;
  the façade composes accepted lower contracts; generated projections consume
  one schema authority.
- Accidental coupling risk: a single oversized engine, verifier-owned metadata,
  copied Router rules, parallel schema models, policy-aware graph behavior, or
  analysis projections that expose repository layout.
- Policy/state/lifecycle owners: standards documents own meaning; sidecars own
  policy-unit identity; policy-impact declarations own relations; coverage
  attestations own reviewer conclusions; schemas own transport shape; fact
  requirements, certificates, and analysis results are derived projections.
- Future changes that remain independent: evidence-oracle policy, controlled
  authoring, external project baselines, text presentation, and additional
  graph consumers do not change the A1 analysis kernel unless their accepted
  contract requires it.

## Milestones

### Milestone 0: Architecture And Canonical Schema Admission

**Goal:** Accept the durable module, authority, schema, serialization,
authorization, and impact-composition decisions before runtime implementation.

**Allowed write set:**

- `docs/decisions/standards-engine-navigation-analysis.md`
- `tools/standards_engine/contracts/**`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [x] Produce the ADR with context, selected decisions, alternatives,
  consequences, affected boundaries, and supersession links.
- [x] Select one canonical schema representation and define mechanical
  generation or validation for Python, JSON, agent tools, examples, and text
  rendering.
- [x] Define versioned canonical serialization and domain-separated identities
  for snapshots, navigation, analyses, obligations, and certificates.
- [x] Define every A1 request, result, handle, rejection, submission,
  authorization, inspection, and state-machine variant.
- [x] Select the exact named graph groups used by modification, addition,
  removal, move, split, and merge.
- [x] Define policy-unit, semantic-overlay, applicability, coverage,
  certificate, decision-fingerprint, and completion schemas; the initial audit
  declaration shape was superseded by the accepted two-identity coverage
  contract.
- [x] Validate every brief example against the accepted schema and remove any
  independent example authority.
- [x] Confirm that no write-set refinement is required. Record the exact
  implementation base in the next admission slice after this planning boundary
  is committed; a commit cannot record its own identity without a second
  authority update.

**Acceptance gate:** The ADR and canonical schemas receive recorded manual
architecture and contract review; every schema and included example parses and
validates deterministically; identity fixtures are stable; no runtime module,
production loader, or compatibility path is introduced; plan structure and
link checks pass.

**Status:** `Accepted`

### Milestone 1: Neutral Metadata And Single-Authority Cutover

**Goal:** Provide one reusable neutral metadata API and migrate every
inventoried production consumer without retaining verifier-owned or parallel
loading authority.

**Allowed write set:**

- `tools/standards_metadata/**`
- `tools/standards_verifier/pyproject.toml`
- `tools/standards_verifier/standards_verifier/canonical_modules.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/standards_verifier/checks/metadata.py`
- `tools/standards_verifier/standards_verifier/checks/metadata_route.py`
- `tools/standards_verifier/standards_verifier/policy_impact.py`
- `tools/standards_verifier/tests/test_canonical_modules.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `tools/standards_verifier/tests/test_metadata.py`
- `tools/standards_verifier/tests/test_metadata_route.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/query_edges.py`
- `evaluation/standards-effectiveness/canonical-module-corpus.toml`
- `evaluation/standards-effectiveness/edge-source-registry.toml`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [x] Inventory every canonical metadata consumer before source edits and
  record its current authority, API, diagnostics, and cutover disposition.
- [x] Implement immutable corpus, identity, alias, document-path, `Requires`,
  and `Specializes` views from canonical sources.
- [x] Compare old and new normalized membership, identities, aliases, paths,
  edges, transitive groups, ordering, and invalid-input outcomes.
- [x] Treat every unexplained difference as blocking.
- [x] Cut over all inventoried consumers coherently and delete the old neutral
  loading implementation without a wrapper or compatibility import.
- [x] Keep verifier-specific checks and diagnostics in `standards_verifier`.

**Acceptance gate:** Focused neutral-metadata tests, old/new equivalence
fixtures, verifier metadata tests, repository graph-provider tests, and
`tools/query_edges.py` integration pass; import inspection proves neutral
dependency direction; the inventory has one disposition per consumer; no
parallel production loader remains.

**Status:** `Accepted`

### Milestone 2: Snapshot-Bound Navigation

**Goal:** Deliver the first independently useful A1 behavior: an agent routes,
reads, relates, and inspects canonical standards through typed snapshot-bound
requests without repository paths.

**Allowed write set:**

- `tools/standards_metadata/**`
- `tools/standards_graph/**`
- `tools/standards_analysis/**`
- `tools/standards_engine/**`
- `tools/standards_verifier/standards_verifier/graph_adapters.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/standards_verifier/checks/metadata_route.py`
- `tools/standards_verifier/tests/test_metadata.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `STANDARDS-ROUTER.md`
- `evaluation/standards-effectiveness/fixtures/routing/**`
- `evaluation/standards-effectiveness/router-projection.toml`
- `evaluation/standards-effectiveness/suites/s1-routing.toml`
- `evaluation/standards-effectiveness/policy-units/**`
- `evaluation/standards-effectiveness/canonical-module-corpus.toml`
- `evaluation/standards-effectiveness/edge-source-registry.toml`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [x] Build clean-Git and dirty/non-Git snapshots with exact scope,
  tracked/untracked files, exclusions, modes, symlink targets, submodules, and
  relevant contract/tool versions.
- [x] Implement accepted canonical serialization and immutable snapshot,
  navigation, policy, relationship, and inspection handles.
- [x] Validate policy-unit identity, module-relative locators, accepted and
  proposed semantic revisions, moves, splits, merges, retirement, successors,
  aliases, and tombstones.
- [x] Generate or mechanically validate executable Router projection from
  Router-owned authority and existing typed fixtures.
- [x] Before any normative Router edit, query its `policy-impact` consumers and
  record exact change-specific dispositions; do not edit the Router merely to
  simplify projection.
- [x] Implement snapshot-bound `query` variants for route, read, related, and
  provenance inspection with typed rejection outcomes.
- [x] Return `Requires` and `Specializes` closure through their existing named
  graph groups without redefining traversal.
- [x] Exercise the complete route to canonical ID to read interaction through
  the real typed tool adapter.

**Acceptance gate:** Snapshot and policy-unit contract fixtures pass; Router
projection matches every accepted positive, negative, and unresolved routing
fixture; route/read/related agent evidence proves same-snapshot continuity and
cross-snapshot rejection; no result requires a repository path or text parsing;
affected security, containment, filesystem, contract, and documentation checks
pass.

**Status:** `Accepted`

### Milestone 3: Semantic Impact Selection And Coverage

**Goal:** Deterministically compile accepted/proposed changes into complete
impact candidates, applicability state, audit coverage, and typed obligations
without claiming to judge arbitrary meaning.

**Allowed write set:**

- `tools/standards_metadata/**`
- `tools/standards_applicability/**`
- `tools/standards_policy_impact/**`
- `tools/standards_graph/**`
- `tools/standards_analysis/**`
- `tools/standards_engine/**`
- `tools/standards_verifier/standards_verifier/policy_impact.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/standards_verifier/checks/policy_impact.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `tools/graph_engine/README.md`
- `.gitignore`
- `evaluation/standards-effectiveness/policy-impact-*.toml`
- `evaluation/standards-effectiveness/policy-impact/**`
- `evaluation/standards-effectiveness/policy-semantic-impact.toml`
- `evaluation/standards-effectiveness/policy-consumer-audits.toml`
- `evaluation/standards-effectiveness/policy-coverage/**`
- `evaluation/standards-effectiveness/policy-units/**`
- `evaluation/standards-effectiveness/edge-source-registry.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/**`
- `evaluation/standards-effectiveness/fixtures/standards-engine/**`
- `evaluation/standards-effectiveness/suites/policy-semantic-impact.toml`
- `docs/decisions/standards-engine-navigation-analysis.md`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [x] Implement deterministic change classification and the accepted seed and
  obligation rules for modification, addition, and removal.
- [x] Implement deterministic change classification and the accepted seed and
  obligation rules for move, split, and merge.
- [x] Traverse the union of accepted and proposed selected graph groups and
  retain exact traces and provenance.
- [x] Compile source-owned typed policy-impact declarations into one neutral
  graph contribution and one semantics index without replacing node or group
  authority.
- [x] Cut repository graph composition, analysis, verifier validation, and
  Standards Engine inspection to the compiled authority and remove the old
  edge blocks and string metadata without fallback.
- [x] Inventory every legacy module-source relationship and record a semantic
  one-to-one or one-to-many policy-unit source disposition without treating 39
  as the replacement edge count.
- [x] Define and review the Planning and Commit heading-scoped policy-unit
  baseline, including accepted semantic revision 1 and exact locator evidence.
- [x] Move policy-unit models, sidecar loading, locator/lifecycle validation,
  digest production, and focused tests to `standards_metadata`; move graph-only
  projection to `standards_graph`; remove the analysis-owned loader without a
  compatibility re-export.
- [x] Cut declarations, compiler validation, graph contribution, inspection,
  verifier consumers, and module-level related aggregation to policy-unit
  sources atomically; remove module-source support without fallback.
- [x] Generate mandatory `unmapped-normative-change` obligations for uncovered
  or unresolved normative changes.
- [x] Implement neutral compiled fact schemas, applicability programs, and fact
  sets with typed errors, schema identity checks, deterministic digests, exact
  unresolved facts, empty-schema `always`, aliases, nullable and absent states,
  and documented three-valued truth tables.
- [x] Compile Router and policy-impact declarations through the neutral Module;
  make analysis and verifier consume the same programs, mechanically prove A1
  schema/runtime agreement, and delete both former applicability parsers and
  re-exports without fallback.
- [x] Implement complete `AnalysisSnapshot` and narrower
  `CoverageAuthorityView` identities, with typed-role projection and exact
  semantic, relationship, applicability, horizon-member, authorization,
  evidence-provider, and identity-resolution dependencies.
- [x] Register `audit-horizon.policy-impact-consumers` version 1 over canonical
  modules, policy units, graph-source registrations, registered suites and
  their declared repository inputs, and supplemental policy-impact nodes;
  fingerprint every member's relevant content rather than IDs alone.
- [x] Implement derived coverage requirements whose identity excludes their
  source snapshot, authored attestations whose identity derives from canonical
  content, deterministic reusable certificates, and exact invalidation
  independent from report dispositions or accepted/proposed labels.
- [x] Remove the legacy audit catalog, compiler audit matching,
  `audit_declaration` semantics, `audited_owners`, old verifier loading, and
  module-level audit authority in the same cutover without fallback.
- [x] Keep applicability unknown during conservative whole-artifact selection.
- [x] Prove that missing or expired audit coverage cannot return successful
  empty impact.
- [x] Convert every definitely applicable policy-impact selection into one
  consumer-review obligation per exact consumer, scope, and review-contract
  key, retaining all selecting sources, traces, facts, and evidence owners.
- [x] Replace singular obligation provenance and v1 obligation/packet
  identities atomically across schema, runtime types, examples, fixtures, and
  verification without compatibility interpretation.

**Acceptance gate:** Focused policy-unit, impact, applicability, audit, and
certificate tests cover every required positive, negative, unknown, stale, and
invalid outcome; modification/addition/removal pilot selection and
move/split/merge fixtures select exact expected identities, groups, scopes, and
obligations; graph-engine tests remain unchanged and pass.

**Status:** `Accepted` through the superseding
[consumer-obligation recovery](reports/milestone-3-consumer-obligation-recovery.md)

### Milestone 4: Analysis Resolution And A1 Acceptance

**Goal:** Expose the complete A1 workflow through one immutable analysis state,
iterative pure transitions, reading plans, decision reuse, typed agent tools,
and optional text rendering, then accept the objective from one exact
repository state.

**Allowed write set:**

- `tools/standards_analysis/**`
- `tools/standards_applicability/**`
- `tools/standards_policy_impact/**`
- `tools/standards_engine/**`
- `tools/standards_metadata/standards_metadata/serialization.py`
- `tools/standards_metadata/tests/test_metadata.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `evaluation/standards-effectiveness/router-projection.toml`
- `evaluation/standards-effectiveness/policy-impact-facts.toml`
- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-coverage/horizons.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`
- `evaluation/standards-effectiveness/fixtures/standards-engine/**`
- `evaluation/standards-effectiveness/suites/standards-engine-navigation-analysis.toml`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/check-plan-structure.sh`
- `evaluation/standards-effectiveness/verify-plan-fixtures.sh`
- `evaluation/standards-effectiveness/fixtures/plans/**`
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-nodes.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-edges.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-components.tsv`
- `docs/decisions/standards-engine-navigation-analysis.md`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [x] Implement stable obligation identities, typed questions and submissions,
  required evidence, and state-derived next operations.
- [x] Replace the opaque node-catalog horizon fingerprint with the typed
  provider-v2 coverage projection; keep the complete catalog in snapshot
  closure and prove reading-only authority changes do not alter coverage.
- [x] Implement the typed plural-cause reading-plan compiler, explicit
  canonical target authority, exact target/scope collapse, deterministic state
  and ordering, complete Router and dependency provenance, and consumer entries
  derived only from authoritative obligations.
- [x] Freeze every horizon-affecting input, record the 27 node dispositions and
  unchanged topology/compiled semantics, generate the exact 28 requirements,
  and renew Planning and Commit attestations once with authorized audit
  evidence as the final authority step.
- [x] Replace `FactDefinition` with semantic `FactContract` authority while
  keeping aliases and prompts outside decision identity; compile a reverse
  fact-to-program dependency index.
- [x] Derive one content-addressed standards-change `AnalysisContext`, one
  `FactRequirement` per missing canonical fact/context, and typed
  `FactObservation` records bound to exact evidence and authorization.
- [x] Remove actionable applicability questions, relationship-specific
  fact-answer obligations, and generic fact-answer dispositions; pending
  impacts reference requirements and are reevaluated through reverse fact
  dependencies.
- [x] Replace packet, report, and state identity with one immutable normalized
  `AnalysisState` and `AnalysisHandle`; store only authority inputs and
  dependency-valid accepted decisions; derive pending and complete results.
- [x] Bind exact authorization-authority and provider-contract/input views;
  prohibit ambient provider inputs and distinguish deterministic no-observation
  from provider or evidence unavailability.
- [x] Remove global supersession, packet/report stores, and temporal A1
  staleness; make repeated transitions idempotent and different valid
  submissions natural independent child states.
- [x] Add typed deterministic provider claims while keeping canonical
  observation construction, evidence-contract validation, provider-contract
  validation, and authorization validation inside analysis.
- [x] Make only requirements material to the final fixed point completion
  blocking; retain dormant-valid observations and dispositions while excluding
  derived requirement history from state authority.
- [x] Freeze the resulting horizon after every fact-contract, schema, registry,
  and test input is final; prove the existing 28-subject attestations remain
  valid because no coverage-authority input changed.
- [x] Derive `CompleteResult` only from exact final reached/disposition
  and fact-requirement/observation set equality and resolution of every
  non-consumer obligation, applicability, authorization, evidence, and audit
  condition.
- [x] Return `CompleteResult` directly when preparation produces no
  outstanding obligation.
- [x] Implement tagged inspection results and keep programming defects as
  exceptions rather than domain rejections.
- [x] Generate or validate Python, JSON, agent-tool, documentation, and renderer
  projections from the accepted schema; make drift fail verification.
- [x] Implement deterministic compact text rendering from typed results only.
- [x] Run complete typed-agent modification, addition, and removal workflows,
  including iterative obligation expansion and negative disposition cases.
- [x] Run move, split, and merge behavioral fixtures before claiming their
  contracts complete.
- [x] Record final objective evidence, exact commit and tree, and any deferred
  findings with owners and triggers.

**Acceptance gate:** Every objective acceptance row has matching evidence; the
real typed tool adapter passes route/read and full prepare/resolve workflows;
missing, duplicate, extra, stale, unresolved, blocked, unaudited, unauthorized,
and cross-snapshot cases fail with the required typed result; schema drift,
serialization, package, verifier, graph, declarative, freshness, link, and plan
checks pass from one clean recorded tree.

**Status:** `Accepted` through the
[A1 final acceptance](reports/a1-final-acceptance.md); the earlier
[A1 boundary repair acceptance](reports/a1-boundary-repair-acceptance.md) and
[single-state acceptance](reports/milestone-4-single-state-acceptance.md) remain
withdrawn historical boundaries

## Blockers

Milestone 3's missing consumer-obligation generator was resolved by the
superseding recovery acceptance. The coverage identity cycle and inadequate
declaration-only horizon were resolved by the accepted two-identity coverage
direction and independent registered horizon. Ambiguous typed projection,
missing independent corpus authority, failed attestation bootstrap review,
ambiguous evidence or authorization resolution, or need to change another
graph authority remains a re-plan trigger rather than an implicit blocker.

No active issue blocks Plan A1 acceptance. SENA-022 was resolved by the
independently accepted Repair VI boundary. The single-state model remains
accepted and no packet/report compatibility runtime exists. Controlled
authoring, evidence-oracle policy, and external project baselines remain
blocked behind their separately admitted future plans.

## Re-Plan Triggers

- The ADR or schema review rejects a brief contract or changes the module,
  authority, identity, or public-interface boundary.
- Metadata consumer inventory finds an owner or production loader outside the
  Milestone 1 write set.
- Old/new metadata comparison produces an unexplained semantic or diagnostic
  difference.
- Router authority cannot be projected mechanically without a new normative
  representation or second decision table.
- The generic graph lacks a required repository-neutral operation and adding
  it would change the accepted graph contract.
- Snapshot, filesystem, symlink, submodule, or supported-platform facts cannot
  satisfy the selected identity and containment contract.
- Policy-unit or audit coverage requires duplicate canonical paths, module
  metadata, dispositions, or graph authority.
- A1 requires semantic judgment, canonical mutation, application eligibility,
  external project state, or evidence-oracle policy to satisfy its objective.
- A new latency, resource, caching, or optimization claim selects Performance.
- A third-party dependency becomes necessary.
- The active verifier migration admits an overlapping shared-file slice or
  changes metadata, registry, graph-provider, or generated-evidence contracts.
- Multiple outstanding A1 or shared-authority proposals make current-state
  integration facts stale and select Concurrent Plan Integration.
- A milestone misses its named acceptance gate or lower-fidelity evidence is
  being used for an objective claim.

## Concurrent Work

No concurrent A1 implementation is admitted. Package-local work may be
delegated only when the accepted ADR and current plan identify non-overlapping
primary write sets; schemas, registries, canonical metadata, active plans, and
generated artifacts remain serial integration-owner writes.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: controlled authoring, Plan B evidence-oracle recovery,
  and Plan C external project baselines remain outside A1 with their brief-owned
  prerequisites.
- Final status: `Accepted`
