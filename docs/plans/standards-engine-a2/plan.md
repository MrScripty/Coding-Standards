# Plan: Standards Engine A2 Controlled Authoring

**Plan status:** `Active`

**Current phase:** Milestone 0 combined-design efficiency validation

**Next slice:** Correct and independently re-audit the isolated A2-P5
combined-efficiency prototype against its clarified execution admission before
any complete dual-runtime measurement; both supported runtimes must first pass
the focused contract, oracle, lifecycle, and report-integrity probes on the
same frozen source hash

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Formation audit:**
[A2 current-boundary and standards audit](reports/formation-and-standards-audit.md)

**A1c reauthorization:**
[Projected-material identity and replay](reports/a1c-projected-material-reauthorization.md)

**P4R decision record:**
[Facade-composition admission and terminal evidence](reports/p4r-facade-composition-admission.md)

**P5 execution admission:**
[Combined-design efficiency comparison and oracle](reports/p5-combined-efficiency-admission.md)

## Objective

Provide software-development agents with one controlled-authoring workflow that
creates and revises a non-Git standards proposal rooted in an immutable A1c
snapshot, reuses the accepted A1c navigation and analysis kernel, obtains
explicit apply authority, and publishes one verified change to the selected
canonical standards authority without exposing partial publication or guessing
at stale, interrupted, or unknown outcomes.

Every A2 design preserves the explicit user-selected A1c product and
architecture decisions except the one exact snapshot-only proposed-material
assumption the user reauthorized for projected-material identity validation on
2026-09-01. Milestone 0 owns the product, contract, architecture, and
design-validation facts required to make the A2 objective implementable. It
admits only isolated, disposable prototypes and minimum viable design tests; it
does not authorize production source, public contract, persisted-store, ADR,
or canonical-standards mutation.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A2-A1 | An authorized agent creates, discovers, revises, reads, and analyzes a durable proposal across process and agent-turn boundaries without supplying repository paths, Git objects, raw authority bytes, or independently duplicated analysis facts. | `user-workflow` | `representative` | `automated` | `pending` | pending |
| A2-A2 | Every proposal revision is immutable and binds its base snapshot, exact mutations, semantic-proposal material, and material contract identities; one durable proposal head advances only by compare-and-swap and rejects a stale expected head without altering another revision. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A2-A3 | Proposal navigation and impact analysis execute through the accepted A1c metadata, graph, applicability, policy-impact, coverage, and single-`AnalysisState` semantics; a current complete `AnalysisHandle` is reused rather than replaced by an A2 analyzer, packet, report lifecycle, or mutable analysis head. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A2-A4 | Apply readiness is a distinct immutable proof bound to the exact current proposal revision, complete analysis handle, required semantic, relationship, and lifecycle approvals, evidence, authorization authority, target authority, and verification contract; mutation or authority change invalidates only materially dependent proof. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A2-A5 | Application writes an isolated candidate, runs every required correctness proof against its exact bytes, publishes canonical authority only through the selected atomic expected-head transition, and returns success only after the published identity and postcondition are established. | `system` | `required-real` | `automated` | `pending` | pending |
| A2-A6 | Invalid input, unsupported contract or platform, unavailable authority, unauthorized action, stale proposal or target state, verification failure, interruption, and unknown publication outcome remain distinguishable; no path silently retries, rebases, rolls back, substitutes authority, or reports partial success. | `integration` | `repository-supported verification environments` | `automated` | `pending` | pending |
| A2-A7 | Durable proposal, head, readiness, attempt, and snapshot-dependent state have one owner, exact schema and version roles, atomic lifecycle and purge behavior, cold-process reconstruction, and an accepted A1c-store migration or typed-rejection decision derived from current consumers. | `system` | `required-real` | `automated` | `pending` | pending |
| A2-A8 | One canonical generated public contract governs every admitted authoring input, result, handle, operation capability, typed failure, Python model, agent-tool projection, example, and actual facade path; freshness, semantic conformance, and public behavior have separate deciding evidence. | `contract` | `repository-supported verification environments` | `automated` | `pending` | pending |
| A2-A9 | Real Linux CPython 3.11 and 3.12 evidence exercises cross-invocation proposal work, concurrent head and target changes, Git and SQLite behavior, authorization, verification failure, interruption recovery, and the complete public workflow. | `user-workflow` | `required-real` | `automated` | `pending` | pending |
| A2-A10 | One coherent candidate has complete implementation-consumer dispositions, exact policy-impact and coverage closure, focused and repository-wide verification, and independent Standards and specification acceptance. | `integration` | `not-applicable` | `manual` | `pending` | pending |
| A2-A11 | An exact preservation matrix demonstrates that every explicit user-selected A1c decision is unchanged or has one exact explicit user reauthorization with supersession scope and new acceptance evidence; each A2 responsibility is a non-conflicting composition, an A2-local addition, or unavailable. No plan, prototype, contract, migration, or implementation silently supersedes A1c. | `contract` | `not-applicable` | `manual` | `pending` | [Projected-material reauthorization](reports/a1c-projected-material-reauthorization.md) and pending independent reconciliation |
| A2-A12 | Before a material A2 design or procedure is admitted, a question-specific disposable prototype or minimum viable test records representative workflows, predeclared effectiveness criteria, an owned efficiency metric and comparison or budget, correctness invariants and negative cases, the current routed standards set, deciding oracles, limitations, and a pass, revise, or reject disposition. | `integration` | `representative` | `manual` | `pending` | pending |
| A2-A13 | No production Standards Engine source, public contract, canonical store, generated facade, or canonical standards authority changes before A2-A11 and every design-dependent A2-A12 record required by the exact implementation slice are accepted; prototype shells, fake success, test-only state, and scratch persistence remain unreachable from and absent from the canonical implementation. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A2-A14 | Every A2 plan, procedure, prototype-evidence, and implementation outcome is routed through the current applicable standards, passes claim-matched verification, receives exact staged-scope and sensitive-file review, and is recorded through a coherent conventional commit boundary selected by the Commit workflow without plan-owned commit topology. | `integration` | `repository-supported verification environments` | `manual` | `pending` | pending |

## Scope

### In Scope

- Current product and consumer discovery for controlled standards authoring.
- An exact preservation matrix for explicit user-selected A1c decisions and
  every proposed A2 interaction with them.
- Pre-canonical design validation through bounded, disposable prototypes and
  minimum viable tests of effectiveness, efficiency, correctness, and current
  standards compliance.
- One proposal lifecycle rooted in an immutable A1c `SnapshotHandle`.
- Non-Git change material, immutable revisions, and one durable mutable head.
- A complete projected standards view governed by the same semantic owners as
  accepted A1c content.
- Reuse of A1c `query`, `prepare`, `resolve`, `inspect`, `AnalysisState`,
  `AnalysisHandle`, decision reuse, coverage, and typed uncertainty semantics.
- Separately authorized semantic, relationship, lifecycle, mutation, and
  application decisions.
- Apply-readiness, isolated staging, verification, canonical publication,
  idempotency, interruption, and recovery contracts.
- Durable aggregate ownership, schema evolution, current-consumer migration or
  rejection, and snapshot quarantine, undelete, expiry, and purge effects.
- Generated Python and agent-tool contract evolution through the existing
  Standards Engine facade.
- Current Git dependency and Adapter assessment before any write-capable Git
  semantic surface is selected.
- Linux CPython 3.11 and 3.12 required-real behavior and independent final
  acceptance.
- Commit-governed isolation, staged review, verification, evidence capture,
  and terminal disposition for plans, procedures, prototypes, and development.

### Out Of Scope

- Production implementation during Milestone 0.
- Changing, weakening, reinterpreting, or silently superseding an explicit
  user-selected A1c design decision outside the exact projected-material
  identity reauthorization recorded by this plan.
- Treating an unvalidated design as implementation authority or placing
  prototype-only source, fake state, scratch stores, or test scaffolding in the
  canonical Standards Engine implementation.
- A second navigation, applicability, impact, coverage, or analysis authority.
- Automated judgment of arbitrary prose meaning or generated semantic
  acceptance.
- Caller-selected repository paths, commits, refs, Git object IDs, store paths,
  raw patches, raw snapshot bytes, or immediate destructive purge.
- Treating a proposal revision as an accepted canonical snapshot merely to
  reuse the current public shape.
- Plan C external-project baselines, project bindings, and standards-upgrade
  analysis.
- Windows or macOS support claims without equivalent real-platform evidence.
- Engine backup and restore, cross-store merge, speculative compatibility
  readers, or indefinite cross-engine state migration.
- A production GUI, prose command language, autonomous pull-request policy, or
  release publication. Bounded prototype efficiency measurements do not create
  a production performance promise.

## Constraints And Assumptions

### Constraints

- The current accepted A1c architecture and its corrective revalidation are
  the implementation baseline. Historical A1 packet, report, authority-view,
  and A1b persistence mechanisms are evidence, not fallback design authority.
- Explicit user-selected A1c decisions are immutable inputs to A2 unless the
  user separately and exactly reauthorizes one through an A1c re-plan. The
  2026-09-01 authority covers only replacement of snapshot-only proposed
  analysis material with an exact immutable projected-revision reference. A2
  acceptance, prototype evidence, convenience, or implementation pressure
  cannot broaden that authority.
- The user authorized formation of a standards-compliant proposal, not
  production implementation or canonical standards mutation.
- Milestone 0 is the only admitted discovery scope. No production edit is
  available until the A1c preservation matrix and every applicable design
  validation record are accepted, Milestone 0 is accepted, this plan is
  re-planned with one exact implementation slice and write set, and the
  required implementation operation is explicitly admitted.
- A material design or procedure requires the smallest adequate pre-canonical
  prototype or minimum viable test. Its record names the question, claim,
  representative workload or scenario, oracle, effectiveness criterion,
  efficiency metric and comparison or budget, correctness invariants,
  standards route, limitations, and decision threshold before execution.
  Missing or failed evidence blocks or rejects the design rather than being
  waived by review or replaced by a weaker check.
- Prototype source is experimental evidence, not production input. It remains
  isolated from the canonical integration branch, uses only scratch or
  disposable state, is trivial to run, exposes relevant state, and is never
  copied wholesale into production. Only an independently reviewed decision
  and the smallest validated logic may inform a later admitted implementation.
- Every repository mutation follows the current routed standards and Commit
  workflow. Plans do not prescribe commit count or topology; Commit owns the
  coherent boundary, exact staging, sensitive-file review, verification,
  conventional message, branch/worktree lifecycle, and evidence record.
- The active Generic Standards Verification Engine migration must publish its
  required fresh graph audit before A2 freezes verifier consumers, graph
  relationships, coverage subjects, generated projections, or acceptance
  totals.
- Work is serial. Product proposal-head concurrency selects Concurrency, not
  the Concurrent Plan Integration profile. That profile remains inapplicable
  unless multiple development proposals can actually become stale before
  integration.
- Generated freshness, local implementation agreement, a successful Git
  command, a SQLite commit, or a passing verifier process proves only its named
  property and cannot independently establish product success.

### Assumptions

- Software-development agents acting for developers remain the first caller,
  and a harness-managed Python tool call remains the primary deployment. The
  A2 product owner validates this in Milestone 0.
- Linux on CPython 3.11 and 3.12 remains the initial supported platform. The
  Platform owner validates every new Git, filesystem, locking, persistence,
  and process behavior on both versions.
- A proposal depends on one retained snapshot root and participates in that
  root's aggregate quarantine and purge lifecycle. The product and Persistence
  owners must determine whether any independent proposal abandonment lifecycle
  has a real caller before selecting it.
- The current repository may have A1c stores or public consumers created after
  the historical empty inventory. The Contracts owner must perform a fresh
  bounded inventory rather than inheriting the old absence finding.
- The selected canonical publication outcome is an atomic expected-target
  update of the configured Coding Standards `refs/heads/main`. Only an exact
  observed verified candidate at that ref is `applied`; external artifacts or
  submissions are distinct non-application outcomes.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| This plan is the sole current planning authority for A2. The Plan A1 brief's controlled-authoring passages remain historical discovery evidence and must be interpreted through current A1c terminology. | Planning owner | [Formation audit](reports/formation-and-standards-audit.md) and the historical brief's non-authorizing status | Scattered future-A2 notes as an apparent proposal |
| Treat every explicit user-selected A1c product and architecture decision as a protected inherited contract unless an exact later user decision reauthorizes it through an A1c re-plan. The 2026-09-01 reauthorization is limited to projected-material Analysis identity and replay; every other A1c choice remains protected. | User and A1c product owner | Accepted [A1c binding decisions](../standards-engine-a1c/plan.md#binding-decisions), the [formation audit](reports/formation-and-standards-audit.md#a1c-user-decision-preservation-boundary), and the [exact reauthorization](reports/a1c-projected-material-reauthorization.md) | A blanket prohibition on any A1c reconsideration, and A2 ownership treated as authority to reopen unrelated A1c choices |
| Evolve the snapshot-only proposed input of one immutable `AnalysisState` into one exact immutable proposed-material reference whose closed variants identify either an accepted snapshot or a projected proposal revision. Include that reference in Analysis identity, typed dependency closure, and cold replay; a proposal revision is not snapshot authority. This decision authorizes prototype-first validation, not canonical implementation or ADR amendment. | User, A1c product owner, Analysis, Authoring, and Architecture owners | [P2R terminal evidence](reports/prototype-evidence-index.md#a2-p2r-projected-analysis-identity-and-replay) and [projected-material reauthorization](reports/a1c-projected-material-reauthorization.md) | A1c proposed analysis material restricted to `SnapshotId` and the prior P2R product-reauthorization blocker |
| Preserve A1c snapshot immutability, unique lifecycle roots, generated facade, single aggregate `AnalysisState`, deterministic pending and complete projections, exact dependency-local coverage, opaque handles, and typed failures. Use one private material-resolution seam with snapshot and projected-revision Adapters feeding the same compiler and Analysis kernel; do not create a second analysis authority or public generic material Interface. | A2 product and Architecture owners | Accepted [A1c ADR](../../decisions/standards-engine-a1c.md), [corrective plan](../standards-engine-a1c-repair/plan.md), and the [deep Module composition](reports/a1c-projected-material-reauthorization.md#selected-composition) | Pre-A1c packet/report designs, proposal-as-snapshot, mutable analysis, composite external handles, or a second authoring-analysis state |
| Store proposed edits as non-Git change material rooted in one immutable A1c snapshot. A revision owns exact proposed content and semantic-proposal material but is not accepted canonical authority. | Authoring and Snapshot owners | Accepted [A1c product decision](../standards-engine-a1c/plan.md#binding-decisions) | Embedded Git repositories, full corpus copies per edit, or proposal-as-accepted-snapshot |
| Keep revisions immutable and content-bound while one proposal lifecycle root owns a durable mutable head. Advance the head only from an exact expected revision through compare-and-swap; keep A1c analysis transitions immutable and branchable. | Authoring, Concurrency, and Persistence owners | Accepted [A1 single-state replan](../standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md) | Mutable packet/report supersession or a mutable analysis head |
| Bind apply readiness to the current complete A1c `AnalysisHandle`; do not store or accept an independently authored completion Boolean. Semantic, relationship, and lifecycle acceptance remain separately authorized authoring decisions. | Authoring and Analysis owners | Current A1c contract and historical A2 separation rationale | `CompletedAnalysisReport`, packet completeness, or analysis completion as apply authority |
| Treat controlled authoring as one coherent responsibility and evaluate one deep Authoring Module whose Interface hides revision identity, head coordination, approval invalidation, staging, publication, and recovery mechanics. Add only evidence-backed internal seams and Adapters. | Architecture owner | [Formation audit](reports/formation-and-standards-audit.md) and Architecture composed-design admission | Separate shallow public Modules for revisions, heads, approvals, attempts, and recovery |
| Write and prove an isolated candidate before authoritative publication whenever the selected repository mechanism supports that ordering. Publish only through an exact expected-target transition and return success only after the published identity and postcondition are established. | Authoring, Persistence, Repository, Verification, and Commit owners | Persistence durable-mutation contract and historical A2 post-write-verification requirement | Publish-then-hope, default rollback, or successful staging treated as application |
| Publish a verified candidate directly to the configured Coding Standards `refs/heads/main` and return `applied` only after an atomic expected-target transition and exact postcondition observation. Keep the repository, ref, expected object, candidate object, and Git coordination behind the Authoring Interface. | User, Product, Authoring, Repository Adapter, and Release owners | [Selected application success](reports/product-contract-discovery.md#application-success-decision) and accepted P3 publication/recovery evidence | Candidate creation, patch export, or external submission treated as application; caller-supplied Git target facts; success inferred from an unavailable observation |
| Handles identify state but grant no capability. Trusted execution context supplies operation-specific authority, and apply-time proof binds the exact revision, target, action, evidence, and current authorization authority. | Security and Authoring owners | Accepted A1c authorization decision and Security input-validation authority | Self-asserted request capabilities, possession authority, or proposal-time authorization reused without proof |
| Select public and persisted compatibility only from a fresh producer, consumer, retained-state, deployment, and feature-completeness inventory. Use coordinated replacement when all affected contracts are owned and no overlap is promised; add migration or compatibility only for a real supported consumer. | Contracts, Persistence, and Release owners | Contracts evolution policy and A1c's deferred cross-engine promise | Automatic v12/store-v1 compatibility, speculative dual readers, or silent reinterpretation |
| Retain Linux CPython 3.11 and 3.12 as the only current platform claim. Platform-neutral design remains a constraint, not evidence for Windows or macOS support. | Product and Platform owners | Accepted A1c platform evidence | Inheriting A1c read-only evidence for new authoring, Git-write, or recovery behavior |
| Admit each material A2 design and procedure only after a bounded prototype or minimum viable test supplies distinct effectiveness, efficiency, correctness, and current standards-compliance evidence against predeclared questions and oracles. Prototype success admits a decision for implementation planning, not production behavior or objective acceptance. | Product, Architecture, Performance, and Verification owners | User direction and claim/evidence boundaries in Verification, Performance, and Architecture | Paper-only design acceptance, successful execution as correctness, or prototype behavior treated as production proof |
| Keep prototype source outside the canonical integration branch. Commit it only on a governed isolated prototype branch as primary evidence, point the canonical issue or report to the exact commit, and integrate only the validated decision. Select retention, archival, worktree removal, and branch disposition through the Commit workflow. | Prototype owner, A2 integration owner, and Commit owner | Prototype isolation contract and Commit branch/worktree lifecycle | Experimental shell, scratch state, fake success, or broad prototype code copied into production |
| Apply the current Router and every selected standard to all A2 plans, procedures, prototypes, verification, and implementation. Commit each coherent verified repository outcome through exact staged review and a conventional commit; the plan records semantic slices and evidence but does not own Git topology or cadence. | Planning, Implementation, Verification, Documentation, and Commit owners | Current routed standards and Commit workflow | Uncommitted durable authority, unchecked procedure changes, plan-prescribed commit topology, or verification logs used as commit messages |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| A proposal view preserves current standards meaning | Semantic and public behavior | Compile and exercise the exact projected content through current metadata, graph, analysis, and verifier entry points | Canonical standards sources and their existing semantic owners | Proposal-only parser or weaker validator | Proposed content passes a new path while the canonical path rejects it |
| Revision and head identity are correct | Identity and concurrency | Deterministic revision construction plus real concurrent expected-head transitions | Authoring state contract and durable store postcondition | Scheduling not exercised by the selected environment | Stale writer changes the current head or another revision |
| Analysis is complete for the current proposal | Analysis | Reproject the exact stored `AnalysisState` and establish current `CompleteResult` invariants | A1c Analysis owner and dependency-valid authorities | Historical packet/report interpretation | Stale or unrelated complete analysis authorizes readiness |
| Apply readiness is authorized | Security and contract | Validate exact approvals, evidence, current authority, revision, analysis, and target binding through the real authoring Interface | Trusted execution context and authored approval authorities | Self-asserted capability fields | Possession or a stale approval grants apply authority |
| Application publishes one verified result | Persistence and repository behavior | Stage exact candidate bytes, run selected verification, perform expected-target publication, and resolve the published identity | Canonical repository authority and current verifier contracts | Successful command or process exit alone | Verification failure or stale target still returns success |
| Interrupted application is recoverable | Resilience | Fault injection before, during, and after staging, verification, and publication plus cold-process resumption | Durable attempt state and exact repository/store observations | Helper-only simulation without the real transition | Retry duplicates work, guesses publication, or destroys authority |
| Generated contract is conformant | Generated contract | Compile every reachable operation and exercise actual facade producer and consumer paths | Selected JSON Schema implementation and canonical operation declaration | Fresh output alone | A generated shape is fresh but incomplete or semantically wrong |
| Platform support is real | Cross-platform system behavior | Provider-neutral facade harness on real Linux CPython 3.11 and 3.12 | OS, Git, CPython, SQLite, filesystem, and process observations | Windows and macOS | Linux result is represented as deferred-platform evidence |
| A1c user decisions remain intact | Product and architecture authority | Exact decision-preservation matrix plus differential A1c public workflow and stored-state evidence for every touched boundary | User-owned A1c decisions, accepted A1c plan, and current A1c implementation | A2-local review as authority to change A1c | An A2 design changes an explicit A1c choice without separate user authorization |
| A design is effective and correct enough to implement | Product, contract, and state behavior | Question-specific prototype or minimum viable test over representative happy, edge, stale, unauthorized, interruption, and recovery scenarios with predeclared outcomes | Caller workflow, A1c invariants, external contracts, and independent standards owners | Prototype convenience or successful execution alone | A design advances despite a failed scenario, missing oracle, or unexamined material state |
| A design is efficient enough to implement | Performance and resource use | Predeclared workload, metric, baseline or budget, environment, variability policy, and candidate comparison at the narrowest claim-complete boundary | Product-owned efficiency need and Performance measurement contract | Guessed threshold, single timing, debug build, or unrelated microbenchmark | A slower or materially more resource-heavy design is selected without accepted tradeoff authority |
| A repository outcome is standards-compliant and commit-complete | Process and change integrity | Current Router projection, claim-matched checks, staged diff and sensitive-file review, conventional commit inspection, and ledger evidence | Canonical standards owners and Git index/commit object | Working-tree success or an uncommitted document | A plan, procedure, prototype result, or source change becomes authority without compliant commit evidence |
| A2 acceptance is complete | Planning and verification | Exact current policy-impact population, dispositions, coverage equality, complete checkpoint, and independent review | Canonical graph, authored attestations, verification owners, and reviewers | Stale pre-migration graph totals | Passing focused tests substitute for an undispositioned consumer |

## Systemic Finding Audit

- Invariant family and canonical owner: immutable A1c analysis versus mutable
  authoring lifecycle; Analysis owns immutable decision state and the future
  Authoring owner owns proposal heads, readiness, publication, and recovery.
- Bounded authority, representation, and reachable consumer population: A1c
  snapshots, analysis state and results, generated facade, Snapshot persistence,
  Repository Git Adapter, current verifier Interface, harness authorization,
  explicit user-owned A1c decisions, future proposal representations,
  prototype evidence records, and every registered implementation consumer
  selected by the fresh policy-impact graph.
- Expansion facts: a distinct proposal-view consumer promise, retained A1c
  store, independently deployed facade consumer, new publication target,
  platform claim, dependency, or authoritative recovery state expands the
  population.
- Consumer dispositions: Milestone 0 must inventory and disposition every
  current public, persisted, generated, graph, verifier, harness, and
  documentation consumer before production admission.
- Deletion, consolidation, smaller-Interface, stronger-proof, and
  evidence-replacement alternatives: reuse A1c analysis; derive work and
  readiness; prefer immutable revision construction and transactional CAS;
  keep staging non-authoritative; decline independent child lifecycles,
  compatibility paths, registries, adapters, or evidence mechanisms without a
  current owner and deciding claim.
- Evidence-backed stopping condition: every authority and reachable consumer
  capable of confusing accepted snapshots, proposal revisions, complete
  analysis, apply readiness, or canonical publication has one non-blocked
  disposition and a claim-matched oracle.
- Repaired-composition comparison: the accepted design must add only the
  mutable authoring and publication complexity inherent in the product; it may
  not restore the removed packet/report, generic authority, or broad version
  machinery around A1c.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: accepted immutable standards, proposed content, proposal lifecycle, analysis completeness, semantic approval, application authority, candidate verification, canonical publication, and recovery change for different reasons and require explicit composition.
- State, identity, value, time, policy, and mechanism: revisions are immutable content-bound values; the proposal head is mutable lifecycle state; approvals and readiness are policy decisions; attempts and target refs carry time and publication state; SQLite and Git are mechanisms rather than domain authority.
  - Canonical authority scope and referenced authorities: Authoring owns proposal transitions and references A1c snapshot, analysis, approval, authorization, verifier, and repository authorities without absorbing their meaning.
  - Version roles and owned promises: Milestone 0 must classify public current-format, handle identity-domain, authoring-state format, store schema, compatibility, migration, operation, verifier-contract, and allocation values independently.
  - Supported compatibility overlaps and consumer matrix: none is assumed; a fresh inventory selects coordinated replacement, migration, or rejection and names every supported overlap and retirement trigger.
  - Material identity-invalidation effects: mutation changes revision and head; changed analysis dependencies change the analysis handle; changed approvals or authorization change readiness; only meaning-affecting contract changes invalidate semantic identity.
- Caller and composition-root knowledge: callers learn proposal lifecycle operations, opaque handles, required work, readiness, and typed outcomes; the composition root alone knows Snapshot storage, Git and verifier execution, configuration, authorization adapters, and recovery mechanics.
- Representative change paths and forced owners: a mutation rule should change Authoring and its contract evidence; a Git security change should change the Repository Adapter; an analysis invariant should change Analysis; a store guarantee should change Snapshot persistence; a public shape should change Contracts and facade projections; an authorization rule should change Security-owned authority and Authoring consumption.
- Stable Interfaces versus hidden knowledge: A1c domain Modules continue to consume immutable content sources and typed values; the Authoring Interface must hide SQL, Git plumbing, staging paths, verifier registry layout, retry position, approval storage, and child cleanup.
- Independent evolution, testing, failure, and replacement: revision construction, durable CAS, semantic analysis, authorization, repository staging, verification, and publication require owner-local evidence plus end-to-end proof; internal seams remain private unless a real independent Adapter or lifecycle requires exposure.
- Necessary complexity and containment: durable mutable head coordination, approval invalidation, exact staging, atomic publication, and interruption recovery are inherent in controlled authoring and belong behind one Authoring Interface rather than in callers or A1c Analysis.
- Deletion and cumulative machinery result: deleting the Authoring Module should remove proposal mutation and application while leaving A1c read-only behavior intact; deleting a proposed registry, compatibility reader, Adapter, ledger, or evidence mechanism must remove incidental machinery rather than redistribute a required invariant.
- Prototype containment result: deleting every prototype shell and scratch artifact must leave the accepted A1c implementation untouched and the admitted A2 decision reproducible from its question, evidence, oracle, limitations, and exact primary-source pointer; prototype-only machinery cannot become a production dependency.

## Milestones

### Milestone 0: Product, Contract, And Architecture Admission

**Goal:** Produce one independently reviewed product, Interface, authority,
persistence, application, recovery, dependency, platform, design-validation,
and acceptance design that preserves every unreopened A1c user decision,
validates the one exact projected-material reauthorization, and can admit an
exact first A2 implementation slice without relying on stale A1 terminology,
paper-only assumptions, or unresolved publication facts.

**Allowed write set:**

- `docs/plans/standards-engine-a2/plan.md`
- `docs/plans/standards-engine-a2/execution-ledger.md`
- `docs/plans/standards-engine-a2/issues.md`
- `docs/plans/standards-engine-a2/reports/product-contract-discovery.md`
- `docs/plans/standards-engine-a2/reports/a1c-user-decision-preservation.md`
- `docs/plans/standards-engine-a2/reports/a1c-projected-material-reauthorization.md`
- `docs/plans/standards-engine-a2/reports/consumer-and-state-inventory.md`
- `docs/plans/standards-engine-a2/reports/interface-and-composed-design.md`
- `docs/plans/standards-engine-a2/reports/application-and-recovery-contract.md`
- `docs/plans/standards-engine-a2/reports/design-validation-protocol.md`
- `docs/plans/standards-engine-a2/reports/prototype-evidence-index.md`
- `docs/plans/standards-engine-a2/reports/p4r-facade-composition-admission.md`
- `docs/plans/standards-engine-a2/reports/p5-combined-efficiency-admission.md`
- `docs/plans/standards-engine-a2/reports/a2-plan-admission.md`
- `docs/decisions/standards-engine-a2.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html`
- `tools/standards_engine/tests/prototypes/a2/projected-view.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/projected-analysis-replay.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/projected-material-identity.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/publication-recovery.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/facade-workflow.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/facade-composition.prototype.py`
- `tools/standards_engine/tests/prototypes/a2/efficiency-measurement.prototype.py`

The eight currently registered prototype paths are writable only in governed
isolated prototype branches or worktrees and never enter the canonical
integration branch. The
canonical branch accepts their exact evidence pointers, verdicts, and validated
decisions through the named reports. Each prototype branch also owns its local
mechanically regenerated `evaluation/standards-effectiveness/generated/suite-inputs.json`
because staging a new prototype path changes that branch's repository-index
observation. Executable Python prototypes must remain below the package's
existing `tests` boundary so the package contract excludes them from production
source ownership and import-closure checks. The generated diff must change only
the derived index digest; a package-input entry is a stop condition. No
registry, suite-definition, existing-file, graph, inventory, or retirement
evidence may change. The branch-local projection is never integrated into
canonical `main`.

**Tasks:**

- [x] Route the exact product and artifact facts through the current executable
  Router and record selected owners and explicit exclusions.
- [x] Build an exact A1c decision-preservation matrix from every binding choice
  explicitly selected or clarified by the user. For every A2 design element,
  record `unchanged`, `composed-without-change`, `prohibited-conflict`, or
  `requires-separate-user-reauthorization`; leave no decision implicit.
- [x] Record the user's exact 2026-09-01 reauthorization of projected-material
  Analysis identity and replay, its supersession scope, the unchanged A1c
  choices, and the prohibition on treating planning authority as production or
  ADR amendment authority.
- [x] Trace representative create, discover, revise, query, analyze, approve,
  apply, stale-head, verification-failure, interruption, recovery, snapshot
  deletion, and agent-handoff workflows through the current A1c Interface.
- [x] Inventory every current facade consumer, retained store, deployment,
  harness, provider, authorization owner, publication target, repository
  integration, generated artifact, and implementation consumer.
- [x] Choose one exact canonical application success meaning. If an external
  patch or pull-request integration is selected, use an exported or submitted
  outcome until external canonical publication is independently confirmed.
  The user selected direct expected-target publication to the configured
  Coding Standards `refs/heads/main`; only its exact observed verified
  candidate postcondition is `applied`.
- [ ] Compare proposal-view Interface designs against caller knowledge, A1c
  reuse, public contract evolution, identity meaning, migration, failure,
  Locality, and Depth; reject both proposal-as-snapshot and a second analyzer.
- [ ] Define the Authoring authority, revision and head state machine,
  operation variants, idempotency, stale outcomes, approval invalidation,
  apply-readiness proof, and exact next-operation derivation.
- [ ] Define durable source and destination states, schema/version roles,
  transaction and CAS guarantees, staging visibility, publication boundary,
  interruption points, unknown-outcome behavior, resumption, snapshot aggregate
  lifecycle, and current-store migration or rejection.
- [ ] Define the trusted execution context, principals, issuers, capabilities,
  review independence where required, revocation, path containment, Git
  environment, target-ref authority, and apply-time authorization proof.
- [ ] Re-evaluate Git implementation-versus-dependency ownership before
  extending `repository_git`; select the smallest write-capable Adapter or
  existing-Module change supported by actual consumers and the deletion test.
- [ ] Classify generated, internal-coordinated, persisted, public-versioned,
  and distributed-independent contracts; decide whether A2 is the
  feature-completeness trigger for cross-engine compatibility planning.
- [x] Define one design-validation protocol that requires a named question,
  effectiveness criterion, efficiency metric and comparison or budget,
  correctness invariants and negative cases, current standards route, deciding
  oracle, environment, limits, and pass, revise, or reject threshold before a
  prototype or minimum viable test begins.
- [x] Run the isolated logic prototype for proposal revision, head CAS,
  analysis/readiness invalidation, apply, interruption, and recovery states.
  Expose the complete relevant state and exercise guided happy, stale,
  unauthorized, conflicting, and unknown-outcome scenarios.
- [ ] Run isolated minimum viable experiments for projected-view equivalence,
  real scratch SQLite CAS and cold reopen, stage-before-publication, concurrent
  target change, interruption recovery, generated facade shape, and the
  representative agent workflow. Use disposable repositories and stores only.
- [x] Revise the P2 end-to-end claim with an exact projected-analysis identity
  and cold-replay experiment. Determine whether one private Authoring seam can
  reuse the existing analyzer while preserving A1c's immutable AnalysisState,
  non-Git change-set, lifecycle, and no-proposal-snapshot decisions; reject the
  seam and require product reauthorization if those constraints cannot coexist.
  P2R rejected all five bounded representation seams and admitted no A2 design;
  exact evidence is recorded in the prototype index.
- [x] Run A2-P2R2 against the selected exact projected-revision material
  reference. Prove injective canonical identity, unchanged snapshot analysis,
  exact cold-process replay after head movement, real SQLite dependency and
  lifecycle behavior, typed missing/wrong-base/tampered/quarantined outcomes,
  bounded identity overhead, one Analysis authority, and dependency-complete
  Linux CPython 3.11 and 3.12 execution before admitting an ADR or source plan.
  Passing evidence is archived at exact commit
  `b76f443b5bc05b179d20193bf27ea4d3054db7f3` and recorded in the prototype
  evidence index.
- [x] Revise P4 only after P2R2 accepts projected-material identity. Retest the
  explicit additive facade without a projected `SnapshotHandle`, mutable
  current-evidence selector, caller-supplied ref or object ID, tagged dispatch,
  or A1c query/inspect overload before selecting any operation root. Execute
  the exact typed-continuation comparison admitted in the
  [P4R report](reports/p4r-facade-composition-admission.md) from fixed base
  `fc7dbeabb5828b5b6f3840a1ff004209ae291385`. P4R passed all 34 gates on
  CPython 3.11 and 3.12; exact evidence is archived at commit
  `9a0c34325e2849c437072b12b3188bede7f08d4e` and recorded in the prototype
  evidence index.
- [ ] Measure every material candidate against its predeclared efficiency
  claim using an owned workload, metric, baseline or budget, environment, and
  variability policy. Record the correctness and resource tradeoff; do not
  guess a threshold or substitute a weaker microbenchmark.
- [ ] Record each prototype's exact question, commit identity, reproduction
  instructions, results, limitations, A1c preservation disposition, standards
  review, verdict, and terminal branch/worktree status. Reject or revise a
  design when any required dimension fails or is unavailable.
- [ ] Perform the complete Architecture composed-design admission, record the
  superseding A2 ADR candidate, derive exact objective oracles, and delete or
  decline every permanent mechanism without distinct deciding value.
- [ ] After the active verification migration's fresh graph audit, query the
  exact A2 implementation-consumer population and record every non-blocked
  disposition and required coverage owner.
- [ ] Obtain one independent planning review of all Milestone 0 artifacts and
  re-plan this file with exact implementation milestones, write sets, gates,
  blockers, and one next slice.

**Acceptance gate:**

- The product owner selects the exact caller-visible application outcome and
  accepts every representative workflow and typed terminal result.
- The A1c preservation report covers every explicit user-selected decision,
  distinguishes unchanged choices from the one exact projected-material
  reauthorization, records no unauthorized expansion, and is independently
  reconciled against the accepted A1c plan and current public behavior.
- Every material design and procedure has accepted, question-specific
  effectiveness, efficiency, correctness, and standards-compliance evidence.
  Prototype success is used only to admit a decision; no prototype source or
  scratch authority appears in the canonical implementation write set.
- Independent Architecture, Contracts, Persistence, Security, Concurrency,
  Resilience, Dependencies, Platform, Verification, and Planning review reports
  no unresolved blocking fact or undispositioned consumer.
- The selected design satisfies every composed-design probe, version role,
  consumer/store compatibility decision, threat-model obligation, and evidence
  oracle without restoring superseded A1/A1b machinery.
- Plan structure, linked-artifact presence, generated suite-input freshness,
  affected declarative suites, policy-impact closure, and diff hygiene pass.
- Every canonical and prototype-only repository outcome has Commit-owned
  staged-scope, sensitive-file, verification, conventional-message, exact
  commit, and branch/worktree disposition evidence in the ledger or prototype
  index.
- This plan names one exact first production implementation slice and write set
  before Milestone 0 becomes `Accepted`.

**Status:** `Active`

## Blockers

- The first uncommitted P5 source revision failed independent specification and
  standards audits before measurement. The clarified committed
  [P5 admission](reports/p5-combined-efficiency-admission.md) keeps the accepted
  combined design, baselines, five workloads, thresholds, 23-standard route,
  exact base, isolated write set, and terminal disposition, while freezing the
  invalid-workflow applicability matrix, raw-report recalculation, one-store
  evidence boundary, and external-gate bundle. Source correction, frozen-source
  audits, and focused probes are admitted. Complete P5 measurement remains
  blocked until the corrected frozen source passes both independent audits and
  the focused contract, oracle, lifecycle, and report-integrity probes on
  CPython 3.11 and 3.12.
- An A1c ADR amendment, public or persisted contract selection, and production
  planning remain unavailable until P5 passes and its canonical verdict is
  recorded.
- Production implementation remains unavailable until A2-A11 and every
  design-dependent A2-A12 record are satisfied, Milestone 0 is accepted, and
  the plan names and admits an exact implementation slice.

## Re-Plan Triggers

- The selected application success meaning, canonical target, first caller, or
  deployment differs from the current assumptions.
- A current facade consumer or retained A1c store requires compatibility or
  migration overlap.
- Proposal content cannot pass through the existing semantic owners without a
  material A1c Interface or Analysis replacement.
- Any design requires changing, weakening, or reinterpreting an explicit
  user-selected A1c decision outside the exact projected-material identity and
  replay reauthorization.
- A prototype or minimum viable test fails, lacks a deciding oracle, cannot
  establish a representative effectiveness or efficiency claim, or reveals a
  materially different state, trust, persistence, or publication model.
- Prototype-only code, scratch state, fake success, or a test seam appears
  necessary in the canonical implementation.
- Safe application requires authoritative publication before correctness proof
  or cannot establish an atomic expected-target postcondition.
- Interruption evidence cannot distinguish unchanged, applied, and
  recovery-required states without a new durable authority.
- Authorization, containment, Git, dependency, platform, or release facts
  expand the selected trust or support contract.
- The active verifier migration changes the consumer population, graph owner,
  execution Interface, or adequate acceptance oracle assumed by Milestone 0.
- A material replacement changes the admitted Module, Interface, Seam,
  Adapter, state, version, or persistence composition.
- Cumulative machinery or observed change propagation exceeds the current
  composed-design admission.

## Concurrent Work

Milestone 0 is serial. Shared plans, ADRs, schemas, generated artifacts,
registries, policy-impact declarations, and coverage authority remain with one
integration owner. Concurrent Plan Integration must be re-routed only if two
or more development proposals can remain outstanding and become stale before
integration.

## Repository Isolation

Material isolation is required for prototype code because it is evidence, not
an implementation candidate. Each prototype uses a task-owned private branch
and worktree based on current integration authority. Before creation, its
record names the question, responsible prototype owner, admitted base when
staleness matters, exact prototype-only write set, integration target, A2
integration owner, visibility, and expected terminal disposition.

The prototype is committed as coherent verified work on its isolated branch
and is never merged into the canonical integration branch. The canonical
branch receives only the evidence record and validated decision. After the
question is settled, the prototype worktree is either `removed-archived` after
its exact commits are protected by a named recovery ref, or
`retained-protected` under an explicit long-lived purpose, owner,
synchronization policy, consumer, and retirement trigger. Commit owns the exact
mechanism and evidence; no cleanup is inferred from acceptance or rejection.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: Plan C external-project baselines; Windows and macOS
  support; cross-engine stored-state compatibility when Milestone 0 does not
  select A2 as its feature-completeness trigger
- Final status: `Active`
