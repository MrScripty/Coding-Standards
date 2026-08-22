# Python Verification Engine Design Recovery Execution Ledger

## 2026-08-21: Plan Construction And Admission

- Plan path: `docs/plans/python-verification-engine-recovery/plan.md`.
- Operation: `start`.
- Accepted base: `08190314808665cfe8ab10a0284d90274ac6f021`.
- Preconditions: M6-I60 is accepted; no later checker package is admitted; the
  only pre-existing working-tree change is the reviewed design audit that this
  recovery adopts as investigation evidence.
- Architecture applicability: selected because corpus authority, graph
  composition, suite-catalog ownership, check interfaces, and dependency
  direction change. The neutral graph engine remains upstream and unchanged.
- Performance applicability: selected only for Milestone 4 and any measured
  loading or scan implementation; no optimization is authorized by diagnostic
  timings alone.
- Decision: use a complete canonical-module graph with explicit path-only corpus
  membership and metadata-derived node, alias, `Requires`, and `Specializes`
  facts.
- Coordination: pause Bash-checker packages; shared graph, verifier, registry,
  standards, plan, and acceptance writes remain serial.
- Result: Milestone 1 is the only admitted implementation slice.

## 2026-08-21: Canonical Corpus Scope Re-Plan

- Finding: the audit measures 44 normative/routable modules, but canonical
  metadata exists in 58 documents: 44 normative modules and 14 references.
- Current behavior: suite-derived composition exposes 28 normative and eight
  reference metadata documents. A 44-member replacement would therefore remove
  currently queryable reference nodes even while closing normative omissions.
- Impact: the corpus owner and objective scope cannot be accepted until
  reference membership is explicit. No engine or graph implementation began.
- Recommended resolution: register all 58 canonical metadata documents in one
  paths-only corpus and derive the normative 44 as the `Role != reference`
  view. IDs, aliases, roles, `Requires`, and `Specializes` remain derived from
  document metadata; counts remain observations.
- Status: plan and Milestone 1 are blocked pending the corpus-scope decision.

## 2026-08-21: All-Canonical Corpus Re-Admission

- Decision: accept the recommended all-canonical corpus. One reviewed
  paths-only manifest contains every metadata-bearing canonical document.
- Derivation boundary: document metadata remains the sole authority for module
  ID, role, path alias, `Requires`, and `Specializes`; normative/routable
  membership is the derived `Role != reference` view.
- Count authority: the observed total and role distribution are evidence only.
  Tests and acceptance do not hardcode corpus, node, or edge counts.
- No-fallback check: suite-selected metadata membership is replaced, not
  retained as a secondary provider or compatibility lookup.
- Admission: operation `continue`; Milestone 1 is active and is the only
  implementation slice.

## 2026-08-21: Milestone 1 Acceptance

- Replaced suite-selected metadata graph membership with the strict
  `canonical-module-corpus.toml` path authority. No old provider, fallback
  lookup, or duplicate metadata representation remains.
- Reused canonical metadata parsing and neutral graph adapters. Module IDs,
  roles, path aliases, `Requires`, and `Specializes` are derived from each
  document; normative membership is the derived non-reference view.
- Added fact-driven verifier-change routing evidence for Architecture,
  Performance, migration lifecycle, local changes, graph composition, and
  unresolved facts without changing normative Router text.
- Focused evidence: 34 corpus, metadata, and repository-graph tests passed;
  `s1-routing` passed 12 checks; logical and path aliases for
  `topic.performance` returned the same dependency edges.
- Broad evidence: 35 neutral graph tests, 350 verifier tests, all 207
  declarative suites, generated freshness, and the complete checkpoint with 65
  retained Bash checkers passed. `git diff --check` remained clean before plan
  projection.
- Result: Milestone 1 accepted. Milestone 2 is the only admitted next slice.

## 2026-08-21: Milestone 2 Acceptance

- Added one immutable `SuiteCatalog` loaded through the strict configuration
  owner and injected it into execution contexts. Registry entries, suite paths,
  dependencies, and parsed check objects now share one invocation snapshot.
- Removed the `edge_dispositions` registry-path field and its check-local TOML
  parsers. A post-load mutation test proves execution does not reopen registry
  or suite configuration, and no compatibility representation remains.
- Moved every source-index `ASSERT.*` diagnostic onto the ordinary result path.
  `EngineError` now derives invalid, unavailable, and unsupported statuses from
  typed outcomes; text and JSON formats preserve the same status contract.
- Focused evidence: 106 catalog, edge-disposition, source-index, and engine
  tests passed. Source-index mutation evidence distinguishes assertion status
  `1`, invalid status `2`, and unavailable status `3`.
- Broad evidence: 353 verifier tests, 35 neutral graph tests, all 207
  declarative suites, generated freshness, and the complete checkpoint with 65
  retained Bash checkers passed. No assertion diagnostic remains on the
  exception path and `edge_dispositions` contains no TOML parser.
- Investigation correction: the reported duplicated decorator was an
  overlapping line-range display, not a source defect; issue M2-01 records the
  false positive without changing working code.
- Result: Milestone 2 accepted. Milestone 3 is the only next slice and remains
  pending explicit admission.

## 2026-08-21: Milestone 3 Admission

- Operation: `continue`.
- Accepted base: `ecfa527669e231bdc8e826c9caa8fd9ac0a30c33`.
- Preconditions: the canonical worktree is clean; Milestone 2 is accepted; no
  Bash migration package or overlapping graph/verifier change is admitted.
- Architecture applicability: selected because two shared check kinds and one
  generic Markdown-check interface change. Performance is not selected because
  this slice makes no loading, scan, cache, or speed claim.
- Source-index decision: compose policy from `markdown_structure`, `table`,
  `relation`, `repository_paths`, `markdown_links`, `markdown_link_coverage`,
  `table_text_absence`, and `text`. Add only an explicit exact-destination mode
  to the existing link-coverage check because resolved-path coverage cannot
  preserve declared anchors.
- Acceptance-claim decision: replace the serialized claim mini-language with a
  Verification-owned decision table over claim identity, required/evidence
  mode, and complete required-set coverage.
- No-fallback decision: delete both specialized implementations, parser
  branches, private tests, and superseded fixture topology in the accepting
  slice. No wrapper or dual representation is authorized.
- Result: Milestone 3 is the only active implementation slice.

## 2026-08-21: Milestone 3 Acceptance

- Replaced `source_index_closure` with 43 generic checks composed from table,
  repository-path, relation, Markdown structure/link/coverage, text-absence,
  and text assertions. Consolidated route and prohibited-text evidence by
  concern and removed the fixed per-source fixture topology.
- Extended `markdown_link_coverage` with one required neutral identity choice:
  normalized repository path or exact source-relative Markdown destination.
  Exact-destination mode preserves anchor identity while retaining strict
  containment, target availability, and typed invalid diagnostics.
- Replaced the `kind@environment@mode` acceptance-claim grammar with a normal
  Verification-owned decision table over exact identity, required/evidence
  mode, and required-set completeness.
- Deleted both specialized check implementations, parser branches, private
  tests, and superseded fixtures. No wrapper, compatibility parser, fallback,
  or second policy representation remains.
- Mutation evidence preserves source membership, owner/disposition equality,
  heading order, route coverage, line ceilings, prohibited prose, no-fallback
  text, typed path failures, claim identity, evidence-mode, and required-set
  behavior.
- Focused evidence: 182 generic invariant tests passed; `source-index-closures`
  passed 43 checks; `acceptance-claims` passed 2 checks; affected root,
  planning-admission, template, and policy-impact suites passed.
- Broad evidence: 348 verifier tests, 35 neutral graph tests, all 207
  declarative suites, generated freshness, affected plan structure and links,
  and the complete checkpoint with 65 retained Bash checkers passed.
- Result: Milestone 3 accepted. Milestone 4 is the only next slice and remains
  pending explicit admission and measurement.

## 2026-08-21: Milestone 4 Admission

- Operation: `continue`.
- Accepted base: `de2289ad4c905c7bf9e0bba9a37da90955f4ce0a`.
- Preconditions: Milestone 3 is accepted and committed; the canonical worktree
  is clean; no Bash migration package or overlapping engine change is admitted.
- Architecture and Performance are selected: the slice changes catalog loading
  and invocation state ownership and records latency claims for five named
  verifier workflows.
- Seven post-warmup samples establish medians of 0.191 seconds for listing,
  0.198 seconds for one focused suite, 1.215 seconds for all declarative suites,
  and 1.071 seconds for generated evidence. Three complete-checkpoint samples
  establish a 128.647-second median and 128.244–131.777-second range.
- Decision: listing consumes the strict registry only; focused execution parses
  only its dependency closure; all and complete execution parse every suite.
  A check whose owned invariant inspects suite bodies outside execution closure
  explicitly requests the complete suite catalog.
- Generated scan consolidation and caching are not selected. The measured
  generated workload is approximately one second, while retained Bash dominates
  the complete checkpoint; added snapshot/invalidation machinery is unjustified.
- No-fallback decision: keep one strict registry loader, suite parser, and
  invocation catalog. Do not retain eager loading as a compatibility path.
- Result: Milestone 4 focused-loading implementation is the only active slice.

## 2026-08-21: Milestone 4 Acceptance

- Registry parsing and dependency validation remain the universal construction
  boundary. Listing now returns IDs from that authority without parsing suite
  bodies.
- Focused execution extends the invocation catalog with only the deterministic
  selected dependency closure. Selected and dependency configuration failures
  retain their typed diagnostics; unrelated malformed suite bodies no longer
  block listing or ordinary focused execution.
- Added one neutral complete-catalog marker for checks whose invariant inspects
  suite bodies outside execution closure. `edge_dispositions` declares that
  requirement explicitly and continues to validate cross-suite assertion IDs
  from the canonical parser snapshot.
- Post-change medians are 0.104 seconds for listing, 0.111 seconds for focused
  execution, 1.247 seconds for all suites, and 1.069 seconds for generated
  evidence. Every workload remains within its accepted budget; listing and
  focused execution improve by approximately 45% and 44%.
- Generated scan consolidation, persistent caching, repository snapshots, and
  Bash parallelism were rejected because measurements do not justify their
  ownership and invalidation complexity.
- Focused and broad evidence: 101 loading/catalog-aware tests, 353 verifier
  tests, 35 neutral graph tests, all 207 declarative suites, generated
  freshness, and the complete checkpoint with 65 retained Bash checkers passed.
  The post-change complete run finished in approximately 116.5 seconds, below
  the 150-second budget.
- Result: Milestone 4 accepted. Milestone 5 is the only next slice and remains
  pending explicit admission.

## 2026-08-21: Milestone 5 Pre-Resume Disposition Acceptance

- Operation: `continue` at accepted base
  `4d99b2de0b60fa134016c3b42a52bba42728e505`.
- An AST import inventory plus strict parser, registry, CLI, engine, model,
  evidence, test, and documentation review found no current post-zero-Bash
  consumer for the temporary migration implementation.
- Added one reviewed terminal table covering every migration-only module and
  exposed check kind plus the exact launchers, integration hooks, tests, suites,
  live records, generated artifacts, and documentation that depend on them.
- The existing generic migration-package suite now validates exact headers,
  required values, unique subjects, disposition domains, post-zero consumers,
  terminal trigger, and evidence owner. No custom check kind or duplicate
  lifecycle representation was added.
- The table schedules deletion of temporary migration mechanics at accepted
  zero-Bash closure. `--complete` and its README contract are replaced in place
  with Python-only semantics; no mixed-mode fallback is authorized.
- Focused mutation evidence passed 12 package/disposition contract tests and
  the two-check migration-package suite. All 357 verifier tests, 35 neutral
  graph tests, 207 declarative suites, generated freshness, three active-plan
  structure checks, terminal path/module closure, and `git diff --check`
  passed.
- The shared-contract checkpoint passed all declarative suites and all 65
  retained Bash checkers. The new report links resolve to current repository
  files; the repository has no standalone global Markdown-link script beyond
  registered bounded link checks.
- Result: the pre-resume Milestone 5 gate is accepted. Milestone 5 remains
  active until its zero-Bash terminal dispositions execute; checker migration
  may resume only from a fresh graph audit.

## 2026-08-21: Audit Follow-Up Admission And Milestone 6 Acceptance

- Operation: `continue` at accepted base
  `56f5124b1ed848fa80b8f35e46a298d4a33ed37c`.
- The external audit's eight findings remain reproducible at the current base.
  Bash retirement is paused with no package admitted.
- Current derived state is 215 suites, 56 retained Bash checkers, 373 verifier
  tests, 35 neutral graph tests, 60 temporary nodes, 401 edges, and 60
  components.
- Architecture is selected for exact routing closure and migration-candidate
  provider responsibility. It is explicitly excluded for the already accepted
  table features, parser consolidation, diagnostic-input removal, and
  performance evidence because those do not change architectural boundaries.
- Performance is selected. The recovery plan owns the five local workflow
  budgets; historical values are provisional until current seven-sample fast
  and three-sample complete measurements justify them.
- Result: Milestone 6 accepted. Milestone 7 is the only active implementation
  milestone.

## 2026-08-21: Milestone 7 Acceptance

- Added one downstream metadata-route adapter that maps reviewed decision
  outcomes to exact canonical IDs and derives transitive `Requires` closure
  through the existing neutral graph.
- Corrected routing evidence so a material migration selects Planning while a
  bounded local migration mechanic does not; missing authority or workload facts
  remain unresolved.
- Added module-local structural lifecycle declarations and one temporary AST
  adapter that compares derived migration module/check-kind candidates exactly
  with terminal dispositions. The adapter and its exposed check kind are
  themselves terminally dispositioned.
- No graph schema, edge authority, lexical route inference, copied candidate
  inventory, compatibility representation, or fallback was introduced.
- Evidence: 22 focused tests, 383 verifier tests, 35 graph tests, 215 declarative
  suites, focused routing/package suites, generated freshness, mutation tests,
  and diff checks passed.
- Result: Milestone 7 accepted. Milestone 8 is the only active implementation
  milestone.

## 2026-08-21: Milestone 8 Acceptance

- Consolidated projected-table parsing and reading without changing the
  accepted projection schema or retaining a compatibility path.
- Removed the optional numeric `EngineError` status input; diagnostic outcome
  is now the only process-status authority.
- Replaced repeated eight-source literals with a membership projection derived
  from existing corpus facts. No copied member fixture or stored count was
  introduced.
- Rejected an ambiguous one-to-many member mode after the complete 916-pair
  relation proved a stronger invariant with existing mechanics.
- Architecture is not selected: responsibility and dependency direction remain
  inside existing verifier and suite owners.
- Evidence: 126 focused tests, 386 verifier tests, 35 graph tests, all 215
  declarative suites, the 43-check source-index suite, and generated freshness
  passed.
- Result: Milestone 8 accepted. Milestone 9 current performance revalidation is
  the only next slice.
