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
