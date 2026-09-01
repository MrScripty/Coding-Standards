# A1c User-Decision Preservation Matrix

**Status:** `exact projected-material reauthorization recorded; independent
reconciliation pending`

## Authority And Method

The accepted [A1c binding decisions](../../standards-engine-a1c/plan.md#binding-decisions)
remain authoritative. This report does not restate them as A2 authority. It
indexes every choice explicitly selected or clarified by the user, compares
the proposed A2 responsibility with that choice, and applies one of these
dispositions:

- `unchanged`: A2 does not touch the decision;
- `composed-without-change`: A2 adds behavior around the decision while the A1c
  contract and deciding owner remain intact;
- `prohibited-conflict`: the named alternative is unavailable to A2; or
- `requires-separate-user-reauthorization`: only an explicit A1c re-plan could
  reopen the decision; or
- `explicitly-reauthorized-for-replan`: the user named one exact supersession
  scope, but prototype, ADR, contract, migration, and implementation acceptance
  remain separately required.

Prototype evidence may validate an A2 composition. It cannot authorize a
different A1c choice.

## Exact Matrix

| ID | Protected A1c user decision | A2 interaction | Disposition | Deciding preservation oracle |
| --- | --- | --- | --- | --- |
| A1C-U01 | Software-development agents acting for developers are the first caller; the Python Interface is the access seam. | Controlled authoring serves the same caller through additive generated Python operations. | `composed-without-change` | Representative agent workflow requires no human CLI or second public access contract. |
| A1C-U02 | Harness-managed tool calls are the primary deployment; embedded Python is a custom integration under the same public behavior. | Proposal and application handles must round-trip through independent tool invocations. | `composed-without-change` | Cold-process workflow and generated-facade evidence agree on one result contract. |
| A1C-U03 | Engine invocation, agent turn, workflow, and agent instance are distinct lifetimes; handles survive ordinary invocation and authorized handoff boundaries. | Proposal, revision, readiness, and attempt handles must be durable and possession must not grant authority. | `composed-without-change` | Close/reopen and coordinator-to-subagent scenarios resolve the same immutable identity under current authorization. |
| A1C-U04 | Snapshot creation captures the configured canonical repository's current `HEAD`; callers cannot select repository paths, commits, trees, Git objects, or raw bytes. | A proposal begins from a caller-supplied opaque `SnapshotHandle`; target authority is deployment-owned trusted context. | `composed-without-change` | No authoring request field exposes repository path, revision, ref, object ID, store path, or authority bytes. |
| A1C-U05 | Snapshots remain until explicit authorized deletion; no age, inactivity, process, agent, reachability, or pressure inference deletes them. | Proposal abandonment cannot implicitly delete its base snapshot. | `unchanged` | Only the accepted snapshot lifecycle operations can initiate aggregate quarantine. |
| A1C-U06 | Proposed edits are non-Git change sets linked to one immutable snapshot, use the same navigation, inspection, analysis, and verification semantics, and are deleted with that snapshot. | A2 owns immutable proposal revisions over exact non-Git mutations. The selected private projected-revision material reference must feed the same compiler and Analysis kernel without turning the revision into snapshot authority. | `composed-without-change` | P2 proves compiler equivalence; P2R2 must prove identity and replay. Proposal-as-snapshot, embedded Git, full-corpus-per-edit, and a second analyzer remain `prohibited-conflict`. |
| A1C-U07 | A snapshot and all linked change sets, analyses, and dependent artifacts form one lifecycle aggregate. | Proposal roots, revisions, readiness proofs, and attempts declare exact snapshot dependencies. | `composed-without-change` | Quarantine, undelete, expiry, and purge operate over the complete dependency closure with no caller enumeration. |
| A1C-U08 | Deletion is aggregate quarantine followed by policy expiry; complete undelete is available; backup/restore remains outside the Engine Interface. | A2 adds no backup, restore, partial undelete, or independent child movement operation. | `unchanged` | Existing A1c lifecycle differential remains unchanged after any later A2 contract slice. |
| A1C-U09 | Quarantine defaults to seven days, deployment configuration alone may change it, and each deletion freezes its deadline. | A2 state inherits the base root's fixed deadline and cannot set or extend it. | `unchanged` | Repeated deletion and proposal activity leave the recorded purge deadline unchanged. |
| A1C-U10 | Immediate purge is not exposed. | A2 adds no proposal or apply variant that bypasses quarantine. | `unchanged` | Generated operation closure contains no immediate-purge capability or result. |
| A1C-U11 | `delete_snapshot` and `undelete_snapshot` are the only destructive snapshot-lifecycle behaviors; quarantine, expiry, retry, invalid-configuration, and later transactional purge semantics are exact. | A2 may reject proposal use because its root is quarantined or expired but cannot reinterpret those states. | `composed-without-change` | Existing typed lifecycle results remain byte-for-byte compatible and proposal dependents follow the aggregate transition. |
| A1C-U12 | Snapshot management uses explicit `create_snapshot`, `find_snapshots`, `delete_snapshot`, and `undelete_snapshot` methods over one internal Snapshot Module; no tagged dispatch, query/inspect overload, caller catalog, or constructor-held lifecycle state. | Candidate authoring operations must remain explicit facade operations and reuse the Snapshot Module rather than hiding mutation in `query` or `inspect`. | `composed-without-change` | Facade prototype rejects tagged dispatch and preserves all eight current operation roots. |
| A1C-U13 | Every snapshot creation yields a unique opaque lifecycle root; equal bytes may deduplicate internally and content identity cannot allocate work or couple deletion. | Proposal identity binds the opaque root and immutable revision identity without exposing the internal content hash. | `composed-without-change` | Equal-content roots remain independently deletable and no A2 public handle contains a content digest. |
| A1C-U14 | One SQLite-backed Snapshot Module owns durable aggregate state and derived child indexes; there is no generic repository, public persistence Protocol, Engine backup/restore Interface, or independent child authority. | A2 durable state is evaluated as records and indexes within that owned aggregate, with one schema decision. | `composed-without-change` | Persistence design has one owner and deletion test; a second store or public storage abstraction is `prohibited-conflict`. |
| A1C-U15 | One compiled public facade contract and domain-local material identity/version constants govern A1c; broad version bags and per-operation persisted authority are absent. | A2 may add reachable schema definitions and operations through the same compiler while each new durable identity owns only its material version. | `composed-without-change` | One schema/interface projection produces Python and agent-tool shapes; version-role audit finds no ambient bag. |
| A1C-U16 | Coverage identity is dependency-local; repository-global suite-input freshness is outside product analysis identity. | Proposal analysis binds exact relevant content, facts, relationships, contracts, and horizon inputs, not the current repository index. | `unchanged` | Unrelated repository-index changes do not invalidate a retained analysis; material dependency changes do. |
| A1C-U17 | Cross-engine stored-state compatibility and migration are deferred until Coding Standards is feature complete; incompatible state is never silently reinterpreted. | Milestone 0 must decide whether A2 is the feature-completeness trigger before selecting coordinated replacement, migration, or a compatibility window. | `requires-separate-user-reauthorization` until feature-completeness selection | Current consumer/store inventory plus an explicit product-owner feature-completeness decision. Prototype evidence alone cannot trigger compatibility. |
| A1C-U18 | Linux CPython 3.11 and 3.12 are the only accepted platforms; Windows and macOS remain unclaimed without equivalent real evidence. | A2 must re-prove new Git, SQLite, filesystem, locking, and recovery behavior on both accepted runtimes. | `composed-without-change` | Required-real public workflow passes on Linux CPython 3.11 and 3.12; other platforms remain unsupported or unclaimed. |
| A1C-U19 | Semantic understanding and judgment stay with the agent; the Engine owns declared mechanical contracts and projections only. | A2 records authorized semantic, relationship, and lifecycle decisions but cannot generate their meaning or infer acceptance from prose. | `composed-without-change` | Apply readiness contains explicit authorized decisions and mechanical proof; no generated semantic-acceptance Boolean exists. |
| A1C-U20 | The current eight public operations and their typed behavior are the accepted A1c Interface. Canonical mutation requires separate A2 authority. | A2 evaluates only additive authoring operations and separate apply capability; it cannot remove, rename, overload, or weaken an A1c operation. | `composed-without-change` | Contract differential exercises all eight A1c operations before and after any admitted A2 cutover. |
| A1C-U21 | The accepted A1c ADR and current codec identify proposed analysis material only through `proposed_snapshot`; exact cold replay reloads snapshot bytes. | Replace only that snapshot-only material assumption with one closed Analysis-owned proposed-material reference whose variants identify an exact snapshot or an exact immutable proposal revision. Include it in identity, typed dependency closure, and cold replay while retaining one `AnalysisState` and one analyzer. | `explicitly-reauthorized-for-replan` on 2026-09-01 | [Exact product authority and selected scope](a1c-projected-material-reauthorization.md), followed by P2R2 identity collision, head-movement, real SQLite cold-reopen/lifecycle, negative-dependency, snapshot-regression, bounded-overhead, and Linux CPython 3.11/3.12 evidence. |

## Conflict Register

The following ideas are already invalid for A2 because they conflict with the
matrix: caller-selected repository or Git identity, mutable snapshots,
proposal-as-accepted-snapshot, full corpus copies per edit, embedded Git state,
a second analysis authority, implicit snapshot deletion, immediate purge,
child-level lifecycle authority, a second persistence Module, public generic
storage, tagged dispatch over the A1c operations, content-hash handles, broad
version bags, repository-index analysis invalidation, Engine-inferred semantic
acceptance, or expanded platform claims without real evidence. The
snapshot-only proposed-analysis input is no longer protected against the exact
P2R2 candidate, but mutable head lookup, proposal-as-snapshot, identity salting,
composite external handles, and a second analysis authority remain invalid.

## Current Verdict

The user explicitly reauthorized A1C-U21 for prototype-first re-planning and no
other A1c choice. This clears the product-authority blocker for P2R2 but does
not admit an ADR, version, migration, public operation shape, persisted state,
or source change. A1C-U17 remains deliberately unresolved: A2 cannot declare
feature completeness or a cross-engine compatibility promise without a fresh
consumer/store inventory and separate product selection. A2-A11 remains
`pending` until P2R2 and an independent equivalent review reconcile the new
material identity with current public and stored behavior.
