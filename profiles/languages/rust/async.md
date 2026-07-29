# Rust Async Profile

**Standards metadata**

- ID: `profile.language.rust.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust code changes an asynchronous API, suspension boundary, concurrent I/O contract, stream, backpressure, cancellation-aware operation, or async resource lifetime.
- Does not apply when: The affected Rust behavior is synchronous and does not select or change an asynchronous contract or mechanism.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.rust`
- Specializes: `topic.concurrency`, `profile.language.rust`
- Verification: Rust async-boundary, lifecycle, blocking-isolation, and synchronization decisions plus affected API, cancellation, integration, and shutdown tests.
- Canonical owner: `profiles/languages/rust/async.md`

## Select The Execution Contract

Select synchronous or asynchronous behavior from:

- whether the operation suspends for I/O or scheduling;
- whether concurrent I/O, streaming, or backpressure is part of the contract;
- caller and consumer deployment/API constraints;
- cancellation and lifecycle obligations; and
- supported execution capabilities.

Do not add `async` merely because a caller is asynchronous. Do not remove
`async` merely to satisfy a blanket synchronous-core preference.

## Keep Non-Suspending Logic Synchronous

Parsing, validation, transformation, policy, and other pure logic remain
synchronous when they have no suspension, concurrency, cancellation, or async
resource-lifetime contract. An async shell may call that synchronous logic
without making the inner operation asynchronous.

A function with no suspension point requires an explicit contract reason to be
async. Caller convenience alone is not sufficient.

## Preserve Genuine Async Contracts

An async core or library API is valid when concurrent I/O, streaming,
backpressure, cancellation, or an async resource lifetime is part of its
observable contract. Record that contract and verify it through the real
supported execution path.

Library ownership does not imply synchronous or asynchronous behavior by
default. Public API shape follows the library's consumer and lifecycle
contract.

## Runtime Composition

The adopting application's composition root owns runtime construction,
configuration, sharing, and shutdown. A library consumes an injected runtime
capability or exposes an async contract to its caller; it does not create a
process-global or alternate runtime to make an operation execute.

The composition owner records supported runtime capabilities and makes them
available to all operations that share that runtime. A request, task, binding,
or library call may use the selected capability without becoming the runtime
owner.

## Own Spawned Work

Every spawned task is registered with one lifecycle owner before it can outlive
its spawning scope. That owner:

- retains the task's completion capability;
- observes success, failure, panic, and cancellation;
- defines whether and when restart is valid;
- includes the task in shutdown; and
- releases tracking only after a terminal outcome is observed.

The concrete task set or handle type follows the selected runtime. Returning
from a spawn call, logging inside the task, or discarding a handle does not
establish ownership.

## Coordinate Shutdown

An owned shutdown sequence:

1. makes repeated shutdown requests idempotent or returns the same typed
   terminal outcome;
2. closes admission for new owned work;
3. signals cancellation through the selected mechanism;
4. drains and observes tracked work; and
5. reports complete, incomplete, or failed shutdown through typed outcomes.

A time limit does not itself authorize abort. Force-abort is permitted only
when the lifecycle owner has abort authority and the operation contract proves
that interruption cannot violate required consistency, durability, or release
obligations. Otherwise an incomplete drain remains a typed incomplete or
unavailable outcome for the owning operation.

## Isolate Blocking Work

Classify whether an operation can block its executing thread or consume
sustained CPU before placing it on an async execution path. Use a supported
async capability only when it preserves the operation's I/O, cancellation,
resource-lifetime, ordering, and failure contract.

The runtime composition and lifecycle boundary owns the isolation capability
for unavoidable blocking or CPU-heavy work. That capability defines admission,
capacity, completion observation, cancellation/shutdown behavior, and resource
accounting. Isolation without a bounded or otherwise governed capacity contract
is not sufficient.

Do not execute blocking work inline on an async request or lifecycle path. Do
not invoke or await blocking work while holding a synchronization guard.
Preserve related invariants through an appropriate ownership, coordination, or
transaction design rather than splitting the protected operation for
convenience.

## Select Synchronization From Contract

Select synchronization from:

- whether the protected critical section can suspend;
- the complete invariant and ownership boundary;
- contention and read/write behavior;
- fairness, poisoning, recovery, and cancellation obligations; and
- capabilities supported by the selected runtime and deployment.

A non-suspending critical section uses a mechanism that does not require
suspension support. A guard crosses suspension only when the selected mechanism
supports that behavior and the invariant requires the protected scope. If no
supported mechanism can preserve the invariant, redesign ownership or
coordination, or return the operation's typed unavailable outcome.

Do not call external, plugin, callback, or user-controlled behavior while a
guard is held. Do not select one synchronization implementation as a universal
default for all Rust state.

## Prove Cancellation State

Stopping or dropping future polling proves only that the future will not be
polled by that owner. It does not prove that external I/O, a remote request, a
blocking operation, or another independently owned side effect stopped or
rolled back.

Derive external cancellation and terminal-state claims from the affected
capability's contract and evidence. If external work may continue, preserve its
identity and ownership so completion, cancellation, reconciliation, or retry
can be handled explicitly.

## Preserve Durable Work

Before a durable multi-step operation crosses a cancellation point, select a
transactional, idempotent, resumable, or compensating design that preserves its
required invariant. A cancellation boundary cannot leave authoritative state
in an unclassified partial outcome.

## Own Asynchronous Cleanup

Cleanup that can suspend has an explicit lifecycle-owned completion path.
Synchronous destruction may release synchronous resources or enforce a local
safety invariant, but it does not stand in for required asynchronous cleanup.
Do not detach cleanup merely to let destruction or shutdown return.

## Own Lifecycle Evidence

The lifecycle owner observes health, success, failure, panic, cancellation, and
shutdown outcomes for its owned work. Leaf operations may emit diagnostic
context, but leaf logging does not establish terminal-state ownership or prove
that a failed task remains supervised.

Select health, telemetry, and inspection mechanisms from the operational
contract and supported environment. Tool availability is not evidence unless
the lifecycle owner consumes the relevant signal and connects it to an owned
operation and terminal outcome.

## Typed Outcomes

Return the operation's typed `unsupported` or `unavailable` outcome when its
required execution contract cannot be provided. Preserve operation-specific
failures when they are more precise. Runtime, task, and shutdown failures retain
their operation-specific terminal outcome. Missing blocking-isolation,
capacity, synchronization, cancellation, cleanup, or observation capability
remains explicit.

## No Fallback

Unresolved execution requirements cannot select sync, async, a thread, a
runtime, blocking, or detached work by convenience. Do not silently change the
API contract, block an async path, create a runtime, or discard owned work to
make the operation execute.

Missing lifecycle proof cannot create a library-global or alternate runtime,
detach work, treat leaf logging as ownership, discard failure or panic, keep
admission open while draining, or force-abort work without authority and
interruption safety.

Missing execution or synchronization proof cannot block inline, create an
alternate executor or thread, run unbounded isolated work, hold an unsupported
guard across suspension, split a related invariant, or select a universal
mutex.

Runtime construction, task ownership, shutdown sequencing, blocking isolation,
synchronization selection, cancellation safety, cleanup, and lifecycle
evidence are defined above without selecting a project-specific mechanism.

Missing cancellation or observation proof cannot assume external cancellation
from a dropped future, leave durable work unprotected, delegate async cleanup
only to synchronous destruction, detach cleanup, treat leaf logging as
ownership, permit silent task death, or present tool availability as lifecycle
evidence.

## Verification

Evidence covers the affected contract:

- pure non-suspending logic remains callable synchronously;
- real I/O or streaming paths suspend through the supported mechanism;
- cancellation and resource lifetimes remain observable where contracted;
- sync and async public consumers receive the declared API;
- unsupported or unavailable execution capability returns a typed outcome;
- runtime construction occurs only at the selected composition owner;
- spawned work reaches one observed terminal outcome;
- shutdown closes admission, signals cancellation, and drains tracked work;
- abort paths prove authority and interruption safety; and
- blocking work uses an equivalent async capability or governed isolation;
- isolated work participates in admission, completion, and shutdown ownership;
- synchronization preserves the complete invariant across any suspension;
- unsupported isolation, capacity, or synchronization returns a typed outcome;
- dropped future polling is distinguished from external operation state;
- durable work remains transactional, idempotent, resumable, or compensating;
- asynchronous cleanup reaches an owned observed completion;
- lifecycle health and terminal outcomes are observed by their owner;
- unavailable cancellation, cleanup, or observation returns a typed outcome;
  and
- no convenience fallback changes execution mode or ownership.
