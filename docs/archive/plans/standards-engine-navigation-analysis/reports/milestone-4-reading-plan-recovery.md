# Milestone 4 Reading And Horizon Recovery

## Result

The bounded Milestone 4 recovery is accepted. Milestone 4 remains active;
packet staleness and decision reuse are the sole next slice.

## Reading-Plan Result

One typed compiler now derives reading plans from Router selections,
`Requires` edges, and consumer-review obligation handles. It does not traverse
policy-impact relationships or copy their semantic provenance.

Entries collapse only under an exact canonical target and scope. They retain a
sorted, unique union of typed causes, derive authority from canonical target
metadata, and apply deterministic state precedence and ordering. Direct and
dependency routing preserve every selecting rule, referenced fact, and edge.
Several compatible consumer obligations produce one entry containing their
obligation handles; the obligations remain the semantic authority.

The coordinated replacement advances the analysis contract to 2, public
interface to 5, navigation identity to 2, packet identity and schema to 3, and
completed-report identity and schema to 2. No former reading representation is
accepted under the new identities.

## Coverage Result

All 27 registered non-module targets now declare explicit reading authority:
five are `projection` and 22 are `evidence`. Node identities, aliases, paths,
groups, edges, and all 126 compiled policy-impact relationships and semantics
are unchanged.

The complete node catalog remains in `AnalysisSnapshot`. Audit-horizon
provider version 2 excludes only `nodes[].metadata.authority` from that
catalog's coverage fingerprint; unknown or future metadata remains
coverage-relevant. The final horizon contains 856 members with digest
`sha256:35ed5271ffb9573eb1ae4dd6949debd9f6aad011bb9d0b43dbbfba9eb5b077e9`.
The exact 28 requirements and node dispositions are recorded in the
[horizon-v2 audit](milestone-4-horizon-v2-audit.md).

After every horizon-affecting input was frozen, Planning and Commit received
one authorized attestation renewal. The resulting 28 attestations match all 28
requirements exactly and compile into 28 valid certificates.

## Verification

- Standards analysis: 78 tests passed.
- Standards Engine: 16 tests passed.
- Graph engine: 35 tests passed.
- Standards metadata: 17 tests passed.
- Applicability: 9 tests passed.
- Policy impact: 7 tests passed.
- Standards graph: 2 tests passed.
- Standards verifier: 380 tests passed.
- Contract validation: 29 examples, seven identity fixtures, four operation
  envelopes, and 120 definitions passed.
- Declarative verification: 218 of 218 suites passed.
- Complete checkpoint: all 218 declarative suites and 53 retained Bash
  checkers passed.
- Plan structure, logical/path policy-impact equality, and `git diff --check`
  passed.

## Next Boundary

Implement packet staleness and decision reuse from exact narrower dependency
fingerprints. Reading plans remain derived navigation and must not become a
second authority for routing, policy impact, or review semantics.
