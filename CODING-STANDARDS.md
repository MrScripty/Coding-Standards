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

## Disabled Features

When disabling functionality due to bugs or incomplete implementation:

### Documentation Requirements

```markdown
Status: DISABLED

Reason:
Incremental rebuild produces corrupted indices when concurrent writes overlap
with the rebuild window.

Tracking:
Issue #42 - Fix concurrent index rebuild corruption.

Conditions for Re-enabling:
1. Implement write-ahead locking during rebuild.
2. Add integrity check after each incremental pass.
3. Pass stress test with concurrent writes during rebuild.

Workaround:
Full rebuild runs nightly via scheduled task.
```

### Config Pattern

Keep the disabled default close to the documented feature flag and reference the
reason from the configuration site.

### Unimplemented Stubs

Do not commit stub functions that accept requests and return empty or dummy
data. Stubs silently violate the caller's expectations and are difficult to
distinguish from working code.

```text
BAD: Registering a handler that returns empty or dummy data.
GOOD: Do not register the route until it is implemented.
```

**If a placeholder is truly needed** (e.g., for integration testing), use the
[Disabled Features](#disabled-features) pattern: document the reason, create a
tracking issue, and specify re-enabling conditions.

### Review Checklist

Before merging code that disables features:

- [ ] Reason documented in code
- [ ] Issue created for tracking
- [ ] Re-enabling conditions specified
- [ ] Workaround documented if applicable

## License Attribution

When adapting algorithms or code from other projects:

### Attribution Format

```text
Priority Queue with Decrease-Key
Adapted from: <project name> (<source URL>)
License: MIT/Apache-2.0
Copyright: <copyright holder>
Source file: <source path>

Modifications:
- Simplified API for single use case.
- Added project-specific key type.
- Integrated with project's graph representation.
```

### License Compatibility

Before adapting code, verify license compatibility:

| Source License | Can Use In | Notes |
|---------------|------------|-------|
| MIT | Any project | Attribution required |
| BSD | Any project | Attribution required |
| Apache 2.0 | Any project | Patent grant included |
| GPL | GPL projects only | Viral license |
| LGPL | Any (with care) | Dynamic linking usually OK |

### File-Level Attribution

For files with significant adapted code:

```text
Graph Processing Engine

Attribution:
- <project> (<license>) - <adapted component>
- <project> (<license>) - <adapted component>

See individual functions for specific attributions.
```

## Language-Specific Guidelines

Rust-specific coding rules live in
[languages/rust/RUST-API-STANDARDS.md](languages/rust/RUST-API-STANDARDS.md),
[languages/rust/RUST-UNSAFE-STANDARDS.md](languages/rust/RUST-UNSAFE-STANDARDS.md),
and the broader [Rust standards index](languages/rust/RUST-STANDARDS.md).

New or substantially expanded language-specific guidance should follow the same
pattern: keep the root standard focused on cross-language principles, then link
to `languages/<language>/` for toolchain-specific details. Existing inline
ecosystem sections can be migrated incrementally.

## TypeScript-Specific Guidelines

### Explicit Return Types on Public Functions

Functions that form part of an API surface (exported, called across modules)
must declare their return type. This catches accidental changes at the
definition site rather than propagating `any` to callers.

```typescript
// BAD: Inferred return type — callers don't know what to expect
export async function getTimeline() {
    return request('/api/timeline');
}

// GOOD: Explicit return type — contract is clear
export async function getTimeline(): Promise<Timeline> {
    return request('/api/timeline');
}
```

Private helpers and inline callbacks may rely on inference when the type is
obvious from context.

### Contract Types for API Boundaries

When calling external APIs, define types that match the expected response
shape and use them to type API functions. Don't pass raw `string` or `any`
where a domain type exists.

```typescript
// BAD: Untyped parameters accept anything
export function createArc(name: string, type: string) { ... }

// GOOD: Domain types enforce valid values
export function createArc(name: string, type: ArcType) { ... }
```

This ensures the compiler catches mismatches (like `'a_plot'` vs `'APlot'`)
at build time rather than at runtime.

### Frontend-Specific Standards

For frontend rendering, state synchronization, hook timer management, UI
testing practices, and React-specific tooling notes, see
[FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md).

## Performance-Critical Code

### Documentation

Mark hot paths explicitly:

```markdown
Process all pending events in the current frame.

# Performance
Hot path: called once per frame in the main loop.

## Optimizations Applied
- Pre-allocated scratch buffers.
- Batch transformations.
- Early-out for empty event queues.

## Benchmarks
Target: less than 1 ms for 10K events.
```

### Guidelines

1. **Profile before optimizing** - Measure, don't guess
2. **Document optimizations** - Future maintainers need context
3. **Benchmark critical paths** - Automated regression detection
4. **Avoid allocations in hot paths** - Use pre-allocated buffers

```text
BAD: Allocate a new result buffer on every hot-path call.
GOOD: Reuse caller-owned or pooled buffers where measurement proves it matters.
```

### When to Optimize

Optimize when:

- Profiling shows this is a bottleneck
- Code is called in hot loops (per-frame, per-item)
- Memory allocation is measurably impacting performance

Don't optimize when:

- Code runs once at startup
- Code is not on the critical path
- Readability would suffer significantly
