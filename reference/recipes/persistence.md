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

## Illustrative Staged Publication

When the selected store and invariant require isolated staging, an adapter may
use this shape:

```text
facts = read_authoritative_facts(request)
candidate = construct_candidate(facts, request)
prove_preconditions(candidate)
staged = stage_outside_authoritative_visibility(candidate)
publish_with_selected_atomicity(staged)
prove_authoritative_postcondition()
```

Omit, combine, or replace steps when the selected mechanism proves the same
contract differently. The names and order above do not authorize placeholders,
fixed phase counts, append-only behavior, debug-only proof, or partial
authoritative publication.

## Illustrative Migration Adapters

A repository may represent selected migration identity through numbered files,
timestamped files, embedded artifacts, package resources, or generated records.
For example:

```text
migrations/001_initial_schema.sql
migrations/002_add_preferences.sql
```

A store adapter may persist migration identity, integrity, and completion in a
dedicated table or in another authoritative record:

```sql
CREATE TABLE migration_ledger (
    identity TEXT PRIMARY KEY,
    integrity TEXT NOT NULL,
    completed_at TEXT NOT NULL
);
```

These filenames, fields, SQL types, and table shape are illustrative. They do
not select lexical ordering, a version table, SQL, timestamps, one ledger schema,
or one migration tool.

An accepted lifecycle adapter, including an explicitly selected startup adapter,
may call the same migration-execution service after Contracts and Persistence
have selected the transition. The adapter must preserve typed outcomes; it does
not discover pending work by guess, repeat an unproven migration, select
rollback, or convert migration failure into successful startup.
