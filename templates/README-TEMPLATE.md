# [Directory Name]

Brief one-line description of the responsibility this directory owns.

## Purpose

One paragraph explaining:
- What this directory is responsible for
- Why this boundary exists (not another location)
- Which system behavior depends on this module

## Contents

| File/Folder | Description |
|-------------|-------------|
| `main-entry.ts` | Why this artifact exists and what callers rely on |
| `policies/` | Why this folder is separate and what invariant it protects |

List key artifacts only (typically 3-7). Do not list every file unless the
directory is very small and each file is externally relevant.

## Problem

What system-level problem this directory solves, including who/what is impacted
if this module fails.

## Constraints

List the constraints that shaped the implementation:

- Performance, latency, memory, or throughput limits
- Compatibility or migration constraints
- Product or UX constraints

## Decision

State the chosen approach and why it best satisfied the constraints.

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

What other parts of the codebase this directory depends on and why:

- `../other-module` - Why this dependency exists

### External

Third-party libraries used and why:

- `library-name` - What it's used for

## Related ADRs

- `ADR-00X` - Brief description
- Or: `None`

## Usage Examples

```typescript
// Real usage example that matches current public entry points.
import { createWorkflowRuntime } from './index';

const runtime = createWorkflowRuntime(config);
await runtime.start();
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
