# Rust Tooling Recipes

**Standards metadata**

- ID: `reference.recipes.rust-tooling`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: Accepted Rust tooling and verification contracts need illustrative Cargo commands, manifests, configurations, or Rust test and benchmark syntax.
- Does not apply when: Selecting claims, tests, lint policy, tools, configuration authority, schedules, performance requirements, dependencies, security requirements, targets, features, mechanisms, or acceptance.
- Requires: `workflow.verification`, `workflow.tooling`, `profile.language.rust.tooling`
- Specializes: `none`
- Verification: Rust tooling recipe dispositions, links, metadata, and non-authority checks.
- Canonical owner: `reference/recipes/rust-tooling.md`

This material is non-normative. Generic owners select policy and claims. The
[Rust Tooling profile](../../profiles/languages/rust/tooling.md) selects
supported Rust and Cargo mechanisms only after those contracts are accepted.
Examples added during migration cannot select tools, commands, configurations,
versions, targets, features, schedules, thresholds, or acceptance.

## Cargo Baseline Command Examples

One legacy baseline listed:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --workspace --doc
cargo check --workspace --all-features
cargo check --workspace --no-default-features
```

These commands are illustrative only after Verification selects matching
claims and scopes. They do not require workspace, local, CI, all-target,
all-feature, warning-denial, doctest, no-default-feature, or public-feature
coverage.

## Cargo Workspace Lint Examples

One legacy configuration used workspace lint tables and member inheritance:

```toml
[workspace.lints.clippy]
dbg_macro = "deny"
todo = "warn"
unwrap_used = "warn"
large_enum_variant = "warn"

[workspace.lints.rust]
unsafe_code = "deny"
missing_docs = "warn"

[lints]
workspace = true
```

The example does not select root ownership, lint rules, severity, member
inheritance, or unsafe-boundary policy. Those facts must be accepted by Tooling
and Rust Unsafe before Cargo syntax is selected.

## Criterion Benchmark Examples

One legacy setup used a Criterion development dependency, disabled the Cargo
benchmark harness, and registered a benchmark function:

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

This example does not select Criterion, a dependency version, benchmark
trigger, workload, input, throughput report, directory, harness setting,
regression threshold, CI schedule, or noise policy.

## Nextest Command Examples

One legacy example invoked nextest and Cargo doctests separately:

```sh
cargo nextest run --workspace
cargo test --workspace --doc
```

These commands do not select nextest, workspace scope, CI execution, timeout,
JUnit output, isolation, partitioning, retries, or doctest claims.

## Cargo Feature-Matrix Command Examples

Legacy examples included:

```sh
cargo hack check --each-feature --workspace --no-dev-deps
cargo hack check --feature-powerset -p my-core-crate
cargo check --workspace --all-features
cargo check --workspace --no-default-features
```

These commands do not select cargo-hack, each-feature or powerset coverage,
feature-count thresholds, package or workspace scope, dependency exclusions,
baseline commands, target support, or evidence claims.

## Compile-Fail Harness Examples

Legacy guidance listed single-use tokens, capability tokens, typestate,
dimensional types, sealed traits, and non-exhaustive matching as possible
compile-time rejection claims. These categories are illustrative only. They do
not select trybuild, a fixture layout, expected diagnostics, CI execution, or a
compile-fail claim.

## Property-Test Harness Examples

One legacy example used `proptest!` with generated graph and edge values and
asserted that a successful edge insertion preserved acyclicity. Legacy
categories also mentioned validated types, serialization and parser
roundtrips, state machines, ordering, deduplication, and normalization.

These examples do not select proptest, a property, input domain, generator,
strategy, oracle, seed, shrink behavior, case count, or CI schedule.

## Rust Test-Style Examples

Legacy guidance used `condition_expected_behavior` and
`operation_condition_expected_behavior` names, colocated `#[cfg(test)]` units,
`tests/` for public or cross-crate behavior, `benches/` for Criterion, and
builders or fixture helpers for verbose setup. It also suggested recording an
issue, invariant, or production symptom for regressions.

These are illustrative Rust forms only. They do not select naming vocabulary,
placement, helper type, directory, colocation, benchmark location, or durable
documentation content.
