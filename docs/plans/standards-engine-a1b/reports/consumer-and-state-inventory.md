# A1b Consumer And Persisted-State Inventory

**Status:** Proposed planning evidence

**Inventory base:** commit `c4408363752b10060f631247f3e2f1fa26eae003`,
tree `84477150bd368a168dd04da3770de55c23bbb817`

## Purpose

This inventory decides whether A1b requires compatibility or state migration
and maps every repository-controlled consumer of the contract, identity, and
authority foundations. It is not a fixed file-count oracle. New consumers or
persisted states are classified by identity and ownership, not by preserving a
cardinality.

## Public Consumer Inventory

| Surface | Consumers at the inventory base | Ownership | Migration disposition |
| --- | --- | --- | --- |
| `standards_engine` Python exports | Standards Engine package tests and repository-local examples | Repository-controlled | Update atomically to v11 |
| `StandardsEngine.query`, `prepare`, `resolve`, `inspect` | Standards Engine navigation, analysis, rendering, and tool-facade tests | Repository-controlled | Preserve operations; replace models and handles |
| `AgentToolFacade` and generated agent-tool declarations | Standards Engine tests and checked-in generated projection | Repository-controlled | Regenerate from reachable v11 operation closure |
| Canonical A1 schema and validator entry points | Contract validator, generator, Standards Engine tests, Metadata tests, and Analysis tests | Repository-controlled | Replace local keyword interpreters with `standards_contracts` |
| Checked-in public examples and identity fixtures | Contract validation, documentation, package tests, and identity-domain regressions | Repository-controlled | Replace all v10 examples and v1 identity expectations atomically; add the missing semantic-consumer relationships |
| Generated Python request/result algebra | Standards Engine facade, renderer, tools adapter, and package tests | Repository-controlled | Regenerate complete v11 algebra; no internal domain type crosses facade |
| Identity serialization public export | Metadata, Analysis, Policy Impact, Standards Graph, Standards Engine contract tooling, and Verifier tests | Repository-controlled | Replace recursive NFC encoding with codepoint-preserving identity encoding v2; move semantic ordering, deduplication, and normalization to owning domains |
| Content capture and handles | Analysis snapshots, Standards Engine composition, navigation and cold-process tests | Repository-controlled | Move exact-list Git/native capture and storage to `standards_authority`; make ContentSnapshot contain only logical Unicode-scalar paths and exact bytes; discard source locators, filesystem metadata, and Adapter observations; handle v4 |
| Standards authority composition | Standards Engine bootstrap, query, analysis preparation, navigation and cold-process tests | Repository-controlled composition authority | Add one reference-only StandardsAuthorityView; callers supply one view while results bind narrower execution closure |
| Operation authority contracts | Standards Engine composition and route/read/related/analysis execution | Repository-controlled semantic authority | Store four executable `OperationAuthorityContractV2` values with typed per-operation compatibility revisions and exact required/allowed dynamic role-kind/cardinality contracts; keep direct-dependency semantics owner-local and prohibit encoded selectors, aggregate profiles, central codec manifests, and parallel edge catalogs |
| Material execution closure | Routing, reading, related navigation, policy/relationship inspection, and analysis projection | Repository-controlled generated evidence | Persist exact side- and role-qualified roots and derive transitive authority dependencies from AuthorityBoundValues and the selected operation contract; prohibit handwritten version/dependency bags and hypothetical-future closure |
| Consumed trust authority | Analysis providers, authorization validation, observations, dispositions, coverage attestations, and cold replay | Repository-controlled semantic authority | Store exact `ProviderAuthorityV1` and `AuthorizationGrantV1` objects only when a successful transition consumes them; remove aggregate trust views and ambient replay |
| Analysis-state stores and handles | Standards Engine facade/tool adapter and analysis/cold-process tests | Repository-controlled | Replace with directly stored material analysis root; omit complete base/proposed views; handle v4 |
| Navigation handle cache/inspection | Standards Engine navigation and inspection tests | Repository-controlled | Store navigation result directly; handle v4 |
| Child artifact inspection | Context, requirement, observation, coverage, certificate, policy, and relationship inspection tests | Repository-controlled | Store every advertised child as a direct typed authority object; remove owner maps, scans, and cache authority |
| Supplemental implementation node catalog | Standards graph composition, policy-impact compilation, analysis coverage horizon, and verifier | Repository-controlled semantic authority | Replace created/retired implementation artifacts atomically and preserve stable retained identities |
| Source-owned policy-impact relationships | Contracts, Architecture, Dependencies, Generated Contract, Cross-Platform, and Security policy units plus the closed declaration-source registry | Repository-controlled semantic authority | Register every admitted source explicitly and remap implementation consumers to the new compiler, projection, identity, authority, schema, generated, and facade artifacts |
| Python package and supported-target metadata | Every manifest and root `__init__.py` in the closed Engine Module dependency table plus exact repository entrypoints | Repository-controlled source-tree dependency, source-ownership, and public-export authority | Declare every production direct-import edge, one public root, and repository entrypoints exactly; resolve root `__all__` statically; reject private, root-form unexported, star, dynamic, or unowned cross-Module imports; and execute every root, export, and entrypoint without an ambient package, script-directory import, or build backend |

Search at the inventory base found no non-test Python importer outside the
repository packages, no deployed process or foreign-language binding, and no
independently versioned consumer of the generated agent-tool file. IPC and
Language Binding are therefore not applicable to this cutover. A discovery of
such a consumer is a re-plan trigger.

## Persisted-State Inventory

The directory-backed A1 store is used only by temporary test directories and
cold-process fixtures. No checked-in analysis-state directory, snapshot bundle,
navigation store, exported state fixture, release artifact, or documented
retention contract was found.

The repository therefore has no state that must be converted. Existing v10 and
handle-v3 values become typed `unsupported`; A1b must not add a migration tool,
dual reader, compatibility writer, alias, or fallback decoder.

If retained state appears before cutover, implementation stops and re-plans its
owner, retention requirement, exact version, conversion or retirement
decision, and verification.

## Authority Closure Inventory

### Direct object contract

Every public handle resolves exactly one stored `AuthorityObjectEnvelope v1`.
Public roots include ContentSnapshot, StandardsAuthorityView, ExecutionClosure,
navigation result, analysis root, policy/relationship inspection, and the
existing analysis/coverage child objects. Owner-local semantic authorities and
compiled views use the same repository but retain domain-owned validation.
A child artifact never requires scanning another root to resolve its handle.

### Content snapshot

The replacement closes only over an exact requested set of logical repository
paths and the exact bytes of each regular file required by later semantic
compilation.

Arbitrary file bytes use the canonical padded standard-Base64 representation
owned by `content-snapshot.v2`, with decoded SHA-256 and length bound beside the
representation. No text decoding or separate blob-store identity is implied.
Paths are nonempty Unicode-scalar component tuples; codepoints and case are
preserved. Empty, dot, dot-dot, slash, NUL, lone-surrogate, repository-control
`.git`, duplicate, nonregular, and unsupported path inputs reject.
Directories, modes, symlinks, nested snapshot handles, scope/exclusion records,
Adapter kind, Git commit/tree OIDs, tracking/inclusion explanations, checked-out
revisions, worktree state, filesystem metadata, Git object availability, and
process caches are capture inputs or observations only. Adapters validate and
discard them; they are not replay authority.

### Standards authority view

One immutable `StandardsAuthorityView` selects a content snapshot and exact
owner-produced semantic authority objects required to interpret it. The view
owns reference selection and coherence only. It does not acquire the semantic
authority of metadata, routing, graph, policy-impact, applicability, coverage,
provider, authorization, or contract Modules.

The view may include more authority than one operation uses. Its identity does
not become the identity of every derived result.

Each separately stored Engine-owned `OperationAuthorityContractV2` for route,
read, related, or analysis owns that family's exact required and allowed
dynamic roles, kinds, cardinalities, and per-operation compatibility revision.
Owner-local codec sets own allowed direct-dependency kinds and extract exact
references; Engine owns one generic operation/role/kind/cardinality coherence
algorithm. The codec sets are injected as one explicit tuple. Their union and
the structural dependency matrix are mechanically derived evidence only; there
is no encoded selector, aggregate operation, separate role or edge profile, or
central codec manifest.

### Execution closure

Each domain Module returns an immutable `AuthorityBoundValue` containing its
value and exact direct authority references. The composing kernel persists one
sorted `ExecutionClosureV2` root set whose roots retain side and role, then
derives the transitive dependency set by deterministic traversal. The selected
operation contract is a root. Analysis closure includes authority consumed by
the current state and projection. A successor adds newly consumed authority;
the current state does not speculate about every possible future submission.
Callers and handwritten version maps do not declare closure membership.

### Analysis root

The replacement stores narrow context, normalized changes and semantic
proposals, dependency-valid observations and dispositions, coverage
attestations and decisions, evidence and authorization records, and the
roots-only material analysis execution closure. Complete base/proposed
authority views are prepare inputs only and never state or result fields. The
state derives requirements, obligations, traces, reading plans, certificates,
results, and next operations. Provider and authorization authorities
participate in state transitions only. A successful transition stores exact
direct provider/authorization authority; deterministic no-observation stores
nothing. Live trust services are not ambient requirements for replay.

### Navigation root

The replacement stores the identity-bearing navigation projection and its
material execution-closure handle needed for exact cold inspection. It does
not make renderings, summaries, the complete authority view, or caches
authoritative.

### Materialized derived objects

Policy, relationship, coverage, context, requirement, and observation objects
store their exact typed payload and owner-declared direct dependencies. They
remain generated projections rather than authored semantic authority. Direct
materialization is required so cold inspection has one resolution rule for
roots and children.

### Durable publication

The Linux ext4 adapter uses SQLite schema v1 with one
`authority_objects(handle PRIMARY KEY, envelope NOT NULL)` table. One
transaction verifies and inserts each object. Identical same-handle bytes are
idempotent; different bytes are a contradiction and never overwrite. The
envelope owns object kind, so SQL does not duplicate it. SQLite provides writer
serialization, crash recovery, integrity checking, cold reopen, and
byte-preserving backup. A1b adds no migration framework, semantic
export/import, dual reader, mutable semantic index, or checked-in database.

## Consumer Migration Rules

1. Every public request and result enters or leaves through the generated v11
   algebra. Query and analysis preparation accept authority views; results bind
   their mechanically derived execution closures.
2. Domain Modules exchange their own immutable types and never import generated
   facade models.
3. Every handle resolves one direct typed object through
   `standards_authority`; the repository owns envelope integrity and direct
   lookup while explicitly injected owner codec sets own semantic construction,
   identity, dependency extraction, and decoding. Authority and Contracts do
   not depend on each other. No owner lookup table, discovery, store
   enumeration, root scan, or cache index is permitted.
4. Every old validator, decoder, serializer import, snapshot compiler,
   analysis store, version bag, and ambient authority-completion path is
   deleted in the same accepted cutover.
5. Current operation names and high-level behavior remain; unknown old versions
   return typed `unsupported`.
6. Consumer tests assert stable identities, relationships, and behavior rather
   than mutable repository counts.
7. Every production cross-Module import names the dependency manifest's exact
   public root, and every root-form imported name belongs to its statically
   resolved `__all__`. Package initializers own exported symbols; verifier
   suites do not maintain symbol or package allowlists.
8. Relationship files enter compilation only through the closed policy-impact
   registry. Policy-unit membership and filesystem paths do not imply
   relationship-source membership.
9. Governed source ownership derives from manifest roots and exact repository
   entrypoints. Git-indexed non-test Python under `tools/` with no owner is
   invalid rather than silently outside package enforcement.
10. Repository entrypoints import owner functionality only through the owner's
    canonical manifest root and execute under safe-path isolation; own-package
    private-import permission applies only beneath the package root.
11. Execution closures store only roots from the selected operation contract
    and `AuthorityBoundValue` results. The exact transitive dependency set is
    derived from immutable owner references. Roots retain side and role. A
    caller-supplied or handwritten closure is invalid.
12. Successful analysis transitions store exact consumed provider and
    authorization objects. Deterministic no-observation stores nothing; replay
    never invokes live trust services.

## Required Evidence

- Import and source inventory showing no external consumer or retained state.
- Generated closure proving every public operation input and result is covered.
- Public package tests proving only generated v11 values cross the facade.
- AST-derived source ownership, manifest/import equality, and root/export checks
  across every production Module and repository entrypoint, including separate
  below-root and root-form-private-child fixtures for generated output and
  handwritten facade code, plus safe-path execution of every exact entrypoint.
- Mutation-after-capture and genuine cold-process reconstruction with no source
  path, live provider, live authorization authority, or injected private
  authority.
- Included-authority mutation changes the applicable owner object and material
  execution closure; excluded-authority mutation leaves unrelated operation
  identity unchanged.
- Roots-only closure tests proving every consumed dependency is derivable,
  every unused view member is absent, successor authority enters only the child
  state, ordering is deterministic, cycles reject, and no handwritten
  version/dependency list participates.
- SQLite transaction, idempotence, contradiction, integrity, backup,
  crash-recovery, ignored-runtime-file, and cold-reopen evidence on ext4.
- Git-object and descriptor-relative native capture parity, exact path-set
  closure, path-grammar rejection, mutation endpoint revalidation, and proof
  that no directory/symlink/mode/locator field enters snapshot identity.
- Direct cold inspection for every advertised handle variant.
- Identity fixtures proving codepoint preservation and domain-owned semantic
  ordering, normalization, and deduplication.
- Accepted/proposed policy-impact compilation, exact admitted-source
  registration, node and relationship dispositions, consumer dispositions,
  final horizon freeze, and certificate equality.
- Exact deletion evidence for former validators, stores, and compatibility
  paths.
- Broad package, declarative-suite, retained-checker migration, generated
  freshness, and diff-hygiene gates.

## Conclusion

Use one coordinated breaking replacement. Compatibility machinery would have
no consumer and would create parallel authority, so it is prohibited unless
this inventory is invalidated by a newly discovered retained consumer or state.
