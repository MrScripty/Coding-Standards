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

## Illustrative Producer Adapter

An adapter may use an explicit lookup and proof sequence:

```text
outcome = execute_validated_operation(request)
mapping = selected_http_contract.lookup(operation, version, outcome.variant)
response = mapping.construct(outcome, selected_disclosure)
mapping.prove_complete(response)
emit_once(response)
```

The adapter may use a shared error type, middleware, exceptions, result values,
or direct response construction. None of those mechanisms may classify an
unknown outcome, select a default status, expose an unapproved message, or emit
before complete proof.

## Illustrative Consumer Adapter

A consumer may adapt a response through one complete decoder:

```text
raw_response = receive()
mapping = selected_http_contract.for(operation, version)
validated_response = mapping.decode_complete(raw_response)
outcome = mapping.construct_outcome(validated_response)
```

The decoder may inspect status before the body as an optimization, but it must
still validate every response part required by the selected variant. A generic
catch-all branch, alternate decoder, empty object, or readable body is not a
valid replacement for an unsupported or unavailable mapping.

## Selected HTTP Success And Error Representations

One contract may represent a missing resource as:

```text
HTTP/1.1 404 Not Found
{"error": "Project not found"}
```

Another explicitly governed application protocol may carry a rejected
application outcome through successful HTTP transport:

```text
HTTP/1.1 200 OK
{"errors": [{"code": "PROJECT_NOT_FOUND"}]}
```

Neither example is universally good or bad. The valid representation is the one
selected and proven by the producer and every applicable consumer. Human-
readable text remains subject to the Security-owned disclosure decision.

## Conditional Interpretation Claims

Uniform handling, intermediary visibility, monitoring, and self-documentation
are claims, not automatic benefits of status codes. Verify each claim against
the actual consumer, proxy, cache, monitoring rule, body decoder, and disclosure
contract. A `4xx` or `5xx` count does not by itself prove operation-level
failure observability, and a `2xx` count does not prove operation success.
