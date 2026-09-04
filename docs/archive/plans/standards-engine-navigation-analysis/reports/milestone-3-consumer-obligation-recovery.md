# Milestone 3 Consumer-Obligation Recovery

## Superseding Result

Milestone 3 is accepted through this recovery. The earlier lifecycle-selection
report remains valid evidence for classification and traversal, but its claim
to complete Milestone 3 is superseded because applicable policy-impact
candidates did not yet produce consumer-review obligations.

## Obligation Result

`standards_analysis` now converts every definitely applicable policy-impact
trace into a canonical consumer selection. Selections group only on exact
consumer identity, canonical review scope, and review-contract identity.
Overlapping scopes are not inferred to be compatible.

Each selection derives one consumer-review obligation containing sorted,
unique reasons. Every reason retains the selecting policy unit, edge,
relationship kind, evidence owner, and content-addressed accepted or proposed
trace handles. The source and evidence-owner sets derive from those reasons;
they are not separately authored.

The decision fingerprint binds the complete changed-policy state, exact
relationship semantic dependencies, accepted and proposed traces, normalized
scope, complete review contract, referenced applicability fact values, and
required evidence owners. Input reordering and duplicate traces are stable;
adding or removing a selector or changing a fact value, scope, or contract
changes the obligation identity.

## Applicability Result

- `true` policy traces contribute to consumer review.
- `false` traces contribute no review.
- `unknown` traces retain exact applicability questions and whole-artifact
  resolution work.
- A definite and an unknown trace reaching one consumer produce both the
  definite review and unresolved applicability work.
- Non-policy graph traces never become consumer reviews.

Accepted-only relationship removals and proposed-only additions both remain
reviewable. Compatible causes consolidate into one review; different exact
scopes or review contracts remain separate.

## Contract Cutover

The public A1 contract is version 4. Singular obligation `source` and `reason`
were replaced by nonempty plural `reasons`; consumer obligations expose their
immutable review contract. Content-addressed domains advanced to
`coding-standards:obligation:v2` and `coding-standards:packet:v2`, and packet
schema version 2 replaced version 1. Runtime types, schema, examples, identity
fixtures, packet projections, and tests changed together. No compatibility
interpretation remains.

## Verification

- Graph engine: 35 tests passed.
- Standards metadata: 17 tests passed.
- Applicability: 9 tests passed.
- Policy impact: 7 tests passed.
- Standards graph: 2 tests passed.
- Standards analysis: 72 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Contract validation: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 114 definitions passed.
- Declarative verification: 218 of 218 suites passed.
- Complete checkpoint: all 218 declarative suites and 53 retained Bash
  checkers passed.
- Plan structure, Markdown links, and `git diff --check` passed.

## Next Boundary

Milestone 4 may compile reading plans from authoritative obligations. It must
not traverse policy-impact relationships a second time or independently infer
affected consumer scopes.
