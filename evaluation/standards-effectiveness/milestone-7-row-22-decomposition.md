# Milestone 7 Row 22 Rust Release Decomposition

## Owner Contract

`profiles/languages/rust/release.md` will be a narrow Rust and Cargo release
mechanism specialization. It applies only after Release, Verification,
Contracts, Dependencies, Performance, Tooling, Licensing, Documentation, and
other applicable generic owners accept their contracts. It may select supported
Rust toolchain, Cargo package metadata, publication-control, workspace release
metadata, release-automation adapter, and release-evidence mechanisms.

It does not own release boundaries, artifact identity, version promises,
reproducibility claims, dependency-resolution policy, lockfile ownership,
license selection, documentation requirements, performance claims, tool
selection, automation cadence, checklist claims, or command recipes.

The owner requires `core`, `workflow.verification`, `workflow.release`,
`profile.language.rust`, and `profile.language.rust.dependencies`. Generic
owners route conditionally. Contradictory accepted contracts or mechanisms are
`invalid`; a valid contract with no supported Rust or Cargo expression is
`unsupported`; missing authority, release-unit, consumer, channel, toolchain,
manifest, tool, or evidence facts are `unavailable`. Existing manifests,
installed tools, ecosystem convention, command success, and manual procedure
are not fallbacks.

## Exact Dispositions

`STD-0810` is an index. Six substantive sections split generic authority from
narrow Rust release mechanisms. Four manifest and configuration examples move
to a new non-normative `reference/recipes/rust-release.md`. Examples embedded
inside split sections are extracted under the same single split disposition;
they do not acquire independent normative ownership.

## Ordered Children

1. `22.1`: create the useful Rust Release owner, recipe boundary, and parent
   route with `STD-0810`.
2. `22.2`: preserve reproducibility and lockfile policy in Release and
   Dependencies, preserve Cargo resolver and lockfile mechanisms in Rust
   Dependency, split only Rust toolchain declaration mechanisms from
   `STD-0811`, and move `STD-0812` to reference.
3. `22.3`: split `STD-0813` release, contract, licensing, and documentation
   authority from Cargo package metadata mechanisms while extracting its
   manifest example under the same disposition.
4. `22.4`: split `STD-0814` artifact and publication authority from Cargo
   publication-control mechanisms while extracting its manifest and category
   examples under the same disposition.
5. `22.5`: split `STD-0815` release-unit and version authority from Cargo
   workspace package metadata mechanisms; move `STD-0816` and `STD-0817` to
   reference.
6. `22.6`: split `STD-0818` release-procedure and tool-selection authority from
   supported Rust release-automation adapters; move `STD-0819` to reference.
7. `22.7`: split `STD-0820` release and claim authority from supported Rust
   evidence mechanisms, extract fixed commands to reference under the same
   disposition, then close the legacy source.

Each child adds focused positive and negative decisions, records exact
dispositions, updates plan and ledger state, and creates one atomic commit.
The profile, recipe, legacy source, dispositions, routing, and shared planning
artifacts remain serial integration-owner files.

## Child 22.2 Lockfile Ownership Replan

Release owns the reproducibility claim and applies the accepted released
dependency-resolution contract. Dependencies owns lockfile selection and
resolution policy. Rust Dependency owns Cargo resolver metadata and lockfile
mechanisms. Rust Release owns only Rust toolchain declaration mechanisms.

`STD-0811` retains one split disposition to Rust Release for its toolchain
lineage while its canonical routes preserve the already-owned release,
dependency, and Cargo resolution semantics. No alias, shared lockfile owner, or
context-dependent transfer of mechanism authority is permitted.

## Re-plan Triggers

Stop if the Rust profile must select generic policy; a product, command,
manifest, checklist, threshold, or category example must remain normative; one
identifier needs multiple dispositions; a dependency cycle appears; Rust
Tooling must own release policy; or legacy closure would retain authority.
