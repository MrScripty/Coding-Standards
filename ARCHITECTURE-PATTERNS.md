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

A general-purpose project layout:

```
project-root/
├── src/
│   ├── presentation/           # UI layer
│   │   ├── components/         # Reusable UI components
│   │   ├── views/              # Page/screen compositions
│   │   └── styles/             # CSS/styling
│   │
│   ├── application/            # Application layer
│   │   ├── controllers/        # Request handlers
│   │   ├── handlers/           # Event/message handlers
│   │   └── mappers/            # DTO transformations
│   │
│   ├── domain/                 # Domain layer
│   │   ├── services/           # Business logic
│   │   ├── entities/           # Domain objects
│   │   └── value-objects/      # Immutable values
│   │
│   ├── infrastructure/         # Infrastructure layer
│   │   ├── api/                # External API clients
│   │   ├── database/           # Database access
│   │   └── messaging/          # Message queue/IPC
│   │
│   └── shared/                 # Cross-cutting concerns
│       ├── types/              # Shared type definitions
│       ├── utils/              # Utility functions
│       └── constants/          # Application constants
│
├── tests/                      # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                       # Documentation
├── scripts/                    # Build/deploy scripts
└── config/                     # Configuration files
```

### Directory README Requirement

Document meaningful architecture boundaries according to the
[Documentation Workflow](workflows/documentation.md). Directory depth and the
presence of a `src/` path do not create a documentation obligation.

Use a boundary README when this structure owns a responsibility or invariant
that is not clear from its public entry points. Use an ADR for durable
cross-boundary decisions and link to it instead of repeating its rationale.

---

## Activity Tracing Pattern

Canonical diagnostic purpose, audience, causal identity, context, projection,
lifecycle, disclosure, and typed outcomes are owned by
[Diagnostics](topics/diagnostics.md). Illustrative TypeScript and logger
mechanisms moved to the non-normative
[Diagnostic Mechanism Recipes](reference/recipes/diagnostics.md).

---

## Process Instance Coordination

### The Pattern

Ensure only one instance of a process or service is running by using PID files
with liveness checks. This prevents duplicate instances while handling crashes
and stale state gracefully.

```
Process starts
    │
    ├── PID file exists?
    │       │
    │       ├── Yes → Is PID alive AND start time matches?
    │       │           │
    │       │           ├── Yes → Another instance is running (exit or connect)
    │       │           │
    │       │           └── No → Stale PID file (delete and reclaim)
    │       │
    │       └── No → Continue
    │
    ├── Create PID file (write atomically)
    ├── Run
    └── Clean up PID file on exit
```

### PID File Rules

| Rule | Rationale |
|------|-----------|
| Write PID file atomically (write-to-temp, then rename) | Prevents partial reads by concurrent starters |
| Include process start time alongside PID | Detects PID reuse by the OS (see below) |
| Lock the PID file while running | OS-level mutual exclusion prevents TOCTOU races |
| Clean up PID file on graceful exit | Prevents stale files from blocking future starts |
| Always verify PID is alive before trusting | PID files survive crashes; the process may not |

### PID File Contents

Store enough information to distinguish a live instance from a stale file:

```json
{
    "pid": 48210,
    "start_time": 1706140800,
    "version": "1.2.0"
}
```

### Handling PID Reuse

Operating systems recycle PIDs. After a process dies, the OS may assign its PID
to an unrelated process. Checking `kill(pid, 0)` alone will return "alive" for
the wrong process.

**The fix:** Store the process start time in the PID file and compare it against
the actual start time of the running process.

```text
function is_original_process_alive(pid_file):
    recorded = read_and_parse_pid_file(pid_file)
    if recorded is invalid:
        return false

    if process_does_not_exist(recorded.pid):
        return false

    actual_start = get_process_start_time(recorded.pid)
    return actual_start == recorded.start_time
```

On Linux, process start time can be read from `/proc/[pid]/stat`. On Windows,
use the process creation time via the Windows API. See
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) for platform
abstraction strategies.

### Stale PID File Cleanup

When a PID file references a dead process (or a reused PID with a different
start time), the file is stale. Delete it and proceed with normal startup.
Always log when reclaiming a stale PID file — it indicates a previous crash.

---

## Discover-or-Create Pattern

### The Pattern

When a process needs access to a shared service (local server, registry,
coordinator), it first attempts to discover an existing instance. If none
exists, it creates one itself. All processes converge to using the same
instance.

This pattern builds on [Process Instance Coordination](#process-instance-coordination)
for detecting existing instances and uses network transport safety practices
from [SECURITY-STANDARDS.md](SECURITY-STANDARDS.md) `## Network Transport Safety`
for the listener.

### Instance Convergence Flow

```
Process starts
    │
    ├─► Try to connect to existing service (known address/port)
    │       │
    │       ├── Success → Use existing instance
    │       │
    │       └── Failure → No instance found
    │               │
    │               ├─► Acquire creation lock (file lock, PID file)
    │               │       │
    │               │       ├── Lock acquired → Create service, release lock
    │               │       │
    │               │       └── Lock failed → Another process is creating
    │               │               │
    │               │               └─► Retry connection with backoff
    │               │
    │               └─► Connect to newly created service
```

### Rules

| Rule | Rationale |
|------|-----------|
| Attempt connection before creation | Avoids duplicate instances |
| Use a creation lock | Prevents race between concurrent starters |
| Retry with backoff after lock failure | Gives the creator time to finish startup |
| Verify service health after connecting | Existing instance may be shutting down |
| Define an ownership model | Determines when the service exits |

### Ownership Models

| Model | How It Works | When to Use |
|-------|-------------|-------------|
| Creator-owned | Service exits when the process that created it exits | Simple tools, short-lived sessions |
| Last-client-standing | Service exits when all clients disconnect | Shared background services |
| Independent daemon | Service runs until explicitly stopped | Long-lived infrastructure |

### Example

```text
function get_or_create_service(address):
    if connect(address) succeeds:
        return existing connection

    lock = acquire_creation_lock()

    if connect(address) succeeds:
        release lock
        return existing connection

    start service
    release lock

    retry connect(address) until ready or timeout
```

### Benefits

- No duplicate services consuming resources
- Automatic recovery from crashed instances
- Race-condition-safe startup sequence via double-check after lock acquisition

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
