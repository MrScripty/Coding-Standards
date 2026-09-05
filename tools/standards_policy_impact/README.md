# Standards Policy Impact

`tools/standards_policy_impact/` owns the typed policy-impact relationship
compiler. Source-owner declarations are the sole relationship authority. One
compile produces neutral graph topology and typed policy semantics without
moving policy behavior or coverage-certificate authority into the generic
graph engine. Expressions compile once through the standard-library-only
`standards_applicability` Module, and each semantics row stores the resulting
immutable program rather than a dictionary for callers to reparse.

`contracts/policy-impact-authoring-v2.toml` is the single internal serialized
contract for supplemental artifact kinds, relationship kinds, graph groups,
propagation, traversal, evidence requirements, and exact target compatibility.
The canonical metadata corpus remains the authority for modules and policy
units; the registered node catalog owns supplemental artifact declarations;
source-owned schema-version-2 files own relationship membership. The compiler
rejects predecessor schemas and mixed catalog-edge authority without a
compatibility loader.

Compiled edge IDs use injective percent-encoded natural-key segments.
Policy-aware callers inspect the typed semantics index; generic graph callers
continue to see only neutral topology and compiler provenance. Downstream
Modules consume `CompiledPolicyImpactSet` and do not reload the node catalog or
reclassify relation targets.

Consumer coverage is not compiled relationship semantics. The downstream
`standards_analysis` Module derives coverage views, requirements, attestations,
and certificates from this compiled set plus a registered audit horizon.
That horizon bounds declared review inputs; it cannot discover missing consumers.

An evidence owner is either a registered `suite:<id>` or `review:consumer`.
Consumer review binds the exact policy, relationship, and consumer content without
adding a suite dependency. It requires an actual review before certification.
The compiler still accepts the earlier suite-only contract for historical reads.

Run focused tests with:

```bash
python3 -m unittest discover -s tools/standards_policy_impact/tests
```
