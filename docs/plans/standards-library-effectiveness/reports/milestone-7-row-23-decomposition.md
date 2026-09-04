# Milestone 7 Row 23 Rust Tooling Decomposition

## Owner Contract

`profiles/languages/rust/tooling.md` will be a narrow Rust and Cargo tooling
mechanism specialization. It applies only after Tooling, Verification,
Performance, Dependencies, Security, Implementation, Cross-Platform, Rust API,
Rust Dependency, Rust Unsafe, and other applicable owners accept their
contracts. It may select supported Cargo formatting, lint, test-runner,
feature-matrix, compile-fail, property-test, benchmark, coverage, diagnostic,
and build-script adapter mechanisms.

It does not own claim selection or evidence sufficiency, test design, naming or
placement, lint purpose or severity, tool selection, automation scheduling,
performance claims or thresholds, dependency selection, unsafe policy, target
support, feature contracts, build-script authority, or `no_std` requirements.

The owner requires `core`, `workflow.verification`, `workflow.tooling`, and
`profile.language.rust`. Other generic and Rust owners route conditionally.
Contradictory accepted contracts or mechanisms are `invalid`; a valid contract
with no supported Rust expression is `unsupported`; missing claim, authority,
scope, tool, capability, target, or evidence facts are `unavailable`. Installed
tools, repository size, workspace layout, ecosystem popularity, command
success, and legacy required/optional/recommended labels are not fallbacks.

## Exact Dispositions

`STD-0831` is an index that establishes the useful owner and non-normative
recipe boundary. `STD-0832` through `STD-0838`, `STD-0840`, and `STD-0841`
split generic authority from narrow Rust tooling mechanisms. `STD-0839` refines
Verification's test-design, naming, placement, and regression-record authority.
`STD-0842` splits target and `no_std` authority into Rust Cross-Platform while
preserving Rust API, Dependency, and Tooling routes. Embedded commands,
manifests, dependency versions, thresholds, tables, and code examples are
extracted under each section's single disposition to non-normative Rust tooling
recipes.

## Ordered Children

1. `23.1`: create the Rust Tooling owner, recipe boundary, routes, and parent
   index with `STD-0831`.
2. `23.2`: split `STD-0832` Verification claims from Cargo baseline command
   mechanisms without workspace, CI, all-target, all-feature, warning, doctest,
   or public-feature defaults.
3. `23.3`: split `STD-0833` Tooling lint authority from Cargo workspace lint
   expression without root, lint-set, severity, inheritance, or unsafe defaults.
4. `23.4`: split `STD-0834` Performance and Verification authority from
   Criterion adapter mechanisms without tool, PR, hot-path, budget, input,
   throughput, directory, dependency-version, harness, or CI defaults.
5. `23.5`: split `STD-0835` Tooling, Verification, and Resilience authority
   from supported Rust test-runner adapters without nextest, repository-size,
   timeout, JUnit, partition, doctest, retry, or CI defaults.
6. `23.6`: split `STD-0836` feature-contract and evidence authority from Cargo
   feature-matrix adapters without cargo-hack, crate-category, powerset,
   feature-count, workspace, no-dev-deps, or baseline-command defaults.
7. `23.7a`: split `STD-0837` compile-time rejection contract and evidence
   authority from compile-fail harness mechanisms without trybuild,
   restriction-category, CI, or example defaults.
8. `23.7b`: split `STD-0838` invariant, property, generator, and evidence
   authority from property-test harness mechanisms without proptest,
   invariant-category, parser, state-machine, or example defaults.
9. `23.8`: refine `STD-0839` into Verification and move Rust syntax examples to
   reference without naming, placement, helper, directory, or documentation
   defaults.
10. `23.9`: split `STD-0840` generic owner decisions from a capability-matched
   Rust tool-adapter inventory without required, optional, recommended, tool,
   category, or Miri defaults.
11. `23.10`: split `STD-0841` Build, Contracts, Dependencies, Cross-Platform,
    Security, Release, Tooling, and Verification authority from supported Cargo
    build-script mechanisms without sparing-use, purpose, directive, output,
    compiler, runtime-detection, timestamp, or dependency defaults.
12. `23.11`: split `STD-0842` target and `no_std` authority into Rust Cross-
    Platform, preserve API, Dependency, and Tooling routes, extract commands,
    then close the legacy source without target, crate-category, feature,
    dependency, host-test, or practical-coverage defaults.

Each child adds focused positive and negative decisions, records exact
dispositions, updates plan and ledger state, and creates one atomic commit.
Shared routing, profile indexes, recipes, dispositions, the legacy source, and
planning artifacts remain serial integration-owner files.

## Child 23.5 Test-Retry Ownership Replan

Tooling owns runner selection, configuration, isolation, partitioning,
reporting, and scheduling. Verification owns test and doctest claims and
evidence sufficiency. Resilience owns retry eligibility, attempt and time
budgets, repeated-execution safety, termination, and recovery outcomes. Rust
Tooling owns only supported Cargo and nextest invocation and result-transport
mechanisms after those contracts are accepted.

Retain one `STD-0835` split disposition. Do not create a flaky-test owner,
silently exclude retries, or let a runner capability select retry policy.

## Child 23.7 Harness Decomposition Replan

`STD-0837` and `STD-0838` retain separate split dispositions and identifier
order but execute as separate atomic children. Compile-fail evidence starts from
Contracts-owned compile-time rejection requirements and Rust API expression.
Property evidence starts from Contracts-owned invariants and Verification-owned
domain, generator, and evidence design. Tooling selects each harness; Rust
Tooling owns only the supported harness adapter mechanisms.

## Child 23.10 Generic Build Owner Replan

The original child named generic build authority that had no canonical owner.
`workflows/build.md` now owns build-time action authorization, inputs, outputs,
consumers, side effects, invalidation, environment access, and deterministic-
build requirements. Contracts, Dependencies, Cross-Platform, Security, Release,
Tooling, and Verification retain their narrower authority. Rust Tooling owns
only supported Cargo and `build.rs` expression mechanisms after all applicable
contracts are accepted.

Create and verify Build as a useful generic owner before moving `STD-0841`.
Retain one `STD-0841` split disposition and do not transfer build policy into a
language profile.

## Re-plan Triggers

Stop if Rust Tooling must select generic policy; test style or `no_std` must be
owned by the new profile; a product, command, manifest, threshold, tool table,
or code example must remain normative; one identifier needs multiple
dispositions; a dependency cycle appears; or legacy closure retains authority.
