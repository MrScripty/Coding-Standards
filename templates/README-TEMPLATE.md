# [Directory Name]

Brief one-line description of what this directory contains.

## Purpose

One paragraph explaining:
- What this directory is responsible for
- Why it exists as a separate directory
- What problems it solves

## Contents

| File/Folder | Description |
|-------------|-------------|
| `example.ts` | Brief description of what this file does |
| `subfolder/` | Brief description of what this folder contains |

## Problem

What system-level problem this directory solves.

## Constraints

List the constraints that shaped the implementation:

- Performance, latency, memory, or throughput limits
- Compatibility or migration constraints
- Product or UX constraints

## Decision

State the chosen approach and the rationale.

## Alternatives Rejected

Capture the main alternatives and why they were rejected:

- **[Alternative 1]:** Why rejected
- **[Alternative 2]:** Why rejected

## Invariants

List conditions that must remain true for this module to be correct:

- Invariant 1
- Invariant 2

## Revisit Triggers

List concrete events that should trigger re-evaluation:

- Trigger 1
- Trigger 2

## Dependencies

### Internal

What other parts of the codebase this directory depends on:

- `../other-module` - Why this dependency exists

### External

Third-party libraries used:

- `library-name` - What it's used for

## Related ADRs

- `ADR-00X` - Brief description
- Or: `None`

## Usage Examples

```typescript
// Example of how to use the main exports from this directory
import { Something } from './index';

const result = Something.doThing();
```

## Testing

How to run tests for this directory:

```bash
npm test -- --grep "directory-name"
```

## Notes

Any additional context, gotchas, or important information:

- Note 1
- Note 2
