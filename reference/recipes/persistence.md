# Persistence Mechanism Recipes

**Standards metadata**

- ID: `reference.recipes.persistence`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A selected Persistence boundary contract needs an illustrative implementation mechanism.
- Does not apply when: Durable-state policy, authority, invariants, or mechanism selection is unresolved.
- Requires: `profile.boundary.persistence`
- Specializes: `none`
- Verification: Reference-boundary checks keep examples non-normative and linked to the Persistence profile.
- Canonical owner: `reference/recipes/persistence.md`

This material is non-normative. Select durable authority, supported states,
invariants, mechanism capabilities, typed outcomes, and evidence through the
[Persistence boundary profile](../../profiles/boundaries/persistence.md) before
adapting a mechanism.

## Adapting A Mechanism

Use only the transaction, replacement, journal, ledger, migration, locking, or
store-adapter behavior required by the selected contract. Database products,
file layouts, migration names, version tables, startup hooks, rollback commands,
and phase sequences are examples rather than defaults.
