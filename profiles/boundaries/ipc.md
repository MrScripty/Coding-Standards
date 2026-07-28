# IPC Boundary Profile

**Standards metadata**

- ID: `profile.boundary.ipc`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Structured requests, responses, commands, queries, or events cross a process, message, plugin-host, worker, or independently deployed component boundary.
- Does not apply when: Values remain inside one trusted process without serialization, message dispatch, or independently evolving producer and consumer.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `topic.security`
- Specializes: `topic.contracts`, `topic.security`
- Verification: Action-specific payload decision fixtures and affected producer/consumer boundary tests.
- Canonical owner: `profiles/boundaries/ipc.md`

## Boundary Authority

Treat every received representation as unknown at the consumer boundary.
Producer-side static types, generated bindings, preload typing, transport
parsing, and successful deserialization do not prove the consumer's runtime
contract.

Use the [Contracts topic](../../topics/contracts.md#runtime-decoding-at-boundaries)
for generic runtime proof and the [Security topic](../../topics/security.md#untrusted-structured-input)
when the message can authorize work or side effects.

## Decode Before Dispatch

Decode in this order:

1. validate the envelope shape and applicable transport-independent metadata;
2. decode the complete category/action discriminant;
3. select the schema for that exact supported pair;
4. validate every payload field, cross-field rule, and applicable correlation
   field;
5. construct a closed validated variant; and
6. dispatch only that validated variant.

The selected operation determines the required payload proof. Validating only
that an envelope is an object or that category and action are strings is
incomplete.

Projects own their category and action vocabulary. This profile does not
mandate command/query/event names, a message catalog, a transport, a language,
or a validation library.

## Variant And Schema Outcomes

Return:

- `invalid` for a malformed envelope, failed metadata, recognized action with
  an invalid payload, incomplete validation, or dispatch of an unvalidated
  representation;
- `unsupported` for a well-formed category/action pair outside the supported
  contract; or
- `unavailable` when the required schema or decoder for a supported pair cannot
  be obtained.

An unknown category, unknown action, or mismatched category/action pair cannot
fall through to a generic handler. A missing decoder cannot select a weaker
schema.

## Extra Fields And Metadata

The contract states whether extra fields are rejected, accepted, or preserved
for a versioned purpose. When no extra-field policy is defined, receiving
extras is `invalid`; silently discarding them can hide producer drift or
smuggled input.

Validate correlation identifiers, version markers, timestamps, routing keys,
and other metadata whenever the selected variant gives them semantics.
Envelope validity does not exempt action-specific metadata.

## Dispatch Contract

Dispatch accepts only closed validated variants. It must not:

- cast an unknown or generic payload to the selected action type;
- pass the original received object alongside the validated value;
- use a default action or fall-through branch for unknown pairs;
- reinterpret validation failure as another action; or
- retry through an alternate permissive decoder.

Exhaustive dispatch is evidence that every supported variant has an explicit
handler. A typed `unsupported` result remains distinct from malformed
`invalid` input and unavailable decoding capability.

## Verification

Affected tests cover:

- valid variants from each supported category used by the change;
- malformed envelopes and invalid metadata;
- unknown and mismatched category/action pairs;
- missing, wrong-type, bounded, and cross-field payload values;
- explicit extra-field acceptance and rejection;
- producer-only and envelope-only typing attempts;
- unavailable schemas or decoders; and
- proof that handlers receive validated variants rather than raw payloads.
