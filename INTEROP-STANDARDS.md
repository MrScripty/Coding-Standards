# Interop Standards

Canonical foreign-memory, resource-authority, initialization, callback,
lifetime, and release contracts moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md).

## Boundaries

Foreign-boundary applicability moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md).

## Core Principles

Generic foreign-authority principles moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md).

### 1. Validate at Every Boundary Crossing

Complete authority proof moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#validate-before-access).

### 2. Copy Data Out of Foreign Buffers Immediately

Copy-after-proof requirements moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#copying-is-not-proof).

### 3. Symmetric Init/Shutdown

Initialization, shutdown, and release ownership moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#initialization-and-release).

### 4. Document Thread Requirements

Thread and callback authority moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#thread-and-callback-contract).

### 5. Isolate Unsafe Code to Thin Wrappers

Adapter isolation moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#adapter-isolation).

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

Classify generated sources, public APIs, ABIs, persisted values, and
independently deployed consumers with
[Contract Evolution And Degraded Outcomes](topics/contracts.md). Cross-language
does not by itself require indefinite backward compatibility.

### Rules

1. **Update coordinated repository-owned definitions in the same commit** —
   prevents drift
2. **Add the handler/listener on both sides together** — prevents dead messages
3. **Use shared schema files when possible** — protobuf, JSON Schema, or OpenAPI
   generate types for both sides from a single source of truth
4. **Version or negotiate independently deployed boundaries** — reject
   unsupported versions explicitly instead of guessing a compatible shape

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
4. **Update coordinated sides in the same commit** — independently deployed
   sides follow their version window and negotiation contract

---

## When These Rules Apply

| Boundary Type | Examples | Key Concerns |
|--------------|---------|--------------|
| FFI (same process) | Rust ↔ C, C# P/Invoke | Memory safety, thread affinity |
| IPC (separate process) | WebSocket, stdin/stdout, pipes | Serialization, message validation |
| Plugin/Extension | Dynamically loaded libraries | Init/shutdown lifecycle, versioning |
| Web API | HTTP REST, gRPC | Schema validation, auth |
