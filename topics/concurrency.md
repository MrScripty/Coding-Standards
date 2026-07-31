# Concurrency And Async Lifecycle

**Standards metadata**

- ID: `topic.concurrency`
- Role: `topic`
- Level: `MUST`
- Applies when: Work can overlap, state can be accessed concurrently, or asynchronous work has failure, cancellation, or lifecycle obligations.
- Does not apply when: Execution is proven sequential and no asynchronous work can outlive its immediate caller.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Concurrency ownership decisions plus affected synchronization and lifecycle tests.
- Canonical owner: `topics/concurrency.md`

## Select Coordination From The Invariant

Identify the state, allowed writers, required atomicity, ordering, and lifetime
before selecting a coordination mechanism.

Immutable or otherwise thread-safe data does not require a lock merely because
multiple threads can access it. Shared mutable invariants require an explicit
strategy such as:

- exclusive ownership;
- message passing;
- synchronization;
- atomic operations; or
- a transaction.

Select the strategy from the invariant and the available mechanism guarantees.
Message passing can remove shared mutation, but it is not a universal
architecture. Do not replace an unavailable strategy with unprotected shared
mutation or present one language-specific mechanism as universal policy.

## Preserve Related Invariants

State that must change or be observed consistently must share one coordination
contract. The contract may use one critical section, an atomic snapshot, a
transaction, serialized ownership, or another mechanism that proves the whole
invariant. Do not mandate one lock when a different mechanism provides the
required atomicity, and do not split related updates across mechanisms that
permit an invalid intermediate state to escape.

## Keep External Code Outside Locks

Do not invoke callbacks, signals, user code, plugin code, or other externally
controlled behavior while holding a lock. Capture the required immutable
snapshot or result, release the lock, and then invoke the external behavior.

This rule applies even when the current callback appears synchronous or
trusted. External behavior can re-enter the owner, acquire another lock, block,
or change independently.

## Keep Async And Lifecycle Paths Nonblocking

Async request, startup, shutdown, health, and supervision paths must not perform
blocking work directly. Use a mechanism that preserves the path's nonblocking
contract, or return the operation's typed `unsupported` or `unavailable`
outcome when no valid mechanism exists.

Do not synchronously wait on asynchronous work as a fallback. Do not hold a
lock across blocking work. Language and runtime profiles own concrete
mechanisms for isolating unavoidable blocking work.

## Own Work, Failure, And Cancellation

Every asynchronous operation that can outlive its immediate call site must
have an owner responsible for:

- observing completion and failure;
- propagating or explicitly terminating cancellation;
- defining shutdown behavior; and
- retaining only the operation state required by the current invocation.

Dropping a task, future, promise, handle, or equivalent does not transfer
ownership. Logging inside detached work is not sufficient unless a selected
owner also tracks its completion and lifecycle.

Cancellation must propagate through all owned work that remains part of the
operation. A boundary may translate cancellation into another concrete
mechanism, but it must preserve the cancellation decision and typed outcome.

## Isolate Verification Resources

Verification that can overlap must give each case exclusive ownership of its
mutable process-global and durable resources, or apply an explicit coordination
contract that proves the affected invariant. Environment variables, temporary
roots, databases, registry or configuration files, caches, ports, singleton
services, and process-wide state are shared resources when concurrent cases can
observe or mutate the same identity.

Restore borrowed global state and terminate owned work before the case exits.
Exercise the selected parallelism and lifecycle conditions needed to expose
state leakage, but derive repetition count, schedule, and environment from the
claim rather than a fixed test recipe.

Serialization is a valid selected mechanism only when the owner records the
shared invariant, exclusion scope, and reason independent ownership cannot be
established. Do not serialize as a fallback for unidentified interference,
retain stale durable state, reuse an ambient resource identity, or weaken
parallel verification to make a race disappear. Return a typed diagnostic when
the required ownership or coordination facts are missing or unavailable.

## Typed Outcomes

Return the operation's typed `invalid`, `unsupported`, or `unavailable`
diagnostic when required coordination, ownership, observation, cancellation,
or nonblocking execution cannot be established. Preserve more specific
operation failures when they exist.

Do not continue through fire-and-forget work, discarded failures, ignored
cancellation, synchronous blocking, callbacks under locks, unprotected
mutation, or an alternate language/runtime mechanism.

## Verification

Evidence must exercise the affected invariant and lifecycle decisions,
including applicable:

- concurrent reads and writes;
- related-state consistency;
- callback re-entry or lock ordering;
- nonblocking request and lifecycle behavior;
- success, failure, and cancellation observation;
- owner shutdown with active work; and
- timer, subscription, polling, and retry cleanup;
- restart termination without duplicate work;
- current-invocation results winning over stale overlapping work;
- cancellation without residual partial state;
- verification-resource isolation under selected parallel execution; and
- rejection when the required mechanism or owner is unavailable.

A passing build, startup smoke, happy path, serialized rerun, or assertion that
omits the lifecycle outcome does not prove these claims.
