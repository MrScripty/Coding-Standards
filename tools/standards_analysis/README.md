# Standards Analysis

`tools/standards_analysis/` owns read-only standards snapshot comparison,
policy-unit change interpretation, impact selection, consumer coverage,
immutable analysis states, fact requirements, and resolution. It consumes
neutral applicability, metadata, policy-impact, and graph contracts and does
not depend on verifier checks or repository-writing behavior.

Current implemented foundation:

- canonical JSON and domain-separated identities;
- clean-Git and deterministic manifest snapshots;
- metadata-owned policy-unit corpus consumption;
- deterministic modification, addition, removal, move, split, and merge
  classification with exact accepted/proposed graph seeds;
- mandatory whole-artifact obligations for unmapped normative changes;
- three-valued accepted/proposed impact applicability with exact fact-resolution
  work and conservative whole-artifact scope for unknown candidates;
- consolidated consumer-review obligations keyed by exact consumer, scope, and
  review contract, with plural source/edge/trace provenance and fact-bound
  decision fingerprints;
- independent content-fingerprinted policy-consumer horizons;
- mandatory audit-coverage work for changed policies without current
  certificates, including policies with no declared consumers; and
- two-identity coverage requirements, attestations, and reusable certificates;
- one content-addressed `AnalysisState` containing exact authority references
  and dependency-valid accepted decisions;
- deterministic pending and complete projections with no independent packet or
  report lifecycle;
- evidence- and authorization-bound fact observations, stable obligation
  handles, narrow prior-analysis reuse, and state-derived next operations.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_analysis/tests
```
