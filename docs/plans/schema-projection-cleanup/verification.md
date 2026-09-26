# Schema Projection Correctness and Ownership — Verification

Status: **Verifying**. The implementation is complete; configured-client and
independent-review acceptance gates remain separate. Supported-runtime local
integration results are recorded below.
Baseline: `ebf2fda1c10a69db2dcdff463a8f6a46d34ffac6`.
Interface: **39, unchanged**.

## Outcome and scope

The public catalog no longer confuses an ordinary property named `$ref` or
reference-shaped instance data with a schema reference. Compiler dependency
selection and CLI schema inspection use the same structural owner. A small pure
catalog module owns MCP tool presentation; the transport owns JSON-RPC, stdio
lifetime and framing. The facade derives its decoded type from the selected
operation contract rather than accepting an ignored caller-supplied type.

A directly related generated-Python defect was also reproduced and fixed: an
admitted field spelling such as `$ref` previously produced invalid Python source.
The compiler now preserves wire spellings through its existing field map and
escapes exceptional Python identifiers deterministically. Collisions reject
explicitly. Existing ordinary field names and current generated artifacts remain
unchanged.

No dependency, canonical schema, policy, approval, provenance, persisted format,
state-handle version or authorization change is included. Existing agent evidence
variants and their normalization into native requests remain active capabilities.
Compatibility is retained as the default, with native mode and its existing
smaller-complete-representation selection also unchanged. Removing the workaround
or switching to reference-only presentation requires actual host-client evidence.

## Standards and ownership

Core and Router were read from the pinned source. The executable Router was run
with explicit facts, selected 24 applicable modules and reported zero unresolved
conditions. The implementation followed the selected implementation, verification,
contracts, generated-contract, IPC, code-design, library and related guidance.
The write set and directly related field-name finding were recorded before repair.

`standards_contracts.schema_structure` owns locations and same-resource reference
closure for the admitted profile. The compiler still owns closed-profile admission;
jsonschema/referencing still own validation and reference evaluation. The traversal
recognizes the catalog adapter's emitted `allOf` composition without admitting it
into canonical inputs. There is no additional validator or generic schema engine.
The public contracts root exports the four helpers needed across package boundaries;
compiler and union selection use their own package-internal structural functions.

`mcp_catalog.tool_catalog` consumes an already compiled interface. Installation
loading stays with MCP/CLI composition, and every repository Python consumer was
updated together. It creates detached output without store or connection access.
No forwarding wrappers, plugin registry, mutable session or new workflow state
were added.

## Regression and conformance evidence

Before-change probes reproduced all three original public-catalog failures in both
schema modes: `$ref`-named properties crash, literal `const` objects change meaning,
and literal `default` data is rewritten. After-change probes accept the property
and preserve both literals exactly. The old compiler also rejected literal
reference-shaped annotation data or wrongly treated it as a dependency.

Seventeen added test methods cover structural locations; literal field names;
const, enum and default payloads through supported containers; real missing and
unsupported references; schema reference cycles and sibling constraints; generated
Python construction and round-trip field maps; escaping collisions; pure detached
catalog construction; purpose-specific decoding; and the native/table-present
evidence-validation paths. The hand-authored fixtures use independent expected
valid/invalid outcomes checked by `Draft202012Validator`, not merely agreement
between two local transformations. Unknown canonical `allOf` still rejects.

The relevant external semantics were checked against JSON Schema Draft 2020-12
Core and Validation: schema-bearing applicators are distinct from literal data,
`const`/`enum` retain instance values, `default` remains an annotation, and `$ref`
sibling constraints remain effective. This is evidence for the admitted profile,
not a claim of arbitrary JSON Schema implementation or full official-corpus coverage.

Primary specifications consulted:
- https://json-schema.org/draft/2020-12/json-schema-core
- https://json-schema.org/draft/2020-12/json-schema-validation

## Local test results

| Check | Observed result |
| --- | --- |
| Full Engine selection, four complete file-disjoint shards | **415 passed**, no failures/errors/skips |
| Contracts/compiler package | **61 passed; 1 supported-environment check skipped** (62 methods) |
| Metadata package | **43 passed** |
| Policy-impact package | **10 passed** |
| Analysis package | **121 passed** |
| Verifier package | **168 passed** |
| Structural complete checkpoint | **121 checks across 73 suites passed** |
| Generated-contract/model/tool freshness | **Passed; no generated interface changes** |
| Current catalogs, both purposes/modes and focused/advanced | **8 of 8 byte-identical to baseline** |
| Old-code snapshot/Analysis/readiness reopened by new code | **Exact content and observations preserved** |
| Base-pinned patch application and delivered file hashes/modes | **Passed in fresh-clone reconstruction** |
| Diff whitespace validation and ZIP integrity | **Passed** |

The Engine selection is split into four file-disjoint shards, with 104, 104, 104
and 103 test methods respectively. The evidence includes the module inventory,
all final logs and exit codes. Subtest cases are not counted as additional methods.
The added focused tests are included in the package totals rather than counted twice.
After the clean Engine run, an unused test import was removed and the existing
catalog-description test was pointed directly at the contracts-owned public helper.
The contracts package and affected Engine tests were rerun after that import-only
cleanup; production code and wire behavior were unchanged.

The first broad attempt was stopped after the compiler correctly rejected an
inconsistent candidate capture: new source files had not been tracked before the
suite-input manifest was regenerated. Tracking the sources and regenerating through
`verify_repository` exposed a private cross-package import; the helper API was
exported from its public owner and the imports were corrected. The final complete
Engine run was restarted after both issues were fixed. Initial logs are retained
as rejected-attempt evidence, not counted as passing tests. No production validation
or test assertion was weakened to work around either failure.

## Catalog and retained-state equivalence

Every current catalog combination was compared with the exact baseline using the
same JSON serializer. All eight are structurally and byte-for-byte identical:

| Purpose | Mode | Focused bytes | Advanced bytes |
| --- | --- | ---: | ---: |
| Application | Compatibility | 39,274 | 51,224 |
| Application | Native | 39,274 | 51,224 |
| Authoring | Compatibility | 721,935 | 1,021,662 |
| Authoring | Native | 616,282 | 877,152 |

Tool descriptions, input/output schemas, ordering, annotations and catalog digest
inputs are unchanged for the actual corpus. The repair changes the previously
incorrect boundary cases rather than changing installed clients' ordinary schemas.
This refactor makes no additional model-token, billing, latency or memory savings
claim; the prior interface-efficiency behavior is retained.

An old-code process from the exact baseline created a snapshot, proposal Analysis
and review readiness in a disposable repository. The new-code process reopened the
same store without migration, returned identical exact policy content and workflow
observations, and produced the same readiness when repeating the explicit review.
No publication occurred in that replay probe. Existing integration tests separately
exercise explicit publication, interruption and recovery in disposable repositories.
User repositories and retained stores were not edited.

## Packaging and integration

The archive supplies complete repository-relative updated files plus a full-index,
base-pinned patch, per-file SHA-256/mode manifest and local evidence. Reconstruction
uses a separate fresh clone of the original source bundle, applies the patch with
`--index`, and compares every delivered path, byte hash and mode. The exact result
is recorded in `DELIVERY/reconstruction.json`. Staging new files matters because
the input manifest enumerates tracked inputs; source and generated capture inputs
must be integrated together.

Restart the MCP process and reconnect or refresh clients after implementation
replacement. Keep existing schema-mode flags and stores. No schema/state migration
or interface-version bump is needed for these preserved wire contracts. Private
implementation commits were confined to the working clone; nothing was pushed,
merged or published remotely.

## Environment and acceptance gates

Local environment: CPython 3.13.5, Linux x86-64, jsonschema 4.26.0, referencing
0.37.0, attrs 26.1.0, rpds-py 2026.5.1 and typing-extensions 4.16.0. The repository
supports locked Python 3.11/3.12 and pins rpds-py 2026.6.3. An attempted supported
Python installation failed because network DNS was unavailable. The lock was
preserved, and the supported-runtime test is explicitly skipped, not counted as a
pass. The existing locked CI remains required for supported-environment acceptance.

Configured Codex and MCP SDK clients are unavailable in this environment. Actual
client/model-visible schema qualification and independent review remain open.
The updated harness is available to the host operator; local stdio and schema
checks do not establish how every supported client renders nested authoring inputs.
Record the supported client/version results (or explicit support retirement), then
remove compatibility code and obsolete launch flags in one coordinated cutover.
That retirement is not implicitly performed by this correctness cleanup.

## Local integration qualification — 2026-09-26

The delivery patch applied to its exact base. All 31 staged file contents and Git
file modes matched the delivery manifest before adding this integration record.
Python 3.12.3 with every dependency at its requirements.lock version passed all
62 contracts tests without skips, 43 metadata tests, 10 policy-impact tests,
121 Analysis tests and 168 verifier tests. Generated projection freshness and
all 73 structural suites passed. All eight catalog configurations matched the
delivered baseline objects exactly.

The working tree already lacked the tracked
`Coding-Standards-agent-workflow-simplification.zip`. Engine publication fixtures
copy every tracked file, so the initial run encountered FileNotFoundError on that
unrelated deletion. Qualification therefore uses a disposable clone of the exact
base with the complete patch staged; the user's working-tree deletion is preserved.
The isolated reproduction of the affected publication test passed without source
changes. Engine suite results are recorded in the integration ledger.

These supported-runtime local checks supplement the original delivery evidence;
they do not claim a CI run, independent review or configured-client qualification.
