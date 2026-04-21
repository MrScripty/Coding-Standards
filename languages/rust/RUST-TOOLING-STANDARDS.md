# Rust Tooling Standards

Rust verification, linting, benchmarks, feature checks, build scripts, and
`no_std` guidance.

## Required Baseline Verification

Every Rust workspace should define local and CI commands that cover:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --workspace --doc
cargo check --workspace --all-features
```

For crates with public feature contracts, also run:

```bash
cargo check --workspace --no-default-features
```

## Workspace Lints

Configure shared lint policy at the workspace root when possible.

```toml
[workspace.lints.clippy]
dbg_macro = "deny"
todo = "warn"
unwrap_used = "warn"
large_enum_variant = "warn"

[workspace.lints.rust]
unsafe_code = "deny"
missing_docs = "warn"
```

Each member crate should opt in:

```toml
[lints]
workspace = true
```

Crates that intentionally own unsafe boundaries may relax `unsafe_code` to
`warn` as described in [RUST-UNSAFE-STANDARDS.md](RUST-UNSAFE-STANDARDS.md).

## Required Criterion Benchmarks

Criterion is required for Rust performance claims and performance regression
protection.

Use Criterion when:

- a PR claims a Rust performance improvement
- a PR changes performance-critical algorithms or hot paths
- a crate has documented latency, throughput, memory, or scaling expectations
- a regression budget is needed for a public API or production path

Rules:

- Do not make performance decisions from ad hoc `Instant::now()` benchmarks.
- Do not use unstable `#[bench]` examples as the project standard.
- Use `black_box` to prevent optimizer removal.
- Benchmark representative input sizes and report throughput when applicable.
- Store benchmarks under `benches/`.
- Keep benchmark fixtures realistic and versioned with the code.
- Gate benchmark comparisons in CI only where noise can be controlled.

Minimal setup:

```toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "critical_path"
harness = false
```

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_critical_path(c: &mut Criterion) {
    c.bench_function("critical path", |b| {
        b.iter(|| run_critical_path(black_box(sample_input())))
    });
}

criterion_group!(benches, bench_critical_path);
criterion_main!(benches);
```

## Optional `cargo nextest`

`cargo nextest` is not part of the official Rust/Cargo toolchain. It is a
third-party Cargo subcommand and should be treated as an optional tooling choice.

Use nextest when it materially improves local or CI feedback:

- large workspaces with many test binaries
- suites that need per-test timeouts
- suites that benefit from JUnit output
- suites that need better process isolation than plain `cargo test`
- CI systems that partition tests across workers

Rules:

- Do not require nextest for small repos that are well served by `cargo test`.
- If nextest is used in CI, still run doctests separately with `cargo test --doc`.
- Configure timeouts deliberately; do not hide slow or deadlocked tests behind
  broad retries.
- Treat retries as a temporary diagnostic aid unless the test is explicitly
  marked as integration-with-external-flake.

Example:

```bash
cargo nextest run --workspace
cargo test --workspace --doc
```

## Optional Feature Matrix Checks

`cargo hack` is optional. Use it when feature interactions are important enough
to justify the extra CI time.

Recommended uses:

- public library crates with multiple feature flags
- `no_std` or `alloc`/`std` split crates
- optional unsafe or platform-specific implementations
- binding crates with feature-gated host integrations
- crates where downstream consumers commonly select minimal features

Do not require exhaustive feature powerset checks by default. Feature powersets
are exponential and become expensive quickly.

Practical optional checks:

```bash
cargo hack check --each-feature --workspace --no-dev-deps
```

Use powerset checks only for small core crates with fewer than eight features:

```bash
cargo hack check --feature-powerset -p my-core-crate
```

Baseline Cargo checks remain required for public feature contracts:

```bash
cargo check --workspace --all-features
cargo check --workspace --no-default-features
```

## Compile-Fail Tests

Use `trybuild` when the API promises compile-time rejection:

- single-use tokens or nonces
- capability tokens
- type-state transitions
- dimensional/unit types
- sealed traits
- non-exhaustive enums requiring wildcard matches

Compile-fail tests should run in CI for crates whose safety or correctness
claims depend on type-level restrictions.

## Property-Based Tests

Use property tests for:

- validated boundary types
- serialization/deserialization round trips
- parser/formatter round trips
- state machine invariants
- graph, ordering, deduplication, or normalization algorithms

For validated boundary types, assert that any value that successfully parses can
be used by all public accessors without panicking.

Example:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn graph_remains_acyclic_after_any_add(
        graph in arbitrary_dag(),
        edge in arbitrary_edge()
    ) {
        let mut graph = graph;
        if graph.try_add_edge(edge).is_ok() {
            prop_assert!(graph.is_acyclic());
        }
    }
}
```

## Rust Test Style

Rules:

- Name tests as `condition_expected_behavior` or
  `operation_condition_expected_behavior`.
- Keep unit tests close to the module with `#[cfg(test)]` when they need private
  access.
- Put public API and cross-crate behavior tests under `tests/`.
- Put Criterion benchmarks under `benches/`.
- Use builders or fixture helpers when setup data would obscure the behavior
  being asserted.
- Document regression tests with the issue, failed invariant, or production
  symptom that made the test necessary.

## Recommended Rust Tools

| Tool | Status | Use |
| --- | --- | --- |
| `cargo fmt` | Required | formatting |
| `cargo clippy` | Required | linting and correctness hints |
| `cargo test` | Required | standard test execution and doctests |
| Criterion | Required for performance claims | statistical benchmarks |
| `cargo nextest` | Optional | faster isolated test execution and CI reporting |
| `cargo hack` | Optional | deeper feature matrix verification |
| `cargo llvm-cov` | Recommended | coverage |
| `cargo audit` | Recommended | vulnerability scanning |
| `cargo deny` | Recommended | license, source, duplicate, and advisory policy |
| `cargo machete` or `cargo udeps` | Recommended | unused dependency detection |
| `cargo tree` | Recommended | dependency graph inspection |
| `cargo expand` | Optional | macro expansion inspection |
| `cargo geiger` | Optional | unsafe usage visibility |
| Miri | Required for pure-Rust unsafe where practical | undefined behavior checks |

## Build Scripts

Use `build.rs` sparingly. Build scripts are part of the supply chain and can
make builds non-reproducible if abused.

Rules:

- Use `build.rs` only for compile-time metadata, generated code, C/C++ build
  integration, system-library probing, or target-specific cfg emission.
- Always emit precise `cargo::rerun-if-changed` or `cargo::rerun-if-env-changed`
  instructions.
- Write generated files to `OUT_DIR`, never to `src/`.
- Use the `cc` crate for C/C++ compilation instead of raw compiler commands.
- Prefer runtime detection over build-time detection for optional hardware or
  environment capabilities.
- Respect `SOURCE_DATE_EPOCH` when embedding timestamps so release builds can be
  reproducible.
- Keep build dependencies minimal and audited.

## `no_std` And Embedded-Compatible Crates

Use `no_std` only when the target requires it or when a core library is intended
to serve both hosted and embedded contexts.

Rules:

- Separate `core`, `alloc`, and `std` functionality behind features.
- Default to `std` for application crates unless there is a clear target need.
- Verify `no_std` compilation with `cargo check --no-default-features` and a
  representative target where practical.
- Ensure dependencies support `default-features = false` before using them in
  `no_std` crates.
- Test `no_std` library logic on the host with `cargo test --lib` when possible.
