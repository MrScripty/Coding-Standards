# Plan: Python Verification Engine Design Recovery

**Plan status:** `Active`

**Current phase:** Milestone 5 terminal migration lifecycle and Bash retirement

**Next slice:** run a fresh post-M6-I123 checker graph audit; do not preselect
the next Bash-retirement package from earlier evidence

**Acceptance status:** `pending`

**Accepted base:** `56f5124b1ed848fa80b8f35e46a298d4a33ed37c`

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
| A1 | Every metadata-bearing canonical document is queryable by logical ID and path alias, with normative/routable membership, `Requires`, and `Specializes` derived from canonical metadata rather than validation-suite selection. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 1 acceptance](execution-ledger.md#2026-08-21-milestone-1-acceptance) |
| A2 | Verifier-interface scenarios select exact canonical modules and their graph-derived transitive `Requires` closure from Router facts, including positive, negative, and unresolved cases. | `focused` | `not-applicable` | `automated` | `satisfied` | [Milestone 7 routing evidence](reports/milestone-7-routing-and-candidates.md) |
| A3 | One validated immutable suite catalog supplies execution and checks; assertions and invalid, unavailable, and unsupported conditions return their documented statuses. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 2 acceptance](execution-ledger.md#2026-08-21-milestone-2-acceptance) |
| A4 | `source_index_closure` and `acceptance_claims` policy are expressed through the smallest owned mechanics without compatibility adapters, policy literals in generic checks, or independently repeated source-membership sets. | `integration` | `not-applicable` | `automated` | `satisfied` | [Milestone 8 shared-contract acceptance](reports/milestone-8-shared-contracts.md) |
| A5 | Named list, focused, all-suite, generated-artifact, and complete workloads have owned performance claims with identified budget authority and current three-sample complete-workload evidence. | `focused` | `representative` | `automated` | `satisfied` | [Milestone 9 current performance and recovery acceptance](reports/milestone-9-current-performance-and-acceptance.md) |
| A6 | Every mechanically derived migration-only Python candidate has one terminal disposition, and zero-Bash closure removes every item without a current post-migration consumer. | `complete` | `not-applicable` | `automated` | `pending` | Candidate completeness is satisfied by [Milestone 7 evidence](reports/milestone-7-routing-and-candidates.md); terminal deletion remains due at zero Bash. |
| A7 | Graph, verifier, declarative, generated, plan, link, and mixed gates pass without dual authority, fallback, or a changed temporary Bash graph schema. | `complete` | `not-applicable` | `automated` | `satisfied` | [Milestone 9 current performance and recovery acceptance](reports/milestone-9-current-performance-and-acceptance.md) |

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

**Applicability:** `applicable`

- Independent concepts and dimensions: neutral graph mechanics, canonical corpus membership,
  metadata parsing, suite catalog loading, check execution, policy adapters,
  performance evidence, and migration lifecycle.
- State, identity, value, time, policy, and mechanism: canonical documents own
  policy identity and metadata values; the catalog owns invocation state;
  migration lifecycle remains in this plan rather than generic mechanics.
- Caller and composition-root knowledge: the repository composition root injects explicit
  metadata and suite providers into the neutral graph; verifier checks consume
  one catalog through their execution context.
- Representative change paths and forced owners: adding a canonical Module
  changes corpus membership and metadata loading without changing neutral
  graph mechanics; adding a suite changes catalog data without check-local
  parsing.
- Stable Interfaces versus hidden knowledge: copying metadata into the corpus manifest, exposing
  policy schemas through generic checks, or retaining migration modules because
  tests or incumbent imports exist would leak hidden knowledge across an
  otherwise stable provider Interface.
- Independent evolution, testing, failure, and replacement: canonical documents own standards metadata;
  Router owns applicability; suites and fixtures own policy; the verifier owns
  mechanics; the migration plan owns temporary lifecycle, so those concerns can
  be tested, fail, and be replaced independently.
- Necessary complexity and containment: strict providers, typed outcomes, and
  migration adapters exist only for accepted corpus, execution, and retirement
  contracts and remain behind the verifier Module's Interfaces.
- Deletion and cumulative machinery result: migration-only paths require a
  current consumer and terminal disposition; pass-through or incumbent-only
  machinery is deleted, while retained generic mechanics must still provide
  Leverage over their exposed Interface.

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

- [x] Add one strict path-only corpus owner for every metadata-bearing canonical
  document.
- [x] Load and validate every member's canonical metadata once for graph
  composition without depending on semantic suite checks.
- [x] Derive the normative/routable view from canonical `Role` metadata without
  storing a second membership list.
- [x] Prove exact ID/path alias parity, complete `Requires`/`Specializes`, typed
  duplicate/missing/escape failures, and independence from suite composition.
- [x] Add positive, negative, and unresolved routing decisions for verifier
  interface, local check, graph composition, migration cleanup, and measured
  performance scenarios.
- [x] Confirm the neutral graph package remains unchanged and upstream.

**Acceptance gate:** focused catalog/repository-graph/routing tests, all graph
and verifier tests, all declarative suites, exact logical/path queries including
`topic.performance`, generated freshness, affected plan/link checks, complete
mixed checkpoint, diff check, and staged review pass.

**Status:** `Accepted`

### Milestone 2: Single Catalog And Result Semantics

**Goal:** remove duplicate suite authority and make every check obey one result
classification contract.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/config.py`
- `tools/standards_verifier/standards_verifier/model.py`
- `tools/standards_verifier/standards_verifier/engine.py`
- `tools/standards_verifier/standards_verifier/diagnostics.py`
- `tools/standards_verifier/standards_verifier/checks/edge_dispositions.py`
- `tools/standards_verifier/standards_verifier/checks/policy_impact.py`
- `tools/standards_verifier/standards_verifier/checks/derived_evidence.py`
- `tools/standards_verifier/standards_verifier/checks/source_index_closure.py`
- `evaluation/standards-effectiveness/suites/executable-edge-dispositions.toml`
- affected verifier tests and README sections
- affected declarative suite evidence
- this plan directory and parent current-state plans

**Tasks:**

- [x] Define the smallest immutable catalog interface needed by execution and
  catalog-aware checks.
- [x] Parse registry and suite bodies through one strict owner.
- [x] Remove raw registry and suite TOML parsing from `edge_dispositions`.
- [x] Route assertion diagnostics through status `1` and retain exact statuses
  for invalid, unavailable, and unsupported outcomes.
- [x] Add shared cross-check-kind status-contract evidence.

**Acceptance gate:** focused catalog, edge-disposition, and exit-contract tests;
all Python and declarative gates; generated freshness; complete mixed checkpoint;
and no fallback parser pass.

**Status:** `Accepted`

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
- `evaluation/standards-effectiveness/suites/root-index-closure.toml`
- directly affected fixtures and documentation
- `tools/standards_verifier/tests/test_routing_checks.py`
- `tools/standards_verifier/tests/test_engine.py`
- `tools/standards_verifier/tests/test_source_index_closure.py`
- `docs/plans/python-verification-engine-recovery/reports/milestone-3-interface-disposition.md`
- this plan directory and parent current-state plans

**Tasks:**

- [x] Map each source-index responsibility to an existing mechanic before
  adding one.
- [x] Select declarative composition or a policy adapter from module depth,
  locality, and interface evidence rather than consumer count.
- [x] Preserve positive, negative, ordering, membership, route, line-budget,
  no-fallback, and typed-outcome evidence.
- [x] Delete replaced check kinds, implementations, parser branches, and private
  tests in the accepting slice.

**Acceptance gate:** the two migrated suites preserve mutation parity; their
generic implementations contain no source-index, Router, canonical Verification,
or migration-state policy literals; all broad gates pass; no wrapper or dual
authority remains.

**Status:** `Accepted`

### Milestone 4: Measured Loading And Performance

**Goal:** establish owned performance claims and improve fault isolation or
performance only where representative evidence justifies change.

**Allowed write set:**

- performance claim and measurement evidence under this plan's `reports/`
- `tools/standards_verifier/standards_verifier/config.py`
- `tools/standards_verifier/standards_verifier/engine.py`
- `tools/standards_verifier/standards_verifier/model.py`
- `tools/standards_verifier/standards_verifier/checks/edge_dispositions.py`
- generated-artifact orchestration modules only when measurements select that
  work
- `tools/standards_verifier/tests/test_engine.py`
- `tools/standards_verifier/tests/test_edge_dispositions.py`
- `tools/standards_verifier/tests/test_derived_evidence.py`
- `tools/standards_verifier/tests/test_file_contracts.py`
- `tools/standards_verifier/tests/test_metadata.py`
- `tools/standards_verifier/tests/test_routing_checks.py`
- affected verifier documentation
- this plan directory and parent current-state plans

**Tasks:**

- [x] Define list, focused, all-suite, generated-artifact, and complete
  workloads with metric, environment, baseline, variability, and consumer
  impact.
- [x] Decide strict focused-loading behavior from correctness and fault-isolation
  claims before changing loading.
- [x] Load only the accepted catalog/body scope when measurements and semantics
  justify it.
- [x] Consolidate scans only when a measured claim is materially affected; do
  not add persistent caching.

**Acceptance gate:** claim-matched before/after evidence, unchanged correctness
and diagnostics, all broad gates, and no unmeasured optimization pass.

**Status:** `Accepted`

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

- [x] Record one `retain`, `replace`, or `delete` disposition, current consumer,
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

**Status:** `Active`; pre-resume disposition gate accepted

### Milestone 6: Audit Follow-Up Admission And Current Baseline

**Goal:** replace stale acceptance claims with current authority and record the
applicability decisions required before shared verifier interfaces change.

**Allowed write set:**

- this plan and its execution ledger
- `docs/plans/standards-verification-engine/plan.md`
- current-baseline and applicability reports under this plan's `reports/`

**Tasks:**

- [x] Record the exact clean accepted revision and current suite, Bash, graph,
  test, and workload populations.
- [x] Record explicit Architecture applicability for the already accepted table
  membership/conditional-row changes and each proposed shared-interface change.
- [x] Select Performance for the measurement contract and identify the owner and
  derivation of every retained or revised budget.
- [x] Keep Bash retirement paused and admit no migration package.

**Acceptance gate:** current facts replace stale projections, each proposed
shared change has an explicit Router applicability result, performance claims
have an identified owner and derivation, and no implementation change is mixed
into admission.

**Status:** `Accepted`; evidence in
[audit-follow-up admission](reports/audit-follow-up-admission.md)

### Milestone 7: Exact Routing And Terminal Candidate Completeness

**Goal:** prove route decisions against exact canonical module identities and
graph-derived closure, and prove that terminal migration dispositions cover the
entire mechanically derived candidate set.

**Allowed write set:**

- downstream routing and migration-lifecycle adapters in
  `tools/standards_verifier/standards_verifier/`
- their focused unit tests
- `evaluation/standards-effectiveness/fixtures/s1/`
- `evaluation/standards-effectiveness/suites/s1-routing.toml`
- migration disposition and candidate evidence under
  `evaluation/standards-effectiveness/`
- affected generated evidence and verifier documentation
- this plan and its execution ledger

**Tasks:**

- [x] Represent expected direct route selections without copying graph edges.
- [x] Resolve selected modules through canonical metadata and compare exact
  graph-derived transitive `Requires` closure for every scenario.
- [x] Preserve positive, negative, unresolved, and no-inference behavior.
- [x] Derive migration-only candidates from explicit provider or registration
  authority, compare them exactly with disposition subjects, and add a deletion
  mutation test.

**Acceptance gate:** each route scenario proves exact direct selections and
closure; candidate and disposition sets are exactly equal; deleting a candidate
disposition fails; no lexical inference, duplicate authority, or fallback is
introduced.

**Status:** `Accepted`; evidence in
[routing and candidate completeness](reports/milestone-7-routing-and-candidates.md)

### Milestone 8: Shared Contract Simplification

**Goal:** remove duplicated parsing and repeated policy configuration while
keeping generic mechanics policy-neutral.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/checks/table.py`
- `tools/standards_verifier/standards_verifier/diagnostics.py`
- direct verifier callers and focused tests affected by those contracts
- `evaluation/standards-effectiveness/suites/source-index-closures.toml`
- one policy-owned source-index membership provider and its focused evidence
- affected verifier documentation
- this plan and its execution ledger

**Tasks:**

- [x] Extract one projection parser and layer source-specific requirements on
  the shared parsed representation.
- [x] Remove the redundant numeric `EngineError.exit_code` input and derive it
  solely from the diagnostic outcome.
- [x] Establish one policy-owned source-index membership set and consume it by
  bounded composition without a generic query language.
- [x] Record the explicit Architecture result for the final design before
  changing exposed module or dependency responsibility.

**Acceptance gate:** projection syntax has one parser, exit status has one
authority, source membership has one policy owner, existing diagnostics and
mutation behavior remain exact, and no compatibility path remains.

**Status:** `Accepted`; evidence in
[shared-contract acceptance](reports/milestone-8-shared-contracts.md)

### Milestone 9: Current Performance And Recovery Acceptance

**Goal:** revalidate the current repository workload using the declared
measurement contract and accept the recovery only from current evidence.

**Allowed write set:**

- performance reports under this plan's `reports/`
- this plan and its execution ledger
- verification-engine and parent current-state plans

**Tasks:**

- [x] Measure list, focused, all-suite, and generated-artifact workloads using
  the accepted sampling method.
- [x] Run three serial complete-workload samples and report median and range.
- [x] Compare current evidence with budgets whose owner and derivation are
  recorded; revise claims rather than fitting implementation to arbitrary
  numbers.
- [x] Run all broad recovery gates and resume Bash retirement only after
  current acceptance.

**Acceptance gate:** current claim-matched evidence satisfies owned budgets or
produces an explicit re-plan; all graph, verifier, declarative, generated, plan,
link, mixed, and diff gates pass from a clean boundary.

**Status:** `Accepted`; evidence in
[current performance and recovery acceptance](reports/milestone-9-current-performance-and-acceptance.md)

## Blockers

- `none`

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
- Exact route evidence cannot be derived from canonical metadata without
  duplicating dependency authority in fixtures.
- Migration-only candidate completeness cannot be derived from explicit
  provider or registration authority without lexical inference or a duplicate
  hand-maintained inventory.
- Source-index membership cannot be composed once without a generalized query
  language or policy logic in generic checks.
- Current three-sample complete-workload evidence exceeds an owned budget or
  exposes material unexplained variance.
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
