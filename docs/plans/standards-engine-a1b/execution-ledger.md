# Standards Engine A1b Execution Ledger

## 2026-08-26 - Planning Started

- Planning comparison base: commit
  `c4408363752b10060f631247f3e2f1fa26eae003`, tree
  `84477150bd368a168dd04da3770de55c23bbb817`.
- Upstream authority: accepted standards recovery at that exact boundary.
- Operation: create the A1b plan and superseding proposed ADR only.
- Lifecycle: `Blocked` pending independent exact-tree planning admission.
- Excluded authority: no A1b runtime, dependency installation, contract
  generation, state migration, policy mutation, A2, or Plan C work is admitted.

## 2026-08-26 - Router Projection

- Supplied facts selected Planning, Implementation, Verification,
  Documentation, Build, Tooling, Architecture, Contracts, Dependencies,
  Licensing, Security, Diagnostics, Library, Persistence, and Generated
  Contract policy.
- IPC was not selected because no cross-process or independently deployed A1
  consumer was found.
- Language Binding was not selected because schema-to-Python generation does
  not create a native/foreign language boundary.
- The route is planning evidence. Canonical standards and policy relationships
  remain authority.

## 2026-08-26 - Design Review (Superseded)

- Two independent high-reasoning design reviews evaluated the contract and
  authority seams.
- Contract result: select an established Draft 2020-12 validator behind one
  project-owned compiler; keep generation build-time; generated models do not
  execute keywords; preserve identity and applicability as separate domains.
- Authority result: use one module with three typed roots; remove split stores,
  enumeration, and cache authority; prefer bounded snapshot bundles over a
  generic object graph while the measured scope remains small.
- Reconciliation: preserve NFC identity format version 1. Changing identity
  normalization was rejected as unrelated churn because the known defect is
  JSON Schema instance equality, not A1 identity.
- Lifecycle: these design choices were later `Superseded` by the replacement
  design after exact-tree admission review exposed broader identity and
  authority-closure defects.

## 2026-08-26 - Planning Candidate Prepared (Rejected)

- Added the blocked active plan, issue registry, execution ledger, dependency
  and dialect decision, consumer and persisted-state inventory, and proposed
  superseding ADR.
- Current next slice: independent Standards and Specification review of the
  exact planning candidate.
- Admission must follow the four-identity report/transition protocol in
  `plan.md`; implementation remains unavailable.

## 2026-08-26 - Candidate Admission Rejected

- Reviewed candidate: commit
  `f41037bf71deddba36056b27d418fe767a7cfb62`, tree
  `042f97101d50df79dcac0b029aa1b9324cf8b881`.
- Standards and Specification review rejected admission because the candidate
  did not mechanically close the admission/start ancestry, changed production
  schema and generated output before facade cutover, omitted semantic
  catalog/relationship migration, left schema annotations and identity
  versions underspecified, and bound only aggregate roots while promising cold
  child inspection.
- The dependency record also lacked exact transitive artifacts and licenses.
- No implementation was admitted. The candidate and its active design
  decisions are `Superseded` by the replacement candidate prepared below.

## 2026-08-26 - Replacement Design

- Replaced recursive NFC identity format v1 with representation-preserving
  identity encoding v2. Applicability retains deliberate domain-owned NFC
  behavior; ordering, deduplication, and normalization move to owning typed
  contracts.
- Replaced three-root storage plus owner-qualified child lookup with direct
  immutable storage for every public inspectable object under one closed
  envelope and resolution rule.
- Replaced schema `x-standards-engine-*` authority with one closed interface
  contract and named domain-owned executable contracts.
- Preserved `jsonschema.Draft202012Validator` as the sole Draft validator.
  Removed the proposed complete official-corpus run because A1b adapts a
  validator and does not implement or independently certify JSON Schema.
- Replaced the partial schema/generated milestone with private staging
  foundations followed by one atomic production v11 cutover.
- Added exact identity/version, schema/owner, consumer/state, and
  policy-impact migration inventories.

## 2026-08-26 - Exact Dependency Resolution Recorded

- Selected direct dependencies: `jsonschema==4.26.0` and
  `referencing==0.37.0`.
- Recorded the exact six-package transitive resolution, universal wheel hashes,
  and CPython 3.11/3.12 Linux x86-64 glibc 2.17
  `manylinux_2_17_x86_64.manylinux2014_x86_64` `rpds-py` artifacts, plus
  license expressions and license-file hashes.
- OSV queries on the recorded date returned no known vulnerability for the
  exact versions. Milestone 0 must reproduce rather than silently update this
  evidence.
- No third-party corpus, package source, or wheel is selected for repository
  incorporation.

## 2026-08-26 - Replacement Planning Candidate Prepared

- Current lifecycle remains `Blocked`.
- Next slice is independent Standards and Specification review of the exact
  replacement candidate.
- Admission requires the direct candidate, reviewer-report, mechanical
  admission-transition, and start-transition chain defined in `plan.md`.
- A1b runtime and A2 implementation remain unavailable.

## 2026-08-26 - Pre-Candidate Independent Review

- Standards review found four planning gaps: licensing acceptance was too
  late, checked-in generated/example/identity artifacts lacked explicit
  migration dispositions, durable publication lacked interruption and
  overlapping-writer rules, and the schema profile omitted exact vocabulary
  URIs.
- The dependency decision now records exact release/source authorities,
  copyright owners, embedded license identities, compatibility, notice
  obligations, and the non-bundling result. Planning admission must explicitly
  accept A1B-A6P before start.
- The policy-impact migration now includes the generated agent-tool artifact,
  public examples, identity fixtures, and their missing relationship
  corrections.
- The authority contract now defines same-filesystem staged directory
  publication, durable flushes, overlapping writers, collision behavior,
  interruption states, idempotent retry, and reopening evidence.
- The schema audit now binds the exact Draft 2020-12 meta-schema and vocabulary
  URIs while retaining `jsonschema` as the sole validator.
- A sequencing audit found that separately committed foundation Modules would
  create unregistered semantic consumers. Milestones 0 through 2 are therefore
  uncommitted working-tree checkpoints; Milestone 3 is the first implementation
  commit and atomically includes their policy-impact and coverage migration.

## 2026-08-26 - Pre-Candidate Specification Review

- Specification review found that the direct-object design lacked an explicit
  acyclic payload graph and self-handle rule, snapshot capture lacked a new
  owner, identity v2 lacked byte-complete framing, dependency artifacts were
  missing from the migration map, and public operation closure remained
  deferred.
- Added closed payload contracts for every inspectable object. Stored payloads
  exclude their own handles; context and requirement identities precede
  observations; no child points to an analysis root.
- Assigned Git-tree and mutable-manifest capture, source-race validation, nested
  snapshot publication, and root publication to `standards_authority`.
- Defined exact scalar escaping, surrogate rejection, integer rendering,
  Unicode ordering, hash framing, SHA-256, and ID grammar for identity v2.
- Added package manifest, exact lock, dependency decision, and implementation
  provenance artifacts to the semantic-consumer migration.
- Froze the four operation records, capability map, and exact reachable v11
  public definition-name set before implementation.
- Split pre-start licensing admission A1B-A6P from final exact-lock review
  A1B-A6L and prohibited schema-default injection without exception.
- Router correction: Concurrency and Resilience apply to overlapping durable
  publication and interruption/retry; Release applies to dependency and
  distribution lifecycle. They join the previously selected Planning,
  Implementation, Verification, Documentation, Build, Tooling, Architecture,
  Contracts, Dependencies, Licensing, Security, Diagnostics, Library, and
  Persistence policies. Cross-Platform is also selected because A1b defines
  filesystem identity, aliases, ext4 support, and typed unsupported outcomes.
  IPC, Language Binding, and A2 remain unselected for the exact in-process
  Linux x86-64 boundary.

## 2026-08-26 - Replacement Contract Closure Review

- A second pre-candidate review found missing snapshot-to-analysis dependency
  edges, underdefined authority payload records, three unlisted production
  consumers, underdefined generated-versus-authored fixture ownership, and an
  overwrite race in the former directory-rename publication design.
- Added a closed authority record algebra, required-field and ordering rules,
  direct snapshot dependencies, and cross-object coherence predicates.
- Added the Metadata and Analysis package initializers and Standards Engine
  renderer to the policy-impact migration, and classified examples and identity
  fixtures as authored oracles while agent-tool declarations remain generated.
- `Superseded`: staged directory rename and per-staging writer coordination.
  The current durable design supports Linux ext4, serializes writers through
  one non-authoritative repository publication lock, uses atomic create-only
  hard-link publication, leaves readers lock-free, and assigns crash staging
  cleanup to the next writer.
- Narrowed dependency support to the exact CPython 3.11/3.12 Linux x86-64,
  glibc 2.17-or-newer wheel tags. Other platforms and source builds are
  unsupported until separately reviewed.
- Added reviewed revision-1 policy-unit projections for the existing
  Cross-Platform `Filesystem Paths` and Security `Filesystem Containment`
  headings so the Authority Module, required-real fixture, and suite become
  durable semantic consumers rather than Router-only selections.
- Lifecycle remains `Blocked`; no implementation is admitted.

## 2026-08-26 - Machine Contract And Review Closure

- Replaced the duplicated prose definition-name inventory with two exact
  machine-readable proposed v11 authorities: the public schema and the closed
  operation/capability Interface. Their admitted bytes, not a mutable count or
  prose transcription, govern Milestone 1 and the atomic production cutover.
- Added the policy-unit registry to the cutover because new Cross-Platform and
  Security sidecars do not enter the canonical corpus merely by existing on
  disk.
- Split authority-object validation deliberately: the repository proves local
  object integrity and dependency kind/existence; the bound analysis kernel or
  inspection adapter proves aggregate semantic coherence.
- Required all durable store mutation to remain descriptor-relative after one
  verified Linux ext4 root open, including directory initialization and
  concurrent parent-component replacement evidence.
- Closed package targets to CPython 3.11/3.12 on the exact reviewed Linux wheel
  closure and retained domain-owned ordering rather than generic identity-byte
  ordering.
- A non-authoritative isolated `/tmp` review environment resolved the exact six
  planned package versions, and `jsonschema==4.26.0`
  `Draft202012Validator.check_schema` accepted the proposed v11 schema with a
  closed local `referencing` registry. Milestone 0 still owns hash-checked
  reproduction and acceptance of that closure.
- The replacement planning lifecycle remains `Blocked`; no implementation or
  A2 work is admitted.

## 2026-08-26 - Final Pre-Candidate Contract Corrections

- Specification review found four remaining planning defects: callers were
  asked to supply a preconstructed coverage attestation, store-root validation
  did not reject intermediate symlink components, direct package dependencies
  were specified only for the new Modules and Engine, and several Analysis
  collections still lacked frozen typed ordering keys.
- Replaced `CoverageAttestationSubmission.attestation` with an input-only
  `CoverageAttestationClaim`. The bound kernel now obtains trusted
  authorization, validates evidence and current work, and alone constructs the
  immutable attestation and handle.
- `Superseded`: opening or reopening the complete configured store path once
  with `O_NOFOLLOW`. The current design requires a canonical absolute path and
  walks every component from a trusted `/` descriptor with no-follow directory
  opens, then repeats that walk and compares device, inode, and mount identity
  before success.
- Expanded the package migration to every manifest in the closed Engine Module table and
  froze their direct internal dependency graph. The canonical A1b local
  execution boundary is a clean-venv, hash-checked external install followed
  by safe-path imports from the reviewed source tree; A1b does not silently
  select a local wheel-build backend.
- Added the closed typed key table for changes, scopes, consumer aggregation,
  reading reasons and entries, observations, dispositions, coverage decisions,
  result work, and next operations. Generic identity bytes no longer decide
  domain order, grouping, deduplication, or conflict.
- The edited proposed v11 schema adds the input-only claim and remains a closed
  operation-reachable Draft 2020-12 schema accepted by the selected validator.
  Its current SHA-256 is
  `349c06fce684accce477675a9048690100b999058fa25463b2f656028d666d50`.
- Lifecycle remains `Blocked`; the next operation remains independent exact-tree
  review of the replacement candidate. No A1b implementation or A2 work is
  admitted.

## 2026-08-26 - Final Specification Claim Repair

- Independent specification re-review found that A1B-A6 incorrectly claimed
  the future internal manifest/import closure at Milestone 0, and that the
  typed-key table used encoded-byte identity as one same-key equality test.
- Split the claims. A1B-A6 now governs only the exact external lock, target
  artifacts, isolated dependency imports, and security result in Milestone 0.
  A1B-A6I governs exact production-import/manifest equality and public
  source-tree import smoke at the atomic Milestone 3 cutover.
- Replaced byte equality in duplicate handling with owner-defined normalized
  typed-record equality. Boolean/integer and codepoint-distinct strings remain
  distinct; encoded identity bytes never decide equality or conflict.
- The fixes change no machine schema or interface bytes and no runtime path.
  Lifecycle remains `Blocked` pending renewed independent review of the final
  candidate.

## 2026-08-26 - Candidate C Admission Rejection And Replan

- Independent exact-tree review rejected candidate
  `44de7dff9c83f08b24225c82ad1b6a974f6655a9`, tree
  `24925cfce1d87f69bfde78d9f060eddae6963308`, on two high-severity
  closure defects.
- `Superseded`: Candidate C's Milestone 3 relationship migration. It admitted
  new Cross-Platform and Security declaration files without admitting the
  closed `policy-impact-registry.toml` that alone makes them compiler inputs.
- `Superseded`: Candidate C's import/manifest gate. Direct-dependency equality
  and successful import smoke did not reject imports through another Module's
  private submodules, repeating a historical A1 repair class.
- Replacement decision: retain the policy-impact registry as sole explicit
  declaration-source membership authority and require migration evidence for
  every admitted source and natural key. Do not infer relationship authority
  from paths or policy-unit membership.
- Replacement decision: each Engine Module manifest owns one public import
  root beside its requirements and Python range. One AST-backed Standards
  Verifier contract enforces exact roots across every production cross-Module
  import; package initializers remain symbol-surface authority, and import smoke
  remains separate importability evidence.
- The two corrections retain separate owners and negative fixtures but enter
  one replacement planning candidate because either blocks the exact C-R-T-S
  admission chain. No Bash checker or copied package/symbol allowlist is added.
- The proposed v11 schema and interface contract remain byte-identical. No
  runtime, package manifest, relationship registry, fixture, A1, or A2
  implementation changed. Lifecycle remains `Blocked` pending independent
  exact-tree review of candidate C-prime.

## 2026-08-26 - Candidate C-Prime Admission Rejection And Replan

- Independent exact-tree review rejected candidate
  `ecdf5a55588d18d068a513d910959ccbd9c65f71`, tree
  `ec19cb2c02a67f96229176302d5dbcd3f4964022`, on two high-severity
  public-package closure findings.
- `Superseded`: C-prime's module-path-only import rule. Python may satisfy
  `from public_root import private_child` by implicitly loading a child module
  even though the AST `ImportFrom.module` equals the public root.
- `Superseded`: C-prime's package migration inventory. It listed manifests and
  verifier artifacts without dispositioning every affected public root,
  repository entrypoint, and existing production private-import consumer.
- Replacement decision: manifests own one public root and exact repository
  entrypoints; root initializers own names through one closed, statically
  resolvable `__all__` profile. The verifier checks both imported modules and
  root-form names, rejects cross-Module star/dynamic imports, verifies runtime
  binding separately, and rejects Git-indexed non-test Python without an owner.
- Replacement decision: add a revision-1 projection of the existing
  Dependencies `Requirement And Ownership` heading and map every package
  contract artifact plus every current private-import update or retirement.
  The canonical graph-query and Git-reachability scripts become Verifier-owned
  repository entrypoints rather than ambient-path exceptions.
- The proposed v11 schema and interface remain byte-identical. No runtime,
  package manifest, policy unit, relationship, fixture, A1, or A2 implementation
  changed. Lifecycle remains `Blocked` pending independent review of C2.

## 2026-08-26 - Candidate C2 Admission Rejection And Replan

- Candidate C2 `c2aea75c85800aec6ac00fcc3b2690f8629845ab`, tree
  `19074828c41ac1c2d8814578f08604106112ad1c`, passed independent
  Specification review and failed independent Standards review on four
  high-severity closure findings.
- `Superseded`: C2's entrypoint rule treated files outside the package root as
  own-Module importers and smoked only roots/exports. Verifier entrypoints must
  call canonical-root adapters and execute from outside the checkout under
  safe-path mode with only the checkout root on `PYTHONPATH`.
- `Superseded`: C2's Authority dependency graph declared only Identity while
  requiring canonical v11 record validation. Authority now declares Contracts
  directly and delegates embedded named-definition validation to it; Authority
  retains its closed internal envelope/payload, identity, dependency-kind,
  object-local, and DAG invariants.
- `Superseded`: C2's cutover write set admitted attestation files without the
  closed attestation-source registry. The registry and exact owner-local
  Dependencies, Cross-Platform, and Security sources now participate in the
  atomic coverage renewal.
- `Superseded`: the prior Router projections omitted Commit while prescribing
  commit creation, exact parentage, history, and terminal lifecycle operations.
  The current route selects Commit together with Planning, Implementation,
  Verification, Documentation, Build, Tooling, Architecture, Contracts,
  Dependencies, Licensing, Security, Diagnostics, Library, Persistence,
  Generated Contract, Concurrency, Resilience, Release, and Cross-Platform.
  IPC, Language Binding, and A2 remain unselected for the exact in-process A1b
  boundary.
- The proposed v11 schema and interface remain byte-identical. No runtime,
  package manifest, policy unit, relationship, coverage source, fixture, A1, or
  A2 implementation changed. Lifecycle remains `Blocked` pending independent
  exact-tree review of C3.

## 2026-08-26 - Candidate C3 Admission Rejection And Replan

- Independent exact-tree Specification review rejected candidate C3
  `ebc75340781bf032164d93817edca7c5a04ba892`, tree
  `389b6134b1971ea4b290c041b9508cdf22439e02`, on three high-severity
  closure findings. One blocking review is sufficient to reject admission; the
  still-running Standards review was stopped without becoming evidence.
- `Superseded`: C3's coverage sequence froze the horizon before registering the
  new owner-local attestation sources. C4 creates and registers every source,
  freezes the complete coverage authority, then derives requirements, renews
  attestations, and compiles certificates.
- `Superseded`: C3's public snapshot and navigation inspections referenced
  `AnalysisVersions` while their immutable stored records omitted analysis-only
  provider and authorization fields. Supplying those fields ambiently would
  break cold reconstruction; copying them into snapshots would create unrelated
  invalidation. C4 instead adds exact object-specific public `SnapshotVersions`
  and `NavigationVersions` records matching stored authority.
- `Superseded`: C3's Milestone 1 evidence named only historical equality and
  pattern regressions. C4 adds the complete feature-driven semantic scenario
  and mutation matrix required by the brief. The direct selected `jsonschema`
  validator remains the oracle; the repository does not implement or claim to
  re-certify Draft 2020-12.
- The exact proposed v11 schema changes only to replace overbroad snapshot and
  navigation provenance with the object-specific version records. The
  resulting schema SHA-256 is
  `d40332050e163bdbd5e60f505eab2f698ebdfb7d4248a636e44c7a0772248eba`;
  the operation Interface is unchanged. No runtime, package manifest, policy unit,
  relationship, coverage source, fixture, A1, or A2 implementation changed.
  Lifecycle remains `Blocked` pending independent exact-tree review of C4.

## 2026-08-26 - Candidate C4 Admission Rejection And C5 Replan

- Candidate C4 `b92ed7828982723d0118294ea1a09f30001ad25e`, tree
  `125b53038737628af82271a2eee6ec29aa8b6bf6`, is `Rejected` and
  `Superseded`. Historical replan review found that its object-specific version
  records remained copied umbrella authority, ContentSnapshot still mixed
  capture with semantic interpretation, the generic repository acquired domain
  identity/decoding responsibility, and provider/authorization authority was
  broader than existing-result replay required.
- The accepted project-agnostic authority-scope, declaration-authority, and
  material-invalidation standards at commit
  `396144ad9a75c948484d1e564fab73c857bd6f4d` confirm that this is a systemic
  design defect rather than a missing version field.
- Replacement decision: ContentSnapshot contains only captured content and
  capture semantics. One StandardsAuthorityView references exact
  owner-produced semantic authority without acquiring its lifecycle. Domain
  Modules return AuthorityBoundValues, and the composing kernel derives each
  operation's exact ExecutionClosure by traversing stored direct references.
- Replacement decision: the immutable repository owns envelope integrity and
  direct lookup. Registered domain Modules own semantic identity, decoding, and
  object-local invariants. Provider and authorization authorities participate
  only in transitions that create new decisions; replay of an existing result
  requires only its persisted closure.
- `Superseded`: all C4 `SnapshotVersions`, `NavigationVersions`,
  `AnalysisVersions`, generic VersionMap, snapshot-as-query authority, copied
  dependency lists, and ambient authority-completion decisions.
- The proposed machine schema is replaced atomically at v11; no v12 or
  compatibility path is introduced. Its proposed SHA-256 is
  `d5362c1c8d2a6ea2db469065b2c29cc293e61d2e637ec5b71045c8f54139c3c7`.
  The operation/capability Interface remains byte-identical at
  `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
- No production runtime, package, manifest, policy, relationship, coverage,
  fixture, A1, or A2 implementation changed. Lifecycle remains `Blocked`
  pending independent exact-tree review of C5 through the direct C5-R-T-S
  chain.

## 2026-08-26 - Candidate C5 Admission Rejection And C6 Replan

- Candidate C5 `4f69f9940b806ca602f44dab7aa00c1df4db8abd`, tree
  `88f963e33240415e891182a7e3891db4386e87f3`, is `Rejected` and
  `Superseded`. Independent design review found that its ContentSnapshot still
  retained source Git identity, its AnalysisRoot and results retained complete
  base/proposed views, and its analysis closure covered current projection but
  not every advertised valid transition.
- `Superseded`: C5's direct Authority-to-Contracts dependency. Authority now
  owns only its small closed envelope proof. Authority and Contracts have no
  dependency in either direction; explicitly injected owner codec sets own
  semantic payload construction, validation, dependency extraction, identity,
  and decoding.
- `Superseded`: C5's ambient codec and required-role membership. C6 freezes the
  exact owner/kind/payload/identity/dependency inventory, the stable
  role-kind requirements and coherence-rule IDs within one separately stored
  Engine-owned operation contract for each of route, read, related, and
  analysis. Their union is derived evidence only. No aggregate operation
  profile, separate role catalog, or discovery mechanism is admitted.
- `Superseded`: C5's Git/manifest-specific canonical snapshot fields. Capture
  Adapters validate source consistency, construct one source-neutral selected
  content record, and discard commit, tree, Adapter, tracking, inclusion,
  revision, and worktree observations. Locator-only changes cannot invalidate
  semantic results.
- `Superseded`: C5's complete-view analysis identity. AnalysisState stores
  narrow context, dependency-valid decisions, and a role- and side-qualified
  transition-closed ExecutionClosure. Complete accepted/proposed views remain
  prepare inputs and are omitted from state and result projections.
- The proposed v11 schema is revised only where required by those source-neutral
  snapshot and material-analysis contracts. Its proposed SHA-256 is
  `71f59fe47aa857f2692c8ba5569fb2890816888742d4416cc2c1021d40fae843`;
  the operation/capability Interface remains byte-identical at
  `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
  No runtime, package manifest, policy unit, relationship, coverage source,
  fixture, A1, or A2 implementation changed. Lifecycle remains `Blocked`
  pending independent exact-tree review of C6 through the direct C6-R-T-S
  chain.

## 2026-08-27 - Serial Planning Protocol Correction

- Trigger: repository history from 2026-08-23 through 2026-08-26 showed a
  self-reinforcing administrative commit loop. The active plan had taken
  ownership of Git parentage and commit cadence through its C6-R-T-S protocol,
  despite canonical Planning, Implementation, and Commit guidance assigning
  commit boundaries to coherent outcomes.
- `Superseded`: the complete C6-R-T-S direct-child chain, exact-HEAD admission,
  intervening-commit invalidation, sole-change review-report rule, standalone
  admit/start/verify/accept commits, and Milestone-3-parent requirement.
- Replacement: review binds explicitly identified material content. A later
  reviewer report, lifecycle record, or unrelated commit does not invalidate
  unchanged reviewed semantics. A material semantic change does require a new
  consolidated review.
- Lifecycle changes are applied in the serial integration working tree and
  recorded with the first substantive implementation slice, a material replan,
  an accepted implementation boundary, or final acceptance evidence.
- Review findings are collected for one review round before the integration
  owner revises the plan. One blocking finding still rejects admission, but it
  does not create a mandatory commit chain.
- A1b work is serial. The Concurrent Plan Integration profile is not applicable;
  no stale-proposal coordination or state-only Git mechanism is authorized.
- Existing history remains unchanged. Any history rewrite requires separate
  explicit authority under Commit.
- A focused registered Python guardrail remains the next corrective slice. Its
  attempted preflight correctly showed that changing a registered suite
  invalidates affected coverage, so that slice must include the exact coverage
  audit and renewal rather than silently updating an attestation.
- No new verifier or Bash behavior is authorized. A1b remains `Blocked` pending
  the guardrail and consolidated review of the replacement design. No A1b
  runtime or A2 implementation is authorized by this correction.

## 2026-08-27 - Serial Planning Guardrail And Coverage Renewal

- Added the project-agnostic Planning rule that plans own semantic work and
  lifecycle but do not prescribe Git count, cadence, parentage, topology,
  exact-HEAD review, or standalone lifecycle commits. Commit retains ownership
  of coherent commit boundaries.
- Advanced `workflow.planning.milestones-and-slices` from semantic revision 1
  to 2 and projected the rule through the existing Planning prompt, template,
  consolidation suite, and typed decision fixture. No new suite, fixture
  authority, verifier, or Bash behavior was introduced.
- Added the two missing Commit relationships from
  `workflow.commit.per-commit-boundary` to the existing Planning fixture and
  suite. The compiled graph changes from 251 to 253 relationships without
  removing an edge.
- Froze the resulting provider-v3 horizon, reviewed every one of the 44 policy
  subjects, and renewed all 44 exact attestations. The requirement mapping,
  consumer dispositions, authorization, and acceptance gates are recorded in
  [serial-plan-commit-boundary-guardrail.md](reports/serial-plan-commit-boundary-guardrail.md).
- `A1B-020` is `controlled`. A1b remains `Blocked`; the next slice is one
  consolidated review of the complete C7 replacement design. No A1b runtime or
  A2 implementation is authorized by this outcome.

## 2026-08-27 - Candidate C6 Rejection And C7 Consolidated Replan

- C6 is `Rejected` and `Superseded`. Consolidated design review found
  unresolved operation/trust contracts, structural snapshot identity beyond
  material file content, speculative platform and storage-migration scope,
  duplicated SQL/object-kind authority, and closure over hypothetical future
  transitions.
- Historical review confirmed that direct cold inspection, owner-local codecs,
  structural dependency derivation, closed package/import membership, atomic
  public cutover, and one immutable analysis state remain valid. C7 retains
  those decisions and replaces only the defective repository, capture,
  operation, closure, and consumed-trust contracts.
- C7 selects one in-memory Adapter and one SQLite schema-v1 Adapter. SQLite
  stores only `(handle, envelope)`; the envelope owns object kind. Application
  ID is `1397047601`, user version is `1`, busy timeout is 5000 milliseconds
  without retry, and runtime support is capability-based rather than bound to
  an implementation-preserving SQLite patch release.
- C7 replaces structural snapshots with exact-list `ContentSnapshotV2` values
  whose identity is only sorted logical Unicode-scalar paths and exact bytes.
  Git and Linux/ext4 Adapters validate source endpoints and discard locator,
  filesystem, mode, directory, symlink, and capture observations.
- C7 replaces repeated dependency payloads with roots-only
  `ExecutionClosureV2`. Four Engine-owned executable
  `OperationAuthorityContractV2` values own exact roles and structural edges.
  Owner-local exported codec sets remain semantic authority; Verification
  derives aggregate evidence instead of introducing a central codec manifest.
- C7 removes aggregate provider/authorization views and stores exact consumed
  `ProviderAuthorityV1` and `AuthorizationGrantV1` objects only in successful
  child states. Existing states replay without live trust services, and current
  state does not pre-authorize hypothetical successors.
- The proposed public interface versions remain v11/request-v3/result-v3 and
  handle v4 because no C6 public cutover occurred. The revised proposed schema
  SHA-256 is
  `518cc75e915e25b579f6ec4c08255a8277a8cc46854e4848575bbb7ae0b306b6`;
  the interface SHA-256 remains
  `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
- The A1b ADR, active plan, identity/version matrix, schema/domain audit,
  consumer inventory, policy-impact migration, SQLite audit, issue records,
  write sets, evidence gates, and re-plan triggers now agree with C7. The C6
  authority reports are explicitly historical.
- No production runtime, package manifest, normative policy, relationship,
  coverage attestation, A1, or A2 implementation changed. A1b remains
  `Blocked` pending one content-bound review of this complete planning set.

## 2026-08-27 - C7 Admission Rejection And Contract Closure Replan

- Independent review rejected commit
  `748d30f778ba04ddbf33e3b82fb8031cf947c815`, tree
  `e581dc5b17079f230ebf9df8aa0dc94e003aa95b`. The plan remains `Blocked` and
  no A1b implementation is admitted.
- The review retained SQLite schema v1, exact logical-path/raw-byte snapshots,
  roots-only closure, owner-local codec sets, and direct consumed trust as the
  simpler maintainable architecture. No return to C6 or new architecture
  variant is authorized.
- Removed the migration report's residual working-tree/first-commit topology
  rule. The semantic cutover remains atomic while Commit continues to own
  coherent repository boundaries.
- Closed `authority-envelope.v1` as exact identity-v2 canonical typed bytes over
  six fields, exact two-field dependency references, closed grammars, sorted
  unique dependencies, unknown-field rejection, and a 67,108,864-byte bound.
- Closed SQLite recovery around the default repository-local store, verified
  backup, offline non-overwriting restore to an absent store, new-Engine
  selection, unchanged-former-store rollback, failed-restore isolation, and
  operator-owned retention/deletion.
- Selected a capability-checked Linux `strace` syscall-injection harness as the
  test-only during-commit oracle. Production keeps standard-library `sqlite3`;
  the harness must prove injection at real `fsync` or `fdatasync` and cannot use
  sleeps, retries, or probabilistic repetition.
- Closed every operation role-to-kind/cardinality pair, removed the phantom
  decision kind and every analysis-to-routing dependency, and enumerated the
  exact dynamic analysis roles and structural dependencies.
- Replaced opaque authorization/revocation digests with exact issuer,
  principal, action, typed subject, capability, contract, evidence, immutable
  not-revoked, and allow fields plus explicit typed outcomes.
- Removed `stale` and `incomplete` from the proposed A1b rejection algebra.
  Pending work remains a `PendingResult`; immutable A1b analysis has no temporal
  stale result.
- Removed the unowned analysis contract/schema `7/4` umbrella. Analysis payload,
  identity, handle, result, and operation compatibility remain independently
  versioned by their actual owners.
- The revised proposed schema SHA-256 is
  `bd618af35fc7280805cabe8adaeebfba5e1def0cbf6b3e334e91563f2435bca8`;
  the interface SHA-256 remains
  `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
- No production runtime, package manifest, normative policy, relationship,
  coverage attestation, A1, or A2 implementation changed. The next operation is
  one content-bound review of the corrected complete C7 planning content.

## 2026-08-27 - Corrected-C7 Admission Rejection And Typed Contract Replan

- Independent review rejected commit
  `ac362dc5f6ca2ac51c9b593cecde3639f4a883fb`, tree
  `88d6f49805fbe0f9e328b1dc9e9981afe11efbdf`. The plan remains `Blocked`; no
  A1b implementation is admitted.
- The review accepted the C7 architecture, SQLite recovery lifecycle,
  operation role/cardinality closure, result algebra, version ownership, and
  demonstrated `strace` interruption mechanism. It found four remaining
  contract-closure defects rather than a reason to return to C6 or redesign
  storage.
- Superseded the generic lower-kebab/version-suffix envelope grammar and the
  prior six-field representation. The envelope now has seven exact fields,
  including structural `envelope_kind` and integer `envelope_version`.
  Object-kind and payload-contract values are opaque domain-owned strings;
  Authority performs structural dispatch and exact comparison without
  semantic inference or Unicode normalization.
- Froze exact closed `AuthorizationGrantV1`, tagged
  `AuthorizationSubjectV1`, and `EvidenceReferenceV1` shapes. Evidence
  uniqueness is keyed only by provider contract, provider-contract version,
  and evidence ID, so a repeated logical key rejects regardless of digest.
- Froze the four operation compatibility selectors at route/read/related/
  analysis v2 and separated them from each stored record's
  `operation-authority-contract:sha256:` semantic identity.
- Expanded the test-only `strace` decision to bind Ubuntu Noble source version
  `6.8-0ubuntu2`, exact binary/source/executable hashes, authoritative package
  copyright and LGPL-2.1 text hashes, intended host-only use, and the current
  no-bundling/no-redistribution obligation decision.
- The proposed public schema and interface did not change. Their SHA-256
  values remain
  `bd618af35fc7280805cabe8adaeebfba5e1def0cbf6b3e334e91563f2435bca8` and
  `8d4adb47f90f0c8168873d89578b292c728badad7334d5f15c15125279ec6b00`.
- No production runtime, package manifest, normative policy, relationship,
  coverage attestation, A1, or A2 implementation changed. The next operation
  remains one content-bound review of the complete corrected C7 planning
  content.

## 2026-08-27 - Typed Operation Compatibility And Opaque Identity Replan

- Independent review rejected commit
  `ee7f2a47b5497112f3c8ce81c1ed45de3921bab9`, tree
  `6277f388e92e5b9fcc729745e73b6fbda5c9a6d8`. The plan remains `Blocked`; no
  A1b implementation is admitted.
- The review accepted the exact `strace` provenance and typed authorization
  algebra. It found that Authority still parsed a generic semantic-ID grammar
  and that active version summaries confused operation compatibility with the
  shared operation-record payload contract.
- Historical review confirmed that encoded operation selectors first appeared
  in unimplemented C6 planning. They have no retained runtime or persisted-state
  consumer. Their operation and revision components duplicate a typed pair and
  introduce avoidable parsing and mismatch states.
- `Superseded`: the four encoded `operation-contract.<operation>.v2` selector
  strings. `OperationAuthorityContractV2` now carries one typed `operation` and
  positive `compatibility_revision`; the initial exact keys are `(route, 2)`,
  `(read, 2)`, `(related, 2)`, and `(analysis, 2)`. Revisions are immutable,
  monotonically allocated per operation, may have gaps, and are supported only
  through explicit key membership rather than numeric ranges.
- `Superseded`: generic Authority ownership of semantic-ID grammar and
  object-kind/prefix agreement. Authority treats semantic IDs as opaque
  nonempty Unicode-scalar strings and requires exact handle/envelope/reference
  equality. Owner codecs validate and recompute their IDs.
- Separated the shared `operation-authority-contract.v2` payload format from
  exact semantic identity under
  `coding-standards:operation-authority-contract-identity:v1` and from each
  operation's typed compatibility key. Representation-only changes cannot
  invalidate semantic identity without an owner-proved material effect.
- Resolved the operation-edge ownership contradiction. Operation records own
  operation, compatibility, role, kind, and cardinality. Owner codecs own
  allowed direct-dependency kinds and exact extracted references. Engine owns
  one generic coherence algorithm. The structural dependency matrix is derived
  verification evidence, not payload authority or a second catalog.
- The proposed public schema and interface remain byte-identical. No production
  runtime, package manifest, normative policy, relationship, coverage
  attestation, A1, or A2 implementation changed. The next operation is one
  content-bound review of this corrected complete C7 planning content.
## 2026-08-27 - Corrected-C7 Admission And Milestone 0 Start

- Independent review accepted commit
  `36dd75790b2f08a6e66624ccae4f8530bc111a92`, tree
  `19e1b0f329c3d83988a703775309ebcc0fe8d4b0`, with no Standards or
  Specification findings after the operation-authority summary correction.
- The reviewer-owned decision is recorded in
  `reports/a1b-plan-admission.md`. It satisfies A1B-A6P for the exact selected
  dependency and required-real test-oracle provenance while leaving A1B-A6L
  pending final acceptance.
- Applied the admitted `Blocked` to `Planned` operation, then started the
  serial plan with `Planned` to `Active`. No concurrent-integration profile,
  mutable plan head, or Git-topology protocol applies.
- Began Milestone 0 in the same coherent implementation outcome by adding the
  isolated stdlib-only identity Module and exact dependency lock boundary.
- Accepted A1 production imports and behavior remain outside the Milestone 0
  write set.

## 2026-08-27 - Milestone 0 Implemented

- Added the stdlib-only `standards_identity` package with immutable array and
  object inputs, exact codepoint-preserving encoding, typed invalid outcomes,
  the reviewed identity-v2 hash frame, and seven focused fixtures.
- Added the `standards_contracts` dependency manifest, complete hash lock,
  install instructions, and three dependency-resolution tests without adding
  contract-compiler behavior or changing accepted A1 imports.
- Fresh CPython 3.11.14 and 3.12.3 environments installed the lock with
  `--require-hashes --only-binary=:all:`. Both selected the reviewed `rpds-py`
  wheel, passed import/version checks, and reported no broken requirements.
- Reproduced every installed license-file hash. The exact six-package OSV
  batch returned no known vulnerability on 2026-08-27. No third-party artifact
  was copied or bundled.
- Both runtimes passed all 10 isolated foundation tests. The accepted A1
  baseline passed 82 Analysis, 46 Engine, and 18 Metadata tests; contract
  validation and generated freshness passed unchanged.
- The canonical complete checkpoint passed 225 of 225 declarative suites and
  all 53 retained Bash checkers. Ruff, plan validation, lifecycle fixtures,
  and diff checks passed.
- Milestone 0 is `Implemented`; A1B-A6 is satisfied. A1B-A6L remains pending
  final independent exact-lock acceptance. The next substantive work is the
  isolated Milestone 1 contract compiler.

## 2026-08-27 - Milestone 1 Implemented

- Added the isolated `standards_contracts` compiler around the selected
  `jsonschema.Draft202012Validator` and a retrieval-free local `referencing`
  registry. The Module owns stable diagnostics, public-root reachability, the
  closed projection profile, and immutable staging projections without
  implementing JSON Schema validation semantics.
- The admitted v11 schema and interface compile to an exact 140-definition
  reachable closure. Unreachable definitions, unsupported reachable keywords,
  remote references, incomplete operation roots, and capability-map drift
  reject before projection.
- Eighteen focused tests passed on both CPython 3.11.14 and 3.12.3. They cover
  the complete admitted feature matrix, all JSON value families, Draft
  mathematical-number and codepoint string equality, stable diagnostics,
  direct-validator agreement, and one local mutation for every admitted
  projection semantic.
- Generated staging models are immutable, preserve omission separately from
  explicit values, validate through the compiled runtime, and contain no
  validation-keyword interpreter or default injection. Agent-tool projections
  are deterministic and complete for all four public operations.
- Accepted A1 contract generation and validation remained unchanged and green.
  The canonical checkpoint passed 225 of 225 declarative suites. Ruff and diff
  hygiene passed; no policy, facade, production contract, or A2 artifact
  changed.
- Milestone 1 is `Implemented`. The next substantive work is the isolated
  Milestone 2 authority repository and capture adapters.

## 2026-08-28 - Identity Integer Boundary Replan

- Milestone 2 envelope testing reproduced a latent Milestone 0 defect:
  identity-v2 integer encoding used `str(int)` and therefore failed above
  CPython's ambient 4300-decimal-digit limit despite the admitted contract's
  implementation-size-independent integer grammar.
- The active Milestone 2 write set now admits only the identity encoder and its
  focused test for this prerequisite correction. The selected correction uses
  module-local fixed-width decimal chunks, preserves all formerly valid bytes,
  and does not disable or mutate CPython's process-wide safety limit.
- A contract limit, global interpreter mutation, Authority-local workaround,
  or alternate identity version is rejected because each would weaken or
  duplicate the existing owner contract. Authority implementation remains
  isolated until this correction passes on CPython 3.11 and 3.12.
- The local chunked encoder passed focused tests on CPython 3.11.14 and 3.12.3
  for positive and negative 5001-digit values. Boundary samples through the
  largest ambiently convertible values reproduce the former bytes exactly;
  Ruff, plan validation, and diff hygiene pass.

## 2026-08-28 - Milestone 2 Implemented

- Added `standards_authority` with one canonical seven-field envelope, opaque
  semantic references, explicit immutable owner-codec sets, direct resolution,
  owner identity/dependency verification, and iterative cycle-safe transitive
  closure. A 1500-object fixture proves closure does not depend on Python
  recursion depth.
- Added in-memory and SQLite schema-v1 stores. SQLite persists only canonical
  envelope BLOBs under typed-handle keys, rejects update/delete and parallel
  schema authority, uses explicit `BEGIN IMMEDIATE`, and enforces application
  ID 1397047601, user version 1, DELETE/EXTRA/NORMAL, trusted-schema off, and a
  5000-millisecond busy bound without application retry.
- Added verified backup and non-overwriting offline restore, source-preserving
  failure behavior, rollback-store retention, private descriptor-validated
  default composition, cold-process reconstruction, and direct corruption,
  contention, idempotence, and collision evidence.
- Added exact-list Git and native ext4 capture. Git hash-verifies selected
  commit/tree/blob objects and explicitly mapped gitlinks; native capture uses
  retained no-follow descriptors, double reads, mount/casefold checks, and an
  independent complete binding rewalk. Both produce the same path/raw-byte
  ContentSnapshot identity and exclude locator, mode, and metadata changes.
- Added roots-only ExecutionClosure and immutable AuthorityBoundValue. Closure
  payloads retain only role/side-qualified roots while their identities bind
  the exact dependency set derived from owner references.
- Thirty-seven focused tests passed on CPython 3.11.14 with SQLite 3.50.4 and
  CPython 3.12.3 with SQLite 3.45.1. Both report serialized THREADSAFE=1. The
  capability-selected required-real oracle injected SIGKILL at `fsync` on 3.11
  and `fdatasync` on 3.12 after an exact pre-commit barrier; each cold reopen
  recovered to an absent row and converged on retry.
- Required-real evidence reproduced Ubuntu `strace` 6.8-0ubuntu2 amd64, the
  admitted executable, copyright, and LGPL-2.1 hashes, and the admitted source
  artifact provenance. The tool remains host-only and unbundled.
- The complete 225-suite declarative checkpoint, Ruff, and diff hygiene pass.
  Generated SQLite databases and journal forms are Gitignored. No accepted A1
  production import, public contract, domain codec, facade, or A2 behavior
  changed.
- Milestone 2 is `Implemented`. The next substantive work is the atomic
  Milestone 3 v11 production cutover.

## 2026-08-28 - Milestone 3 Coverage Authority Replan

- Policy-impact migration verification exposed two reachable coverage identity
  generations: the accepted C7 v3 owner codecs and the old v2 static compiler
  still used by the Standards Verifier.
- The v2 path also treated repository provenance text as sufficient authority,
  bypassing C7's exact authorization evidence and revocation contracts.
- `Superseded`: retaining the v2 static coverage compiler beside C7 and renewing
  its requirement handles. Repository attestation files are now claim inputs,
  not self-validating certificates or a second identity authority.
- Replacement: one closed repository authorization/revocation authority feeds
  one Analysis-owned v3 constructor used by Engine composition and Verifier.
  Every old v2 coverage identity, export, and fallback is removed in the same
  Milestone 3 cutover.
- Added only the authorization and revocation authority files to the Milestone
  3 write set. The ADR, public v11 contract, A2 scope, and horizon-freeze order
  are unchanged. No separate lifecycle or commit-topology operation applies.

## 2026-08-28 - Milestone 3 Generated-Handle Claim Replan

- Final diff hygiene found one representation-only trailing line in a
  registered Analysis source after repository claims had been mechanically
  rewritten to current coverage-requirement hashes. The byte change altered the
  global horizon digest and would have required replacing every authored claim
  again despite no consumer-coverage change.
- `Superseded`: repository claim schema v3, where each authored TOML record
  copied a generated `coverage-requirement:sha256` handle and every generated
  handle change required source mutation.
- Replacement: repository claim schema v4 names the stable policy-unit subject
  and exact semantic compatibility versions. Analysis resolves the current
  requirement and remains the sole constructor of grants, attestations, and
  certificates. Exact hashes remain in immutable snapshots and generated proof
  objects only.
- Interactive v11 submissions continue to reference their current generated
  requirement handles. No public schema, ADR, policy meaning, relationship
  contract, A2 behavior, or new authority registry changes.
- Representation-only bytes may regenerate exact proof identities without
  claim edits. A material subject or coverage-contract incompatibility still
  rejects and requires explicit review.

## 2026-08-28 - Milestone 3 Implemented

- Replaced the accepted A1 production boundary atomically with the admitted
  v11 generated algebra, codepoint-preserving identity encoding, dependency-
  backed Draft validator, exact immutable authority repository, reference-only
  standards views, roots-only execution closures, and immutable branchable
  analysis state.
- Every domain now exports its owner codec set. Public package roots,
  manifests, direct imports, generated prelude, and repository entrypoints form
  one statically verified dependency closure. Retired validators, generic
  serializers, snapshot/session implementations, compatibility models, and old
  coverage identities are absent.
- Policy-impact migration compiles the closed accepted and proposed sources and
  dispositions every natural key without a mutable count oracle. Cross-
  Platform, Security, and Requirement And Ownership projections are registered
  with their exact implementation and evidence consumers.
- Repository coverage claims use schema v4 stable subjects and semantic
  contract selectors. They contain no generated requirement or proof hash.
  Analysis derives the current v3 grant, attestation, and certificate objects;
  Engine and Verifier consume the same result. Exact required subjects equal
  certificate subjects.
- Focused package evidence passed: Identity 8, Contracts 18, Authority 38,
  Applicability 12, Metadata 17, Graph Engine 37, Policy Impact 9, Standards
  Graph 2, Analysis 66, Standards Engine 30, and Standards Verifier 385 tests.
  The required-real SQLite interruption case passed through the admitted host
  oracle.
- All 226 registered declarative suites and all 53 retained migration checkers
  passed. Generated freshness, plan validation, changed-file Ruff, and diff
  hygiene passed.
- Milestone 3 is `Implemented`. Automated objectives are satisfied. A1B-A6L
  licensing confirmation and A1B-A11 independent content acceptance remain the
  only pending objective claims; A2 remains inactive.

## 2026-08-28 - Milestone 3 Content Review Rejection And Replan

- Independent Licensing, Standards, and Specification review rejected commit
  `d61172168101744a83f708e1da73bd3eb956ce1d`, tree
  `8fd3b6fd9370a38952c115190069b6a288f77f2f`.
- External package, artifact, license, notice, non-bundling, security, and
  required-real `strace` selections matched admission. A1B-A6L remains pending
  because the implemented internal dependency boundary did not.
- Confirmed systemic defects: Authority named downstream codec kinds; no
  production owner returned `AuthorityBoundValue`; required `1..1` closure
  roots could collapse duplicates; provider inputs lost side/role
  qualification; Verifier depended directly on Engine; the retired Engine
  generator remained; dynamic-import aliases bypassed verification; documented
  entrypoints failed; clean-environment execution and genuine public-object
  cold reconstruction were not proved; and two retired suites remained.
- `Superseded`: the Milestone 3 `Implemented` claim and candidate `d6117216`.
  The immutable commit remains historical evidence but is not an accepted A1b
  boundary.
- Replacement: reopen Milestone 3 as one coordinated correction slice owned by
  Authority, domain Modules, Engine composition, Analysis coverage, Contracts
  projection, package verification, suite migration, and cold-process evidence.
  No compatibility layer, fixed catalog count, new Bash checker, A2 work, or
  change to the admitted third-party selection is authorized.

## 2026-08-28 - Milestone 3 Corrected Implementation

- Removed Authority's downstream codec catalog and composed execution-closure
  support from injected owner codec sets. Domain owners now return bound
  authority values; exact role cardinality is checked before projection, and
  provider inputs retain side and role qualification.
- Moved deterministic public-contract projection generation to Contracts,
  removed the retired Engine generator, and corrected every affected semantic
  relationship disposition. The two unregistered superseded suites were
  deleted.
- Removed Verifier's direct Engine dependency. Static coverage now uses the
  Analysis-owned repository composition path, while package verification
  rejects dynamic-import aliases and executes every public root, export, and
  repository entrypoint in both admitted clean Python environments.
- Added genuine fresh-interpreter reconstruction for every public handle
  family using persisted SQLite authority and public composition. The evidence
  found and removed one lazy import of the retired handwritten Engine model.
- Focused package suites passed, including 33 Engine and 386 Verifier tests.
  The capability-selected required-real SQLite interruption test passed. All
  226 registered suites, all 53 retained migration checkers, generated
  freshness, plan validation, changed-file Ruff, and diff hygiene passed.
- A1B-023, A1B-024, and A1B-025 are resolved. Milestone 3 is `Implemented`.
  The next operation is to commit this coherent content and record that exact
  commit and tree for Milestone 4 review; A2 remains inactive.

## 2026-08-28 - Milestone 4 Implementation Candidate

- Recorded corrected A1b implementation commit
  `3da674c1227a8ff6544e846a252a21a255854f49`, tree
  `63d55780f77c7f1af64762b6363b8ba776e7fd51`, as the exact content subject for
  independent acceptance.
- The candidate report consolidates the implemented contract, identity,
  authority, operation, trust, migration, coverage, and verification evidence
  without introducing a second machine authority or a mutable catalog-count
  oracle.
- Milestone 4 is `Active`. A1B-A6L and A1B-A11 remain pending independent
  review; the ADR remains `Proposed`, the plan remains `Active`, and A2 remains
  inactive.

## 2026-08-28 - Milestone 4 Content Review Rejection

- Independent Standards and Specification review rejected implementation
  `3da674c1227a8ff6544e846a252a21a255854f49`, tree
  `63d55780f77c7f1af64762b6363b8ba776e7fd51`.
- A1B-A6L passed: the implemented lock, package and source hashes, license and
  notice authorities, non-bundling disposition, and required-real Linux oracle
  match the admitted selection.
- A1B-A11 failed. The consolidated findings cover exact authorization and
  provider input selection, analysis root qualification, source-independent
  persisted reconstruction, atomic no-overwrite recovery publication,
  alternate import machinery, real entrypoint operations, implementation-
  consumer migration closure, and executable operation/codec evidence.
- `Superseded`: the candidate's Milestone 3 `Implemented` claim and Milestone 4
  `Active` state. Milestone 3 is reopened as one correction slice; Milestone 4
  returns to `Planned`. The admitted C7 architecture, v11 public algebra,
  dependency selection, and A2 exclusion are unchanged.

## 2026-08-28 - Typed Suite-Input Horizon Replan Trigger

- The strict implementation migration now derives every current and retired
  production path and passes exact node, relationship, and disposition closure
  without a mutable count oracle.
- Engine reconstruction then failed on the intentionally retired
  `standards_analysis` fact source. The registered authority-reconstruction
  suite asserts that path is absent, but Coverage recursively treats every
  path-like suite value as a required readable input.
- Treating every missing path as a valid absence would hide misspelled or
  unavailable required evidence. Teaching Analysis the meaning of each
  Verifier check would duplicate authority in the opposite direction.
- A1B-027 records the replacement requirement: one typed, owner-produced suite
  input projection must identify required-present content and intentional
  absence. Coverage consumes that projection and fingerprints the declared
  state. Milestone 3 remains active; Milestone 4 and A2 remain unavailable.

## 2026-08-28 - Milestone 3 Consolidated Correction Verification

- Implemented every A1B-026 correction as one coordinated boundary: injected
  typed authorization contracts, exact provider input-role selection,
  transition-qualified analysis authority, source-independent persisted Engine
  composition, atomic no-overwrite restore, typed executable entrypoint
  operations, closed alternate import-machinery detection, complete changed-
  source migration, and executable operation/codec evidence.
- Resolved A1B-027 through a Verifier-owned, versioned suite-input projection.
  Present registered inputs bind exact bytes; intentional-absence assertions
  bind explicit repository state; missing required inputs still reject.
  Analysis verifies projection closure and freshness without interpreting
  check-specific suite contracts.
- Advanced the coverage horizon provider to version 4, renewed every exact
  current repository coverage claim, and added the new implementation paths to
  catalog, relationship, and migration authority without a fixed cardinality
  oracle.
- Focused package verification passed: Graph Engine 37, Applicability 12,
  Authority 39 with one capability-selected skip, Contracts 18, Graph 2,
  Identity 8, Metadata 17, Policy Impact 9, Analysis 66, Engine 35, and
  Verifier 394.
- Generated freshness passed. All 226 registered declarative suites and all 53
  retained Bash migration checkers passed. `git diff --check` passed.
- A1B-027 is `Resolved` and Milestone 3 is `Implemented`. A1B-026 remains
  `Active` only until a new content-bound implementation review. Milestone 4
  remains `Planned`; the ADR remains `Proposed`; A2 remains inactive.

## 2026-08-28 - Corrected Implementation Content Review Rejection

- Independent Standards and Specification review rejected implementation
  `ead04bc55c6cb43b0be66d31371d9fc909c3355c`, tree
  `3a5f623c0891a1dd744f4a9280f9f31f6d2ae811`.
- The suite-input projection duplicated check semantics and omitted transitive
  inventory, repository-index, package-source, and entrypoint authority. The
  accepted replacement gives each check one input-closure Interface and makes
  Analysis the sole serialized-manifest contract owner.
- Package verification still admitted reflective import acquisition through
  `sys.modules`, built isolated fixtures from ambient working-directory files,
  and classified Git copies as retired sources. Operation/codec evidence proved
  membership but not declared cardinalities and dependency contracts.
- The replacement import contract is a closed governed-source AST profile. It
  rejects explicit and reflective runtime-import constructs while avoiding the
  false claim that static analysis can decide adversarial arbitrary Python
  computation.
- `Superseded`: the Milestone 3 `Implemented` claim for `ead04bc5`. Milestone 3
  returns to `Active`; A1B-027 is reopened and A1B-028 records the consolidated
  correction. A1B-A6L remains satisfied. Milestone 4 and A2 remain unavailable.

## 2026-08-28 - Milestone 3 Derived Checker Inventory Replan

- The corrected check-owned authority test names one exact transitive retained
  checker input. The temporary checker inventory therefore gains one executable
  inbound reference while every checker source and dependency remains
  unchanged.
- `Superseded`: excluding the checker inventory from the Milestone 3 write set
  after changing a source scanned by its existing generator.
- Replacement: admit only the generated inventory and permit only the one
  mechanically affected row's inbound-reference fields to change. Checker
  source, dependency fields, graph artifacts, and unrelated rows remain
  byte-identical.
- This replan changes no checker behavior, migration architecture, C7 design,
  semantic horizon, A2 scope, or commit topology. Milestone 3 remains `Active`.

## 2026-08-28 - Milestone 3 Derived Checker Graph Replan

- Generated freshness proved that the newly recorded executable inbound
  reference also belongs in the temporary checker dependency graph. It adds no
  checker dependency and changes no strongly connected component or wave.
- `Superseded`: requiring every checker graph artifact to remain byte-identical
  while admitting a new executable reference already owned by that graph.
- Replacement: admit the three generated graph projections. Permit exactly one
  executable-reference edge, its target node's inbound count, and its
  component's inbound-file list to change. Dependency topology, checker source,
  and all unrelated graph records remain byte-identical.
- This is generated-evidence closure only. C7 architecture, semantic horizon,
  A2 scope, and Milestone 3 lifecycle remain unchanged.

## 2026-08-28 - Milestone 3 Exact-Index And Evidence Replan

- Consolidated content review retained the corrected C7 architecture but
  rejected the staged correction because indexed fixtures copied working-tree
  bytes, migration comparison did not select the staged index or sanitize Git
  repository overrides, and the governed-source AST profile rejected benign
  shadowed capability names.
- The same review found incomplete executable evidence: operation roles lacked
  wrong-kind regressions, not every owner codec extractor was exercised, and
  the suite-input matrix omitted tracked removal, stale suite-definition,
  stale registry, and transitive-byte cases.
- `Superseded`: independent Git calls in package and migration verification,
  name-only capability matching, and the incomplete evidence matrix.
- Replacement: one internal sanitized Git-index adapter owns exact membership,
  staged comparison, and staged-blob materialization; the AST profile resolves
  lexical shadowing and limits reflective rejection to known capability
  provenance; owner and integration tests derive complete role, codec, and
  manifest evidence from executable contracts without copied catalogs.
- Coverage claims remain unrenewed. Milestone 3 and A1B-028 remain `Active`;
  Milestone 4 and A2 remain unavailable.

## 2026-08-28 - Milestone 3 Content Review Rejection And Authority Replan

- Independent content review retained staged comparison, exact indexed-blob
  materialization, Git copy/rename semantics, operation-role wrong-kind proof,
  the suite-input mutation matrix, and complete changed-source migration.
- It rejected coverage renewal because Analysis still owned a second Git-index
  reader, Numeric Lifecycle omitted its inventory and checker-source inputs,
  Analysis codec evidence copied the production tuple, and the AST scope model
  admitted a class-body bypass while rejecting a benign comprehension binding.
- `Superseded`: Verifier-local Git-index ownership, accidental cross-check input
  coverage, the copied Analysis codec tuple, and unordered class/comprehension
  scope approximation.
- Replacement: Standards Authority owns one sanitized Git-index adapter used by
  Analysis and Verifier; Numeric Lifecycle reads and declares the canonical
  generated inventory plus its selected checker sources; owner tests derive
  directly from `ANALYSIS_CODECS`; and the AST profile uses ordered binding
  provenance with explicit comprehension scope.
- Provider-v5 coverage claims remain unrenewed. Milestone 3 and A1B-028 remain
  `Active`; Milestone 4 and A2 remain unavailable.

## 2026-08-28 - Milestone 3 Corrected Content Review

- Focused independent review accepted the shared Standards Authority Git-index
  owner, Numeric Lifecycle authority closure, production-derived Analysis codec
  evidence, policy-impact migration, and generated evidence.
- The first review found one remaining Python lookup defect: methods and class
  comprehensions incorrectly treated the containing class namespace as a
  lexical parent. The scanner now skips non-current class scopes while retaining
  ordered lookup in a directly executing class body.
- Regressions prove nested methods and class comprehensions cannot hide a
  module-level `sys.modules` capability, direct class-body ordering remains
  correct, and benign comprehension bindings remain accepted.
- The focused re-review found no blocker and authorized provider-v5 coverage
  renewal. Milestone 3 remains `Active` until renewed certificate equality and
  the complete verification checkpoint pass.

## 2026-08-28 - Milestone 3 Implemented

- All current attestations were explicitly renewed against the frozen
  provider-v5 horizon. Required coverage subjects equal valid certificate
  subjects, and the Verifier no longer reports uncovered owners.
- Focused verification passed: Authority 39 with one capability-selected skip,
  Analysis 66, Engine 36, Verifier 414, and the complete A1b public-cutover
  dependency closure.
- Generated freshness passed. The complete checkpoint passed all 226 registered
  declarative suites and all 53 retained Bash migration checkers. Diff hygiene
  passed.
- A1B-026, A1B-027, and A1B-028 are `Resolved`; Milestone 3 is `Implemented`.
  Milestone 4 is `Active` for one content-bound acceptance review. The ADR
  remains `Proposed`, final A1b acceptance remains pending, and A2 remains
  unavailable.

## 2026-08-28 - Final Content Review Rejection And Binding-Lifetime Replan

- Independent Standards and Specification review rejected implementation
  `8b8a4b481d4e330e118f879a862d2a3630c85f84`, tree
  `3435dd4e7cd5784913389f53fb90d6fbb06b73d7`.
- The governed-source scanner treated textual Store and Del positions as
  bindings. It therefore hid a capability used on an assignment RHS, retained
  a deleted binding, and rejected a benign exception alias.
- Three Verifier fixture and migration paths executed Git outside the shared
  sanitized Standards Authority Adapter; an ambient `GIT_DIR` override changed
  a passing suite into an untyped subprocess failure.
- `Superseded`: the Milestone 3 `Implemented` decision and the provider-v5
  coverage claim as final acceptance evidence. The authored attestations remain
  current inputs but must be revalidated after the corrected horizon is frozen.
- Replacement: typed execution-ordered bind/unbind events, one exported typed
  Git command Adapter used by every Verifier Git call, exact focused and public
  suite regressions, then regenerated migration, generated evidence, and
  coverage. A1B-028 and Milestone 3 return to `Active`; Milestone 4 and A2 are
  unavailable.

## 2026-08-29 - Milestone 3 Binding And Git-Authority Correction Implemented

- The governed-source scanner now models execution-ordered bind and unbind
  events. Assignment right-hand sides execute before target binding, deletion
  removes a binding, exception aliases expire after their handler, and loaded
  names inside assignment targets are not misclassified as bindings.
- Standards Authority exports the one sanitized typed Git command Adapter.
  Every Verifier fixture, entrypoint, and accepted-tree Git operation uses it;
  inherited `GIT_*` overrides no longer change authority or escape typed
  diagnostics.
- The 24 focused regressions and the hostile-ambient-Git public-cutover suites
  passed under the exact locked CPython 3.11 and 3.12 environments.
- Authority 39, Analysis 66, Engine 36, and Verifier 421 tests passed.
  Generated freshness passed, followed by all 226 registered declarative
  suites and all 53 retained Bash migration checkers. Diff hygiene passed.
- A1B-028 is `Resolved`; the reopened automated objectives are `satisfied`;
  Milestone 3 is `Implemented`; Milestone 4 is `Active` for A1B-A11. The ADR
  remains `Proposed`, final A1b acceptance remains pending, and A2 remains
  unavailable.
