# Accessibility Standards

Semantic HTML, keyboard interaction, and ARIA guidelines for building accessible UI components.

## Core Principle: Use Semantic Elements

HTML provides built-in accessibility for interactive elements. Using the correct
element eliminates the need for ARIA attributes and custom keyboard handling.

```
Semantic Element ──► Built-in accessibility (focus, keyboard, screen reader)
Generic Element  ──► Must manually add role, tabIndex, keyboard handlers, labels
```

**Prefer semantic elements.** Only use generic elements with ARIA when a semantic
element cannot achieve the required visual or behavioral result.

## Interactive Elements

### Use `<button>` for Actions

Any element that triggers an action on click must be a `<button>`, not a `<div>`,
`<span>`, or `<a>`.

```tsx
// BAD: div with click handler — no keyboard support, no screen reader role
<div className="close-btn" onClick={onClose}>
  X
</div>

// BAD: anchor as button — announces as link, href="#" is meaningless
<a href="#" onClick={(e) => { e.preventDefault(); doAction(); }}>
  Do something
</a>

// GOOD: semantic button
<button type="button" onClick={onClose}>
  X
</button>

// GOOD: button with accessible label when there's no visible text
<button type="button" onClick={onClose} aria-label="Close dialog">
  <XIcon />
</button>
```

**Why `type="button"`:** Without it, buttons inside forms default to `type="submit"`.
Always set `type="button"` for non-submit buttons.

### Use `<a>` Only for Navigation

Anchors are for navigating to a URL. If clicking an element does not navigate
the user to a new page or location, use `<button>`.

```tsx
// GOOD: anchor navigates to a page
<a href="/settings">Settings</a>

// GOOD: anchor opens external URL
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  Documentation
</a>

// BAD: anchor triggers an action — use button instead
<a href="#" onClick={handleExport}>Export</a>
```

### When a Generic Element Must Be Interactive

In rare cases where a semantic element cannot achieve the required result
(e.g., a full-screen backdrop overlay), add all necessary accessibility
attributes:

```tsx
<div
  role="button"
  tabIndex={0}
  onClick={onClose}
  onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") onClose(); }}
  aria-label="Close dialog"
>
```

**Required attributes for interactive generic elements:**

| Attribute | Purpose |
|-----------|---------|
| `role` | Tells screen readers the element's function |
| `tabIndex={0}` | Makes the element focusable via keyboard |
| `onKeyDown` | Handles Enter and Space for activation |
| `aria-label` | Provides an accessible name if no visible text |

## Keyboard Navigation

### All Interactive Elements Must Be Keyboard-Accessible

Every element that responds to `onClick` must also be reachable and activatable
via keyboard. Semantic `<button>` and `<a>` elements handle this automatically.

### Focus Indicators

Never remove focus outlines without providing an alternative:

```css
/* BAD: removes focus indicator entirely */
button:focus { outline: none; }

/* GOOD: custom focus indicator */
button:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

### Dialog Focus Management

When opening a modal or dialog:

1. Move focus into the dialog on open
2. Trap focus within the dialog while open
3. Return focus to the triggering element on close
4. Close on Escape key press

## Labels and Names

### Every Interactive Element Needs an Accessible Name

Screen readers announce the accessible name of focused elements. Without one,
the element is announced as just "button" or "link" with no context.

```tsx
// BAD: icon-only button with no name — announced as just "button"
<button onClick={onDelete}>
  <TrashIcon />
</button>

// GOOD: aria-label provides the name
<button onClick={onDelete} aria-label="Delete item">
  <TrashIcon />
</button>

// ALSO GOOD: visually hidden text
<button onClick={onDelete}>
  <TrashIcon />
  <span className="sr-only">Delete item</span>
</button>
```

### Form Inputs Need Labels

Every `<input>`, `<select>`, and `<textarea>` must have an associated label:

```tsx
// GOOD: explicit label association
<label htmlFor="username">Username</label>
<input id="username" type="text" />

// GOOD: aria-label when no visible label exists
<input type="search" aria-label="Search models" placeholder="Search..." />
```

## Images and Media

### Decorative vs Informative Images

```tsx
// Decorative: adds no information — hide from screen readers
<img src="divider.svg" alt="" />

// Informative: conveys meaning — describe it
<img src="error-icon.svg" alt="Error" />
```

### Icon Components

When using icon components (Lucide, Heroicons, etc.):

```tsx
// Decorative icon next to text — hide from screen readers
<button>
  <SaveIcon aria-hidden="true" />
  Save
</button>

// Standalone icon — parent needs aria-label (see Labels section)
<button aria-label="Save">
  <SaveIcon aria-hidden="true" />
</button>
```

## Linting Enforcement

### Required ESLint Plugin

Projects with React/JSX must include `eslint-plugin-jsx-a11y`:

```bash
npm install eslint-plugin-jsx-a11y --save-dev
```

### Recommended Rules

At minimum, enable these rules as errors (not warnings):

| Rule | What It Catches |
|------|----------------|
| `jsx-a11y/click-events-have-key-events` | `onClick` without `onKeyDown` on non-interactive elements |
| `jsx-a11y/no-static-element-interactions` | Interactive handlers on `<div>`, `<span>`, etc. |
| `jsx-a11y/anchor-is-valid` | `<a href="#">` or `<a>` without valid href |
| `jsx-a11y/no-noninteractive-element-interactions` | Click handlers on elements like `<p>`, `<li>` |
| `jsx-a11y/alt-text` | Missing `alt` on `<img>` |
| `jsx-a11y/label-has-associated-control` | `<input>` without associated `<label>` |

### CI Gate

Accessibility lint rules must be enforced in CI. See
[TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) for the CI quality gates that
include a11y as part of the lint step.
