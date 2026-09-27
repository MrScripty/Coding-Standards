# Agent Interaction Quality

Status: Verifying
Acceptance: pending
Base: `67266105cbd900d89572eb540b54b298653ed01c`
Operation: implement this plan (explicit user-approved follow-up).

## Outcome and authority

Make malformed input and graph vocabulary discoverable at the agent boundary,
and make focused routing concise without changing applicability. Preserve exact
policy, evidence, immutable handles, qualification, authorization and publication.
The clean source bundle at the pinned base is the only implementation workspace;
production and the operator's unrelated ZIP edits remain untouched.

The executable Router selected 23 applicable standards with no unresolved facts:
Core/Router; implementation, verification, planning, documentation, build and
development proportionality; library, generated-contract and IPC profiles;
contracts, architecture, dependencies, security, diagnostics, performance; code
design, schema/protocol/evolution, replay and independent-oracle details.
The first routing attempt used an invalid activity spelling and was rejected;
the registered vocabulary was inspected and the corrected admission succeeded.

## Composition and decisions

- The contracts runtime still delegates validity to jsonschema. It derives a
  bounded value-free diagnostic from structured validator errors, using a known
  disjoint discriminator only to select relevant error causes, never to approve
  an input. The facade projects it into typed feedback and input discovery.
- Snapshot navigation owns registered relationship vocabulary. A read-only
  `relationship_groups` operation returns whole paged group records from the
  selected graph. The application projection supplies only permitted groups.
  Unknown focused queries return the same first page; valid empty relationships
  stay successful. No alias guessing or second group registry is introduced.
- Focused authoring `route` defaults to a compact result with selected reading
  entries, exact supplied facts, all unanswered questions, unresolved-target count
  and a same-snapshot full explanation request. Explicit full route and native
  query keep existing explanation semantics. Application remains qualified and
  does not disclose authoring explanations. No missing fact is treated as absent.
- Input and graph detail have separate owners: installed contract discovery vs
  snapshot vocabulary. Presentation never grants permission or mutates standards.
- Catalog costs are measured by purpose and mode. Compatibility remains default
  until actual supported-client and review dispositions permit retirement. Add no
  new mode or host heuristic. Provide a read-only inventory/reporting command and
  document the native/application deployment choices and concrete retirement gate.

These are three independent projections over existing owners, not another workflow
engine. Callers carry one snapshot/context and supply only missing information.
Changing a validation explanation affects runtime feedback and its facade; changing
registered groups affects the graph snapshot, not schemas or descriptions; changing
routing presentation affects the focused adapter, not rule evaluation. Bounds and
continuations are explicit. No service, mutable session, or new state store is needed.

## Write set

Contracts runtime/errors and one diagnostic-projection helper plus focused tests;
Engine canonical schema/interface, generated Python/tool projections and examples;
agent_navigation, a relationship vocabulary presentation module, context_projection,
engine/tools facade, mcp_catalog and affected rendering/client/test consumers;
read-only catalog inventory utility; operational skill/reference guidance, Engine
and Contracts documentation; this plan/ledger/issues/verification, and the owning
generated suite-input manifest. Extend only to directly affected consumers.
Normative policy, approvals, provenance, dependency pins and user state are excluded.

## Acceptance and cutover

1. Invalid fields/constraints are identified with bounded non-sensitive feedback;
   no proposal, decision, evidence acceptance or publication occurs on rejection.
   Ambiguous unions stay explicit; valid requests and original validation pass/fail
   outcomes remain unchanged. Private/unpublished operations remain unavailable.
2. Vocabulary pages and recovery use the exact snapshot and permitted graph,
   cover paging and lifetime failure, and separate unknown groups from empty edges.
3. Compact/full routing has identical selected closure, facts and unresolved
   questions. Explanation and routed-content continuations retain exact authority
   and presentation; known-empty and omitted remain distinct.
4. Canonical generation, independent schema validation, focused and affected suites,
   cold MCP interactions and retained-state checks pass. Measure calls and serialized
   data without inferring model-token/billing savings.
5. Interface 41 versions the additive diagnostics/group operation and coordinated
   compact-route result. Native mutation declarations and persisted versions stay
   unchanged. Restart/reconnect; preserve stores and handles. Update explicit old
   result-kind consumers together.
6. Patch reconstructs against the base with exact bytes/modes; unrelated files do
   not change. Supported locked-runtime CI and independent review remain named
   acceptance gates when unavailable here. Actual model behavior is not inferred
   from scripted MCP tests.

Implementation and local verification are complete. See [verification](verification.md)
for the 488-test Engine selection, affected package runs, exact measurements and
retained-state checks. The next slice is supported-runtime CI on this patch, a
check of the deployed new navigation/feedback surface and independent review.
Acceptance remains pending. Compatibility retirement is a separately conditional
cutover, not an unimplemented part of these three presentation features.
