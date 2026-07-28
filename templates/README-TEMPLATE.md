# [Boundary Name]

Use this template only after
[the Documentation Workflow](../workflows/documentation.md) selects a
`boundary-readme` or `contract-readme`. Delete instructions and optional
sections that do not apply.

## Purpose

State why this boundary exists and what system behavior depends on it.

## Responsibility

State the behavior and state owned here. Name important exclusions when they
prevent ownership ambiguity.

## Invariants

- A concrete condition that must remain true.
- A second condition only when it adds information.

## Entry Points

- `path/or/symbol` - Why callers or maintainers start here.

## Decision Links

Delete this section when no canonical decision or contract applies.

- `docs/adr/ADR-XXX-title.md` - Accepted rationale affecting this boundary.
- `path/to/contract.md` - Canonical consumer or producer contract.

Link the owner of accepted rationale. Do not repeat its alternatives and full
decision history here.

## Consumer Contract

Include only for a public, process, language, persistence, or generated
boundary consumed outside this owner.

- Inputs and validation:
- Outputs and stable semantics:
- Lifecycle, ordering, cancellation, and idempotency:
- Typed failures and retry behavior:
- Compatibility, versioning, migration, or coordinated replacement:
- Producer and consumer owners:
- Contract verification:

## Produced Contract

Include only when this boundary publishes machine-consumed data, configuration,
schemas, manifests, generated APIs, or persisted artifacts.

- Stable and intentionally volatile fields:
- Absence and default semantics:
- Enum, label, and ordering semantics:
- Persistence and compatibility:
- Regeneration or migration:
- Producer and consumer owners:
- Contract verification:

## Operations

Include only when this boundary owns non-obvious operator actions. Link a
runbook when the procedure needs preconditions, recovery, rollback, or detailed
validation.
