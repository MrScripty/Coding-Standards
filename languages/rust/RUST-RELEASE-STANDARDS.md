# Rust Release Standards

Cargo release rules for Rust workspaces. These specialize the generic
[Release Standards](../../RELEASE-STANDARDS.md).

## Toolchain Pinning

Pin the Rust toolchain for reproducible builds:

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.78.0"
components = ["rustfmt", "clippy"]
```

Application repositories and production workspaces should commit `Cargo.lock`.
Published library crates may omit `Cargo.lock` when they intentionally allow
consumer resolution, but CI must still test a resolved dependency graph.

## Cargo.toml Metadata

Publishable crates should have complete metadata:

```toml
[package]
name = "my-library"
version = "0.1.0"
edition = "2021"
rust-version = "1.78"
description = "Brief description of what the crate does"
license = "MIT"
repository = "https://github.com/org/repo"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["category"]
```

Rules:

- Set `rust-version` to the minimum supported Rust version for published
  libraries and reusable workspace crates.
- Keep package metadata accurate before publishing or cutting release artifacts.
- Avoid using the crate name as the product name when the release artifact is a
  generated binding, native library, or host-language package.

## Publish Control

Crates that should never be published to crates.io must set:

```toml
[package]
publish = false
```

Use `publish = false` for:

- binary-only crates
- `cdylib` crates for specific runtimes
- internal tooling
- test harness crates
- workspace-only integration crates

## Workspace Version Management

Use `[workspace.package]` to define shared version metadata once:

```toml
# Workspace root Cargo.toml
[workspace.package]
version = "0.2.0"
edition = "2021"
rust-version = "1.78"
license = "MIT"
repository = "https://github.com/org/repo"

# Member crate Cargo.toml
[package]
version.workspace = true
edition.workspace = true
rust-version.workspace = true
license.workspace = true
repository.workspace = true
```

Do not force shared versions across unrelated crates only because they live in
one workspace. Shared versions are appropriate when crates ship as one product
or must remain version-matched.

## cargo-release

For automating version bumps, tag creation, and optional crates.io publishing,
`cargo-release` is recommended once release cadence stabilizes:

```toml
# release.toml (workspace root)
[workspace]
shared-version = true
consolidate-commits = true
tag-prefix = "v"

[[pre-release-replacements]]
file = "CHANGELOG.md"
search = "## \\[Unreleased\\]"
replace = "## [Unreleased]\n\n## [{{version}}] - {{date}}"
```

`cargo-release` is optional for first releases. Manual release steps are
acceptable if they are documented and repeatable.

## Rust Release Checklist

Before every Rust release:

1. `cargo fmt --all -- --check` passes.
2. `cargo clippy --workspace --all-targets --all-features -- -D warnings`
   passes.
3. `cargo test --workspace` and `cargo test --workspace --doc` pass.
4. Public feature checks pass: `cargo check --workspace --all-features` and
   `cargo check --workspace --no-default-features`.
5. Dependency audit passes according to
   [RUST-DEPENDENCY-STANDARDS.md](RUST-DEPENDENCY-STANDARDS.md#auditing).
6. Criterion benchmarks are updated when the release includes performance claims
   or performance-sensitive changes.
7. `Cargo.toml` metadata, `CHANGELOG.md`, tags, and artifact names agree.
