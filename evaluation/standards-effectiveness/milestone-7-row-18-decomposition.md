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
| `18.7` | `STD-0608`-`STD-0610`, `STD-0612`-`STD-0615` | Verification replaces suite labels and cross-layer hierarchies with claim-selected acceptance evidence. |
| `18.8` | `STD-0618`-`STD-0624` | Verification owns focused test design and selects structure, mocks, edge cases, and property-based techniques from the observable claim. |
| `18.9` | `STD-0603`-`STD-0607` | Verification owns repository-sensitive test placement, discovery, and naming decisions. |
| `18.10` | `STD-0625`-`STD-0631` | Verification owns coverage interpretation and durable evidence documentation without fixed targets or templates. |
| `18.11` | `STD-0632`-`STD-0634` | Verification owns test-data authority, identity, isolation, construction, and lifecycle. |
| `18.12` | `STD-0636`-`STD-0638`, `STD-0640` | Verification owns async completion and success, failure, and service-boundary evidence selection. |
| `18.13` | `STD-0645`-`STD-0652` | Verification owns supporting-gate classification and claim-directed diagnosis procedures. |
| `18.14` | `STD-0602`, `STD-0653` | Verification closes the legacy source as a non-normative index and rejects checklist completion as acceptance. |

## Ordered Implementation

Implement specialized owner contracts first so Verification can link to
accepted authority instead of copying it. Within Verification, establish
acceptance-path evidence and focused test design before organization,
coverage/documentation, test data, async/failure evidence, and supporting
diagnosis. Child `18.14` then replaces `TESTING-STANDARDS.md` with a pure
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

## Refined Verification Boundary

The eight Verification children share a canonical owner but not one semantic
decision or fixture family. Each child has one observable outcome and a bounded
legacy section. No child may delete undisposed text owned by a later child.
The final legacy-closure child requires exact disposition coverage for all 52
row-18 identifiers and accepted status for children `18.1` through `18.13`.

## Next Slice

Milestone `7.4b8ch` refines `STD-0636` through `STD-0638` and `STD-0640` into
Verification async completion and failure-boundary evidence.
