# Standards Effectiveness Evaluation

This directory contains the reproducible baseline and neutral evaluation
fixtures for the standards-library effectiveness restructure.

## Baseline

The baseline is frozen at commit
`6b4df85f042898374e9d23d265f4ecd25b0a7ba7`, immediately after the
restructure plan was added and before normative standards changed.

`corpus.tsv` classifies every Markdown artifact by its current kind,
normative role, preliminary target role, preliminary disposition, and frozen
source.
`generate-baseline.sh` reads each artifact from the frozen commit and writes:

- `generated/file-metrics.tsv`: lines, headings, and strong imperative
  occurrences by file;
- `generated/section-inventory.tsv`: a stable identifier for every heading in
  normative or operationally derived guidance; and
- `generated/summary.tsv`: corpus totals used by the baseline report.

Run:

```bash
./evaluation/standards-effectiveness/generate-baseline.sh \
  /path/to/Coding-Standards
```

Generated metrics are factual inventory. `findings.md` owns semantic findings
such as duplication, conflicts, broad obligations, and ownership gaps.

The working tree contains ignored prompt files. Their contents are frozen under
`snapshots/prompts/` for baseline reproducibility only, with trailing whitespace
normalized. The snapshots are not canonical guidance; Milestone 1 must decide
whether prompts are versioned distribution artifacts or remain explicitly
local.

## Fixtures

`fixtures/scenarios.md` defines seven product-neutral tasks. Each scenario
declares expected routing, acceptance, exclusions, prohibited errors, and plan
artifacts. `baseline-scores.md` applies the fixed rubric to current guidance.

The same fixtures and rubric must be used after restructuring. A changed
fixture requires a recorded reason and before/after rescoring.

## Architecture Contract

- `information-architecture.md` owns roles, paths, routing, precedence, and
  migration decisions.
- `metadata-schema.md` defines canonical module metadata.
- `owner-map.tsv` and `owner-overrides.tsv` map the baseline corpus to proposed
  canonical owners.
- `generate-owner-map.sh` writes the complete 916-section owner proposal.
- `check-metadata.sh` and `verify-metadata-fixtures.sh` validate the metadata
  contract and its negative cases.

## Scoring

Each rubric dimension is scored:

- `0`: missing, contradictory, or requires an incorrect outcome;
- `1`: partially covered, ambiguous, duplicated, or disproportionate;
- `2`: clear, sufficient, proportionate, and owned.

Reducing document size cannot compensate for a lower correctness score.
