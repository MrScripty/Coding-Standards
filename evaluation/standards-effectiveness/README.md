# Standards Effectiveness Evaluation

This directory contains the frozen baseline, evaluation fixtures, and live
Standards Engine configuration. The
[active restructure plan](../../docs/plans/standards-library-effectiveness/plan.md)
owns current work; its [ledger](../../docs/plans/standards-library-effectiveness/execution-ledger.md)
and [issues](../../docs/plans/standards-library-effectiveness/issues.md) retain execution history.

## Run Verification

Use the locked Python environment and commands in the
[Verifier README](../../tools/standards_verifier/README.md). The complete
checkpoint runs all registered suites. The
[verification guide](verification-guide.md) describes their fixtures and evidence.

## Baseline And Scoring

- [Baseline report](baseline-report.md) and [baseline scores](baseline-scores.md)
- [Evaluation scenarios](fixtures/scenarios.md)
- [Scoring rubric](verification-guide.md#scoring)

The baseline is frozen at commit `6b4df85f042898374e9d23d265f4ecd25b0a7ba7`.
`corpus.tsv`, frozen generated metrics, and `snapshots/` retain historical
observations. Current prompts are versioned in the root `prompts/` directory;
`snapshots/prompts/` contains historical copies only.

## Live Configuration

The canonical module corpus, router projection, suite registry, policy-unit
registry, policy-impact declarations, coverage records, and generated suite
inputs are active engine inputs. They remain here even though the directory
also contains historical evaluation material.

- [Module metadata schema](../../tools/standards_metadata/metadata-schema.md)
- [Library information architecture decision](../../docs/decisions/standards-library-information-architecture.md)
- [Policy-impact ownership](../../tools/standards_policy_impact/README.md)

## History

Milestone reports live beside the
[active plan](../../docs/plans/standards-library-effectiveness/plan.md).
Completed plan bundles and their acceptance evidence are indexed in the
[archive](../../docs/archive/README.md). Retained migration tables in this
directory remain inputs to registered suites; archival location alone does
not make an artifact disposable.
