# Bounded Rust Parser Repair Routing Example

**Standards metadata**

- ID: `reference.routing.bounded-rust-repair`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: An optional example is useful for routing a one-module Rust parser repair in a reusable library.
- Does not apply when: The actual task has different applicability facts; route those facts independently.
- Requires: `router`
- Specializes: `none`
- Verification: Compare the example's explicit facts with Router selection and required closure.
- Canonical owner: `reference/routing/bounded-rust-repair.md`

This optional example illustrates the Router's contract and adds no requirements.

## Example Conditions

The task repairs one parser module in a Rust library. Its public contract,
persistence, user interface, dependencies, and release promises remain unchanged.
No outstanding proposal can become stale before integration. The repair also
leaves architecture, abstraction/terminology decisions, diagnostics, performance,
security and trust handling, unsafe/async mechanisms, target/filesystem behavior,
generated contracts, cross-language/process boundaries, framework mechanisms,
and advanced test-oracle design unchanged. No commit, build/release procedure,
tooling configuration, or durable design-documentation change is part of this
example. Ordinary focused regression evidence is adequate for the stated claim.

## Selected Guidance

The applicable reading path contains Core, Router, Implementation, Verification,
the Library application profile, and the Rust language profile.

The task's stated facts leave architecture patterns, release, frontend, launcher,
accessibility, cross-platform, interop, bindings, persistence, and concurrent
plan integration outside the selected route. If an investigation changes a
material fact, route the new fact and obtain its required guidance.

## Evidence And Work

A focused regression check observes the repaired parser result, with affected
Rust static/toolchain checks. Planning, Documentation, and Release are selected
when the corresponding complexity, durable-knowledge, or publication conditions
arise in the actual task.
