# Rust Dependency Profile

**Standards metadata**

- ID: `profile.language.rust.dependencies`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A Rust change expresses or inspects an accepted dependency contract through Cargo manifests, workspaces, features, resolution metadata, dependency graphs, audit adapters, or build-cost measurements.
- Does not apply when: No Rust or Cargo dependency mechanism changes, or the task only selects generic dependency, security, licensing, performance, verification, tooling, public-feature, or recipe policy.
- Requires: `core`, `workflow.verification`, `profile.language.rust`, `topic.dependencies`
- Specializes: `profile.language.rust`
- Verification: Rust dependency mechanism decisions plus claim-matched Cargo resolver, manifest, graph, audit-adapter, or measurement evidence selected by generic owners.
- Canonical owner: `profiles/languages/rust/dependencies.md`

## Mechanism Authority

Generic owners select dependency requirements, ownership, candidates, features,
security and licensing findings, performance claims, verification evidence,
tooling schedules, and public feature contracts. This profile selects a Rust or
Cargo mechanism only after every applicable contract is accepted.

Applicable mechanisms may include Cargo manifest declarations, workspace
inheritance, feature and target expressions, resolver metadata, dependency-graph
queries, audit-tool adapters, and build-cost measurement. Existing manifests,
workspace shape, installed tools, ecosystem conventions, and successful
commands cannot create or complete generic policy.

## Typed Outcomes

Return `invalid` when the selected mechanism contradicts an accepted owner,
consumer, target, resolver, feature, or evidence contract. Return `unsupported`
when a valid contract has no supported Cargo or Rust expression. Return
`unavailable` when a required owner, manifest, resolver, toolchain, consumer,
tool, or evidence fact cannot be established.

Do not fall back to the incumbent manifest, root workspace, inherited
dependency, enabled feature, cached resolution, installed audit tool,
conventional command, successful compile, or smallest diff.

## Verification

Evidence covers the actual supported Cargo resolver and toolchain, affected
manifests and consumers, selected target and feature configurations, resolved
identity and graph, adapter diagnostics, and the measurement contract selected
by generic owners. Command success proves only that invocation's declared
mechanism claim.
