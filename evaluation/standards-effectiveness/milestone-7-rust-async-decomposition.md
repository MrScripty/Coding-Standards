# Milestone 7 Rust Async Decomposition

## Purpose

This planning report decomposes the Rust Async lifecycle bridge after generic
Concurrency ownership was accepted. It is planning evidence, not a normative
Rust, runtime, lifecycle, or observability owner.

Only the first implementation slice is fully specified. Later slices have
frozen ownership and dependency boundaries but require a fresh pre-slice review
before their implementation contracts become active.

## Trigger And Evidence

The nine remaining Rust Async identifiers mix four independently verifiable
concerns:

- profile applicability and the sync/async boundary;
- runtime, spawned-task, and graceful-shutdown ownership;
- blocking-work isolation and mutex selection; and
- cancellation safety and lifecycle observability.

Moving them together would couple routing, ownership, synchronization, and
operational evidence in one commit. The source also contains defaults that
cannot become canonical unchanged:

- synchronous cores and synchronous library APIs are preferences only when
  the operation contract does not require asynchronous behavior;
- one named runtime, task container, cancellation primitive, mutex, or
  inspection tool is not a universal Rust mechanism;
- a timeout does not by itself authorize force-aborting work whose consistency
  contract cannot tolerate interruption;
- blocking-pool delegation does not imply that already-running work is
  cancellable; and
- dropping a Rust future stops polling that future but does not prove that an
  external side effect or delegated operation was cancelled.

These defects are recorded as `F045`. They must be refined, not preserved as
compatibility guidance.

## Ownership Boundaries

| Owner | Authority |
| --- | --- |
| `topics/concurrency.md` | Generic coordination, nonblocking paths, work/failure ownership, cancellation propagation, and typed no-fallback outcomes. |
| `profiles/languages/rust/README.md` | Baseline Rust routing and invariants. |
| `profiles/languages/rust/async.md` | Rust mechanisms that specialize the generic concurrency contract. |
| composition root selected by the adopting project | Concrete runtime construction, configuration, and shutdown wiring. |
| application or service lifecycle owner | Tracked task sets, admission closure, draining, cancellation, and completion/failure observation. |

The Rust Async profile does not own domain policy, host-binding adaptation,
generic concurrency rules, or a project-specific runtime singleton. A binding
profile may adapt a host entrypoint to the selected runtime owner, but it may
not create a competing runtime or task lifecycle.

## Slice Map

[milestone-7-rust-async-slices.tsv](milestone-7-rust-async-slices.tsv) freezes
all nine identifiers and their proposed final dispositions:

| Slice | Frozen IDs | Outcome | Dependency |
| --- | --- | --- | --- |
| `7.4b4d` | `STD-0717`-`STD-0718` | Establish Rust Async applicability and sync/async boundary selection. | Accepted generic Concurrency and base Rust profile. |
| `7.4b4e` | `STD-0719`-`STD-0721` | Specialize runtime, task, and graceful-shutdown ownership. | `7.4b4d`. |
| `7.4b4f` | `STD-0722`-`STD-0723` | Specialize blocking-work isolation and mutex selection. | `7.4b4d`; accepted lifecycle owner must remain authoritative. |
| `7.4b4g` | `STD-0724`-`STD-0725` | Specialize cancellation safety and lifecycle observability. | `7.4b4e` and `7.4b4f`. |

The slices are serial. After `7.4b4g`, dependent Rust Security and Rust
Language Binding sections must be decomposed against the accepted owner before
they move.

## Next Slice 7.4b4d: Rust Async Foundation

**Outcome:** create `profiles/languages/rust/async.md` as the routed Rust
specialization for async boundary selection without moving runtime, task,
shutdown, blocking, mutex, cancellation, or observability mechanisms.

**Allowed write set:**

- `profiles/languages/rust/async.md` (new);
- `profiles/languages/rust/README.md`;
- `languages/rust/RUST-ASYNC-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/rust/async-boundary-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-async-boundary.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic topic, other Rust specialization, binding profile, launcher,
generated artifact, template, lockfile, Cargo file, runtime integration, or
downstream repository belongs to this slice.

**Required semantics:**

- select synchronous or asynchronous APIs from the operation contract, actual
  I/O/concurrency behavior, callers, and cancellation/lifecycle obligations;
- keep pure parsing, validation, transformation, and policy synchronous when
  asynchronous behavior is not part of their contract;
- permit an asynchronous core or library API when the contract genuinely owns
  concurrent I/O, streaming, backpressure, cancellation, or async resource
  lifetimes;
- do not add `async` merely to match a caller or remove it merely to satisfy a
  blanket synchronous-core preference;
- specialize `topic.concurrency` and the base Rust profile without restating
  generic lifecycle policy; and
- return the operation's typed `unsupported` or `unavailable` outcome when its
  required execution contract cannot be provided.

**No fallback:** unresolved execution requirements cannot choose sync, async, a
thread, a runtime, blocking, or detached work by convenience. The foundation
slice cannot introduce runtime creation or task-lifecycle mechanisms assigned
to later slices.

**Focused evidence:** decisions cover pure synchronous logic, async I/O shells,
async behavior central to the contract, functions with no suspension point,
synchronous and asynchronous library contracts, unknown requirements, and
non-Rust/generic-only exclusions.

**Acceptance gate:** both identifiers have exact dispositions; metadata and
routing select the specialization only for Rust async concerns; the legacy
sections are bounded links without competing defaults; later mechanism
sections remain untouched; and focused plus affected regressions pass.

## Later Slice Constraints

### 7.4b4e: Owned Runtime, Tasks, And Shutdown

Refine `STD-0719` through `STD-0721`. Composition owns runtime construction;
each spawned task has a tracked lifecycle/failure owner; shutdown closes
admission before draining; cancellation and abort behavior follow operation
consistency; and inability to complete the lifecycle returns typed outcomes.
Evidence must reject global-library runtimes, discarded handles, unobserved
panics, silent detach, and unauthorized force-abort fallback.

### 7.4b4f: Blocking And Mutex Mechanisms

Refine `STD-0722` and `STD-0723`. Select async equivalents, blocking
isolation, and synchronization from actual runtime capabilities, cancellation
semantics, critical-section behavior, contention, and invariants. Evidence must
reject blocking on runtime threads, guards across suspension when unsupported,
callbacks under locks, universal mutex choices, and alternate-executor
fallback.

### 7.4b4g: Cancellation Safety And Observability

Refine `STD-0724` and `STD-0725`. Distinguish future polling cancellation from
external-operation cancellation; protect durable multi-step invariants with
transactional, idempotent, resumable, or compensating designs; and assign
health, panic, cancellation, and shutdown evidence to the lifecycle owner.
Named inspection tools remain optional reference mechanisms. Evidence must
reject assumed external cancellation, async cleanup delegated only to `Drop`,
leaf-only logging, silent worker death, and tool availability presented as
proof.

## Re-plan Triggers

- A frozen section must split across canonical owners and one disposition
  cannot represent the split.
- The Rust specialization would need to weaken generic Concurrency.
- A runtime or binding adapter would become the implicit lifecycle owner.
- Correctness requires a project-specific runtime, executor, timeout, mutex, or
  telemetry tool in generic Rust guidance.
- A slice needs another Rust specialization, generated artifact, package file,
  or downstream repository outside its approved write set.
- Verification cannot distinguish a typed unavailable mechanism from an
  alternate-runtime, blocking, detached-work, abort, or observability fallback.
