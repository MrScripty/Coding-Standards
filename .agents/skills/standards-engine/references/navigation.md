# Navigation And Analysis

Use this workflow for immutable reading. Request shapes come from the generated
contract; inspect them with `invoke.py --example <operation>` and
`invoke.py --schema <operation>`.

## Snapshot-Bound Reading

1. Call `create_snapshot` and retain the returned `snapshot` handle. A snapshot
   captures the current canonical Git revision and all authority needed for
   later reads; it is not the live worktree.
2. Call `query` with that handle and one request:
   - `route` selects the directly applicable standards and required closure
     from explicit facts;
   - `read` returns one canonical standard by logical ID;
   - `related` traverses an allowed relationship group and direction.
3. Use returned inspect operations and handles when more detail is needed.
   `inspect` accepts opaque handles; it does not accept repository locators.

A `read-result` includes its complete related projection and can be large. For
a graph question, issue `related` directly. For policy text, retain the result
in task-owned scratch state and select its `content` and `policy` fields rather
than loading unrelated relationship rows into the working context.

For a non-standard relationship consumer, `related` may return an
`authoring-target-handle`. Preserve that whole Snapshot-bound handle for a
later explicit relationship edit.

Use `find_snapshots` to resume a known lifecycle. Delete or undelete a snapshot
only when the user requested that lifecycle change; deletion does not authorize
standards mutation.

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
