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
