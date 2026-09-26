---
name: standards-engine
description: Maintain this repository's coding standards through an authoring-purpose Standards Engine connection. Use when an agent needs to route or read standards, inspect related policies, propose or revise a standards change, review or apply a proposal, verify standards, or recover an application; do not use for ordinary source-code edits.
---

# Standards Engine Authoring

This skill is maintenance material for standards authors. Ordinary application
agents use their application-purpose tool catalog and approved guidance, rather
than loading this authoring skill.

Use the generated public Interface. The Engine is the sole writer of standards
Markdown, metadata, supplementary projections, SQLite state, and local Git
publication. Supply domain intent and reuse opaque handles; never translate an
Engine request into direct file, SQL, or Git mutations.

## Use The Agent Tools

Use the `standards-authoring` MCP tools (or the host's explicitly configured authoring-purpose registration). The client supplies each operation's
current input schema; call the named tool directly with structured arguments.
Tool-name prefixes vary by client; operation names match the Engine contract
(for example, `route`, `read`, and `propose`).

Use `routing_facts` when the registered fact vocabulary is unknown. Use
`route` with explicit engineering facts, then `read_many` for the selected
exact policies in one call. Use `read` for one item and `related` for relationships.
Omit `snapshot` on the first call to capture
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
references immutable Engine records; preserve it unchanged. Act directly on
that result: another `analyze` or `workflow_status` call is normally unnecessary.
Use `workflow_status` for lightweight observation after reconnecting or an unknown
outcome. `resume` explicitly selects the current revision and returns a draft.

Inspect each result's `kind`. A `workflow-result` carries `status`, a compact
`outcome` summary by default, and Engine-derived `next_operations`. Successful
compact pending mutations also carry `work`; full diagnostic results remain
available through `detail: "full"`:

- `needs-action`: supply only the actual evidence or authorized decision named
  in a `workflow-work-page`'s `items`, using `resolve_many` with decisions ready for that exact
  context. Use `resolve_workflow` for one decision. Each result issues the
  successor context and work; newly revealed obligations belong to that round.
  Summary counts cover all work, while the inline page covers one section.
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

Focused action continuations inherit the enclosing result's `context` and name
remaining caller inputs. Supply that context once in the next call. For more
work, invoke `workflow_details` with `analysis` set to that context and the fields
from `work.next`. A `workflow-work-deferred` result preserves the successful
mutation and offers `work.request` for an explicit size-unbounded full-record
read; select it only when the client can receive it. A status observation has
counts but no inline work; choose the needed section through `workflow_details`.

A continuation's presence is not an authorization grant; the Engine revalidates
current state
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
