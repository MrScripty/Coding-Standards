# Milestone 7 Row 13 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 13,
`STD-0273` through `STD-0279`. It is planning evidence, not normative policy.

The frozen row places C# await-context behavior, a Rust routing section,
TypeScript stale-result handling, and Godot thread and object-lifetime
mechanisms under one provisional Concurrency owner. These concerns share
generic lifecycle invariants but do not share a specialization owner,
dependency set, semantic decision, or verification contract.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0273` | C# `ConfigureAwait(false)` rule and example | A C# Async profile owns await-context specialization. The generic Concurrency topic owns nonblocking execution and work lifecycle; library/service location alone cannot select context suppression. |
| `STD-0274` | Rust concurrency cross-reference | This is structural navigation, not policy. It becomes a non-normative route to the canonical Rust Async and Rust Security profiles. |
| `STD-0275`, `STD-0276` | TypeScript heading and request-counter stale-response recipe | A TypeScript Async profile owns the mechanism specialization. Current-invocation authority and terminal outcomes must not depend on an implicit global counter or silently discarded stale work. |
| `STD-0277`-`STD-0279` | Godot heading, main-thread dispatch, and object validity | A Godot framework profile owns engine-thread and object-lifetime mechanisms. `CallDeferred` and `IsInstanceValid` are available mechanisms, not universal proof or fallback. |

## Ordered Children

### Child 13.1: C# Async Owner And Population

1. Establish a non-empty `profiles/languages/csharp/async.md` owner contract
   with bounded applicability, exclusions, dependencies, precedence, typed
   outcomes, and focused routing evidence.
2. Refine and move `STD-0273` only after that owner exists.

### Child 13.2: Rust Routing Index

Close `STD-0274` as non-normative routing to the existing Rust Async and Rust
Security profiles. It introduces no alternate Rust concurrency authority.

### Child 13.3: TypeScript Async Owner And Population

1. Establish a non-empty `profiles/languages/typescript/async.md` owner
   contract.
2. Refine `STD-0276` around current-invocation authority, cancellation, and
   explicit terminal outcomes; close `STD-0275` as its legacy index.

### Child 13.4: Godot Framework Owner And Population

1. Establish a non-empty `profiles/frameworks/godot.md` owner contract.
2. Refine `STD-0278` and `STD-0279` around selected main-thread dispatch and
   object-lifetime proof; close `STD-0277` as its legacy index.

## No Fallback

This decomposition does not preserve context suppression, request counters,
silent stale-result discard, deferred calls, main-thread assumptions, or
validity checks as defaults. Missing or contradictory runtime, invocation,
dispatch, lifetime, cancellation, or evidence facts require typed diagnostics
rather than another mechanism, implicit continuation, or default success.

## Scope

This planning slice changes only the row-13 decomposition overlay, package
classification, this report and checker, plan/ledger/evaluation tracking, and
superseded cursor assertions. It changes no normative or legacy standard,
disposition, router, metadata, generated inventory, owner map, configuration,
lockfile, or downstream repository.

## Next Slice

Milestone `7.4b8am` establishes the C# Async owner contract. It does not
dispose or move `STD-0273`.
