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
