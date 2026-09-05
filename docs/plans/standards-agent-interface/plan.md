# Plan: A Simpler Agent Interface For The Standards Engine

**Plan status:** `Active`

**Current phase:** Milestone 2 — discoverable facts and explainable routing

**Next slice:** Expose snapshot-bound routing facts and typed deterministic routing explanations.

**Acceptance status:** `partial`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Let an engineering agent retrieve applicable authoritative standards and advance
standards proposals with less protocol knowledge and handle bookkeeping. The
Engine continues to decide applicability, validate evidence and state, bind
review to exact content, and own repository mutation. The calling agent supplies
explicit engineering facts and semantic intent.

The existing MCP transport removes shell invocation and manual schema discovery.
This plan improves the Interface that transport exposes. The user has authorized implementation and milestone commits. The existing
MCP work is included as the Milestone 1 prerequisite; it is not evidence that
the focused improvements are already delivered.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Given known explicit facts, one `route` call without a snapshot captures authority and returns the same selections, required closure, and unresolved conditions as explicit snapshot plus native routing. | `integration` | isolated repository | `automated` | `satisfied` | [Milestone 1 evidence](reports/milestone-1.md) |
| A2 | Default `read` returns exact policy content and essential authority metadata without the full relationship projection; full detail remains retrievable against the same snapshot. | `integration` | isolated repository | `automated` | `satisfied` | [Milestone 1 evidence](reports/milestone-1.md) |
| A3 | An agent can discover the registered fact vocabulary and distinguish base selection, matched rules, required dependencies, and unresolved applicability from structured results. | `integration` | isolated repository | `automated` | `pending` | Milestone 2 |
| A4 | One returned workflow context carries the identities needed for subsequent authoring steps and survives process replacement without silently switching proposal revisions. | `integration` | isolated durable repository, separate processes | `automated` | `pending` | Milestone 3 |
| A5 | Stale, mismatched, forged, or cross-repository contexts and illegal transitions cannot publish or reinterpret accepted content; current authorization remains independently required. | `integration` | isolated durable repository | `automated` | `pending` | Milestone 3 |
| A6 | Mechanical progression stops at missing facts, evidence, semantic decisions, authorization, rejection, or recovery; application uses the exact accepted readiness and is never automatically retried. | `integration` | isolated repository with controlled failure injection | `automated` | `pending` | Milestone 3 |
| A7 | A real MCP client can perform lookup and the authoring/recovery scenarios with native tools and the revised skill, without shell schema discovery or caller-managed private state. | `user-visible` | configured MCP client and isolated repository | `manual` | `pending` | Recorded client walkthrough |
| A8 | Generated contracts, focused regressions, skill validation, and the complete repository checkpoint pass; declared supported Python and reference-transport consumers remain usable. | `integration` | repository-supported Python environments | `automated` | `pending` | Final verification report |

## Scope

In scope: focused navigation tools; optional snapshot creation; compact reading;
registered fact discovery; deterministic routing explanations; bound workflow
contexts; Engine-owned continuations; bounded mechanical composition; generated
contracts, MCP exposure, skill updates, and realistic acceptance evidence.

Out of scope: embeddings, semantic search, an interpreter model, free-text
applicability decisions inside the Engine, new routing ontologies or policy
meaning, fabricated evidence or review decisions, remote publication, a general
workflow framework, and unrelated MCP protocol or client-installation redesign.

## Constraints And Assumptions

- Preserve explicit facts, immutable authority, exact revision/readiness binding,
  stale-state rejection, and Engine ownership of Markdown, SQLite, and Git.
- The current MCP server, tests, and skill edits exist in the working tree.
  Establish their usable baseline before changing them; preserve unrelated work.
- This effort is separate from the existing Standards Library Effectiveness
  plan. Its lifecycle and acceptance do not close or replace that objective.
- Work integrates serially through the shared contract and Engine owners. No
  branch, worktree, parallel agents, or commit topology is required by this plan.
- Admission: `start docs/plans/standards-agent-interface/plan.md`, authorized
  by the user’s instruction to proceed with implementation and milestone commits.
- Runtime persistence or identity changes are allowed only if required by the
  exact context and cold-process acceptance promises below. Prefer reconstructing
  aggregates from existing durable records over adding a new state store.

## Binding Decisions And Ownership

| Decision | Owner | Basis |
| --- | --- | --- |
| Engineering facts, policy meaning, dispositions, review acceptances, and actual evidence remain explicit inputs. | Calling agent and authorized human/evidence owners | User-approved deterministic scope |
| Applicability, routing causes, required closure, immutable identities, and transition admissibility remain authoritative domain behavior. | Engine and existing domain Modules | Existing `_route_value`, proposal, analysis, and application implementations |
| Tool names, argument convenience, deliberate operation composition, and presentation live in the agent-facing facade. | Engine agent facade | One implementation pays the bookkeeping cost for all MCP callers |
| Public request/result shapes have one canonical schema and generated projections. New facade shapes do not become handwritten MCP schemas. | Existing contract schema/interface and compiler | `contracts/README.md` authority rules |
| The MCP server transports calls and results. It owns no proposal head, policy inference, workflow state machine, or authoritative context map. | MCP Adapter | Existing serial, per-call durable facade lifecycle |
| Omitted snapshot means create a new snapshot for that call; supplied snapshot means use exactly that authority. Return the effective snapshot in either case. | Facade composition with Engine validation | Convenience without ambient shared state |
| Compact reads preserve exact text and all fields needed to interpret authority, scope, prerequisites, specialization, and incompleteness. | Engine projection; facade presentation selection | Smaller results must not change policy meaning |
| Workflow context is an immutable, Engine-validated aggregate/reference to existing exact identities. It is not a mutable session or an authorization grant. | Engine identity and lifecycle owners | Reconnection and concurrency guarantees |
| Continuations are projected from Engine state and revalidated on execution. Their presence indicates a candidate next operation, not guaranteed authorization or success. | Engine | Prevent a second state machine in the skill/facade |
| Review, application, and recovery remain explicit actions. Only mechanical work within the requested action is composed automatically. | Facade delegates to Engine | No implicit semantic acceptance or apply retries |
| Retain the native Python/reference CLI for advanced and administrative operations. Promote the focused tools in the skill; add no automatic fallback between old and new semantics. | Facade, MCP catalog, and skill owners | Existing consumers and debugging remain supported |

## Intended Agent Experience

These are operation responsibilities, not final JSON field definitions. Each
milestone makes the exact shapes executable in the canonical contract.

- `route(facts, snapshot?)`: use explicit registered facts; return the effective
  snapshot, selected standards, required closure, deterministic causes, and
  unresolved questions. No missing category becomes a negative answer.
- `read(target, snapshot?, detail?)`: default to exact policy and essential
  authority metadata. An explicit full-detail request retains the existing
  complete projection. Never truncate normative text silently.
- `related(target, relationship selection, snapshot?)`: traverse the existing
  permitted graph relationships. Preserve bound authoring-target handles.
- `routing_facts(snapshot?)`: expose registered IDs, types, allowed values,
  nullability, meanings, and prompts without requiring the full Router document
  or editable routing rules.
- Authoring operations accept and return one bound context for ordinary use.
  Historical revision reads and advanced inspection remain explicit. Final
  operation names are selected in Milestone 3 from the existing lifecycle,
  rather than targeting an arbitrary total tool count.

A task starts with known facts or vocabulary discovery, routes, then reads the
selected policies using the returned snapshot. A changed task supplies revised
facts; a request for current accepted standards explicitly creates new snapshot
state. Neither action silently changes existing proposal or reading authority.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- **Independent concepts and dimensions:** engineering facts, policy authority,
  snapshot identity, proposal revision, analysis obligations, review readiness,
  and application outcome remain distinct. Convenience groups their references;
  it does not collapse their meanings.
- **State, identity, value, time, policy, and mechanism:** existing domain records
  own state; facts and authored changes are values; snapshots and exact revisions
  pin time; Engine policy decides validity; the facade composes mechanisms.
  - **Canonical authority scope and referenced authorities:** accepted snapshot,
    proposal revision, analysis, readiness, and application are linked through
    Engine validation. MCP connection identity carries no standards authority.
  - **Version roles and owned promises:** distinguish public shape versions,
    handle identity versions, and policy semantic revisions. Change only the
    owners affected by an actual compatibility or identity change.
  - **Supported compatibility overlaps and consumer matrix:** native Python,
    reference CLI, MCP catalog, generated examples, and skill are the bounded
    consumers. Preserve current native calls; migrate normal skill workflows
    to the focused tools. Avoid exposing duplicate default navigation tools
    without a documented advanced-use reason.
  - **Material identity-invalidation effects:** new proposal content invalidates
    applicability of old current-head actions; historical reads remain historical.
    Readiness remains bound to exact reviewed content. Reconnection invalidates
    no durable identity and cannot manufacture a newer one.
- **Caller and composition-root knowledge:** callers know engineering facts,
  canonical policy IDs when selecting text, and requested decisions. The facade
  owns default capture and plumbing; Engine owns authority and validation.
- **Representative change paths and forced owners:** a routing-rule change flows
  through the existing Router and projection; a result-shape change flows through
  the contract compiler; a transition-rule change belongs in Engine lifecycle
  logic, not in MCP descriptions or skill branches.
- **Stable Interfaces versus hidden knowledge:** typed results expose required
  decisions and exact outcomes. Paths, record layouts, private locators, revision
  selection algorithms, and publication mechanics remain private.
- **Independent evolution, testing, failure, and replacement:** exercise the same
  facade from Python and MCP. Replace the transport without replacing state;
  test process replacement separately from in-process agreement.
- **Necessary complexity and containment:** authoring identity and recovery remain
  strict; reading becomes cheaper. One Engine-derived continuation model serves
  the facade and skill instead of adding parallel workflow logic.
- **Deletion and cumulative machinery result:** delete routine CLI instructions,
  duplicate navigation exposure, and caller scratch extraction when superseded.
  Reuse current routing causes and fact projections. Reject a new mutable workflow
  database, generic orchestration language, or parallel routing authority unless
  new evidence changes this plan.

## Evidence And Oracle Plan

| Claim | Deciding oracle | Independent authority / limitation | Intended negative evidence |
| --- | --- | --- | --- |
| Routing is unchanged | Fixed registered-fact fixtures with reviewed expected selections and causal paths, plus comparison with native routing on the same snapshot | Native agreement detects projection drift; fixture expectations establish correctness independently of the wrapper | Unknown/invalid facts rejected; omitted facts remain unresolved; closure entry traceable to an actual requires edge |
| Compact policy is faithful | Compare exact content and essential metadata with accepted snapshot content and full native reads | Byte comparison proves fidelity, not whether the policy is well written | Long normative content is never silently cut; omitted detail is retrievable against the original snapshot |
| Contexts preserve authority | Real durable Engine operations across separate processes and concurrent revision changes | Mocks alone cannot prove persistence, stale-state rejection, or publication | Swapped analysis/revision, old head, foreign repository, unsupported version, and altered context fail before publication |
| Composition preserves lifecycle | Explicit-call baseline and composed-call scenarios over reviewed fixture outcomes | Failure injection verifies publication and recovery invariants, not only method call order | No decision inferred, no mutation retry, no re-verification/publication inside observational recovery |
| Agent experience improves | Same fixed tasks through old/native and focused MCP paths; record calls, caller-carried handles, catalog size, result bytes, and actual client walkthrough | Smaller bytes or passing unit tests alone do not establish usable agent behavior | No shell discovery, private storage access, or unreported authority loss needed to complete the tasks |

Record evidence in this plan directory as it is produced; do not create reports
claiming future acceptance. A missing relevant fixture or client environment is
reported explicitly rather than replaced by a weaker proof.

## Milestones

### Milestone 1: Focused Snapshot-Bound Navigation

**Goal:** Make ordinary routing and policy reading cheap through native tools.

**Allowed write set:**

- `tools/standards_engine/contracts/{a1-contract.schema.json,a1-interface.toml,examples/a1-examples.json,README.md}`
- `tools/standards_engine/standards_engine/{engine.py,tools.py,mcp.py,__init__.py}`
- A focused facade/projection module under `tools/standards_engine/standards_engine/` if required to keep transport and domain logic separate.
- Generated `tools/standards_engine/standards_engine/_generated_contract.py` and `tools/standards_engine/contracts/generated/agent-tools.json`, through their compiler.
- `tools/standards_engine/tests/{test_mcp.py,test_navigation.py,test_generated_contract.py}` and a focused agent-facade test file.
- `tools/standards_engine/README.md`, `.agents/skills/standards-engine/{SKILL.md,references/navigation.md,references/environment.md}`.
- This plan directory; verification-input projections refreshed only through the Engine.

**Tasks:**

- [x] Capture the current MCP/native baseline for a known-facts route, a policy
  read with substantial relationships, an unresolved route, and two interleaved
  tasks. Record complete output shape and observable interaction costs.
- [x] Add generated focused operations and result projections. Keep request
  validation in the existing contract path; include typed rejection variants.
- [x] Implement explicit supplied-snapshot versus omitted-snapshot semantics;
  preserve failure outcomes from capture without advancing to a query.
- [x] Add compact read selection without removing essential authority fields;
  provide full-detail retrieval and preserve related authoring-target identities.
- [x] Integrate MCP exposure and navigation skill changes in the same slice.
  Use conservative tool annotations when optional capture can write snapshot
  state; do not label the whole operation read-only solely because it reads policy.
- [x] Confirm an actual client can consume generated definitions and results.

**Acceptance gate:** A1 and A2; targeted negative tests; generated-contract
checks; initial real-client navigation evidence for A7. Known-facts routing
requires one agent tool invocation; full normative text and required closure
remain authoritative. Record result-size reduction on the relationship-heavy
fixture without adopting an arbitrary percentage target.

**Status:** `Accepted`

### Milestone 2: Discoverable Facts And Explainable Routing

**Goal:** Let the calling agent supply and audit explicit routing facts without
loading the Router's representation.

**Allowed write set:** Milestone 1 paths, plus focused routing fixtures under
`tools/standards_engine/tests/`. Changes to Router/applicability owner code or
fact semantics require an evidence-backed write-set revision before editing.

**Tasks:**

- [ ] Expose `routing_facts` from current snapshot-bound fact definitions.
  Separate consumer vocabulary discovery from authoring rule inspection.
- [ ] Project existing base, rule, and dependency causes in a compact structured
  form. Retain all applicable causes when several rules select one standard.
- [ ] Bind explanations to the supplied facts and same snapshot. Show registered
  rule meaning and graph causes; do not generate semantic prose or claim
  minimal causal proofs that the evaluator does not establish.
- [ ] Preserve unresolved applicability separately from selected standards and
  definite non-selection. Include answer shapes suitable for the actual fact
  type; check nullable and set-valued facts as well as enumerations.
- [ ] Cover complete, partial, conflicting/invalid, unknown, aliased, and explicit
  negative facts using the existing vocabulary's actual supported semantics.
- [ ] Update the navigation skill around discover → supply facts → route → read,
  allowing agents with known valid facts to start directly at route.

**Acceptance gate:** A3 and the routing portions of A7. Existing routing causes,
questions, and definitions remain the source of explanations; no second Router
or policy selection logic appears in the facade.

**Status:** `Planned`

### Milestone 3: Bound Authoring Contexts And Mechanical Continuations

**Goal:** Remove routine authoring handle plumbing while preserving exact state,
explicit decisions, and controlled application.

**Allowed write set:** Milestone 1 paths; the authoring skill reference;
`tools/standards_engine/standards_engine/{authoring.py,logical_authoring.py}`;
focused authoring, analysis, and recovery tests under `tools/standards_engine/tests/`.
Changes to analysis identity/store owners outside the Engine package require the
bounded owner-path revision described below before implementation.

**Tasks:**

- [ ] Specify the minimal context aggregate and its lifecycle from the existing
  snapshot, proposal, revision, analysis, readiness, and application records.
  Choose a generated value/reference representation that Engine can validate
  after restart; avoid new persistence if existing records suffice.
- [ ] Bound the exact identity/store owner paths if durable representation must
  change. Record the required compatibility and invalidation effects, then
  revise the write set before editing those owners.
- [ ] Validate association and repository scope for every context member. Return
  a new immutable context after progression; never mutate an old context to
  select a newer proposal head. Resume exposes current head explicitly.
- [ ] Project actionable continuations from Engine state with bound identities
  and schemas for the remaining caller inputs. Retain historical inspection;
  reject stale transition attempts even when a prior result offered them.
- [ ] Add focused context-consuming authoring operations. Compose only the
  deterministic steps authorized by each operation, stopping on the first
  pending decision, unavailable authority, rejection, or recovery result.
- [ ] Keep `review`, `apply`, and `recover` explicit and semantically distinct.
  Reuse existing verification within apply; do not introduce a second review
  lifecycle or repeat an apply after interruption. Coverage-audit sequencing
  remains governed by current Engine readiness requirements.
- [ ] Test process replacement, concurrent revisions, changed authorization,
  foreign/malformed contexts, interrupted application, and observational recovery.
- [ ] Cut over the authoring skill and complete the real-client walkthrough.
  Reduce default tool duplication with explicit dispositions for every existing
  native/administrative operation; preserve supported advanced access.

**Acceptance gate:** A4–A8, with fresh A1–A3 regression evidence after composition.
Record baseline-versus-final tool calls and caller-carried identities for an
ordinary proposal, a proposal requiring a decision, a stale revision, and
recovery. A successful happy path alone cannot accept this milestone.

**Status:** `Planned`

## Blockers

None for planning. MCP client registration is not established in this session;
real-client evidence is required before acceptance. See issue I2.

## Re-Plan Triggers

- A compact result omits information necessary to interpret authoritative policy.
- Existing routing projections cannot express the needed explanations or typed
  missing-fact answers without an owner-level contract change.
- A context needs new mutable state, a global current snapshot, implicit head
  selection, or a new identity/storage owner beyond the admitted composition.
- Existing low-level publication or recovery entrypoints can bypass a claimed
  Engine invariant; a facade-only guard would not satisfy that claim.
- Actual MCP clients cannot consume the generated schemas or the intended
  default catalog without a new compatibility contract.
- A caller needs semantic inference, a changed fact ontology, or new policy
  decisions for acceptance; do not silently add them to deterministic scope.
- A supported consumer, material write set, or acceptance environment changes.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: semantic search and interpreter models are excluded by
  user direction; reconsider only on an explicit future request.
- Final status: `Planned`
