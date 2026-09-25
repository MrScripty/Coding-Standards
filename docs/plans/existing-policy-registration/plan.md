# Existing-Standard Policy Registration

**Plan status:** `Verifying`
**Acceptance status:** `blocked`
**Current phase:** Full-checkout and real-MCP qualification of the implemented source.
**Next slice:** Run the canonical compiler, replay and MCP publication regressions in a full supported checkout; repair any findings before content migration.
**Repository baseline:** `MrScripty/Coding-Standards@5a9dcb08effda50a485e6ae08d9fe4c349c74eda`.
**Admission:** The owner requested this plan and its implementation. Canonical plan path: `docs/plans/existing-policy-registration/plan.md`; operation: `start`.
**Composed-design review:** applicable; see below.
**Execution ledger:** [execution-ledger.md](execution-ledger.md). **Issues:** [issues.md](issues.md). **Evidence:** [reports/verification.md](reports/verification.md). **ADRs:** none required; this extends the existing authoring owner.

## Objective

An author can give a selected scope in an existing standard a stable policy identity through the Standards Engine, then maintain its consumer relationships and provenance through the existing reviewed publication workflow. Registration preserves the existing standard's prose unless an explicit same-candidate content edit changes it.

This is an Engine code correction. The real standards migration remains separately owned by `docs/guides/positive-guidance-and-provenance.md`. Real standards, policy declarations, relationships, exposure approvals and the installed proposal store remain unchanged by this task. In particular, preserve proposal `503f233b-5c9f-442f-a04f-99f330142bae` and its review evidence; that store is not present in this environment.

## Scope And Constraints

Apply Core and Router; Implementation, Planning, Verification, Development Proportionality, Build, Documentation and Commit; Library, Generated Contract, IPC and Persistence; Contracts and its schema/evolution detail, Architecture/replay, Security, Diagnostics and verification-oracle guidance where affected. The prospective guide supplies the owner's agreed practices: generic mechanisms, affirmative instructions, separate supplementary examples/provenance, coherent slices, bounded repair and evidence proportional to risk.

The new edit is generic and uses canonical identities and authored scope/intent. No Core-specific inference, automatic heading registration, raw path-editing API, second graph, alternate authoring lifecycle or new database is introduced.

No backward-compatibility layer is required. Extend the current contract coherently and retire nothing that remains the correct implementation. Existing proposal representations and storage need no forced replacement: adding a supported edit kind changes the interface, not the meaning of prior edits. Increment the interface version, regenerate its projections and refresh the actual client after installation. Preserve existing stores and historical evidence.

## Baseline and bounded findings

The existing `create-standard` can introduce initial policy units, `revise-standard.scope_updates` addresses the registered set, and `revise-policy-unit`/`put-policy-relationship` require registered identities. The parser and projection lack registration on an existing standard. The affected source was recovered from prior delivery archives and checked against published Git blob identities. Direct Git download is unavailable in this environment; the recovered tree is partial. Full-repository and installed-MCP acceptance are distinct from checks that can run against the available files.

## Binding Decisions

1. **Logical authoring owns the edit.** Add `register-policy-unit` with `standard` (canonical existing module ID) and `policy_unit` (the existing `NewPolicyUnit` declaration: ID, heading chain, revision one, explicit intent, aliases and lineage). Reuse closed field validation and normalized immutable `StructuredEdit` payloads. Its facet is the policy identity, so contradictory same-set policy edits fail before projection.
2. **Projection owns ordering.** Apply module and existing-policy content changes first, then stage all registrations in the change set as one group before relationship compilation, supporting-content binding and final validation. Grouping lets the existing corpus validator see all newly declared identities and scopes without loading a half-registered corpus; existing lineage constraints remain authoritative. Input edit order does not determine semantics.
3. **Metadata remains authoritative.** Resolve existing canonical module ownership, reject reserved identities, append declarations through existing sidecar/registry writers, and let the canonical metadata loader validate headings, aliases, lineage and scope. Reuse a registered owner sidecar even after its last active policy was retired, retaining its tombstones. No standard body is rewritten by registration.
4. **Analysis sees additions.** Produce revision-one semantic intent against an absent accepted identity and include the containing module in analysis. Registration establishes identity, not evidence of exhaustive consumer discovery or automatic coverage certification.
5. **Existing publication remains authoritative.** Relationships and provenance target the final candidate. Proposal validation remains private and atomic; restart/replay uses stored logical edits. Full replay and eligible incremental successors produce equivalent material and intents. The original accepted base retains authority.
6. **Generated interface remains single-source.** Add the new variant to the canonical JSON Schema and interface edition; run the existing projection compiler for Python and tool schemas. Reuse `propose`/`revise`; no new MCP tool or dispatch service is needed. Application-purpose authorization remains unchanged.

## Simplicity And Ownership Review

**Applicability:** `applicable`

**Independent concepts and dimensions:** logical authoring owns intent and staging; canonical metadata owns identities/scopes; impact and coverage own review obligations; snapshots/publication own durability; generated contracts own public representation. Registration introduces no new lifetime or authority.

**State, identity, value, time, policy and mechanism:** a new policy ID binds a selected current candidate scope at semantic revision one. Registration time is not the date the rule's meaning originated. The declared intent is preserved for review. IDs, body bytes, semantic revisions, evidence and coverage are separate.

**Caller and composition-root knowledge:** authors provide module ID, selected heading chain and intent, rather than sidecar paths, digests or generated files. Existing Engine composition consumes the resulting projection without new dependencies.

**Representative change paths and forced owners:** one registration changes its declaration and analysis intent; a same-candidate rewrite is a separate explicit edit; a relationship remains an explicit declaration; a later prose change uses the existing policy revision mechanism.

**Stable Interfaces versus hidden knowledge:** keep the existing `NewPolicyUnit` contract and metadata validator. The projection owns batching and file placement. The graph compiler receives the same canonical declarations as before.

**Independent evolution, testing, failure, and replacement:** current metadata and graph contracts remain unchanged. An invalid candidate publishes no partial registration. Application reading and authoring permission do not broaden. No authority is inferred from cached projections.

**Deletion and cumulative machinery result:** a new registration service, dynamic filesystem editor or graph-inference layer can be omitted entirely. The batch staging is required to keep final-candidate identity/scope validation independent of input order. A shared sidecar helper avoids duplicated registration representation.

**Necessary complexity and containment:** one edit variant, one bounded projection phase, existing analysis selection, generated projections and regression tests. Existing storage, generic graph, purpose filtering and review lifecycle remain untouched. File counts and commit counts do not drive decomposition.

## Milestones

### M1 — Implement the complete authoring transition

**Status:** `Implemented`. **Goal:** registration is expressible and composes correctly through the current owner and contract.

Allowed production files:
- `tools/standards_engine/standards_engine/logical_authoring.py`
- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/standards_engine/_generated_contract.py` (generator output)
- `tools/standards_engine/contracts/generated/agent-tools.json` (generator output)

Allowed verification and technical handoff files:
- `tools/standards_engine/tests/test_policy_registration.py`
- `tools/standards_engine/tests/test_registration_contract.py`
- `tools/standards_engine/contracts/examples/a1-examples.json` (authored contract fixture)
- `tools/standards_engine/tests/mcp_policy_registration_client.py`
- `tools/standards_engine/tests/codex_navigation_client.py` only if its declared edit catalog needs updating
- `.agents/skills/standards-engine/references/authoring.md`
- `tools/standards_engine/PURPOSE-SEPARATION.md`
- `docs/guides/positive-guidance-and-provenance.md` (H0 capability clarification only)
- this plan directory and its evidence
- the canonical suite-input manifest only through its owning generator when a full checkout is available

Preserve prior operations, existing policy identities/tombstones, prose, review obligations, current-only runtime and durable stores. Prove decoder agreement, both existing-module cases, same-candidate rewrite/relationships/provenance, rejection/atomicity and replay. Repair failures within this decision boundary. Replan for a different ownership model, broader identity semantics, a persisted-format change or evidence that the selected operation cannot express the blocker.

### M2 — Qualify and hand off

**Status:** `Blocked`. **Goal:** prove source and consumer behavior at their actual boundaries and provide a safe patch package.

Write set: M1 corrective changes, evidence/plan lifecycle, package manifest and delivery instructions outside the repository. Run available focused checks; run full-checkout logical/contract/package suites and real MCP publication when dependencies are present. Bind each result to the actual source and environment. Report missing environmental evidence explicitly rather than treating an isolated test as installed acceptance. Provide complete changed files and a base-bound patch, hashes, plan, tests and installation/resume instructions. No push, production publication, live proposal mutation or store reset is part of delivery.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Current schema and generated models admit the new edit and reject malformed declarations; projections are current. | contract | not-applicable | automated | satisfied | [Contract evidence](reports/verification.md) |
| R2 | Existing standards with zero or other units retain prose, identities and tombstones after registration. | integration | representative | automated | blocked | Canonical metadata/compiler run requires a full checkout; isolated owner probes are supporting only. |
| R3 | Same-candidate rewrite, registrations, relationships and provenance resolve correctly independent of edit ordering. | integration | representative | automated | blocked | Complete authority compiler is unavailable locally. |
| R4 | Invalid candidates preserve accepted and predecessor state; full replay and incremental construction agree. | integration | representative | automated | blocked | Full compiler/replay regressions are supplied but unexecuted. |
| R5 | Real MCP discovers, authors, resolves, reviews, publishes, restarts and reads the registration in an isolated repository. | system | required-real | automated | blocked | Full checkout, supported locked interpreter and actual client processes are required. |
| R6 | ZIP patch reproduces the intended changed-file tree and excludes real normative content and the external proposal store. | release-artifact | not-applicable | automated | satisfied | [Package round-trip evidence](reports/verification.md) |

For R2–R4 use the canonical metadata, graph, analysis and logical compiler in a supported Python 3.11/3.12 environment. R5 additionally uses the existing official MCP SDK qualification environment, actual local subprocesses, Git and SQLite. The available Python 3.13 observations do not qualify that installed environment.

## Blockers

A complete Git checkout and supported locked runtime are unavailable here. Direct source download is unavailable and the recovered source omits modules needed by Engine startup. This blocks R2–R5; it does not turn the passed contract/isolated checks into acceptance. The installed user store and proposal are outside this environment.

## Re-Plan Triggers

A required operation or invariant that cannot be expressed with these owners triggers a design update. Local test failures trigger repair while the contract remains valid. New unrelated code quality findings are recorded with owner and revisit trigger rather than expanding scope.

## Evidence And Oracle Plan

Add the regression before production changes and show that the baseline rejects the new edit. Derive focused expectations from the intended behavior, not copied generated outputs. Validate runtime and schema separately. Use a full-checkout MCP client to exercise actual publication, with explicit fixture decisions confined to disposable test repositories.

The plan is `Accepted` only when all required claims have matching evidence. Source implementation can be delivered as `Implemented`/`Verifying` with environment-gated evidence explicitly outstanding. Resume the preserved content proposal only after installing the candidate, refreshing the MCP contract and satisfying H0. Earlier Core text/review evidence remains historical evidence; the revised candidate receives the affected current review rather than inheriting old readiness.

## Systemic Finding Audit

The bounded invariant family is explicit policy identity authoring through the public logical-edit contract. Inspect the parser, registration representation, projection ordering, semantic/coverage inputs, generated schemas, proposal consumers and actual MCP path. The missing operation spans these projections of one owner; it is not evidence that all standards or graph mechanisms need redesign.

The new edit reuses the existing declaration/metadata authority and the existing authoring lifecycle. Sibling creation, revision and retirement operations establish preserved contracts; only the shared tombstone-sidecar reuse case needed a corrective change. Generated outputs come from the existing compiler. Code inspection and isolated observations support the composition, while full consumer acceptance remains blocked. Stop expansion when these named consumers are qualified or a specific new consequence changes scope.

## Version And Material Boundaries

The interface edition advances from 32 to 33 because the public edit vocabulary expands. Analysis request 6, result/state 7, Snapshot, proposal and SQLite formats remain unchanged: their meanings were not replaced. A server restart is required to obtain its newly installed catalog. There is one current decoder, with no compatibility branch, dual write or automatic store migration.

Canonical policy identity/scope belongs to metadata; edit intent and atomic staging belong to logical authoring; generation transports the schema. Adding a registration changes its declaration, module mapping and review inputs. It does not automatically approve coverage, rewrite a provenance history or revive retired identities. Existing proposal text and review evidence remain available subject to ordinary stale-state rules; old readiness does not authorize changed material.

## Repository Isolation

All work occurs in a disposable partial reconstruction under `/mnt/data/policy-registration-work`. It is not the user's checkout or installed MCP store. ZIP integration is owned by the user's repository integrator. No upstream branch, remote, live proposal, shared history or user workspace is modified. Temporary repositories used to prove patch application contain only package-selected fixture files and confer no upstream commit identity.

## Final Acceptance

- Acceptance status: `blocked`.
- Source status: `Implemented`; the new contract, projection, tests and technical handoff are supplied.
- Deferred independent feature work: `none`.
- Required outstanding work: canonical full-checkout/replay tests, generated suite-input refresh, structural checks and actual MCP publication qualification.
- Final plan status: `Verifying`. Accept after R1–R6 are satisfied; the content guide's H0 remains closed until then.
