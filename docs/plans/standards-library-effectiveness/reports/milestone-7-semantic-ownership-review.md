# Milestone 7 Semantic Ownership Review

Reviewed on 2026-09-05 against commit
`2cbe11e1b6372aac580d59b4fd06a24214ebbf35`. Canonical policy was read through
the live Standards Engine MCP interface using one accepted snapshot. Legacy
entrypoints, templates, prompts, historical tables, and current suite
declarations were inspected separately. The reviewer is the implementing
Codex agent; this is manual repository evidence, not an independent downstream
pilot or a policy-coverage attestation.

The D001–D010 review is complete as a findings-producing review. Milestone 7
is **not accepted**: canonical ownership is substantially separated, but some
retained legacy sources still prescribe behavior or route to obsolete anchors.
The earlier assertion that source consolidation was complete cannot establish
the current source-closure claim.

## Review Method And Limits

For each historical cluster, compare its concern with the current canonical
owner, its specializations, and the original competing entrypoints. Distinguish
a generic invariant from a mechanism specialization and from a copied rule.
Check whether the legacy reader can still encounter a competing instruction.
Use current owners rather than promoting the baseline's intended-owner column
to policy. For example, Contracts now owns runtime representation proof;
Security owns authorization and trust consequences.

An aligned result below means no competing owner was found for the named
concern in the inspected surfaces. It does not certify every policy paragraph,
all undeclared consumers, or the effectiveness of downstream use. Source
purity remains a separate gate even where repeated wording currently agrees.
No normative text, coverage certificate, or historical baseline was changed.

## Cluster Results

| Cluster | Current authority and preserved semantics | Review result |
| --- | --- | --- |
| D001: layering | [Architecture](../../../../topics/architecture.md#dependency-direction-and-services) owns concern placement and dependency direction; Core supplies the general ownership invariant; architecture patterns illustrate conditional arrangements. | Aligned for layering: Coding routes to the owner and the legacy Architecture section rejects universal layer counts. The Architecture entrypoint still needs the separate source-purity correction below. |
| D002: state | [Architecture](../../../../topics/architecture.md#data-and-state-authority) owns authoritative state; [Frontend](../../../../profiles/applications/frontend.md#projection-authority) specializes presentation, synchronization, and lifecycle. | Aligned: process or backend location does not determine authority, and optimistic projections require the selected reconciliation contract. |
| D003: validation | [Contracts](../../../../topics/contracts.md#runtime-decoding-at-boundaries) owns decoding and proof lifetime; [Security](../../../../topics/security.md#input-validation-authority) owns trust consequences; [Interop](../../../../profiles/boundaries/interop.md) specializes foreign validity, lifetime, and access. | Aligned for ownership: the inspected legacy Coding, Security, Architecture, and Interop validation sections route to these owners. Copying follows valid-access proof; it cannot repair an invalid source. Historical imperative Interop headings are source-purity review inputs, not alternate rules. |
| D004: README | [Documentation](../../../../workflows/documentation.md) selects documentation from impact; the [README template](../../../../templates/README-TEMPLATE.md) applies after boundary/contract README selection. | Aligned in inspected policy and template: no README-per-directory or directory-name trigger remains in the compared sections. Current documentation suites check metadata, not README prose or downstream traceability compliance. Their passing status cannot close that separate claim. |
| D005: slices and commits | [Planning](../../../../workflows/planning.md) owns lifecycle and admission; [Implementation](../../../../workflows/implementation.md) owns change execution; [Commit](../../../../workflows/commit.md) owns atomic commits and history. | Legacy Plan and Commit are routing indexes. Current tracked planning/implementation prompts refer to the owners but also repeat procedural instructions. No conflicting slice/commit instruction was identified; the original route-only prompt simplification is not achieved and remains part of A5. The baseline's description of ignored prompts is historical. |
| D006: evidence | [Verification](../../../../workflows/verification.md) owns evidence kind, environment, execution mode, and sufficiency; Tooling owns scheduling mechanisms; Launcher preserves delegated outcomes; Release owns shipped-artifact obligations. | Open: legacy Tooling prescribes scheduling defaults, and legacy Rust Bindings mandates a three-level test structure. Neither structure follows automatically from the canonical claims. See M7-OWN-01 and M7-OWN-02. |
| D007: Rust baseline | [Rust Tooling](../../../../profiles/languages/rust/tooling.md) owns Cargo adapters and practical starting guidance under Verification and Tooling; Rust API and Release own their narrower mechanisms. | Aligned across API, Tooling, and Release entrypoints: these are indexes, without copied baseline command lists. The ordinary Rust starting point is not a universal feature/target/workspace acceptance matrix. The legacy Bindings command and default-member advice remains open under D010. |
| D008: unsafe | [Rust Unsafe](../../../../profiles/languages/rust/unsafe.md) owns unsafe isolation, adjacent proof, caller contracts, module invariants, and feature-path evidence; [Rust Interop](../../../../profiles/languages/rust/interop.md) specializes checked dimensions and raw foreign access. | Aligned for unsafe ownership across the compared API, Unsafe, and Interop routes. Framework lifting is not C-ABI proof; the misleading representation example in legacy Bindings remains open under D010. |
| D009: generic versus Rust | Dependencies, Security, and Cross-Platform own their generic contracts; the corresponding Rust profiles express Cargo resolution, checked sizing/filesystem mechanisms, and target configuration. | Canonical ownership is aligned in the reviewed authority sections. Source navigation remains open: Rust Security points its panic-policy reader to a removed legacy Rust API heading. See M7-OWN-04. |
| D010: bindings | [Language Bindings](../../../../profiles/boundaries/language-bindings.md) owns mechanism and consumer-boundary contracts; [Rust Bindings](../../../../profiles/languages/rust/language-bindings.md) owns Rust adapters; Contracts owns compatibility; Release owns artifact composition; recipes are non-normative. | Open: the legacy Rust document still permits framework annotation in core, supplies an overgeneralized representation example, and mandates test topology/default-member advice. See M7-OWN-02. |

## Source-Closure Findings

Line references below identify the reviewed commit, not permanent anchors.
These findings are systemic: retained migration text is a second agent-facing
representation of canonical policy. A disclaimer does not make a contradictory
instruction a pure navigation index.

### M7-OWN-01: Tooling Retains Competing Defaults

`TOOLING-STANDARDS.md:6–10` claims ownership of automation, scheduling, and
reporting. Lines 36–46 say both that the hook table does not define default
stages and that these are scheduling defaults. Lines 59–62 prescribe parallel
checks, staged-file scope, and globs; lines 71–79 recommend staged validation
and pre-commit/pre-push placement.

The canonical Tooling workflow's Hook Selection, Scheduling And Cost, and
Persisted Artifact Checks sections select those mechanisms from actual inputs,
dependencies, concurrency safety, and claim requirements. Remove the competing
legacy prescriptions through Engine-owned authoring. Preserve useful examples
only in an explicitly conditional non-normative reference with an actual need;
do not copy every retired recommendation into a new document.

### M7-OWN-02: Rust Bindings Contradicts Its Canonical Adapter Boundary

`languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:99–116` permits direct core
annotation and illustrates feature-gated `uniffi::Record`. Canonical Rust
Bindings, Core And Adapter Boundary, places framework-owned derives in the
adapter and explicitly explains why a disabled-by-default core dependency still
couples the core when enabled.

Lines 66–96 label a particular flattened wrapper GOOD and generalize
representation safety without keeping framework lifting distinct from stable
ABI representation. Lines 287–314 prescribe three testing levels and excluding
foreign-runtime crates from `default-members`. Canonical Package And Workspace
Placement selects workspace membership from actual package/runtime contracts;
native and real-host evidence remains required for the selected binding claim.

The correction must cover this whole legacy entrypoint, not just the derive
example. Preserve checked conversion, framework-free core proof, real-host
evidence, and independently owned compatibility/artifact contracts in their
canonical owners; remove legacy commands and topology as alternate authority.

### M7-OWN-03: Other Entrypoints Are Not Pure Navigation

`LAUNCHER-STANDARDS.md:8–11` still claims remaining legacy authority, and lines
22–29 prescribe an `--install` output format. The canonical Launcher profile
delegates dependency procedures and selects interface/discovery from the actual
application contract; the old index cannot establish a universal command or
output format.

`ARCHITECTURE-PATTERNS.md:48–57` retains an independent contract-freeze
instruction in addition to extensive summaries of canonical decisions.
Agreement with an owner today does not meet the plan's link-without-restating
source-purity rule. Accessibility and Rust Async also retain migration-pending
language, and the Interop indexes retain imperative historical headings.
Review all 27 manifest entrypoints against the same navigation-only invariant;
do not use file length, disclaimer presence, or a keyword count as proof.

### M7-OWN-04: Rust Security Contains An Obsolete Anchor

`languages/rust/RUST-SECURITY-STANDARDS.md:41` routes to
`RUST-API-STANDARDS.md#result-option-panic`, but the target is now an index with
no such heading. Canonical Rust API owns Failure Expression Mechanisms, and
Rust Security owns Panic And Recoverable Error Boundary. Correct the route
with its owner-specific source correction and verify the actual destination.

The source-index suite's `source-links` membership selects only historical
corpus rows with `kind=standard` and `normative=derived`, plus separately named
route-coverage checks. It does not establish link correctness or source purity
for the full 27-source closure population. The current `markdown_links`
implementation resolves the path before `#` and checks existence; it does not
validate heading fragments. Even adding a source to that check would not by
itself detect this obsolete anchor.

### M7-OWN-05: Closure Must Distinguish Historical And Live Evidence

The [evaluation README](../../../../evaluation/standards-effectiveness/README.md)
freezes `corpus.tsv`, generated baseline metrics, and snapshots at their
historical boundary. The current plan's instruction to regenerate inventories
and eliminate normative legacy rows cannot be applied to those frozen facts.
The [Verifier README](../../../../tools/standards_verifier/README.md) also
explicitly retires historical migration and exact-prose gates.

Preserve frozen lineage; use the live canonical module corpus, Engine routing
projection, current registry, actual source contents, and manual semantic
review for present-tense claims. Supersede the old closure procedure where it
assumes mutable baseline classifications or retired checker authority.

## Inventory And Routing Evidence

A read-only comparison of `generated/section-inventory.tsv` with
`consolidation-dispositions.tsv` found 916 rows in each, no duplicate IDs,
no missing or extra IDs, and no source-path mismatch for any ID. Every named
target file exists; `none` is the explicit removal sentinel, not a file.
This proves bookkeeping correspondence, not the semantic correctness of every
historical disposition or current target anchor.

All 27 paths in `milestone-7-final-source-closure.tsv` exist. None is a member
of the current 70-module canonical corpus. The Engine snapshot exposes 54
registered routing rules targeting canonical IDs, with no legacy file target.
The current metadata checkpoint is the structural resolver evidence; neither
registered routing nor metadata membership makes legacy prose harmless to a
reader arriving through an old link.

## Corrective Slice And Acceptance

The next slice admits the Engine-owned legacy-index correction for the bounded
27-entrypoint population, using the existing canonical owners. First establish
the supported typed authoring operation and declared consumer impact; do not
translate this report into direct Markdown or repository-state mutation.
If a needed semantic edit is not expressible, record and admit the smallest
Engine capability change before source correction. Do not introduce a raw
file-write escape hatch.

The correction's acceptance claim is navigation-only behavior across the
bounded source population: no independently prescriptive policy, competing
example, applicability default, or stale route remains. Preserve required
inbound navigation and give each affected declared consumer a disposition.
Prefer deletion of repeated guidance and links to existing owners over new
policy or machinery. Any canonical meaning change requires an explicit
owner-specific proposal and review, not a silent index rewrite.

After correction, rerun the affected semantic review, validate destinations
across the complete selected population, and run the current structural
checkpoint. Do not resurrect retired exact-prose checks or use an automated
purity heuristic as semantic acceptance. Milestone 8, its pilots, migration
publication, and A5 prompt/concision review remain downstream of Milestone 7.

## Verification Of This Review Slice

The write set is this report, `issues.md`, `plan.md`, and
`execution-ledger.md` in the parent plan bundle, plus Engine-refreshed suite
inputs only if needed. Acceptance is a recorded manual ownership review and
current-state re-plan, supported by inventory reconciliation and the current
structural checkpoint. No implementation behavior changed, so implementation
unit tests are not an acceptance claim for this documentation slice.

The execution ledger records the final checkpoint result. A passing checkpoint
does not resolve M7-OWN-01 through M7-OWN-04 or accept Milestone 7.
