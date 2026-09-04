# Milestone 7 Row 31 Diagnostics Decomposition

## Owner Contract

Create `topics/diagnostics.md` as the generic owner for selecting diagnostic
purpose, audience, causal identity, bounded context, channel, detail, sampling,
retention, redaction projection, propagation, and diagnostic failure behavior.
Contracts owns typed outcome meaning; Resilience owns failure handling and
recovery; Security owns sensitive-data authority; Performance owns performance
claims; Verification owns evidence; Tooling owns collection and storage
mechanisms; application and language profiles own their adapters.

Diagnostics does not mandate logging, tracing, metrics, exceptions, correlation
IDs, fixed layers, start/completion events, a telemetry product, or raw error
capture.

## Exact Ownership

- `STD-0089` is an `index` route created with the useful Diagnostics owner.
- `STD-0090` refines unconditional correlation and structured logging into
  selected causal-context policy.
- `STD-0091` splits generic lifecycle and propagation policy into Diagnostics
  while moving TypeScript and logger syntax to a non-normative recipe.
- `STD-0092` is an `index`; debugging, performance, and observability benefits
  are claims selected by their existing owners, not independent policy.

## Ordered Children

1. `31.1`: create and route the useful Diagnostics owner, metadata, owner
   decisions, reference boundary, and `STD-0089` index disposition.
2. `31.2`: migrate `STD-0090` through `STD-0092`, extract the legacy mechanism
   example, replace Architecture policy with a concise route, and close row 31.

Shared router, README, metadata, dispositions, plan, and ledger remain serial.
Each child may additionally touch only its owner/reference section, focused
fixtures/checker, legacy section, decomposition validation, and affected cursor
assertions.

## Typed Outcomes And No Fallback

Missing purpose, audience, authority, context, propagation, redaction, or
capability is `unavailable`; contradictory context, unsafe disclosure, duplicate
terminal reporting, or broken causal identity is `invalid`; an unsupported
selected diagnostic mechanism is `unsupported`.

Do not substitute logging for a typed outcome, generate correlation without a
selected identity contract, emit raw context, duplicate every failure at every
layer, silently discard required diagnostics, or report diagnostic success when
the selected channel failed.

## Re-plan Triggers

Stop if implementation requires Diagnostics to own business failure semantics,
recovery, security authorization, performance proof, evidence acceptance,
tooling mechanisms, a telemetry platform, multiple dispositions per identifier,
or files outside the approved write set.
