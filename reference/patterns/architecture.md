# Architecture Pattern Reference

**Standards metadata**

- ID: `reference.patterns.architecture`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A canonical Architecture decision is complete and an illustrative structural pattern may help communicate or implement it.
- Does not apply when: Responsibility, authority, dependency, lifecycle, contract, capability, or acceptance decisions are unresolved.
- Requires: `topic.architecture`
- Specializes: `none`
- Verification: Reference-owner metadata, non-authority decisions, canonical links, and accepted legacy-extraction dispositions.
- Canonical owner: `reference/patterns/architecture.md`

This material is non-normative. Select responsibilities, boundaries,
dependencies, state authority, runtime composition, and typed outcomes through
[Architecture](../../topics/architecture.md) before adapting an example.
Pattern presence does not establish applicability.

## Adaptation Boundary

An illustrative pattern can communicate an already selected design. It cannot
select a layer count, package role, dependency direction, state owner,
lifecycle, transport, persistence strategy, synchronization mechanism, or
evidence claim.

Before adapting an example, return to the applicable canonical owners when any
of these facts are missing or contradictory:

- the responsibility and authority assigned to each participant;
- the stable contracts toward which dependencies point;
- lifecycle, concurrency, persistence, security, and failure obligations;
- supported mechanisms and environment capabilities; and
- the observable claim and evidence required for acceptance.

## Reading A Pattern

A useful adaptation can record:

| Part | Purpose |
| --- | --- |
| Selected facts | Names the canonical decisions that make the pattern applicable |
| Illustrative shape | Shows one arrangement that preserves those decisions |
| Variation points | Identifies mechanisms the example does not select |
| Rejection conditions | Names facts that make the illustration invalid or unsupported |
| Evidence | Links the checks selected by the canonical owners |

The table is an explanatory aid, not a required artifact or fixed planning
format. Pattern families and examples are added only after their legacy
lineage and non-authority boundaries are accepted.

## Typed Outcomes

Canonical owners determine whether missing or contradictory facts are
`invalid`, `unsupported`, or `unavailable`. This reference does not replace
those outcomes with an incumbent pattern, nearest example, fixed diagram, or
smallest structural change.

## Conditional Layered Arrangement

After Architecture selects four independently meaningful responsibilities, one
possible arrangement is:

```text
presentation
    |
application coordination
    |
domain policy
    ^
infrastructure adapters
```

| Illustrative role | Possible responsibility |
| --- | --- |
| Presentation | Project selected state and translate interaction |
| Application coordination | Orchestrate an accepted use case |
| Domain policy | Own business rules that are independent of delivery mechanisms |
| Infrastructure adapters | Implement selected external-system contracts |

This shape does not require these names, four layers, horizontal organization,
or a domain module with no dependencies. A selected design may collapse,
split, reorder, or omit roles when its ownership, lifecycle, deployment, and
change facts differ.

Dependencies in an adaptation point toward the owner of each stable contract.
For example, presentation and infrastructure adapters can both depend on
application or domain contracts without depending on each other's concrete
implementation.

### Conditional Consequences

When the selected boundaries actually isolate independent decisions, this
arrangement can make business policy testable without delivery mechanisms and
can allow an adapter to change without changing that policy. Those outcomes
require affected dependency and behavior evidence; the diagram alone proves
neither separation nor maintainability.
