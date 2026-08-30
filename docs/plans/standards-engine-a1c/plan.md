# Plan: Standards Engine A1c Product Contract And Architecture Discovery

**Plan status:** `Planned`

**Current phase:** Product-contract discovery before architecture admission

**Next slice:** Revalidate current consumers and retained state for A1C-002 and
trace the representative agent workflows needed to close A1C-001, then define
the bounded architecture experiments

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Develop an admissible A1c product and architecture plan that preserves A1b's
demonstrated semantic corrections while retaining only guarantees and
machinery justified by concrete caller, deployment, state-lifetime, and risk
facts. This initial plan owns discovery and design admission only. It grants no
A1c implementation authority.

## Objective Acceptance

These claims close planning readiness, not A1c implementation. Runtime
acceptance claims will be added only after a binding architecture and exact
implementation scope are admitted.

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1C-P1 | The first real caller, deployment form, handle lifetime, retained non-derivable state, loss consequence, and operational owner are explicit and supported by inspectable evidence. | `user-workflow` | `not-applicable` | `manual` | `pending` | Pending product-owner procedure in [product-contract discovery](reports/product-contract-discovery.md) |
| A1C-P2 | Current A1b public consumers, persisted-state consumers, operational callers, and compatibility obligations are revalidated without inferring demand from tests or incumbent machinery. | `contract` | `not-applicable` | `automated` | `pending` | Pending current-tree consumer and state inventory |
| A1C-P3 | Competing A1c designs are exercised through representative caller workflows, deletion tests, and locality probes before one composition is selected. | `integration` | `not-applicable` | `automated` | `pending` | Pending design experiments |
| A1C-P4 | The selected composition passes the complete Architecture-owned composed-design probe and identifies every retained concern, authority, lifecycle, Interface, dependency direction, and removal condition. | `integration` | `not-applicable` | `manual` | `pending` | Pending architecture decision and ADR |
| A1C-P5 | A revised implementation plan defines exact runtime write sets, coherent milestones, migration and deletion ownership, claim-matched verification, re-plan triggers, and a separate content-bound acceptance step. | `focused` | `not-applicable` | `manual` | `pending` | Pending binding A1c implementation plan |

## Acceptance Procedures

| Claim | Procedure or command | Evidence owner | Unresolved risk |
| --- | --- | --- | --- |
| A1C-P1 | The product owner executes each named caller workflow against the current public Interface, records the deployment and retained handles, and signs the completed discovery fields. | A1c product owner | A test-only or hypothetical caller could be mistaken for product demand. |
| A1C-P2 | Search current package imports, tool registrations, persisted stores, fixtures, and operational documentation; record every match and an explicit bounded-empty result for every searched class. | A1c consumer-inventory owner | An unregistered external consumer cannot be discovered from repository evidence alone. |
| A1C-P3 | Run each admitted experiment through the same representative workflows and compare Interface knowledge, representative change Locality, deletion results, and failure ownership. Exact commands belong to the later experiment admission. | Architecture owner | A prototype may omit a material deployment or lifetime boundary. |
| A1C-P4 | Complete the Architecture-owned composed-design probe against the produced candidate composition and record all unavailable or invalid outcomes before ADR selection. | Architecture owner | Review prose could assert simplicity without an inspectable produced artifact. |
| A1C-P5 | Run the plan structure and routed planning suites, then manually trace every architecture decision to one exact write set, milestone, migration/deletion owner, gate, and re-plan trigger. Exact commands belong to the binding implementation plan. | Planning owner | A correct plan structure could still omit a semantic consumer or migration owner. |

## Scope

### In Scope

- Product-fact discovery for A1c's first supported caller and deployment.
- Handle-lifetime, state-retention, durability, recovery, compatibility,
  platform, and operational-ownership decisions.
- Revalidation of actual A1b consumers and retained state.
- Small design experiments for aggregate versus child-object replay, public
  Interface depth, package enforcement, version scope, coverage invalidation,
  and verification subsumption.
- A composed-design comparison and eventual superseding A1c ADR.
- Development of the later exact implementation scope, milestones, deletion
  plan, and acceptance claims.

### Out Of Scope

- A1c production source, schema, generated artifact other than the exact suite-
  input freshness projection listed in Milestone 0, fixture, suite, policy
  graph, or runtime-state mutation under the current plan state.
- Deleting or weakening accepted A1b behavior or evidence before an admitted
  replacement owns the same required claim or explicitly removes its product
  requirement.
- Returning to A1's local JSON Schema interpretation or conflated equality and
  identity behavior.
- Normative standards changes. General standards findings require their own
  project-agnostic plan and consumer audit.
- A2 authoring, mutation, proposal-state, or recovery work.
- Compatibility, migration, persistence, platform, or threat-model promises
  inferred from incumbent A1b machinery rather than real consumers.
- A Standards Engine backup/restore Interface. File-level protection and
  archival remain administrative responsibilities outside the product API.

## Constraints And Assumptions

### Constraints

- Accepted A1b implementation `84412f22fa9fe082f089eaa347c30c23f185ffee`
  and its final acceptance remain the behavior and evidence baseline. This plan
  does not reopen that acceptance.
- The accepted A1/A1b audit supplies design constraints and experiments, not a
  binding A1c architecture.
- The selected Draft 2020-12 dependency remains the schema-semantics owner.
  A1c will not implement a repository-local JSON Schema validator.
- JSON Schema equality, domain equality, identity encoding, ordering, and
  deduplication remain separately owned concepts.
- Counts, file size, test totals, dependency totals, and incumbent structure
  may locate cost but cannot select the design.
- No implementation write set exists until A1C-P1 through A1C-P4 support a
  binding architecture and this plan is re-planned with exact implementation
  authority.
- Work is serial. The Concurrent Plan Integration profile is not applicable
  unless multiple proposals can actually become stale before integration.

### Assumptions

- The product owner has selected software-development agents acting for
  developers across projects as A1c's first caller and the Python Interface as
  their access seam. The primary deployment is a harness-managed tool call;
  direct in-process package embedding is a custom integration. Repository
  discovery must still identify concrete current integrations, retained A1
  state, non-test `open_persisted` callers, and operational backup/restore
  callers rather than inferring them from that intended use.
- The four read-only operations with typed request/result/rejection behavior
  and explicit uncertainty without valid-looking fallback are inherited A1c
  behavioral constraints. Discovery may simplify their internal composition,
  but does not reopen whether callers receive those behaviors.
- Identity and Contracts remain strong candidate deep Modules because deleting
  them while retaining their behavior would redistribute semantic complexity
  to callers.
- Durable internal snapshot ownership and active multi-turn analysis continuity
  are product requirements. A snapshot is a complete immutable copy of
  canonical standards at one Git commit. Proposed edits are non-Git change sets
  linked to that snapshot and are projected through the same behavior and
  verification authority without copying or mutating the snapshot. Snapshots
  remain until authorized explicit caller deletion, which also deletes linked
  change sets. Coding Standards cannot infer disuse from age, inactivity, or
  apparent reachability. Each snapshot, its change sets, and every dependent
  analysis or artifact form one lifecycle aggregate for atomic deletion and
  movement; callers do not coordinate child cleanup. Cross-engine stored-state
  compatibility is deliberately deferred until feature completeness. Closed
  stores are machine-portable, and Linux, Windows, and macOS are product targets
  while current development remains Linux-based. Deletion quarantines the
  aggregate for bounded undelete before expiry. The default period is seven
  days and may be changed only through deployment configuration, not the Python
  Interface or a deletion request. Coding Standards does not own backup/restore;
  administrators copy a closed consistent store or use storage-aware tools.
  SQLite, physical aggregate layout, exact historical coverage replay, and the
  custom governed-source interpreter remain mechanism or product hypotheses
  rather than presumed requirements.
- The agent owns semantic understanding and judgment. Coding Standards owns
  declared mechanical parsing, validation, routing, identity, graph,
  applicability, storage, and projection behavior; it must not infer prose
  meaning or claim semantic correctness for the agent.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Keep A1c architecture unselected until concrete product facts resolve A1C-001. | A1c product owner | [Accepted audit](../standards-engine-a1-a1b-audit/reports/final-synthesis.md) and [product discovery](reports/product-contract-discovery.md) | Architecture selection from incumbent A1b mechanisms |
| Select software-development agents acting for developers across projects as the first caller and the Python Interface as the access seam. A1c supplies read, navigation, inspection, and analysis behavior; canonical standards mutation remains outside A1c and requires separate A2 authority. | A1c product owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Treating tests, repository packages, or a human CLI as the first product caller |
| Treat a harness-managed tool call as the primary deployment. Directly embedding the Python package in an agent process is a custom integration whose additional lifecycle and composition choices are owned by that harness. Preserve one public behavior contract rather than creating separate tool-call and embedded product semantics. | A1c product owner and harness integrator | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Two equally authoritative deployment contracts or implementation-specific guarantees leaking into the public Interface |
| Distinguish one engine invocation/process from one multi-turn agent workflow and from one agent instance; do not use the ambiguous term session as lifecycle authority. The normal tool deployment may terminate the engine process after every request, so handles and accepted decisions remain resolvable across invocations, turns, and authorized coordinator/subagent handoffs during the workflow. A replacement agent instance may instead start an independent run without inferred lineage. | A1c product owner, Coding Standards store, and harness integrator | User clarification recorded in [product discovery](reports/product-contract-discovery.md) | Process-local handles, forced replay between turns, or global supersession between independent runs |
| Coding Standards owns a complete immutable snapshot of canonical standards at one selected Git commit and resolves its opaque handle without requiring callers to manage raw content. The commit is source provenance rather than the internal storage mechanism or snapshot handle. | A1c product owner and Coding Standards snapshot owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Caller-managed snapshot bytes, mutable snapshots, embedded Git storage, or Git identity as the storage mechanism |
| Retain every snapshot until an authorized caller explicitly deletes it. Do not infer permission to delete from age, inactivity, process exit, agent replacement, apparent lack of internal references, or storage pressure. | A1c product owner and Coding Standards snapshot owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Automatic expiration, implicit garbage collection, or caller-managed raw snapshot storage |
| Store proposed edits as a non-Git change set linked to one complete immutable snapshot. Project the resulting working view through the same navigation, read, inspection, analysis, and verification contracts as canonical content. Deleting the snapshot deletes every linked change set. | A1c product owner, Coding Standards snapshot owner, and Verification owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Copying the full corpus per edit, mutating snapshots, embedded Git repositories, weaker proposal validation, separate change-set read semantics, or orphaned change sets |
| Treat each snapshot, every linked change set, and all analyses and artifacts whose validity depends on them as one lifecycle aggregate. Delete that aggregate atomically, and move it as one closure if movement is supported. Child handles may remain inspectable but do not own independent retention or transfer lifecycles. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Caller-enumerated cleanup, orphaned artifacts, independently moved invalid children, or storage reachability guesses |
| Implement snapshot deletion as aggregate quarantine followed by policy-governed expiry; permit authorized undelete of the complete aggregate before expiry. Keep backup and restore outside the Standards Engine Interface while requiring transactionally consistent publication and a documented administrative file closure. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Immediate accidental data loss, partial undelete, conflating quarantine with disaster recovery, or an engine-owned backup subsystem without a product caller |
| Default snapshot quarantine to seven days. Allow a deployment owner to change the duration only through configuration, not through the agent-facing Python Interface or an individual deletion. Bind each deletion to the exact purge deadline calculated from the effective policy so later configuration changes do not rewrite existing lifecycle decisions. | A1c product owner and deployment configuration owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Agent-selected retention, mutable existing deadlines, ambient policy lookup during undelete, or an unexplained hard-coded expiry |
| Do not expose immediate purge. Every snapshot deletion follows the same quarantine and undelete contract until policy-governed irreversible expiry. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Accidental bypass of quarantine, separate destructive authorization paths, or caller-selected irreversible deletion |
| Expose only `delete_snapshot` and `undelete_snapshot` for snapshot lifecycle. Deletion atomically quarantines the aggregate with a fixed deadline; repeat deletion does not extend it; normal operations return `SNAPSHOT.QUARANTINED`; undelete restores every identity before the deadline; expiry returns `SNAPSHOT.EXPIRED` and physical purge occurs transactionally on a later invocation without a background service. Missing duration uses seven days and invalid explicit configuration rejects rather than falling back. | A1c product owner, Interface owner, Persistence owner, and configuration owner | User agreement recorded in [product discovery](reports/product-contract-discovery.md) | Child-level lifecycle operations, deadline extension through retries, hidden use of quarantined authority, partial undelete, ambient expiry, or invalid-config fallback |
| Defer cross-engine stored-state compatibility and migration until Coding Standards is feature complete. Do not claim a current overlap window or silently reinterpret incompatible state; require stable-release planning to revisit the decision. | A1c product owner and Contracts owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Premature compatibility machinery, accidental indefinite promises, or silent fallback across incompatible engine contracts |
| Support machine-portable closed stores and target Linux, Windows, and macOS while retaining CPython 3.11 and 3.12. Linux is the current development environment, but final platform claims require real execution on every named operating system. | A1c product owner, Persistence owner, and Platform owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | POSIX-only storage identity, caller-enumerated transfer, or Linux-only evidence presented as cross-platform acceptance |
| Keep semantic understanding with the agent. Limit Coding Standards authority to declared mechanical contracts and projections over authored standards, supplied facts, evidence, and decisions. | A1c product owner and Architecture owner | User clarification recorded in [product discovery](reports/product-contract-discovery.md) | Engine-inferred prose meaning, generated semantic judgments, or compatibility framed around nonexistent engine understanding |
| Preserve A1b's demonstrated external-schema correction, equality/identity separation, typed uncertainty, and non-ambient behavior for the eventually selected lifetime. | A1c contract and architecture owners | Accepted A1b evidence and A1/A1b audit | Returning wholesale to A1 |
| Select persistence, object granularity, recovery, compatibility, platform, and version promises from real consumers and loss consequences. | A1c product and domain owners | AUD-008 and routed Contracts/Persistence guidance | Treating A1b guarantees as automatic A1c requirements |
| Compare designs through caller workflows, deletion tests, representative locality probes, and cumulative machinery review rather than structural counts. | Architecture owner | Core, Architecture, and accepted audit synthesis | Smallest-diff, smallest-count, or incumbent-design selection |
| Keep this initial semantic write authority inside the A1c plan directory; regenerate the existing suite-input projection only because the four new tracked paths change its repository-index observation. | Planning and Verification owners | Generated-freshness preflight and A1b suite-input contract | Premature runtime implementation or changed suite semantics |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| A caller requires an operation | Product behavior | A concrete caller workflow invoking the public Interface | Caller-owned use case or executable consumer | Hypothetical future caller | Incumbent API or test treated as demand |
| A handle needs a lifetime | Contract and compatibility | Named continuation/replay scenario across the selected boundary | Consumer retention and deployment facts | Unnamed archival or portability promise | Process restart assumed to require indefinite replay |
| State requires persistence | Durable authority | Non-derivable state, retention period, loss consequence, and recovery owner | Persistence owner and real reopening workflow | Reconstructible cache state | Existing SQLite tables treated as product authority |
| A design is simpler and sufficiently deep | Architecture | Caller-workflow prototype, deletion test, complete composed-design probe, and representative locality changes | Architecture review against accepted standards | Count-only comparison | Complexity moves into callers or another owner |
| Recoverable deletion works | Product behavior and persistence | Accidental-deletion workflow proving aggregate quarantine, ordinary-use exclusion, complete undelete, and expiry purge | Product owner and snapshot-aggregate loss consequences | Treating backup/restore as an undelete Interface | Undelete omits dependent state or quarantine leaks into ordinary standards operations |
| A contract remains conformant | External semantics | Selected Draft validator through the actual public Adapter | Official Draft contract and dependency-owned implementation | Repository-local Draft interpretation | Local implementations agree on the same wrong behavior |
| Evidence can be removed or consolidated | Verification | Claim-level reachable failure, consequence, oracle, overlap, and substitution analysis | Consumer contract or demonstrated prior defect | Test-count reduction | A test is deleted because machinery was renamed or moved |

## Systemic Finding Audit

- Invariant family: cumulative authority, persistence, compatibility, and
  verification machinery added around a small public product Interface.
- Sibling producers and consumers: Standards Engine, Authority, Contracts,
  Identity, Analysis, Applicability, Metadata, Policy Impact, Graph, Verifier,
  generated public models, coverage claims, and retained migration checks.
- Authority and projection inventory: the accepted A1/A1b audit owns the
  historical baseline; A1c discovery must revalidate current consumers and
  state rather than copying that report as current product authority.
- Consumer dispositions: no runtime disposition is authorized. Every retained,
  aggregated, replaced, or deleted concept requires a later design disposition
  tied to a product claim.
- Scope or sequencing replacement: resolve product facts, run bounded design
  experiments, select one composition, then replace this discovery-only scope
  with exact implementation and acceptance authority.

## Simplicity And Ownership Review

**Applicability:** `not-applicable`

**Reason:** Milestone 0 records product and consumer facts and introduces no
candidate composition or permanent mechanism.

Milestone 0 records product and consumer facts only. It introduces no candidate
Module, Interface, Seam, Adapter, composition root, or permanent mechanism, so
there is not yet a produced composition for the Architecture-owned probe to
evaluate. The complete probe becomes mandatory when a candidate composition
exists. That later artifact must include representative changes for one public
field, one internal field, one inspectable concept, one identity rule, and one
compatibility change, plus deletion results for every retained mechanism.

## Milestones

### Milestone 0: Product Facts And Design Inputs

**Goal:** Establish the concrete caller, deployment, lifetime, state, risk, and
compatibility facts required to select an A1c architecture.

**Allowed write set:**

- `docs/plans/standards-engine-a1c/plan.md`
- `docs/plans/standards-engine-a1c/execution-ledger.md`
- `docs/plans/standards-engine-a1c/issues.md`
- `docs/plans/standards-engine-a1c/reports/product-contract-discovery.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

**Tasks:**

- [ ] Name the first real caller and its end-to-end workflows.
- [ ] Define deployment form and supported process, repository, machine, and
  upgrade boundaries.
- [ ] Define handle lifetime and portability requirements.
- [ ] Inventory non-derivable state, retention, loss consequences, and
  operational ownership.
- [ ] Revalidate external consumers, persisted state, and compatibility
  obligations against the current repository and intended deployment.
- [ ] Classify each major A1b guarantee as required, conditional, unsupported,
  or unnecessary for A1c, with evidence.
- [ ] Define bounded design experiments and their deciding oracles without
  selecting an implementation from incumbent structure.
- [x] Regenerate the suite-input projection after the tracked A1c planning paths
  are final. Only its repository-index observation may change; registry,
  suites, file inputs, input uses, and contract version must remain unchanged.

**Acceptance gate:** A1C-P1 is satisfied; A1C-001 is resolved; every remaining
unknown is either assigned to a named experiment or recorded as a blocker; and
the suite-input projection is fresh with only the admitted repository-index
delta; and the plan is re-planned with an admitted architecture-discovery write
set before any prototype or runtime mutation.

**Status:** `Planned`

## Blockers

These blockers constrain architecture and implementation; they do not make the
bounded Milestone 0 discovery work unavailable.

- A1C-001 prevents architecture selection and implementation admission until
  the first caller, deployment form, handle lifetime, non-derivable state, loss
  consequence, and operational owner are selected. It does not prevent the
  Milestone 0 discovery work needed to obtain those facts.
- A1C-002 prevents compatibility, migration, deletion, and persistence design
  until current consumer and retained-state facts are revalidated. It does not
  prevent the bounded inventory that resolves it.
- A1c runtime mutation and all A2 work remain unavailable throughout Milestone
  0 regardless of discovery progress.

## Re-Plan Triggers

- Product facts select a concrete handle lifetime, persistence boundary,
  compatibility promise, platform, or deployment model.
- A real external consumer or retained state is discovered.
- A design experiment requires source changes or another path outside the
  discovery write set.
- Suite-input regeneration changes any field other than the repository-index
  digest or stales another generated artifact.
- A candidate removes an accepted A1b behavior without explicitly removing or
  replacing its product claim.
- A candidate reimplements standardized schema semantics or conflates schema,
  domain, and identity equality.
- Representative change probes show that a candidate moves required reasoning
  into callers or increases cumulative machinery without a distinct claim.
- A normative standards defect is found; that work requires a separate
  project-agnostic standards plan and consumer audit.
- A2 work becomes part of the requested objective.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `A1c implementation and A2 remain unauthorized`
- Final status: `Planned`
