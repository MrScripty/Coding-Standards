# Standards Policy Impact

`tools/standards_policy_impact/` owns the typed policy-impact relationship
compiler. Source-owner declarations are the sole relationship authority. One
compile produces neutral graph topology and typed policy semantics without
moving node, group, traversal, applicability evaluation, or coverage-certificate
authority into the generic graph engine. Expressions compile once through the
standard-library-only `standards_applicability` Module, and each semantics row
stores the resulting immutable program rather than a dictionary for callers to
reparse.

Relationship-kind contract version 1 is a module-owned code table rather than
a second configurable manifest. All eight admitted kinds compile into the
existing `policy-impact` and `semantic` groups, propagate from source to
consumer, and require an explicitly authored evidence owner. Compiled edge IDs
use injective percent-encoded natural-key segments. Policy-aware callers inspect
the typed semantics index; generic graph callers continue to see only neutral
topology and compiler provenance.

Consumer coverage is not compiled relationship semantics. The downstream
`standards_analysis` Module derives coverage views, requirements, attestations,
and certificates from this compiled set plus an independent registered audit
horizon.

Run focused tests with:

```bash
python3 -m unittest discover -s tools/standards_policy_impact/tests
```
