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

FFI-specific validation rules depend on the host language and runtime. Rust FFI
validation rules live in
[languages/rust/RUST-INTEROP-STANDARDS.md](languages/rust/RUST-INTEROP-STANDARDS.md#validate-before-unsafe-access).

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

Rust foreign-buffer ownership rules live in
[languages/rust/RUST-INTEROP-STANDARDS.md](languages/rust/RUST-INTEROP-STANDARDS.md#copy-foreign-buffers-immediately).

### 3. Symmetric Init/Shutdown

Every initialization must have a corresponding shutdown. Track initialization
state to prevent double-init or missing shutdown.

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

Rust callback thread contract examples live in
[languages/rust/RUST-INTEROP-STANDARDS.md](languages/rust/RUST-INTEROP-STANDARDS.md#callback-thread-contracts).

```csharp
/// Must be called on the **main thread**.
/// Uses CallDeferred internally to marshal UI operations.
public Task<Response> HandleAsync(Message message) { }
```

### 5. Isolate Unsafe Code to Thin Wrappers

Unsafe operations such as raw pointers and FFI calls should live in small,
focused wrapper modules. Business logic should never contain unsafe boundary
mechanics. Rust-specific unsafe isolation rules live in
[languages/rust/RUST-INTEROP-STANDARDS.md](languages/rust/RUST-INTEROP-STANDARDS.md#unsafe-isolation).

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

Tagged enum serializers produce specific wire shapes. The receiving language
must use the same tag values, payload structure, and casing. Rust serde guidance
lives in
[languages/rust/RUST-INTEROP-STANDARDS.md](languages/rust/RUST-INTEROP-STANDARDS.md#serde-wire-format-alignment).

### Enum Variant Alignment

When enum values are sent as strings, both sides must agree on casing and
format. Check the serializer configuration in the source language before writing
the receiver type.

### Struct Field Alignment

Check serializer configuration on structs or records to determine field name
casing.

### Rules

1. **Check serializer attributes before writing client types** — casing, tags,
   content fields, and explicit renames affect the wire format
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
