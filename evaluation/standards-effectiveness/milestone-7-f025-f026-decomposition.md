# Milestone 7 F025/F026 Dependent Rust Decomposition

## Purpose

This planning report decomposes the Rust Language Binding and Rust Security
remainder that depends on the accepted generic Concurrency and Rust Async
owners. It is planning evidence, not a normative binding, runtime, task,
filesystem, listener, or security owner.

Only accepted implementation slices are fully specified. Planned later slices
have frozen identifiers, owners, outcomes, and dependencies, but require a
fresh pre-slice review before their implementation contracts become active.

## Slice 7.4b5a: Planning-Only Decomposition

**Allowed write set:**

- this report and its slice map;
- `verify-milestone-7-f025-f026-decomposition.sh`;
- the parent trust/lifecycle checker for removal of its obsolete current-slice
  assertion only;
- parent decomposition and handoff reports;
- evaluation README, active plan, and execution ledger.

No normative standard/profile, final disposition, owner map, generated
inventory, fixture, template, package file, lockfile, runtime integration, or
downstream repository belongs to this slice.

**Acceptance gate:** the checker proves the exact ten currently undisposed
identifiers, canonical owners, proposed dispositions, serial dependency order,
stable parent acceptance, one implementation-ready slice, planning-only write
boundary, plan lifecycle, shell syntax, whitespace, and all affected
standards-effectiveness regressions.

## Trigger And Scope

`F025` and `F026` remain partial after Rust Async completion because ten
undisposed legacy sections still present dependent or competing guidance:

- the binding architecture permits framework dependencies in the core;
- binding resources embed and therefore appear to own a runtime;
- async binding examples select named runtime and blocking mechanisms instead
  of consuming the selected lifecycle capability;
- composite executor delegation still needs a disposition-backed canonical
  owner even though the source now delegates only explicit unsupported work;
- Rust path validation returns a pathname whose authority can race before use;
  and
- the listener example spawns work without showing registration with the
  accepted lifecycle owner.

The accepted `STD-0802` disposition already proves that core tests run without
binding features. It is a dependency, not an identifier to dispose again.
Callback/event delivery, packaging, generation, workspace layout, bounded
queues, panic policy, and other undisposed sections are outside this bounded
remainder unless a later pre-slice review records a new finding and re-plan.

## Canonical Ownership

| Owner | Authority |
| --- | --- |
| `profiles/languages/rust/language-bindings.md` | Rust host-adapter structure, runtime-capability adaptation, handle lifecycle, and explicit typed executor delegation. |
| `profiles/languages/rust/async.md` | Runtime construction, tracked spawned work, shutdown, cancellation, blocking isolation, and terminal-state observation. |
| composition root and application lifecycle owner | Concrete runtime construction, capability injection, task registration, and shutdown wiring. |
| `topics/security.md` | Generic filesystem authority, containment, validation/use race, and typed no-weaker-path outcome. |
| `profiles/languages/rust/security.md` | Rust mechanisms that preserve filesystem authority through use and secure listener constraints that consume the accepted lifecycle owner. |

Bindings adapt a host call to an injected runtime/lifecycle capability; they do
not construct or own a competing runtime. Security specializes the generic
filesystem and lifecycle contracts; it does not duplicate them or treat a
checked pathname as authority to a later operation.

## Slice Map

[milestone-7-f025-f026-slices.tsv](milestone-7-f025-f026-slices.tsv) freezes
the ten identifiers and proposed final dispositions:

| Slice | Frozen IDs | Outcome | Dependency |
| --- | --- | --- | --- |
| `7.4b5b` | `STD-0759`, `STD-0760`, `STD-0790`, `STD-0791` | Make the core/binding adapter boundary framework-independent. | Accepted generic and Rust binding profiles plus `STD-0802`. |
| `7.4b5c` | `STD-0798`-`STD-0800` | Make binding handle and async adaptation consume the selected runtime/lifecycle capability. | `7.4b5b` and accepted Rust Async lifecycle. |
| `7.4b5d` | `STD-0781` | Canonicalize explicit typed executor delegation without catch-all fallback. | `7.4b5b` and accepted generic Concurrency. |
| `7.4b5e` | `STD-0822` | Preserve validated filesystem authority through the Rust operation. | Accepted generic Security filesystem contract. |
| `7.4b5f` | `STD-0825` | Bind listener connection work to capacity and lifecycle owners. | Accepted Rust Async lifecycle and `7.4b5e`. |

The slices are serial so the same canonical profiles and legacy sources never
have overlapping write ownership. Independent trust-boundary groups remain
queued until `7.4b5f` is accepted.

## Accepted Slice 7.4b5b: Binding Core And Adapter Boundary

**Outcome:** refine the Rust Language Binding profile and four legacy sections
so domain/core behavior has no binding-framework or host-runtime dependency,
while adapters own only the selected host representation and adaptation.

**Allowed write set:**

- `profiles/languages/rust/language-bindings.md`;
- `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/binding-architecture-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-binding-architecture.sh`;
- this decomposition checker for disposition and handoff state only;
- the parent trust/lifecycle checker for disposition-derived progress only;
- the accepted Rust Async lifecycle checker for removal of temporary finding-
  status assertions only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic topic, Rust Async or Security profile, runtime implementation,
binding framework configuration, workspace/Cargo file, generated artifact,
template, lockfile, host-language package, or downstream repository belongs to
this slice.

**Required semantics:**

- core domain behavior and types remain usable without a binding framework,
  generated host code, or foreign runtime;
- binding annotations on domain types are permitted only when they do not add
  a framework dependency or host-specific behavior to the core contract;
- wrapper/adapter modules depend on the core, never the reverse;
- optional binding support belongs to the adapter/package boundary rather than
  a core feature that changes domain behavior or dependencies;
- framework-free core verification remains required and is linked to the
  accepted `STD-0802` evidence without disposing that identifier again; and
- inability to maintain the boundary returns a typed planning or build
  diagnostic rather than merging layers for convenience.

**No fallback:** missing adapter, packaging, annotation, or framework support
cannot add a binding dependency to the core, move domain behavior into a
wrapper, skip framework-free core verification, hand-edit generated code, or
select another binding framework implicitly.

**Focused evidence:** decisions cover framework-free domain types, annotations
that do and do not couple the core, wrapper-to-core dependency direction,
adapter-scoped optional dependencies, missing adapter capability, and
framework-free core verification.

**Acceptance gate:** all four identifiers have exact dispositions; profile
metadata and routing remain valid; migrated legacy sections are bounded links
without competing architecture or feature defaults; later runtime, executor,
path, and listener sections remain untouched; `F025` remains accurately
partial; and focused plus affected regressions pass.

**Accepted result:** the Rust binding profile now owns a framework-independent
core/adapter boundary, one-way adapter dependency, adapter-scoped framework
features, generated-code ownership, and framework-free core verification.
Fifteen focused decisions and four exact dispositions prove the boundary
without moving runtime adaptation assigned to `7.4b5c`.

**Resolved re-plan trigger:** the parent trust/lifecycle checker treated its
accepted 90-ID trust and 42-ID Rust binding snapshot as immutable current
counts. Dispositioning this slice correctly changes the current counts to 86
and 38, so affected regression verification failed outside the original write
set.

**Approved correction:** retain the group fixture as historical baseline
evidence and derive current Rust binding, Rust Security, and total trust counts
from exact accepted identifiers in this decomposition map. The parent checker
accepts only the serial disposition states `0`, `4`, `7`, `8`, `9`, and `10`;
it does not own current slice sequencing or duplicate normative policy.

**Resolved second re-plan trigger:** the accepted Rust Async lifecycle checker
also asserted the temporary `7.4b4e` partial-resolution rows for both `F025`
and `F026`. Advancing `F025` in this slice made that historical checker own
mutable finding state outside its accepted behavioral contract.

**Second approved correction:** remove only those two temporary status
assertions and their now-unused file variable. The checker retains exact Rust
Async dispositions, profile behavior, migrated legacy evidence, accepted-plan
state, and decomposition linkage. Active dependent-Rust checkers own current
finding state.

## Later Slice Constraints

## Accepted Slice 7.4b5c: Binding Runtime And Handle Adaptation

**Outcome:** refine `STD-0798` through `STD-0800` so binding handles own only
host-visible handle lifetime and adaptation. Runtime construction, sharing,
task tracking, cancellation, and shutdown remain with the selected composition
and lifecycle owners.

**Allowed write set:**

- `profiles/languages/rust/language-bindings.md`;
- `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/binding-runtime-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-binding-runtime.sh`;
- the accepted binding architecture checker for removal of its temporary
  `F025` status assertion only;
- this decomposition checker for disposition and handoff state only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic topic, Rust Async or Security profile, runtime implementation,
binding framework configuration, workspace/Cargo file, generated artifact,
template, lockfile, host-language package, scheduler implementation, or
downstream repository belongs to this slice.

**Required semantics:**

- distinguish host-visible handle lifetime from runtime and task lifecycle;
- consume a composition-owned runtime capability without constructing,
  embedding as binding-owned state, replacing, or synchronously driving it;
- permit that runtime capability to remain loaded and shared across calls or
  workflow runs without making any requesting call or workflow its owner;
- keep each call's input, cancellation, result, and failure state scoped to
  that call and never carry them into later work because the runtime persists;
- expose a host-compatible asynchronous result or submit work through the
  accepted tracked lifecycle owner;
- release host handles according to their declared ownership without treating
  last-handle release as runtime shutdown authority; and
- return typed `unsupported` or `unavailable` when the selected host/runtime
  adaptation capability cannot be provided.

**No fallback:** missing runtime, host-async, handle, task-registration, or
result-delivery capability cannot create an embedded/global/alternate runtime,
call a synchronous runtime driver, block a host scheduler thread, detach work,
discard terminal outcomes, retain prior request state, or select another
binding mechanism.

**Focused evidence:** decisions cover shared runtime reuse across calls and
workflow runs, workflow persistence hints without ownership transfer,
request-scoped state, host-handle release, scoped await, tracked submission,
missing capabilities, binding/request-owned runtimes, retained prior input,
cancellation, and results, synchronous driving, alternate runtime creation,
detached tasks, and missing lifecycle registration.

**Acceptance gate:** all three identifiers have exact dispositions; profile
metadata and routing remain valid; migrated legacy sections are bounded links
without named runtime or blocking defaults; `F025` is resolved; later executor,
path, and listener sections remain untouched; and focused plus affected
regressions pass.

**Pre-slice review:** accepted. All three sections refine one canonical Rust
binding owner and consume the existing Rust Async owner without changing it.
The review found no split disposition, new owner, or objective change.

**Accepted result:** 22 focused decisions prove runtime reuse without
request-state carry-forward, handle/runtime ownership separation, scoped or
lifecycle-tracked work, typed capability failure, and no alternate-runtime,
synchronous-drive, blocking, detached-work, or alternate-binding fallback.
All three identifiers have exact dispositions and `F025` is resolved.

## Accepted Slice 7.4b5d: Explicit Executor Delegation

**Outcome:** refine `STD-0781` into the Rust binding specialization so a
composite executor delegates only the exact typed `unsupported` outcome
assigned by its contract. Delegation is a current-call routing decision, not a
general recovery strategy.

**Allowed write set:**

- `profiles/languages/rust/language-bindings.md`;
- `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/binding-executor-delegation-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-binding-executor-delegation.sh`;
- accepted Rust binding architecture/runtime checkers only to remove their
  temporary `Composite Executors` preservation assertions;
- this decomposition report and checker for accepted disposition and handoff
  state;
- consolidation dispositions, evaluation README, active plan, and execution
  ledger.

No generic Contracts or Concurrency topic, Rust Async profile, runtime or
executor implementation, binding framework configuration, workspace/Cargo
file, generated artifact, template, lockfile, host-language package, scheduler
implementation, finding status, or downstream repository belongs to this
slice.

**Required semantics:**

- define the exact typed `unsupported` variant that makes an operation eligible
  for the next executor;
- delegate only that variant and preserve validation, execution, cancellation,
  resource, lifecycle, and unavailable-capability outcomes as terminal;
- pass only the current call's already validated input to the selected next
  executor;
- keep delegated work within the scoped or lifecycle-tracked execution
  contract established by the accepted runtime/handle slice;
- return the selected typed outcome when the next executor or its required
  capability is unavailable; and
- keep successful local completion terminal without invoking another executor.

**No fallback:** a composite cannot catch every error, reinterpret a failure as
unsupported, retry with rebuilt/default/prior input, continue after
cancellation, select an alternate executor/runtime/binding mechanism, detach
delegated work, or discard the original typed outcome.

**Focused evidence:** decisions cover local completion, exact unsupported
delegation, unsupported without a delegate, unavailable delegate capability,
preserved invalid/execution/cancellation/resource/lifecycle/unavailable
outcomes, delegation attempts for each forbidden outcome, retained prior
input, invalid current input, catch-all recovery, retry, carry-forward, and
alternate-executor fallback.

**Acceptance gate:** `STD-0781` has one exact disposition; profile metadata and
routing remain valid; the legacy composite-executor section is a bounded link
without catch-all code or framework-specific mechanisms; prior runtime and
architecture gates no longer own temporary section-preservation state; later
path and listener sections remain untouched; `F026` remains accurately
partial; and focused plus affected regressions pass.

**Pre-slice review:** accepted. The section refines one canonical Rust binding
owner and consumes accepted Contracts, Concurrency, and runtime/handle
semantics without changing those owners. The review found no split
disposition, new owner, objective change, or fallback requirement.

**Accepted result:** 25 focused decisions prove successful local completion,
one exact unsupported delegation with current validated input, preservation of
all other typed outcomes, typed unavailable delegate capability, and no
catch-all, retry, carry-forward, default-input, alternate-executor, or detached
fallback. `STD-0781` has one exact disposition.

## Accepted Slice 7.4b5e: Rust Filesystem Authority Through Use

**Outcome:** refine `STD-0822` as a Rust specialization of generic Security.
Rust path validation produces authority that the filesystem operation must
preserve through use; a canonicalized `PathBuf` alone is not durable authority
when path components can change concurrently.

**Allowed write set:**

- `profiles/languages/rust/security.md`;
- `languages/rust/RUST-SECURITY-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/filesystem-authority-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-filesystem-authority.sh`;
- this decomposition report and checker for accepted disposition and handoff
  state;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic Security or Cross-Platform topic, Rust API/Interop/Unsafe profile,
runtime or filesystem implementation, dependency/configuration/lockfile,
generated artifact, platform recipe, template, host-language package, scheduler
implementation, or downstream repository belongs to this slice.

**Required semantics:**

- treat canonical identity and component containment as validation facts, not
  permanent authority to reopen a pathname;
- record whether concurrent component mutation is excluded, possible, or
  unknown for the complete validation/use interval;
- when mutation is possible, use a held file/directory capability,
  handle-relative operation, or equivalent platform mechanism through the
  operation;
- when mutation is excluded, immediate revalidation may satisfy the recorded
  threat model, but a stale or merely lexical path cannot;
- anchor creation to validated directory authority when concurrent mutation is
  possible; and
- return typed `invalid`, `unsupported`, or `unavailable` when containment,
  authority-preserving use, or required facts cannot be established.

**No fallback:** failed or incomplete authority cannot continue through a
plain/stale `PathBuf`, lexical prefix, ignored canonicalization failure,
revalidation under concurrent mutation, unanchored creation, alternate root,
or another filesystem mechanism selected only because the required one is
unavailable.

**Focused evidence:** decisions cover existing reads, anchored creation,
excluded and concurrent mutation, held and handle-relative authority,
immediate revalidation, stale/plain paths, escaped/unproven/unknown
containment, unknown mutation facts, unavailable authority mechanisms, and
plain-path, revalidation, lexical, alternate-root, and unanchored-creation
fallbacks.

**Acceptance gate:** `STD-0822` has one exact disposition; profile metadata and
routing remain valid; the legacy path section is a bounded link without
canonicalize-then-use code or pathname-authority defaults; generic filesystem
containment evidence remains unchanged and passes; later listener sections
remain untouched; `F026` remains partial only for listener lifecycle; and
focused plus affected regressions pass.

**Pre-slice review:** accepted. The section refines one canonical Rust Security
owner and consumes generic Security without changing it. The review found no
split disposition, new owner, objective change, platform-mechanism mandate, or
fallback requirement.

**Accepted result:** 19 focused decisions prove authority-preserving existing
use and creation, threat-model-qualified revalidation, typed invalid,
unsupported, and unavailable outcomes, and no plain/stale path, lexical,
concurrent-revalidation, alternate-root, or unanchored-creation fallback.
`STD-0822` has one exact disposition and `F026` remains partial only for
listener lifecycle.

### Slice 7.4b5f: Lifecycle-Owned Listener Work

Refine `STD-0825` so admission capacity and task lifecycle are distinct,
explicit owners. Acquire capacity at the correct acceptance boundary, register
connection work with the accepted lifecycle owner, observe terminal outcomes,
and include it in shutdown. Missing registration, capacity, cancellation, or
drain capability returns a typed outcome; it cannot detach a task, discard a
handle, or silently continue accepting work.

## Re-Plan Triggers

- An implicated section cannot be represented by one final disposition without
  splitting it across canonical owners.
- Binding adaptation requires changing generic Concurrency or Rust Async
  policy rather than consuming the accepted owner.
- Rust filesystem safety requires a generic Security change not already owned
  by the canonical topic.
- A focused checker cannot distinguish retained runtime capability from
  retained request/workflow input or state.
- Listener lifecycle proof requires a runtime-specific mechanism to become
  universal policy.
- Implementation would need an undisposed identifier, source, generated file,
  package file, lockfile, or downstream repository outside the activated write
  set.
