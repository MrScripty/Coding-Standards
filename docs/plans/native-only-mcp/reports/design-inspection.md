# Native-only MCP design inspection

**Date:** 2026-09-27. **Purpose:** evidence for an implementation plan, not a source implementation or release qualification.

## Source and evidence boundaries

The public connector returned `MrScripty/Coding-Standards@52b122683faf05ef85c86c6903a61d54870a9be4`. The automatically mounted source archive had SHA-256 `51a012f96e004708c7cf759965651c2d1909304efcb6be17e0e2c5c906f9acdd`. Its Git bundle was cloned into an inspection-only directory and HEAD verified.

The delivered `Coding-Standards-output-contract-delivery.zip` has SHA-256 `6b6b8ffe62c139a889315f6e31f8f1bf078230917c94af9df82ae27632198f8e`. The existing delivery manifest was applied and checked: 39 updated/new files and one deletion, with original and resulting hashes. This reconstructed the delivered interface-42 tree for inspection. The real integrated commit must be recorded when implementation starts; no claim is made that the older public head contains interface 42.

The user's reports establish that their saved Codex registration and restarted connection serve interface 42 using `--schema-mode native --output-schemas on-demand`, and that navigation, targeted output discovery and invalid-proposal feedback worked through connected tools. Earlier reported Codex 0.157.1 / gpt-6-astra qualification reached readiness using actual fixture evidence, shared discovery, eight discovery calls and zero authoring repairs; original and independent observer verdicts were retained. Those are **reported observations**, not a new replay or independently observed live run during this planning task.

The latest instruction is the support decision: compatibility input presentation is no longer required. Testing the forthcoming native-only candidate remains necessary, but it is not a reason to keep the retired alternate implementation.

## Findings mapped to source owners

| Source owner in the reconstructed tree | Observation | Plan disposition |
| --- | --- | --- |
| `standards_engine/mcp_catalog.py`, `SchemaMode` and `tool_catalog` | Both modes select the same canonical operations but differ in input rendering and embedded schema text. Output delivery has a distinct enum and argument. | Delete only the input-mode system; keep separately owned output delivery. |
| Same module, `input_schema` and `presented_input_schema` | Native still constructs a recursive inline schema and a reference schema and selects the smaller serialized result. | Replace the two-transform algorithm with the existing canonical reference closure. |
| `standards_contracts/schema_structure.py` | Schema-location traversal already preserves literals and reference semantics. `map_schema_children` is used by the inliner; closure and traversal have other active owners. | Remove the unused mapper after caller confirmation; retain shared structural APIs and their admitted semantics. |
| `standards_engine/mcp.py` | Mode choice appears in the constructor, instance state, catalog call, argparse option and final construction. | Delete the parameter/state/CLI branch in the same change; retain normal process lifecycle and output selection. |
| `standards_engine/tools.py`, `_catalog_observers` | Direct facade observers derive a full purpose-qualified catalog using builder defaults. | Verify resulting identity/semantics, without forcing the facade to learn a constant native-mode setting. |
| `.agents/skills/standards-engine/scripts/invoke.py` | CLI schema inspection uses shared structural closure; observer catalog construction uses defaults. | Verify current behavior; change only an actually affected assumption. No new mode flag. |
| `contract_discovery.py` | Selects canonical input/output roots with bounds, purpose/operation scope and exact catalog binding. | Keep; it is the working solution for abbreviated model declarations, not temporary fallback text. |
| `runtime_identity.py` | Actual catalog, canonical schema and installed implementation have separate digests. | Preserve ownership and scoped invalidation; a removed launch option does not invalidate a proposal. |
| `request_evidence.py` and `qualified_operations` | Generated agent input variants normalize typed request-local evidence into native domain calls. | Keep unchanged; native presentation is not permission to drop agent evidence variants. |
| Codex harnesses and `replay_discovery_qualification.py` | Live mode selection and historical recorded mode are currently connected to catalog reconstruction. Some validators are obtained by constructing an eager catalog. | Remove live selection, preserve evidence provenance, enforce current-source replay boundaries and derive private validators from canonical roots. |

The supporting [consumer inventory](consumer-inventory.json) records discovered file paths, line locations and hashes. It is an inspection snapshot, not an exhaustive claim about unknown external clients.

## Comparison of implementation choices

### Selected: one exact reference-preserving input schema

Use the existing `schema_closure` over each purpose-qualified operation input definition. This preserves field names, requiredness, unions, recursive references, literal/default values and constraints while eliminating expansion and the competition between two representations. Validation remains delegated to the existing JSON Schema library/runtime. Discovery remains available whenever a host abbreviates a declaration.

The input root and definition closure remain independent data; mutating a returned catalog must not affect later calls or the compiled interface. Source retrieval and additional schema evaluation are not added.

### Rejected: preserve the mode as a one-value enum or ignored flag

This would keep caller/configuration knowledge and test plumbing after the underlying choice is gone. Updating the source and the known launch command together is simpler and makes misconfigured old installations fail visibly.

### Rejected: keep all old output and input machinery under a renamed profile

Purpose, operation scope, input presentation and output transmission are not one domain concept. A renamed umbrella profile would hide rather than remove the retired input branch. The plan retains only independent choices that still have a separately declared contract.

### Not part of this slice: removing eager output

The previous delivery established eager and on-demand as separate ways to transmit the same canonical result contract. Omitting `outputSchema` is supported by the selected MCP tools specification, but upfront validation remains a different consumer need. The native-only input decision does not authorize collapsing this axis. The known host keeps its explicit on-demand choice; this plan neither restores eager delivery there nor retires eager for other native consumers.

The same distinction protects structuredContent plus JSON TextContent. The selected MCP protocol recommends that result framing; it is not the embedded input-contract description workaround. The reference consulted was the official MCP `2025-11-25/server/tools` specification, in its Tool/Output Schema/Structured Content sections.

## Read-only measurement

The experiment loaded the reconstructed compiled interface and constructed its native catalogs. It then substituted a reference-preserving `inputSchema` in memory for every published tool. Output schemas or digest metadata, descriptions, annotations and operation selection remained unchanged. It used the same `json.dumps(...).encode('utf-8')` byte measurement as the earlier delivery.

| Scope | Output delivery | Current native bytes | Reference-only bytes | Difference |
| --- | --- | ---: | ---: | ---: |
| Authoring / focused | eager | 708,288 | 712,662 | +4,374 |
| Authoring / focused | on-demand | 104,285 | 108,659 | +4,374 |
| Authoring / advanced | eager | 1,027,382 | 1,034,331 | +6,949 |
| Authoring / advanced | on-demand | 178,268 | 185,217 | +6,949 |
| Application / focused | eager | 82,266 | 83,514 | +1,248 |
| Application / focused | on-demand | 14,656 | 15,904 | +1,248 |
| Application / advanced | eager | 97,914 | 99,574 | +1,660 |
| Application / advanced | on-demand | 17,700 | 19,360 | +1,660 |

The 1,040 comparisons included applicable canonical examples and basic empty/null/boolean/list/extra-field inputs, repeated over these catalog combinations. Every substituted schema passed the independent Draft 2020-12 schema check and agreed with the baseline validator on these cases. This is finite fixture consistency evidence, not universal conformance, a full test-suite pass, or proof of a host renderer's behavior.

Actual tool counts are preserved in the measurement: 23 focused and 40 advanced authoring tools; 10 focused and 11 advanced application tools. Their count is not a simplicity criterion. The maintainability gain is deletion of configuration, transformation and co-change obligations, with a recorded size tradeoff.

Raw results: [reference-projection-measurements.json](reference-projection-measurements.json). Local environment: CPython 3.13.5, jsonschema 4.26.0 and rpds-py 2026.5.1. No installed client, model run, production mutation or automated package suite was exercised in this experiment.

## Standards route

A disposable authoring facade routed the removal/change task against the accepted standards at `52b12268`. The interface-42 code overlay does not change that normative corpus. All eight routing categories were explicitly supplied; absent framework/language-specific and workflow-profile mechanisms were represented as known empty categories, not inferred from silence. The selected route includes planning, implementation, verification, build, documentation, tooling, release and commit, with the corresponding library/generated-contract/IPC and architecture/contract/security/diagnostic/performance closure.

Twenty-six modules were selected with no unresolved questions, and exact reads were obtained. The saved [standards-route.json](standards-route.json) preserves those task facts and selections. Its snapshot handle belongs to the disposable inspection store and is not an argument for the production server.

## Acceptance implications

The current plan is ready for implementation admission; its future claims remain pending. The biggest avoidable cutover error would be removing the option in source while leaving it in the saved registration. The biggest data/evidence error would be treating a changed catalog as permission to discard old proposals or rewrite recorded verdicts. The planned owner boundaries, negative tests and narrow runbook address these independently.

The reference-only experiment and the user's earlier successful native discovery justify a bounded implementation and final real-client check. They do not justify inventing an unsupported-client matrix, repeatedly re-testing retired compatibility paths, or treating historical artifacts as active compatibility software.
