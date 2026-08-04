# Accessibility Recipes

**Standards metadata**

- ID: `reference.recipes.accessibility`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A project has selected an accessibility outcome and needs illustrative platform or interface mechanisms.
- Does not apply when: Accessibility outcomes, supported users, modalities, platforms, conformance obligations, tools, or acceptance evidence are being selected.
- Requires: `topic.accessibility`
- Specializes: `none`
- Verification: Accessibility-reference metadata, routing, authority, and legacy-extraction checks.
- Canonical owner: `reference/recipes/accessibility.md`

This material is non-normative. [Accessibility](../../topics/accessibility.md)
owns user-access outcomes and conformance obligations. Application, frontend,
language, and framework profiles own concrete mechanisms. Tooling and
Verification own automation and evidence selection.

## Adapting A Mechanism

Before adapting an example, identify the accepted user task, required outcome,
platform, modalities, capability constraints, conformance obligations, and
evidence claim. Treat product names, markup, event handling, style rules,
assistive-technology procedures, lint configuration, and commands as
replaceable mechanisms rather than policy.

Legacy web and tooling examples will move here only with the semantic child
that establishes their canonical outcome. Their presence will not make HTML,
ARIA, CSS, JSX, a browser, an input method, an assistive technology, a lint
product, a rule set, or a CI command a default.

## Web Interaction Mechanisms

These examples illustrate one web projection after action, navigation, and
custom-interaction outcomes have been selected. They do not establish HTML,
ARIA, JSX, event names, keys, or attributes as generic policy.

An action might use a native button:

```tsx
<button type="button" onClick={onClose} aria-label="Close dialog">
  <XIcon />
</button>
```

A navigation outcome might use a link with an actual destination:

```tsx
<a href="/settings">Settings</a>
```

When accepted web constraints require a generic element, the projection must
implement every selected role, modality, state, name, and feedback obligation.
One illustrative projection is:

```tsx
<div
  role="button"
  tabIndex={0}
  onClick={onClose}
  onKeyDown={(event) => {
    if (event.key === "Enter" || event.key === " ") onClose();
  }}
  aria-label="Close dialog"
>
```

The specific keys and attributes above follow one selected web contract. Do not
copy them as proof that another role, platform, modality, state model, or
assistive-technology contract is satisfied.

## Web Focus Mechanisms

After a web contract selects visible focus evidence, one CSS mechanism might be:

```css
button:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

The selector, dimensions, color, and outline mechanism are illustrative. Test
the selected contrast, visibility, state, browser, theme, and modality claims;
do not copy these values as acceptance thresholds.

For one selected modal interaction, a web implementation might move focus on
entry, constrain movement while modal, support a selected Escape dismissal,
and restore focus on exit. Each behavior is conditional on the accepted task,
platform, nesting, target-lifetime, and cancellation contract. “Trap focus and
close on Escape” is not a universal dialog recipe.

## Web Naming And Form Mechanisms

After selecting naming and input-relationship outcomes, a web projection might
use visible content, hidden content, or an accepted accessibility API name:

```tsx
<button type="button" onClick={onDelete} aria-label="Delete item">
  <TrashIcon />
</button>
```

One explicit form association might use matching identifiers:

```tsx
<label htmlFor="username">Username</label>
<input id="username" type="text" />
```

When the selected web contract permits a non-visible name, another mechanism is:

```tsx
<input type="search" aria-label="Search models" placeholder="Search..." />
```

These attributes and JSX forms are illustrative. Placeholder text, visual
proximity, an identifier match, or an API attribute proves only the relationship
and modalities covered by the selected implementation and evidence.

## Web Image And Icon Mechanisms

After content ownership classifies one web image as decorative, an illustrative
HTML projection can suppress alternate text:

```tsx
<img src="divider.svg" alt="" />
```

An informative image might project its selected equivalent meaning:

```tsx
<img src="error-icon.svg" alt="Error" />
```

An icon already accompanied by an accepted visible name might be hidden from a
selected accessibility API projection:

```tsx
<button type="button">
  <SaveIcon aria-hidden="true" />
  Save
</button>
```

The empty `alt`, text value, `aria-hidden` attribute, icon component, and parent
control are web mechanisms. They do not classify the content or prove equivalent
meaning across other states, contexts, platforms, or modalities.

## Legacy JSX Lint Mechanisms

The legacy web example used `eslint-plugin-jsx-a11y`, installed with an npm
development-dependency command, and named rules such as
`click-events-have-key-events`, `no-static-element-interactions`,
`anchor-is-valid`, `alt-text`, and `label-has-associated-control`. It also ran
those checks as CI errors.

This is historical mechanism information only. Tooling must select the product,
dependency procedure, rules, scope, severity, command, schedule, and CI
placement from current repository contracts. Verification must define what any
result proves. Do not treat this list as a minimum, current syntax, installation
authority, or accessibility acceptance evidence.
