# Rust Async Profile

**Standards metadata**

- ID: `profile.language.rust.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust code changes an asynchronous API, suspension boundary, concurrent I/O contract, stream, backpressure, cancellation-aware operation, or async resource lifetime.
- Does not apply when: The affected Rust behavior is synchronous and does not select or change an asynchronous contract or mechanism.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.rust`
- Specializes: `topic.concurrency`, `profile.language.rust`
- Verification: Rust async-boundary decisions plus affected API, cancellation, integration, and lifecycle tests.
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

## Typed Outcomes

Return the operation's typed `unsupported` or `unavailable` outcome when its
required execution contract cannot be provided. Preserve operation-specific
failures when they are more precise.

## No Fallback

Unresolved execution requirements cannot select sync, async, a thread, a
runtime, blocking, or detached work by convenience. Do not silently change the
API contract, block an async path, create a runtime, or discard owned work to
make the operation execute.

Runtime construction, task ownership, shutdown, blocking isolation, mutex
selection, cancellation mechanisms, and observability are separate Rust Async
concerns and are not defined by this foundation.

## Verification

Evidence covers the affected contract:

- pure non-suspending logic remains callable synchronously;
- real I/O or streaming paths suspend through the supported mechanism;
- cancellation and resource lifetimes remain observable where contracted;
- sync and async public consumers receive the declared API;
- unsupported or unavailable execution capability returns a typed outcome; and
- no convenience fallback changes execution mode or ownership.
