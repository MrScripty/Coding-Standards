# Typed routing-edit pilot — external source review

## Scope reviewed

- Slice: typed routing-edit pilot only.
- Baseline `cbf9cdd2d7627d2c45f0001486a8872ab6b5206d` → production commit `7d563f032267d8d96fd45675147b9de7206a7cac`, tree `fa5722c82a2cb6cd260e5cef8001137bbd1e412b`.
- Integrated on `main` without a pilot PR; this is a read-only source review, not a retrospective PR review.

## Source and evidence inspected

- [SOURCE_IDENTITY.txt](/tmp/coding-standards-external-review-7d563f03/SOURCE_IDENTITY.txt), [REVIEW_ASSIGNMENT.md](/tmp/coding-standards-external-review-7d563f03/REVIEW_ASSIGNMENT.md)
- [06-typed-routing-edits.diff](/tmp/coding-standards-external-review-7d563f03/patches/06-typed-routing-edits.diff) (full baseline→slice diff; baseline routing logic read from removed lines)
- [plan.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/typed-routing-edits/plan.md), [issues.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/typed-routing-edits/issues.md), [execution-ledger.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/typed-routing-edits/execution-ledger.md), [verification.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/typed-routing-edits/reports/verification.md)
- Production: [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py) (full, 157 lines), [logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py) (parse, change-set, compile, analysis, `_edit_routing`, rendering)
- Direct consumers/boundaries: [consumer_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/consumer_authoring.py), [compiled_cache.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/compiled_cache.py), [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py) (revision identity, stored-revision decode), [encoding.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_identity/standards_identity/encoding.py), [engine.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/engine.py) (consumer/audit scans)
- Committed tests: [test_typed_routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_typed_routing_edits.py) (11 methods), [test_typed_routing_projection.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_typed_routing_projection.py) (6), [test_typed_routing_workflow.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_typed_routing_workflow.py) (3); plus `test_logical_authoring.py` fixtures used by projection tests.

I did not edit files, run commands, or verify CI/DELIVERY logs.

## Assessment summary

Source supports the pilot's core claims: authored declarations stay distinct from compiled facts; nested values are detached and returned contracts are fresh; map order is canonical-sorted with array order preserved; bool/int/null are type-distinguished; canonical serialization, revision/aggregate identities, TOML/Markdown rendering, validation timing, atomic batching, incremental/full equivalence, and proportionality are preserved. No source blocker found. Findings below are low/informational.

## Findings

### F1 — Low: `Put*` edits have value equality but identity-based hash

- Evidence: [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:45) (`RoutingFactDeclaration`, `eq=False`, no `__hash__`, custom `__eq__` at 62-66); [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:77) (same for rules, 87-91); [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:98) (`PutRoutingFact`/`PutRoutingRule` use generated frozen `__hash__` over `fact`/`rule`, whose hash is object identity).
- Invariant (A1): immutable explicit variants; Python requires equal objects to hash equally. Baseline `StructuredEdit` hashed by value (payload string).
- Impact: latent only. No production consumer hashes edits: facets are string tuples ([logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:879)), sorting/continuation/identities use `_canonical_json(as_contract())` or identity-codec bytes ([logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:876), [logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:1005), [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:188)), cache keys use identity bytes not edit hash ([compiled_cache.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/compiled_cache.py:195)). Equal `Put*` values in different objects would compare equal but hash differently if ever placed in a set/dict.
- Disposition: advisory, not a blocker. Owner may set `__hash__ = None` on the two declaration classes and the two `Put*` classes (making them explicitly unhashable, since `MappingProxy` is unhashable anyway) or document that edits must not be hashed. No persisted-contract change.

### F2 — Low (concur with deferred Q5): float `-0.0` vs `0.0` conflated only by `__eq__`

- Evidence: [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:34) (`_same_value` uses `type` check then `==`, so `-0.0 == 0.0`); identities/hashes use `_canonical_json` ([logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:133)) and the identity codec, which rejects floats ([encoding.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_identity/standards_identity/encoding.py:189)) via [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:1305).
- Invariant (A1/A2): scalar distinctions preserved; canonical identities/hashes match baseline.
- Impact: none demonstrated in valid workflows. Any float in a routing edit fails revision-identity construction identically in baseline and candidate, so no persisted revision can contain floats. `_same_value` affects only direct `==` comparisons, not change-set sorting, `_projection_order`, revision IDs, aggregate hashes, signatures, or projected files, which all flow through `as_contract()` + canonical/identity encoders that preserve float spelling or reject floats.
- Disposition: keep deferred as recorded in Q5. Reassessed against source; no contract violation or blocker. Do not widen the pilot for this.

### F3 — Informational (concur with deferred note): broad `AnalysisError` assertions in new projection tests

- Evidence: [test_typed_routing_projection.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_typed_routing_projection.py:77) (`test_shape_normalization...`, `test_fact_semantic_revision...` second half, `test_duplicate_targets...` second half assert `AnalysisError` without code/message).
- Invariant (A3): failure stage/owner preserved for unknown refs, invalid types, used-fact removal.
- Impact: source shows stage is preserved regardless of assertion breadth: parse performs no semantic compile ([logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:374), stdlib-only [routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:9)); semantic failures arise from the same `_edit_routing` checks plus the same final `self._compile_authorities(source)` call ([logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:1077)) over identical projected files. Parse-vs-projection split is directly pinned by `compile_fact_schema`-patched tests.
- Disposition: keep deferred; the separate 23-case differential is owner-verified delivery evidence, not re-verified here. No source-level stage change found.

### F4 — Informational: exotic inputs and two unconverted scans have no behavioral effect

- Evidence: `_freeze` preserves map keys as-is ([routing_edits.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/routing_edits.py:15)) while a JSON round trip would coerce non-string keys; `engine.py` still calls `edit.as_contract()["kind"]` for consumer/audit scans ([engine.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/engine.py:904), [engine.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/engine.py:1681)).
- Invariant (A2/A5): serialized payloads match; inner JSON decodes disappear.
- Impact: none via real workflows. MCP JSON inputs always have string keys, so the key-coercion divergence is unreachable except via direct private `_edit` calls. The two engine scans construct fresh dicts but invoke no `json.loads` (routing has no `payload` anymore; only `StructuredEdit` retains `json.loads(self.payload)` at [logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:323)).
- Disposition: note only; no repair required. Optionally validate exact-string keys in `_freeze` and use `_edit_kind` in the two scans.

## Evidence gaps

- Inspected `source/` is extracted from docs commit `506656f8`, not directly from production `7d563f03`. Production-file equivalence rests on the exact patch plus the reconciliation claim that the later commit touched only records/manifest. I could not run git to confirm zero production drift.
- No CI logs (run `36358571883`), DELIVERY logs, `test-summary.json`, 23-case diagnostic JSONs, or 8-process replacement transcripts are in this packet. Counts, byte-identical differentials, and cold-baseline-history observations are therefore taken as owner/CI evidence, not independently re-verified. Committed tests plus source equivalence for the stored contract format (canonical dicts decoded via `StandardsChangeSet.from_mapping` in [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:1249)) make the no-migration readback credible, but the baseline-produced-history observation itself remains outside this packet.
- No baseline checkout; baseline behavior was read from the diff's removed lines, which fully show the old routing parse/store/project path.

## Recommendation for this slice's external-review claim

**Satisfied** — source review finds no blocker to A1–A5 or proportionality; the two deferred observations remain appropriately deferred on source evidence, and remaining items are low/informational advisories above.

This is my review recommendation only. Acceptance remains the acceptance owner's decision after disposing F1–F4, confirming the `7d563f03`↔`506656f8` production-file equivalence and exact-source CI run `36358571883`, and closing Q2 per the plan.

