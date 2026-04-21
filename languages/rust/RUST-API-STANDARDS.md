# Rust API Standards

Crate architecture, API design, error handling, feature contracts, and
correct-by-construction rules for Rust codebases.

## Correct-By-Construction Policy

Use the type system to make invalid states impossible when the bug class is
expensive or crosses a module boundary.

Use stronger type-level guarantees for:

- safety-critical or security-sensitive boundaries
- public APIs consumed across crates or teams
- state machines with three or more meaningful states
- protocol, capability, permission, or lifecycle constraints
- parsed external input that downstream code must trust

Do not overuse type-level machinery for:

- small private helpers with obvious local invariants
- throwaway prototypes
- code where the domain is still being discovered
- trivial formatting or display logic

The decision test is: if this bug ships, how bad is it? Use types for expensive
bugs; use tests and assertions for cheap bugs.

## Parse, Do Not Re-Validate

Raw external input should be parsed once at the boundary into a validated type.
Internal code should accept the validated type, not the raw unchecked value.

```rust
pub struct Port(u16);

#[derive(Debug, thiserror::Error)]
pub enum PortError {
    #[error("port must be non-zero")]
    Zero,
}

impl TryFrom<u16> for Port {
    type Error = PortError;

    fn try_from(value: u16) -> Result<Self, Self::Error> {
        if value == 0 {
            Err(PortError::Zero)
        } else {
            Ok(Self(value))
        }
    }
}

fn start_server(port: Port) {
    // No re-validation needed. The type is the proof.
}
```

Rules:

- Use `TryFrom` for fallible conversion from raw structured data.
- Use `FromStr` for CLI, config, and text boundary parsing.
- Use newtypes for values with domain invariants.
- Prefer enums over stringly typed mode, kind, state, or action fields.
- Replace unclear boolean parameters with named two-variant enums.
- Keep constructors private when callers must go through validation.
- Do not pass raw `String`, `u16`, `usize`, `PathBuf`, or byte slices through
  internal APIs when a domain type would encode required validity.

## Crate Roles

Cargo workspace members should have clear architectural roles.

Common roles:

- `*-core`: domain logic, validated types, pure services, traits
- `*-contracts`: shared wire DTOs, schema types, boundary enums
- `*-adapter` or `*-infra`: persistence, network, OS, hardware, or subprocess
  integration
- `*-bindings`: FFI or host-language wrappers around core
- `*-cli`, `*-server`, `*-app`: composition roots and runtime wiring
- `xtask`: repository-owned automation

Rules:

- Core crates must not depend on app, transport, binding, or framework crates.
- Binding crates wrap core; core must compile and test without binding features.
- App crates compose other crates and own runtime wiring.
- Infrastructure crates may depend on core contracts but should expose narrow
  traits or adapters upward.
- Shared utility crates must stay small and generic. Promote workflow ownership
  into a clearer core or app crate.

## Module Layout

Prefer a crate root that curates the public API with re-exports.

```text
crate_name/
├── Cargo.toml
├── src/
│   ├── lib.rs          # public API and re-exports
│   ├── error.rs        # crate-level error types
│   ├── types.rs        # common domain types
│   ├── feature/
│   │   ├── mod.rs      # feature API
│   │   ├── impl.rs     # implementation details
│   │   └── tests.rs    # unit tests
│   └── platform/
│       ├── mod.rs      # cfg re-exports
│       ├── linux.rs
│       └── windows.rs
├── tests/              # public API integration tests
├── benches/            # Criterion benchmarks
└── examples/           # runnable examples
```

Rules:

- Public types used by most consumers should be re-exported from `lib.rs`.
- Keep implementation modules `pub(crate)` unless they are intentionally part
  of the public contract.
- Use `error.rs` for structured error types when the crate has meaningful
  fallible operations.
- Keep `cfg()` in thin platform modules. Inline `cfg()` is acceptable only for
  small documented exceptions.

## Result, Option, Panic

| Situation | Use |
| --- | --- |
| External input or recoverable failure | `Result<T, E>` |
| Expected absence | `Option<T>` |
| Internal invariant violation | `debug_assert!`, `panic!`, or `unreachable!` |
| Compile-time impossibility | type-state, enum, trait bound, or sealed trait |

Rules:

- Return `Result`, not `panic!`, for fallible public APIs.
- Prefer specific error enums with `thiserror` for libraries and production
  code.
- Reserve `anyhow` for top-level binaries, scripts, tests, or contexts that only
  report errors.
- Avoid `Result<T, String>` in public APIs.
- Add context when adapting lower-level errors into higher-level errors.

## `unwrap` And `expect`

Do not use `unwrap()` or `expect()` in production request paths, lifecycle code,
background services, library APIs, or startup/shutdown flows.

Allowed exceptions:

- tests
- examples where brevity is explicitly acceptable
- prototypes not intended for production
- immediately guarded invariants with a useful `expect` message
- compile-time constants or construction that is truly infallible by design

Prefer `expect("why this cannot fail")` over `unwrap()` when an invariant is
being asserted.

## Public Contract Traits

Rules:

- Implement or derive `Debug` for most public types.
- Implement `Display` for user-facing or error-like types.
- Derive `Clone`, `Copy`, `Eq`, `Ord`, `Hash`, and `Default` only when their
  semantics are correct and cheap enough.
- Use `#[must_use]` on guard types, validated values, builders, and return
  values that are almost certainly bugs when ignored.
- Use `#[non_exhaustive]` on public enums or structs when future extension is
  likely.
- Seal traits that downstream crates should use but not implement.
- Prefer associated types when one implementation has one natural output type.
- Use trait objects only when runtime polymorphism is required; otherwise prefer
  generics for static dispatch.

## Parameter Ergonomics

Rules:

- Accept borrowed data when ownership is not needed: `&str`, `&Path`, `&[u8]`.
- Use `impl AsRef<Path>` or `impl AsRef<str>` for ergonomic read-only APIs.
- Use `impl Into<String>` or `impl Into<PathBuf>` only when the function stores
  or owns the value.
- Use `Cow<'_, T>` when mutation is rare and borrowing is common.
- Avoid accepting `String` when `&str` is sufficient.
- Avoid cloning inputs just to satisfy an API shape.

## Feature Contracts

Cargo features are part of the public contract for libraries and reusable
workspace members.

Rules:

- Keep default features minimal.
- Use `dep:` syntax for optional dependencies to avoid implicit public feature
  names.
- Document all public features in README and crate-level docs.
- Make expensive, platform-specific, unsafe, or binding-specific dependencies
  optional when consumers should not always pay their cost.
- Do not use mutually exclusive features unless unavoidable.
- If mutually exclusive features are unavoidable, enforce conflicts with
  `compile_error!`.
- Public library crates with feature flags must at minimum compile with default,
  all-features, and no-default-features modes.

Required baseline checks for crates with public feature contracts:

```bash
cargo check --workspace --all-features
cargo check --workspace --no-default-features
```

Optional deeper checks with `cargo hack` are covered in
[RUST-TOOLING-STANDARDS.md](RUST-TOOLING-STANDARDS.md#optional-feature-matrix-checks).

## Documentation

Rust crates should document contracts where the compiler cannot fully enforce
intent.

Required documentation:

- crate-level `//!` docs for public library crates
- `# Errors` sections on public fallible functions where behavior is not obvious
- `# Panics` sections on public functions that can panic
- `# Safety` sections on every `unsafe fn` and unsafe-owning module
- feature-flag documentation in README or crate docs
- examples for public APIs that are intended for external users

Do not document obvious implementation mechanics. Document invariants,
contracts, safety obligations, compatibility expectations, and why a design
exists.

