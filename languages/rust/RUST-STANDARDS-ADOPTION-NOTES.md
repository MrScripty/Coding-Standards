# Rust Standards Adoption Notes

Current adoption notes for the Rust standards split.

## Decisions

- Rust standards are split by concern instead of kept in one large file.
- `unsafe_code = "deny"` is the workspace default.
- Crates that legitimately own unsafe boundaries may explicitly relax
  `unsafe_code` to `warn` with documentation and verification.
- `cargo nextest` is optional because it is not part of the official Rust/Cargo
  toolchain.
- `cargo hack` is optional and should be used selectively because exhaustive
  feature combinations can become expensive.
- Criterion is required for Rust performance claims and performance regression
  protection.

## Current File Set

| File | Role |
| --- | --- |
| [RUST-STANDARDS.md](RUST-STANDARDS.md) | Rust standards index |
| [RUST-API-STANDARDS.md](RUST-API-STANDARDS.md) | Crate roles, API design, errors, traits, feature contracts, and documentation |
| [RUST-ASYNC-STANDARDS.md](RUST-ASYNC-STANDARDS.md) | Sync-core/async-shell, runtime boundaries, blocking work, mutexes, and cancellation |
| [RUST-CROSS-PLATFORM-STANDARDS.md](RUST-CROSS-PLATFORM-STANDARDS.md) | Target triples, platform modules, `cfg()` placement, and cross-target checks |
| [RUST-DEPENDENCY-STANDARDS.md](RUST-DEPENDENCY-STANDARDS.md) | Cargo dependency ownership, feature selection, tree inspection, and audits |
| [RUST-INTEROP-STANDARDS.md](RUST-INTEROP-STANDARDS.md) | FFI validation, foreign buffers, unsafe isolation, callback contracts, and serde wire formats |
| [RUST-LANGUAGE-BINDINGS-STANDARDS.md](RUST-LANGUAGE-BINDINGS-STANDARDS.md) | Rust core plus generated host-language binding architecture |
| [RUST-RELEASE-STANDARDS.md](RUST-RELEASE-STANDARDS.md) | Toolchain pinning, Cargo metadata, publish control, workspace versioning, and release checks |
| [RUST-SECURITY-STANDARDS.md](RUST-SECURITY-STANDARDS.md) | Path validation, checked arithmetic, bounded queues, listener limits, and panic policy |
| [RUST-TOOLING-STANDARDS.md](RUST-TOOLING-STANDARDS.md) | Lints, baseline verification, Criterion, optional nextest/cargo-hack, `trybuild`, and `no_std` |
| [RUST-UNSAFE-STANDARDS.md](RUST-UNSAFE-STANDARDS.md) | Unsafe policy, exceptions, safety documentation, verification, and review requirements |

## Integration Policy

Root standards should stay language-agnostic where possible. If a rule depends
on Cargo, Rust syntax, Tokio, serde, unsafe Rust, or Rust-specific verification
tools, it belongs in this directory and should be linked from the generic
standard.

Generic standards may still include Rust in multi-ecosystem tables when the row
is comparative rather than instructional. Detailed commands, code examples, and
tool-specific policy should live in the Rust files above.

## Review Checklist

- Root standards link to Rust standards instead of embedding Rust-only sections.
- Active relative Markdown links resolve from their current file locations.
- New Rust-specific standards are listed in [RUST-STANDARDS.md](RUST-STANDARDS.md).
- Top-level discoverability is provided through [../../README.md](../../README.md)
  and [../README.md](../README.md).
- Rust-specific recommendations do not weaken the generic standards; they add
  stricter Rust defaults where the toolchain supports them.
