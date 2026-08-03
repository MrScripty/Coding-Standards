# Rust Release Recipes

**Standards metadata**

- ID: `reference.recipes.rust-release`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A Rust project has accepted a release contract and needs illustrative Cargo, toolchain, manifest, adapter, or command syntax.
- Does not apply when: Selecting a release boundary, artifact, version, dependency policy, lockfile policy, license, documentation, performance claim, tool, procedure, checklist, evidence claim, or supported mechanism.
- Requires: `workflow.release`, `profile.language.rust.release`
- Specializes: `none`
- Verification: Rust release recipe dispositions, links, metadata, and non-authority checks.
- Canonical owner: `reference/recipes/rust-release.md`

This material is non-normative. [Release](../../workflows/release.md) and other
applicable generic owners select policy and claims. The
[Rust Release profile](../../profiles/languages/rust/release.md) selects
supported Rust and Cargo mechanisms after those contracts are accepted.
Examples added during migration cannot select versions, package metadata,
publication, tools, commands, schedules, thresholds, or acceptance.

## Toolchain Declaration Example

One legacy example expressed selected Rust toolchain facts as:

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.78.0"
components = ["rustfmt", "clippy"]
```

The accepted reproducibility and toolchain contracts select channel, version,
components, targets, profile, update behavior, consumers, and evidence. This
example does not require pinning, select listed components, distinguish
applications from libraries, decide lockfile ownership, or prove a
reproducible build.

## Cargo Package Metadata Example

One legacy publishable-package example used:

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

Every value and included field must come from accepted canonical contracts and
the selected registry capability. This example does not define required fields,
versions, licensing, documentation placement, taxonomy, completeness, or a
relationship between crate and product names.

## Publication-Control Example

One legacy example disabled registry publication:

```toml
[package]
publish = false
```

The release and channel contracts decide whether this mechanism is applicable.
The example does not make `publish = false` a default for binaries, `cdylib`
packages, internal tools, test harnesses, integration crates, or workspace-only
packages, and it does not select crates.io or any other channel.

## Workspace Package-Metadata Example

The following manifests illustrate Cargo syntax after Release has selected a
lockstep release unit and the applicable owners have accepted each shared fact:

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

This example does not select a release unit, require shared versions, prescribe
workspace layout, or authorize inheritance of any field. Dependency inheritance
uses the separately owned Rust Dependency mechanisms.

## Cargo-Release Adapter Example

This legacy configuration illustrates syntax only after Release and Tooling
have selected the procedure, tool, operations, and evidence contract:

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

The example does not recommend `cargo-release`, select workspace placement,
require shared versions or consolidated commits, define tags or changelog
policy, establish cadence, or choose automation over a manual procedure.

## Release Evidence Command Examples

The legacy checklist used commands such as:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --workspace --doc
cargo check --workspace --all-features
cargo check --workspace --no-default-features
```

These examples are selected only when their scope and output match accepted
Verification claims. They do not form an every-release checklist or require
workspace scope, all features, warning denial, audits, benchmarks, metadata,
changelog, tags, or artifact-name comparisons.
