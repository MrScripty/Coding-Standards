# Frontend Standards

Frontend architecture, rendering, state synchronization, tooling, and testing rules.

## Scope

These standards apply to browser UIs and desktop frontends (Electron/Tauri/WebView).
They complement:
- [CODING-STANDARDS.md](CODING-STANDARDS.md) for general coding rules
- [TESTING-STANDARDS.md](TESTING-STANDARDS.md) for general test strategy
- [TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) for CI/hooks/lint infrastructure
- [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) for a11y-specific requirements

---

## Rendering and DOM Updates

### Prefer Declarative Rendering

Use framework state/props/store bindings as the source of truth for UI output.
Do not manually mutate DOM structure in component code when declarative bindings
can express the same behavior.

Avoid direct mutation patterns in component code:
- `innerHTML` writes for normal rendering
- manual `appendChild` trees for regular UI updates
- ad hoc DOM edits that bypass reactive state

If direct DOM access is unavoidable (for example canvas/WebGL integration),
keep it isolated, documented, and cleaned up in lifecycle teardown.

```typescript
// BAD: Rebuild UI through imperative DOM writes
container.innerHTML = '';
container.appendChild(renderStatusNode(status));

// GOOD: Update state; framework re-renders declaratively
setStatus(status);
```

---

## UI State Synchronization

Prefer event-driven synchronization over polling for frontend UI state.

Rules:
1. Do not use global high-frequency polling loops to keep UI stores/components in sync when event or subscription hooks are feasible.
2. Push updates from the source of truth (input handlers, service callbacks, store actions) instead of repeatedly scanning DOM/state on an interval.
3. If polling is unavoidable, scope it to the smallest owner, use the lowest practical frequency, and stop it deterministically on unmount/shutdown.
4. Document why event-driven synchronization is not feasible when introducing polling.

Exception:
- Pull-based protocol/FFI event delivery patterns (for example `drain_events()` bridges) are allowed at system boundaries as described in
  [LANGUAGE-BINDINGS-STANDARDS.md](LANGUAGE-BINDINGS-STANDARDS.md). These are transport patterns, not UI synchronization loops.

```typescript
// BAD: Global loop to discover changes indirectly
setInterval(() => {
    syncLinkedInputsFromDom();
}, 100);

// GOOD: Emit targeted updates when values actually change
input.addEventListener('input', (e) => {
    linkStore.notifyValueChanged(nodeId, (e.target as HTMLInputElement).value);
});
```

### Hook/Composable Timer Management

For polling hooks/composables/stores, timer lifecycle must be explicit and
stale-closure-safe.

Rules:
1. Store interval/timeout handles in refs or dedicated mutable holders, not state.
2. Clear timers on completion, dependency changes, and unmount.
3. Prevent duplicate timers when start/retry logic reruns.
4. Add deterministic cleanup tests.

```typescript
// GOOD: Ref-based timer management with deterministic cleanup
const timerRef = useRef<number | null>(null);

useEffect(() => {
    timerRef.current = window.setInterval(pollStatus, 500);
    return () => {
        if (timerRef.current !== null) {
            window.clearInterval(timerRef.current);
            timerRef.current = null;
        }
    };
}, [pollStatus]);
```

---

## Frontend Tooling Notes

### React 19+ ESLint Configuration

React 19 uses the automatic JSX runtime. Configure ESLint to avoid outdated
rules:

```javascript
// Inside the files block for React projects
rules: {
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
}
```

---

## Frontend Testing

### Selector Strategy

Choose selectors that match what you're actually testing. Fragile selectors are
the most common reason UI tests break during legitimate component improvements.

| Priority | Selector | When to Use | Resilience |
|----------|----------|-------------|------------|
| 1 | `getByRole('button', { name: 'Save' })` | Interactive elements with visible text | High |
| 2 | `getByTitle('ComfyUI')` / `getByLabelText(...)` | Elements with accessible names | High |
| 3 | `getByTestId('submit-btn')` | No accessible name available | Medium |
| 4 | `container.querySelector('button')` | Targeting a specific HTML element type | Medium |
| 5 | `getAllByRole('button')` + count assertion | Verifying total count | Low |

```typescript
// BAD: Breaks when accessibility improvements add more role="button" elements
const buttons = screen.getAllByRole('button');
expect(buttons.length).toBe(3);

// BAD: Breaks when another button is added elsewhere in the tree
screen.getByRole('button'); // throws if multiple found

// GOOD: Targets a specific element by name
screen.getByRole('button', { name: 'Launch' });

// GOOD: Targets by title when name is not practical
screen.getByTitle('ComfyUI');

// GOOD: Targets the HTML element type directly when needed
container.querySelector('button');
```

### Accessibility and Tests

Adding ARIA roles (`role="button"`, `tabIndex`, `onKeyDown`) is expected to
change role-based query results. This is a feature, not a bug.

When adding accessibility attributes to components:
1. Update existing tests that use generic `getByRole` queries.
2. Switch to queries with accessible names: `getByRole('button', { name: '...' })`.
3. Add a dedicated test that verifies keyboard interaction.

### `userEvent` vs `fireEvent`

`userEvent` simulates realistic browser behavior and triggers the full pointer
event chain (`pointerMove` -> `pointerDown` -> `pointerUp` -> `click`). This can
trigger side effects in components that track pointer state.

Use `userEvent` for user flows. Use `fireEvent` when isolating a single event
and avoiding side-effect chains.

```typescript
// userEvent simulates the full interaction chain
await user.click(element);

// fireEvent dispatches a single event with no pointer chain
fireEvent.click(element);
```

| Scenario | Use | Why |
|----------|-----|-----|
| Testing user flows (click, type, tab) | `userEvent` | Realistic simulation |
| Component tracks mouse/pointer position | `fireEvent` | Avoids pointer move side effects |
| Testing keyboard interactions | `userEvent` | Simulates focus and keypress correctly |
| Window-level events (`mousemove`, `resize`) | `act()` + `dispatchEvent` | Not user interactions |

```typescript
act(() => {
    window.dispatchEvent(new MouseEvent('mousemove', {
        clientX: 100,
        clientY: 200,
    }));
});
```

### DOM Geometry in Tests

`jsdom` returns zeroed rectangles for `getBoundingClientRect()`. For
position-dependent behavior:
- Mock geometry on specific elements.
- Keep position logic in pure functions where practical.
- Test integration paths with explicit geometry assumptions.

### Polling Cleanup Tests

Polling hooks/composables must have tests that prove timers stop on completion
and unmount.

```typescript
it('stops polling after completion', async () => {
    const clearSpy = vi.spyOn(window, 'clearInterval');
    const { unmount } = renderHook(() => useJobPolling());

    await act(async () => markJobComplete());
    unmount();

    expect(clearSpy).toHaveBeenCalled();
});
```

---

## Accessibility

See [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) for semantic HTML,
keyboard interaction, ARIA, and a11y linting requirements.
