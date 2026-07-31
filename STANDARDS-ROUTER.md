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
| CI or tool configuration changes | [Current tooling guidance](TOOLING-STANDARDS.md) until migration |
| Shipping an artifact, changing a published version promise, or preparing consumer-visible release information | [Release](workflows/release.md) |

Small, local, low-risk changes do not require a large implementation plan when
the objective, write set, regression check, and acceptance are obvious.

## Application Profiles

| Condition | Select |
| --- | --- |
| Reusable package, crate, SDK, or library module | [Library](profiles/applications/library.md) |
| Web or web-technology user interface | [Current frontend guidance](FRONTEND-STANDARDS.md) until migration |
| Common application launcher command projection, lifecycle, delegation, or outcome-preservation contract is required | [Launcher application profile](profiles/applications/launcher.md) |

Do not select frontend or launcher guidance for a library-only code change.

## Boundary Profiles

| Condition | Select |
| --- | --- |
| Foreign memory, handles, callbacks, FFI, or cross-language resource access | [Interop boundary profile](profiles/boundaries/interop.md) |
| Generated host-language APIs, binding adapters, host wrappers, or cross-language value representation | [Language Binding boundary profile](profiles/boundaries/language-bindings.md) |
| Structured request, response, command, query, or event crosses a process, message, worker, plugin-host, or independently deployed component boundary | [IPC boundary profile](profiles/boundaries/ipc.md) |
| Persisted data or migration | [Current architecture persistence guidance](ARCHITECTURE-PATTERNS.md) |

Select a boundary from a real crossing, not because the repository happens to
contain infrastructure code.

## Language Profiles

| Condition | Select |
| --- | --- |
| C# `await`, `Task`, continuation scheduling, synchronization context, or thread-affinity mechanism changes | [C# Async profile](profiles/languages/csharp/async.md) plus the Concurrency topic |
| Rust source, Cargo metadata, or Rust-generated artifacts change | [Rust profile](profiles/languages/rust/README.md) |
| Rust async API, suspension boundary, concurrent I/O, stream, backpressure, cancellation-aware operation, or async resource lifetime changes | [Rust Async profile](profiles/languages/rust/async.md) plus the Rust profile |
| Rust target contracts, triples, support claims, target-dependent source/configuration, target artifacts, or target evidence obligations change | [Rust Cross-Platform profile](profiles/languages/rust/cross-platform.md) plus the Rust profile and Cross-Platform topic |
| TypeScript source, compiler configuration, declarations, generated TypeScript, or TypeScript-visible contract surfaces change | [TypeScript profile](profiles/languages/typescript.md) |
| TypeScript `Promise`, overlapping invocation, stale-result, cancellation, or async state-application mechanism changes | [TypeScript Async profile](profiles/languages/typescript/async.md) plus the TypeScript profile and Concurrency topic |
| No language-specific mechanism changes | No language profile |

Language profiles specialize mechanisms only. Cross-language policy remains in
Core, workflows, and topics.

## Framework Profiles

| Condition | Select |
| --- | --- |
| Godot object, node, scene-tree, signal, resource, thread-affinity, deferred-dispatch, or object-lifetime mechanism changes | [Godot framework profile](profiles/frameworks/godot.md) plus the Concurrency topic |
| No framework-specific mechanism changes | No framework profile |

Framework profiles specialize selected framework mechanisms only. Generic
policy remains in Core, workflows, and topics.

## Topic Selection

Until topic migration completes, use the current canonical file only when its
condition is present:

| Concern | Current owner |
| --- | --- |
| Accessibility or user interaction semantics | [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) |
| Runtime decoding, contract evolution, persistence compatibility, version overlap, or degraded outcomes | [Contracts](topics/contracts.md) |
| Shared mutable state, overlapping work, async failure ownership, cancellation, or shutdown | [Concurrency](topics/concurrency.md) |
| Dependency or service failure, retry, degradation, startup resilience, or recovery semantics | [Resilience](topics/resilience.md) |
| Filesystem path construction, identity, comparison, or supported-filesystem behavior | [Cross-platform](topics/cross-platform.md) |
| Other multiple declared operating-system target concerns | [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) until migration |
| Dependency requirement, ownership, selection, resolution, provisioning, update, or removal policy is required | [Dependencies](topics/dependencies.md) |
| Third-party material is selected, incorporated, adapted, generated from, redistributed, or published | [Licensing](topics/licensing.md) |
| Module, layer, service, data/state authority, dependency direction, or runtime composition changes | [Architecture](topics/architecture.md) |
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
