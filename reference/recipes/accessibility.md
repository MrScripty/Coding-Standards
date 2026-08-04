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
