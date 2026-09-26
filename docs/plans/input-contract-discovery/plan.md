# Input Contract Discovery

**Plan status:** Verifying
**Current phase:** M1 locally verified; M2 host qualification and review
**Next slice:** Run supported CI and actual-client/model qualification, then obtain independent review.
**Acceptance status:** pending
**Execution ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)

## Objective and admission

User-authorized continuation from `190491fb36314624aec74946f58fd0f61f852a60`:
make essential nested authoring inputs discoverable even when a client abbreviates
its model-facing declarations. The reported native-mode client qualification failed;
full-schema transport and scripted navigation passed. Compatibility retirement is
not authorized by those passing checks and remains outside this implementation.
Operation: implement this plan. The executable Router selected the applicable
implementation, verification, planning, documentation, build, proportionality,
library, generated-contract, IPC, architecture, contracts, diagnostics, security,
performance, code-design, replay, evolution, schema, protocol and oracle owners
from explicit facts, with no unresolved conditions.

## Binding decisions and scope

1. One small, flat `describe_input` operation observes the installed compiled input
   contracts for tools actually published in the running purpose/catalog. Catalog
   projection and validation keep their existing owners. No standards snapshot,
   Git read, evidence registration, mutation or store is needed for discovery.
2. An operation's input definition and its reachable named definitions form its
   discoverable scope. Optional selectors name only definitions within that scope.
   Exact schema records are returned as JSON document strings (`schema_json`):
   this preserves arbitrary literal data without creating another schema dialect
   interpreter or changing structured mutation inputs into strings. Read a record's
   `$ref` to select its named definition directly. Breadth-first pages put containing
   shapes and union choices before their descendants. Complete closure is available
   through explicit paging; a focused selection avoids unrelated alternatives.
3. The existing runtime catalog digest binds every selected or continued request.
   A first operation-only read captures current catalog identity; selector/offset
   requests require its exact `expected_catalog`. Changed catalogs reject. Names
   confer no permission; unpublished operations/definitions remain unavailable.
   Defaults: eight records, maximum sixteen, at most 16 KiB complete domain result
   JSON. Byte pressure yields fewer whole records; one oversized record is an
   explicit unsupported result, not a truncated or silently incomplete schema.
4. All published tool descriptions point to discovery before long descriptions or
   compatibility text. Coverage follows the actual operation list, not a handwritten
   authoring subset. Both schema modes remain supported and compatibility remains
   the default. Validation, batching, evidence checks, review and publication remain
   unchanged. No model-visible effect is claimed from raw-schema tests alone.
5. Interface 40 adds discovery. Analysis/request/state/handle and persistence
   versions remain unchanged. Restart/reconnect; preserve stores and handles.

## Write set

- Engine canonical interface/schema, examples and generated projections.
- A pure input-discovery owner, MCP catalog/transport composition, and reference CLI.
- Contracts package public export of the existing reference iterator if needed.
- Focused tests, directly affected interface/catalog consumers, configured-client
  harness, and a separately named model-visible qualification procedure/harness.
- Skill references, Engine contracts/readme, this plan and generated suite inputs.

Normative standards, application approvals, user stores, upstream Codex source,
new dependencies, client budget policy and compatibility removal are out of scope.
Direct consumers may be updated atomically with the new operation; record findings.

## Objective acceptance and evidence

| ID | Criterion | Oracle / mode | Status |
| --- | --- | --- | --- |
| A1 | Flat input and complete exact reachable schemas for every available operation; no cross-purpose disclosure | Canonical compiler + independent Draft 2020-12 validation and direct equality, automated | Passed locally |
| A2 | Selected/continued reads bind catalog; bounded pages, explicit failures, literal data and recursive closure | Focused negative and equivalence tests, automated | Passed locally |
| A3 | Actual stdio discovery works after process replacement without repository/store or client source access | Cold-process consumer and CLI tests, automated | Passed locally |
| A4 | Discovered fields suffice for all five focused authoring operations, ready batches and evidence reuse without semantic changes | Real disposable-workflow tests, automated | Passed locally |
| A5 | Actual client/model obtains missing shapes using exposed tools, constructs valid inputs and follows the workflow without source/schema fixtures | Operator-run model-visible qualification on exact client/version; separate from scripted harness | pending |
| A6 | Generated outputs, affected suites and complete structural checkpoint pass; independent review and supported locked environment qualify the diff | Automated checks + integration review | pending |

The deciding external semantic oracle remains jsonschema Draft 2020-12; discovery
copies selected declarations and performs no instance constraint evaluation.
Performance evidence records discovery call and byte costs, not inferred model
billing. A reported client success must include the actual transcript and exposure
surface, not only a catalog dump or an agent's assertion.

## Simplicity and ownership review

**Applicability:** applicable

- Independent concepts: canonical input semantics, purpose/catalog availability,
  observation identity, bounded presentation, and client/model qualification.
- State/identity: one process-owned immutable interface and the existing catalog
  digest; no mutable workflow pointer, persistent discovery token or registry.
- Caller knowledge: tool name; returned named selection and catalog digest when
  narrowing or paging. Composition roots supply the compiled interface and actual
  published catalog; discovery does not load another installation.
- Change paths: input changes are automatically described; availability changes are
  inherited from catalog membership; paging policy changes touch discovery; client
  rendering changes touch qualification, not native authoring or persisted records.
- Stable boundaries: shared schema traversal owns reference discovery; the existing
  compiler/validator owns dialect semantics; MCP frames typed observation outcomes.
- Necessary complexity: cycle-safe reference closure, bounded whole-record pages
  and explicit stale/invalid/unavailable/oversize outcomes. No general query language.
- Deletion result: no prior validation or schema modes removed; the new read replaces
  repeated ad hoc source/schema lookups. Compatibility text remains until its actual
  supported consumers have a qualified direct or discovery path.

## Milestones and replanning

M1: Discovery, correlated guidance, regressions, real workflow evidence and
qualification handoff implemented and locally verified. State: Verifying until
M2 closes the named external acceptance gates.
M2: Operator qualification and independent acceptance review. State: Planned.

Replan for a demonstrated change to native validation, authority, atomic mutation,
persisted identity or disclosure semantics. Unknown client/model access does not
block independently useful discovery implementation; it keeps A5 unaccepted.
