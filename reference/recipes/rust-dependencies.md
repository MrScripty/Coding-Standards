# Rust Dependency Recipes

**Standards metadata**

- ID: `reference.recipes.rust-dependencies`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A Rust project has accepted a dependency inspection contract and needs illustrative Cargo command syntax.
- Does not apply when: Selecting a dependency, tool, threshold, schedule, evidence claim, supported target, feature contract, or resolver policy.
- Requires: `topic.dependencies`, `profile.language.rust.dependencies`
- Specializes: `none`
- Verification: Rust dependency recipe dispositions, links, metadata, and non-authority checks.
- Canonical owner: `reference/recipes/rust-dependencies.md`

This material is non-normative. [Dependencies](../../topics/dependencies.md)
owns candidate selection and evidence requirements. The
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md) owns
supported Cargo mechanisms after those requirements are accepted. Commands
below do not select a candidate, tool, threshold, schedule, or policy.

## Candidate Inspection Examples

One legacy example inspected a package-scoped normal-dependency tree:

```bash
cargo tree -p <crate> --depth=0 -e normal
```

Another inspected reverse-dependency paths:

```bash
cargo tree -i <crate>
```

Placeholders, package scope, depth, dependency kinds, target, features,
resolver, and result interpretation must come from the accepted contract and
supported Cargo capabilities. These commands do not make transitive count,
current graph presence, standard-library availability, framework size, or
written justification a selection rule.

## Workspace Inheritance Examples

An accepted workspace coordination contract might be expressed as:

```toml
[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

An accepted consuming member might inherit those selected facts:

```toml
[dependencies]
serde = { workspace = true }
tokio = { workspace = true }
```

Package names, versions, features, declaration location, and inheritance must
come from canonical ownership and resolution decisions. The examples do not
make member count, root placement, centralization, or inheritance defaults.
