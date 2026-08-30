# Standards Engine A1c Execution Ledger

## 2026-08-29 - Planning Workspace Created

- The user requested an A1c plan workspace while explicitly stating that the
  complete plan is not ready to be written.
- The workspace is `Blocked` rather than `Planned` because the accepted A1/A1b
  audit found no concrete external caller or retained-state requirement from
  which to select handle lifetime, persistence, compatibility, recovery, or
  object granularity.
- Current write authority is limited to this plan directory and one
  product-contract discovery report. No runtime, contract, generated artifact,
  fixture, suite, policy graph, normative standard, A1b deletion, or A2 change
  is authorized.
- Accepted A1b implementation
  `84412f22fa9fe082f089eaa347c30c23f185ffee` remains the behavioral and
  evidence baseline. The accepted audit supplies constraints and experiments,
  not a binding A1c architecture.
- Routed guidance: Core, Router, Implementation, Verification, Planning,
  Documentation, Architecture, Contracts, Dependencies, and the conditional
  Persistence boundary. Concurrent Plan Integration is not applicable to this
  serial planning workspace.
- The next planning step is A1C-001 product-fact discovery. Architecture
  comparison, prototypes, implementation milestones, and acceptance claims are
  deferred until those facts are explicit.

## 2026-08-29 - Discovery Scaffold Standards Review

- Review found that the initial `Blocked` lifecycle made the only authorized
  fact-discovery work unavailable. The plan and Milestone 0 are now `Planned`;
  A1C-001 and A1C-002 block architecture and implementation admission rather
  than the bounded work that resolves them.
- The former candidate treatment of the four public operations and explicit
  uncertainty is superseded. They are inherited A1c behavioral constraints
  from the accepted A1/A1b audit; discovery selects their internal composition
  and promised lifetime, not whether those behaviors exist.
- The former composed-design result is superseded by `not-applicable` for the
  discovery-only slice. The complete probe becomes applicable when a candidate
  composition exists.
- The earlier routing note conditionally selected Persistence before a durable
  crossing was known. Current Persistence applicability is `unresolved`
  pending A1C-001; no Persistence policy is selected or rejected by this
  correction.
- Acceptance evidence contracts now distinguish caller workflow, public and
  persisted contract inventory, multi-component experiments, composed-design
  review, and plan completeness. The issues register now records affected
  boundaries, fix/defer dispositions, and required verification.
- Runtime source, schema, generated artifacts, fixtures, suites, policy graph,
  normative standards, A1b behavior, and all A2 work remain outside the write
  set.

## 2026-08-29 - Planning-Path Generated-Evidence Replan

- Generated freshness exposed that the initial scaffold commit added four Git-
  indexed planning paths without regenerating the suite-input projection. Its
  repository-index digest changed from
  `sha256:e1f14e48c2c401861256e44cb2f1092c18d94e3f9c42591fe6d94df5d93d41b7`
  to
  `sha256:87ce6b28b1d88202e9c3991de7a233960701759eddad6b11a5e94e8d88bb6b7a`.
- `Superseded`: the initial decision that all generated artifacts were outside
  Milestone 0, because it omitted the existing projection mechanically derived
  from tracked-path membership.
- Replacement: admit only
  `evaluation/standards-effectiveness/generated/suite-inputs.json` and require
  registry, suite, file-input, input-use, and contract fields to remain
  identical. A1c runtime, suite behavior, coverage policy, and normative
  standards remain unchanged.
- A1b claim schema v4 resolves current coverage requirements from stable
  subjects, so this freshness repair does not require rewriting authored
  attestations. A1C-007 retains the separate product/design question of whether
  A1c should preserve global suite-input invalidation.
- Commit `36de9b23b51072e7488672bcb7ccd6ed6b5a53cd` is unpushed and owned only by
  `main`. The user explicitly authorized its rewrite after identifying its
  missing rationale body. The original tip is protected at
  `refs/recovery/pre-a1c-scaffold-rewrite-20260829` until the corrected boundary
  is verified.
- Regeneration changed only `repository_index.digest`; registry, suite,
  file-input, input-use, and contract fields remained identical. Generated
  freshness, plan structure, diff hygiene, the three focused suites, all
  registered declarative suites, and every retained Bash checker passed.

## 2026-08-29 - First Caller Product Direction

- The product owner identified software-development agents acting for
  developers across projects as the intended Standards Engine user. Agents use
  the Python Interface to read and analyze standards while guiding software
  design.
- The accepted four operations supply the A1c interaction vocabulary:
  `query`, `prepare`, `resolve`, and `inspect`. Exact request/result values and
  retained handles still require workflow tracing; current implementation
  structure is not product demand by itself.
- Agents may also edit the Coding Standards corpus, but canonical mutation is
  not part of A1c's read-only authority. That workflow remains an A2 product
  input and does not activate A2 implementation in this plan.
- A1C-001 remains open for the Python Interface's process/deployment boundary,
  handle lifetime, non-derivable state, loss consequence, and operational
  owner. A1C-002 remains open for concrete current integrations and retained
  state.

## 2026-08-29 - Primary Harness Deployment

- The product owner selected a harness-managed tool call as the normal agent
  deployment. The harness invokes the Coding Standards Python Interface and
  presents the result to the agent.
- Direct import and in-process use remain possible, but are custom harness
  integrations. Their extra composition, scheduling, and lifecycle choices do
  not create a second A1c product contract.
- Multi-call workflows such as `query` then `inspect` and `prepare` then
  `resolve` require handles to remain usable across calls in one harness
  session. This fact does not yet require survival across harness or worker-
  process restart.
- The next product decision is restart lifetime. It determines whether session
  state may be memory-resident or whether non-derivable decisions need durable
  storage and an operational owner.

## 2026-08-29 - Fresh-Session Rerun Contract

- The product owner rejected mandatory continuity of prior analysis handles
  across harness or Python-worker restart. A1c does not enforce caller use of a
  prior handle.
- A caller may rerun from a new session and resupply prior decisions. A1c need
  not know that the new analysis repeats an earlier one, maintain a mutable
  head, or impose global supersession between runs.
- Loss of memory-resident analysis handles or decisions ends that session but
  does not corrupt standards authority. Continuity beyond the session is a
  caller or custom-harness feature.
- A fresh run still needs a way to select previously used immutable standards
  content. Discovery must now identify whether Coding Standards retains that
  content or the caller supplies it from an external authority such as source
  history or an archive.

## 2026-08-29 - Multi-Turn And Snapshot-Ownership Correction

- The product owner clarified that an agent turn or tool call is not a session.
  Agents make multi-turn, multi-step decisions and must not replay analysis
  between those steps.
- Coordinator agents may pass handles to authorized subagents. Coding Standards
  must resolve those handles through shared internal state; a subagent should
  not be forced to rediscover the same standards or reconstruct prior
  decisions. A handle remains a reference, not authorization.
- `Superseded`: the prior broad statement that session handles need not survive
  a Python-worker restart. Replacement: active workflow handles and decisions
  survive turns, calls, worker boundaries, and coordinator/subagent handoff.
  If the agent instance itself ends, a replacement agent may start a fresh
  independent analysis without inferred rerun lineage.
- Coding Standards owns immutable snapshot content and its handle resolution.
  Git can supply starting bytes when no snapshot exists, but Git commits are
  not snapshot identities and callers do not manually retain or resubmit raw
  snapshot content.
- Snapshot compatibility across Coding Standards engine versions is not a
  product promise. An incompatible stored snapshot must be rejected explicitly
  rather than interpreted through fallback behavior.
- Persistence is now required for internal snapshots and active workflow
  continuity. The storage mechanism, object granularity, retention, cleanup,
  backup, restore, and interruption guarantees remain unselected.

## 2026-08-29 - Invocation And Agent-Workflow Terminology

- The product owner clarified that `session` depends on perspective and is too
  ambiguous for a compatibility or persistence promise.
- An **engine invocation** is one tool request handled by one Coding Standards
  process. In the normal harness deployment that process may terminate after
  returning the result.
- An **agent workflow** is the multi-turn, multi-step activity that can span
  many engine invocations and authorized coordinator/subagent participants.
- An **agent instance** is one running agent context. Its replacement may begin
  an independent analysis over a retained snapshot without inheriting analysis
  lineage.
- Therefore active workflow handles and decisions require Coding Standards-
  owned storage across normal process termination. Direct in-process custom
  integrations may optimize the mechanism but do not weaken or broaden that
  public behavior.

## 2026-08-29 - Explicit Snapshot Retention Replan

- The product owner requires every snapshot to remain available until an
  authorized caller explicitly deletes it. Coding Standards has no reliable
  basis for inferring that externally held handles or future reruns no longer
  need a snapshot.
- Automatic expiry by age, inactivity, process exit, agent replacement,
  apparent lack of internal references, or storage pressure is rejected.
- This selects a concrete durable-retention boundary and activates the plan's
  persistence re-plan trigger. It does not select SQLite, table layout,
  universal child storage, backup/restore, or another mechanism.
- Explicit deletion is operational state lifecycle, not standards-authoring
  semantics. It must not be hidden inside `query`, `prepare`, `resolve`, or
  `inspect`, and it does not activate A2.
- A1C-010 now owns the unresolved behavior when active analyses reference the
  snapshot and whether analysis state has a corresponding explicit cleanup
  operation. Architecture and runtime implementation remain unavailable until
  that product contract is selected.

## 2026-08-29 - Unified Snapshot And Proposal View

- The product owner selected one immutable public snapshot abstraction for
  canonical standards and proposed standards views. A caller uses the same
  navigation, read, inspection, and analysis behavior regardless of storage
  representation.
- An edit creates a new logical snapshot. Internally the store may represent it
  as complete content or as a parent snapshot plus an immutable overlay, but
  the overlay is not a public artifact or operation family.
- Internal overlay storage must not use Git or embed repositories. Git remains
  an Adapter for obtaining initial source bytes and later exporting a reviewed
  proposal as a patch or pull request.
- Proposed snapshots must pass the same applicable corpus, metadata, graph,
  contract, and verification authority as canonical standards. An overlay-
  specific validation shortcut is rejected.
- Authorized deletion of one snapshot also deletes every descendant snapshot
  that depends on it. The remaining A1C-010 decision is what happens to active
  analyses referencing any snapshot in that deletion lineage and the exact
  operational deletion Interface.
- This decision establishes product behavior and storage constraints only. It
  does not select SQLite, overlay encoding, table layout, A1c runtime changes,
  or A2 authoring implementation.

## 2026-08-29 - Snapshot And Change-Set Terminology Correction

- `Superseded`: the preceding interpretation that a proposed view is another
  logical snapshot which might be internally stored as a parent plus overlay.
- A **snapshot** is instead a complete immutable Coding Standards-owned copy of
  canonical standards at one selected Git commit. The commit is provenance;
  the store does not embed Git and the snapshot handle is owned by Coding
  Standards.
- A **change set** stores proposed edits linked to the active snapshot. It does
  not copy or mutate the complete standards corpus. Operations project the
  snapshot plus change set as one coherent working view and apply the same
  corpus, metadata, graph, contract, and verification authority as canonical
  content.
- Deleting a snapshot deletes every linked change set. Active-analysis effects
  and the exact operational deletion Interface remain A1C-010 decisions.
- The product owner requires projects to retain a selected standards snapshot
  while adopting compatible engine updates. This supersedes the earlier broad
  no-cross-engine-snapshot-compatibility assumption and activates A1C-006.
  The exact compatibility window, migration policy, and unsupported-old-state
  result remain unselected.
- Git remains an Adapter for initial canonical input and eventual patch or pull
  request export. No Git repository or Git object model belongs inside the
  snapshot/change-set store.

## 2026-08-29 - Snapshot-Owned Aggregate Lifecycle

- The product owner requires a snapshot, every linked change set, and every
  analysis or artifact whose validity depends on either to remain together as
  one lifecycle aggregate.
- Authorized snapshot deletion atomically removes that complete aggregate.
  Analyses do not remain as unavailable shells, and callers do not enumerate or
  clean up dependent handles individually.
- If snapshot movement, backup, restore, or machine transfer is supported, the
  same exact aggregate moves together. Partial movement based on caller guesses
  is invalid.
- Individual artifacts may remain inspectable through handles, but those
  handles do not create independent retention, deletion, or transfer
  lifecycles.
- This selects aggregate ownership, not a physical schema. SQLite, one-file-
  per-snapshot storage, shared tables, export representation, publication, and
  recovery mechanics remain unselected.
- A1C-010 now owns only the explicit operational deletion Interface and its
  authorization, idempotence, unavailable-handle, result, and interruption
  contracts. A1C-003 owns physical storage and recovery experiments.

## 2026-08-29 - Recoverable Deletion Candidate

- The product owner identified accidental aggregate deletion as a reason to
  consider bounded restoration before committing to immediate physical purge.
- This is a candidate, not yet a binding requirement. The leading model is
  `active -> quarantined -> purged`, with `quarantined -> active` restoration
  before expiry.
- Quarantine would remove the complete aggregate from ordinary listing and use
  while preserving it for one narrowly authorized restore operation. Restore
  must recover the entire aggregate with the same identities; partial child
  restoration is invalid.
- Automatic purge after quarantine does not contradict explicit retention. The
  caller's deletion authorized that delayed consequence; it is not inferred
  from age, reachability, inactivity, process exit, or storage pressure.
- One declared retention policy is preferred over caller-selected durations.
  Immediate-purge need, policy ownership, upgrade compatibility during
  quarantine, and exact result semantics remain unresolved.
- Quarantine is not operational backup/restore and must not silently make
  deleted authority available to normal read or analysis operations.

## 2026-08-29 - Quarantine Selected; Backup Excluded

- The product owner confirmed that bounded quarantine and undelete are the
  intended protection against accidental snapshot deletion.
- Snapshot deletion removes the complete aggregate from active listing and use,
  preserves it through one declared quarantine window, and atomically purges it
  at expiry. Authorized undelete before expiry restores the complete aggregate.
- Use **undelete** for this lifecycle operation. Backup and restore refer to
  storage-loss recovery and are not part of the Standards Engine Interface.
- File administrators own archival and disaster recovery. They may copy a
  closed consistent store or use storage-aware backup tools. The engine owns
  transactional publication, crash consistency, and documentation of the exact
  file closure; it does not own scheduling, retention, or restoration of
  backups.
- This supersedes treating immediate purge versus quarantine as an open product
  choice and removes an engine backup/restore subsystem from A1c candidates.
  Quarantine duration and policy ownership, optional immediate purge, upgrade
  behavior, and exact operation results remain unresolved.

## 2026-08-29 - Quarantine Duration And Configuration

- The product owner selected a seven-day default quarantine duration.
- A deployment owner may override the duration through configuration files.
  Agents cannot inspect or modify the setting through the Python Interface and
  deletion requests cannot select their own duration.
- Each deletion records its exact purge deadline from the effective policy.
  Later configuration changes affect only future deletions and do not rewrite
  prior lifecycle decisions.
- This keeps retention authority outside agent semantics while avoiding an
  unexplained fixed implementation constant. Exact configuration format and
  path remain mechanism decisions for the later implementation plan.
- Expiry enforcement and physical purge scheduling, invalid configuration,
  optional immediate purge, upgrade compatibility, and exact operation results
  remain unresolved.

## 2026-08-29 - Immediate Purge Rejected

- The product owner rejected an immediate irreversible purge operation.
- Every deletion follows one lifecycle: atomically quarantine the complete
  snapshot aggregate, permit authorized undelete until its recorded deadline,
  then purge irreversibly at expiry.
- Agents cannot bypass quarantine through another operation, request option,
  zero-duration override, or child-level deletion.
- This removes a second destructive path and its authorization, result, and
  verification contracts. Expiry enforcement, invalid configuration, upgrade
  compatibility, and exact delete/undelete results remain unresolved.

## 2026-08-29 - Snapshot Lifecycle Contract Selected

- The product owner accepted `delete_snapshot` and `undelete_snapshot` as the
  only snapshot lifecycle operations.
- Deletion authorizes and atomically quarantines the complete active aggregate,
  records its fixed deadline, and returns that deadline. Repeating deletion is
  idempotent and cannot extend quarantine.
- Ordinary operations reject addressed quarantined authority with
  `SNAPSHOT.QUARANTINED`. Authorized undelete before the deadline restores the
  complete aggregate with identical snapshot and child handles.
- At the deadline the aggregate is logically expired and undelete returns
  `SNAPSHOT.EXPIRED`. A later invocation purges bytes transactionally; no
  background service is required.
- Missing duration configuration uses seven days. Invalid explicit
  configuration rejects and does not silently select the default.
- A1C-010 is resolved as a product decision. A1C-003 owns storage, atomicity,
  clock, physical cleanup, and expired-handle experiments; A1C-006 owns engine-
  upgrade behavior for active and quarantined aggregates.

## 2026-08-29 - Compatibility, Semantics, Portability, And Platforms

- The product owner deferred cross-engine stored-state compatibility and
  migration until Coding Standards is feature complete. A1c makes no current
  overlap promise; stable-release planning must revisit it before users can
  depend on long-lived cross-version snapshots.
- The term semantic interpretation was rejected for engine behavior. Agents own
  understanding of standards meaning and semantic judgment. Coding Standards
  owns only declared mechanical parsing, validation, routing, identity, graph,
  typed applicability, storage, and projection contracts.
- Closed snapshot stores are machine-portable administrative units. Portability
  must not depend on source-machine paths, inode identity, POSIX metadata, or
  caller enumeration of snapshot children. Current authorization applies after
  reopening on the destination.
- Linux, Windows, and macOS are supported platform targets. Development
  currently occurs on Linux, but final support claims require real execution on
  all three systems. Retain the accepted CPython 3.11 and 3.12 baseline.
- A1C-006 and A1C-008 are resolved as product decisions. A1C-001 remains open
  only for representative workflow evidence and the current consumer/state
  inventory; A1C-003 owns portable-storage experiments.

## 2026-08-29 - Snapshot Bootstrap And Discovery Replan

- Current-tree revalidation at commit
  `2dbf7cf5313ce7d15292e8caf0a51ab20f5c9e0f`, tree
  `5dfd117dea873ba5dcdc955ec12abf22d6f3d68d`, found no independent non-test
  Engine consumer, persisted-state caller, operational backup/restore caller,
  package entrypoint, or retained database. A1C-002 is resolved with the
  bounded-empty search recorded in product discovery.
- Representative workflow tracing exposed a product-Interface gap: the four
  inherited read and analysis behaviors require an already-known authority
  handle, while the selected product must create and find retained snapshot
  roots across process and agent-instance loss.
- The agent does not select a Git commit. Snapshot creation captures the
  configured canonical standards repository's current commit through an
  internal Adapter and records that commit as provenance.
- The former treatment of the four inherited operations as the complete
  Interface is superseded. Their behavior remains required, while a bounded
  experiment will compare public shapes for snapshot creation, discovery,
  deletion, and undelete.
- This replan does not select final operation count, storage schema, or runtime
  implementation. It does not reopen deferred cross-engine compatibility or
  admit A2 authoring.

## 2026-08-29 - Snapshot Content And Lifecycle Identity Separation

- The product owner accepted separate canonical-content and snapshot-root
  identities. Exact canonical paths and bytes retain content-addressed
  identity; each snapshot creation receives an independently retained opaque
  lifecycle root.
- Two projects may therefore create snapshots from the same current canonical
  commit without sharing deletion, change-set, analysis, or quarantine
  authority. Internal storage may deduplicate their canonical bytes.
- The representative workflows now cover create and navigation, fresh-process
  discovery, multi-turn coordinator/subagent analysis, and deleting or
  undeleting one of two equal-content snapshot roots.
- Six bounded experiments are defined for snapshot Interface shape,
  content-versus-lifecycle identity, aggregate persistence, discovery summary,
  operation/version authority, and verification substitution. No final schema,
  storage layout, or production implementation is selected.
- A1C-001 and A1C-002 are resolved. Milestone 0 is Implemented; architecture
  selection remains unavailable until the experiment milestone is separately
  admitted with exact prototype paths and deciding evidence.

## 2026-08-29 - Architecture Experiment Scope Admitted

- Milestone 1 admits one self-contained Python snapshot-aggregate prototype
  and one results report under the A1c plan's `reports/` directory. The
  prototype is disposable design evidence and cannot become production or
  compatibility authority by location or reuse.
- The prototype may use standard-library SQLite in memory to exercise
  transactional ownership, but SQLite remains an experiment candidate rather
  than a selected production schema or storage contract.
- The admitted cases cover equal-content independent roots, discovery,
  quarantine, undelete, expiry, purge, cold reopen, aggregate child inspection,
  public Interface alternatives, representative change Locality, and evidence
  substitution.
- Production packages, canonical contracts, policy authority, standards,
  prompts, templates, registered fixtures, and A2 remain read-only.
- Adding the two tracked experiment paths will change the generated
  repository-index observation. Milestone 1 owns the corresponding mechanical
  suite-input regeneration after those paths are final; no suite semantics may
  change.
