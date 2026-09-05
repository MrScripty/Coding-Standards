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
- content-fingerprinted horizons for explicitly registered policy consumers;
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

## Repository coverage evidence

Repository attestation schema 6 stores each `evidence` and `explicit_exclusions`
entry as an exact evidence reference: `id`, `digest`, `provider_contract`, and
`provider_contract_version`. The supported repository provider is
`repository-content`, version `1`; its ID is the repository evidence path.
Loading a current claim verifies both evidence and exclusion bytes against the
stored SHA-256 digests before accepting the authorization.

Schema 5 remains readable for existing and historical certificates. Its entries
are paths and have no retained review-time digest. Do not mechanically convert
them to schema 6: hashing current files cannot establish which bytes a past
review examined. New certificate publication must retain the references from
the actual authorized review. Both formats still require the exact current
coverage requirement and the configured repository auditor.

Attestation registry schema 3 adds `engine_sources`, an explicit list of
repository-trusted Engine audit receipt files. Each receipt preserves the
Engine authority contract, authorization record and proof bytes, reviewed
claim, and originating Analysis ID. Registry membership admits that Engine
authority; the loader checks the authorization identity and pinned repository
evidence rather than substituting the historical repository auditor. The
existing `revoked_grants` list also rejects revoked Engine authorization IDs.
Stale requirements are ignored, and duplicate current claims are rejected.
Receipt readback requires no Engine database. Legacy `sources` retain their
original auditor and formats; the publication path does not relabel them.

Receipts also retain a publication authorization whose subject binds the whole
claim, original review authorization, Analysis ID, and policy subject. Replaying
it detects claim changes even when all referenced files still match their
digests. Either retained authorization ID can be revoked.

The horizon is a declared review scope. It cannot establish that undeclared
consumers do not exist. A `review:consumer` relationship binds its direct consumer
without importing a suite's unrelated inputs; suite evidence adds the selected
suite closure. Neither relationship ownership nor a passing graph check supplies
an audit decision. The current repository has no stored certificates following
the September 2026 retirement; review-required is the expected state.
