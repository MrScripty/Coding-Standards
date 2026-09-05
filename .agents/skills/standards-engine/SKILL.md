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
(for example, `create_snapshot`, `query`, and `create_proposal`).

Use `route` with explicit engineering facts, `read` for exact policy, and
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

Inspect every returned `kind`:

- A success result advances the workflow using only its returned handles.
- A `pending-result` is an immutable Analysis state. Follow its projected work
  and `next_operations`, then submit the requested evidence or disposition with
  `resolve`.
- A `rejected-result` is a domain outcome. Follow its `next_operations` when
  present; otherwise report the code and outcome. Preserve the Engine boundary
  instead of bypassing rejection with repository edits.
- An `application-recovery-required-result` advances only through
  `recover_application` using the same readiness handle. Do not repeat apply,
  infer publication, or repair Git manually.

The MCP transport opens the normal durable Engine store with the repository's
owner-operated, in-process always-allow authorizer. It authorizes each exact
request and records local authorization and revocation evidence; no external
authorization service or session token is required. Low-level Engine callers
may deliberately supply another authorization adapter or none. Treat
`ANALYSIS.AUTHORIZATION_UNAVAILABLE`, `ANALYSIS.UNAUTHORIZED`, and
`ANALYSIS.AUTHORIZATION_UNSUPPORTED` from such a caller as stopping outcomes.

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
