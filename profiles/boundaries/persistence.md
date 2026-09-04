# Persistence Boundary Profile

**Standards metadata**

- ID: `profile.boundary.persistence`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A change creates or changes a durable read, write, publication, transaction, migration-application, version-ledger, or store-mutation boundary.
- Does not apply when: State is proven process-local and ephemeral, or the change preserves every selected durable-state mechanism and contract unchanged.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `topic.contracts.evolution`
- Specializes: `topic.contracts`
- Verification: Persistence owner decisions plus claim-matched durable source, destination, publication, interruption, and reopening evidence.
- Canonical owner: `profiles/boundaries/persistence.md`

## Concurrent Durable Updates

When two writers can update the same invariant, a read followed by an
unconditional write can lose an update. For example, both writers reading
revision 7 and saving a new balance must not silently overwrite one another.
Use a conditional revision update and check that it succeeded, or a transaction
whose isolation and locking protect the entire invariant. A uniqueness check
followed by a separate insert is subject to the same race; enforce uniqueness
at the durable boundary.

On a retryable conflict, re-read and re-evaluate the whole transaction within
a bounded budget. Do not retry only the final statement using stale decisions,
and do not repeat nontransactional external effects without their own
idempotency or coordination contract. Test concurrent writers and aborted
transactions against the actual store guarantees.

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

## Durable Mutation Contract

For each durable mutation, define the authoritative precondition, accepted
postcondition, integrity constraints, publication boundary, interruption
behavior, and proof required by actual consumers. Select operation structure
from those facts and the available store guarantees. Gathering, validation,
isolated staging, publication, and postcondition proof are distinct
responsibilities when the selected contract requires them; they are not a
mandatory five-phase implementation sequence.

Complete every precondition and input proof that must hold before publication.
Staging may use incomplete representations only when they are non-authoritative,
unobservable to consumers, bounded by an owned lifecycle, and either completed
or removed according to the selected failure contract. Never publish a
placeholder or temporarily invalid representation as authoritative state.

Publish through a mechanism that makes the selected postcondition observable
without exposing a prohibited partial state. A transaction, atomic replacement,
journal, or append-only operation satisfies this requirement only when its
proven guarantees match the complete invariant. Successful API return, an
allocated identifier, or completion of one write does not prove related
indexes, references, records, or metadata are consistent.

Run every proof required for authoritative correctness in each supported
production path. Optional debug audits may add evidence, but they cannot replace
required runtime validation or postcondition proof. If publication may have
partly occurred or its outcome cannot be established, do not report success or
continue from guessed state; preserve the typed outcome for the owning recovery
contract.

## Migration Execution Contract

Execute a migration only for source and destination states selected by
Contracts. Before mutation, prove the authoritative current state, applicable
migration identity and integrity, deterministic dependency and ordering facts,
required store capabilities, ledger consistency, and coordination authority.
A migration directory, filename sort, pending row, startup hook, or newer
application version does not prove those facts.

Give each selected migration stable identity under the applicable contract and
verify that the artifact to execute is the accepted artifact. Define how changed,
missing, duplicate, or conflicting identities are classified. Discover and
order migrations from explicit accepted metadata or another deterministic
contract; do not infer authority from filesystem enumeration or an incidental
lexical order.

Keep durable state and its migration ledger consistent at every authoritative
publication boundary. Record completion only after the destination postcondition
is proven. Re-entry behavior is selected per migration: proven idempotent
application, one-shot rejection, continuation from an owned checkpoint, or
another explicit mechanism. Prior attempt, process restart, or an apparently
pending ledger entry does not authorize repeated application.

Define interruption and unknown-outcome handling before execution. Preserve the
observed source, destination, and ledger facts for Resilience to select recovery;
do not delete, rebuild, roll back, roll forward, or mark completion by default.
The caller that owns an accepted lifecycle trigger invokes migration execution.
Application startup is one possible trigger, not migration authority or a
universal execution phase.

Contracts determines whether different application versions or retained states
must coexist. Derive overlap handling from actual deployment and consumer facts.
Additive shape, a default value, ignored data, a two-phase shim, or coordinated
replacement is safe only when the selected producer-consumer contract proves
it; none is a compatibility default owned by Persistence.

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
authoritative source and destination state, precondition and postcondition
proof, isolated staging, interruption before and during publication, reopening
through real store adapters, supported and unsupported versions, overlapping
access, corrupt or contradictory state, and rejection of every prohibited
fallback.

Illustrative mechanism adaptation belongs in the non-normative
[Persistence Mechanism Recipes](../../reference/recipes/persistence.md).
