# Navigation And Analysis

Use this workflow for immutable reading. Request shapes come from the generated
MCP tool definitions supplied by the client; invoke the tools directly.

## Snapshot-Bound Reading

1. Call `route`, `read`, or `related`. Supply a retained `snapshot` to continue
   an existing task, or omit it to capture current canonical accepted authority.
   Snapshot capture reads the canonical Git revision, not the live worktree.
2. Reuse the complete returned `snapshot` in subsequent calls. Independent calls
   without that handle intentionally capture authority independently.
3. `route` selects applicable standards and required closure from explicit facts;
   `read` returns exact policy by canonical ID; `related` traverses explicitly
   selected permitted relationship groups and directions.
4. Request `content: {}` on `route` to receive the selected exact policies directly
   (see the bounded-content contract below). For an explicit subset instead,
   group the selected policies into `read_many` with the returned
   snapshot and ordered `items` such as `[{"target":"core"}]`. Select up to 32
   unique read items per call. The complete result is bounded to 2 MiB and any
   unavailable item rejects the whole group; narrow the selection on a limit.
   Grouping preserves the same exact text, authority and detail options as `read`.
5. Use returned inspect operations and handles when more detail is needed.
   `inspect` accepts opaque handles, not repository locators.

The default `read` result is compact: exact content, policy authority,
prerequisites, specialization, and continuations. Use `detail: "full"` for the
complete relationship projection or call `related` for a graph question.
`include_coverage` remains available when coverage status matters. The advanced
`query` operation retains its native request and complete-result behavior.

For a non-standard relationship consumer, `related` may return an
`authoring-target-handle`. Preserve that whole Snapshot-bound handle for a
later explicit relationship edit.

Use `find_snapshots` to resume a known lifecycle. Delete or undelete a snapshot
only when the user requested that lifecycle change; deletion does not authorize
standards mutation.

## Bounded Content With Routing

Focused `route` accepts optional `content: {"limit": 8, "offset": 0}` in both
purposes. Omission preserves selection-only behavior; `{}` requests the first
page with defaults. A page contains up to 32 exact compact reads in the route's
selected, deduplicated target order. `content.total` counts all selected targets;
`content.offset` identifies this page. Follow `content.next` as the entire next
`route` request, preserving its facts and snapshot. Nonzero offsets require an
explicit snapshot. Changing facts intentionally starts a different selection.

The complete route result, including its plan, questions, items and continuation,
is limited to 2 MiB. Byte pressure returns fewer whole reads. A first record that
cannot fit returns a typed limit rejection, never clipped policy text. Request a
selection-only route and explicitly `read` that target when the client can receive
it. An unavailable selected dependency or a failed read rejects the result;
partial prefixes are not returned as success. An offset equal to the selected
count returns an empty final page; a larger offset is invalid.

All content uses the same captured authority and ordinary read/qualification
rules. Missing facts remain unresolved even when selected text is returned.
Only the selected content is paged; the reading plan and questions remain complete.
Native `query` and candidate previews keep their existing request contracts.

## Explicit Facts And Routing Explanations

Call `routing_facts` to discover fact IDs, aliases, types, allowed values,
nullability, meaning, and prompts. Reuse its snapshot when routing. Supply a
`FactValue` for each known fact using the tool schema; enum-set values are arrays,
boolean values are booleans, and null is valid only for nullable definitions.
An explicit empty set or `known-absent` is different from an omitted/unknown fact.

Focused `route` returns canonicalized supplied `facts`, `reading_plan` causes,
selected or unresolved `rules` with their exact expressions, and typed
`unresolved_questions`. Each question carries its registered `fact` definition.
A rule expression describes evaluated applicability; it is not a semantic
explanation invented from policy prose. Required dependency reasons identify
their exact graph edge and source. Several reasons may select the same standard.

Supply only facts supported by the task. Unknown facts remain unresolved; a
route with unresolved questions is not proof that the selected set is complete.
Use returned definitions to request the missing engineering information, then
route again against the same snapshot. The advanced Router read with
`include_routing` remains available for explicit rule authoring.

## Accepted-Snapshot Analysis

Use the advanced MCP catalog for accepted-snapshot Analysis and snapshot
administration. The single-decision loop below applies to that native Analysis
API. Proposal workflows use focused contexts and `resolve_many` instead, as
specified in [authoring.md](authoring.md).

Use `prepare` only when comparing two accepted Snapshot handles. Supply the
explicit change descriptors required by its schema; proposal authoring instead
uses `analyze_proposal`, which derives those descriptors from the immutable
proposal.

`prepare` and `resolve` return either `pending-result` or `complete-result`.
For pending work:

1. inspect the projected requirements, obligations, and `next_operations`;
2. obtain the exact evidence or owner decision named by that state;
3. call `resolve` with the current Analysis handle and exactly one supported
   submission; and
4. continue until complete or a typed rejection makes progress unavailable.

Do not invent facts, semantic dispositions, coverage attestations, or
authorization. A complete result is evidence for its exact immutable Analysis
state only.

An `unmapped-normative-change` obligation means changed normative scope lacks
one exact registered policy-unit mapping, so Analysis requires an explicit
impact disposition for its conservative whole-artifact scope. It is not an
instruction to infer an impact decision.


## Input Discovery Is Not Standards Navigation

Use `describe_input` for argument shapes, not policy text. It observes only the
running purpose-qualified catalog and needs no snapshot. Application connections
can discover their own reviewed-guidance navigation inputs but cannot discover
unpublished authoring operations or definitions. `route`, `read`, and `related`
remain the owners of policy selection, text and relationships.
