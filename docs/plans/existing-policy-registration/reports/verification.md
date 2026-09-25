# Existing-Policy Registration — Implementation And Verification

**Source implementation:** delivered.
**Objective acceptance:** blocked on complete-checkout and installed-boundary evidence.
**Date:** September 24, 2026.
**Upstream baseline:** `5a9dcb08effda50a485e6ae08d9fe4c349c74eda`, branch `implementation/purpose-separated-standards-engine`.

## Full-checkout integration qualification

The delivered patch was applied to the complete local checkout on the same implementation branch. The archive integrity and patch hash matched its manifest, `git apply --check` succeeded, and only the declared patch files were staged. A Python 3.12.3 environment with the repository's locked contract dependencies ran the new contract tests (8 passed), the new full-compiler registration tests (14 passed), and the focused logical-authoring (31), metadata (43), policy-impact (10), contracts (52), and analysis (114) suites successfully. Canonical public-contract projection freshness passed.

The temporary-store repository verification refreshed the tracked `suite-inputs.json` through its owner and passed 73 suites and 121 structural checks. The manifest diff contains the expected changed contract/source digests and repository-index digest. A precommit run of the full Engine suite passed 280 of 281 tests. Its sole failure was `test_main_advancement_and_cold_historical_read_use_exact_captures`: that fixture clones committed `HEAD`, then copies the new contract files from the working tree, leaving the clone's committed verification manifest stale. Recheck this case after committing the candidate, as the package's application instructions require.

The official MCP SDK client walkthrough has not run in this checkout. The available Python environments do not contain the `mcp` client package, and a download attempt failed DNS resolution. This qualification has not opened the installed proposal store or published real standards content.

## Implemented behavior

The current logical-edit contract includes `register-policy-unit`. It accepts an existing canonical standard ID and the existing `NewPolicyUnit` declaration. The parser freezes the declaration into the normal logical-edit representation and uses the policy identity as its conflict facet.

The compiler performs module and existing-policy edits before a grouped registration phase, then resolves consumer relationships and final supporting content. It uses the existing sidecar renderer, registry writer and canonical corpus validator. Existing module bytes are untouched by registration alone. Registered sidecars with only tombstones are reusable without deleting their retired records. New primary identities and aliases cannot claim a canonical module identity; existing policy/tombstone reservations and the canonical validator remain authoritative.

New identities enter semantic analysis as additions at revision one, with explicit intent and the containing module selected for analysis. Coverage is not automatically certified. Existing proposal storage, immutable snapshots, publication, purpose filtering and full/incremental replay mechanisms remain the owners of their current guarantees.

Interface edition 33 replaces edition 32 for discovery of the expanded edit vocabulary. Analysis request 6 and result/state 7 remain unchanged. No alternate decoder, compatibility shim, database reset or persisted-format conversion was added. The current generated Python and tool schemas were produced by the existing contract compiler.

Technical authoring documentation and the guide's H0 handoff now explicitly include registration within existing modules. The rest of the standards-content migration remains separate. This source package does not certify H0: actual consumer qualification below is still required.

## Source and environment boundary

Direct repository download was unavailable. Source was reconstructed from existing delivery archives and a small number of retrieved baseline files. Before editing, each of the nine existing files included in the patch was checked against its published Git blob identity at the baseline. All matched. New files are the plan/evidence and feature tests. No recovered dependency file is distributed as a feature change.

The reconstruction is **not a complete Git checkout**. It lacks the graph engine and other unchanged packages required to import the Standards Engine. The available interpreter is Python 3.13.5, outside the repository's supported locked 3.11/3.12 qualification environment. The actual installed MCP server and user proposal database are not accessible here.

The blocked proposal `503f233b-5c9f-442f-a04f-99f330142bae` was never opened, edited, published or reset. No real normative body, policy-unit declaration, consumer relationship or application exposure approval was changed. No upstream commit or push is claimed.

## Executed evidence

| Observation | Result | Proof boundary |
| --- | --- | --- |
| Baseline JSON Schema validation of the proposed new edit, before production edits | Rejected as unsupported by the existing `StandardEdit` union | Reproduces the missing public contract; not an MCP process test. |
| Existing contract/compiler suites available in the recovered source | 14 tests passed | Canonical schema compilation, validation and projection behavior. This is the available subset, not a claim about every upstream test. |
| New `test_registration_contract.py` | 8 tests passed | Proposal reachability, generated model ownership/roundtrip, required/closed fields, revision and scope constraints, authored examples and projection freshness. |
| Existing canonical projection generator and `--check` | Passed | Both generated artifacts agree with their source schema/interface. Baseline generation also reproduced both original generated files exactly. |
| Isolated owner-mechanism probe | 9 checks passed | Selected real function bodies exercise registration staging, sidecar reuse/tombstones, reservation checks, ordering and error propagation. Metadata compilation and transport are explicitly substituted or excluded. |
| Python compilation and supported-grammar parsing | Passed for changed Python files | Syntax only; imports and supported-environment execution remain separate. |
| Full registration integration suite invocation | Blocked during import: `ModuleNotFoundError: No module named 'tools.graph_engine'` | No canonical metadata/compiler integration test ran. The collection error is not a test pass. |
| Base-file Git identities | All nine existing patch inputs match the published baseline | Exact changed-file provenance, not completeness of the recovered repository. |
| Patch round trip, changed-file hashes and ZIP integrity | Passed | A disposable index of the exact baseline inputs accepts the patch and reproduces every packaged replacement/addition. |

The isolated probe lives in the delivery's `verification/` area rather than the repository's test discovery. It extracts selected function bodies from the actual source and supplies a bounded model at missing imports. It is retained to make the experiment inspectable. It neither reimplements nor verifies the canonical metadata validator, graph, manifest generator, analysis, storage, MCP or full logical compiler. Its nine observations are not added to a claim that the full Engine suite passed.

Executed commands used the available interpreter and recovered source:

```bash
PYTHONPATH=. python -m unittest discover -s tools/standards_contracts/tests
PYTHONPATH=. python -m unittest discover -s tools/standards_engine/tests -p test_registration_contract.py -v
PYTHONPATH=. python -m tools.standards_contracts.standards_contracts.projection --check
python isolated_registration_probe.py /path/to/recovered/source
```

Raw outputs, baseline rejection, and the one-off probe are included in the ZIP's `verification/` directory. The full-checkout attempt is retained separately from successful logs.

## Supplied but unexecuted acceptance coverage

`test_policy_registration.py` contains fourteen integration cases using the existing real compiler/capture fixture. It starts from an already-created module so registration is actually against existing authority. It covers empty and populated policy mappings, unchanged prose/aliases, multiple registrations, same-candidate rewrite and relationships/provenance, tombstone-only owners, unavailable/reserved identities, scope/alias/lineage rejection, failed candidate isolation, mutation resistance and full/incremental replay equivalence.

`mcp_policy_registration_client.py` extends the existing official SDK qualification approach. It creates and publishes synthetic owners in a disposable repository, registers a policy in an accepted previously unmapped owner, resumes that pending workflow after process replacement, then registers another scope alongside a rewrite, consumer relationship and provenance. It includes explicit fixture coverage/consumer/impact decisions, reviewed publication, a rejected successor preserving its predecessor, cold historical/current readback and application-purpose rationale isolation. The harness has no option for selecting the user's real repository/store as its mutation target.

Neither file has been runtime-qualified in this environment. Their Python syntax is checked. Run them with the full source and supported environments before claiming the blocker resolved end to end. A future failure requires an ordinary bounded repair; a syntax pass is not a substitute for that execution.

## Generated verification inputs

The repository's complete `suite-inputs.json` manifest was deliberately **not** regenerated from a partial tree or manually edited. The schema's generated Python and tool definitions are included and current. The full verification-input manifest must be regenerated through its existing owner in the complete checkout, after adding these new files to its tracked membership. The package's application instructions show a temporary-store native invocation so this does not require opening the preserved production proposal store.

The complete structural checkpoint, full package suites, official MCP walkthrough, installed Codex catalog and any independent external code review remain outstanding. This report is an implementation/self-review record, not independent acceptance.

## Material self-review

The source diff was reviewed for one semantic owner per concern, explicit canonical identity rather than paths, absence of Core-specific branches, immutable program payloads, deterministic group staging, reserved identities, preservation of existing declarations, one-source generated contracts, original-base semantic intent and absence of new persistence authority. The sidecar reuse repair was kept inside the existing helper because both registration and existing movement use its owner contract.

The added public operation is intentionally a logical edit within `propose`/`revise`, not a new MCP tool or a general file-edit escape path. The unchanged Codex catalog harness discovers edit variants from the canonical union, so no hard-coded variant-count patch is necessary. The new handoff requirement asks for the actual existing-owner transition, not merely successful creation of a new standard containing initial policies.

## Integration and resume boundary

Apply the patch to a reviewed local code branch, refresh the verification-input projection with a temporary verification store, and run the supplied full-checkout tests. Commit the candidate before the SDK walkthrough clones it. Integrate the qualified code using the repository's normal process, then restart the server and refresh the client catalog for interface 33.

Read the preserved proposal's actual state through supported authoring operations. `workflow_status` reconstructs its exact context; `resume` selects its explicit current revision where needed. It does not rebase the original accepted source. A changed accepted base may require the Engine's supported stale-state disposition or a new proposal carrying the preserved draft/evidence against current authority. Keep the original records and follow returned decisions rather than editing stored bytes.

Reanalyze the candidate containing the new registrations/relationships. The previous Core wording review remains useful historical evidence; it is not automatic readiness for a changed candidate. Resume standards publication only after the missing handoff claim is actually satisfied.
