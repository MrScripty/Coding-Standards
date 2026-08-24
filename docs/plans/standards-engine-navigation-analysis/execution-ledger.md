# Standards Engine Navigation And Analysis Execution Ledger

## 2026-08-23: Milestone 4 Immutable Packet Foundation

- Added one analysis-owned packet Module over already-derived changes,
  obligations, questions, and reading entries. It performs no repository
  loading, graph traversal, or verifier execution.
- Packet identity follows the canonical schema projection exactly: complete
  base/proposed snapshot handles and semantic work enter identity, while
  summaries, derived next operations, and implementation-only versions do not.
- Added typed fact-answer, consumer-disposition, impact-disposition, and
  coverage-attestation submissions. Review submissions require immutable,
  unique evidence references; their semantic validity remains for iterative
  resolution.
- Next operations derive only from required questions and obligations. Resolved
  or blocked work cannot advertise a resolution operation, and duplicate work
  identities fail packet construction.
- Verification passed 64 analysis tests, 15 Standards Engine tests, 17 metadata
  tests, 7 policy-impact tests, 35 graph tests, 380 verifier tests, the public
  contract validator, all 218 declarative suites, and `git diff --check`.
- The sole next slice is bounded reading-plan construction and deterministic
  dependency/scope ordering.

## 2026-08-23: Milestone 3 Lifecycle Impact Selection

- Implemented move, split, and merge as distinct lifecycle classifications
  rather than approximating them as additions, removals, or modifications.
- A move preserves canonical identity and accepted semantic revision. Same-module
  moves select policy impact; cross-module moves additionally select the old
  and new module dependency context.
- A split requires one exact predecessor tombstone and at least two new
  revision-1 successors with reciprocal lifecycle declarations. A merge
  requires the corresponding exact many-to-one lifecycle authority.
- Accepted predecessors and proposed successors are independent generic-graph
  seeds whose traversals are unioned deterministically. Tests prove every old
  and new policy-impact relationship remains visible.
- Focused package, contract, verifier, and all 218 declarative suites passed.
  The complete mixed checkpoint is recorded in the
  [Milestone 3 acceptance](reports/milestone-3-lifecycle-impact-selection.md).
- Milestone 3 is accepted. Milestone 4 becomes current with one next slice:
  immutable packets, stable obligation identities, typed submissions and
  questions, required evidence, and state-derived next operations.

## 2026-08-23: Milestone 3 Empty-Impact Coverage Gate

- Added a deterministic coverage-work projection over changed target policy
  authority: proposed subjects for additions and surviving changes, and
  accepted subjects for removals.
- A changed policy without a certificate for its exact current requirement now
  produces one mandatory fingerprinted `audit-coverage` obligation, even when
  its compiled relationship set and impact candidate set are empty.
- A current generated certificate removes the obligation. Existing stale
  attestation validation remains fail-closed when policy relationships or an
  independently fingerprinted horizon member changes.
- The obligation uses the accepted public `Obligation` and `DecisionContract`
  shapes and permits only `coverage-attestation` submissions.
- Acceptance evidence is recorded in the
  [empty-impact coverage report](reports/milestone-3-empty-impact-coverage.md).

## 2026-08-23: Milestone 3 Unknown Applicability Resolution

- Impact selection now evaluates the accepted and proposed trace union through
  the immutable programs compiled by `standards_applicability`; analysis does
  not parse expressions or implement another truth table.
- Equal accepted/proposed fact schemas share one bound fact set. A differing
  schema is the explicit `IMPACT.FACT_SCHEMA_EVOLUTION_UNSUPPORTED` outcome,
  and an incompatible fact set is rejected.
- Trace applicability is retained independently and candidate applicability is
  a three-valued union. A definitely applicable trace dominates; otherwise an
  unknown trace remains unknown rather than becoming selected or excluded.
- Unknown candidates receive conservative whole-artifact scope, one deduplicated
  typed question per material unresolved fact, and one fingerprinted
  `applicability-resolution` obligation per relationship and fact.
- Acceptance evidence is recorded in the
  [unknown applicability report](reports/milestone-3-unknown-applicability.md).

## 2026-08-23: Milestone 3 Unmapped Normative Obligations

- Added a metadata-owned projection that removes exact, non-overlapping active
  policy-unit heading scopes and fingerprints the remaining module
  representation without exposing line-based identity.
- Analysis now emits one deterministic mandatory whole-artifact obligation for
  changed normative authority outside policy-unit scopes, added or removed
  normative modules, and changed policy units omitted from the classified
  change set.
- Explicit canonical `reference` modules remain non-normative and do not
  produce these obligations. Analysis does not infer normative meaning from
  prose or search copied policy content.
- The obligation uses the accepted public `Obligation` and
  `DecisionFingerprint` schemas, with one typed decision contract declaring
  representation, module-locator, policy-unit, and analysis-contract
  dependencies.
- Acceptance evidence is recorded in the
  [unmapped normative report](reports/milestone-3-unmapped-normative-obligations.md).

## 2026-08-23: Milestone 3 Coverage Identity Cutover

- Added a complete snapshot input closure for coverage authority,
  attestations, exclusions, and evidence while deriving reusable
  `CoverageAuthorityView` identities from consumer-discovery inputs only.
- Registered an independent 856-member consumer horizon over canonical
  standards, graph providers, registered suites, declared suite inputs, and
  supplemental policy-impact nodes. Every member carries a content or semantic
  fingerprint.
- Bootstrapped 28 reviewed Planning and Commit policy-unit attestations and
  generated 28 current certificates. Verification remains deliberately
  uncovered and therefore cannot return a successful empty result.
- Removed the legacy module audit catalog, compiler matching, graph semantics,
  inspection field, verifier flags, fixture requirements, and public schema
  shapes without fallback. Structural relationship diagnostics run before the
  downstream coverage gate.
- Narrowed relationship invalidation: each view binds its subject's outgoing
  relationship fingerprints and the compiler provider contract, not unrelated
  relationship instances or declaration storage paths.
- Acceptance evidence is recorded in the
  [coverage cutover report](reports/milestone-3-coverage-identity-cutover.md).

## 2026-08-23: Milestone 3 Coverage Identity Replan

- Coverage implementation exposed a repository-local identity cycle: an
  attestation changes the complete analysis snapshot whose requirement it
  answers. Binding the requirement directly to that snapshot would invalidate
  every newly committed attestation.
- Accepted two distinct identities. `AnalysisSnapshot` binds all analysis
  inputs and stales packets after an attestation commit;
  `CoverageAuthorityView` excludes attestations and other downstream artifacts
  by typed role while binding every consumer-discovery dependency.
- Rejected the legacy `policy-impact-declarations:v1` horizon because it can
  inspect only declared relationships. The replacement provider derives
  content-fingerprinted members from canonical corpora, graph registrations,
  registered suites, and their declared repository inputs, with the node
  catalog only as a supplement.
- The active next slice atomically replaces legacy audit catalogs, compiler
  matching, verifier flags, and schema shapes with requirements, attestations,
  reusable certificates, and exact completion evidence. Detailed authority and
  cutover decisions are in the
  [coverage identity replan](reports/milestone-3-coverage-identity-replan.md).

## 2026-08-23: Milestone 3 Policy-Unit Authority Cutover

- Loaded canonical modules and policy-unit sidecars through one immutable
  `CanonicalStandardsCorpus`; moved neutral failures and digest production to
  `standards_metadata` and graph-only node projection to `standards_graph`.
- Replaced 39 module-source inventory rows with 126 reviewed policy-unit
  relationships from 28 accepted Planning and Commit units. The compiler now
  rejects module, alias, retired, cross-owner, and unknown sources.
- Module navigation aggregates exact contained-unit edges without creating
  module-source policy authority. Exact policy-unit navigation remains exact,
  and modules with no mapped units expose incomplete mapping.
- Removed the analysis-owned loader and graph adapter without re-export,
  fallback, or parallel parser. Verifier and repository composition reuse the
  same snapshot-bound corpus and compiled relationship set.
- Acceptance evidence is recorded in the
  [cutover report](reports/milestone-3-policy-unit-source-cutover.md).

## 2026-08-23: Milestone 3 Policy-Unit Ownership Replan

- The admitted policy-unit source cutover exposed a real dependency cycle:
  policy-unit loading lived in analysis, while policy impact must now validate
  those sources and analysis already consumes policy impact.
- Accepted the [ownership replan](reports/milestone-3-policy-unit-ownership-replan.md):
  sidecars retain authority; `standards_metadata` loads and validates one
  immutable module and policy-unit corpus; `standards_graph` owns node
  projection; analysis retains comparison and impact behavior.
- A separate `standards_policy_units` package and an analysis-owned injected
  index were rejected as unnecessary surface or inverted semantic ownership.
- The ownership move is part of the same atomic source cutover and retains no
  old loader, re-export, fallback, or second parser.

## 2026-08-23: Milestone 3 Policy-Unit Source Replan

- Coverage design review separated reusable consumer-discovery coverage from
  change-specific disposition closure and removed the report/certificate
  identity cycle from the binding direction.
- Inspection found that every current policy-impact relationship originates
  from `workflow.planning` or `workflow.commit`, while accepted semantic
  revisions belong only to policy units. Module revisions and optional semantic
  revisions were rejected as competing or weakened authority.
- The [policy-unit source replan](reports/milestone-3-policy-unit-source-replan.md)
  makes policy units semantic relationship sources while modules remain
  navigation, document, and dependency identities.
- The [39-row mapping](reports/policy-impact-source-mapping.tsv) gives every
  legacy relationship one reviewed `mapped` or `split` disposition and uses
  existing non-overlapping level-two headings. The legacy count is an inventory
  baseline, not a replacement acceptance constant.
- The [28-unit baseline](reports/policy-unit-baseline.tsv) records exact
  existing heading locators and accepts semantic revision 1 only for the
  reviewed identity, content scope, and relationship mapping. No locator
  extension or canonical policy-text correction is required.
- No production declaration, compiler, graph, schema, verifier, or generated
  artifact changed during this planning slice.

## 2026-08-22: Plan Construction

- Planning evidence: the
  [development brief](../standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md)
  was independently reviewed and refined to separate A1 navigation and
  read-only analysis from controlled authoring, evidence-oracle recovery, and
  external project baselines.
- Recovery prerequisite: accepted commit
  `13a9f48b95ed7532f480e4604d9dfa23443e8f43`, tree
  `c27a1e2bbf52244c5b30eb1d21381be6e5c86d68`, preserves the M6-I71 regression,
  repairs its representation-only failure, and accepts M6-I72.
- Recorded acceptance evidence: 218 declarative suites, 386 verifier tests, 35
  graph tests, focused mutation evidence, numeric lifecycle, and generated
  freshness passed at the recovery boundary.
- Independent focused revalidation during plan construction: the
  `rust-binding-callback-task` and `rust-binding-executor-delegation` suites
  both passed, two selected and zero failed.
- Routing selected Core, Router, Planning, Implementation, Verification,
  Documentation, Tooling, Commit, Architecture, Contracts, Diagnostics,
  Security, Cross-Platform, and Persistence. Performance and Concurrent Plan
  Integration are not applicable to the current claims and serial planning
  state.
- Plan boundary: A1 owns typed snapshot-bound navigation and read-only impact
  analysis. It does not own semantic acceptance, controlled authoring,
  repository mutation, evidence-oracle policy, or external project baselines.
- Admission result: plan state is `Planned`. Milestone 0 architecture and
  canonical schema admission is the sole next slice. No runtime implementation
  is admitted.
- Plan validation: the repository plan-structure checker passed; the
  `planning-admission`, `plan-template-projection`,
  `contract-planning-boundary`, `s1-routing`, and `documentation-decisions`
  suites passed, five selected and zero failed; `git diff --check` passed.

## 2026-08-22: Milestone 0 Architecture And Contract Acceptance

- Accepted the
  [Standards Engine architecture decision](../../decisions/standards-engine-navigation-analysis.md)
  with read-only A1 boundaries, neutral dependency direction, trusted snapshot
  bootstrap, explicit capability injection, and no controlled-authoring path.
- Accepted one JSON Schema Draft 2020-12 document as the machine authority for
  Python, JSON, agent-tool, example, identity, and renderer projections.
- Selected exact impact groups: `policy-impact` for consumer propagation and
  `standards-requires` plus `standards-specializes` only for additions and
  cross-module moves. The broad `semantic` and combined
  `standards-dependencies` groups are excluded.
- Recorded canonical serialization, six identity domains, policy-unit and audit
  schemas, typed applicability, decision dependency contracts, exact completion
  equality, trusted authorization context, package entry points, and contract
  version behavior.
- Contract validation passed 22 examples, seven stable identity fixtures, four
  public operation envelopes, 94 definitions, and embedded negative checks.
- Twelve affected declarative suites passed, including Architecture,
  composition-root, Contracts, Diagnostics, Persistence, Tooling,
  Documentation, Planning, Security-command, template, and routing contracts.
- The full declarative registry passed 218 selected, 218 passed, zero failed,
  and zero blocked.
- Plan structure passed. The existing Markdown-link engine resolved 57 local
  links across all eight changed Markdown artifacts. Python syntax compilation
  and `git diff --check` passed.
- Detailed architecture and contract review is in
  [the Milestone 0 report](reports/milestone-0-architecture-contract-review.md).
- No runtime module, production loader, generated Python projection,
  compatibility path, or authoring behavior was introduced.
- Milestone 0 is `Accepted`. Runtime admission remains unavailable until this
  boundary is committed and its exact commit and tree are recorded through the
  plan's `start` operation.

## 2026-08-22: Implementation Start And Metadata Inventory Freeze

- The accepted Milestone 0 boundary is commit
  `c7d23dfa55a9558b929e6b838d7ea0563981a1ef`, tree
  `5e9c4eb211ee0a67039b0ec11142db9b106243ae`.
- The repository was clean, only the main worktree existed, M6-I72 was the
  latest accepted verifier package, and no later verifier package was admitted.
- Operation `start` moved this plan from `Planned` to `Active` and admitted
  Milestone 1 within its accepted write set.
- The
  [metadata-consumer inventory](reports/metadata-consumer-inventory.tsv)
  froze the complete current cutover set before runtime source edits. Neutral
  authority is split between verifier-owned corpus loading and document
  metadata parsing; all other rows are consumers, projections, entrypoints, or
  tests.
- `graph_adapters.py` consumes only the structural `MetadataModule` protocol
  and owns graph projection rather than metadata loading. It requires
  equivalence evidence but no source change. Declarative suite files invoke
  registered verifier checks and are not independent metadata consumers.
- No consumer outside the accepted Milestone 1 write set requires a source
  change. No re-plan trigger was reached.

## 2026-08-22: Milestone 1 Neutral Metadata Cutover

- Added `tools/standards_metadata/` as the sole loader for corpus membership,
  canonical document metadata, immutable module views, ID/path resolution,
  `Requires`, `Specializes`, and neutral structural failures.
- Cut repository graph composition, metadata-route validation, policy-impact
  validation, metadata checks, and their tests over to the neutral API. The
  verifier retains suite configuration, suite context, diagnostic translation,
  and policy-specific validation only.
- Deleted the verifier-owned `canonical_modules.py` and the duplicated document
  parser from `checks/metadata.py`. No wrapper, compatibility import, fallback,
  or second production metadata representation remains.
- The admitted old loader and new loader produced exactly equal normalized
  JSON for 58 modules and 39,305 bytes, with SHA-256
  `ff5e206875e60c03dbd8e408a7e71c1661afa199b0525b6f5aef666e88f9e826`.
- Neutral metadata tests include strict corpus paths, missing and malformed
  inputs, symlink escape, duplicate/unresolved identities, distinct cycle
  outcomes, and an iterative 1,200-module acyclic chain.
- Focused consumer tests passed 44 tests. The complete neutral package passed
  seven tests, verifier package passed 381 tests, graph engine passed 35 tests,
  all 218 declarative suites passed, the A1 contract validator passed, logical
  and path graph aliases remained exact, and `git diff --check` passed.
- The complete mixed checkpoint passed generated freshness, all 218
  declarative suites, and all 53 retained Bash checkers from the final
  candidate tree.
- Detailed design, equivalence, disposition, and verification evidence is in
  [Milestone 1 acceptance](reports/milestone-1-neutral-metadata-cutover.md).
- Milestone 1 is `Accepted`. Milestone 2 is active with snapshot and policy-unit
  foundations as its sole next slice.

## 2026-08-22: Milestone 2 Snapshot And Policy-Unit Foundation

- Added `standards_analysis` as a verifier-independent package with canonical
  serialization, domain-separated identities, immutable source snapshots, and
  explicit policy-unit authority.
- Clean Git snapshots bind tree content separately from commit provenance and
  declared scope, exclusions, submodule state, and contract versions. Dirty
  Git and non-Git inputs use deterministic manifests with tracked, untracked,
  ignored-but-selected, mode, symlink, nested-repository, gitlink, and explicit
  exclusion state.
- Manifest construction rejects lexical and symlink-ancestor escape, does not
  follow symlinks by default, captures dirty nested Git content through a
  nested snapshot handle, and distinguishes a Git repository with no tracked
  files from a non-Git source.
- Added an explicit registered policy-unit source and the first accepted unit,
  `workflow.verification.acceptance-claims`. Canonical module metadata derives
  its document path; the sidecar owns only stable unit identity, module-relative
  locator, accepted semantic revision, aliases, and lifecycle relationships.
- Policy-unit validation resolves each heading exactly once, rejects duplicate
  locator ownership and identity conflicts, preserves separate representation
  and structural digests, and enforces reciprocal split/merge tombstone links.
- Seventeen analysis tests, seven neutral metadata tests, 381 verifier tests, 35
  graph tests, all 218 declarative suites, 22 contract examples, seven identity
  fixtures, four operation envelopes, 94 schema definitions, and
  `git diff --check` passed.
- No canonical standard, Router rule, graph schema, verifier behavior, or
  migration package changed. The complete mixed checkpoint remains reserved
  for the Milestone 2 shared integration boundary.
- This foundation slice is accepted. The sole next slice is typed
  snapshot-bound `read`, `related`, and `inspect`; Router projection and impact
  analysis remain outside that slice.

## 2026-08-22: Milestone 2 Standards-Graph Ownership Replan

- Pre-slice inspection found that `standards-requires` and
  `standards-specializes` are projected only by verifier-owned
  `graph_adapters.py` even though both the verifier and A1 navigation now need
  them.
- Importing the verifier from the Standards Engine would reverse the accepted
  dependency direction. Copying the projection would create two authorities
  for edge identity, grouping, direction, and traversal.
- Accepted a small neutral `standards_graph` module as the shared seam. It owns
  only canonical metadata-to-generic-edge projection and repository standards
  graph composition; generic traversal remains in `graph_engine`, canonical
  facts remain in `standards_metadata`, and suite dependency projection remains
  in `standards_verifier`.
- Expanded the Milestone 2 write set only to the current metadata-graph
  consumers and their tests. The cutover must remove verifier ownership in one
  coherent change without a wrapper, re-export, duplicate provider, or fallback.
- Router projection, impact analysis, suite dependency ownership, graph schema,
  and canonical metadata are unchanged. No concurrent verifier package is
  admitted and the replan base is clean commit
  `8edbc46ec89f9a82cdd7bc8636ee955c5684d533`.
- Detailed alternatives and acceptance conditions are recorded in
  [the ownership replan](reports/milestone-2-standards-graph-ownership-replan.md).

## 2026-08-22: Milestone 2 Neutral Standards-Graph Cutover

- Added `standards_graph` as the single adapter from canonical module metadata
  and explicit standards relationship manifests to the generic graph engine.
- Pre-cutover comparison proved exact equality for 58 nodes, 178 edges, and
  three named groups, including stable source, provenance, aliases, edge IDs,
  relation names, group memberships, traversal policy, and metadata.
- Removed metadata graph constants and provider implementation from
  `standards_verifier.graph_adapters`. Repository composition, metadata route
  checks, and tests now import the neutral owner; no wrapper or re-export
  remains. Suite dependency projection remains verifier-owned.
- The neutral navigation registry composes only canonical metadata relations
  and the explicitly registered policy-impact manifest. It does not scan,
  infer relationships, or load suite execution dependencies.
- Two neutral graph tests, 34 focused consumer tests, all 381 verifier tests,
  35 generic graph tests, seven metadata tests, all 218 declarative suites,
  plan structure, query integration, and `git diff --check` passed.
- The ownership cutover is accepted. The sole next slice is snapshot-bound
  typed `read`, `related`, and `inspect` over this neutral seam.

## 2026-08-22: Milestone 2 Module Inspection Contract Replan

- Navigation design found that accepted Router examples return canonical
  module IDs while `PolicyInspectionResult` could describe only registered
  policy units. Policy-unit coverage is intentionally partial, so restricting
  reads to sidecars would make accepted whole-artifact routes unreadable.
- Rejected synthetic policy-unit declarations because they would invent stable
  identity and semantic revision authority. Rejected full policy-unit
  population because it is unnecessary authoring and audit scope for read-only
  navigation.
- Accepted one explicit derived `CanonicalModuleDeclaration` variant alongside
  `PolicyUnitDeclaration`. Module reads use whole-artifact scope; policy-unit
  reads use their exact structured scope. Both retain the existing snapshot-
  bound `PolicyHandle` and discriminated declaration kind.
- This is a version-1 pre-runtime schema correction: no Python projection,
  agent tool, external adopter, or serialized runtime value exists. The ADR now
  states that post-publication variant additions require contract migration.
- Detailed rationale and acceptance checks are in
  [the module inspection replan](reports/milestone-2-module-inspection-contract-replan.md).
- Runtime projection then exposed a second narrow schema omission: generic
  graph edge identities are stable opaque strings and accepted metadata edge
  IDs contain `->`, while `RelationshipHandle` incorrectly reused the narrower
  canonical policy-ID grammar.
- Accepted a distinct non-empty `EdgeId` contract for relationship handles and
  edge selection provenance. Registered graph resolution remains mandatory;
  canonical module and policy identity grammar is unchanged. Hashing, renaming
  accepted edges, or widening every canonical ID was rejected.

## 2026-08-22: Milestone 2 Read, Related, And Inspect

- Corrected the version-1 contract before runtime acceptance so module
  inspection returns a derived canonical-module declaration while policy-unit
  inspection returns authored sidecar authority. Added a distinct registered
  `EdgeId` contract rather than widening canonical policy identities.
- Added the `standards_engine` typed facade with snapshot-bound `read`,
  `related`, and `inspect` operations. Canonical module reads use whole-artifact
  scope; registered policy-unit reads use exact heading scope.
- Named-group and transitive traversal delegate to the accepted generic graph
  engine. Relationship handles retain exact registered edge identities, and
  repository locations remain explicit inspection provenance rather than
  caller input.
- Added typed rejection for stale snapshots, malformed native requests,
  repository-path reads, unknown policies and groups, and forbidden traversal.
  Policy-unit queries normalize to their canonical owning graph node.
- The contract validator passed 23 examples, seven identities, four operation
  envelopes, and 96 definitions. Seven engine, 17 analysis, seven metadata,
  two standards-graph, 35 graph-engine, and 381 verifier tests passed. All 218
  declarative suites, plan structure, and `git diff --check` passed.
- Detailed evidence is in [the navigation acceptance report](reports/milestone-2-read-related-inspect.md).
  The sole next slice is mechanical Router projection and typed route/read
  evidence; impact analysis remains excluded.

## 2026-08-22: Milestone 2 Router Projection Replan

- The next slice found that general Router conditions exist only in normative
  prose while executable fixtures cover bounded verifier and language cases.
  Parsing English or copying the decisions into Python would violate the
  accepted projection and authority contracts.
- Generic graph queries for `router` and its path alias were exact. Because the
  owner is not globally audited, a bounded manual review classified current
  entrypoints and executable routing consumers instead of treating empty
  outgoing impact as complete.
- Accepted one registered reviewed executable projection, generic
  three-valued evaluation in `standards_analysis`, and graph-derived closure in
  `standards_engine`. Router remains normative; no Router wording or broad
  consumer projection changes are authorized.
- Detailed scope, dispositions, alternatives, and acceptance are in
  [the Router projection replan](reports/milestone-2-router-projection-replan.md).

## 2026-08-23: Milestone 2 Router Projection And Navigation Acceptance

- Added one reviewed executable Router projection with seven typed fact
  categories and 38 unique rules. Its target set must exactly match the 38
  canonical modules linked by Router selection tables.
- Brought forward the accepted generic three-valued applicability evaluator.
  It supports `all`, `any`, `not`, `equals`, `in`, `contains`, and `exists`;
  malformed configuration rejects while unavailable contextual facts remain
  unknown.
- Added typed `route` results, deterministic graph-derived Requires closure,
  bounded unresolved questions, contract-ordered reading plans, and a thin
  schema-validating structured tool facade. No Python policy decision table,
  Router wording change, fallback lookup, or verifier dependency was added.
- Existing verifier-change fixtures now run through the public route API and
  match exact direct and closure expectations. The real structured tool routes
  and reads through the same snapshot without repository paths.
- Focused analysis and engine tests, all downstream unit suites, canonical
  contract validation, focused S1 routing, and all 218 declarative suites pass.
- The complete mixed checkpoint passed generated-evidence freshness, all 218
  declarative suites, and all 53 retained Bash checkers from the final
  candidate tree.
- Detailed acceptance is in [the Milestone 2 report](reports/milestone-2-route-acceptance.md).
  Milestone 3 becomes current with modification, addition, and removal
  classification and seed selection as its sole next slice.

## 2026-08-23: Commit Message History Reconciliation

- The repository owner authorized a reword-only rewrite from the Milestone 0
  commit through Milestone 2 Router acceptance because the substantial commits
  had conventional subjects but omitted required rationale, scope, and
  contract-effect bodies.
- The original tip remains protected at
  `refs/recovery/pre-a1-message-rewrite-20260823`. One worktree and one local
  branch existed; no other local ref depended on the rewritten commits.
- Exact commit lineage changed as follows while every tree remained identical:

| Original | Replacement | Tree |
| --- | --- | --- |
| `8b632df4` | `c7d23dfa` | `5e9c4eb2` |
| `38e40279` | `3383ec68` | `11a737a9` |
| `eb1f863d` | `3e8aae87` | `4746269e` |
| `d6813ba2` | `8edbc46e` | `a613ae62` |
| `84797b5a` | `3fe09812` | `76cbffa2` |
| `0e910fcc` | `bbbab878` | `a246d0de` |
| `ca3dda6f` | `5849ffd4` | `fca200cd` |

- `origin/main` still names the original `8b632df4` history. This reconciliation
  does not authorize a force push or remote rewrite.

## 2026-08-23: Milestone 3 Classification And Graph Union

- Added immutable modification, addition, and removal classification against
  accepted and proposed policy-unit corpora. Exact semantic overlays bind the
  prior revision, next revision, and proposed structural digest; absent
  semantic evidence remains a representation candidate or unresolved state.
- Added exact schema-checked graph seed/group selection and a node-only
  policy-unit provider. The analyzer consumes supplied generic registries and
  does not own graph storage, manifests, or inferred edges.
- Added deterministic accepted/proposed union traversal with retained seed,
  group, path, edge, metadata, and declaration provenance. One stable edge ID
  remains one candidate with all snapshot traces.
- Focused analysis tests pass 40 cases. Engine, metadata, standards-graph,
  graph-engine, verifier, canonical-contract, and all 218 declarative suites
  passed for the classification boundary; final graph-union verification is
  recorded in the acceptance report.
- Obligation work reached a replan trigger: existing policy-impact
  applicability is explanatory string metadata, while A1 requires typed domain
  semantics that the neutral graph must not interpret. The
  [applicability replan](reports/milestone-3-policy-impact-applicability-replan.md)
  initially recorded four options.

## 2026-08-23: Milestone 3 Compiled Policy-Impact Authority

- Architecture review rejected the initial edge-ID sidecar because it would
  require generic topology and typed semantics to remain synchronized.
- Accepted one `standards_policy_impact` module whose source-owner
  declarations compile into a neutral graph contribution and a typed semantics
  index. Generic node and group catalogs remain independent upstream
  authorities.
- Domain propagation now belongs to the relationship-kind contract rather than
  generic group direction. Evidence ownership is explicit authored semantics;
  audit association requires strict resolution and neither may be guessed from
  consumers.
- Versioned applicability to add fact-free `always`. All 39 existing
  relationships were manually classified as unconditional review relations;
  their former explanatory text remains rationale only.
- Deliberately superseded exact authored policy-impact EdgeIds with injective
  percent-encoded identities derived from unique `(source, relation, consumer)`
  keys. The exact mapping is recorded in
  [the edge inventory](reports/policy-impact-edge-inventory.tsv).
- The revised ADR, schema, cutover inventory, and one-authority migration
  sequence were accepted before production compiler implementation.

## 2026-08-23: Milestone 3 Corrective Green Boundary

- Review found that the accepted v2 schema had replaced the v1 contract before
  current analysis and Standards Engine producers emitted the v2 interface and
  applicability versions. The producer versions and fact-free `always`
  evaluator were updated together with focused tests.
- Replaced stale plan authority: Milestone 3 is explicitly admitted, the
  resolved authority blocker is no longer current, and unimplemented move,
  split, and merge behavior is no longer marked complete.
- Defined relationship-kind contract version 1 as a small module-owned Python
  table, removed speculative declaration-level propagation overrides, made
  evidence ownership explicitly authored, and adopted injective percent-encoded
  compiled edge identities.
- Expanded ADR and Milestone 3 traceability to include
  `standards_policy_impact`, repository graph composition, and the graph-engine
  README's published edge example.

## 2026-08-23: Milestone 3 Applicability Ownership Replan

- Compiler work exposed a dependency cycle: policy-impact must validate typed
  applicability before producing semantics, while analysis already consumes
  compiled policy impact and owned the only complete evaluator.
- Accepted one standard-library-only `standards_applicability` Module. The A1
  JSON Schema remains serialized-shape authority; the neutral Module owns
  executable compilation, normalization, type checking, truth tables,
  unresolved facts, schema compatibility, identities, and typed failures.
- The replacement slice compiles Router and policy-impact expressions once,
  binds one fact set per request, stores immutable programs in compiled
  policy-impact semantics, and deletes both former parsers without fallback.
- The active next slice and allowed write set were replaced before source
  implementation continued. Detailed authority and verification decisions are
  in the [applicability ownership replan](reports/milestone-3-applicability-ownership-replan.md).

## 2026-08-23: Milestone 3 Applicability And Policy-Impact Cutover

- Accepted the standard-library-only applicability Module after exhaustive
  operator, fact-type, fact-state, truth-table, schema-identity, digest,
  unresolved-fact, and dependency-direction evidence.
- Compiled Router and policy-impact expressions into immutable programs and
  removed both former executable parsers without compatibility behavior.
- Cut all registered policy-impact relationship consumers to one compiled
  authority while preserving independent generic node and group ownership.
- All 218 declarative suites and the complete checkpoint with 53 retained Bash
  checkers passed. Detailed evidence is recorded in the
  [cutover report](reports/milestone-3-applicability-policy-impact-cutover.md).
- The sole next slice is request-bound applicability evaluation, exact impact
  obligations, and bounded audit coverage.

## 2026-08-23: Milestone 3 Consumer-Obligation Recovery

- Reopened SENA-006 after review proved that the accepted impact pipeline
  stopped at candidates and never generated consolidated consumer-review work.
- Added one canonical consumer-selection aggregate keyed by exact consumer,
  canonical scope, and review contract. Plural typed reasons retain every
  selecting policy unit, edge, relationship, evidence owner, and accepted or
  proposed trace while one aggregate derives both display provenance and the
  decision fingerprint.
- Preserved definite review alongside unknown applicability work and bound
  consumer identity to exact changed-policy state, relationship semantics,
  traces, applicability fact values, scope, review contract, and evidence
  owners.
- Replaced obligation identity v1, packet identity v1, packet schema v1, and
  public interface v3 atomically with obligation v2, packet v2, packet schema
  v2, and interface v4. No compatibility interpretation remains.
- Superseded the earlier whole-Milestone-3 acceptance while preserving its
  valid lifecycle evidence. The recovery passed 72 analysis, 15 Standards
  Engine, 17 metadata, 9 applicability, 7 policy-impact, 2 standards-graph, 35
  graph-engine, and 380 verifier tests; 29 contract examples; all 218
  declarative suites; and the complete checkpoint with 53 retained Bash
  checkers.
- Reaccepted Milestone 3 through the superseding recovery report and advanced
  exactly one next slice: bounded reading-plan compilation from obligations.

## 2026-08-23: Milestone 4 Reading-Plan Replan

- Reopened the reading-plan slice after review proved that singular permissive
  reasons lose Router and dependency causes and cannot reference several
  compatible consumer obligations without copying semantic provenance.
- Accepted one deep compiler over typed selections. It derives authority from
  canonical target metadata, collapses exact target/scope keys, unions causes,
  and applies deterministic state and ordering rules.
- Bound the atomic version replacement: analysis contract 2, public interface
  5, navigation 2, packet 3, and completed report 2.
- Added explicit non-module authority classification to the admitted write set;
  path, relationship kind, and reason inference remain prohibited.

## 2026-08-23: Milestone 4 Horizon Projection Replan

- Focused comparison proved that the 27-node catalog's identity, aliases,
  paths, groups, and edges and all 126 compiled policy-impact semantics were
  unchanged; only five projection and 22 evidence classifications were added.
- Rejected both path-derived authority and immediate repeated attestation
  renewal. Accepted a typed provider-v2 projection that excludes only
  reading-only authority from coverage while retaining complete snapshot
  binding.
- Moved the node catalog from accepted Milestone 2 authority into the active
  Milestone 4 recovery write set and admitted horizon declaration, coverage
  attestations, tests, and final audit evidence.
- Bound attestation renewal as the final authority step after all proposed
  horizon-affecting inputs are frozen.

## 2026-08-23: Milestone 4 Reading And Horizon Recovery

- Added one typed reading-plan compiler over Router selections, dependency
  edges, and consumer-obligation handles. Exact target/scope collapse retains
  all canonical causes, while target metadata alone determines authority.
- Replaced singular reading reasons and incomplete route provenance under the
  coordinated analysis-contract 2, interface 5, navigation 2, packet 3, and
  report 2 identity cutover.
- Added explicit authority to all 27 registered non-module reading targets.
  Provider-v2 coverage projection removes only this typed reading field from
  the catalog fingerprint while the complete catalog remains snapshot-bound.
- Froze the final 856-member horizon, recorded unchanged topology and all 126
  compiled relationship semantics, generated the exact 28 requirement
  handles, and renewed Planning and Commit attestations once under authorized
  audit evidence.
- Resolved SENA-016 and SENA-017 through the
  [recovery acceptance](reports/milestone-4-reading-plan-recovery.md). The sole
  next slice is packet staleness and decision reuse from exact narrower
  dependency fingerprints.

## 2026-08-23: Milestone 4 Fact-Authority Replan

- Stopped packet-reuse implementation after finding that fact answers carry no
  fingerprint and one question may feed several relationship-specific
  applicability obligations.
- Rejected both relationship-obligation fingerprints and a question-level
  fingerprint as the durable authority. Accepted one semantic `FactContract`,
  one topology-independent `AnalysisContext`, one content-addressed
  `FactRequirement`, and one evidence/authorization-bound `FactObservation`.
- Bound reuse to exact requirement identity. Prompt wording and aliases remain
  projections; unrelated topology changes and additional consumers do not
  invalidate observations.
- Reopened the horizon freeze only for this superseding architecture change.
  Router fact contracts and every other horizon-affecting input must be final
  before affected coverage attestations are renewed once.

## 2026-08-24: Milestone 4 Immutable-State Replan

- Rejected raw `AnalysisRequest` facts because they can resolve applicability
  without a requirement, evidence, or authorization.
- Rejected caller-coordinated observation lists because they expose storage,
  conflict handling, and reuse selection through the agent Interface.
- Confirmed that the in-progress packet identity omits accepted observations
  and dispositions while hidden sessions retain them, allowing distinct
  decision histories to alias to one content-addressed packet handle.
- Accepted one immutable generated `AnalysisState` bound into every packet and
  report, one optional prior-analysis handle, exact narrow decision
  revalidation, provider claims with analysis-owned observation construction,
  and current-material rather than accumulated requirement completion.

## 2026-08-24: Milestone 4 Packet-Supersession Replan

- Implemented the immutable-state cutover far enough to remove raw analysis
  facts, hidden sessions, and caller-coordinated observation lists and to run
  real typed-agent modification, addition, and removal workflows.
- A blocked-disposition fixture exposed that supersession is stored globally by
  packet ID. Repeating the same preparation after an earlier completion
  recreated the byte-identical packet ID, but resolving it returned
  `PACKET.STALE` solely because of the earlier run.
- Confirmed the conflict with a focused real-engine reproduction: the initial
  and repeated packet IDs were equal while the latter could not be resolved.
- Stopped implementation and opened SENA-020. The recommended replan treats A1
  packets as immutable branchable analysis states and reserves compare-and-swap
  head staleness for future controlled-authoring sessions.

## 2026-08-24: Milestone 4 Single-State Replan Admission

- Accepted a deeper replacement of the initial SENA-020 correction: one
  content-addressed `AnalysisState` and one `AnalysisHandle` are the complete A1
  lifecycle model.
- Pending and complete results, requirements, obligations, reading plans,
  certificates, and completion proofs are deterministic projections rather
  than stored identity-bearing artifacts.
- Bound authorization-authority and provider contract/input views as exact
  state inputs. Provider execution is prohibited during projection and cannot
  read undeclared ambient state.
- Admitted one atomic runtime and schema cutover with no packet/report
  compatibility layer. A1 has no global supersession, mutable head, or temporal
  stale outcome; those semantics remain reserved for A2 authoring.

## 2026-08-24: Milestone 4 And Plan A1 Acceptance

- Committed the single-state implementation as
  `94b295b40bc1cef9a6281355d68115f3a98ed112`, tree
  `ff032da51fcaff45533c07daa8de464065b8e55c`.
- Replaced packet, report, hidden-session, and global-supersession authority
  with one immutable `AnalysisState` and `AnalysisHandle`; pending and
  complete results are deterministic projections.
- Closed SENA-003, SENA-007, SENA-018, SENA-019, and SENA-020. Existing move,
  split, and merge impact fixtures satisfy the lifecycle acceptance row.
- The frozen coverage projection and 28 requirement subjects remained valid;
  no coverage-authority input changed, so no additional attestation renewal
  was required.
- Verified 80 analysis tests, 30 Standards Engine tests, 12 applicability
  tests, 7 policy-impact tests, 17 metadata tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, and the complete checkpoint with 53
  retained Bash checkers.
- Accepted Milestone 4 and completed Plan A1. Controlled authoring,
  evidence-oracle policy, and external project baselines remain outside this
  plan.

## 2026-08-24: A1 Acceptance Reopened

- A post-implementation audit found that whole-module reads could return live
  filesystem bytes after snapshot issuance, invalidating snapshot-bound
  reproducibility.
- The same audit found incomplete schema projection, inspection, canonical
  serialization, next-operation binding, documentation, and acceptance-oracle
  conformance.
- Withdrew the prior A1 acceptance, returned the plan to `Verifying`, and
  retained the single-state architecture. Plan A2 remains blocked until every
  A1 objective acceptance projection is mechanically reconciled.

## 2026-08-24: A1 Boundary Repair Implemented

- Captured immutable file bytes from exact Git trees or verified manifests and
  made whole-module reads consume only that snapshot content.
- Advanced snapshot identity to version 2 and public interface version 9;
  semantic contract versions now affect snapshot identity while implementation
  releases remain provenance.
- Generated the native Python algebra and agent tool schemas from the canonical
  JSON Schema, made deterministic `--check` freshness part of contract
  validation, and made text rendering exhaustive over generated result kinds.
- Consolidated canonical key normalization in `standards_metadata`, separated
  caller decoding from engine invariant failures, bound every continuation to
  an exact snapshot or analysis, and implemented every advertised inspection
  result.
- Strengthened plan lifecycle verification to reject accepted plans with
  unsatisfied objective rows or contradictory final projections, then refreshed
  the canonical 53-checker inventory and 57-node/375-edge dependency graph.
- Verified 82 analysis tests, 39 Standards Engine tests, 18 metadata tests, 12
  applicability tests, 7 policy-impact tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, and the complete checkpoint with 53
  retained Bash checkers.

## 2026-08-24: A1 Boundary Repair Accepted

- Accepted the repaired Plan A1 implementation at commit
  `51dcd258942b0774c73ae8b620227c7ce34d1129`, tree
  `f8d028e887f4061a1d03ad6e75b9776a5fc3966b`.
- Closed SENA-021 after immutable snapshot reads, semantic-contract-bound
  snapshot identity, generated interface projections, exhaustive inspection,
  canonical key normalization, exact continuation bindings, and coherent plan
  acceptance projections were implemented and verified.
- Verified 82 analysis tests, 39 Standards Engine tests, 18 metadata tests, 12
  applicability tests, 7 policy-impact tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, and the complete checkpoint with 53
  retained Bash checkers.
- Reaccepted Milestone 4 and satisfied objective rows A1 through A9. The
  withdrawn `94b295b4` boundary remains historical evidence and is not
  relabeled green.
- Completed read-only Plan A1. Controlled authoring requires separate Plan A2
  review and admission; Plans B and C remain inactive.

## 2026-08-24: A1 Boundary Repair Acceptance Reopened Again

- A follow-up audit reproduced a live-worktree leak in whole-module policy
  inspection, cold-process loss of advertised analysis child artifacts, and
  incomplete schema ownership of the generated native Python algebra.
- The audit also proved that malformed objective statuses and missing final
  projections could pass the accepted-plan checker and found one stale
  snapshot-v1 identity domain in the accepted ADR.
- Withdrew the `b8f52240` acceptance authority, returned Plan A1 to
  `Verifying`, and opened SENA-022. The single-state architecture remains
  binding; Plan A2 remains inactive.

## 2026-08-24: A1 Boundary Repair II Implemented

- Recorded the repair implementation at commit
  `714ba23fb5186b549ab44865d36c77509dbf654a`, tree
  `d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b`.
- Made whole-module policy inspection consume immutable snapshot content and
  added a full-result mutation regression alongside the existing read check.
- Replaced the in-memory analysis-artifact cache with deterministic
  reconstruction from persisted immutable analysis states; fresh engines now
  inspect advertised context, requirement, and observation handles.
- Replaced the field-name-only generator with a canonical-schema walker that
  generates Python object types, defaults, constants, discriminated unions,
  nested request and submission variants, decoding, exports, and agent tools.
  Removed the duplicate hand-written agent-facade request and submission
  decoders.
- Strengthened accepted-plan verification to parse every objective row, reject
  unknown or missing statuses, require objective rows, and require both final
  projections. Corrected the ADR's remaining snapshot-v1 identity domain.
- Verified 82 analysis tests, 41 Standards Engine tests, 18 metadata tests, 12
  applicability tests, 7 policy-impact tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, every current plan through the stronger
  checker, and the complete checkpoint with 53 retained Bash checkers.
- The implementation remains a candidate under SENA-022. Plan A1 stays
  `Verifying`; no acceptance is inferred from implementation-owned evidence,
  and Plan A2 remains inactive.
- Published the exact evidence as
  [A1 boundary repair II candidate](reports/a1-boundary-repair-ii-candidate.md)
  for independent acceptance review.

## 2026-08-24: A1 Boundary Repair II Review Failed

- Independent review rejected candidate commit `714ba23f`, tree
  `d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b`.
- Generated dataclass construction omitted the schema's integer minimum, and
  result variants remained arbitrary mapping wrappers outside the generated
  native algebra.
- Cold child-artifact inspection reprojected with the fresh engine's execution
  authorizations and providers, while the advertised public behavior required
  deterministic reconstruction from authority views stored in immutable state.
- Objective rows A4 through A7 cited withdrawn evidence, `partial` remained an
  unsupported accepted objective status, satisfied rows did not require
  evidence, and the ADR still listed retired packet and report domains as
  current.
- Kept Plan A1 `Verifying`, retained SENA-022 as active, and left Plan A2
  inactive while the remaining boundary repair proceeded.

## 2026-08-24: A1 Boundary Repair III Implemented

- Recorded the repair implementation at commit
  `8ed8ba0beba5dd16c0a2da50655952842ab61c85`, tree
  `eaeac78739468fc2c79241f6a7830e54986d2f95`.
- Expanded generated Python authority from operation inputs to the complete
  public input and result closure. Concrete result dataclasses, nested models,
  required fields, constants, discriminants, and integer minimums now use one
  recursive schema-derived decoder; incomplete results and revision zero are
  rejected.
- Made analysis-state inspection return the generated `AnalysisState` result
  model rather than a handwritten domain object.
- Added a projection-only analysis kernel that binds authorization and provider
  authority from persisted immutable state and never invokes providers. Public
  cold context inspection now succeeds without execution-authority injection;
  requirement and observation inspection use the same state-bound path.
- Replaced withdrawn A4 through A7 evidence with still-valid milestone
  evidence, removed retired packet/report domains from the ADR's current list,
  rejected `partial` objective status, and required evidence for every
  satisfied objective row.
- Verified 82 analysis tests, 43 Standards Engine tests, 18 metadata tests, 12
  applicability tests, 7 policy-impact tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, every current plan, and the complete
  checkpoint with 53 retained Bash checkers. Generated freshness, scoped Ruff,
  and Git diff integrity also passed.
- Plan A1 remains `Verifying`, SENA-022 remains active pending independent
  acceptance review, and Plan A2 remains inactive.
- Published the exact evidence as
  [A1 boundary repair III candidate](reports/a1-boundary-repair-iii-candidate.md).

## 2026-08-24: A1 Boundary Repair III Review Failed

- Independent review rejected candidate commit `8ed8ba0b`, tree
  `eaeac78739468fc2c79241f6a7830e54986d2f95`.
- Generated const and enum validation used Python equality, allowing Boolean
  values to satisfy integer constants, and pattern validation used full-match
  rather than JSON Schema search semantics.
- Native `prepare` and `resolve` returned analysis-domain pending and complete
  results instead of the generated Standards Engine result models.
- The two new negative plan fixtures omitted mandatory plan structure, so they
  failed before reaching their claimed objective-status and evidence checks.
- Retired packet/report terminology also remained in current ADR prose. Plan
  A1 stayed `Verifying`, SENA-022 stayed active, and Plan A2 stayed inactive.

## 2026-08-24: A1 Boundary Repair IV Implemented

- Recorded the repair implementation at commit
  `3d389dd7f73f48c21d80570331c8058737f941db`, tree
  `6fcbfed114dcfd768186f8610c0792e220657b32`.
- Made generated constant and enum validation use type-sensitive canonical
  equality, so Boolean values cannot satisfy integer schema values, and made
  generated pattern validation use JSON Schema search semantics.
- Adapted native `prepare` and `resolve` results to the generated
  `PendingResult` and `CompleteResult` models before crossing the public
  Standards Engine boundary. Unsupported domain result kinds remain internal
  invariant failures rather than caller rejections.
- Rebuilt both objective regression fixtures as otherwise-valid plans and made
  their verification assert the exact missing-evidence and invalid-status
  diagnostics. Refreshed the generated checker-structure inventory.
- Replaced remaining current ADR packet/report terminology with immutable
  analysis-state and result terminology. The rejected repair III report
  remains historical evidence.
- Verified 82 analysis tests, 43 Standards Engine tests, 18 metadata tests, 12
  applicability tests, 7 policy-impact tests, 35 graph-engine tests, 2
  standards-graph tests, 380 verifier tests, 33 contract examples, 8 identity
  fixtures, all 218 declarative suites, every current plan, and the complete
  checkpoint with 53 retained Bash checkers. Generated freshness, scoped Ruff,
  and Git diff integrity also passed.
- Plan A1 remains `Verifying`, SENA-022 remains active pending independent
  acceptance review, and Plan A2 remains inactive.
- Published the exact evidence as
  [A1 boundary repair IV candidate](reports/a1-boundary-repair-iv-candidate.md).

## Ledger Contract

Add dated entries only for plan admission, accepted planning decisions,
implemented slices, material deviations, verification results, re-planning,
commit boundaries, or final acceptance. Current objective, blockers, binding
decisions, milestone state, and next slice remain owned by `plan.md`.
