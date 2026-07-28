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

Canonical path-containment policy moved to
[Security](topics/security.md#filesystem-containment). That topic owns
component boundaries, canonical identity, symlinks, non-existing targets,
validation/use races, and typed unresolved outcomes.

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

Canonical untrusted-input consequences moved to
[Security](topics/security.md#untrusted-structured-input). Runtime proof belongs
to [Contracts](topics/contracts.md#runtime-decoding-at-boundaries), and
action-specific message decoding belongs to the
[IPC Boundary Profile](profiles/boundaries/ipc.md).

---

## Network Transport Safety

When building TCP/IPC listeners (local servers, service endpoints, inter-process
communication), transport-level configuration is a security concern separate from
message validation. See the
[IPC Boundary Profile](profiles/boundaries/ipc.md) for message-level contracts;
this section covers the transport itself.

### Bind Address Rules

| Scenario | Bind Address | Rationale |
|----------|-------------|-----------|
| Local-only IPC / dev server | `127.0.0.1` or `::1` | Only accepts connections from the same machine |
| Service exposed to LAN/internet | `0.0.0.0` or `::` | Accepts connections from any interface |

**The rule:** Local-only services **must** bind to `127.0.0.1` (or the
platform's loopback address), never `0.0.0.0`. Binding to all interfaces
exposes the service to the network — even if "just for development."

Language-specific listener examples belong in the matching language standard.
For Rust, see
[languages/rust/RUST-SECURITY-STANDARDS.md](languages/rust/RUST-SECURITY-STANDARDS.md#network-listener-limits).

### Connection Limits

Every listener must define a maximum concurrent connection count. Unbounded
accept loops allow a single misbehaving client (or deliberate flood) to exhaust
file descriptors or memory.

Use the runtime's semaphore, bounded worker pool, or accept-loop backpressure
mechanism to enforce the limit. Rust-specific Tokio guidance lives in
[languages/rust/RUST-SECURITY-STANDARDS.md](languages/rust/RUST-SECURITY-STANDARDS.md#network-listener-limits).

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
