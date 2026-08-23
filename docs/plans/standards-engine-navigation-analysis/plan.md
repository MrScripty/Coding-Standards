# Plan: Standards Engine Navigation And Analysis

**Plan status:** `Active`

**Current phase:** Milestone 4 packets, agent resolution, and A1 acceptance

**Next slice:** implement immutable packets, stable obligation identities,
typed questions and submissions, required evidence, and state-derived next
operations

**Acceptance status:** `pending`

**Recovery boundary:** commit
`13a9f48b95ed7532f480e4604d9dfa23443e8f43`, tree
`c27a1e2bbf52244c5b30eb1d21381be6e5c86d68`

**Implementation base:** commit
`c7d23dfa55a9558b929e6b838d7ea0563981a1ef`, tree
`5e9c4eb211ee0a67039b0ec11142db9b106243ae`

**Implementation admission:** operation `continue` accepted for Milestone 3
from the recorded implementation base and the accepted Milestone 3 replans
through the coverage-identity cutover; implementation remains bounded by
Milestone 3's write set

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Development brief:**
[Standards Engine Navigation and Analysis](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md)

## Objective

Provide one agent-facing, typed Standards Engine that lets a caller discover,
retrieve, and navigate canonical standards without repository paths, then
compare supplied accepted and proposed standards snapshots and resolve every
deterministically selected impact obligation into a complete read-only analysis
report. The engine must expose uncertainty and authority explicitly, preserve
one source for canonical metadata and schemas, and leave semantic acceptance,
repository mutation, and external-project application outside A1.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Every canonical corpus member, module ID, alias, document path, `Requires` edge, and `Specializes` edge is loaded through one neutral metadata API, and every inventoried consumer uses that API without a parallel production loader. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 acceptance](reports/milestone-1-neutral-metadata-cutover.md) |
| A2 | Clean Git, dirty/non-Git, untracked-file, file-mode, symlink, submodule, exclusion, schema, tool-version, and integrity-closure inputs produce deterministic immutable snapshot identities under the accepted serialization contract. | `contract` | `not-applicable` | `automated` | `pending` | Milestone 2 evidence |
| A3 | A typed agent can route from structured facts, receive canonical IDs, read canonical content, and navigate declared relations through follow-up requests bound to the same immutable snapshot without supplying repository paths. | `user-workflow` | `not-applicable` | `automated` | `pending` | Route/read agent fixture |
| A4 | Policy-unit identity, accepted and proposed semantic state, move, split, merge, retirement, successor, alias, and unmapped normative-change rules preserve identity and produce the required typed outcomes without treating structure as semantic proof. | `contract` | `not-applicable` | `automated` | `pending` | Milestones 2 and 3 evidence |
| A5 | Modification, addition, removal, move, split, and merge select deterministic seeds, traverse the accepted/proposed relation union through the existing graph engine, retain unknown applicability, and generate every required scoped obligation. | `integration` | `not-applicable` | `automated` | `pending` | Impact fixtures |
| A6 | Derived coverage requirements plus authorized attestations generate deterministic reusable certificates, reject stale or unaudited coverage, and never infer successful empty impact from absent edges or convert unknown applicability into true. | `contract` | `not-applicable` | `automated` | Coverage and applicability fixtures |
| A7 | `prepare` and iterative `resolve` return a `CompletedAnalysisReport` only when the final reached consumer-obligation IDs exactly equal the valid current disposition IDs and every other required question, obligation, authorization, and coverage condition is resolved. | `integration` | `not-applicable` | `automated` | Full prepare/resolve fixtures |
| A8 | One canonical interface schema mechanically governs Python types, JSON validation, agent-tool definitions, examples, identity-bearing serialization, result variants, derived `next_operations`, and text rendering; projection drift fails verification. | `contract` | `not-applicable` | `automated` | Schema conformance suite |
| A9 | Representative modification, addition, and removal changes complete through the real typed agent adapter; move, split, and merge behavioral fixtures pass; focused package tests and affected broad repository verification pass from one recorded clean tree. | `user-workflow` | `not-applicable` | `automated` | Final A1 acceptance report |

## Scope

### In Scope

- A neutral `tools/standards_metadata/` package for canonical corpus and module
  metadata access.
- A `tools/standards_analysis/` package for snapshot comparison, policy-unit
  impact, applicability, audit coverage, packets, reading plans, and decision
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
  attestation therefore stales the old packet without changing the requirement
  it answers.
- Consumer coverage is bounded by a mechanically derived requirement, an
  authorized attestation, and a generated certificate over an independent
  registered audit horizon. Coverage certificates never own change-specific
  dispositions. An unaudited empty edge result is not success.
- Coverage projection exclusions are based on typed artifact roles, never an
  ignored directory. Attestations, their source registrations, certificates,
  packets, reports, timestamps, summaries, and dispositions do not enter the
  coverage view; relationship authority cannot escape projection by location.
- Coverage identity binds the target semantic payload and relationship state,
  not the transient `proposed` or `accepted` label. Promotion of identical
  reviewed content and relationships preserves applicable coverage.
- `CompletedAnalysisReport.complete` is derived from exact obligation,
  disposition, question, authorization, evidence, and coverage invariants.
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
| Module direction | `standards_engine` composes accepted lower Modules; `standards_applicability` is standard-library-only; policy-impact and analysis consume its compiled schemas and programs; analysis, verifier, and repository graph composition consume compiled policy-impact authority. | [Architecture decision](../../decisions/standards-engine-navigation-analysis.md) | Applicability owned by analysis, verifier ownership of neutral metadata discovery, and the pre-Milestone-3 graph-manifest edge authority |
| Metadata authority | The corpus provider owns membership only; canonical documents own IDs, aliases, paths, `Requires`, and `Specializes`; neutral code only loads, validates, and projects them. | [Brief neutral metadata](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#6-neutral-metadata-module) | Suite-selection-dependent discovery and duplicate catalogs |
| Public interface | Typed requests and typed results are authoritative. Text is a derived optional rendering, not an input command language. | [Brief public interface](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#8-public-interface) | Prose command examples as interface authority |
| Snapshot binding | Canonical tool requests carry an immutable snapshot handle; every result and follow-up handle preserves it. Native Python may offer a snapshot-bound convenience view only. | [Brief navigation](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#14-navigation) | Ambient current-tree navigation |
| Policy identity | Policy-unit sidecars own stable unit ID, canonical module reference, module-relative locator, and accepted semantic revision; document path derives from canonical metadata. Policy-impact relationships originate from policy units, while modules remain navigation and document identities. | [Policy-unit source replan](reports/milestone-3-policy-unit-source-replan.md) | Paths, headings, line numbers, migration IDs, or module revisions as semantic identity |
| Proposal state | A1 carries proposed semantic state only in `AnalysisRequest.semantic_proposals`; `CompletedAnalysisReport` proves analysis completion but is not apply-eligible. | [Brief A1 proposal state](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#a1-proposal-state) | Proposed state represented as accepted authority |
| Impact completeness | Change-type adapters select explicit seeds and the accepted/proposed relation union, then use the existing graph engine. Unmapped normative change creates a mandatory obligation. | [Brief impact contract](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#change-type-impact-contract) | Current-graph-only traversal and optional whole-artifact selection |
| Applicability | The A1 JSON Schema owns serialized shapes. `standards_applicability` owns executable operator semantics, compilation, normalization, type checking, truth tables, unresolved-fact reporting, and domain-separated program identity. Adapters load declarations; callers own questions and diagnostics. | [Applicability ownership replan](reports/milestone-3-applicability-ownership-replan.md) | Analysis-owned evaluator, policy-impact private parsing, Boolean coercion, or verifier-predicate reuse |
| Coverage authority | `AnalysisSnapshot` owns complete reproducibility while `CoverageAuthorityView` contains only typed consumer-discovery dependencies. Analysis derives an exact requirement from that view; an authorized attestation approves the requirement; and a generated reusable certificate binds view, requirement, attestation, evidence, and contract digests. Reports alone own change-specific dispositions and reference the certificates they used. | [Coverage identity replan](reports/milestone-3-coverage-identity-replan.md) | Report-dependent certificates, permanent audited flags, snapshot-bound requirement identity, and copied packet dispositions |
| Audit horizon | `audit-horizon.policy-impact-consumers` version 1 derives typed members and content fingerprints from canonical modules, policy units, registered graph providers, every registered suite and its declared repository inputs, plus the policy-impact node catalog as a supplement. Existing policy-impact declarations and nodes are not sufficient horizon authority. | [Coverage identity replan](reports/milestone-3-coverage-identity-replan.md#audit-horizon) | `policy-impact-declarations:v1` and any horizon derived only from relationships under audit |
| Completion | Analysis completion is mechanically derived from the final reached-obligation set and exact valid disposition set plus every other typed obligation. | [Brief report invariant](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#exact-completedanalysisreport-invariant) | Authored or unchecked complete flags |
| Agent evidence | A1 acceptance requires real typed route/read and iterative prepare/resolve workflows, not schema inspection alone. | [Brief agent evidence](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md#24-required-a1-agent-evidence) | Interface usability inferred from declarations |
| Canonical schema | JSON Schema Draft 2020-12 plus documented Standards Engine annotations is the sole A1 machine contract; generated Python and agent-tool projections must pass deterministic conformance. | [Architecture decision](../../decisions/standards-engine-navigation-analysis.md) and [Milestone 0 review](reports/milestone-0-architecture-contract-review.md) | Independent Python, JSON, tool, example, identity, or renderer contracts |
| Snapshot bootstrap | A trusted source provider issues the initial opaque snapshot handle; caller operations remain explicitly handle-bound and cannot fall back to ambient current state. | [Architecture decision](../../decisions/standards-engine-navigation-analysis.md#public-interface) | Caller repository paths or implicit current-tree lookup |
| Impact graph groups | Use `policy-impact`; add `standards-requires` and `standards-specializes` only for additions and cross-module moves. Do not select `semantic` or `standards-dependencies` for A1 impact composition. | [Architecture decision](../../decisions/standards-engine-navigation-analysis.md#graph-composition) | Broad semantic traversal or combined dependency provenance |
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
  packets that expose repository layout.
- Policy/state/lifecycle owners: standards documents own meaning; sidecars own
  policy-unit identity; policy-impact declarations own relations; coverage
  attestations own reviewer conclusions; schemas own transport shape; packets,
  requirements, certificates, and reports are immutable derived artifacts.
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
  for snapshots, navigation, packets, obligations, reports, and certificates.
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

**Acceptance gate:** Focused policy-unit, impact, applicability, audit, and
certificate tests cover every required positive, negative, unknown, stale, and
invalid outcome; modification/addition/removal pilot selection and
move/split/merge fixtures select exact expected identities, groups, scopes, and
obligations; graph-engine tests remain unchanged and pass.

**Status:** `Accepted`

### Milestone 4: Packets, Agent Resolution, And A1 Acceptance

**Goal:** Expose the complete A1 workflow through immutable packets, iterative
resolution, reading plans, decision reuse, typed agent tools, and optional text
rendering, then accept the objective from one exact repository state.

**Allowed write set:**

- `tools/standards_analysis/**`
- `tools/standards_engine/**`
- `evaluation/standards-effectiveness/fixtures/standards-engine/**`
- `evaluation/standards-effectiveness/suites/standards-engine-navigation-analysis.toml`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `docs/plans/standards-engine-navigation-analysis/**`

**Tasks:**

- [ ] Implement immutable packets, stable obligation identities, typed
  questions and submissions, required evidence, and state-derived next
  operations.
- [ ] Implement bounded reading plans with deterministic dependency and scope
  ordering.
- [ ] Implement packet staleness and decision reuse from exact narrower
  dependency fingerprints.
- [ ] Derive `CompletedAnalysisReport` only from exact final reached/disposition
  set equality and resolution of every non-consumer obligation, question,
  authorization, evidence, and audit condition.
- [ ] Return `CompletedAnalysisReport` directly when preparation produces no
  outstanding obligation.
- [ ] Implement tagged inspection results and keep programming defects as
  exceptions rather than domain rejections.
- [ ] Generate or validate Python, JSON, agent-tool, documentation, and renderer
  projections from the accepted schema; make drift fail verification.
- [ ] Implement deterministic compact text rendering from typed results only.
- [ ] Run complete typed-agent modification, addition, and removal workflows,
  including iterative obligation expansion and negative disposition cases.
- [ ] Run move, split, and merge behavioral fixtures before claiming their
  contracts complete.
- [ ] Record final objective evidence, exact commit and tree, and any deferred
  findings with owners and triggers.

**Acceptance gate:** Every objective acceptance row has matching evidence; the
real typed tool adapter passes route/read and full prepare/resolve workflows;
missing, duplicate, extra, stale, unresolved, blocked, unaudited, unauthorized,
and cross-snapshot cases fail with the required typed result; schema drift,
serialization, package, verifier, graph, declarative, freshness, link, and plan
checks pass from one clean recorded tree.

**Status:** `Active`

## Blockers

No current blocker is accepted. The coverage identity cycle and inadequate
declaration-only horizon were resolved by the accepted two-identity coverage
direction and independent registered horizon. Ambiguous typed projection,
missing independent corpus authority, failed attestation bootstrap review,
ambiguous evidence or authorization resolution, or need to change another
graph authority remains a re-plan trigger rather than an implicit blocker.

Runtime implementation is admitted from the recorded implementation base and
remains bounded by the active milestone, exact next slice, allowed write set,
and serial shared-authority checks. A newly admitted overlapping verifier or
shared-authority proposal triggers re-planning before further source edits.

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

- Acceptance status: `pending`
- Deferred follow-ups: controlled authoring, Plan B evidence-oracle recovery,
  and Plan C external project baselines remain outside A1 with their brief-owned
  prerequisites.
- Final status: `Active`
