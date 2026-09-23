# Implementation Plan: Purpose-Separated Standards Engine and Decision Provenance

**Plan status:** `Verifying`
**Current phase:** M3 — qualify the implemented candidate in the supported installed environment
**Next slice:** M3/S3 — complete pinned-client qualification and independent integrated review
**Acceptance status:** `blocked`
**Prepared:** September 23, 2026
**Repository:** `MrScripty/Coding-Standards`
**Inspected baseline:** `366c1d90a24bbfb50973f62b155a5f3396c0f107`
**Execution ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)
**Separate content guide:** [Positive guidance and decision provenance](../../guides/positive-guidance-and-provenance.md)

This document owns the implementation plan. Executed source observations and remaining qualification are recorded in [implementation evidence](reports/implementation-evidence.md); complete plan acceptance is still pending. The baseline is a research reference, not a requirement to revert a newer checkout. Reconcile material differences at M0. Runtime/code acceptance precedes standards-content migration.

## Objective

Extend the existing Standards Engine so a host can provide either an **application** interface for using standards or an **authoring** interface for maintaining them. Application interfaces expose reviewed operational guidance and selectively requested supplementary examples. Authoring interfaces additionally expose the evidence, assumptions, alternatives, and reasoning behind standards.

Provide a complete Engine-mediated path for the later content work: read existing material, revise guidance and registered prompts/templates, author supplementary references and provenance, update relationships, review exact candidate content, publish coherently, and reopen the result. Preserve one authoritative standards corpus and the existing graph, snapshot, proposal, and publication machinery.

The code release establishes representation, discovery, output separation, and authoring capabilities. The separate content migration establishes positive wording, generic applicability, appropriate examples, and the quality of the reasoning. Neither deliverable substitutes for the other.

### Observable completion

A real local client can read a reviewed synthetic rule and its selected example through an application server, while its authoring-only rationale is absent from every application response. A separately configured authoring client can read and revise that rationale and the associated rule through the real proposal/review/publication path. After process replacement, each supported snapshot resolves the corresponding captured content and the active interface still enforces its purpose.

## Governing Practice And Bootstrap Authority

Apply the user-approved future practices below as this task's explicit design and execution contract. They are prospective requirements for this work, not a claim that unpublished standards are already canonical. Their generic formulations and the intended content migration are in guide revision 1, sections G1–G9.

| Practice | Application in this plan |
| --- | --- |
| Positive operational direction | Tasks specify the required action, invariant, evidence, and stopping condition. Historical failure arguments belong in authoring material. |
| Generic normative guidance | Product-specific names and mechanisms remain in this implementation plan, fixtures, and implementation documentation. Existing normative bodies remain unchanged. |
| One coherent implementation unit | Each milestone delivers a usable path or independently necessary qualification; file count and commit count do not determine slices. |
| Early decisive evidence | Qualify the current client/environment in M0 and the new read–author–publish path in M1 before extending coverage. |
| Proportional investigation | Investigate only facts that can change the current design or safe cutover; implement reversible choices directly. |
| Ordinary repair versus replanning | Repair within the admitted objective and ownership; replan when evidence changes the contract, scope, risk, or composition. |
| Discriminating verification | Derive expected visibility independently of the selector under test; distinguish existing failing checks from evidence that still reaches the changed behavior. |
| Consumer-driven compatibility | Adopt one supported new contract. Remove superseded compatibility machinery when replacement improves the design or user experience. |
| Purpose-separated reasoning | Apply one explicit exposure boundary to discovery, reads, inspection, continuations, and transport presentation. |

Retain applicable current requirements for authority, security, integrity, concurrency, persistence, generated contracts, and meaningful acceptance. The user's compatibility direction authorizes contract replacement, not deletion of retained user state or rewriting shared Git history. Any other material conflict with current adopted rules receives an explicit task-local disposition before the affected action. A checker that rejects only a prospective planning convention is not itself authority to rewrite published standards during this phase.

Use the existing Core/Router and the relevant Implementation, Planning, Verification, Development Proportionality, Architecture, Contracts, Security, Library, Generated Contract, IPC, and Persistence guidance. Select Build, Tooling, Documentation, Commit, and detailed contract/replay guidance where the concrete change activates them. Preserve current Python and test conventions; unrelated language and GUI profiles are outside this work.

## Scope

### Code deliverable

Implement trusted purpose selection; typed application projections; explicit application-content eligibility; provenance records and graph associations; coherent supporting-content authoring; snapshot-bound replay; contract generation; purpose-qualified MCP and reference CLI behavior; focused tests; and deployment/cutover documentation. Update affected implementation registrations and generated evidence through their current owners.

Runtime schemas, empty infrastructure manifests, test fixtures, transport instructions, and implementation documentation are code-support changes. Actual standards wording, rule applicability, precedence, normative relationships, operational prompt/template wording, historical rationales, and example selection are content decisions reserved for the later guide.

### Deferred concerns

Positive rewriting of the real corpus and its operational prompts/templates, provenance backfilling, substantive improvements to individual standards, and real-project examples belong to the content migration. A model-based positivity scorer, automatic prose rewriter, new search/indexing platform, remote authorization system, additional database, and replacement graph engine are outside this implementation. A file-based application distribution is a separate adapter only if an actual consumer requires one; the accepted delivery boundary here is the Engine API and its local transports.

The feature controls content supplied by the Engine. It does not erase material already present in a model conversation, constrain information learned during training, or prevent an agent with independent filesystem/Git/database access from reading that material.

## Source-Backed Starting Point

The inspected implementation provides useful foundations:

- `agent_navigation.navigate()` implements compact reads by removing relationship rows from an otherwise normal read result. Compactness currently changes detail, not audience. [S1]
- `engine.py` reads complete module bytes or scoped policy-unit content; snapshot-child relationship inspection includes rationale. These paths need one consistent purpose boundary. [S2]
- The MCP focused catalog contains both navigation and authoring operations. `tools.py` opens the local authorizer, while `invoke.py` can list schemas/examples and dispatch generated operations. Catalog filtering alone will not cover these entrypoints. [S3, S4]
- `ChangePurpose` already records summary, rationale, and evidence. `revise-standard`, `revise-policy-unit`, routing edits, and relationship edits already exist. Extend these paths rather than implement a second editor. [S5]
- Policy-impact models separate relation semantics from neutral graph topology. Metadata, snapshots, and the contract compiler already supply the corresponding ownership boundaries. [S6, S7]
- The complete structural checkpoint does not execute Python unit tests or establish prose correctness. Acceptance must run the affected implementation tests separately. [S8]

## Binding Decisions

### D1 — Host-selected purpose, independent authorization

Use exactly two initial purposes: `application` and `authoring`. Require the purpose at the public Engine/facade construction boundary and in MCP/reference-CLI launch configuration. Keep it immutable for the lifetime of that interface. A tool request, handle, query parameter, or detail option cannot change it.

One implementation can serve separately configured registrations. An application process exposes application operations; an authoring process exposes maintenance operations according to existing authorization. Authoring read access is distinct from permission to mutate, review, apply, recover, or administer state. Preserve the authorization injection point and accurately document the existing owner-operated local always-allow adapter; this work does not turn it into a multi-user permissions service.

The `--advanced` catalog option, if retained, selects additional operations only within the host's purpose and capabilities. Application snapshot capture may create Engine-owned derived state as part of a read, while standards mutation and snapshot administration remain authoring operations. Tool annotations describe behavior; server dispatch and domain checks enforce it. [S3, S10]

### D2 — One content authority, explicit application eligibility

Preserve the existing normative role model. `core`, `workflow`, `topic`, `profile`, and `reference` still describe normative meaning and applicability; they do not establish exposure by themselves.

Add a small application-exposure manifest owned by the standards-content loading/authoring boundary. An application-eligible entry identifies an existing canonical module or registered prompt/template artifact and binds the exact reviewed content, material metadata, and owned application-facing routing inputs. For the first implementation, qualify complete modules, including their headings, tables, examples, footnotes, and links. A policy-unit read inherits its containing module's eligibility. This avoids a new fragment-redaction language and prevents whole-module reads from exposing unreviewed remainder text.

Support three derived states: `unreviewed`, `current`, and `needs-review`. A current entry is produced only through explicit content-authoring intent and the existing reviewed publication workflow. The Engine computes the binding from the final candidate; the agent supplies the decision, not a guessed digest. Unchanged eligibility is not automatically renewed after a content change. Withdrawal is an explicit content change with an impact disposition.

Create an empty manifest for the production corpus in the code phase. Existing normative bytes remain unchanged and initially authoring-readable. Application requests requiring unqualified material return a clear incomplete/unavailable result. This is an intentional clean cutover, not a compatibility fallback. The code tests use their own reviewed synthetic corpus.

Application eligibility is a reviewed editorial classification. Mechanical validation establishes its binding and completeness, not whether the language is genuinely positive or the reasoning is sound.

### D3 — A small provenance record model

Add a typed loader and model for decision-provenance records in the existing content-loading ownership boundary. A proposed internal implementation file is `tools/standards_metadata/standards_metadata/supporting_content.py`; confirm its fit in M0 without creating a new package merely for file organization.

A record has a stable ID, a canonical module or policy-unit subject, a subject-revision binding, rationale, and evidence references. Optional sections hold assumptions, limits, alternatives/trade-offs, reconsideration conditions, and supersession links. Distinguish documented original reasoning, reconstructed history, a current justification, and an explicitly unrecorded origin. Empty optional sections are valid; an unrecorded origin does not require fabricated evidence or justification.

Reuse the existing evidence-reference representation when its identity and provider semantics match. Preserve these distinctions:

- change purpose explains a proposed edit;
- relationship rationale explains a graph association;
- decision provenance explains a standard;
- technical provenance identifies source/snapshot material.

Provenance is authoring-only by content class. Existing reference modules provide supplementary examples, with explicit application eligibility after content review. Registered prompts and templates are operational aids: their policy meaning remains owned by linked standards, and their application exposure requires the same exact-content review. Real rationale, reference text, and prompt/template rewrites remain absent from code-phase infrastructure manifests.

### D4 — One source for each graph association

Extend the standards relationship compiler to express a standard's descriptive association with decision provenance. Register provenance as a supplemental artifact, not a normative rule or dependency. Declare its subject association once in the provenance record; derive the corresponding neutral graph edge from that declaration. Preserve existing source-owned declarations for other relationships. A second editable copy of the subject–record link is unnecessary.

Use existing reference relationships for supplementary references when their semantics fit. Descriptive provenance associations do not acquire `Requires`/`Specializes` meaning or automatic policy-impact propagation. A separate, explicitly declared impact relationship may require review when evidence undermines a rule; it does not automatically rewrite or invalidate the rule's semantics.

The generic graph engine remains neutral. The standards-aware layer constructs the view permitted for each purpose and filters traversal before producing results. A hidden intermediate node cannot create a visible application traversal path. Keep authoring impact traversal over the complete relevant graph.

For a requested application route, compute the actual required dependency closure and establish that its required content is eligible before returning a complete reading plan. Preserve unknown applicability. A required authoring-only dependency produces an unresolved application path; it is not silently dropped. Optional example discovery remains selective and is separate from prerequisite closure.

### D5 — Application DTOs, not field deletion from authoring results

Add one purpose-aware projection owner, proposed as `standards_engine/context_projection.py`. It constructs explicit application result types from qualified domain values. Authoring projections retain the material needed for maintenance. Existing compact/full detail is subordinate to purpose.

Application results may contain reviewed policy content, essential applicability, permitted dependency facts, selected examples, bounded technical identity, and permitted next operations. Authoring rationale, source excerpts from private support records, proposal history, audit discussion, and maintenance targets remain in authoring results.

Route all public paths through this boundary: focused navigation, native query variants, routing facts, reads, relationship traversal, inspection, summaries, and continuations. Apply operation admission before invoking authoring or administrative behavior. A handle identifies material; it never grants additional exposure or mutation authority.

MCP JSON text, `structuredContent`, tool descriptions, reachable schema definitions, reference-CLI schemas/examples, registered prompt/template reads, rendered output, and client-visible diagnostics must agree. Renderers accept qualified results; they do not perform independent hiding. Host-private logs remain separate from client-visible output.

No new search API is required. Any later search or exporter must consume the same qualified content boundary. No cache is added; an affected existing cache must include the purpose and material content binding where relevant.

### D6 — Coherent authoring and publication

Extend the existing logical edit algebra with the minimum operations for putting/revising and retiring provenance and for approving or withdrawing application exposure. Existing standard and reference revisions remain the normative/reference content-editing mechanism. Add one bounded edit for an existing registered prompt or template, identified through its existing opaque authoring target. It replaces authored title/body content through that artifact owner, retains or explicitly revises declared consumer relationships, and permits no arbitrary repository path or source-code write. Extend qualified reads to these registered artifacts so the later migration can review and verify them through the Engine. Names are finalized in the public contract in M0/M1; operation behavior is binding here.

Support provenance-only maintenance and coordinated rule/reference/prompt/template/provenance/exposure changes in one `StandardsChangeSet`. An unordered atomic change set resolves against the final candidate, including references to records created in that same set. Conflicting edits and dangling references reject before publication.

Use existing proposal, analysis, review, apply, and recovery. Review binds the exact material content and actual consumer/impact dispositions. Application exposure becomes active only when the reviewed candidate is published to accepted authority. Draft proposal reads remain authoring operations.

Standard revision or movement preserves canonical identity where meaning remains the same, with updated locator and binding. Retirement or division records explicit successor and relationship dispositions. Provenance corrections affect their own content and relevant reviews; they do not automatically advance unrelated normative revisions or renew every consumer certificate.

### D7 — Replay through the existing store

Capture exposure declarations, provenance, relationship declarations, and required routing material through the existing `ContentSource`/snapshot machinery. Include them in compilation and frozen replay. Derived historical reads use captured records, never the current working tree as a substitute. Reuse the existing SQLite aggregate/proposal store and Git publication protocol.

A wording change alters its representation binding. A substantive rule change alters its owned semantic revision. A provenance-only edit changes the supporting record and snapshot but does not change unchanged normative meaning. An opaque snapshot ID may change when hidden captured content changes; constant-time behavior and complete side-channel noninterference are outside the promised exposure guarantee.

Supported new-contract snapshots remain immutable across process replacement, including their captured exposure decisions. Exposure withdrawal governs newly accepted snapshots; historical snapshots preserve their recorded decisions. Retrospective content revocation and erasure of already delivered context are not promised by this feature. Unsupported older stores or handles receive an explicit outcome. Current purpose checks apply even to a valid handle received from an authoring client.

### D8 — Clean compatibility cutover

Maintain one supported post-change interface and representation for each changed boundary. Regenerate native models and tool schemas together; update in-repository consumers in the same coherent change. Retire superseded purpose-less entrypoints, mixed catalogs, duplicate serializers, and compatibility branches made unnecessary by this design. Preserve existing mechanisms that remain the best implementation, rather than removing them solely because they predate the feature.

Allocate versions from the actual changed wire, persisted, and interpretation contracts. Version 30 is the inspected Engine interface, not permission to hard-code the next number without checking the implementation base. Do not couple unrelated version domains.

Before installed cutover, identify active proposals, readiness records, and recovery-required applications. Complete required old-version recovery before replacement or retain the affected work with an explicit operator disposition. Preserve old store bytes and Git history. A fresh supported store may capture current canonical Git content; automatic deletion, hidden conversion, old-format readers, dual-write paths, compatibility aliases, and fallback execution are outside the design. An unsupported store is not equivalent to an empty store.

### D9 — Deployment and context boundary

Run the canonical checkout and Engine store behind the purpose-configured server. Application agents receive only the application registration and approved results. Authoring sessions are separate; a fresh application session receives only reviewed application material after a standards-authoring task. The Engine does not claim to erase an existing conversation.

Filesystem/host configuration establishes whether an agent can independently read the checkout, store, or private logs. Document that requirement explicitly. Enforcing OS isolation, remote roles, and a file exporter is outside this local Engine implementation.

## Responsibility And Change Map

Paths below are bounded implementation areas, not permission for unrelated rewrites. Before each edit, name its exact files in the task or ledger. A newly discovered file inside the same affected owner can be included without a new planning cycle when objective, contract, risk, and acceptance remain unchanged.

| Owner / existing area | Allowed change |
| --- | --- |
| `tools/standards_contracts/` | Named operation wire variants within the existing compiler, exact root closure, and capability-coverage tests. |
| `tools/standards_engine/contracts/` and generated contract outputs | Purpose-qualified operation/results, logical supporting-content edits, version allocation, authored examples, regenerated native and tool schemas. |
| `tools/standards_engine/standards_engine/` | Trusted construction context; shared application projection; navigation/inspection; coherent authoring; supporting-content capture and bounded diagnostics. Preserve unrelated runtime behavior. |
| `tools/standards_metadata/standards_metadata/` and relevant schema documentation | Structural supporting-content and exposure loading, canonical bindings, exact source capture; no normative judgment or graph policy. |
| `tools/standards_policy_impact/` | Supplemental provenance artifact/relationship interpretation and validation; one association declaration; purpose-relevant relationship classification. |
| `tools/standards_graph/` | Standards-specific graph composition/view integration only if its current owner is the appropriate seam. |
| `tools/standards_analysis/` | Affected change descriptors, localized impact and evidence binding for the new record/edit kinds. |
| `tools/standards_snapshots/` | Only a demonstrated capture/replay or supported-format change; reuse existing persistence otherwise. |
| `.agents/skills/standards-engine/scripts/invoke.py` and connection references | Required host purpose; filtered list/schema/example and dispatch; accurate installation and cutover procedures. |
| Affected package tests and existing Engine client harnesses | Independent exposure fixtures, real publication/replay, unsupported-contract and purpose-escalation cases. |
| `evaluation/standards-effectiveness/` | Empty `application-content.toml`, empty supporting-content registration as needed, actual implementation graph registrations, affected suite definitions and generated input metadata. No authored real-policy exposure approvals. |
| Plan bundle and touched implementation READMEs | Current plan state, concise evidence/dispositions, and durable implementation contract changes. |

Normative files in Core, Router, `workflows/`, `topics/`, and `profiles/`, real reference content, real `prompts/` and `templates/` content, and substantive policy declarations are preserved during code implementation. Review those bytes once at final acceptance against the bound implementation base; keep this as task evidence rather than a permanent freeze checker.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: Normative meaning belongs to standards authors; content structure to metadata loading; relationships to the standards graph compiler; exposure to Engine projection; permission to host authorization; storage and publication to existing owners.
- State, identity, value, time, policy, and mechanism: Canonical content and immutable snapshots hold values and revision history. Host construction selects purpose. Purpose is neither a content identity nor a permission grant. There is no mutable global current-purpose state. Each changed wire or persistence contract owns its version; unchanged normative semantics remain unchanged.
- Caller and composition-root knowledge: Callers use canonical IDs and existing opaque handles. The host selects purpose and authorization. Clients do not select paths, private record storage, graph encodings, or sanitization steps.
- Representative change paths and forced owners: A new rationale changes one support record and its derived association; a positive rewrite changes the owning standard plus explicit exposure approval; a new transport consumes the qualified facade; an unrelated provenance edit leaves normative semantic revisions intact.
- Stable Interfaces versus hidden knowledge: Content loaders return typed values; projection consumes those values; serializers render qualified results. The generic graph receives neutral contributions and knows no agent-audience policy.
- Independent evolution, testing, failure, and replacement: Prose review, exposure checks, relationship compilation, and transport tests have separate claims. A missing provenance record can be represented honestly; it does not invalidate a rule unless the authored policy makes that evidence necessary.
- Necessary complexity and containment: Trusted purpose, exact reviewed eligibility, supporting-record capture, and localized impact are necessary to the selected exposure and authoring promises. Existing graph, contract, snapshot, authorization, and publication owners contain their mechanics. User-facing catalogs expose only relevant operations.
- Deletion and cumulative machinery result: Removing purpose enforcement or bound eligibility breaks the exposure promise. A second graph, store, workflow lifecycle, semantic prose detector, or duplicate rationale authority would add incidental complexity and is omitted. Retain two purposes, one small supporting-content representation, one exposure manifest, one projection boundary, and minimal existing contract/authoring extensions.

The exposure tests address a real boundary that current full reads/inspection do not provide. A new general evidence framework is unnecessary. Synthetic content plus existing integration harnesses is the smallest adequate mechanism. Keep only tests that decide a named behavior; use the existing test runner and failure reporting.

## Milestones

### M0 — Bind the baseline and qualify the current path

**Status:** `Accepted`. **Goal:** remove only uncertainties that could invalidate the code-first implementation or safe cutover.

**Allowed write set:** this plan bundle; temporary disposable fixtures outside the canonical corpus. Repository source remains unchanged.

**Tasks:**

1. Inspect repository status and current revision. Map the advertised Engine/facade, MCP focused/advanced, reference CLI list/schema/example/invocation, generated definitions, and existing client tests. Confirm module-wide standard edits, preservation of existing policy-unit scopes during a whole-module rewrite, metadata/graph owners, and the actual supported Python/environment commands.
2. Run the current minimal navigation/authoring/client path and affected package tests in the locked environment. Record existing failures by identity and where execution stops; determine whether they obscure a later acceptance claim.
3. Record the current client/store consumer matrix and pending-operation dispositions. Finalize proposed internal filenames and the next actual contract version. Reuse the existing authorizer and publication machinery.
4. Stop discovery once every listed public output/mutation path has an owner and disposition and the smallest real client path is executable or precisely blocked. Begin M1 for independent work even when a rollout-only fact is unresolved.

**Acceptance gate:** a bounded entrypoint map, material baseline differences, current environment result, and concrete cutover facts. This gate does not require a separate research framework or a normative standards edit.

### M1 — Deliver one complete purpose-separated read–author–publish path

**Status:** `Implemented`; depends on M0's implementation-relevant facts. **Goal:** prove the architecture with working production code over a small synthetic corpus.

**Allowed write set:** Engine contracts/runtime/tests; supporting-content loader/tests; policy-impact schema/compiler/tests; affected graph composition; reference CLI/MCP construction; empty infrastructure manifests and strictly affected registrations; plan bundle.

**Tasks:**

1. Implement host-purpose construction, typed qualified read/related results, strict application eligibility, and provenance loading/association. Extend the canonical contract and regenerate its consumers in the same slice.
2. Implement provenance, registered prompt/template, and exposure logical edits through existing standard/reference editing and proposal/review/apply. Publish a synthetic rule, reference, operational prompt, template, and rationale together in a disposable Git repository; materialize the actual serialized files through the Engine.
3. Exercise an application read and authoring inspection through the real local transport. Demonstrate that full detail, a direct hidden ID, an authoring handle, and a request-supplied purpose cannot disclose rationale or invoke mutation.
4. Confirm the production corpus's empty eligibility state returns a bounded unavailable result while the authoring path can still read the unchanged real standards. Confirm new edits are reachable, not stubs.

**Acceptance gate:** C1–C4 on the synthetic path plus focused contract/compiler tests. Review the integrated design now; expand only after the real path demonstrates the selected boundaries.

### M2 — Complete public-surface coverage, coherent changes, and cold replay

**Status:** `Implemented`; depends on M1. **Goal:** make the guarantee hold across the complete bounded consumer population.

**Allowed write set:** the affected M1 owners plus Engine analysis, snapshots only if required, rendering, CLI discovery helpers, client harnesses, and their tests/registrations.

**Tasks:**

1. Apply the same admission/projection boundary to native query, routing facts and descriptions, whole-module/policy reads, inspection kinds, continuations, schema closures, CLI examples, diagnostics, and both MCP result encodings. Verify hidden intermediate nodes and invalid required closures.
2. Support provenance-only edits, whole-module rewrites with explicit registered-scope dispositions, same-change-set references, moves, retirements, subject-binding changes, exposure withdrawal, and renewed approval of a materially changed module. Preserve localized semantic revisions and impact obligations.
3. Capture and reopen all supporting inputs in cold processes. Exercise concurrent proposal revisions and interruption at existing publication boundaries; reuse the current recovery contract and actual SQLite/Git guarantees.
4. Retire replaced purpose-less paths and update all in-repository consumers. Verify unsupported old requests/handles/stores are explicit and non-destructive. Keep unrelated historical cleanup outside this work.

**Acceptance gate:** C2–C7 and C9 pass across all inventoried surfaces; a second process reproduces exact supported-snapshot reads. Newly exposed integration assumptions receive bounded resolution rather than expansion into unrelated infrastructure.

### M3 — Qualify installation, review, and hand off to content authoring

**Status:** `Verifying`; depends on M2. **Goal:** deliver the code capability required to carry out the separate guide.

**Allowed write set:** touched runtime/contract files for ordinary repairs; existing real-client harnesses; installation/cutover documentation; implementation evidence and generated registrations; plan bundle. Normative bodies remain preserved.

**Tasks:**

1. Run the revised Engine in its locked installed environment through the real supported MCP client and reference CLI. Inspect actual purpose-specific catalogs and execute application navigation and authoring publication/recovery in disposable repositories. Reconnect clients after the contract change.
2. Run affected package suites, generated freshness/shape checks, and the full structural checkpoint separately. Reconcile existing failing checks with the changed claim paths; preserve unresolved acceptance honestly.
3. Obtain independent integrated review against the prospective practice contract, exposure threat boundary, data preservation, and exact material candidate. Repair findings in the same scope; repeat evidence only where affected.
4. Record cutover commands, consumer/store dispositions, supported new versions, and the content-authoring API operation map. Confirm normative bytes are unchanged, fixtures remain test-only, and every required code claim is satisfied before marking this plan `Accepted`. The handoff map must include every guide operation, including module metadata, registered prompts/templates, reference creation, provenance maintenance, exposure approval, and graph changes; it may not substitute direct file edits for a missing content operation.

**Acceptance gate:** C1–C10. Code acceptance authorizes the content guide's workflow; it does not certify the real corpus as positively written or application-eligible.

## Objective Acceptance

Source evidence is recorded in [implementation evidence](reports/implementation-evidence.md). Pending claims retain their stated qualification limits; the overall plan is blocked on the supported installed environment and independent final review.

| ID | Observable criterion | Kind / environment / mode | Deciding evidence | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | Host purpose is immutable and request input cannot elevate it or grant mutation. | contract + system / representative local host / automated | Independently authored operation matrix; actual facade/MCP/CLI calls; verify rejected mutations produce no canonical change. | `pending` | pending |
| C2 | Application reads, relationships, full detail, inspection, summaries, schemas, examples, and continuations contain only permitted material. | contract + system / representative / automated | Distinctive synthetic markers and expected permitted fields authored independently of projection code; inspect JSON, text, catalogs, and nested fields. | `pending` | pending |
| C3 | Required routing closure is complete or explicitly unavailable; hidden support nodes do not alter permitted traversal paths. | integration / not-applicable / automated | Small explicit graph fixtures, required/optional cases, unknown facts, and hidden intermediary cases. | `pending` | pending |
| C4 | The Engine can publish coordinated guidance/reference/prompt/template/provenance/exposure changes and later provenance-only changes. | system / representative Git + SQLite / automated | Public authoring operations, actual candidate materialization, accepted-ref readback, and independent content assertions. | `pending` | pending |
| C5 | Supported snapshots reopen after process replacement with matching content and current-purpose enforcement. | system / required-real local processes + store / automated | Two-process capture/read; later source mutation; real store reopening; exact requested subject/revision checks. | `pending` | pending |
| C6 | Draft exposure cannot become application-visible before reviewed publication; changed content cannot silently retain stale approval. | integration + system / representative / automated | Before/after publication reads; stale bindings; concurrent revisions; withdrawal; interruption/recovery. | `pending` | pending |
| C7 | One new contract is supported across in-repository consumers; old unsupported formats fail without corrupting retained data. | contract + system / representative / automated | Version/consumer matrix, old-format fixtures, unchanged-store checks, actual startup outcomes. | `pending` | pending |
| C8 | The installed local transports execute the complete supported workflow with correct catalogs and bounded diagnostics. | release-artifact + system / required-real locked environment and actual MCP client / automated | Existing real-client harness extended for both purposes; installed entrypoint and CLI execution. No paid model turn required. | `blocked` | [Environment limits](reports/implementation-evidence.md#remaining-acceptance) |
| C9 | Provenance-only changes leave unchanged normative semantics and unrelated impact requirements stable. | integration / not-applicable / automated | Independent before/after domain revisions and local impact expectations; allow changed opaque snapshot identity. | `pending` | pending |
| C10 | The code release preserves real normative bodies and leaves an executable content-migration path. | acceptance review / inspected repository / manual + automated comparison | One-time scoped diff review; API operation map; empty real-corpus eligibility; independent final review. | `pending` | pending |

A marker-absence test proves only sampled disclosure paths; pair it with positive field assertions, operation admission, and the complete bounded entrypoint inventory. Codepoint text equality is used where exact returned content is the contract. Generated freshness proves derived files are current, not that the prose is correct or the exposure boundary works.

For a failing baseline, record whether the same test reaches the changed behavior. An unchanged failure identity or count cannot establish that behavior. Repair an obstructing local check, add a focused discriminator, or leave the affected claim pending. Unrelated debt is separately dispositioned.

### Execution commands

Use an existing isolated interpreter installed from `tools/standards_contracts/requirements.lock`, following the current environment instructions [S9]. Commands below illustrate the existing verification entrypoints; M0 records the exact supported invocations and M3 updates examples for the new contract.

```bash
# Run from the repository root; ENGINE_PYTHON names the locked interpreter.
: "${ENGINE_PYTHON:?Set ENGINE_PYTHON to the locked Engine interpreter}"
PYTHONPATH=. "$ENGINE_PYTHON" -m unittest discover -s tools/standards_engine/tests
PYTHONPATH=. "$ENGINE_PYTHON" -m unittest discover -s tools/standards_metadata/tests
PYTHONPATH=. "$ENGINE_PYTHON" -m unittest discover -s tools/standards_policy_impact/tests
PYTHONPATH=.:tools/standards_verifier "$ENGINE_PYTHON" -m unittest discover -s tools/standards_verifier/tests
```

Run additional touched-owner suites from their established READMEs. Execute the repository structural checkpoint separately through the Engine. Regenerate contracts with the existing compiler and generated-input mechanism, then check freshness. The new `--purpose` syntax and new edit schemas are proposed work, not commands claimed to exist today. Retain the supported transport protocol unless a separately evidenced interoperability issue requires changing it.

## Execution Discipline

The integration owner maintains this plan and serializes shared contracts, manifests, generated files, and publication. Parallel read-only review is useful. Parallel coding is conditional on actual independent write sets; the default sequence here is one integration owner. Create a branch/worktree for the breaking integration when it provides review or rollback isolation, record its purpose and final disposition, and preserve reachable commits. This plan prescribes no commit topology or count.

## Re-Plan Triggers

Ordinary implementation/test repair continues within the admitted contract. Replan only when a newly discovered consumer needs a materially different exposure boundary, existing storage cannot support the replay promise, a required content edit cannot be represented coherently, the host-access assumption is false, or an existing recovery obligation changes safe cutover. A broader proposal to replace the graph/store/authentication system requires a separately justified decision.

A new implementation file, additional focused assertion, or unchanged review record is not by itself a reason to reopen design admission. Investigation ends when the fact that could change the decision has been resolved. Independent work continues while a real environment or rollout claim is pending.

## Blockers

The available Python 3.13 environment is outside the supported locked range. Official MCP SDK/installed-client qualification and independent integrated review remain outstanding. User installation and pending-store recovery facts remain operator-owned. Remote Git push is unavailable; the user selected changed-files ZIP delivery.

## Code-To-Content Handoff

Hand off the accepted runtime revision, new supported interface versions, purpose-specific connection commands, the tested operation map, and the authoring workflow demonstrated in a disposable repository. Supply only the reviewed design summary and application artifacts to a later application session; keep this implementation plan and its maintenance evidence in authoring context.

The first content work should migrate Core, the application-relevant Router/fact presentation, and a minimal ordinary task's true prerequisites as one coherent reviewed application path. Other modules remain explicitly unqualified until their content is reviewed. Detailed sequencing is owned by the separate guide.

## Final Acceptance

- Acceptance status: `blocked`
- Final status: `Verifying`
- Deferred follow-ups: normative content migration and downstream effectiveness evaluation, owned by the separate guide and existing effectiveness effort.

## Source baseline

All repository sources below were inspected at `366c1d90a24bbfb50973f62b155a5f3396c0f107`. They support observations about existing behavior; the design above is proposed work.

| ID | Source |
| --- | --- |
| S1 | `tools/standards_engine/standards_engine/agent_navigation.py` — focused navigation and compact reads. |
| S2 | `tools/standards_engine/standards_engine/engine.py` — `_read_value`, `_related_value`, `_relationships_from_targets`, `_inspect_snapshot_child`, snapshot compilation/capture. |
| S3 | `tools/standards_engine/standards_engine/mcp.py`, `tools.py` — catalogs, schema presentation, dispatch, local authorization. |
| S4 | `.agents/skills/standards-engine/scripts/invoke.py` — reference CLI invocation, list, schema, and examples. |
| S5 | `tools/standards_engine/standards_engine/logical_authoring.py` — `ChangePurpose`, logical edits, standard/routing/relationship changes. |
| S6 | `tools/standards_policy_impact/standards_policy_impact/model.py`; `contracts/policy-impact-authoring-v2.toml`; package README. |
| S7 | `tools/standards_metadata/README.md`; metadata schema; `tools/standards_engine/contracts/README.md` and canonical interface/schema files. |
| S8 | `tools/standards_verifier/README.md` — structural checkpoint and separate functional tests. |
| S9 | `.agents/skills/standards-engine/references/environment.md` — locked environment, real transport, and deployment assumptions. |
| S10 | Model Context Protocol maintainers, “Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do,” March 16, 2026 — annotations are hints, not enforcement. |
| S12 | `prompts/implement-plan.md` — current operational instructions requiring later positive rewriting and policy-aligned prompt maintenance. |
| S11 | `CORE-STANDARDS.md`, `STANDARDS-ROUTER.md`, `topics/architecture.md`, `templates/PLAN-TEMPLATE.md`, `workflows/{planning,implementation,verification,development-proportionality,tooling}.md`, `profiles/boundaries/persistence.md`. |

Repository source form: `https://github.com/MrScripty/Coding-Standards/blob/366c1d90a24bbfb50973f62b155a5f3396c0f107/<path>`.
S10: `https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/`.
