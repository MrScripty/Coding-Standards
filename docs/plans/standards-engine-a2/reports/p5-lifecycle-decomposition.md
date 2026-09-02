# A2-P5 Lifecycle-First Decomposition Re-Plan

**Status:** `execution admitted from exact prototype base 8a0d7df08e68fddbd60a7e2f3d2e267036c827ae; no branch or worktree created`

## Trigger And Terminal Evidence

The combined P5 evidence implementation stopped before measurement. Its final
frozen source was 20,102 lines and 800,190 bytes with SHA-256
`2ea0e614494d9ad6034aab7bd9955c93e38f949486de08400584ffac7a87635f`.
All five focused modes passed on CPython 3.11 and 3.12, but independent
specification and Standards audits found that the real workload retained the
original owner after cold reopen, clone and store acquisition began outside
atomic ownership, and the process fixture did not prove ownership across the
`Popen` return-to-registration interval. The focused checks therefore proved a
helper path rather than the complete registered transition.

The failed primary source is preserved only on the isolated prototype history
at commit `c939f693660561833e4a079ad7ebe9d725fbabe2` and archive ref
`refs/archive/a2-prototypes/p5-efficiency-measurement`. Its clean task-owned
worktree and temporary branch were removed after archive verification. It was
never measured and never entered canonical `main`.

This is a systemic evidence-design finding. Process ownership, runtime
composition, persistence evolution, Authoring behavior, measurement,
independent recomputation, and external gates changed through one source and
allowed supporting checks to certify a different lifecycle path from the
measured workflow. The former correction admission and combined executable are
superseded. The accepted P2R2 material, P3 publication/recovery, and P4R
typed-continuation decisions are not rejected.

## Replacement Composition

P5 is replaced by two dependency-ordered questions:

1. **A2-P5L lifecycle ownership minimum viable test (MVT)** decides one private
   owner Module for scratch Git process acquisition, the one A1c-shaped
   Snapshot/SQLite owner, Engine lifetime, cold reopen, sequential post-close
   observation, and terminal cleanup. It makes no Authoring product,
   comparative resource, dominance, schema, migration, or production claim.
2. **A2-P5M combined measurement** remains unavailable until P5L passes and
   its exact owner Module source is immutable. A future durable P5M admission
   must add only a measurement driver that consumes that Module's Interface.
   It may not edit, copy, wrap, or independently reimplement lifecycle
   ownership, and it may not rebuild the accepted predecessor prototypes'
   general negative frameworks.

The dependency is one-way: the P5L owner Module does not know comparison
candidates, metrics, dominance, or report formats. Its MVT knows only the three
lifecycle Interface shapes and the registered lifecycle oracle. P5M may observe
an owned workflow but cannot start, reopen, inspect, or clean individual
resources. A P5M need that expands the P5L Interface or changes its
implementation rejects the proposed measurement shape and re-plans; it does
not reopen P5L in place.

## P5L Registered Question

Can one deep private owner Module make every required resource unreachable
outside one current generation, perform cold reopen without an unowned or stale
owner handoff, and preserve the primary failure while terminating all acquired
state?

The MVT compares three bounded Interface shapes:

- one persistent owner whose `reopen` transition replaces its current
  generation internally;
- a linear replacement owner that returns a new generation and requires the
  caller to transfer ownership; and
- a callback-scoped owner that retains all phase and reopen control.

No candidate is preferred by method, type, or line count. A candidate is
correctness-equivalent only if callers cannot retain a stale live generation,
no resource exists before an owner can dispose it, and the caller never owns
component cleanup order. The selected Interface must provide more lifecycle
Leverage than the facts and ordering it exposes.

## Four-Dimension Oracle

### Effectiveness

Using actual current A1c Snapshot/Engine construction, scratch SQLite, and
local Git, every candidate must execute this exact sequence:

1. acquire a scratch clone and one live generation `G1` under logical owner
   identity `O`;
2. call current
   `StandardsEngine.create_snapshot(CreateSnapshotCall.from_value({"kind":
   "create-snapshot"}))`, require a `CreateSnapshotResult`, retain its returned
   `ActiveSnapshotSummary` as `S`, and bind only its nested `SnapshotHandle` as
   `H = S.snapshot`;
3. call current `StandardsEngine.query(QueryCall(H, ReadRequest("read",
   "core")))`, require a `ReadResult`, and retain its complete
   `as_contract()` value as `R1`;
4. close `G1`, require one sequential read-only SQLite observation that `S`
   remains present while no writable connection or Engine is live, and reopen
   the same store as generation `G2` with no resource overlap;
5. call current `StandardsEngine.find_snapshots(FindSnapshotsCall.from_value(
   {"kind": "find-snapshots", "lifecycle": "active", "limit": 50}))`, require
   a `FindSnapshotsResult` whose sole scratch-store entry exactly equals
   `ActiveSnapshotSummary` `S`;
6. repeat the identical
   `StandardsEngine.query(QueryCall(H, ReadRequest("read", "core")))`, require
   `ReadResult` `R2`, and require `R2.as_contract()` to equal `R1`; and
7. reach one terminal owner state with no active store, process, process group,
   graph, connection, scratch path, or stale resource reference.

`O` is allocated before any owned resource. `G1` and `G2` are distinct,
monotonic owner-private generation identities bound to `O`; closing `G1`
irrevocably prevents further operation through it, reopening returns `G2`, and
the selected candidate must prove that `O`—not the caller or a retained `G1`
reference—controls `G2`. A candidate-specific transfer token is permitted only
for the linear comparison and must atomically invalidate the prior Interface;
an independently usable old owner or generation is `reject`.

The `O`/`G1`/`G2` values are opaque prototype evidence emitted in an immutable
transition record only after the corresponding transition. They cannot access,
operate, reopen, or clean a component and are counted in caller-visible state;
only the owner retains concrete resource identities and live references.

The caller receives one owner Interface and operation results. It does not
receive store/Engine/process cleanup responsibilities.

### Efficiency

For every candidate and runtime, the MVT records this complete vector:

- owner-Interface call count and the fixed four current A1c public calls;
- atomic caller-supplied field count, counted by named field occurrence at
  each call boundary rather than by object or serialized byte count;
- caller-visible resource identities, required ordering facts, cleanup
  branches, and owner/generation state values;
- A1c durable bytes as the SQLite database, WAL, and shared-memory file sizes
  after the initial operations, after closed-store observation, and after the
  reopened operations;
- total scratch bytes as the recursive regular-file byte total below the owned
  scratch root at the same three checkpoints.

Each deterministic structural count is derived once from the complete actual
trace for each candidate/runtime. Each byte checkpoint is observed once in a
fresh scratch root for each candidate/runtime; both runtime values are reported
without averaging or normalization. A differing value is not discarded and a
candidate cannot dominate if its durable or scratch value is worse on either
runtime after equivalent work. Wall time is not applicable: P5L has no owned
latency claim, budget, or timing-based Interface decision, so timing would have
no deciding value. Zero owner-specific product persistence remains invariant.
A candidate is dominated only when another correctness-equivalent candidate
exposes no more calls, fields, resources, ordering facts, cleanup branches, or
retained state and is strictly better on at least one of those structural
dimensions without worse durable or scratch observations. No weighted score,
repetition harness, or guessed resource budget is admitted.

### Correctness

Faults execute on the actual representative path before or after every
material boundary: owner creation, scratch allocation, each clone child,
process registration, store construction, Engine construction, operation body,
pre-reopen close, read-only observation, reopen construction, post-reopen
operation, and terminal close. Applicable catchable asynchronous
failure is injected across process creation and registration.

Every fault must preserve the exact primary cause, terminally dispose every
resource that could have been acquired, remove owned scratch state, leave no
active store or child/process group, and permit one fresh independent run. A
cleanup failure is diagnostic context only. The normal path must prove that
the exact `O`/`G1`/`G2` identities and public result sequence above hold. A
helper-only, simulated, labelled, differing-operation, or post-registration
fault is insufficient.

### Standards Compliance

The exact A1c route selects the current Core, Planning, Implementation,
Verification, Documentation, Commit, Build, Tooling, Release, Library,
Generated Contract, IPC, Persistence, Architecture, Contracts, Concurrency,
Resilience, Cross-Platform, Dependencies, Security, Diagnostics, and
Performance owners. Independent specification and Standards reviewers audit
one frozen bundle identity derived from both exact source paths before
execution. Their remit includes actual-path ownership, cause preservation,
process containment, deletion tests, and unnecessary machinery.

P5L passes only when all four dimensions pass unchanged on dependency-complete
Linux CPython 3.11 and 3.12. An unavailable real boundary is `revise`; stale or
overlapping ownership, residual state, masked cause, helper-only evidence,
unnecessary Interface knowledge, or a supported-runtime design failure is
`reject`. There is no correction cycle: either nonpassing verdict terminates
the P5L source and requires a new canonical re-plan.

## Composed-Design Admission

| Probe | Replacement disposition |
| --- | --- |
| Independent concerns | Lifecycle ownership and comparative measurement have different change reasons, evidence, and failure behavior. Accepted Authoring domain behavior remains a referenced dependency. |
| Required interleaving | The owner necessarily coordinates process, store, Engine, and reopen time. Metrics need only terminal observations through its Interface. Candidate and dominance policy do not enter the owner. The former collector graph is deleted. |
| Caller knowledge | The MVT and later driver know one owner Interface, operation results, typed failures, and opaque terminal transition evidence. Only the owner knows concrete resource order and identities, live generation references, cleanup, and observation gaps. |
| Representative change paths | A process-containment change touches only P5L. A metric or comparison change touches only future P5M. An A2 domain change returns to its canonical owner and invalidates dependent evidence rather than changing P5L. |
| Dependency direction | Current A1c values and Interfaces are stable inputs. SQLite and local Git are local-substitutable real dependencies. Fault seams remain private to the MVT. |
| Independent verification | P5L freezes, audits, and accepts before P5M is admitted. P5M cannot change the accepted owner identity. Each may fail or be deleted without becoming canonical Engine code. |
| Deletion result | Deleting the owner Module redistributes necessary lifecycle ordering and cleanup into every caller. Deleting the MVT removes only validation evidence. Deleting future P5M removes only the comparison. No collector, combiner, fault registry, or benchmark becomes permanent. |
| Cumulative machinery | The admitted executable scope is only the owner Module, one lifecycle MVT, and the mechanically derived branch projection. P5M source, report schema, candidate harness, and canonical integration remain absent. |

The replacement composed design is `applicable` and provisionally admissible
for execution from the exact base below. P5L acceptance decides a
prototype-only owner design, not a permanent production Module or public
Interface.

## Exact A1c Preservation Dispositions

| Accepted A1c decision or owner | P5L disposition | Executable preservation oracle |
| --- | --- | --- |
| A1C-U03 invocation and handoff lifetimes | `composed-without-change`: P5L tests close/reopen ownership; it does not alter public handle durability or make possession authoritative. | The exact public `SnapshotHandle` returned before close works after reopen, while `G1` does not. |
| A1C-U04 configured-`HEAD` capture | `unchanged`: the scratch repository is deployment/test configuration; no A1c call receives a path, ref, OID, commit, tree, or bytes. | Exact generated call fields for create, read, find, and repeated read contain none of those facts. |
| A1C-U06 current navigation semantics | `unchanged`: both generations execute the same current `read(core)` query through the current compiler and navigation path. | Complete generated `ReadResult` values `R1` and `R2` are equal; no projected or Authoring material enters P5L. |
| A1C-U12 and A1C-U20 eight explicit operation roots | `unchanged`: P5L invokes three existing roots and adds no public operation, overload, dispatch, or constructor-held public lifecycle state. | The current operation manifest and generated contract remain byte-identical; the other five roots remain present and unmodified. |
| A1C-U14 one Snapshot/SQLite owner | `composed-without-change`: the current `SnapshotModule` remains sole schema, durable aggregate, lifecycle, dependency, and index owner. P5L owns only the lifetime of its current instance and scratch path. | One SQLite database exists; all writes arise from current Engine calls; observation is read-only; no P5L table, codec, repository abstraction, or second store exists. |
| A1C-U15 one generated facade contract | `unchanged`: P5L consumes current generated request/result values and adds no schema or contract definition. | Generated-contract and package-input identities are unchanged on the prototype branch. |
| A1C-U18 supported runtimes | `composed-without-change`: lifecycle evidence claims only dependency-complete Linux CPython 3.11 and 3.12. | The identical frozen bundle and oracle pass separately on both runtimes; no other platform claim is made. |
| Accepted Engine composition root | `unchanged`: current `StandardsEngine` still composes `GitRepository`, `SnapshotModule`, compiler, navigation, and Analysis dependencies. The prototype owner is an outer test-lifecycle boundary, not an Engine replacement. | P5L imports and constructs the current Engine without editing, subclassing, wrapping, or copying its implementation. |
| Accepted Repository Git Adapter | `unchanged`: current `GitRepository` remains the Engine's sole repository-observation Adapter. The owner contains only scratch-clone process lifetime as test setup and exposes no repository facts through the A1c Interface. | Create reaches current `GitRepository` exactly once; both reads and post-reopen find replay Snapshot-owned captured content without a repository reread; no competing production Adapter or caller-supplied Git fact exists. |

Any disposition or oracle that cannot be proven on the frozen actual path is a
P5L rejection, not permission to alter A1c.

## Environment And Reproduction Contract

The only claimed environment is dependency-complete Linux with current local
Git and SQLite under CPython 3.11 and 3.12. The immutable repository input is
exact base `8a0d7df08e68fddbd60a7e2f3d2e267036c827ae`; each observation creates a
fresh local scratch clone, one scratch SQLite store, and no network or external
service. Git, Python, SQLite, filesystem type, and kernel versions are recorded
with every result. Windows, macOS, network clones, shared stores, concurrency,
throughput, and production resource behavior remain unclaimed.

After both source files are frozen and independently audited as one bundle,
the registered behavior command is run unchanged with each supported runtime:

```text
PYTHONDONTWRITEBYTECODE=1 python3.11 -P tools/standards_engine/tests/prototypes/a2/p5_lifecycle_ownership_mvt.py --all
PYTHONDONTWRITEBYTECODE=1 python3.12 -P tools/standards_engine/tests/prototypes/a2/p5_lifecycle_ownership_mvt.py --all
```

The MVT must also pass repository Ruff check and format verification for both
authored files, generated freshness, every declarative suite, exact branch
write-set and generated-digest review, sensitive-value review, and Commit
review. Supporting repository gates cannot override a P5L oracle failure.

## Isolation And Write Set

The intended private resources are:

- branch `prototype/a2-m0-lifecycle-ownership`;
- worktree `/tmp/coding-standards-a2-p5l-lifecycle-ownership`;
- owner source
  `tools/standards_engine/tests/prototypes/a2/p5_lifecycle_owner_prototype.py`;
- MVT source
  `tools/standards_engine/tests/prototypes/a2/p5_lifecycle_ownership_mvt.py`;
- branch-local generated
  `evaluation/standards-effectiveness/generated/suite-inputs.json`; and
- archive ref `refs/archive/a2-prototypes/p5l-lifecycle-ownership`, with
  expected terminal disposition `removed-archived`.

The exact admitted prototype base is
`8a0d7df08e68fddbd60a7e2f3d2e267036c827ae`. This durable re-plan binds the
question, paths, oracle, base, and terminal disposition before prototype
creation; Commit remains free to select the coherent boundary for this re-plan.
The prototype branch never merges to `main`. The two authored files must remain
excluded from production package inputs, and the generated projection may
change only its repository-index digest.

## Explicit Exclusions And Next Slice

P5L may not contain A2 proposal/revision/readiness/attempt implementations,
the former collector graph, full-corpus or aggregate measurement candidates,
dominance logic, a report combiner, external-gate bundle, the former
17-failure registry, public schema,
migration, compatibility reader, canonical Engine change, or a second
Snapshot/Analysis/persistence authority.

The next slice creates the registered isolated branch and worktree from the
exact admitted base, then authors only the owner Module and lifecycle MVT.
Future P5M, canonical Engine work, and all excluded machinery remain
unavailable.
