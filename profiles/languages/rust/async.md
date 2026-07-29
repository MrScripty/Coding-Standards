# Rust Async Profile

**Standards metadata**

- ID: `profile.language.rust.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust code changes an asynchronous API, suspension boundary, concurrent I/O contract, stream, backpressure, cancellation-aware operation, or async resource lifetime.
- Does not apply when: The affected Rust behavior is synchronous and does not select or change an asynchronous contract or mechanism.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.rust`
- Specializes: `topic.concurrency`, `profile.language.rust`
- Verification: Rust async-boundary and lifecycle decisions plus affected API, cancellation, integration, and shutdown tests.
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

## Typed Outcomes

Return the operation's typed `unsupported` or `unavailable` outcome when its
required execution contract cannot be provided. Preserve operation-specific
failures when they are more precise. Runtime, task, and shutdown failures retain
their operation-specific terminal outcome.

## No Fallback

Unresolved execution requirements cannot select sync, async, a thread, a
runtime, blocking, or detached work by convenience. Do not silently change the
API contract, block an async path, create a runtime, or discard owned work to
make the operation execute.

Missing lifecycle proof cannot create a library-global or alternate runtime,
detach work, treat leaf logging as ownership, discard failure or panic, keep
admission open while draining, or force-abort work without authority and
interruption safety.

Blocking isolation, mutex selection, cancellation-safety mechanisms, and
observability are separate Rust Async concerns not defined by these sections.
Runtime construction, task ownership, shutdown sequencing are now defined
above without selecting a project-specific mechanism.

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
- no convenience fallback changes execution mode or ownership.
