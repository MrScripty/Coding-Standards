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
