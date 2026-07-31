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


### Validate at Boundaries

Validate input at system boundaries, not throughout the code:

```
// API boundary - validate here
function handleRequest(input: unknown): Response {
    const validated = validateInput(input);  // Throws if invalid
    return processValidatedInput(validated);
}

// Internal function - trust the input
function processValidatedInput(input: ValidatedInput): Result {
    // No need to re-validate
}
```

### Validate Outbound Responses

HTTP handlers must check the response status before treating the body as valid.
This applies to both client code consuming APIs and server code calling upstream
services.

```typescript
// BAD: Assumes response is always valid JSON
const data = await fetch('/api/items').then(r => r.json());

// GOOD: Check status before parsing
const res = await fetch('/api/items');
if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `HTTP ${res.status}`);
}
const data = await res.json();
```

**Why:** Without status checks, error responses (404, 500) are silently
deserialized as empty or malformed data, causing confusing downstream failures.

## Dependency Management

See [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) for comprehensive guidelines on
evaluating, versioning, auditing, and minimizing third-party dependencies.

## Code Style

### Code Volume Discipline

Use the smallest amount of code that clearly satisfies the required behavior.
Correct input-to-output behavior is the baseline; extra structure must earn its
place by improving correctness, clarity, maintainability, diagnostics,
performance, or an explicitly required extension point.

Prefer direct implementations when:
- the behavior has one or two call sites
- the requirements are stable and narrow
- a simple function or data transform expresses the rule clearly
- abstraction would mostly move code around instead of reducing real complexity

Verbose code is acceptable when it makes an objective improvement:
- preserving important domain language
- making error handling or validation explicit
- separating genuinely different responsibilities
- documenting non-obvious invariants through names and structure
- supporting multiple existing variants without complex parameterization

Do not add code volume for speculative future needs. Add structure when the
current requirements, current variants, or demonstrated maintenance risk justify
it.

### Avoid Over-Engineering

Only make changes that are directly requested or clearly necessary:

- Don't add features beyond what was asked
- Don't refactor surrounding code when fixing a bug
- Don't add comments to code you didn't change
- Don't add error handling for impossible scenarios
- Don't create abstractions for one-time operations

```
// BAD: Over-engineered for a single use case
class ConfigurableGreeterFactory {
    constructor(private config: GreeterConfig) {}
    create(): Greeter { ... }
}

// GOOD: Simple and direct
function greet(name: string): string {
    return `Hello, ${name}!`;
}
```

### Abstractions Must Reduce Reasoning Load

An abstraction is justified when it removes a real reasoning burden from callers
without hiding lifecycle, ordering, state ownership, failure behavior, or side
effects.

Avoid abstractions that merely hide complexity behind a smaller API while
forcing maintainers to understand the hidden behavior to make safe changes.

Before adding an abstraction, answer:
- What concern does this let callers ignore safely?
- What invariant does the abstraction preserve?
- What behavior remains intentionally visible?
- What future change becomes easier because this boundary exists?

### Don't Repeat Yourself (DRY)

When the same logic appears in multiple places, extract it into a shared
function or module. Duplicated code creates divergence risk — when one copy
is updated, the others are often missed.

```text
BAD: Same logic in two modules
     prompt/gather_surrounding(...)
     consistency/gather_surrounding(...)

GOOD: Shared helper
      shared/gather_surrounding_context(...)
```

**When to extract:**

- Two or more call sites with identical or near-identical logic
- The duplicated code serves the same purpose (not coincidental similarity)
- The extracted function has a clear name and single responsibility
- Prefer extraction once the second or third hook/service variant appears
  rather than allowing near-copies to diverge

**When duplication is acceptable:**

- Test setup code (clarity > reuse in tests)
- Two implementations that happen to look similar but serve different purposes
- Extraction would require complex parameterization that obscures intent

### Delete Unused Code

Remove speculative or expired compatibility code. Preserve a compatibility path
only when [the contract decision](topics/contracts.md) identifies a real
consumer and active support window.

```
// BAD: Keeping dead code for an unverified consumer
const _oldVariable = null;  // Unused, kept for "compatibility"
// removed: oldFunction()

// GOOD: Delete it after coordinated replacement or support-window expiry
// (nothing here - it's gone)
```

## Naming Conventions

### Be Descriptive

Names should explain what something is or does:

```
// BAD
const d = new Date();
function proc(x) { ... }
const temp = users.filter(u => u.active);

// GOOD
const createdAt = new Date();
function processPayment(payment) { ... }
const activeUsers = users.filter(user => user.active);
```

### Consistent Terminology

Use the same term for the same concept throughout the codebase:

```
// BAD: Inconsistent naming
getUserById()
fetchCustomerById()  // Same concept, different name
loadPersonById()     // Same concept, another name

// GOOD: Consistent
getUserById()
getOrderById()
getProductById()
```

## Invariants and Safety

### Documenting Invariants

For functions that must maintain data structure invariants, document them explicitly:

```markdown
Remove a node from the dependency graph and rewire edges.

# Invariants Maintained
- Graph remains acyclic.
- All nodes have at least one path to a root.
- Edge weights remain non-negative.
- In-degree counts stay consistent with actual edges.

# Preconditions
- Node has no dependents or all dependents have been reassigned.
- Node exists in the graph.
- Removal would not disconnect any subgraph from roots.

# Postconditions
- Node count reduced by exactly one.
- Edge count reduced by the removed node's connected edges.
- All remaining paths remain valid.
```

### Validation Strategy

| Build | Validation Level |
|-------|-----------------|
| Debug | Full validation, panic on violation |
| Release | Critical checks only, log and recover |

Use full validation in debug builds when it catches developer mistakes quickly.
In release builds, keep critical validation that protects data integrity and
prefer explicit errors, logging, or graceful aborts over silent corruption.

### Invariant Testing

Every invariant should have corresponding tests:

```text
test_remove_node_maintains_acyclic_invariant
test_add_edge_rejects_cycle
```

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
