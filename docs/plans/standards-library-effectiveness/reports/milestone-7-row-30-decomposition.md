# Milestone 7 Row 30 Contract Artifact Decomposition

## Owner Contract

`topics/contracts.md` is the sole normative owner for deciding whether a
contract artifact is justified, where its authority is accessible, and which
producer semantics a consumer must preserve. Architecture may route to this
policy but does not independently define contract placement, cost, or semantic
preservation.

No dedicated package, mirrored DTO, wrapper, schema, default, ordering rule,
description, or compatibility behavior is universal. Each requirement follows
from recorded authority, consumers, invariants, representation, persistence,
deployment, and evolution facts.

## Exact Ownership

- `STD-0055` and `STD-0056` refine useful artifact-placement and necessity
  policy into Contracts; `STD-0057` becomes an index because benefit claims are
  not independent authority.
- `STD-0058` becomes an index route; `STD-0059` through `STD-0061` refine
  producer-consumer semantic preservation into Contracts; `STD-0062` becomes
  an index because benefit claims are not independent authority.

Each identifier receives exactly one disposition. No example or benefit list
becomes normative or a compatibility promise.

## Ordered Children

1. `30.1`: migrate `STD-0055` through `STD-0057` artifact necessity and
   authority-access placement, remove the dedicated-package default, and add
   focused artifact-selection evidence.
2. `30.2`: migrate `STD-0058` through `STD-0062` producer-consumer semantic
   preservation, reject inferred or silently dropped semantics, replace the
   duplicate Architecture sections with a concise index, and close row 30.

The decomposition, owner-validation table, checker, Contracts sections, legacy
sections, exact dispositions, focused fixtures/checkers, plan, ledger, and
affected cursor assertions are the only allowed write set.

## Typed Outcomes And No Fallback

Return `unavailable` when required authority, consumer, invariant, or evolution
facts cannot be obtained; `invalid` when an artifact or transformation
contradicts the selected contract; and `unsupported` when a well-formed variant
is outside the supported contract.

Do not create a mirror merely to satisfy a pattern, hide shared authority in an
unrelated implementation, infer semantics from field names, preserve every
description or ordering rule by default, silently drop selected semantics, or
substitute a guessed default or compatibility path.

## Re-plan Triggers

Stop if a child requires Architecture to own contract policy, a universal
package layout, multiple dispositions for one identifier, preservation of
examples as authority, implicit compatibility, a third semantic child, or files
outside the approved write set.
