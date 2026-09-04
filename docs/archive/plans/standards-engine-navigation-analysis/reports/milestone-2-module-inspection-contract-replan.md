# Milestone 2 Module Inspection Contract Replan

## Trigger

The accepted route and read examples use canonical module IDs such as
`profile.boundary.persistence`. The A1 contract intentionally permits partial
policy-unit coverage and conservative whole-artifact scope, but its inspection
result could represent only `PolicyUnitDeclaration`.

## Decision

Add a derived `CanonicalModuleDeclaration` and permit policy inspection to
contain exactly one of:

- a canonical module declaration derived from `standards_metadata`; or
- an authored policy-unit declaration loaded from the explicit sidecar registry.

The existing `PolicyHandle` remains the common snapshot-bound handle. Its ID is
resolved before inspection, and the declaration's discriminating `kind`
identifies the authority class without caller interpretation.

Canonical module declarations expose IDs, role, level, applicability,
exclusion, Requires, Specializes, and verification text. Repository paths and
canonical-owner locators remain internal provenance and are available only
through explicit inspection.

## Version Decision

Retain contract version 1 because this corrects an omission before any runtime
type, agent-tool projection, or external serialized value exists. Record the
decision in the ADR. Once a runtime projection is accepted, adding or changing
a declaration variant requires explicit contract-version migration.

## Rejected Alternatives

| Alternative | Rejection |
| --- | --- |
| Read only registered policy units | Breaks accepted Router-to-module navigation and whole-artifact scope. |
| Populate policy units for every module | Adds broad semantic identity and audit work unrelated to read-only navigation. |
| Synthesize policy-unit declarations | Invents semantic revisions and stable identity authority not present in sidecars. |
| Return paths instead of declarations | Exposes repository topology and bypasses canonical IDs. |

## Acceptance

- Module and policy-unit declaration examples validate as distinct variants.
- A module read and inspection use whole-artifact scope and derived metadata.
- A policy-unit read and inspection use structured scope and authored identity.
- Unknown, retired, stale-snapshot, and cross-snapshot requests return typed
  rejection rather than falling back to paths or ambient repository state.

## Relationship Identity Clarification

The first runtime relationship projection exposed that registered graph edge
IDs and canonical policy IDs have different grammars. For example,
`metadata-requires:workflow.planning->core` is an accepted stable graph edge ID
but `>` is intentionally absent from canonical module and policy IDs.

Version 1 therefore defines `EdgeId` as a non-empty registered graph identity
and uses it for relationship handles and edge selection provenance. The engine
still resolves every supplied edge ID through the exact graph registry. This
does not authorize inferred relationships or weaken canonical policy identity.
