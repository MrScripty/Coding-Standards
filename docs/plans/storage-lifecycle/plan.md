# Plan: Storage lifecycle admission without redundant work

**Plan status:** Accepted
**Acceptance status:** satisfied
**Current phase:** Accepted; exact-source CI and independent material review dispositioned.
**Next slice:** none — this bounded slice is Accepted.
**Canonical plan / operation:** `docs/plans/storage-lifecycle/plan.md` / `verify`; source implementation admitted under the user's storage-lifecycle instruction.
**Execution ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)
**Report:** [reports/verification.md](reports/verification.md)

## Acceptance-owner closure — 2026-09-27

**Accepted.** L1–L7 are satisfied for exact source `87873de5e1405590209dad389f7010a6b61f0bbe`. [Exact-source Python 3.12 CI](https://github.com/MrScripty/Coding-Standards/actions/runs/36342508184) passed under the unchanged lock and current complete workflow; [independent external review](reports/external-review.md) recommends this slice as satisfied. The acceptance owner dispositioned its non-blocking observations in the [six-slice decision](../typed-routing-edits/reports/acceptance-dispositions.md). The earlier local-only or pending statements below document the implementation-stage state; this decision supersedes those status statements. No further implementation slice is admitted here.

## Objective and scope

Implement audit F02/F03 against `0f24bac9b5bf773e9981bc027d6afd409607e89e` (interface 44), preserving the integrated boundary repairs and immutable-work reuse. An observation of active data should not acquire a writer transaction solely to discover that no purge is due. Reopening an already-current store should authenticate its authority with one full integrity/foreign-key audit, not repeat that audit without a schema transition.

Keep SQLiteSnapshotStore as the only owner of these decisions. Scope is current-store admission, opportunistic synchronous maintenance, their real consumers/tests and documentation. Keep expiry time, quarantine duration, transactional cascade/tombstones, rollback, migration, typed failures and per-record integrity behavior. No public schema, interface edition, store schema, lock, identity, evidence or publication change is admitted.

Do not add a maintenance daemon, cached no-work decision, long-lived connection, skip-integrity flag, weaker check, index, WAL switch, alternate store or catch-and-continue path. Broader integrity-audit scheduling and index design remain separate audit work requiring their own evidence. This slice removes the demonstrated redundant work without changing the once-per-open full audit policy.

## Standards and authority

Apply Core, Router, Implementation, Verification, Development Proportionality, Planning, Persistence, Concurrency, Contracts/Evolution, Security, Resilience, Architecture, Performance, Documentation and the selected required closure. The executable Router and exact policy readback were run before source editing: 25 selected modules, no unresolved conditions. Records are included in delivery evidence. Normative policies, approvals, unrelated ZIPs and production stores remain outside this task.

SQLite's documented transaction owner remains authoritative: a read probe may run while a RESERVED writer exists, but `BEGIN IMMEDIATE` requires the writer slot. Close the probe cursor before requesting that slot. Re-read due rows inside the existing write transaction; the probe itself grants no deletion authority. References: https://www.sqlite.org/lang_transaction.html and https://www.sqlite.org/pragma.html#pragma_integrity_check.

## Binding decisions and owners

- **D1 / Snapshots store:** use one short-lived existence query for due quarantine rows. Return only when the query observes no work. If it observes work, acquire the unchanged writer guard and select the authoritative due set again. Selection uses the same caller-observed time and inclusive deadline as before.
- **D2 / Snapshots store:** the verified pre-configuration source schema version determines integrity-proof lifetime. Current stores keep the complete pre-configuration audit and post-configuration exact schema check, but omit the second full audit. New initialization keeps its final audit. Admission from v1 keeps all existing migration audits and the final audit, including a migration completed by another opener. No v1 migration code is weakened.
- **D3 / Module and Engine:** keep the synchronous maintenance call sites. Actual due work may still return BUSY; no failure is converted into successful access or stale cached authority. Readers may still block on EXCLUSIVE locks or actual maintenance. There is no promise of lock-free SQLite reads.
- **D4 / Contract and deployment:** retain interface 44, all published operations/digests and SQLite v2; no migration/reset/configuration flag is needed. Restart loads implementation changes only.

## Simplicity and ownership review

**Applicability:** applicable; timing of storage admission and writer acquisition changes.

1. Independent concerns: the module supplies time and lifecycle triggers; the store owns SQLite admission and purge; callers request observations or mutations. Pure identity/revision reuse remains elsewhere.
2. State/identity/value/time: an existence observation is short-lived data, not a retained proof. Deletion eligibility is re-evaluated under the writer guard at the supplied time. Source-version admission is scoped to one open, not a store cache or shared epoch.
3. Caller knowledge: no caller signature or lifecycle choice changes. The store alone decides whether writer admission and a repeated integrity audit are needed.
4. Change paths: expiry-policy changes stay with Snapshots; migrations retain their guarded checks; request schemas, agent tools and reusable material have no forced changes.
5. Stable interfaces: only a private store helper returns its authenticated schema version. No new public type, mode, persisted flag or test-specific production callback is introduced.
6. Independent verification: real SQLite connections and subprocesses test locking; migration/corruption fixtures test admission; Engine/MCP tests cover actual consumer behavior. Private trace instrumentation observes rather than substitutes for SQLite.
7. Deletion result: remove the unconditional no-work writer acquisition and redundant current-store audit. The short-lived probe is necessary to decide whether the writer is needed. Removing it would recreate the measured contention; retain the existing guarded selection.
8. Inherent complexity: atomic purge, source/destination validation and rejection cleanup remain. The change adds no permanent mechanism outside the existing owner. Performance evidence is distinct from this caller-knowledge/deletion assessment.

## Exact initial write set

- `tools/standards_snapshots/standards_snapshots/store.py`
- `tools/standards_snapshots/tests/test_storage_lifecycle.py`
- `tools/standards_engine/tests/test_storage_lifecycle_transport.py`
- `tools/standards_snapshots/README.md`
- `docs/plans/README.md` and this directory
- Owner-generated `evaluation/standards-effectiveness/generated/suite-inputs.json`

Additional directly affected tests may be admitted in the ledger without widening the domain scope. Module, Engine, immutable caches, generated contracts, store schema and dependencies are read-only unless evidence requires re-planning.

## S1 — Implementation and verification

**Status:** Implemented. **Goal:** both storage optimizations preserve authority and cleanup. **Write set:** as above.

1. Reproduce the unnecessary writer request and duplicate full audit; add regression tests before production edits.
2. Implement D1/D2 together in the existing store. Keep all call-site and migration contracts.
3. Test active observations during a competing writer, actual-due BUSY, inclusive deadlines, no-work followed by new work, and concurrent undelete/requarantine/purge between probe and guarded selection. Verify rollback and dependent heads/children/tombstones through reopened stores.
4. Count and locate full integrity checks on new/current/migrated/concurrently migrated stores. Corrupt rows, foreign keys or schemas must still fail at the required phase and preserve existing files. Failed new initialization owns cleanup of only its new file.
5. Run affected package suites, real cold MCP/storage process tests, fresh contract/catalog comparison and structural checks. Measure same-source open costs at recorded payload scales and preserve raw baseline/candidate samples.
6. Package a base-checked patch and complete changed files; retain reports, manifests and all failed/rerun evidence. Required locked-runtime CI and independent review remain separate if unavailable.

**Gate:** claims L1–L7 below. Once source/local evidence is complete, transition to Verifying and name the one remaining integration slice. This slice does not publish standards or modify the operator's configuration.

## S2 — Integration qualification

**Status:** Planned. **Goal:** qualify the same material candidate in the supported locked environment and obtain independent review. **Write set:** this plan's acceptance records, with any material repair subject to the S1 scope and re-plan rules. Run the existing complete locked CI, disposition the independent storage/corruption/race review, and record source/package identity. Only then mark the plan Accepted, acceptance satisfied, and next slice none. No production standards publication or model-authored change is required by this storage-only slice.

## Acceptance and evidence

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | With no due root, existing and new-process active observations succeed alongside a RESERVED writer; SQL trace shows no maintenance write transaction | system | representative | automated | satisfied (local) | [Verification](reports/verification.md) |
| L2 | Actual due work retains BUSY/rollback behavior; eligible rows are selected under the guard, including competing lifecycle transitions; expiry/dependencies/shared content/tombstones survive reopening correctly | integration | representative | automated | satisfied (local) | [Verification](reports/verification.md) |
| L3 | Current admission runs one full audit before configuration; creation and v1/concurrent migration keep required full checks; corruption/schema/profile failures are not bypassed | integration | representative | automated | satisfied (local) | [Verification](reports/verification.md) |
| L4 | Actual MCP reads/status and retained baseline workflow outcomes, evidence failures and publication targets preserve meaning | system | representative | automated | satisfied (local) | [Verification](reports/verification.md) |
| L5 | Recorded paired open measurements show reduced duplicate scan work with unchanged successful results and no weaker integrity algorithm | focused | required-real (named local benchmark environment) | automated | satisfied (local) | [Verification](reports/verification.md) |
| L6 | Public contracts/catalogs/schema are unchanged; generated inputs are fresh; complete affected tests/checkpoint and fresh-base reconstruction pass | release-artifact | not-applicable | automated | satisfied (local) | [Verification](reports/verification.md) |
| L7 | Supported locked-runtime CI and independent material review of this candidate pass before acceptance | integration | representative | either | satisfied | [Acceptance decision](../typed-routing-edits/reports/acceptance-dispositions.md) |

Deciding oracles are real SQLite lock/content observations, the existing full PRAGMA integrity/foreign-key checks, exact metadata/row/readback comparisons, existing public schemas, and file/hash reconstruction. Tests may inject a lifecycle change at a deterministic scheduling point through test-only instrumentation; they must perform it on a separate real SQLite connection and preserve error evidence. No sleeps decide a race and no timing threshold substitutes for behavior. Local benchmarks prove only their recorded workload, not model latency or deployment performance.

## Blockers and re-plan conditions

No implementation blocker. The original implementation container lacked a supported interpreter; the later exact-source Python 3.12 locked CI and independent external review satisfied the acceptance gate.

Re-plan for any change to expiry meaning, data authority, supported schema/identity, corruption guarantees, cross-operation connection lifetime, or evidence showing that the probe weakens observation. Fix ordinary test/manifest errors inside S1. Additional scale/index/audit scheduling changes require a separately recorded decision.

The private implementation clone and source baseline described the delivery stage. The exact source slice is integrated on `main` at the candidate linked above; no operator store, configuration or standards content was changed.

**Final acceptance:** satisfied; L1–L6 retain their local evidence and L7 is satisfied by exact-source locked CI and independent review. **Deferred:** broader audit scheduling/indexing, cache working-set and domain/API redesign. Accept only with every required claim satisfied; final next slice then becomes none.
