# Proposal-Scoped Consumer Registration And Application Preview

**Plan status:** `Verifying`
**Acceptance status:** local code evidence recorded; supported installation and user-proposal qualification pending
**Current phase:** Source implementation and local verification complete; installed qualification and handoff remain.
**Next slice:** Qualify interface 34 in the supported installed environment and resume the preserved proposal through the returned Engine workflow.
**Canonical plan:** `docs/plans/proposal-consumers-and-preview/plan.md`; operation: `verify`.
**Source baseline:** `9091bc72ac146b47d613b1836fbd8a89bd46f9ba`.
**Composed-design review:** `applicable`; admission below.
**Execution ledger:** [execution-ledger.md](execution-ledger.md).
**Issues:** [issues.md](issues.md).
**Reports:** [verification](reports/verification.md).

## Objective And Scope

Allow one immutable proposal to register existing repository consumers, connect them to policy units created in that proposal, revise registered Markdown guidance, and preview its proposed application view before publication. Keep the existing graph, proposal, review, application, recovery and snapshot owners.

The reported draft `503f233b-5c9f-442f-a04f-99f330142bae`, reviewed candidate prefix `ece4619f`, is outside this environment. This work preserves it by changing neither the user's store nor accepted standards. Real consumer names are evidence and integration cases, not special branches in production code.

## Authority And Selected Standards

Apply Core, Router, Implementation, Verification, Planning, Development Proportionality, Library, Generated Contract, IPC, Persistence, Contracts, Security, Code Design, and immutable-replay guidance to their affected concerns. Apply the agreed positive-guidance guide prospectively: generic requirements, explicit ownership, correct operational direction, substantive evidence, bounded repair and separate editorial work.

The user permits replacing inferior older contracts. Select one interface edition and regenerate its actual consumers. Preserve existing draft records and historical evidence; permission to improve an API is distinct from authority to erase stores. No broad standards rewrite is part of this slice.

## Verified Gap And Deciding Facts

The current `maintain_evidence` operation works on an exact repository revision and its working tree, not a proposal. Its consumer registration relies on an already-declared policy relationship owner. The three reported files are tracked at the original revision but are not in the ordinary captured authority closure. Registering metadata alone would cause a later missing-input failure.

`query_proposal` belongs to the authoring interface. Ordinary application sessions correctly lack it. A safe candidate preview must therefore be an explicit authoring operation using the application renderer, with proposal identity rather than a fabricated published snapshot.

## Binding Design

### Consumer admission and immutable source

Add `register-consumer` to the logical edit algebra, with an explicit canonical consumer ID, repository-relative path, admitted artifact kind, and authority (`evidence` or `projection`). Support fixture, documentation, implementation-artifact, prompt and template consumers. A registration selects an existing regular file from the proposal's original repository revision. Canonical source and consumer ownership remain distinct; duplicate IDs, aliases, paths and canonical-module reclassification reject.

Before recording a new revision, Engine preparation reads the selected file through the existing verified Git reader against the base snapshot's exact source revision. It retains those exact bytes in the new logical edit's private source binding. Public request schemas accept the selection, not caller-supplied captured bytes. Existing proposal identity/storage then owns the complete input closure; cold replay needs no current checkout read or new side database.

The pure compiler validates the binding, imports original consumer material, then stages registrations before consumer relationships. Full and incremental construction use the same complete-program source identity. A registration may target a policy created in the same change set. Registration establishes existence, not coverage completeness or approval.

Allow explicit canonical IDs to select registered consumers in the candidate, including newly registered IDs; returned snapshot-bound targets remain a useful exact selection form. A bare unregistered path does not gain write authority.

Publication compares the candidate to original captured material augmented only by the Engine-bound consumer inputs. Registration alone leaves fixture/source bytes unchanged. An explicitly requested Markdown documentation edit uses the existing registered-guidance operation. Documentation, prompts and templates require `.md` paths; fixtures and implementation artifacts remain read-only through this content editor. Hidden repository paths such as `.agents/...` are eligible under the same tracked-file and canonical-path rules.

### Application preview

Add authoring-only `preview_application(revision, request)` for read, route and related requests. It reconstructs the exact proposal and uses the same eligibility, dependency closure, permitted graph and output-content construction as published application reading.

Preview results carry the exact proposal revision and an explicit candidate result kind. They return no published snapshot handles and their continuations remain preview operations. The ordinary application catalog stays unchanged. Unreviewed/stale required material returns the normal bounded application-unavailable observation; preview supplies neither approvals nor readiness and publishes nothing.

Keep compact read as the default and select one target/request per preview. Existing workflow-response truncation and automatic client catalog reload are separate findings; this slice documents exact process refresh and avoids claiming those mechanisms are implemented.

### Current contract and storage

Advance interface 33 to 34 for the new edit/preview API and regenerate models/tool schemas from the owning schema. New bound consumer data is a new logical-edit representation inside the existing content-addressed revision aggregate. Existing snapshot/store formats and unrelated handle versions retain their meaning. Old clients need the current catalog; no compatibility adapter, implicit downgrade or store reset is introduced.

## Exact Write Set

- `tools/standards_engine/standards_engine/consumer_authoring.py` (new): selected consumer representation, private captured binding and catalog projection.
- `logical_authoring.py`: edit admission, deterministic ordering, import closure, canonical consumer selection and projection baseline material.
- `engine.py`: source preparation, preview entrypoint, and publication baseline comparison.
- `context_projection.py`: shared application view with honest snapshot/candidate output identity.
- `supporting.py`, `supporting_authoring.py`: registered Markdown documentation read/revise/review ownership.
- `tools.py`, `mcp.py`: generated-call dispatch, focused authoring catalog and descriptions.
- Engine public schema, interface, generated contract/tool definitions, and affected examples/tests.
- Engine tests: registration, replay, source binding, previews, exposure denial and actual-process publication.
- Engine implementation/authoring technical documentation, H0 operation map, this plan directory.
- `evaluation/standards-effectiveness/generated/suite-inputs.json`, through its existing generator only.

An additional changed file requires a concrete consumer obligation, not an unrelated cleanup. The real policy units, consumer registrations, normative prose and application manifests stay unchanged.

## Composed-Design Admission

1. **Independent concerns:** Git owns verified file reads; Engine preparation binds selected inputs; logical authoring owns immutable edits; metadata/graph own compiled meaning; application view owns disclosure; existing publication owns atomic state changes.
2. **Identity and state:** original snapshot and revision identify the imported file authority; exact retained bytes complete replay; a registration ID is neither coverage nor approval; preview is not publication.
3. **Caller knowledge:** callers name consumer identity/type/path and relationships. They do not choose sidecars, serialize source bytes, calculate digests, mutate stores or construct application snapshots.
4. **Representative change paths:** one fixture registration adds metadata plus a captured input; one documentation update changes its owned Markdown; a preview uses the existing renderer and a different authority envelope. Independent policy semantics stay with current owners.
5. **Interfaces:** the public schema exposes authored intent; only trusted preparation adds captured material. Canonical IDs are resolved against final candidate declarations. Purpose remains host-selected.
6. **Evolution/failure:** invalid registration leaves the prior draft intact; replay uses retained inputs after process replacement; preview failure cannot publish or weaken a required dependency.
7. **Deletion results:** removing captured bytes would make replay depend on live files; duplicating the application renderer would permit drift. Reuse the existing store and renderer. A new graph, publication workflow, metadata service, ambient source fallback and policy-specific exceptions add no deciding value and are omitted.
8. **Cumulative cost:** bound only explicitly selected files; add one edit and one focused read operation; preserve normal route/read behavior. Carry exact source bytes once per registration in the existing aggregate rather than capturing every repository file.

## Milestones

### M0 — Confirm the defect and recover complete source

**Status:** `Accepted` for source qualification, not implementation acceptance. The exact CI source artifact was downloaded and its SHA-256 matched `3bec00071ddef6113c4b91d6185662afb6f57fc2bd9bfdc38c33c351178a458e`. The Git bundle resolves to the stated baseline. No user checkout/store was used.

### M1 — Coherent implementation and focused evidence

**Status:** `Accepted` for the local code evidence in the verification report. Use the write set above. Add failing cases for registration of uncaptured tracked consumers and preview unavailability. Implement input binding, same-candidate compilation, documentation support, application preview and schema projection together. Gate on full real-compiler and contract tests, including rejection without mutation and full/incremental equality.

### M2 — Public workflow qualification and handoff

**Status:** `Verifying`; local public workflow, package and checkpoint observations passed as recorded, while supported-environment and user-store observations remain external. Verify the exact new catalog and public workflow in disposable Git/SQLite stores: register policy and three consumers, add relationships/provenance, read authoring documentation, preview qualified candidate, review/apply, then compare published application content. Exercise cold replay without rereading source files. Run affected package suites, structural checkpoint and generated freshness; record interpreter/dependency scope precisely.

Package complete changed files, patch, checksums and installation guidance. The user's actual reviewed draft remains a separate installed acceptance observation. No success claim about it is inferred from test fixtures.

## Acceptance

| Claim | Kind | Environment | Mode | Status |
| --- | --- | --- | --- | --- |
| C1: Same-proposal consumer registration resolves newly registered policy scopes and preserves original files. | integration | complete repository | automated | passed locally |
| C2: Captured input, identity, scope and publication topology remain coherent through cold and incremental replay. | integration | real Git/SQLite | automated | passed locally |
| C3: Registered Markdown documentation under normal or hidden directories is editable without exposing source-code writes. | integration | deterministic actual metadata/compiler | automated | passed locally |
| C4: Candidate previews use application checks and exact revision identity; ordinary application clients remain excluded from drafts. | contract/system | actual local MCP process | automated | passed locally |
| C5: A coordinated disposable proposal passes analysis/review/verification/application and readback. | user-workflow | complete local Git/SQLite/transport | automated | passed locally |
| C6: Generated contracts, affected tests, structural checks and package reproduction pass with environment limits recorded. | contract/release-artifact | recorded local environment | automated | passed locally |
| C7: The installed current Engine resumes the user's preserved proposal and clears the reported gap. | user-workflow | user's installation and store | manual | pending: external |

## Repair, Blockers And Replan Triggers

Repair test failures inside the admitted owners without restarting planning. Replan only if a required change alters input authority, retained-state meaning, application disclosure, code-write scope or atomic publication. A test that does not reach the changed behavior supplies no evidence for that behavior.

The local interpreter is Python 3.13.5 with rpds-py 2026.5.1, outside the repository's pinned Python 3.11/3.12 and rpds-py 2026.6.3 qualification. Keep execution evidence useful but distinguish it from pinned deployment acceptance. The actual user store and independent model reviewer are unavailable here.

## Handoff

Refresh the complete installed server process and reconnect the client; verify interface 34, the `register-consumer` edit and authoring `preview_application` tool. Continue the existing proposal through supported status/resume/revise operations. Refresh only affected review/coverage obligations and current readiness; historical review evidence remains preserved. Publication still requires explicit owner authorization.
