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
4. Use returned inspect operations and handles when more detail is needed.
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
