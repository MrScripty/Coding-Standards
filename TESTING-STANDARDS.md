# Testing Standards

Guidelines for writing maintainable, effective tests.

## Test Organization

### Choose a Consistent Test Placement Strategy

Use one clear test placement strategy per repo or per package. Test placement
should improve discoverability without mixing unrelated conventions randomly.

Acceptable strategies:

| Strategy | Structure | Works Well When |
|----------|-----------|-----------------|
| Colocated | `src/auth/login.ts` + `src/auth/login.test.ts` | Modules are small, packages are numerous, and local discoverability matters |
| Mirrored test tree | `src/auth/login.ts` + `tests/unit/auth/login.test.ts` | The language/tooling ecosystem strongly prefers separate test roots |
| Hybrid by level | unit tests colocated, integration/e2e under `tests/` | Fast local tests benefit from adjacency but system-level tests need shared harnesses |

Examples:

```text
# Colocated
src/
├── auth/
│   ├── login.ts
│   └── login.test.ts
└── billing/
    ├── invoice.ts
    └── invoice.test.ts
```

```text
# Mirrored test tree
src/
├── auth/
│   └── login.ts
tests/
├── unit/
│   └── auth/
│       └── login.test.ts
├── integration/
└── e2e/
```

Rules:
- Choose the strategy intentionally and keep it consistent within the chosen
  repo/package boundary.
- Name tests predictably so source files and related tests are easy to find.
- Keep integration/e2e/shared-harness tests in a dedicated location when they
  depend on multi-module fixtures or system setup.
- Document any hybrid approach briefly in the repo README or testing guide.

Selection criteria:
- Prefer colocated tests when package count is high and module-local reasoning
  matters more than a single central test tree.
- Prefer mirrored test trees when tooling, language conventions, or build
  systems make separate test roots simpler.
- Prefer hybrid placement when unit tests are local but integration/e2e tests
  need shared infrastructure and fixtures.

### Test Naming Convention

Use descriptive names that explain the scenario:

```
test_<function>_<scenario>_<expected_result>
```

**Examples:**

```rust
#[test]
fn test_remove_node_with_dependents_returns_rejected()

#[test]
fn test_add_edge_between_valid_nodes_succeeds()

#[test]
fn test_graph_after_100_operations_remains_acyclic()
```

```typescript
// TypeScript/JavaScript
describe('UserService', () => {
    it('creates user with valid email successfully', () => { ... });
    it('rejects user with invalid email format', () => { ... });
});
```

---

## Test Categories

| Category | Scope | Speed | When to Run |
|----------|-------|-------|-------------|
| Unit | Single function/module | < 10ms | Every commit |
| Integration | Multiple modules | < 1s | Pre-push |
| E2E | Full system | < 30s | CI only |

### Unit Tests

- Test a single function or method in isolation
- No external dependencies (database, network, filesystem)
- Fast enough to run on every save

### Integration Tests

- Test multiple components working together
- May use test databases or mock services
- Verify interfaces between modules

### End-to-End Tests

- Test complete user workflows
- Run against real (or realistic) environments
- Slower but catch integration issues

### Cross-Layer Acceptance Checks

For changes that span multiple layers or components, require at least one
acceptance check that exercises the full path from producer input to consumer
output.

This check should verify that, in practice:
- schema or metadata production is correct
- consumer binding preserves the produced contract
- execution behavior matches the bound values
- output handling agrees with the original producer semantics

Do not treat typecheck, isolated unit tests, or partial integration tests as a
substitute for one end-to-end acceptance path when the feature crosses layers.

### Replay, Recovery, and Idempotency Checks

For systems that use durable commands/events, projections, background workers,
or reconnect/retry behavior, add verification for:

- replay/bootstrap from persisted state
- duplicate command/request handling
- projection/read-model consistency after recovery
- partial failure recovery before new work resumes

These checks may be integration or end-to-end tests depending on system shape,
but they must exercise the real workflow boundaries rather than only pure helper
functions.

---

## Unit Test Guidelines

### Test One Thing

Each test should verify a single behavior:

```rust
// BAD: Tests multiple behaviors
#[test]
fn test_user_service() {
    // tests creation, validation, AND persistence
}

// GOOD: Focused tests
#[test]
fn test_create_user_with_valid_email_succeeds() { ... }

#[test]
fn test_create_user_with_invalid_email_returns_error() { ... }

#[test]
fn test_create_user_persists_to_database() { ... }
```

### Arrange-Act-Assert Pattern

Structure tests with clear phases:

```rust
#[test]
fn test_remove_node_with_active_dependents_rejected() {
    // Arrange - Set up test data
    let graph = create_graph_with_dependencies();
    let node_with_deps = find_node_with_dependents(&graph);

    // Act - Execute the code under test
    let result = can_remove_node(&graph, node_with_deps);

    // Assert - Verify the result
    assert_eq!(result, RemovalCheck::Rejected(HasDependents));
}
```

```typescript
// TypeScript
test('calculateTotal applies discount correctly', () => {
    // Arrange
    const items = [{ price: 100 }, { price: 50 }];
    const discount = 0.1;

    // Act
    const total = calculateTotal(items, discount);

    // Assert
    expect(total).toBe(135);
});
```

### Avoid Mocks When Possible

**Prefer (in order):**

1. Real implementations (if fast enough)
2. In-memory fakes
3. Test fixtures
4. Mocks (last resort)

**Use mocks only for:**

- External services (APIs, databases in unit tests)
- Non-deterministic behavior (time, randomness)
- Slow operations that can't be made fast

```typescript
// BAD: Mocking everything
const mockRepo = jest.fn();
const mockValidator = jest.fn();
const mockLogger = jest.fn();

// GOOD: Use real implementations where possible
const repo = new InMemoryUserRepository();
const validator = new UserValidator(); // Real, it's fast
const logger = new NullLogger(); // Simple fake
```

### Test Edge Cases

Always test:

- Empty inputs
- Null/undefined values
- Boundary conditions
- Error cases

```rust
#[test]
fn test_remove_node_empty_graph_returns_none() { ... }

#[test]
fn test_remove_node_invalid_id_returns_none() { ... }

#[test]
fn test_remove_node_leaf_succeeds() { ... }
```

---

## Property-Based Testing

For algorithms with mathematical invariants, use property-based testing:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn graph_remains_acyclic_after_any_add(
        graph in arbitrary_dag(),
        edge in arbitrary_edge()
    ) {
        let mut g = graph.clone();
        if let Ok(_) = g.try_add_edge(edge) {
            prop_assert!(g.is_acyclic());
        }
    }

    #[test]
    fn serialize_then_deserialize_is_identity(
        record in arbitrary_record()
    ) {
        let bytes = record.serialize();
        let restored = Record::deserialize(&bytes).unwrap();
        prop_assert_eq!(record, restored);
    }
}
```

### When to Use Property-Based Testing

- Mathematical invariants (graph properties, sorting)
- Serialization/deserialization roundtrips
- Inverse operations (encode/decode, compress/decompress)
- Algorithms that should work for any valid input

---

## Coverage Guidelines

### Targets

| Type | Minimum | Ideal |
|------|---------|-------|
| Line | 70% | 85% |
| Branch | 60% | 75% |
| Function | 80% | 90% |

### What to Exclude from Coverage

- Generated code
- Simple getters/setters with no logic
- Framework boilerplate
- Debug-only code (`#[cfg(debug_assertions)]`)
- Panic handlers and unreachable code

### Coverage is Not Quality

High coverage does not mean good tests. Focus on:

- Testing behavior, not implementation
- Edge cases and error paths
- Meaningful assertions

---

## Test Documentation

### Document Non-Obvious Tests

```rust
/// Regression test for #127: Node merge was creating duplicate edges
/// when both nodes had 4+ shared neighbors.
///
/// The fix deduplicates edges after reconnection.
#[test]
fn test_merge_nodes_shared_neighbors_deduplicates_edges() {
    // Test implementation
}
```

### Document Test Fixtures

```rust
/// Create a diamond graph: four nodes with two paths from top to bottom.
///
/// ```text
///       A
///      / \
///     B   C
///      \ /
///       D
/// ```
fn create_diamond_graph() -> Graph { ... }
```

---

## Test Data Management

### Use Factories or Builders

```typescript
// BAD: Inline object construction
const user = {
    id: '123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'admin',
    createdAt: new Date(),
    // ... 10 more fields
};

// GOOD: Factory with defaults
const user = createUser({ role: 'admin' });
// Only specify what matters for this test
```

```rust
// Rust builder pattern
let graph = GraphBuilder::new()
    .with_nodes(4)
    .with_edge("a", "b")
    .build();
```

### Avoid Shared Mutable State

```typescript
// BAD: Tests depend on shared state
let sharedDb: Database;

beforeAll(() => {
    sharedDb = new Database();
});

// GOOD: Fresh state per test
beforeEach(() => {
    db = new InMemoryDatabase();
});
```

### Validate Persisted Dynamic Artifacts

Persisted examples and fixtures that depend on dynamic schemas or generated
contracts must be validated or regenerated before commit.

Examples include:
- templates
- manifests
- saved graphs or workflows
- schema-backed JSON/YAML fixtures
- example requests/responses derived from current producers

The goal is to catch silent drift between the checked-in artifact and the
current producer contract.

---

## Async Testing

### Always Await Async Operations

```typescript
// BAD: Missing await
test('fetches user', () => {
    const user = fetchUser('123'); // Returns Promise!
    expect(user.name).toBe('Test'); // Fails or passes randomly
});

// GOOD: Properly awaited
test('fetches user', async () => {
    const user = await fetchUser('123');
    expect(user.name).toBe('Test');
});
```

### Test Both Success and Failure

```typescript
test('fetchUser returns user for valid ID', async () => {
    const user = await fetchUser('valid-id');
    expect(user).toBeDefined();
});

test('fetchUser throws for invalid ID', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow(NotFoundError);
});
```

### Lifecycle Regression Checks

When changing polling, timers, retries, restart logic, or cancellation paths,
add targeted regression checks for:
- Timer/subscription cleanup after unmount, shutdown, or dependency changes
- Restart loops terminating correctly instead of spawning duplicate work
- Overlapping requests or retries not racing stale results over newer state
- Cancellation aborting in-flight work without leaving partial state behind

Do not rely on a passing build or happy-path smoke test to cover these cases.

### Service-Layer Error Paths

For service-layer changes, verify expected failure behavior directly, not just
successful builds/tests. Add targeted checks for relevant paths such as:
- Upstream non-success responses
- Retry exhaustion and backoff termination
- Partial failures during orchestration
- Cancellation or timeout propagation
- Logged or surfaced error context

---

## Frontend Component Testing

Frontend-specific testing guidance (selector strategy, accessibility interaction
tests, `userEvent` vs `fireEvent`, DOM geometry constraints, and polling timer
cleanup tests) is defined in [FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md).

---

## Performance Testing

### Benchmark Critical Paths

```rust
#[bench]
fn bench_process_10k_records(b: &mut Bencher) {
    let records = create_test_records(10_000);

    b.iter(|| {
        process_batch(&records)
    });
}
```

### Set Performance Budgets

```typescript
test('search completes within 100ms for 10k items', async () => {
    const items = generateItems(10_000);

    const start = performance.now();
    await search(items, 'query');
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
});
```

---

## Verification Layers

Testing is not limited to unit test suites. Use these verification layers in order. Each catches a different class of problem. Stop at the first failure and fix it before proceeding.

```
┌──────────────────────────────────────────┐
│  1. Static Analysis (fastest)            │  Compiler errors, type checks, lint
├──────────────────────────────────────────┤
│  2. Build Verification                   │  Full project build succeeds
├──────────────────────────────────────────┤
│  3. Dev Server Validation                │  Dev server starts without errors
├──────────────────────────────────────────┤
│  4. Runtime Verification                 │  App launches and runs correctly
├──────────────────────────────────────────┤
│  5. Reference Lookup (when stuck)        │  Library source, docs, examples
└──────────────────────────────────────────┘
```

### Layer 1: Static Analysis

Run your language's type checker and linter first — it's the fastest feedback loop.

| Language | Command | What It Catches |
|----------|---------|-----------------|
| TypeScript | `tsc --noEmit` / `svelte-check` | Type errors, unused variables |
| Rust | `cargo check` | Borrow errors, type mismatches |
| C# | `dotnet build` | Compiler errors, nullability |
| Python | `mypy` / `pyright` | Type errors |

### Layer 2: Build Verification

Run the full project build after cross-cutting changes. For single-layer changes, use targeted builds for speed.

### Layer 3: Dev Server Validation

If your project has a dev server (Vite, webpack, etc.), start it and watch for:
- Import resolution errors
- Module compilation failures
- Runtime reference errors in the terminal

### Layer 4: Runtime Verification

Launch the full application. Verify:
- No runtime exceptions in console/logs
- Core user flows work end to end
- Cross-layer communication succeeds

### Layer 5: Reference Lookup

When an error is unclear or an API is unfamiliar:
1. Check local library source code (exact version in use)
2. Read official documentation
3. Search library issues/discussions
4. Search the web as a last resort

**Prefer local source over web lookups.** Local source is always accurate for the exact version in use.

---

## Diagnosis Workflow

When something breaks, follow this decision tree:

```
Error encountered
    │
    ├─ Is it a compiler/type error?
    │   ├─ Yes → Read the full error message
    │   │        Look up the type/method in library source
    │   │        Fix and re-run static analysis
    │   └─ No ↓
    │
    ├─ Is it a build error?
    │   ├─ Yes → Check dependencies are installed
    │   │        Check for version mismatches
    │   │        Fix and re-run the build
    │   └─ No ↓
    │
    ├─ Is it a runtime error?
    │   ├─ Yes → Read the full stack trace
    │   │        Identify which layer threw the error
    │   │        Check data flow across boundaries
    │   │        Fix and re-launch
    │   └─ No ↓
    │
    ├─ Is it a logic/behavior error?
    │   ├─ Yes → Trace the data flow through the system
    │   │        Add debug logging if needed
    │   │        Compare with known working examples
    │   │        Fix and verify
    │   └─ No ↓
    │
    └─ Unknown → Search library source for related code
                 Search web for the error message
                 Ask for help only as a last resort
```

---

## Self-Correction Principles

1. **Always compile after edits.** Never assume a change is correct — verify with the appropriate build command.
2. **Read the full error.** Compiler and runtime errors contain file paths, line numbers, and descriptions. Use all of them.
3. **Check one layer at a time.** If you changed multiple layers, build them separately to isolate which one broke.
4. **Don't guess APIs — look them up.** Read the actual method signatures in library source or documentation.
5. **Use the dev server for fast iteration.** Hot reload gives sub-second feedback. Use it instead of full builds when iterating on frontend code.
6. **Run integration verification after cross-layer fixes.** After fixing a multi-component issue, verify the full pipeline works.
7. **Exhaust local resources before asking for help.** Check library source → check docs → search web → then ask.

---

## Test Checklist

Before submitting code:

- [ ] All new code has corresponding tests
- [ ] Tests pass locally
- [ ] Edge cases are covered
- [ ] Error paths are tested
- [ ] Lifecycle cleanup/restart/cancellation regressions are covered when applicable
- [ ] Cross-layer changes include at least one full-path acceptance check
- [ ] Persisted schema-backed artifacts were validated or regenerated when applicable
- [ ] No flaky tests introduced
- [ ] Test names clearly describe the scenario
- [ ] Complex test logic is documented
