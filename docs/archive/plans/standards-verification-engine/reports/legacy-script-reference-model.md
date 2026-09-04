# Legacy Script Reference Model Boundary

## Purpose

This report defines the narrow role and lifecycle of the generated checker
inventory and migration graph while Bash verification is being removed. It is
not a standards-navigation graph, a canonical ownership graph, or the suite
execution graph.

The model exists only to identify legacy script paths and conservative
references that must be reviewed before a script is deleted. Registered suite
`requires` relationships are the sole execution-dependency authority for the
Python engine. Package owners and accepted dispositions remain explicit
reviewed authority; neither is inferred from reference topology.

## Current Consumer Audit

No retained shell file reads the generated inventory or graph schemas. The
direct machine consumers are limited to:

- `tools/standards_verifier/standards_verifier/inventory.py`;
- `tools/standards_verifier/standards_verifier/migration_graph.py`;
- `evaluation/standards-effectiveness/suites/executable-edge-dispositions.toml`;
  and
- `evaluation/standards-effectiveness/suites/milestone-7-row-35-decomposition.toml`.

Legacy scripts are scanned inputs only. They do not require annotations,
metadata, parser accommodations, or edits before their accepted replacement
slice deletes them.

## Data Lifecycle

| Category | Authority | Persistence rule | Examples |
| --- | --- | --- | --- |
| Authoritative configuration | Reviewed owner | Store and validate strictly | suite registry, package owner, accepted disposition |
| Current derived state | Canonical collector inputs | Compute when needed; persist only as a bounded temporary interface for a named consumer | live path membership, references, adjacency, components, waves, counts |
| Immutable historical evidence | Accepted baseline owner | Store once and do not regenerate from later source state | baseline hashes, source positions, historical metrics |
| Optional report | None | Generate on request; never use as modification or acceptance authority | topology summaries and aggregate counts |

Current derived data does not become authoritative merely because a generated
TSV is committed. Freshness proves agreement with its collector; it does not
grant the projection ownership, execution, or semantic meaning.

## Temporary Serialized Vocabulary

The current serialized graph schema is frozen for the remainder of Bash
migration. Its existing tokens have these bounded meanings:

- `executable_reference`: a shell or Python source contains a target script
  basename; this is a conservative code-text reference, not proof of
  execution;
- `contract_reference`: a TOML or TSV source contains a target script
  basename;
- `verifier_dependency`: the lexical extractor matched a path-shaped verifier
  reference in a script; and
- `helper_dependency`: the lexical extractor matched a path-shaped helper
  reference in a script.

Path-shaped references remain deletion-lifecycle obligations. Exact review or
structured suite authority decides whether a reference executes, inspects, or
only names its target. The schema must not gain new fields, aliases, edge
types, inference rules, or consumers during the remaining migration.

Names such as `lines`, `uses_sed`, `uses_awk`, `uses_rg`, component ordinals,
waves, and inbound or outbound counts are current derived observations. They
must not authorize package selection, ownership, acceptance, or modification.
No new permanent engine contract may copy them.

## Selected Narrow Migration

The current schema remains unchanged because physically renaming temporary
edge types would rewrite accepted edge-disposition history and regenerated
reports without improving the permanent engine. Removing individual redundant
columns now would also require changes to a temporary strict-header consumer.

Until Bash closure:

1. keep legacy scripts read-only except in their accepted replacement and
   deletion slices;
2. use the generated edge identities only for conservative incident-reference
   completeness;
3. use typed checker and suite subjects for stable package identity;
4. use registered suite `requires` only for exact execution dependencies;
5. derive mutable membership and totals rather than copying them into new
   authority; and
6. add no Bash AST, script annotations, compatibility representation, or
   generalized permanent graph API.

This is a semantic fence, not a compatibility fallback. The temporary schema
has one representation and one deletion condition; no replacement schema runs
beside it.

## Zero-Bash Sunset

When canonical inventory contains no Bash verifier, verification helper, or
migration launcher, one final closure slice removes the temporary model rather
than refining it. The closure owns:

- checker inventory and migration-graph Python modules that have no permanent
  consumer;
- current generated inventory, node, edge, and component artifacts;
- Bash-edge disposition checks and migration-only declarative consumers;
- migration-only tests and documentation; and
- complete-mode branches whose only purpose is retained Bash execution.

The closure retains immutable historical evidence and accepted package history
when those records remain required to explain the migration. It does not
retain current-state graph generation, serialized aliases, empty adapters, or
fallback execution.

## Re-plan Triggers

Re-plan before changing this boundary if:

- a retained shell file is discovered to consume a generated schema;
- a migration package requires exact invocation semantics that structured
  suite or reviewed disposition authority cannot provide;
- a new permanent consumer requires current graph data after Bash closure;
- deleting a temporary artifact would invalidate required immutable historical
  evidence; or
- a package cannot prove incident-reference completeness without adding copied
  counts, inferred ownership, or another authority representation.
