# Milestone 7 Row 33 HTTP Error Contract Decomposition

## Owner Contract

`topics/contracts.md` is the sole normative owner for outcome meaning,
response representation, and projection through a selected protocol contract.
The protocol or adapter specializes an already authoritative outcome; transport
success, status class, body shape, or decoder success cannot redefine it.

Contracts does not mandate HTTP, a universal status table, one JSON envelope,
raw human-readable messages, one server error type, a client parsing sequence,
or a success/failure encoding. IPC remains transport-independent. Security
owns disclosure, Diagnostics owns reporting projections, Resilience owns retry
and recovery, and Verification owns claims.

## Exact Ownership

- `STD-0126` becomes an index and `STD-0127` refines selected outcome-to-
  transport projection.
- `STD-0128` and `STD-0129` split response and status consistency policy from
  fixed JSON-envelope and status-table mechanisms.
- `STD-0130`, `STD-0131`, and `STD-0132` split producer/consumer proof and
  protocol-consistency policy from pseudocode and fixed HTTP examples.
- `STD-0133` becomes an index because uniformity, observability, and
  self-documentation are conditional claims rather than independent policy.

Each identifier receives exactly one disposition. Mechanisms move only to
`reference/recipes/http.md`, which is non-normative and cannot select policy.

## Ordered Children

1. `33.1`: migrate `STD-0126` through `STD-0129` selected outcome projection
   and response representation, create the HTTP recipe boundary, and extract
   the fixed JSON envelope and status table.
2. `33.2`: migrate `STD-0130` through `STD-0133` producer and consumer adapter
   proof, extract pseudocode and fixed examples, retire unsupported benefit
   claims, replace duplicate Architecture policy with an index, and close row
   33.

Shared decomposition, dispositions, plan, ledger, and cursor assertions remain
serial. Each child may additionally touch only Contracts, the HTTP recipe,
the legacy HTTP section, and its focused fixtures and checker.

## Typed Outcomes And No Fallback

Return `unavailable` when outcome authority, protocol contract, representation,
adapter, disclosure decision, or required evidence is absent; `invalid` when
the projection contradicts the selected outcome or representation; and
`unsupported` when a well-formed outcome or representation has no supported
projection.

Do not guess a status or envelope, default an unknown failure to `500`, treat
transport success as domain success, hide a contradictory error in `200`,
expose raw diagnostic text, switch decoders, retry, recover, or claim
observability without the applicable canonical contract.

## Re-plan Triggers

Stop if implementation requires an HTTP profile, transport ownership in IPC,
a universal status/envelope mapping, Security/Diagnostics/Resilience authority
transfer, multiple dispositions per identifier, a third semantic child, or
files outside the approved write set.
