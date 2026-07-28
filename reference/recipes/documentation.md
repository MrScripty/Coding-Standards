# Documentation Recipe

**Standards metadata**

- ID: `reference.recipes.documentation`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A contributor needs examples for comments, Markdown, public interfaces, or algorithm explanations.
- Does not apply when: Documentation applicability, required artifacts, or consumer contracts are being decided.
- Requires: `workflow.documentation`
- Specializes: `none`
- Verification: Documentation-reference consolidation dispositions and link checks.
- Canonical owner: `reference/recipes/documentation.md`

This recipe illustrates the
[Documentation Workflow](../../workflows/documentation.md). It does not require
documentation for every public symbol or algorithm, define a project TODO
format, or override language-specific documentation tools and repository
formatters.

## Comments

Comments are most useful when they preserve rationale that names and structure
cannot express:

```typescript
// Filter first because transforming inactive records performs a remote lookup.
const active = users.filter((user) => user.isActive);
```

When a name can express the same fact, prefer the name:

```typescript
if (user.isAdmin()) {
    authorize();
}
```

A tracked TODO can use the repository's issue convention:

```typescript
// TODO(#123): Remove this branch after the v2 endpoint is retired.
```

Language-native documentation comments can describe a consumer-visible
contract:

```typescript
/**
 * Calculates the total price including tax.
 *
 * @param items - Cart items to total.
 * @param taxRate - Tax rate as a decimal.
 * @returns Total price with tax applied.
 */
declare function calculateTotal(items: Item[], taxRate: number): number;
```

## Markdown

Add a language identifier to fenced blocks when the renderer supports one.
Use `text` for output or prose-like diagrams:

````markdown
```text
request -> validation -> execution
```
````

Portable tables use leading and trailing pipes. Let the repository formatter
decide alignment and padding:

```markdown
| Name | Purpose |
| --- | --- |
| input | Accepted request data |
| output | Produced result |
```

## Public Interfaces

Document semantics that a consumer cannot infer reliably from the declaration,
especially lifecycle, failures, side effects, ordering, and compatibility.
Avoid repeating types and names as prose.

```typescript
/**
 * Authenticates credentials and starts a new session.
 *
 * Rotates any anonymous session identifier after successful authentication.
 *
 * @throws AuthError when the credentials are rejected.
 */
declare function login(credentials: Credentials): Promise<Session>;
```

The selected language profile or documentation generator determines exact tag
syntax. The canonical contract, not this example, owns required behavior.

## Algorithms

An explanation can name the properties a maintainer must preserve:

```markdown
# Topological ordering

Produces an ordering in which each source precedes every node it points to.

## Preconditions

- Node identifiers are unique.

## Postconditions

- Every node occurs exactly once.
- A cycle returns a typed cycle diagnostic.

## Complexity

- Time: `O(V + E)`.
- Space: `O(V)`.

## Attribution

Based on Kahn's algorithm, adapted to preserve deterministic node ordering.
```

Useful details may include preconditions, postconditions, invariants,
complexity, failure outcomes, attribution, or a small text diagram. Include
only details that are non-obvious and material to maintenance or use.
