# Standards Analysis

`tools/standards_analysis/` owns read-only standards snapshot comparison,
policy-unit change interpretation, impact selection, consumer coverage,
packets, questions, and resolution. It consumes neutral applicability,
metadata, policy-impact, and graph contracts and does not depend on verifier checks or
repository-writing behavior.

Current implemented foundation:

- canonical JSON and domain-separated identities;
- clean-Git and deterministic manifest snapshots;
- metadata-owned policy-unit corpus consumption;
- mandatory whole-artifact obligations for unmapped normative changes;
- three-valued accepted/proposed impact applicability with exact fact-resolution
  work and conservative whole-artifact scope for unknown candidates;
- independent content-fingerprinted policy-consumer horizons;
- mandatory audit-coverage work for changed policies without current
  certificates, including policies with no declared consumers; and
- two-identity coverage requirements, attestations, and reusable certificates.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_analysis/tests
```
