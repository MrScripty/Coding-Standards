# Plan: Generic Directed Edge System

**Plan status:** `Accepted`

**Current phase:** Objective accepted

**Next slice:** none; parent verification work resumes with a fresh graph audit

**Acceptance status:** `satisfied`

**Accepted base:** `7ae51ba996827cbf35cb6a5d73476b9eeb724437`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Provide one repository-neutral directed-edge engine with canonical nodes,
aliases, named edge groups, deterministic bidirectional discovery, provenance,
and explicitly permitted traversal. Migrate policy impact and the justified
permanent graph consumers to that engine without dual authority or fallback.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | One explicit edge declaration is discoverable from both endpoints through canonical IDs and aliases. | `focused` | repository | `automated` | `satisfied` | 32 graph-engine tests |
| A2 | Named groups filter and traverse only explicitly eligible edges, with transitive traversal prohibited by default. | `focused` | repository | `automated` | `satisfied` | 32 graph-engine tests |
| A3 | Policy impact is one named group consumed through a policy adapter; no bespoke policy graph, reverse index, old manifest schema, or query fallback remains. | `integration` | repository | `automated` | `satisfied` | 323 verifier tests and no-old-authority review |
| A4 | Planning aliases return the same complete 24-edge policy-impact set, including the full-review prompt, fixture, and suite, and audited suite-owner closure remains enforced. | `integration` | repository | `automated` | `satisfied` | Exact generic-query comparison and policy suite |
| A5 | Every graph-like mechanism has one reviewed migration disposition, and every `migrate-now` or `adapt-now` mechanism uses the upstream engine. | `review` | repository | `manual` | `satisfied` | Repository composition and [graph consumer inventory](reports/graph-consumer-inventory.tsv) |
| A6 | All focused, Python, declarative, generated, plan, link, and mixed repository gates pass with a clean accepted worktree. | `complete` | repository | `automated` | `satisfied` | [Final acceptance report](reports/final-acceptance.md) |

## Scope

### In Scope

- A standard-library-only neutral graph package under `tools/graph_engine/`.
- Canonical nodes and aliases, explicit edge sources, stable edge and group
  identities, immutable deterministic indexes, provenance, queries, and
  controlled traversal.
- A generic read-only query command and strict generic manifest loader.
- Mandatory migration of policy impact to generic `policy-impact` and
  `semantic` groups.
- Adaptation of permanent suite dependency and standards metadata dependency
  graphs to generic edge views where this removes duplicated graph mechanics.
- Exact inventory and deferred triggers for all other reviewed mechanisms.
- Planning policy-impact projection updates and exact review dispositions.

### Out Of Scope

- M6-I17 or any unrelated Bash-verifier migration package.
- Changes to the temporary Bash-checker graph schema, generated graph output,
  package lifecycle, or migration ordering.
- Automatic migration of table comparisons, owner maps, source closures,
  Markdown links, or other non-graph relations.
- A graph database, scheduler, inferred semantic links, compatibility schema,
  fallback lookup, or append-only impact history.
- Pantograph-specific graph behavior or third-party dependencies.

## Constraints And Assumptions

### Constraints

- `tools/graph_engine/` is upstream and imports no standards-verifier,
  planning, suite, migration, policy, or Bash-retirement code.
- All authoritative sources are explicitly registered declarative manifests or
  deterministic providers. Queries never scan for declarations or infer
  relationships from links, names, paths, ownership, `Requires`, or topology.
- Generic diagnostics remain neutral. Domain adapters translate failures and
  validate opaque domain metadata.
- One edge is declared once and may belong to several groups without being
  copied. Derived indexes and reports are never authority.
- Repository paths are contained after symlink resolution. Existing artifacts
  without edges, missing artifacts, and unknown logical IDs remain distinct.
- Exact-edge traversal follows one edge. Group traversal follows only selected,
  eligible group edges in an explicit direction. Transitive traversal requires
  group permission, terminates cycles, and reports deterministic explanatory
  paths and provenance.
- Shared graph, registry, standards, plans, generated artifacts, and acceptance
  state have one serial integration owner.
- No temporary checker-graph or M6-I17 file is in an allowed write set.

### Assumptions

- A repository-local Python package is the smallest neutral owner because no
  neutral graph component exists at the accepted base.
- Explicit node aliases can unify logical IDs and repository paths without
  changing the canonical identity owned by each downstream domain.
- Suite and metadata dependency sources can produce generic edges while their
  existing TOML and Markdown declarations remain their sole domain authority.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Neutral owner | `tools/graph_engine/` owns only graph mechanics and neutral errors. | [Inventory](reports/graph-consumer-inventory.tsv) found no existing neutral owner. | Downstream graph implementations owning shared mechanics |
| Canonical authority | Explicit registered sources own nodes, groups, and edges; indexes are derived in memory. | Objective and no-dual-authority constraint | Independent forward and reverse declarations |
| Identity | Edge IDs and group IDs are declared stable identifiers; line numbers and declaration locations are provenance only. | Stable query and migration requirements | Location-derived identities |
| Aliases | One resolver maps explicit logical and repository-path aliases to one canonical node and rejects contradictions and escapes. | Required Planning and suite alias behavior | Endpoint-specific lookup logic |
| Groups | A graph is a filtered view of edges in named groups; one edge may join several groups. | Generic data model | Separate storage per domain graph |
| Metadata | The core transports immutable extension metadata but does not interpret it. | Dependency direction | Policy fields in generic models |
| Traversal | Direction is explicit; transitive traversal is denied unless the selected group permits it. | Traversal safety requirements | Implicit closure |
| Policy impact | The current manifest is replaced by one generic graph manifest loaded through the source registry; a downstream policy adapter owns semantic validation and suite-owner closure. | Mandatory migration | `PolicyImpact` graph and bespoke reverse query |
| Permanent dependencies | Suite `requires` and metadata `Requires`/`Specializes` retain their domain declarations but use generic edge construction and traversal/cycle mechanics. | [Inventory](reports/graph-consumer-inventory.tsv) | Duplicated closure and cycle implementations |
| Temporary migration graph | Keep its frozen schema, generated output, SCCs, waves, and lifecycle unchanged until zero-Bash closure. | Active verifier migration authority | Architectural-uniformity migration |

## Simplicity And Ownership Review

- Independent concepts: neutral edge mechanics, domain declarations, domain
  validation, and temporary migration lifecycle.
- Intentional coupling: adapters construct or load generic nodes/groups/edges;
  the core knows no adapter.
- Accidental coupling risk: import bootstrapping, policy metadata leakage, or
  treating temporary checker topology as permanent graph authority.
- Policy/state/lifecycle owners: policy adapter and suite registry remain
  downstream owners; this plan owns only recovery state.
- Future changes that remain independent: new edge groups and validators do not
  modify core storage or traversal unless they require a genuinely generic
  capability.

## Canonical Models And Interface

- `Node`: canonical ID, explicit aliases, provenance, and opaque metadata.
- `Edge`: stable ID, canonical source and target, relation, one or more group
  IDs, provenance, opaque metadata, and traversal eligibility.
- `EdgeGroup`: stable ID, purpose, allowed directions, transitive permission,
  provenance, and optional validator registration name.
- `EdgeSource`: explicitly registered manifest or deterministic provider.
- `NodeResolver`: canonical ID and alias resolution with containment checks.
- `EdgeRegistry`: immutable indexes for incoming, outgoing, incident,
  edge-to-groups, group-to-edges, and provenance queries.
- `TraversalResult`: deterministic visited nodes, edges, explanatory paths,
  and provenance.

The canonical repository command will be `python3 tools/query_edges.py` with
mutually exclusive `--node`, `--edge`, and `--list-groups` selectors; explicit
`--direction`; optional `--group`; `--traverse`; and `--transitive`. Its
default TSV output rejects record-breaking control characters rather than
silently emitting malformed records.

## Migration Dispositions

The canonical inventory is
[graph-consumer-inventory.tsv](reports/graph-consumer-inventory.tsv).

- `migrate-now`: policy-impact storage, reverse lookup, and query.
- `adapt-now`: registered suite dependency closure/order and standards metadata
  dependency cycle validation.
- `defer`: temporary Bash graph and migration-package prerequisite/lifecycle
  authority until their listed retirement triggers.
- `retain-specialized`: executable-edge dispositions and source/owner closure
  assertions that compare explicit lifecycle or membership tables.
- `not-a-graph`: ordinary relation/keyed-relation checks, Markdown links, and
  generated owner maps.

## Milestones

### Milestone 1: Neutral Graph Engine Foundation

**Goal:** accept the upstream package, strict source schema, deterministic
query interface, and all required neutral graph behavior before any downstream
authority depends on it.

**Allowed write set:**

- `tools/graph_engine/**`
- `docs/plans/generic-edge-system/plan.md`
- `docs/plans/generic-edge-system/execution-ledger.md`
- `docs/plans/generic-edge-system/issues.md`
- `docs/plans/generic-edge-system/reports/**`

**Tasks:**

- [x] Implement neutral models, errors, source registration, alias resolution,
  immutable indexes, deterministic queries, exact-edge traversal, and
  explicitly permitted group traversal.
- [x] Implement the strict generic TOML source loader and read-only CLI.
- [x] Prove all 22 required core behaviors, including cycles, hostile output,
  containment, unregistered sources, and declaration-order independence.
- [x] Confirm the package has no downstream imports and accept its public
  contract before migration.

**Acceptance gate:** focused and complete graph-engine tests pass; CLI smoke
queries pass; dependency-direction inspection, link checks, plan structure,
`git diff --check`, and staged write-set review pass.

**Status:** `Accepted`

### Milestone 2: Downstream Graph Migration And Acceptance

**Goal:** replace the bespoke policy graph and duplicated permanent dependency
mechanics with generic groups and adapters, then accept the complete objective.

**Allowed write set:**

- `tools/graph_engine/graph_engine/manifest.py`
- `tools/graph_engine/graph_engine/cli.py`
- `tools/graph_engine/graph_engine/registry.py`
- `tools/graph_engine/graph_engine/__init__.py`
- `tools/graph_engine/query_edges.py` (delete after canonical composition entrypoint)
- `tools/graph_engine/tests/test_manifest.py`
- `tools/graph_engine/tests/test_cli.py`
- `tools/graph_engine/tests/test_registry.py`
- `tools/standards_verifier/pyproject.toml`
- `tools/standards_verifier/verify.py`
- `tools/standards_verifier/query_policy_impact.py` (delete)
- `tools/standards_verifier/standards_verifier/config.py`
- `tools/standards_verifier/standards_verifier/engine.py`
- `tools/standards_verifier/standards_verifier/graph_adapters.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/standards_verifier/checks/metadata.py`
- `tools/standards_verifier/standards_verifier/checks/policy_impact.py`
- `tools/standards_verifier/standards_verifier/policy_impact.py`
- `tools/standards_verifier/standards_verifier/policy_impact_cli.py` (delete)
- `tools/standards_verifier/tests/test_engine.py`
- `tools/standards_verifier/tests/test_metadata.py`
- `tools/standards_verifier/tests/test_policy_impact.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `tools/query_edges.py`
- `tools/standards_verifier/README.md`
- `evaluation/standards-effectiveness/policy-semantic-impact.toml`
- `evaluation/standards-effectiveness/edge-source-registry.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/**`
- `evaluation/standards-effectiveness/suites/policy-semantic-impact.toml`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `workflows/planning.md`
- every additional Planning consumer returned by the accepted pre-migration
  query, but only after an exact disposition is recorded in this plan's reports
- this plan directory and the two parent active plans/ledgers only for current
  authority, accepted state, or material verification evidence

**Tasks:**

- [x] Add generic deterministic cycle detection and dependency ordering needed
  by both permanent dependency adapters; do not recreate DFS in either domain.
- [x] Register one generic policy graph source, migrate all 24 Planning edges,
  and preserve policy-specific diagnostics and audited-suite closure in an
  adapter over `policy-impact` edges.
- [x] Replace the bespoke policy query with the generic CLI and remove all old
  storage, reverse-index, schema, and query authority.
- [x] Adapt suite dependency and metadata relation validation to named generic
  groups without changing their canonical input formats or diagnostics.
- [x] Record exact Planning consumer dispositions; update only affected
  standards, prompts, templates, fixtures, suites, and documentation.
- [x] Run focused downstream tests, all Python tests, every declarative suite,
  generated freshness, affected plan/link checks, and the complete mixed
  checkpoint.
- [x] Register the adapted suite and metadata providers beside the policy
  manifest in one repository composition without adding downstream imports to
  the neutral engine.
- [x] Make the canonical generic query use that composition and prove an
  arbitrary artifact can discover all incident migrated groups without
  knowing which source declared them.

**Acceptance gate:** all objective claims pass; both Planning aliases return
the same 24 policy-impact edges; no bespoke policy graph/reverse index or old
query/manifest fallback remains; adapted consumers preserve diagnostics and
formats; deferred mechanisms remain unchanged; staged scope is exact; accepted
commits leave the canonical worktree clean.

**Status:** `Accepted`

## Verification Gates

1. Foundation: graph unit tests, CLI tests, dependency-direction inspection,
   plan structure, links, diff check, staged review.
2. Migration: focused policy, suite dependency, and metadata tests; negative
   policy fixtures; generic alias/query integration; no-old-authority search.
3. Complete: all graph and standards-verifier unit tests, all registered
   declarative suites, generated freshness, affected plan and Markdown checks,
   complete mixed checkpoint, `git diff --check`, staged write-set review, and
   clean canonical repository.

## Blockers

- `none`

## Re-Plan Triggers

- No neutral upstream owner can be kept independent of downstream consumers.
- Another active component owns incompatible canonical node or edge identity.
- A justified migration requires changing the frozen temporary graph schema or
  generated migration output.
- Generic behavior begins depending on policy, suite, metadata, planning, or
  migration semantics.
- One declaration cannot provide stable bidirectional lookup, aliases resolve
  to conflicting nodes, or traversal cannot be made explicit.
- Implementation requires an unregistered source, inferred edge, dual
  authority, compatibility copy, or fallback lookup.
- The migration expands materially beyond this inventory or exact write sets.
- The accepted base or shared authority changes before integration.

## Concurrent Work

Implementation and shared integration are serial because the graph API,
policy manifest, verifier adapters, suite registry, standards projections, and
acceptance state are shared authority. Read-only investigation may be
delegated, but no concurrent writer may edit these sets.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: temporary Bash graph and package-lifecycle mechanisms
  remain governed by their explicit inventory triggers.
- Final status: `Accepted`
