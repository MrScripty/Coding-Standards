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

## Choosing Patterns

| Situation | Recommended Pattern |
|-----------|-------------------|
| Multi-layer application | Layered Separation of Concerns |
| Client-server state management | Backend-Owned Data |
| Parallel team development | Immutable Contracts |
| Multi-process communication | IPC/Message Contract |
| Complex UI with data | View Model |
| Distributed debugging | Activity Tracing |
| Complex data structure mutations | Phased Mutation |
