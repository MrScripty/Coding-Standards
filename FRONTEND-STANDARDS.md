# Frontend Standards

Canonical Frontend application-boundary policy is owned by the
[Frontend application profile](profiles/applications/frontend.md).
This legacy source is a migration index and does not independently define
frontend architecture, rendering, synchronization, tooling, testing, or
accessibility policy.

## Scope

Applicability moved to the profile's
[Applicability Decision](profiles/applications/frontend.md#applicability-decision).
Browser, Electron, Tauri, WebView, desktop-shell, framework, and directory names
do not select ownership. Contracts, Tooling, Verification, Accessibility, and
language profiles retain their canonical responsibilities.

---

## Rendering and DOM Updates

Rendering authority and mechanism selection moved to
[Rendering And Synchronization](profiles/applications/frontend.md#rendering-and-synchronization).
TypeScript and DOM examples moved to the non-normative
[Frontend Mechanism Recipes](reference/recipes/frontend.md).

Declarative and imperative rendering are selected mechanisms. This index does
not authorize framework state, DOM reads, canvas, WebGL, or native widgets as
authority or fallback.

---

## UI State Synchronization

Synchronization authority, event, subscription, query, polling, cancellation,
stale-result, and boundary-adapter policy moved to
[Rendering And Synchronization](profiles/applications/frontend.md#rendering-and-synchronization).
Fixed event, timer, DOM-scan, and FFI-drain examples remain only in the
non-normative recipes.

This index does not prefer event delivery or polling without source and consumer
contract evidence, and it does not authorize global loops, fixed cadence,
copied state, DOM authority, or alternate synchronization fallback.

### Hook/Composable Timer Management

Frontend timer, polling, subscription, observer, cancellation, supersession,
cleanup, and stale-result obligations moved to
[Lifecycle-Owned Frontend Work](profiles/applications/frontend.md#lifecycle-owned-frontend-work).
Generic work lifecycle remains in [Concurrency](topics/concurrency.md), and
TypeScript invocation mechanisms remain in the
[TypeScript Async profile](profiles/languages/typescript/async.md).

The React hook example moved to the non-normative
[Frontend Mechanism Recipes](reference/recipes/frontend.md#illustrative-react-timer-adapter).
This index does not mandate refs, mutable holders, state exclusion, intervals,
cadence, dependency lists, retries, unmount cleanup, or one testing mechanism.

---

## Frontend Tooling Notes

### React 19+ ESLint Configuration

TypeScript project boundaries, static-analysis selection, compiler and parser
compatibility, and typed outcomes are owned by the
[TypeScript profile](profiles/languages/typescript.md#static-analysis-and-compiler-configuration).
Lint purpose, rules, scope, severity, orchestration, and evidence are owned by
[Tooling](workflows/tooling.md#lint-policy-and-orchestration).

The React automatic-JSX example moved to the non-normative
[Tooling Recipes](reference/recipes/tooling.md#illustrative-react-automatic-jsx-lint-adapter).
This index does not select React 19, the automatic JSX runtime, ESLint, plugin
rules, rule disablement, prop validation, parser, preset, severity, or a copied
configuration.

---

## Frontend Testing

Canonical frontend evidence requirements are defined by the
[Frontend application profile](profiles/applications/frontend.md#evidence).
This legacy file does not prescribe selector, event-dispatch, simulated DOM,
browser, or lifecycle-testing defaults.

Selector priority tables, generic role counts, `userEvent` and `fireEvent`
preferences, DOM-shim geometry, mocked rectangles, timer-spy assertions, and
fixed embedded-control smoke checks are retired mechanisms. Verification
selects evidence from the changed claim and required environment; Frontend
specializes the user-observable behavior being proved.

---

## Accessibility

See [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) for semantic HTML,
keyboard interaction, ARIA, and a11y linting requirements.
