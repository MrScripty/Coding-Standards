# Milestone 3 Policy-Impact Authority Replan

## Trigger

Change classification and accepted/proposed graph-union traversal are
implemented. The next step must evaluate every reached policy-impact relation
and generate scoped obligations.

The current generic graph manifest declares nodes, groups, edge topology, and
two string metadata values on every edge. The `applicability` value is
explanatory prose rather than a typed expression, and `evidence_owner` is
policy-specific authority. The generic graph intentionally does not understand
policy scope, applicability, evidence, propagation, or audit semantics.

The accepted A1 contract requires those semantics. Continuing without an
authority correction would require interpreting prose, maintaining a second
edge-keyed declaration, encoding structured data in strings, or adding policy
behavior to the neutral graph. Each would violate an accepted contract.

## Accepted Design

Create one deep `standards_policy_impact` module. Its reviewed declarations are
the sole authority for policy-impact relationships and compile once into:

- a neutral `GraphContribution` containing policy-impact edges;
- typed policy semantics indexed by the same edge identities; and
- deterministic provenance, declaration digests, and dependency fingerprints.

The module does not replace generic node or group authority. The existing
policy-impact manifest is split into:

- one upstream generic catalog containing canonical non-module nodes and the
  `policy-impact` and `semantic` group declarations; and
- source-owner declaration files containing the 39 Planning and Commit
  relationships.

The compiler consumes canonical nodes, the policy relationship-kind catalog,
typed applicability, explicit evidence bindings, and bounded audit
declarations. It rejects unknown endpoints, duplicate natural keys,
contradictory registrations, malformed expressions, and ambiguous evidence or
audit matches.

The dependency direction becomes:

```text
standards_policy_impact
  |-- standards_metadata
  `-- graph_engine

standards_analysis
  |-- standards_metadata
  |-- standards_policy_impact
  `-- graph_engine

standards_graph --------> standards_policy_impact
standards_verifier -----> standards_policy_impact
standards_engine -------> standards_policy_impact
```

`graph_engine` remains domain-neutral and does not depend on any of these
consumers.

## Binding Authority Decisions

| Value | Authority |
| --- | --- |
| Canonical nodes and aliases | Existing upstream node catalogs and canonical module metadata |
| Generic group definitions and traversal | Existing registered graph-group authority |
| Source, consumer, relationship kind, typed applicability, rationale, and exceptional scope | Source-owner policy-impact declaration |
| Group membership | Relationship-kind catalog |
| Domain propagation | Relationship-kind contract, normally `source-to-consumer`; never generic group direction |
| Evidence owner | One explicit declaration binding or one exact registered binding; zero required matches is unavailable and multiple matches are invalid |
| Audit association | One exact owner, scope, relationship-class, horizon, and snapshot match; zero is unaudited and multiple matches are invalid |
| Edge topology, provenance, and digests | Compiler projection |
| Review dispositions | Snapshot-bound analysis reports, never relationship authority |

The existing 39 explanatory strings are not translated into conditions. Manual
review classifies every current relationship as an unconditional review
relationship using `{ operator = "always" }`. Explanatory meaning becomes
`rationale` and is never evaluated.

`always` is a new typed applicability expression. It has no fact dependency and
evaluates to `true` with an empty fact set. This deliberately versions the A1
applicability contract.

## Edge Identity

The accepted registered-edge rule is superseded for compiled policy-impact
relationships only. Their canonical identity derives deterministically from
the unique natural key:

```text
policy-impact:<source>:<relation>:<consumer>
```

The compiler rejects more than one relationship with that natural key.
Different scopes should normally be canonical consumer nodes or one combined
relationship; an exceptional narrow scope does not create a second edge with
the same key. A source, consumer, or relationship-kind change creates a new
relationship identity. Applicability, scope, evidence, or rationale changes
retain the identity and change its dependency fingerprint.

The cutover records an exact old-to-new identity map and deliberately versions
the ADR and contract. No hash, lookup fallback, legacy alias, or parallel edge
identity remains in accepted runtime behavior.

## Compilation And Reuse

Compilation always rebuilds the complete registered declaration set. At the
current and expected repository scale, this is simpler and safer than an
incremental compiler. Localized decision reuse is governed separately by exact
dependency fingerprints over declarations, nodes, aliases, kind mappings, fact
schemas, evidence bindings, audit horizons, group contracts, and applicable
tool contracts. A changed global dependency may invalidate more than incident
edges.

## Rejected Options

- **Edge-ID sidecar:** rejected because topology and semantics would be two
  declarations that must remain synchronized.
- **Policy fields in generic graph metadata:** rejected because it weakens the
  domain-neutral graph interface.
- **Structured values encoded as strings:** rejected because it creates opaque
  nested serialization and duplicate parsing.
- **One broad relationship authority:** rejected because `Requires`,
  `Specializes`, suite dependencies, and other relations already have correct
  independent owners.
- **One giant declaration file:** rejected because source-owned files provide
  better locality while one registry, schema, and compiler preserve one logical
  authority.

## One-Authority Cutover

1. Revise the ADR and A1 schema for the module graph, `always`, compiled
   declarations, domain propagation, and derived relationship identities.
2. Inventory all canonical node, group, relationship, evidence, audit, runtime,
   test, and generated consumers.
3. Manually classify all 39 current relationships and record exact old-to-new
   identity mappings.
4. Implement the compiler and validate typed declarations independently.
5. Compare compiled topology, groups, traversal, aliases, and query results
   against the old manifest in a pre-cutover equivalence test.
6. Switch repository graph composition, analyzer, verifier, and Standards
   Engine inspection to `CompiledPolicyImpactSet`.
7. Remove old edge blocks and policy string metadata in the same accepted
   change. Keep only the independent node/group catalog.
8. Reject any production fallback to the old manifest or metadata fields.

Old and new loaders may coexist only inside the pre-cutover equivalence test.

## Replan Triggers

Re-plan if canonical non-module nodes cannot be separated from relationship
authority, an existing consumer requires stable old edge IDs that cannot be
migrated coherently, a relationship needs duplicate natural keys, policy-aware
behavior would enter `graph_engine`, strict evidence or audit resolution cannot
distinguish missing from ambiguous state, or the cutover requires an unrelated
graph authority change.

## Current Accepted Boundary

The implemented classifier and graph-union selector remain valid. They consume
exact seeds, named groups, and generic graph views. Their trace identities will
change only through the deliberate policy-impact EdgeId contract revision.
