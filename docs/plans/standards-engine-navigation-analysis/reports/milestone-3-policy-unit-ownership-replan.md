# Milestone 3 Policy-Unit Ownership Replan

## Trigger

The policy-impact compiler must validate policy-unit relationship sources. The
neutral policy-unit loader currently resides in `standards_analysis`, while
analysis already depends on `standards_policy_impact`. Reusing that loader would
create a dependency cycle; copying it would create a second parser and
authority projection.

## Decision

Policy-unit sidecars continue to own identities, locators, aliases, lifecycle,
and semantic revisions. `standards_metadata` loads, validates, resolves, and
projects those facts with canonical module metadata as one immutable standards
corpus. It also remains the sole producer of policy-unit representation and
structural digests.

`standards_analysis` retains semantic proposals, accepted/proposed comparison,
change classification, graph seeds, impact selection, obligations, coverage,
packets, and reports. It imports immutable policy-unit views from
`standards_metadata` and does not parse sidecars or resolve locators.

`PolicyUnitGraphSource` contains no analysis behavior and moves to
`standards_graph`. Metadata remains independent from graph storage.

```text
standards_metadata
  -> canonical modules and policy-unit corpus

standards_policy_impact
  -> standards_metadata + standards_applicability + graph_engine

standards_graph
  -> standards_metadata + standards_policy_impact + graph_engine

standards_analysis
  -> standards_metadata + standards_policy_impact + graph_engine
```

The Standards Engine composition root loads one immutable accepted or proposed
standards corpus per snapshot and passes that same object to policy-impact
compilation, graph composition, navigation, classification, and adapters.
Module-only metadata callers may continue to load only the module corpus and do
not compile policy impact.

## Cutover

The coherent replacement:

1. moves policy-unit models, sidecar loading, locator and lifecycle validation,
   digest production, and focused tests to `standards_metadata`;
2. adds `load_canonical_standards_corpus` without changing sidecar authority;
3. moves policy-unit graph projection to `standards_graph`;
4. makes policy impact consume the immutable standards corpus;
5. changes analysis and the Standards Engine to consume the upstream views;
6. deletes `standards_analysis.policy_units` and its re-exports; and
7. retains no old loader, wrapper, fallback, or second parser.

Callers translate neutral `MetadataError` failures at their own boundaries.
No source document, policy meaning, locator, semantic revision, or generic
graph contract changes in this ownership move.
