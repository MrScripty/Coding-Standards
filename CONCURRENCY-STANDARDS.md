# Concurrency Standards

Canonical generic concurrency and asynchronous-lifecycle policy has moved to
[Concurrency And Async Lifecycle](topics/concurrency.md).

The language-specific sections retained below remain migration material only.
They may specialize mechanisms when routed, but they cannot weaken or override
the canonical topic.

## Core Principles

Shared-state coordination, related invariants, lock boundaries, and
nonblocking lifecycle paths are owned by
[the canonical Concurrency topic](topics/concurrency.md).

---

## C# Async/Await Rules

### Always Observe Task Errors

Asynchronous failure observation and work ownership are canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#own-work-failure-and-cancellation).

### Never Block on Async

The nonblocking async-path contract is canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#keep-async-and-lifecycle-paths-nonblocking).

### Pass CancellationToken Through Async Chains

Cancellation ownership and propagation are canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#own-work-failure-and-cancellation).

### Use ConfigureAwait(false) in Library/Service Code

Code that doesn't touch UI or engine nodes should use `ConfigureAwait(false)` to
avoid capturing the synchronization context.

```csharp
// In handlers and services (no UI access):
var data = await File.ReadAllBytesAsync(path, ct).ConfigureAwait(false);

// In code that calls UI/engine APIs: do NOT use ConfigureAwait(false)
// Must remain on the main/UI thread
```

---

## Rust Concurrency Cross-Reference

Rust-specific concurrency rules live in
[languages/rust/RUST-ASYNC-STANDARDS.md](languages/rust/RUST-ASYNC-STANDARDS.md)
and security-sensitive resource limit rules live in
[languages/rust/RUST-SECURITY-STANDARDS.md](languages/rust/RUST-SECURITY-STANDARDS.md).

---

## TypeScript Concurrency Rules

### Guard Against Stale Async Responses

When a user action triggers an async request, a second action may arrive
before the first response. Use a request ID to discard stale responses:

```typescript
let currentRequestId = 0;

async function loadData(path: string) {
    const requestId = ++currentRequestId;
    isLoading = true;
    const result = await api.request({ action: 'load', payload: { path } });
    if (requestId !== currentRequestId) return;  // Stale — discard
    applyResult(result);
}
```

---

## Godot Thread Safety

### Main Thread Rule

Godot node operations (`AddChild`, `Call`, `QueueFree`, signal emission)
must run on the main thread. Use `CallDeferred` or `Callable.From(...).CallDeferred()`
to marshal work to the main thread from async contexts.

### `IsInstanceValid` Before Use

Always check `GodotObject.IsInstanceValid(node)` before calling methods on
a Godot node reference that may have been freed.
