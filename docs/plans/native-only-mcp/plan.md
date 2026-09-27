# Plan: Native-only MCP input contracts

**Plan status:** `Verifying`
**Acceptance status:** `blocked`
**Current phase:** N2 acceptance preparation; source complete, required environment/host/review evidence pending
**Next slice:** **N2 — Installed qualification and accepted cutover**
**Canonical plan:** `docs/plans/native-only-mcp/plan.md`
**Current admission:** `verify` — source implemented; required N2 acceptance evidence pending
**Execution ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)
**Design evidence:** [reports/design-inspection.md](reports/design-inspection.md)

## Objective

Make native input contracts the sole supported Coding-Standards MCP presentation. Agents obtain exact fields directly or through `describe_input`, and receive exact output contracts through the existing selected delivery and `describe_output`. Operators and repository consumers no longer select, implement, or maintain an input compatibility mode.

The target is a smaller maintenance model: one input-schema construction path, one canonical contract authority, no compatibility renderer or dormant switch, and unchanged standards-reading, evidence, authorization, authoring, recovery, and retained-data semantics. Successful implementation removes accidental choices; it does not promise smaller JSON than the already deployed native/on-demand catalog.

The owner's latest native-only instruction explicitly retires the compatibility input-presentation promise. Earlier requirements to qualify every compatibility-dependent client before removal are superseded **for that promise only**. Identifying deployed launch commands remains necessary for cutover; hypothetical clients are not a continuing implementation blocker.

## Baseline, authority, and scope

### Source baseline

The intended baseline is **interface 42**, including on-demand output delivery. During this planning inspection, the GitHub connector returned `52b122683faf05ef85c86c6903a61d54870a9be4`, which precedes interface 42. Inspection therefore used that verified source plus the delivered `Coding-Standards-output-contract-delivery.zip`, SHA-256 `6b6b8ffe62c139a889315f6e31f8f1bf078230917c94af9df82ae27632198f8e`. Its manifest's 40 changed/deleted paths were checked against the base.

For integration, use the actual interface-42-or-newer checkout and record its revision and relevant differences. Preserve later changes. This is source identification, not a permanent exact-HEAD workflow or permission to replace the operator's checkout with the older retrieved revision. Resolve a material difference through this plan's re-plan rules.

### Standards authority

Apply [Core](../../../CORE-STANDARDS.md), [Router](../../../STANDARDS-ROUTER.md), [Planning](../../../workflows/planning.md), [Implementation](../../../workflows/implementation.md), [Verification](../../../workflows/verification.md), [Development Proportionality](../../../workflows/development-proportionality.md), and the selected required closure. The executable Router was run against accepted standards with explicit task facts: 26 selected modules, zero unresolved questions. The facts and result are retained in [reports/standards-route.json](reports/standards-route.json).

The route covers documentation, build, tooling, release and commit work; library, generated-contract and IPC boundaries; architecture, contracts, diagnostics, security and performance; code ownership, schemas, protocol projection, contract evolution, replay and independent oracles. Dependency guidance is selected through required closure, not through a planned dependency update. No language-specific mechanism or overlapping proposal-integration workflow is assumed.

This is **code and operational-documentation maintenance**. Normative standards, policy-unit semantics, application approvals, decision provenance and production standards publication are outside the write set. Applicable existing rules remain the authority; this plan does not redefine them.

### In scope

Retire the input-mode API, CLI option, alternate catalog construction and compatibility-only description generation. Replace the dual inline/reference sizing algorithm with one reference-preserving input projection. Update actual repository callers, qualification tooling, relevant tests, generated interface metadata, operational documentation and the known host registration. Verify domain preservation, discovery, new-catalog handling, and a fresh real native/on-demand authoring path.

### Preserved and out of scope

- Preserve `describe_input`, `describe_output`, purpose filtering, focused/advanced operation scope, compact/full reads, routing uncertainty, relationship vocabulary, typed input feedback and exact returned policy content.
- Preserve native domain request types and the agent variants that implement request-local evidence references. “Native presentation” does not mean selecting the base domain request instead of its published agent input variant.
- Preserve `OutputSchemaDelivery`, `--output-schemas eager|on-demand`, their current default and semantics. Output transmission is a separate existing consumer contract, not the retired input workaround. The known Codex deployment remains explicitly **on-demand**. Changing the output default or retiring eager delivery is not admitted here.
- Preserve the selected MCP protocol, structured results and matching JSON text results, schema validation, atomic decisions, explicit review/application, and recovery. MCP result framing is not the schema-description fallback.
- Preserve supported existing stores, snapshots, proposals, Analysis, readiness and recovery handles. Existing unsupported historic formats do not acquire new support.
- Preserve locks, dependency versions, unrelated ZIPs, unrelated working changes and remote refs. No production publication, automatic proposal retry, new session/cache/registry, client-name heuristic, transport negotiation layer, or replacement validator is included.

## Binding decisions and ownership

| ID | Decision | Owner | Replaces or preserves |
| --- | --- | --- | --- |
| D1 | Native is an invariant of the input presentation; the `schema_mode` argument and `--schema-mode` option cease to exist. | MCP catalog and process entry point; host operator for launch commands | Replaces `SchemaMode`, its default, branches and user selection. |
| D2 | Produce each input schema with the existing `schema_closure` over the purpose-qualified operation's canonical input definition. Preserve references rather than recursively expanding them. | `mcp_catalog.py`; structural semantics remain in Standards Contracts | Replaces `input_schema` and `presented_input_schema` dual construction/size selection. |
| D3 | Exact contract discovery and output delivery remain independent responsibilities. | `contract_discovery.py` and existing output-delivery owner | Preserves both discovery operations, bounds, digests and eager/on-demand output choices. |
| D4 | Only accepted live native consumers are supported after cutover. An old mode argument is a configuration error, including `--schema-mode native`. | Operator-facing CLI and Python composition APIs | Replaces a compatibility window with coordinated replacement; no no-op alias. |
| D5 | Catalog/interface changes and workflow persistence have separate invalidation scopes. | Interface declaration, `RuntimeIdentity`, existing store/handle owners | Versions presentation without changing request/state identities. |
| D6 | Qualification checks the exact canonical contracts and chronological knowledge, rather than requiring a second presentation or duplicate discovery. | Existing client observers/tests | Preserves cross-operation reuse and exact source/catalog admission. |

### Chosen implementation shape

The resulting catalog construction is conceptually:

```python
# Existing qualified operation and compiled definitions; not a new schema authority.
input_schema = schema_closure(
    definitions[operation["input_definition"]], definitions
)
```

`tool_catalog(interface, *, purpose, advanced=False, output_schemas=...)` retains only meaningful choices. `MCPServer` retains installation/lifecycle and those same choices. It does not store a constant `schema_mode`, expose a one-value enum, or accept the removed keyword through `**kwargs`.

Delete `SchemaMode`, `INPUT_CONTRACT_DESCRIPTIONS`, the embedded input-contract text block, `input_schema`, `presented_input_schema`, mode-specific imports, state and plumbing. Preserve the ordinary short descriptions and discoverability instructions. `Enum` remains where needed for the independent output-delivery enum.

The inliner is the only production caller of exported `map_schema_children` in the inspected population. Remove that unused transform helper, its export and transform-only tests in the coordinated cleanup after reconfirming its callers. Keep the schema-location/reference-closure APIs, compiler admission, literal-data and recursion safeguards. Structural vocabulary such as recognizing `allOf` is a separate declared helper contract: retain its conformance behavior, remove obsolete claims that the deleted MCP inliner produces it, and preserve the compiler's existing unsupported-keyword boundary. Erasing a spelling is not a reason to silently change traversal semantics.

The existing module split already fits the domain. Keep catalog projection in `mcp_catalog.py`, schema structure in Standards Contracts, immutable schema selection/paging in `contract_discovery.py`, process behavior in `mcp.py`, and normalized execution in the facade/domain. Add no module, facade hierarchy, renderer strategy, or generalized configuration object.

### Cost decision

A read-only planning experiment replaced only native catalog input schemas with exact reference-preserving closures. The focused native/on-demand authoring catalog changes from **104,285 to 108,659 JSON bytes**; application changes from **14,656 to 15,904 bytes**. The added 4,374 and 1,248 bytes are accepted design tradeoffs for deleting the recursive inliner and representation-selection mechanism. Current fixture/basic-invalid comparisons agreed across 1,040 checks; this is limited planning evidence, not implementation or client acceptance.

Measure the final candidate again using the same serializer and record each component. A difference beyond the expected projection effect needs explanation, not a weaker schema or arbitrary truncation. No token, billing or latency saving is inferred from these bytes.

## Public contracts, versions, and retained evidence

### Interface cutover

Advance `interface_schema_version` once for the breaking launch/composition contract: **42 → 43** when implementing against the inspected baseline; use the next unallocated edition if intervening work has advanced it. Update version-bearing examples and generated projections through their canonical owner. Do not renumber historical test inputs as though they were current results.

Keep `request_contract_version = 6`, `result_projection_version = 7`, handle versions, SQLite formats and the canonical schema identifier unchanged unless a separately admitted semantic change actually requires otherwise. This plan makes no such change. Package-release numbering remains the release owner's concern, not an automatic copy of the interface edition.

Let catalog digests reflect the actual new schemas/descriptions/metadata. Preserve output-schema digests and output-only invalidation. An old discovery selection whose catalog differs receives the existing typed stale-catalog result; the client rediscovers. A workflow handle does not become stale merely because a schema presentation changed. A still-running old process is replaced explicitly; no hot reload or automatic mutation retry is introduced.

### Consumer dispositions

| Consumer or material | Disposition |
| --- | --- |
| Known Codex registration, reported Codex 0.157.1 / gpt-6-astra qualification | Migrate its launch command, retain on-demand output and exercise the actual resulting client/build/surface. The reported earlier result is design evidence, not a pass of this unimplemented candidate. |
| Application-purpose clients and focused/advanced scopes | Preserve operation authorization/visibility and native discovery; verify via actual MCP processes and the applicable client path. |
| Repository Python, CLI, inventory and qualification callers | Replace signatures/configuration atomically; mode selection is removed. |
| Clients requiring compatibility input rendering | That support promise is retired by the owner. They must use native discovery or an explicitly pinned old release outside the new supported deployment; they do not justify retaining the old code. |
| Native clients selecting eager output | Continue to receive exact eager outputs; the separate output contract is unchanged. |
| Existing supported workflow records | Reopen unchanged with real baseline-produced records, current authority checks and preserved recovery behavior. |
| Historical qualification recordings and verdicts | Preserve their original bytes, version, source/catalog bindings and meaning; they are not reclassified as candidate acceptance. |

### Qualification and replay cleanup

Remove `--schema-mode` and its callable parameters from live navigation/model harnesses, inventory and trace generation. A report may continue to record the constant fact `schema_mode: "native"` for provenance; that field is not a runtime switch. Keep requested/observed client, model, exposure surface, output delivery, catalog and observer-source evidence.

In current-source replay, remove the ability to reconstruct a compatibility catalog. A compatibility recording is explicitly outside the current replay contract. A prior native recording remains eligible only when the existing exact source/catalog/observer requirements really match; native labeling alone is insufficient. Mismatched recordings receive a clear non-passing report under the existing report outcome contract, directing review to their original pinned tooling. Retain that tooling as an original release/evidence artifact if required; do not vendor an old renderer into the new runtime or silently translate old hashes.

Reuse the existing canonical `operation_output_schema` and purpose-qualified roots for private observer validation instead of building a second complete eager catalog merely to obtain result validators. Share this small derivation within the existing qualification owner where repeated. Schemas used privately by an observer are not injected into the model; the model must obtain any missing knowledge through its actual exposed tools.

## Simplicity and ownership review

**Applicability:** `applicable`. Retirement changes a public configuration/composition surface and removes permanent schema transformation machinery. The full artifact probe follows.

1. **Independent concepts and dimensions.** Contracts define what inputs/results mean; structural helpers locate schemas; catalog projection decides how a fixed contract is advertised; discovery selects complete records; the host chooses installation, purpose, operation breadth and output delivery at process startup; the domain owns evidence and workflow transitions; observers judge recorded behavior. Native input selection ceases to be an independently configurable concept.
2. **State, identity, value, time, policy and mechanism.** Canonical schema values and local reference closure are immutable inputs. Catalog identity binds discovery for a process; workflow identities bind durable state separately. The native-only support policy is fixed by this decision, not inferred from client names or time. Host output delivery remains independent. Current permission and publication state remain live domain checks, never catalog-derived grants.
3. **Caller/composition knowledge.** Callers know their purpose, permitted operations, explicit workflow contexts and optional discovery. They no longer know a renderer enum, fallback list or inline/reference size algorithm. Startup owns the compiled interface and process lifetime; catalog building remains pure. The one external change is removing the old launch argument.
4. **Representative change paths.** An input-field change touches its canonical definition/generated artifacts and affected tests, not a hand-authored renderer. A paging change stays in discovery. An output-delivery change stays in its existing catalog/startup owner. A permission or evidence change remains in its domain. No new co-change across these paths is imposed by native-only presentation.
5. **Stable interfaces versus hidden knowledge.** Boundaries exchange compiled contracts, qualified operation roots, ordinary JSON schemas and existing digests/handles. They do not share expansion-depth counters, duplicate schema text, store paths, alternate validators, or a hidden current-catalog pointer. Schema annotations/literals remain data.
6. **Independent evolution, testing, failure and replacement.** Catalog projection can be tested without Git, stores or transport. Discovery remains no-store after construction. Process/host checks test real registration separately. Retained-state tests replace the actual old producer process with the candidate. Replay source mismatch is not a production workflow failure.
7. **Deletion result.** Deleting compatibility descriptions, mode plumbing, recursive input expansion and size comparison removes their complexity instead of relocating it. Deleting structural closure would force reference logic into multiple callers, so it stays. Deleting discovery would remove necessary access to abbreviated fields, so it stays. Removing output digests would weaken invalidation, so they stay. No new permanent module, generator, registry, validator or persisted format is introduced.
8. **Necessary complexity and cumulative result.** Required complexity is canonical schema validation, purpose filtering, bounded discovery, output delivery and domain lifecycle. Optionality is retained only for those separately owned promises. Test axes lose the obsolete input-mode dimension; semantic, failure and real-consumer assertions remain. Passing tests proves the stated behavior, while this change-path/deletion review separately establishes the intended simplification.

## Allowed write set

This is an exact initial set by owner. An additional directly affected caller may be added in the ledger when it preserves the same objective/authority/risk; a new semantic owner or promise triggers re-planning.

**Runtime and contracts**

- `tools/standards_engine/standards_engine/mcp_catalog.py`
- `tools/standards_engine/standards_engine/mcp.py`
- `tools/standards_contracts/standards_contracts/schema_structure.py`
- `tools/standards_contracts/standards_contracts/__init__.py`
- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- Owner-generated `tools/standards_engine/contracts/generated/agent-tools.json` and `tools/standards_engine/standards_engine/_generated_contract.py`, only when regeneration changes them.
- `evaluation/standards-effectiveness/generated/suite-inputs.json`, regenerated after the tracked file set is final.

**Live callers, observers and tests**

- `tools/standards_engine/tests/{catalog_inventory,agent_efficiency_trace,codex_navigation_client,codex_discovery_client,replay_discovery_qualification}.py`
- `tools/standards_engine/tests/{test_schema_presentation,test_schema_locations,test_mcp,test_efficiency_trace,test_discovered_workflow,test_agent_input_feedback,test_agent_interaction_transport,test_input_discovery,test_output_delivery,test_catalog_inventory,test_model_discovery_qualification,test_replay_discovery_qualification,test_replay_discovery_workflow,test_generated_contract,test_runtime_identity,test_consumer_publication,test_purpose_transport}.py`
- `tools/standards_contracts/tests/{test_schema_structure,test_schema_locations,test_compiler}.py`
- Existing `.agents/skills/standards-engine/scripts/invoke.py` only if consumer checks demonstrate an affected assumption; its observer currently relies on the catalog builder's defaults rather than an explicit input-mode argument.

**Documentation and operational cutover**

- `tools/standards_engine/{README.md,PURPOSE-SEPARATION.md}`
- `tools/standards_contracts/README.md`
- `.agents/skills/standards-engine/{SKILL.md,references/environment.md}`
- `tools/standards_engine/tests/INPUT-DISCOVERY-QUALIFICATION.md`
- `docs/plans/README.md` and this plan's directory.
- Scoped supersession notices, only where a still-active input-presentation decision needs one: `docs/plans/{agent-interface-efficiency,schema-projection-cleanup,input-contract-discovery,agent-interaction-quality,output-contract-delivery}/plan.md`. Keep original measurements/verdicts and unrelated parent objectives intact.
- Operator-owned `/home/jeremy/.codex/config.toml`: only the confirmed Coding-Standards registration's obsolete argument pair, as a separate deployed change, never as a whole-file replacement in the source ZIP.

`tools.py`, `context_projection.py`, `contract_discovery.py`, `runtime_identity.py`, native evidence/workflow/store implementations, canonical schema definitions and dependency locks are read-only design dependencies unless an independently demonstrated in-scope need is recorded. Their inspection is not a reason to rewrite them.

## Milestones

### N1 — Native-only implementation and repository consumers

**Status:** `Implemented`
**Goal:** A coherent candidate has exactly one input presentation and no live input-mode selection.
**Write set:** Runtime/contracts/callers/tests/docs above; no deployed host or production store changes.

1. Check status, integrated baseline, existing plan lifecycle and actual mode callers. Record unrelated work and leave it outside staging. Preserve original qualification artifacts and baseline source needed for retained-state tests. Confirm the inliner/mapper caller disposition with a bounded repository search.
2. Add focused removal and semantic regression assertions before or with the change. Preserve a baseline native catalog and real baseline-produced workflow records; old-code evidence is kept outside the new production import path.
3. Apply D1–D3 together: remove mode and fallback code, use reference closure, remove the orphan transform helper, and update all direct consumers. Keep output delivery independent and validation unchanged.
4. Repair tests/observers at their real owners: remove input-mode loops and compatibility-positive assertions; preserve payload, scope, chronology, evidence and failure tests. Derive private output validators from canonical roots. Make historical replay's supported source boundary explicit.
5. Update interface metadata and examples; run the existing projection owner, not hand-edits to generated models. Refresh the suite-input manifest only after the intended tracked additions/deletions and source are present. Update current guidance and scoped supersession links together.
6. Run the focused checks, complete affected Engine/Contracts suites, existing locked CI checkpoint, reference/size inventory, cold-process discovery and retained-state cases. Record exact failed and rerun evidence without relabeling earlier failures.

**Gate:** A1–A7 satisfied in their named environments; candidate marked `Implemented` or `Verifying`, not Accepted. Failure of an ordinary regression is repaired within N1. Actual new authority/persistence/client-contract requirements trigger re-planning.

### N2 — Installed qualification and accepted cutover

**Status:** `Planned`
**Goal:** The real supported registration runs the candidate without the obsolete option and preserves the agent's successful workflow.
**Write set:** Operator registration, acceptance records and material fixes remaining within N1's scope; no production standards mutation.

1. Obtain independent review of the material candidate and its deletion/consumer map, including the test oracle changes. Disposition findings before accepted integration; a new material change receives proportionate re-review.
2. Perform the cutover runbook below. Capture the observed current process/interface/catalog rather than inferring success from a file on disk.
3. In a fresh client context, exercise actual discovery/navigation and a disposable, evidence-backed model-authored proposal through readiness using native/on-demand. Independently read back the intended changes and unchanged accepted ref. The observer credits exact definitions discovered earlier through any operation in the same verified context. Stop at readiness.
4. Finalize A8–A9, preservation and packaging records. Mark this plan `Accepted`, acceptance `satisfied`, next slice `none` only after every required claim passes. Preserve genuinely outstanding items with owner and scope instead of claiming completion.

This split exists because host configuration and real model evidence have an independent deployment boundary. It does not prescribe separate commits or a fixed commit topology.

## Objective acceptance and evidence oracles

A1–A6 have local representative evidence. A7–A9 retain the explicit environment, host and review limitations in [verification](reports/verification.md). Earlier user reports remain design evidence, not candidate acceptance.

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence owner / planned record |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | No supported live input compatibility path, enum, keyword, option, embedded schema fallback or positive compatibility test remains. Ordinary native startup succeeds; both old flag values and removed Python keyword fail at their correct boundary before store work. | contract | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A2 | Every published input retains exact supported semantics and reference closure. Valid/invalid inputs, literals, annotations, recursion, constraints and purpose visibility remain correct against the canonical schema and independent Draft 2020-12 validator. | contract | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A3 | Both discovery operations remain usable, bounded, deterministic, no-store and scoped. Exact output-schema digests, output-only invalidation, stale/off-purpose rejection and eager/on-demand behavior are preserved. | integration | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A4 | Actual fresh MCP processes route, paginate, read, discover/traverse relationships and reject malformed authoring with useful fields and zero created drafts. | system | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A5 | Records produced by the real supported baseline process reopen under the candidate: snapshots, proposal/Analysis/readiness and recovery observations retain meaning; current evidence checks remain active and no accepted ref advances. | system | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A6 | Native qualification traces credit prior exact cross-operation discovery; missing/late/altered/foreign definitions still fail. Historical source mismatch produces an explicit non-pass while original files/verdicts remain unchanged. | integration | representative | automated | satisfied | [Local evidence and remaining gates](reports/verification.md) |
| A7 | Final generated projections, complete affected suites and locked structural checkpoint pass; catalog cost and deletion/change-path review match the admitted composition. | integration | representative | either | blocked | [Local evidence and remaining gates](reports/verification.md) |
| A8 | Saved production registration and the actual restarted agent connection match the candidate catalog with no `--schema-mode`. A fresh isolated model uses discovery as needed to propose, revise, decide singly/in batch and review to independently verified readiness, without schema-repair loops or publication. | user-workflow | required-real | either | blocked | [Local evidence and remaining gates](reports/verification.md) |
| A9 | Independent material review is dispositioned, unrelated work/data and original evidence are preserved, source package reconstructs exactly including deletions, and deployment/acceptance records identify the actual accepted artifact. | release-artifact | representative | either | blocked | [Local evidence and remaining gates](reports/verification.md) |

**Deciding oracles.** Use canonical definitions plus `jsonschema.Draft202012Validator` for admitted-schema semantics; real JSON-RPC/server execution for transport; real old/new process and Git/store adapters for retention; chronological events, actual arguments/results, independently read content and unchanged refs for model workflow; and base reconstruction/file hashes/modes for delivery. Byte counting decides only byte counts. Generated freshness does not decide semantic equivalence; the local planning substitution is not a real client test.

**Required negative cases.** From otherwise valid fixtures, introduce one failing condition: removed flag/keyword; missing required field; unsupported schema keyword/reference; literal `$ref` data; closed-object extra field; wrong discriminant; stale catalog; foreign purpose/selector; output-only schema change; tampered evidence or foreign work; missing/late discovery; incomplete or mismatched original recording. Assert the intended field/diagnostic and absence of effects, rather than any generic exception.

**Verification economy.** Retire compatibility-positive cases and duplicate input-mode matrix axes, not independent invariants. Reuse the existing harnesses and CI; no new test runner or benchmark framework. A fresh client run is justified by the new reference-only projection and changed launch contract. It does not require production publication or re-proving unrelated Engine subsystems through paid model turns.

The supported locked environment remains CPython 3.11/3.12 with hash-enforced `tools/standards_contracts/requirements.lock`; existing CI uses Python 3.12. Keep that lock unchanged. Local planning used Python 3.13.5 and rpds-py 2026.5.1; those measurements are not supported-runtime qualification. Gate inability affects its claim, not unrelated safe implementation.

The existing commands remain the basis for execution:

```sh
# Use the supported, explicitly selected locked interpreter as "$python".
PYTHONPATH=. "$python" -m tools.standards_contracts.standards_contracts.projection --check
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_contracts/tests
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_engine/tests
PYTHONPATH=.:tools/standards_verifier "$python" tools/standards_verifier/verify.py --complete
```

Run the unchanged broader CI package commands as required by the repository; keep any sharding file-disjoint, with the candidate held stable and all failures/reruns identified. Regeneration uses the same projection module without `--check`; manifest refresh uses the existing Engine verification-input owner.

## Operator cutover runbook

1. Identify the actual affected registration and preserve the exact previous command/configuration as an operator-owned rollback reference. Inspect pending production work; publication/recovery in flight must be settled or explicitly quiesced by its owner before process replacement. This authorizes no cancellation, store deletion or lock removal.
2. Stage the candidate code and generated files coherently. In `/home/jeremy/.codex/config.toml`, remove only the `--schema-mode`, `native` pair from the Coding-Standards command. A still-configured `compatibility` pair is likewise removed, not translated into a fallback. Preserve command path, interpreter, environment, repository, purpose, `--advanced` choice and unrelated registrations.
3. Keep `--output-schemas on-demand` for this deployment. The example argument fragment is now `--purpose authoring --output-schemas on-demand`; an application registration keeps its application purpose instead. No new native-only flag replaces the removed one.
4. Restart the relevant server through the host's normal mechanism and reconnect/refresh clients. Query `runtime_info`; require current installation, the candidate interface edition and expected actual catalog digest. Observe the saved command and the connection that the agent actually uses, not merely a separate test process.
5. Run navigation/discovery/rejection smoke checks and N2's isolated model path. Keep production files/ref/store unchanged by these tests. Treat legitimate unresolved facts as unknown; discovery is needed when knowledge is missing, not on every action.
6. On startup failure, retain diagnostic evidence, stop attempted use and repair the configuration or restore the exact previous code **and** its corresponding launch arguments under operator control. Preserve all stores and submitted work. Observe unknown mutation outcomes with retained contexts; never infer a retry from elapsed time. This plan's no-store-migration contract permits code/config rollback, but an intervening data-format change requires its own reviewed disposition.

## Documentation, packaging, and completion

Put the lasting native-only operator contract and removal instructions in the existing Engine/environment owners. Link current plans to the scoped supersession rather than repeating conflicting defaults. Keep terminal historical reports and original qualification verdicts unchanged; they are evidence of their original source, not current deployment instructions. Leave the Standards Library Effectiveness parent effort and its acceptance unrelated.

Deliver a patch against the actual selected integrated baseline, complete changed files, an explicit deletion list, hashes/modes, commands/results, and the updated plan/ledger/issues/reports. Reconstruct in a fresh checkout to prove copying will not leave obsolete runtime code. External user configuration is documented as a narrow operator change and is not bundled wholesale. No blanket `git add -A`, archive replacement, history rewrite or automatic remote publication is implied.

## Blockers, assumptions, and re-plan triggers

**Source implementation is complete.** The verified interface-42 delivery was reconstructed and identified in the ledger; patch base checks protect later integration differences. Supported-runtime CI, actual host access/model qualification and independent review block acceptance of their named claims, not removal of the retired compatibility promise.

Assumptions: the reported native/discovery deployment is the supported host for this cutover; the inspected mode/mapper caller population is complete within the repository; contract/store semantics remain unchanged; the shared structural closure supports the selected native schemas. Owners and stopping conditions are respectively the operator's observed registration, the bounded source/caller audit, canonical/retained-state comparison, and schema plus fresh-client checks. Evidence that disproves an assumption is recorded before expanding the affected work.

Re-plan only when new facts alter scope, authority, consumer promises, ownership, retained-data risk or acceptance meaning—for example, a real independent library consumer requires the mapper being removed, reference-only input cannot be discovered on the supported host, an intervening revision changes persistence, or maintaining this design requires a new renderer/registry. Ordinary affected call sites, imports, test expectations and stale generated files are repaired inside N1 and recorded. A request to retire eager output is a separate explicit contract decision, not an inferred part of native input removal.

Use serial integration for this small cross-cutting contract change. A review branch/worktree is appropriate to isolate the material candidate from unrelated user work; the implementer/integrator owns it, targets the repository's accepted integration branch, and retains it through review. The plan grants no deletion of user resources. Existing Commit rules govern its final safe integration/retention and any explicitly authorized cleanup.

**Final acceptance:** blocked on A7–A9; source implementation completed. **Deferred work:** eager-output retirement/default changes and any unrelated schema-size optimization. **Terminal state after successful completion:** `Accepted`, acceptance `satisfied`, next slice `none`.
