# Architecture Patterns

Reusable design patterns for multi-layer and client-server applications.

## Layered Separation of Concerns

Canonical concern boundaries, responsibility placement, stable-contract
dependency direction, and typed outcomes are owned by
[Architecture](topics/architecture.md). No universal layer count, layer name,
inward diagram, or domain-independence rule applies.

One conditional four-layer illustration and its qualified consequences are in
the non-normative
[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-layered-arrangement).

---

## Monorepo Package Roles

Canonical package responsibility, boundary selection, and stable-contract
dependency direction are owned by
[Architecture](topics/architecture.md). Shared artifact necessity and
producer-consumer semantics are owned by [Contracts](topics/contracts.md).
Repository layout and repeated data shapes do not select a package boundary.

A conditional role catalog, dependency illustration, and schema-sharing
example are in the non-normative
[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-monorepo-role-catalog).

---

## Backend-Owned Data

Canonical data and state authority, projections, reconciliation, and typed
outcomes are owned by [Architecture](topics/architecture.md). Web-technology
projection, synchronization, interaction, lifecycle, and evidence specialize
that decision through the
[Frontend application profile](profiles/applications/frontend.md). Process
location does not determine authority, and optimistic projection is neither
universally required nor prohibited.

A conditional server-authoritative projection example and its qualified
consequences are in the non-normative
[Architecture Pattern Reference](reference/patterns/architecture.md#conditional-server-authoritative-projection).

---

## Contract Planning Boundary

Use [Contract Evolution And Degraded Outcomes](topics/contracts.md) before
freezing or changing a shared contract. Contract stability, append-only
evolution, coordinated replacement, migration, and version overlap depend on
actual consumers, deployment, persistence, generated sources, and external
promises.

Freeze the selected contract shape while parallel work depends on it. Do not
turn that implementation-phase freeze into an indefinite compatibility promise.

---

## Executable Boundary Contracts

Canonical applicability, runtime-proof, validated-construction, and typed
diagnostic policy moved to
[Runtime Decoding At Boundaries](topics/contracts.md#runtime-decoding-at-boundaries).

## Structured Producer-Consumer Contracts

Canonical authority selection, applicable semantic facts, producer and consumer
proof, explicit transformation, typed diagnostics, and no-fallback policy moved
to [Producer-Consumer Semantic Preservation](topics/contracts.md#producer-consumer-semantic-preservation).

---

## IPC/Message Contract Pattern

Canonical message decoding, category/action selection, payload proof, typed
diagnostics, and validated-variant dispatch moved to the
[IPC Boundary Profile](profiles/boundaries/ipc.md).

---

## Composition Root Pattern

Canonical composition boundaries, responsibility placement, dependency
direction, lifecycle ownership, and typed outcomes moved to
[Runtime Composition](topics/architecture.md#runtime-composition). A
composition root is one possible arrangement after those facts are selected,
not a required module, application entrypoint, role catalog, injection style,
or test substitution mechanism.

One non-normative adaptation is available in the
[Conditional Composition Root](reference/patterns/architecture.md#conditional-composition-root).
Its diagram and role labels do not authorize ambient globals, feature-owned
infrastructure, one universal startup owner, or incumbent wiring as fallback.

---

## Realtime Workflow Systems

Canonical state authority and participant placement remain with
[Architecture](topics/architecture.md#data-and-state-authority). Operation and
transition meaning remain with
[Invariant Contracts](topics/contracts.md#invariant-contracts); durable
acceptance remains with the selected
[Persistence contract](profiles/boundaries/persistence.md#durable-mutation-contract);
ordering remains with
[Concurrency](topics/concurrency.md#select-coordination-from-the-invariant);
and replay, duplicate handling, convergence, and partial-failure recovery remain
with [Resilience](topics/resilience.md#replay-and-resumption-evidence).
Verification selects evidence through
[Selecting Claims](workflows/verification.md#selecting-claims).

A non-normative [Conditional Durable Workflow Map](reference/patterns/architecture.md#conditional-durable-workflow-map)
may communicate one arrangement after those owners select the applicable facts.
It does not require event sourcing, commands, a durable store, read models,
publishers, replay, or one fixed component catalog. A transient workflow does
not acquire durability or recovery obligations from this pattern name.

---

## View Model Pattern

Canonical frontend authority, presentation state, rendering, synchronization,
interaction adaptation, and lifecycle moved to the
[Frontend application profile](profiles/applications/frontend.md#projection-authority).
Canonical data and state ownership remains with
[Architecture](topics/architecture.md#data-and-state-authority), and evidence
claims remain with [Verification](workflows/verification.md#selecting-claims).

A view model, component store, derived selector, presenter, controller, or
framework binding is a possible frontend mechanism after those contracts are
selected. Existing non-normative synchronization examples are in the
[Frontend mechanism recipes](reference/recipes/frontend.md). The pattern name
does not require a dedicated class, source-view-model-view chain, subscription,
action forwarding, copied state, backend owner, or separate test surface.

---

## Directory Structure Template

Canonical module, package, and directory placement moved to
[Concern Boundaries](topics/architecture.md#concern-boundaries). Documentation
selection, boundary README use, and ADR linkage remain with the
[Documentation Workflow](workflows/documentation.md).

No general-purpose project tree is retained. Names such as `src`, `domain`,
`shared`, `tests`, or `docs`, directory depth, and a neighboring repository do
not select responsibilities, dependencies, ownership, documentation, or
evidence. Missing boundary or documentation facts return the canonical typed
diagnostic instead of selecting this legacy layout.

---

## Activity Tracing Pattern

Canonical diagnostic purpose, audience, causal identity, context, projection,
lifecycle, disclosure, and typed outcomes are owned by
[Diagnostics](topics/diagnostics.md). Illustrative TypeScript and logger
mechanisms moved to the non-normative
[Diagnostic Mechanism Recipes](reference/recipes/diagnostics.md).

---

## Process Instance Coordination

Canonical exclusion and atomicity are owned by
[Concurrency](topics/concurrency.md#select-coordination-from-the-invariant).
Instance identity and representation meaning remain with
[Contracts](topics/contracts.md), supported process-observation mechanisms with
[Cross-Platform](topics/cross-platform.md#platform-support-contract), and
stale-state classification and recovery with
[Resilience](topics/resilience.md#failure-classification-and-decision).
Architecture selects lifecycle ownership, while Diagnostics selects any
required reporting.

A PID file, operating-system mutex, supervisor, bound endpoint, lock, or other
mechanism is selected only after those facts are complete. No PID contents,
process-start-time check, liveness probe, cleanup action, or log is a universal
requirement.

One non-normative arrangement is available in the
[Conditional Process Instance Coordination](reference/patterns/architecture.md#conditional-process-instance-coordination).
Missing or contradictory identity, coordination, lifecycle, target, recovery,
or diagnostic facts retain the canonical typed outcome instead of selecting a
PID file or incumbent mechanism.

---

## Discover-or-Create Pattern

Canonical service placement, participant responsibility, and lifecycle
authority are owned by [Architecture](topics/architecture.md). Instance
identity and discovery outcomes remain with [Contracts](topics/contracts.md),
creation exclusion with
[Concurrency](topics/concurrency.md#select-coordination-from-the-invariant),
readiness and bounded retry with [Resilience](topics/resilience.md), and any
listener exposure or transport liveness with
[Security](topics/security.md#network-transport-boundary).

Discovery before creation, a creation lock, retry with backoff, a health probe,
and creator, client, or daemon ownership are possible mechanisms or lifecycle
arrangements, not defaults. Select each from the applicable contracts and
capabilities without substituting another mechanism when required facts are
missing.

One non-normative structural map is available in the
[Conditional Discover-Or-Create Convergence](reference/patterns/architecture.md#conditional-discover-or-create-convergence).
It cannot establish applicability, service identity, readiness, ownership,
transport, retry, or evidence.

---

## Phased Mutation Pattern

Canonical durable mutation invariants, isolated staging, publication, proof,
and typed outcomes are owned by the
[Persistence boundary profile](profiles/boundaries/persistence.md#durable-mutation-contract).
Fixed phases and pseudocode are non-normative examples in the
[Persistence Mechanism Recipes](reference/recipes/persistence.md#illustrative-staged-publication).
Generic process-local mutation remains outside the Persistence profile unless
state crosses a durable boundary.

---

## Schema Versioning and Migration

Canonical migration selection, artifact identity and integrity, deterministic
ordering, ledger consistency, re-entry, interruption, lifecycle triggering,
overlap, and typed outcomes are owned by the
[Persistence boundary profile](profiles/boundaries/persistence.md#migration-execution-contract)
under the source and destination states selected by
[Contracts](topics/contracts.md). SQL, filenames, ledger schemas, and startup
adapters are non-normative examples in the
[Persistence Mechanism Recipes](reference/recipes/persistence.md#illustrative-migration-adapters).

---

## Infrastructure Failure Recovery Index

Canonical dependency criticality, startup resilience, retry, recovery,
best-effort behavior, and evidence requirements moved to
[Resilience](topics/resilience.md). Contract authority for degraded outcomes
and reconstruction of disposable derived state remains in
[Contracts](topics/contracts.md#degraded-outcomes).

This is a non-normative migration index. It does not authorize defaults,
deletion, stale or cached reads, partial results, alternate backends, silent
continuation, or startup success.

---

## HTTP API Error Convention

Canonical outcome meaning, selected protocol mapping, response representation,
typed projection failures, and no-fallback policy moved to
[Protocol Outcome Projection](topics/contracts.md#protocol-outcome-projection).
Fixed HTTP status, envelope, and response-shape examples moved to the
non-normative [HTTP Projection Mechanism Recipes](reference/recipes/http.md).

This is a migration index, not an HTTP convention. It does not mandate a status
table, JSON envelope, message field, default `500`, or inference of operation
success from transport success.

Producer and consumer proof moved to
[Protocol Adapter Proof](topics/contracts.md#protocol-adapter-proof).
General boundary decoding remains in
[Inbound And Outbound Boundary Proof](topics/contracts.md#inbound-and-outbound-boundary-proof).
Pseudocode, selected `200` and `404` examples, and conditional interpretation
claims remain only in the non-normative recipes. Security, Diagnostics,
Resilience, and Verification retain their existing authority.

---

## Choosing Patterns

| Situation | Recommended Pattern |
|-----------|-------------------|
| Multi-layer application | Layered Separation of Concerns |
| Client-server state management | Backend-Owned Data |
| Parallel team development | Immutable Contracts |
| Multi-process communication | IPC/Message Contract |
| Complex UI with data | View Model |
| Distributed debugging | Activity Tracing |
| Single-instance process requirement | Process Instance Coordination |
| Service that any process may need to start | Discover-or-Create |
| Complex data structure mutations | Phased Mutation |
| Evolving database schemas across versions | Schema Versioning and Migration |
| Handling infrastructure failures | [Resilience](topics/resilience.md) |
| Consistent error responses from HTTP APIs | HTTP API Error Convention |
