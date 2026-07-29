# Security Standards

Input validation, path safety, and sanitization requirements.

## Core Principle: Validate Once, at the Boundary

Canonical validated-representation authority and invalidation behavior moved
to
[Validation Proof Lifetime](topics/contracts.md#validation-proof-lifetime).
Security continues to own when untrusted input requires proof and the
consequences of invalid input.

## Path Validation

Canonical path-containment policy moved to
[Security](topics/security.md#filesystem-containment). That topic owns
component boundaries, canonical identity, symlinks, non-existing targets,
validation/use races, and typed unresolved outcomes.

---

## Input Validation

Canonical untrusted-input validation authority moved to
[Input Validation Authority](topics/security.md#input-validation-authority).
That topic selects authority per operation contract, routes specialized
filesystem and IPC mechanisms, consumes Contracts proof semantics, and rejects
global-validator, fixed-rule, cast, duplicate-inline, and weaker-mechanism
fallbacks.

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

Consume an intact proof-bearing representation without redundant decoding.
Re-establish proof when the representation, invariant, contract, or applicable
boundary changes. See
[Validation Proof Lifetime](topics/contracts.md#validation-proof-lifetime).
