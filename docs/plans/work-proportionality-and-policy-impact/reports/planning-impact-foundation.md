# Planning Semantic-Impact Foundation

## Accepted Boundary

The permanent current-state authority is
`evaluation/standards-effectiveness/policy-semantic-impact.toml`. This report
records Milestone 1 review evidence only; it does not replace or extend that
manifest.

Initial coverage is deliberately bounded to `workflow.planning`. The owner
resolves to `workflows/planning.md` through canonical metadata. No global
completeness is claimed, and an owner absent from the manifest returns
`POLICY_IMPACT.OWNER_NOT_AUDITED` as typed `unavailable`.

Each reviewed edge contains:

- one canonical policy-owner ID;
- one contained consumer artifact;
- one supported semantic relation;
- one non-empty applicability condition; and
- one registered evidence-owner suite.

The accepted relation types are normative consumer, Router projection, prompt
projection, template projection, fixture projection, and enforcement-suite
projection. Consumer shape is checked against the relation. Markdown links,
lexical similarity, standards `Requires`, and the temporary Bash checker graph
confer no semantic edge.

Registered suite ownership supplies one bounded completeness invariant: every
suite whose explicit `owner` is an audited policy owner must have a matching
enforcement-suite edge. Other relations remain explicit review decisions and
are not inferred from content or links.

## Reverse-Impact Review

The deterministic command:

```bash
python3 tools/standards_verifier/query_policy_impact.py \
  --owner workflow.planning
```

returns these reviewed consumers, sorted by artifact path:

- `STANDARDS-ROUTER.md`
- `evaluation/standards-effectiveness/fixtures/implementation/plan-entrypoint-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/admission-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/concurrent-integration-applicability.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/concurrent-integration-outcomes.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/consolidation-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/full-review-prompt-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/template-projection-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/planning/work-slice-proportionality.tsv`
- `evaluation/standards-effectiveness/suites/concurrent-plan-integration.toml`
- `evaluation/standards-effectiveness/suites/full-review-prompt-entrypoint.toml`
- `evaluation/standards-effectiveness/suites/plan-implementation-entrypoint.toml`
- `evaluation/standards-effectiveness/suites/plan-template-projection.toml`
- `evaluation/standards-effectiveness/suites/planning-admission.toml`
- `evaluation/standards-effectiveness/suites/planning-consolidation.toml`
- `evaluation/standards-effectiveness/suites/policy-semantic-impact.toml`
- `evaluation/standards-effectiveness/suites/s1-routing.toml`
- `profiles/workflows/concurrent-plan-integration.md`
- `prompts/full-codebase-standards-refactor.md`
- `prompts/implement-plan.md`
- `prompts/planning.md`
- `templates/PLAN-TEMPLATE.md`
- `workflows/commit.md`
- `workflows/implementation.md`

Milestone 2 must assign one exact recovery disposition to every artifact in
this query result. New semantic consumers introduced while changing Planning
must be added to the manifest and disposition review in the same accepting
slice.

## Negative Contract

Declarative fixtures reject:

- duplicate owner/consumer/relation edges;
- an edge whose owner has no audited coverage;
- a consumer that does not resolve for its declared relation;
- empty applicability;
- unsupported relation types;
- repository path escape; and
- unavailable files; and
- an audited owner with a registered suite missing its enforcement-suite edge.

Direct unit tests additionally cover canonical owner mismatch, unknown
evidence-owner suites, deterministic ordering, unaudited-owner queries, and
TSV command output.

## Acceptance Evidence

- focused `policy-semantic-impact`: passed two checks;
- reverse query: returned every required Planning consumer;
- Python unit tests: passed;
- registered declarative suites: passed;
- generated checker inventory, graph, and numeric-retirement evidence: current
  and unchanged;
- affected plan structure and Markdown links: passed;
- complete mixed checkpoint: passed every registered declarative suite and
  every retained Bash checker; and
- temporary checker graph schema and artifacts: unchanged.
