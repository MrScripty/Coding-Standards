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
