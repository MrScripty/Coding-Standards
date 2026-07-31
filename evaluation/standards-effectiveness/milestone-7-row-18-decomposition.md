# Milestone 7 Row 18 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 18,
`STD-0602` through `STD-0653`. It is planning evidence, not normative policy.

The frozen row assigns the complete legacy Testing source to Verification, but
the source also contains concurrency, language-binding, resilience, contract,
frontend, and performance policy. Those concerns do not share one canonical
owner, dependency set, semantic decision, or verification contract.

## Ownership Findings

| Child | IDs | Canonical outcome |
| --- | --- | --- |
| `18.1` | `STD-0611`, `STD-0639` | Concurrency owns shared-state isolation and lifecycle semantics; Verification later selects evidence for those contracts. |
| `18.2` | `STD-0616` | Language Bindings owns native/host representation and lifecycle requirements; Verification owns claim selection. |
| `18.3` | `STD-0617` | Resilience owns replay, recovery, duplicate handling, and partial-failure outcomes. |
| `18.4` | `STD-0635` | Contracts owns persisted dynamic artifact agreement with the current producer and consumer. |
| `18.5` | `STD-0641` | Frontend owns component-specific interaction, accessibility, geometry, and lifecycle rules. |
| `18.6` | `STD-0642`-`STD-0644` | Performance owns workloads, metrics, budgets, environments, and benchmark evidence requirements. |
| `18.7` | All other row-18 IDs | Verification owns generic test design, acceptance claims, supporting checks, reporting, and final legacy-index closure while linking to specialized owners. |

## Ordered Implementation

Implement specialized owner contracts first so the final Verification package
can link to accepted authority instead of copying it. Child `18.7` then removes
the remaining legacy defaults and replaces `TESTING-STANDARDS.md` with a pure
non-normative index after every row-18 identifier has an exact disposition.

## No Fallback

The decomposition does not preserve suite labels as evidence, fixed local or CI
schedules, realistic-environment substitution, wrapper-only binding proof,
helper-only recovery proof, stale generated artifacts, fixed coverage or
runtime targets, universal mock hierarchies, universal edge-case lists,
checklist completion, weakened assertions, alternate environments, or default
success. Missing or contradictory contract, environment, workload, lifecycle,
consumer, or evidence facts require typed diagnostics.

## Scope

This planning slice changes only the row-18 decomposition overlay, this report
and checker, active plan, execution ledger, and superseded cursor assertions.
It changes no normative or legacy standard, disposition, generated artifact,
router, metadata, configuration, lockfile, or downstream repository.

## Next Slice

Milestone `7.4b8bv` refines `STD-0611` and `STD-0639` into the existing
Concurrency owner.
