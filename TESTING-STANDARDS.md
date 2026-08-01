# Testing Standards

> **Migration authority:** [workflows/verification.md](workflows/verification.md)
> is canonical for acceptance claims, evidence kinds, environment
> qualifications, execution modes, test design, organization, and completion.
> Remaining sections are bounded migration routes and do not override the
> workflow's claim model.

Guidelines for writing maintainable, effective tests.

## Test Organization

Placement, discovery, naming, and typed outcomes are owned by
[Verification](workflows/verification.md#test-placement-and-naming). Concrete
syntax and runner discovery rules belong in the applicable language profile.

---

## Test Suite Shapes

Suite labels are repository organization mechanisms. Acceptance-path evidence,
boundary selection, environment fidelity, and typed unavailable outcomes are
owned by [Verification](workflows/verification.md#acceptance-paths-and-boundaries).

### Global State and Durable Resource Isolation

Canonical verification-resource ownership and coordination requirements are in
[Concurrency](topics/concurrency.md#isolate-verification-resources). This
legacy heading is a non-normative migration route.

### Binding Verification Requirements

Canonical native, host, package-cohort, and boundary evidence requirements are
in [Language Binding Evidence Cohorts](profiles/boundaries/language-bindings.md#binding-evidence-cohorts).
This legacy heading is a non-normative migration route.

### Replay, Recovery, and Idempotency Checks

Canonical replay, duplicate-handling, convergence, resumption, and partial-
failure evidence requirements are in
[Replay and Resumption Evidence](topics/resilience.md#replay-and-resumption-evidence).
This legacy heading is a non-normative migration route.

---

## Unit Test Guidelines

Focused test structure, substitutes, edge-condition selection, and typed
outcomes are owned by [Verification](workflows/verification.md#test-design).
Language-specific syntax belongs in the applicable language profile.

---

## Property-Based Testing

Property-based and generative evidence selection is owned by
[Verification](workflows/verification.md#test-design). Concrete tooling, when
selected, belongs in the applicable language profile.

---

## Coverage Guidance

Coverage interpretation, threshold authority, exclusions, and typed outcomes
are owned by [Verification](workflows/verification.md#coverage-and-durable-evidence-records).

---

## Test Documentation

Durable evidence and fixture-context records are owned by
[Verification](workflows/verification.md#coverage-and-durable-evidence-records).
Documentation mechanisms follow the owning repository and evidence artifact.

---

## Test Data Management

Test-data authority, identity, construction, isolation, and lifecycle are owned
by [Verification](workflows/verification.md#test-data-authority-and-lifecycle).
Factories, builders, direct construction, and shared or isolated fixtures are
mechanisms selected from that contract, not defaults.

### Validate Persisted Dynamic Artifacts

Canonical authority, validation, regeneration, consumer-evidence, and typed-
outcome requirements are in
[Persisted Contract Artifacts](topics/contracts.md#persisted-contract-artifacts).
This legacy heading is a non-normative migration route.

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

Canonical lifecycle ownership and evidence requirements are in
[Concurrency](topics/concurrency.md#verification). This legacy heading is a
non-normative migration route.

### Service-Layer Error Paths

For service-layer changes, verify expected failure behavior directly, not just
successful builds/tests. Add targeted checks for relevant paths such as:
- Upstream non-success responses
- Retry exhaustion and backoff termination
- Partial failures during orchestration
- Cancellation or timeout propagation
- Surfaced or recorded diagnostic context, including safe correlation fields
  when the project has an owned diagnostic channel

---

## Frontend Component Testing

Frontend-specific testing guidance (selector strategy, accessibility interaction
evidence, browser geometry, embedded controls, and lifecycle cleanup) is owned
by the [Frontend application profile](profiles/applications/frontend.md#evidence).

---

## Performance Testing

Performance benchmark, budget, workload, environment, variability, and
regression evidence is owned by
[Performance](topics/performance.md#performance-test-evidence). Language
profiles may select concrete tools but do not override the claim contract.

---

## Supporting Development Checks

Static analysis, formatting, linting, compilation, builds, dev-server startup,
and runtime launch are useful supporting checks. They prove only their explicit
properties and do not replace missing contract, system, user-workflow, or
release-artifact claims.

Use language profiles for concrete commands and
[TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) for scheduling mechanisms. When an
error is unclear, consult the exact local dependency source and official
documentation before relying on examples for another version.

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
- [ ] Production error paths surface or record bounded diagnostic context
- [ ] Lifecycle cleanup/restart/cancellation regressions are covered when applicable
- [ ] Cross-layer changes include at least one full-path acceptance check
- [ ] New cross-layer features include a thin vertical slice before broad
      horizontal layer expansion
- [ ] Persisted schema-backed artifacts were validated or regenerated when applicable
- [ ] No flaky tests introduced
- [ ] Test names clearly describe the scenario
- [ ] Complex test logic is documented
