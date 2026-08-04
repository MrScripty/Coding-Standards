# Architecture Patterns

Reusable design patterns for multi-layer and client-server applications.

## Layered Separation of Concerns

### The Pattern

Organize code into horizontal layers, each with a single responsibility:

```
┌─────────────────────────────────────┐
│           Presentation              │  UI, views, user interaction
├─────────────────────────────────────┤
│           Application               │  Use cases, orchestration
├─────────────────────────────────────┤
│            Domain                   │  Business logic, rules
├─────────────────────────────────────┤
│          Infrastructure             │  External systems, I/O
└─────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Contains |
|-------|---------------|----------|
| Presentation | Display and user input | UI components, views, formatters |
| Application | Orchestrate use cases | Controllers, handlers, coordinators |
| Domain | Business logic | Services, entities, value objects |
| Infrastructure | External communication | APIs, databases, file systems |

### Dependency Rule

**Dependencies point inward only.**

```
Presentation → Application → Domain ← Infrastructure
```

- Outer layers depend on inner layers
- Inner layers never depend on outer layers
- Domain is the core and depends on nothing

### Benefits

- **Testability:** Domain logic testable without UI or database
- **Flexibility:** Replace infrastructure without changing business rules
- **Maintainability:** Changes isolated to appropriate layer

### Layering Is Not Simplicity By Itself

Layering only helps when layers separate independent decisions. Moving complex,
entangled behavior into separate files, packages, services, or layers does not
make the design simple by itself.

A boundary is justified when it prevents unrelated concerns from needing to be
understood, changed, tested, or deployed together. If two layers must always be
changed together for ordinary feature work, review whether the boundary is
missing an explicit contract or whether the split is only organizational.

---

## Monorepo Package Roles

### The Pattern

In multi-package repositories, assign each package a stable architectural role.
Package boundaries should enforce responsibility and dependency direction, not
just group files by convenience.

Package names and folder names may vary. The rule is about what a package is
allowed to contain and which other roles it may depend on.

### Common Roles

| Role | Contains | Must Not Contain |
|------|----------|------------------|
| App | Deployable/runtime entrypoints, composition, startup, transport wiring | Reusable shared logic that should live outside the app |
| Contracts | Shared schemas, DTOs, message formats, boundary enums/IDs | I/O, side effects, business workflows, framework runtime glue |
| Domain/Core | Business rules, entities, pure orchestration rules | UI, transport handlers, persistence drivers |
| Shared Utilities | Small reusable helpers and low-level utilities | Feature ownership, workflow orchestration, app entrypoints |
| Tooling/Config | Build config, lint config, shared scripts, codegen config | Product runtime logic |

Only create the roles your repo actually needs. Small repos may collapse some
roles into directories instead of separate packages.

### Dependency Direction

```
apps ─────────────▶ contracts
apps ─────────────▶ domain/core
apps ─────────────▶ shared utilities
domain/core ──────▶ contracts
shared utilities ─▶ contracts (only when truly generic)
tooling/config ───▶ none of the runtime app layers by default
```

Rules:
- App packages may compose other roles, but should not import another app's
  internal implementation modules.
- Contracts packages should be safe for both producers and consumers to depend
  on.
- Domain/core packages should depend on contracts or narrow infrastructure
  interfaces, not UI or transport implementations.
- Shared utilities should stay narrow; if a package starts owning workflow
  decisions, promote it to a clearer domain/app role.
- Tooling/config packages should support development workflows without becoming
  a back door for runtime dependencies.

### Why This Helps

- **Boundary enforcement:** Imports reflect architecture, not accidental file location
- **Refactor safety:** Shared contracts and shared logic can move without cross-app tangling
- **Review clarity:** Misplaced code is easier to spot during review
- **Reuse control:** Shared packages stay intentional instead of becoming dump folders

### Example Decision

If a web app and a server both need the same request/response schema, place it
in a contracts package. Do not import server implementation modules into the
web app just to reuse type definitions.

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

Canonical durable-state authority, mechanism selection, boundary ownership,
and typed outcomes are owned by the
[Persistence boundary profile](profiles/boundaries/persistence.md). The legacy
mutation and migration mechanisms below remain only until their scheduled
extraction in children 32.2 and 32.3.

### The Pattern

For complex mutations that modify interconnected data structures, use explicit phases to ensure atomicity and debuggability:

```text
function merge_nodes(source, target):
    data = gather_merge_data(source, target)
    validate_merge_preconditions(data)
    new_elements = create_merged_edges(data)
    reconnect_edges(data, new_elements)
    update_indexes(data, new_elements)
    validate_postconditions_in_debug_builds()
    return merge result
```

### Phase Responsibilities

| Phase | Purpose | Mutates State? |
|-------|---------|----------------|
| Gather | Collect all needed data | No |
| Validate | Check preconditions | No |
| Create | Allocate new elements | Yes (append only) |
| Connect | Wire up relationships | Yes |
| Update | Sync auxiliary structures | Yes |
| Validate | Check postconditions | No (debug only) |

### Benefits

- **Fail early** - All validation happens before any mutation
- **Atomic** - Either completes fully or not at all
- **Debuggable** - Clear phase boundaries for stepping through code
- **Documentable** - Each phase has a single responsibility
- **Reversible** - Easier to implement undo when phases are clear

### When to Use

Use this pattern when:

- Modifying graphs or linked structures (trees, dependency graphs, state machines)
- Operations have multiple interrelated updates
- Partial completion would corrupt state
- You need to support undo/redo
- Debugging complex state transitions

### Anti-Pattern: Interleaved Mutation

```text
BAD:
1. Read source node.
2. Add new edge.
3. Read target node.
4. Add reference.

If step 3 fails after step 2 mutates state, the operation leaves partial state.
```

### Implementation Tips

1. **Gather returns a struct** - Bundle all gathered data into a typed struct
2. **Create returns IDs** - Return identifiers of created elements for later phases
3. **Use placeholder values** - Create elements with temporary/invalid values, fix in Connect phase
4. **Validate is optional in release** - Keep expensive checks in debug or
   diagnostic builds when runtime cost is too high for production paths.

Bundle gathered data and created element IDs into named structures so later
phases do not recompute or accidentally read partially mutated state.

---

## Schema Versioning and Migration

### The Pattern

Use migrations when [the contract decision](topics/contracts.md) requires
retained persisted states to move between schema versions. A project may use
numbered migrations applied in order with a version table; other stores may use
transactional replacement, export/import, or explicit rejection when their
recorded contract permits it.

### Migration Rules

| Rule | Rationale |
|------|-----------|
| Published migrations are immutable while supported states depend on them | Preserve reproducibility for retained data |
| Re-entry behavior is explicit | Use idempotency or enforce one-shot transactional preconditions |
| Rollback behavior is explicit | Provide down migration, restore, forward repair, or documented no-rollback handling |
| A version table tracks applied migrations | Know exactly what state the schema is in |
| Test migrations against realistic data | Empty-table migrations can mask column-type or constraint issues |

### Migration File Structure

```
migrations/
├── 001_initial_schema.sql
├── 002_add_user_preferences.sql
├── 003_add_index_on_created_at.sql
└── 004_add_status_column.sql
```

Use sequential numbering (`NNN_description.sql`) for ordering clarity. Timestamp
prefixes (`20240125_120000_description.sql`) work for teams where concurrent
branch development would create numbering conflicts.

### Schema Version Tracking

Maintain a metadata table that records which migrations have been applied:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL DEFAULT (datetime('now')),
    description TEXT NOT NULL
);
```

At startup, check the current version and apply any pending migrations:

```text
function apply_pending_migrations(database, migrations):
    current_version = read_current_schema_version(database)

    for migration in migrations where migration.version > current_version:
        apply migration SQL inside a transaction
        record migration version and description
        log applied migration
```

### Version Overlap

Only require coexistence when recorded deployment facts allow different
application versions to access the same database:

| Change Type | Strategy | Example |
|------------|----------|---------|
| Add column | Add with a default value | `ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'member'` |
| Add table | Create unconditionally | New table is ignored by older versions |
| Remove column | Two-phase removal | Deprecate in v*N*, stop reading in v*N+1*, drop in v*N+2* |
| Rename column | Add new + copy + two-phase remove old | Older versions still read the old column |

Additive changes can still break defaults, constraints, readers, or exhaustive
consumers. Validate each change against the selected contract class. When all
consumers deploy atomically and retained states are migrated, coordinated
destructive replacement does not require a speculative two-phase shim.

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

### The Pattern

HTTP APIs must use status codes to communicate success or failure. Error
details are returned in a consistent JSON envelope so clients can handle
errors uniformly.

### Error Response Format

```json
{
    "error": "Human-readable description of what went wrong"
}
```

### Status Code Usage

| Status Code | Meaning | When to Use |
|-------------|---------|-------------|
| 200 | OK | Successful retrieval or action |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Invalid input, missing fields |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Concurrent modification conflict |
| 500 | Internal Server Error | Unhandled server-side failure |

### Server Implementation

Use a shared error type that converts to the correct status code:

```text
ApiError:
    status_code
    message

not_found(message) -> ApiError(404, message)
bad_request(message) -> ApiError(400, message)

HTTP adapter converts ApiError into:
    status: error.status_code
    body: { "error": error.message }
```

### Client Implementation

Clients must check the status code before parsing the response body.
See [Contracts](topics/contracts.md#inbound-and-outbound-boundary-proof) for
canonical boundary-proof policy.

### Anti-Pattern: Status 200 with Error Body

```
// BAD: Returns 200 with an error message in the body
HTTP/1.1 200 OK
{ "error": "Project not found" }

// GOOD: Returns proper status code
HTTP/1.1 404 Not Found
{ "error": "Project not found" }
```

**Why:** Returning 200 for errors breaks HTTP semantics. Clients, proxies,
and monitoring tools all rely on status codes to distinguish success from
failure. An error hidden inside a 200 response is invisible to everything
except custom parsing logic.

### Benefits

- **Uniform error handling:** Clients use one pattern for all error responses
- **Observable:** Monitoring and logging tools can alert on 4xx/5xx rates
- **Self-documenting:** Status codes convey intent without reading the body

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
