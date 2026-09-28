## External review — 02-immutable-work-reuse: satisfied

This is a source review only. Acceptance remains with the acceptance owner. No PR review happened; production is integrated on main without a pilot PR.

Scope: baseline `e384fffdcf73e43b2f784619f4812e135f5f3393` → slice `0f24bac9b5bf773e9981bc027d6afd409607e89e`. Production candidate `7d563f032267d8d96fd45675147b9de7206a7cac`, tree `fa5722c82a2cb6cd260e5cef8001137bbd1e412b`. Inspected `source/` from acceptance-record `506656f8`, whose production `tools/` files are identical to `7d563f03` per `SOURCE_IDENTITY.txt`.

### Evidence inspected

- `SOURCE_IDENTITY.txt`, `REVIEW_ASSIGNMENT.md` (slice table, CI `36340163409`).
- `patches/02-immutable-work-reuse.stat`, full `patches/02-immutable-work-reuse.diff` (20 files, write set matches plan).
- `source/docs/plans/immutable-work-reuse/plan.md`, `issues.md`, `execution-ledger.md`, `reports/verification.md`.
- Production: [module.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/module.py:123), [model.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/model.py:116), [store.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/store.py:494), [compiled_cache.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/compiled_cache.py:127), [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:638), [operation_materials.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/operation_materials.py:27), [agent_workflow.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/agent_workflow.py:62), [decision_batch.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/decision_batch.py:28), `engine.py` `_compiled_snapshot`/`_compile`/`revision_decoding` paths.
- Tests: [test_immutable_work_reuse.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_immutable_work_reuse.py:1) (22 methods), [test_process_reuse.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_process_reuse.py:257) failure/accounting update, `test_authoring.py`/`test_nested_materials.py` adapter forwarding.

### Invariants verified in source

- Identity reuse happens only after `maintain` + `store.load_content` lifecycle and per-file length/sha checks, and the reused/calculated ID is still compared to the stored ID on every call. Wrong stored IDs, rewritten bytes with updated digests, quarantine/purge, and store replacement cannot become hits.
- Cache keys are exact `CapturedContent` equality (source label + sorted files); calculator/compiler reuse additionally requires `is` identity on plain functions. Closures, bound methods, and callables go cold. Hash-collision, disabled/oversized/evicted/failed/closed cases recompute without semantic change.
- Identity and compilation share one LRU entry and byte budget; replacement subtracts prior accounting; failed computations are never retained while an independent successful identity may survive a compilation failure.
- `RevisionDecoding` admits only via canonical `_revision_from_record`, equality covers the full frozen record, and every `read_revision`/`current_revision` still reloads aggregate + root and validates membership. Operation exit clears the slot on success and failure. Publication/recovery/readiness paths stay cold.

Tests have independent oracles, not just pass counts: exact `SNAPSHOT.CONTENT_ID_MISMATCH` / `AUTHORING.INVALID_STORED_REVISION` codes, load/codec/decode call counts proving reads still execute while proofs decode once, cross-calculator value differences, warm-vs-cold and restart response equality.

### Findings

All informational; none blocks correctness.

1. Low — missing `aggregate_id` negative variant. [test_immutable_work_reuse.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_immutable_work_reuse.py:246): covers kind/payload/snapshots/children but not `aggregate_id`. Invariant: exact aggregate equality including identity. Impact: coverage gap only; code is correct via frozen-dataclass equality plus `revision.aggregate() != record` in [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:1275). Disposition: non-blocker; owner may add variant.
2. Low — generic oracle in one lifecycle negative. [test_immutable_work_reuse.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_immutable_work_reuse.py:270): `test_quarantine_after_decode_still_denies_read` asserts `SnapshotError` without exact code. Invariant: lifecycle denial after decode. Impact: weaker diagnosis; store tests cover exact quarantine codes elsewhere. Disposition: non-blocker.
3. Info — `current_revision` corrupt-head diagnostic delta. [authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/authoring.py:720): new path calls `read_revision(root.head_id)`, so a malformed stored `head_id` now raises `AUTHORING.INVALID_REVISION_ID` before store lookup, where old `_summary_from_root` path would surface store `AGGREGATE.UNAVAILABLE`. Invariant: preserved validation/error contracts. Impact: corrupt-store diagnostics only; no false success or stale acceptance; both root observations/validations retained. Disposition: non-blocker; disclose for owner error-taxonomy confirmation.
4. Info — resume path stays cold. [agent_workflow.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/agent_workflow.py:230): `advance` resume uses cold `current_revision` even with materials. Invariant: operation reuse propagation. Impact: extra decode, safe direction, no stale leak. Disposition: non-blocker.

### Exact evidence gaps

- Read-only: no test execution, no patch-reconstruction, no hash/mode verification.
- Locked CI run `36340163409` logs not in workspace; U7 not verified here.
- Delivery-only evidence not in workspace (`DELIVERY/evidence/final-artifact-checks.json`, `DELIVERY/reconstruction.json`, Router 23-module readback, raw timing samples/response hashes, baseline-vs-candidate replacement-process logs; `DELIVERY` search empty). In-repo tests prove warm/cold and restart equivalence, not baseline equality; U4/U5 baseline claims depend on that external evidence.
- Baseline tree `e384...` not checked out; comparison is via the exact diff text only.
- `source/` includes post-slice extensions (e.g. `retain_verified`, identity key-preservation); slice behavior was judged from the diff plus current files.

Recommendation for this slice: **satisfied**. Plan acceptance (including pending locked-runtime U7 and final disposition of the above notes) is the acceptance owner's decision, not this review's.

