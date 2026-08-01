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

Async completion and contract-selected outcome evidence are owned by
[Verification](workflows/verification.md#async-completion-and-failure-evidence).
Await syntax, callback completion, polling, events, and harness controls are
mechanisms selected from that contract, not evidence by themselves.

### Lifecycle Regression Checks

Canonical lifecycle ownership and evidence requirements are in
[Concurrency](topics/concurrency.md#verification). This legacy heading is a
non-normative migration route.

### Service-Layer Error Paths

Service-boundary success, failure, retry, cancellation, timeout, partial-result,
and diagnostic evidence are owned by
[Verification](workflows/verification.md#async-completion-and-failure-evidence).

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

Supporting-gate classification and claim-directed diagnosis are owned by
[Verification](workflows/verification.md#supporting-gates-and-claim-directed-diagnosis).
Language profiles own concrete commands and
[Tooling](TOOLING-STANDARDS.md) owns execution mechanisms.

---

## Diagnosis Workflow

Diagnosis selection, evidence preservation, and typed blocked outcomes are owned
by [Verification](workflows/verification.md#supporting-gates-and-claim-directed-diagnosis).

---

## Self-Correction Principles

Correction and re-verification follow the unresolved acceptance claim and
affected contracts in
[Verification](workflows/verification.md#supporting-gates-and-claim-directed-diagnosis),
not a fixed compile, layer, launch, lookup, or escalation sequence.

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
