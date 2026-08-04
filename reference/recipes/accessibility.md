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
