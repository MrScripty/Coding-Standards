# Routing Input Design Comparison

Status: planning evidence only. Baseline `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`
(interface 44). The prototype is outside the repository and uses the real current
binder/evaluator and Router on an in-memory snapshot; it is not a released or
integrated implementation. Source remains unchanged.

## Alternatives

| Candidate | Decision | Reason |
| --- | --- | --- |
| Keep the full per-fact `{type,state,value}` envelope | Baseline for comparison | Precise canonical shape, but repeats schema-owned type and the common known state at every call. |
| Raw known values only | Declined | Cannot represent explicit known absence without conflating it with null or omission. |
| `known_facts` plus `absent_facts` and `unknown_facts` buckets | Declined for this scope | Adds bucket names and a cross-bucket collision mechanism for the same fact/alias. No current consumer requires that separation. |
| Raw known values plus minimal nonknown state objects, in one `facts` map | Selected | One name-to-assertion grammar, all current states/types preserved, no redundant type choice, no cross-bucket overwrite rule. |
| Interpret prose or infer unanswered categories | Out of scope | Changes epistemic/authority semantics rather than representation. |
| Add a mode flag or silently accept old and new envelopes | Declined | Adds live dual-shape behavior without an admitted independent deployment overlap. |

The selected form reserves an object only for `{"state":"known-absent"}` or
`{"state":"unknown"}`. Known values are boolean, null, string or unique string
array; actual admissibility comes from the selected fact definition. A raw string
`"unknown"` is still data. Numeric and arbitrary object facts are not currently
supported. This is a closed current-domain decision, not a general-purpose JSON
value convention.

## Canonical semantics exercised

The schema fixture independently declares boolean, enum, string, string-set,
enum-set and canonical-id facts, including nullable facts and aliases. Twenty-one
inputs per type give **126 cases**: 33 valid bound results and 93 final rejections.
The prototype agrees with the existing typed shape plus canonical binder on final
validity, and on exact canonical values for every successful binding.

This is not a 126-test production suite. The same semantic binder is deliberately
reused. Separate literal `exists` expectations distinguish semantic states:

| Case | Expected `exists` |
| --- | --- |
| Omitted | unknown |
| Explicit unknown marker | unknown |
| Known-absent marker | false |
| Known false boolean | true |
| Known empty set | true |
| Known nullable null | true |

A canonical name and alias supplied together reject even if values agree. An alias
alone binds to its canonical name. The same raw `mode: "x"` is valid against an enum
schema and invalid against a boolean schema with that name; the schema digest and
selected definition decide, not JSON-type guessing.

Six real Router examples execute after lowering and canonical roundtrip using the
same captured authority. Canonical facts, selected modules, unresolved questions,
status and complete existing Engine results agree. This does not implement the new
result projection or prove application-purpose qualification, cold continuations,
new error mapping, lifetime behavior or model success. Those are R1/R2 checks.

## The important failure-stage consequence

**41 cases have different static-stage acceptance**: the original envelope tells
its static schema which type to enforce, whereas the new raw union must wait for
the registered fact type. Example: a raw string is a legal generic assertion shape
but is wrong for an enum-set fact. Final validity must remain rejection with useful
feedback after snapshot binding. Conversely, malformed state objects are rejected
by the new static grammar rather than guessed as values.

This is why merely swapping a `$ref` in RouteCall is insufficient. The implementation
must bind through applicability before passing a validated FactSet to selection;
it must not create an invalid generated canonical request and leak a ContractError.
Application permission/qualification must still precede private fact interpretation.
The plan deliberately does not claim identical old/new parser stages for a changed
public syntax. It requires equal semantics and explicitly specified typed failure
boundaries.

## Size observations

All measurements are ordinary `json.dumps` UTF-8 byte counts using the same
serializer. These request figures include the `facts` member but omit an identical
snapshot handle and unchanged detail/content arguments on both sides.

| Known/explicit facts | Baseline request | Proposed request | Change |
| --- | ---: | ---: | ---: |
| None | 13 | 13 | 0 |
| Implementation activity plus known-empty application category | 179 | 81 | -54.75% |
| Eight explicitly empty category sets | 612 | 220 | -64.05% |
| Eight categories with implementation and IPC values | 633 | 241 | -61.93% |
| Explicit unknown activity | 75 | 55 | -26.67% |
| Explicit absent activity | 80 | 60 | -25.00% |

The eight-empty-set example is **not** a recommendation to mark real unanswered
categories empty. No content was omitted from policy reads and no unanswered fact
was auto-filled. In the two-known-fact example all six unanswered categories remain.

The schema-only prototype modifies three existing focused field references
(RouteCall, CompactRouteResult, AgentRouteResult) and adds two assertion definitions.
It compiles through the current contract generator in memory, including Python
projection generation. No generated repository file is replaced.

| Catalog | Current tool-array JSON | Schema-only proposed JSON |
| --- | ---: | ---: |
| Authoring, eager | 713,206 | 711,534 |
| Authoring, on-demand | 108,812 | 107,962 |
| Application, eager | 83,735 | 82,035 |
| Application, on-demand | 15,955 | 15,105 |

The route's standalone input schema changes from **2,475 to 1,625 bytes**. Tool counts
remain 23/10 for focused authoring/application. These are not a final implemented
catalog: necessary descriptions and diagnostics have not been installed. Output
schema duplication and on-demand policy are unchanged. Do not promise these exact
final totals, model-context savings, billing reductions or latency gains.

## What the experiment does not establish

It does not validate a deployed schema renderer, prove fewer model turns, preserve
newly implemented transport exceptions, test every malformed string/unicode input,
qualify application permission paths, or prove saved-request rollout. The production
proposal has no integrated candidate yet. Baseline CI does not qualify it.

The script's small error-construction branch is explicitly prototype-only. The
implementation must share required fact-name lookup/error ownership with the
existing schema binder rather than copy that branch into production.

Exact script/results, source identity and current Router readback are under
[evidence](evidence/comparison.json). Run the script from the pinned checkout using
`PYTHONPATH=.` and an explicitly chosen new output directory. It uses local in-memory
snapshot state; it does not submit a standards proposal or contact a model provider.
