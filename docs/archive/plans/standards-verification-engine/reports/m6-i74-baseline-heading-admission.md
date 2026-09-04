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

## Exact Acceptance Write Set

- `docs/archive/plans/standards-verification-engine/execution-ledger.md`
- `docs/archive/plans/standards-verification-engine/issues.md`
- `docs/archive/plans/standards-verification-engine/plan.md`
- `docs/archive/plans/standards-verification-engine/reports/checker-inventory.md`
- `docs/archive/plans/standards-verification-engine/reports/m6-i74-baseline-heading-admission.md`
- `evaluation/standards-effectiveness/checker-migration-packages.tsv`
- `evaluation/standards-effectiveness/executable-edge-dispositions.tsv`
- `docs/plans/standards-library-effectiveness/execution-ledger.md`
- `evaluation/standards-effectiveness/generated/checker-dependency-components.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-edges.tsv`
- `evaluation/standards-effectiveness/generated/checker-dependency-nodes.tsv`
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml`
- `evaluation/standards-effectiveness/suites/checker-migration-packages.toml`
- `evaluation/standards-effectiveness/suites/source-index-closures.toml`
- `evaluation/standards-effectiveness/verify-undisposed-source-gaps.sh`
- `docs/plans/standards-library-effectiveness/plan.md`
- `tools/standards_verifier/README.md`
- `tools/standards_verifier/standards_verifier/checks/__init__.py`
- `tools/standards_verifier/standards_verifier/checks/baseline_markdown_headings.py`
- `tools/standards_verifier/tests/test_baseline_markdown_headings.py`

Final-state compilation renews exactly nine dependency-local requirements: one
Generated Contract, one Dependencies, five Planning, and two Verification
requirements. Every changed view differs only in its `horizon` members; the
other 42 requirements and all relationships, applicability programs,
structural digests, and representation digests remain unchanged.

## Acceptance

M6-I74 is accepted. Ten direct tests and five disposable repository mutations
cover exact pass behavior, unrecorded gaps, missing observations, contradictory
current state, malformed evidence, and unavailable baseline authority. All
eight historical edge records resolve to `source-index-closures`, the obsolete
checker is absent, and whole-checker numeric lifecycle passes.

All 51 current coverage requirements have exact certificates after the nine
admitted renewals. Verifier tests, graph-engine tests, all 228 registered
suites, generated freshness, plan validation, and the complete mixed checkpoint
pass. Final graph: 51 Bash checkers, 55 nodes, 377 edges, and 55 components.
