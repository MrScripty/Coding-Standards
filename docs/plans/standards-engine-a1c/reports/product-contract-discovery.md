# A1c Product-Contract Discovery

**Status:** `Open`

## Purpose

Record the product facts that must exist before A1c selects architecture,
persistence, compatibility, platform, or verification machinery. This report
does not choose an A1c design and does not authorize implementation.

## Current Evidence

The accepted [A1/A1b audit synthesis](../../standards-engine-a1-a1b-audit/reports/final-synthesis.md)
found no independent external Standards Engine consumer, retained A1 state,
non-test persisted-state caller, or operational backup/restore caller at its
fixed observations. A1b nevertheless supplies strong durable child-object
replay and operational recovery because its accepted plan selected those
guarantees.

Those observations motivate discovery; they are not current product decisions.

The product owner subsequently identified software-development agents acting
for developers across projects as the intended user. Agents consume the Coding
Standards through the Python Interface while designing and changing software.
This is product direction, not evidence that any particular current package,
process model, persistence mechanism, or handle lifetime is required.

## Required Product Facts

### First Caller

- Caller identity and owner: software-development agents acting on behalf of
  developers; product requirements are owned by the Standards Engine product
  owner, while each agent integration owns its use of the Python Interface.
- Human or software workflow served: guide software design and implementation
  across different projects by selecting, reading, inspecting, and analyzing
  the applicable Coding Standards.
- Public operation sequence: `query` selects or reads applicable authority;
  `prepare` begins standards-change analysis; `resolve` supplies an authorized
  decision to an existing analysis; and `inspect` retrieves an addressed
  authority or analysis value. Representative end-to-end sequences remain to
  be recorded.
- Inputs controlled by the caller: project/task routing facts and query
  requests; selected accepted and proposed authority for analysis; declared
  changes; and authorized submissions with required evidence.
- Outputs or handles retained by the caller: navigation/read results, typed
  analysis results, analysis handles, inspectable handles, and typed rejection
  results. Handles must survive multiple turns and may be handed from a
  coordinator to an authorized subagent during one workflow.
- Failure and uncertainty outcomes the caller must distinguish: unavailable
  authority or evidence, unsupported behavior, invalid input or authority,
  unauthorized decisions, and explicit unresolved facts or obligations. Exact
  public variants remain governed by the accepted contract until superseded.

### Editing Boundary

Agents are also intended to edit the Coding Standards corpus. A1c remains the
read-only navigation and analysis capability: it can describe applicable
standards and analyze a proposed change, but it does not mutate canonical
authority. Controlled authoring is an A2 concern and requires its own product
contract, lifecycle, and implementation admission. The shared Python access
mechanism does not merge read and mutation authority.

A snapshot is a complete immutable copy of the canonical standards at one Git
commit. Authoring does not edit that copy and does not create another complete
copy for every change. It stores a non-Git change set linked to the active
snapshot. The projected working view is the complete snapshot with those
additions, modifications, moves, or deletions applied.

Callers navigate, read, inspect, and analyze the projected view as one coherent
standards corpus. The fact that part of the view comes from a stored change set
must not create different operation semantics. The projected view must pass
the same applicable corpus, metadata, graph, contract, and verification
authority used for canonical standards; it cannot gain eligibility from a
weaker change-set validator. Exporting an accepted change set as a Git patch or
pull request is a repository Adapter concern. The snapshot and change-set
store must not embed Git repositories or use Git objects as its internal
model.

### Deployment

- Deployment form: primarily a harness-managed tool call backed by the Python
  Interface. Direct Python-package embedding is supported as a custom harness
  integration rather than a separate product mode.
- Process boundary: normally one engine invocation handles one tool request and
  the Coding Standards process terminates after returning the result. The
  public contract therefore requires internal stored state to resolve handles
  across later invocations. A custom harness may embed the Python
  implementation, but that mechanism must not change request/result semantics
  or create a second lifecycle contract.
- Repository and worktree boundary: agents apply guidance to many project
  repositories. Those projects are caller context, not Coding Standards
  authority. Reading accepted standards and proposing edits to the Coding
  Standards corpus are distinct authority operations.
- Machine and user-account boundary: a closed snapshot store is portable as one
  complete file-administration unit. Reopening it must not depend on the source
  machine, native path separators, inode identity, or ambient repository state.
  Authorization remains current to the receiving deployment and is not granted
  by possession of copied handles or files.
- Upgrade and rollback boundary: no cross-engine stored-state compatibility
  promise is required before Coding Standards reaches feature completeness.
  Compatibility and migration policy must be revisited before stable release;
  current work must not accidentally claim indefinite compatibility.
- Independently deployed components: the agent, Standards Engine, and standards
  corpus may evolve independently. Standards-content snapshots are portable,
  but support for opening them with another engine version is deferred until
  feature completeness.

### Handle Lifetime

The contract uses these distinct terms:

- **Engine invocation:** one Coding Standards process handling one tool request.
- **Agent workflow:** one multi-turn, multi-step activity, potentially involving
  a coordinator and subagents.
- **Agent instance:** one running agent context.

For each handle family the caller actually uses, record whether it must survive:

| Boundary | Required | Caller workflow and consequence |
| --- | --- | --- |
| Agent turn or step | required | `query` -> `inspect` and `prepare` -> `resolve` span multiple decisions; replay between turns is not acceptable. |
| Coordinator-to-subagent handoff | required | An authorized subagent may receive and resolve a coordinator-provided handle rather than rediscovering authority. |
| Engine invocation/process termination | required during an active workflow | Normal tool use may start a new Coding Standards process for every request; handles cannot be process-local. |
| Agent instance replacement | analysis continuity not required; snapshot access required | A new agent may start an independent analysis against the internally retained snapshot; A1c need not infer rerun lineage. |
| Repository content change | required for snapshot handles | Coding Standards resolves the prior immutable snapshot independently of changed working-tree or Git content. |
| Coding Standards engine upgrade | deferred until feature completeness | A1c makes no current cross-version stored-state promise. Stable-release planning must decide compatibility and migration before users rely on it. |
| Machine transfer | required for a closed store under one supported engine contract | File administration moves the complete store; snapshot aggregates cannot require caller enumeration or depend on source-machine filesystem identity. |
| Authorization/provider change | current authorization required | Passing a handle does not authorize access; current authority decides whether the recipient may resolve or act on it. |

### State And Loss

| State or decision | Derivable from canonical inputs | Required retention | Consequence of loss | Operational owner |
| --- | --- | --- | --- | --- |
| Navigation result | yes, from selected standards content and request | active multi-turn workflow when referenced by later work | Rerun the query if it is not retained. | Coding Standards store while retained; caller controls use |
| Analysis requirements and obligations | yes, from selected snapshots or projected change-set views, request, and retained decisions | with the owning snapshot aggregate | Forced replay or rediscovery interrupts the agent workflow. | Coding Standards snapshot aggregate |
| Agent observations and dispositions | no | with the owning snapshot aggregate; no independent lifetime after that snapshot is deleted | Loss during the workflow forces repeated semantic decisions; a fresh agent may resupply them in a new run. | Coding Standards snapshot aggregate |
| Immutable standards snapshot content | no, once captured from mutable or externally unavailable source bytes | retained until an authorized caller explicitly deletes it; no inferred expiry | The same standards authority cannot be selected for a fresh run. | Coding Standards snapshot store; caller authorizes deletion |
| Snapshot-linked change set | no, once its edits and accepted proposal decisions exist only in Coding Standards storage | retained with its base snapshot until explicitly removed or the base snapshot is deleted | The proposed standards view and any dependent review or analysis cannot be reproduced. | Coding Standards change-set store; authoring authority remains A2 |

### Workflow And Rerun Semantics

An agent workflow may span many turns, steps, engine invocations, and authorized
coordinator/subagent participants. That is one continuity scope: handles and
accepted decisions remain available without replay even though each engine
process may terminate after its request. A handle identifies stored state but
does not grant authority.

If the agent instance ends, a replacement agent may start an independent
analysis over a Coding Standards-owned prior snapshot. A1c does not require a
prior analysis handle, infer rerun lineage, or coordinate one mutable global
head between the two analyses.

### Snapshot Authority

Coding Standards captures and owns a complete immutable copy of canonical
standards content at a selected Git commit. The source commit is provenance,
while the opaque snapshot handle identifies the Coding Standards-owned copy.
Callers do not retain or resubmit raw snapshot content, and a changed worktree
or later canonical commit cannot alter an existing snapshot.

A snapshot-linked change set stores proposed edits without copying or mutating
the complete snapshot. Operations resolve the complete projected view before
applying the same navigation, read, inspection, analysis, and verification
contracts used for canonical content. Snapshot and change-set representations
are portable across supported machines under the same engine storage contract.
Cross-engine compatibility and migration remain deferred until feature
completeness.

### Semantic-Understanding Boundary

Coding Standards does not infer the meaning of prose, determine whether a
software change semantically satisfies a standard, or replace agent judgment.
The agent using the Interface owns semantic understanding and supplies required
observations, evidence, and dispositions.

The engine owns only declared mechanical contracts: parsing and validation,
canonical identity, routing, graph traversal, typed applicability evaluation,
storage lifecycle, and deterministic projection of supplied authority and
decisions. Engine-upgrade compatibility therefore concerns those mechanical
contracts and stored representations, not an engine-owned semantic
interpretation.

### Snapshot Aggregate

Each snapshot owns one complete dependency closure: its linked change sets and
every analysis, accepted decision, evidence record, inspection artifact, or
other stored value whose validity depends on that snapshot or a projected
change-set view. This aggregate is the lifecycle and movement unit. It does not
require one physical file, database, or table, but the storage owner must be
able to identify the closure exactly without caller-supplied object lists or
reachability guesses.

Individual child handles may remain inspectable. They do not acquire an
independent retention, deletion, backup, restore, or transfer lifecycle outside
their owning snapshot aggregate.

### Retention And Deletion

Coding Standards retains snapshot content until an authorized caller
explicitly deletes it. Process termination, agent replacement, age, inactivity,
storage pressure, and an apparent absence of internal references do not prove
that no external caller still retains the handle. The product therefore has no
automatic snapshot expiration or reachability-only garbage collection.

Deleting a snapshot atomically deletes its complete aggregate, including every
linked change set and every analysis or artifact that references the snapshot
or one of its projected views. The store must not retain an unusable dependent
value, silently materialize a change set as a new snapshot, or ask the caller
to discover and delete children individually.

The leading operation design is one explicit snapshot-root deletion command;
child handles are never deletion targets. Its exact authorization, idempotence,
and result contract remain unresolved. Deletion is not one of the four read-
only analysis operations and is not A2 canonical-standards authoring.

### Recoverable Deletion

Because one snapshot aggregate can contain non-derivable change sets, decisions,
and evidence, immediate physical deletion imposes avoidable accidental-loss
risk. The selected lifecycle is:

```text
active -> quarantined -> purged
             |
             +-> restored -> active
```

Deleting an active snapshot atomically quarantines its
complete aggregate. Normal standards listing, navigation, analysis, and child-
handle resolution no longer expose it. A narrowly authorized lifecycle
operation can restore the complete aggregate before expiry, preserving its
snapshot and child identities. Expiry then purges the aggregate atomically.

The expiry is not an inference that the caller no longer needs active data. It
is a delayed consequence explicitly authorized by the original deletion and
governed by one declared retention policy. The default quarantine duration is
seven days. A deployment owner may change that duration through a configuration
file; agents cannot read or modify it through the Python Interface and cannot
select a per-deletion duration.

Deletion records the exact purge deadline from the effective policy at that
time. A later configuration change affects future deletions only. Partial child
restoration and hidden fallback to quarantined authority are not part of the
contract. The public lifecycle term is **undelete**, not restore, to keep this
operation distinct from administrative storage recovery. Undelete behavior
across engine upgrades remains a compatibility decision. There is no immediate-
purge operation; every deletion receives the same quarantine protection before
irreversible expiry.

The selected operation behavior is:

- `delete_snapshot` accepts only an active snapshot root, authorizes the action,
  atomically quarantines its aggregate, and returns its fixed purge deadline.
- Repeating deletion against the quarantined snapshot is idempotent and does
  not reset or extend the deadline.
- Normal operations do not use quarantined authority and return the typed
  `SNAPSHOT.QUARANTINED` result when its handle is addressed.
- `undelete_snapshot` authorizes and atomically restores the complete aggregate
  with the same snapshot and child handles before the deadline.
- At the deadline the aggregate becomes logically expired. Undelete returns
  `SNAPSHOT.EXPIRED`, and a later engine invocation physically purges the
  aggregate transactionally without a background service.
- A missing configuration value uses seven days. An invalid explicit value is
  a configuration error and never silently falls back to the default.

### Administrative Storage Recovery

Coding Standards does not provide a product-level backup or restore Interface.
Protecting against disk loss, database corruption, machine loss, or archival
requirements belongs to file administration. An operator may copy the complete
closed store or use storage-aware backup tooling.

The engine still owns transactional publication, crash consistency, and a
documented storage closure so administrative tools do not have to guess which
files belong together. Copying a live or partially published store is not a
supported recovery procedure. Quarantine does not protect against loss of the
underlying storage.

### Compatibility

- Independently evolving producers and consumers: agent harnesses, engine code,
  standards snapshots, and snapshot-linked change sets.
- Required overlap window: none before feature completeness; revisit before a
  stable release.
- Persisted or exchanged representations: the closed snapshot store containing
  complete snapshot aggregates.
- Unsupported old-state behavior: no silent fallback; exact typed behavior
  belongs to the future compatibility decision.
- Migration, replacement, or no-compatibility rationale: deferred because the
  product remains structurally changeable and no current caller requires cross-
  version state.

### Platform

- Supported operating systems: Linux, Windows, and macOS.
- Supported filesystems: ordinary supported local filesystems on those
  operating systems; no POSIX-only inode, permission, locking, or path behavior
  may enter portable storage identity.
- Supported architectures: those supported by the selected Python runtime and
  maintained dependencies; no narrower product requirement is currently known.
- Supported Python runtimes: retain the current CPython 3.11 and 3.12 baseline.
- Required-real capabilities: development currently occurs on Linux. Final
  cross-platform support claims require real Windows and macOS execution in
  addition to Linux; local Linux-only success cannot certify those targets.

## Evidence Inputs For Plan-Owned Decisions

The plan owns A1c constraints and hypotheses. This report records the evidence
available to those decisions and must not become a second authority for their
disposition.

| Area | Current evidence | Missing evidence |
| --- | --- | --- |
| Public behavior | The accepted audit binds four read-only operations with typed request/result/rejection behavior and explicit uncertainty without valid-looking fallback. | Caller workflows must identify the minimum values, handles, and lifetime needed to deliver those behaviors. |
| Schema semantics | A1 repairs demonstrated that local Draft interpretation can agree internally while violating the selected external contract. | None for the requirement to use the selected maintained validator; later experiments must determine Adapter depth and internal representation. |
| Equality and identity | A1 repairs demonstrated that schema equality, domain equality, identity encoding, ordering, and deduplication have different semantics and owners. | Candidate locality probes must show where those owners compose without duplicating authority. |
| Immutable results | The accepted audit requires no ambient substitution within the handle lifetime A1c promises. | The caller and deployment facts must establish that promised lifetime and whether immutable branching is externally observable. |
| Child lookup and durable publication | A1b supplies direct cold lookup for child objects, SQLite publication, backup, restore, and interruption behavior. | No current non-test caller, retention period, loss consequence, or recovery owner has yet been established. |
| Recoverable deletion | Snapshot deletion removes a complete aggregate that can include non-derivable work, making accidental loss consequential. | Product behavior is selected; later design must prove atomicity, deterministic time handling, and expired-handle identity without retaining deleted authority. |
| Administrative backup | File administration can copy a closed, transactionally consistent store or use storage-aware tooling. | No Standards Engine backup/restore Interface is required; later storage design must document the exact file closure and safe-copy boundary. |
| Historical coverage replay | A1b can bind broad coverage authority and replay historical evidence. | Product discovery must distinguish externally promised replay from repository-governance evidence. |
| Version scopes | A1b has independently scoped semantic and representation versions. | Actual independently evolving consumers and overlap windows remain unverified. |
| Governed-source interpretation | A1b enforces cross-package source constraints with repository-owned analysis. | A current threat, consumer failure, or contract requiring that mechanism remains unverified. |

## Discovery Completion

This report is complete only when every unresolved product fact is replaced by
evidence or an explicit unsupported/deferred decision, A1C-001 and A1C-002 are
resolved, and the plan can be re-planned with bounded design experiments. Empty
consumer or state results require a documented search boundary; they are not
proof merely because no current caller was found.
