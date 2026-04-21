# Rust Dependency Standards

Cargo dependency rules for Rust workspaces. These specialize the generic
[Dependency Standards](../../DEPENDENCY-STANDARDS.md).

## Before Adding A Crate

Check transitive dependency cost before adding a new crate:

```bash
# How many transitive deps does this crate bring?
cargo tree -p <crate> --depth=0 -e normal

# Is it already in the tree as a transitive dep?
cargo tree -i <crate>
```

Rules:

- Prefer `std` when the required behavior is small and well-supported.
- Avoid adding large framework crates for one small utility.
- If a crate adds 100+ transitive dependencies, it must be feature-gated or
  justified in writing.
- Dependencies used by only one workspace member belong in that member, not in
  the root manifest.

## Workspace Dependency Inheritance

All dependencies used by two or more workspace members should be declared in the
root `Cargo.toml` under `[workspace.dependencies]` and referenced with
`{ workspace = true }` in member crates.

```toml
# Cargo.toml (workspace root)
[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }

# member/Cargo.toml
[dependencies]
serde = { workspace = true }
tokio = { workspace = true }
```

Centralized version management is for consistency, not for hiding dependency
ownership. A crate should still declare every dependency it directly uses.

## Feature Selection

Enable only the features the crate actually needs.

```toml
# BAD: Pulling in everything
[dependencies]
tokio = { version = "1", features = ["full"] }
hyper = { version = "1", features = ["full"] }

# GOOD: Only what is used
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "net", "macros"] }
hyper = { version = "1", features = ["client", "http1"] }
```

Heavy optional functionality must be behind explicit Cargo features:

```toml
[features]
default = []
rag = ["dep:lancedb", "dep:arrow-array", "dep:arrow-schema"]
visualization = ["dep:plotters"]
export-pdf = ["dep:printpdf"]

[dependencies]
lancedb = { version = "0.22", optional = true }
arrow-array = { version = "53", optional = true }
arrow-schema = { version = "53", optional = true }
plotters = { version = "0.3", optional = true }
printpdf = { version = "0.7", optional = true }
```

```rust
#[cfg(feature = "visualization")]
pub mod visualization {
    // Only compiled when the consumer opts in.
}
```

For public feature contracts, also follow
[RUST-API-STANDARDS.md](RUST-API-STANDARDS.md#feature-contracts) and
[RUST-TOOLING-STANDARDS.md](RUST-TOOLING-STANDARDS.md#optional-feature-matrix-checks).

## Tree Inspection

Use `cargo tree` before dependency additions, dependency upgrades, and release
audits:

```bash
# Full tree
cargo tree

# Direct deps only
cargo tree --depth 1

# Who depends on a specific crate?
cargo tree -i lancedb

# Total unique deps for one workspace member
cargo tree -p my-crate --prefix none --no-dedupe | sort -u | wc -l

# Find duplicate versions of the same crate
cargo tree --duplicates
```

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
