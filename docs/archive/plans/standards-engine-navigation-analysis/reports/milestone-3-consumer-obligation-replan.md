# Milestone 3 Consumer-Obligation Recovery Replan

## Trigger

Milestone 3 was marked accepted without implementing one explicit acceptance
requirement: definitely applicable impact candidates never became
`consumer-review` obligations. Coverage, applicability-resolution, and
unmapped-normative generators existed, but no consumer aggregation existed.

The accepted source-remapping design also requires several policy units and
edges selecting one compatible consumer review. The v1 obligation contract's
singular `source` and `reason` cannot represent that provenance. Milestone 4
reading plans must pause because they consume obligations and must not infer
affected consumers independently.

## Binding Replacement

One `ConsumerSelection` aggregate groups definitely applicable policy-impact
traces by this exact normalized key:

```text
canonical consumer ID
+ canonical review scope
+ review-contract identity
```

Scope compatibility is canonical equality only. The review contract fixes
permitted dispositions, evidence semantics, authorization semantics, and review
meaning. A future incompatible contract creates a separate obligation rather
than a conditional merge.

Each aggregate contains a sorted, unique reason set. Every reason identifies:

- selecting policy-unit ID;
- edge ID and relationship kind;
- accepted and/or proposed content-addressed trace identities;
- each applicable graph side;
- evidence owner; and
- applicability result.

The source set and evidence-owner set derive from reasons. Neither is separately
authored or stored as competing authority. Full trace details remain available
from analysis inspection; ordinary projections retain concise trace handles and
sides.

## Identity And Applicability

The aggregate is the sole input for both displayed reasons and the decision
fingerprint. The fingerprint binds every selecting changed policy state,
relationship semantic dependency, trace set, exact scope, review contract,
referenced fact value, and evidence owner. Input ordering cannot change it;
adding or removing a selector, fact value, scope, or contract must.

Applicability remains three-valued per trace:

- `true` contributes to consumer review;
- `false` contributes no review;
- `unknown` contributes applicability-resolution work;
- generic dependency traces never contribute consumer review.

A true and unknown relationship reaching the same consumer produce one
definite review plus unresolved applicability work. If the unknown later becomes
true, packet regeneration adds its reason and changes the review obligation's
fingerprint and identity.

## Versioned Cutover

The replacement is atomic:

- plural typed `reasons` replace singular obligation `source` and `reason`;
- `coding-standards:obligation:v2` replaces the v1 identity domain;
- packet schema and packet identity domain advance to version 2;
- the public A1 interface advances to version 4;
- Python types, generators, schema, examples, identity fixtures, packet
  projections, and tests change together; and
- no compatibility interpretation accepts v1 obligation or packet identities
  under the new contract.

Reading-plan implementation remains paused until this cutover is accepted.

## Required Evidence

- One relationship produces one review.
- Compatible policy units and edges consolidate into one review.
- Different exact scopes or review contracts remain separate.
- Accepted-only removal and proposed-only addition relationships remain visible.
- True plus unknown preserves both definite and unresolved work.
- Trace deduplication and ordering are deterministic.
- Reordered input preserves identity.
- Selector, fact, scope, and contract changes alter identity.
- Schema/runtime examples and identity fixtures agree under the new versions.
- Reading-plan tests later prove consumers originate exclusively from
  obligations.
