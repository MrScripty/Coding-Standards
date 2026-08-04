# Diagnostic Mechanism Recipes

**Standards metadata**

- ID: `reference.recipes.diagnostics`
- Role: `reference`
- Level: `ADVISORY`
- Applies when: A selected Diagnostics contract needs an illustrative implementation mechanism.
- Does not apply when: Diagnostic policy or mechanism selection is unresolved.
- Requires: `topic.diagnostics`
- Specializes: `none`
- Verification: Reference-boundary checks keep examples non-normative and linked to Diagnostics.
- Canonical owner: `reference/recipes/diagnostics.md`

This material is non-normative. Select purpose, audience, context, lifecycle,
disclosure, and failure behavior through [Diagnostics](../../topics/diagnostics.md)
before adapting a mechanism.

## Adapting A Mechanism

Use only the fields, lifecycle observations, propagation, and channel required
by the selected contract. Product APIs, logger calls, trace libraries, context
types, and identifier formats shown here are examples rather than defaults.
