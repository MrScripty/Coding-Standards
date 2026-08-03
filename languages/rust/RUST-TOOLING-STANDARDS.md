# Rust Tooling Standards

Canonical Rust and Cargo tooling mechanisms are migrating to the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md). Generic
tooling policy remains with [Tooling](../../workflows/tooling.md), verification
claims remain with [Verification](../../workflows/verification.md), and concrete
syntax belongs in the non-normative
[Rust tooling recipes](../../reference/recipes/rust-tooling.md). This parent is
a migration route; unmoved sections below retain only their separately tracked
authority.

## Required Baseline Verification

Verification claim and evidence authority belongs to
[Verification](../../workflows/verification.md). Supported Cargo baseline
command mechanisms are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#cargo-baseline-command-mechanisms).
Concrete commands are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#cargo-baseline-command-examples).

## Workspace Lints

Lint policy and orchestration belong to [Tooling](../../workflows/tooling.md),
and unsafe-boundary policy belongs to the
[Rust Unsafe profile](../../profiles/languages/rust/unsafe.md). Supported Cargo
workspace lint-expression mechanisms are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#cargo-workspace-lint-expression-mechanisms).
Concrete manifests are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#cargo-workspace-lint-examples).

## Required Criterion Benchmarks

Performance claim, measurement, workload, budget, variability, benchmark-
design, and regression authority belongs to
[Performance](../../topics/performance.md). Tool selection and configuration
authority belongs to [Tooling](../../workflows/tooling.md), and evidence
sufficiency belongs to [Verification](../../workflows/verification.md).
Supported Criterion adapter mechanisms are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#criterion-benchmark-adapter-mechanisms).
Concrete Cargo and Rust syntax is non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#criterion-benchmark-examples).

## Optional `cargo nextest`

Runner selection, configuration, timeout, isolation, partition, reporting, and
scheduling authority belongs to [Tooling](../../workflows/tooling.md). Test and
doctest claim authority belongs to
[Verification](../../workflows/verification.md). Retry eligibility, budgets,
repeated-execution safety, termination, and recovery authority belongs to
[Resilience](../../topics/resilience.md). Supported Cargo and nextest adapter
mechanisms are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#rust-test-runner-adapter-mechanisms).
Concrete commands are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#nextest-command-examples).

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
