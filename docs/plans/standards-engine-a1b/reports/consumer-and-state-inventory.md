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
| Generated Python request/result algebra | Standards Engine facade, renderer, tools adapter, and package tests | Repository-controlled | Regenerate complete v11 algebra; no internal domain type crosses facade |
| Identity serialization public export | Metadata, Analysis, Policy Impact, Standards Graph, Standards Engine contract tooling, and Verifier tests | Repository-controlled | Move to `standards_identity` without changing identity bytes |
| Snapshot compilation and handles | Analysis snapshots, Standards Engine composition, navigation and cold-process tests | Repository-controlled | Move capture/storage to `standards_authority`; handle v4 |
| Analysis-state stores and handles | Standards Engine facade/tool adapter and analysis/cold-process tests | Repository-controlled | Replace with `standards_authority`; handle v4 |
| Navigation handle cache/inspection | Standards Engine navigation and inspection tests | Repository-controlled | Persist typed navigation root; handle v4 |
| Child artifact inspection | Context, requirement, observation, coverage, certificate, policy, and relationship inspection tests | Repository-controlled | Add explicit snapshot or analysis owner; reconstruct from root |

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

### Snapshot root

The replacement must close over:

- declared scope and exclusions;
- sorted entry paths, types, modes, tracking state, and inclusion reasons;
- symlink targets and inert resolution state;
- nested repository or gitlink identities and nested snapshot handles;
- every included source byte used by metadata, routing, graph, policy-impact,
  applicability, coverage, read, or inspection compilation; and
- semantic contract versions that can change reconstruction.

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

## Consumer Migration Rules

1. Every public request and result enters or leaves through the generated v11
   algebra.
2. Domain modules exchange their own immutable types and never import generated
   facade models.
3. Every handle resolves through `standards_authority` or through an owning
   root resolved there; no store enumeration or cache scan is permitted.
4. Every old validator, decoder, serializer import, snapshot compiler, and
   analysis store is deleted in the same accepted cutover.
5. Current operation names and high-level behavior remain; unknown old versions
   return typed `unsupported`.
6. Consumer tests assert stable identities, relationships, and behavior rather
   than mutable repository counts.

## Required Evidence

- Import and source inventory showing no external consumer or retained state.
- Generated closure proving every public operation input and result is covered.
- Public package tests proving only generated v11 values cross the facade.
- Mutation-after-capture and genuine cold-process reconstruction with no source
  path or injected private authority.
- Owner-qualified inspection for every advertised handle variant.
- Exact deletion evidence for former validators, stores, and compatibility
  paths.
- Broad package, declarative-suite, retained-checker migration, generated
  freshness, and diff-hygiene gates.

## Conclusion

Use one coordinated breaking replacement. Compatibility machinery would have
no consumer and would create parallel authority, so it is prohibited unless
this inventory is invalidated by a newly discovered retained consumer or state.
