# Rust Async Standards

Canonical Rust async applicability and sync/async boundary selection have moved
to the [Rust Async profile](../../profiles/languages/rust/async.md).

The mechanism sections retained below remain migration material only. They
cannot weaken or override the generic
[Concurrency topic](../../topics/concurrency.md) or the Rust Async profile.

## Sync Core, Async Shell

Contract-driven sync/async selection is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#select-the-execution-contract).

## Runtime Boundaries

Runtime composition is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#runtime-composition).

## Task Lifecycle

Spawned-work ownership is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#own-spawned-work).

## Graceful Shutdown

Owned shutdown sequencing is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#coordinate-shutdown).

## Blocking Work

Blocking isolation is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#isolate-blocking-work).

## Mutex Selection

Synchronization selection is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#select-synchronization-from-contract).

## Cancellation Safety

Cancellation-state proof, durable-work safety, and asynchronous cleanup are
canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#prove-cancellation-state).

## Observability

Lifecycle-owned terminal evidence is canonical in the
[Rust Async profile](../../profiles/languages/rust/async.md#own-lifecycle-evidence).
