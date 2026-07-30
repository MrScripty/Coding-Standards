# Milestone 7 Row 6 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 6,
`STD-0294` through `STD-0299`. It is planning evidence, not normative policy.

The baseline row proposes one Cross-Platform owner, but the frozen text mixes
native artifact loading, release artifact presentation, and verification
scheduling. Implementing it as one rule would duplicate accepted Release and
Verification owners and preserve fixed Strategy, filename, CI-provider, and
trigger defaults.

## Scope

This slice changes only:

- this report and its focused checker;
- the execution decomposition overlay;
- the acceleration package outcome; and
- the active plan, acceleration report, evaluation index, findings, and
  execution ledger.

It changes no normative or legacy standard, disposition, generated artifact,
owner map, immutable baseline train row, router, metadata, dependency
declaration, decision fixture, configuration, lockfile, or downstream
repository.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0294`, `STD-0295` | Platform-specific native-library loading through a mandatory Strategy | Cross-Platform owns target- and deployment-selected native artifact loading and typed unresolved outcomes. |
| `STD-0296`, `STD-0297` | Universal library filename table and installation instructions on each platform class | Release owns artifact identity, consumer selection context, installation/load information, and release-artifact evidence. |
| `STD-0298`, `STD-0299` | Fixed CI matrix, provider syntax, fail-fast setting, and pre-commit/pre-push/CI schedule | Verification owns evidence claims, required environments, execution modes, and risk-based scheduling; Release adds shipped-artifact target builds when applicable. |

## Cross-Platform Decomposition

Row 6 receives three ordered children in
[the execution decomposition overlay](milestone-7-execution-decomposition.tsv).

### Child 6.1: Native Artifact Loading

- IDs: `STD-0294`, `STD-0295`
- Owner: `topics/cross-platform.md`
- Outcome: select native artifact loading from the declared target, artifact,
  deployment, capability, and consumer contract.

The contract distinguishes artifact identity from the mechanism that locates,
loads, links, or embeds it. A Strategy object, dynamic loading, embedding,
search path, platform extension, or alternate artifact is not universal.
Contradictory artifact facts are invalid; unsupported targets are unsupported;
missing artifact, deployment, capability, or evidence facts are unavailable.

### Child 6.2: Native Artifact Identity And Installation

- IDs: `STD-0296`, `STD-0297`
- Owner: `workflows/release.md`
- Outcome: derive native artifact identity and consumer installation/loading
  information from the release unit, distribution channel, target, package,
  and consumer contract.

Ecosystem and distribution-channel conventions may select prefixes,
extensions, package coordinates, installers, or registry identities. The
release presents the exact planned identity and enough target, compatibility,
installation, and loading context for consumers. It does not impose one
Linux/Windows/macOS filename table or attach installation prose to every
platform class.

### Child 6.3: Platform Evidence Scheduling

- IDs: `STD-0298`, `STD-0299`
- Owner: `workflows/verification.md`
- Outcome: select target evidence, environment, execution mode, and scheduling
  from the accepted platform support and release claims.

Required target behavior runs in every environment needed to prove its claim.
Shipped artifacts additionally satisfy the Release artifact plan and pipeline.
Provider matrix syntax, Linux/Windows defaults, `fail-fast: false`, and fixed
pre-commit/pre-push/push/PR schedules remain project mechanisms rather than
generic policy.

## Order

The children remain serial:

1. define how the selected native artifact is resolved and loaded;
2. define the shipped artifact identity and consumer installation contract;
3. schedule the evidence required by the platform and release claims.

All children must receive exact dispositions in order before immutable row 7
can activate. Partial or out-of-order completion remains invalid.

## No Fallback

This decomposition does not retain:

- Strategy as a mandatory native-loading abstraction;
- managed-assembly embedding or dynamic loading as a universal choice;
- guessed prefixes, extensions, platform names, or artifact identities;
- installation text on every platform-specific class;
- a fixed Linux/Windows target set or hosted-runner matrix;
- a universal fail-fast setting or commit/push/CI schedule;
- best-effort compilation as evidence for a required target; or
- an alternate loader, artifact, target, or weaker evidence when the selected
  contract is unsupported or unavailable.

Missing or contradictory contract facts produce typed diagnostics.

## Next Slice

Milestone `7.4b8t` accepted child `6.1`, `STD-0294` and `STD-0295`, as the
Cross-Platform native artifact loading contract with focused decision-table
evidence and two exact dispositions.

Milestone `7.4b8u` accepted child `6.2`, `STD-0296` and `STD-0297`, as
Release-owned native artifact identity and installation information with 19
decision cases and two exact dispositions.

Milestone `7.4b8v` accepted child `6.3`, `STD-0298` and `STD-0299`, as
Verification-owned platform evidence coverage and scheduling with 21 decision
cases and two exact dispositions.

Row 6 is complete. Milestone `7.4b8w` begins bounded owner review of immutable
row 7, `STD-0761` through `STD-0771`.
