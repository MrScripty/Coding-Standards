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

## Toolchain Declaration Mechanisms

After Release defines the reproducibility claim and required controlled inputs,
select supported Rust toolchain declaration mechanisms for the accepted channel,
components, targets, consumers, and evidence environment. A declaration records
selected toolchain facts; it does not select a version, channel, component,
target, pinning policy, or reproducibility threshold.

Lockfile selection and resolution policy remain with Release and Dependencies.
Cargo resolver metadata and lockfile mechanisms remain with Rust Dependency.
Rust Release consumes those accepted facts and their evidence; it does not
re-own, alias, or infer them from repository type, package category, an existing
lockfile, or a successful resolved graph.

## Cargo Package Release Metadata Mechanisms

After Release and Contracts define artifact identity, version, publication, and
consumer promises, and Licensing and Documentation accept their applicable
facts, express the selected Rust package facts through supported Cargo package
metadata fields. Include only fields required by the accepted release unit,
channel, registry, package consumer, toolchain, and evidence contracts.

Cargo metadata does not select a package name, product identity, version,
edition, minimum Rust version, description, license, repository, README,
keywords, categories, field completeness, or publication readiness. Existing
manifest values and registry acceptance cannot complete missing authority.

## Cargo Publication-Control Mechanisms

After Release defines which package artifacts may be published through each
channel, express the accepted decision through supported Cargo publication
controls. Select the mechanism from the release unit, package identity,
channel, consumer, artifact composition, and registry capability.

A Cargo control does not decide whether a binary, native library, internal
tool, test harness, integration package, or workspace member is publishable.
Package category, crate type, workspace placement, an existing `publish` field,
or registry behavior cannot create publication authority.

## Cargo Workspace Package-Metadata Mechanisms

After Release defines the release units and their version relationships, and
the applicable generic owners accept shared package facts, express selected
coordination through supported Cargo `[workspace.package]` declarations and
member package-field inheritance. Each inherited field remains an accepted fact
of the member's release unit; inheritance does not merge release units or make
the workspace root their policy owner.

Select coordination per accepted release unit, package consumer, publication
channel, contract, toolchain, licensing, documentation, and evidence facts.
Workspace membership, repository layout, an existing root manifest, shared
versions, or support for `.workspace = true` cannot require lockstep versioning
or inheritance of any package field.

## Verification

Evidence covers the accepted release unit and channels, actual supported Rust
toolchain and Cargo behavior, affected manifests and packages, selected
artifacts and consumers, adapter diagnostics, and every claim selected by the
generic owners. Mechanism or command success proves only its declared claim.
