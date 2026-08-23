# Standards Engine Navigation And Analysis Execution Ledger

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
  `8b632df46db078846f7802ac55fcb54e2fb4e2d2`, tree
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
  admitted and the replan base is clean commit `d6813ba2c41b7f0ada0b38c4ea9ab533c10c65a9`.
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

## Ledger Contract

Add dated entries only for plan admission, accepted planning decisions,
implemented slices, material deviations, verification results, re-planning,
commit boundaries, or final acceptance. Current objective, blockers, binding
decisions, milestone state, and next slice remain owned by `plan.md`.
