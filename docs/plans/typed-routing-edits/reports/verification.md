# Typed routing-edit pilot — verification

> **Current disposition (2026-09-27): Accepted.** The exact-source locked Python 3.12 workflow passed, the independent external reviewer recommended this slice as satisfied, and the acceptance owner dispositioned its findings. Earlier pending status below is historical. See the [acceptance-owner decision](acceptance-dispositions.md).

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

## Sequence reconciliation

This section records the later integration state; the earlier delivery evidence
above remains scoped to its original local environment. The typed pilot is one
commit, `7d563f032267d8d96fd45675147b9de7206a7cac` (tree
`fa5722c82a2cb6cd260e5cef8001137bbd1e412b`), directly after the pre-pilot
baseline `cbf9cdd2d7627d2c45f0001486a8872ab6b5206d`. Both local and GitHub
`main` pointed to the pilot commit at inspection. There is no pilot task branch or
PR; the only repository PR found was an older, unrelated merged PR. The production
delta remains exactly `logical_authoring.py` and `routing_edits.py`, with the
tests, generated verification-input manifest and records named in the commit.

The preceding source slices are also integrated on `main`. Their GitHub Actions
runs used each exact source revision and completed successfully:

| Slice | Source commit | Workflow run | Recorded acceptance |
| --- | --- | --- | --- |
| Boundary repairs | `e384fffd` | [36334749196](https://github.com/MrScripty/Coding-Standards/actions/runs/36334749196) | Verifying; external review pending |
| Immutable-work reuse | `0f24bac9` | [36340163409](https://github.com/MrScripty/Coding-Standards/actions/runs/36340163409) | Verifying; external review pending |
| Storage lifecycle | `87873de5` | [36342508184](https://github.com/MrScripty/Coding-Standards/actions/runs/36342508184) | Verifying; external review pending |
| Fact ownership and working set | `6fa41c31` | [36347662551](https://github.com/MrScripty/Coding-Standards/actions/runs/36347662551) | Verifying; external review pending |
| Snapshot-capture handoff | `cbf9cdd2` | [36350106138](https://github.com/MrScripty/Coding-Standards/actions/runs/36350106138) | Verifying; external review pending |

These runs resolve the previously unavailable exact-source CI observations for
the five earlier commits. They do not supply those plans' separately required
independent external material reviews or retroactively change their recorded
verdicts. Each plan's current owner must disposition its review gate before
marking it Accepted. The implementation sequence is complete and no next code
slice is admitted; the acceptance sequence is not closed while those required
reviews remain open. Optional routing-fact ergonomics, additional typed families
and scale tuning require a new evidence-based admission.

## Current pilot acceptance review

A fresh read-only architecture reviewer inspected the coherent pilot against
`cbf9cdd2`, including both production files, direct consumers, tests and
identity/persistence boundaries. No A1–A5 implementation blocker was found:
authored values remain immutable declarations, parse and semantic owners keep
their stages, the atomic routing batch and canonical identity paths retain their
existing authority, and no new public or stored representation was introduced.
The reviewer did not edit, stage, commit or repair code. This is supplemental
internal review, **not** the independent external review required by Q2.

One low-severity advisory concerns the private same-type float comparison in
`routing_edits.py`: Python considers negative and positive zero equal although
their JSON spellings differ. The identity codec rejects floats and applicability
has no numeric operand path, so no valid-workflow failure was demonstrated.
Record it as a deferred candidate, not an acceptance blocker or reason to widen
this pilot. No production repair was justified by the review.

The actual workflow at `.github/workflows/purpose-separated-engine.yml` requires
Ubuntu 24.04's Python 3.12, hash-locked binary installation from the unchanged
`tools/standards_contracts/requirements.lock`, all twelve package test selections
and the complete structural verifier. The package and lock also support Python
3.11, but the current workflow has no 3.11 matrix entry. The exact-commit
[run 36358571883](https://github.com/MrScripty/Coding-Standards/actions/runs/36358571883)
completed successfully. Its logs show exact public-source retrieval, Python 3.12
hash-locked installation, **589 Engine and 570 supporting tests with no skips**,
and **73 structural suites / 121 checks** passed. The supporting selections
include contracts and generated freshness, structural checkpoint and verification
input manifest checks. The 20 added routing-edit tests are included in the 589;
the recorded 23-case differential and retained-history readback are distinct
earlier evidence, not additional CI tests.

A separate isolated checkout of the same commit/tree ran the identical twelve
package commands and complete structural verifier with Python 3.12.3. All six
installed runtime-package versions matched the unchanged lock; `pip check`
found no broken requirements. It independently passed 589 Engine and 570
supporting tests without skips and 73 structural suites / 121 checks. This
local environment was preinstalled; only the hosted CI run proves this turn's
hash-locked installation. Local results, hosted results and the earlier Python
3.13 campaign are repeated executions of the same selections, not additive
test counts. Python 3.11 was not run because the actual CI workflow requires
only 3.12; no claim of 3.11 behavior is inferred from that result.

For this documentation-only reconciliation, an isolated copy of the candidate
with only the five planned record/index edits initially failed the complete
structural checkpoint at `policy-semantic-impact`: the plans index's digest in
the generated suite-input manifest was stale. Regenerating the manifest from
that isolated source changed only the `docs/plans/README.md` digest. The same
complete checkpoint then passed 73/73 suites and 121 checks. After the final
record text was copied into the isolated checkout, the affected verifier suite
passed 168 tests and the complete checkpoint passed again with the same counts.
The refreshed manifest and records are one closure write set; this check does
not relabel the source revision tested by run 36358571883 as the later
documentation commit.

The connected authoring MCP process reported interface 43 and
`restart-required` after the source update. A fresh process with the saved
registration started at interface 44, retained the expected catalog digest,
and completed an explicit-fact route with zero unresolved questions. This
confirms fresh-process navigation, not a live-model authoring qualification or
the outcome of the stale connected process. A normal host reconnect is needed
to replace the latter; it is outside this internal representation acceptance.

No independent external review report is available for the pilot. Its owner
must inspect the coherent `cbf9cdd2..7d563f03` slice, record each finding with
severity/evidence/disposition, and verify any necessary repair before A6 and
Q2 can be accepted. The fresh internal review above is supporting evidence only.
