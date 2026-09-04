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


## Decision Traceability Examples

The following legacy impact-map, installation, and invocation material is
non-normative. Canonical Documentation policy must select every represented
boundary, artifact, input, and enforcement behavior before adaptation.


### Impact Map

Follow the
[Documentation Workflow](../../workflows/documentation.md). Automated enforcement
must operate on project-owned facts rather than treating every source change as
a decision change.

Configure only paths whose modification is known to alter a durable
responsibility, contract, decision, or procedure:

```text
trigger_path	boundary_id	profile	artifact_path
src/api/public-contract.ts	api	contract-readme	src/api/README.md
src/engine/policy/	engine-policy	adr	docs/adr/ADR-001-engine-policy.md
ops/recovery/	recovery	runbook	docs/runbooks/recovery.md
```

- `trigger_path` is an exact repository-relative path, or a prefix when it ends
  in `/`.
- `boundary_id` is a stable project-owned identifier.
- `profile` is `boundary-readme`, `contract-readme`, `adr`, or `runbook`.
- `artifact_path` is the canonical durable artifact that owns the knowledge.

Do not map broad source directories unless every change beneath that prefix
really changes the named durable knowledge. Routine implementation paths stay
out of the map.

An ADR row requires `## Affected Boundaries` with an exact entry such as:

```markdown
- `boundary:engine-policy`
```

This association prevents an unrelated changed ADR from satisfying every
boundary. A mapped artifact is not interchangeable with another artifact type.

```bash
mkdir -p scripts .standards
cp tools/decision_traceability/decision_traceability/check.py \
  scripts/check-decision-traceability.py
cp templates/decision-traceability-map.tsv \
  .standards/decision-traceability.tsv
```

Copy the standalone
[Python decision-traceability checker](../../tools/decision_traceability/decision_traceability/check.py)
into your repo as `scripts/check-decision-traceability.py` and replace every
example map row with project-owned facts. It uses only Python's standard
library and Git.

### Explicit Diff Modes

Every invocation names what it inspects:

- `--mode staged` reads only the index with `git diff --cached`;
- `--mode range` requires explicit `--base-ref` and `--head-ref` commits and
  reads their three-dot diff.

Missing modes, maps, refs, or invalid refs fail with a configuration diagnostic.
The checker never guesses a branch, falls back to another range, or silently
skips an unresolved diff. It evaluates both prior and current map rows so
removing a row cannot hide the change that deletes or relocates a mapped path.

Add staged mode to pre-commit:

```yaml
pre-commit:
  commands:
    decision-traceability:
      run: >-
        python3 ./scripts/check-decision-traceability.py --mode staged
        --map .standards/decision-traceability.tsv
```

Use explicit pull-request commits in CI:

```yaml
jobs:
  quality:
    steps:
      - name: Decision traceability
        run: |
          python3 ./scripts/check-decision-traceability.py \
            --mode range \
            --map .standards/decision-traceability.tsv \
            --base-ref "${{ github.event.pull_request.base.sha }}" \
            --head-ref "${{ github.event.pull_request.head.sha }}"
```


The paths, boundary identifiers, profiles, artifact locations, commands, map
location, staged hook, GitHub job, and provider expressions are examples only.
They define no fallback impact map, diff range, or documentation requirement.
