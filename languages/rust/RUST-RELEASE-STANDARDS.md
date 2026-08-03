# Rust Release Standards

Canonical Rust and Cargo release mechanisms are migrating to the
[Rust Release profile](../../profiles/languages/rust/release.md). Generic
release policy remains with [Release](../../workflows/release.md), and concrete
syntax belongs in the non-normative
[Rust release recipes](../../reference/recipes/rust-release.md). This parent is
a migration route; unmoved sections below retain only their separately tracked
authority.

## Toolchain Pinning

Reproducibility claims and released lockfile ownership are governed by
[Release](../../workflows/release.md#reproducibility). Dependency resolution
and lockfile policy are governed by
[Dependencies](../../topics/dependencies.md#resolution-and-reproducibility),
with Cargo resolver and lockfile mechanisms owned by the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md).
Supported Rust toolchain declaration mechanisms are owned by the
[Rust Release profile](../../profiles/languages/rust/release.md#toolchain-declaration-mechanisms).
Concrete syntax is non-normative in the
[Rust release recipes](../../reference/recipes/rust-release.md#toolchain-declaration-example).

## Cargo.toml Metadata

Artifact identity, version, publication, and consumer promises are owned by
[Release](../../workflows/release.md). Contract identity and compatibility are
owned by [Contracts](../../topics/contracts.md); license and documentation facts
remain with Licensing and Documentation. Supported Cargo package release
metadata mechanisms are owned by the
[Rust Release profile](../../profiles/languages/rust/release.md#cargo-package-release-metadata-mechanisms).
Concrete manifest syntax is non-normative in the
[Rust release recipes](../../reference/recipes/rust-release.md#cargo-package-metadata-example).

## Publish Control

Artifact and publication-channel authority belongs to
[Release](../../workflows/release.md). Supported Cargo publication-control
mechanisms are owned by the
[Rust Release profile](../../profiles/languages/rust/release.md#cargo-publication-control-mechanisms).
Concrete syntax and legacy category examples are non-normative in the
[Rust release recipes](../../reference/recipes/rust-release.md#publication-control-example).

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
