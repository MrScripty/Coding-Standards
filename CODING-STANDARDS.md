# Coding Standards

Generic coding conventions applicable to any tech stack.

## File Organization

### Maximum File Size

**Target: 500 lines per file**

When a file exceeds 500 lines:
1. Identify logical groupings within the file
2. Extract related functionality into separate files
3. Use clear naming that reflects the extracted responsibility

**Why:** Large files are harder to navigate, review, and test. Smaller files encourage single-responsibility design.

### Directory Structure

Every directory must contain a `README.md` explaining:
- Purpose of the directory
- What files it contains
- How it relates to other directories

See [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) for the template.

## Layered Architecture

Organize code into distinct layers with clear responsibilities:

```
┌─────────────────────────────────────┐
│  Presentation Layer (Views/UI)      │  User-facing components
├─────────────────────────────────────┤
│  Controller Layer (Orchestration)   │  Coordinates between layers
├─────────────────────────────────────┤
│  Service Layer (Business Logic)     │  Core domain logic
├─────────────────────────────────────┤
│  Model Layer (Data Structures)      │  DTOs, entities, types
├─────────────────────────────────────┤
│  Infrastructure Layer (External)    │  APIs, databases, file I/O
└─────────────────────────────────────┘
```

### Layer Rules

| Layer | Can Depend On | Cannot Depend On |
|-------|---------------|------------------|
| Presentation | Controllers, Models | Services directly, Infrastructure |
| Controllers | Services, Models | Infrastructure directly |
| Services | Models, Infrastructure interfaces | Presentation, Controllers |
| Models | Nothing | Any other layer |
| Infrastructure | Models | Services, Controllers, Presentation |

### Why Layering Matters

- **Testability:** Services can be unit tested without UI or database
- **Flexibility:** Swap infrastructure without changing business logic
- **Clarity:** Clear ownership of responsibilities

## Separation of Concerns

### Backend-Owned Data Principle

When building client-server applications:

**The backend is the single source of truth.**

Frontend/client can hold:
- Transient UI state (hover, focus, animation)
- Pending user input (before submission)
- Drag/drop state
- Local preferences

Frontend/client must NOT hold:
- Business data
- Selection state affecting business logic
- Configuration that affects behavior
- Anything that needs to survive a page refresh

**Data Flow:**
```
Backend (source) ──push──▶ Frontend (display)
     ▲                          │
     └────── user action ───────┘
```

**No Optimistic Updates:** Wait for backend confirmation before updating UI state.

### Service Independence

Services should be framework-agnostic:

```
// BAD: Service depends on framework
class UserService {
    save(user: User) {
        FrameworkContext.getCurrentUser();  // Framework coupling
    }
}

// GOOD: Service receives dependencies
class UserService {
    save(user: User, currentUserId: string) {
        // Pure business logic
    }
}
```

**Why:** Framework-agnostic services can be unit tested without mocking the entire framework.

## Constants and Configuration

### No Magic Numbers or Strings

Every literal value should be a named constant:

```
// BAD
if (retryCount > 3) { ... }
element.style.width = '200px';

// GOOD
const MAX_RETRIES = 3;
const PANEL_MIN_WIDTH = 200;

if (retryCount > MAX_RETRIES) { ... }
element.style.width = `${PANEL_MIN_WIDTH}px`;
```

### Centralize Constants

Group related constants together:

```
// constants/ui.ts
export const UI = {
    PANEL_MIN_WIDTH: 200,
    PANEL_MAX_WIDTH: 600,
    ANIMATION_DURATION_MS: 300,
    DEBOUNCE_DELAY_MS: 150,
} as const;

// constants/limits.ts
export const LIMITS = {
    MAX_FILE_SIZE_MB: 50,
    MAX_RETRIES: 3,
    REQUEST_TIMEOUT_MS: 30000,
} as const;
```

## Error Handling

### Exceptions for Exceptional Cases

Use exceptions only for truly unexpected situations:

```
// BAD: Using exceptions for control flow
try {
    user = findUser(id);
} catch (NotFoundError) {
    user = createDefaultUser();
}

// GOOD: Explicit handling
user = findUser(id);
if (!user) {
    user = createDefaultUser();
}
```

### Catch at Boundaries

Handle exceptions at system boundaries:
- API/IPC handlers
- Event handlers
- Entry points

Don't catch and re-throw without adding value:

```
// BAD: Pointless catch
try {
    doSomething();
} catch (error) {
    throw error;  // Adds nothing
}

// GOOD: Add context or handle
try {
    doSomething();
} catch (error) {
    logger.error('Failed during operation X', { error, context });
    throw new OperationError('Operation X failed', { cause: error });
}
```

### Validate at Boundaries

Validate input at system boundaries, not throughout the code:

```
// API boundary - validate here
function handleRequest(input: unknown): Response {
    const validated = validateInput(input);  // Throws if invalid
    return processValidatedInput(validated);
}

// Internal function - trust the input
function processValidatedInput(input: ValidatedInput): Result {
    // No need to re-validate
}
```

## Dependency Management

### Minimize External Dependencies

Before adding a dependency, ask:
1. Can this be implemented in <50 lines?
2. Does this add significant transitive dependencies?
3. Is this actively maintained?
4. Is there already a similar dependency in the project?

### Approved vs. Avoided

Create an explicit list of approved dependencies for your project:

```markdown
## Approved Dependencies
- [List your approved packages]

## Avoid
- Utility libraries for simple operations (implement locally)
- Multiple packages solving the same problem
- Packages with excessive transitive dependencies
```

## Code Style

### Avoid Over-Engineering

Only make changes that are directly requested or clearly necessary:

- Don't add features beyond what was asked
- Don't refactor surrounding code when fixing a bug
- Don't add comments to code you didn't change
- Don't add error handling for impossible scenarios
- Don't create abstractions for one-time operations

```
// BAD: Over-engineered for a single use case
class ConfigurableGreeterFactory {
    constructor(private config: GreeterConfig) {}
    create(): Greeter { ... }
}

// GOOD: Simple and direct
function greet(name: string): string {
    return `Hello, ${name}!`;
}
```

### Delete Unused Code

Don't leave backwards-compatibility hacks:

```
// BAD: Keeping dead code
const _oldVariable = null;  // Unused, kept for "compatibility"
// removed: oldFunction()

// GOOD: Just delete it
// (nothing here - it's gone)
```

## Naming Conventions

### Be Descriptive

Names should explain what something is or does:

```
// BAD
const d = new Date();
function proc(x) { ... }
const temp = users.filter(u => u.active);

// GOOD
const createdAt = new Date();
function processPayment(payment) { ... }
const activeUsers = users.filter(user => user.active);
```

### Consistent Terminology

Use the same term for the same concept throughout the codebase:

```
// BAD: Inconsistent naming
getUserById()
fetchCustomerById()  // Same concept, different name
loadPersonById()     // Same concept, another name

// GOOD: Consistent
getUserById()
getOrderById()
getProductById()
```
