# HTTP Projection Mechanism Recipes

**Standards metadata**

- ID: `reference.recipes.http`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A Contracts-selected protocol projection is implemented through an HTTP adapter.
- Does not apply when: Outcome meaning, protocol mapping, response representation, disclosure, or adapter capability is unresolved.
- Requires: `topic.contracts`, `topic.security`
- Specializes: `none`
- Verification: Reference-boundary checks keep HTTP examples non-normative and linked to Contracts.
- Canonical owner: `reference/recipes/http.md`

This material is non-normative. Select the authoritative outcome, HTTP contract,
response representation, disclosure projection, consumers, and evidence through
[Contracts](../../topics/contracts.md#protocol-outcome-projection) before
adapting a mechanism.

## Illustrative Projection Record

An application may record an explicit mapping such as:

```text
operation: create-project
outcome: revision-conflict
http-version: application-v2
status: 409
body-variant: simple-error
disclosure: public-summary
```

The names, status, body variant, and disclosure label are illustrative. They do
not authorize a shared mapping for another operation, version, or consumer.

## Illustrative Response Shapes

A selected `simple-error` representation might use:

```json
{
  "error": "The project changed before this request completed."
}
```

The message is permitted only when the Security-owned disclosure decision
allows it. A stable code, structured problem representation, empty body, or
other selected shape may be required instead; this example does not make any
field universal.

One application contract could select the following mappings:

| Selected outcome | Illustrative HTTP status |
|---|---:|
| resource-read | 200 |
| resource-created | 201 |
| request-invalid | 400 |
| resource-absent | 404 |
| revision-conflict | 409 |
| internal-unavailable | 500 |

These values are not defaults. Missing outcome authority or mapping remains a
typed diagnostic; an adapter must not choose the nearest row, default an unknown
failure to `500`, or infer operation success from a `2xx` status.
