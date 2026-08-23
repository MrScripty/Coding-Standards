# Milestone 1 Neutral Metadata Cutover

## Result

Milestone 1 is accepted. `tools/standards_metadata/` is the sole runtime loader
for canonical corpus membership and canonical document metadata. The verifier,
repository graph composition, policy-impact adapter, and routing checks consume
that package; the neutral package imports none of those consumers.

## Authority And API

- The corpus manifest owns ordered membership only.
- Each canonical document owns its ID, canonical path, role, level,
  applicability, exclusions, `Requires`, `Specializes`, verification text, and
  canonical owner.
- `ModuleMetadata`, `CanonicalModuleCorpus`, `MetadataFailure`, and
  `MetadataValidation` are immutable neutral values.
- `load_canonical_module_corpus`, `load_module_metadata`, and
  `validate_module_metadata` are the only production loading entrypoints.
- ID and repository-path lookups resolve through the same corpus view. There
  are no additional authored aliases in the current canonical metadata.

`standards_metadata` performs contained reads, parsing, identity and relation
validation, unresolved-target checks, and iterative cycle checks. It does not
store graph indexes or expose traversal. Repository graph composition continues
to project the neutral values through the accepted generic graph adapter.

## Cutover

The frozen [consumer inventory](metadata-consumer-inventory.tsv) contains one
disposition for every discovered authority, production consumer, projection,
entrypoint, test consumer, and declarative entrypoint.

The cutover removed:

- `standards_verifier/canonical_modules.py`; and
- neutral document parsing and graph validation from the verifier metadata
  check.

The verifier metadata check now owns only declarative configuration, suite
context, and translation of neutral failures into verifier diagnostics.
Policy-impact keeps relation-specific checks and typed policy diagnostics.
`graph_adapters.py` remains unchanged because it consumes a structural module
view and creates a graph projection; it neither discovers nor parses metadata.
The registered provider name remains provenance and is not canonical metadata
authority.

No compatibility wrapper, old import path, dual loader, fallback, or copied
catalog remains.

## Equivalence

Before source edits, the admitted verifier-owned loader was evaluated from
commit `3383ec68` against the exact canonical corpus. After cutover, the neutral
loader was normalized through the same field projection and ordering.

| Property | Old | New | Result |
| --- | ---: | ---: | --- |
| Modules | 58 | 58 | exact |
| Normalized JSON bytes | 39,305 | 39,305 | exact |
| SHA-256 | `ff5e206875e60c03dbd8e408a7e71c1661afa199b0525b6f5aef666e88f9e826` | `ff5e206875e60c03dbd8e408a7e71c1661afa199b0525b6f5aef666e88f9e826` | exact |

The comparison includes corpus path, ordered members, module order, IDs, paths,
roles, levels, applicability, exclusions, ordered `Requires`, ordered
`Specializes`, verification text, and canonical owner. Existing verifier
negative tests preserve diagnostic codes and unavailable-input behavior.
Repository graph tests derive and compare every `Requires` and `Specializes`
edge from canonical metadata, preserving groups, transitive behavior, IDs,
path aliases, and query behavior.

## Dependency Evidence

Import inspection found no `standards_verifier`, `standards_analysis`,
policy-impact, or `graph_engine` import in neutral package Python sources. The
only metadata model and corpus class definitions under `tools/` now reside in
`standards_metadata`. Production metadata calls resolve as follows:

```text
standards_verifier checks -----\
policy-impact adapter ----------> standards_metadata
repository graph composition ---/
                                   |
                                   `-- canonical manifest and documents
```

The repository graph composer separately adapts returned module values into
the generic graph engine. `tools/query_edges.py` remains an indirect consumer
of that composition and requires no metadata knowledge.

## Verification

- Neutral metadata: 7 tests passed, including a 1,200-module chain.
- Focused verifier consumers: 44 tests passed.
- Complete verifier unit package: 381 tests passed.
- Graph engine: 35 tests passed.
- Declarative suites: 218 selected and 218 passed.
- Focused `metadata-fixtures`, `s1-routing`, and `policy-semantic-impact`: passed.
- A1 schema contracts: 22 examples, seven identity fixtures, four operation
  envelopes, and 94 definitions passed.
- `query_edges.py` returned exact logical/path alias results for Planning.
- `git diff --check`: passed.

- Complete mixed checkpoint: generated evidence was current, all 218
  declarative suites passed, and all 53 retained Bash checkers passed.

## Remaining Boundary

Milestone 1 establishes module-level metadata only. It does not create snapshot
handles, policy-unit sidecars, applicability evaluation, impact packets,
navigation requests, or controlled authoring. Those remain in their accepted
later milestones.
