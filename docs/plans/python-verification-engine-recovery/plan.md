# Plan: Python Verification Engine Design Recovery

**Plan status:** `Active`

**Current phase:** Milestone 1 canonical graph and routing foundation

**Next slice:** establish the all-canonical path corpus, metadata-derived graph,
and fact-driven verifier routing evidence

**Acceptance status:** `pending`

**Accepted base:** `08190314808665cfe8ab10a0284d90274ac6f021`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Restore a small, repository-neutral Python verification interface whose graph,
configuration, result, loading, and terminal migration behavior have one
canonical owner. The recovery must make every metadata-bearing canonical
document and its complete metadata dependencies discoverable, derive
normative/routable views from canonical roles, remove policy-specific engine
interfaces, improve focused execution only against accepted measurements, and
prevent temporary Bash-migration mechanics from becoming permanent authority.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Every metadata-bearing canonical document is queryable by logical ID and path alias, with normative/routable membership, `Requires`, and `Specializes` derived from canonical metadata rather than validation-suite selection. | `integration` | `not-applicable` | `automated` | `pending` | Milestone 1 |
| A2 | Verifier-interface scenarios select Architecture and Performance only from Router facts, including positive, negative, and unresolved cases. | `focused` | `not-applicable` | `automated` | `pending` | Milestone 1 |
| A3 | One validated immutable suite catalog supplies execution and checks; assertions and invalid, unavailable, and unsupported conditions return their documented statuses. | `integration` | `not-applicable` | `automated` | `pending` | Milestone 2 |
| A4 | `source_index_closure` and `acceptance_claims` policy are expressed through the smallest owned mechanics without compatibility adapters or policy literals in generic checks. | `integration` | `not-applicable` | `automated` | `pending` | Milestone 3 |
| A5 | Named list, focused, all-suite, generated-artifact, and complete workloads have owned performance claims; loading or scan changes occur only when accepted measurements justify them. | `focused` | `representative` | `automated` | `pending` | Milestone 4 |
| A6 | Every migration-only Python module and check kind has one terminal disposition, and zero-Bash closure removes every item without a current post-migration consumer. | `complete` | `not-applicable` | `automated` | `pending` | Milestone 5 and verification-engine zero-Bash acceptance |
| A7 | Graph, verifier, declarative, generated, plan, link, and mixed gates pass without dual authority, fallback, or a changed temporary Bash graph schema. | `complete` | `not-applicable` | `automated` | `pending` | Final acceptance |

## Scope

### In Scope

- Canonical standards-module corpus membership and metadata graph composition.
- Fact-driven routing evidence for verifier interface, architecture,
  performance, migration, and graph-composition changes.
- One validated suite catalog per verifier invocation.
- Result and process-exit classification across check kinds.
- Removal or recomposition of policy-specific `source_index_closure` and
  `acceptance_claims` engine interfaces.
- Owned performance claims and evidence for verifier loading and repository
  scanning.
- Exact terminal dispositions for migration-only Python modules and check
  kinds.
- Current-state projection into the verification-engine and parent plans.

### Out Of Scope

- Further Bash-checker migration packages until Milestones 1 through 4 and the
  terminal-disposition table are accepted.
- Changes to the frozen temporary Bash graph schema, generated artifact format,
  migration package ordering, or accepted package history.
- Changes to neutral graph storage, traversal, or identity unless evidence
  proves a missing repository-neutral capability.
- A generalized expression language, persistent cache, inferred metadata edge,
  duplicate metadata manifest, compatibility parser, or fallback lookup.
- Normative standards changes when current Router, Architecture, Performance,
  Verification, and Core policy already express the required behavior.

## Constraints And Assumptions

### Constraints

- `tools/graph_engine/` remains upstream and imports no standards-verifier,
  metadata, routing, planning, policy, or migration code.
- Corpus membership is explicit. The membership owner stores canonical document
  paths only; document metadata remains the sole authority for module ID,
  canonical-owner alias, `Requires`, and `Specializes`.
- Queries do not infer modules or edges from links, names, directory placement,
  suite ownership, or `metadata_graph` participation.
- The suite registry and suite bodies are parsed through one strict owner; a
  check cannot open and reinterpret them independently.
- Assertion failures use the ordinary result path. Exceptions represent
  invalid, unavailable, or unsupported execution conditions.
- Policy-specific verification may remain a downstream adapter only when its
  interface owns a coherent invariant and keeps policy out of generic mechanics.
- Performance implementation changes require accepted claim-matched evidence.
- Shared graph composition, engine interfaces, registries, plans, and acceptance
  state integrate serially.

### Assumptions

- The accepted neutral graph interface already provides all storage, incidence,
  provenance, filtering, cycle, and dependency-order mechanics required here.
- The observed corpus currently contains 58 metadata-bearing canonical
  documents, including 44 normative/routable modules and 14 references. These
  are derived observations, not stored acceptance constants.
- A strict path-only corpus manifest is the smallest non-inferred membership
  authority compatible with explicit source registration.
- Bash migration can resume after the pre-zero-Bash recovery gates are accepted
  and a terminal-disposition table governs remaining migration-only Python.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Graph contract | The repository graph provides a complete dependency view for all metadata-bearing canonical documents; normative/routable views are derived from canonical roles. | [Design audit](../standards-verification-engine/reports/python-engine-standards-design-audit.md#sw-02--canonical-module-graph-coverage-depends-on-verification-suites) and accepted corpus re-plan | Validation-suite-selected metadata coverage |
| Corpus authority | One reviewed path-only manifest owns all-canonical corpus membership; the provider derives module ID, role, aliases, and all edge facts from document metadata. | Audit SW-02, accepted corpus re-plan, and Core single-authority rule | Suite checks as implicit corpus membership |
| Router applicability | Shared-interface changes require an explicit Architecture applicability result; Architecture and Performance are selected only when Router facts are present. | Audit SW-01/SW-04 | Automatic or omitted topic selection |
| Catalog authority | One immutable validated catalog owns registry entries and loaded suite identities for an invocation. | Audit PE-02 | Check-local TOML reparsing |
| Result semantics | Assertion mismatches return `1`; invalid representation/configuration returns `2`; unavailable returns `3`; unsupported returns `4`. | Engine README and audit PE-04 | Exception-default status for assertion failures |
| Policy interfaces | Module depth and coherent ownership decide retention; consumer count does not. Policy literals remain outside generic checks. | Core and audit PE-01/PE-07 | One-consumer and second-consumer thresholds |
| Performance | Measure named workflows before changing loading, scans, or caching; retain the simplest implementation satisfying accepted claims. | Performance topic and audit PE-03/PE-06 | Unowned speed claims |
| Terminal lifecycle | Every migration-only Python path receives `retain`, `replace`, or `delete` with a current consumer and trigger; no default retention. | Audit PE-05 | Literal zero-Bash closure without Python disposition |

## Simplicity And Ownership Review

- Independent concepts: neutral graph mechanics, canonical corpus membership,
  metadata parsing, suite catalog loading, check execution, policy adapters,
  performance evidence, and migration lifecycle.
- Intentional coupling: the repository composition root injects explicit
  metadata and suite providers into the neutral graph; verifier checks consume
  one catalog through their execution context.
- Accidental coupling risk: copying metadata into the corpus manifest, exposing
  policy schemas through generic checks, or retaining migration modules because
  tests or incumbent imports exist.
- Policy/state/lifecycle owners: canonical documents own standards metadata;
  Router owns applicability; suites and fixtures own policy; the verifier owns
  mechanics; the migration plan owns temporary lifecycle.
- Future changes that should remain independent: adding a standards module
  changes membership and metadata but not graph mechanics; adding a suite
  changes catalog data but not check-local parsers; changing policy changes
  suites or adapters but not generic checks.

## Milestones

### Milestone 1: Canonical Graph And Routing Foundation

**Goal:** make every metadata-bearing canonical document and unconditional
dependency queryable from explicit membership, derive normative/routable views
from document roles, and prove verifier-related Router applicability.

**Allowed write set:**

- `evaluation/standards-effectiveness/canonical-module-corpus.toml`
- `evaluation/standards-effectiveness/fixtures/routing/**`
- `evaluation/standards-effectiveness/suites/s1-routing.toml`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/standards_verifier/standards_verifier/canonical_modules.py`
- `tools/standards_verifier/tests/test_repository_graph.py`
- `tools/standards_verifier/tests/test_canonical_modules.py`
- `tools/standards_verifier/README.md`
- this plan directory
- `docs/plans/standards-verification-engine/plan.md`
- `plans/standards-library-effectiveness-restructure-plan.md`

**Tasks:**

- [ ] Add one strict path-only corpus owner for every metadata-bearing canonical
  document.
- [ ] Load and validate every member's canonical metadata once for graph
  composition without depending on semantic suite checks.
- [ ] Derive the normative/routable view from canonical `Role` metadata without
  storing a second membership list.
- [ ] Prove exact ID/path alias parity, complete `Requires`/`Specializes`, typed
  duplicate/missing/escape failures, and independence from suite composition.
- [ ] Add positive, negative, and unresolved routing decisions for verifier
  interface, local check, graph composition, migration cleanup, and measured
  performance scenarios.
- [ ] Confirm the neutral graph package remains unchanged and upstream.

**Acceptance gate:** focused catalog/repository-graph/routing tests, all graph
and verifier tests, all declarative suites, exact logical/path queries including
`topic.performance`, generated freshness, affected plan/link checks, complete
mixed checkpoint, diff check, and staged review pass.

**Status:** `Active`

### Milestone 2: Single Catalog And Result Semantics

**Goal:** remove duplicate suite authority and make every check obey one result
classification contract.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/config.py`
- `tools/standards_verifier/standards_verifier/model.py`
- `tools/standards_verifier/standards_verifier/engine.py`
- `tools/standards_verifier/standards_verifier/diagnostics.py`
- `tools/standards_verifier/standards_verifier/checks/edge_dispositions.py`
- affected verifier tests and README sections
- affected declarative suite evidence
- this plan directory and parent current-state plans

**Tasks:**

- [ ] Define the smallest immutable catalog interface needed by execution and
  catalog-aware checks.
- [ ] Parse registry and selected suite bodies through one strict owner.
- [ ] Remove raw registry and suite TOML parsing from `edge_dispositions`.
- [ ] Route assertion diagnostics through status `1` and retain exact statuses
  for invalid, unavailable, and unsupported outcomes.
- [ ] Add shared cross-check-kind status-contract evidence.

**Acceptance gate:** focused catalog, edge-disposition, and exit-contract tests;
all Python and declarative gates; generated freshness; complete mixed checkpoint;
and no fallback parser pass.

**Status:** `Planned`

### Milestone 3: Policy-Specific Interface Removal

**Goal:** replace the `source_index_closure` and `acceptance_claims` engine
interfaces with the smallest owned generic mechanics or downstream adapter.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/checks/source_index_closure.py`
- `tools/standards_verifier/standards_verifier/checks/acceptance_claims.py`
- `tools/standards_verifier/standards_verifier/checks/__init__.py`
- directly affected generic check modules and tests when a missing neutral
  mechanic is proven
- `evaluation/standards-effectiveness/suites/source-index-closures.toml`
- `evaluation/standards-effectiveness/suites/acceptance-claims.toml`
- directly affected fixtures and documentation
- this plan directory and parent current-state plans

**Tasks:**

- [ ] Map each source-index responsibility to an existing mechanic before
  adding one.
- [ ] Select declarative composition or a policy adapter from module depth,
  locality, and interface evidence rather than consumer count.
- [ ] Preserve positive, negative, ordering, membership, route, line-budget,
  no-fallback, and typed-outcome evidence.
- [ ] Delete replaced check kinds, implementations, parser branches, and private
  tests in the accepting slice.

**Acceptance gate:** the two migrated suites preserve mutation parity; their
generic implementations contain no source-index, Router, canonical Verification,
or migration-state policy literals; all broad gates pass; no wrapper or dual
authority remains.

**Status:** `Planned`

### Milestone 4: Measured Loading And Performance

**Goal:** establish owned performance claims and improve fault isolation or
performance only where representative evidence justifies change.

**Allowed write set:**

- performance claim and measurement evidence under this plan's `reports/`
- `tools/standards_verifier/standards_verifier/config.py`
- `tools/standards_verifier/standards_verifier/engine.py`
- generated-artifact orchestration modules only when measurements select that
  work
- affected tests and verifier documentation
- this plan directory and parent current-state plans

**Tasks:**

- [ ] Define list, focused, all-suite, generated-artifact, and complete
  workloads with metric, environment, baseline, variability, and consumer
  impact.
- [ ] Decide strict focused-loading behavior from correctness and fault-isolation
  claims before changing loading.
- [ ] Load only the accepted catalog/body scope when measurements and semantics
  justify it.
- [ ] Consolidate scans only when a measured claim is materially affected; do
  not add persistent caching.

**Acceptance gate:** claim-matched before/after evidence, unchanged correctness
and diagnostics, all broad gates, and no unmeasured optimization pass.

**Status:** `Planned`

### Milestone 5: Migration-Python Terminal Lifecycle

**Goal:** govern every temporary Python module through zero-Bash closure and
delete all implementation without a current post-migration consumer.

**Allowed write set:**

- `evaluation/standards-effectiveness/migration-python-dispositions.tsv`
- migration-only verifier modules, check registrations, tests, suites,
  generated artifacts, and documentation named by accepted dispositions
- verification-engine and parent plan/ledger current-state projections
- this plan directory

**Tasks:**

- [ ] Record one `retain`, `replace`, or `delete` disposition, current consumer,
  terminal trigger, and evidence owner for every migration-only module and check
  kind before checker migration resumes.
- [ ] Resume Bash retirement only under the accepted disposition authority.
- [ ] At zero Bash, remove temporary inventory, graph, retirement, edge, numeric,
  and retained-checkpoint paths according to the table.
- [ ] Prove the final Python-only command has one meaning and no migration
  compatibility authority.

**Acceptance gate:** the disposition table is complete before migration resumes;
at zero Bash every triggered disposition is satisfied, the repository-wide
policy-literal prohibition passes, and the Python-only complete checkpoint is
accepted.

**Status:** `Planned`

## Blockers

- Corpus scope is unresolved. A 44-member normative-only manifest would remove
  eight currently queryable reference nodes; an all-canonical corpus contains
  58 documents and materially broadens the audit's stated graph scope.
- Further Bash-checker package selection is paused until Milestones 1 through 4
  and the pre-resume terminal-disposition gate in Milestone 5 are accepted.

## Re-Plan Triggers

- Complete corpus membership cannot be owned without copying metadata authority
  or inferring modules from links, paths, suites, or topology.
- The neutral graph engine lacks a required generic capability or would need a
  downstream dependency.
- Routing evidence requires changing normative applicability rather than
  projecting current Router facts.
- One immutable catalog cannot support focused execution without dual parsing or
  weakening strict configuration.
- Source-index or acceptance-claim parity requires a generalized expression
  language, compatibility adapter, or policy literals in generic mechanics.
- Representative performance evidence does not justify a proposed loading or
  scan change.
- A migration-only Python path has a real post-zero-Bash consumer that the audit
  did not identify.
- Shared authority changes outside the admitted write set or another proposal
  makes the accepted base stale.

## Concurrent Work

Read-only investigation may be delegated. All writes remain serial because
corpus membership, graph composition, routing suites, engine interfaces,
registry/catalog authority, active plans, and acceptance state overlap.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: Milestone 5 deletion executes at the accepted zero-Bash
  trigger; its disposition table is not deferred.
- Final status: `Active`
