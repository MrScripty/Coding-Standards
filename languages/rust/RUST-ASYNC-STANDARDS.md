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

Rules:

- Do not call blocking filesystem, process, network, sleep, compression, or CPU
  heavy operations directly in async request/lifecycle paths.
- Use async equivalents when available.
- Use `tokio::task::spawn_blocking` for unavoidable blocking work.
- Never hold an async lock while running blocking work.

## Mutex Selection

Use:

- `parking_lot::Mutex` for short synchronous critical sections with no `.await`
- `tokio::sync::Mutex` only when the lock must be held across `.await`
- `tokio::sync::RwLock` for many-readers/few-writers async state

Rules:

- Do not use `tokio::sync::Mutex` as the default for CPU-bound synchronous state.
- Do not hold a `std::sync::Mutex` or `parking_lot::Mutex` guard across `.await`.
- Do not split a critical section around `.await` unless the two halves are
  truly independent.
- If the second half depends on state from the first, use an async-aware mutex,
  a transaction, or redesign the data flow.

## Cancellation Safety

Dropping a future cancels it. Treat every `.await` as a possible cancellation
point unless the caller owns the full lifecycle.

Rules:

- Do not split multi-step durable operations across cancellation points unless
  the operation is transactional, idempotent, or compensating.
- Use transactions, durable state machines, or explicit compensation for
  operations that must complete atomically.
- Provide explicit `async fn close(self)` or `shutdown(self)` methods when
  cleanup must await.
- `Drop` is only a synchronous safety net, not the primary async cleanup path.

## Observability

Rules:

- Instrument long-running async workflows with `tracing` spans.
- Log task panics and cancellation reasons at the lifecycle owner.
- Add health checks for worker pools, listeners, and background services whose
  failure would otherwise be silent.
- Use `tokio-console` or equivalent runtime inspection in staging when debugging
  hung tasks, lock contention, or starvation.
