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

Feature behavior belongs to [Dependencies](../../topics/dependencies.md),
consumer configurations to Contracts and Library, and target and `no_std`
support to Cross-Platform. Rust manifest and source expression belong to the
Rust Dependency and Rust API profiles. Tool selection and scheduling belong to
[Tooling](../../workflows/tooling.md), and evidence claims belong to
[Verification](../../workflows/verification.md). Supported Cargo feature-
matrix adapters are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#cargo-feature-matrix-adapter-mechanisms).
Commands are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#cargo-feature-matrix-command-examples).

## Compile-Fail Tests

Compile-time rejection contracts belong to
[Contracts](../../topics/contracts.md), Rust source expression belongs to the
[Rust API profile](../../profiles/languages/rust/api.md), harness selection and
scheduling belong to [Tooling](../../workflows/tooling.md), and evidence claims
belong to [Verification](../../workflows/verification.md). Supported compile-
fail harness adapters are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#compile-fail-harness-adapter-mechanisms).
Illustrative categories are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#compile-fail-harness-examples).

## Property-Based Tests

Invariant and domain authority belongs to
[Contracts](../../topics/contracts.md). Property, domain, generator, shrinking,
reproducibility, oracle, and evidence authority belongs to
[Verification](../../workflows/verification.md), while harness selection and
scheduling belongs to [Tooling](../../workflows/tooling.md). Supported Rust
property-test harness adapters are owned by the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#property-test-harness-adapter-mechanisms).
Illustrative categories and syntax are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#property-test-harness-examples).

## Rust Test Style

Test design belongs to [Verification](../../workflows/verification.md#test-design),
data and helper selection to
[Verification](../../workflows/verification.md#test-data-authority-and-lifecycle),
placement and naming to
[Verification](../../workflows/verification.md#test-placement-and-naming), and
durable regression context to
[Verification](../../workflows/verification.md#coverage-and-durable-evidence-records).
Rust-specific syntax and directory examples are non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#rust-test-style-examples).

## Recommended Rust Tools

Tool selection, configuration, scope, and scheduling belongs to
[Tooling](../../workflows/tooling.md), while each claim remains with its generic
owner. Supported general Rust tool adapters belong to the
[Rust Tooling profile](../../profiles/languages/rust/tooling.md#capability-matched-tool-adapters),
dependency and audit adapters to the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md), and
Miri applicability to the
[Rust Unsafe profile](../../profiles/languages/rust/unsafe.md). The legacy
product catalog is non-normative in the
[Rust tooling recipes](../../reference/recipes/rust-tooling.md#rust-tool-catalog-example).

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
