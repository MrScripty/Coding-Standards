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

## Names And Forms Semantics (Migrated)

The former accessible-name and form-label rules are migrated to
[Accessibility](topics/accessibility.md). JSX, accessibility-API, and web form
association mechanisms are non-normative
[Accessibility Recipes](reference/recipes/accessibility.md).

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
