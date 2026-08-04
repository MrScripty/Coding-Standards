# Persistence Boundary Profile

**Standards metadata**

- ID: `profile.boundary.persistence`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A change creates or changes a durable read, write, publication, transaction, migration-application, version-ledger, or store-mutation boundary.
- Does not apply when: State is proven process-local and ephemeral, or the change preserves every selected durable-state mechanism and contract unchanged.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `topic.contracts`
- Verification: Persistence owner decisions plus claim-matched durable source, destination, publication, interruption, and reopening evidence.
- Canonical owner: `profiles/boundaries/persistence.md`

## Durable Boundary Authority

Treat state as durable when a supported consumer can observe it after the
operation, process, deployment, or runtime that produced it has ended. Before
selecting a persistence mechanism, establish the authoritative source and
destination states, supported versions, required durable invariants, mutation
and publication authority, available store capabilities, and acceptance
evidence.

A configured store, existing table, file path, transaction API, migration
directory, or prior implementation does not select the mechanism. Use the
[Contracts topic](../../topics/contracts.md) to select supported states,
evolution, and compatibility before applying this profile.

## Select The Durable Mechanism

Select the mechanism from the owned invariant and proven capabilities. Record:

- which state is authoritative before and after the operation;
- which component may read, stage, publish, replace, or remove each durable
  representation;
- the atomicity, integrity, ordering, interruption, and reopening guarantees
  the operation requires;
- the versions and persisted states the current contract supports;
- the store guarantees actually available in the required environment; and
- the evidence that proves the selected postcondition to its consumers.

The selected contract may use a transaction, atomic replacement, append-only
record, journal, object publication, explicit version ledger, or another proven
mechanism. None is a universal default. If no durable state crosses the
boundary, do not introduce persistence work merely because a store is present.

## Responsibility Boundaries

Persistence owns durable read, write, staging, publication, transaction,
migration-application, ledger, and store-adapter mechanisms. Contracts owns
supported state and evolution semantics. Resilience owns failure handling and
recovery. Concurrency owns overlapping access and coordination. Security owns
authorization. Build owns generated artifacts. Diagnostics owns reporting.
Verification owns evidence sufficiency.

This profile does not own every in-memory mutation and does not mandate a
database, transaction, migration framework or format, startup execution,
version table, rollback mechanism, compatibility window, or implementation
phase sequence.

## Typed Outcomes And No Fallback

Return `unavailable` when required authority, source or destination state,
durable invariant, store capability, ledger, coordination, or evidence cannot
be established. Return `invalid` for partial authoritative publication,
contradictory durable state or ledger facts, corrupt state, or incomplete proof.
Return `unsupported` when a well-formed persisted version or required mechanism
is outside the selected contract.

Do not fall back to partial writes, temporary invalid authoritative state,
debug-only validation, deletion or rebuild, guessed migration order, repeated
application, startup execution, default rollback, assumed additive
compatibility, a nearby weaker store, or speculative coexistence. Return the
typed diagnostic selected by the failed durable contract.

## Verification

Verify the claims selected for the changed boundary. Applicable evidence covers
authoritative source and destination state, interruption before and during
publication, reopening through real store adapters, supported and unsupported
versions, overlapping access, corrupt or contradictory state, and rejection of
every prohibited fallback.

Illustrative mechanism adaptation belongs in the non-normative
[Persistence Mechanism Recipes](../../reference/recipes/persistence.md).
