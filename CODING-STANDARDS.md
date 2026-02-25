# Coding Standards

Generic coding conventions applicable to any tech stack.

## File Organization

### Maximum File Size

**Target: 500 lines per file**

When a file exceeds 500 lines:
1. Identify logical groupings within the file
2. Extract related functionality into separate files
3. Use clear naming that reflects the extracted responsibility

**Why:** Large files are harder to navigate, review, and test. Smaller files encourage single-responsibility design.

### Directory Structure

Directories with 3+ files or non-obvious purpose should contain a `README.md` explaining:
- Purpose of the directory
- What files it contains
- How it relates to other directories

See [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) for the template.

## Layered Architecture

Organize code into distinct layers with clear responsibilities:

```
┌─────────────────────────────────────┐
│  Presentation Layer (Views/UI)      │  User-facing components
├─────────────────────────────────────┤
│  Controller Layer (Orchestration)   │  Coordinates between layers
├─────────────────────────────────────┤
│  Service Layer (Business Logic)     │  Core domain logic
├─────────────────────────────────────┤
│  Model Layer (Data Structures)      │  DTOs, entities, types
├─────────────────────────────────────┤
│  Infrastructure Layer (External)    │  APIs, databases, file I/O
└─────────────────────────────────────┘
```

### Layer Rules

| Layer | Can Depend On | Cannot Depend On |
|-------|---------------|------------------|
| Presentation | Controllers, Models | Services directly, Infrastructure |
| Controllers | Services, Models | Infrastructure directly |
| Services | Models, Infrastructure interfaces | Presentation, Controllers |
| Models | Nothing | Any other layer |
| Infrastructure | Models | Services, Controllers, Presentation |

### Why Layering Matters

- **Testability:** Services can be unit tested without UI or database
- **Flexibility:** Swap infrastructure without changing business logic
- **Clarity:** Clear ownership of responsibilities

## Separation of Concerns

### Backend-Owned Data Principle

When building client-server applications:

**The backend is the single source of truth.**

Frontend/client can hold:
- Transient UI state (hover, focus, animation)
- Pending user input (before submission)
- Drag/drop state
- Local preferences

Frontend/client must NOT hold:
- Business data
- Selection state affecting business logic
- Configuration that affects behavior
- Anything that needs to survive a page refresh

**Data Flow:**
```
Backend (source) ──push──▶ Frontend (display)
     ▲                          │
     └────── user action ───────┘
```

**No Optimistic Updates:** Wait for backend confirmation before updating UI state.

### Service Independence

Services should be framework-agnostic:

```
// BAD: Service depends on framework
class UserService {
    save(user: User) {
        FrameworkContext.getCurrentUser();  // Framework coupling
    }
}

// GOOD: Service receives dependencies
class UserService {
    save(user: User, currentUserId: string) {
        // Pure business logic
    }
}
```

**Why:** Framework-agnostic services can be unit tested without mocking the entire framework.

## Constants and Configuration

### No Magic Numbers or Strings

Every literal value should be a named constant:

```
// BAD
if (retryCount > 3) { ... }
element.style.width = '200px';

// GOOD
const MAX_RETRIES = 3;
const PANEL_MIN_WIDTH = 200;

if (retryCount > MAX_RETRIES) { ... }
element.style.width = `${PANEL_MIN_WIDTH}px`;
```

### Centralize Constants

Group related constants together:

```
// constants/ui.ts
export const UI = {
    PANEL_MIN_WIDTH: 200,
    PANEL_MAX_WIDTH: 600,
    ANIMATION_DURATION_MS: 300,
    DEBOUNCE_DELAY_MS: 150,
} as const;

// constants/limits.ts
export const LIMITS = {
    MAX_FILE_SIZE_MB: 50,
    MAX_RETRIES: 3,
    REQUEST_TIMEOUT_MS: 30000,
} as const;
```

## Error Handling

### Exceptions for Exceptional Cases

Use exceptions only for truly unexpected situations:

```
// BAD: Using exceptions for control flow
try {
    user = findUser(id);
} catch (NotFoundError) {
    user = createDefaultUser();
}

// GOOD: Explicit handling
user = findUser(id);
if (!user) {
    user = createDefaultUser();
}
```

### Catch at Boundaries

Handle exceptions at system boundaries:
- API/IPC handlers
- Event handlers
- Entry points

Don't catch and re-throw without adding value:

```
// BAD: Pointless catch
try {
    doSomething();
} catch (error) {
    throw error;  // Adds nothing
}

// GOOD: Add context or handle
try {
    doSomething();
} catch (error) {
    logger.error('Failed during operation X', { error, context });
    throw new OperationError('Operation X failed', { cause: error });
}
```

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

```rust
// BAD: Assumes upstream always returns 200
let body: ApiResponse = client.get(url).send().await?.json().await?;

// GOOD: Check status
let res = client.get(url).send().await?;
if !res.status().is_success() {
    return Err(ApiError::upstream(res.status(), res.text().await?));
}
let body: ApiResponse = res.json().await?;
```

**Why:** Without status checks, error responses (404, 500) are silently
deserialized as empty or malformed data, causing confusing downstream failures.

## Dependency Management

See [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) for comprehensive guidelines on
evaluating, versioning, auditing, and minimizing third-party dependencies.

## Code Style

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

### Don't Repeat Yourself (DRY)

When the same logic appears in multiple places, extract it into a shared
function or module. Duplicated code creates divergence risk — when one copy
is updated, the others are often missed.

```rust
// BAD: Same logic in two modules
// ai/prompt.rs
fn gather_surrounding(track: &ArcTrack, clip_id: ClipId) -> Context { ... }

// ai/consistency.rs
fn gather_surrounding(track: &ArcTrack, clip_id: ClipId) -> Context { ... }

// GOOD: Shared helper
// ai/helpers.rs
pub fn gather_surrounding_scripts(track: &ArcTrack, clip_id: ClipId) -> Context { ... }
```

**When to extract:**

- Two or more call sites with identical or near-identical logic
- The duplicated code serves the same purpose (not coincidental similarity)
- The extracted function has a clear name and single responsibility

**When duplication is acceptable:**

- Test setup code (clarity > reuse in tests)
- Two implementations that happen to look similar but serve different purposes
- Extraction would require complex parameterization that obscures intent

### Delete Unused Code

Don't leave backwards-compatibility hacks:

```
// BAD: Keeping dead code
const _oldVariable = null;  // Unused, kept for "compatibility"
// removed: oldFunction()

// GOOD: Just delete it
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

```rust
/// Remove a node from the dependency graph and rewire edges.
///
/// # Invariants Maintained
/// - Graph remains acyclic (no circular dependencies)
/// - All nodes have at least one path to a root
/// - Edge weights remain non-negative
/// - In-degree counts stay consistent with actual edges
///
/// # Preconditions
/// - Node has no dependents (in-degree == 0) or all dependents have been reassigned
/// - Node exists in the graph
/// - Removal would not disconnect any subgraph from roots
///
/// # Postconditions
/// - Node count reduced by exactly 1
/// - Edge count reduced by node's in-degree + out-degree
/// - All remaining paths remain valid
pub fn remove_node(graph: &mut DepGraph, node: NodeId) -> Option<RemovalResult>
```

### Validation Strategy

| Build | Validation Level |
|-------|-----------------|
| Debug | Full validation, panic on violation |
| Release | Critical checks only, log and recover |

```rust
// Pattern: Debug-only full validation
#[cfg(debug_assertions)]
{
    if let Err(e) = graph.validate_acyclic() {
        panic!("Graph invariant violated: {:?}", e);
    }
}

// Pattern: Release-mode graceful degradation
#[cfg(not(debug_assertions))]
{
    if let Err(e) = graph.validate_acyclic() {
        tracing::error!("Graph corruption detected: {:?}", e);
        return None;  // Abort operation gracefully
    }
}
```

### Invariant Testing

Every invariant should have corresponding tests:

```rust
#[test]
fn test_remove_node_maintains_acyclic_invariant() { ... }

#[test]
fn test_add_edge_rejects_cycle() { ... }
```

## Disabled Features

When disabling functionality due to bugs or incomplete implementation:

### Documentation Requirements

```rust
/// Whether incremental index rebuilding is enabled during bulk imports.
///
/// # Status: DISABLED
///
/// ## Reason
/// Incremental rebuild produces corrupted indices when concurrent
/// writes overlap with the rebuild window.
///
/// ## Tracking
/// Issue: #42 - Fix concurrent index rebuild corruption
///
/// ## Conditions for Re-enabling
/// 1. Implement write-ahead locking during rebuild
/// 2. Add integrity check after each incremental pass
/// 3. Pass stress test: 1000 concurrent writes during rebuild
///
/// ## Workaround
/// Full rebuild runs nightly via scheduled task
pub incremental_rebuild_enabled: bool,
```

### Config Pattern

```rust
impl Default for ImportConfig {
    fn default() -> Self {
        Self {
            // DISABLED: See incremental_rebuild_enabled doc for details
            incremental_rebuild_enabled: false,
            // ... other fields
        }
    }
}
```

### Unimplemented Stubs

Do not commit stub functions that accept requests and return empty or dummy
data. Stubs silently violate the caller's expectations and are difficult to
distinguish from working code.

```rust
// BAD: Looks like a working endpoint but does nothing
pub async fn summarize(...) -> Json<SummaryResponse> {
    Json(SummaryResponse { summary: String::new() })
}

// GOOD: Don't register the route until implemented
// (no route, no handler — callers get a clear 404)
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

```rust
// =============================================================================
// Priority Queue with Decrease-Key
// Adapted from: petgraph (https://github.com/petgraph/petgraph)
// License: MIT/Apache-2.0
// Copyright: bluss and petgraph contributors
// Source file: src/scored.rs
//
// Modifications:
// - Simplified API for single-use-case
// - Added generic key type parameter
// - Integrated with project's graph representation
// =============================================================================
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

```rust
//! # Graph Processing Engine
//!
//! ## Attribution
//! Core algorithms adapted from:
//! - petgraph (MIT/Apache-2.0) - Graph traversal algorithms
//! - pathfinding (MIT) - Shortest path implementations
//!
//! See individual functions for specific attributions.
```

## Rust-Specific Guidelines

### Error Handling

#### Result vs Panic

| Situation | Use |
|-----------|-----|
| Invalid input from external source | `Result<T, E>` |
| Programming error (bug) | `panic!` or `debug_assert!` |
| Impossible state | `unreachable!()` |
| Optional value | `Option<T>` |

```rust
// External input: use Result
pub fn parse_config_file(path: &Path) -> Result<Config, ParseError>

// Internal invariant: use Option (caller's responsibility)
pub fn remove_node(&mut self, id: NodeId) -> Option<RemovalResult>

// Bug detection: use debug_assert
debug_assert!(self.is_consistent(), "Data structure corrupted before operation");
```

#### Error Types

Prefer specific error types over strings:

```rust
// BAD
fn process() -> Result<(), String>

// GOOD
#[derive(Debug, thiserror::Error)]
pub enum ImportError {
    #[error("Record {0:?} does not exist")]
    NotFound(RecordId),
    #[error("Validation failed: {field} is {reason}")]
    Validation { field: String, reason: String },
    #[error("Conflict: record was modified concurrently")]
    Conflict,
}
```

### Ownership Patterns

#### Borrow vs Clone

```rust
// BAD: Unnecessary clone
fn process_records(records: Vec<Record>) {
    for r in records.clone() { ... }
}

// GOOD: Borrow when possible
fn process_records(records: &[Record]) {
    for r in records { ... }
}
```

#### Interior Mutability

Use sparingly and document why:

```rust
/// Cache of computed display values.
///
/// Uses RefCell because display values are lazily computed during
/// immutable iteration over records.
display_cache: RefCell<HashMap<RecordId, DisplayValue>>,
```

### Module Organization

```
crate_name/
├── lib.rs           # Public API, re-exports
├── types.rs         # Core types used throughout
├── error.rs         # Error types
└── feature/
    ├── mod.rs       # Feature public API
    ├── impl.rs      # Implementation details (pub(crate))
    └── tests.rs     # Unit tests (#[cfg(test)])
```

### Trait Design

```rust
// Prefer generics for static dispatch (performance)
fn process<S: Storage>(store: &S) { ... }

// Use trait objects for dynamic dispatch (flexibility)
fn process(store: &dyn Storage) { ... }

// Prefer associated types over generic parameters
trait Storage {
    type Item;  // Associated type
    fn items(&self) -> &[Self::Item];
}
```

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

### Accessibility

See [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) for semantic HTML, keyboard
interaction, ARIA, and a11y linting requirements.

## Performance-Critical Code

### Documentation

Mark hot paths explicitly:

```rust
/// Process all pending events in the current frame.
///
/// # Performance
/// **Hot path** - Called once per frame in the main loop.
///
/// ## Optimizations Applied
/// - Pre-allocated scratch buffers (no per-call allocation)
/// - SIMD for batch transformations
/// - Early-out for empty event queues
///
/// ## Benchmarks
/// See `benches/event_processing.rs::process_batch`
/// Target: < 1ms for 10K events
#[inline]
pub fn process_events(&mut self, batch: &EventBatch) { ... }
```

### Guidelines

1. **Profile before optimizing** - Measure, don't guess
2. **Document optimizations** - Future maintainers need context
3. **Benchmark critical paths** - Automated regression detection
4. **Avoid allocations in hot paths** - Use pre-allocated buffers

```rust
// BAD: Allocates every call
fn collect_results(&self) -> Vec<Output> {
    self.items.iter().map(|item| item.transform()).collect()
}

// GOOD: Reuse buffer
fn collect_results(&self, output: &mut Vec<Output>) {
    output.clear();
    output.extend(self.items.iter().map(|item| item.transform()));
}
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
