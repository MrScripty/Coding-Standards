## External review: 03-storage-lifecycle — recommendation: satisfied

This is an external source review of one slice only, not a PR review. Production was integrated on main without a pilot PR.

- Baseline → source: `0f24bac9b5bf773e9981bc027d6afd409607e89e` → `87873de5e1405590209dad389f7010a6b61f0bbe`
- Final production checked: `7d563f032267d8d96fd45675147b9de7206a7cac`, tree `fa5722c82a2cb6cd260e5cef8001137bbd1e412b`
- Archive read: `source/` from `506656f8`, stated to have identical production `tools/` files to `7d563f03`

My recommendation is satisfied on the slice material inspected. The acceptance owner retains the acceptance decision; the plan is correctly left Verifying/partial until the owner closes L7 (supported locked-runtime CI) and dispositions the minor gaps below.

### Source and evidence inspected

- [SOURCE_IDENTITY.txt](/tmp/coding-standards-external-review-7d563f03/SOURCE_IDENTITY.txt)
- [REVIEW_ASSIGNMENT.md](/tmp/coding-standards-external-review-7d563f03/REVIEW_ASSIGNMENT.md)
- [03-storage-lifecycle.stat](/tmp/coding-standards-external-review-7d563f03/patches/03-storage-lifecycle.stat) and [03-storage-lifecycle.diff](/tmp/coding-standards-external-review-7d563f03/patches/03-storage-lifecycle.diff) — full exact diff read
- [plan.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/storage-lifecycle/plan.md), [issues.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/storage-lifecycle/issues.md), [execution-ledger.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/storage-lifecycle/execution-ledger.md), [verification.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/storage-lifecycle/reports/verification.md)
- Current production: [store.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/store.py) admission at lines 295-307, `purge_expired` probe at 560-580, `_verify_existing_authority` at 1050-1075, `_verify_integrity` at 1147-1155, `_configure` at 989-1021, `_migrate_version_one` at 1077-1104, `_cleanup_failed_open` at 321-339; [module.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/module.py) synchronous `maintain()` at 216-217 with unchanged call sites
- Slice tests in final tree: [test_storage_lifecycle.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/tests/test_storage_lifecycle.py) (17 methods) and [test_storage_lifecycle_transport.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/tests/test_storage_lifecycle_transport.py) (2 methods); v1 fixture helpers in `source/tools/standards_snapshots/tests/test_store.py`

Production delta in the exact diff is confined to one owner file plus docs/tests/README/generated digests. I verified the current-tree hunks match the diff post-image: probe + `closing` import, `admitted_version` branch, private helper returning the verified version. No schema, migration SQL, lock, identity, or public contract change is in the diff.

### Why the core invariants hold

- Storage authority: `SQLiteSnapshotStore` remains the sole decider. Probe uses the same caller time and inclusive `purge_deadline <= ?` as the guarded re-select; cursor is closed before `BEGIN IMMEDIATE`; deletion uses only the under-guard ordered select. No new public type, flag, cache, or daemon.
- Race handling: deterministic second-connection interleavings cover undelete, re-quarantine, competing purge, and newly-due roots, each asserting the interleaving ran (`proxy.calls == 1`) plus final lifecycle/tombstone state. No sleeps decide races.
- Corruption/recovery/cleanup: current-store corruption is rejected before persistent configuration with exact `FOREIGN_KEY_FAILURE`/`INTEGRITY_FAILURE` codes, file preserved, and journal left as `wal` proving `_configure` did not persist; v1 and concurrently-migrated paths retain the final destination audit and catch injected FK corruption; post-configuration exact schema check is retained; failed new init removes only the owned file and closes the connection.
- Retained history: due-work BUSY preserves full `counts()` and leaves no transaction; post-recovery purge checks three distinct expired/unavailable codes, `child_index == 0`, tombstone counts, and shared-content retention (`content_sets == 1`).

Negative oracles are meaningful and largely independent: SQL-trace absence/count of `BEGIN IMMEDIATE`, exact typed failure codes, exact admission-event sequences with `(event, user_version, in_transaction)`, sorted v1 row preservation, and MCP public/private failure boundary (`isError`, no `structuredContent`, `SNAPSHOT_STORE.BUSY` on stderr).

### Findings

No blocker findings.

- Finding 1, severity minor, not blocking. File [store.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/store.py:566): probe read under an `EXCLUSIVE` holder has no direct test. Invariant L1/D3. Impact: probe `BUSY` mapping via `_adapt` is unproven in the documented still-blocking case; writer-`BUSY` and probe-`AUTH` paths are proven. Disposition: owner may accept as-is; a later slice could add an exclusive-lock probe negative without changing this slice.
- Finding 2, severity minor, residual risk, not blocking. File [store.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/store.py:295): no test injects integrity corruption between the retained pre-configuration audit and first use on the current-store path. Invariant L3/D2. Impact: corruption committed in that narrow configure window would surface on next open or per-record checks rather than at this open; both old and new admission are point-in-time, but the removed second audit enlarged that window. Disposition: accept as the explicit once-per-open policy and deferred audit-scheduling work per L-D2; no fix in this slice.
- Finding 3, severity minor, oracle limitation, not blocking. File [test_storage_lifecycle_transport.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/tests/test_storage_lifecycle_transport.py:50): the no-work cold-read test builds expected results from the same transport before contention, so it proves non-interference rather than absolute correctness. Invariants L1/L4. Impact: low, because absolute oracles exist in store unit tests, the fixture `expected` value, and the second transport recovery check. Disposition: accept; no test change required.
- Finding 4, severity info. Probe adds a per-operation existence scan with no index; benchmarks in the report vary payload bytes, not quarantined/active root count. Impact: unmeasured scaling on many-root stores. Disposition: explicitly out of scope per L-D2; no action in this slice.

### Exact evidence gaps

- Locked-runtime CI for this slice (assignment names run `36342508184`) was not inspected; local evidence used CPython 3.13.5/SQLite 3.46.1 versus locked 3.11/3.12 per L-E1. L7 therefore remains an owner gate.
- `DELIVERY/` reconstruction, benchmark instruments, raw samples, SQL-trace artifacts, manifests, and rerun logs cited in verification.md are not in this review bundle; reported medians and trace counts were not independently re-verified.
- No tests were executed in this read-only review; pass counts are taken from the verification report, not observed.
- Retained Engine workflow parity beyond snapshots (Analysis/readiness/evidence-digest reopen checks) has no new oracle in this slice's tests; it rests on existing suites plus the reported MCP reopen checks.
- The two untested windows above (exclusive-lock probe read; inter-audit concurrent corruption on current stores) have no oracle either way.

Distinction: my satisfied recommendation covers the slice's source logic, authority/cleanup/race/retained-history handling, and test-oracle quality against the exact diff. Final plan acceptance is the owner's decision after closing L7 and dispositioning these minor gaps.

