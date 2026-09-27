# Immutable work reuse

**Plan status:** Verifying
**Acceptance status:** partial
**Canonical plan:** `docs/plans/immutable-work-reuse/plan.md`
**Operation:** verify; user-authorized implementation of audit F01/F08
**Current phase:** U1 — Integration qualification; source and local checks complete
**Next slice:** U1 — Qualify the integrated candidate in locked CI and independent review
**Base:** `e384fffdcf73e43b2f784619f4812e135f5f3393` (interface 44)
**Ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)
**Evidence:** [reports/verification.md](reports/verification.md)

## Objective, admission and scope

Reduce complete warm read and workflow-status costs by reusing proofs about exact
immutable material. Preserve the fresh observations which decide existence, lifecycle,
proposal membership/head, current evidence, permission and publication. Implement the
audited F01 and F08 mechanisms, not a cache of live authority or prior responses.

The latest integrated boundary repairs are the baseline. Core and the executable Router
selected 23 applicable modules with zero unresolved facts; exact route/readback is in
delivery evidence. Guidance covers implementation, verification, proportionality,
planning, library, IPC/persistence, architecture/replay, contracts/evolution/schema,
security, diagnostics, performance, code ownership, build, documentation and commit.
This is code maintenance; normative policies, approvals, provenance and production
standards remain unchanged. Performance investigation already demonstrated the costs;
implement the bounded reversible paths and measure them with the same workload.

## Binding decisions and owners

1. **Snapshot owns identity semantics and validation.** Its existing identity-v2 codec
   and content ID domain are unchanged. `load_content` always performs maintenance and
   reloads actual stored bytes with existing file checks. An explicit trusted
   `ContentIdentityReuse` contract may reuse the supplied codec only for exactly equal
   immutable captures. The Snapshot owner always compares the computed/reused proof with
   the currently loaded stored ID. Standalone loading remains cold by default.
2. **The existing process cache owns retention.** Extend `CompiledSnapshotCache` with
   one snapshot-material entry containing optional identity and compiled products. They
   share the capture, two-entry default LRU, 32 MiB accounted-data default and shutdown;
   no parallel identity cache is introduced. Check exact calculator/compiler identity,
   not merely a digest, timestamp, path or source label. Closure functions, bound
   methods and callable objects calculate cold; eligible plain functions still require
   the trusted pure-codec/compiler contract. Account entry replacements and oversized products through the existing owner.
   Successful identity proof may survive a separate compilation failure; a failed
   computation is never retained. Live observations are never cache entries.
3. **Authoring owns stored-revision decoding.** A one-record `RevisionDecoding` value
   admits entries only through the existing canonical decoder and exact aggregate
   equality, including kind, payload, identity and snapshot/child membership. Its
   normalized revision is deeply immutable; exported contract maps remain fresh.
4. **ProposalMaterials owns operation lifetime.** It composes and clears that decoder
   with the existing base/projection material. Binding, evaluation and head observation
   use it explicitly. Each revision access still reloads the actual aggregate and root
   and checks membership. Remove current_revision's summary-only duplicate decode while
   retaining both root observations/validations. Publication/recovery and callers
   without operation material retain their cold independent paths.
5. **Contracts and state are stable.** No public operation/schema/interface edition,
   identity codec, Analysis version, handle format, SQLite schema, default/flag, or
   dependency changes. Existing native-only input, discovery, output choices, field
   errors, atomic decisions, evidence checks and exact policy content remain.

F15 prepared-interface tables, F02/F03 storage maintenance/admission, F09 working-set
policy, F10/F14 ownership/domain pilots and F16 capture seeding are independently scoped
follow-ups. They are not required for this exact-material implementation.

## Simplicity and ownership review

**Applicability:** applicable; process and operation reuse meet durable-read boundaries.

1. Independent dimensions: Snapshot computes/verifies identity; cache retains pure
   products for installed code/root/purpose; Authoring decodes records; operation
   material owns transient reuse; the store and authorizer still own live observations.
2. Identity values are immutable and verified on every read; clocks, root heads,
   revocation and existence are not inferred from them. A source label is part of exact
   capture equality, not a shortcut for file bytes. Public/persisted version roles stay
   separate from the process's implementation lifetime.
3. Callers carry the existing cache or operation material explicitly. Snapshot receives
   an owned one-method reuse contract rather than depending on Engine internals. There
   are no hidden globals, dynamic cache registration, retries or client mode choices.
4. Identity-codec changes remain Snapshot/Identity-owned; compile changes stay with the
   compiler. Both are checked against their retained implementation. A revision grammar
   change affects Authoring; lifecycle/authorization changes remain with existing owners.
5. Stable inputs are full captures and aggregate records. Stored claimed IDs never
   replace those inputs. Fresh root checks remain outside cached decode products.
6. Cold paths remain independently executable. Disabled retention, eviction, corrupted
   bytes/IDs, root changes, altered evidence and replacement processes have direct tests.
7. The only new retained record is a product inside the existing cache; the small
   Snapshot reuse protocol removes an otherwise inverted package dependency. The
   operation decoder contains a single bounded record and disappears at operation exit.
   Deleting those helpers would restore demonstrated repeated work or distribute the
   same proof logic into callers. No new service, registry, persistent cache or validator.
8. The cumulative design has one process LRU and one operation-owned decode slot.
   Inherent current-state and corruption checks remain. Memory accounting excludes
   existing active-operation/transient interpreter allocations and makes no RSS claim.

## Write set and consumer population

- `tools/standards_snapshots/standards_snapshots/{module,__init__}.py`; package README.
- `tools/standards_engine/standards_engine/{compiled_cache,authoring,operation_materials,agent_workflow,decision_batch,engine}.py`.
- `tools/standards_engine/tests/test_immutable_work_reuse.py`, and directly affected
  `test_process_reuse.py`, `test_authoring.py`, `test_nested_materials.py` assertions/fixture signatures.
- Engine README/PURPOSE-SEPARATION only for this behavior and current operator context.
- This plan directory, `docs/plans/README.md`, and the owner-regenerated
  `evaluation/standards-effectiveness/generated/suite-inputs.json`.

The systemic invariant population is full capture identity through Snapshot/cache,
canonical stored-revision reconstruction and its focused operation consumers.
Stop source expansion at these owners unless evidence reveals another reachable
violation. Additional affected tests/callers inside this population are logged;
new authority, persisted semantics or replacement mechanisms require re-planning.

## Milestone U1 — Complete exact-material reuse

**Status:** Verifying. **Goal:** eliminate redundant proof/decoding work while observing
all current state. **Write set:** above. **Preserves:** all public/domain/retained-state
semantics and cold behavior. **Gate:** local evidence for U1–U6 below; supported-runtime qualification and
independent review remain required for acceptance.

- Capture clean source and baseline request/profile evidence in disposable material.
- Implement the two explicit lifetimes and focused regression cases together.
- Review caller propagation and state/proof separation; regenerate tracked inputs.
- Run complete affected packages, selected real transport/lifecycle/recovery tests,
  existing structural checkpoint and same-fixture paired request measurements.
- Reconstruct the patch on its exact baseline and record hashes, modes and unchanged
  schemas/catalogs. Restart installed processes after integration, preserving stores.

## Objective acceptance and oracles

| ID | Criterion | Kind | Environment | Mode | Status |
| --- | --- | --- | --- | --- | --- |
| U1 | Same capture/codec proof reused; all durable reads still execute; wrong stored IDs, altered bytes, hash collisions, quarantine/purge and replaced stores never become false hits | integration | representative | automated | pending |
| U2 | Identity and compilation share original LRU/byte bounds; replacement, disabled/oversized retention, failure, implementation changes and close preserve outputs | focused | representative | automated | pending |
| U3 | Analysis-context status decodes one exact revision per operation, while every aggregate/root read and stale-head/lifecycle/evidence check remains; changed records and mutable exports cannot poison reuse | integration | representative | automated | pending |
| U4 | Real MCP processes and baseline-created records retain exact read/status/readiness/review behavior; no production publication or migration | system | representative | automated | pending |
| U5 | Warm complete MCP read/batch/status requests improve versus unchanged source on same fixture; raw samples, medians/range and response equality are recorded; cold costs and retained bytes reported | integration | required-real | automated | satisfied |
| U6 | Generated freshness, affected package/structural checks and patch reconstruction succeed; public schemas/catalogs remain unchanged | release-artifact | not-applicable | automated | satisfied |
| U7 | Existing locked Python 3.11/3.12 CI passes for the exact integrated candidate | integration | representative | automated | pending |
| U8 | Independent material review dispositions preserve proof/live-state separation, source and user data | focused | not-applicable | manual | pending |

Deciding oracles: the unchanged identity codec on exact material, canonical stored
record decoder, actual SQLite/Git observations, complete public requests, and exact
response/catalog/schema equality. Test-only compiler stand-ins exercise cache accounting,
not domain correctness. Cold-process evidence uses real old/new code, not another call
within the original process. Timings establish only local workload costs, not client
latency, billing, p95/p99 or a universal sixfold guarantee. No absolute performance
budget is invented; paired samples and retained correctness decide the improvement.

Local evidence for U1–U6: [implementation verification](reports/verification.md), with
raw commands, samples, logs and exact package reconstruction in the delivery evidence.
U1–U4 have passing local evidence but retain `pending` because their representative
supported-runtime qualification is not yet supplied; U7 owns that integration run.
U5's required-real environment is the specifically recorded local measurement container,
not a performance promise for the deployment. U6's artifact-equality claim is independent
of the deployment interpreter. U8 independently reviews the material source. No extra
client/model qualification is introduced for unchanged tools and wire contracts.

## Boundaries, blockers and completion

Source branch `implementation/immutable-work-reuse` is a private working-container clone
for review/delivery; accepted main remains at the baseline. Integrator owns adoption;
retain the clone through package verification, with no remote push/history rewrite or
user-worktree removal. Use serial implementation of shared lifecycle/cache code.

No implementation blocker is known. Supported locked Python and independent review
may remain unavailable locally; that blocks only the respective acceptance claims.
Ordinary failed checks are repaired within this scope. Re-plan for changed authority,
record interpretation, support promises, cache lifetime/bounds or material propagation
beyond this invariant family. Preserve other audit findings as separate work.

Final state is Accepted only when every claim is satisfied and evidence is linked.
Until then name the remaining integration slice rather than treating local tests as
proof of the user's runtime. Packaging includes updated files, exact base patch and
manifest, verification results and unmodified baseline identity. No production store,
standards content, evidence approval, remote ref or dependency lock is edited.
