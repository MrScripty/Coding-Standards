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
