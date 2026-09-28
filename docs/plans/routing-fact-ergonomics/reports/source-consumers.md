# Source and Consumer Inventory

Inspected subject: `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`, tree
`6d1f1f8a33d4391c9ab8e315b18bfc25603e1b97`. All line ranges refer to that source,
not to unimplemented candidate code. This is a bounded routing-contract inventory,
not proof that every external consumer has been discovered.

## Semantic and authority owners

| Source | Observed role | Candidate disposition |
| --- | --- | --- |
| `tools/standards_applicability/standards_applicability/core.py:84–109` | Immutable FactValue / FactSet and canonical serialization | Preserve representation, states and schema-digest binding. |
| `core.py:217–235` | FactSchema lookup/bind: registered names, alias collision, canonical values | Keep semantic owner. A narrow shared required-name lookup may be extracted; do not reproduce private index/error logic in transport. |
| `core.py:513–566` | Three-valued evaluation and value-type/domain/nullability normalization | Preserve. New input omits a redundant type declaration, not these rules. |
| `tools/standards_analysis/standards_analysis/routing.py:35–69` | RouterProjection and canonical eight-field fact records | Read/use its existing FactSchema. Do not move input formatting into canonical fact metadata or change fact material identity. |
| `tools/standards_engine/standards_engine/engine.py:2790–2937` | Binding/selection and native/focused route rendering | Separate binding from selection using existing bound FactSet. Preserve native requests and selection algorithm. Keep focused wire projection outside canonical rule interpretation. |
| `engine.py:1140–1163` | Proposal/native route result projection | Continue binding canonical facts; preserve preview semantics and retained contracts. |
| `engine.py:3479–3511` | Domain exception set and authoring rejection projection | Applicability errors are included; generated ContractError is not. A proposed adapter must not create an invalid canonical request and let it escape here. |

## Focused producer and return paths

| Source | Observed role | Candidate disposition |
| --- | --- | --- |
| `tools/standards_engine/contracts/a1-contract.schema.json` | RouteCall uses typed FactSet; FactSet/FactValue are shared; focused results echo facts | Add RoutingFactAssertion/Assertions; replace only RouteCall and focused AgentRouteResult/CompactRouteResult fact fields. Preserve canonical FactSet, RouteRequest, ApplicationRouteRequest and candidate route definitions. |
| `tools/standards_engine/contracts/a1-interface.toml:1–4,122–128` | Interface 44, request 6/result 7, same focused RouteCall in both purposes | Version focused replacement as interface 45 for this baseline; leave request/result and persisted editions unchanged. |
| `tools/standards_engine/contracts/examples/a1-examples.json` | Mixed current fixtures for focused and native operations | Update only affected focused examples. Preserve native/Analysis canonical facts and historical records. |
| `tools/standards_engine/standards_engine/_generated_contract.py` and `contracts/generated/agent-tools.json` | Derived declarations and catalogs | Regenerate from canonical source; no handwritten edits. |
| `tools/standards_engine/standards_engine/tools.py:366–370` | Facade validates and forwards focused route | Keep routing through generated input/result validation. Update only if necessary for narrow typed binding feedback; no pre-snapshot type guessing. |
| `tools/standards_engine/standards_engine/agent_navigation.py:30–70` | Focused authoring route selects snapshot and constructs typed RouteRequest | Insert the small compact-to-bound projection after verified authority. Consume bound selection, then project new fact echoes before generated result validation. |
| `agent_navigation.py:155–214` | Content bounds and returned next RouteCall | Preserve limits/lifecycle/content; derive continuation assertions from the same bound facts, snapshot and selected detail. |
| `tools/standards_engine/standards_engine/context_projection.py:222–240,263–345` | Qualified application route; direct query and preview also call shared route logic | Qualify Router before binding. Distinguish explicitly selected focused route from canonical query/preview at the existing operation boundary, not by guessing payload shape. Project input errors without private data. |
| `tools/standards_engine/standards_engine/input_feedback.py` | Bounded non-sensitive issue and describe_input projection | Reuse its contract for dynamic focused fact failures if needed. Do not introduce raw validator messages or a generic diagnostics rewrite. |
| `tools/standards_engine/standards_engine/mcp_catalog.py` | Native schema closure and brief tool guidance | Update route description/usage only as necessary; new shape is generated. Preserve all tools, purposes and output-delivery choices. |
| `tools/standards_engine/standards_engine/contract_discovery.py`, `mcp.py`, `runtime_identity.py` | Discovery, catalog digest and transport validation | No redesign expected. Include in contract/transport regression coverage; touch only on a demonstrated direct propagation requirement. |

The inspected direct selection graph has one focused authoring caller in
`agent_navigation.py`, application/preview callers through ApplicationView, and two
native/proposal `_route_value` callers in Engine. These canonical consumers must
not receive the new assertion map without explicit binding. Fact inputs are not a
new stored object or mutable task session.

## Direct test and client population

The following current files contain direct focused routing or its shared fixtures.
Classify each call individually: several files use both focused and canonical
native route inputs. Preserve tests' independent expected facts and selected policy
oracles instead of deriving expected values through the implementation under test.

- `tools/standards_engine/tests/test_agent_navigation.py`
- `tools/standards_engine/tests/test_compact_routing.py`
- `tools/standards_engine/tests/test_route_content.py`
- `tools/standards_engine/tests/test_purpose_projection.py`
- `tools/standards_engine/tests/test_proposal_consumers.py`
- `tools/standards_engine/tests/test_fact_material_ownership.py`
- `tools/standards_engine/tests/test_immutable_work_reuse.py`
- `tools/standards_engine/tests/test_capture_handoff.py`
- `tools/standards_engine/tests/test_capture_handoff_transport.py`
- `tools/standards_engine/tests/agent_efficiency_trace.py`
- `tools/standards_engine/tests/codex_navigation_client.py`

Additional directly connected transport, catalog and generated-contract fixtures
are selected from their declarations and module calls, even when requests are
constructed indirectly: `test_mcp.py`, `test_purpose_transport.py`,
`test_agent_interaction_transport.py`, `test_generated_contract.py`,
`test_schema_presentation.py`, `test_input_discovery.py`, `test_output_delivery.py`,
`test_catalog_inventory.py`, `test_efficiency_trace.py` and `mcp_workflow_client.py`.
Reconcile this list at implementation against current names; adding an equivalent
consumer does not by itself widen the architecture.

`test_route_content.known_facts()` currently constructs canonical typed envelopes
and is shared by several tests. Do not blindly change it for every consumer. Keep
an explicit canonical fixture and a separately named focused-assertion fixture (or
literal new request examples). This is test input construction, not a second live
API or runtime fallback.

Add focused tests for the new bidirectional adapter, and actual replacement-process
MCP cases for both purposes. The exact filenames may be
`test_routing_fact_inputs.py` and `test_routing_fact_transport.py`. If a narrow shared
lookup is introduced, add its canonical-binder preservation tests to applicability.
Do not absorb the earlier deferred generic test-strengthening backlog.

## Live guidance and integration artifacts

Update the existing operational owner, not historical reviewer verdicts:

- `.agents/skills/standards-engine/SKILL.md` and
  `.agents/skills/standards-engine/references/navigation.md`: current focused input
  examples, states, type source and continuation guidance.
- `.agents/skills/standards-engine/references/environment.md`: interface refresh and
  saved-request cutover, preserving native/on-demand registration settings.
- `tools/standards_engine/README.md`, `PURPOSE-SEPARATION.md`, and contract README if
  its current input descriptions change: authoritative current behavior with links
  to this plan. Do not scatter copied grammar specifications.
- Existing configured-client qualification instructions/harness only where actual
  routing requests or assertions change. Keep provider authorization and model
  execution opt-in; the plan does not authorize external transfers.
- `docs/plans/routing-fact-ergonomics/**`, a link in `docs/plans/README.md`, and
  `evaluation/standards-effectiveness/generated/suite-inputs.json` through its owner.

## Explicit no-change dispositions

The accepted sequence's plans/reviews/owner decisions; normative Core/Router/policy
text; canonical routing-fact records and their material bindings; expression grammar;
evidence contracts/decisions; typed routing-edit value classes and persisted edit
serialization; cache policies, capture proofs, storage locks and integrity lifecycle;
identity codecs; Python dependency lock/CI matrix; configuration flags and output
schema delivery; baseline audit/history artifacts; unrelated repository ZIPs.

Planning output is a new directory only. Implementation must inspect the actual
worktree, branch and current consumers before starting, stage only its admitted
write set, preserve unrelated work and bind review to the material candidate rather
than prescribing a new commit topology. Source mutations require the later R1
`start` admission; this planning turn made none.
