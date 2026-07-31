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

## C# Async/Await Index

This is a non-normative migration index. Generic asynchronous work ownership,
failure observation, nonblocking execution, and cancellation are canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md). The retained C#
subsections may specialize a selected runtime mechanism; they do not own or
weaken the generic contract.

### Always Observe Task Errors

Asynchronous failure observation and work ownership are canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#own-work-failure-and-cancellation).

### Never Block on Async

The nonblocking async-path contract is canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#keep-async-and-lifecycle-paths-nonblocking).

### Pass CancellationToken Through Async Chains

Cancellation ownership and propagation are canonical in
[Concurrency And Async Lifecycle](topics/concurrency.md#own-work-failure-and-cancellation).

### C# Continuation Scheduling

C# continuation scheduling and affinity mechanisms are canonical in the
[C# Async Profile](profiles/languages/csharp/async.md). Library or service
placement does not select context suppression.

---

## Rust Concurrency Routing Index

This is a non-normative migration index. Rust async mechanisms are canonical
in the [Rust Async profile](profiles/languages/rust/async.md), and
security-sensitive Rust concurrency mechanisms are canonical in the
[Rust Security profile](profiles/languages/rust/security.md).

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
