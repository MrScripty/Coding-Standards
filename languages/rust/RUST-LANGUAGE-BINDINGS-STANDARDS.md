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

- Product-facing naming may differ from the internal wrapper crate name.
- If a native library name or generated package name changes, apply its
  recorded contract class. Coordinated internal artifacts may be replaced
  atomically; independently consumed artifacts follow their published window.
- Binding packages should state whether they are source-only/generated-only or
  whether they intentionally bundle the native product library as a convenience
  artifact.

---

## Binding Surface Policy

Not every internal capability should be exposed through every binding. Treat
the binding surface as a curated client contract, not as an automatic dump of
every technically exportable function or type.

### Rules

1. **Export only client-facing capabilities by default.** A binding surface
   should expose the workflows, sessions, resources, and data types external
   consumers actually need, not every internal helper, debug path, or transport
   shim.
2. **Every exported entry point must map to a documented consumer use case.**
   If no real host-language caller needs a capability, do not export it only
   because the wrapper framework can.
3. **Classify binding APIs by support tier.** At minimum, distinguish
   `supported`, `experimental`, and `internal-only` surfaces. Document which
   tiers are packaged, versioned, and covered by host-language tests.
4. **Do not require identical language parity by default.** Different host
   languages may expose different supported subsets when the product contract
   and documentation make that choice explicit.
5. **Keep canonical semantics out of wrapper-only APIs.** If multiple bindings
   need the same contract shaping, lifecycle rule, or error category, move that
   logic into a backend-owned or binding-neutral layer and keep wrappers thin.
6. **Do not export unstable internal control paths casually.** Admin-only,
   recovery-only, debug-only, or framework-local operations must be explicitly
   justified before they become part of a client binding surface.
7. **New exported surface requires contract documentation.** Document lifecycle
   expectations, error semantics, compatibility promises, and the owning layer
   in the same change that introduces the export.

### Support Tier Guidance

| Tier | Intended Consumer | Packaging Expectation | Verification Expectation |
|------|-------------------|-----------------------|--------------------------|
| `supported` | External production callers | Publish/package deliberately | Native-language tests and host-language tests are both required |
| `experimental` | External evaluators or early adopters | May be packaged with explicit instability note | Native-language tests plus at least one real host-language smoke path |
| `internal-only` | Repo-owned tools or internal harnesses | Not part of the public product contract | Test according to the owning repo/tool needs; do not market as a public binding |

### Surface Review Questions

Before exposing a new binding API, answer:

- Which external caller needs this?
- Is this a product contract or an internal implementation detail?
- Which layer owns the semantics?
- Which host languages actually need this capability?
- What native-language and host-language verification will keep it honest?

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

### Single Source of Truth

Bindings are generated from the compiled core library, never hand-maintained
per language. The annotated Rust code is the single source of truth.

```text
┌──────────────────┐
│  Annotated Rust  │
│  (proc-macros)   │
└────────┬─────────┘
         │ cargo build
┌────────▼─────────┐
│  Compiled cdylib  │
│  (.so/.dll/.dylib)│
└────────┬─────────┘
         │ uniffi-bindgen generate
   ┌─────┼─────┬─────────┐
   ▼     ▼     ▼         ▼
Python  C#   Kotlin    Swift  ...
```

### Annotation Approach

Prefer proc-macro annotations co-located with the implementation over separate
IDL/UDL definition files. This keeps the contract next to the code and
reduces drift.

| Framework | Target Languages | Annotation Style | Async Support |
|-----------|-----------------|-------------------|---------------|
| UniFFI | Python, Kotlin, Swift, Ruby, C#, Go | `#[derive(uniffi::Record)]`, `#[uniffi::export]` | Yes (tokio) |
| Rustler | Elixir/Erlang | `#[rustler::nif]`, `NifStruct`, `NifUnitEnum` | Via dirty schedulers |
| PyO3 | Python only | `#[pyclass]`, `#[pymethods]` | Via pyo3-asyncio |
| cbindgen | C/C++ | None (reads Rust signatures) | No |
| Tauri Commands | TypeScript/JS (desktop) | `#[tauri::command]` | Yes (tokio) |

### Generation Commands

Build the cdylib, then generate per-language bindings from the compiled
artifact:

```bash
# Build the shared library
cargo build -p mylib-uniffi --release

# Generate Python bindings
cargo run -p mylib-uniffi --features cli --bin mylib-uniffi-bindgen -- \
    generate --library --language python \
    --out-dir ./bindings/python target/release/libmylib_uniffi.so

# Generate C# bindings (community bindgen)
uniffi-bindgen-cs --library --config crates/mylib-uniffi/uniffi.toml \
    --out-dir ./bindings/csharp target/release/libmylib_uniffi.so
```

Using a custom bindgen binary (`src/bin/uniffi_bindgen.rs`) instead of a
globally installed tool ensures version consistency across the team:

```rust
fn main() {
    uniffi::uniffi_bindgen_main()
}
```

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
