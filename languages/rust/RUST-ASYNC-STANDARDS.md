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
