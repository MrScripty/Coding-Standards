# Milestone 3 Empty-Impact Coverage Gate

## Result

Missing policy-consumer coverage can no longer look like a successful empty
impact result. Analysis selects the target coverage side for every changed
policy unit and emits one mandatory `audit-coverage` obligation whenever that
subject lacks a current generated certificate. This rule is independent of the
number of declared relationships or selected impact candidates.

The obligation binds the exact coverage requirement and authority view,
semantic revision, policy representation and structure, and coverage decision
contract. It permits only a `coverage-attestation` submission. Once an authored
attestation matches the exact requirement, coverage compilation generates the
certificate and the obligation disappears.

## Expiration

Coverage compilation remains fail-closed for registered attestations that do
not match a current requirement. Tests prove that changing either an
independently fingerprinted horizon member or the subject's relationship set
expires the old attestation with `COVERAGE.STALE_ATTESTATION`. The stale record
cannot be ignored, treated as an empty certificate, or converted into a
successful no-consumer claim.

## Boundaries

- Proposed coverage is selected for additions and surviving changed policy
  identities; accepted coverage is selected for removals.
- The coverage gate does not infer relationships from horizon content.
- A certificate proves bounded discovery completeness, not change-specific
  consumer dispositions.
- Empty impact is permitted only after current bounded coverage is certified.
- Final report set-equality enforcement remains part of Milestone 4 packet and
  completion implementation.

## Verification

- Standards analysis: 51 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Public contract validator: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Missing-certificate, certified-empty, horizon-expiration,
  relationship-expiration, addition-side, removal-side, obligation schema, and
  decision-contract cases passed.
- Declarative verification: 218 of 218 suites passed.
- Plan structure and `git diff --check` passed.
- The complete mixed checkpoint is reserved for the Milestone 3 boundary after
  the immediately following move/split/merge slice. The preceding applicability
  slice passed the complete checkpoint with all 53 retained Bash checkers.
