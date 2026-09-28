# Routing-Fact Ergonomics

**Plan status:** `Verifying`

**Current phase:** R1 source complete and locally verified; R2/integration acceptance evidence pending

**Next slice:** **R2 — Live agent comparison and accepted cutover**

**Acceptance status:** `partial`

**Composed-design review:** `applicable`; see [the composed-design admission](#simplicity-and-ownership-review).

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Admission:** this plan owns priority 2 of the user's new sequence **2 → 4 → 3**:
routing-fact ergonomics, review-evidence packaging, then broader test strengthening.
The prior six-slice refactoring is Accepted and closed. This plan does not reopen it.
The user admitted `start` against this path; R1 is now implemented. The next
admission is `verify` for the R2/integration evidence after checking current state.

## Objective

Let an agent supply known routing values without repeating each fact's registered
type and `known` wrapper. Preserve uncertainty, snapshot authority, applicability,
qualified policy reads and exact continuation behavior. The improvement must be
observable in request construction and real agent use, not just a smaller schema.

## Source and design evidence

The inspected baseline is `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`, tree
`6d1f1f8a33d4391c9ab8e315b18bfc25603e1b97`, interface **44**. It was obtained from
Actions source artifact `10956749223` and checked against its SHA-256. Baseline CI
run `36393453038` is successful; it is baseline evidence, not candidate acceptance.
Implementation uses the actual integrated checkout and reconciles intervening
changes. This plan does not require a particular commit chain or exact-HEAD policy.

[Design comparison](reports/design-comparison.md) records a planning-only experiment:
126 six-type/state binding cases preserve final validity; 33 bind successfully.
Six real Router examples round-trip through the current Engine with unchanged
results. A two-fact request decreases from 179 to 81 JSON bytes. A proposed schema
compiles through the current generator without changing repository source. These
observations select a feasible design; they do not qualify a deployed candidate.

## Selected public representation

Keep one `facts` map. A primitive value means a known fact; a small state object
represents known absence or explicit uncertainty. Example of the proposed API:

```json
{
  "facts": {
    "routing.activities": ["implementation"],
    "routing.boundaries": ["ipc"],
    "routing.applications": []
  }
}
```

`routing.applications: []` is appropriate only when the task establishes that empty
set. It is not a way to silence questions. The current registry has eight enum-set
categories, but this contract covers all six currently supported fact types.

| Supplied assertion | Meaning |
| --- | --- |
| Key omitted | No supplied information; the fact remains unknown. |
| `true` / `false` | Known boolean, only for a boolean fact. False is not absence. |
| String | Known string/enum/canonical-ID value, as determined by the registered fact, not the JSON/Python type alone. |
| String array, including `[]` | Known set value; empty is not absent or unknown. Existing membership, uniqueness and normalization rules apply. |
| `null` | Known null, only when the selected fact is nullable. `exists` remains true. |
| `{"state":"known-absent"}` | Explicit known absence. `exists` is false. |
| `{"state":"unknown"}` | Explicit uncertainty; retain that explicit entry in canonical observations. |

State markers have exactly one field, no payload, and no new spellings. The string
`"unknown"` is an ordinary known string, not a marker. No numeric or object-valued
fact type is currently supported: numbers and arbitrary objects remain invalid.
Adding such a fact type later requires an explicit grammar review, not guessing
whether an object is a value or a marker.

Use **one focused representation**, not `known_facts` plus absence/unknown buckets,
multiple aliases for the new syntax, or an old/new shape detector. The canonical
typed `FactValue` / `FactSet` remains the semantic representation for applicability,
Analysis, native queries and stored contracts. It is not a retired renderer.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| R-A1 | The new focused input and output fact grammar is explicit, generated, discoverable, and has no old-envelope fallback. | contract | supported locked runtime | automated | pending | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A2 | Equivalent supported inputs produce identical canonical fact bindings, rule truth/unknown sets, selected dependencies, ordering and qualified content. | focused + differential | supported locked runtime | automated | pending | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A3 | Static and snapshot-dependent failures are bounded, useful typed input rejections; no invalid value becomes success, a transport exception or fabricated absence. | contract + negative | both MCP purposes | automated | satisfied | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A4 | Fact binding uses the selected snapshot after qualification; content and full-explanation continuations round-trip that binding without additional capture or compilation. | integration | real SQLite and replacement stdio | automated | satisfied | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A5 | Native query/preview, evidence-backed Analysis, authoring, stored identities/handles and prior retained workflows preserve their contracts and results. | compatibility/retention | baseline producer and candidate consumers | automated | satisfied | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A6 | All actual affected producers, consumers, generated examples and live guidance are coordinated; complete required CI and structural checks pass on the relevant material. | integration | current hash-locked CI | automated | pending | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A7 | The supported live agent can construct and refine routing facts with the smaller format, use discovery as needed and preserve unknowns, without new repair loops or a required extra call. | user workflow | actual authorized client/model/surface | observed | pending | [Verification and remaining environment/host/review claims](reports/verification.md) |
| R-A8 | Independent review and acceptance-owner disposition establish the exact candidate's invariants and proportionality; unrelated work and previous acceptance are preserved. | review | independent reviewer and owner | manual | pending | [Verification and remaining environment/host/review claims](reports/verification.md) |

No production standards proposal or publication is necessary for the navigation
workflow qualification. Required existing authoring regressions and retained-state
checks remain part of R-A5/R-A6; a fresh model authoring lifecycle is required only
if evidence shows this implementation changed an authoring boundary.

## Scope and authority

### In scope

The focused `route` input in both application and authoring catalogs, its canonical
fact binding, focused fact echoes, routed-content continuations and full explanation
requests; the directly affected shared routing-selection call sites, generated
contracts, diagnostics, consumers, documentation and qualification.

### Out of scope

Review-packet generation (priority 4); the deferred broad test-strengthening backlog
(priority 3); downstream pilots; additional typed edit families; automatic NLP fact
inference; per-project fact presets; sessions, saved mutable task state or new caches;
changing rule semantics, normalization, evidence/authorization, snapshot capture
proofs, store lifecycle, policy content, exact read text or output-delivery choices.
This slice still includes all ordinary tests needed to prove its own change.

## Binding Decisions

### D1 — Separate wire shape from fact semantics

Add `RoutingFactAssertion` and `RoutingFactAssertions` to the canonical interface.
The first is the disjoint union of boolean, null, string, unique string array, and
the closed state-marker object above. The second maps supplied fact IDs/aliases to
that assertion. Replace `RouteCall.facts` with the new map. Keep `facts` required;
`{"facts":{}}` explicitly starts with no known facts. Snapshot/content/detail
arguments retain their existing meanings and defaults.

Change only the focused authoring `CompactRouteResult.facts` and
`AgentRouteResult.facts` to the same compact map. These observations use canonical
fact IDs and normalized values produced by the existing binder, including an
explicit unknown marker when supplied. Application route results need no new fact
echo. Preserve the existing canonical `FactSet` and `FactValue` definitions.

The new union is statically unambiguous because existing fact values cannot be
objects. Do not add a custom general schema parser or generator behavior to express
it: the planning probe already compiles it through the current schema profile.

### D2 — Bind once against exact, authorized authority

Static generated validation owns the common JSON shape before snapshot capture or
rule evaluation. It cannot determine whether a string is valid for an arbitrary
registered name. Select/capture the snapshot by the existing contract, load and
verify it once, and require application Router qualification before interpreting
its fact vocabulary. Infer **only the declared type** from that snapshot's
`FactSchema`, never from an ambient registry, the caller's spelling, or Python
coercions. No negative fact value is inferred.

A small Engine-owned `routing_inputs.py` projection translates raw known values and
markers to canonical typed-state dictionaries, then uses the existing
`FactSchema.bind` as the sole semantic binder. Factor the existing required-name
lookup into a shared `FactSchema` lookup method if needed so the adapter does not
copy identifier/alias error rules. Preserve supplied names through binding so a
fact and its alias remain a duplicate, even when their values agree. This lookup
change must preserve the ordinary canonical binder's contract and diagnostics.

Pass the resulting existing applicability `FactSet` to a shared bound-fact routing
selection step. Split the present binding-plus-selection wrapper at its real
boundary: native query and candidate-preview callers still bind their canonical
requests; focused callers bind their compact inputs. Both use the same rule
selection, dependencies, three-valued evaluation and schema-digest guard. Do not
bind twice, create a new mutable context, or add a mode flag inside applicability.
Local helper names may follow the code's conventions; these ownership and single-
binding requirements are fixed.

Implementation finding RF-10 refines the focused boundary: after canonical binding,
validate the reverse projection with the existing generated assertion contract
before selection. Canonical normalization may merge distinct Unicode spellings;
such a collision returns a typed focused input failure, not an internal result
exception. Native binding/queries retain their original behavior. This preserves
one semantic binder while proving the new wire observation is representable.


### D3 — Preserve the failure meaning, acknowledge its necessary boundary move

In the smaller schema a raw string is statically admissible, but it may be wrong
for the fact actually selected by the snapshot. The planning experiment contains
41 examples whose **static-stage** validity changes while final validity agrees.
That is a known consequence of removing caller-supplied type, not proof that all
rejection stages are byte-identical.

Validate dynamic type, domain, nullability and alias conditions via the existing
binder **before** creating a purportedly valid canonical request/result. A malformed
fact must not escape as an uncaught `ContractError` or MCP internal error because
conversion was deferred. Static shape failures use existing input feedback; dynamic
focused-routing input failures get the ordinary invalid outcome with safe field
feedback. For application purpose, adapt those identified input failures to
`APPLICATION.INPUT_INVALID`, not a false availability or permission result.
Qualification/lifecycle failures retain their separate outcomes and precede private
vocabulary disclosure. Native-query failure behavior remains unchanged.

Reuse the existing bounded `input_feedback` and discovery conventions. Messages
refer only to safe registered vocabulary and constraint meaning; unrecognized
caller keys/values are not dumped into errors. Include a useful `describe_input`
route hint; the existing `routing_facts` operation remains the vocabulary source.
No new diagnostics framework or tool is needed. Cover single-error cases exactly
and explicitly disposition ordering where multiple defects compete.

An input with valid static shape may capture a snapshot before a vocabulary-dependent
rejection when none was supplied. Do not claim that every invalid request creates
no snapshot. No invalid routing input may create a proposal, decision, review,
publication or guessed successful routing result.

### D4 — Continuations must be valid calls under the new contract

Construct focused fact echoes, `explanation.facts`, and `content.next.facts` from
the same bound canonical facts through one reverse projection. Reuse canonical IDs
and normalized values; do not maintain an independent second spelling of the facts.
Carry exact snapshot, detail, page limit and next offset as required today.

A returned continuation must validate as the new `RouteCall` and execute in a new
process without access to earlier session state. Preserve the whole selected
closure and all unknown questions. Changing supplied facts intentionally selects
a different route; pagination does not silently change facts or authority.

Keep native `RouteRequest`, application native queries and candidate previews typed
as they are. They are independent canonical consumers, not fallback paths for an
old focused call. Move focused explanation construction out of generic routing
code if necessary to avoid making the canonical selector own wire presentation.
Do not change `RouterProjection.fact_definitions()` or material digests.

### D5 — Coordinated public replacement, no persistence migration

At the inspected interface-44 baseline, use interface **45** for the breaking focused
wire replacement. Reconcile the actual integrated edition before implementation;
do not overwrite someone else's release metadata. Keep request contract 6, result
projection 7, applicability language/schema versioning, handles, schemas for native
queries, identity encodings and store format unchanged unless contrary evidence
requires a re-plan. Generate models/catalogs/examples through their existing owner.

The new focused endpoint rejects the old `{type,state,value}` envelopes and unknown
extra fields; it does not auto-detect or retain them under a flag. Empty maps are
naturally shared syntax. Update actual supported consumers atomically and document
any independently deployed consumer needing a separate versioned rollout before
cutover. The scope is not permission to revive retired input compatibility support.

Old saved focused `route` calls and their content/explanation continuations are
interface-44 requests: preserve historical files and replay them only with matching
source/tooling. Resume a live task by refreshing its catalog and constructing the
new facts against the retained valid snapshot, not by migrating or deleting stores.
Other workflow handles and canonical stored fact values remain valid. Runtime/catalog
digests naturally invalidate changed input and output-discovery selections.

### D6 — Adoption and evidence remain explicit

Use the existing native/on-demand deployment; no registration flags change. Restart
and refresh tools after the new interface is integrated, preserving other settings.
Before expanding a host-specific design, observe the generated union through the
actual supported client's tool declarations/discovery. No unobserved assumption
that maps or unions will be rendered fully should drive a large implementation.
Continue independently useful canonical/projection tests while the host is unavailable.

Compare representative fresh baseline/candidate agent tasks, with the same task
facts, starting authority and comparable model/surface. Count construction errors,
repairs, fact-discovery calls, request bytes and repeat reads separately. The schema
and values may be discovered through real tools, not injected by the observer.
Do not require extra discovery as a ritual or supply fabricated empty sets. The
new mode should succeed without worse task correctness or an added mandatory round
trip; repeated gains may justify a stronger efficiency claim. Raw JSON is not model
context, billed tokens, latency or evidence of correctness by itself.

## Simplicity And Ownership Review

**Applicability:** `applicable`

The artifact changes a public generated input,
its snapshot-dependent binding and multiple continuation producers.

- Independent concepts and dimensions: wire assertion syntax belongs to the Engine contract;
   registered fact meaning/aliases/nullability to applicability; selected policy
   authority to verified snapshots and application qualification; routing selection
   to the existing selector; client declaration rendering to its host.
- State, identity, value, time, policy, and mechanism: input type completion occurs after exact authority
   selection, once per call. A bound `FactSet` carries the fact-schema digest. Neither
   local inference nor a cached schema may establish current permission/lifecycle.
   Installation edition 45 versions the wire; no stored fact identity is redefined.
- Caller and composition-root knowledge: know a fact name and observed value, or one explicit nonknown
   state; retain the snapshot and returned continuation. Do not repeat registered
   types, know internal error classes, or translate canonical facts manually.
- Representative change paths and forced owners: a new allowed enum value changes its fact definition and tests,
   not an agent schema's hardcoded registry. A new fact **type** requires a deliberate
   assertion-grammar review. A wire marker change affects the adapter/schema and
   focused consumers; an evaluator change stays outside this presentation slice.
- Stable Interfaces versus hidden knowledge: reuse FactSchema resolution/binding and existing immutable
   FactSet. The Engine's assertion syntax never enters normative material hashing,
   applicability expression parsing or persisted revisions. No facade reaches into
   a private definition index to bypass its owner.
- Independent evolution, testing, failure, and replacement: projection and binding have deterministic
   tests; source/codegen checks are separate from host/model observations. Lost
   snapshots or unqualified Router content fail at their existing owners. A stale
   client cannot silently switch syntax.
- Deletion and cumulative machinery result: one small bidirectional boundary projection removes wrapper
   construction knowledge from all callers; deleting it would redistribute that
   knowledge into both purpose adapters and continuation builders. It replaces the
   focused old shape instead of adding aliases. A shared required lookup avoids
   duplicated authority rules; it is not a new semantic registry or validator.
- Necessary complexity and containment: three fact states, six fact types, explicit nullability,
   aliases and snapshot scope already exist and remain necessary. They stay with
   their canonical owners. One new wire grammar, one small adapter, ordinary bound-
   selection factoring and one interface edition are sufficient. No task state,
   provider orchestration, cache or generalized facts mini-language is admitted.

## Milestones

### R1 — Coordinated focused contract and consumers

**Status:** `Implemented`

**Goal:** implement the single smaller focused route representation with semantic
and authority equivalence and useful error behavior.

**Allowed write set:** the exact owned families below, with concrete paths and
per-consumer dispositions in [source-consumers.md](reports/source-consumers.md).
Shared schema/generator inputs and the plan have one serial integration owner.

- `tools/standards_engine/contracts/{a1-contract.schema.json,a1-interface.toml,examples/a1-examples.json,generated/agent-tools.json}`;
  `tools/standards_engine/standards_engine/_generated_contract.py` via generation.
- `tools/standards_engine/standards_engine/{routing_inputs.py,agent_navigation.py,context_projection.py,engine.py}`.
- `tools/standards_applicability/standards_applicability/core.py` and direct tests,
  limited to shared required-name lookup if that is needed; no new binding semantics.
- The direct callers, transport/fixture tests and live operational guidance listed
  in the inventory; new focused binding and transport regression files.
- Existing input-feedback adapter only if a narrow focused-binding error projection
  is required. Do not change unrelated error taxonomies.
- This plan directory, `docs/plans/README.md` as a link-only index update, and the
  owning generated suite-input manifest. Do not alter closed-plan acceptance records.

**Work:** confirm current source/callers; capture literal baseline cases and current
catalogs; implement the vertical contract/binding/selection/continuation path; update
both purposes and native/query/preview consumers explicitly; update live tests and
fixtures; regenerate affected artifacts; run R-A1–R-A6 evidence. Qualify the initial
host schema/discovery path before expanding host-dependent machinery.

**Gate:** independent literal state tests plus differential cases, real cold stdio
and no-extra-capture/compile checks, unchanged native and retained-state behavior,
current locked CI and generated freshness. Old focused input must fail usefully.

### R2 — Live agent comparison and accepted cutover

**Status:** `Planned`; depends on the coherent R1 candidate.

**Goal:** establish the externally meaningful reduction in construction burden and
complete review/acceptance without a new feature slice.

**Allowed write set:** existing qualified host's single registration only if needed
for installation/restart (no new flag); the existing navigation qualification harness
and its current fixtures; this plan's evidence, issue and lifecycle records; generated
verification inputs affected by those records. Source repairs are confined to R1's
boundaries unless their meaning triggers re-planning.

**Work:** run matched fresh navigation tasks through connected tools; observe correct
values, omitted facts, absent/null/false distinctions, incremental answers, page and
explanation reuse, alias failures and useful repairs. Preserve observations and
independent review. The acceptance owner dispositions findings and current evidence.
No model standards mutation is invented for this navigation task.

**Gate:** R-A7/R-A8 satisfied and all other claims have the required fidelity. Select
review-packet work only after this scope's normal completion; its future automation
is not a circular prerequisite to this acceptance.

## Evidence and oracle plan

Use literal expectations for omitted/unknown/absent and `exists`; current schema-
bound validation for types and domains; independently derived expected selected
modules/rule truth for representative Router scenarios; and the exact baseline for
serialization/authority equivalence where preservation is intended. A converter
roundtrip alone is not proof of semantic preservation.

Include the whole state/type matrix, aliases and canonical collisions, nullable
versus absent versus empty, booleans versus numbers, unknown IDs, wrong scalar/set
types, empty strings according to existing contracts, duplicate elements, Unicode
normalization, extra marker fields and old typed envelopes. Type interpretation must
change when the **selected** snapshot changes, not when unrelated live files change.
Use the existing error/data-redaction owner; test application denials independently
of authoring diagnostics.

Native query/preview tests must retain canonical fixtures rather than blindly
replacing every occurrence of `facts` in the repository. Change only focused
callers. Prove a real cold baseline-produced workflow remains readable without
migration/publication. Compare bindings and result meaning; enumerate the intentionally
changed focused `.facts`/continuation fields rather than claiming all result bytes
are unchanged. Verify final lifecycle invalidation still discards content pages.

Use the existing supported locked environment/CI. The current workflow runs Python
3.12; do not claim 3.11 evidence or change the matrix/lock as a side effect of this
plan. Independent review is for this coherent new slice, not a re-review of the
already accepted six-slice sequence. Tests for this feature are required now;
priority 3 only defers broader unrelated test hardening.

## Blockers

The source candidate is locally verified. Supported-runtime CI and actual host/model
behavior and independent review remain unqualified; their owner and procedure are
R2/integration. The missing environment cannot be
silently marked passed. Source and static planning checks do not claim R-A7.

## Re-Plan Triggers

Re-plan if the real fact domain requires object/numeric values; a supported client
cannot use the selected map/state shape and discovery; a consumer requires an
independent overlap period; static-to-semantic error moves cannot remain safe and
useful; a retained-state/public promise outside focused routing must change; or
implementation requires a second validator, mutable session, registry or broader
Engine redesign. A newly found direct caller inside the same invariant is added to
the write set, not an automatic restart of the design. Preserve explicit failure
meaning and uncertainty rather than shipping a permissive fallback.

## Final Acceptance

Source implementation and local verification are complete. R-A3–R-A5 have the
requested local/real-process evidence. R-A1/R-A2/R-A6 still require supported locked
CI; R-A7/R-A8 require actual host/model evidence and independent review/owner
disposition. See the verification report rather than substituting baseline CI or
planning probes. Preserve original failures and repaired candidate evidence.
Use ordinary repository branching/commit/review rules; no prescribed commit count,
retrospective PR or history rewrite is part of this plan.

After R1/R2 acceptance, the user's next priority is **review-evidence packaging**;
then **targeted test strengthening**. Neither is implemented or admitted as a source
slice here, and neither reopens the closed six-slice refactoring.

- Acceptance status: `partial`
- Final status: `Verifying`
