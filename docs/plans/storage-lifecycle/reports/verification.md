# Storage lifecycle verification

**Status: Verifying; acceptance partial.** Source baseline:
`0f24bac9b5bf773e9981bc027d6afd409607e89e` (immutable-work reuse).
Engine interface remains **44**. The bounded source implementation and local
verification are complete. Candidate locked-runtime CI and independent review
remain separate acceptance requirements.

## Implemented outcome

Only `tools/standards_snapshots/standards_snapshots/store.py` changes production
behavior. SnapshotModule, the Engine, the immutable-material cache, and all caller
signatures retain their existing responsibilities.

### Writer admission follows an observed need for purge

`purge_expired(now)` first executes an existence query for quarantined roots whose
purge deadline is at or before the supplied time. Its SQLite cursor is explicitly
closed. When there is no work, maintenance returns without acquiring the writer
slot. A positive observation is only a reason to request the existing
`BEGIN IMMEDIATE` transaction: that transaction re-selects the current eligible
rows and owns the unchanged deletion, dependent-record cascade and tombstone work.

The probe's answer is never cached. A new due root is visible on the next operation;
the deadline remains inclusive. A concurrent undelete, renewed quarantine, purge,
or additional eligible root is handled by the under-lock selection, not by stale
rows from the probe. Existing rollback behavior is retained.

Maintenance is still synchronous at the same module call sites. When purge really
is due, contention can still produce BUSY and access does not silently succeed.
Reads are not generally lock-free: an EXCLUSIVE writer, configuration transition,
actual maintenance, or other SQLite constraints can still prevent access. No WAL
switch, connection cache, maintenance daemon, scheduling interval, suppressed error,
or relaxed expiry rule was introduced.

### One full audit for current-schema admission

Every open of an existing current-schema store still verifies its application ID,
exact schema and full SQLite integrity/foreign-key state before persistent
configuration. The existing exact schema check runs after configuration. Only the
redundant second full integrity audit is removed from this no-transition path.

The private admission helper returns the source version it verified. New database
initialization keeps its final full audit and owned-file failure cleanup. Admission
from version 1 retains its original pre-configuration, guarded pre-migration,
guarded post-migration and final audits. The final destination audit also remains
when another opener finishes the migration before this opener prepares or obtains
the migration transaction. No schema or migration SQL changed.

This is a point-in-time full audit on each open, not a cache of database validity.
Selected content and aggregate reads retain their own checks. Broader audit
scheduling, indexes and long-lived connections are outside this repair; there is no
replacement with the weaker `quick_check` or a new skip-integrity option.

## Standards and source scope

The executable Router was run with explicit task facts before implementation:
25 selected modules, no unresolved facts, followed by exact policy reads. The
route and readback are preserved in delivery evidence. The scope follows the
existing storage, persistence, concurrency, contract, security, verification and
performance owners. The plan records the composition review, exact write set,
acceptance claims and remaining gates.

Normative policy, approvals, evidence provenance, production stores, dependency
locks, unrelated ZIP files and remote refs were not changed. All execution used
private container clones and disposable fixtures. Repository main and HEAD remain
at the source baseline; the delivered changes are a scoped working/index diff.

## Automated checks

| Evidence | Observed result |
| --- | --- |
| Complete Engine campaign, four file-disjoint shards | 547 passed; no failures or skips |
| Complete snapshots suite | 40 passed; includes 17 new methods |
| New cold-process MCP lifecycle tests | 2 passed; included in Engine count |
| Contracts/compiler package | 80 passed; one supported-environment check skipped |
| Other ten supporting-package suites | 485 passed; one root-inapplicable permission test skipped |
| Permission test separately rerun as unprivileged `nobody` | Passed |
| Complete structural checkpoint | 121 checks across 73 suites passed |
| Generated-contract freshness, syntax and diff checks | Passed |
| Public contract/catalog/store schema comparison | All equal to the baseline |
| Fresh-base patch reconstruction and archive checks | See `DELIVERY/reconstruction.json` |

Supporting packages cover identity, applicability, graph engine, standards graph,
snapshots, Repository Git, metadata, policy-impact, contracts, Analysis and
verifier. There are 567 supporting-package executions in total: 565 passed and two
skipped. The separate permission rerun resolves one skipped environment case; it
is not counted twice as an extra distinct suite test.

The 19 new test methods include active reads and opening a current store alongside
a real RESERVED writer; future/exact/new purge deadlines; busy purge preserving
all rows; deterministic interleavings of real second-connection lifecycle changes;
probe-error propagation; full audit count and phase; competing version-1 migration;
CHECK and foreign-key corruption before configuration; post-configuration schema
validation; and failed-new-file cleanup. Existing tests retain purge rollback,
quarantine/dependency, corruption, migration and publication/recovery coverage.

Real MCP tests launch a fresh stdio process for every request. Authoring and
application reads, batch reads, content routing and relationship-group discovery
return the same results during another connection's RESERVED write transaction
when maintenance has no work. With genuinely due purge, the existing open-time
MCP failure boundary is preserved: `isError` with generic public text, the exact
`SNAPSHOT_STORE.BUSY` diagnostic on private stderr, and no fabricated structured
success. Once the writer releases, normal access purges the expired fixture root
and its dependents while retaining the active root's shared content.

### Preliminary attempts and corrections

Three pre-implementation regressions reproduced the old unnecessary writer request,
duplicate audits and writer admission before a failing probe. They are intentionally
failing baseline evidence, not included in the final successful count.

The first expanded snapshot run had one new assertion expecting an aggregate-record
error for an aggregate root; it was corrected to the existing
`AGGREGATE.ROOT_UNAVAILABLE` outcome. An early complete cold-MCP run had one new test
assuming that store-open BUSY was a structured domain result. Its assertion now
checks the existing public/private transport boundary described above. No production
error handling was weakened or expanded to satisfy those tests.

Several early synchronous tool invocations were interrupted by execution-tool
limits before producing complete test verdicts. The complete campaign uses owned
processes whose results are captured through exit. Interrupted logs are retained
and are not counted as passing. Early verification-input refresh attempts omitted
a required request discriminator or authorizer; those correctly rejected without
effects. The final refresh uses the existing authorized Engine verification owner.

## Local performance observations

The before/after benchmark runs actual baseline and candidate code against the
same baseline-created SQLite files. Each file has a small unchanged snapshot and
0, 8, 32 or 64 MiB of unrelated synthetic aggregate payload. Each timed observation
opens a new process/connection, but measures `SnapshotModule.open` only; interpreter
startup, model work and network traffic are outside the clock.

After one untimed warm-up for each source/size, six paired samples per implementation
and size use counterbalanced order. Filesystem caches are warm. All observed rows
and selected content remain equal. Raw samples, environment and commands are in
`DELIVERY/evidence/storage-benchmarks.json` and its retained instruments.

| Unrelated aggregate payload | Baseline median open | Candidate median open |
| --- | ---: | ---: |
| 0 MiB | 1.99 ms | 1.86 ms |
| 8 MiB | 9.46 ms | 6.12 ms |
| 32 MiB | 40.15 ms | 20.66 ms |
| 64 MiB | 83.08 ms | 42.01 ms |

The 64 MiB local fixture's median decreases about 49.4%. A separate SQL trace for
open plus content observation records two full integrity/foreign-key audit pairs
and two maintenance writer admissions before, versus one audit pair and no writer
admission afterward. The improvement removes repeated work; full audits still run.

In a separate actual contention reproduction with no due root, the baseline read
waited 5.009 seconds and returned `SNAPSHOT_STORE.BUSY`; the candidate succeeded in
about 0.264 ms while the other connection retained its writer transaction. This is
a demonstrated failed-versus-successful observation, not a general latency ratio.
The production 5,000 ms SQLite busy timeout is unchanged. Small fixture timeouts in
some unit tests only bound their own deliberate contention.

These data establish the named local mechanism and workload, not p95/p99, model
latency, deployment speed, total-memory use or a result for the user's database.
The benchmark was completed before the broad parallel test campaign.

## Retained state and contract parity

An actual baseline process created a snapshot, proposal, complete Analysis and
readiness using real fixture evidence. Baseline and candidate replacement MCP
processes then reopened those exact records in the same disposable store. Policy
read, Analysis status, readiness status, repeated review and exact proposal readback
were identical. Modified fixture evidence still returned
`ANALYSIS.EVIDENCE_DIGEST_MISMATCH`. Restoring the original bytes reproduced the
original readiness and results. The fixture's accepted main never advanced.

All eight purpose/scope/output-delivery catalogs are byte-identical. Canonical
schema, interface declaration, generated projections and dependency locks are
unchanged. SQLite application ID, current v2 schema, expected v1 schema and migration
SQL hashes match the baseline. Interface 44, public operation contracts, identities,
handles, evidence validation and existing immutable-work reuse remain unchanged.

## Acceptance, environment and integration

Local environment: CPython 3.13.5, SQLite 3.46.1, Linux x86-64, jsonschema 4.26.0 and
rpds-py 2026.5.1. The supported deployment is the repository's locked Python
3.11/3.12 environment with rpds-py 2026.6.3. Provisioning a supported interpreter was
attempted but could not complete because DNS was unavailable. No dependency lock
was modified. Local results do not substitute for candidate locked-runtime CI.

Independent material review remains required. No actual Codex/model test was run;
this storage-only change has real Engine and MCP process evidence without requiring
production authoring. The plan remains Verifying until its named acceptance gates
are closed. No remote commit, push, merge or production publication was performed.

Apply the complete scoped patch using `DELIVERY/README.md`; its read-only preimage
check refuses conflicting touched files. Preserve unrelated work. Restart the MCP
process to load the implementation and reconnect normally. Catalogs and interface
are unchanged, so no launch option or data migration is needed. Preserve all stores,
proposals, snapshots, readiness and recovery handles.

## References

The existing database implementation remains the authority for transactional
behavior. SQLite's [transaction documentation](https://www.sqlite.org/lang_transaction.html)
explains read versus IMMEDIATE writer admission and statement/cursor lifetime.
Its [PRAGMA documentation](https://www.sqlite.org/pragma.html#pragma_integrity_check)
distinguishes full integrity checking from foreign-key checking and `quick_check`.
No third-party implementation code was copied into this patch.
