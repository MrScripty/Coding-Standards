# Rust Security Standards

Rust-specific security rules for validation, resource limits, network listeners,
and panic-safe production paths. These specialize the generic
[Security Standards](../../SECURITY-STANDARDS.md).

## Path Validation

Canonical Rust filesystem authority and validation/use behavior moved to the
[Rust Security Profile](../../profiles/languages/rust/security.md#filesystem-authority-through-use).

Generic containment, creation, concurrent-mutation, and typed-failure policy
remains governed by [Security](../../topics/security.md#filesystem-containment).

## Checked Arithmetic At Boundaries

Checked conversion, arithmetic, resource limits, and typed rejection moved to
the
[Rust Security Profile](../../profiles/languages/rust/security.md#checked-boundary-sizing).

## Bounded Queues

Any queue that accepts external input must have a maximum capacity:

```rust
const MAX_QUEUE: usize = 10_000;

let mut msgs = queue.lock();
if msgs.len() >= MAX_QUEUE {
    let drop_count = msgs.len() / 2;
    msgs.drain(..drop_count);
    tracing::warn!(drop_count, "queue overflow; dropped oldest messages");
}
msgs.push(new_message);
```

Rules:

- Define queue capacity near the queue owner.
- Decide whether overflow rejects new input, drops oldest input, or applies
  backpressure.
- Emit telemetry when dropping or rejecting work.

## Network Listener Limits

Local-only services must bind to loopback, not all interfaces:

```rust
// BAD: Exposes local IPC server to the network.
let listener = TcpListener::bind("0.0.0.0:9500").await?;

// GOOD: Local-only service bound to loopback.
let listener = TcpListener::bind("127.0.0.1:9500").await?;
```

Every listener must define a maximum concurrent connection count:

```rust
use std::sync::Arc;
use tokio::sync::Semaphore;

const MAX_CONNECTIONS: usize = 64;
let semaphore = Arc::new(Semaphore::new(MAX_CONNECTIONS));

loop {
    let permit = semaphore.clone().acquire_owned().await?;
    let (stream, _addr) = listener.accept().await?;

    tokio::spawn(async move {
        handle_connection(stream).await;
        drop(permit);
    });
}
```

Also follow task ownership and shutdown rules in
[RUST-ASYNC-STANDARDS.md](RUST-ASYNC-STANDARDS.md).

## Panic Policy

Production request paths, lifecycle code, background services, and network
handlers must not use `unwrap()` or `expect()` for recoverable errors. Follow
[RUST-API-STANDARDS.md](RUST-API-STANDARDS.md#unwrap-and-expect).
