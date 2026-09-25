# Engine Routing and Review Workflow

**Plan status:** `Verifying`
**Acceptance status:** `pending`
**Current phase:** M3 — source implementation and local qualification; installed migrated-host verification remains.
**Next slice:** Verify U7 on the actual migrated, supported locked host using the delivered code and current catalog.
**Canonical plan:** `docs/plans/engine-routing-review-ux/plan.md`; current operation: `verify`.
**Source baseline:** `c947f5456d37c9fffbaefdf0bb0d4004eee699cf`.
**Composed-design review:** `applicable`; section 6.
**Ledger:** [execution-ledger.md](execution-ledger.md). **Issues:** [issues.md](issues.md).
**Evidence:** [reports/verification.md](reports/verification.md).
**Durable contract:** `tools/standards_engine/PURPOSE-SEPARATION.md`; update that owner rather than create another ADR.

## 1. Objective and authority

Complete the remaining Engine work reported after the initial positive-guidance migration:

1. Router compilation, readable routing inspection, and logical routing edits work independently of historical display headings.
2. Authors submit several explicit review decisions in one request with bounded responses and retrievable complete detail.
3. Operators and clients can identify the actual running interface/catalog and detect an installation requiring a server restart.

Code work owns mechanisms, transport contracts, tests, and technical documentation. It leaves real standards, policy identities, consumer registrations, receipts, and proposal stores unchanged. Neither batching nor compact output supplies approval. Existing explicit review, preflight, apply, and recovery remain the publication authority.

The owner reports accepted local content commit `72963ad5`. GitHub could not resolve that local commit; the available complete checkout is the published implementation branch at the baseline above. Apply the accessible Core/Router and their selected dependencies together with the user's agreed positive-guidance practices and `docs/guides/positive-guidance-and-provenance.md`. Verify integration against the exact local accepted content separately; do not substitute older source for the user's migrated files or claim to have reviewed unseen wording.

### Standards selection

Applicable owners are Core, Router; Implementation, Planning, Verification, Development Proportionality, Documentation, Build, Commit; Library, Generated Contract, IPC, Persistence; Contracts and its Schema/Evolution/Protocol details; Architecture, Code Design, Replay; Security, Diagnostics, Performance, and Verification Oracles. Follow their `Requires` closure. Concurrency applies to publication/head changes and immutable review observations, not new worker scheduling. No UI, hardware, Rust implementation, remote service, model inference, or new dependency is needed.

Prospective practice: write affirmative operational guidance; separate generic semantics from fixtures; preserve exact authority and explicit authorization; prefer a coherent reversible implementation; repair within the admitted scope; judge evidence by the property it proves. This task is not a whole-library policy audit or effectiveness pilot.

## 2. Scope and binding design

### Router guidance

The remaining literal heading dependency occurs in the Analysis Router loader, Engine `read(include_routing)`, and logical route guidance editing. Replace all three with one shared parser owned by the existing Analysis routing boundary and exported through its public package.

The selected representation is a narrow, documented pipe-table contract: unfenced top-level two-column Markdown tables in Router are selection tables; inline canonical normative-module links in their destination cells identify selected targets. Header wording, section titles, and surrounding prose are presentation. A reference destination is optional help rather than an executable selection. Validate local destination containment and canonical resolution. Code blocks and prose examples supply no route authority. The helper records exact row spans so authoring replaces only the selected rows. New rows append to a real table, not relative to a historical heading. Ambiguous multiple selection rows for an edited target fail explicitly.

This uses existing Router table structure without a new metadata registry or migration that would overwrite accepted prose. Executable applicability remains in `router-projection.toml`; declared target agreement remains checked. The parser is deliberately not a general Markdown interpreter. Preserve unchanged text outside selected rows. A heading can be renamed or the optional historical example removed without changing facts/rules. No compatibility fallback to the old delimiters is retained.

### Batched decisions

Add authoring-only `resolve_many(context, submissions, detail?)` for 1–128 ordered explicit submissions, at most 256 KiB of serialized submissions. The context must bind a current proposal Analysis. Each supplied work handle binds that original analysis. Reject duplicate decision targets, incompatible/stale handles, unsupported submissions, and oversized input before authorization or durable mutation.

Use the existing `_apply_submission`, evidence validation, current authorization and Analysis evaluation. For each item, re-evaluate the staged successor and verify its target is still applicable; internally bind the already-validated original work identity to that staged analysis. An item that becomes inapplicable rejects the batch. Final evaluation/provider completion uses the same owner as single submissions.

Publish only the final immutable Analysis aggregate. A rejected batch publishes none of its intermediate analyses. Authorization/provider observations can occur during validation; this is not a transaction over external providers. No review, readiness, Git publication, or new mutable batch store is created. Final head and material checks preserve proposal currency. An ambiguous persistence failure is observed using the original context rather than blindly retried. A lost response can be safely re-evaluated against immutable analysis authority, while current evidence and authorization remain required.

Keep single-decision resolution as a useful interactive operation. Both paths use the same decision validator, not parallel rule implementations. Preserve records, fingerprints, rationale, and evidence per decision. Registration and coverage certification remain distinct.

### Compact results and detail

Focused workflow calls default to `detail: compact`; explicit `full` requests retain complete diagnostic analysis. Native analysis interfaces remain complete. A compact outcome includes exact analysis identity, truthful counts, completion state, and typed continuations to selected detail. Errors, readiness, publication, and recovery results retain their decision-relevant fields.

Add authoring-only `workflow_details` for one exact analysis and one selected section, returning at most 16 items (default 8) with a 64 KiB domain payload bound. Pagination is observational, not authorization. An observation digest binds the selected complete live section, section name, and analysis. Subsequent pages require it; changed evidence/observations return a stale-observation rejection rather than silently skip items. Pages contain full selected items, not truncated strings. If an item exceeds the bound, return a precise result-limit diagnostic; targeted existing inspection or explicit full reading remains available. Recompute live checks; cache only existing immutable material.

Default responses exclude duplicated full obligations, decisions and routing context; the complete evidence remains accessible. A compact success never represents a partial batch as accepted. Retain explicit status such as `needs-action`, `requires-change`, `stale`, or `recovery-required`.

### Running interface and catalog

Add a read-only `runtime_info` operation available to both purposes, independent of standards content and authoring-store availability. A process-owned identity records interface version, purpose, implementation version, startup implementation fingerprint, exact catalog digest, and an opaque instance ID. Fingerprint only installed runtime code/contract inputs, not mutable standards, Git refs, paths, credentials or databases. Distinguish startup identity from current on-disk installation state when queried; a changed/unreadable installation gives `restart-required`/`unavailable`.

MCP initialization, tool-list metadata and tool-response metadata identify that process/catalog. Unknown-tool errors carry bounded current-interface context and a refresh/restart action. A supplied expected catalog digest can identify client mismatch. This cannot inspect a client's private cache or refresh it automatically. Keep `listChanged: false` because this implementation does not hot-reload. After code updates, restart the server, reconnect, list tools and compare runtime identity before mutations. Keep protocol 2025-11-25; protocol modernization is separate work.

The same identity service supports native/reference transports. Use generated request/result schemas. Identity queries execute no Git write, snapshot capture, authorization mutation, code reload, or store reset.

## 3. Compatibility, retained state, and installation

Allocate interface edition 36 for the coordinated public API change. Generated models, catalogs, examples, clients and focused-result consumers update together. Old default-full response assumptions are intentionally replaced; full diagnostic detail remains a current selected feature, not an old-version adapter.

Do not increment independent Analysis, Snapshot, readiness or storage formats unless a real changed representation requires it. Batched decisions use the existing Analysis aggregate and record semantics. Preserve current authorization/evidence revalidation and admitted recovery behavior. No compatibility shim, historical parser, database migration, or rewriting shared history is needed.

Return a base-bound patch plus complete changed files, manifest, plan, report and application instructions. Because the user's local migration is unavailable, do not replace the real Router, Core, skill reference, manifests containing content approvals, or generated input manifest with baseline-derived copies. Regenerate derived suite inputs at integration using the actual merged tree. Patches to shared tests/technical docs require normal reconciliation if locally changed.

Work in local branch `implementation/engine-routing-review-ux` in the disposable checkout. This isolates cross-boundary changes and supports reproducible tests; it is not a requirement on other projects. Deliver through ZIP, without remote writes or local-user database access. Keep the branch/commits as evidence; no shared ref is advanced.

## 4. Milestones, write sets and gates

### M1 — Heading-independent routing

Status: `Implemented`. Owners/write set: `tools/standards_analysis/standards_analysis/{routing.py,router_guidance.py,__init__.py}`; `tools/standards_engine/standards_engine/{logical_authoring.py,engine.py}`; affected routing and authoring tests; this plan directory.

Deliver one parser consumed by loader, readable inspection and authoring. Test renamed/deleted historical headings, fenced examples, prose links, references, malformed destinations, repeated targets, escaped cells, additions/removals/retarget swaps, and unchanged surrounding text. Gate: baseline reproductions fail for the old heading-bound code; corrected focused and canonical-compiler tests pass. Existing ordinary routing results remain equal.

### M2 — Coherent review batching and bounded views

Status: `Implemented`. Owners/write set: Engine `engine.py`, `agent_workflow.py`, new `decision_batch.py`, `workflow_presentation.py`, `tools.py`, `context_projection.py`; canonical `contracts/a1-contract.schema.json`, `contracts/a1-interface.toml`, generated models/catalog; `tools/standards_contracts/standards_contracts/compiler.py` for array submission capability coverage and validated numeric page bounds; affected contract and workflow tests and client harnesses.

Deliver shared decision validation, final-only publication, compact focused responses and section paging. Gate: equivalent single/batch outcomes, mixed coverage/consumer/impact/fact decisions, duplicate and stale rejection, missing evidence and denied authorization leave no partial Analysis, head change prevents success, cold replay, cross-context page invalidation, full-detail availability, and application-purpose exclusion. Prove response reduction on the same material and report measured scope, not an unmeasured universal speed claim.

### M3 — Runtime identification, composed qualification and delivery

Status: `Implemented`. Owners/write set: Engine `runtime_identity.py`, `__init__.py`, `mcp.py`, `tools.py`, relevant schema/generated files; reference CLI `.agents/skills/standards-engine/scripts/invoke.py` if needed; technical Engine `PURPOSE-SEPARATION.md`, `contracts/README.md`, package READMEs; focused runtime/MCP tests and real stdio workflow test; plan/ledger/issues/report.

Gate: a real server returns consistent identity through initialize/list/call/runtime_info; code changes require restart, ordinary content publication does not; unknown tools and mismatched catalog observations remain nonmutating; no private paths escape. Qualify actual batch-to-review-to-preflight-to-apply-to-readback in a disposable Git/SQLite repository and a cold process. Run selected full package suites, generated freshness, structural checkpoint, exact staged review, preservation and patch reproduction. Report the actual environment and distinguish the raw MCP peer from an official SDK/client.

## 5. Acceptance claims

| ID | Observable criterion | Kind | Environment | Mode | Status |
| --- | --- | --- | --- | --- | --- |
| U1 | Router loader, readable inspection and authoring are independent of display headings and agree on exact selection rows. | integration | representative source corpus | automated | passed |
| U2 | A batch retains each explicit decision and publishes only its valid final analysis; rejected items leave no partial authoritative batch result. | integration | real SQLite plus controlled authorization/evidence | automated | passed |
| U3 | Compact summaries and paged detail preserve all actionable states; changed observations cannot silently alter pagination. | contract | deterministic fixtures and context/section substitution | automated | passed |
| U4 | Actual MCP batch/review/publication/readback works; application purpose excludes authoring operations and material. | system | real stdio, Git and SQLite | automated | passed |
| U5 | Running process/catalog identity and installation drift are observable without writing or opening the standards store. | system | real server and source replacement fixture | automated | passed |
| U6 | Canonical declarations and all generated consumers agree; changed implementation satisfies selected tests and structural checks. | contract | complete checkout and available interpreter | automated | passed |
| U7 | Integration preserves real migrated content/store and works on the supported locked host with local accepted revision. | release-artifact | user's Python 3.11/3.12 and actual migrated corpus | either | pending |

M1–M3 implementation can finish while U7 remains pending. The final report must distinguish implemented/tested code from installed acceptance and full compliance against unavailable local wording. Passing tests never certifies every unrelated standard or the entire library.

## 6. Composed-design admission

1. **Independent concerns:** Analysis owns decisions; metadata/Router representation owns exact selection; presentation owns bounded delivery; transport owns running identity; store/publication owners remain unchanged.
2. **Interleaving:** Exact original Analysis work identities bind batch input; staged successor IDs are internal. Content revisions are independent of interface/catalog identity. A page observation is neither permission nor a durable revision.
3. **Caller knowledge:** Authors supply an original context and actual decisions, then follow current context/continuations. They need no file layout, sidecar, SQLite transaction, private cache, or repeated intermediate analysis handles.
4. **Change paths:** New submission variants update domain/schema/capability declarations; page formatting stays in presentation; heading wording changes no code; runtime deployment identity does not invalidate standards snapshots.
5. **Stable boundaries:** Reuse immutable state/evaluation, authorization, publication, generated codecs, and proposal-material scopes. No second domain validator or persisted workflow state.
6. **Independent evolution:** Single and batched resolution share their rule owner. Router representation is tested separately from workflow transport. Decision submission and publication retain their existing live evidence checks; historical detail reads remain bound to immutable Analysis.
7. **Deletion:** Removing the shared Router parser recreates inconsistent readers/editors. Removing batch staging recreates partial writes or serial transport. Removing summary/paging recreates truncation. Removing running identity recreates ambiguous deployments. A generic job system, ACL service, new database, hot reload, Markdown platform or model-based reviewer adds no deciding value and is omitted.
8. **Contained complexity:** The necessary additions are one shared selector, final-only batch composition, one presentation adapter, and one process identity owner. Keep other semantics in existing owners; do not split to satisfy file/line counts.

## 7. Verification procedure and repair

Start with the known counterexamples before changing production code. Run focused cases with the complete checkout; use the existing compiler and real stores. Regenerate public contracts from their canonical owner. Refresh suite-input data locally for verification but exclude baseline-derived content manifests from delivery where they could overwrite local migration state.

Record test commands, actual versions, complete versus interrupted runs, isolated/controlled providers, and uncovered environments. Make an independent final pass over staged code and test assertions; an external reviewer is unavailable here and must not be invented. Code-level self-review is not the prior independent material review of standards.

Repair local failures in the admitted scope. Replan only when a needed result requires new retained state, changed decision authority, a different Router semantic contract, or exposure beyond purpose separation. Keep unknown local content and supported-host qualification in the handoff rather than discarding requested implementation.

## Sources

Source anchors: baseline Core/Router and routed owners; `docs/guides/positive-guidance-and-provenance.md`; `routing.py`, `_project_route_guidance`, Engine `_read_value`; `agent_workflow.py`, `_apply_submission`, `_evaluate_publish_project`; `mcp.py`, `tools.py`, generated-contract authority. Public protocol source: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx . The protocol supports explicit tool discovery and describes `listChanged` as notification capability, not automatic server-code reload.
