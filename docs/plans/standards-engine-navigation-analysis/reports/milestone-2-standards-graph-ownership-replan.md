# Milestone 2 Standards-Graph Ownership Replan

## Trigger

Snapshot-bound `related` must consume the accepted `standards-requires` and
`standards-specializes` groups. Their only provider currently lives in
`standards_verifier.graph_adapters`, but A1 analysis is prohibited from
depending on verifier implementation or suite execution machinery.

## Decision

Create `tools/standards_graph/` as the neutral repository-owned adapter between
`standards_metadata` and `graph_engine`:

```text
standards_metadata + graph_engine
              |
              v
       standards_graph
          /       \
standards_analysis standards_verifier
```

Its small interface provides the canonical metadata edge source and a standards
navigation registry assembled from explicit registered sources. It does not
parse canonical metadata, implement generic traversal, load suites, evaluate
policy applicability, or expose verifier diagnostics.

Suite dependency projection remains verifier-owned because suite execution is
not a canonical standards relationship and A1 navigation does not require it.
The verifier's complete repository registry composes that suite provider with
the neutral standards provider.

## Rejected Alternatives

| Alternative | Rejection |
| --- | --- |
| Import verifier graph adapters from A1 | Reverses the accepted upstream dependency direction and exposes suite machinery to analysis. |
| Copy metadata projection into analysis | Creates competing edge IDs, groups, traversal declarations, and forward/reverse authority. |
| Put graph projection in `standards_metadata` | Makes the metadata loader own a downstream graph representation rather than preserving a focused metadata interface. |
| Inject only a verifier-built registry | Avoids immediate duplication but leaves the verifier as the hidden production owner of A1 navigation. |

## Cutover Contract

- Move metadata group constants and provider construction without changing
  normalized nodes, aliases, edge IDs, relations, groups, provenance, metadata,
  traversal direction, or transitivity.
- Update every current import in repository composition, metadata routing, and
  tests in the same change.
- Leave suite projection in `standards_verifier.graph_adapters`.
- Do not retain re-exports, wrappers, fallback imports, or duplicate tests
  against the old owner.
- Prove old/new graph equality before deleting the old implementation and run
  neutral, verifier, graph, declarative, alias, and query integration tests.

## Navigation Boundary

After cutover, implement `read`, `related`, and `inspect` through the neutral
module. Route projection remains a later Milestone 2 slice because it adds a
different Router-owned decision contract.

## Acceptance Evidence

The former and replacement metadata providers were compared before removal and
were exactly equal: 58 nodes, 178 edges, and three groups. Every known consumer
now imports the neutral owner, and repository search finds no metadata graph
projection in `standards_verifier.graph_adapters`.

- Neutral graph tests: 2 passed.
- Focused repository-graph, metadata, and metadata-route tests: 34 passed.
- Standards verifier tests: 381 passed.
- Generic graph tests: 35 passed.
- Neutral metadata tests: 7 passed.
- Declarative suites: 218 of 218 passed.
- Existing `tools/query_edges.py` standards-requires query: passed.
- Plan structure and `git diff --check`: passed.

The cutover is accepted without changing graph authority, schema, or observable
behavior.
