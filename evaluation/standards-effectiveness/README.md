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

## Accelerated Milestone 7 Execution

`milestone-7-accelerated-execution-replan.md` preserves the immutable
execution train while classifying its 43 pending rows into 39 owner-, outcome-,
and train-coherent packages. `milestone-7-accelerated-packages.tsv` freezes
risk, owner action, verification family, parallel-draft eligibility,
integration gate, semantic outcome, and prerequisites.

`verify-milestone-7-accelerated-execution-replan.sh` proves exact pending-row
coverage, package cohesion, missing-owner state, immutable-train alignment,
active-plan handoff, and plan lifecycle. Shared integration remains serial,
and complete-suite checkpoints remain fail-fast.

`check-decision-table.sh` is the reusable semantic-fixture engine. A package
supplies an ordered schema, decisions with expected outcomes, and observed
outcomes derived by its own domain logic. The engine validates exact headers,
finite domains, unique cases, exact observed coverage, and outcome equality.
`verify-decision-table-engine.sh` covers valid input plus duplicate schema,
invalid wildcard, invalid domain, duplicate case, mismatch, missing case,
extra case, and unavailable-input failures.

`milestone-7-row-5-decomposition.md` splits immutable row 5 into Rust
core/adapter testability, generic boundary-mechanism selection, Contracts-owned
evolution, and Rust contract-discovery adaptation. Its checker proves exact
ordered overlay coverage, ordered child dispositions, package handoff, and
active cursor integrity.

`milestone-7-row-6-decomposition.md` splits immutable row 6 into
Cross-Platform native artifact loading, Release-owned artifact identity and
installation information, and Verification-owned platform evidence
scheduling. Its checker proves exact ordered overlay coverage, zero premature
dispositions, existing owners, package handoff, and active cursor integrity.

`milestone-7-row-7-decomposition.md` splits immutable row 7 into Rust binding
workspace/evidence, Release-owned binding artifact composition,
Contracts-owned artifact compatibility, and generic Language Binding-owned
surface governance. Its checker proves exact ordered overlay coverage, zero
premature dispositions, existing owners, package prerequisite correction, and
active cursor integrity.

`milestone-7-row-8-decomposition.md` splits immutable row 8 into Contracts
generation authority, Rust annotation placement, Release build/generation
procedures, and a legacy-index closure. Its checker proves exact ordered
coverage, zero premature dispositions, package prerequisites, and active
cursor integrity.

`milestone-7-row-13-decomposition.md` splits immutable row 13 into C# Async,
Rust routing, TypeScript Async, and Godot framework children. Its checker
proves exact ordered coverage, zero premature dispositions, three missing
owner contracts, package handoff, no-fallback evidence, and active cursor
integrity.

`milestone-7-row-14-decomposition.md` splits immutable row 14 into Launcher,
Verification, Dependencies, Release, and Security children. Its checker proves
exact coverage of all 26 identifiers, owner states, package classification,
zero premature dispositions, no-fallback findings, and the next bounded child.

`milestone-7-row-15-decomposition.md` splits immutable row 15 into 15
owner-coherent coding-policy children and records five missing owner contracts.

`fixtures/csharp/async-owner-contract-decisions.tsv` and
`verify-csharp-async-owner-contract.sh` establish the C# Async profile before
population. They select continuation scheduling from explicit affinity and
capability facts while rejecting blanket context suppression, blocking,
alternate dispatch, missing evidence, and default success.

`fixtures/dependencies/population-decisions.tsv` and
`verify-dependencies-population.sh` prove the Launcher dependency-installation
migration. They cover independently identified requirements, satisfaction
evidence, explicit mutation authority, selected procedures, post-mutation
verification, owner-selected grouped transactions, and rejection of fixed
function, numeric-success, monolithic-result, implicit-install, and
successful-no-op fallbacks.

`fixtures/release/build-procedure-decisions.tsv` and
`verify-release-build-procedure.sh` prove artifact-plan-derived build
procedure selection and reject fixed modes, guessed targets, implicit builds,
development substitution, and successful no-op fallback.

`fixtures/security/generated-command-decisions.tsv` and
`verify-generated-command-security.sh` prove operation validation,
destination-grammar encoding, argument preservation, negative evidence, and
typed rejection of raw, evaluated, cross-grammar, partial, alternate, and
default generated commands.

`fixtures/typescript/async-owner-contract-decisions.tsv` and
`verify-typescript-async-owner-contract.sh` establish the TypeScript Async
profile before population. They require scoped current-invocation authority
and explicit terminal classification while rejecting process-global counters,
stale mutation, discarded completion, ignored cancellation, alternate
mechanisms, missing evidence, and default success.

`fixtures/godot/owner-contract-decisions.tsv` and
`verify-godot-owner-contract.sh` establish the Godot framework profile before
population. They require explicit engine affinity, observed dispatch, and
point-of-use object-lifetime proof while rejecting off-thread access,
detached deferred work, check-then-use gaps, stale references, alternate
dispatch, missing evidence, and default success.

`fixtures/launcher/owner-contract-decisions.tsv` and
`verify-launcher-owner-contract.sh` establish the Launcher application profile
before row-14 population. They require declared action capability, exact
procedure delegation, process lifecycle, and outcome preservation while
rejecting guessed actions or targets, alternate commands, successful no-ops,
missing evidence, and default success.

`fixtures/launcher/population-decisions.tsv` and
`verify-launcher-population.sh` validate canonical Launcher population,
13 action, lifecycle, state, mechanism, and outcome decisions, 18 exact
dispositions, bounded legacy replacement, and handoff to GUI smoke acceptance.

`fixtures/verification/gui-smoke-decisions.tsv` and
`verify-gui-smoke-evidence.sh` validate GUI smoke claim, environment, mode,
capability, lifecycle, and assertion decisions, exact `STD-0495` refinement,
legacy removal, and handoff to the Dependencies owner contract.

`fixtures/dependencies/owner-contract-decisions.tsv` and
`verify-dependencies-owner-contract.sh` establish the Dependencies topic before
population. They validate 19 requirement, ownership, candidate, resolution,
authorization, evidence, and no-fallback decisions plus routing, metadata,
owner-state, and zero premature dispositions.

`fixtures/rust/binding-core-adapter-testability-*.tsv` and
`verify-rust-binding-core-adapter-testability.sh` require distinct
framework-free core and real native/host adapter evidence. They reject
framework-coupled core behavior, missing or failed evidence, native-only
adapter claims, NIF-only architecture, skipped core checks, alternate
frameworks, and default success with typed outcomes.

`fixtures/rust/binding-workspace-evidence-*.tsv` and
`verify-rust-binding-workspace-evidence.sh` select shared or separate Rust
package placement while preserving core-to-adapter dependency direction and
required native/host evidence. They reject missing or contradictory package
facts, reversed dependencies, required-evidence exclusion, native-only or
alternate-framework substitution, and default success with typed outcomes.

`fixtures/language-bindings/mechanism-selection-*.tsv` and
`verify-language-binding-mechanism-selection.sh` select in-process framework,
serialized, stable-ABI, or opaque-handle mechanisms, or a separately governed
IPC boundary, from complete boundary facts. They reject topology and lifecycle
contradictions, unavailable evidence, target-count and host-label defaults,
UI-technology defaults, alternate mechanisms, process substitution, and
default success.

`fixtures/language-bindings/surface-contract-*.tsv` and
`verify-language-binding-surface-contract.sh` select exported operations,
host-language subsets, semantic ownership, support, documentation,
compatibility, and evidence from declared consumer and product contracts.
They reject automatic exports, fixed support tiers, forced parity,
wrapper-owned domain semantics, native-only evidence, and default success.

`fixtures/contracts/binding-evolution-*.tsv` and
`verify-binding-contract-evolution.sh` classify binding artifacts by applicable
contract class, regenerate only affected generated outputs, and derive version
relationships from deployment and consumer facts. They reject assumed
additive compatibility, regenerate-all and skip-regeneration paths, forced
lockstep or independent versions (including lockstep inferred from shared
build provenance), compatibility shims, incomplete evidence, and default
success.

`fixtures/contracts/binding-generation-authority-*.tsv` and
`verify-binding-generation-authority.sh` select canonical binding-generation
authority from declared contract facts and require deterministic derivation
plus producer/consumer consistency evidence. They reject compiled artifacts,
source annotations, generated consumer outputs, alternate generators,
hand-maintained bindings, and default success as authority or recovery paths.

`fixtures/rust/binding-annotation-placement-decisions.tsv` and
`verify-rust-binding-annotation-placement.sh` select Rust annotation placement
from the declared mechanism and core-adapter ownership. They reject coupled
core annotations plus proc-macro or separate-definition defaults.

`fixtures/release/binding-generation-procedure-decisions.tsv` and
`verify-release-binding-generation-procedure.sh` derive binding generation
procedures from accepted release artifact plans. They reject fixed commands,
compiled-artifact defaults, alternate generators, and missing toolchain or
evidence facts.

`verify-rust-binding-index-closure.sh` verifies that the former Rust build
system heading is only a non-normative routing index and that its separately
owned child references remain explicit.

`fixtures/rust/security-panic-boundary-decisions.tsv` and
`verify-rust-security-panic-boundary.sh` specialize recoverable-error and
panic handling for Rust security-sensitive production boundaries. They reject
recoverable panics, missing invariant proof, and fallback recovery.

`fixtures/resilience/owner-contract-decisions.tsv` and
`verify-resilience-owner-contract.sh` establish the Resilience owner contract
for dependency criticality, degradation, retry, startup recovery, and typed
diagnostics. They reject unbounded retry, ignored required failures, default
success, and fallback recovery while the remaining resilience identifiers are
populated.

`fixtures/resilience/recovery-policy-decisions.tsv` and
`verify-resilience-recovery-policy.sh` populate that owner with required and
best-effort behavior, startup readiness, bounded retry, explicit degradation,
derived-state reconstruction, and typed outcomes. They prove seven exact
dispositions and reject destructive rebuild, defaults, stale or cached reads,
partial results, alternate backends, and silent continuation.

`fixtures/rust/binding-contract-discovery-*.tsv` and
`verify-rust-binding-contract-discovery.sh` adapt only a Contracts-selected
identity, version, or capability mechanism. They reject universal version
exports, package-version substitution, alternate or stale discovery, guessed
compatibility, missing evidence, and default success.

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

## Network Transport Decision Fixtures

`fixtures/security/network-transport-decisions.tsv` and
`verify-network-transport-policy.sh` check service/deployment-selected
exposure, listener-owned admission before acceptance, tracked connection
outcomes, ordered shutdown, termination authority, and protocol-selected
liveness. They prove exact disposition of `STD-0596` through `STD-0600`,
resolve `F016`, and reject universal address, capacity, timeout, liveness,
accept-first, detached-work, unsafe-termination, and alternate-mechanism
fallback.

## Platform Target Decision Fixtures

`fixtures/cross-platform/platform-target-decisions.tsv` and
`verify-platform-target-policy.sh` check declared target support, cohesive
platform isolation, contract-selected mechanism and layout, semantic fidelity,
typed invalid/unsupported/unavailable outcomes, exact disposition of
`STD-0280` through `STD-0288`, bounded legacy replacement, and rejection of
fixed-target, universal-pattern, stub, alternate-mechanism, and weaker-evidence
fallback.

`fixtures/cross-platform/native-artifact-loading-*.tsv` and
`verify-native-artifact-loading.sh` select linking, loading, package/OS
resolution, supplied-handle, or embedded-resource mechanisms from declared
artifact and deployment contracts. They prove two exact dispositions and
reject mandatory Strategy, guessed names, ambient discovery, alternate
loaders/artifacts, embedded copies, and default success with typed outcomes.

`fixtures/release/native-artifact-*.tsv` and
`verify-native-artifact-release.sh` derive native identity and consumer
information from release and channel facts. They prove two exact dispositions
and reject OS filename tables, class-local installation prose, ambient package
identity, alternate artifacts, and incomplete publication.

`fixtures/release/binding-artifact-composition-*.tsv` and
`verify-binding-artifact-composition.sh` classify native implementation,
internal adapter/generator, generated host, and bundled roles before deriving
the shipped binding artifact set. They reject missing roles, identities,
relationships, consumer information, or evidence plus fixed artifact counts,
package/bundle defaults, framework names, example names, internal-input
publication, and default success.

`fixtures/verification/platform-evidence-*.tsv` and
`verify-platform-evidence-coverage.sh` require complete evidence for declared
target claims and project-selected scheduling. They prove two exact
dispositions and reject fixed targets, current-platform substitution, weakened
support, provider matrices, fixed triggers/fail-fast behavior, and default
success.

## IPC Payload Decision Fixtures

`fixtures/ipc/action-payload-decisions.tsv` and
`verify-ipc-payload-validation.sh` check complete envelope and category/action
selection, action-specific payload and metadata proof, extra-field policy,
validated-variant dispatch, typed invalid/unsupported/unavailable outcomes,
11 exact frozen-ID dispositions, metadata and routing, legacy links, and removal
of unchecked message and payload assertions.

`fixtures/language-bindings/serialized-wire-decisions.tsv` and
`verify-language-binding-wire-representation.sh` check canonical schema and
serializer selection, complete tagged-enum/variant/field shape derivation,
consumer agreement, directional evidence, typed
invalid/unsupported/unavailable outcomes, three exact dispositions, and
bounded legacy replacement. They reject inferred casing/tagging, schema-free
or default shapes, omitted unsupported variants, alternate serializers, and
producer-only evidence.

`verify-interop-applicability-index.sh` proves the exact `STD-0482` index
disposition and requires the legacy Interop applicability section to route by
boundary fact to Interop, IPC, Language Bindings, Contracts, and Security. It
rejects active rules, code, examples-as-policy, prescriptive defaults, fallback
guidance, and stale concern summaries in the non-normative index.

`fixtures/rust/binding-error-mapping-decisions.tsv` and
`verify-rust-binding-error-mapping.sh` check selected host error contracts,
stable typed categories, cancellation preservation, bounded non-sensitive
context, checked mapping, real native/host evidence, two exact dispositions,
and bounded legacy replacement. They reject universal string flattening,
infallible conversion claims, generic catch-all errors, named-framework
defaults, dropped semantics, sensitive context, and default success.

`fixtures/rust/binding-event-delivery-decisions.tsv` and
`verify-rust-binding-event-delivery.sh` check contract-selected push, pull, and
stream delivery, provider authority, governed capacity and overflow, ordering,
callback thread and current-input lifetime, cancellation, shutdown, real
native/host evidence, two exact dispositions, and bounded legacy replacement.
They reject push/pull substitution, unbounded buffering, silent discard,
lock-unsafe or wrong-thread callbacks, prior-event carry-forward, alternate
runtimes, detached work, and default success.

`fixtures/rust/binding-callback-task-decisions.tsv` and
`verify-rust-binding-callback-task.sh` check selected task representation,
callback authority, checked input/output, response correlation, fresh
invocation state, scoped or lifecycle-owned async completion, cancellation,
typed outcomes, real native/host evidence, one exact disposition, and bounded
legacy replacement. They reject no-op executors, polling substitution,
alternate runtimes, detached work, input carry-forward, default output, and
default success.

`fixtures/rust/binding-enum-representation-decisions.tsv` and
`verify-rust-binding-enum-representation.sh` check mechanism-specific enum
contracts for framework lifting, serialized wire data, stable C ABI, opaque
handles, and generated wrappers; complete variants, discriminants, payloads,
unknown values, checked conversion, real native/host evidence, one exact
disposition, and bounded legacy replacement. They reject native-layout,
implicit-name/number, unknown-sentinel, omitted-variant, alternate-mechanism,
unchecked-conversion, and default-success fallbacks.

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

## Rust Binding Runtime Decision Fixtures

`fixtures/rust/binding-runtime-decisions.tsv` and
`verify-rust-binding-runtime.sh` distinguish host-handle lifetime from
composition-owned runtime and task lifecycle. They check shared runtime reuse
with fresh per-call state, persistence hints without ownership transfer,
scoped or lifecycle-tracked work, typed unavailable outcomes, exact
dispositions, bounded legacy replacement, no alternate-runtime or synchronous-
drive fallback, and F025 closure.

## Rust Binding Executor-Delegation Decision Fixtures

`fixtures/rust/binding-executor-delegation-decisions.tsv` and
`verify-rust-binding-executor-delegation.sh` distinguish successful local
completion, exact typed unsupported delegation, preserved terminal failures,
and unavailable delegate capability. They check current-call input ownership,
scoped or lifecycle-tracked work, exact disposition, bounded legacy
replacement, and rejection of catch-all, retry, carry-forward, default-input,
alternate-executor, and detached-work fallback.

## Rust Wire-Representation Decision Fixtures

`fixtures/rust/wire-representation-decisions.tsv` and
`verify-rust-wire-representation.sh` require a selected schema and serializer,
complete attribute-derived wire shape, consumer agreement, typed outcomes, and
native/host evidence for Rust serialized bindings. They prove the exact
`STD-0757` disposition, preserve unrelated legacy Rust Interop sections, and
reject schema-free JSON, native layout, assumed shape defaults, unknown
sentinels, omitted variants, alternate serializers or bindings, unsupported
generation claims, and producer-only or weaker evidence.

## Rust Filesystem-Authority Decision Fixtures

`fixtures/rust/filesystem-authority-decisions.tsv` and
`verify-rust-filesystem-authority.sh` check that Rust operations preserve
validated filesystem authority through existing-object use and creation. They
distinguish excluded, concurrent, and unknown mutation; held, handle-relative,
revalidated, plain, and unavailable authority; typed outcomes; exact
disposition; bounded legacy replacement; and rejection of weaker-path
fallback.

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
language-specific mechanisms. It also verifies the exact `STD-0269` C# async
parent-index disposition while preserving separately owned language
specialization.

`milestone-7-rust-async-decomposition.md` and
`milestone-7-rust-async-slices.tsv` split the nine Rust Async identifiers into
four serial specialization slices after generic Concurrency. The focused
decomposition checker validates exact ownership, proposed dispositions,
dependency order, lifecycle progress, active-plan handoff, and the
planning-only boundary without moving normative guidance.

`milestone-7-f025-f026-decomposition.md` and
`milestone-7-f025-f026-slices.tsv` split ten dependent Rust Language Binding
and Rust Security identifiers into core/adapter, runtime adaptation, typed
delegation, filesystem-authority, and listener-lifecycle slices. The focused
checker validates exact ownership, dispositions, serial progress,
accepted-owner dependencies, active-plan handoff, and the planning-only
boundary without moving normative guidance.

`milestone-7-independent-trust-replan.md`,
`milestone-7-independent-trust-groups.tsv`, and
`milestone-7-independent-trust-next-slice.tsv` resume the independent
trust-boundary wave after the lifecycle bridge. The focused checker proves the
61-ID/six-proposed-owner frozen baseline, 59-ID current remainder after event
registration and wire-representation acceptance, owner existence, accepted
Contracts/Interop/Rust Language Binding dependencies, residual decomposition
status, and the historical corrected `STD-0757` proposal. The accepted
`7.4b7h` re-plan rejects a six-ID Security draft that still mixed Core,
Contracts, Security, implementation structure, and field-rule ownership.
Accepted `7.4b7i` establishes the bounded Rust wire-representation contract
and disposition. Accepted `7.4b7j` re-measures the remainder, records accepted
baseline IDs structurally, and selects only the Rust external-input queue
contract for `STD-0824`. Accepted `7.4b7k` establishes that contract with 18
focused decisions. Accepted `7.4b7l` re-measures the 58-ID trust remainder and
selects only `STD-0583` plus `STD-0601` for a Contracts-owned validation
proof-lifetime slice. Accepted `7.4b7m` establishes that contract with 16
focused decisions; `7.4b7n` next replans the 56-ID trust remainder.

`fixtures/contracts/validation-proof-lifetime-decisions.tsv` and
`verify-validation-proof-lifetime.sh` check retained validated
representations, smart constructors, proof invalidation, new applicable
boundaries, typed outcomes, exact dispositions, and bounded legacy
replacement. They reject original-input reuse, history flags, stale proof,
mutable aliases, implicit cross-boundary trust, permissive defaults, weaker
decoders, and redundant-decoding mandates.

`milestone-7-execution-train.tsv` and
`verify-milestone-7-execution-train.sh` replace routine planning/implementation
alternation for the 589-ID remainder. They prove exact one-time coverage across
47 source/owner clusters, owner-state honesty, final-closure isolation, five
dependency waves, five complete-suite checkpoints, and the active integration
cursor. The manifest is immutable: exact dispositions derive a contiguous
completed prefix and the first wholly remaining row, while partial cluster
completion is rejected. Manifest rows authorize pre-slice review; they do not
pre-approve final owners or dispositions.

`milestone-7-execution-decomposition.tsv` overlays ordered owner-coherent child
slices when pre-slice review rejects a mixed-role baseline row. The baseline
manifest remains immutable; the train checker requires exact child coverage,
whole-child dispositions, contiguous logical progress, honest owner state, and
an active plan cursor naming every noncontiguous child identifier. Children
may retain one canonical owner while separating independently testable
contracts, as in Rust binding error mapping, event delivery, and callback task
adaptation.

`fixtures/security/input-validation-authority-decisions.tsv` and
`verify-input-validation-authority.sh` check operation-specific validation
authority, complete-contract coverage, generated or conformance-proven
implementation equivalence,
typed invalid/unsupported/unavailable outcomes, exact dispositions, bounded
legacy replacement, and rejection of global-validator, fixed-rule, cast,
duplicate-inline, original-input, permissive-default, and weaker-validator
fallbacks.

`fixtures/contracts/cross-language-contract-decisions.tsv` and
`verify-cross-language-contract.sh` check contract-class selection, canonical
wire/schema authority, coordinated and independently deployed consumer
updates, contract-matched evidence, typed invalid/unsupported/unavailable
outcomes, four exact dispositions, and bounded legacy replacement. They reject
schema guessing, old-shape and dual-shape compatibility shims, permissive
defaults, ambiguous authority, incomplete updates, and missing evidence.

`fixtures/rust/external-input-queue-decisions.tsv` and
`verify-rust-external-input-queue.sh` check selected capacity, overload,
retention/eviction, telemetry, ownership, typed outcomes, exact disposition,
bounded legacy replacement, and Rust operation evidence. They reject fixed or
unbounded capacity, default overflow, silent discard, alternate runtime,
prior-input carry-forward, and weaker evidence.

`verify-interop-event-registration.sh` checks provider-governed registration
phases, delivery and local-work independence, current callback input,
conditional Concurrency ownership, in-flight delivery, provider-selected
repeated/concurrent unregistration outcomes, valid release/shutdown orders, and
phase-aware typed diagnostics. It proves exact disposition of `STD-0473` and
rejects destruction/finalizer/garbage-collection cleanup, stale registration,
silent callback dropping, wrong-thread retry, alternate events, detached work,
input carry-forward, assumed idempotence, universal ordering, and false cleanup
success.

`verify-rust-target-configuration.sh` checks declared Rust targets,
contract-selected `cfg`/build/feature/composition/dispatch mechanisms with
explicit basis/ownership/precedence, cohesive placement, claim-matched
evidence, profile metadata and routing, exact legacy replacement, and exact
disposition of `STD-0726` through `STD-0730`. It rejects fixed triples,
best-effort support, feature-as-target substitution, unjustified build
scripts, ambiguous combinations, universal layouts, numeric `cfg` thresholds,
named substitute tools, alternate targets, and weaker evidence.

`verify-rust-binding-architecture.sh` checks framework-independent Rust core
types and behavior, one-way adapter dependencies, adapter-scoped binding
features, generated-output ownership, framework-free core verification, and
typed capability failure. It proves exact disposition of `STD-0759`,
`STD-0760`, `STD-0790`, and `STD-0791` and rejects layer merging, skipped core
verification, hand-edited generated output, and alternate-framework fallback.

`verify-rust-async-boundary.sh` checks contract-driven Rust sync/async
selection, exact disposition of `STD-0717` and `STD-0718`, profile metadata and
routing, bounded legacy replacement, later-section preservation, and rejection
of caller-convenience, blanket-sync, runtime-creation, blocking, and detached-
work fallback.

`verify-rust-async-lifecycle.sh` checks composition-owned runtime capability,
tracked task/failure ownership, admission closure, drain completion, abort
authority, and idempotent shutdown. It proves exact disposition of `STD-0719`
through `STD-0721` and rejects global/alternate runtimes, detached tasks,
leaf-only logging, open admission, silent incomplete drains, and unauthorized
or interruption-unsafe force-abort fallback.

`verify-rust-listener-lifecycle.sh` checks service-contract exposure,
listener-owned admission capacity before acceptance, Rust Async lifecycle
registration, terminal outcome observation, and ordered shutdown. It proves
the exact disposition of `STD-0825`, preserves the canonical Rust Async owner,
and rejects broad binding, fixed default capacity, accept-first ordering,
detached or discarded work, leaf-only logging, open admission during shutdown,
unsafe force-abort, and alternate-runtime fallback.

`verify-rust-async-blocking-mutex.sh` checks equivalent async execution,
governed blocking isolation, capacity availability, guard behavior, invariant
preservation, and synchronization capability. It proves exact disposition of
`STD-0722` and `STD-0723` and rejects inline or guard-held blocking, unbounded
isolation, alternate executor/thread fallback, unsupported suspended guards,
split invariants, and universal mutex defaults.

`verify-rust-async-cancellation-observability.sh` checks future-polling versus
external-operation state, durable cancellation design, owned async cleanup,
terminal evidence ownership, and inspection proof. It proves exact disposition
of `STD-0724` and `STD-0725` and rejects assumed external cancellation,
unprotected durable work, destruction-only or detached async cleanup,
leaf/missing ownership, silent terminal outcomes, and tool-only evidence.

The Milestone `7.4b7f1` fail-fast audit found that
`verify-rust-binding-executor-delegation.sh` still required the temporary
partial `F026` status superseded by accepted Milestone `7.4b5f`. Accepted
verification-only slice `7.4b7f2` resolves `F050` by requiring the stable
resolved state without weakening executor-delegation behavior or disposition
evidence. Event-registration implementation may proceed after the restored
fail-fast complete suite.

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
