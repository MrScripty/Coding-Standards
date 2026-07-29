# Standards Router

**Standards metadata**

- ID: `router`
- Role: `router`
- Level: `MUST`
- Applies when: A task must select guidance from this standards library.
- Does not apply when: The project has not adopted this standards library.
- Requires: `core`
- Specializes: `none`
- Verification: Routing fixtures resolve expected modules, exclusions, and dependencies.
- Canonical owner: `STANDARDS-ROUTER.md`

Use this file after [CORE-STANDARDS.md](CORE-STANDARDS.md). Select guidance from
observable task conditions. Do not read every document by default.

## Routing Procedure

1. State the requested outcome and affected artifact.
2. Select workflow modules for the activities being performed.
3. Select application, boundary, and language profiles from actual repository
   facts.
4. Select topics only when the concern is affected.
5. Follow each selected module's `Requires` metadata.
6. Confirm common exclusions.
7. If a required fact is unknown, report unresolved routing instead of
   selecting a convenient default.

## Workflow Selection

| Condition | Select |
| --- | --- |
| Any code or standards change | [Implementation](workflows/implementation.md) |
| Behavior or contract must be proven | [Verification](workflows/verification.md) |
| Multi-step work, architectural decisions, or re-planning | [Planning](workflows/planning.md) |
| Commit creation or history maintenance | [Commit](workflows/commit.md) |
| Durable responsibility, decision, contract, or operational procedure changes | [Documentation](workflows/documentation.md) |
| Dependency or CI/tool configuration changes | [Current tooling guidance](TOOLING-STANDARDS.md) until migration |
| Shipping an artifact, changing a published version promise, or preparing consumer-visible release information | [Release](workflows/release.md) |

Small, local, low-risk changes do not require a large implementation plan when
the objective, write set, regression check, and acceptance are obvious.

## Application Profiles

| Condition | Select |
| --- | --- |
| Reusable package, crate, SDK, or library module | [Library](profiles/applications/library.md) |
| Web or web-technology user interface | [Current frontend guidance](FRONTEND-STANDARDS.md) until migration |
| Common application launcher contract is required | [Current launcher guidance](LAUNCHER-STANDARDS.md) until migration |

Do not select frontend or launcher guidance for a library-only code change.

## Boundary Profiles

| Condition | Select |
| --- | --- |
| Foreign memory, handles, callbacks, FFI, or cross-language resource access | [Interop boundary profile](profiles/boundaries/interop.md) |
| Generated host-language APIs | [Current bindings guidance](LANGUAGE-BINDINGS-STANDARDS.md) |
| Structured request, response, command, query, or event crosses a process, message, worker, plugin-host, or independently deployed component boundary | [IPC boundary profile](profiles/boundaries/ipc.md) |
| Persisted data or migration | [Current architecture persistence guidance](ARCHITECTURE-PATTERNS.md) |

Select a boundary from a real crossing, not because the repository happens to
contain infrastructure code.

## Language Profiles

| Condition | Select |
| --- | --- |
| Rust source, Cargo metadata, or Rust-generated artifacts change | [Rust profile](profiles/languages/rust/README.md) |
| No language-specific mechanism changes | No language profile |

Language profiles specialize mechanisms only. Cross-language policy remains in
Core, workflows, and topics.

## Topic Selection

Until topic migration completes, use the current canonical file only when its
condition is present:

| Concern | Current owner |
| --- | --- |
| Accessibility or user interaction semantics | [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) |
| Runtime decoding, contract evolution, persistence compatibility, version overlap, or degraded outcomes | [Contracts](topics/contracts.md) |
| Shared mutable state, async work, cancellation, or shutdown | [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) |
| Filesystem path construction, identity, comparison, or supported-filesystem behavior | [Cross-platform](topics/cross-platform.md) |
| Other multiple declared operating-system target concerns | [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) until migration |
| Third-party package selection or update | [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) |
| Untrusted input authorizes an operation, resource access, side effect, or security-relevant decision | [Security](topics/security.md) |
| Other network transport or secret concerns | [SECURITY-STANDARDS.md](SECURITY-STANDARDS.md) until migration |

The presence of a topic document in the repository is not an applicability
condition.

## S1 Rust Library Bug-Fix Route

For a one-module Rust parser bug in a library with no public-contract,
persistence, UI, dependency, or release change, select exactly:

- Core;
- Router;
- Implementation workflow;
- Verification workflow;
- Library application profile; and
- Rust language profile.

Explicitly exclude architecture patterns, release, frontend, launcher,
accessibility, cross-platform, interop, bindings, and persistence guidance.

Acceptance is a focused regression test plus affected Rust static/toolchain
checks. No ADR, release procedure, directory README, or large plan is required
unless the investigation discovers a corresponding condition.

## Migration Authority

New modules are canonical for the rules they state. Existing files retain
authority only for rules not yet moved and carry migration notices when overlap
exists. If old and new wording conflict for a moved rule, the new module wins.

This is explicit migration ownership, not runtime fallback or duplicated
normative authority.

## Invalid Routing

Stop and report a routing diagnostic when:

- selected modules form a dependency or precedence cycle;
- two canonical modules claim the same rule;
- applicability depends on an unknown consumer, platform, persistence, or
  deployment fact;
- a profile would weaken Core without an explicit project exception; or
- the routed set cannot name acceptance evidence for the objective.
