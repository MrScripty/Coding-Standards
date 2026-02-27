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

### 4. Keep Async Paths Non-Blocking

Async request paths and lifecycle paths (startup/shutdown/health loops) must not
run blocking calls directly. Blocking operations stall the runtime thread and can
delay unrelated work.

Avoid direct blocking calls such as:
- `std::thread::sleep`
- blocking process/file/network calls in async handlers
- `Thread.Sleep`, `Task.Wait`, or sync process waits in async C# code

Use async equivalents, or isolate unavoidable blocking work:

```rust
// BAD: Blocks async runtime worker thread
std::thread::sleep(Duration::from_millis(200));

// GOOD: Non-blocking async timer
tokio::time::sleep(Duration::from_millis(200)).await;

// GOOD: Isolate unavoidable blocking work
let output = tokio::task::spawn_blocking(move || std::fs::read(path)).await??;
```

```csharp
// BAD: Blocks thread inside async flow
Thread.Sleep(200);
process.WaitForExit();

// GOOD: Async-friendly alternatives
await Task.Delay(200, ct);
await process.WaitForExitAsync(ct);
```

Never hold an async lock across blocking operations. If blocking work is
unavoidable, copy required data, release the lock, and then run the work.

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

### Async Mutex Selection

Choose the right mutex based on whether the lock is held across `.await` points:

| Mutex | When to Use | Key Characteristic |
|-------|------------|-------------------|
| `parking_lot::Mutex` | Lock held briefly, no `.await` while locked | Blocks OS thread; ideal for fast CPU-bound work |
| `tokio::sync::Mutex` | Lock held across `.await` points | Yields the async task, does not block the runtime thread |
| `tokio::sync::RwLock` | Many concurrent readers, infrequent writers | Read-parallelism when writes are rare; still async-aware |

**The rule:** Use `parking_lot::Mutex` (or `std::sync::Mutex`) for synchronous critical sections. Use `tokio::sync::Mutex` only when the lock must be held across an `.await`.

```rust
// BAD: std/parking_lot mutex held across .await — blocks the runtime thread
let guard = self.state.lock();
let result = self.client.send(guard.pending_request()).await; // Deadlock risk!
guard.mark_sent(result);

// GOOD: tokio mutex when holding across .await
let mut guard = self.state.lock().await;
let result = self.client.send(guard.pending_request()).await;
guard.mark_sent(result);
```

```rust
// BAD: tokio mutex for synchronous CPU-bound work — unnecessary overhead
let guard = self.cache.lock().await;
let parsed = expensive_parse(&guard.raw_data); // No .await needed
drop(guard);

// GOOD: parking_lot mutex for synchronous work
let guard = self.cache.lock();
let parsed = expensive_parse(&guard.raw_data);
drop(guard);
```

### Async Task Lifecycle

#### Spawn Cleanup

Every `tokio::spawn` must have a corresponding `JoinHandle` that is awaited or
aborted during shutdown. Spawning without tracking the handle creates orphaned
tasks that leak resources or prevent clean exit.

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
            if let Err(e) = handle.await {
                tracing::error!("Task panicked during shutdown: {e}");
            }
        }
    }
}
```

#### Graceful Shutdown of Spawned Services

Use a cancellation signal (e.g., `tokio_util::sync::CancellationToken` or
`tokio::sync::watch`) to coordinate shutdown across spawned tasks. Each task
selects on both its work and the shutdown signal.

```rust
async fn run_listener(
    listener: TcpListener,
    cancel: CancellationToken,
) {
    loop {
        tokio::select! {
            result = listener.accept() => {
                let (stream, _addr) = match result {
                    Ok(conn) => conn,
                    Err(e) => {
                        tracing::warn!("Accept error: {e}");
                        continue;
                    }
                };
                let cancel = cancel.clone();
                tokio::spawn(async move {
                    handle_connection(stream, cancel).await;
                });
            }
            _ = cancel.cancelled() => {
                tracing::info!("Listener shutting down");
                break;
            }
        }
    }
}
```

#### Task Panic Propagation

A `JoinError` from awaiting a `JoinHandle` means the task panicked. Always
inspect the result — silently ignoring panicked tasks hides bugs.

```rust
match handle.await {
    Ok(()) => { /* task completed normally */ }
    Err(e) if e.is_panic() => {
        tracing::error!("Task panicked: {e}");
        // Decide: propagate, restart, or degrade
    }
    Err(e) => {
        tracing::warn!("Task cancelled: {e}");
    }
}
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
