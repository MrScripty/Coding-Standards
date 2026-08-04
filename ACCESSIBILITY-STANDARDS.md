# Accessibility Standards

Migration index. [Accessibility](topics/accessibility.md) owns modality-neutral
user-access outcomes and conformance obligations. The remaining sections await
their ordered semantic migration; they do not override the canonical owner.
Non-normative platform and tool examples move to
[Accessibility Recipes](reference/recipes/accessibility.md) with their owning
semantic child.

## Interaction Semantics (Migrated)

The former semantic-element, action, navigation, and generic-interaction rules
are migrated to [Accessibility](topics/accessibility.md). Their web-specific
examples are non-normative [Accessibility Recipes](reference/recipes/accessibility.md).

## Keyboard And Focus Semantics (Migrated)

The former keyboard, focus visibility, and dialog-focus rules are migrated to
[Accessibility](topics/accessibility.md). CSS, key, and web dialog mechanisms
are non-normative [Accessibility Recipes](reference/recipes/accessibility.md).

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
