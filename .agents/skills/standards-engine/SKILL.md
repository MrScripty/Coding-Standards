---
name: standards-engine
description: Navigate, analyze, and author this repository's coding standards through the Standards Engine. Use when an agent needs to route or read standards, inspect related policies, propose or revise a standards change, review or apply a proposal, verify standards, or recover an application; do not use for ordinary source-code edits.
---

# Standards Engine

Use the generated public Interface. The Engine is the sole writer of standards
Markdown, metadata, supplementary projections, SQLite state, and local Git
publication. Supply domain intent and reuse opaque handles; never translate an
Engine request into direct file, SQL, or Git mutations.

## Use The Agent Tools

Use the `standards-engine` MCP tools. The client supplies each operation's
current input schema; call the named tool directly with structured arguments.
Tool-name prefixes vary by client; operation names match the Engine contract
(for example, `route`, `read`, and `propose`).

Use `routing_facts` when the registered fact vocabulary is unknown. Use
`route` with explicit engineering facts, `read` for exact policy, and
`related` for relationships. Omit `snapshot` on the first call to capture
accepted authority; reuse the returned snapshot on subsequent calls. Omission
always captures a new snapshot, so carry the handle when continuing a task.
Compact reads preserve exact policy text and essential authority. Select
`detail: "full"` only when the complete relationship projection is needed.
Route from known facts; obtain missing facts instead of inventing applicability.
Natural-language interpretation remains the calling agent's responsibility.

If the tools are unavailable, read
[references/environment.md](references/environment.md) for MCP setup. The
Python CLI remains a debugging/reference transport, not the normal skill
workflow. An unavailable tool connection does not authorize direct standards
mutation.

For authoring, `propose` and `revise` automatically analyze the exact new
revision. Carry the returned `context` into subsequent workflow calls. It
references immutable Engine records; preserve it unchanged. `workflow_status`
reconstructs that exact state after reconnecting. `resume` explicitly selects
the current proposal revision and returns a draft context.

Inspect each result's `kind`. A `workflow-result` carries `status`, the native
`outcome` when applicable, and Engine-derived `next_operations`:

- `needs-action`: supply only the actual evidence or authorized decision named
  in `outcome`, using `resolve_workflow` and the current context.
- `complete`: review is possible only with explicit evidence-backed acceptances.
- `requires-change`: revise the proposal; do not treat completed analysis as
  approval of its content.
- `ready`: `apply` verifies and locally publishes the exact accepted context
  only when the user's authorization covers application.
- `recovery-required`: use `recover` with the same context. Do not repeat apply,
  infer publication, or repair Git manually.
- `stale`: inspect the historical result or explicitly `resume`; never replace
  a reviewed revision implicitly.
- `rejected` or a top-level `rejected-result`: report the exact code/outcome and
  follow supported continuations. An unavailable tool or authority is not
  permission to mutate standards directly.

A continuation supplies bound `context` and names remaining caller inputs. Its
presence is not an authorization grant; the Engine revalidates current state
and authority on every action. Transport failure after a mutation has an unknown
outcome. For interrupted application, retain the readiness context and inspect
`workflow_status` to obtain the supported recovery continuation.

The default MCP catalog exposes focused tools. Native snapshot administration,
accepted-snapshot Analysis, verification preflight, and evidence maintenance
remain available through the explicit advanced catalog; see
[references/environment.md](references/environment.md).

## Choose The Workflow

- For routing, reading, relationship discovery, or accepted-snapshot Analysis,
  read [references/navigation.md](references/navigation.md).
- For proposal edits (including routing), verification, review, application,
  or recovery, read
  [references/authoring.md](references/authoring.md) before the first authoring
  call.

Review and apply are privileged mutations. The user's request and the bound
authorization authority must both cover the exact operation. Engine application
ends at the configured local canonical ref; remote publication is a separate,
out-of-scope action.

Completion means the requested structured result has been inspected, every
pending or recovery state is either resolved or reported with its exact typed
outcome, and no caller-owned standards-file, SQLite, index, object, or ref
mutation was used.
