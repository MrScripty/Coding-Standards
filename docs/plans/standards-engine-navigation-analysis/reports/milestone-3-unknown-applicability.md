# Milestone 3 Unknown Applicability

## Result

Policy-impact applicability is now evaluated inside impact selection from the
immutable programs compiled by `standards_applicability`. Accepted and proposed
traces retain their own truth and exact unresolved facts. The candidate union
uses three-valued disjunction: `true` dominates, then `unknown`, then `false`;
generic relationships remain `not-declared`.

An aggregate `unknown` result remains unknown while analysis assigns a
conservative whole-artifact review scope. Analysis generates one question per
exact material fact and one mandatory `applicability-resolution` obligation per
relationship and fact. Each obligation links typed source, target, edge, fact,
question, scope, and decision-fingerprint fields and permits only a
`fact-answer` submission.

## Boundaries

- Analysis consumes compiled applicability programs and does not parse authored
  expressions or duplicate three-valued evaluation.
- Missing facts default to valid unknown states; malformed facts and mismatched
  fact sets remain invalid.
- Accepted and proposed policy-impact fact schemas must currently match. Schema
  evolution rejects explicitly instead of being treated as false or as a
  permanent equality invariant.
- A definitely applicable accepted or proposed trace makes the union applicable
  without unnecessary resolution work.
- A false candidate remains available for deterministic provenance but creates
  no applicability-resolution obligation.
- Conservative scope selection does not convert unknown to true.

## Verification

- Standards applicability: 9 tests passed.
- Policy-impact compiler: 7 tests passed.
- Standards analysis: 48 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Public contract validator: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Unknown, false, true-over-unknown union, exact material-fact, incompatible
  fact-set, schema-evolution, question, obligation, and deterministic scope
  cases passed.
- Declarative verification: 218 of 218 suites passed.
- Complete mixed checkpoint: generated evidence, 218 declarative suites, and
  all 53 retained Bash checkers passed.
- Plan structure and `git diff --check` passed.
