# Milestone 7 Row 37 Architecture Reference Closure Decomposition

## Owner Contract

Row 37 retains an independent owner review even though
`reference/patterns/architecture.md` now exists through row 36's completed
owner-scoped transition. Existing owner presence does not pre-approve any row
37 disposition or make the Architecture reference a general policy owner.

`topics/architecture.md` owns responsibility placement, runtime composition,
dependency direction, and state authority. `topics/resilience.md` owns replay,
resumption, duplicate handling, convergence, and partial-failure recovery.
`profiles/applications/frontend.md` owns frontend projection, presentation
state, synchronization, and interaction adaptation. Contracts, Persistence,
Concurrency, and Verification retain their existing specialized authority.

`reference/patterns/architecture.md` may retain only conditional structural
illustrations after canonical owners select the applicable facts.
`reference/recipes/frontend.md` remains the mechanism owner for already
selected frontend behavior; the legacy view-model class does not justify a new
recipe or canonical owner.

## Exact Ownership

- `STD-0069` through `STD-0073` split runtime-composition authority from one
  conditional composition-root illustration and qualified consequences.
- `STD-0074` through `STD-0079` split Architecture and Resilience authority
  from one conditional durable-workflow illustration. Fixed event sourcing,
  durable-event acceptance, projection, component, and benefit defaults are
  removed.
- `STD-0080` is duplicate Verification evidence and is replaced without
  copying its checklist into reference.
- `STD-0081` through `STD-0084` route to the Frontend profile. The fixed
  source-view-model-view chain, subscription rule, action forwarding rule, and
  backend-by-location authority do not survive.
- `STD-0085` is duplicate frontend synchronization mechanism material; the
  legacy mutable TypeScript class is removed rather than copied.
- `STD-0086` is duplicate claim-selected Verification policy.
- `STD-0087` is replaced by Architecture's fact-selected concern boundaries
  and explicit rejection of a universal directory tree.

Every identifier receives exactly one disposition. A split may link several
applicable canonical owners, but only the owner recorded in the validation
table owns the retained rule or reference outcome.

## Ordered Children

1. `37.1`: migrate `STD-0069` through `STD-0073`, retain one conditional
   composition-root illustration, and remove universal wiring, lifecycle,
   dependency-injection, and benefit defaults.
2. `37.2`: migrate `STD-0074` through `STD-0080`, retain one conditional
   durable-workflow illustration, and remove universal event-sourcing,
   persistence, component, replay, and evidence defaults.
3. `37.3`: migrate `STD-0081` through `STD-0086` to existing Frontend,
   Architecture, recipe, and Verification authority without retaining the
   legacy class example or fixed view-model rules.
4. `37.4`: replace `STD-0087`, close the remaining row 37 legacy span, and run
   the deferred P30 complete-suite integration gate.

## Reference Selection

The composition-root illustration remains useful because it communicates one
possible application-boundary arrangement after runtime-composition decisions
are complete. The durable-workflow illustration remains useful only as a
cross-owner structural map and cannot select event sourcing, durable commands,
projections, or replay.

The view-model class and directory tree are removed. Existing Frontend recipes
already illustrate selected synchronization mechanisms, and the directory
template conflicts with Architecture's rejection of organization by a
universal tree. Duplicating either would add maintenance cost and preserve an
incumbent default without unique explanatory value.

## Bounded Write Sets

Child `37.1` may touch the composition-root section of
`ARCHITECTURE-PATTERNS.md`, `reference/patterns/architecture.md`, one focused
fixture and verifier, five exact dispositions, this row checker, plan, and
ledger.

Child `37.2` may touch the realtime-workflow section of
`ARCHITECTURE-PATTERNS.md`, `reference/patterns/architecture.md`, one focused
fixture and verifier, seven exact dispositions, this row checker, plan, and
ledger. Canonical owner files remain read-only unless focused decisions prove
a policy gap, which triggers re-planning.

Child `37.3` may touch the view-model section of
`ARCHITECTURE-PATTERNS.md`, one focused fixture and verifier, six exact
dispositions, this row checker, plan, and ledger. Existing Frontend and recipe
owners remain read-only because the selected outcome is routing and duplicate
closure, not new policy or example creation.

Child `37.4` may touch the directory-template section of
`ARCHITECTURE-PATTERNS.md`, one focused source-closure fixture and verifier,
the exact `STD-0087` disposition, this row checker, plan, and ledger. It runs
the P30 complete suite only after every row 36 and row 37 disposition is
present.

Shared dispositions, row checker, plan, ledger, legacy source, and reference
owner remain serial integration-owner work. No child may edit generated maps,
the immutable train, accelerated package manifest, router, lockfile, template,
configuration, or downstream repository.

## Verification Gates

Each implementation child requires focused positive and negative decisions,
exact disposition proof, prohibited-default checks, preservation of unrelated
legacy sections, row checker success, execution-train advancement, plan
structure, shell syntax, and diff integrity.

P30 closes only in child `37.4`, after which the complete fail-fast standards
suite must pass. Planning acceptance alone does not claim semantic or package
completion.

## Typed Outcomes And No Fallback

Missing or contradictory responsibility, composition, authority, persistence,
replay, projection, lifecycle, synchronization, or evidence facts retain the
typed outcome selected by their canonical owner. Do not choose a composition
root, event-sourced workflow, view-model class, backend owner, directory tree,
or incumbent example as fallback.

Legacy wording is removed or replaced when its child is accepted. It cannot
remain as a compatibility copy, advisory default, or alternate authority.

## Re-plan Triggers

Stop if focused decisions prove a missing canonical policy, require a new
owner, require retaining the view-model class or directory tree, make a
reference normative, change an exact disposition, require more than four
semantic children, require files outside a child's bounded write set, change
P30 membership, edit generated or immutable artifacts, or prevent the complete
suite from proving package closure.
