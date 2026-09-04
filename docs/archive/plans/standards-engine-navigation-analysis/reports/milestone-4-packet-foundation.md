# Milestone 4 Immutable Packet Foundation

## Result

`standards_analysis` now exposes an immutable snapshot-bound pending packet and
all four accepted typed submission variants. The packet is a compact work queue
over analysis results; it does not load repository state, traverse relationships,
or decide whether a submission closes an obligation.

## Identity And State

Packet construction canonicalizes change and work ordering, rejects duplicate
obligation or question IDs, and requires outstanding work. Its content identity
uses the exact schema-owned projection over base/proposed snapshots, changes,
changed units, obligations, questions, reading entries, and contract-relevant
provenance.

Display summaries, derived next operations, report-only versions, and analyzer
or graph implementation versions remain provenance outside packet identity.
Changing either bound snapshot changes the packet ID. Reordering otherwise
identical obligations does not.

Obligation identities remain owned by their existing narrower decision
fingerprints. The packet neither rewrites those identities nor makes them depend
on unrelated packet work, preserving safe carry-forward when a later packet
contains the same obligation dependencies.

## Typed Work

- Questions and obligations retain their typed states and permitted outcomes.
- Fact answers, consumer dispositions, impact dispositions, and coverage
  attestations are immutable typed values matching the canonical schema.
- Review submissions require at least one uniquely identified evidence
  reference with an exact SHA-256 digest and provider-contract version.
- `next_operations` is derived from required state. Required questions produce
  fact-answer operations; required obligations produce only their permitted
  submission operations; blocked or resolved work produces none.

Disposition authorization, fingerprint comparison, evidence-provider
validation, packet staleness during `resolve`, and completed-report generation
remain later Milestone 4 behavior.

## Verification

- Standards analysis: 64 tests passed.
- Standards Engine: 15 tests passed.
- Standards metadata: 17 tests passed.
- Policy-impact compiler: 7 tests passed.
- Graph engine: 35 tests passed.
- Standards verifier: 380 tests passed.
- Public contract validator: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Declarative verification: 218 of 218 suites passed.
- `git diff --check` passed.

## Next Boundary

The next slice derives bounded reading plans and their deterministic dependency
and scope ordering. Packet resolution, decision reuse, report completion, and
agent façade integration remain outside this slice.
