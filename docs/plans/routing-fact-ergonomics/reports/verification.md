# Routing-Fact Ergonomics — Verification

**Status: Verifying.** R1 source implementation and local evidence are complete;
the integrated exact-head locked CI and independent source review now pass. The
actual connected client still needs interface-45 qualification before acceptance.
R2 is the next slice. This change does
not reopen the accepted six-slice refactoring or implement later priorities.

## Baseline and scope

The source is `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`, tree
`6d1f1f8a33d4391c9ab8e315b18bfc25603e1b97`, obtained from the verified Actions
source archive SHA-256
`4b3179f85138ef92b55a2a54879c950ed78ffdd060f97ebc3c14912766c4a816`.
GitHub main still identified that commit at admission. Candidate interface: **45**.
The caller changes are incremental to that exact source, not an unverified overlay.

The written plan was read and admitted as `start` in an isolated branch. The
baseline Router selected 22 standards and all were read back without unresolved
facts. The inherited planning facts already selected implementation/build through
their prerequisite closure; a later explicit implementation/build fact check
selected exactly the same 22 owners. Both observations are retained rather than
relabeling the earlier request. No user checkout, external provider, production
standards, accepted main, or remote ref was modified.

The closed acceptance records, normative corpus, identity/persistence/caching/edit
owners and dependency/CI configuration remain unchanged. Five existing handwritten
runtime modules change, with one new Engine boundary module. The remaining source
changes are generated contracts, direct tests/client guidance and this plan bundle.
No review-packet generator or unrelated test-strengthening work is included.

## Implemented contract and ownership

Focused `route` in both purposes accepts raw known boolean/null/string/string-array
values in one required `facts` map. Nonknown observations use the closed one-field
markers `{"state":"unknown"}` and `{"state":"known-absent"}`. An omitted key,
false, empty set, nullable known null, explicit unknown and known absence remain
distinct. Old typed envelopes, numbers and arbitrary objects are invalid focused
inputs; there is no fallback parser or flag.

Static shape validation remains at the generated input boundary. The existing
snapshot load/verification and application Router qualification precede interpreting
its fact vocabulary. `FactSchema.require` owns required-name lookup; the new small
`routing_inputs` adapter fills only the declared type, retains caller names until
binding, and invokes the unchanged semantic binder once. Fact aliases, type/domain/
nullability/normalization and three-valued evaluation stay with applicability.

Both canonical and focused callers use the same bound selection algorithm. Native
query and candidate-preview requests still supply canonical typed `FactSet` values.
The focused authoring result projection moved from the generic selector into agent
navigation. Focused fact echoes, explanation requests and content-page continuations
use one reverse projection of the same bound canonical facts. Canonical IDs and
normalized values are reusable in a replacement process with the same snapshot,
detail, limit and next offset. No extra capture, content load, bind or compilation
is needed for a composed page. Existing final lifecycle checks still discard a
page whose authority becomes unavailable.

Dynamic focused input failures return existing bounded input feedback, with
`ROUTE.INPUT_INVALID` for authoring and `APPLICATION.INPUT_INVALID` for application.
The `describe_input` continuation names route; vocabulary remains available through
`routing_facts`. Known field names may be identified; unknown keys, supplied values,
and excessive/ambiguous locations are not echoed. Native-query error handling is
unchanged. Static failures occur before capture; a dynamic failure with no selected
snapshot can follow a new capture. No invalid input admits a proposal, decision,
review, publication, or guessed routing result.

## Discovered normalization boundary (RF-10)

Two different input strings, `e\u0301` and `é`, satisfy raw uniqueItems. The existing
canonical binder normalizes both to `é`, retaining a duplicate tuple. Returning
that array in the focused result or continuation would violate its declared
uniqueItems contract and could escape during result validation.

This change preserves canonical native binding and instead validates the focused
reverse projection with the existing generated assertion contract before selection.
A collision produces safe field feedback; one corrected spelling round-trips as
the normalized value. It is not an additional fact semantics engine, deduplication
policy, or change to stored sets. Tests explicitly observe the unchanged canonical
binding, static acceptance, focused rejection, repaired continuation, and actual
MCP behavior in both purposes.

Other static-to-dynamic boundary movement is intentional: omitting a repeated type
means a raw string can be statically admissible but invalid for the selected enum-
set fact. The final semantic outcome is checked, not falsely called an identical
parser stage. Required-name resolution occurs before the binder pass, so a later
unknown name can precede an earlier value error in a multi-error request. Single-
error diagnoses and that ordering are directly tested.

## Verification evidence

| Check | Observed result |
| --- | --- |
| Complete Engine selection plus corrected affected rerun | All 608 distinct Engine methods observed passing; two stale version-assertion methods corrected after the full selection |
| Eleven complete supporting-package suites | 569 passed; two existing environment-dependent skips (571 run) |
| Final focused feature/consumer rerun | 85 passed; included in the package selections above |
| New feature regression methods | 19 Engine + one applicability; included in the totals above |
| Baseline/candidate routing comparisons | All 20 matched their intended semantics and authority |
| Replacement-process retained-state observations | All ten exact domain results matched; accepted main unchanged |
| Registered structural checkpoint | 73 suites / 121 checks passed |
| Generated projection, syntax, scoped diff and final artifact checks | Final post-record results retained in DELIVERY/evidence |

The six-type/state matrix contains **126 cases**, with **33 successful equal
canonical bindings** and **93 rejections** under both final interpretations.
Literal `exists`/truth/unknown expectations, immutable-container checks, exact
failure codes and field pointers, escaped/long names and alias collisions add
independent oracles beyond converter equality.

Integration checks use real SQLite snapshots with distinct vocabularies and
application qualification. They prove selection from snapshot A versus B rather
than ambient files, one semantic bind/load/compile per composed call, no capture
on retained continuations, canonical query preservation, complete selected closure,
unknown questions and actual replacement-stdio results. A foreign fact-schema
digest still fails at the applicability evaluator. Unqualified Router content is
rejected before the new binder reads its private vocabulary.

The baseline/candidate comparison records **20 routing observations**: five source
fact scenarios across compact, full, content-bearing and canonical native results.
Only the deliberately changed focused facts/continuation fields are transformed
for comparison; native results match exactly. Ten replacement MCP processes then
reopen baseline-produced Analysis status, readiness status, repeated review,
proposal content and canonical routing under both output-delivery choices. Results
and accepted main remain unchanged, without migration or publication. A saved
nonempty old focused request is deliberately rejected, not replayed through a
hidden compatibility path.

## Original failures and repairs

Initial binding-test fixtures omitted required declaration fields (aliases and
nullability); those fixtures were repaired and validation was not relaxed. The
first 54-method focused integration selection passed 53 methods and found one
mixed-consumer test that had sent new assertions to a canonical query; it now uses
an explicit typed native fixture. An initial test-launch precondition error produced
no acceptance result. The first broad Engine run was stopped at the task-owned
process group after the concrete RF-10 boundary was found; its partial logs are
preserved as non-acceptance evidence. The complete selection was restarted after
the normalized-output guard and its regression tests were added.

The full Engine selection then found two remaining current-version assertions in
test_schema_presentation and test_capture_handoff_transport that still expected
interface 44. The latter reports a failure in each output-delivery subtest. These
are two failing methods/three failure reports, not a runtime regression. Both were
updated to 45 with all other behavioral assertions preserved and included in the
successful final focused selection. All 608 current Engine method IDs have passing
evidence; this is complete-selection coverage plus the affected rerun, not a claim
of one uninterrupted all-green full-suite execution. The runtime source did not
change for these test metadata repairs. Post-run records and operational wording
are separately checked; repeated executions are not added to distinct-test totals.

## Measured effects and compatibility boundary

Ordinary JSON serialization of the known-fact request changes from **179 to 81
bytes** for two facts, and **612 to 220 bytes** for eight explicitly empty category
sets. The latter measures syntax only and is not an instruction to fill missing
facts with empty sets. The route input schema changes from **2,475 to 1,625 bytes**.

| Focused catalog | Baseline JSON bytes | Candidate JSON bytes |
| --- | ---: | ---: |
| Authoring / eager | 713,206 | 711,743 |
| Authoring / on-demand | 108,812 | 108,171 |
| Application / eager | 83,735 | 82,200 |
| Application / on-demand | 15,955 | 15,270 |

All purpose/breadth/delivery variants were measured; operation names, counts and
output-delivery choices remain. These are raw catalog/request bytes, not model
context, billing, latency or a measured reduction in model repairs. The supported
live agent comparison is still required before closing R-A7.

Of the previous **326** canonical definitions, **323 are unchanged**. Only
`RouteCall`, `CompactRouteResult` and `AgentRouteResult` change their facts reference;
`RoutingFactAssertion` and `RoutingFactAssertions` are added. The **40 operation
declarations**, canonical FactSet/FactValue/RouteRequest, native and preview model
definitions, request contract 6 and result projection 7 remain unchanged. Reachable
tool-schema closures and catalog digests naturally change where they include the
focused route definition. This is not a claim that every native catalog closure
has identical bytes. The preservation inventory independently checks **839**
protected repository paths, including the prior plans/acceptance and the unchanged
authoring, identity, store, cache, lock and CI owners.

## Qualification and integration

### Integrated exact-head CI (R2)

GitHub Actions run `36465019273`, job `109072809297`, completed successfully on
integrated commit `39d44f007c36684e1ebc546f31a19e20e2e660e5`, tree
`ca0e6c212003fff0d8be2c3d73f2a07b3897bfdd`, which contains the production
pilot commit `09d7829df79d2e0c25b8fb9add4b7c47d6368684`. The workflow fetched
that exact public source, created its Python 3.12 environment, and installed the
unchanged `tools/standards_contracts/requirements.lock` with `--require-hashes`.
All eleven supporting-package selections passed (571 tests), the complete Engine
selection passed (608 tests), and `verify.py --complete` reported 73 selected,
73 passed, zero failed or blocked. The completed test summaries report no skips.
This is supported-environment candidate evidence for R-A1, R-A2 and R-A6. The
earlier local full-selection failure and affected rerun remain recorded above;
the CI run is a distinct all-green execution, not a relabeling of that local run.
The uncommitted R2 record additions and unrelated output-contract documentation
edits are outside the tested source tree.

The [read-only external source review](external-review.md) found no blocking source
defect and made two advisory observations dispositioned in `issues.md`. It did not
claim CI or live-agent evidence. The [paired fresh-model comparison and current
connected-session state](r2-live-agent.md) remain distinct: the disposable model
comparison succeeded, but this session's connected catalog still reports 44 and
must be refreshed before R-A7 can be decided.

At the R1 handoff, local runtime was CPython 3.13.5 with jsonschema 4.26.0 and
rpds-py 2026.5.1. The existing supported hash-locked CI selects Python 3.12 and
rpds-py 2026.6.3. A bounded attempt to provision Python 3.12 failed due to DNS;
no pin or CI matrix was changed.
The baseline CI success is not candidate CI. No Python 3.11 result is claimed.

At that handoff, no authenticated Codex/model turn, independent external review,
provider transfer, operator configuration edit, remote push, or production standards
publication was performed. The existing configured-client navigation harness has been updated but
was not executed on the operator's host. Its observation is distinct from a fresh
model task; the new qualification guide describes both without requiring artificial
standards mutations or the future review-packet generator.

Apply the base-checked patch and generated outputs as one coordinated source change.
Restart the Engine and refresh/reconnect the actual client catalog for interface 45.
No registration flags change; preserve purpose and on-demand output selection.
Existing valid snapshot/workflow handles and canonical stored facts remain valid.
Old focused calls/continuations require their original interface/source or explicit
reconstruction in the new grammar against the retained snapshot. Do not migrate or
erase stores to update an input representation.

R1 is Implemented and the plan is Verifying. Required locked-runtime and actual
host/review claims remain pending at R2/integration; no global Accepted verdict is
fabricated from local tests. The next priorities remain review-evidence packaging,
then broader test strengthening, only after this scope's normal completion.
