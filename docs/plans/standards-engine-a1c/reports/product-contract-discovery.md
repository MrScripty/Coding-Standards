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
  authority or analysis value. These four behaviors remain the read and
  analysis Interface; they are not the complete snapshot-management Interface.
  Representative end-to-end sequences remain to be recorded.
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
standards content at the canonical repository's current commit when snapshot
creation occurs. The engine resolves that commit internally from its configured
canonical source. The agent cannot select a historical commit, repository path,
tree object, or raw content through the Coding Standards Interface. The source
commit is recorded provenance, while the opaque snapshot handle identifies the
Coding Standards-owned copy. A changed worktree or later canonical commit
cannot alter an existing snapshot.

A snapshot-linked change set stores proposed edits without copying or mutating
the complete snapshot. Operations resolve the complete projected view before
applying the same navigation, read, inspection, analysis, and verification
contracts used for canonical content. Snapshot and change-set representations
are portable across supported machines under the same engine storage contract.
Cross-engine compatibility and migration remain deferred until feature
completeness.

### Snapshot Creation And Discovery

The agent-facing product must support four snapshot-management behaviors in
addition to the existing read and analysis behaviors:

- create a snapshot from the canonical standards repository's current commit;
- find retained active snapshots without remembering every handle outside
  Coding Standards;
- delete one active snapshot aggregate into quarantine; and
- undelete one quarantined aggregate before its fixed deadline.

Creation accepts no caller-selected Git revision. Canonical-source selection,
exact commit resolution, and immutable byte capture belong to the deployment
and Git Adapter. A creation result returns the new snapshot handle and enough
provenance for an agent to distinguish retained snapshots. Discovery returns
stored snapshot roots and lifecycle metadata, not independent child-object
inventory. The exact Python method or tagged-operation shape remains a bounded
Interface experiment; overloading `query`, `inspect`, or repository constructors
is not an accepted substitute because those paths cannot own creation or
recover a forgotten handle after process termination.

This does not create a cross-engine compatibility promise. The current engine
contract may create, find, delete, and undelete its own stored snapshots;
opening the same store through a later incompatible engine remains deferred
until feature completeness.

### Snapshot And Content Identity

The product uses two identities because content equality and lifecycle
ownership answer different questions:

| Term | Meaning | Identity and ownership |
| --- | --- | --- |
| Canonical content | One exact immutable standards corpus captured from the configured canonical repository | Content-addressed by exact logical paths and bytes; may be physically shared by several snapshots |
| Snapshot root | One caller-visible retained copy of that corpus and the root of its dependent work | Receives an opaque store-assigned identity; owns its change sets, analyses, decisions, evidence, lifecycle state, and quarantine deadline |
| Snapshot aggregate | The snapshot root plus every value whose validity or retention depends on it | Identified mechanically from stored ownership links; moved, quarantined, undeleted, and purged as one unit |

Two snapshot creations while canonical standards remain at the same commit
produce two snapshot roots that may reference one deduplicated canonical-content
object. Their handles, change sets, analyses, and lifecycle decisions remain
independent. Quarantining one root cannot make the other unavailable.

This separation is not an exception to content identity. Canonical content is
still identified by content. A snapshot root represents a retained lifecycle
instance, so content equality is insufficient for its identity. Creation time,
source-machine paths, and Git object identity do not become semantic content
identity. The store may use a generated opaque instance identifier, but the
exact generation mechanism remains an experiment detail.

Agents address snapshots only through that unique opaque root ID. The content
hash remains an internal deduplication and integrity key; exposing or retaining
it cannot substitute for the root ID because equal content may have several
independent lifecycle owners.

Physical deduplication is internal. Purging a snapshot removes that root and
all solely owned aggregate values. Shared canonical content remains while
another active or quarantined snapshot owns it. The store must decide this
from exact transactional ownership records, not a caller-supplied object list
or a filesystem reachability guess.

## Representative Agent Workflows

These workflows define required behavior. Method names and result layouts are
experiment variables unless already fixed by the four inherited behaviors.

### Create And Navigate

1. An authorized agent requests snapshot creation without a Git revision,
   repository path, or raw standards content.
2. Coding Standards resolves the configured canonical repository's current
   commit, captures its exact canonical authority, validates the complete
   corpus, and creates one active snapshot root.
3. The result returns the snapshot handle and display provenance. A second
   creation at unchanged canonical content returns a distinct snapshot root;
   internal content bytes may be shared.
4. The agent supplies that snapshot handle to `query` with routing facts.
5. The returned reading plan, later `query` reads, and `inspect` calls remain
   bound to the same snapshot root. No operation falls back to a newer
   canonical commit.

### Find And Resume After Process Or Agent Loss

1. A later engine invocation starts without a remembered snapshot handle.
2. An authorized discovery request returns active snapshot-root summaries from
   the configured store. It does not expose child storage objects.
3. Each summary supplies the unique opaque handle, active lifecycle state, and
   contextual provenance. The handle, not content hash, path, project label,
   commit, or timestamp, addresses the root and allocates dependent work.
4. The agent selects a root and starts a fresh `query` or `prepare`. Coding
   Standards does not infer that this is a rerun and does not require a prior
   analysis handle.

### Multi-Turn Analysis And Handoff

1. The agent selects accepted and proposed snapshot or projected-view handles
   and calls `prepare` with declared changes and semantic proposals.
2. A pending result returns one analysis handle plus only current material
   requirements, obligations, reading guidance, and next operations.
3. A coordinator may pass the analysis handle to an authorized subagent. The
   subagent calls `inspect` for needed detail and `resolve` with evidence-backed
   decisions; possession of the handle does not grant authority.
4. Every successful decision produces an immutable successor analysis. A
   different valid decision can branch from the same parent without global
   supersession.
5. A complete result remains bound to its snapshot aggregate. Losing the agent
   process does not lose accepted non-derivable decisions.

### Delete And Undelete One Of Two Equal-Content Snapshots

1. Two active snapshot roots reference identical canonical content and own
   different dependent analyses.
2. An authorized caller deletes one root. Coding Standards atomically marks
   only that aggregate quarantined and returns its fixed purge deadline.
3. Normal discovery excludes the quarantined root; ordinary operations against
   it or its children return `SNAPSHOT.QUARANTINED`. The other equal-content
   root remains active and usable.
4. A narrowly authorized lifecycle discovery can find quarantined roots so an
   agent that lost the deletion result can still request undelete.
5. Undelete before the deadline restores the complete aggregate with identical
   handles. Repeated delete or undelete is deterministic and does not extend
   the deadline.
6. At the deadline the aggregate is logically expired. A later invocation
   purges it transactionally without deleting canonical content still owned by
   another root.

## Bounded Architecture Experiments

The experiments compare behavior and ownership; they do not authorize final
runtime implementation.

| ID | Question | Compared designs | Deciding evidence |
| --- | --- | --- | --- |
| A1C-E1 | What is the smallest clear snapshot-management Interface for agents? | One tagged snapshot-management operation versus explicit create/find/delete/undelete methods over one internal Snapshot Module | Execute every representative workflow; compare caller knowledge, authorization dispatch, generated algebra, failure ownership, and the change path for adding one lifecycle result field |
| A1C-E2 | Can content identity and lifecycle identity remain separate without duplicating authority? | Content-addressed canonical content plus opaque snapshot roots versus content-only snapshot identity | Create two roots over equal content, attach different children, quarantine one, undelete it, purge it, and prove the other root and shared content remain valid |
| A1C-E3 | What aggregate persistence shape supplies required replay with less machinery than A1b? | Snapshot-owned aggregate records with derived projections versus independently durable storage for every inspectable child | Cold process query/analysis/inspection, child-handle resolution, aggregate deletion, deletion test, and representative change Locality |
| A1C-E4 | Which snapshot summary fields are genuinely required? | Unique handle/lifecycle/provenance summary versus content hashes or optional caller-authored display metadata | Address several same-content and different-content roots by unique ID without exposing paths, storage objects, project inference, or semantic claims |
| A1C-E5 | Which operation/version authority remains necessary? | A1b's per-operation stored authority objects versus domain-owned compatibility constants projected through one facade contract | Change one navigation behavior, one snapshot lifecycle result, and one analysis decision; record every Module and identity that must change |
| A1C-E6 | Which accepted verification machinery remains necessary after aggregation? | Current direct-object, package-governance, closure, and coverage evidence versus claim-matched substitutes at the deeper aggregate Interface | Claim-level failure injection, external-schema oracle preservation, cold reconstruction, deletion results, and evidence-substitution analysis |

Experiment implementations must use temporary or separately admitted prototype
paths. They cannot modify A1b production packages, canonical contracts, policy
authority, or A2 code under the discovery milestone. Exact prototype paths and
commands belong to the next plan revision.

## Post-Experiment A1b Guarantee Classification

| A1b guarantee or mechanism | A1c disposition | Reason |
| --- | --- | --- |
| `query`, `prepare`, `resolve`, and `inspect` behavior | required | Representative navigation and multi-turn analysis workflows require them |
| Typed results, explicit uncertainty, and no valid-looking fallback | required | Agents must distinguish unavailable, invalid, unsupported, unauthorized, and unresolved outcomes |
| Maintained Draft 2020-12 validator | required | A1 reproduced that local agreement is not external conformance |
| Separate schema equality, domain equality, and identity | required | They answer different contracts and A1 conflation caused a demonstrated defect |
| Immutable snapshot content and analysis branching | required | Cross-invocation workflows and coordinator/subagent handoff cannot depend on mutable ambient authority |
| Coding Standards-owned durable state | required | Normal tool deployment terminates after each request and retains non-derivable decisions |
| One independently stored object per inspectable child | replace | No independent child lifecycle exists; store the owning input/decision aggregate once and derive child inspection indexes and projections |
| SQLite | selected candidate | The disposable probe demonstrated the required current-version transactions, cold reopen, closed-copy portability, shared-content ownership, and interruption rollback; the exact production schema remains implementation-plan work |
| Engine backup/restore Interface | unnecessary | File administration owns backup; quarantine owns accidental deletion |
| Cross-engine state migration | deferred | No release or overlap contract exists before feature completeness |
| Linux-only native capture and publication | insufficient | A1c targets Linux, Windows, and macOS; design cannot embed POSIX identity |
| Exact coverage replay and byte-complete global invalidation | split | Preserve exact current-engine replay from immutable snapshots and retained decisions; use typed dependency-local coverage identity and keep repository-global freshness outside product identity |
| Custom governed-source interpreter | unnecessary as product authority | Repository architecture discipline remains Verification-owned, but the incumbent mechanism has no independent Standards Engine caller and must justify its own continued evidence cost |

## Current-Tree Consumer And State Revalidation

**Observation boundary:** commit
`2dbf7cf5313ce7d15292e8caf0a51ab20f5c9e0f`, tree
`5dfd117dea873ba5dcdc955ec12abf22d6f3d68d`.

The current tree preserves the accepted audit's bounded-empty consumer result:

- no non-test Python source outside `tools/standards_engine/standards_engine/`
  imports or constructs `StandardsEngine`;
- `AgentToolFacade` remains the only production caller of `query`, `prepare`,
  `resolve`, and `inspect`;
- the Standards Engine and Standards Authority package manifests declare no
  repository entrypoint, CLI, service, or foreign-language binding;
- `open_persisted` has no non-test caller;
- SQLite backup and restore have no operational caller; and
- no Git-tracked or worktree `.db`, `.sqlite`, or `.sqlite3` state was found.

The search covered non-test Python imports and call sites, package manifests,
README operational claims, tracked and present database filenames, default
store references, and recovery call sites. Tests, fixtures, plans, reports, and
generated declarations remain evidence or repository-process consumers rather
than independent product consumers.

The exact current-tree commands were run from the repository root:

```bash
rg -l --glob '!**/tests/**' --glob '!**/fixtures/**' \
  --glob '!docs/plans/**' \
  'from tools\.standards_engine|import tools\.standards_engine|from standards_engine|import standards_engine|StandardsEngine\(' .
rg -n --glob '!**/tests/**' --glob '!**/fixtures/**' \
  'open_persisted|SQLiteAnalysisStateStore|AnalysisStateStore|backup|restore' tools
rg -n 'standards_engine|standards-engine|StandardsEngine' \
  tools/*/pyproject.toml tools/*/README.md \
  evaluation/standards-effectiveness/*.toml
git ls-files '*.db' '*.sqlite' '*.sqlite3' '.standards-engine/**'
find . -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -print
```

Empty output from the first, fourth, and fifth commands established only the
bounded absence described above. It does not prove that an unregistered
external harness or privately retained store does not exist.

The current implementation creates a durable store at
`.standards-engine/authority.sqlite3` through `open_repository`, exposes the
selected view as a process object's property, and can reopen a store only when
the caller already supplies the store path and view handle. Its object store
has direct get and put behavior but no snapshot enumeration, aggregate
quarantine, deletion, or undelete contract. This is current implementation
evidence, not authority for A1c's design.

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
