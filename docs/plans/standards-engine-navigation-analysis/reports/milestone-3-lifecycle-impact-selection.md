# Milestone 3 Lifecycle Impact Selection

## Result

Milestone 3 is accepted. `standards_analysis` classifies all six admitted
change kinds and selects exact accepted and proposed graph contexts without
creating another graph implementation. Move, split, and merge preserve their
distinct identity and lifecycle meaning rather than being reduced to additions,
removals, or modifications.

## Lifecycle Rules

- A same-module move retains one canonical ID and accepted semantic revision,
  changes its heading locator, and selects `policy-impact` on both sides.
- A cross-module move also selects the former and proposed module nodes through
  `standards-requires` and `standards-specializes` so ownership-context changes
  remain visible.
- A split requires one accepted predecessor, one exact proposed tombstone, and
  at least two new active successors. The tombstone and successors must be
  reciprocal, and each successor starts under an exact revision-1 semantic
  proposal.
- A merge requires at least two accepted predecessors, exact proposed
  tombstones that each name the sole successor, and one new active successor
  carrying the complete predecessor set under a revision-1 semantic proposal.
- Split and merge predecessor/successor roles remain explicit in
  `ChangedPolicyUnit`; they are not aliases or implicit identity continuity.

## Impact Selection

The accepted and proposed graph registries are queried separately using the
schema-owned group matrix, then unioned by the existing generic graph engine's
stable edge identities. Tests prove that cross-module moves retain policy and
module dependency context, splits retain the predecessor plus every successor
consumer, and merges retain every predecessor plus the successor consumer.

Lifecycle validation remains metadata-owned. Analysis consumes the immutable
corpora and translates invalid change descriptors into typed analysis failures;
it does not parse sidecars or duplicate reciprocal-lifecycle validation.

## Verification

- Graph engine: 35 tests passed.
- Standards applicability: 9 tests passed.
- Standards metadata: 17 tests passed.
- Policy-impact compiler: 7 tests passed.
- Standards graph: 2 tests passed.
- Standards analysis: 57 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Public contract validator: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Declarative verification: 218 of 218 suites passed.
- Complete mixed checkpoint: generated evidence, all 218 declarative suites,
  and all 53 retained Bash checkers passed.
- Plan structure and `git diff --check` passed.

## Next Boundary

Milestone 4 may now consume complete deterministic change and obligation
foundations. Its first bounded slice owns immutable packet state, stable
obligation identities, typed questions and submissions, required evidence, and
state-derived next operations. Reading-plan ordering, decision reuse, final
report completion, renderers, and end-to-end agent acceptance remain later
Milestone 4 work.
