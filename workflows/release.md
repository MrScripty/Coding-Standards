# Release Workflow

**Standards metadata**

- ID: `workflow.release`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change ships or publishes an artifact, changes a published version promise, or prepares consumer-visible release information.
- Does not apply when: A coordinated internal change is neither shipped independently nor part of a published contract.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Release decision fixtures, ownership checks, and affected release acceptance claims.
- Canonical owner: `workflows/release.md`

## Release Boundary

Select this workflow when at least one release fact is present:

- an artifact or package will be shipped or published;
- independently deployed consumers rely on a published version promise;
- a public contract, supported persisted state, or distribution channel changes;
  or
- consumer-visible release information must be prepared.

An internal coordinated replacement does not require release compatibility,
versioning, or changelog work merely because the repository has versions. If
the release facts are unknown, report an unresolved release diagnostic instead
of assuming a public or internal boundary.

## Contract And Version Decision

Classify affected contracts through
[Contract Evolution](../topics/contracts.md) before choosing a version,
compatibility window, deprecation, or migration.

- `internal-coordinated` changes replace all owned consumers atomically and do
  not create a compatibility version by default.
- `public-versioned` changes follow the published version promise.
- `distributed-independent` changes define negotiation, overlap, migration, or
  typed rejection for unsupported versions.
- `persisted` changes name supported source states and migration evidence.

When a project adopts Semantic Versioning, choose the bump from observable
published-contract effects: incompatible change, compatible capability, or
compatible correction. Do not infer compatibility from source syntax, commit
type, or additive shape alone.

Major version zero denotes initial development under SemVer; it is not a
prerelease identifier and does not erase explicit consumer or migration
promises. Prerelease identifiers such as `-alpha.1` separately describe release
precedence.

Define the release unit from actual publication and consumer ownership.
Packages may version independently or in lockstep. Do not force workspace-wide
version alignment without an adopted release-unit contract.

## Deprecation And Migration

A deprecation policy exists only for a published promise that requires overlap.
It states:

- the deprecated behavior and supported replacement;
- the versions or time window in which both remain supported;
- how consumers discover the deprecation;
- the removal version or decision trigger; and
- evidence for the replacement and removal path.

Breaking public or persisted changes provide migration instructions
proportional to consumer needs. Internal coordinated replacement removes the
old path in the same change and must not add a speculative deprecation shim.

## Changelog

Record consumer-visible changes for a release boundary. A project may collect
entries directly under an unreleased section or use independently mergeable
fragments. The chosen mechanism must avoid silent loss and merge-conflict-prone
shared edits.

An entry states the observable change, affected consumers, and migration or
security implications when applicable. Typical categories include added,
changed, deprecated, removed, fixed, and security, but project-owned formats
may differ.

Do not derive changelog inclusion solely from commit types. Internal refactors,
tests, formatting, and tooling changes are omitted unless they alter the
published artifact or consumer contract.

At release preparation:

1. assemble all applicable entries for the selected release unit;
2. resolve the version and date from the accepted version decision;
3. link required migration instructions and public diagnostics;
4. exclude sensitive security details until disclosure is authorized; and
5. verify that the released entries match the artifact and published contract.

## Acceptance Boundary

Before publishing, identify every claim required by the release:

- `release-artifact` claims for packaging, installation, loading, checksums,
  signatures, or publication properties;
- behavior claims for changed contracts, systems, or user workflows; and
- environment qualifications for supported targets or required infrastructure.

The [Verification Workflow](verification.md) owns claim meaning and evidence
sufficiency. An artifact startup smoke proves only its named artifact
assertions; it does not prove changed feature behavior, other target artifacts,
or a user workflow.

Unsatisfied required claims remain visible release blockers. Release procedure
and publication gates consume accepted claims but cannot downgrade or replace
them.

## Pending Migration Boundary

[Legacy Release Standards](../RELEASE-STANDARDS.md) temporarily retain only
unmigrated artifact/packaging, reproducible-build, pipeline/publication,
channel/download, checklist, rollback, and tool-recipe guidance. Those sections
cannot override applicability, versioning, changelog, contract, deprecation,
migration, or acceptance decisions owned here.
