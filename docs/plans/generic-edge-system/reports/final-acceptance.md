# Generic Edge System Final Acceptance

## Canonical Architecture

The neutral graph engine is `tools/graph_engine/`. It owns canonical nodes and
aliases, stable directed edges, named groups, explicit source registration,
derived incoming and outgoing indexes, provenance, deterministic querying, and
controlled traversal. It imports no standards-verifier, policy, planning,
migration, suite, or Bash-retirement code.

The repository composition is `standards_verifier.repository_graph`, and the
canonical command is `tools/query_edges.py`. The composition supplies only
providers explicitly named by the source registry; it does not scan for graph
declarations. The dependency direction is:

```text
tools/graph_engine
  <- repository composition
       -> policy manifest
       -> standards-verifier suite-dependency provider
       -> standards-verifier metadata-dependency provider
```

One `Edge` declares a stable ID, canonical source and target, relation, group
memberships, provenance, traversal eligibility, and opaque metadata. One
`EdgeGroup` declares a stable ID, purpose, allowed directions, transitive
permission, provenance, and an optional validator name. Groups are filtered
views over shared edges; group membership does not copy an edge.

`NodeResolver` maps explicit logical IDs and repository paths to one canonical
node. Compatible declarations from registered sources merge into that node;
contradictory aliases or metadata fail. Existing contained artifacts without
edges return an empty result; missing paths and unknown logical IDs remain
distinct failures.

## Query And Traversal

Representative commands are:

```bash
python3 tools/query_edges.py --node workflow.planning
python3 tools/query_edges.py --node workflows/planning.md \
  --direction outgoing --group policy-impact
python3 tools/query_edges.py --edge policy.planning.router \
  --direction outgoing --traverse
python3 tools/query_edges.py --node workflow.planning \
  --direction outgoing --group policy-impact --traverse
python3 tools/query_edges.py --list-groups
```

Exact-edge traversal follows only the selected edge. Group traversal follows
only eligible edges in the selected group and explicit direction. Transitive
traversal is rejected unless the group permits it; cycles terminate with
deterministic de-duplication and explanatory paths.

## Registered Groups And Migrated Consumers

The canonical query composes six groups: `policy-impact`, `semantic`,
`suite-dependencies`, `standards-requires`, `standards-specializes`, and
`standards-dependencies`.

- Policy impact is declared once in the registered generic manifest. The
  verifier applies policy relation, applicability, evidence-owner,
  audited-owner, and suite-closure validation as a downstream adapter.
- Suite `requires` declarations retain registry authority and generate the
  `suite-dependencies` group for generic traversal and dependency ordering.
- Metadata `Requires` and `Specializes` declarations retain Markdown authority
  and generate three filtered groups for generic cycle validation.
- `workflow.implementation` reports policy and metadata edges together. The
  `concurrent-plan-integration` suite reports policy and suite-dependency edges
  through either its ID or path.
- The previous policy query and manifest-only graph command were deleted. No
  legacy schema, reverse index, compatibility copy, or fallback remains.

The Planning group includes the previously omitted full-codebase review prompt,
its fixture, and its suite. Every registered suite explicitly owned by audited
Planning has an enforcement-suite edge. The exact 24-consumer review is in
[planning-consumer-dispositions.tsv](planning-consumer-dispositions.tsv).

## Inventory And Deferrals

The complete reviewed inventory and exact dispositions are in
[graph-consumer-inventory.tsv](graph-consumer-inventory.tsv). The temporary
Bash checker graph and migration-package dependencies remain deferred because
their schemas and lifecycle are frozen during Bash retirement. Executable-edge
dispositions, source closure, and complete-checkpoint order remain specialized
table or lifecycle checks. Ordinary relation checks, owner maps, and Markdown
links are not graph authorities.

Deferred mechanisms must be reconsidered only at their recorded triggers. No
global completeness is claimed beyond explicitly inventoried mechanisms and
audited policy owners.

## Verification

- 32 graph-engine tests passed.
- 323 standards-verifier tests passed.
- All 164 registered declarative suites passed.
- Generated evidence remained current.
- The complete mixed checkpoint passed all 109 retained Bash verifiers.
- Both Planning aliases returned the same exact 24 edge IDs.
- All 24 Planning consumers had one exact review disposition.
- The canonical query exposed all six migrated groups and cross-source
  incident edges.
- Affected plan structure, Markdown links, no-old-authority inspection,
  `git diff --check`, and staged write-set review passed.

M6-I17 was neither selected nor admitted. The parent migration resumes with a
fresh post-recovery graph audit.
