---
name: standards-engine
description: Navigate, analyze, and author this repository's coding standards through the Standards Engine. Use when an agent needs to route or read standards, inspect related policies, propose or revise a standards change, review or apply a proposal, or recover an application; do not use for ordinary source-code edits.
---

# Standards Engine

Use the generated public Interface. The Engine is the sole writer of standards
Markdown, metadata, supplementary projections, SQLite state, and local Git
publication. Supply domain intent and reuse opaque handles; never translate an
Engine request into direct file, SQL, or Git mutations.

## Invoke The Interface

Run from the repository root. The bundled transport reads one JSON object from
standard input and prints one structured Engine result:

```bash
printf '%s\n' '{"kind":"create-snapshot"}' |
  PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py create_snapshot
```

Discover the current contract rather than recalling fields:

```bash
PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py --list
PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py --example create_proposal
PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py --schema create_proposal
```

Contract discovery needs only Python 3.11 or newer. Engine invocation also
needs the repository's pinned Python dependencies. If the transport reports
that they are unavailable, read
[references/environment.md](references/environment.md); do not replace the
locked environment with guessed packages or versions.

Keep scratch request JSON outside the repository. Pass the complete result
handle from one operation into the next without constructing, shortening, or
editing its identity.

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

The skill transport opens the normal durable Engine store and cannot create
authorization. `review_proposal`, `apply_proposal`, and
`recover_application` succeed only when the host composition root binds the
required current authorization adapter. Treat
`ANALYSIS.AUTHORIZATION_UNAVAILABLE`, `ANALYSIS.UNAUTHORIZED`, and
`ANALYSIS.AUTHORIZATION_UNSUPPORTED` as stopping outcomes; test authorizers are
not production credentials.

## Choose The Workflow

- For routing, reading, relationship discovery, or accepted-snapshot Analysis,
  read [references/navigation.md](references/navigation.md).
- For any proposal, revision, review, application, or recovery, read
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
