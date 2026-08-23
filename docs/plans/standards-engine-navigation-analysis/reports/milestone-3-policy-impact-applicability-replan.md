# Milestone 3 Policy-Impact Applicability Replan

## Trigger

Change classification and accepted/proposed graph-union traversal are
implemented. The next step must evaluate every reached policy-impact relation
and generate scoped obligations.

The current canonical graph manifest stores fields such as:

```toml
metadata = {
  applicability = "Fixture records conditional planning decisions.",
  evidence_owner = "suite:planning-admission"
}
```

`applicability` is explanatory prose, not a typed expression. It cannot produce
`true`, `false`, or `unknown`. The generic graph also intentionally restricts
extension metadata to string keys and values and does not own policy scopes,
applicability, evidence, or audit semantics.

The accepted A1 schema instead requires typed applicability, source and
consumer scopes, propagation direction, evidence ownership, and audit
association. Continuing without an authority decision would require one of:

- interpreting prose;
- duplicating edge topology in another declaration;
- encoding structured policy state as opaque strings; or
- widening the generic graph with policy-specific behavior.

Each violates an accepted contract, so this is a replan trigger.

## Options

### Option 1: Edge-ID-Keyed Policy Semantics Sidecar (Recommended)

Keep the generic manifest as the sole owner of edge ID, endpoints, relation,
groups, traversal, and declaration provenance. Add one reviewed
policy-specific declaration keyed only by registered edge ID. It owns:

- source and consumer review scopes;
- propagation direction;
- typed applicability expression;
- evidence owner;
- audit declaration reference; and
- explanatory rationale where useful.

The analyzer and policy verifier load the sidecar, resolve each edge ID through
the generic registry, and reject missing, extra, duplicate, stale, or
non-policy-impact bindings. Remove applicability and evidence ownership from
generic edge metadata during one cutover so no field has two owners.

This requires a pre-runtime schema refinement: replace the current
`PolicyImpactDeclaration` shape, which repeats source, target, and relation,
with an edge-reference domain-semantics shape. The generic edge supplies those
facts mechanically.

**Effect:** smallest bounded change, no generic-engine modification, no
topology duplication, and typed policy semantics remain downstream.

### Option 2: One Policy-Specific Manifest That Generates Generic Edges

Replace the current generic policy-impact manifest with a policy-specific
manifest containing topology and typed semantics once, then provide a
registered adapter that generates generic nodes and edges.

**Effect:** strong single-file ownership, but broader cutover across graph
composition, query tooling, verifier loading, tests, and generated evidence.
The provider boundary also needs careful placement so neither the verifier nor
the analyzer becomes an upstream graph owner.

### Option 3: Structured Generic Graph Metadata

Expand generic edge metadata from strings to arbitrary typed values and store
the complete policy contract on each generic edge.

**Effect:** compact storage but changes the generic graph contract for one
domain, complicates deterministic metadata comparison and display, and weakens
the accepted domain-neutral boundary. Not recommended.

### Option 4: Encoded Expressions In String Metadata

Serialize typed expressions as JSON or another mini-format inside the current
string field.

**Effect:** minimal file movement but creates opaque nested serialization,
double parsing, poor review ergonomics, and unclear schema ownership. Not
recommended.

## Recommended Cutover

Use Option 1 with one serial cutover:

1. Refine the A1 schema and ADR so policy domain metadata references one
   registered edge ID and does not repeat topology.
2. Inventory every current policy-impact edge and give it one exact typed
   semantics disposition.
3. Add the canonical sidecar and strict loader in `standards_analysis`.
4. Adapt the policy verifier to validate the same declaration through a thin
   downstream adapter.
5. Remove applicability and evidence-owner fields from generic edge metadata.
6. Prove all prior edge IDs, endpoints, relations, groups, and query results are
   unchanged.
7. Add malformed, missing, extra, duplicate, unknown-edge, wrong-group,
   unresolved-fact, and stale-audit negative cases.

The write set must expand to the ADR, schema examples, policy verifier adapter
and tests, policy-impact manifest, new domain declaration, edge-source
registry if required, and this plan. `graph_engine` remains unchanged.

## Current Accepted Boundary

The implemented classifier and graph-union selector do not depend on the
choice. They consume exact seed/group plans and registered graph views, so they
remain valid under any option that preserves generic edge identity and named
groups.
