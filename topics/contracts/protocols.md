# Protocol Adapters

**Standards metadata**

- ID: `topic.contracts.protocols`
- Role: `topic`
- Level: `MUST`
- Applies when: A change projects domain outcomes into a protocol or adapts a protocol boundary.
- Does not apply when: No domain outcome or boundary representation is projected into a protocol.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/protocols.md`

## Protocol Outcome Projection

Classify the authoritative operation outcome before projecting it through a
protocol. Record the outcome authority, applicable protocol and version,
supported outcome variants, status or control metadata, response
representation, disclosure decision, consumers, and evidence that each
projection preserves the selected meaning.

The selected protocol contract decides how an outcome is represented. A
transport-level success may carry a rejected application outcome only when that
is an explicit supported representation; a transport-level failure does not by
itself classify the operation. Status, headers or equivalent control metadata,
and body must describe one consistent selected outcome. Serialization,
readability, a status class, or a familiar envelope does not establish that
consistency.

Do not infer a universal mapping from outcome names to HTTP status codes or
other protocol controls. A protocol may define different mappings for
different operations, versions, consumers, or externally governed promises.
Likewise, no JSON envelope, human-readable message field, error code, empty
body, or response wrapper is a default. Security selects what may be disclosed;
Diagnostics selects reporting projections without changing the operation
outcome.

Return:

- `unavailable` when the authoritative outcome, protocol contract,
  representation, disclosure decision, adapter capability, or required
  evidence cannot be obtained;
- `invalid` when status, control metadata, body, or disclosure contradicts the
  selected outcome or representation; or
- `unsupported` when a well-formed outcome or representation has no supported
  projection in the selected protocol contract.

Do not guess a status or envelope, map an unknown failure to a default internal
error, treat transport success as operation success, expose raw diagnostic text,
switch representations or decoders, retry, recover, or emit a partial response
as a fallback. Illustrative HTTP mechanisms are isolated in the
[HTTP projection recipes](../../reference/recipes/http.md).
## Protocol Adapter Proof

A producer adapter accepts an already authoritative operation outcome, selects
the exact operation and protocol-version projection, constructs its complete
response representation, proves status or control metadata, body, and
disclosure consistency, and only then emits the response. A shared error type,
middleware layer, exception mapping, or response wrapper is optional mechanism,
not outcome authority.

A consumer adapter treats the received response as unknown. It selects the
applicable operation and protocol-version contract, validates all required
status or control metadata, headers, content type, and body variant, constructs
the validated outcome representation, and only then exposes that outcome to its
caller. Checking status before body, body before status, or both in one decoder
is a mechanism decision; neither status nor body alone proves the outcome when
the selected contract requires both.

Producer and consumer proof must agree on every selected variant, including
success, rejection, failure, empty, and degraded responses. A protocol may
explicitly represent an application error through successful HTTP transport;
that is valid only when producer and consumer contracts select and prove the
same representation. Conversely, a status convention cannot hide a body that
contradicts it.

Adapters do not select disclosure, diagnostic reporting, retry, recovery, or
degradation policy. Security owns disclosure, Diagnostics owns reporting
projection, Resilience owns retry and recovery, and Verification owns claims
that clients, intermediaries, or monitoring systems interpret the projection.

Return `unavailable` when the adapter, mapping, decoder, disclosure decision,
consumer facts, or evidence is absent; `invalid` for incomplete proof,
contradictory response parts, unsafe disclosure, duplicate or partial emission,
or a false interpretation claim; and `unsupported` for a well-formed response
variant outside the selected contract.

Do not substitute a generic error, raw message, default internal-error mapping,
status-only or body-only interpretation, alternate decoder, successful
transport, retry, recovery, or duplicate response. Preserve the typed outcome
when complete adapter proof cannot be established.
