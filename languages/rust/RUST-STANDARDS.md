# Rust Standards

Opinionated Rust standards for modular, maintainable, framework-like Rust
codebases.

This file is an index. Rust-specific requirements are split by concern so each
document can be reviewed and adopted independently.

## Documents

| Document | Purpose | When to Use |
| --- | --- | --- |
| [RUST-API-STANDARDS.md](RUST-API-STANDARDS.md) | Crate roles, public API design, correct-by-construction types, feature contracts, error handling, and documentation | Rust libraries, core crates, workspace architecture, and public APIs |
| [RUST-ASYNC-STANDARDS.md](RUST-ASYNC-STANDARDS.md) | Sync-core/async-shell architecture, Tokio runtime boundaries, blocking work, task lifecycle, mutex selection, and cancellation safety | Rust services, workers, async CLIs, and runtime-integrated crates |
| [RUST-CROSS-PLATFORM-STANDARDS.md](RUST-CROSS-PLATFORM-STANDARDS.md) | Target triples, platform modules, `cfg()` placement, and cross-target verification | Rust crates with OS-specific behavior, native libraries, or cross-platform support |
| [RUST-DEPENDENCY-STANDARDS.md](RUST-DEPENDENCY-STANDARDS.md) | Cargo dependency ownership, workspace dependency inheritance, feature selection, tree inspection, and audits | Rust workspaces, reusable crates, and dependency review |
| [RUST-INTEROP-STANDARDS.md](RUST-INTEROP-STANDARDS.md) | FFI validation, foreign buffer copying, unsafe isolation, callback contracts, and serde wire formats | Rust FFI, IPC DTOs, native bridges, and cross-language contracts |
| [RUST-LANGUAGE-BINDINGS-STANDARDS.md](RUST-LANGUAGE-BINDINGS-STANDARDS.md) | Rust core plus generated host-language binding architecture, wrapper crates, UniFFI, Rustler, and artifact packaging | Rust libraries exported to Python, C#, Kotlin, Swift, Ruby, Go, Elixir, or TypeScript |
| [RUST-RELEASE-STANDARDS.md](RUST-RELEASE-STANDARDS.md) | Toolchain pinning, Cargo metadata, publish control, workspace versioning, and Rust release checklist | Rust release pipelines, published crates, native artifacts, and workspace releases |
| [RUST-SECURITY-STANDARDS.md](RUST-SECURITY-STANDARDS.md) | Path validation, checked arithmetic, bounded queues, listener limits, and Rust panic policy | Rust services, IPC handlers, FFI boundaries, and externally-facing code |
| [RUST-UNSAFE-STANDARDS.md](RUST-UNSAFE-STANDARDS.md) | Default unsafe policy, exception process, safety documentation, feature-gated unsafe paths, and verification matrix | FFI, OS integration, embedded, memory-mapped, no_std, and performance-sensitive crates |
| [RUST-TOOLING-STANDARDS.md](RUST-TOOLING-STANDARDS.md) | Workspace lints, required verification, Criterion benchmark requirements, optional nextest/cargo-hack guidance, build scripts, and no_std checks | Rust workspaces, CI, release pipelines, and performance-sensitive changes |

## Relationship To Generic Standards

These documents specialize, but do not replace, the generic standards:

- [CODING-STANDARDS.md](../../CODING-STANDARDS.md)
- [ARCHITECTURE-PATTERNS.md](../../ARCHITECTURE-PATTERNS.md)
- [CONCURRENCY-STANDARDS.md](../../CONCURRENCY-STANDARDS.md)
- [TESTING-STANDARDS.md](../../TESTING-STANDARDS.md)
- [DEPENDENCY-STANDARDS.md](../../DEPENDENCY-STANDARDS.md)
- [TOOLING-STANDARDS.md](../../TOOLING-STANDARDS.md)
- [INTEROP-STANDARDS.md](../../INTEROP-STANDARDS.md)
- [SECURITY-STANDARDS.md](../../SECURITY-STANDARDS.md)
- [CROSS-PLATFORM-STANDARDS.md](../../CROSS-PLATFORM-STANDARDS.md)
- [RELEASE-STANDARDS.md](../../RELEASE-STANDARDS.md)

When a Rust-specific rule conflicts with a generic example, the Rust-specific
rule wins for Rust crates.

## Default Rust Position

- Use the type system to make expensive bug classes impossible.
- Keep domain/core logic synchronous unless async is genuinely part of the
  operation's contract.
- Deny unsafe code by default at the workspace level, and explicitly relax that
  lint only in crates that own legitimate unsafe boundaries.
- Treat Cargo features as a public contract for libraries.
- Require Criterion for Rust performance claims and performance regression
  protection.
- Prefer standard Cargo verification first; add third-party tools when they
  materially improve confidence or CI ergonomics.
