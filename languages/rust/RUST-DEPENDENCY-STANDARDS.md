# Rust Dependency Standards

Canonical Rust and Cargo dependency mechanisms are migrating to the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md).
Generic dependency policy remains with
[Dependencies](../../topics/dependencies.md). This parent is a non-normative
migration route; unmoved sections below retain only their separately tracked
authority.

## Before Adding A Crate

Candidate selection policy is owned by
[Dependencies](../../topics/dependencies.md#candidate-selection). Supported
Cargo inspection mechanisms are owned by the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md#candidate-inspection-mechanisms).
Concrete commands are non-normative examples in the
[Rust dependency recipes](../../reference/recipes/rust-dependencies.md#candidate-inspection-examples).

## Workspace Dependency Inheritance

Dependency ownership is defined by
[Dependencies](../../topics/dependencies.md#requirement-and-ownership). Cargo
workspace inheritance expression is owned by the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md#workspace-inheritance-mechanisms).
Concrete manifests are non-normative examples in the
[Rust dependency recipes](../../reference/recipes/rust-dependencies.md#workspace-inheritance-examples).

## Feature Selection

Generic feature policy is owned by
[Dependencies](../../topics/dependencies.md#features-and-footprint), with
consumer and evidence obligations in their applicable canonical owners. Cargo
manifest dependency feature mechanisms are owned by the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md#cargo-manifest-dependency-feature-mechanisms).
Rust source and public API feature mechanisms are owned by the
[Rust API profile](../../profiles/languages/rust/api.md#rust-source-feature-expression-mechanisms).
Concrete examples are non-normative in the
[Rust dependency recipes](../../reference/recipes/rust-dependencies.md#dependency-feature-examples).

## Tree Inspection

Dependency graph claims and evidence requirements are selected by
[Dependencies](../../topics/dependencies.md) and
[Verification](../../workflows/verification.md). Supported Cargo graph-query
mechanisms are owned by the
[Rust Dependency profile](../../profiles/languages/rust/dependencies.md#candidate-inspection-mechanisms).
Concrete commands are non-normative in the
[Rust dependency recipes](../../reference/recipes/rust-dependencies.md#dependency-graph-inspection-examples).

## Auditing

Recommended Rust dependency checks:

| Check | Tool | Baseline Command |
| --- | --- | --- |
| Security advisories | `cargo audit` | `cargo audit` |
| Licenses, duplicate bans, sources, advisories | `cargo deny` | `cargo deny check` |
| Unused dependencies, fast heuristic | `cargo machete` | `cargo machete --with-metadata` |
| Unused dependencies, precise nightly check | `cargo udeps` | `cargo +nightly udeps` |
| Duplicate versions | Cargo | `cargo tree --duplicates` |

`cargo machete` is fast enough for most PR workflows. `cargo udeps` is more
precise but requires nightly, so treat it as an optional deeper audit unless the
repository explicitly adopts it.

Manual usage checks are still useful when tools are inconclusive:

```bash
# Replace <crate> and <path> with the dependency and source directory.
rg "use <crate>|<crate>::" <path>/src
```

Watch for masking: a local `mod foo` can shadow an external crate `foo`. If
source contains `use foo::` and also declares `mod foo;`, the external crate may
not actually be in use.

## Build-Time Cost

Measure heavy dependencies instead of guessing:

```bash
# Build timing per crate
cargo build --timings

# Count transitive deps per workspace member
cargo tree -p <crate> --prefix none --no-dedupe | sort -u | wc -l
```

If a dependency accounts for more than 20% of total compile time, investigate
lighter alternatives, feature reductions, or moving it to a leaf crate.
