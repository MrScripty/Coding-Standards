# Rust Language Bindings Standards

Architecture patterns for generating and maintaining language bindings from a
single core library. For low-level FFI safety rules (boundary validation, buffer
copying, unsafe isolation), see [RUST-INTEROP-STANDARDS.md](RUST-INTEROP-STANDARDS.md).
For platform-specific build concerns (library naming, CI matrix), see
[RUST-CROSS-PLATFORM-STANDARDS.md](RUST-CROSS-PLATFORM-STANDARDS.md).
For generated, public, ABI, persisted, and independently deployed compatibility
decisions, see
[Contract Evolution And Degraded Outcomes](../../topics/contracts.md).

## Three-Layer Architecture

Canonical core/adapter dependency direction, annotation placement, generated-
code ownership, and framework-free core verification moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#core-and-adapter-boundary).

The workspace material below remains migration reference for undisposed
packaging and repository-layout sections. It cannot override the canonical
core/adapter boundary.

### Workspace Layout

Canonical package/workspace placement and required native/host evidence moved
to [Package And Workspace Placement](../../profiles/languages/rust/language-bindings.md#package-and-workspace-placement).
No crate tree, generated-output directory, script name, workspace membership,
or default-member list is universal. Separately provisioned foreign-runtime
evidence remains required when selected by the binding contract.

---

## Product-Native Artifact Model

Canonical binding artifact roles, release composition, identity, relationships,
consumer information, and evidence moved to
[Binding Artifact Roles And Composition](../../workflows/release.md#binding-artifact-roles-and-composition).
Artifact counts, target coverage, separate packages, bundles, framework names,
and archive names are not universal release defaults.

### Compatibility Notes

Canonical per-artifact compatibility classes, replacement windows, generated
consistency, version relationships, and typed outcomes moved to
[Cross-Language Contract Selection](../../topics/contracts.md#cross-language-contract-selection).
Common build or release provenance does not impose one compatibility promise
or lockstep versioning across binding artifacts.

---

## Binding Surface Policy

Canonical consumer selection, host-language subsets, semantic ownership,
support and publication status, documentation, compatibility, and evidence
moved to the generic
[Exported Surface Contract](../../profiles/boundaries/language-bindings.md#exported-surface-contract).
Rust does not define a universal support-tier vocabulary, language-parity
policy, or automatic export set.

---

## FFI Wrapper Design

Canonical Rust representation and conversion rules moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md).

### Wrapper Type Conventions

When a selected binding mechanism cannot represent a core type directly, its
adapter defines an explicit boundary representation and a checked conversion.

```rust
// BAD: Exposing non-FFI-safe types directly
#[uniffi::Record]
pub struct ModelRecord {
    pub hashes: HashMap<String, String>,  // HashMap not FFI-safe
    pub metadata: serde_json::Value,       // Arbitrary JSON not FFI-safe
    pub total_count: usize,                // Platform-dependent size
}

// GOOD: Wrapper with flattened types
#[derive(uniffi::Record)]
pub struct FfiModelRecord {
    pub hashes: Vec<FfiHashEntry>,     // HashMap → Vec of key-value pairs
    pub metadata_json: String,          // serde_json::Value → JSON string
    pub total_count: u64,               // usize → u64
}

#[derive(uniffi::Record)]
pub struct FfiHashEntry {
    pub key: String,
    pub value: String,
}
```

The selected framework or ABI defines which adapter representations are
supported. Narrowing integers, paths, durations, enums, and serialization use
fallible conversion whenever the target can reject.

### When to Annotate Core Types Directly

Types may be annotated for a named binding framework only when that framework's
contract supports the complete representation. Framework support does not
establish stable C-ABI layout.

```rust
// Core library — annotation only active with "uniffi" feature
#[derive(Debug, Clone, Serialize, Deserialize)]
#[cfg_attr(feature = "uniffi", derive(uniffi::Record))]
pub struct DownloadOption {
    pub quant: String,
    pub size_bytes: Option<u64>,
}
```

Keep framework annotations out of core when they would couple domain behavior
to a binding mechanism. Otherwise, use a dedicated adapter representation.

### From/Into Implementation Pattern

Use `From` only for genuinely infallible conversions. Use `TryFrom`, `TryInto`,
or an explicit fallible constructor when any value, schema, range, path, or
host representation can be rejected.

---

## Error Handling Across FFI

Rust-to-host error representation and diagnostic preservation moved to
[Host Error Representation](../../profiles/languages/rust/language-bindings.md#host-error-representation).

### Rules

The selected host contract, not one universal enum or framework recipe,
defines categories, fields, cancellation, context, and conversion outcomes.

---

## Host-Language Callbacks and Event Delivery

Rust-to-host event-delivery adaptation moved to
[Host Event Delivery](../../profiles/languages/rust/language-bindings.md#host-event-delivery).

### Event Sink Bridges

The selected host contract owns delivery mode, representation, ordering,
capacity, overflow, callback authority, failure, cancellation, and shutdown.
An unavailable selected mode returns its typed diagnostic rather than changing
delivery mechanisms.

### Callback-Based Task Execution

Rust-to-host callback-task adaptation moved to
[Host Callback Task Adaptation](../../profiles/languages/rust/language-bindings.md#host-callback-task-adaptation).

The selected task contract owns representation, callback authority,
correlation, completion, cancellation, and lifecycle outcomes. Missing
capability returns its typed diagnostic rather than installing a no-op or
polling substitute.

### Composite Executors

Canonical composite-executor routing and typed outcome preservation moved to
the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#explicit-executor-delegation).

Delegation is valid only for the exact typed unsupported outcome assigned by
the contract. It is not a catch-all recovery path.

---

## Code Generation Strategy

Canonical generation authority, generator capability, deterministic derivation,
and producer/consumer consistency moved to
[Cross-Language Contract Selection](../../topics/contracts.md#cross-language-contract-selection).
Compiled artifacts, Rust annotations, framework inputs, and generated consumer
output do not become canonical authority by default.

### Annotation Approach

Canonical Rust annotation placement moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#core-and-adapter-boundary).
Place a binding annotation on an adapter only when the selected binding
mechanism and adapter ownership require it. Do not prefer proc macros, a
separate authority file, a framework, or a target language by default.

### Generation Commands

Binding build and generation procedures moved to
[Binding Generation Procedures](../../workflows/release.md#binding-generation-procedures).
The release artifact plan selects the applicable authority, generator,
toolchain, targets, outputs, reproducibility controls, and evidence. Rust does
not prescribe a package, binary, output path, framework, language, or command.
Missing or contradictory procedure facts return a typed release-procedure
diagnostic rather than a guessed command or alternate generator.

---

## Build System Organization

### Feature Flags for Optional Binding Support

Canonical binding dependency and optional-feature placement moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#core-and-adapter-boundary).

Binding-framework dependencies remain adapter/package scoped. A disabled
default does not make a framework dependency in the core independent.

### cdylib Configuration

The FFI wrapper crate must produce a C-compatible dynamic library:

```toml
# mylib-uniffi/Cargo.toml
[lib]
crate-type = ["cdylib", "lib"]
```

- `cdylib` produces the shared library for foreign languages.
- `lib` allows the crate to be used as a Rust dependency in tests and the
  bindgen binary.
- Crates that need foreign runtimes to test (Rustler) should be excluded from
  `default-members` so `cargo test` works without those runtimes installed.

See [RUST-CROSS-PLATFORM-STANDARDS.md](RUST-CROSS-PLATFORM-STANDARDS.md) for
platform-specific library naming (`.so`, `.dll`, `.dylib`).

---

## Type Mapping Rules

Canonical Rust type classification moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#representation-categories).

### FFI-Safe Type Inventory

Do not maintain a universal FFI-safe inventory for native Rust types.
`String`, `Vec<T>`, `Option<T>`, Rust enums, and framework objects may be
liftable by a named framework while remaining invalid as native C-ABI values.
Fixed-width scalars are C-ABI candidates only with an explicit ABI contract.

### Conversion Strategy Decision Matrix

Select framework lifting, schema-governed serialization, a stable ABI value, or
an opaque handle from the concrete boundary contract. Do not switch mechanisms
after conversion failure.

### Enum Representation

Canonical enum representation moved to
[Enum Representation](../../profiles/languages/rust/language-bindings.md#enum-representation).

The selected framework, wire, ABI, opaque-handle, or generated-wrapper contract
defines variant, discriminant, payload, and unknown-value behavior.

---

## Memory Ownership Model

Canonical host-handle lifetime, runtime adaptation, and request-state ownership
moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#handle-and-runtime-adaptation).

Raw foreign-memory authority remains governed by the
[Rust Interop Profile](../../profiles/languages/rust/interop.md). A host handle
or binding resource does not own the selected runtime merely because it uses
that runtime.

---

## Async Bridging

Canonical host-async and runtime-capability adaptation moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#handle-and-runtime-adaptation).

Runtime construction, tracked work, cancellation, shutdown, and blocking
isolation remain governed by the
[Rust Async Profile](../../profiles/languages/rust/async.md). A binding adapter
consumes those capabilities without creating or synchronously driving another
runtime.

---

## Testing Strategy

Canonical conversion-test requirements moved to the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md#verification).

Test at three levels, matching the three-layer architecture:

```text
┌─────────────────────────────────────────────┐
│  Layer 3: Per-Language Integration Tests     │
│  Verify: API works end-to-end in each lang  │
├─────────────────────────────────────────────┤
│  Layer 2: Conversion Tests                  │
│  Verify: From impls, error mapping, types   │
├─────────────────────────────────────────────┤
│  Layer 1: Core Unit Tests                   │
│  Verify: Business logic independent of FFI  │
└─────────────────────────────────────────────┘
```

| Level | What to Test | Runs Without | How to Run |
|-------|-------------|--------------|------------|
| Core unit tests | Business logic, data operations | Any FFI crate | `cargo test -p mylib-core` |
| Conversion tests | Fallible conversion, error mapping, type round-trips | Foreign language runtimes | Project-selected Rust test command |
| Language integration | Full API from Python/C#/etc. | Nothing (needs everything) | pytest, NUnit, XCTest, etc. |

### Rules

1. Every conversion must cover success and each rejection class.
2. Error conversion tests must cover every variant of the core error enum.
3. Core crate tests must pass without any binding features enabled.
4. Crates that need foreign runtimes (Rustler) should be excluded from
   `default-members` so `cargo test` works without those runtimes.

### Conversion Test Example

Test the concrete fallible converter and the real native/host boundary. A
native-only success test does not prove framework lifting, wire compatibility,
generated wrappers, or ABI behavior.

### NIF Pure-Logic Separation

Framework-independent core behavior and separately provisioned adapter/host
evidence are governed by
[Rust core and adapter verification](../../profiles/languages/rust/language-bindings.md#verification).
Rustler/NIF is one possible selected adapter, not the architecture or a
substitute for the required core and real native/host evidence.

See [../../TESTING-STANDARDS.md](../../TESTING-STANDARDS.md) for general test
organization and naming conventions.

---

## Choosing a Binding Approach

Boundary-mechanism selection moved to the
[Language Binding Boundary Profile](../../profiles/boundaries/language-bindings.md#select-the-boundary-mechanism).
Rust adapters apply the selected mechanism through the
[Rust Language Binding Profile](../../profiles/languages/rust/language-bindings.md).
No framework, ABI, serializer, generated wrapper, Tauri bridge, or process
transport is selected from target count or host-language label.

---

## Versioning and Compatibility

Binding artifact classification, regeneration, compatibility, and version
relationships moved to
[Cross-Language Contract Selection](../../topics/contracts.md#cross-language-contract-selection).
Rust binding changes consume those decisions and do not restore blanket
additive compatibility, unconditional regeneration, or lockstep
native-library and host-package versions.

### Version Export

Rust adaptation of a contract-selected discovery or negotiation mechanism
moved to
[Contract Discovery Adaptation](../../profiles/languages/rust/language-bindings.md#contract-discovery-adaptation).
A package-version string or universal `version()` export does not establish
runtime compatibility.
