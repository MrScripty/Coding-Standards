# Interop Standards

Guidelines for safe communication across language and process boundaries.

## Boundaries

Any place where data crosses between languages, runtimes, or processes is
an interop boundary that requires care:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Frontend   │ ◄──►│  Native Code │ ◄──►│   Backend    │
│  (JS/TS)    │     │  (Rust/C++)  │     │  (C#/Go)     │
└─────────────┘     └──────────────┘     └──────────────┘
   Managed           Unsafe FFI           Managed
   runtime           boundary             runtime
```

Each arrow is a boundary where data must be validated and resources tracked.

## Core Principles

### 1. Validate at Every Boundary Crossing

Data received from another language or process is untrusted. Validate before use.

```rust
// Rust receiving from FFI callback:
fn on_data_received(&self, buffer: *const u8, width: c_int, height: c_int) {
    // Step 1: Null check
    if buffer.is_null() { return; }
    // Step 2: Range check
    if width <= 0 || height <= 0 { return; }
    // Step 3: Overflow check
    let size = (width as usize).checked_mul(height as usize)
        .and_then(|s| s.checked_mul(4))
        .unwrap_or(0);
    if size == 0 { return; }
    // Step 4: Now safe to create slice
    let data = unsafe { std::slice::from_raw_parts(buffer, size) };
}
```

```csharp
// C# receiving deserialized JSON from another process:
var request = JsonSerializer.Deserialize<ProjectRequest>(payload);
if (request == null) return ErrorResponse("Invalid payload");
if (string.IsNullOrWhiteSpace(request.Path))
    return ErrorResponse("Path is required");
// Now safe to use request.Path
```

### 2. Copy Data Out of Foreign Buffers Immediately

Foreign code may free or reuse buffers after the callback returns.
Always copy data into language-owned memory before the callback exits.

```rust
// GOOD: Copy immediately, then work with the copy
let buffer_copy = raw_data.to_vec();  // Owned by Rust now
*shared.buffer.lock() = Some(Arc::new(buffer_copy));

// BAD: Store a pointer/slice to foreign memory
let buffer_ref = raw_data;  // Dangling after callback returns!
```

### 3. Symmetric Init/Shutdown

Every initialization must have a corresponding shutdown. Track initialization
state to prevent double-init or missing shutdown.

```rust
use std::sync::OnceLock;

static INITIALIZED: OnceLock<bool> = OnceLock::new();

fn init_subsystem() {
    INITIALIZED.get_or_init(|| {
        native_lib::initialize(settings);
        true
    });
}

fn shutdown_subsystem() {
    if INITIALIZED.get().is_some() {
        native_lib::shutdown();
    }
}
```

```csharp
// IDisposable for C# resources
public sealed class MessageDispatcher : IDisposable
{
    public void Dispose()
    {
        // Disconnect signals, clear handlers, release references
    }
}
```

### 4. Document Thread Requirements

Every function that crosses a boundary must document which thread it expects
to be called on, and which thread it calls back on.

```rust
/// Called on the **native library's thread** (not the main thread).
/// Buffer is only valid for the duration of this callback.
fn on_data_received(&self, buffer: *const u8, width: c_int, height: c_int) { }
```

```csharp
/// Must be called on the **main thread**.
/// Uses CallDeferred internally to marshal UI operations.
public Task<Response> HandleAsync(Message message) { }
```

### 5. Isolate Unsafe Code to Thin Wrappers

Unsafe operations (raw pointers, FFI calls) should live in small, focused
modules. Business logic should never contain `unsafe` blocks.

```
my_native_binding/
├── ffi_wrapper.rs       ← Contains unsafe (raw pointer access). Thin wrapper.
├── types.rs             ← Pure Rust, no unsafe. Data structures.
├── bridge.rs            ← Safe Rust API over the FFI wrapper.
└── lib.rs               ← Public API, re-exports safe interfaces.
```

### 6. Event Subscription Lifecycle

When subscribing to events/signals across boundaries, always unsubscribe
when the subscriber is destroyed.

```csharp
// Subscribe
_sourceNode.Connect("data_received", Callable.From<string>(OnDataReceived));

// Unsubscribe (in Dispose or cleanup)
if (GodotObject.IsInstanceValid(_sourceNode))
    _sourceNode.Disconnect("data_received", Callable.From<string>(OnDataReceived));
```

```typescript
// Subscribe
eventBus.on('data:updated', handleUpdate);

// Unsubscribe (in cleanup/unmount)
eventBus.off('data:updated', handleUpdate);
```

---

## Cross-Language Contract Maintenance

When message types or API contracts are defined in multiple languages,
they must stay in sync.

### Rules

1. **Define contracts in both languages in the same commit** — prevents drift
2. **Add the handler/listener on both sides together** — prevents dead messages
3. **Use shared schema files when possible** — protobuf, JSON Schema, or OpenAPI
   generate types for both sides from a single source of truth

### Validate Received Messages

Don't trust deserialized messages from other processes. Check required fields:

```typescript
// Receiving from another process:
const parsed = JSON.parse(json);
if (!parsed || typeof parsed.type !== 'string' || typeof parsed.action !== 'string') {
    console.error('Malformed message received');
    return;
}
```

---

## Serialization Format Alignment

When data types are defined in multiple languages and serialized across a
boundary (JSON over HTTP, WebSocket, IPC), the serialization format must
match exactly on both sides.

### Tagged Enum Alignment

Rust's serde tagged enums produce specific JSON shapes. The receiving language
must use the same tag values and casing.

```rust
// Rust (server side)
#[derive(Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ServerEvent {
    TimelineChanged,
    BeatUpdated { clip_id: String },
    GenerationProgress { clip_id: String, token: String },
}
// Serializes to: { "type": "timeline_changed" }
```

```typescript
// TypeScript (client side) — must match the serde output exactly
type ServerMessage =
    | { type: 'timeline_changed' }
    | { type: 'beat_updated'; clip_id: string }
    | { type: 'generation_progress'; clip_id: string; token: string };
```

### Enum Variant Alignment

When enum values are sent as strings, both sides must agree on casing and
format. Check serde's `rename_all` attribute to determine the wire format.

```rust
// Rust: PascalCase variants, no rename_all → wire format is PascalCase
#[derive(Serialize, Deserialize)]
pub enum ArcType { APlot, BPlot, CPlot, Runner }
// Serializes to: "APlot"
```

```typescript
// BAD: Wrong casing — will fail to deserialize
type ArcType = 'a_plot' | 'b_plot' | 'c_plot' | 'runner';

// GOOD: Matches Rust's PascalCase output
type ArcType = 'APlot' | 'BPlot' | 'CPlot' | 'Runner';
```

### Struct Field Alignment

Check serde's `rename_all` on structs to determine field name casing:

```rust
// Rust: rename_all = "snake_case" on the struct
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub struct TimeRange {
    pub start_ms: u64,
    pub end_ms: u64,
}
// Serializes to: { "start_ms": 123, "end_ms": 456 }
```

```typescript
// TypeScript — must use snake_case to match
interface TimeRange {
    start_ms: number;
    end_ms: number;
}
```

### Rules

1. **Check serde attributes before writing client types** — `rename_all`,
   `tag`, `content`, and `rename` all affect the wire format
2. **Test serialization round-trips** — serialize in one language, deserialize
   in the other, and verify the result matches
3. **Use a shared schema when possible** — OpenAPI, JSON Schema, or protobuf
   definitions generate types for both sides from a single source of truth
4. **Update both sides in the same commit** — prevents drift between languages

---

## When These Rules Apply

| Boundary Type | Examples | Key Concerns |
|--------------|---------|--------------|
| FFI (same process) | Rust ↔ C, C# P/Invoke | Memory safety, thread affinity |
| IPC (separate process) | WebSocket, stdin/stdout, pipes | Serialization, message validation |
| Plugin/Extension | Dynamically loaded libraries | Init/shutdown lifecycle, versioning |
| Web API | HTTP REST, gRPC | Schema validation, auth |
