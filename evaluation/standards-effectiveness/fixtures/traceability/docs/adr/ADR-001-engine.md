# ADR-001: Engine Policy

## Status

Accepted.

## Context

The engine fixture needs one policy owner.

## Decision

Keep policy decisions in the engine boundary.

## Alternatives

- A global policy was rejected because it obscures ownership.

## Consequences

Engine policy changes update this record.

## Affected Boundaries

- `boundary:engine`
