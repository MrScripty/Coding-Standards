# Concurrency Standards

Guidelines for safe concurrent and asynchronous programming across C#, Rust, and TypeScript.

## Core Principles

### 1. Prefer Message Passing Over Shared Mutable State

When two components need to communicate, send a message rather than sharing a
mutable variable. Apply this at both macro level (IPC between processes) and
micro level (between modules).

```
// GOOD: Send a message
dispatcher.Send("selection", "changed", newState);

// AVOID: Share a mutable reference
sharedState.Selection = newState;  // Who else reads this? When?
```

When shared state is unavoidable, protect it (see below).

### 2. Protect Shared Mutable State

Any data accessed by more than one thread must be protected.

**C# — Use `lock`, `Interlocked`, or immutable snapshots:**

```csharp
// GOOD: Atomic operations for simple values
private int _count;
Interlocked.Increment(ref _count);

// GOOD: Lock for compound operations
lock (_stateLock)
{
    _state = _state with { SelectedId = newId };
    SelectionChanged?.Invoke(_state);
}

// BAD: Unprotected field access
private bool _isProcessing;  // Read/written from multiple threads
```

**Rust — Use `parking_lot::Mutex` (preferred) or `std::sync::Mutex`:**

```rust
// GOOD: parking_lot (no poisoning, faster)
use parking_lot::Mutex;
let data = mutex.lock();  // Returns guard directly, no unwrap needed

// AVOID: std::sync::Mutex with unwrap (poison cascade)
let data = mutex.lock().unwrap();  // Panics if any thread panicked while holding lock
```

### 3. Keep Related State Under One Lock

If two fields are logically related and must be consistent, protect them with
a single lock. Never update them under separate locks.

```rust
// BAD: Two locks for related data — race condition between updates
*shared.buffer.lock() = Some(data);
*shared.buffer_size.lock() = (width, height);  // Consumer reads between these two lines

// GOOD: Single lock for related data
let mut frame = shared.frame_data.lock();
frame.buffer = Some(data);
frame.width = width;
frame.height = height;
```

```csharp
// BAD: Separate updates
_pendingRequestId = message.Id;     // Thread A writes
_pendingAction = "open";            // Thread A writes
// Thread B reads _pendingRequestId before _pendingAction is set

// GOOD: Atomic update
lock (_pendingLock)
{
    _pendingRequestId = message.Id;
    _pendingAction = "open";
}
```

---

## C# Async/Await Rules

### Always Observe Task Errors

Never discard a Task without handling potential exceptions.

```csharp
// BAD: Fire and forget — exception silently lost
_ = DoWorkAsync();

// GOOD: Observe errors
DoWorkAsync().ContinueWith(
    t => _logger.Error(t.Exception!.InnerException, "Unhandled error"),
    TaskContinuationOptions.OnlyOnFaulted);

// GOOD: If you truly don't care about the result, at minimum log
_ = Task.Run(async () =>
{
    try { await DoWorkAsync(); }
    catch (Exception ex) { _logger.Error(ex, "Background task failed"); }
});
```

### Never Block on Async

Calling `.Result` or `.Wait()` on a Task can deadlock in UI synchronization
contexts.

```csharp
// BAD: Blocks thread, deadlock risk
var result = client.GetAsync(url).Result;

// GOOD: Await properly
var result = await client.GetAsync(url);

// ACCEPTABLE: When truly synchronous context is required and you control the scheduler
var result = client.GetAsync(url).ConfigureAwait(false).GetAwaiter().GetResult();
```

### Pass CancellationToken Through Async Chains

Every async method that could be long-running should accept and forward a
`CancellationToken`.

```csharp
// GOOD: Token flows through the chain
public async Task ExtractAsync(string path, CancellationToken ct)
{
    await _manager.OpenAsync(path, ct);
    await File.WriteAllBytesAsync(outputPath, data, ct);
}

// BAD: Token ignored or not accepted
public async Task ExtractAsync(string path)
{
    await _manager.OpenAsync(path);  // Can't cancel
}
```

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

## Rust Concurrency Rules

### Use `parking_lot` Over `std::sync`

`parking_lot::Mutex` does not poison on panic, avoids cascading failures,
and is measurably faster. Use it as the default.

### Overflow-Check Arithmetic at Boundaries

Values received from external sources (FFI callbacks, network data) may be
malformed. Use checked arithmetic before allocating:

```rust
let buffer_size = (width as usize)
    .checked_mul(height as usize)
    .and_then(|s| s.checked_mul(4))
    .expect("buffer size overflow");
```

### Bound Queue Sizes

Any queue that accepts external input must have a maximum capacity:

```rust
const MAX_QUEUE: usize = 10_000;
let mut msgs = queue.lock();
if msgs.len() >= MAX_QUEUE {
    msgs.drain(..msgs.len() / 2);
    tracing::warn!("Queue overflow — dropped oldest messages");
}
msgs.push(new_message);
```

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
