# Testing Standards

Guidelines for writing maintainable, effective tests.

## Test Organization

### Mirror Source Structure

```
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
- [ ] No flaky tests introduced
- [ ] Test names clearly describe the scenario
- [ ] Complex test logic is documented
