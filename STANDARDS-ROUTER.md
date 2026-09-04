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

## Concept Map

Start with the shared decision, then follow only its affected details:

- **Design:** Architecture covers responsibility and state ownership; Contracts
  covers invariants, representations, and consumer promises; Security covers
  trust and permission. Follow their conditional detail links when needed.
- **Develop:** Implementation owns the change; Verification owns its evidence;
  Documentation records durable knowledge. Specialized test techniques are
  selected separately from an ordinary regression check.
- **Operate and distribute:** Build owns artifact production, Release owns
  distribution promises, and Resilience owns failure and recovery.

Application, boundary, language, and framework profiles refine these concepts.
`Requires` loads an unconditional prerequisite. `Specializes` names the broader
concept refined by a page; it does not mean that the parent loads every child.
The tables below and each page's conditional links support further discovery.
A reading plan is a prerequisite order, not a requirement to explore every
possible refinement.

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
| Change code or standards | [Implementation](workflows/implementation.md) |
| Prove a behavior, contract, or artifact | [Verification](workflows/verification.md) |
| Investigation or evidence work may delay a sufficient implementation | [Development Proportionality](workflows/development-proportionality.md) |
| Coordinate material sequencing, migration, rollout, risk, or acceptance complexity | [Planning](workflows/planning.md) |
| Create commits or manage history, branches, or worktrees | [Commit](workflows/commit.md) |
| Change durable responsibility, design, contract, or operational knowledge | [Documentation](workflows/documentation.md) |
| Change build inputs, outputs, invalidation, native integration, or environment use | [Build](workflows/build.md) |
| Select or configure development tools, CI, scheduling, or orchestration | [Tooling](workflows/tooling.md) |
| Ship an artifact or change a published promise | [Release](workflows/release.md) |

A bounded change with a clear objective and acceptance path needs no written
plan solely because it crosses files or layers.

## Workflow Profiles

| Condition | Select |
| --- | --- |
| Multiple outstanding proposals can become stale before serial integration | [Concurrent Plan Integration profile](profiles/workflows/concurrent-plan-integration.md) |

## Application Profiles

| Condition | Select |
| --- | --- |
| Develop a reusable library, package, crate, or SDK | [Library](profiles/applications/library.md) |
| Change a web interface, rendering, interactions, or frontend state | [Frontend application profile](profiles/applications/frontend.md) |
| Change a launcher command, lifecycle, delegation, or outcome | [Launcher application profile](profiles/applications/launcher.md) |

## Boundary Profiles

| Condition | Select |
| --- | --- |
| Cross foreign memory, handles, callbacks, or FFI | [Interop boundary profile](profiles/boundaries/interop.md) |
| Expose host APIs, wrappers, or cross-language representations | [Language Binding boundary profile](profiles/boundaries/language-bindings.md) |
| Generate a representation consumed as a program contract | [Generated Contract boundary profile](profiles/boundaries/generated-contract.md) |
| Exchange structured messages across processes or independently changing components | [IPC boundary profile](profiles/boundaries/ipc.md) |
| Read, write, publish, transact, or migrate durable state | [Persistence boundary profile](profiles/boundaries/persistence.md) |

## Generated Contract Profile Applicability

Select the Generated Contract profile when a schema or generator produces a
representation consumed as program behavior, including models, validators,
tool definitions, bindings, or executable configuration. A generated text or
data file does not select the profile when no program consumer interprets it as
a contract.

Select Language Binding separately only when an actual native/host or
cross-language representation exists. Select IPC separately only when the
representation crosses a process, message, plugin-host, or independently
deployed boundary. Select Persistence separately only when a supported
consumer observes the representation or state after the producing process or
operation ends.

Route the observable task facts through the executable Router projection. Do
not replace unresolved boundary, consumer, deployment, or persistence facts
with a smaller static module list.

## Language Profiles

| Condition | Select |
| --- | --- |
| Change C# tasks, await, continuation scheduling, or thread affinity | [C# Async profile](profiles/languages/csharp/async.md) |
| Change Rust source, Cargo metadata, or generated Rust artifacts | [Rust profile](profiles/languages/rust/README.md) |
| Change Rust public types, conversions, errors, visibility, traits, features, or Rustdoc | [Rust API profile](profiles/languages/rust/api.md) |
| Change Cargo dependencies, resolution, auditing, or build-cost measurement | [Rust Dependency profile](profiles/languages/rust/dependencies.md) |
| Change Rust release toolchains, packages, publication, or evidence | [Rust Release profile](profiles/languages/rust/release.md) |
| Change Cargo formatting, lint, test, benchmark, coverage, or build-script adapters | [Rust Tooling profile](profiles/languages/rust/tooling.md) |
| Change Rust async APIs, backpressure, cancellation, or async resource lifetimes | [Rust Async profile](profiles/languages/rust/async.md) |
| Change Rust targets, target-dependent behavior, or support evidence | [Rust Cross-Platform profile](profiles/languages/rust/cross-platform.md) |
| Change TypeScript source, compiler settings, declarations, or visible contracts | [TypeScript profile](profiles/languages/typescript.md) |
| Change promises, overlapping calls, cancellation, or stale-result handling | [TypeScript Async profile](profiles/languages/typescript/async.md) |
| Rust unsafe operations, unsafe contracts, or unsafe implementations change | [Rust Unsafe](profiles/languages/rust/unsafe.md) |
| Rust untrusted paths, sizing, queues, or listeners affect security | [Rust Security](profiles/languages/rust/security.md) |
| Rust crosses a foreign-memory, FFI, or callback boundary | [Rust Interop](profiles/languages/rust/interop.md) |
| Rust supplies generated host APIs or cross-language representations | [Rust Language Bindings](profiles/languages/rust/language-bindings.md) |
| No language-specific mechanism changes | No language profile |

Language profiles specialize mechanisms only; shared policy remains in the
applicable general owner.

## Framework Profiles

| Condition | Select |
| --- | --- |
| Change Godot object, scene, signal, resource, threading, or lifetime mechanisms | [Godot framework profile](profiles/frameworks/godot.md) |
| No framework-specific mechanism changes | No framework profile |

## Topic Selection

Select a canonical topic only when its observable condition is present:

| Concern | Current owner |
| --- | --- |
| Accessibility outcome, user interaction semantics, modality, or conformance obligations | [Accessibility](topics/accessibility.md) |
| Diagnostic purpose, audience, causal identity, context, propagation, retention, disclosure projection, or reporting claim | [Diagnostics](topics/diagnostics.md) |
| Runtime decoding, contract evolution, persistence compatibility, version overlap, or degraded outcomes | [Contracts](topics/contracts.md) |
| Shared mutable state, overlapping work, async failure ownership, cancellation, or shutdown | [Concurrency](topics/concurrency.md) |
| Dependency or service failure, retry, degradation, startup resilience, or recovery semantics | [Resilience](topics/resilience.md) |
| Filesystem path construction, identity, comparison, or supported-filesystem behavior | [Cross-platform](topics/cross-platform.md) |
| Dependency requirement, ownership, selection, resolution, provisioning, update, or removal policy is required, including a decision to implement difficult standardized semantics instead of adopting an established implementation | [Dependencies](topics/dependencies.md) |
| Third-party material is selected, incorporated, adapted, generated from, redistributed, or published | [Licensing](topics/licensing.md) |
| Performance budget, measurement, optimization, benchmark, resource use, or regression claim changes | [Performance](topics/performance.md) |
| Module, layer, service, data/state authority, dependency direction, or runtime composition changes | [Architecture](topics/architecture.md) |
| Untrusted input, protected operations, sensitive data, credentials, transport security, or dependency trust changes | [Security](topics/security.md) |

The presence of a topic document in the repository is not an applicability
condition.

## Conditional Details

After selecting broad concerns, use these conditions to narrow the reading.
The executable fact `routing.details` accepts the canonical IDs below. Known
absence is an empty set; unknown conditions remain unresolved. Generated
contracts, IPC, persistence, cross-language bindings, and platform verification
also select their corresponding details from the existing boundary and task
facts. An ordinary Rust parser fix selects none of these detail pages.

| Condition | Select |
| --- | --- |
| A change makes structural, abstraction, or terminology decisions | [Code Design And Ownership](topics/code-design.md) |
| A handle promises immutable results or replay | [topic.architecture.replay](topics/architecture/replay.md) |
| A change affects schema dialects, generated contracts, or contract version invalidation | [topic.contracts.schemas](topics/contracts/schemas.md) |
| A change projects domain outcomes into a protocol or adapts a protocol boundary | [topic.contracts.protocols](topics/contracts/protocols.md) |
| A change affects contract compatibility, persisted representations, or independently changing consumers | [topic.contracts.evolution](topics/contracts/evolution.md) |
| A change creates a validator, negative fixture, property test, differential test, or other independent oracle | [workflow.verification.oracles](workflows/verification/oracles.md) |
| A claim spans supported targets or requires platform-specific evidence | [workflow.verification.platforms](workflows/verification/platforms.md) |
| Rust bindings adapt events, callback tasks, runtime handles, or executors | [profile.language.rust.binding-lifecycle](profiles/languages/rust/binding-lifecycle.md) |
| A change selects maintenance channels, publication presentation, or release recovery procedures | [workflow.release.operations](workflows/release/operations.md) |
| A graphical user workflow requires smoke evidence | [workflow.verification.gui](workflows/verification/gui.md) |

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
The Concurrent Plan Integration profile is also excluded when no outstanding
proposal can become stale before integration.

Acceptance is a focused regression test plus affected Rust static/toolchain
checks. No ADR, release procedure, directory README, or large plan is required
unless the investigation discovers a corresponding condition.

## Invalid Or Legacy Routing

Use canonical owners for policy; legacy entrypoints are navigation only.
Report unresolved material facts, conflicting ownership, dependency cycles,
or a missing canonical route. Continue independently routable work. Do not
substitute a legacy rule or assume an unknown condition is absent.
