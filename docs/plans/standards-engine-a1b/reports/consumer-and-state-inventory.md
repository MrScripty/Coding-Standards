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
| Snapshot compilation and handles | Analysis snapshots, Standards Engine composition, navigation and cold-process tests | Repository-controlled | Move Git/manifest capture and storage to `standards_authority`; store snapshot root directly; handle v4 |
| Analysis-state stores and handles | Standards Engine facade/tool adapter and analysis/cold-process tests | Repository-controlled | Replace with directly stored analysis root; handle v4 |
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

Every public handle resolves exactly one stored
`AuthorityObjectEnvelope v1`. The closed object-kind vocabulary contains
snapshot root, navigation result, analysis root, policy inspection,
relationship inspection, coverage certificate, coverage view, coverage
requirement, coverage attestation, analysis context, fact requirement, and
fact observation. A child artifact may depend on an aggregate root, but it does
not require scanning that root to resolve its handle.

### Snapshot root

The replacement must close over:

- declared scope and exclusions;
- sorted entry paths, types, modes, tracking state, and inclusion reasons;
- symlink targets and inert resolution state;
- nested repository or gitlink identities and nested snapshot handles;
- every included source byte used by metadata, routing, graph, policy-impact,
  applicability, coverage, read, or inspection compilation; and
- semantic contract versions that can change reconstruction.

Arbitrary file bytes use the canonical padded standard-Base64 representation
owned by `snapshot-root.v1`, with decoded SHA-256 and length bound beside the
representation. No text decoding or separate blob-store identity is implied.

Repository paths, worktree bytes, Git object availability, and process caches
are capture inputs only. They are not replay authority.

### Analysis root

The replacement stores exact snapshot handles, normalized changes and semantic
proposals, dependency-valid observations and dispositions, coverage
attestations and decisions, evidence, authorization records, authority views,
and semantic contract versions. It derives requirements, obligations, traces,
reading plans, certificates, results, and next operations.

### Navigation root

The replacement stores the snapshot handle and identity-bearing navigation
projection needed for exact cold inspection. It does not make renderings,
summaries, or caches authoritative.

### Materialized derived objects

Policy, relationship, coverage, context, requirement, and observation objects
store their exact typed payload and dependency handles. They remain generated
projections rather than authored semantic authority. Direct materialization is
required so cold inspection has one resolution rule for roots and children.

### Durable publication

The Linux ext4 adapter serializes writers through one repository-scoped
advisory publication lock that is coordination state, not semantic authority.
The adapter retains trusted directory descriptors and performs every creation,
link, unlink, and status operation relative to them; configured-root
replacement cannot redirect publication. Newly created `objects` and
object-kind directories and their parents are flushed before use. While holding
the lock, a writer removes abandoned regular files from the reserved staging
namespace, stages one complete envelope, flushes it, and publishes the absent
content-addressed filename with an atomic create-only hard link. It then flushes
the directory and removes the staging name. Reads remain lock-free. Overlapping same-ID publication is
idempotent only after exact byte verification; contradictory content is
invalid and never overwrites. A crash releases the publication lock, and the
next writer performs bounded staging cleanup. A retry after an unknown
post-link outcome returns the same verified handle. Dependencies publish
before roots, so incomplete work cannot create a resolvable root with missing
closure. Other durable filesystem families are unsupported in A1b.

## Consumer Migration Rules

1. Every public request and result enters or leaves through the generated v11
   algebra.
2. Domain Modules exchange their own immutable types and never import generated
   facade models.
3. Every handle resolves one direct typed object through
   `standards_authority`; no owner lookup table, store enumeration, root scan,
   or cache index is permitted.
4. Every old validator, decoder, serializer import, snapshot compiler, and
   analysis store is deleted in the same accepted cutover.
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

## Required Evidence

- Import and source inventory showing no external consumer or retained state.
- Generated closure proving every public operation input and result is covered.
- Public package tests proving only generated v11 values cross the facade.
- AST-derived source ownership, manifest/import equality, and root/export checks
  across every production Module and repository entrypoint, including separate
  below-root and root-form-private-child fixtures for generated output and
  handwritten facade code, plus safe-path execution of every exact entrypoint.
- Mutation-after-capture and genuine cold-process reconstruction with no source
  path or injected private authority.
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
