# Rust Async Standards

Async architecture, Tokio runtime boundaries, task lifecycle, mutex selection,
and cancellation safety for Rust codebases.

## Sync Core, Async Shell

Async is an I/O and scheduling tool, not an architecture by itself.

Default to synchronous domain/core APIs. Add async at the outermost I/O boundary
and pull it inward only when concurrent I/O is central to the operation.

Rules:

- Keep parsing, validation, transformation, planning, policy, and pure
  orchestration synchronous when possible.
- Use async shells for HTTP, IPC, database, filesystem, stream, queue, and
  runtime integration.
- Do not make a function async only because its caller is async.
- If a function performs no `.await`, it should usually not be async.
- Libraries should default to sync APIs unless async behavior is part of the
  contract.
- If the core must be async, document which concurrent I/O operations justify
  the complexity.

```rust
// GOOD: async shell, sync core.
async fn handle_request(raw: RawRequest) -> Result<Response, AppError> {
    let user = fetch_user(raw.user_id).await?;
    let input = RequestInput::try_from(raw)?;
    Ok(build_response(input, user)?)
}

fn build_response(input: RequestInput, user: User) -> Result<Response, DomainError> {
    // pure domain logic
}
```

## Runtime Boundaries

Rules:

- Runtime creation belongs in the composition root, not library/core crates.
- Libraries should not create global Tokio runtimes.
- Background tasks must be owned by a lifecycle manager.
- Every `tokio::spawn` must have a tracked `JoinHandle`, `JoinSet`, or
  `TaskTracker`.
- Shutdown must propagate cancellation and await or abort spawned tasks.
- Task panics must be inspected and logged, propagated, restarted, or degraded
  deliberately.

## Task Lifecycle

Every spawned task must have an owner responsible for shutdown.

Rules:

- Do not call `tokio::spawn` and discard the handle.
- Store `JoinHandle`s, use `JoinSet`, or use `tokio_util::task::TaskTracker`.
- Await, abort, or drain spawned tasks during shutdown.
- Treat `JoinError::is_panic()` as a production defect unless the task is
  explicitly isolated and restartable.
- Log cancellation and panic paths at the lifecycle owner, not inside every leaf
  task.

Example:

```rust
struct Server {
    tasks: Vec<tokio::task::JoinHandle<()>>,
}

impl Server {
    fn spawn_worker(&mut self, work: impl Future<Output = ()> + Send + 'static) {
        self.tasks.push(tokio::spawn(work));
    }

    async fn shutdown(self) {
        for handle in self.tasks {
            match handle.await {
                Ok(()) => {}
                Err(error) if error.is_panic() => {
                    tracing::error!("task panicked during shutdown: {error}");
                }
                Err(error) => {
                    tracing::warn!("task cancelled during shutdown: {error}");
                }
            }
        }
    }
}
```

## Graceful Shutdown

Spawned services must receive a cancellation signal and stop accepting new work
before draining in-flight work.

Recommended mechanisms:

- `tokio_util::sync::CancellationToken` for tree-shaped cancellation.
- `tokio::sync::watch` when tasks need the latest shutdown state.
- `tokio::sync::broadcast` when many independent listeners need the same signal.
- `JoinSet` or `TaskTracker` to await task completion.

Rules:

- Select on both work and shutdown signals in long-running loops.
- Stop accepting new connections or queue items before draining existing work.
- Apply a timeout before force-aborting tasks that do not shut down.
- Make shutdown idempotent; repeated shutdown requests should not panic.

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
