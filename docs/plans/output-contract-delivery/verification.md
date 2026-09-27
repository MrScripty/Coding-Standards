# Output-contract delivery verification

**Status: Verifying; acceptance pending.** Base: `52b122683faf05ef85c86c6903a61d54870a9be4`.
The implemented Engine interface is **42**. Supported-runtime CI for this exact diff,
actual configured-client/model qualification and independent review remain separate.

## Outcome and architecture

`describe_output` exposes the exact purpose-qualified result algebra and its reachable
schema definitions as bounded, catalog-bound tool-result data. Clients begin with an
operation name and may retrieve the complete closure or select a referenced definition.
It shares immutable schema selection, traversal and pagination with `describe_input` in
`contract_discovery.py`. The old internal `input_discovery.py` module is replaced, not
retained as a parallel implementation. Public input-discovery shapes are unchanged.

The MCP startup choice `--output-schemas eager|on-demand` is independent of input schema
presentation. **Eager remains the default.** It advertises complete output schemas for
existing consumers; all prior eager tool entries are unchanged. On-demand omits the
optional MCP `outputSchema` entirely, rather than claiming a permissive schema is an
exact replacement. A per-tool output-schema digest in `_meta` binds the omitted contract
into the existing catalog identity, so output-only changes cannot reuse stale discovery
selections. Equal workflow output algebras share the same schema digest, not permissions.

Domain results, structuredContent, matching JSON TextContent, validation, authorization,
evidence normalization, atomic decisions, current readiness and publication/recovery
checks use their existing owners. No result fields are removed or summarized. No model
prompt, policy text, routing-fact truth value, persisted handle or store format changes.
There is no new schema registry, client cache, mutable session, validator or background
operation. Clients decide when they need exact output contracts; ordinary result handling
does not require an additional discovery call after every action.

Output discovery returns the exact root JSON, result-root names, full-schema digest,
dialect and schema records. Reconstruct the schema by parsing the root and setting its
`$defs` from all unselected pages. Selected pages cover only the selected definition's
closure and are not claimed to be a complete result validator. The digest uses sorted
keys, ASCII JSON escaping and compact separators in UTF-8, without injecting a `$schema`
field. The separately returned dialect identifies Draft 2020-12. This schema covers the
structured domain result, not MCP's outer CallToolResult wrapper.

Pages default to eight whole records, allow at most sixteen, and are limited to 16 KiB
of complete domain-result JSON. Byte pressure returns fewer records; an oversized first
record returns a typed limit rejection. Expected catalog identity is required for a
selected definition or nonzero offset. Source, purpose, operation scope, recursion and
literal schema data remain under the existing contract/traversal owners.

## Standards and scope

The executable Router was run with explicit repository/task facts and returned no
unresolved conditions. Its route and exact readback are included in delivery evidence.
The selected guidance covers implementation, verification, proportionality, planning,
documentation, build, library, generated contracts, IPC, architecture, contracts,
security, diagnostics, dependencies, performance, replay, schema evolution, protocols
and independent oracles. The plan records ownership, composed-design decisions and the
write set. No normative policy, approval, provenance, dependency lock, production store,
unrelated user ZIP or remote ref was modified.

The only scope expansion was repair of a directly affected test-fixture helper. A
HEAD-based disposable clone retained files deleted from the current tracked candidate.
Removing the old input-discovery module exposed that error as a correct projection
integrity rejection. The helper now removes only obsolete tracked paths in its own
clone before overlaying current files. A real Git regression checks additions, deletion,
modified tracked bytes and preservation/exclusion of unrelated source work. Production
integrity checks remain unchanged.

## Automated evidence

| Check | Observed result |
| --- | --- |
| Complete Engine campaign, four file-disjoint shards | **506 passed; no failures or skips** |
| Newly added regression methods | **18; included in the 506** |
| Final focused rerun after report/manifest finalization | **51 passed; included in the 506** |
| Contracts/compiler package | **69 passed; one supported-environment check skipped** |
| Metadata / policy-impact / Analysis / verifier | **43 / 10 / 121 / 168 passed (342 total)** |
| Graph package | **37 passed** |
| Source/generated-contract freshness and diff checks | Passed |
| Registered structural checkpoint | 121 checks across 73 suites passed |
| Actual 41-to-42 cold retained-state observation | Passed in eager and on-demand delivery |
| Direct facade and CLI output observation | Passed; purpose exclusion preserved |

Engine shard counts are 147, 130, 105 and 124. `DELIVERY/evidence/test-summary.json`
records all 506 distinct observed test IDs. No earlier failed or stopped run is
included in that total. The package reconstruction record separately names the
verified file/hash/mode count and deletion. Final post-report check results are
recorded in `DELIVERY/evidence/final-checks.json`.

The final complete Engine campaign uses four file-disjoint module selections. Initial
failed/aborted investigations are preserved separately and are not counted as successful
final tests. The first output-test attempt used an incorrect compiler fixture argument;
that fixture was repaired before the successful focused run. The first broad campaign
was stopped after establishing the disposable-clone deletion defect, then restarted
against the coordinated source and generated manifest. The final runtime and test source
was held fixed for the restarted campaign; documentation and final verification hashes
were finalized afterward and checked separately.

The output tests reconstruct every published result algebra for both purposes, both
input-schema modes and both output-delivery choices, including the advanced operation
surface. Independent Draft 2020-12 validation covers real examples and invalid values.
Tests exercise whole-record limits, selectors, unknown/off-purpose operations, stale
catalogs, output-only changes, equivalent shared workflow digests, missing/equal numeric
representations, no store/filesystem access after construction, and cold continuations.

A native/on-demand discovered workflow replaces the actual MCP stdio process for every
call through proposal, successor revision, single decision, decision batch and review.
It retrieves the shared output contract once, validates real structured outcomes, checks
shared/inline evidence equivalence and leaves the fixture's accepted main unchanged.
Other mode/delivery combinations exercise the same actual Engine through in-process MCP
dispatch. Separate cold stdio checks compare eager and on-demand navigation, exact
policy reads, unresolved facts and invalid-input/relationship feedback for both purposes.

Observer tests use synthetic client events. Real Engine results are also recorded into
a synthetic client trace and replayed through a fresh process in both delivery choices.
These are observer/integration tests, **not an actual Codex or model execution**.

## Retained-state evidence

An actual interface-41 process from the untouched baseline created a proposal, Analysis
and readiness in a disposable repository. After changing only the fixture's installed
contract inputs, replacement interface-42 processes observed those same records under
both eager and on-demand delivery. Analysis/status, readiness/status, repeated review
and exact proposal readback matched; the accepted ref did not move. No migration,
publication, store reset or new authoring request was needed. The source script and
asserted results are retained with the evidence.

The canonical comparison establishes **322 unchanged previous schema definitions** and
unchanged prior operation declarations. Four output-discovery definitions and one public
operation were added. Analysis request/state, SQLite, snapshot, proposal, readiness and
recovery contracts remain intact. Interface 42 versions the additive observer and catalog
configuration, not persisted state.

## Catalog measurements

Complete focused tool-array JSON, measured with the same serializer and including tool
metadata and descriptions:

| Purpose/input mode | Baseline eager bytes | Updated eager bytes | Updated on-demand bytes |
| --- | ---: | ---: | ---: |
| Authoring/native | 702,074 | 708,288 | 104,285 |
| Authoring/compatibility | 807,727 | 813,941 | 209,938 |
| Application/either | 76,052 | 82,266 | 14,656 |

The new catalogs contain 23 focused authoring tools or ten application tools. Relative
to the actual native baseline, on-demand delivery reduces authoring catalog JSON by
**597,789 bytes / 85.15%** and application JSON by **61,396 bytes / 80.73%**. The eager
catalog grows by 6,214 bytes to describe the added tool; omission is opt-in, not a claimed
default size improvement. Current on-demand digest metadata totals 2,668 JSON bytes for
authoring and 1,160 for application and is included in the totals above.

Whole-schema discovery can cost more than a single eagerly embedded schema because the
records are paginated and escaped as result data. With limit 16, the complete shared
workflow result algebra has 92 definitions and takes six pages (46,701 domain-result
JSON bytes for propose). It can be reused for the other operations sharing that exact
digest. A selected WorkflowAnalysisSummary closure takes one page and 2,179 bytes;
ReadinessHandle takes one page and 996 bytes. No per-action rediscovery is prescribed.

These are raw serialized catalog/result measurements, **not billed tokens, final
model-visible declaration sizes, client startup latency, server CPU savings or general
reliability claims**. Matching structuredContent/TextContent remains, so MCP envelope
bytes and host rendering are separate measurements. The reported prior 77,000-character
host view was not supplied as an actual export and is not relabeled by these numbers.

## Actual-host qualification and deployment

The existing configured-client harness accepts `--output-schemas on-demand`, checks
absence rather than a permissive output schema, reconstructs the read-result contract,
and validates results independently against canonical schemas. The opt-in actual-model
harness configures its disposable server for the selected delivery and records that
choice. Its observer uses exact validation schemas that are **not supplied to the
model or advertised catalog out of band**. Optional describe_output calls are checked;
shared exact definitions may be reused chronologically within the verified session.

The model harness records `host-catalog.json` separately. That is an inventory, not a
captured model prompt/declaration. The harness still requires explicit model-turn
permission and verifies readiness, readback, evidence and no publication. Replay honors
the recorded delivery choice; old recordings default to eager and must match their
source/catalog. The matching-source requirement is not bypassed.

Neither configured Codex harness nor a paid model turn was executed here. Keep eager
for supported clients that require upfront schemas. Qualify the opt-in path on the actual
client/model/surface before promoting it. Measure actual rendered declarations where
the host exposes them, plus task success, repair count and discovery calls. Those
checks cannot be replaced by raw byte accounting or a synthetic trace.

Local environment: CPython 3.13.5, Linux x86-64, jsonschema 4.26.0, rpds-py 2026.5.1.
The repository's supported locked environment is Python 3.11/3.12 with rpds-py 2026.6.3;
the lock was not changed. Baseline CI run 36288832601 passed but does not qualify this
new diff. Run the existing locked CI and obtain independent review before acceptance.

## Integration

Apply the complete base-pinned patch from DELIVERY/README.md, including deletion of the
old internal discovery module and addition of its shared replacement. Overlaying files
alone does not remove obsolete code. Stage only the delivered paths and preserve
unrelated work. Restart the MCP server and refresh/reconnect clients for interface 42.
For the smaller candidate catalog use `--schema-mode native --output-schemas on-demand`.
Omission of the output option keeps eager behavior; input compatibility remains available.
Preserve all installed stores and workflow handles. No remote operation was performed.
