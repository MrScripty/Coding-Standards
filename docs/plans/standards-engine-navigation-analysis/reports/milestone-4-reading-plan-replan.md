# Milestone 4 Reading-Plan Replan

## Trigger

Milestone 3 now generates authoritative consumer-review obligations, but the
existing reading-plan projection still accepts one permissive reason. Router
selection also overwrites earlier direct causes and chooses one dependency
parent. Continuing with that representation would either copy policy-impact
semantics into navigation or discard valid provenance.

Reading-plan work is therefore admitted only as a coordinated replacement of
the projection contract and every current producer and consumer.

## Authority Model

A reading plan is a derived navigation view. It may consume:

- authoritative consumer-review obligation handles;
- Router base and rule selections; and
- canonical `Requires` and `Specializes` dependency edges.

It must not traverse policy-impact relationships or copy their policy units,
traces, applicability evidence, evidence owners, or review contracts. Those
facts remain owned by the referenced obligation and are available through
`inspect`.

Each registered non-module target declares one canonical authority
classification in the policy-impact node catalog. Module authority derives
from canonical module metadata, and policy-unit authority derives from its
owning module. Reasons never determine authority.

## Typed Causes

The public `ReadingPlanEntry` contains a nonempty, sorted, unique `reasons`
collection. Version 1 admits these exact cause variants:

- `consumer-review-obligation`: one obligation handle;
- `routing-base`: the Router projection ID;
- `routing-rule`: the rule ID and every referenced canonical fact ID;
- `requires`: the exact edge ID and selecting source; and
- `specializes`: the exact edge ID and selecting source.

The former fake `routing-fact: routing.request` representation is removed.
Display summaries are not cause authority.

## Compilation

One deep reading-plan compiler accepts typed selections and an authority
resolver. It:

1. canonicalizes exact target and scope identities;
2. groups by exact `(target, scope)`;
3. rejects conflicting target authority;
4. unions and canonicalizes all causes;
5. derives `selected` when any cause is selected, otherwise `unresolved`
   when any cause is unresolved, otherwise `conditional`; and
6. orders entries by reading class, dependency order, canonical target, and
   canonical scope.

Whole-artifact and structured scopes remain distinct. No overlap or
containment merge is admitted.

Router compilation retains the base cause, every applicable rule cause, every
unresolved rule cause, and every canonical dependency edge whose source and
target participate in the selected closure. A direct-plus-dependency target
retains both causes. Consumer compilation creates one selection for each
consumer-review obligation and never inspects its internal policy-impact
reasons.

## Version Cutover

Reading-plan compilation semantics are part of the analysis contract, so that
contract advances from 1 to 2. The replacement is atomic:

| Contract | Old | New |
| --- | ---: | ---: |
| Public interface | 4 | 5 |
| Navigation handle, schema, identity domain | 1 | 2 |
| Packet handle, schema, identity domain | 2 | 3 |
| Completed report handle, schema, identity domain | 1 | 2 |
| Analysis contract | 1 | 2 |

Old identities are not interpreted under the new representation.

## Verification

Acceptance requires:

- one obligation produces one consumer reading entry;
- two compatible obligations produce one entry with two references;
- duplicate references collapse;
- input reordering preserves identity;
- adding or removing a cause changes identity;
- direct plus dependency selection retains both causes;
- multiple dependency parents retain every edge;
- routing rules retain all referenced facts;
- selected plus unresolved derives selected while retaining both causes;
- distinct scopes remain distinct;
- missing or conflicting authority is rejected;
- reading-plan consumer compilation does not accept policy-impact traces; and
- schema, runtime, examples, identity fixtures, package tests, affected
  declarative suites, and repository checks agree at one exact tree.
