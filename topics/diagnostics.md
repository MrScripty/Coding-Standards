# Diagnostics

**Standards metadata**

- ID: `topic.diagnostics`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes diagnostic context, causal identity, reporting, propagation, retention, sampling, redaction projection, or a diagnostic claim.
- Does not apply when: The change affects no diagnostic behavior or claim and preserves every selected diagnostic contract unchanged.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Diagnostics owner and activity-context decision fixtures plus claim-matched producer, consumer, disclosure, lifecycle, and failure evidence.
- Canonical owner: `topics/diagnostics.md`

## Diagnostic Authority

Diagnostics projects information about an operation or outcome for a selected
consumer or operator. Record the diagnostic purpose, audience, owning operation
or event, required context, disclosure authority, lifecycle, destination, and
evidence before selecting a mechanism.

A typed business or protocol outcome remains owned by its contract. Emitting a
diagnostic does not classify, handle, recover, retry, suppress, or convert that
outcome and cannot replace returning it to the responsible caller.

## Diagnostic Selection

Select a diagnostic only when an accepted operator, consumer, verification, or
support claim requires observable information beyond the owned result. Select
its channel, detail, timing, sampling, and retention from that claim and the
available application and operational capabilities.

Logging, tracing, metrics, events, status surfaces, exceptions, and persisted
records are possible projections, not universal requirements or substitutes.
Success through one channel does not prove another channel or the underlying
operation.

## Causal Identity And Context

Use operation, event, parent, or correlation identity only when the selected
workflow requires observations to be associated across applicable boundaries.
Define creation, propagation, uniqueness, scope, invalidation, and terminal
behavior from that workflow. Do not generate or forward correlation identifiers
merely because multiple layers exist.

Carry only bounded context required by the selected audience and claim. Field
availability does not authorize disclosure. Apply Security authority before
including sensitive data and preserve the selected redaction at every
projection and transport boundary.

## Lifecycle And Failure

Define which start, progress, completion, failure, cancellation, retry, and
recovery observations are required. Emit each selected terminal observation
once at the boundary that owns the diagnostic projection; do not report the
same failure independently at every layer.

Specify diagnostic channel failure, buffering, backpressure, recursion,
shutdown, and retention behavior where applicable. A failed diagnostic channel
does not change the operation outcome or authorize a successful diagnostic
claim.

## Responsibility Boundaries

Contracts owns outcome meaning. Resilience owns failure handling and recovery.
Security owns sensitive-data authority. Performance owns performance claims.
Verification owns evidence sufficiency. Tooling owns collection, storage, and
orchestration mechanisms. Application, boundary, language, and framework
profiles own their accepted adapters.

Diagnostics owns only the generic projection contract and does not mandate a
telemetry product, fixed application layers, correlation model, transport,
storage system, or language mechanism.

## Typed Outcomes

Return `unavailable` when required purpose, audience, authority, context,
propagation, redaction, destination, or capability cannot be established;
`invalid` for contradictory context, unsafe disclosure, broken causal identity,
duplicate terminal reporting, or a false diagnostic claim; and `unsupported`
when the selected mechanism cannot represent a supported diagnostic contract.

Do not fall back to raw context, guessed identity, duplicate logs, swallowed
outcomes, a nearby channel, silent discard, or reported success without the
selected diagnostic evidence.
