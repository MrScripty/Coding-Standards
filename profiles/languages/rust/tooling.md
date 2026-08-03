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

## Verification

Evidence covers the accepted claim and scope, actual supported Rust and Cargo
mechanism behavior, selected tool and configuration authority, affected
packages, targets, features, consumers, and environments. Mechanism or command
success proves only its declared claim.
