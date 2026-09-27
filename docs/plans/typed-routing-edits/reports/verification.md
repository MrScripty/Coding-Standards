# Typed routing-edit pilot — verification

**Status: Verifying.** Source implementation and local behavioral evidence are
complete. Supported locked-runtime CI on this exact diff and independent external
review remain acceptance requirements. No live model qualification is claimed.

## Exact baseline and bounded scope

The implementation starts at `cbf9cdd2d7627d2c45f0001486a8872ab6b5206d`, the verified
main head at admission, including the snapshot-capture handoff. Its source tree is
`1c1a7c6f170abb291a38ce0aa50d2e3b082e34b4`. The Actions source artifact ZIP hash
`46934bdb5711fa0c5af4fce8f23381d635e4555d95c5cd4fd5b14c88ab5ceae3` was checked
before independent baseline and candidate checkouts were created. The baseline CI
was still running at initial inspection; its eventual outcome is not evidence for
this candidate. No remote source, user checkout or production standard was changed.

The executable Router selected 24 applicable standards with no unanswered facts.
Their exact contents were read and retained for the implementation admission.
Core, Implementation, Planning, Verification/oracles, proportionality, architecture,
code design, contract and persistence requirements guide the bounded change.

The production write set is two files: the existing `logical_authoring.py` and
new `routing_edits.py`. Tests, maintenance records and the generated verification
input manifest make up the remaining delta. All other edit families, existing
proof/cache/storage refinements and public operation contracts remain unchanged.
The Engine stays at **interface 44** with the same catalogs and launch arguments.

## Implemented model and ownership

Four explicit frozen edit variants model putting/removing routing facts and rules.
Their kind is a class constant; their conflict facet derives from the selected
fact/rule identity. No independently settable kind, target, facet-name or inner
JSON payload is retained for this family. Existing StructuredEdit behavior remains
for other families; this is not a wholesale representation rewrite.

Put edits contain immutable authored fact/rule declarations. Nested JSON-shaped
values are detached into immutable tuples and mappings. Their map ordering matches
the former canonical JSON round trip; authored array order is preserved. Returned
contract dictionaries are new values, so a caller cannot mutate retained history.
Authored equality preserves scalar-type distinctions such as true versus integer
one, rather than inheriting Python's equality between those values.

These are **authored declarations, not compiled FactContracts or applicability
programs**. Some fact semantic fields remain unbound JSON values until their
existing semantic owner interprets them. The value module neither understands an
operator nor validates its dependencies. Existing authoring shape/text/revision
checks remain in logical_authoring, in their former order. Fact-domain interpretation,
semantic-revision checks, rule targets, references and resulting graph validity
remain at their existing final-context projection/compiler stages. This preserves
same-set fact/rule changes and declaration-before-binding behavior, including the
rejection stage of semantically invalid declarations.

The new value module imports only standard-library value types. It has no reverse
import into the compiler/parser, no validation registry, and no new general-purpose
freeze package. Typed routing dispatch replaces dictionary reconstruction when
classifying edits, attributing Router scope and staging the atomic routing batch.
Canonical serialization remains at deterministic order, identity, persistence and
file-rendering boundaries. There is no new cache, lifecycle, authorization or
schema-discovery requirement.

## Independent baseline comparison

Separate baseline and final-candidate processes interpreted the same exact captured
baseline authority across **23 scenarios**: eight successful projections and fifteen
rejections. Their complete diagnostic JSON files are byte-identical. For successful
paths the comparison includes normalized change sets, serialized object/array order,
facets, deterministic revision IDs, aggregate payload hashes, every projected file
hash, repository paths, semantic proposals, analysis policy/module selection and
compiled semantic signatures. For rejection paths it includes the failure stage,
error owner/type and structured code, outcome and message.

Cases cover put/remove variants, co-edited fact/rule references, restored rules and
fact removal, target swaps, presentation-only fact changes, changed fact meaning
with the correct revision, wrong revisions, missing or referenced removals, duplicate
targets/facets, unavailable targets/facts, unknown expression operators, invalid
fact types/nullability, duplicate values, unsupported literal values and multiline
conditions. The fixed IDs in the pure identity probe are comparison fixtures,
not invented evidence authority. Actual persisted-record checks are separate.

Focused tests additionally compare incremental successor construction with full
replay, mixed new-standard/routing changes and input-order permutations. Both paths
retain exact files, semantic proposals, analysis attribution and predecessor bytes.
No earlier semantic normalization was used to make the typed values easier to model.

## Runtime and test evidence

| Check | Result |
| --- | --- |
| Complete frozen-source Engine selection, four file-disjoint shards | 589 passed, no failures or skips |
| Added routing representation/projection/stdio methods | 20 passed, included in the complete selection |
| Eleven supporting packages | 568 passed; two existing environment-dependent skips |
| Baseline/final-candidate differential | All 23 scenarios match exactly |
| Cold persisted-history upgrade | Eight replacement MCP processes returned exact baseline results |
| Catalog preservation | All eight purpose/scope/output-delivery variants byte-identical |
| Canonical preservation | All 326 definitions and 40 operation declarations unchanged |
| Registered structural checkpoint | 121 checks across 73 suites passed |

The final Engine selection ran after the last production/module-boundary refinement.
Its test IDs and file-disjoint shard outcomes are recorded in test-summary.json;
counts do not add earlier focused reruns. Runtime hashes bind that campaign to the
delivered two production files. A final targeted rerun and post-report checks are
recorded separately in delivery evidence; they overlap, rather than inflate, the
package totals.

The original no-inner-decode regression failed on all four baseline routing forms
as intended. Before final qualification, composition review moved parsing back
into logical_authoring so the new module owns values only. The initial task-owned
Engine campaign was stopped and restarted after that change; its partial logs are
retained separately and are not counted as a completed passing campaign. Existing
checks were not weakened. No failed candidate test is relabeled as passed without
its observed rerun.

The three new real-stdio scenarios create proposals and revisions using all four
routing variants, consume actual returned obligations with explicit test-fixture
evidence, and reach reviewed readiness in both eager and on-demand delivery. They
verify repeated/shared versus inline evidence results and original/successor Router
readbacks; main is not published. Malformed public input and semantic unknown-fact
failures remain rejections without creating a proposal. These are deterministic
Engine fixtures, not claims that a model produced the requests or audited production
semantic intent.

An untouched baseline implementation separately produced a two-revision routing
history, completed Analysis and readiness. Eight replacement candidate stdio
processes reopened completed status, ready status, repeated review and exact Router
readback under both output deliveries. Every structured result and matching text
copy was identical; the accepted Git ref stayed unchanged. No history rewrite,
store migration, state deletion or publication was needed.

## Measured work reduction and limits

Instrumentation observes calls to the original inner JSON decoder directly, not a
mocked substitute. Four routing edit forms serialized 100 times each caused **400
inner JSON loads at the baseline and zero in the candidate**, with exact result
objects and canonical map order preserved. A warm status observation on the real
retained routing history still serialized 52 edit representations for its existing
identity/observation needs, but **inner JSON loads fell from 52 to zero**. The full
structured status was identical.

Serialization call counts themselves are not claimed to disappear: returned
objects remain freshly constructed, and canonical encoding at genuine boundaries
remains necessary. Local twelve-thousand-call timing samples are retained as an
inner-operation experiment only. They ran alongside other verification and do not
establish general MCP latency, memory/RSS, token or billing improvements. There is
no claimed cache-capacity or allocation-budget change. Review this pilot's actual
maintenance and workload effects before admitting another edit family.

## Preservation and acceptance

All previous schema, operation, generated-model, normative-content, CI and lock
files selected by the preservation check are byte-identical (91 protected files).
The complete reconstructed Git-tree check also ensures no unlisted baseline path
changed. The fact/capture/working-set/storage improvements already on main remain
intact. Current source documentation describes the pilot and links its evidence;
historical verdicts and acceptance records are not rewritten.

Local environment: CPython 3.13.5, Linux x86-64, Git 2.47.3, jsonschema 4.26.0 and
rpds-py 2026.5.1. The unchanged supported lock requires Python 3.11/3.12 and rpds-py
2026.6.3. A bounded attempt to provision Python 3.12 failed on DNS. The two existing
supporting-suite skips concern supported interpreter qualification and a permission
case inappropriate under the local root user. No authenticated Codex/model session
or independent external review was performed here. Local self-review is not
represented as independent acceptance.

A1–A5 have local deciding evidence. T1 is Implemented and Verifying, not Accepted.
T2—exact-diff locked CI and independent review—is the single next integration slice.
The implementation does not authorize broader typed-edit conversion. No new tools,
MCP settings, public schemas or persistent formats are required.

## Integration

Use DELIVERY/README.md, the read-only baseline preflight and the base-pinned patch.
Preserve unrelated source and ZIP changes. Apply the new value module and compiler
consumer together and stage only listed paths, including new tests and generated
verification inputs. Restart long-running processes through the normal host
mechanism to load changed Python, after resolving active publication/recovery
ownership. Keep all existing stores and handles; no registration or catalog change
is needed. No remote push or production standards publication occurred.

The final report/status updates and generated input refresh occur after the full
frozen-source test run. Final focused/freshness/structural results, per-file hashes,
base preflight and complete-tree patch reconstruction are recorded under DELIVERY.
