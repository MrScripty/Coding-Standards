# Language Bindings Standards

Architecture patterns for generating and maintaining language bindings from a
single core library. For low-level FFI safety rules (boundary validation, buffer
copying, unsafe isolation), see [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md).
For platform-specific build concerns (library naming, CI matrix), see
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md).

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

## FFI Wrapper Design

### Wrapper Type Conventions

When core types contain fields that are not FFI-safe, the wrapper crate defines
parallel types with an `Ffi` prefix and implements `From<CoreType>` for them.

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

| Core Type | FFI-Safe Replacement | Conversion |
|-----------|---------------------|------------|
| `HashMap<K, V>` | `Vec<FfiKeyValuePair>` | Iterate into key-value records |
| `serde_json::Value` | `String` | Serialize to JSON string |
| `usize` / `isize` | `u64` / `i64` | Cast with `as` |
| `PathBuf` | `String` | `.to_string_lossy().into_owned()` |
| `Duration` | `u64` (milliseconds) | `.as_millis() as u64` |
| `(f64, f64)` | Separate `x: f64, y: f64` fields | Destructure tuple |
| Deeply nested structs | `String` (JSON) | `serde_json::to_string()` |

### When to Annotate Core Types Directly

Types that are already FFI-safe can be annotated in the core library using
conditional compilation. This avoids creating redundant wrappers.

```rust
// Core library — annotation only active with "uniffi" feature
#[derive(Debug, Clone, Serialize, Deserialize)]
#[cfg_attr(feature = "uniffi", derive(uniffi::Record))]
pub struct DownloadOption {
    pub quant: String,
    pub size_bytes: Option<u64>,
}
```

| Core Type Characteristics | Strategy |
|--------------------------|----------|
| All fields are primitives, String, Vec, Option | Annotate in core with `cfg_attr` |
| Contains HashMap, serde_json::Value, usize, or PathBuf | Create Ffi* wrapper in FFI crate |
| Stateful object with methods | Wrap as `#[uniffi::Object]` with Arc |
| Deeply nested or recursive | Serialize entire value to JSON String |
| Contains embedded error types | Always create dedicated FFI error enum |

### From/Into Implementation Pattern

Every FFI wrapper type implements `From<CoreType>`. Keep conversions explicit
and one-directional where possible.

```rust
impl From<ModelRecord> for FfiModelRecord {
    fn from(r: ModelRecord) -> Self {
        Self {
            hashes: r.hashes
                .into_iter()
                .map(|(k, v)| FfiHashEntry { key: k, value: v })
                .collect(),
            metadata_json: r.metadata.to_string(),
            total_count: r.total_count as u64,
        }
    }
}
```

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
            Err(_) => self.host.execute_task(node_type, inputs).await,
        }
    }
}
```

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

See [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) for
platform-specific library naming (`.so`, `.dll`, `.dylib`).

---

## Type Mapping Rules

### FFI-Safe Type Inventory

| Type | FFI-Safe? | Notes |
|------|-----------|-------|
| `String` | Yes | UTF-8, heap-allocated |
| `bool` | Yes | |
| `i8` / `i16` / `i32` / `i64` | Yes | Fixed-size integers |
| `u8` / `u16` / `u32` / `u64` | Yes | Fixed-size unsigned |
| `f32` / `f64` | Yes | IEEE 754 |
| `Vec<T>` (T is FFI-safe) | Yes | Serialized as sequence |
| `Option<T>` (T is FFI-safe) | Yes | Nullable in foreign languages |
| `HashMap<K, V>` | **No** | Convert to `Vec<KeyValuePair>` |
| `serde_json::Value` | **No** | Serialize to JSON `String` |
| `usize` / `isize` | **No** | Platform-dependent; use `u64` / `i64` |
| `PathBuf` | **No** | Use `String` |
| `(T, U)` tuples | **No** | Destructure into named fields |
| Enums with complex fields | Conditional | Simple fields OK; embedded errors need wrapping |

### Conversion Strategy Decision Matrix

| Situation | Strategy |
|-----------|----------|
| All fields are FFI-safe | Annotate core type with `cfg_attr` |
| Contains one or two non-FFI-safe fields | Create Ffi* wrapper in FFI crate |
| Deeply nested or recursive structure | Serialize entire value to JSON String |
| Stateful object with methods | Wrap in `Arc<>`, expose as `#[uniffi::Object]` |
| Object shared across NIF calls | Wrap in `ResourceArc<>` with embedded runtime |

### Enum Representation

| Enum Shape | FFI Strategy | UniFFI | Rustler |
|-----------|-------------|--------|---------|
| Unit variants only | Direct mapping | `uniffi::Enum` | `NifUnitEnum` |
| Variants with simple fields | Direct mapping | `uniffi::Enum` | `NifTaggedEnum` |
| Variants with complex fields | FFI-specific enum in wrapper crate | Hand-written | JSON string |

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

See [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md) for the general principle
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

See [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) for general async
patterns and tokio conventions.

---

## Testing Strategy

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
| Conversion tests | From impls, error mapping, type round-trips | Foreign language runtimes | `cargo test -p mylib-uniffi` |
| Language integration | Full API from Python/C#/etc. | Nothing (needs everything) | pytest, NUnit, XCTest, etc. |

### Rules

1. Every `From` impl must have a corresponding test.
2. Error conversion tests must cover every variant of the core error enum.
3. Core crate tests must pass without any binding features enabled.
4. Crates that need foreign runtimes (Rustler) should be excluded from
   `default-members` so `cargo test` works without those runtimes.

### Conversion Test Example

```rust
#[test]
fn test_model_record_conversion() {
    let mut hashes = HashMap::new();
    hashes.insert("sha256".to_string(), "abc123".to_string());

    let record = ModelRecord {
        id: "test".to_string(),
        hashes,
        metadata: serde_json::json!({"key": "value"}),
        total_count: 42,
    };

    let ffi = FfiModelRecord::from(record);
    assert_eq!(ffi.hashes.len(), 1);
    assert_eq!(ffi.hashes[0].key, "sha256");
    assert!(ffi.metadata_json.contains("key"));
    assert_eq!(ffi.total_count, 42);
}
```

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

See [TESTING-STANDARDS.md](TESTING-STANDARDS.md) for general test
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

1. **Additive changes are backward-compatible:** new methods, new record fields
   with defaults, new enum variants.
2. **Removals and renames are breaking:** removing or renaming methods, fields,
   or enum variants requires a major version bump.
3. **Re-generate bindings after every API change** and test all target
   languages before release.
4. **The FFI wrapper crate version should track the core library version.**

### Version Export

Include a `version()` export so foreign code can verify the loaded library
version at runtime:

```rust
#[uniffi::export]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}
```

See [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) for general versioning
and semver conventions.
