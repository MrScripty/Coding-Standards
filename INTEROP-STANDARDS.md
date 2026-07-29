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

Complete consumer-side envelope, variant, payload, and metadata decoding before
dispatch moved to
[Decode Before Dispatch](profiles/boundaries/ipc.md#decode-before-dispatch).

---

## Serialization Format Alignment

Canonical wire/schema authority and contract-matched producer/consumer
evidence moved to
[Cross-Language Contract Selection](topics/contracts.md#cross-language-contract-selection).

### Tagged Enum Alignment

Tagged-enum form, keys, payload structure, and consumer evidence moved to
[Serialized Wire Representation](profiles/boundaries/language-bindings.md#serialized-wire-representation).

### Enum Variant Alignment

Variant spelling, values, casing, renames, and unsupported behavior moved to
[Serialized Wire Representation](profiles/boundaries/language-bindings.md#serialized-wire-representation).

### Struct Field Alignment

Field naming, casing, renames, flattening, omission, defaults, and extra-field
policy moved to
[Serialized Wire Representation](profiles/boundaries/language-bindings.md#serialized-wire-representation).

### Rules

Language-specific representation mechanisms remain in the selected Language
Binding profile. Contract selection, version policy, and acceptance evidence
remain in the canonical Contracts owner.

---

## When These Rules Apply

This legacy section is a non-normative routing index. Select every row whose
boundary fact applies; one boundary can require multiple canonical owners.

| Boundary fact | Canonical owner |
| --- | --- |
| Foreign memory, handles, callbacks, initialization, or release | [Interop Boundary Profile](profiles/boundaries/interop.md) |
| Structured messages crossing a process, worker, plugin-host, or deployment boundary | [IPC Boundary Profile](profiles/boundaries/ipc.md) |
| Cross-language lifting, serialization, ABI values, opaque handles, or generated wrappers | [Language Binding Boundary Profile](profiles/boundaries/language-bindings.md) |
| Contract class, schema authority, versioning, migration, or degraded outcome | [Contracts](topics/contracts.md) |
| Untrusted input authorizing work, resource access, or side effects | [Security](topics/security.md) |

The canonical owners define applicability, behavior, diagnostics, and
verification. This index defines none of them.
