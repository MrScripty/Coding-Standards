# Plan: Standards Engine A1c Product Contract And Architecture

**Plan status:** `Planned`

**Current phase:** Binding design complete; production implementation inactive

**Next slice:** Explicitly start Milestone 3 Repository Git and Snapshot
foundation implementation

**Acceptance status:** `partial`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Develop an admissible A1c product and architecture plan that preserves A1b's
demonstrated semantic corrections while retaining only guarantees and
machinery justified by concrete caller, deployment, state-lifetime, and risk
facts. This plan owns discovery, binding architecture, and implementation-plan
admission. It grants no A1c production implementation authority until the
design-definition gate is satisfied and a production milestone is active.

## Objective Acceptance

These claims close planning readiness, not A1c implementation. Runtime
acceptance claims will be added only after a binding architecture and exact
implementation scope are admitted.

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1C-P1 | The first real caller, deployment form, handle lifetime, retained non-derivable state, loss consequence, and operational owner are explicit and supported by inspectable evidence. | `user-workflow` | `not-applicable` | `manual` | `satisfied` | Product-owner decisions and representative workflows in [product-contract discovery](reports/product-contract-discovery.md) |
| A1C-P2 | Current A1b public consumers, persisted-state consumers, operational callers, and compatibility obligations are revalidated without inferring demand from tests or incumbent machinery. | `contract` | `not-applicable` | `automated` | `satisfied` | Bounded current-tree inventory in [product-contract discovery](reports/product-contract-discovery.md) |
| A1C-P3 | Competing A1c designs are exercised through representative caller workflows, deletion tests, and locality probes before one composition is selected. | `integration` | `not-applicable` | `automated` | `satisfied` | Executable prototype and composed-design review in [architecture experiment results](reports/architecture-experiment-results.md) |
| A1C-P4 | The selected composition passes the complete Architecture-owned composed-design probe and identifies every retained concern, authority, lifecycle, Interface, dependency direction, and removal condition. | `integration` | `not-applicable` | `manual` | `satisfied` | [A1c ADR](../../decisions/standards-engine-a1c.md) reconciled with [architecture experiment results](reports/architecture-experiment-results.md) |
| A1C-P5 | A revised implementation plan defines exact runtime write sets, coherent milestones, migration and deletion ownership, claim-matched verification, re-plan triggers, and a separate content-bound acceptance step. | `focused` | `not-applicable` | `manual` | `satisfied` | Milestones 3 through 5 and [A1b-to-A1c migration inventory](reports/a1b-to-a1c-migration-inventory.md) |
| A1C-A1 | The generated v12 Python Interface exposes exactly create/find/delete/undelete snapshot plus query/prepare/resolve/inspect; every request and result is Draft 2020-12 valid and no v11 reader or fallback remains. | `contract` | `not-applicable` | `automated` | `pending` | Milestone 4 |
| A1C-A2 | Snapshot creation captures the complete loader-requested canonical authority closure from one exact current HEAD, persists immutable raw bytes under a unique opaque root, and never rereads mutable repository content for that root. | `integration` | `not-applicable` | `automated` | `pending` | Milestones 3 and 4 |
| A1C-A3 | Equal-content roots retain independent lifecycle and dependent analysis; quarantine, undelete, expiry, purge, and shared-content cleanup are transactional and preserve the complete aggregate. | `integration` | `representative` | `automated` | `pending` | Milestone 3 and public workflow evidence in Milestone 4 |
| A1C-A4 | Query, prepare, resolve, inspect, and every advertised child inspection reconstruct deterministically from the closed store in a fresh process without live repository, provider, authorization, or session substitution. | `system` | `representative` | `automated` | `pending` | Milestone 4 |
| A1C-A5 | Coverage requirements and certificates bind only their typed semantic, relationship, fact-contract, horizon, evidence, and authorization dependencies; unrelated repository or suite-input changes preserve identity while a selected dependency changes it. | `integration` | `not-applicable` | `automated` | `pending` | Milestone 4 |
| A1C-A6 | The complete A1b Authority runtime, wrappers, public v11 forms, historical runtime fixtures, and stale package relationships are absent, with every migration consumer replaced or explicitly retired and no compatibility path. | `integration` | `not-applicable` | `automated` | `pending` | Milestone 4 migration and absence evidence |
| A1C-A7 | Snapshot creation, closed-store movement, locking, path handling, transaction behavior, cold replay, and quarantine work on real Linux, Windows, and macOS with supported CPython 3.11 and 3.12 combinations. | `system` | `required-real` | `automated` | `pending` | Milestone 5 platform evidence |
| A1C-A8 | The eight agent-facing workflows produce typed results or exact typed rejections through the real Python facade; agents need no content hashes, Git revisions, database paths, child catalogs, or project labels. | `user-workflow` | `representative` | `automated` | `pending` | Milestones 4 and 5 |

## Acceptance Procedures

| Claim | Procedure or command | Evidence owner | Unresolved risk |
| --- | --- | --- | --- |
| A1C-P1 | The product owner executes each named caller workflow against the current public Interface, records the deployment and retained handles, and signs the completed discovery fields. | A1c product owner | A test-only or hypothetical caller could be mistaken for product demand. |
| A1C-P2 | Search current package imports, tool registrations, persisted stores, fixtures, and operational documentation; record every match and an explicit bounded-empty result for every searched class. | A1c consumer-inventory owner | An unregistered external consumer cannot be discovered from repository evidence alone. |
| A1C-P3 | Run `python3 docs/plans/standards-engine-a1c/reports/snapshot-aggregate-prototype.py` from the repository root, then compare both public Interface candidates, the A1b direct-object baseline, representative change paths, and evidence substitutions in the experiment report. | Architecture owner | A self-contained prototype may omit a material deployment, platform, authorization, or lifetime boundary. |
| A1C-P4 | Complete the Architecture-owned composed-design probe against the produced candidate composition and record all unavailable or invalid outcomes before ADR selection. | Architecture owner | Review prose could assert simplicity without an inspectable produced artifact. |
| A1C-P5 | Run the plan structure and routed planning suites, then manually trace every architecture decision to one exact write set, milestone, migration/deletion owner, gate, and re-plan trigger. Exact commands belong to the binding implementation plan. | Planning owner | A correct plan structure could still omit a semantic consumer or migration owner. |
| A1C-A1 | Run the Contracts compiler freshness and reachable-definition checks, validate every example and public producer result through `jsonschema.Draft202012Validator`, and prove v11 inputs reject. | Contracts owner | Local producer agreement could still disagree with the selected Draft semantics. |
| A1C-A2 | Create from a controlled Git repository, mutate the repository immediately afterward, reopen the store in a fresh process, and compare requested path closure, raw bytes, semantic projections, and provenance. | Repository Git, Snapshot, and Metadata owners | A traced loader could omit an undeclared authority input. |
| A1C-A3 | Exercise two equal-content roots and dependent analyses through injected transaction failures, quarantine, undelete, expiry, purge, and content reference release. | Snapshot owner | Filesystem and SQLite failure modes may vary by platform. |
| A1C-A4 | Close process one, remove access to its repository and runtime collaborators, then use process two to project and advance every advertised handle solely from the copied closed store and declared current contracts. | Analysis and Engine owners | Deferred cross-engine compatibility remains intentionally unproved. |
| A1C-A5 | Vary one dependency class at a time and compare coverage identities; separately run false-empty horizon fixtures that omit a real consumer. | Analysis and Verification owners | A typed projection can still omit a dependency if no negative fixture selects it. |
| A1C-A6 | Run package, import, path-state, policy-impact migration, and repository-index checks over the final tree; reject every retired path and old public version. | Migration and Verification owners | An unregistered external consumer cannot be discovered from repository evidence alone. |
| A1C-A7 | Run the same registered platform suite on real Linux, Windows, and macOS runners across the supported Python matrix and retain environment-qualified results. | Platform owner | Local Linux simulation cannot prove the required platforms. |
| A1C-A8 | Drive the eight public operations through the generated Python facade in a fresh-process harness, including coordinator/subagent handle transfer and typed lifecycle failures. | Engine Interface owner | Direct package tests could bypass the agent-facing Adapter. |

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
  input freshness projection listed by the active milestone, fixture, suite,
  policy graph, or runtime-state mutation during design definition.
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
- No production mutation is authorized until A1C-P1 through A1C-P5 are
  satisfied and the first exact production milestone is active.
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
- The four read-only and analysis operations with typed
  request/result/rejection behavior and explicit uncertainty without
  valid-looking fallback are inherited A1c behavioral constraints. They are
  not an exhaustive operation list: snapshot creation, discovery, deletion,
  and undelete require a separate bounded Interface experiment. Discovery may
  simplify internal composition but does not remove the four inherited
  behaviors.
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
  SQLite is the selected persistence candidate, while its physical aggregate
  layout remains an implementation-plan decision. Exact current-engine replay
  and dependency-local coverage are required; cross-engine replay remains
  deferred. The custom governed-source interpreter remains repository-process
  machinery rather than presumed product authority.
- The agent owns semantic understanding and judgment. Coding Standards owns
  declared mechanical parsing, validation, routing, identity, graph,
  applicability, storage, and projection behavior; it must not infer prose
  meaning or claim semantic correctness for the agent.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Select the bounded aggregate composition as the candidate for a superseding A1c ADR after product facts, executable experiments, deletion tests, and the composed-design probe. The candidate is not binding production authority until that ADR and an exact implementation plan are separately admitted. | A1c product and Architecture owners | [Accepted audit](../standards-engine-a1-a1b-audit/reports/final-synthesis.md), [product discovery](reports/product-contract-discovery.md), and [architecture experiment results](reports/architecture-experiment-results.md) | The prior decision to keep architecture unselected pending A1C-001 and selection from incumbent A1b mechanisms |
| Select software-development agents acting for developers across projects as the first caller and the Python Interface as the access seam. A1c supplies read, navigation, inspection, and analysis behavior; canonical standards mutation remains outside A1c and requires separate A2 authority. | A1c product owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Treating tests, repository packages, or a human CLI as the first product caller |
| Treat a harness-managed tool call as the primary deployment. Directly embedding the Python package in an agent process is a custom integration whose additional lifecycle and composition choices are owned by that harness. Preserve one public behavior contract rather than creating separate tool-call and embedded product semantics. | A1c product owner and harness integrator | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Two equally authoritative deployment contracts or implementation-specific guarantees leaking into the public Interface |
| Distinguish one engine invocation/process from one multi-turn agent workflow and from one agent instance; do not use the ambiguous term session as lifecycle authority. The normal tool deployment may terminate the engine process after every request, so handles and accepted decisions remain resolvable across invocations, turns, and authorized coordinator/subagent handoffs during the workflow. A replacement agent instance may instead start an independent run without inferred lineage. | A1c product owner, Coding Standards store, and harness integrator | User clarification recorded in [product discovery](reports/product-contract-discovery.md) | Process-local handles, forced replay between turns, or global supersession between independent runs |
| Coding Standards creates a complete immutable snapshot from the configured canonical standards repository's current commit and resolves its opaque handle without requiring callers to manage raw content. The agent cannot select a commit, repository path, tree object, or raw bytes through the Interface. The internally resolved commit is source provenance rather than the storage mechanism or snapshot handle. | A1c product owner, Coding Standards snapshot owner, and canonical-source Adapter | User clarification recorded in [product discovery](reports/product-contract-discovery.md) | Caller-selected history, caller-managed snapshot bytes, mutable snapshots, embedded Git storage, or Git identity as the storage mechanism |
| Retain every snapshot until an authorized caller explicitly deletes it. Do not infer permission to delete from age, inactivity, process exit, agent replacement, apparent lack of internal references, or storage pressure. | A1c product owner and Coding Standards snapshot owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Automatic expiration, implicit garbage collection, or caller-managed raw snapshot storage |
| Store proposed edits as a non-Git change set linked to one complete immutable snapshot. Project the resulting working view through the same navigation, read, inspection, analysis, and verification contracts as canonical content. Deleting the snapshot deletes every linked change set. | A1c product owner, Coding Standards snapshot owner, and Verification owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Copying the full corpus per edit, mutating snapshots, embedded Git repositories, weaker proposal validation, separate change-set read semantics, or orphaned change sets |
| Treat each snapshot, every linked change set, and all analyses and artifacts whose validity depends on them as one lifecycle aggregate. Delete that aggregate atomically, and move it as one closure if movement is supported. Child handles may remain inspectable but do not own independent retention or transfer lifecycles. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Caller-enumerated cleanup, orphaned artifacts, independently moved invalid children, or storage reachability guesses |
| Implement snapshot deletion as aggregate quarantine followed by policy-governed expiry; permit authorized undelete of the complete aggregate before expiry. Keep backup and restore outside the Standards Engine Interface while requiring transactionally consistent publication and a documented administrative file closure. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Immediate accidental data loss, partial undelete, conflating quarantine with disaster recovery, or an engine-owned backup subsystem without a product caller |
| Default snapshot quarantine to seven days. Allow a deployment owner to change the duration only through configuration, not through the agent-facing Python Interface or an individual deletion. Bind each deletion to the exact purge deadline calculated from the effective policy so later configuration changes do not rewrite existing lifecycle decisions. | A1c product owner and deployment configuration owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Agent-selected retention, mutable existing deadlines, ambient policy lookup during undelete, or an unexplained hard-coded expiry |
| Do not expose immediate purge. Every snapshot deletion follows the same quarantine and undelete contract until policy-governed irreversible expiry. | A1c product owner and Persistence owner | User product direction recorded in [product discovery](reports/product-contract-discovery.md) | Accidental bypass of quarantine, separate destructive authorization paths, or caller-selected irreversible deletion |
| Expose only `delete_snapshot` and `undelete_snapshot` as destructive snapshot-lifecycle behaviors. Deletion atomically quarantines the aggregate with a fixed deadline; repeat deletion does not extend it; normal operations return `SNAPSHOT.QUARANTINED`; undelete restores every identity before the deadline; expiry returns `SNAPSHOT.EXPIRED` and physical purge occurs transactionally on a later invocation without a background service. Missing duration uses seven days and invalid explicit configuration rejects rather than falling back. | A1c product owner, Interface owner, Persistence owner, and configuration owner | User agreement recorded in [product discovery](reports/product-contract-discovery.md) | Child-level lifecycle operations, deadline extension through retries, hidden use of quarantined authority, partial undelete, ambient expiry, or invalid-config fallback |
| Add snapshot creation and discovery as required product behaviors. Creation captures the configured canonical repository's current commit without accepting a caller-selected revision. Discovery finds retained snapshot roots after process or agent-instance loss. Use explicit `create_snapshot`, `find_snapshots`, `delete_snapshot`, and `undelete_snapshot` methods over one internal Snapshot Module; do not overload read-only `query`/`inspect`, add a tagged dispatch layer, or use constructor state as hidden lifecycle authority. | A1c product owner, Interface owner, and snapshot owner | Current-tree workflow gap, user clarification, and A1C-E1 in [architecture experiment results](reports/architecture-experiment-results.md) | Treating the inherited four operations as exhaustive, caller-maintained handle catalogs, selectable Git history, hidden mutation, or four independent internal owners |
| Separate immutable canonical-content identity from snapshot-root lifecycle identity. Equal canonical bytes may be deduplicated internally, but each creation produces an independently retained unique opaque snapshot root that owns its dependent aggregate. Agents address snapshots by root ID; the content hash remains internal and cannot allocate work. Deleting one equal-content root cannot affect another. | A1c product owner, Identity owner, Snapshot owner, and Persistence owner | Same-content workflow and A1C-E2/A1C-E4 in [architecture experiment results](reports/architecture-experiment-results.md) | Content equality conflated with lifecycle identity, content hashes exposed as snapshot handles, shared deletion authority, duplicated canonical bytes required by the Interface, project inference, or caller-managed ownership links |
| Select one SQLite-backed Snapshot Module as the A1c persistence candidate. Store each analysis input/decision aggregate once, derive child inspection indexes, and make the closed store the file-administration movement unit. Do not expose a generic object repository, public persistence Protocol, Engine backup/restore Interface, or independent storage authority for every projected child. | A1c product, Persistence, and Analysis owners | A1C-E3 close/reopen, closed-copy, interruption, deletion, and child-inspection cases in [architecture experiment results](reports/architecture-experiment-results.md) | Treating SQLite as semantic authority, caller-coordinated child cleanup, partial aggregate publication, speculative Adapter generality, or independently durable derived projections |
| Keep one compiled public facade contract and domain-owned material identity or compatibility constants. Domain-owned immutable state contains exact typed dependency references whose constructors enforce cardinality and whose generic closure traversal rejects missing or contradictory authority. Do not persist per-operation authority objects or broad version bags when no independent consumer or cross-engine overlap exists. | Contracts, domain, and Standards Engine owners | A1C-E5 locality and deletion analysis in [architecture experiment results](reports/architecture-experiment-results.md) | Umbrella invalidation, duplicated role/cardinality authority, ambient dependencies, or removal of exact dependency binding |
| Bind coverage identity only to typed coverage-relevant subject, relationship, fact-contract, and independent-horizon inputs. Preserve exact current-engine replay from immutable snapshots and retained decisions, but keep repository-global suite-input freshness outside product analysis identity. | Analysis and Verification owners | A1C-E6 coverage-local-invalidation case and evidence portfolio in [architecture experiment results](reports/architecture-experiment-results.md) | False empty impact, graph/catalog self-certification, unrelated repository invalidation, or loss of exact snapshot-local authority |
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

**Applicability:** `applicable`

**Produced artifacts:** [Architecture experiment results](reports/architecture-experiment-results.md)
and [A1c ADR](../../decisions/standards-engine-a1c.md)

- Independent concepts and dimensions: Contracts, repository Git observation,
  content identity, snapshot-root lifecycle, aggregate persistence, analysis,
  and coverage remain distinct concerns with named owners.
- State, identity, value, time, policy, and mechanism: Immutable content values, unique root identity, quarantine time, lifecycle policy, and SQLite mechanics are separated rather than encoded in one handle or object.
- Caller and composition-root knowledge: Agents use opaque root IDs and public
  operations; the Standards Engine composition root alone wires Contracts,
  Repository Git, Snapshot, Analysis, and authority resolvers.
- Representative change paths and forced owners: Public methods, private storage, inspectable children, identity, lifecycle, and coverage changes each have one primary owner and focused evidence in the produced artifact.
- Stable Interfaces versus hidden knowledge: The Python Interface exposes snapshot and analysis behavior while hiding content hashes, tables, child indexes, deduplication, transaction boundaries, and repository layout.
- Independent evolution, testing, failure, and replacement: Contracts,
  repository observation, Snapshot persistence, analysis projection, and
  coverage dependencies retain separate tests and failures and can be
  replaced behind their declared Interfaces.
- Necessary complexity and containment: Immutable aggregate retention, quarantine, exact dependency closure, and deterministic replay are required product complexity contained by the Snapshot Module and domain owners.
- Deletion and cumulative machinery result: Generic object repositories, per-operation authority objects, caller catalogs, project inference, and independently stored derived projections are removed; retained Modules pass the deletion test without duplicating authority.

The composed-design probe records the retained concerns and owners, caller and
composition-root knowledge, stable and representation-leaking dependencies,
representative changes for public, private, inspectable, identity, lifecycle,
and analysis behavior, failure ownership, deletion results, and cumulative
inherent machinery. It selects one deep Snapshot Module and aggregate analysis
storage while retaining Contracts, Identity, and domain owners that pass the
deletion test. The ADR adds one neutral `repository_git` Adapter because both
snapshot capture and the Verifier need the same hostile-environment and exact-
object behavior; deleting it would duplicate that security-sensitive mechanism
or reverse the Verifier dependency into snapshot lifecycle. It declines
mechanism-shaped authority whose removal does not redistribute required
complexity.

The result is an architecture candidate, not production authority. Any ADR
change to its Interface, owner, lifecycle, dependency direction, or deletion
result must rerun the composed-design probe before implementation admission.

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

- [x] Name the first real caller and its end-to-end workflows.
- [x] Define deployment form and supported process, repository, machine, and
  upgrade boundaries.
- [x] Define handle lifetime and portability requirements.
- [x] Inventory non-derivable state, retention, loss consequences, and
  operational ownership.
- [x] Revalidate external consumers, persisted state, and compatibility
  obligations against the current repository and intended deployment.
- [x] Trace creation and discovery after process or agent-instance loss without
  caller-selected Git history or caller-maintained snapshot catalogs.
- [x] Classify each major A1b guarantee as required, conditional, unsupported,
  or unnecessary for A1c, with evidence.
- [x] Define bounded design experiments and their deciding oracles without
  selecting an implementation from incumbent structure.
- [x] Regenerate the suite-input projection after the tracked A1c planning paths
  are final. Only its repository-index observation may change; registry,
  suites, file inputs, input uses, and contract version must remain unchanged.

**Acceptance gate:** A1C-P1 is satisfied; A1C-001 is resolved; every remaining
unknown is either assigned to a named experiment or recorded as a blocker; and
the suite-input projection is fresh with only the admitted repository-index
delta; and the plan is re-planned with an admitted architecture-discovery write
set before any prototype or runtime mutation.

**Status:** `Implemented`

### Milestone 1: Snapshot Aggregate And Interface Experiments

**Goal:** Exercise the required caller workflows against disposable candidate
models and select or reject the snapshot, persistence, inspection, and public
Interface hypotheses without changing A1b production behavior.

**Allowed write set:**

- `docs/plans/standards-engine-a1c/plan.md`
- `docs/plans/standards-engine-a1c/execution-ledger.md`
- `docs/plans/standards-engine-a1c/issues.md`
- `docs/plans/standards-engine-a1c/reports/product-contract-discovery.md`
- `docs/plans/standards-engine-a1c/reports/snapshot-aggregate-prototype.py`
- `docs/plans/standards-engine-a1c/reports/architecture-experiment-results.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

No file under a production package, canonical contract, policy graph,
standards Module, prompt, template, fixture registry, or A2 plan is writable in
this milestone. The executable report is design evidence, not a shipped Module,
validator, migration utility, or compatibility reader.

**Tasks:**

- [x] Model content-addressed canonical content and opaque independently
  retained snapshot roots over a disposable temporary SQLite database.
- [x] Exercise two equal-content roots with independent children, quarantine,
  undelete, expiry, transactional purge, and shared-content retention.
- [x] Exercise active and lifecycle discovery, cold reopen, current-canonical
  capture with no caller revision, and ordinary-operation quarantine refusal.
- [x] Compare one tagged snapshot-management operation with explicit
  create/find/delete/undelete methods over the same internal Snapshot Module.
- [x] Compare aggregate-derived child inspection with A1b's independently
  durable child-object mechanism through deletion and representative Locality
  probes.
- [x] Record the required summary fields, unresolved tombstone/expired-handle
  behavior, authorization seam, platform limits, and every omitted production
  concern instead of silently treating the prototype as complete.
- [x] Complete the composed-design probe for every candidate retained after
  the executable cases.
- [x] Regenerate the suite-input projection after the two tracked experiment
  paths are final; only the repository-index observation may change.

**Deciding command:**

```bash
python3 docs/plans/standards-engine-a1c/reports/snapshot-aggregate-prototype.py
```

The command must exit nonzero on any failed case and report named outcomes for
unique-ID addressing, same-content isolation, active and quarantined discovery,
cold reopen, closed-store copy, interrupted-purge rollback, undelete, expiry,
purge, shared-content preservation, child inspection, Interface comparison,
and dependency-local coverage invalidation.

**Acceptance gate:** A1C-P3 is satisfied; every A1C-E1 through A1C-E6 question
has an evidence-backed disposition or remains an explicit blocker; no
production source or contract changed; the composed-design probe identifies
Interface knowledge, owner, lifecycle, change reason, deletion result, and
failure ownership for each retained concern; generated freshness, focused
planning suites, the complete declarative/checker checkpoint, and diff hygiene
pass.

**Status:** `Implemented`

### Milestone 2: Binding Architecture And Implementation Plan

**Goal:** Convert the selected candidate into one durable A1c ADR and one exact
implementation and migration plan without changing production behavior.

**Allowed write set:**

- `docs/decisions/standards-engine-a1c.md`
- `docs/plans/standards-engine-a1c/plan.md`
- `docs/plans/standards-engine-a1c/execution-ledger.md`
- `docs/plans/standards-engine-a1c/issues.md`
- `docs/plans/standards-engine-a1c/reports/a1b-to-a1c-migration-inventory.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

The accepted A1b ADR and implementation remain historical and behavioral
baselines. Production packages, canonical contracts, generated public models,
runtime fixtures, suite definitions, policy authority, and every A2 artifact
are read-only in this milestone.

**Tasks:**

- [x] Author a superseding A1c ADR that fixes concern ownership, dependency
  direction, public Interface shape, lifecycle, failure ownership, and removal
  conditions without duplicating the experiment report.
- [x] Define opaque snapshot-root ID generation and collision behavior without
  exposing content identity, Git identity, project meaning, or store mechanics.
- [x] Define complete canonical-corpus capture, immutable authority resolution,
  SQLite transaction and file boundaries, aggregate encoding, derived child
  inspection, quarantine, undelete, expiry, and minimal tombstones.
- [x] Define the generated public request/result algebra, authorization and
  provider boundaries, exact dependency closure, local coverage identity, and
  current-engine replay contract.
- [x] Inventory every A1b Module, contract, handle, stored representation,
  generated projection, test family, and consumer selected for retain,
  replace, migrate, or delete; record one owner and disposition for each.
- [x] Replace this plan's design-only milestone structure with exact coherent
  production milestones, write sets, dependency order, migration/deletion
  ownership, focused evidence, objective acceptance claims, and re-plan
  triggers. Listing a later write set does not activate it.
- [x] Reconcile the ADR against the complete composed-design probe. Re-run the
  probe if the ADR changes the selected composition rather than merely making
  an experiment decision exact.
- [x] Regenerate the suite-input projection after the new tracked design paths
  are final. Only the repository-index observation may change.

**Acceptance gate:** A1C-P4 and A1C-P5 are satisfied; the ADR and plan have one
authority for every retained decision; every selected A1b consumer has a
non-blocked migration disposition; every future production path belongs to
one coherent milestone; no production, policy, suite, or A2 artifact changed;
the composed-design review remains valid or is replaced; generated freshness,
focused planning and architecture suites, the complete checkpoint, and diff
hygiene pass.

**Status:** `Implemented`

### Milestone 3: Repository Git And Snapshot Foundation

**Goal:** Implement the two upstream infrastructure Modules and their owned
identity framing without exposing A1c publicly or creating a second semantic
authority.

**Allowed write set:** exact set `M3` in the
[migration inventory](reports/a1b-to-a1c-migration-inventory.md#exact-milestone-path-sets),
plus this plan, ledger, issues, and the generated suite-input projection.

`M3` contains only `standards_identity`, new `repository_git`, new
`standards_snapshots`, and their direct tests and package documentation. The
current Engine, Analysis, semantic loaders, public contract, A1b Authority,
suite registry, policy graph, coverage authority, standards, and A2 are
read-only.

**Preserved or replaced contracts:**

- Preserve Standards Identity's representation-preserving framing and
  domain-separated hashing; add only path/raw-byte and snapshot aggregate
  material framing.
- Extract sanitized Git command execution and exact object/index observation
  from A1b Authority into `repository_git` without standards semantics.
- Introduce unique opaque roots, internal content sets, SQLite persistence,
  discovery, quarantine, undelete, expiry, purge, dependent aggregate storage,
  and derived child lookup behind `standards_snapshots`; accept captured
  content as input without depending on Repository Git.
- Do not expose either new package through the A1b public facade and do not
  retain a generic object repository, native-filesystem capture, backup,
  restore, import, export, merge, or migration Interface.

**Tasks:**

- [ ] Implement and document the public roots of `repository_git` and
  `standards_snapshots` with no private cross-package imports.
- [ ] Preserve hostile `GIT_*` sanitization, exact object typing, bounded
  output, and typed invalid/unavailable outcomes in `repository_git`.
- [ ] Implement SQLite publication and aggregate lifecycle transactions,
  unique UUID root allocation, content deduplication, minimal tombstones, and
  closed-store movement invariants.
- [ ] Prove equal-content root independence, collision rejection, repeated
  deletion without deadline extension, complete undelete, interrupted purge
  rollback, reference-aware cleanup, and cold reopen.
- [ ] Keep every new Module unreachable from the public Engine until the
  atomic replacement milestone.

**Focused evidence:** direct package unit tests for Identity, Repository Git,
and Snapshots; package-manifest verification; generated freshness; and absence
checks proving no A1b public or semantic package imports the new Modules.

**Acceptance gate:** the two Modules independently satisfy their declared
Interfaces and failure contracts; the Snapshot Module can store opaque domain
aggregates without interpreting them; no public behavior, canonical semantic
projection, suite registration, policy relationship, coverage requirement, or
A2 artifact changes; and focused verification plus diff hygiene passes.

**Re-plan conditions:** a semantic loader must depend on Snapshot or SQLite; the
Verifier must depend on snapshot lifecycle; roots require caller-provided
meaning; aggregate storage cannot preserve atomic lifecycle; or a path outside
`M3` is required to make the foundation independently valid.

**Status:** `Planned`

### Milestone 4: Atomic A1c Runtime And Authority Cutover

**Goal:** Replace A1b with the complete eight-operation A1c product across the
semantic loaders, Analysis aggregate, Engine facade, generated contract,
packages, registered suites, graph authority, and coverage evidence in one
coherent repository boundary.

**Allowed write set:** exact sets `M4-runtime`, `M4-contract`,
`M4-verification`, `M4-authority`, and `M4-deletions` in the
[migration inventory](reports/a1b-to-a1c-migration-inventory.md#exact-milestone-path-sets),
plus this plan, ledger, issues, and the A1c cutover evidence report. The named
sets are path identities, not mutable counts or globs. A newly discovered
consumer outside them is a re-plan trigger.

**Preserved or replaced contracts:**

- Preserve semantic Metadata, Applicability, Policy Impact, Graph, routing,
  impact, obligation, reading, fact, coverage, and immutable AnalysisState
  behavior unless the ADR explicitly narrows its authority representation.
- Replace repository-path semantic loading with immutable content-source
  loading composed by Engine; semantic packages do not depend on Snapshot.
- Replace public contract v11 and handle representation v4 with v12 and v5.
  No reader, converter, dual write, fallback, or retained old operation exists.
- Replace generic Authority objects and independent child persistence with one
  snapshot-root aggregate and one Analysis aggregate; derived handles remain
  cold-inspectable through their parent identity.
- Replace repository-global coverage invalidation with dependency-local typed
  inputs while retaining an independently auditable horizon and exact
  certificate/disposition completion equality.

**Tasks:**

- [ ] Refactor Metadata and downstream compilers to consume one immutable
  content-source Interface and prove repository/snapshot parity before deleting
  repository-path authority loading.
- [ ] Implement traced roots-only capture at the Engine composition root,
  rerun compilers against captured bytes, and reject incomplete or
  contradictory closure before transactional publication.
- [ ] Normalize AnalysisState around exact snapshot roots and accepted
  decisions; derive requirements, obligations, reading plans, certificates,
  completion, and child inspection without independent authority rows.
- [ ] Compile the complete v12 request/result algebra and agent-tool
  projection, implement all eight public operations, and map domain failures
  to exact public typed rejections without catching programming errors.
- [ ] Replace package dependencies and Verifier Git imports according to the
  ADR Module graph, then delete A1b Authority and every wrapper or stale public
  export in `M4-deletions`.
- [ ] Replace A1b suites and fixtures with A1c contract, snapshot lifecycle,
  aggregate replay, public workflow, package-closure, and migration evidence.
  Negative fixtures must assert their intended typed diagnostic.
- [ ] Freeze final package, contract, suite, node-catalog, relationship, and
  horizon paths; regenerate derived evidence; renew only the exact registered
  attestations in `M4-authority`; and prove required coverage subjects equal
  valid certificates.
- [ ] Record one disposition for every migration-inventory row and every
  graph-selected consumer. No blocked or implicit disposition may remain.

**Focused evidence:** direct package suites for every changed Module; canonical
Draft validation through Standards Contracts; public facade workflows; cold
process and repository-mutation tests; aggregate transaction and lifecycle
tests; package/import closure; policy-impact migration; false-empty coverage;
registered A1c declarative suites; generated freshness; and absence checks for
every retired path and public version.

**Acceptance gate:** A1C-A1 through A1C-A6 are satisfied on one coherent tree;
all eight operations use only generated v12 values; every advertised handle is
cold-inspectable; no mutable source or ambient collaborator can substitute for
stored authority; all migration dispositions and coverage certificates are
complete; old Authority and v11 behavior are absent; the complete declarative
checkpoint, retained checker checkpoint, generated freshness, package checks,
and diff hygiene pass.

**Re-plan conditions:** any external consumer or retained A1b state is found;
the atomic replacement cannot stay coherent without compatibility overlap; a
domain package must learn SQLite, Git, or snapshot lifecycle; capture closure
requires semantic inference or whole-repository scanning; an advertised child
requires independent retention; a coverage dependency cannot be represented
locally; a selected consumer lies outside the exact sets; or verification
requires extending retained Bash checkers.

**Status:** `Planned`

### Milestone 5: Required-Platform And Final Acceptance

**Goal:** Prove the completed A1c product on every supported real platform and
record content-bound final acceptance without changing product semantics.

**Allowed write set:**

- `docs/plans/standards-engine-a1c/plan.md`
- `docs/plans/standards-engine-a1c/execution-ledger.md`
- `docs/plans/standards-engine-a1c/issues.md`
- `docs/plans/standards-engine-a1c/reports/a1c-platform-evidence.md`
- `docs/plans/standards-engine-a1c/reports/a1c-final-acceptance.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

Production source, contracts, fixtures, suites, graph authority, attestations,
standards, and A2 are read-only. A product correction discovered by acceptance
returns to Milestone 4 through re-planning; it is not repaired inside the
acceptance write set.

**Tasks:**

- [ ] Run the registered A1c platform suite on real Linux, Windows, and macOS
  with the supported Python matrix and record exact environment-qualified
  results without treating simulation as substitution.
- [ ] Move a closed store between supported machines and prove root discovery,
  query, cold analysis projection, child inspection, quarantine, and undelete
  without filesystem or path identity leakage.
- [ ] Run the eight agent-facing workflows through the generated facade and
  prove opaque handle transfer between coordinator and subagent invocations.
- [ ] Re-run the complete repository checkpoint, generated freshness, final
  migration absence checks, coverage/certificate equality, and diff hygiene.
- [ ] Bind final acceptance to the reviewed implementation content and record
  any deferred compatibility work without prescribing Git topology.

**Acceptance gate:** A1C-A1 through A1C-A8 are satisfied; all focused,
integration, contract, system, user-workflow, platform, generated, declarative,
retained-checker, and migration gates selected by those claims pass; every
issue is resolved or explicitly deferred outside the accepted product; the
worktree is clean; and A2 remains inactive.

**Re-plan conditions:** any required-real platform is unavailable or fails; a
closed store is not portable; acceptance needs production or authority
mutation; a final consumer or retained state is discovered; or content-bound
review finds a material contract or architecture change.

**Status:** `Planned`

## Blockers

- `none`; Milestone 3 is planned and has not been started.
- Unknown external consumers remain a standing re-plan trigger.
- A1c production mutation and all A2 work remain unavailable until their own
  exact milestone and lifecycle authority exist.

## Re-Plan Triggers

- Product facts select a concrete handle lifetime, persistence boundary,
  compatibility promise, platform, or deployment model.
- A real external consumer or retained state is discovered.
- A milestone requires a path outside its exact named write sets.
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

- Acceptance status: `partial`
- Deferred follow-ups: `A2 remains unauthorized; cross-engine migration remains deferred until feature completeness`
- Final status: `Planned`
