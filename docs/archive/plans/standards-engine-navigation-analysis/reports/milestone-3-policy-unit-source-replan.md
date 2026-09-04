# Milestone 3 Policy-Unit Source Replan

## Trigger

The accepted coverage model requires one stable semantic subject with an
accepted semantic revision. The current 39 policy-impact relationships use
`workflow.planning` or `workflow.commit` module IDs as their sources. Modules
own navigation, document identity, `Requires`, and `Specializes`; they do not
own semantic revisions. Only policy units own that lifecycle.

Adding module revisions would create a competing semantic lifecycle. Making a
revision optional would weaken coverage invalidation. Policy-impact sources
will therefore migrate to canonical policy units before coverage certificates
are implemented.

## Binding Model

```text
canonical module
    -> contains policy units
        -> own semantic revisions
        -> declare policy-impact relationships
            -> compile to generic graph edges and policy semantics
```

Declaration files remain module-owned. Their `owner` identifies the module
responsible for the source file; each relationship `source` identifies one
active policy unit contained by that module.

Module-level `related` navigation is a derived aggregation over contained
policy units. It creates no module-source relationship authority. Unmapped
normative module content must remain visible as incomplete policy-unit
coverage.

## Semantic Remapping

The 39 current relationships are an inventory baseline, not a target count.
Each receives one exact disposition in
[the source mapping](policy-impact-source-mapping.tsv):

- `mapped`: one legacy relationship maps to one coherent policy unit;
- `split`: one broad legacy relationship maps to several coherent policy
  units;
- `corrected`: the replacement changes an inaccurate semantic claim; or
- `retired`: reviewed evidence shows that no relationship remains applicable.

One policy unit may own several consumer relationships. One broad legacy
relationship may compile into several edges when it projected several
independently changeable policies. Acceptance proves reviewed semantic
coverage and exact dispositions, not edge-count equality.

Planning and Commit already provide non-overlapping level-two heading scopes
for the required baseline. No metadata-field locator or new heading is needed
for this cutover. The new units use those existing heading paths and bootstrap
`semantic_revision = 1` only after the identity, exact locator content, and
relationship mapping are reviewed together.

## Coverage Model

Coverage remains independent from change-specific dispositions:

1. Analysis derives a `CoverageAuditRequirement` from an exact authority view.
2. An authorized reviewer submits a `CoverageAttestation` for that requirement.
3. Analysis generates a reusable `ConsumerCoverageCertificate`.
4. Impact analysis generates change-specific consumer obligations.
5. `CompletedAnalysisReport` references the exact certificates and contains
   the sole authoritative change-specific dispositions.

Certificates bind the policy-unit identity, semantic revision, authority-view
and structural digests, relationship set, applicability contract, fact schema,
and registered audit horizon. They never bind a report or disposition set.

Accepted and proposed applicability contexts are snapshot-local. Equal schema
digests may share one immutable fact set; different schemas require separately
validated fact sets. Until that behavior is implemented, schema evolution must
return `FACT_SCHEMA_EVOLUTION_UNSUPPORTED` rather than silently impose schema
equality as permanent policy.

## Compiler Cutover Contract

The replacement compiler must reject a relationship source unless it:

- resolves to exactly one active policy unit;
- has an accepted semantic revision and exactly one resolved locator;
- belongs to the declaration file's owner module;
- exists as a canonical graph node; and
- is not a canonical module ID.

The cutover changes policy-unit declarations, relationship declarations,
compiler validation, graph composition, policy inspection, verifier adapters,
module-level navigation, and all affected tests together. Module-source support
is removed without fallback or compatibility loading.

When several changed units reach the same consumer with compatible consumer
scope and review kind, analysis emits one consumer-review obligation retaining
every selecting unit and graph trace. Different scopes or review kinds remain
separate obligations.

## Replan Triggers

Replan again if:

- an inventoried relationship cannot be assigned to coherent non-overlapping
  heading scopes;
- accepted meaning requires a locator form not currently supported;
- compiler cutover would require module-source fallback;
- policy-unit source aggregation requires generic graph-engine changes;
- the semantic mapping reveals an unaudited correction to canonical policy;
  or
- coverage identity cannot remain independent from change dispositions.
