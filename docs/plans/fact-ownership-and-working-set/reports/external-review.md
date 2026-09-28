## External review: 04-fact-ownership-working-set — recommendation: satisfied

Scope: baseline `87873de` → slice source `6fa41c3`, reviewed as an exact-diff source review (no PR; production is integrated on main). This recommendation is my review judgment only; the acceptance owner decides plan status after dispositioning findings and confirming the locked-runtime CI gate.

### Sources inspected

- [REVIEW_ASSIGNMENT.md](/tmp/coding-standards-external-review-7d563f03/REVIEW_ASSIGNMENT.md) and [SOURCE_IDENTITY.txt](/tmp/coding-standards-external-review-7d563f03/SOURCE_IDENTITY.txt) for scope and provenance
- [04 stat](/tmp/coding-standards-external-review-7d563f03/patches/04-fact-ownership-working-set.stat) and [04 diff](/tmp/coding-standards-external-review-7d563f03/patches/04-fact-ownership-working-set.diff) (full diff, all hunks)
- Slice plan, [issues.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/fact-ownership-and-working-set/issues.md), [execution-ledger.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/fact-ownership-and-working-set/execution-ledger.md), [verification.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/fact-ownership-and-working-set/reports/verification.md)
- Current production files in `source/`: [routing.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_analysis/standards_analysis/routing.py:45), [compiled_cache.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/compiled_cache.py:232), [supporting.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/supporting.py:37), [agent_navigation.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/agent_navigation.py:246), plus `context_projection.py`, `engine.py` consumer sites, `core.py` (`FactContract`), and the three new test files

### What the diff actually does

R1 moves the 8-field fact projection from deleted `agent_navigation.fact_definitions` to `RouterProjection.fact_definitions`, updating all six consumer call sites (navigation facts, two application-view sites, two engine sites, material binding). R2 adds a 10-line exact-identity recency touch of the already-retained compiled base before retaining a successful projection. I verified field-by-field that old and new projections are identical (same 8 fields/order, same empty `values`/`aliases` handling — the old code overwrote `values` unconditionally and `as_contract` always emits `aliases`, matching the new direct construction), so A1 holds by construction, not just by test.

### Findings

Per-item detail follows (prose shape used: six dimensions per finding exceed table budget).

#### F1 — Analysis independence test pins types, not freshness
Severity: minor. File: [test_routing_records.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_analysis/tests/test_routing_records.py:52). Invariant: each call returns independent containers. Impact: `expected` is itself a live returned container, so a shared-container regression would mutate `expected` alongside `changed` and still pass; the test verifies list-ness and determinism only. The property holds in code (fresh dict/list comprehensions). Disposition: accept slice; harden by deep-copying the snapshot before mutation.

#### F2 — Engine presentation-mutation binding assertion is weak
Severity: minor. File: [test_fact_material_ownership.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_fact_material_ownership.py:58). Invariant A1: navigation edits cannot redefine material. Impact: `build_materials` never reads presentation output, so `rebound == materials` passes trivially; real enforcement rests on the AST no-import check and facade-equality test. Disposition: accept slice; the invariant is otherwise covered (F-free literal binding test, dependency guard).

#### F3 — Dependency guard misses some import forms
Severity: minor (hardening). File: [test_fact_material_ownership.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_fact_material_ownership.py:95). Invariant: `supporting` depends on the Analysis owner, not navigation. Impact: only `ImportFrom` with two module names is checked; `import agent_navigation` or `from . import agent_navigation` would slip past. Disposition: accept slice; broaden to `Import` nodes and dotted names.

#### F4 — Application-purpose consumers lack direct new-test coverage
Severity: info. Files: [context_projection.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/context_projection.py:224) (`routing_facts`, `route`). Invariant: all consumers coordinated on the canonical owner. Impact: low — both sites are updated in the diff and the full-suite claim covers them; new facade tests exercise native-purpose paths only. Disposition: accept slice; rely on existing suite.

#### Verified, no finding
- R2 promotion uses exact identity (`compilation[1] is base`), only touches already-retained snapshot entries, never inserts or pins, preserves 2-entry/32 MiB bounds, and is unreachable on compile failure or disabled cache (key `None` path). Predecessor borrowing uses order-neutral `.get`, so eviction correctly prefers the predecessor. No authority/lifecycle check moved into the cache.
- `supporting.py` top-level Analysis import is cycle-free (Analysis production code imports nothing from Engine; sole `build_materials` caller passes a real `RouterProjection` from [engine.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/engine.py:1967)). `_route_question` builds a distinct question shape, not a duplicate canonical record — correctly out of scope.
- No interface/schema/MCP/storage change in the diff; `suite-inputs.json` touches only the expected paths plus the repo index.

### Test assessment (independent oracles, negative cases)

Strong: literal 8-field + `json.dumps` order oracles; raw-TOML-derived expectations with a reversed-tuple order negative; manual record rebuild + `content_digest` binding check; prompt-edit sensitivity with unrelated-material containment; zero compile/content-ID counts via profiler on original method code; per-path cold-engine equivalence; 5-config capacity matrix; `AUTHORING.NO_EFFECT` rejection with unchanged cache keys; stale-status + old-content historical-read negatives; `main` unchanged. Weak: F1/F2 as above. The deferred `AnalysisError`/float-zero observations need no reassessment — nothing in this slice touches them.

### Exact evidence gaps

- G1: read-only session — no suite was executed; pass counts and the operation-count table are report claims, not observations.
- G2: baseline failure logs (missing-method error, 1/1 extra compile) are retained separately and not in these materials; regression power for the transition miss rests on the ledger claim plus my LRU-mechanism analysis.
- G3: exact-source CI run `36347662551` was not inspected; the A6 locked-runtime gate is unverified by this review.
- G4: `suite-inputs.json` digests could not be recomputed; only path scope was verified.
- G5: the 83-material baseline-comparison instrument output is not in these materials; binding preservation was instead verified via the in-diff manual-record test and code equivalence.

Bottom line: the slice is correctly owned, behavior-preserving, minimally scoped, and mostly strongly tested; F1–F4 are test-hardening notes, not product defects. Satisfied as source review, pending the owner's A6 locked-CI confirmation.
