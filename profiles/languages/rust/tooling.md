# Rust Tooling Profile

**Standards metadata**

- ID: `profile.language.rust.tooling`
- Role: `profile`
- Level: `PROFILE`
- Applies when: An accepted claim or tooling contract must be expressed through Rust or Cargo formatting, lint, test, feature-matrix, benchmark, diagnostic, coverage, or build-script adapter mechanisms.
- Does not apply when: No Rust tooling mechanism changes, or the task only selects generic verification, test design, tooling, performance, dependency, security, target, feature, build, or recipe policy.
- Requires: `core`, `workflow.verification`, `workflow.tooling`, `profile.language.rust`
- Specializes: `profile.language.rust`
- Verification: Rust tooling mechanism decisions plus claim-matched adapter, command, configuration, target, and evidence checks selected by generic owners.
- Canonical owner: `profiles/languages/rust/tooling.md`

## Mechanism Authority

Generic owners select claims, evidence sufficiency, test design, lint purpose
and severity, tools, configuration authority, orchestration, scheduling,
performance contracts, dependencies, security requirements, targets, features,
build behavior, and acceptance. This profile selects a supported Rust or Cargo
tooling mechanism only after every applicable contract is accepted.

Applicable mechanisms may include Cargo formatting and lint adapters, test
runners, feature-matrix execution, compile-fail and property-test harnesses,
benchmark, coverage, diagnostic, and build-script adapters. Installed tools,
workspace shape, repository size, ecosystem convention, legacy status labels,
example syntax, and command success cannot create or complete generic policy.

## Typed Outcomes

Return `invalid` when selected claim, authority, scope, tool, mechanism, target,
configuration, or evidence facts contradict one another. Return `unsupported`
when a valid contract has no supported Rust or Cargo expression. Return
`unavailable` when required claim, authority, scope, tool, capability, target,
configuration, environment, or evidence facts cannot be established.

Do not fall back to an installed or popular tool, conventional Cargo command,
workspace-wide scope, all features or targets, fixed lint severity, CI
execution, retries, a required/optional/recommended label, successful no-op, or
smallest diff.

## Cargo Baseline Command Mechanisms

After Verification selects claims, scopes, environments, and evidence
obligations, express each accepted Rust formatting, lint, build, test, doctest,
or feature claim through supported Cargo and Rust tool command mechanisms. Map
only the packages, targets, features, profiles, environments, and diagnostics
required by that claim.

A baseline command mechanism does not create a universal baseline or require
local and CI duplication, workspace scope, all targets, all features, warning
denial, doctests, no-default-feature checks, or a public-feature category.
Missing or contradictory claim, scope, capability, environment, or evidence
facts retain the typed outcomes instead of selecting a conventional command.

## Cargo Workspace Lint-Expression Mechanisms

After Tooling selects lint purpose, rules, scope, severity, debt handling, and
orchestration, and Rust Unsafe accepts any unsafe-code boundary, express the
accepted rules through supported Cargo workspace lint tables and member
inheritance mechanisms. Each member remains within the selected lint scope;
inheritance does not transfer lint-policy authority to the workspace root.

Workspace layout, a root manifest, available inheritance, an existing lint
table, or a lint name cannot require centralization, member opt-in, a rule set,
severity, warning or denial, or relaxation of unsafe policy. Unsupported or
missing expression facts retain typed outcomes rather than changing policy.

## Criterion Benchmark Adapter Mechanisms

After Performance accepts the claim, workload, metric, environment, baseline,
variability policy, budget or comparison, input representativeness, and
benchmark design, Tooling selects Criterion, and Verification accepts the
evidence obligation, express that contract through supported Criterion Cargo
configuration, harness, measurement, and reporting mechanisms. Adapter syntax
may preserve accepted inputs and throughput reporting but cannot create them.

A performance claim, changed hot path, regression budget, Rust project,
installed Criterion package, conventional `benches` directory, available
`black_box`, example dependency version, harness setting, or CI environment
cannot select Criterion or create benchmark triggers, thresholds, workloads,
fixture policy, storage, schedules, or noise controls. Missing or unsupported
adapter facts retain typed outcomes rather than weakening the accepted
performance or evidence contract.

## Rust Test-Runner Adapter Mechanisms

After Tooling selects a test runner, configuration, timeout, isolation,
partition, reporting, and schedule contract, Verification accepts the test and
doctest claims, and Resilience accepts any retry eligibility, budgets, repeated-
execution safety, termination, and recovery contract, express those decisions
through supported Cargo and Rust test-runner invocation and result-transport
mechanisms. When the accepted runner is nextest, its adapter may expose only
capabilities selected by those contracts.

An installed nextest command, workspace size, test-binary count, CI provider,
available timeout, JUnit, isolation, partition, or retry feature cannot select
nextest or create policy. Runner success cannot satisfy omitted doctest or other
claims. Missing or unsupported adapter facts retain typed outcomes rather than
selecting `cargo test`, nextest, retries, or weaker evidence.

## Cargo Feature-Matrix Adapter Mechanisms

After Dependencies, Contracts, Library, and Cross-Platform accept feature,
consumer-configuration, footprint, target, and support contracts; Rust
Dependency and Rust API accept manifest and source expressions; Tooling selects
a matrix tool and schedule; and Verification accepts the evidence claims,
express the selected matrix through supported Cargo and cargo-hack invocation
and result mechanisms.

Cargo-hack availability, crate category, feature count, workspace layout,
`no_std`, optional dependencies, platform conditions, or public visibility
cannot select a tool, each-feature or powerset coverage, scope, exclusions,
baseline commands, or CI schedule. Missing or unsupported matrix facts retain
typed outcomes rather than selecting all features, no default features, a
feature-count threshold, or weaker evidence.

## Compile-Fail Harness Adapter Mechanisms

After Contracts accepts a compile-time rejection contract, Rust API accepts
the source expression, Tooling selects a harness and schedule, and Verification
accepts the rejection evidence, express the claim through supported Rust
compile-fail harness, fixture, diagnostic-matching, and invocation mechanisms.

Type-level syntax, public API status, safety or correctness labels, an installed
trybuild dependency, or a restriction category cannot select trybuild, fixture
shape, diagnostic matching, CI execution, or claim coverage. Missing or
unsupported adapter facts retain typed outcomes rather than substituting a
compile check, runtime assertion, panic, or successful build.

## Property-Test Harness Adapter Mechanisms

After Contracts accepts the invariant and domain authority, Verification
accepts the property, input domain, generator, shrinking, reproducibility,
oracle, and evidence contract, and Tooling selects a harness and schedule,
express those decisions through supported Rust property-test generator,
strategy, runner, seed, shrinking, and result mechanisms.

An algorithm, roundtrip, parser, state machine, validated type, graph operation,
or installed proptest dependency cannot select property testing, a generator,
strategy, oracle, case count, seed, shrink behavior, CI execution, or claim.
Missing or unsupported adapter facts retain typed outcomes rather than
narrowing the domain, weakening the property, or accepting harness success.

## Verification

Evidence covers the accepted claim and scope, actual supported Rust and Cargo
mechanism behavior, selected tool and configuration authority, affected
packages, targets, features, consumers, and environments. Mechanism or command
success proves only its declared claim.
