# Security Standards

Input validation, path safety, and sanitization requirements.

## Core Principle: Validate Once, at the Boundary

All external input is validated at the point it enters the system. Internal
code trusts validated input. This prevents both missed validation and
redundant validation scattered through the codebase.

```
External Input ──► [Validation Module] ──► Trusted Internal Code
                        │
                   Reject if invalid
```

## Path Validation

### The Problem

User-supplied file paths can escape intended directories using `..` sequences
or symlinks. A path like `../../etc/passwd` could access arbitrary files.

### Centralized Path Validator

All path validation goes through a single, shared utility. No handler
validates paths inline.

**C# — `PathValidator` utility:**

```csharp
/// <summary>
/// Centralized path validation. All file path inputs must pass through this.
/// </summary>
public static class PathValidator
{
    /// <summary>
    /// Validates that a path resolves to a location within the allowed root.
    /// Returns the resolved absolute path, or null if validation fails.
    /// </summary>
    public static string? ValidateAndResolve(string inputPath, string allowedRoot)
    {
        if (string.IsNullOrWhiteSpace(inputPath)) return null;

        // Resolve to absolute path (handles ../ sequences)
        var resolved = Path.GetFullPath(inputPath);
        var normalizedRoot = Path.GetFullPath(allowedRoot);

        // Ensure the resolved path is within the allowed root
        if (!resolved.StartsWith(normalizedRoot, StringComparison.OrdinalIgnoreCase))
            return null;

        return resolved;
    }

    /// <summary>
    /// Validates a path is within the project directory.
    /// </summary>
    public static string? ValidateWithinProject(string inputPath, string projectRoot)
    {
        return ValidateAndResolve(inputPath, projectRoot);
    }
}
```

**TypeScript — Path validation:**

```typescript
import path from 'node:path';

export function isPathWithinRoot(inputPath: string, allowedRoot: string): boolean {
    const resolved = path.resolve(inputPath);
    const root = path.resolve(allowedRoot);
    return resolved.startsWith(root);
}
```

**Rust — Path validation:**

```rust
use std::path::{Path, PathBuf};

pub fn validate_within_root(input: &Path, allowed_root: &Path) -> Option<PathBuf> {
    let resolved = input.canonicalize().ok()?;
    let root = allowed_root.canonicalize().ok()?;
    if resolved.starts_with(&root) {
        Some(resolved)
    } else {
        None
    }
}
```

### Usage in Handlers

Every handler that receives a file path from external input must validate it:

```csharp
public async Task<Response> HandleOpenProject(Request request)
{
    // Validate path BEFORE any file operations
    var validPath = PathValidator.ValidateWithinProject(request.ProjectPath ?? "", _projectRoot);
    if (validPath == null)
        return ErrorResponse("Invalid or disallowed path");

    // Safe to use validPath
    var files = Directory.GetFiles(validPath);
}
```

---

## Input Validation

### Centralized Input Validator

String inputs from external sources should be validated through shared utilities:

```csharp
/// <summary>
/// Centralized input validation for external input payloads.
/// </summary>
public static class InputValidator
{
    private static readonly Regex SafeNamePattern = new(@"^[a-zA-Z0-9_-]+$", RegexOptions.Compiled);

    /// <summary>
    /// Validates a user-provided name (project name, file name, etc.).
    /// </summary>
    public static (bool isValid, string? error) ValidateName(
        string? name, int minLength = 1, int maxLength = 64)
    {
        if (string.IsNullOrWhiteSpace(name))
            return (false, "Name is required");
        if (name.Length < minLength)
            return (false, $"Name must be at least {minLength} characters");
        if (name.Length > maxLength)
            return (false, $"Name must be at most {maxLength} characters");
        if (!SafeNamePattern.IsMatch(name))
            return (false, "Name can only contain letters, numbers, underscores, and hyphens");
        return (true, null);
    }

    /// <summary>
    /// Validates a required non-empty string field.
    /// </summary>
    public static (bool isValid, string? error) ValidateRequired(string? value, string fieldName)
    {
        if (string.IsNullOrWhiteSpace(value))
            return (false, $"{fieldName} is required");
        return (true, null);
    }
}
```

### Validation Rules

| Input Type | Validation | Where |
|------------|-----------|-------|
| File paths | Resolve and check against allowed root | PathValidator |
| User-provided names | Regex allowlist, length bounds | InputValidator |
| Required string fields | Non-empty check | InputValidator |
| JSON payloads | Runtime type check before cast | API boundary |
| Numeric ranges | Bounds check before use | Handler |

### No Duplicate Validation Logic

The validation modules above are the **single implementation**. Handlers must
not write their own regex patterns or path checks inline.

```csharp
// BAD: Inline regex duplicating InputValidator logic
if (!Regex.IsMatch(name, @"^[a-zA-Z0-9_-]+$"))
    return error;

// GOOD: Use the shared validator
var (isValid, error) = InputValidator.ValidateName(name);
if (!isValid)
    return ErrorResponse(error!);
```

---

## Message/API Payload Validation

### TypeScript — Validate Before Dispatch

```typescript
function receiveMessage(json: string): void {
    let parsed: unknown;
    try {
        parsed = JSON.parse(json);
    } catch {
        console.error('Invalid JSON received');
        return;
    }

    // Runtime type check — don't trust as-casts
    if (!parsed || typeof parsed !== 'object') return;
    const msg = parsed as Record<string, unknown>;
    if (typeof msg.type !== 'string' || typeof msg.action !== 'string') {
        console.error('Missing required fields');
        return;
    }

    // Now safe to dispatch
    handleMessage(msg as ValidatedMessage);
}
```

### C# — Validate Deserialized Payloads

```csharp
// Deserialize and null-check
var request = JsonSerializer.Deserialize<OpenProjectRequest>(payload);
if (request == null)
    return ErrorResponse("Invalid payload");

// Then validate domain-specific fields
var (nameValid, nameError) = InputValidator.ValidateName(request.ProjectName);
if (!nameValid)
    return ErrorResponse(nameError!);

var validPath = PathValidator.ValidateWithinProject(request.Path, _projectRoot);
if (validPath == null)
    return ErrorResponse("Invalid file path");
```

---

## Network Transport Safety

When building TCP/IPC listeners (local servers, service endpoints, inter-process
communication), transport-level configuration is a security concern separate from
message validation. See [ARCHITECTURE-PATTERNS.md](ARCHITECTURE-PATTERNS.md)
`## IPC/Message Contract Pattern` for message-level contracts; this section
covers the transport itself.

### Bind Address Rules

| Scenario | Bind Address | Rationale |
|----------|-------------|-----------|
| Local-only IPC / dev server | `127.0.0.1` or `::1` | Only accepts connections from the same machine |
| Service exposed to LAN/internet | `0.0.0.0` or `::` | Accepts connections from any interface |

**The rule:** Local-only services **must** bind to `127.0.0.1` (or the
platform's loopback address), never `0.0.0.0`. Binding to all interfaces
exposes the service to the network — even if "just for development."

```rust
// BAD: Exposes local IPC server to the entire network
let listener = TcpListener::bind("0.0.0.0:9500").await?;

// GOOD: Local-only service bound to loopback
let listener = TcpListener::bind("127.0.0.1:9500").await?;
```

### Connection Limits

Every listener must define a maximum concurrent connection count. Unbounded
accept loops allow a single misbehaving client (or deliberate flood) to exhaust
file descriptors or memory.

```rust
use tokio::sync::Semaphore;

const MAX_CONNECTIONS: usize = 64;
let semaphore = Arc::new(Semaphore::new(MAX_CONNECTIONS));

loop {
    let permit = semaphore.clone().acquire_owned().await?;
    let (stream, _addr) = listener.accept().await?;
    tokio::spawn(async move {
        handle_connection(stream).await;
        drop(permit); // Release on completion
    });
}
```

### Graceful Listener Shutdown

Listeners must support graceful shutdown: stop accepting new connections, allow
in-flight connections to drain within a timeout, then force-close remaining
connections. See [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md)
`### Graceful Shutdown of Spawned Services` for the async task mechanics.

```
Shutdown signal received
    │
    ├── Stop accepting new connections
    ├── Wait for in-flight connections (with timeout)
    │       ├── Connections complete normally
    │       └── Timeout expires → force-close remaining
    └── Release bound address
```

### Half-Open Connection Handling

A half-open connection occurs when one side has closed (or crashed) but the
other side's TCP stack has not yet detected it. These connections leak resources
indefinitely without intervention.

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| TCP keepalive | OS sends periodic probes on idle connections | Long-lived connections with idle periods |
| Application heartbeat | Protocol-level ping/pong messages | When you need faster detection than TCP keepalive |
| Read timeout | Close connections that send no data within a deadline | Request-response protocols |

**The rule:** Every listener must use at least one of these mechanisms. For
local IPC, a read timeout (e.g., 30–60 seconds of inactivity) is usually
sufficient.

---

## What NOT to Validate

Internal code that receives already-validated data should not re-validate.
Trust the boundary.

```csharp
// Called by handler AFTER validation
internal async Task ProcessFile(string validatedPath, string validatedName)
{
    // No need to re-validate — the handler already did it
    Directory.CreateDirectory(validatedPath);
}
```

**The rule:** Validate at the boundary. Trust internally. Never duplicate.
