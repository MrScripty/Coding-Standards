# Plan: Standards Engine A1b Contract And Authority Foundations

**Plan status:** `Active`

**Current phase:** Milestone 4 content-bound acceptance

**Next slice:** Identify the coherent Milestone 3 implementation boundary and
obtain content-bound licensing, Standards, and Specification acceptance

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Replace A1's duplicated contract semantics, generic normalized identity
serialization, fragmented immutable-authority storage, and copied version bags
with one dependency-backed contract compiler, one codepoint-preserving identity
encoder, one generic immutable SQLite object repository with domain-owned
semantic decoding, one reference-only StandardsAuthorityView, roots-only
operation ExecutionClosures, exact leaf-file ContentSnapshots, and one
generated public request/result algebra.
Preserve the four-operation read-only Standards Engine and immutable analysis
kernel while making every issued handle directly resolvable in a cold process.
Complete independent content-bound acceptance before any A2 review or
implementation begins.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1B-A1 | The canonical schema is checked and every accepted instance is validated through the exact selected `jsonschema.Draft202012Validator`; the complete admitted feature matrix and known A1 regressions agree between the direct validator and production Adapter without a repository keyword interpreter. | `contract` | `not-applicable` | `automated` | `satisfied` | [Contract profile audit](reports/a1b-contract-profile-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A2 | Every public operation request and result has one complete reachable schema closure, generated models preserve it, stale projections fail, and unsupported reachable projection semantics reject. | `contract` | `not-applicable` | `automated` | `satisfied` | [Contract profile audit](reports/a1b-contract-profile-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A3 | JSON Schema validation, applicability equality, identity encoding, and domain ordering/deduplication pass owner-specific fixtures without one domain deciding another. | `focused` | `not-applicable` | `automated` | `satisfied` | [Contract profile audit](reports/a1b-contract-profile-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A4 | Every advertised content snapshot, authority view, execution closure, analysis, navigation, policy, relationship, coverage, context, requirement, and observation handle directly reconstructs its owner-typed object in a fresh process after source and process mutation; snapshot identity contains only exact logical paths and bytes; analysis roots exclude complete views; existing results require no live provider or authorization service; and SQLite durability, deterministic during-commit interruption, verified backup, non-overwriting offline restore, rollback selection, and cold reopen pass on the admitted Linux ext4 profile. | `system` | `required-real` | `automated` | `satisfied` | [Authority closure audit](reports/a1b-authority-closure-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A4C | Every operation closure stores only unique role- and side-qualified roots and derives its transitive dependency set through owner-declared references: the exact selected operation contract is included, consumed provider and authorization objects enter only successful successor states, unused view authority is excluded, ordering is deterministic, cycles reject, and material authority mutation changes only dependent identities. | `integration` | `not-applicable` | `automated` | `satisfied` | [Authority closure audit](reports/a1b-authority-closure-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A5 | Public `query`, `prepare`, `resolve`, and `inspect` accept and return only generated v11 contract values; internal domain models and dependency exceptions cannot cross the facade. | `integration` | `not-applicable` | `automated` | `satisfied` | [Contract profile audit](reports/a1b-contract-profile-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A6 | The selected external dependency closure is exact, hash-checked, reproducible on Linux x86-64 with glibc 2.17 or newer for CPython 3.11 and 3.12, imports from an isolated install, and is free of unresolved blocking security findings. | `release-artifact` | `required-real` | `automated` | `satisfied` | [Milestone 0 dependency provenance](reports/a1b-dependency-provenance.md) and isolated lock tests on CPython 3.11/3.12 |
| A1B-A6I | Every Engine Module manifest exactly declares its production direct imports, Python range, public import root, and repository entrypoints; package roots expose one statically resolvable `__all__`; all production cross-Module and entrypoint imports resolve through those roots and exports; private, alternate-root, star, dynamic, or unowned imports reject; and every public export and exact entrypoint executes in both clean environments with only the admitted external lock. | `integration` | `required-real` | `automated` | `satisfied` | [Consumer dispositions](reports/a1b-consumer-dispositions.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A6P | Before implementation starts, an independent planning review accepts the selected package and test-oracle artifact/source identity, exact hashes, copyright/notice and license authorities, intended use, compatibility, and current non-bundling disposition. | `release-artifact` | `not-applicable` | `manual` | `satisfied` | [Corrected-C7 plan admission](reports/a1b-plan-admission.md) |
| A1B-A6L | Final independent review proves the implemented exact lock and required-real test-oracle provenance match the admitted selection and introduce no changed license or notice obligation. | `release-artifact` | `not-applicable` | `manual` | `pending` | Pending final acceptance review |
| A1B-A7 | No old validator, generated keyword interpreter, generic NFC identity encoder, snapshot compiler, split or directory object store, owner map, scan, compatibility path, copied version bag, ambient authority-completion path, aggregate operation-profile identity, complete-view analysis identity, Git-lineage or filesystem-metadata snapshot field, speculative migration/export path, or old-version fallback remains reachable. | `integration` | `not-applicable` | `automated` | `satisfied` | [Authority closure audit](reports/a1b-authority-closure-audit.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A8 | Accepted and proposed policy-impact catalogs compile; every changed implementation node and relationship has a disposition; selected consumers equal disposition subjects; required coverage subjects equal valid certificate subjects. | `integration` | `not-applicable` | `automated` | `satisfied` | [Consumer dispositions](reports/a1b-consumer-dispositions.md) and [cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A9 | Existing routing, analysis, coverage, reading, rendering, and inspection behavior remains valid except for declared contract, handle, identity, and storage replacements. | `integration` | `not-applicable` | `automated` | `satisfied` | [Cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A10 | All focused package tests, registered declarative suites, retained migration checkers, generated freshness, plan checks, and diff hygiene pass without mutable catalog-count assertions. | `integration` | `not-applicable` | `automated` | `satisfied` | [Cutover evidence](reports/a1b-cutover-evidence.md) |
| A1B-A11 | One clean implementation boundary has a reviewer-owned acceptance record confirming every claim, migration deletion, consumer disposition, and exclusion. The review binds the identified content; later evidence or lifecycle recording does not invalidate unchanged reviewed semantics. | `release-artifact` | `not-applicable` | `manual` | `pending` | Pending final acceptance report |

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
  inspectable objects through in-memory and SQLite adapters, owning its small
  internal envelope proof, and delegating semantic identity and payload
  decoding to explicitly injected owner codec sets. Authority and Contracts
  have no dependency in either direction.
- Exact-file ContentSnapshots containing only logical Unicode-scalar path
  components and raw bytes, reference-only StandardsAuthorityViews, and
  roots-only operation ExecutionClosures composed from owner-produced
  AuthorityBoundValues. Git locators, filesystem metadata, capture receipts,
  and complete base/proposed views are excluded from derived state identity.
- One Engine-owned `OperationAuthorityContractV2` for each of route, read,
  related, and analysis, with exact required and allowed dynamic roles; no
  second role profile or central codec manifest.
- Direct `ProviderAuthorityV1` and `AuthorizationGrantV1` objects consumed by
  successful analysis transitions; no aggregate provider/authorization view.
- Contract v11, request v3, result projection v3, public handle v4, authority
  envelope v1, identity encoding v2, and independently scoped owner payload,
  identity, operation, and result versions. The former umbrella analysis
  contract/schema pair has no A1b successor.
- The exact proposed v11 public schema and interface contract in
  `reports/a1-contract-v11.schema.json` and `reports/a1-interface-v11.toml`.
- Domain-owned ordering, deduplication, normalization, and identity records.
- Complete repository-controlled consumer migration and deletion of
  superseded implementations.
- Supplemental node-catalog and source-owned relationship migration for
  created, retained, and retired implementation artifacts.
- Registered Python verification, dependency and licensing evidence, coverage
  reconciliation, and content-bound acceptance.
- Manifest-owned public import roots and repository entrypoints,
  initializer-owned static export closure, and one AST-backed verifier contract
  for every governed production cross-Module import.

### Out Of Scope

- A2 authoring, mutation, proposal heads, canonical application, or recovery.
- A compatibility layer, old-state converter, dual reader/writer, old-contract
  fallback, or identity migration tool.
- SQLite schema migration, semantic export/import, checked-in database files,
  in-place destructive restore, Engine-owned backup retention/deletion, or use
  of SQLite as authored policy authority. A1b admits schema v1 only; verified
  backup and offline restore to an absent store are operational recovery.
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
- macOS, Windows, non-ext4 durable storage, casefolded filesystems, non-UTF-8
  repository names, special files, or transient-mutation detection stronger
  than exact endpoint revalidation.
- Runtime remote schema retrieval, custom vocabularies, format assertion, or
  dynamic references.
- New or extended Bash verification.
- Plan C external-project baselines.

## Constraints And Assumptions

### Constraints

- This plan is unavailable while `Blocked`. Independent review must accept the
  current material planning semantics before any implementation edit.
- The accepted standards-recovery boundary is the comparison base. After
  admission, lifecycle transitions are applied in the serial integration
  working tree before implementation and committed with the first substantive
  implementation outcome; they do not require independent commits.
- Foundation Modules may be implemented and tested only against private staging
  fixtures. They may not modify or become dependencies of accepted production
  A1 before the atomic Milestone 3 cutover.
- Milestones 0 through 2 are ordered evidence checkpoints. They do not prescribe
  commit count, parentage, or cadence. Commit boundaries follow Commit and each
  commit must remain a coherent green outcome. Milestone 3 includes every
  production consumer, catalog/relationship migration, and final coverage
  update in one coordinated replacement boundary.
- Public replacement is atomic. Old and new production authorities never
  coexist in an accepted runtime.
- Dependency installation and verification use the accepted hash-checked lock.
  Ambient alternate packages are not evidence.
- Generated freshness and semantic correctness are separate gates.
- Repository coverage claims bind stable subjects and semantic contract
  versions, never generated requirement, view, attestation, or certificate
  hashes. Exact handles are derived after every horizon-affecting input is
  frozen. A representation-only byte change may regenerate those handles but
  does not require an authored claim change.
- Mutable repository totals are not acceptance oracles.

### Assumptions

- [Consumer and state inventory](reports/consumer-and-state-inventory.md) found
  no external consumer and no retained A1 persisted state.
- The bounded repository snapshot remains small enough for one exact file-list
  capture and SQLite transaction; Milestone 2 measures the admitted capture.
- The reviewed dependency resolution supports Linux x86-64 with glibc 2.17 or
  newer for CPython 3.11 and 3.12; Milestone 0 reproduces both exact native
  wheel tags. Other targets are unsupported.
- SQLite support is capability-based: runtime 3.31.0 or newer,
  `THREADSAFE=1`, Python `sqlite3.threadsafety == 3`, exact pragma
  acceptance, backup support, and the full required-real transaction suite.
  Acceptance records exact tested releases; patch releases do not enter
  semantic identity.
- The required-real Linux environment supplies a capability-checked `strace`
  syscall-injection oracle for deterministic interruption at SQLite `fsync` or
  `fdatasync`. Its exact release is evidence, not runtime semantic identity;
  production Authority retains only standard-library `sqlite3`.
- The durable authority and native capture adapters support Linux ext4 only in
  A1b. The in-memory adapter remains repository-neutral; another operating
  system or durable filesystem requires a separate capability and durability
  decision.
- Existing applicability NFC semantics are domain-owned and remain unchanged
  after byte-level dependency proof.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Preserve the four-operation read-only facade and immutable analysis kernel. | Accepted A1 architecture | [A1 ADR](../../decisions/standards-engine-navigation-analysis.md) | None |
| Use `jsonschema.Draft202012Validator` as the sole Draft validator behind one deep project adapter. | Contracts and Dependencies | [A1b ADR](../../decisions/standards-engine-a1b.md), [dependency decision](reports/dependency-and-dialect-decision.md) | Local validator and generated keyword interpreter |
| Keep schema validation, applicability equality, identity encoding, and domain ordering separate. | Owning domain Modules | [Schema/domain audit](reports/schema-and-domain-contract-audit.md) | Generic serializer as cross-domain semantics |
| Use codepoint-preserving identity encoding v2; domain Modules own typed identity records and any semantic normalization. | Identity and domain owners | [Identity/version matrix](reports/identity-version-object-matrix.md) | Recursive NFC identity encoding v1 |
| Capture an exact requested file list into `ContentSnapshotV2` using only logical Unicode-scalar paths and raw bytes; discard Git, filesystem, and Adapter observations after validation; compose one reference-only StandardsAuthorityView; require domain Modules to return AuthorityBoundValues; store only role- and side-qualified execution roots; and derive the transitive dependency set structurally. | Architecture, Authority, Engine composition, and domain owners | [C7 design](reports/c7-design-proposal.md), [C6/C7 history](reports/c6-c7-design-history-research.md), [identity/version matrix](reports/identity-version-object-matrix.md), and [consumer inventory](reports/consumer-and-state-inventory.md) | C4 object-specific version bags, C5 Git lineage, C6 structural snapshot entries and transition-future closure, snapshot-as-query authority, copied dependency lists, and umbrella invalidation |
| Directly store every inspectable object through one closed immutable authority Interface backed by in-memory and SQLite adapters; encode the exact bounded authority envelope with structural kind `authority-envelope` and integer version `1`; persist only `(handle, envelope)` because the envelope owns kind; let the repository own envelope/dependency integrity while explicitly injected owner codec sets own opaque identifier dispatch, semantic construction, identity, dependency extraction, and decoding; keep Authority and Contracts independent; and admit SQLite schema v1 with verified non-overwriting backup/restore but without migration or semantic export. | Architecture, Persistence, Authority, Resilience, and domain owners | [C7 design](reports/c7-design-proposal.md), [SQLite audit](reports/c7-sqlite-storage-audit.md), and [consumer inventory](reports/consumer-and-state-inventory.md) | Three-root storage, C6 directory/hard-link publication, duplicate SQL kind authority, generic semantic ownership or identifier grammar, owner maps, scans, caches, schema-mediated domain dispatch, duplicated schema interpretation, destructive restore, or Engine-owned retention |
| Store four executable Engine-owned `OperationAuthorityContractV2` values with typed per-operation compatibility revisions and exact role-to-kind/cardinality requirements; analysis has no routing role and dispositions remain fields of `analysis-root.v1`; keep direct-dependency semantics and codec sets with their domain owners, inject the closed codec tuple at composition, and let Engine apply one generic coherence algorithm; verify the aggregate inventory mechanically rather than creating encoded selectors, a central codec authority, or a second edge catalog. | Engine composition and domain owners | [C7 design](reports/c7-design-proposal.md) | Aggregate operation profiles, encoded selector strings, ambient required-role policy, central codec manifests, separate role or edge catalogs, phantom decision kinds, routing-to-analysis leakage, and cross-operation invalidation |
| Persist analysis state as narrow context plus dependency-valid decisions and roots-only material closure. Provider and authorization Adapters produce direct `ProviderAuthorityV1` and exact subject/action/evidence/revocation-bound `AuthorizationGrantV1` objects only for successful child states; deterministic no-observation stores nothing. Existing states replay without live trust services. | Analysis and Engine composition | [C7 design](reports/c7-design-proposal.md) | C5 complete-view state identity, C6 hypothetical-future transition closure, aggregate trust views, opaque authorization digests, and ambient trust replay |
| Support one exact Linux ext4 durable-store and native-capture contract with descriptor-relative no-follow access, exact endpoint revalidation, and typed unsupported outcomes. | Cross-Platform and Security | [A1b ADR](../../decisions/standards-engine-a1b.md), [C7 design](reports/c7-design-proposal.md), [SQLite audit](reports/c7-sqlite-storage-audit.md), and [migration plan](reports/policy-impact-migration-plan.md) | Operating-system-name inference, path-based validation/use, and unproved macOS or Windows portability |
| Remove all schema `x-standards-engine-*` annotations; use one closed interface contract and domain-owned executable contracts. | Contracts and domain owners | [Schema/domain audit](reports/schema-and-domain-contract-audit.md) | Mixed machine prose in public schema |
| Build isolated foundations, then perform one atomic production v11 cutover. | Planning and integration owner | This plan | Partial schema/generated production cutover |
| Migrate implementation catalog and policy-impact relationships in the atomic cutover. | Policy Impact and coverage owners | [Migration plan](reports/policy-impact-migration-plan.md) | Treating implementation artifact changes as incidental paths |
| Keep `policy-impact-registry.toml` as the sole closed declaration-source membership authority and register every admitted source explicitly. | Policy Impact | [Migration plan](reports/policy-impact-migration-plan.md) | Filesystem discovery or policy-unit-derived relationship registration |
| Make each Engine Module manifest own one public import root and its repository entrypoints; make the root's closed `__all__` expression own exported names; require entrypoints to call canonical-root adapters; and enforce all three with one AST-backed Standards Verifier contract plus safe-path execution. | Dependencies and Verification | [Dependency decision](reports/dependency-and-dialect-decision.md), [consumer inventory](reports/consumer-and-state-inventory.md) | Root-only smoke, script-directory imports, generator-only checks, implicit Python child-module loading, and copied package or symbol allowlists |
| Keep A2 inactive through independent A1b acceptance. | Planning | Accepted standards recovery | Direct progression to authoring |
| Execute A1b serially; the Concurrent Plan Integration profile is not applicable. Review binds identified semantic content, not later Git ancestry. Collect a review round's findings before revising, and record lifecycle changes with substantive implementation, material replanning, accepted implementation boundaries, or final acceptance evidence rather than state-only commits. | Planning, Implementation, and Commit | [Planning](../../../workflows/planning.md), [Implementation](../../../workflows/implementation.md), [Commit](../../../workflows/commit.md), and this corrective replan | C6-R-T-S direct-child protocol, exact-HEAD admission, intervening-commit invalidation, and standalone lifecycle commits |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Generated files are current | Freshness | Deterministic projection `--check` | Canonical schema, interface contract, and compiler | Semantic correctness | Stale generated output diagnostic |
| Contract adapter is correct | External-contract adapter | Production adapter regressions and schema self-check | Selected validator API and canonical contract | Independent Draft re-certification | Exact keyword/path diagnostic |
| Projection closure is complete | Public shape | Reachability compiler and public-operation fixtures | Canonical v11 schema and closed interface contract | Constructs outside the admitted projection profile | Unsupported reachable construct or unreachable public definition |
| Identity is representation preserving | Content identity | Exact codepoint fixtures and domain identity records | Identity v2 contract | Domain semantic equality | NFC-equivalent inputs remain distinct unless owner normalizes |
| Domain equality/order is local | Domain semantics | Applicability and analysis owner fixtures | Each domain contract | Generic identity-byte ordering or equality | Generic identity bytes cannot decide semantic equality or order |
| Persisted envelope is exact | Storage representation | Canonical decode/re-encode, exact structural kind/version dispatch, opaque owner identifier, ordering, unknown-field, bound, and byte-collision fixtures | Authority envelope kind `authority-envelope`, version `1`, plus identity-v2 encoding | Domain payload meaning or generic identifier grammar | Noncanonical, oversized, duplicate, unsorted, malformed, unknown-version, or same-handle/different-byte cases reach their exact typed outcomes |
| Cold reconstruction is complete | Persisted authority | Fresh process with SQLite store path and handle only | Persisted object envelope and dependencies | In-process caches, authored database files, or unavailable durable filesystem | Missing is unavailable; contradiction is invalid |
| SQLite publication and recovery are durable | Required-real persistence | Real Adapter stages, capability-checked `strace` sync-syscall injection, cold reopen, verified backup, and offline restore to an absent destination | SQLite atomic-commit contract, exact runtime capability profile, and operator-selected store lifecycle | Custom VFS, probabilistic kill, destructive overwrite, semantic transfer, or Engine-owned retention | Unsupported oracle blocks acceptance; failed restore leaves live source unchanged |
| Operation authority is exact | Material semantic dependency | Roots-only traversal of AuthorityBoundValue direct references | Executable owner codec sets, Engine operation contracts, and reference-only StandardsAuthorityView | Handwritten closure, central codec manifest, version bag, hypothetical future authority, or full-view invalidation | Missing consumed dependency, included unused dependency, cycle, or owner mismatch rejects |
| Public algebra is exhaustive | Public path | Real facade/tool calls using exported generated types | Public operation closure | Internal domain values crossing the facade | Unhandled domain result is a programming error |
| External dependency is reproducible | Release artifact | Hash-checked isolated install and dependency import smoke | Reviewed lock, artifact hashes, provenance, licenses | Unreviewed platform, Python, wheel, or source build | Missing or mismatched artifact blocks installation |
| Internal Module closure is exact | Source-tree integration | AST-derived production-import/manifest equality, root-export resolution, governed-source ownership, and isolated root/export/entrypoint execution | Manifest-owned requirements, roots, repository entrypoints, package `__all__`, and reviewed checkout | Independently published or installed local distributions | Missing, transitive-only, unused, ambient, alternate-root, undeclared, private-child, root-plus-private-child, star, dynamic, or unowned production import fails |
| Policy-impact migration is complete | Semantic consumers | Accepted/proposed compile, exact admitted-source registration, and exact disposition equality | Closed policy-impact registry, compiled relationship authority, and independent horizon | Empty impact without certified coverage | Unregistered source, unmapped node, edge, consumer, or coverage subject blocks |
| Negative fixture reaches intended rule | Negative evidence | Otherwise-valid fixture and exact diagnostic assertion | Owning typed diagnostic | Failure at another precondition | Failure at another precondition rejects the test |

A1b does not use agreement between local implementations as external Draft
conformance and does not run the complete upstream corpus.

## Systemic Finding Audit

- **Invariant families:** contract validation and projection, identity encoding,
  semantic ordering/deduplication, exact leaf-file capture, authority
  composition, roots-only execution closure, consumed trust, immutable SQLite
  object resolution, package
  dependency/public-export closure, and implementation-consumer coverage.
- **Inventories:** [schema/domain audit](reports/schema-and-domain-contract-audit.md),
  [identity/version matrix](reports/identity-version-object-matrix.md),
  [C7 design](reports/c7-design-proposal.md),
  [SQLite audit](reports/c7-sqlite-storage-audit.md),
  [C6/C7 history](reports/c6-c7-design-history-research.md),
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

Candidate C3 `ebc75340781bf032164d93817edca7c5a04ba892`, tree
`389b6134b1971ea4b290c041b9508cdf22439e02`, is `Superseded` by C4.
Its Specification review found that coverage sources were sequenced after the
horizon freeze, snapshot and navigation records could not reconstruct their
advertised public version projections without ambient authority, and the
contract Adapter evidence covered historical regressions rather than every
admitted semantic feature.

Candidate C4 `b92ed7828982723d0118294ea1a09f30001ad25e`, tree
`125b53038737628af82271a2eee6ec29aa8b6bf6`, is `Rejected` and
`Superseded` by C5. Historical replan review found that its object-specific
version records remained copied umbrella authority, its snapshot still mixed
content capture with semantic interpretation, its generic repository acquired
domain identity/decoding responsibility, and provider/authorization authority
remained broader than existing-result replay required. The accepted
authority-scope and version-scope standards at commit `396144ad` require the
systemic replacement recorded in
[authority composition and execution closure](reports/authority-composition-and-execution-closure.md).

Candidate C5 `4f69f9940b806ca602f44dab7aa00c1df4db8abd`, tree
`88f963e33240415e891182a7e3891db4386e87f3`, is `Rejected` and
`Superseded` by C6. Its review found that source Git identity still entered the
snapshot model, analysis retained complete base/proposed views, analysis
closure covered current projection but not every advertised valid transition,
Authority and Contracts had an unnecessary dependency, and exact codec,
role-to-kind, and operation-requirement catalogs were absent. C6 replaces
those decisions without adding a package, compatibility layer, aggregate
profile, or provenance object.

C6 is `Rejected` and `Superseded` by C7. Its review found unresolved operation
and trust contracts, an over-broad structural snapshot, speculative platform
and storage-migration scope, duplicated SQL/object-kind authority, and closure
over hypothetical future transitions. C7 preserves direct inspectability,
domain-owned codecs, and structural dependency derivation while replacing the
repository, capture, operation, and consumed-trust contracts. The complete
rationale and historical cross-check are in [C7 design](reports/c7-design-proposal.md),
[SQLite audit](reports/c7-sqlite-storage-audit.md), and
[C6/C7 history](reports/c6-c7-design-history-research.md).

C7 is planned from accepted standards commit
`1d18b70d99db48317de2cc9243fc06b133d7329a`. It retains the original
standards-recovery comparison base above while replacing all C6 planning
authority. The public v11 cutover remains unimplemented, so C7 may revise the
proposed v11 machine artifacts without a compatibility layer or v12.

C7 admission candidate `748d30f778ba04ddbf33e3b82fb8031cf947c815`,
tree `e581dc5b17079f230ebf9df8aa0dc94e003aa95b`, is `Rejected` and
`Superseded` by the corrected C7 planning content. Its independent review
accepted SQLite schema v1, exact path/raw-byte snapshots, roots-only closure,
owner-local codecs, and direct consumed trust, but found that the persisted
envelope, restore lifecycle, operation role-to-kind closure, authorization
grant, commit-interruption oracle, rejection algebra, and analysis version
scope were incomplete. It also found one residual plan-owned commit-topology
instruction in the migration report. The current content corrects those
contracts without returning to C6 or creating a new architecture variant.

The C6-R-T-S direct-child protocol, exact-HEAD admission rule, standalone
admit/start transitions, and intervening-commit invalidation rule are
`Superseded`. They were plan-owned Git coordination for serial work and
conflicted with Commit's ownership of coherent commit boundaries.

Admission now uses this content-bound contract:

1. Review identifies the exact plan, ADR, reports, and dependency decision it
   evaluated, using a candidate commit/tree or artifact digests as evidence.
2. The reviewer reports all Standards and Specification findings from that
   review round before the integration owner revises material planning
   semantics. One blocking finding rejects admission; findings from the same
   round are corrected together.
3. Adding the reviewer-owned report, recording lifecycle state, or making an
   unrelated commit does not alter the reviewed subject. Only a material change
   to reviewed semantics requires another review.
4. After a review with no blocking finding, the integration owner applies the
   `Blocked` to `Planned` admission and `Planned` to `Active` start operations in
   the serial working tree before implementation. Their final lifecycle fields,
   report, and ledger evidence are committed with the first substantive
   implementation slice.
5. Verification and acceptance lifecycle changes are recorded with an accepted
   implementation boundary or final acceptance evidence, not in standalone
   state-only commits.

Commit count, parentage, branch topology, and the placement of review evidence
are governed by Commit. Existing published history is retained; changing that
history would require separate explicit rewrite authority.

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

- [x] Reproduce the exact dependency names, versions, target wheels, and hashes.
- [x] Record authoritative provenance, license files, supported targets,
  security results, and install command.
- [x] Implement identity encoding v2, domain hashing, immutable typed inputs,
  and exact codepoint/invalid-value fixtures.
- [x] Prove no accepted A1 production import or output changes.

**Acceptance gate:** Identity foundation and A1B-A6 pass; isolated package
tests and the accepted broad baseline remain green. A1B-A6L remains a distinct
manual exact-lock final-acceptance claim; A1B-A6P must already be satisfied
before start. Record the checkpoint when it materially changes current plan or
verification authority; Commit decides its coherent commit boundary.

**Status:** `Implemented`

### Milestone 1: Isolated Contract Compiler

**Goal:** Implement the contract adapter and projection compiler against the
exact admitted machine-readable v11 schema and interface contract without
changing the production schema, generated output, or facade.

**Allowed write set:**

- `tools/standards_contracts/`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [x] Implement schema self-check, retrieval-free local registry, stable errors,
  reachable closure, and projection-profile admission.
- [x] Compile the admitted `reports/a1-interface-v11.toml` and
  `reports/a1-contract-v11.schema.json` without rewriting or extending their
  public algebra. Any required shape change is a re-plan trigger.
- [x] Generate staging immutable Python and agent-tool projections without a
  keyword interpreter or default injection.
- [x] Execute every case in the feature-driven contract-semantic matrix in
  `reports/schema-and-domain-contract-audit.md` through both the direct selected
  validator and the production-intended Adapter. Cover mathematical-number,
  Unicode, object-key-order, array-order, and all-type `uniqueItems` equality;
  every admitted core, reference, primitive, composition, object, array,
  string, numeric, and annotation keyword; and every excluded dialect,
  vocabulary, extension, retrieval, reference, pattern, and projection class.
- [x] Apply one feature-local schema mutation for every admitted projection
  semantic and prove the compiled model plus affected public behavior change.
  These are Adapter/compiler tests against `jsonschema`, not a repository
  implementation or independent certification of Draft 2020-12.
- [x] Reject unsupported projection constructs and unreachable public roots.

**Acceptance gate:** A1B-A1, the isolated half of A1B-A2, and contract portions
of A1B-A3 pass while every accepted production A1 artifact remains byte
identical. Record the checkpoint when it materially changes current plan or
verification authority; Commit decides its coherent commit boundary.

**Status:** `Implemented`

### Milestone 2: Isolated Authority Repository

**Goal:** Implement exact leaf-file capture and the generic immutable-object
repository, then prove transactional SQLite publication, explicit codec
injection, roots-only dependency traversal, backup, and cold reconstruction
independently of the accepted facade.

**Allowed write set:**

- `tools/standards_authority/`
- `tools/standards_identity/standards_identity/encoding.py` and
  `tools/standards_identity/tests/test_identity.py`, solely to correct the
  reproduced CPython decimal-digit limit in identity-v2 integer encoding
- `.gitignore`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger

**Tasks:**

- [x] Replace implementation-limited integer rendering with local arbitrary-
  length decimal encoding while preserving every previously issued identity
  byte. Prove positive and negative values beyond CPython's ambient decimal-
  digit limit on both supported runtimes; do not mutate the process-wide limit.
- [x] Implement the generic envelope, explicit owner-codec-set Interface, typed
  handles, in-memory adapter, and SQLite schema-v1 adapter. The repository
  validates its closed envelope proof and direct references; the injected codec
  computes semantic identity, extracts dependencies, and decodes its payload.
  Authority does not import Contracts, and Contracts does not import Authority.
- [x] Treat envelope and reference semantic IDs as opaque nonempty Unicode-scalar
  strings inside Authority. Prove exact handle/envelope/reference comparison,
  owner-codec grammar validation and identity recomputation, empty-ID rejection,
  unknown-owner `unsupported`, owner-invalid `invalid`, and no generic ID parser
  or object-kind/prefix inference in the repository.
- [x] Encode authority envelope kind `authority-envelope`, version `1`, through
  the identity-v2 canonical typed encoder with its exact seven fields,
  two-field references, structural kind/version dispatch, exact opaque
  owner-defined object-kind/payload-contract values, ordering, unknown-field
  rejection, and 67,108,864-byte pre-decode bound. Prove that Authority does
  not normalize or infer domain meaning, plus raw-byte owner payload
  projection, noncanonical encodings, boundary sizes, and same-handle byte
  contradiction.
- [x] Store only `(handle, envelope)` in SQLite; verify the envelope's kind
  agrees with the typed handle. Implement one-transaction `put_if_absent`,
  same-ID idempotence, contradictory collision, integrity verification,
  deterministic backup, non-overwriting offline restore to an absent store,
  rollback selection, crash recovery, and cold reopen. Do not add migration,
  semantic export/import, enumeration, garbage collection, checked-in
  databases, destructive restore, or Engine-owned retention/deletion.
- [x] Freeze and verify application ID `1397047601`, user version `1`,
  DELETE journal mode, EXTRA synchronization, NORMAL locking,
  `trusted_schema=OFF`, disabled extension loading, explicit
  `BEGIN IMMEDIATE`, and a 5000-millisecond busy timeout with no retry.
- [x] Use the capability-checked Linux `strace` oracle to inject `SIGKILL` at
  the real SQLite `fsync` or `fdatasync` reached after the pre-commit barrier.
  Require trace proof of the selected syscall and reject sleeps, retries,
  probabilistic repetition, ordinary process failure, or a custom VFS as
  substitutes. Record and verify the exact executable digest, binary package,
  source descriptor and artifacts, license/notice bytes, and capability in
  required-real evidence against the admitted provenance.
- [x] Default live storage to
  `<repository-root>/.standards-engine/authority.sqlite3`. Verify backup source
  and absent destination completely; restore offline into another absent store,
  cold-verify it, and select it only through a new Engine composition. Prove
  existing/aliased/in-use destinations reject, failed restore leaves the live
  store unchanged, the former store remains selectable for rollback, and
  retention/deletion remains operator-owned.
- [x] Implement immutable `AuthorityBoundValue` and roots-only
  `ExecutionClosureV2`. Persist unique qualified roots and derive the exact
  transitive dependency set from owner-declared references. Prove missing
  dependencies, owner mismatch, contradictory content, and cycles reject while
  input ordering does not alter closure or result identity.
- [x] Implement exact-list Git and Linux-native capture adapters over
  `CaptureRequestV1`. Both construct the same `ContentSnapshotV2` containing
  only sorted `(RepositoryPathV1, exact bytes)` entries and discard commit,
  tree, Adapter, mode, tracking, inclusion, source-root, and worktree
  observations after validation.
- [x] Store and resolve ContentSnapshot plus private fixture-owned root and child
  kinds directly by handle. Domain production kinds enter only in the atomic
  cutover.
- [x] Enforce `RepositoryPathV1` as a nonempty tuple of Unicode-scalar
  components whose UTF-8 encoding is 1 through 255 bytes; reject empty, `.`,
  `..`, `/`, NUL, lone surrogate, `.git` control paths, and duplicate logical
  paths. Preserve codepoints and case; order by scalar sequence with prefixes
  first. Backslash is an ordinary Linux scalar.
- [x] For Git capture, resolve one commit OID and hash-verify every traversed
  commit, tree, and blob object; accept regular file modes only. Resolve an
  explicitly mapped gitlink through its object database and flatten only the
  requested nested file bytes. Read neither worktree nor index.
- [x] For Linux-native capture, walk from a retained `/` descriptor using
  descriptor-relative no-follow opens, retain directory/file descriptors on one
  ext4 mount, reject casefold and cross-mount traversal, read every file twice,
  then independently rewalk and require endpoint metadata and binding equality.
  Record that endpoint agreement does not prove absence of every transient
  same-user mutation.
- [x] Prove the exact requested path set equals the bootstrap-derived source
  closure. No recursive discovery, exclusions, directory entries, symlink
  entries, nested snapshot records, mode bits, `CaptureReceipt`, or locator
  fields enter snapshot identity.
- [x] Prove fresh-process reconstruction using only persisted objects, exact
  injected codec sets, and handles after source and process mutation.
- [x] Prove equal selected content captured through Git and native Adapters
  produces one ContentSnapshot identity, and locator-only or filesystem-metadata
  mutation does not change any snapshot, closure, or result identity.
- [x] Prove no enumeration, owner map, root scan, cache index, or ambient
  provider authority is needed.

**Acceptance gate:** The isolated halves of A1B-A4 and A1B-A4C pass on both
adapters.
Record the checkpoint when it materially changes current plan or verification
authority; Commit decides its coherent commit boundary.

**Status:** `Implemented`

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
- `evaluation/standards-effectiveness/policy-coverage/authorization-authority.toml`
- `evaluation/standards-effectiveness/policy-coverage/revocations.toml`
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

- [x] Promote the exact admitted planning schema and interface contract
  byte-for-byte to their canonical production paths; generate the complete
  public Python and agent-tool algebra.
- [x] Advance every identity and public contract in the identity/version matrix
  and use domain-owned typed keys for ordering and deduplication.
- [x] Route all public wire validation through `standards_contracts` and all
  public object persistence/inspection through `standards_authority` without a
  dependency between those Modules. Authority owns envelope,
  direct-reference, and DAG integrity. Each explicitly injected domain codec
  set owns its semantic record, construction, identity, dependency extraction,
  decoding, and object-local invariants.
- [x] Make Standards Engine composition create one reference-only
  StandardsAuthorityView from owner-produced semantic objects. Store one
  executable `OperationAuthorityContractV2` for each initial exact
  compatibility key `(route, 2)`, `(read, 2)`, `(related, 2)`, and
  `(analysis, 2)`. Revisions are immutable and per-operation, may contain gaps,
  and are matched only through an explicit supported-key set. Store each record
  under its independently derived semantic ID using
  `coding-standards:operation-authority-contract-identity:v1`; Authority treats
  that ID as opaque. Route requires
  metadata/routing/graph; read and related require metadata/graph; analysis
  requires metadata/graph/policy-impact/coverage.
  Each role carries its exact object kind and cardinality. Analysis allows only
  context, requirement, observation, coverage-view, coverage-requirement,
  coverage-attestation, coverage-certificate, provider-authority, and
  authorization-grant dynamic roles; it has no routing or decision role.
  Operation records do not duplicate structural edges: owner codecs own allowed
  dependency kinds and extract exact direct references, while Engine applies
  one generic coherence algorithm. Query and analysis preparation accept views,
  not content snapshots.
- [x] Prove operation compatibility and identity independently: accept explicit
  sparse and overlapping supported key sets, reject numeric-range inference and
  Boolean/nonpositive revisions, prevent reuse of one key for unequal promises,
  keep unrelated operation identities stable, require accepted and proposed
  analysis views to select the same exact semantic ID, and return `unsupported`
  for a well-formed unknown payload format or compatibility key. Prove the
  semantic identity constructor receives only the normalized material record,
  not payload/envelope/SQLite representation, and that no encoded selector
  parser, alias, or fallback exists.
- [x] Make every domain execution path return an AuthorityBoundValue. Derive and
  persist each result's exact role- and side-qualified roots, then derive its
  transitive dependency set by traversing owner-declared references. Never
  accept a caller-supplied closure or handwritten version/dependency bag.
- [x] Keep executable codec membership owner-local: each public Module root
  exports its closed codec set, composition injects the exact tuple, and the
  verifier derives facade, inventory, and dependency evidence from those
  executable owners. Do not introduce a central codec manifest.
- [x] Persist analysis as narrow context plus dependency-valid decisions and
  roots needed by the current state. Store direct `ProviderAuthorityV1` and
  `AuthorizationGrantV1` objects only when a successful transition consumes
  them; deterministic no-observation stores nothing. Pending and complete
  results omit complete views and hypothetical future-transition authority.
- [x] Require every authorization grant to bind exact issuer and revocation
  authority revisions, principal, capability, action, typed work subject,
  authorization/revocation contracts, evidence, `not-revoked` state, and allow
  decision through the exact closed `AuthorizationGrantV1`, tagged
  `AuthorizationSubjectV1`, and `EvidenceReferenceV1` shapes. Sort evidence by
  `(provider_contract, provider_contract_version, id)` and reject repeated
  logical keys regardless of digest. Prove mismatch, denial, revocation,
  missing trust, and unsupported contracts reach their distinct typed
  outcomes; do not store opaque substitute digests or admit temporal grants.
- [x] Prove included authority mutation changes every dependent closure and
  identity, excluded view-member mutation leaves unrelated identities stable,
  and existing cold inspection requires no live provider or authorization
  authority. Provider claims and authorization grants are validated against
  exact immutable inputs only while producing a successor analysis state.
- [x] Exhaustively adapt domain requests and outcomes at the facade.
- [x] Accept coverage claims as input, validate evidence and trusted execution
  authorization, and construct stored coverage attestations only inside the
  analysis kernel.
- [x] Update every manifest in the closed Module dependency table with exact
  direct requirements, the admitted Python range, one public source-tree import
  root, and its repository entrypoint scripts. Require each public-root
  `__init__.py` to define exactly one statically resolvable `__all__` through the
  closed literal-and-local-star export profile. Derive imports with Python AST,
  require exact manifest equality and source ownership, and reject imports
  below another Module's root, root-form names absent from resolved `__all__`,
  cross-Module star imports, or literal/dynamic import bypasses.
- [x] Derive all governed production Python from manifest roots and repository
  entrypoints, and reject tracked non-test Python under `tools/` that has no
  manifest owner. Assign the canonical graph query and Git-reachability scripts
  to the Standards Verifier manifest. Replace ambient or alternate-root imports
  in every exact Verifier entrypoint with canonical-root adapters.
- [x] Execute every manifest-owned public root, every resolved export, and every
  exact repository entrypoint in clean CPython 3.11 and 3.12 environments after
  installing only the admitted external lock. Use safe-path mode from outside
  the checkout with the checkout root as the sole `PYTHONPATH`; mutating
  entrypoints operate only on isolated repository fixtures.
- [x] Make generated imports a closed compiler prelude, verify their AST in
  focused compiler tests, and independently reject otherwise-valid generated
  and handwritten-facade fixtures for both `from public_root.private_child`
  and `from public_root import private_child`. Require the intended rule's exact
  diagnostic and prove that exported root names remain accepted.
- [x] Delete old validators, generated keyword walkers, generic NFC serializer,
  snapshot compiler, split and directory stores, owner maps, scans, aliases,
  copied version bags, aggregate operation profiles, complete-view analysis
  fields, structural/directory/symlink/mode/Git locator snapshot fields,
  aggregate provider/authorization views, ambient authority-completion paths,
  migration/export scaffolding, and fallbacks.
- [x] Register the Cross-Platform and Security declaration files explicitly in
  the closed policy-impact registry. Compile accepted and proposed
  catalogs/relationships; require every admitted declaration source and natural
  key to appear in migration evidence; and record every node, edge, and
  selected-consumer disposition without fixed cardinality assertions.
- [x] Reject an otherwise-valid migration fixture whose admitted relationship
  source is absent from the closed registry with the exact migration-completeness
  diagnostic; the relationship compiler remains responsible only for compiling
  its registered closed input.
- [x] Create the new owner-local Cross-Platform and Security attestation source
  files and register them, together with the updated Dependencies source, in
  the closed attestation-source registry.
- [x] Remove the v2 static coverage identity and certificate path. Treat
  repository attestation TOML as authored claims only; validate each claim
  by stable policy-unit subject, target semantic revision, horizon provider and
  version, relationship-kind contract version, applicability language version,
  and coverage-evidence contract version. Reject generated handles in authored
  claim sources. Resolve the current requirement, validate one closed
  repository authorization authority, exact evidence bytes, and exact
  revocation state, then construct the same v3 authorization grant, coverage
  attestation, and generated certificate objects used by interactive Analysis
  resolution. Engine composition and the static verifier must consume this one
  Analysis-owned result without reconstructing identities or accepting
  provenance text as authorization.
- [x] After every declaration, suite input, horizon provider, canonical corpus,
  and attestation-source registration is final, freeze the complete semantic
  horizon; then derive requirements and compile grants, attestations, and
  certificates from the stable claims. Prove a representation-only raw-byte
  change alters exact snapshot and generated proof identities without requiring
  an authored claim edit. A material subject revision, horizon
  provider/version, relationship-kind contract, applicability language,
  evidence contract, registration, or consumer-coverage change after this
  freeze invalidates compatibility and triggers re-planning.
- [x] Prove exact selected-consumer/disposition and
  requirement/certificate equality.

**Acceptance gate:** Every automated objective claim passes. Final manual
A1B-A6L and A1B-A11 remain pending content-bound acceptance.
Any required path outside this write set, any substantive ADR change, blocked
disposition, or material semantic horizon change after claim finalization is a
re-plan trigger. A generated digest or handle change alone is not. The
admitted ADR remains byte-identical and `Proposed` throughout Milestone 3;
Milestone 4 alone may change its status after content-bound acceptance.

**Status:** `Implemented`

### Milestone 4: Content-Bound Acceptance

**Goal:** Identify one clean implementation boundary, run complete evidence,
and obtain independent acceptance of its material content.

**Allowed write set:**

- `docs/plans/standards-engine-a1b/reports/a1b-implementation-candidate.md`
- `docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`
- lifecycle fields in this plan and issues, plus append-only checkpoint,
  verification, deviation, and transition records in the ledger
- ADR status only in `docs/decisions/standards-engine-a1b.md`

The final review identifies the implementation content it evaluated. Adding its
report or final lifecycle evidence afterward does not invalidate unchanged
reviewed semantics and does not require a prescribed parent/child sequence.

**Tasks:**

- [ ] Record the identified implementation commit/tree or equivalent artifact
  digests, dependency resolution,
  generated outputs, owner-local identity contracts, object kinds, authority
  views, execution closures, node/edge/consumer dispositions, coverage
  identities, and complete verification.
- [ ] Obtain independent Standards and Specification review against that
  identified content.
- [ ] Accept only with no blocked claim or consumer and a clean worktree.
- [ ] Mark the ADR and plan Accepted with the final acceptance evidence.

**Acceptance gate:** Every objective acceptance claim is satisfied.

**Status:** `Planned`

## Blockers

- No current plan-level blocker. Milestone-specific acceptance claims remain
  pending until their implementation and verification gates are reached.

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
- An inspectable value cannot use the closed SQLite object repository without
  scans, caller-maintained indexes, or ambient authority.
- An authority envelope requires another value family, an encoded size above
  67,108,864 bytes, unknown-field preservation, or non-JSON-compatible payload
  storage.
- One semantic object must be republished under another payload or envelope
  representation in the same repository, requiring representation coexistence
  or storage migration beyond the admitted single-format schema v1 boundary.
- Authority and Contracts require a dependency in either direction, or an owner
  codec cannot validate its closed semantic payload without public-wire schema
  authority.
- A codec kind, payload contract, identity domain, allowed dependency, stable
  role, role-to-kind binding, operation compatibility key, required role, or
  allowed dynamic role differs from the exact admitted executable contracts;
  compatibility aliases, branches, or decentralized revision allocation become
  necessary; or operation-specific edge policy cannot be expressed by the
  generic coherence algorithm and owner-declared direct dependencies.
- A domain cannot declare the direct semantic authorities it actually consumes,
  or the composing kernel cannot derive exact material closure without a
  handwritten version/dependency list.
- StandardsAuthorityView would need to own a domain's semantic lifecycle rather
  than reference the domain-owned authority.
- Replaying an existing result requires live provider or authorization
  authority not stored as a directly consumed immutable trust object.
- Authorization requires expiration, live temporal validity, an action or
  subject outside the closed grant variants, or evidence that cannot be
  retained as exact immutable references.
- An analysis result requires a complete accepted/proposed view, Git capture
  locator, filesystem metadata, or authority that does not affect the current
  state and projection.
- Exact-list snapshot capture is invalidated by streaming, recursive discovery,
  non-regular files, non-UTF-8 paths, or semantics beyond logical paths and raw
  bytes.
- SQLite schema migration, semantic export/import, another database engine,
  checked-in database authority, macOS, Windows, another architecture or
  filesystem, casefolding, or stronger transient-mutation guarantees become
  required.
- In-place destructive restore, automatic backup retention/deletion, or a
  required environment without the admitted deterministic Linux syscall fault
  oracle becomes necessary.
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
- Final status: `Active`
