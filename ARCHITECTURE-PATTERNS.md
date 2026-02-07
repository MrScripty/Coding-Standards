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

## Immutable Contracts

### The Pattern

Define shared interfaces/types FIRST, freeze them, then build implementations.

```
Phase 1: Define contracts (types, interfaces)
    ↓
Phase 2: Freeze contracts
    ↓
Phase 3: Implement against frozen contracts
```

### Contract Rules

1. **Define before implementing** - Contracts come first
2. **Freeze before parallel work** - No changes during implementation
3. **Append-only changes** - Add new types, don't modify existing
4. **Breaking changes require sync** - All parties must agree

### Example Contract

```typescript
// contracts/message.ts - FROZEN

interface Message {
    type: MessageType;
    action: string;
    payload: unknown;
    id?: string;
}

type MessageType =
    | 'request'
    | 'response'
    | 'notification';
    // New types can be added, existing cannot change
```

### Benefits

- **Parallel development:** Teams can work independently
- **Integration confidence:** Interfaces guaranteed to match
- **Clear boundaries:** Explicit API between components

---

## IPC/Message Contract Pattern

### The Pattern

For multi-process or client-server communication, use typed message contracts.

```
┌─────────────┐                    ┌─────────────┐
│  Process A  │ ── Message ──────▶ │  Process B  │
│             │ ◀─── Response ──── │             │
└─────────────┘                    └─────────────┘
```

### Message Structure

```typescript
interface IPCMessage {
    // Message category
    type: 'command' | 'query' | 'event' | 'response';

    // Specific action within category
    action: string;

    // Typed payload (varies by action)
    payload: unknown;

    // For request/response correlation
    correlationId?: string;

    // ISO timestamp
    timestamp: string;
}
```

### Message Categories

| Type | Direction | Purpose | Expects Response |
|------|-----------|---------|------------------|
| command | A → B | Request state change | Yes |
| query | A → B | Request data | Yes |
| event | A → B | Notify of occurrence | No |
| response | B → A | Reply to command/query | N/A |

### Example Implementation

```typescript
// Define specific messages
interface SelectItemCommand extends IPCMessage {
    type: 'command';
    action: 'selectItem';
    payload: { itemId: string };
}

interface ItemSelectedEvent extends IPCMessage {
    type: 'event';
    action: 'itemSelected';
    payload: { item: Item; previousId: string | null };
}

// Type-safe handler
function handleMessage(msg: IPCMessage): void {
    switch (msg.action) {
        case 'selectItem':
            handleSelectItem(msg.payload as SelectItemCommand['payload']);
            break;
        // ...
    }
}
```

### Benefits

- **Type safety:** Compile-time checking of message structure
- **Debugging:** Clear message format for logging
- **Versioning:** Easy to add new message types

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

Every directory under `src/` must contain a README.md with:
- Purpose
- Contents
- Dependencies
- Usage examples

---

## Activity Tracing Pattern

### The Pattern

Track operations across layers using correlation IDs and structured logging.

```
Request → [ID: abc-123]
    ├── Controller [ID: abc-123] "Handling request"
    ├── Service [ID: abc-123] "Processing business logic"
    ├── Repository [ID: abc-123] "Querying database"
    └── Response [ID: abc-123] "Request completed"
```

### Implementation

```typescript
interface ActivityContext {
    traceId: string;      // Request-level ID
    spanId: string;       // Operation-level ID
    parentSpanId?: string;
}

function withActivity<T>(
    name: string,
    context: ActivityContext,
    operation: () => T
): T {
    const span = {
        id: generateId(),
        parent: context.spanId,
        name
    };

    logger.debug(`Starting: ${name}`, { ...context, spanId: span.id });

    try {
        const result = operation();
        logger.debug(`Completed: ${name}`, { ...context, spanId: span.id });
        return result;
    } catch (error) {
        logger.error(`Failed: ${name}`, { ...context, spanId: span.id, error });
        throw error;
    }
}
```

### Benefits

- **Debugging:** Trace issues across entire request flow
- **Performance:** Identify slow operations
- **Observability:** Understand system behavior

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

```rust
use std::fs;
use std::path::Path;

fn is_original_process_alive(pid_file: &Path) -> bool {
    let contents = match fs::read_to_string(pid_file) {
        Ok(c) => c,
        Err(_) => return false,
    };
    let recorded: PidRecord = match serde_json::from_str(&contents) {
        Ok(r) => r,
        Err(_) => return false, // Corrupt file — treat as stale
    };

    // Check if process exists
    #[cfg(unix)]
    let alive = unsafe { libc::kill(recorded.pid, 0) } == 0;
    #[cfg(not(unix))]
    let alive = false; // Platform-specific check needed

    if !alive {
        return false;
    }

    // Compare start time to detect PID reuse
    match get_process_start_time(recorded.pid) {
        Some(actual_start) => actual_start == recorded.start_time,
        None => false, // Can't verify — treat as stale
    }
}
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

```rust
async fn get_or_create_service(addr: SocketAddr) -> Result<TcpStream> {
    // Step 1: Try to connect to existing instance
    if let Ok(stream) = TcpStream::connect(addr).await {
        return Ok(stream);
    }

    // Step 2: No instance found — acquire creation lock
    let lock = FileLock::acquire("service.lock")?;

    // Step 3: Double-check after acquiring lock (another process may have created it)
    if let Ok(stream) = TcpStream::connect(addr).await {
        drop(lock);
        return Ok(stream);
    }

    // Step 4: Create the service
    start_service(addr).await?;
    drop(lock);

    // Step 5: Connect to the newly created service
    let mut retries = 5;
    loop {
        match TcpStream::connect(addr).await {
            Ok(stream) => return Ok(stream),
            Err(_) if retries > 0 => {
                retries -= 1;
                tokio::time::sleep(Duration::from_millis(100)).await;
            }
            Err(e) => return Err(e.into()),
        }
    }
}
```

### Benefits

- No duplicate services consuming resources
- Automatic recovery from crashed instances
- Race-condition-safe startup sequence via double-check after lock acquisition

---

## Phased Mutation Pattern

### The Pattern

For complex mutations that modify interconnected data structures, use explicit phases to ensure atomicity and debuggability:

```rust
pub fn merge_nodes(&mut self, source: NodeId, target: NodeId) -> Option<MergeResult> {
    // ===== PHASE 1: GATHER (read-only, fail early) =====
    let data = self.gather_merge_data(source, target)?;

    // ===== PHASE 2: VALIDATE (check all preconditions) =====
    self.validate_merge_preconditions(&data)?;

    // ===== PHASE 3: CREATE (new elements with placeholders) =====
    let new_elements = self.create_merged_edges(&data);

    // ===== PHASE 4: CONNECT (wire up relationships) =====
    self.reconnect_edges(&data, &new_elements);

    // ===== PHASE 5: UPDATE (auxiliary structures) =====
    self.update_index(&data, &new_elements);

    // ===== PHASE 6: VALIDATE (debug-only postconditions) =====
    #[cfg(debug_assertions)]
    self.validate_consistency().expect("Merge corrupted graph");

    Some(new_elements.result())
}
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

```rust
// BAD: Validation and mutation interleaved
pub fn bad_merge_nodes(&mut self, source: NodeId, target: NodeId) -> Option<...> {
    let src = self.get_node(source)?;
    let new_edge = self.add_edge(...);  // Mutation!

    let tgt = self.get_node(target)?;  // May fail AFTER mutation
    let new_ref = self.add_reference(...);  // More mutation

    // If anything fails here, state is corrupted
}
```

### Implementation Tips

1. **Gather returns a struct** - Bundle all gathered data into a typed struct
2. **Create returns IDs** - Return identifiers of created elements for later phases
3. **Use placeholder values** - Create elements with temporary/invalid values, fix in Connect phase
4. **Validate is optional in release** - Use `#[cfg(debug_assertions)]` for expensive checks

```rust
struct MergeData {
    source: NodeId,
    target: NodeId,
    source_edges: Vec<EdgeId>,
    target_edges: Vec<EdgeId>,
    shared_neighbors: Vec<NodeId>,
}

struct CreatedElements {
    new_edges: Vec<EdgeId>,
    removed_nodes: Vec<NodeId>,
}
```

---

## Schema Versioning and Migration

### The Pattern

Every schema change is captured as a numbered, idempotent migration. Migrations
are applied in order at startup, and a version table tracks which migrations
have been applied. This ensures reproducible schema state across environments
and safe upgrades when different application versions share the same database.

### Migration Rules

| Rule | Rationale |
|------|-----------|
| Migrations are append-only | Never modify a released migration — create a new one |
| Each migration is idempotent | Safe to run twice (use `IF NOT EXISTS`, `IF EXISTS`) |
| Include both up and down logic | Enables rollback during failed deployments |
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

```rust
fn apply_pending_migrations(db: &Connection, migrations: &[Migration]) -> Result<()> {
    let current_version = db
        .query_row("SELECT COALESCE(MAX(version), 0) FROM schema_migrations", [], |r| r.get(0))
        .unwrap_or(0);

    for migration in migrations.iter().filter(|m| m.version > current_version) {
        db.execute_batch(&migration.up_sql)?;
        db.execute(
            "INSERT INTO schema_migrations (version, description) VALUES (?1, ?2)",
            params![migration.version, migration.description],
        )?;
        tracing::info!("Applied migration {}: {}", migration.version, migration.description);
    }

    Ok(())
}
```

### Forward/Backward Compatibility

When different application versions may access the same database:

| Change Type | Strategy | Example |
|------------|----------|---------|
| Add column | Add with a default value | `ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'member'` |
| Add table | Create unconditionally | New table is ignored by older versions |
| Remove column | Two-phase removal | Deprecate in v*N*, stop reading in v*N+1*, drop in v*N+2* |
| Rename column | Add new + copy + two-phase remove old | Older versions still read the old column |

**The rule:** Additive changes are safe. Destructive changes (drop, rename,
change type) require a two-phase rollout so that the old and new versions of the
application can coexist during deployment.

---

## Infrastructure Failure Recovery

### The Pattern

Infrastructure (databases, caches, file system, external services) can fail
independently of application logic. The application must categorize each piece
of infrastructure as **required** or **optional** and respond appropriately to
failures — never silently corrupt state, never crash on a non-essential failure.

**The principle:** Optional infrastructure is best-effort. Its failure must
never block core initialization or request handling.

### Failure Categories

| Category | Examples | Recovery Strategy |
|----------|----------|-------------------|
| Corrupt data store | Corrupted SQLite DB, invalid JSON config | Delete and rebuild from scratch, or seed defaults |
| Unavailable resource | Disk full, permissions changed | Log error, degrade gracefully, retry on next operation |
| Stale or missing cache | Cache file deleted, format changed | Treat as cold start, rebuild lazily |
| External service down | API timeout, DNS failure | Use cached fallback or return partial results |

### Decision Flow

```
Infrastructure operation fails
    │
    ├── Is this infrastructure required for the current operation?
    │       │
    │       ├── Yes → Propagate the error to the caller
    │       │
    │       └── No → Log a warning, continue with defaults or degraded mode
    │
    └── Is this a startup-time failure?
            │
            ├── Required infrastructure → Fail with a clear error message
            │
            └── Optional infrastructure → Start in degraded mode, log warning
```

### Startup Resilience

Categorize infrastructure at initialization:

| Infrastructure | Category | Failure at Startup |
|----------------|----------|--------------------|
| Core database / primary data store | Required | Fail with clear error message |
| Cache, index, or search | Optional | Start degraded, rebuild in background |
| Analytics, telemetry, logging sinks | Optional | Start without, retry later |
| Configuration file | Required | Fail with clear error message |

**The rule:** The application must start and serve requests even if optional
infrastructure is unavailable. See [CODING-STANDARDS.md](CODING-STANDARDS.md)
`## Error Handling` for code-level error handling patterns; this section covers
the architectural decision of *which failures to tolerate*.

### Best-Effort Service Pattern

Wrap optional infrastructure in a layer that catches failures, logs them,
and returns safe defaults:

```rust
pub struct BestEffortRegistry {
    db: Option<Connection>,
}

impl BestEffortRegistry {
    pub fn lookup(&self, key: &str) -> Option<String> {
        let db = self.db.as_ref()?;
        match db.query_row(
            "SELECT value FROM registry WHERE key = ?1",
            params![key],
            |row| row.get(0),
        ) {
            Ok(value) => Some(value),
            Err(e) => {
                tracing::warn!("Registry lookup failed for '{key}': {e}");
                None
            }
        }
    }

    pub fn is_healthy(&self) -> bool {
        self.db.is_some()
    }
}
```

### Benefits

- System remains available during partial infrastructure failures
- Clear separation of essential vs optional dependencies
- Predictable behavior under degraded conditions
- Failures are logged for diagnosis without crashing the application

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
| Handling infrastructure failures without crashing | Infrastructure Failure Recovery |
