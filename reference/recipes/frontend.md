# Frontend Mechanism Recipes

**Standards metadata**

- ID: `reference.recipes.frontend`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A Frontend-selected rendering, synchronization, lifecycle, interaction, or evidence contract needs an illustrative web-technology mechanism.
- Does not apply when: Frontend authority, source contracts, lifecycle ownership, mechanism capability, or evidence is unresolved.
- Requires: `profile.application.frontend`, `profile.language.typescript.async`
- Specializes: `none`
- Verification: Reference-boundary checks keep frontend and framework examples non-normative and linked to canonical owners.
- Canonical owner: `reference/recipes/frontend.md`

This material is non-normative. Select projection authority, rendering,
synchronization, lifecycle, interaction, accessibility, and evidence through
the [Frontend application profile](../../profiles/applications/frontend.md)
before adapting a mechanism.

## Illustrative Rendering Mechanisms

A framework with an accepted declarative projection might update owned state:

```typescript
setStatus(status);
```

A selected imperative renderer might isolate direct mutation:

```typescript
renderSurface.replaceChildren(renderStatusNode(status));
```

Neither mechanism is a default. `innerHTML`, `appendChild`, canvas, WebGL,
native widgets, component state, and stores are mechanisms whose authority,
cleanup, and evidence come from the selected contract.

## Illustrative Synchronization Mechanisms

An event-capable source might publish a targeted change:

```typescript
input.addEventListener('input', event => {
  linkStore.applySourceUpdate(readValidatedValue(event));
});
```

A pull-only boundary might expose a deliberate drain:

```text
events = boundary.drain_events()
apply_validated_events(events)
```

A selected polling adapter may use a timer only after its owner, cadence,
cancellation, stale-result handling, and terminal outcomes are established.
These examples do not select event delivery, polling, a frequency, DOM reads,
global timers, or periodic reconciliation.

## Illustrative React Timer Adapter

After Frontend, Concurrency, and TypeScript Async select lifecycle ownership, a
React adapter might retain a timer handle in a ref:

```typescript
const timerRef = useRef<number | null>(null);

useEffect(() => {
  timerRef.current = window.setInterval(runSelectedPoll, selectedCadence);
  return () => {
    if (timerRef.current !== null) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };
}, [runSelectedPoll, selectedCadence]);
```

This example does not select React, a ref rather than another owner, an
interval, cadence, dependency list, retry behavior, or unmount as the only
cleanup boundary. The adapter still proves duplicate exclusion, cancellation,
completion classification, stale-result rejection, and every selected teardown
path.
