# Rust Release Profile

**Standards metadata**

- ID: `profile.language.rust.release`
- Role: `profile`
- Level: `PROFILE`
- Applies when: An accepted release contract must be expressed or evidenced through Rust toolchain or Cargo package, publication, workspace, automation-adapter, or release-check mechanisms.
- Does not apply when: No Rust or Cargo release mechanism changes, or the task only selects generic release, contract, dependency, reproducibility, licensing, documentation, performance, tooling, verification, or recipe policy.
- Requires: `core`, `workflow.verification`, `workflow.release`, `profile.language.rust`, `profile.language.rust.dependencies`
- Specializes: `profile.language.rust`
- Verification: Rust release mechanism decisions plus claim-matched toolchain, manifest, package, publication, adapter, and artifact evidence selected by generic owners.
- Canonical owner: `profiles/languages/rust/release.md`

## Mechanism Authority

Generic owners select release boundaries and units, version and artifact
contracts, reproducibility claims, dependency resolution, lockfile ownership,
license and documentation facts, performance claims, tool selection,
automation procedures, verification claims, and evidence obligations. This
profile selects a supported Rust or Cargo mechanism only after every applicable
contract is accepted.

Applicable mechanisms may include Rust toolchain declarations, Cargo package
and workspace release metadata, publication controls, supported release-tool
adapters, and Rust release evidence collection. Existing manifests, installed
tools, ecosystem convention, manual procedure, and successful commands cannot
create or complete generic policy.

## Typed Outcomes

Return `invalid` when selected contract, release-unit, consumer, channel,
manifest, toolchain, mechanism, or evidence facts contradict one another.
Return `unsupported` when a valid contract has no supported Rust or Cargo
expression. Return `unavailable` when required authority, release-unit,
consumer, channel, toolchain, manifest, tool, artifact, or evidence facts
cannot be established.

Do not fall back to incumbent metadata, a pinned version, committed lockfile,
installed release tool, manual steps, conventional command, fixed checklist,
successful build, or smallest diff.

## Verification

Evidence covers the accepted release unit and channels, actual supported Rust
toolchain and Cargo behavior, affected manifests and packages, selected
artifacts and consumers, adapter diagnostics, and every claim selected by the
generic owners. Mechanism or command success proves only its declared claim.
