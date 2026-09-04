# A2 Current-Boundary And Standards Formation Audit

## Status And Purpose

This report records the evidence used to form the current
[A2 controlled-authoring plan](../plan.md). It does not admit production
implementation, select the final public operation set, or resolve the open
Milestone 0 product decisions.

## Audit Disposition

The historical A2 direction was coherent discovery input but not an executable
plan:

- the Plan A1 development brief labels itself non-authorizing;
- no `docs/archive/plans/standards-engine-a2/plan.md` existed;
- future-authoring requirements were distributed across historical A1, A1b,
  and A1c documents;
- the oldest text referred to immutable packets and
  `CompletedAnalysisReport`; and
- publication, durable head state, authorization, compatibility, recovery,
  and objective evidence lacked current owners and complete contracts.

Those facts make implementation admission unavailable rather than making the
historical brief defective in its declared investigative role. This plan
formation resolves the authority gap and carries the material design gaps as
Milestone 0 issues.

## Current A1c Boundary

The A2 starting point is accepted A1c after corrective revalidation:

- eight generated facade operations: `create_snapshot`, `find_snapshots`,
  `delete_snapshot`, `undelete_snapshot`, `query`, `prepare`, `resolve`, and
  `inspect`;
- public Interface schema v12, request and result contract v4, and public
  handle schema v5;
- immutable snapshot lifecycle roots captured from configured canonical
  repository `HEAD` without caller-selected history or raw content;
- one SQLite-backed Snapshot Module storing exact content, roots, opaque
  aggregates, snapshot dependencies, and derived child indexes;
- one immutable Analysis-owned `AnalysisState`, one `AnalysisHandle`, and
  deterministic pending and complete projections;
- dependency-valid decision reuse and cold reconstruction from stored snapshot
  and aggregate authority rather than ambient repository, provider, or process
  state;
- current JSON Schema Draft 2020-12 semantics delegated to the selected
  `jsonschema` implementation and generated through the current Contracts
  compiler;
- handles as identifiers rather than authorization;
- Linux CPython 3.11 and 3.12 as the only verified platforms; and
- no cross-engine stored-state compatibility promise before feature
  completeness.

The accepted A1c product decisions also constrain A2: proposals are non-Git
change material linked to one immutable snapshot, the complete projected view
uses the same navigation and verification semantics as accepted content, and
snapshot deletion owns linked proposal and analysis lifecycle rather than
requiring caller-coordinated child cleanup.

## A1c User-Decision Preservation Boundary

The accepted [A1c binding decisions](../../standards-engine-a1c/plan.md#binding-decisions)
remain the canonical owner. This section is a preservation index for A2, not a
second statement of those decisions. A2 may add controlled authoring only by
composition that leaves these user-selected choices intact:

- software-development agents remain the first caller, the Python Interface
  remains the access seam, and harness-managed tool calls remain the primary
  deployment contract;
- process invocation, agent turn, workflow, and agent instance remain distinct
  lifetimes, with resolvable handles and accepted decisions across ordinary
  tool invocations and authorized handoffs;
- snapshot creation captures the configured canonical repository's current
  `HEAD` without caller-selected repositories, paths, history, Git objects, or
  raw authority bytes;
- every creation yields a unique opaque snapshot lifecycle root; immutable
  content identity remains internal and deleting one equal-content root cannot
  affect another;
- snapshots remain until explicit authorized deletion, which quarantines the
  complete aggregate for a fixed seven-day default, permits complete undelete,
  exposes no immediate purge, and does not extend deadlines on repeat deletion;
- proposed edits remain non-Git change sets linked to one immutable snapshot,
  use the same navigation, inspection, analysis, and verification semantics,
  and participate in the snapshot's aggregate deletion lifecycle;
- one SQLite-backed Snapshot Module owns current durable aggregate storage and
  derived child indexes without exposing a generic repository, public
  persistence Protocol, or engine backup/restore Interface;
- one generated public facade and domain-local contract identities remain the
  contract shape; A2 does not restore broad version bags or per-operation
  persisted authority objects;
- coverage identity remains dependency-local, and repository-wide suite-input
  freshness remains outside product analysis identity;
- cross-engine stored-state compatibility remains deferred until feature
  completeness, Linux CPython 3.11 and 3.12 remain the only current platform
  claim, and semantic understanding remains with the agent; and
- the current eight A1c operations and their accepted behavior remain available
  while A2 evaluates additive authoring operations through the generated facade.

Milestone 0 must turn this index into an exact decision-by-design matrix. A row
may be `unchanged`, `composed-without-change`, or `prohibited-conflict`. A row
that would require an A1c change remains unavailable until the user separately
and explicitly authorizes an A1c re-plan; A2 review or prototype evidence
cannot grant that authority.

## Retained Historical A2 Requirements

The following requirements remain valid after translating them into current
A1c terminology:

1. Controlled authoring is a separately admitted product with a stronger
   lifecycle than read-only analysis.
2. It reuses A1c identity, snapshot, query, applicability, impact, coverage,
   decision-reuse, and analysis behavior rather than creating a second
   analyzer.
3. Proposed semantic state remains proposed until separately authorized
   semantic, relationship, and lifecycle decisions promote it.
4. Analysis completion is derived from one immutable `AnalysisState`; it is not
   apply authority and is not an authored Boolean.
5. A distinct apply-readiness proof binds the current proposal revision to the
   exact complete `AnalysisHandle` and required approvals.
6. A2 alone owns a mutable proposal head and compare-and-swap staleness. A1c
   analysis remains immutable, branchable, and free of global supersession.
7. Tool availability and handle possession do not grant authority.
8. Application does not return success until verification and the canonical
   publication postcondition pass; failure has an explicit non-success and
   recovery contract.

## Routed Standards

The observable A2 facts select:

- Core and Router;
- Planning, Implementation, Verification, Documentation, Build, Tooling, and
  Commit workflows;
- the Library application profile;
- Generated Contract, IPC, and Persistence boundary profiles;
- Architecture, Contracts, Concurrency, Resilience, Cross-Platform,
  Dependencies, Security, Diagnostics, and Performance topics; and
- Release when current consumers, published compatibility, stable feature
  completeness, dependency changes, or publication artifacts establish its
  applicability.

The current facts exclude Frontend, Accessibility, Launcher, Interop, Language
Binding, and language-specific profiles. Performance is selected only for the
user-required bounded efficiency claims used to admit a design; those
measurements do not create a production performance promise. Concurrent Plan
Integration remains excluded for serial planning and is not selected by
product proposal-head concurrency.

Milestone 0 must execute the current Router projection and replace this
formation-time route if its product discovery supplies a new or contradictory
fact.

## Required Authoring Shape

The candidate design has one coherent Authoring responsibility:

```text
A1c Snapshot
    -> ChangeSet lifecycle root
    -> immutable ProposalRevision values
    -> one durable current-head CAS
    -> exact projected standards view
    -> A1c prepare / resolve
    -> current complete AnalysisHandle
    -> authorized semantic / relationship / lifecycle decisions
    -> apply-readiness proof
    -> isolated candidate staging
    -> complete required verification
    -> expected-target canonical publication
    -> applied identity and resulting SnapshotHandle
```

A deep Authoring Module is the current candidate because callers should learn
proposal operations and typed outcomes while revision encoding, head
coordination, approval invalidation, staging, Git publication, verification
orchestration, persistence, and recovery remain hidden. The final Module,
Interface, internal seams, and Adapters are not admitted by this report; the
complete composed-design comparison belongs to Milestone 0.

## Prototype-First Design Admission

No material A2 idea or procedure becomes implementation authority from prose,
review agreement, or a successful toy execution. Before production planning,
Milestone 0 records a question-specific prototype or minimum viable test with:

1. the design question and competing outcomes;
2. the representative caller workflow, state transition, workload, or failure;
3. a predeclared effectiveness criterion;
4. an owned efficiency metric plus an applicable baseline, comparison, or
   budget and variability policy;
5. correctness invariants, negative cases, and an independent or authoritative
   oracle;
6. the current Router projection and every applicable standards owner;
7. the exact disposable environment, inputs, reproduction procedure, and
   unsupported boundary; and
8. a `pass`, `revise`, `reject`, or typed `unavailable` disposition.

The state-model prototype is a self-contained, human-drivable logic demo that
exposes complete relevant state after each action. Persistence, Git,
interruption, and facade experiments instead use the smallest executable
minimum viable harness capable of exercising the real boundary against scratch
repositories and stores. A lower-fidelity prototype cannot establish a
higher-fidelity production or platform claim.

Prototype source is visibly experimental, trivial to run, isolated on a
governed non-canonical branch, and committed there as primary evidence. The
canonical branch records the exact prototype commit, question, result,
limitations, and validated decision; it does not merge the prototype shell,
scratch state, fake success, or speculative abstractions. A later production
slice reimplements only the admitted decision under production contracts and
tests, then re-runs the narrowest complete claim at the real boundary.

## Material Decisions Still Required

### Proposal View And A1c Reuse

Current `QueryCall` and `AnalysisRequest` accept `SnapshotHandle`, but a
proposal revision is not an accepted canonical snapshot. Milestone 0 must
compare at least:

- a current-facade evolution that accepts an explicitly typed immutable
  standards-view reference; and
- authoring operations that take a proposal revision and internally derive the
  existing A1c navigation or analysis call.

The selected Interface must preserve one analysis owner, avoid requiring the
caller to submit facts already owned by the proposal, keep proposal authority
distinct from accepted snapshot authority, and minimize coordinated public and
persisted change.

### Application Success

`Applied` must have one observer and postcondition. Direct canonical-ref
publication, creation of a candidate commit, patch export, and pull-request
submission are different outcomes. If canonical publication is external, A2
may return an exported or submitted result but cannot infer that the standards
authority changed.

### Durable Publication And Recovery

The preferred ordering is:

1. establish exact proposal, analysis, approval, authorization, and target
   preconditions;
2. materialize an isolated non-authoritative candidate;
3. run every required proof against the exact candidate bytes;
4. create the selected publication artifact;
5. publish through an exact expected-target transition;
6. establish the published identity and durable postcondition; and
7. return success.

Milestone 0 must prove that the selected Git and store mechanisms support that
ordering or record a different complete contract. It must define idempotency
and cold recovery for interruption before staging, during staging, during
verification, before publication, during publication, and after publication
but before response.

### Compatibility And Versions

A2 must separately classify public Interface, operation, request, result,
handle, proposal-revision identity, proposal-state format, analysis reference,
readiness, attempt, SQLite schema, repository publication, compatibility,
migration, and allocation values. Similar numbering or coordinated cutover is
not authority to share a version.

A current inventory determines whether A1c public or persisted values require
overlap. If all consumers and stores are controlled and no overlap is promised,
the design should prefer one atomic replacement with typed rejection of stale
state. A real retained consumer may instead require a bounded migration or
compatibility window with an owner and retirement trigger.

## Non-Authorizing Downstream Dependency Order

Milestone 0 must replace this sequence with exact milestones and write sets
after its decisions are accepted:

1. accept the A1c preservation matrix and every applicable effectiveness,
   efficiency, correctness, and standards-compliance design-validation record;
2. implement proposal construction, immutable revisions, projected content,
   durable CAS, and A1c analysis reuse behind the admitted Authoring Interface;
3. implement apply-readiness, trusted authorization, isolated staging,
   verification, atomic publication, interruption, and recovery;
4. perform one atomic public-contract, facade, persisted-state, consumer,
   documentation, graph, and coverage cutover without speculative fallback;
5. run real Linux CPython 3.11/3.12 public workflows, complete repository
   verification, exact consumer reconciliation, and independent acceptance.

This order is planning evidence only. It neither admits production changes nor
prescribes commit topology.

## Formation Conclusion

A2 can continue from A1c without reopening its immutable product core. The
standards-compliant continuation adds only the inherent mutable authoring
responsibility, keeps accepted and proposed authority distinct, binds mutable
head state to immutable A1c analysis, proves candidates before canonical
publication, validates each material design before canonical implementation,
commits every coherent outcome through the Commit workflow, and treats unknown
application state as a recovery obligation rather than a successful fallback.
