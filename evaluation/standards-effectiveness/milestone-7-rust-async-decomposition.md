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

## Accepted Slice 7.4b4e: Owned Runtime, Tasks, And Shutdown

**Outcome:** refine `STD-0719` through `STD-0721` in the existing Rust Async
profile. Composition owns runtime construction, spawned work has one tracked
lifecycle/failure owner, and shutdown follows an explicit admission,
cancellation, drain, and completion contract.

**Allowed write set:**

- `profiles/languages/rust/async.md`;
- `languages/rust/RUST-ASYNC-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/async-lifecycle-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-async-lifecycle.sh`;
- `evaluation/standards-effectiveness/verify-rust-async-boundary.sh`
  (lifecycle-handoff assertion only);
- `evaluation/standards-effectiveness/verify-concurrency-policy.sh`
  (historical next-slice assertion only);
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generic topic, base Rust profile, other Rust specialization, binding
profile, launcher, generated artifact, template, lockfile, Cargo file, runtime
integration, or downstream repository belongs to this slice.

**Required semantics:**

- the adopting application's composition root owns runtime construction,
  configuration, sharing, and shutdown;
- libraries consume an injected runtime capability or expose an async contract
  without creating a process-global or alternate runtime;
- every spawned task is registered with one lifecycle owner that observes
  completion, failure, panic, and cancellation;
- shutdown stops admission before signalling cancellation and draining tracked
  work;
- time limits and abort are selected from the operation consistency contract,
  and abort is permitted only when authority and interruption safety are
  established;
- repeated shutdown is idempotent or returns the same typed terminal outcome;
  and
- unavailable ownership, runtime capability, or safe shutdown completion
  returns the operation's typed outcome.

**No fallback:** missing lifecycle proof cannot create a library-global or
alternate runtime, discard a task handle, detach work, treat leaf logging as
ownership, silently lose panic/failure, keep admission open while draining, or
force-abort work without authority and interruption safety.

**Focused evidence:** decisions cover composition-owned and missing runtimes,
library-global and alternate runtime rejection, tracked and detached tasks,
observed and discarded failures/panics, admission closure, complete and
incomplete drains, authorized safe abort, unauthorized/unsafe force abort,
idempotent repeated shutdown, and unavailable lifecycle capability.

**Acceptance gate:** all three identifiers have exact dispositions; the Rust
Async profile specializes generic ownership without selecting one runtime,
task container, cancellation primitive, or timeout; migrated legacy sections
are bounded links; later blocking, mutex, cancellation-safety, and
observability sections remain untouched; `F025`, `F026`, and `F045` accurately
record partial resolution; and focused plus affected regressions pass.

**Resolved re-plan trigger:** implementation proved the new lifecycle policy
and parent handoff, but the affected `verify-rust-async-boundary.sh` checker
hard-codes `7.4b4e` as the next slice after the foundation is already
accepted. That checker was outside the original activated write set.

**Approved re-plan decision:** the write set is narrowly expanded to include
only the prior boundary checker's redundant hard-coded next-slice assertion.
That assertion is removed; the checker continues to require `7.4b4d`
acceptance and delegates current sequencing to the canonical Rust Async
decomposition checker. No policy, fixture, disposition, or other verification
scope is added.

**Resolved second re-plan trigger:** the full regression suite reached
`verify-concurrency-policy.sh`, whose historical acceptance checker hard-codes
`7.4b4c` as the repository's current next slice. The new lifecycle checker
also hard-codes `7.4b4f`, which would repeat the same ownership defect after
the next accepted slice.

**Second approved re-plan decision:** remove only those two mutable
current-sequence assertions. Both policy checkers retain their accepted-slice,
finding, fixture, disposition, metadata, routing, and regression assertions.
The canonical Rust Async decomposition checker remains the sole owner of the
first planned Rust Async slice. No generic policy or broader checker refactor
is authorized.

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
