# Native-only MCP implementation verification

**Status: Verifying. Source implementation is complete; acceptance is blocked only
by the named supported-environment, actual-host and independent-review evidence.**
Engine interface: **43**. Observer edition: **3**.

## Baseline and admission

The selected plan is `docs/plans/native-only-mcp/plan.md`; the user authorized its
implementation. The connector returned upstream
`52b122683faf05ef85c86c6903a61d54870a9be4` (interface 41). Direct Git network access
was unavailable. The implementation therefore reconstructed the already delivered,
verified interface-42 output-contract package against that source, checking all
40 changed/deleted paths against its manifest. Its archive SHA-256 is
`6b6b8ffe62c139a889315f6e31f8f1bf078230917c94af9df82ae27632198f8e`; the reconstructed
tree is `de9e4cf6f89f9d2c5200d175d53671855e7a8549`. The local qualification commit
`086260d9ca1230a8bcb6be2a398a5a6a79228dfc` is not claimed as an upstream commit.

The incremental patch is against those interface-42 bytes, not against interface
41 alone. Per-file base hashes protect later integration work. A mismatch requires
reconciliation; this execution did not access or replace the user's checkout.
The executable Router selected 26 applicable standards with zero unknown task
facts. Exact route/readback is retained in delivery evidence. Normative policy,
approval/provenance, dependency pins, user ZIPs and remote refs were outside scope.

## Implemented architecture

`mcp_catalog.py` now applies the existing `schema_closure` directly to each
purpose-qualified operation's input definition. There is no input-presentation
enum, argument, CLI option, recursive inliner, size-based selection, fallback list,
embedded input schema description, or replacement no-op alias. The orphaned
`map_schema_children` helper and its export are removed. Structural schema
locations, reference closure, literal-data and recursion semantics remain with
Standards Contracts; no new evaluator or projection framework was added.

Catalog and startup APIs retain only purpose, operation breadth and the independent
output-delivery choice. `OutputSchemaDelivery` and `--output-schemas eager|on-demand`
are unchanged, including the eager default. The operator's existing deployment
must retain its explicit on-demand choice. Both discovery operations and all
server-side validation, structured/text results, evidence normalization, decision,
review, publication and recovery owners remain unchanged.

Live repository consumers no longer pass or select an input mode. Qualification
reports may record the constant native provenance. The native-only replayer
rejects retired/missing presentation provenance before loading an installation,
and retains exact source/catalog/chronology checks for native records. Original
recordings and verdicts are not modified or relabeled. Private observer output
validators now come directly from canonical result roots through the existing
observer owner, rather than constructing another complete eager catalog.

No new production module, registry, cache, renderer strategy, mutable session or
persisted representation was introduced. Across the four runtime/contract Python
files, the change removes four functions (including the nested expansion function),
one enum and a net 95 source lines. Those counts are supporting inventory, not the
architectural proof: callers no longer carry a retired presentation decision,
and deleted transformation complexity is not relocated elsewhere.

## Automated evidence

| Check | Observation |
| --- | --- |
| Complete Engine selection | 511 distinct methods in four file-disjoint shards; 510 passed initially and one stale trace-dimension assertion failed |
| Final affected-consumer rerun | 108 passed, including the corrected real cold-stdio trace and current-example assertions |
| Reconciled Engine coverage | All 511 current method IDs have observed passing evidence; no remaining failed method |
| Contracts/compiler, final rerun | 69 passed; one supported-environment check skipped (70 run) |
| Metadata / policy-impact / Analysis / verifier | 43 / 10 / 121 / 168 passed, 342 total |
| Graph package | 37 passed |
| Structural checkpoint | 121 checks across 73 suites passed; final post-report result is recorded in delivery evidence |
| Generated-contract freshness, syntax and diff checks | Passed; final post-report check results are in delivery evidence |
| Actual 42-to-43 cold retained-state checks | Exact snapshot reads, Analysis/status, readiness/review, proposal readback and recovery observation preserved in both output-delivery choices |

`DELIVERY/evidence/test-summary.json` maps every current Engine method to its
passing log. This is complete-selection coverage plus the final focused rerun,
**not** a claim of one uninterrupted all-green full-suite execution. The four
full-selection counts were 148, 134, 105 and 124. The initial 134-method shard
contained the one failure; its exact log is retained.

Before implementation the three new removal-boundary tests failed against the
old behavior as intended. An early 90-method candidate selection exposed two
outdated consumer expectations (catalog dimensions and observer edition); they
were repaired at their owners. The complete campaign then exposed the related
`test_efficiency_trace.py` count: two purposes were still multiplied by the removed
mode dimension. The trace itself had completed; its assertion now checks the two
actual purposes and one evidence workflow while retaining content, authority,
shared-reference, cold-readback, byte-comparison and no-publication assertions.
No production fallback or weakened validator was introduced for these repairs.

Final review also aligned two current authored discovery-result examples from
historical interface labels 40/42 to 43 and added an assertion for current-example
consistency. Historical test inputs and recordings were preserved. Runtime code
and canonical schema definitions remained fixed after the initial implementation;
the final rerun covers the consumer/metadata repairs. Five added test methods cover
retired arguments/exports, canonical private validators and retired replay admission;
existing semantic and failure cases remain after removal of redundant mode axes.

## Deciding boundary checks

Removed Python keywords raise `TypeError` before installation loading. The server,
inventory and both Codex harness CLIs reject both former values and both flag
spellings before creating fixture/store paths. No compatible alias remains.
Published schemas are compared with canonical contracts and the independent
Draft 2020-12 validator, including missing/extra fields, discriminants, recursive
expressions, reference siblings and literal `$ref` property/const/enum/default data.
Application-purpose exclusion and focused/advanced operation scope are retained.

Existing discovery/output tests cover complete input/result reconstruction,
whole-record bounds, current catalog binding, output-only invalidation, stale and
foreign selections, private no-store observation and cold continuations. The
real discovered workflow exercised all five authoring operations through readiness;
on-demand calls use replacement stdio processes. These are deterministic fixture
calls, not an actual model session. Observer tests preserve earlier cross-operation
knowledge reuse while rejecting missing, late, altered or foreign definitions.

An actual interface-42 process produced snapshots, a proposal, Analysis and
readiness. It also admitted a second publication and encountered a test-owned
Git ref lock, leaving real recovery-required state without advancing main.
Replacement interface-43 processes reopened all of those records with equal domain
results in eager and on-demand delivery. The original lock and accepted ref were
preserved; only recovery observation was requested. Altering real fixture evidence
returned `ANALYSIS.EVIDENCE_DIGEST_MISMATCH` with `invalid`; restoring the original
bytes produced the original readiness. No migration, deletion or publication was
used to make the retention check pass.

## Contract preservation and catalog cost

All **326** prior canonical schema definitions and all **40** operation declarations
are unchanged. Generated Python models are byte-identical. Interface metadata
advances 42 to 43; request contract 6, result projection 7, schema identifiers,
handles, SQLite and workflow-state meanings do not change. Output schemas/digests,
descriptions, operation names and annotations are identical to the baseline native
entries; only the input-schema representation changes within each catalog.

| Focused catalog | Baseline native bytes | Native-only bytes | Difference |
| --- | ---: | ---: | ---: |
| Authoring / on-demand | 104,285 | 108,659 | +4,374 |
| Application / on-demand | 14,656 | 15,904 | +1,248 |
| Authoring / eager | 708,288 | 712,662 | +4,374 |
| Application / eager | 82,266 | 83,514 | +1,248 |

These totals use the same ordinary JSON serializer on complete tool arrays.
The small increase matches the approved tradeoff for deleting the inliner and
size-selection mechanism. It is not a token/billing/latency claim. The source's
23 focused authoring and ten application tools remain. Full scope/delivery
breakdowns and the deletion/protected-file inventory ship with the evidence.
85 selected normative/profile/template/reference/CI/lock files were independently
checked unchanged; fresh patch reconstruction additionally checks the complete
resulting Git tree, preserving every other baseline path.

## Acceptance and remaining evidence

A1–A6 have local representative evidence for removal, semantics, discovery,
transport, retention and observer behavior. A7 remains blocked on the supported
locked runtime/CI, despite local package and structural success. A8 remains blocked
on the actual host registration and a fresh model workflow. A9 has packaging and
implementer scope-review evidence but requires independent external material review.
The plan is Verifying with next slice N2; it is not Accepted.

Local environment: CPython 3.13.5, Linux x86-64, Git 2.47.3, jsonschema 4.26.0 and
rpds-py 2026.5.1. The supported lock requires Python 3.11/3.12 and rpds-py 2026.6.3.
Pins and CI configuration were preserved. The actual Codex executable and
`/home/jeremy/.codex/config.toml` are not present here. No host configuration edit,
paid model turn, independent external review, remote push or production standards
publication was performed. Earlier user-reported native success informs design;
it is not relabeled as a pass of this reference-only candidate.

## Integration

Use the archive's `DELIVERY/README.md`, read-only base preflight and patch rather
than overlaying a newer checkout. Stage only the delivered write set; preserve
unrelated changes. Remove the obsolete `--schema-mode` argument and its value from
the actual registration, preserve `--output-schemas on-demand`, then restart and
refresh the real agent connection. Both old flag values now correctly fail startup.
Keep every existing store and workflow handle.

Run the unchanged supported-runtime CI and obtain independent review. The existing
qualification guide describes the actual native-only host/model path: fresh
context, real fixture evidence, proposal, revision, single and batch decisions,
complete review, independent readback, and stop at readiness. Contract discovery
is available as needed and is not required before every operation.
