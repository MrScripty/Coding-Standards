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
