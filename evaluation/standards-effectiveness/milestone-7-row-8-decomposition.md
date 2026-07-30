# Milestone 7 Row 8 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 8,
`STD-0782` through `STD-0789`. It is planning evidence, not normative policy.

The frozen Rust language-binding text combines generation authority, Rust
annotation placement, release procedure examples, and a structural build
heading. One Rust-specific rule would duplicate accepted Contracts and Release
authority while making a compiled-library generator, proc-macro annotations,
project command names, and example target languages appear universal.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0782`, `STD-0783` | Code-generation strategy and one annotated Rust source | Contracts owns the canonical generation authority, generator/input selection, deterministic derived outputs, and producer/consumer consistency. A compiled native library or annotated Rust source is not universally the authority. |
| `STD-0784` | Prefer proc-macro annotations over IDL/UDL files | Rust Language Binding owns annotation placement only as an adapter/core-boundary specialization. The selected mechanism and ownership facts choose annotations, separate authority files, or another declared input. |
| `STD-0785`-`STD-0788` | Build and per-language generation commands | Release owns selected artifact build/generation procedures, toolchain inputs, target coverage, and evidence. Product, package, binary, path, output, framework, and target-language example commands are not universal rules. |
| `STD-0789` | Build-system-organization heading | The heading is structural legacy navigation. Its remaining concrete child configuration identifiers have separate immutable ownership; the heading becomes a non-normative routing index only after the preceding children move. |

## Ordered Children

1. `STD-0782`, `STD-0783`: Contracts-owned generation authority and derived
   output consistency.
2. `STD-0784`: Rust Language Binding-owned annotation placement.
3. `STD-0785` through `STD-0788`: Release-owned build and generation
   procedures.
4. `STD-0789`: legacy-index closure for the structural heading.

## No Fallback

This decomposition does not retain a compiled-library, annotated-Rust,
proc-macro, framework, per-language command, package name, output path, or
host target as a generation default. Missing or contradictory authority,
toolchain, artifact, or evidence facts require typed diagnostics rather than
hand-maintained bindings, guessed commands, another generator, or default
success.

## Scope

This planning slice changes only the row-8 decomposition overlay, package
outcome/prerequisites, this report and checker, active-plan/ledger/evaluation
tracking, and superseded cursor assertions. It changes no normative or legacy
standard, disposition, router, metadata, generated inventory, configuration,
lockfile, or downstream repository.

## Next Slice

Milestone `7.4b8ac` performs bounded pre-slice review and implementation of
child `8.1`, `STD-0782` and `STD-0783`, in Contracts.
