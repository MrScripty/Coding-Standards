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
| Material sequencing, independently owned contract, migration, coordination, rollout, risk, acceptance complexity, or re-planning | [Planning](workflows/planning.md) |
| Commit creation, history maintenance, or branch/worktree isolation, integration, terminal lifecycle, or cleanup decisions | [Commit](workflows/commit.md) |
| Durable responsibility, decision, contract, or operational procedure changes | [Documentation](workflows/documentation.md) |
| Build-time actions, authoritative build inputs or outputs, invalidation, native integration, environment access, or deterministic-build requirements change | [Build](workflows/build.md) |
| CI or development-tool selection, configuration, scheduling, or orchestration changes | [Tooling](workflows/tooling.md) |
| Shipping an artifact, changing a published version promise, or preparing consumer-visible release information | [Release](workflows/release.md) |

Apply the bounded-local exclusion before Planning triggers. A coherent change
with an obvious objective, exact write set, regression check, and acceptance
path does not require a written plan merely because it touches multiple files,
layers, or a public, generated, persistence, process, language, or
user-interface boundary.

## Workflow Profiles

| Condition | Select |
| --- | --- |
| Two or more proposals may remain outstanding from the same mutable plan revision before integration, and correctness depends on detecting intervening plan or shared-authority change | [Concurrent Plan Integration profile](profiles/workflows/concurrent-plan-integration.md) plus Planning |

Do not select concurrent plan integration for serial collaboration, read-only
investigation, non-authorizing reports, work whose admission facts cannot become
stale, or one current-state integration owner with no outstanding proposals.

## Application Profiles

| Condition | Select |
| --- | --- |
| Reusable package, crate, SDK, or library module | [Library](profiles/applications/library.md) |
| Web or web-technology user interface, component, rendering path, interaction, frontend state projection, or frontend test changes | [Frontend application profile](profiles/applications/frontend.md) |
| Common application launcher command projection, lifecycle, delegation, or outcome-preservation contract is required | [Launcher application profile](profiles/applications/launcher.md) |

Do not select frontend or launcher guidance for a library-only code change.
Frontend framework mechanisms do not transfer domain, persistence, transport,
contract, or accessibility authority into the presentation layer.

## Boundary Profiles

| Condition | Select |
| --- | --- |
| Foreign memory, handles, callbacks, FFI, or cross-language resource access | [Interop boundary profile](profiles/boundaries/interop.md) |
| Generated host-language APIs, binding adapters, host wrappers, or cross-language value representation | [Language Binding boundary profile](profiles/boundaries/language-bindings.md) |
| A schema or generator produces program-facing models, validators, tool definitions, bindings, configuration, or another consumed representation | [Generated Contract boundary profile](profiles/boundaries/generated-contract.md) |
| Structured request, response, command, query, or event crosses a process, message, worker, plugin-host, or independently deployed component boundary | [IPC boundary profile](profiles/boundaries/ipc.md) |
| Durable read, write, publication, transaction, migration application, version ledger, or store mutation | [Persistence boundary profile](profiles/boundaries/persistence.md) plus Contracts and any applicable Resilience, Concurrency, Security, Build, Diagnostics, or Verification owner |

Select a boundary from a real crossing, not because the repository happens to
contain infrastructure code.

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
| C# `await`, `Task`, continuation scheduling, synchronization context, or thread-affinity mechanism changes | [C# Async profile](profiles/languages/csharp/async.md) plus the Concurrency topic |
| Rust source, Cargo metadata, or Rust-generated artifacts change | [Rust profile](profiles/languages/rust/README.md) |
| Rust public or boundary-facing type, conversion, visibility, result, panic, trait, parameter, Cargo-feature, or Rustdoc mechanism changes | [Rust API profile](profiles/languages/rust/api.md) plus the Rust profile and applicable generic owners |
| Rust Cargo dependency declaration, workspace inheritance, resolver metadata, dependency graph, audit adapter, or build-cost measurement mechanism changes | [Rust Dependency profile](profiles/languages/rust/dependencies.md) plus the Rust profile and applicable generic owners |
| Rust toolchain, Cargo package/workspace release metadata, publication control, release automation adapter, or Rust release evidence mechanism changes | [Rust Release profile](profiles/languages/rust/release.md) plus Release, the Rust profile, and applicable generic owners |
| Rust or Cargo formatting, lint, test-runner, feature-matrix, benchmark, coverage, diagnostic, or build-script adapter mechanism changes | [Rust Tooling profile](profiles/languages/rust/tooling.md) plus Tooling, Verification, the Rust profile, Build for build-script behavior, and other applicable generic owners |
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
| Untrusted input authorizes an operation, resource access, side effect, or security-relevant decision | [Security](topics/security.md) |

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
The Concurrent Plan Integration profile is also excluded when no outstanding
proposal can become stale before integration.

Acceptance is a focused regression test plus affected Rust static/toolchain
checks. No ADR, release procedure, directory README, or large plan is required
unless the investigation discovers a corresponding condition.

## Legacy Entry Points

Canonical modules own all normative rules. A retained former standards or
profile entrypoint is non-normative navigation only. It does not establish
applicability, preserve an older rule, or provide fallback authority.

If a legacy index conflicts with its canonical owner, report the index as
invalid and use only the canonical owner after the conflict is corrected. If a
canonical route is missing or unresolved, return an Invalid Routing diagnostic
instead of selecting a legacy entrypoint.

## Invalid Routing

Stop and report a routing diagnostic when:

- selected modules form a dependency or precedence cycle;
- two canonical modules claim the same rule;
- applicability depends on an unknown consumer, platform, persistence, or
  deployment fact;
- a profile would weaken Core without an explicit project exception; or
- the routed set cannot name acceptance evidence for the objective.
