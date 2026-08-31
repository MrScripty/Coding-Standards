# M6-I74 Baseline Markdown Heading Admission

## Decision

Admit one `shared-contract` package at train order 189 to replace
`evaluation/standards-effectiveness/verify-undisposed-source-gaps.sh` with a
bounded native `baseline_markdown_headings` assertion in the existing
`source-index-closures` suite.

Fresh post-M6-I73 evidence contains only two caller-free verifiers. Decision
traceability remains an external-template integration boundary. The 114-line
source-gap audit is the smaller candidate and has no executable dependency,
but its safety contract cannot be represented by the current empty expected
table alone.

## Preserved Contract

The package preserves:

- the summary-owned immutable baseline commit and its exact availability as a
  Git commit;
- the fixed repository-wide Markdown diff, limited to removed ATX headings;
- exact old-path and old-line resolution through the generated section
  inventory;
- exclusion of every identifier already present in canonical dispositions;
- exact equality between observed undisposed identities and the expected-gap
  table, including empty-table detection of a newly introduced gap;
- strict `retained-diff`, `deferred-row38`, and `deferred-row47`
  classifications with nonempty reasons and current heading-state checks; and
- the eight historical independent-gate records already pointing at the
  aggregate source-gap authority.

## Shared Assertion Boundary

The assertion accepts only four contained evidence paths and one explicit map
from classification names to `present` or `absent`. Git invocation, baseline
key, Markdown pathspec, diff flags, ATX syntax, table headers, and identifier
shape remain engine-owned and non-configurable. Repository Git execution uses
the existing bounded, sanitized adapter. Missing Git or baseline objects,
malformed evidence, invalid UTF-8, and output-limit failures retain typed
outcomes.

The check adds no arbitrary command, configurable revision or pathspec, shell
bridge, policy callback, copied source list, alternate baseline, compatibility
schema, inferred classification, waiver, or fallback. One safety-critical
migration invariant justifies the bounded primitive under the current plan.

## Acceptance Evidence

Acceptance requires direct parser and Git-fixture tests; positive parity with
the retained checker; mutations for unrecorded removal, missing expected
identity, current-state contradiction, malformed evidence, and unavailable
Git authority; exact historical-edge transfer; whole-checker numeric
retirement; final dependency-local coverage compilation; generated freshness;
all Verifier and graph-engine tests; all registered suites; the complete mixed
checkpoint; plan validation; source preservation; removed-path proof; and
staged write-set review.

The final exact write set and dependency-local attestation renewal are frozen
after governed admission inputs are included in the final-state compilation
and before acceptance.
