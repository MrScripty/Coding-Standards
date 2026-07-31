# Coding Standards Legacy Index

> **Migration authority:** [CORE-STANDARDS.md](CORE-STANDARDS.md) is canonical
> for universal simplicity, ownership, boundary, failure, lifecycle, and change
> integrity rules. This file remains canonical only for detailed coding topics
> not yet moved. Conflicts for moved rules resolve to Core.

This file is a migration index for detailed coding topics not yet moved.
Universal simplicity and ownership are canonical in
[Core](CORE-STANDARDS.md#simplicity-and-ownership).

Architecture authority is canonical in
[Architecture](topics/architecture.md). This legacy index does not define file,
layer, service, data/state ownership, dependency-direction, or composition
policy.

Constants and configuration authority is canonical in
[Core](CORE-STANDARDS.md#semantic-constants-and-configuration).

## Error Handling Legacy Route

Failure handling and diagnostic authority is canonical in
[Resilience](topics/resilience.md#failure-boundaries-and-diagnostics).


## Boundary Validation Legacy Route

Inbound and outbound validation authority is canonical in
[Contracts](topics/contracts.md#inbound-and-outbound-boundary-proof).

## Dependency Management Legacy Route

Dependency requirement, ownership, selection, resolution, provisioning,
update, and removal authority is canonical in
[Dependencies](topics/dependencies.md).

## Code And Naming Legacy Route

Code volume, abstraction, duplication, deletion, naming, and terminology
authority is canonical in
[Core](CORE-STANDARDS.md#code-and-terminology-discipline).

## Invariants And Safety Legacy Route

Invariant, precondition, postcondition, and enforcement authority is canonical
in [Contracts](topics/contracts.md#invariant-contracts). Verification evidence
is selected by the
[Verification workflow](workflows/verification.md#selecting-claims).

## Disabled Features Legacy Route

Disabled, removed, and incomplete behavior lifecycle authority is canonical in
the [Implementation workflow](workflows/implementation.md#disabled-and-incomplete-behavior).
Acceptance evidence is selected by the
[Verification workflow](workflows/verification.md#disabled-behavior-claims).

## License Attribution Legacy Route

Third-party provenance, license compatibility, obligation, attribution, and
distribution authority is canonical in [Licensing](topics/licensing.md).

## Language-Specific Guidelines Legacy Route

Select language mechanism guidance from the
[Language Profiles](STANDARDS-ROUTER.md#language-profiles) table. Generic
policy remains in Core, workflows, and topics.

## TypeScript-Specific Guidelines Legacy Route

TypeScript mechanism guidance is canonical in the
[TypeScript profile](profiles/languages/typescript.md). Async concurrency
mechanisms additionally use the
[TypeScript Async profile](profiles/languages/typescript/async.md).

## Frontend Standards Legacy Route

Frontend projection, rendering, synchronization, interaction, and
frontend-specific evidence are canonical in the
[Frontend application profile](profiles/applications/frontend.md).

## Performance Legacy Route

Performance claims, measurement contracts, optimization decisions, benchmarks,
and regression evidence are canonical in [Performance](topics/performance.md).
