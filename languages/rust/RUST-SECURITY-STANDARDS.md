# Rust Security Standards

Rust-specific security rules for validation, resource limits, network listeners,
and panic-safe production paths. These specialize the generic
[Security Standards](../../SECURITY-STANDARDS.md).

## Path Validation

Canonical Rust filesystem authority and validation/use behavior moved to the
[Rust Security Profile](../../profiles/languages/rust/security.md#filesystem-authority-through-use).

Generic containment, creation, concurrent-mutation, and typed-failure policy
remains governed by [Security](../../topics/security.md#filesystem-containment).

## Checked Arithmetic At Boundaries

Checked conversion, arithmetic, resource limits, and typed rejection moved to
the
[Rust Security Profile](../../profiles/languages/rust/security.md#checked-boundary-sizing).

## Bounded Queues

Canonical external-input queue resource, overload, telemetry, ownership, and
evidence guidance moved to
[External-Input Queues](../../profiles/languages/rust/security.md#external-input-queues).

## Network Listener Limits

The canonical listener exposure and admission contract is
[Listener Admission And Lifecycle](../../profiles/languages/rust/security.md#listener-admission-and-lifecycle).
Connection work consumes the Rust Async contracts for
[owning spawned work](../../profiles/languages/rust/async.md#own-spawned-work)
and
[coordinated shutdown](../../profiles/languages/rust/async.md#coordinate-shutdown).

## Panic Policy

Production request paths, lifecycle code, background services, and network
handlers must not use `unwrap()` or `expect()` for recoverable errors. Follow
[RUST-API-STANDARDS.md](RUST-API-STANDARDS.md#unwrap-and-expect).
