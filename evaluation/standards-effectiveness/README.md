# Standards Effectiveness Evaluation

This directory contains the reproducible baseline and neutral evaluation
fixtures for the standards-library effectiveness restructure.

## Baseline

The baseline is frozen at commit
`6b4df85f042898374e9d23d265f4ecd25b0a7ba7`, immediately after the
restructure plan was added and before normative standards changed.

`corpus.tsv` classifies every Markdown artifact by its current kind,
normative role, preliminary target role, preliminary disposition, and frozen
source.
`generate-baseline.sh` reads each artifact from the frozen commit and writes:

- `generated/file-metrics.tsv`: lines, headings, and strong imperative
  occurrences by file;
- `generated/section-inventory.tsv`: a stable identifier for every heading in
  normative or operationally derived guidance; and
- `generated/summary.tsv`: corpus totals used by the baseline report.

Run:

```bash
./evaluation/standards-effectiveness/generate-baseline.sh \
  /path/to/Coding-Standards
```

Generated metrics are factual inventory. `findings.md` owns semantic findings
such as duplication, conflicts, broad obligations, and ownership gaps.

The working tree contains ignored prompt files. Their contents are frozen under
`snapshots/prompts/` for baseline reproducibility only, with trailing whitespace
normalized. The snapshots are not canonical guidance; Milestone 1 must decide
whether prompts are versioned distribution artifacts or remain explicitly
local.

## Fixtures

`fixtures/scenarios.md` defines seven product-neutral tasks. Each scenario
declares expected routing, acceptance, exclusions, prohibited errors, and plan
artifacts. `baseline-scores.md` applies the fixed rubric to current guidance.

The same fixtures and rubric must be used after restructuring. A changed
fixture requires a recorded reason and before/after rescoring.

## Architecture Contract

- `information-architecture.md` owns roles, paths, routing, precedence, and
  migration decisions.
- `metadata-schema.md` defines canonical module metadata.
- `owner-map.tsv` and `owner-overrides.tsv` map the baseline corpus to proposed
  canonical owners.
- `generate-owner-map.sh` writes the complete 916-section owner proposal.
- `check-metadata.sh` and `verify-metadata-fixtures.sh` validate the metadata
  contract and its negative cases.

## Routed Vertical Slice

`verify-s1-routing.sh` checks the first complete routed path:

- S1 small local bug fix;
- Rust language profile;
- library application profile;
- Core, Router, implementation, and verification workflows; and
- explicit exclusion of unrelated standards.

The selected context is compared with the frozen baseline line count.

## Plan Lifecycle Fixtures

`check-plan-structure.sh` and `verify-plan-fixtures.sh` enforce deterministic
active-plan structure:

- current lifecycle state, phase, and exactly one next slice;
- plan-level acceptance status;
- separate ledger and issue artifacts;
- valid milestone states;
- no embedded execution diary; and
- no `Accepted` state while acceptance remains pending, partial, or blocked.

Human review still owns whether the named evidence semantically proves the
objective.

## Acceptance Claim Fixtures

`verify-acceptance-claims.sh` checks the seven fixed scenarios and focused
regressions against the canonical claim model:

- evidence kind, environment qualification, and execution mode are separate;
- every required claim must have matching observed evidence;
- simulated hardware evidence cannot satisfy required-real acceptance;
- startup smoke cannot substitute for a user workflow; and
- manual execution is not a higher evidence kind.

`verify-verification-ownership.sh` checks that Verification remains the single
acceptance owner while Testing, Tooling, Launcher, and Release retain only their
test-design, scheduling, command, and shipping responsibilities. It rejects the
legacy universal timing/CI taxonomy and smoke-as-feature substitution.

## Contract Decision Fixtures

`verify-contract-decisions.sh` checks coordinated replacement, persisted
migration, public versioning, independently deployed negotiation, generated
artifacts, derived-state rebuild, valid degradation, and typed unavailable,
invalid, or unsupported outcomes. It rejects replacement across independent or
authoritative-state boundaries and degradation without an authoritative,
semantically equivalent source.

`verify-contract-ownership.sh` checks that legacy architecture, coding,
interop, release, and binding guidance links to the canonical topic and does not
restore universal append-only evolution, mandatory coexistence, destructive
recovery, untyped cache/default fallback, blanket additive compatibility, or
catch-all executor delegation.

`fixtures/contracts/runtime-decoding-decisions.tsv` and
`verify-runtime-decoding-policy.sh` check when runtime decoding applies, what
constitutes complete proof, validated-value construction, typed invalid,
unsupported, and unavailable outcomes, exact frozen-ID dispositions, legacy
linkage, and removal of assertion/original-input fallback.

## IPC Payload Decision Fixtures

`fixtures/ipc/action-payload-decisions.tsv` and
`verify-ipc-payload-validation.sh` check complete envelope and category/action
selection, action-specific payload and metadata proof, extra-field policy,
validated-variant dispatch, typed invalid/unsupported/unavailable outcomes,
exact frozen-ID dispositions, metadata and routing, legacy links, and removal
of unchecked message and payload assertions.

## Interop Authority Decision Fixtures

`fixtures/interop/foreign-memory-decisions.tsv` and
`verify-interop-boundary-policy.sh` check foreign representation and allocation
authority, initialized extent, access, lifetime, thread, release, copy ordering,
typed invalid/unsupported/unavailable outcomes, exact dispositions, metadata,
routing, legacy links, and removal of copy-before-proof guidance.

## Language Binding Representation Fixtures

`fixtures/language-bindings/representation-decisions.tsv` and
`verify-language-binding-boundary.sh` distinguish framework lifting,
serialization, stable ABI values, opaque handles, and generated wrappers. They
check typed invalid/unsupported/unavailable outcomes, exact dispositions,
metadata, routing, link-only legacy replacement, and no representation
fallback.

## Rust Foreign-Memory Decision Fixtures

`fixtures/rust/foreign-memory-decisions.tsv` and
`verify-rust-interop-memory.sh` check checked conversion before arithmetic,
pointer/alignment/allocation/provenance proof, initialized extent, zero-length
rules, callback lifetime, copy ordering, typed failures, exact dispositions,
metadata, routing, and legacy unsafe-pattern removal.

## Rust Boundary-Arithmetic Decision Fixtures

`fixtures/rust/checked-boundary-arithmetic-decisions.tsv` and
`verify-rust-boundary-arithmetic.sh` check conversion before arithmetic,
operation-wide checked arithmetic, separate resource limits, zero contracts,
typed rejection, no-fallback behavior, exact disposition, metadata, routing,
and legacy unchecked-example removal.

## Rust Unsafe-Contract Decision Fixtures

`fixtures/rust/unsafe-contract-decisions.tsv` and
`verify-rust-unsafe-contracts.sh` distinguish adjacent operation proof, caller
contracts, module invariants, wrapper claims, mechanism-selected evidence, and
feature-path execution. They also check exact dispositions, metadata, routing,
legacy replacement, no-fallback behavior, and F023 closure.

## Rust Binding-Conversion Decision Fixtures

`fixtures/rust/binding-conversion-decisions.tsv` and
`verify-rust-binding-conversions.sh` distinguish framework lifting,
serialization, opaque handles, and stable C-ABI values. They check fallible
conversion, real native/host evidence, exact dispositions, routing, legacy
unsafe-pattern removal, no-fallback precedence, and F022 closure.

## Filesystem Containment Fixtures

`fixtures/security/path-containment-decisions.tsv` and
`verify-filesystem-containment-policy.sh` check component-aware containment,
canonical filesystem identity, symlink escape, anchored creation, race control,
typed unresolved outcomes, exact frozen-ID dispositions, metadata, routing,
legacy links, and removal of lexical string-prefix containment examples.

## Documentation Decision Fixtures

`verify-documentation-decisions.sh` checks that durable documentation is
selected from changed responsibilities, invariants, contracts, decisions, and
operational procedures rather than directory or file changes. It distinguishes
no-documentation, boundary README, contract README, ADR, and runbook profiles
and rejects the removed universal per-directory rule.

`verify-decision-traceability.sh` runs the distributed checker in isolated Git
repositories. It proves staged mode reads the index, range mode reads the
explicit base/head commits, mapped decision-bearing changes require their exact
artifact, unstaged work is excluded from staged mode, and an unrelated ADR
cannot satisfy another boundary. Prior/current map union cases ensure removing
a row cannot hide a deleted or relocated trigger.

## Commit Authority Fixtures

`verify-commit-authority.sh` separates per-commit staged review from full
branch-history review and history-maintenance authority. It permits rewriting
only for an explicitly authorized, unshared, recoverable range, distinguishes
linear and merge topology, and rejects the removed mandatory cleanup policy.

## Consolidation Dispositions

`consolidation-dispositions.tsv` records the final owner and disposition of
every frozen section identifier as roles are migrated.

`milestone-7-decomposition.md`, `milestone-7-waves.tsv`, and
`milestone-7-first-slice.tsv` define the rolling owner-and-correctness sequence
for the remaining consolidation. `verify-milestone-7-decomposition.sh` checks
the remaining inventory totals, complete wave ownership, missing-owner count,
and exact first-slice proposal without treating later proposed dispositions as
accepted.

`milestone-7-f018-decomposition.md` and
`milestone-7-f018-slices.tsv` split critical untrusted-payload finding `F018`
into a generic runtime-decoding contract followed by action-specific IPC
decoding and Security linkage. `verify-milestone-7-f018-decomposition.sh`
checks the exact fourteen identifiers, owners, dispositions, ordering, named
fixtures, and active-plan handoff without moving normative guidance.

`milestone-7-f022-f023-decomposition.md` and
`milestone-7-f022-f023-slices.tsv` split critical foreign-memory, unsafe-
contract, ABI-classification, and conversion findings `F022` and `F023` into
six serial generic and Rust-specialized slices.
`verify-milestone-7-f022-f023-decomposition.sh` checks the exact 34
identifiers, owners, dispositions, ordering, named fixtures, and active-plan
handoff without moving normative guidance.

`milestone-7-trust-lifecycle-replan.md`,
`milestone-7-trust-lifecycle-groups.tsv`, and
`milestone-7-trust-lifecycle-next-slice.tsv` replace the premature final-
closure handoff after the critical trust-boundary slices. The focused checker
proves the 90-ID trust remainder, the 26-ID lifecycle bridge, owner
availability, dependency order, and the exact generic Concurrency next slice
without changing normative guidance or final dispositions.

`verify-concurrency-policy.sh` checks generic shared-state, lock-boundary,
nonblocking async, failure-observation, and cancellation-ownership decisions.
It proves exact disposition of `STD-0263` through `STD-0268` and `STD-0270`
through `STD-0272`, validates canonical metadata and routing, preserves only
unmoved language-specific migration material, and rejects unprotected
mutation, callbacks under locks, fire-and-forget work, synchronous async
fallback, discarded failure, ignored cancellation, and universal
language-specific mechanisms.

`milestone-7-rust-async-decomposition.md` and
`milestone-7-rust-async-slices.tsv` split the nine Rust Async identifiers into
four serial specialization slices after generic Concurrency. The focused
decomposition checker validates exact ownership, proposed dispositions,
dependency order, lifecycle progress, active-plan handoff, and the
planning-only boundary without moving normative guidance.

`verify-consolidation-dispositions.sh` proves complete, unique coverage for all
68 `COMMIT-STANDARDS.md` identifiers, validates target owners, and ensures the
legacy path is only a bounded migration index.

`verify-documentation-reference.sh` proves exact disposition of frozen
documentation identifiers `STD-0376` through `STD-0399`, validates the
non-normative reference owner, and rejects restoration of the removed blanket
API, TODO, table-alignment, and algorithm-template rules.

`verify-documentation-policy-consolidation.sh` proves exact disposition of
directory/README, ADR, and project-entry identifiers, validates the workflow
and derived boundary template, and rejects restoration of universal directory,
fixed-section, placeholder, and per-change README obligations.

`verify-release-workflow-foundation.sh` checks release and changelog
applicability decisions, exact disposition of `STD-0531` through `STD-0540`,
canonical workflow metadata and routing, and the optional-reference boundary.

`verify-release-reference-closure.sh` checks exact disposition of `STD-0541`
and `STD-0542`, validates the non-normative release-recipe owner and workflow
route, and rejects normative or executable guidance in the legacy release
index.

`verify-documentation-changelog-closure.sh` checks exact disposition of
`STD-0421` through `STD-0436`, canonical release ownership of retained
changelog semantics, removal of fixed-format boilerplate, and the bounded
legacy documentation migration index.

`verify-release-artifact-policy.sh` checks artifact, SBOM, checksum, and
lockfile decisions, exact disposition of `STD-0543` through `STD-0551`,
canonical artifact and reproducibility ownership, and dependent legacy sections
for conflicting defaults.

`verify-release-pipeline-policy.sh` checks authenticated publication handoff
decisions, exact disposition of `STD-0552` through `STD-0560`, canonical
pipeline ownership, required-artifact failure behavior, and removal of
provider-specific trigger and matrix recipes.

`verify-release-maintenance-policy.sh` checks maintenance and channel decision
contracts, exact disposition of `STD-0561` through `STD-0565`, supported-line
reconciliation, typed unresolved outcomes, and removal of branch, duration,
channel-name, and feature-flag defaults.

`verify-release-publication-policy.sh` checks provider-neutral publication
decisions, exact disposition of `STD-0566` through `STD-0574`, release-note and
artifact presentation, typed unresolved outcomes, and removal of hosted-service
and product-specific download defaults.

`verify-release-procedure-policy.sh` checks router-driven profile selection,
exact disposition of `STD-0575` through `STD-0576`, decision-derived release
steps, typed unresolved outcomes, and removal of universal language, commit,
tag, audit-tool, and publication-command defaults.

`verify-release-recovery-policy.sh` checks impact- and capability-driven
recovery decisions, exact disposition of `STD-0577` through `STD-0581`,
explicit emergency authority, immutable publication behavior, typed unresolved
outcomes, and removal of provider, registry, branch, patch-version, and
universal incident-record defaults.

## Scoring

Each rubric dimension is scored:

- `0`: missing, contradictory, or requires an incorrect outcome;
- `1`: partially covered, ambiguous, duplicated, or disproportionate;
- `2`: clear, sufficient, proportionate, and owned.

Reducing document size cannot compensate for a lower correctness score.
