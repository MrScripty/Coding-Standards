# Plan: Standards Engine A2 Logical Authoring

**Plan status:** `Active`

**Current phase:** Milestone 1: proposal-safe logical authoring

**Next slice:** replace the public repository-shaped proposal payload with the
admitted atomic logical change set, implement its private projection through
the existing A1c compiler path, and verify immutable replay and typed failures

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Formation evidence:**
[Current Interface gap and authority inventory](reports/current-interface-gap.md)

## Objective

Let a software-development agent create, revise, remove, and reorganize
standards through one Standards Engine Interface expressed in canonical
standards IDs, authored standards content, explicit relationships, rationale,
and evidence. The Engine, not its caller, must resolve repository paths and
own Markdown/TOML/JSON serialization, corpus and relationship projection,
SQLite persistence, candidate construction, verification, and local Git
publication.

The outcome deepens the existing A2 Authoring Module rather than adding a
second authoring path. It preserves the accepted A1c snapshot, navigation,
analysis, immutable-handle, aggregate-lifecycle, and typed-outcome design and
the accepted A2 review, readiness, application, and recovery lifecycle wherever
their contracts remain applicable. Application ends at the configured local
canonical Git authority; remote push is not part of this plan.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| LA-A1 | The generated public Interface accepts canonical-ID standards-domain intent and never requires a repository path, full-file replacement, raw Markdown metadata envelope, TOML/JSON representation, SQL, Git ref, or Git object ID from the agent. | `contract` | `repository-supported verification environments` | `automated` | `pending` | pending |
| LA-A2 | Through the public proposal workflow, an agent can add a standard, revise its authored policy, explicitly change its relationships or placement, remove it, query the exact proposal revision, and analyze the resulting standards graph after process replacement. | `user-workflow` | `required-real` | `automated` | `pending` | pending |
| LA-A3 | For each supported intent, the Engine updates every mechanically required canonical representation and derived projection selected by current authorities, while semantic relationships, policy-impact declarations, lifecycle meaning, rationale, and evidence originate only from explicit caller or reviewer decisions and are never inferred. | `integration` | `repository-supported verification environments` | `automated` | `pending` | pending |
| LA-A4 | Apply materializes additions, revisions, relocations, and removals in an isolated candidate, rejects invalid or incomplete authority closure, passes the exact current complete checkpoint, creates a proposal-specific standards-compliant commit, and atomically publishes only the verified commit to the configured local canonical ref. | `system` | `required-real` | `automated` | `pending` | pending |
| LA-A5 | A1c snapshot and Analysis behavior and A2 proposal-head, readiness, authorization, application, and recovery invariants remain one coherent implementation with no second parser, graph, analyzer, store, semantic authority, or caller-owned persistence/repository mechanism. | `integration` | `repository-supported verification environments` | `automated` | `pending` | pending |
| LA-A6 | Invalid IDs or content, dangling or cyclic relationships, incomplete semantic declarations, stale proposal or target state, unavailable authority, unsupported retained formats, failed verification, and uncertain publication remain typed and publish no partial canonical result. | `integration` | `repository-supported verification environments` | `automated` | `pending` | pending |
| LA-A7 | The complete public workflow and its real Git/SQLite boundaries pass on the supported Linux CPython 3.11 and 3.12 runtimes, including cold reopen, concurrent proposal-head and target changes, and interruption recovery. | `user-workflow` | `required-real` | `automated` | `pending` | pending |
| LA-A8 | The admitted design passes a pre-canonical minimum viable test for effectiveness, efficiency, correctness, and routed standards compliance, then implementation proceeds without another investigation unless a named unresolved issue threatens an irreversible or high-consequence outcome. | `integration` | `representative` | `manual` | `satisfied` | [Milestone 0 Interface admission](reports/m0-interface-admission.md) |

## Scope

### In Scope

- A canonical-ID public authoring contract for standards-domain changes.
- Explicit creation, revision, removal, relationship change, and logical
  reorganization of standards.
- Agent-authored policy content, semantic declarations, rationale, evidence,
  and lifecycle intent represented independently from repository formats.
- Engine-owned resolution and deterministic serialization of canonical
  standards modules, metadata, corpus membership, policy units, policy-impact
  and broader semantic relationships, coverage authorities, routing
  projections, and other current mechanically affected representations.
- Exact distinction between caller-authored semantic decisions and
  Engine-derived mechanical projections.
- Proposal-specific conventional commit subject and material rationale derived
  from validated proposal information and checked before candidate creation.
- Add, modify, relocate, and remove support in isolated candidate construction.
- Coordinated public/generated/persisted contract replacement or a narrower
  migration only if Milestone 0 finds a real retained consumer or state.
- Current Linux CPython 3.11 and 3.12 support and the existing local
  `refs/heads/main` application target.
- Current plan, ledger, issue, decision, contract, implementation, and
  verification documentation affected by the accepted design.

### Out Of Scope

- Remote push, hosting-provider operations, pull requests, credentials, remote
  ref negotiation, or release publication.
- Letting agents edit repository files, generated outputs, Git objects, the
  working tree, index, refs, SQLite files, tables, or SQL directly.
- Inferring semantic relatedness, `Requires`, `Specializes`, policy impact,
  applicability, evidence sufficiency, routing meaning, or lifecycle intent
  from prose, links, names, or lexical similarity.
- A general document AST, general repository patch language, arbitrary path
  editor, generic graph authoring framework, second standards compiler,
  second Analysis implementation, or second persistence owner.
- Preserving path-and-full-file mutations as a compatibility layer without a
  current independently deployed consumer or retained-state obligation.
- Changing A1c behavior merely to make the implementation convenient. An A1c
  change is permitted only when the admitted design requires it and the same
  owner, contract, and evidence are updated coherently.
- Windows or macOS support without real-platform evidence.
- New background workers, caches, retry loops, mutable phase ledgers,
  measurement frameworks, or speculative extension mechanisms.

## Constraints And Assumptions

### Constraints

- The current A2 implementation remains the truthful baseline until a later
  milestone passes and performs a coordinated cutover. It supports exact
  replacement of existing files; this plan does not describe that baseline as
  logical graph authoring.
- The accepted A1c Architecture is the preferred design vocabulary and
  composition: one generated facade, opaque immutable handles, one compiler and
  graph, one immutable Analysis kernel, one Snapshot/SQLite owner, and a bounded
  Repository Git Adapter.
- The public seam is standards-domain intent. Repository layout and storage
  representation are private implementation knowledge even if internal
  Adapters continue to operate on paths and bytes.
- The Engine may derive only facts mechanically determined by an explicit
  domain decision and current canonical contracts. It must request or reject
  missing semantic authority rather than inventing it.
- Every material pre-canonical investigation must satisfy Development
  Proportionality: one decision, one consequence, the least costly adequate
  method, and an observable stopping condition. Adjacent uncertainty does not
  renew or expand an investigation by itself.
- Prototype code uses disposable state outside production imports and is not
  copied wholesale into the canonical implementation. Only the admitted
  contract and the smallest independently reviewed logic may cross into
  production.
- A candidate that changes normative standards must use the current policy-
  impact query and disposition process. Engine source and proposal records do
  not become members of standards graphs.
- Generated outputs change only through their canonical generators and are
  verified separately for freshness, semantics, and real consumer behavior.
- The complete candidate verification checkpoint runs before local ref
  publication. No passing partial check, commit creation, or Git exit code is
  application success.
- All repository commits for this plan follow the Commit workflow: exact staged
  scope, sensitive-file review, claim-matched checks, and one coherent
  conventional message with material rationale when the subject is
  insufficient.

### Assumptions

- Software-development agents using the generated Python/tool facade remain the
  only current public caller. Milestone 0 refreshes this fact before choosing
  compatibility behavior.
- No retained external A2 SQLite store or independently deployed v19 caller
  requires overlap. Milestone 0 either confirms coordinated replacement or
  re-plans migration and compatibility before production edits.
- Existing canonical loaders and the complete verifier remain authoritative for
  whether an Engine-produced standards repository is structurally valid.
- Existing metadata, policy-unit, policy-impact, coverage, and Router
  authorities expose enough typed read semantics to support a private writer;
  Milestone 0 records any missing write-side contract rather than duplicating
  their semantics.
- The selected local Git target remains the configured Coding Standards
  `refs/heads/main`; a changed target or remote-publication requirement causes
  re-planning.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Treat the accepted A2 implementation as complete only for replacement-based controlled authoring. Use this plan as the sole authority for the corrective logical-authoring continuation. | Product and Planning owners | [Current Interface gap](reports/current-interface-gap.md) and user agreement on 2026-09-03 | The broader interpretation that accepted A2 already provides full logical standards authoring |
| Place one deep standards-domain Interface at the existing Standards Engine seam. Keep repository paths, formats, projection propagation, SQLite, and Git behind that Interface. | Architecture and Product owners | A1c composition, the existing generated facade, and the Interface gap audit | Caller-authored repository-shaped replacement material |
| Require explicit semantic intent; automate only deterministic projection and consistency work. The Engine must reject missing meaning and must not infer relationships or impact. | Standards owners, Product, and Security | Canonical metadata and policy-impact authority contracts | Any interpretation of “automatic supplementary graph updates” as automatic semantic judgment |
| Preserve the A1c compiler/navigation/Analysis/Snapshot design and A2 readiness/application/recovery lifecycle unless Milestone 0 produces a specific conflicting invariant. | A1c, A2, Architecture, and Contracts owners | Accepted A1c and A2 decisions and the current implementation | A parallel logical-authoring engine or an unnecessary A1c rewrite |
| Use coordinated replacement of the current public and persisted authoring representation only if the refreshed inventory confirms there is no retained independent consumer. Otherwise stop and plan the exact overlap or migration. | Contracts and Persistence owners | Current accepted A2 inventory, to be refreshed in Milestone 0 | A speculative compatibility shim or unconditional breaking replacement |
| End application at the configured local canonical ref. Do not add remote push. | Product and Repository owners | User direction on 2026-09-03 | Any earlier interpretation that A2 must publish to a remote |
| Admit production implementation after the selected Interface satisfies the product contract and routed standards in one bounded minimum viable test. Do not add another design cycle without a named high-consequence or irreversible issue. | Development Proportionality, Product, and Planning owners | `workflow.development-proportionality` and the observed prior investigation loop | Open-ended prototype/review/re-plan cycles |
| Keep the existing operation roots and carry one atomic, cumulative, closed `StandardsChangeSet` through `create_proposal` and `revise_proposal`. Support plain authored policy content and registered policy-unit placement, but no public document AST or arbitrary unregistered-section reorganization. | Product, Architecture, Contracts, and Authoring owners | [Milestone 0 Interface admission](reports/m0-interface-admission.md) | Public replacement mutations, a one-edit restriction, a collapsed effect facade, and a general desired-document algebra |
| Cut over to public Interface v20 and Authoring contract v2 without compatibility overlap; preserve Analysis request v4, result/state v5, handle schema v5, and Snapshot store schema v2. | Contracts, Identity, and Persistence owners | [Milestone 0 consumer and state inventory](reports/m0-current-consumer-inventory.md) | A speculative compatibility reader, store migration framework, or unrelated identity/version change |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| The Interface hides repository representation | Public contract and Architecture | Generated call shapes plus representative caller scripts contain canonical IDs and domain values but no repository paths, full-file replacements, SQL, refs, or object IDs | Objective LA-A1 and accepted A1c public-seam decision | Internal Adapter path/byte values, which remain permitted | A caller must know which Markdown or TOML file to replace |
| Logical edits compile to a complete candidate | Domain behavior and generation | Compile each representative intent through the real metadata, policy-unit, policy-impact, Router, graph, coverage, and verifier consumers | Current canonical loaders and declarations | Meaning not explicitly supplied by the caller/reviewer | A locally plausible edit leaves a required authority stale or dangling |
| Semantic decisions are not inferred | Authority and Security | Negative fixtures omit or contradict required relationships, impact, lifecycle, rationale, or evidence and receive the exact typed diagnostic before publication | Standards metadata and policy-impact semantic owners | Natural-language semantic inference | The Engine guesses an edge or silently deletes an affected declaration |
| Proposal revisions remain immutable and replayable | Identity and persistence | Exact revision identity, proposal-head CAS, cold SQLite reopen, and historical query/analysis after later revisions | Authoring and Snapshot contracts | Unsupported historical formats after an admitted coordinated replacement | A stale revision mutates the head or replays through current ambient files |
| Add, change, reorganize, and remove are correct | Candidate repository behavior | Public-workflow fixtures compare the logical result and Git tree, then compile and verify the exact candidate | Explicit test intent and canonical standards compilers | Arbitrary non-standards repository editing | A remove leaves a corpus/edge/coverage reference, or a move changes canonical identity |
| Candidate commits comply with repository policy | Commit behavior | Inspect exact candidate commit subject, body, parent, tree, and verification identity | Commit workflow and validated proposal summary/rationale | Signing unless a separate candidate-signing contract is admitted | Every proposal receives the same generic message or omits material rationale |
| The design is deep enough to implement | Architecture and efficiency | Compare bounded Interface alternatives by caller knowledge, representative change Locality, deletion result, and permanent machinery; then exercise the selected design | Product contract and Architecture composed-design admission | A runtime performance promise without a product budget | Representation knowledge or projection coordination remains spread across callers |
| Implementation effort remains proportionate | Development process | The Milestone 0 admission records `implement` once the selected reversible design passes; another investigation requires all investigation-admission fields | Development Proportionality | Confidence-only investigation | An adjacent uncertainty starts another prototype cycle without changing the decision |

## Systemic Finding Audit

- Invariant family and canonical owner: standards-domain intent must be the
  public Authoring Interface; each standards semantic family retains its own
  canonical owner while the Engine owns orchestration and physical projection.
- Bounded authority, representation, and reachable consumer population: the
  generated facade and schema, Authoring revision aggregate, Engine proposal
  compiler, A1c loaders and Analysis, Snapshot persistence, Repository Git
  candidate construction, canonical module and policy-unit corpora, metadata
  relationships, policy-impact/semantic declarations, coverage authorities,
  Router projections, generated contract artifacts, verifier checkpoint,
  public documentation, fixtures, and actual current consumers.
- Expansion facts: a retained external store, independently deployed caller,
  new semantic owner, unsupported standards representation, new platform, or
  remote publication promise expands the population and forces re-planning.
- Consumer dispositions: Milestone 0 must give every discovered public,
  generated, persisted, standards-authority, repository, verifier, and
  documentation consumer one update, preserve, derive, reject, or re-plan
  disposition before source admission.
- Deletion, consolidation, smaller-Interface, stronger-proof, and
  evidence-replacement alternatives: replace public `ReplacementMutation`;
  reuse the existing compiler, graph, Analysis, Snapshot, Git, and complete
  checkpoint; keep internal representation writers private; delete rejected
  compatibility and generic-editor paths; test through the public Interface.
- Evidence-backed stopping condition: every reachable representation has a
  disposition and one selected Interface completes the representative logical
  workflows through canonical compilation with no public repository knowledge,
  inferred semantics, or unresolved high-consequence invariant.
- Repaired-composition comparison: the correction must move existing
  repository/projection complexity behind the Engine seam. It may add the
  unavoidable write-side compiler and file-topology operations, but no new
  public lifecycle root, graph, analyzer, store, or remote publication path.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: agent-authored policy, explicit semantic relationships, deterministic repository projection, proposal lifecycle, analysis/review, candidate verification, commit description, and local publication have distinct owners and change reasons.
- State, identity, value, time, policy, and mechanism: immutable intent and revision identity remain separate from mutable proposal/target heads; policy meaning remains separate from Markdown/TOML/JSON, SQLite, and Git mechanisms.
  - Canonical authority scope and referenced authorities: Authoring owns intent and proposal transitions, while metadata, policy units, policy impact, coverage, routing, Analysis, Snapshot, Repository Git, and Commit retain their existing semantic authorities.
  - Version roles and owned promises: Milestone 0 classifies the public interface, Authoring aggregate, generated projection, identity domain, and store format independently before changing any version.
  - Supported compatibility overlaps and consumer matrix: none is assumed; coordinated replacement is admitted only after a fresh no-consumer/no-retained-state finding.
  - Material identity-invalidation effects: a change to normalized domain intent or its semantic contract changes revision identity; representation-only serialization changes do not unless the selected contract proves a semantic effect.
- Caller and composition-root knowledge: callers know canonical IDs, authored content, explicit decisions, handles, and typed outcomes; only the Engine composition root knows repository roots, authority paths, formats, generators, store location, target ref, and Git/verifier Adapters.
- Representative change paths and forced owners: add, revise, relate/reorganize, and remove each cross the same Authoring Interface; only affected semantic owners and mechanical projections change, with candidate verification deciding closure.
- Stable Interfaces versus hidden knowledge: the public Interface is one domain intent algebra carried by existing create/revise operations; format-specific writers are internal implementation details and do not become public Adapters.
- Independent evolution, testing, failure, and replacement: domain intent is tested through the public Interface; each private projector is tested against its canonical parser/consumer; Snapshot, Analysis, Git, and verifier behavior remain independently replaceable behind their existing seams.
- Necessary complexity and containment: standards representation diversity and atomic verified publication are inherent; the Engine contains their coordination so callers do not reproduce it.
- Deletion and cumulative machinery result: deleting the private authoring compiler would force repository formats and projection propagation back into every caller; deleting any proposed second graph/analyzer/store or general editor removes incidental machinery, so those mechanisms are prohibited.

## Milestones

### Milestone 0: Validate The Logical-Authoring Contract

**Goal:** Select and admit the smallest standards-domain Interface that supports
the complete representative lifecycle without public repository knowledge or
semantic inference.

**Allowed write set:**

- `docs/plans/standards-engine-a2-logical-authoring/plan.md`
- `docs/plans/standards-engine-a2-logical-authoring/execution-ledger.md`
- `docs/plans/standards-engine-a2-logical-authoring/issues.md`
- `docs/plans/standards-engine-a2-logical-authoring/reports/m0-current-consumer-inventory.md`
- `docs/plans/standards-engine-a2-logical-authoring/reports/m0-interface-admission.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

Scratch prototype files are permitted only under one task-owned temporary
directory outside the repository and are deleted after their evidence is
recorded. No production source, canonical contract, standards authority, or
accepted A2 document changes in this milestone.

**Tasks:**

- [x] Refresh public/generated consumers, persisted stores, supported runtimes,
  current formats, and every standards representation the logical writer must
  project; give each one a disposition.
- [x] Frame and compare radically different Interface shapes, including a
  minimal command algebra, operation-specific authoring, and desired-state
  definition, by Depth, caller knowledge, Locality, failures, and deletion
  result. This comparison is bounded design evidence, not three production
  implementations.
- [x] Select one candidate and run one disposable minimum viable test covering
  create, revise, explicit relationship change/reorganization, remove,
  deterministic projection, cold replay, stale head, and invalid semantic
  closure through real canonical compilers.
- [x] Record effectiveness, caller-efficiency, correctness, standards route,
  negative results, limitations, dependency decision, and version/invalidation
  decisions; confirm the predeclared Milestone 1 write set or re-plan it before
  implementation.
- [x] Return one Development Decision: `implement`, `investigate`,
  `defer-and-implement`, or `blocked`. Only a named unresolved irreversible or
  high-consequence issue may select another investigation.

**Acceptance gate:**

- The inventory has no unresolved reachable consumer; one candidate satisfies
  LA-A1 through LA-A3 at prototype fidelity; canonical compilers accept every
  positive candidate and reject each targeted negative case; the complete
  composed-design probe passes; and the decision is `implement` with an exact
  production write set, or the plan records the precise blocker/re-plan.

**Status:** `Accepted`

### Milestone 1: Implement Proposal-Safe Logical Authoring

**Goal:** Replace repository-shaped public mutations with the admitted
canonical-ID intent and make create, revise, query, and analyze operate on its
complete Engine-produced standards projection.

**Allowed write set:**

- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- `tools/standards_engine/contracts/generated/agent-tools.json`
- `tools/standards_engine/contracts/README.md`
- `tools/standards_engine/standards_engine/__init__.py`
- `tools/standards_engine/standards_engine/_generated_contract.py`
- `tools/standards_engine/standards_engine/authoring.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/standards_engine/logical_authoring.py`
- `tools/standards_engine/standards_engine/tools.py`
- `tools/standards_engine/tests/platform_harness.py`
- `tools/standards_engine/tests/test_analysis.py`
- `tools/standards_engine/tests/test_authoring.py`
- `tools/standards_engine/tests/test_generated_contract.py`
- `tools/standards_engine/tests/test_logical_authoring.py`
- `tools/standards_engine/tests/test_navigation.py`
- `tools/standards_engine/tests/test_platform_harness.py`
- `tools/standards_engine/README.md`
- `docs/plans/standards-engine-a2-logical-authoring/plan.md`
- `docs/plans/standards-engine-a2-logical-authoring/execution-ledger.md`
- `docs/plans/standards-engine-a2-logical-authoring/issues.md`
- `docs/plans/standards-engine-a2-logical-authoring/reports/m1-logical-authoring-evidence.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

`tools/repository_git/` candidate-publication changes and canonical standards
content are forbidden in this milestone. If the admitted design needs any
other file, Milestone 0 must re-plan before implementation.

**Tasks:**

- [ ] Change the canonical schema and generated facade atomically; remove the
  rejected public replacement shape and its old producer/consumer paths unless
  Milestone 0 admitted a real compatibility obligation.
- [ ] Implement normalized immutable intent, deterministic revision identity,
  validation, persistence/reopen behavior, and proposal-head compare-and-swap.
- [ ] Implement the private write-side compiler for only the admitted standard
  lifecycle and relationship operations, delegating existing semantic
  validation to canonical owners.
- [ ] Reuse the exact A1c projection, navigation, and Analysis paths for the
  compiled revision; do not introduce a proposal-only parser or graph.
- [ ] Add focused, generated-contract, persistence, integration, and public
  cross-process tests for positive and typed-negative cases on both runtimes.

**Acceptance gate:**

- LA-A1, LA-A2 through analysis, LA-A3, and the proposal/replay portion of
  LA-A5 through LA-A7 pass through the public generated Interface; the staged
  design matches the Milestone 0 admission and contains no forbidden legacy or
  parallel machinery.

**Status:** `Active`

### Milestone 2: Apply A Complete Standards Change Locally

**Goal:** Extend the existing verified A2 application path to publish the exact
Engine-owned file topology and a standards-compliant proposal-specific commit
to the configured local canonical ref.

**Allowed write set:**

- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- `tools/standards_engine/contracts/generated/agent-tools.json`
- `tools/standards_engine/contracts/README.md`
- `tools/standards_engine/standards_engine/__init__.py`
- `tools/standards_engine/standards_engine/_generated_contract.py`
- `tools/standards_engine/standards_engine/authoring.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/standards_engine/logical_authoring.py`
- `tools/standards_engine/standards_engine/tools.py`
- `tools/standards_engine/tests/platform_harness.py`
- `tools/standards_engine/tests/test_authoring.py`
- `tools/standards_engine/tests/test_generated_contract.py`
- `tools/standards_engine/tests/test_logical_authoring.py`
- `tools/standards_engine/tests/test_platform_harness.py`
- `tools/standards_engine/README.md`
- `tools/repository_git/repository_git/__init__.py`
- `tools/repository_git/repository_git/model.py`
- `tools/repository_git/repository_git/repository.py`
- `tools/repository_git/tests/test_repository.py`
- `docs/decisions/standards-engine-a2.md`
- `tools/repository_git/README.md`
- `docs/plans/standards-engine-a2-logical-authoring/plan.md`
- `docs/plans/standards-engine-a2-logical-authoring/execution-ledger.md`
- `docs/plans/standards-engine-a2-logical-authoring/issues.md`
- `docs/plans/standards-engine-a2-logical-authoring/reports/m2-local-application-evidence.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

Remote configuration, credentials, remote refs, canonical standards policy
content, and unrelated repository tooling are forbidden. Any required path not
listed above triggers re-planning before implementation.

**Tasks:**

- [ ] Materialize additions, modifications, relocations, removals, executable
  modes, and generated projections in the existing isolated candidate
  lifecycle without changing the configured worktree or index.
- [ ] Derive and validate one proposal-specific conventional commit subject
  and material body from explicit normalized proposal facts; include it in
  candidate identity and deterministic reconstruction where required.
- [ ] Preserve readiness, current authorization, exact complete verification,
  application selection, local ref compare-and-swap, observation, durable
  outcome, and observation-only recovery semantics.
- [ ] Prove that incomplete authority closure, invalid graph/corpus state,
  verification failure, stale target, and uncertain publication never become
  application success.
- [ ] Update the A2 ADR and contract documentation to supersede only the
  replacement-shaped public Interface and generic candidate message.

**Acceptance gate:**

- LA-A4 through LA-A7 pass on Linux CPython 3.11 and 3.12 through real local
  Git and SQLite boundaries; candidate commit inspection passes the Commit
  workflow; no remote operation is reachable; and all A1c/A2 preserved
  behavior remains green.

**Status:** `Planned`

### Milestone 3: Objective Acceptance

**Goal:** Independently establish that the complete logical-authoring workflow
satisfies the product contract and standards without retained unnecessary
machinery.

**Allowed write set:**

- `docs/plans/standards-engine-a2-logical-authoring/plan.md`
- `docs/plans/standards-engine-a2-logical-authoring/execution-ledger.md`
- `docs/plans/standards-engine-a2-logical-authoring/issues.md`
- `docs/plans/standards-engine-a2-logical-authoring/reports/final-acceptance.md`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- Exact implementation or evidence paths required to resolve a review finding
  only after this plan is re-planned with that write set.

**Tasks:**

- [ ] Run the focused, contract, integration, user-workflow, dual-runtime, and
  complete-checkpoint evidence named by LA-A1 through LA-A8.
- [ ] Perform independent specification and routed-standards review against one
  identified implementation candidate.
- [ ] Re-run the Architecture artifact probe and deletion test against the
  produced artifact, removing any retained compatibility, registry, Adapter,
  test, or measurement mechanism without a current owner.
- [ ] Record every finding and disposition, final evidence, accepted local
  commit range, and any deferred follow-up with owner and trigger.

**Acceptance gate:**

- LA-A1 through LA-A8 are satisfied; every non-deferred issue has a verified
  disposition; all non-deferred milestones are Accepted or Superseded; and the
  final report identifies the exact accepted implementation and evidence.

**Status:** `Planned`

## Blockers

- `none`

## Re-Plan Triggers

- Milestone 0 discovers a retained independently deployed public caller,
  external store, or supported prior authoring format requiring coexistence.
- A supported logical edit cannot be represented without caller-supplied
  repository paths/raw files or semantic inference.
- A canonical standards authority has no write-side contract adequate to
  preserve its current parser/consumer semantics.
- The selected design requires a second graph, analyzer, persistence owner,
  public lifecycle, generic document model, or other permanent machinery that
  fails the composed-design admission or deletion test.
- The proposal intent or serialization change invalidates A1c/A2 identity,
  persistence, authorization, readiness, application, or recovery behavior
  beyond the decisions recorded here.
- A new dependency, platform, remote publication target, signing promise, or
  compatibility window changes authority, risk, sequencing, or evidence.
- A prototype or implementation gate fails a named objective claim.
- Observed caller knowledge, change propagation, or cumulative machinery is
  materially broader than the Simplicity and Ownership Review predicts.
- Another investigation is proposed after the current reversible design meets
  the contract without a named irreversible or high-consequence uncertainty.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Active`
