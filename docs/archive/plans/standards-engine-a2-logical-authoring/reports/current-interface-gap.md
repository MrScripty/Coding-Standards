# Current A2 Interface Gap And Authority Inventory

**Date:** 2026-09-03

**Disposition:** corrective planning required

## Question

Does accepted A2 already let an agent author the complete standards graph and
its supplementary authorities exclusively through a standards-domain Engine
Interface, without knowing or directly manipulating repository or persistence
representations?

## Observed Current Contract

- `tools/standards_engine/contracts/a1-contract.schema.json` defines
  `ReplacementMutation` as `op = replace`, a repository-relative `path`, and
  the complete replacement string `value`. Both `CreateProposalCall` and
  `ReviseProposalCall` require a non-empty array of that representation.
- `tools/standards_engine/standards_engine/authoring.py` models the same
  `Mutation(path, value)` and requires every target path to exist in the base
  snapshot. There is no public add, remove, relocate, or standards-domain
  relationship operation.
- `tools/repository_git/repository_git/repository.py` materializes only
  replacements of existing regular files and creates every candidate with the
  same `feat(standards): apply approved proposal` message.
- The Engine does own physical candidate writes, Git operations, and SQLite
  access. An agent does not currently write files or SQL directly. The defect
  is at the public seam: the agent must still construct repository-shaped
  content and know which stored representations need replacement.

## Standards Authority Shape

The standards graph is a compiled projection, not one graph file:

- canonical module membership comes from
  `evaluation/standards-effectiveness/canonical-module-corpus.toml`;
- module IDs, roles, levels, `Requires`, `Specializes`, and canonical owners are
  declared in each standards module's metadata;
- policy units and lifecycle declarations come from
  `evaluation/standards-effectiveness/policy-units/registry.toml` and its
  registered module sidecars;
- policy-impact relationships and the broader `semantic` edge group come from
  the registered typed declarations under
  `evaluation/standards-effectiveness/policy-impact/` plus their registries and
  node catalog;
- consumer coverage and audit authority come from the policy-coverage horizon,
  attestation-source, authorization, revocation, and attestation records;
- Router behavior comes from canonical module metadata and the Router
  projection; and
- generated projections remain derived from their canonical sources.

`standards_graph` and `graph_engine` compile these authorities into neutral
nodes, edge groups, and traversal. They do not own the semantic decision to add
or remove an edge. Existing A1c/A2 analysis can detect and review proposed
changes, but current A2 cannot formulate all of them from one logical intent.

## Finding

A2 is complete for controlled, immutable, verified replacement of existing
repository files. It is not complete for path-free logical standards
authoring, file lifecycle, graph reorganization, or Engine-owned coordination
of every supplementary authority.

The corrected seam must accept canonical standards IDs, authored standards
content, explicit semantic/lifecycle decisions, rationale, and evidence. The
Engine may then resolve and serialize every mechanically affected
representation, validate the complete candidate through existing canonical
consumers, and use SQLite and Git internally. It must never infer semantic
relationships or fabricate approval/evidence merely to make the candidate
valid.

## Planning Consequence

- Preserve the accepted A1c design and the working A2 proposal, review,
  application, and recovery lifecycle.
- Replace or deepen the public mutation Interface rather than layering a second
  authoring route over it.
- Validate the exact Interface and write-side projection in one bounded
  pre-canonical minimum viable test before production implementation.
- Once that reversible design satisfies the product contract and routed
  standards, implement it; adjacent uncertainty cannot start an unbounded
  prototype/review/re-plan cycle.
- Keep remote push outside the objective.
