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

### The Pattern

In client-server applications, the backend is the **single source of truth** for all persistent data.

```
┌──────────────────┐         ┌──────────────────┐
│     Backend      │ ──push─▶│    Frontend      │
│  (source of      │         │   (display)      │
│    truth)        │◀─action─│                  │
└──────────────────┘         └──────────────────┘
```

### Rules

**Frontend CAN hold (transient UI state):**
- Hover/focus state
- Animation state
- Form input before submission
- Drag/drop state
- Modal open/closed state

**Frontend CANNOT hold (backend-owned):**
- Business data (users, products, orders)
- Selection state that affects business logic
- Configuration that affects behavior
- Anything that should persist

### Data Flow

1. Backend pushes data to frontend
2. Frontend displays data (read-only view)
3. User takes action
4. Frontend sends action to backend
5. Backend processes and pushes new state
6. Frontend displays updated state

### No Optimistic Updates for Backend-Owned Data

Backend-owned data must never be updated speculatively. The frontend waits
for the backend to confirm the new state before displaying it.

```typescript
// BAD: Update UI before backend confirms
function deleteItem(id) {
    items = items.filter(i => i.id !== id);  // Optimistic — creates desync risk
    api.deleteItem(id);
}

// GOOD: Wait for backend to push new state
async function deleteItem(id) {
    await api.deleteItem(id);
    // Backend pushes updated state → view model updates → UI renders
}
```

**What IS acceptable to update locally:**

- Transient UI state (hover, focus, drag position, loading spinners)
- Animation state
- Form input before submission
- Purely presentational state with no backend equivalent (scroll position,
  panel sizes, expanded/collapsed UI sections)
- Framework-specific reactive state for UI-only reactivity

**The test:** If the backend has no concept of this state, the frontend can
own it. If the backend stores or acts on this data, the backend owns it.

### Benefits

- **Consistency:** No state synchronization bugs
- **Reliability:** UI always reflects actual state
- **Simplicity:** One source of truth

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

### The Pattern

Assemble concrete implementations at one application boundary instead of
letting wiring logic spread through feature modules.

```
composition root
    ├── create infrastructure implementations
    ├── create service implementations
    ├── connect them together
    └── expose only the app/runtime entrypoint
```

Use this pattern for apps with multiple services, infrastructure clients,
background workers, or process lifecycle concerns.

### Roles

| Module Type | Responsibility |
|-------------|----------------|
| Contract/facade module | Defines the public interface used by consumers |
| Implementation module | Contains the concrete behavior and dependency usage |
| Composition root | Chooses implementations, wires dependencies, owns startup/shutdown |

### Rules

- Consumers depend on service contracts/facades, not concrete implementations.
- Concrete implementations are selected at the application boundary.
- Startup and shutdown ownership for sockets, workers, timers, and background
  loops belongs in the composition root or another single lifecycle owner.
- Feature modules may request dependencies, but should not create global
  infrastructure instances ad hoc.
- If a module needs different implementations in test vs production, swap them
  in the composition root rather than branching inside business logic.

```typescript
// GOOD: App boundary wires the implementation
const userRepository = new SqlUserRepository(db);
const userService = new UserService(userRepository);
const server = new ApiServer(userService);
```

```typescript
// BAD: Feature module reaches outward and self-wires infrastructure
export function handleRequest(input: Request) {
    const db = createDatabaseConnection();
    const repo = new SqlUserRepository(db);
    const service = new UserService(repo);
    return service.handle(input);
}
```

### Benefits

- **Replaceability:** Tests, local dev, and production can use different implementations cleanly
- **Lifecycle clarity:** One place owns long-lived resources and cleanup
- **Boundary discipline:** Business logic depends on contracts, not environment wiring

---

## Realtime Workflow Systems

### The Pattern

For systems that handle durable commands, long-lived sessions, reconnects, or
partial failures, separate transport handling from canonical workflow state and
event progression.

This is an optional pattern. Use it when the system must stay predictable across
restarts, retries, reconnects, or partial processing, not for every CRUD app.

### Workflow Shape

```
command/request
    ├── validate + dedupe/idempotency check
    ├── append canonical event(s)
    ├── project read model(s)
    ├── publish updates to consumers
    └── replay/bootstrap on restart
```

### Rules

- Transport layers decode requests and forward commands, but should not own the
  workflow state machine.
- Use stable command identifiers when retries or duplicate delivery are possible.
- Persist canonical events or equivalent durable state transitions before
  treating work as accepted.
- Build read models/projections for query and UI needs instead of coupling
  consumers directly to transient workflow internals.
- On startup, bootstrap workflow state from durable state instead of trusting
  in-memory leftovers.
- After partial failure, reconcile from the persisted source of truth before
  resuming new work.
- Keep event ordering, replay semantics, and projection compatibility explicit.

### Typical Components

| Component | Responsibility |
|-----------|----------------|
| Transport adapter | Decode requests, encode responses, manage connection details |
| Command handler/orchestrator | Validate commands and decide next state transition(s) |
| Durable store | Persist events or equivalent durable transitions |
| Projection/read model | Build query-friendly state for consumers |
| Update publisher | Push new state/events to subscribers |

### Benefits

- **Recovery:** Restarts and reconnects do not silently corrupt workflow state
- **Idempotency:** Retries are less likely to duplicate work
- **Separation:** UI/query consumers read stable projections instead of mutable internals
- **Auditability:** Durable transitions create a clearer history of what happened

### Verification Note

When using this pattern, require tests for replay/bootstrap, duplicate command
handling, projection consistency, and recovery after partial failure. See
[TESTING-STANDARDS.md](TESTING-STANDARDS.md) for cross-layer acceptance
expectations and [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) for
lifecycle/overlap safety.

---

## View Model Pattern

### The Pattern

Separate data management from presentation using dedicated view model objects.

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Source    │ ───▶ │  View Model  │ ───▶ │    View      │
│   (backend)  │      │ (transforms) │      │   (renders)  │
└──────────────┘      └──────────────┘      └──────────────┘
```

### Responsibilities

| Component | Responsibility |
|-----------|---------------|
| Source | Provides raw data |
| View Model | Transforms, derives, exposes data |
| View | Renders what view model provides |

### View Model Rules

1. **Subscribe to data source** - Receive updates automatically
2. **Expose derived values** - Computed properties for display
3. **Forward actions** - Don't implement business logic
4. **Don't duplicate backend-owned data** — The view model reflects backend
   state; it does not maintain a separate copy. Local fields for
   UI-only concerns (loading flags, filter strings, expanded nodes) are fine
   because they have no backend equivalent.

### Example

```typescript
// view-models/user-list.vm.ts

class UserListViewModel {
    // Raw data from source
    private _users: User[] = [];

    // Subscribe to data source
    constructor(private dataSource: DataSource) {
        dataSource.on('users:updated', (users) => {
            this._users = users;
        });
    }

    // Derived: Filtered for display
    get activeUsers(): User[] {
        return this._users.filter(u => u.isActive);
    }

    // Derived: Formatted for display
    get userCount(): string {
        return `${this.activeUsers.length} active users`;
    }

    // Forward action to backend (don't implement here)
    selectUser(userId: string): void {
        this.dataSource.send('selectUser', { userId });
    }
}
```

### Benefits

- **Testable:** View models can be tested without UI
- **Reusable:** Same view model for different view implementations
- **Clean views:** Views only handle rendering

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
