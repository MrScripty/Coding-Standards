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

Provider-governed registration, callback delivery, unregistration, release,
and shutdown requirements moved to the
[Interop Boundary Profile](profiles/boundaries/interop.md#event-registration-lifecycle).

---

## Cross-Language Contract Maintenance

Cross-language contract classification, canonical wire/schema authority,
consumer update policy, and evidence moved to
[Cross-Language Contract Selection](topics/contracts.md#cross-language-contract-selection).

### Rules

Select evolution and compatibility behavior from the canonical Contracts
owner. Do not infer it from the number of implementation languages.

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

Canonical wire/schema authority and contract-matched producer/consumer
evidence moved to
[Cross-Language Contract Selection](topics/contracts.md#cross-language-contract-selection).

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

Language-specific representation mechanisms remain in the selected Language
Binding profile. Contract selection, version policy, and acceptance evidence
remain in the canonical Contracts owner.

---

## When These Rules Apply

| Boundary Type | Examples | Key Concerns |
|--------------|---------|--------------|
| FFI (same process) | Rust ↔ C, C# P/Invoke | Memory safety, thread affinity |
| IPC (separate process) | WebSocket, stdin/stdout, pipes | Serialization, message validation |
| Plugin/Extension | Dynamically loaded libraries | Init/shutdown lifecycle, versioning |
| Web API | HTTP REST, gRPC | Schema validation, auth |
