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

Canonical listener exposure, admission, shutdown, and liveness policy moved to
the [Security topic](topics/security.md#network-transport-boundary).
Connection-work ownership and shutdown mechanics belong to
[Concurrency](topics/concurrency.md#own-work-failure-and-cancellation).
Message proof and dispatch remain with
[Contracts](topics/contracts.md#runtime-decoding-at-boundaries) and the
[IPC Boundary Profile](profiles/boundaries/ipc.md).

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
