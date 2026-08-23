# Milestone 3 Applicability And Policy-Impact Cutover

## Accepted Outcome

The repository now has one executable applicability authority and one
policy-impact relationship authority.

- `tools/standards_applicability/` is standard-library-only and compiles typed
  fact schemas, immutable programs, and immutable request fact sets.
- Router rules and policy-impact declarations store compiled programs. They do
  not retain dictionaries for downstream reparsing.
- Evaluation returns `true`, `false`, or `unknown` plus exact material
  unresolved facts.
- Empty fact schemas and fact-free `always` are valid.
- Program evaluation rejects fact sets from another schema identity.
- Source-owner policy-impact declarations compile the 39 accepted
  relationships into one generic graph contribution and one semantics index.
- Repository graph composition, Standards Engine inspection, analysis traces,
  and verifier validation consume that compiled set.
- The former graph-manifest relationship blocks, policy metadata strings,
  policy compiler parser, and `standards_analysis.applicability` were removed
  without aliases or fallback.

The canonical A1 JSON Schema remains serialized-shape authority. Runtime
conformance tests compare exact operator, fact-type, fact-state, truth, language
version, and empty-schema domains against it.

## Verification

- `standards_applicability`: 9 tests.
- `standards_policy_impact`: 6 tests.
- `standards_analysis`: 39 tests.
- `standards_engine`: 14 tests.
- `standards_verifier`: 379 tests.
- Canonical contract: 27 examples, 7 identity fixtures, 4 operation envelopes,
  and 100 definitions.
- Declarative verification: all 218 suites.
- Complete mixed checkpoint: all 218 suites and 53 retained Bash checkers.
- `policy-semantic-impact`: 2 focused checks.
- `git diff --check`: passed.

## Remaining Milestone Work

Impact traces retain compiled policy semantics, but Milestone 3 still must bind
analysis facts once, evaluate accepted and proposed programs, generate exact
consumer and unresolved-fact obligations, implement unmapped normative-change
obligations, and establish bounded audit certificates before an empty impact
can be accepted.
