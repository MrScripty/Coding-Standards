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

Separate core logic from binding concerns using three layers:

```text
┌───────────────────────────────────────────────────────────┐
│  Layer 3: Generated / Host Bindings                       │
│  Python, C#, Kotlin, Swift, Ruby, Go, Elixir, TypeScript  │
│  Auto-generated from compiled artifact. Never hand-edit.  │
├───────────────────────────────────────────────────────────┤
│  Layer 2: FFI Wrapper Crate(s)                            │
│  FFI-safe types, error conversion, Arc wrapping,          │
│  event sinks, callback bridges                            │
├───────────────────────────────────────────────────────────┤
│  Layer 1: Core Library                                    │
│  Pure domain logic, idiomatic types, no FFI concerns      │
│  HashMap, serde_json::Value, usize, trait objects          │
└───────────────────────────────────────────────────────────┘
```

| Layer | Contains | Depends On | FFI Awareness |
|-------|----------|------------|---------------|
| Core Library | Domain logic, types, services | Standard library, domain deps | None (optional `cfg_attr` annotations) |
| FFI Wrapper | Ffi* types, From impls, error mapping, event bridges | Core library, binding framework | Full |
| Generated Bindings | Language-specific classes/modules | FFI wrapper (compiled artifact) | N/A (auto-generated) |

### Rules

1. **Core compiles without binding features.** `cargo test -p mylib-core` must
   pass with no binding crate present.
2. **FFI wrapper depends on core; core never depends on FFI wrapper.**
3. **Generated code is never hand-edited.** Re-generate after every API change.
4. **Multiple binding crates can coexist.** A UniFFI crate and a Rustler crate
   can live in the same workspace, each wrapping the same core.

### Workspace Layout

```toml
[workspace]
members = [
    "crates/mylib-core",        # Layer 1: Pure domain logic
    "crates/mylib-uniffi",      # Layer 2: UniFFI wrapper
    "crates/mylib-rustler",     # Layer 2: Rustler NIF wrapper
]
# Exclude crates that need foreign runtimes from default test
default-members = ["crates/mylib-core", "crates/mylib-uniffi"]
```

```text
project-root/
├── crates/
│   ├── mylib-core/               # Layer 1
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   └── tests/
│   ├── mylib-uniffi/             # Layer 2 (UniFFI)
│   │   ├── Cargo.toml
│   │   ├── uniffi.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       └── bin/
│   │           └── uniffi_bindgen.rs
│   └── mylib-rustler/            # Layer 2 (Rustler)
│       ├── Cargo.toml
│       └── src/lib.rs
├── bindings/                     # Layer 3 (generated output)
│   ├── python/
│   ├── csharp/
│   └── kotlin/
└── scripts/
    └── generate-bindings.sh
```

---

## Product-Native Artifact Model

When shipping a library to foreign-language consumers, distinguish three
separate identities:

1. **Product-native shared library** — the platform-specific `.so/.dll/.dylib`
   that contains the product's native implementation for foreign-language
   consumers.
2. **Internal FFI wrapper crate/tooling** — the Rust wrapper crate and binding
   generator configuration used to expose the product over FFI.
3. **Generated host-language binding package** — the language-specific source
   or package consumed by host applications.

The internal FFI mechanism is not the product identity.

### Rules

1. **Ship one product-native shared library per platform target.**
2. **Package generated host-language bindings separately by default.**
3. **Do not name shipped artifacts after the binding framework** (`uniffi`,
   `rustler`, etc.) unless the product itself is the framework.
4. **Binding packages must document which native product library they require.**
5. **Binding packages and native libraries must be version-matched from the
   same build or release.**
6. **If convenience bundles include both the native library and generated
   bindings, treat them as optional secondary artifacts, not the primary
   architecture.**

### Example Release Layout

```text
release/
├── pantograph-headless-native-linux-x64.zip
├── pantograph-headless-native-win-x64.zip
├── pantograph-csharp-bindings.zip
├── pantograph-python-bindings.zip
└── checksums-sha256.txt
```

### Rationale

This keeps the product identity tied to the product, avoids duplicating the
same native library across language packages, and makes it explicit that
generated host bindings are optional layers over a shared native implementation.

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

Errors must be converted at the FFI boundary because core error types embed
non-FFI-safe types (`std::io::Error`, `rusqlite::Error`, `reqwest::Error`).
The conversion is intentionally lossy: source chains are dropped and complex
variants collapse into string messages.

```text
Core Error (rich, nested)           FFI Error (flat, string messages)
┌──────────────────────┐            ┌──────────────────────┐
│ MyLibError           │            │ FfiError             │
│  ├─ Network{msg,src} │ ──From──► │  ├─ Network{message} │
│  ├─ Io{msg,path,src} │            │  ├─ Io{message}     │
│  ├─ Database{msg,src}│            │  ├─ Database{message}│
│  └─ Timeout(Duration)│            │  └─ Timeout{message} │
└──────────────────────┘            └──────────────────────┘
       Typed sources                    String messages only
```

### Rules

1. Define a dedicated FFI error enum in the wrapper crate, not in core.
2. Every variant carries a `message: String` (or is a unit variant like
   `Cancelled`).
3. Implement `From<CoreError> for FfiError` with exhaustive match arms.
4. Collapse multiple core variants into fewer FFI variants when they represent
   the same category to the foreign caller.
5. Never expose `std::io::Error`, `rusqlite::Error`, or any third-party error
   type across FFI.
6. For NIF bindings, use `rustler::Error::Term` with a formatted string.

```rust
// BAD: Passing core error types through FFI
#[uniffi::Error]
pub enum FfiError {
    Io(std::io::Error),  // Not FFI-safe
}

// GOOD: Flatten to string messages
#[derive(Debug, Clone, uniffi::Error, thiserror::Error)]
pub enum FfiError {
    #[error("IO error: {message}")]
    Io { message: String },

    #[error("Network error: {message}")]
    Network { message: String },

    #[error("Cancelled")]
    Cancelled,
}
```

---

## Host-Language Callbacks and Event Delivery

When the core engine produces events or needs the host language to execute
logic, the FFI layer bridges the two sides.

### Event Sink Bridges

Two models for delivering events from core to host languages:

**Selection rule:** Prefer push-based delivery when the host runtime supports it
reliably (native channels/message loops/callback scheduling with clear thread
ownership). Use pull-based delivery as a fallback when push integration is
unsafe or excessively complex for that binding.

**Pull-based (buffered):** Core writes events to an internal buffer. The host
polls via a `drain_events()` method. Best for languages without native
message-passing (Python, C#, Swift).

```rust
struct BufferedEventSink {
    buffer: Arc<RwLock<Vec<FfiWorkflowEvent>>>,
}

impl EventSink for BufferedEventSink {
    fn send(&self, event: WorkflowEvent) -> Result<(), EventError> {
        self.buffer.write().unwrap().push(FfiWorkflowEvent::from(event));
        Ok(())
    }
}

// Host calls this to collect events
#[uniffi::export]
impl FfiEngine {
    pub fn drain_events(&self) -> Vec<FfiWorkflowEvent> {
        self.event_buffer.write().unwrap().drain(..).collect()
    }
}
```

**Push-based (message):** Core sends messages directly to a host-language
process or channel. Best for runtimes with native message-passing (Erlang/BEAM,
Go channels).

```rust
struct BeamEventSink {
    pid: rustler::LocalPid,
    owned_env: Arc<Mutex<OwnedEnv>>,
}

impl EventSink for BeamEventSink {
    fn send(&self, event: WorkflowEvent) -> Result<(), EventError> {
        let json = serde_json::to_string(&event)?;
        let env = self.owned_env.lock().unwrap();
        env.send_and_clear(&self.pid, |new_env| {
            (atoms::workflow_event(), json.encode(new_env)).encode(new_env)
        });
        Ok(())
    }
}
```

| Model | When to Use | Trade-off |
|-------|------------|-----------|
| Pull (buffered) | Python, C#, Swift, Kotlin, Ruby | Simple; host controls polling rate; events may lag |
| Push (message) | Elixir/Erlang, Go | Real-time delivery; requires host concurrency support |

When using pull-based delivery:
- Keep polling at the host/core boundary (not as internal UI-state synchronization loops).
- Bound event-buffer retention and document overflow/drop policy.
- Document expected poll cadence and shutdown cleanup behavior.

### Callback-Based Task Execution

When the host language must execute logic the core cannot (custom node types,
plugins), define a trait in the core and implement it differently per binding:

```rust
// Core library — framework-agnostic trait
#[async_trait::async_trait]
pub trait TaskExecutor: Send + Sync {
    async fn execute_task(
        &self,
        node_type: &str,
        inputs: serde_json::Value,
    ) -> Result<serde_json::Value, EngineError>;
}
```

- **UniFFI:** Implement a `NoopTaskExecutor` that returns an error. The host
  drives execution by polling snapshots and feeding results back.
- **Rustler:** Implement a callback executor that sends a message to the BEAM
  process and awaits a response via a oneshot channel.

### Composite Executors

When both core Rust and the host language handle different subsets of work,
chain executors so core handlers run first and fall through to the host for
unknown types:

```rust
struct CoreFirstExecutor {
    core: Arc<CoreTaskExecutor>,
    host: Arc<dyn TaskExecutor>,
}

#[async_trait::async_trait]
impl TaskExecutor for CoreFirstExecutor {
    async fn execute_task(
        &self,
        node_type: &str,
        inputs: serde_json::Value,
    ) -> Result<serde_json::Value, EngineError> {
        match self.core.execute_task(node_type, inputs.clone()).await {
            Ok(result) => Ok(result),
            Err(EngineError::UnsupportedNodeType { .. }) => {
                self.host.execute_task(node_type, inputs).await
            }
            Err(error) => Err(error),
        }
    }
}
```

Delegate only the explicit unsupported outcome that the composite contract
assigns to the next executor. Validation, execution, cancellation, and resource
errors must remain their original typed failures.

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

Core types that can be annotated directly should use feature-gated annotations.
This keeps binding framework dependencies out of the core crate unless
explicitly requested.

```toml
# mylib-core/Cargo.toml
[features]
default = []
uniffi = ["dep:uniffi"]

[dependencies]
uniffi = { version = "0.28", optional = true }
```

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

Enum conversion rejects variants not represented by the selected host contract.
Serialization is permitted only under an explicit schema.

---

## Memory Ownership Model

The core language owns all allocated memory. Foreign languages hold smart
pointers managed by the binding framework, never raw pointers.

```rust
// BAD: Exposing raw pointer
#[uniffi::export]
fn get_api() -> *const MyApi { /* ... */ }

// GOOD: Arc-wrapped object
#[derive(uniffi::Object)]
pub struct FfiApi {
    inner: Arc<MyApi>,
}

#[uniffi::export]
impl FfiApi {
    #[uniffi::constructor]
    pub async fn new(path: String) -> Result<Arc<Self>, FfiError> {
        let api = MyApi::new(&path).await.map_err(FfiError::from)?;
        Ok(Arc::new(Self { inner: Arc::new(api) }))
    }
}
```

### Rules

1. Objects shared across FFI are wrapped in `Arc<>` (UniFFI) or
   `ResourceArc<>` (Rustler).
2. Foreign code holds a reference-counted handle. When all references drop,
   Rust's `Drop` runs automatically.
3. Records (structs without methods) are value types — data is copied at the
   boundary, not shared.
4. Never expose `Box<T>` or raw pointers across FFI.
5. For NIF resources that need async, embed the tokio runtime inside the
   resource so it outlives individual NIF calls:

```rust
pub struct EngineResource {
    executor: Arc<tokio::sync::RwLock<Engine>>,
    runtime: Arc<tokio::runtime::Runtime>,
}
```

See [RUST-INTEROP-STANDARDS.md](RUST-INTEROP-STANDARDS.md) for the general principle
of copying data out of foreign buffers.

---

## Async Bridging

When the core library uses async (tokio), the FFI layer must bridge async
functions so foreign languages can call them naturally.

**UniFFI:** Annotate the impl block with the async runtime. The framework
generates language-appropriate async APIs (Python `async def`, Kotlin
`suspend fun`, Swift `async`).

```rust
#[uniffi::export(async_runtime = "tokio")]
impl FfiApi {
    pub async fn search(&self, query: String) -> Result<Vec<FfiResult>, FfiError> {
        let result = self.inner.search(&query).await.map_err(FfiError::from)?;
        Ok(result.into_iter().map(FfiResult::from).collect())
    }
}
```

**Rustler:** The BEAM VM must never block on a scheduler thread. Use
`spawn_blocking` or the resource's embedded tokio runtime to run async work
off the BEAM scheduler:

```rust
#[rustler::nif(schedule = "DirtyCpu")]
fn execute(resource: ResourceArc<EngineResource>, node_id: String) -> NifResult<String> {
    resource.runtime.block_on(async {
        let engine = resource.executor.read().await;
        let result = engine.execute(&node_id).await
            .map_err(|e| rustler::Error::Term(Box::new(e.to_string())))?;
        serde_json::to_string(&result)
            .map_err(|e| rustler::Error::Term(Box::new(e.to_string())))
    })
}
```

See [RUST-ASYNC-STANDARDS.md](RUST-ASYNC-STANDARDS.md) for Rust async
patterns and tokio conventions.

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

For Rustler crates, separate pure logic from NIF wrappers so tests run without
the Erlang runtime:

```rust
// Pure logic — testable without NIF runtime
fn parse_model_type_impl(type_str: &str) -> ElixirModelType {
    match type_str.to_lowercase().as_str() {
        "llm" => ElixirModelType::Llm,
        "diffusion" => ElixirModelType::Diffusion,
        _ => ElixirModelType::Unknown,
    }
}

// NIF wrapper — delegates to pure logic
#[rustler::nif]
fn parse_model_type(type_str: String) -> ElixirModelType {
    parse_model_type_impl(&type_str)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_model_type() {
        assert!(matches!(parse_model_type_impl("llm"), ElixirModelType::Llm));
        assert!(matches!(parse_model_type_impl("???"), ElixirModelType::Unknown));
    }
}
```

See [../../TESTING-STANDARDS.md](../../TESTING-STANDARDS.md) for general test
organization and naming conventions.

---

## Choosing a Binding Approach

| Approach | When to Use | Pros | Cons |
|----------|------------|------|------|
| UniFFI | Targeting 3+ languages from Rust | One wrapper serves many targets | Limited to UniFFI-supported types |
| Rustler/NIF | Deep BEAM VM integration (Elixir, Erlang) | Native BEAM types and scheduling | Only targets Erlang ecosystem; NIF crash takes down VM |
| PyO3 | Python-only with tight integration | Full Python ecosystem access | Python-specific |
| Tauri IPC | Desktop app with web frontend | Full async; Serde-native IPC | Desktop-only; requires Tauri runtime |
| Hand-written C FFI | Single target with special ABI needs | Maximum ABI control | High maintenance; manual memory management |
| RPC/IPC (HTTP, gRPC) | In-process linking impractical | Process isolation; language-agnostic | Latency overhead; serialization cost |

### Rules

1. Default to UniFFI when targeting multiple languages from Rust.
2. Use Rustler only for Elixir/Erlang targets.
3. Use Tauri IPC when wrapping for a desktop frontend with TypeScript/JS.
4. Use RPC when the foreign language cannot load native libraries.
5. Never hand-write FFI bindings for more than one target language — use
   code generation.
6. Multiple frameworks can coexist in one workspace as separate crates.

---

## Versioning and Compatibility

### Rules

1. **Classify each boundary independently:** generated source, host package,
   native package, ABI, wire data, and persisted data may have different
   consumers and compatibility windows.
2. **Do not assume additive means compatible:** new enum variants, required
   behavior, defaults, fields, methods, or generated shapes can break exhaustive
   or older host consumers.
3. **Use coordinated replacement only for atomically deployed consumers.**
   Public or independently deployed bindings follow their published versioning
   and negotiation contract.
4. **Re-generate bindings after every API change** and test all supported target
   languages before release.
5. **Version artifacts from one release input without assuming one version
   number gives them one compatibility promise.**

### Version Export

Include a `version()` export so foreign code can verify the loaded library
version at runtime:

```rust
#[uniffi::export]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}
```

See [RUST-DEPENDENCY-STANDARDS.md](RUST-DEPENDENCY-STANDARDS.md) for Rust
dependency versioning and semver conventions.
