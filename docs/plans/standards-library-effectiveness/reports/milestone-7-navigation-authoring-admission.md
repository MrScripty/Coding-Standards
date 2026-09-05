# Milestone 7 Navigation Authoring Admission

## Decision And Evidence

Admit one Engine feature: an explicit proposal edit that replaces a registered
legacy entrypoint with Engine-rendered navigation to caller-selected canonical
standards. Then use that feature to correct the nine sources below. Retain the
other eighteen entrypoints and review all 27 for final source closure.

This admission follows the [semantic review](milestone-7-semantic-ownership-review.md)
and was checked against commit `19764768`. It changes no normative source and
does not accept Milestone 7. The next implementation slice must deliver the
complete discover/propose/analyze/review/apply path, not merely a renderer.

The live MCP contract contains fourteen edit variants. `revise-standard`
requires a registered canonical standard; none of the 27 legacy paths belongs
to the canonical module corpus. `related(TOOLING-STANDARDS.md)` returns
`NAVIGATION.UNKNOWN_POLICY` / `unavailable`. There is consequently no legitimate
legacy authoring handle to supply to an existing edit. Evidence maintenance
does not own standards text and is not an alternate publication path.

`related(workflow.tooling, outgoing, policy-impact)` returned no relationships
and an incomplete policy-unit mapping with reason `no-policy-units`. This is
not audited proof of no consumers. The new operation must expose its own exact
index change and review scope; it cannot manufacture a normative policy change
or silently accept an empty analysis.

## Bounded Source Correction

The retention population remains the 27 explicit paths in
`evaluation/standards-effectiveness/milestone-7-final-source-closure.tsv`.
That historical manifest establishes the admitted population only; its shape,
gate labels, and historical owner classifications are not new runtime policy.
Use a current Engine-owned navigation registration for the editable identities,
source locations, and their read/review scope. Keep it separate from the
normative module corpus and the frozen baseline.

| Source to replace | Required destination concerns |
| --- | --- |
| `INTEROP-STANDARDS.md` | Interop, IPC, Language Bindings, Contracts, Security |
| `ACCESSIBILITY-STANDARDS.md` | Accessibility and its non-normative recipes |
| `ARCHITECTURE-PATTERNS.md` | Architecture, Contracts, Frontend, Documentation, Concurrency, Persistence, Resilience, Diagnostics, Security, Verification, and the existing architecture reference |
| `TOOLING-STANDARDS.md` | Tooling, Verification, Commit, Documentation, Implementation, Dependencies, TypeScript, Frontend, and existing tooling/documentation/implementation recipes |
| `LAUNCHER-STANDARDS.md` | Launcher, Verification, Dependencies, Release, Security |
| `languages/rust/RUST-ASYNC-STANDARDS.md` | Rust Async and Concurrency |
| `languages/rust/RUST-INTEROP-STANDARDS.md` | Rust Interop, Rust Unsafe, Rust Language Bindings, generic Interop and Contracts |
| `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md` | Rust Language Bindings and Binding Lifecycle, generic Language Bindings and Interop, Rust Interop, Rust Cross-Platform, Rust Unsafe, Contracts, Release, Verification |
| `languages/rust/RUST-SECURITY-STANDARDS.md` | Rust Security, Rust API, Rust Async, generic Security and Contracts |

These are explicit semantic selections from the inspected source concerns and
canonical owners. Resolve them to current canonical IDs during proposal
construction. Do not have the Engine choose destinations from English,
similarity, old prose, or the manifest's single historical owner column.
Additional useful section-level navigation can be deferred: whole-standard
links satisfy this correction without copying rules or exposing slug creation.

The other eighteen sources retain their current navigation. In particular,
preserve the existing eight source-specific route-coverage inventories,
including their section destinations and the Plan template link. The feature
does not need arbitrary artifact or template editing for this correction.

## Consumer Dispositions

A read-only scan of tracked Markdown inline local links found six references
into the selected legacy population, all inside three files in the rewrite
set. This bounded lexical observation establishes link consumers only; it is
not a semantic-impact graph or proof about external bookmarks, plain-text
references, reference-style links, or undeclared consumers.

| Consumer at the reviewed commit | Observed destination | Disposition |
| --- | --- | --- |
| Tooling, line 139 | `FRONTEND-STANDARDS.md` | Replace with the canonical Frontend destination. |
| Rust Bindings, lines 5 and 7 | Rust Interop and Rust Cross-Platform legacy files | Replace with canonical profiles. |
| Rust Bindings, line 330 | `TESTING-STANDARDS.md` | Replace with Verification. |
| Rust Security, line 5 | `SECURITY-STANDARDS.md` | Replace with canonical Security. |
| Rust Security, line 41 | `RUST-API-STANDARDS.md#result-option-panic` | Replace with canonical Rust API; do not create an alias for a removed heading. |

Retained external entrypoint paths remain available under the existing
retention decision; do not promise every historical heading as a compatibility
contract. Frozen dispositions, corpus rows, snapshots, retired fixtures, and
historical reports keep their original evidence. Current source-index suites
retain their selected destination claims. Engine-generated suite inputs must
reflect the final current sources, without rewriting frozen classifications.

Before application, inspect declared relationships for every destination owner
and disposition any affected current consumer. A missing audited semantic
inventory remains explicit; navigation rewriting cannot issue coverage
attestations or certify the completeness of the library's policy graph.

## Public Operation And Engine Responsibilities

Add `rewrite-navigation-index` to the proposal edit algebra. Its inputs are an
opaque snapshot-bound registered entrypoint handle, a nonempty unique list of
canonical destination IDs, and a rationale. Change-set purpose evidence binds
the recorded source/owner review. No authored Markdown, path, URL, title, shell
command, SQL, or Git operation is an input to this edit.

Expose registered entrypoints through snapshot-bound discovery, using the
existing opaque authoring-target mechanism where its invariants fit. The
response must distinguish an editable navigation index from a canonical
standard or an arbitrary relationship consumer. Do not make all discovered
consumers writable. Keep ordinary `route` and compact `read` behavior unchanged.

The Engine owns source lookup, containment, captured bytes, canonical identity
resolution, title/link escaping, relative paths, deterministic rendering,
candidate change detection, and local publication. The output contains a fixed
non-normative index notice and links to the selected standards. It cannot
contain caller-supplied policy or executable examples. Reject unknown,
duplicate, stale, inapplicable, retired, or noncanonical selections.

Include the registration and source content in immutable snapshot capture and
replay. An index edit must produce explicit whole-index change/review evidence,
even when no normative policy unit changes. Review must bind the exact source,
destinations, candidate bytes, and actual evidence; new or changed selections
invalidate readiness through the existing immutable proposal lifecycle.
Application uses the existing exact-candidate verifier, local publication,
stale-state handling, and recovery continuation. It never goes through the
working-tree evidence-maintenance shortcut.

The first implementation must also define the typed behavior of old snapshots
that do not contain navigation registrations. Do not read current files into
an old snapshot or upgrade an old reviewed candidate implicitly. Advance only
the public/projection compatibility contracts whose accepted shape changes;
do not change unrelated handle or policy semantic revisions.

## Composed Design Review

| Architecture probe | Admitted result |
| --- | --- |
| Independent concerns | Navigation authoring owns selected links and rendered indexes. Canonical owners retain policy meaning; Analysis retains review decisions; repository Git retains candidate publication/recovery. |
| Required interleaving | Snapshot identity binds registration/source bytes; proposal identity binds destinations and rendered bytes; readiness binds evidence to that candidate. Rendering has no clock, current-worktree, or hidden latest-revision dependency. |
| Caller knowledge | One registered entrypoint handle, canonical destination IDs, rationale/evidence, and the existing workflow context. Callers do not learn paths, serializers, slug rules, or publication internals. |
| Representative changes | A destination change touches one index proposal and affected review evidence. A rendering fix touches the navigation compiler and its tests. A canonical owner move is resolved through its identity. A publication fix stays in the existing repository boundary. |
| Dependency shape | Pass captured content, canonical identities, exact change descriptors, and opaque contexts. Do not expose physical repository state or infer policy decisions from links. |
| Independent evolution/failure | Validate/render navigation independently; test the complete proposal path separately. Invalid selection rejects before publication; verification failure leaves the candidate unpublished; interrupted application retains existing recovery semantics. |
| Deletion test | Without registration, arbitrary files could become writable. Without rendering, serialization leaks to the caller. Without explicit review scope, index-only proposals can escape analysis. No second publication adapter, semantic search service, migration executor, or new generic workflow is justified. |
| Inherent complexity | Contain registration, capture, rendering, and change projection inside the Engine. Reuse existing schema generation, workflow handles, evidence provider, verification, and Git lifecycle. Add no automatic policy certification. |

## Implementation And Acceptance Boundary

The implementation owns the navigation registration/renderer inside
`tools/standards_engine`, its snapshot/discovery and logical-authoring
integration, canonical contract and generated tool projections, exact index
change analysis/review integration, and focused tests. Extend
`tools/standards_analysis` only where a distinct non-policy change descriptor
requires it; do not rewrite generic impact or coverage semantics to fit indexes.
Record the exact implementation file set before editing after resolving those
integration points. Update Engine documentation and the authoring skill with
the public edit, not a new transport procedure.

Required evidence covers a real registered legacy source through discovery,
proposal, exact preview, review, verification, and local application; invalid
or forged targets; attempts to target normative or arbitrary files; stale and
cross-snapshot handles; missing/retired destinations; deterministic frozen
replay; rejected/no-op requests; index-only review obligations; changed
candidate/readiness rejection; failed verification; and existing recovery.
Use observable behavior tests, not a frozen copy of rendered text as the only
oracle. Verify generated contract closure and the native/MCP projections.

Commit the accepted Engine capability before applying source corrections.
Then propose the nine index replacements, review actual candidate content and
consumer dispositions, apply through the Engine, and recheck all 27 sources.
Current structural verification is supporting evidence; manual ownership and
navigation review closes M7-OWN-01 through M7-OWN-04. A5 prompt simplification
and downstream pilots remain separately owned.

## Implementation Discovery: Declared Legacy Destinations

The implementation scan of all 73 registered structural suites found four
checks that require obsolete legacy destinations: three Tooling checks require
`FRONTEND-STANDARDS.md`, and the Rust Binding contract check requires legacy
Testing, Rust Cross-Platform, and Rust Interop destinations. These are current
consumers in addition to the eight source-specific inventories considered above.

Extend the admitted edit with optional explicit `retargets` dispositions. Each
pairs a snapshot-bound registered legacy entrypoint handle with a selected
canonical standard. The Engine replaces only matching required destinations in
checks for the edited index; it preserves every other assertion and rejects
unused, duplicated, or stale dispositions. Capture those declarations in the
snapshot and bind their exact content into index review evidence. This realizes
the already reviewed consumer replacements without disabling enforcement.

The implementation file set comprises the Engine navigation catalog and module;
Engine snapshot, authoring, rendering, and MCP integration; Analysis change,
kernel, and obligation integration; the canonical schema/interface/examples and
generated Python/tool projections; focused navigation and rendering tests and
MCP contract-count fixtures; contract documentation and the skill's authoring
reference. Generated verification inputs are refreshed through the Engine.
