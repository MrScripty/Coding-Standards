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

## Conditional Monorepo Role Catalog

After Architecture selects independently meaningful package boundaries, one
repository might describe them with roles such as:

| Illustrative role | Possible responsibility |
| --- | --- |
| Application entrypoint | Compose selected implementations and own process startup |
| Contract artifact | Represent a boundary consumed independently by its participants |
| Policy module | Own business or application decisions independent of delivery |
| Adapter | Implement a selected transport, storage, or platform contract |
| Development tooling | Support build and repository workflows outside product runtime |

These are descriptive labels, not required package kinds. One coherent package
may contain several roles, and one responsibility may span packages when its
deployment, lifecycle, generation, or consumer contracts require that split.
Names and directory locations do not establish ownership.

An illustrative dependency shape is:

```text
application entrypoint --> selected policy and contracts
adapter ----------------> contract it implements
independent consumer ---> shared contract artifact, when one is required
```

The arrows follow selected stable contracts. They do not require every
application to depend on a domain package, every adapter to use a dedicated
contracts package, or development tooling to have no declared runtime
relationship.

### Conditional Schema-Sharing Example

When a web client and server independently consume the same request or response
representation, [Contracts](../../topics/contracts.md) may select one shared or
generated artifact that both can access. Coordinated components with no
independent consumer or boundary may instead keep the representation with its
owner. Similar type shapes alone do not authorize importing an implementation
module or creating a shared package.

### Conditional Consequences

When package boundaries match real ownership and contracts, import evidence can
make misplaced responsibility and unintended coupling easier to detect.
Refactor safety and reuse remain claims to prove for the affected consumers;
the role catalog does not guarantee them.

## Conditional Server-Authoritative Projection

After Architecture selects a server-side component as the owner of particular
application state and the Frontend profile selects its projection contract, one
possible shape is:

```text
selected server owner -- event, response, or query --> frontend projection
selected server owner <-- declared action ----------- frontend interaction
```

The server location does not create authority. Another contract may select a
frontend, local process, device, peer, or external service as owner. Each
authoritative datum and transition still has one selected owner.

| Illustrative state | Possible owner |
| --- | --- |
| Accepted application state | Selected server component |
| Presentation state | Frontend projection owner |
| Unsubmitted input | Frontend interaction owner |
| Derived display value | Frontend projection, linked to its canonical source |

These examples do not classify all business, selection, configuration,
persistent, or transient state. The domain and interaction contracts decide
whether a value is authoritative, pending input, a projection, or purely
presentational.

### Conditional Flow

The selected source and consumer contracts may use events, subscriptions,
responses, or queries. A frontend can issue a declared action and apply the
next authoritative projection when that contract produces it. Push, pull,
read-only display, and a six-step request cycle are not defaults.

Confirmed projection is useful when the UI contract requires authoritative
acceptance before displaying the result. Optimistic projection is also valid
when the selected contract defines pending state, reconciliation, rejection,
ordering, stale-result handling, and user-visible failure semantics. If those
facts are missing, return the canonical typed diagnostic instead of silently
switching projection modes.

### Conditional Consequences

One selected owner plus a proved synchronization contract can prevent a
projection from becoming competing authority. Consistency, reliability, and
simplicity remain observable claims; a server location, confirmed-only update,
or single-source diagram does not prove them.

## Conditional Composition Root

After Architecture selects independently meaningful implementations, the
stable contracts they satisfy, and a boundary that owns configuration and
lifecycle, one possible arrangement is:

```text
selected composition boundary
    |-- construct selected adapters and resources
    |-- connect them through selected contracts
    `-- hand control to the owned runtime entrypoint
```

| Illustrative participant | Possible responsibility |
| --- | --- |
| Composition boundary | Select supported implementations and provide configuration |
| Contract consumer | Receive an implementation without selecting its mechanism |
| Adapter or resource | Implement one selected external or lifecycle contract |
| Runtime entrypoint | Begin work under the selected lifecycle owner |

These labels do not require one composition module, facade type, dependency
injection framework, application-wide root, or separate implementation package.
A coherent component may construct a local dependency when its ownership and
lifecycle do not cross the selected boundary. Several independently deployed
or owned runtimes may require separate composition boundaries.

### Conditional Consequences

Explicit composition can make implementation selection and lifecycle evidence
easier to inspect when the selected contracts actually isolate those decisions.
Replaceability, testability, cleanup, and boundary discipline remain claims to
prove for affected consumers. The diagram, alternate test implementation, or
presence of an application entrypoint proves none of them.

## Conditional Durable Workflow Map

After canonical owners select a workflow whose accepted state or recovery
crosses a durable boundary, one possible structural map is:

```text
selected boundary adapter
    --> selected operation and state-transition owner
        --> selected durable adapter, when durability is required
        --> selected projections or consumers

selected recovery owner
    --> declared authoritative history or checkpoint
        --> proved reconciliation and resumption boundary
```

The operation contract selects identity, preconditions, transitions, and
outcomes. Persistence selects whether and how acceptance crosses a durable
boundary. Resilience selects replay, duplicate, convergence, and partial-failure
behavior. Concurrency selects required atomicity and ordering. Architecture
selects authority and participant placement, and Verification selects evidence.

This map does not require commands, events, event sourcing, a read model,
publisher, durable store, bootstrap at startup, or one component per box. A
transient operation or a workflow with no replay contract can omit the durable
and recovery paths. Missing facts return the canonical typed diagnostic rather
than selecting the illustrated mechanism or continuing from in-memory state.

### Conditional Consequences

Explicit durable and recovery boundaries can make accepted state, duplicate
handling, and resumption evidence easier to inspect when the selected contracts
actually require them. Recovery, idempotency, separation, auditability, and
projection consistency remain claims to prove through affected real boundaries;
the map or a final snapshot proves none of them.

## Conditional Process Instance Coordination

After Contracts defines the identity of one current instance, Architecture
assigns its lifecycle owner, Concurrency selects the exclusion invariant, and
Cross-Platform and Resilience establish supported observation and recovery
behavior, one possible arrangement is:

```text
candidate participant
    --> selected instance identity
        --> selected coordination boundary
            |-- acquired  --> run under the selected lifecycle owner
            |-- occupied  --> return the declared already-active outcome
            `-- unresolved --> return the canonical typed diagnostic
```

The coordination boundary may use an operating-system facility, supervisor,
endpoint, lock, file-backed mechanism, or another capability whose guarantees
satisfy the selected invariant. The illustration does not select a PID file,
identity fields, process-start-time API, liveness test, cleanup action, or
diagnostic channel.

Evidence that appears stale is not deletion authority. Resilience and Contracts
must establish whether the state is disposable, what authoritative observation
supports recovery, who may perform it, and which result is visible. Diagnostics
selects reporting only when an accepted operator or consumer claim requires it.

If one-instance exclusion is not required, this pattern does not apply. Missing
identity, ownership, coordination, platform, recovery, or evidence facts return
the canonical typed outcome rather than selecting the nearest mechanism.

### Conditional Consequences

One selected identity and proved exclusion boundary can prevent overlapping
participants from claiming the same instance role. Crash recovery, portability,
race freedom, and operational visibility remain separate claims requiring
affected real-boundary evidence; the diagram or successful startup proves none
of them.

## Conditional Discover-Or-Create Convergence

After Architecture assigns service responsibility and lifecycle, Contracts
defines service identity and discovery outcomes, Concurrency selects any
creation exclusion, Resilience selects readiness and recovery behavior, and
Security selects applicable listener obligations, one possible map is:

```text
requesting participant
    --> selected discovery operation
        |-- usable selected instance --> consume its declared contract
        |-- creation authorized ------> coordinate selected creation
        `-- unresolved ---------------> return the canonical typed outcome

selected created instance
    --> satisfy the declared readiness contract
        --> become discoverable through the selected authority
```

Discovery may use a registry, supervisor, endpoint, process capability, injected
handle, or another selected authority. Creation may be external, independently
owned, or performed by an authorized participant. Neither discovery failure nor
an absent connection proves that creation is permitted.

The map does not require connection before creation, double checking, a lock,
backoff, health probing, or creator, last-client, or daemon ownership. Those
mechanisms are valid only when their contracts, lifecycle authority, target
capabilities, termination conditions, and evidence are established.

Missing service identity, discovery authority, exclusion, readiness, transport,
retry, lifecycle, or evidence facts retain the canonical typed outcome. Do not
create an incumbent service, connect to a nearby endpoint, or loop until success
as fallback.
