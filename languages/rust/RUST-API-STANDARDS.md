# Rust API Standards

Canonical Rust API mechanisms are migrating to the
[Rust API profile](../../profiles/languages/rust/api.md). Generic contracts
remain with their routed owners. This legacy file retains authority only for
sections not yet moved.

## Correct-By-Construction Policy

Canonical invariant authority belongs to
[Contracts](../../topics/contracts.md#invariant-contracts). Select a Rust
proof-bearing representation through the
[Rust API profile](../../profiles/languages/rust/api.md#validated-type-and-conversion-mechanisms).
This legacy route defines no bug-cost, visibility, state-count, security-label,
type-level-complexity, test, or assertion default.

## Parse, Do Not Re-Validate

Canonical runtime proof and proof lifetime belong to
[Contracts](../../topics/contracts.md#validation-proof-lifetime); untrusted
input authorization belongs to [Security](../../topics/security.md#input-validation-authority).
Select Rust validated types, constructors, and fallible conversions through the
[Rust API profile](../../profiles/languages/rust/api.md#validated-type-and-conversion-mechanisms).
This legacy route defines no parse-once, no-revalidation, `TryFrom`, `FromStr`,
newtype, enum, boolean replacement, private-constructor, primitive-wrapper, or
error-crate default.

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

Select public contract trait mechanisms through the canonical
[Rust API profile](../../profiles/languages/rust/api.md#public-contract-trait-mechanisms).
This legacy route defines no derive, display, result-use, extension, dispatch,
associated-type, generic, sealing, or trait-object default.

## Parameter Ergonomics

Select Rust parameter and ownership mechanisms through the canonical
[Rust API profile](../../profiles/languages/rust/api.md#parameter-and-ownership-mechanisms).
This legacy route defines no borrowing, ownership, conversion-wrapper, `Cow`,
allocation, cloning, primitive, or signature default.

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
