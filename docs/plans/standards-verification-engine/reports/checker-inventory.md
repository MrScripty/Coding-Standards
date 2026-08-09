# Checker Structure Inventory

## Authority And Limits

`evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
is generated structural evidence. It records every current `verify-*.sh`
entrypoint, line count, exact inbound references by executable, contract, and
documentation class, named verifier/helper dependencies, and use of `sed`,
AWK, `rg`, and the legacy decision-table helper.

The generator does not infer canonical owner, semantic risk, migration
disposition, or package cohesion. Those are review decisions owned by this
plan. A documentation reference does not create an execution dependency, while
an executable or frozen contract reference must be migrated or updated before
the named checker can be deleted.

## Baseline Results

- 274 current Bash verifier entrypoints;
- 77 with no named verifier or helper dependency;
- 47 using `sed`;
- 249 using AWK;
- 264 using `rg`; and
- 13 using the legacy decision-table helper.

The exact per-checker values are kept in the generated TSV rather than copied
into this report. `generate_inventory.py --check` is blocking in the generic
launcher, so checker additions, removals, reference changes, dependency changes,
or measured mechanism changes require explicit regeneration and review.

## First Reviewed Package

Package `M2-P1` is accepted and replaced these eight Rust Tooling leaf checkers:

| Suite | Replaced checker | Decision fixture | Exact ID |
| --- | --- | --- | --- |
| `rust-tooling-adapter-inventory` | `verify-rust-tooling-adapter-inventory.sh` | `tooling-adapter-inventory-decisions.tsv` | `STD-0840` |
| `rust-tooling-baseline-commands` | `verify-rust-tooling-baseline-commands.sh` | `tooling-baseline-command-decisions.tsv` | `STD-0832` |
| `rust-tooling-build-script` | `verify-rust-tooling-build-script.sh` | `tooling-build-script-decisions.tsv` | `STD-0841` |
| `rust-tooling-compile-fail` | `verify-rust-tooling-compile-fail.sh` | `tooling-compile-fail-decisions.tsv` | `STD-0837` |
| `rust-tooling-feature-matrix` | `verify-rust-tooling-feature-matrix.sh` | `tooling-feature-matrix-decisions.tsv` | `STD-0836` |
| `rust-tooling-property-test` | `verify-rust-tooling-property-test.sh` | `tooling-property-test-decisions.tsv` | `STD-0838` |
| `rust-tooling-test-runner` | `verify-rust-tooling-test-runner.sh` | `tooling-test-runner-decisions.tsv` | `STD-0835` |
| `rust-tooling-workspace-lints` | `verify-rust-tooling-workspace-lints.sh` | `tooling-workspace-lint-decisions.tsv` | `STD-0833` |

### Cohesion Decision

- Canonical owner: `profile.language.rust.tooling`, with selected generic owner
  prerequisites preserved in each suite's fixture and required text.
- Observable package outcome: selected Rust tooling mechanisms remain adapters
  to accepted owner decisions and cannot create generic policy or named-tool,
  layout, command, harness, feature, lint, or build defaults.
- Risk: `consolidation`; accepted semantics and fixtures do not change.
- Dependencies: none of the eight scripts invokes a verifier/helper, and no
  executable or frozen contract references its path before this report.
- Assertion family: ordered decision outcomes, required canonical profile and
  non-normative reference text, prohibited former-source default, and one exact
  disposition row per suite.
- Write owner: one package author may edit only the eight suite TOMLs, registry
  rows, eight deleted scripts, regenerated structural inventory, and child plan
  records. Engine source and shared historical manifests remain read-only.
- Gate: direct execution of all eight suite IDs, generic launcher, removed-path
  and stale-inventory checks, plan/diff integrity, and one complete mixed suite.

Acceptance reduced current Bash verifier entrypoints from 274 to 266. The one
generic launcher evaluated nine registered suites and 45 checks in one Python
process. All 266 mixed entrypoints passed after removal.

## Next Classification Work

Package `M2-P2` is accepted as five Rust Release leaf checkers:

| Suite | Replaced checker | Decision fixture | Exact IDs |
| --- | --- | --- | --- |
| `rust-release-automation-adapter` | `verify-rust-release-automation-adapter.sh` | `release-automation-adapter-decisions.tsv` | `STD-0818`, `STD-0819` |
| `rust-release-package-metadata` | `verify-rust-release-package-metadata.sh` | `release-package-metadata-decisions.tsv` | `STD-0813` |
| `rust-release-publication-control` | `verify-rust-release-publication-control.sh` | `release-publication-control-decisions.tsv` | `STD-0814` |
| `rust-release-toolchain` | `verify-rust-release-toolchain.sh` | `release-toolchain-decisions.tsv` | `STD-0811`, `STD-0812` |
| `rust-release-workspace-package-metadata` | `verify-rust-release-workspace-package-metadata.sh` | `release-workspace-package-metadata-decisions.tsv` | `STD-0815`, `STD-0816`, `STD-0817` |

### M2-P2 Cohesion Decision

- Canonical owner: `profile.language.rust.release`.
- Observable package outcome: accepted Release, Contracts, Dependencies, and
  Tooling decisions remain authoritative while Rust Release selects only
  supported Cargo and toolchain mechanisms; former named-tool, metadata,
  publication, workspace, pinning, and lockfile defaults remain prohibited.
- Risk: `consolidation`; the 78 accepted fixture outcomes and standards text do
  not change.
- Dependencies: none of the five scripts invokes a verifier/helper or has an
  executable or frozen-contract inbound path reference. The automation checker
  has one documentation reference in this report, which this package updates.
- Assertion family: existing ordered predicates, required/prohibited text, and
  exact disposition-row prefixes. No engine source change is authorized.
- Exclusions: `verify-rust-release-evidence.sh` is frozen by
  `milestone-7-source-package-preparation.tsv`;
  `verify-rust-release-owner-contract.sh` is frozen by both row-35 contracts
  and invokes `check-metadata.sh`. They remain for Milestone 3.
- Write owner: one package author may edit only the five suite TOMLs, registry
  rows, five deleted scripts, generated inventory, and child plan records.
- Gate: 13 engine/inventory self-tests, direct execution of all registered
  suites, generic launcher, stale-inventory and removed-path scans, plan/diff
  integrity, and one complete mixed suite expected to contain 261 Bash
  entrypoints.

Acceptance preserved all 78 decision rows and nine dispositions without an
engine change. The generic launcher now evaluates 14 registered suites and 70
checks in one Python process. Generated inventory and the complete mixed suite
both report 261 remaining Bash entrypoints.

No script is scheduled for deletion solely because it is short, unreferenced,
or mechanically similar. Executable and frozen-contract references are resolved
in the accepting package; historical checker-identity contracts remain deferred
to Milestone 3's shared migration-contract replacement.

## Third Reviewed Package

Package `M2-P3` is accepted as five Tooling policy leaf checkers:

| Suite | Replaced checker | Decision fixture | Exact IDs |
| --- | --- | --- | --- |
| `tooling-ci-orchestration` | `verify-tooling-ci-orchestration.sh` | `tooling/ci-orchestration-decisions.tsv` | `STD-0687`, `STD-0689`, `STD-0690` |
| `tooling-debt-cost` | `verify-tooling-debt-cost.sh` | `tooling/debt-cost-decisions.tsv` | `STD-0691`, `STD-0692` |
| `tooling-editor-configuration` | `verify-tooling-editor-configuration.sh` | `tooling/editor-configuration-decisions.tsv` | `STD-0666`, `STD-0673` |
| `tooling-formatting-policy` | `verify-tooling-formatting-policy.sh` | `tooling/formatting-policy-decisions.tsv` | `STD-0681`, `STD-0682`, `STD-0683`, `STD-0686` |
| `tooling-lint-policy` | `verify-tooling-lint-policy.sh` | `tooling/lint-policy-decisions.tsv` | `STD-0674`, `STD-0675` |

### M2-P3 Cohesion Decision

- Canonical owner: `workflow.tooling`.
- Observable package outcome: repository facts and upstream authority select
  editor, lint, formatting, CI, debt, and automation-cost orchestration without
  editor, product, provider, schedule, cache, mutation, or warning defaults.
- Risk: `consolidation`; the 60 accepted fixture outcomes, standards text, and
  dispositions do not change.
- Dependencies: all five scripts have zero executable and frozen-contract
  inbound references and no verifier/helper dependency.
- Assertion family: existing ordered predicates, required/prohibited text, and
  exact disposition-row prefixes. No engine source change is authorized.
- Exclusions: Tooling owner-contract and reference-recipe scripts remain frozen
  by row-35 contracts; CI workflow and setup reference scripts belong to the
  Tooling reference owner; TypeScript static analysis and Verification quality
  gates belong to different canonical owners.
- Write owner: one package author may edit only the five suite TOMLs, registry
  rows, five deleted scripts, generated inventory, and child plan records.
- Gate: 13 engine/inventory self-tests, direct execution of all registered
  suites, generic launcher, stale-inventory and removed-path scans, plan/diff
  integrity, and one complete mixed suite expected to contain 256 Bash
  entrypoints.

Acceptance preserved all 60 decision rows and 13 dispositions without an
engine change. The generic launcher now evaluates 19 registered suites and 93
checks in one Python process. Generated inventory and the complete mixed suite
both report 256 remaining Bash entrypoints.

The Rust API and Rust Dependency four-script candidates remain independent
future owner packages. They are not combined with `M2-P3` merely to enlarge the
batch.

## Fourth Reviewed Package

Package `M2-P4` is accepted as four Rust API leaf checkers:

| Suite | Replaced checker | Decision fixture | Exact IDs |
| --- | --- | --- | --- |
| `rust-api-boundaries` | `verify-rust-api-boundaries.sh` | `rust/api-boundary-decisions.tsv` | `STD-0709`, `STD-0710` |
| `rust-api-failures` | `verify-rust-api-failures.sh` | `rust/api-failure-decisions.tsv` | `STD-0711`, `STD-0712` |
| `rust-api-features` | `verify-rust-api-features.sh` | `rust/api-feature-decisions.tsv` | `STD-0715` |
| `rust-api-validation` | `verify-rust-api-validation.sh` | `rust/api-validation-decisions.tsv` | `STD-0707`, `STD-0708` |

### M2-P4 Cohesion Decision

- Canonical owner: `profile.language.rust.api`.
- Observable package outcome: generic Architecture, Contracts, Resilience,
  Dependencies, Library, Documentation, Verification, and Security decisions
  remain authoritative while Rust API selects only supported language
  mechanisms without layout, error, feature, trait, or proof defaults.
- Risk: `consolidation`; the 65 accepted fixture outcomes, standards text, and
  dispositions do not change.
- Dependencies: all four scripts have zero executable and frozen-contract
  inbound references and no verifier/helper dependency.
- Assertion family: existing ordered predicates, required/prohibited text, and
  exact disposition-row prefixes. No engine source change is authorized.
- Exclusions: the API owner contract has executable and row-35 inbound
  references and invokes shared metadata verification; the rustdoc checker is
  frozen by source-package preparation. Both remain for Milestone 3.
- Write owner: one package author may edit only the four suite TOMLs, registry
  rows, four deleted scripts, generated inventory, and child plan records.
- Gate: 13 engine/inventory self-tests, direct execution of all registered
  suites, generic launcher, stale-inventory and removed-path scans, plan/diff
  integrity, and one complete mixed suite expected to contain 252 Bash
  entrypoints.

Acceptance preserved all 65 decision rows and seven dispositions without an
engine change. The generic launcher now evaluates 23 registered suites and 109
checks in one Python process. Generated inventory and the complete mixed suite
both report 252 remaining Bash entrypoints.

The Rust Dependency four-script candidate remains an independent future owner
package.

## Fifth Reviewed Package

Package `M2-P5` is accepted as four Rust Dependency leaf
checkers:

| Suite | Replaced checker | Decision fixture | Exact IDs |
| --- | --- | --- | --- |
| `rust-dependency-audit-adapters` | `verify-rust-dependency-audit-adapters.sh` | `rust/dependency-audit-adapter-decisions.tsv` | `STD-0747`, `STD-0748` |
| `rust-dependency-feature-mechanisms` | `verify-rust-dependency-feature-mechanisms.sh` | `rust/dependency-feature-mechanism-decisions.tsv` | `STD-0738` through `STD-0740` |
| `rust-dependency-graph-inspection` | `verify-rust-dependency-graph-inspection.sh` | `rust/dependency-graph-inspection-decisions.tsv` | `STD-0741` through `STD-0746` |
| `rust-dependency-workspace-inheritance` | `verify-rust-dependency-workspace-inheritance.sh` | `rust/dependency-workspace-inheritance-decisions.tsv` | `STD-0735` through `STD-0737` |

### M2-P5 Cohesion Decision

- Canonical owner: `profile.language.rust.dependencies`.
- Observable package outcome: accepted dependency, consumer, resolver,
  ownership, Tooling, and evidence decisions select only supported Cargo
  mechanisms without feature, graph, workspace, audit-product, or schedule
  defaults; Rust API retains source-level feature expression.
- Risk: `consolidation`; 53 fixture outcomes, standards text, and 14 contiguous
  dispositions do not change.
- Dependencies: all four scripts have zero executable and frozen-contract
  inbound references and no verifier/helper dependency.
- Assertion family: existing ordered predicates, required/prohibited text, and
  exact disposition prefixes. No engine source change is authorized.
- Exclusions: adjacent owner and source-closure checkers remain coupled to
  executable, historical, or shared-helper contracts and stay in Milestone 3.
- Gate: 13 engine/inventory self-tests, all registered suites, generic launcher,
  inventory and removed-path scans, plan/diff integrity, and one complete mixed
  suite expected to contain 248 Bash entrypoints.

Acceptance preserved 53 decisions and 14 dispositions without an engine
change. The launcher now evaluates 27 suites and 130 checks; inventory and the
complete mixed suite report 248 Bash entrypoints.

## Sixth Reviewed Package

Package `M2-P6` is accepted as two dependency-free Tooling reference leaves:

| Suite | Replaced checker | Decision fixture | Exact IDs |
| --- | --- | --- | --- |
| `tool-setup-reference` | `verify-tool-setup-reference.sh` | `tooling/tool-setup-reference-decisions.tsv` | `STD-0701`, `STD-0702` |
| `tooling-ci-workflow-reference` | `verify-tooling-ci-workflow-reference.sh` | none | `STD-0693`, `STD-0694` |

Both share the non-normative Tooling reference owner, have zero executable and
contract inbound references and no helper/verifier dependencies, and fit
existing text/decision primitives. The gate expects inventory to fall to 246
and runs self-tests, all suites, launcher, removal/inventory/plan checks, and
the complete mixed suite.

Acceptance preserved ten decisions and four dispositions without an engine
change. The launcher evaluates 29 suites and 137 checks; inventory and the
complete mixed suite report 246 Bash entrypoints.

## Remaining Standalone Leaves

`M2-P7` accepted replacement of `verify-typescript-static-analysis.sh` under
`profile.language.typescript`: ten decisions and dispositions `STD-0677`
through `STD-0680`. `M2-P8` accepted replacement of
`verify-verification-quality-gates.sh`
under `workflow.verification`: eleven decisions and dispositions `STD-0688`
and `STD-0695`. Both have zero executable/contract inbound references and no
helper/verifier dependencies, and both fit existing text/decision primitives.
`M2-P7` preserved all ten decisions and four dispositions; inventory and the
complete mixed suite passed at 245 Bash entrypoints. `M2-P8` preserved all
eleven decisions and both dispositions; the launcher now evaluates 31 suites
and 146 checks, and inventory plus the complete mixed suite passed at 244 Bash
entrypoints.

They remain separate packages because they have different owners. The seven
dependency-free leaves now remaining are migration/acceptance infrastructure
plus the temporary launcher and require structural/shared-contract planning.

## First Structural Consumer

Package `M2-S1` accepted the reusable strict table family and replaced
`verify-dependency-audit-lineage.sh`. The suite preserves twelve decisions,
canonical/former-source text, exact dispositions `STD-0699` and `STD-0700`, and
accepted plan state. Nineteen engine tests and all 32 suites/151 checks pass;
inventory and the complete mixed suite report 243 Bash entrypoints.

The table family is justified beyond this package by measured recurring
structure: 219 remaining scripts use AWK, 198 validate row shape, 165 collect
projections, 83 count rows, and 58 declare expected projections. Cross-file
relations and acceptance claims remain separate shared contracts.

## Final Milestone 2 Policy Leaf

Package `M2-P9` accepted replacement of
`verify-implementation-change-evidence.sh` under `workflow.implementation`.
The suite preserves thirteen decisions, canonical and reference text, the exact
`STD-0698` split, and former-source prohibitions. All 33 suites/156 checks pass;
inventory and the complete mixed suite report 242 Bash entrypoints.

The next dependency-free consumer is the shared acceptance-claim contract;
migration-structure leaves remain assigned to relation and table packages.

## Acceptance Contract Consumer

Package `M3-C1` accepted the canonical acceptance-claim parser and satisfaction
check and replaced `verify-acceptance-claims.sh`. Its seven scenarios preserve
kind, environment, and mode separation without inferred hierarchy. The README
now names the focused Python suite command. All 34 suites/157 checks pass;
inventory and the complete mixed suite report 241 Bash entrypoints.

The remaining dependency-free migration consumers require cross-table lineage
and strict structural projections; the temporary launcher remains assigned to
final convention replacement.

## First Relation Consumer

Package `M3-S1` accepted strict ordered and duplicate-free set relations and
replaced `verify-milestone-7-f018-decomposition.sh`. The suite preserves the
exact fourteen-row map, inventory and final-disposition lineage, report
evidence, and accepted lifecycle while removing obsolete planned-state
compatibility. All 35 suites/162 checks pass; inventory and the complete mixed
suite report 240 Bash entrypoints.

The Row 19 decomposition and owner-validation pair is the final package in the
frozen structural-leaf sequence. The temporary launcher remains separate.

## Row 19 Package And New Boundary

Package `M3-S2` replaced both Row 19 structure scripts with one owner-coherent
suite preserving 18 children, 50 expanded IDs, strict execution and
owner-validation tables, selected split boundaries, report contracts, accepted
plan markers, and canonical owner files. All 36 suites/170 checks pass;
inventory and the complete mixed suite report 238 Bash entrypoints.

The graph now has one dependency-free entrypoint:
`verify-declarative-suites.sh`, the temporary launcher. The other 237 are
coupled. Of all 238 entries, 138 have executable inbound references, 72 have
frozen-contract references, 44 have both, 166 invoke verifiers, and 84 invoke
helpers. Another implementation package requires dependency-ordered graph
planning; deleting the launcher would violate the complete-suite transition.

## Coupled Graph Resolution

The accepted next mechanism is an exact typed dependency graph plus a reviewed
migration-package manifest. Generated graph evidence owns only repository
structure: verifier and helper nodes, executable and frozen-contract inbound
references, verifier and helper invocations, strongly connected components,
and condensation waves. It reports unresolved and ambiguous targets instead of
treating them as absent dependencies.

Semantic classification remains planning authority. Owner, risk, intended
outcome, write set, prerequisites, verification, and lifecycle are reviewed in
`checker-migration-packages.tsv`; none are inferred from graph shape or file
names. This preserves exact structural automation without allowing migration
mechanics to decide standards ownership.

Package authority identifies each reviewed unit by a stable typed checker or
source subject. Generated component ordinals and baseline commits are snapshot
evidence in this report, not durable package keys; deleting one checker may
renumber later components without changing any accepted package subject.

The admitted migration order is decision-table helpers, source-index and
traceability helpers, plan-structure helpers, metadata helpers, then verifier
hubs and frozen identity contracts in component order. Every package removes
its complete old authority and direct invocation edges. The launcher remains
until the complete-suite convention is replaced.

### Accepted Graph Evidence

`M3-G1` generated 243 resolved nodes: 238 verifiers and five helpers. The
1,045 typed edges comprise 388 verifier dependencies, 85 helper dependencies,
486 executable references, and 86 frozen-contract references. The 239
components span waves zero through ten.

Five helpers are acyclic wave-zero nodes. Direct dependency consumers are 13
for decision tables, 55 for metadata, 14 for plan structure, two for
source-index closure, and one for decision traceability. Executable-reference
counts remain separately visible and can exceed direct consumer counts.

Two verifier SCCs require later atomic package review:

- `component-0087` contains Language index closure and Row 45 decomposition.
- `component-0129` contains Row 46 decomposition, Rust adoption-notes
  retirement, Rust index closure, and Rust profile-authority closure.

Both SCCs are wave five and carry frozen row-35 consumer identity. No helper
participates in a cycle, so the selected helper-first train remains valid.

The path-shaped dependency rule corrected seven false dependency records caused
by quoted expected checker names. Those occurrences remain executable-reference
edges and therefore still block unreviewed deletion; they no longer distort the
runtime dependency graph or component waves.

### Decision Table Family Admission

The decision-table helper has 13 direct dependency consumers and 15 executable
references. Eleven consumers own policy behavior; one owns helper fixtures; one
owns the accelerated migration plan. They total 1,199 Bash lines and span
multiple canonical owners, so shared helper use is not package cohesion.

Five direct consumers are presently inbound-free and have no executable or
frozen-contract references: Binding Artifact Composition, Language Binding
Surface Contract, Native Artifact Loading, Platform Evidence Coverage, and Rust
Binding Contract Discovery. `M3-DT1` admits only Language Binding Surface
Contract (`component-0085`) because it is a bounded owner-coherent leaf.

The helper self-test has one direct caller but a 44-verifier transitive inbound
closure through Accelerated Execution. Binding evolution, generation authority,
mechanism selection, native release, core/adapter testability, and workspace
evidence also have unresolved inbound callers. They require later admitted
caller or frozen-identity packages before deletion. The helper remains until
all direct consumers and executable references are removed.

`M3-DT1` pre-implementation review also found a documentation-only reference in
the standards-effectiveness README. Documentation edges do not constrain graph
order, but they still require exact stale-authority reconciliation. The admitted
write set did not include that file, so implementation stopped and was restored
before source integration. Re-admission must either include the README or defer
the package; it cannot ignore the reference because it is absent from the typed
dependency graph.

The selected resolution re-admits `M3-DT1` with the README in its exact write
set and an explicit removed-path verification gate. This keeps documentation
projection, suite registration, obsolete-authority deletion, generated graph
updates, and package lifecycle in one owner-coherent integration outcome. The
package is again eligible for implementation; no compatibility entrypoint or
intermediate documentation authority is permitted.

## First Decision Consumer Migration

Accepted package `M3-DT1` replaces Language Binding Surface Contract with a
five-check declarative suite and retains only the canonical 19-row decisions
fixture. Its Bash checker, schema mirror, and observed-outcome mirror are
deleted; the README projects the suite instead of an executable entrypoint.

The current inventory is 237 Bash verifiers and five helpers. The generated
graph contains 242 nodes, 1,039 typed edges, and 238 components. The migration
therefore removed one verifier node, eight dependency/reference edges, and one
component while preserving strict typed decisions, four exact section IDs, four
exact dispositions, canonical profile evidence, and former-source closure.

### Next Decision Consumer

The remaining inbound-free direct consumers are Binding Artifact Composition
(`component-0024`, 75 lines), Native Artifact Loading (`component-0138`, 110
lines), Platform Evidence Coverage (`component-0151`, 66 lines), and Rust
Binding Contract Discovery (`component-0183`, 72 lines). All have zero inbound
dependency, executable-reference, and contract-reference counts before package
admission.

`M3-DT2` selects Rust Binding Contract Discovery. It has one Rust profile owner,
13 bounded decisions, one exact disposition, and one README reference. Platform
Evidence and Native Loading remain deferred to the Cross-Platform `F085`
source-shape package; Binding Artifact Composition remains the next ordinary
eligible candidate. This ordering uses semantic risk and prerequisites rather
than line count alone.

### Second Decision Consumer Migration

Accepted package `M3-DT2` replaces Rust Binding Contract Discovery with a
five-check declarative suite over its canonical 13-row decisions fixture. The
72-line Bash checker, schema mirror, and observed-outcome mirror are deleted;
the README projects the suite rather than an executable entrypoint.

The current inventory is 236 Bash verifiers and five helpers. The generated
graph contains 241 nodes, 1,031 typed edges, and 237 components. The migration
removed one verifier, ten dependency/reference edges, and one component while
preserving one exact disposition, canonical Rust profile and former-source
evidence, accepted plan lineage, and every typed outcome.

### Third Decision Consumer Admission

`M3-DT3` selects Binding Artifact Composition (`component-0024`). It remains
inbound-free and has one Release owner, 75 Bash lines, 23 decisions, four exact
dispositions, one accepted plan marker, and one README reference. Its decision
fixture remains canonical; schema and observed mirrors are obsolete package
authorities scheduled for deletion.

This is the final ordinary inbound-free decision consumer identified by the
current review. Cross-Platform candidates remain governed by `F085`; package
admission does not weaken or bypass that source-shape dependency.

### Third Decision Consumer Migration

Accepted package `M3-DT3` replaces Binding Artifact Composition with a
five-check declarative suite over its canonical 23-row decisions fixture. The
75-line Bash checker, schema mirror, and observed-outcome mirror are deleted;
the README projects the suite rather than an executable entrypoint.

The current inventory is 235 Bash verifiers and five helpers. The generated
graph contains 240 nodes, 1,023 typed edges, and 236 components. The migration
removed one verifier, ten dependency/reference edges, and one component while
preserving four exact dispositions, Release/former-source evidence, accepted
plan lineage, and all typed outcomes.

The next boundary is `F085`: remaining inbound-free consumers use legacy
Cross-Platform heading ranges, but their canonical behavior belongs to three
owners. Another ordinary package is not admissible until source-wide migration
evidence and its retirement owner are selected.

### Cross-Platform Source-Closure Train

Option 1 is selected. A temporary migration-owned whole-source contract will
first prove exact canonical routes and prohibited legacy defaults across the
entire `CROSS-PLATFORM-STANDARDS.md` index without section delimiters. It is a
closure prerequisite, not a policy owner, and is deleted with final source
closure.

The graph audit adds Rust Target Configuration to the initially identified four
checkers. Platform Target Policy has two live callers: inbound-free Native
Artifact Loading and Rust Target Configuration. Rust Target Configuration is
itself referenced by frozen README/source-preparation evidence but has no live
semantic caller other than those migration contracts. The safe owner train is
Native Loading, Native Release, Platform Evidence, Rust Target Configuration,
then Platform Target Policy. The first three are independently inbound-free;
both Native Loading and Rust Target Configuration must be replaced before
Platform Target Policy can be deleted.

Final source closure follows only after all five replacement suites are
accepted. That closure removes the transitional headings and the temporary
whole-source contract together, preserving exact routes, dispositions,
owner-local typed decisions, and source-wide prohibitions without a wrapper,
compatibility schema, source exception, or cross-owner semantic suite.

### Whole-Source Prerequisite Admission

`M5-CP0` is admitted as a safety-critical migration package with no graph
component because it replaces no semantic checker. Its implementation adds one
registered text-only suite that scans the complete legacy source for seven
canonical routes and the union of prohibited defaults currently distributed
across four heading-bounded scripts.

The package does not inspect headings and does not validate any canonical-owner
semantics, decisions, dispositions, or accepted migration markers. Those
remain with `M5-CP1` through `M5-CP5`. Its exact write set excludes the source
and every semantic checker, which makes source immutability an admission-to-
implementation verification condition rather than a convention.

### Whole-Source Prerequisite Implementation

Accepted `M5-CP0` adds one registered text-only suite with no suite
dependencies and no Bash replacement. It requires seven owner routes and
prohibits 24 defaults over the complete file. The generated Bash graph remains
235 verifiers, 240 nodes, 1,023 edges, and 236 components because the package
adds declarative migration evidence without retaining or adding an executable
checker.

The source and all semantic evidence remain unchanged. `M5-CP1` is now the
smallest useful owner package: Native Artifact Loading is inbound-free, owns
two exact Cross-Platform dispositions, and is the first live caller that must
leave Platform Target Policy before that downstream checker can retire.

### Cross-Platform Dependency-Semantics Trigger

Pre-admission review shows that graph direction alone is insufficient for the
next package. Native Artifact Loading and Rust Target Configuration both invoke
Platform Target Policy, but their scripts also invoke lifecycle and integration
checkers. The graph records executable coupling, not whether a callee is part
of the caller's permanent focused semantic contract.

The engine correctly rejects dependencies that are not registered suites.
Therefore a Bash bridge is unavailable by design. The next planning decision
must classify each nested call as either an owner-required semantic
precondition, which becomes a declarative dependency, or an independent
package/wave gate, which must not remain nested. This classification is needed
before caller deletion; otherwise the migration either weakens evidence or
recreates legacy orchestration under a new schema.

### Cross-Platform Dependency Classification

Option 1 is accepted. Native Loading's target, capability, evidence, and typed
outcomes are explicit within its own decision fixture, so its invocation of the
broader same-owner Platform Target checker is an integration gate rather than
a missing semantic prerequisite. Row 6 and execution-train invocations are
migration gates; the decision-table helper is replaced by the engine. `M5-CP1`
therefore depends only on temporary `M5-CP0`.

Rust Target differs: `profile.language.rust.cross-platform` explicitly requires
and specializes `topic.cross-platform`. Its Platform Target invocation is a
true generic-to-specialization dependency. Platform Target's metadata,
filesystem-containment, and independent-trust calls are structural, adjacent-
owner, and migration gates for this bounded semantic package, not permanent
nested suite dependencies.

The resulting graph migration uses three independent packages followed by one
connected pair. `M5-CP4+5` creates separate generic and Rust suites, registers
Platform Target before Rust Target, declares the Rust dependency, and deletes
both Bash authorities atomically. This preserves owner boundaries and acyclic
once-only execution without reproducing the legacy process graph.

### Native Artifact Loading Admission

`M5-CP1` selects inbound-free `component-0137`: 110 Bash lines, 23 ordered
decisions, two exact dispositions, one Cross-Platform owner, one README
projection, and two redundant fixture mirrors. The retained decisions fixture
is canonical package input.

The admitted suite requires temporary `M5-CP0` and no Platform Target suite.
That dependency boundary follows VE016: Native Loading directly owns target,
capability, evidence, and typed outcomes, while its former nested Platform
Target, Row 6, and execution-train calls are integration or migration gates.
Implementation deletes the checker and mirrors atomically and regenerates the
graph; no wrapper or duplicate semantic authority is permitted.

### Native Artifact Loading Migration

Accepted `M5-CP1` replaces component `0137` with one five-check suite. The
suite retains the 23-row decisions fixture, depends once on temporary whole-
source coverage, and owns only Native Loading semantics. The Bash checker and
schema/observed mirrors are deleted; README now projects the suite.

The former Platform Target and migration-lifecycle invocations do not become
suite dependencies under VE016. Their removal eliminates accidental nested
execution without dropping Native Loading's direct target, capability,
evidence, typed-outcome, disposition, owner, or no-fallback evidence.

Acceptance verification passed all `42` declarative suites, `37` engine tests,
and all `234` remaining mixed checker entrypoints. The regenerated graph has
`239` nodes, `1,015` edges, and `235` components.

### Native Artifact Release Admission

`M5-CP2` selects current component `0137`: 61 Bash lines, 19 ordered decisions,
two exact dispositions, one Release owner, one README projection, and two
redundant fixture mirrors. The retained decisions fixture is canonical package
input.

The admitted suite requires temporary `M5-CP0` only. The former nested Release
Artifact Policy call covers separate `STD-0543` through `STD-0551`
SBOM/checksum/lockfile policy and remains an independently selected same-owner
integration gate. Row 6 and execution-train calls are migration gates. The
implementation must remove all nested execution without dropping Native
Release identity, consumer-information, evidence, typed-outcome, disposition,
owner, or no-fallback evidence.

Admission exposed that `component-0137` is also the historical ordinal recorded
for accepted M5-CP1. This is not a semantic overlap: deleting M5-CP1 renumbered
the generated graph. Component ordinals are snapshot evidence and cannot be the
manifest's unique package subject. M5-CP2 admission therefore uses a stable
reviewed identity and explicit admission graph regeneration.

The accepted recovery uses the stable subject
`checker:evaluation/standards-effectiveness/verify-native-artifact-release.sh`
for M5-CP2. Existing package rows use typed checker/source subjects while
retaining exact uniqueness. Admission-boundary graph regeneration is explicit;
no ordinal rewrite or graph exception is used.

M5-CP2 is admitted under that stable checker subject. Current
`component-0137` remains snapshot evidence and does not participate in package
uniqueness or ownership.

Admission verification passed all 42 declarative suites, 37 engine tests, and
all 234 mixed checker entrypoints. The admission graph contains 239 nodes,
1,017 edges, and 235 components.

### Native Artifact Release Migration

Accepted M5-CP2 replaces stable Native Artifact Release checker subject with
one five-check suite. The suite retains the 19-row decisions fixture, depends
once on temporary whole-source coverage, and owns only `STD-0296` and
`STD-0297` Native Release semantics. The Bash checker and schema/observed
mirrors are deleted; README projects the suite.

The broader Release Artifact Policy and migration-lifecycle invocations do not
become suite dependencies under VE017. Their removal eliminates nested
execution without dropping identity, consumer-information, evidence,
typed-outcome, disposition, owner, or no-fallback evidence.

Acceptance verification passed all 43 declarative suites, 37 engine tests, and
all 233 mixed checker entrypoints. The regenerated graph has 238 nodes, 1,007
edges, and 234 components.

### Platform Evidence Coverage Admission

`M5-CP3` selects current component `0148`: 66 Bash lines, 21 ordered decisions,
two exact dispositions, one Verification owner, one README projection, and two
redundant fixture mirrors. The retained decisions fixture is canonical package
input.

The admitted suite requires temporary M5-CP0 only. The former nested
Verification Ownership call checks the broader owner boundary and remains a
same-owner integration gate. Row 6 and execution-train calls are migration
gates, while the decision-table helper is replaced by engine mechanics. No
nested checker becomes a suite dependency.

Implementation must remove all nested execution without dropping support
contracts, target coverage, real-environment evidence, selected scheduling and
orchestration, typed outcomes, dispositions, canonical owner evidence, or
negative fallback coverage. The stable package subject is
`checker:evaluation/standards-effectiveness/verify-platform-evidence-coverage.sh`;
component `0148` remains snapshot evidence only.

Admission verification passed all 43 declarative suites, 37 engine tests, and
all 233 mixed checker entrypoints. The admission graph contains 238 nodes,
1,009 edges, and 234 components.

### Platform Evidence Coverage Migration

Accepted M5-CP3 replaces the stable Platform Evidence Coverage checker subject
with one five-check suite. The suite retains the 21-row decisions fixture,
depends once on temporary whole-source coverage, and owns only `STD-0298` and
`STD-0299` platform-evidence semantics. The Bash checker and schema/observed
mirrors are deleted; README projects the suite.

The broader Verification Ownership and migration-lifecycle invocations do not
become suite dependencies under VE019. Their removal eliminates nested
execution without dropping support contracts, complete target evidence,
real-environment proof, project-selected scheduling/orchestration, typed
outcomes, dispositions, owner evidence, or no-fallback coverage.

Acceptance verification passed all 44 declarative suites, 37 engine tests, and
all 232 mixed checker entrypoints. The regenerated graph has 237 nodes, 999
edges, and 233 components.

### M5-CP4+5 Verifier-Subject Conflict

Platform Target is current component `0148` with 139 Bash lines and 25
decisions. Rust Target is component `0202` with 169 Bash lines and 30
decisions. The Rust checker directly invokes Platform Target, confirming the
planned generic-to-specialization suite dependency and atomic deletion wave.

The Rust checker is also a live subject in three migration contracts. Root-
README dependency and consumer inventories require the path, while source-
package preparation assigns it as the exclusive writable verifier for Rust
Cross-Platform closure package `7.4c3.20`. These are not semantic Rust policy
dependencies, but they are accepted lifecycle authority. Deleting the path
without transferring that authority would invalidate source-closure ownership;
retaining it would create dual semantic authority.

The recommended recovery generalizes source-preparation identity to strict
typed `checker:` and `suite:` subjects, rewrites existing values atomically,
and transfers package 20 to the Rust Target suite in M5-CP4+5. Bash-only README
inventories then remove the retired checker and update exact counts. No source,
checker, fixture, registry, or canonical policy changes before selection.

Trigger verification passed all 44 declarative suites and all 232 mixed
checker entrypoints; the graph remains 237 nodes, 999 edges, and 233 components.

### Typed Source-Preparation Verifier Authority

Source preparation now identifies every exclusive verifier as either
`checker:<repository-path>` or `suite:<repository-path>`. The eight preparation
packages retain nine unique current checker paths, but path-only and unknown
subjects are invalid. Symlink paths are invalid. Subject and resolved-path
uniqueness prevent a checker and suite alias from claiming the same
preparation authority.

This shared contract creates the required transfer operation for M5-CP4+5:
package `7.4c3.20` can replace its Rust Target `checker:` subject with the
registered Rust Target `suite:` subject in the same atomic migration that
deletes the Bash checker. The Bash-only root-README inventories remain
unchanged until that migration and cannot treat suite subjects as Bash paths.

Focused source-preparation and aggregate source-closure checks passed, as did
all 44 declarative suites, 37 engine tests, Python compilation, graph freshness
at 232 Bash verifiers / 237 nodes / 999 edges / 233 components, both plan
checks, diff integrity, and all 232 mixed checker entrypoints.

### M5-CP4+5 Exact-Evidence Gap

The connected package remains two owner-bounded suites: Platform Target has 25
decisions and nine exact generic dispositions; Rust Target has 30 decisions and
five exact specialization dispositions. Platform requires temporary M5-CP0,
and Rust requires Platform. The audit classified metadata, filesystem
containment, independent-trust, and historical row checks as integration gates.

Deleting Rust Target requires one atomic typed-subject transfer, removal from
the 33-row Bash dependency and 34-row README-consumer inventories, exact
current-count updates in row 35 and row 46, and reduction of negative-purity
ownership to S1. These are lifecycle mechanics, not suite dependencies.

One semantic-preservation gap blocks admission. Rust Target uses `diff` to
require exact UTF-8 content for its seven-line non-normative migration index;
the engine text primitive cannot reject unrecognized extra prose. The smallest
preserving extension is a strict generic `exact_text` check with inline expected
content and raw-byte comparison. A generic source-index grammar is broader but
valid if multiple indexes are admitted together; deferral to source closure is
valid but delays the connected wave. Literal-only weakening, mirrors, wrappers,
opaque hashes, and partial migration are invalid.

Trigger verification passed both plan checks, all 44 declarative suites, graph
freshness at 232 Bash verifiers / 237 nodes / 999 edges / 233 components, diff
integrity, and all 232 mixed checker entrypoints.

### Accepted Exact-Text And Accelerated-Wave Direction

VE021 Option 1 is accepted. The shared engine provides one strict generic
`exact_text` assertion over a contained regular file and inline expected TOML
content encoded as UTF-8. Comparison is byte-for-byte with no newline,
whitespace, or encoding normalization. The assertion is mechanics only; the
suite remains the sole owner of expected policy evidence.

Focused identical-byte, mismatch-offset, missing-input, path-escape, and
unknown-field cases pass. All 42 engine tests, all 44 registered suites, Python
compilation with its cache redirected to `/tmp`, graph freshness, both plan
checks, diff integrity, and all 232 mixed entrypoints pass. M5-CP4+5 can now be
admitted without changing engine source in its package commit.

The post-M5 remainder will use dependency-closed owner waves. The current graph
has 69 inbound-free verifiers, including 13 Testing and eight Release leaves,
but inbound-free does not imply independently removable: the Testing leaves
invoke row-18 decomposition, and other branches retain callers of prospective
prerequisites. Package admission must therefore compute the exact closure that
prevents any remaining Bash verifier from calling a deleted path and prevents
any declarative suite from duplicating an unmigrated Bash prerequisite.

Two to four disjoint owner packages may be prepared concurrently in isolated
worktrees. Suites, fixtures, and deleted checker paths must not overlap. The
registry, package manifest, README, generated graph, and plan remain serial
integration-owner files. Each package keeps separate suite identity and
focused diagnostics; the complete suite runs once at the integrated wave gate.
Filename adjacency, one cross-owner suite, Bash bridges, compatibility
launchers, and duplicated prerequisite evidence are not valid acceleration.

### M5-CP4+5 Admission

The connected pair is admitted as two rows sharing one atomic implementation
write set. Manifest row 8 admits generic Platform Target (`M5-CP5`) before row
9 admits Rust Target (`M5-CP4`) because Rust specializes and depends on the
generic suite. Numeric package suffixes do not override semantic dependency
order.

Platform will require temporary M5-CP0; Rust will require Platform. The
implementation retains the 25-row and 30-row decision fixtures, canonical
owners, nine generic and five Rust dispositions, and the exact seven-line Rust
index. It deletes both Bash paths and reconciles the typed source-preparation
subject, Bash-only README inventories, negative-purity set, current count
validators, README projection, and generated graph in the same commit. Engine,
policy, fixture, legacy-index, and historical evidence changes are excluded.

The implementation is accepted. Focused Rust selection executes M5-CP0,
Platform, and Rust once and passes 17 checks. Both Bash checkers are absent;
source package 20 names the Rust suite; Bash-only dependency/consumer
inventories are 32/33; S1 is the only negative-purity consumer; and lifecycle
validators enforce those counts. All 46 declarative suites and 42 engine tests
pass. Final graph freshness reports 230 Bash verifiers / 235 nodes / 989 edges
/ 231 components, and all 230 mixed entrypoints pass.

Recovery verification passed all 42 declarative suites, 37 engine tests, and
all 234 mixed checker entrypoints. The fresh graph remains 239 nodes, 1,015
edges, and 235 components.

### M5-CP6 Source-Closure Admission

Cross-Platform is next at order 7 in the immutable final source manifest. Its
20 identifiers have exact dispositions, and the five former heading-dependent
semantic checkers now have accepted owner-local declarative replacements. The
remaining temporary M5-CP0 suite is migration structure, not policy.

The existing generic source-index engine is the durable closure authority. The
admitted package adds only a source-owned fixture directory, rewrites the
legacy source as concise non-normative navigation, marks its corpus row
`derived`, removes the four M5-CP0 dependency edges, deletes M5-CP0, and
resolves F085 in one commit. It does not add another verifier or change the
shared engine, Router, dispositions, semantic suites, or canonical standards.

Order 7 remains outside the frozen concurrent-preparation inventory. That
inventory assigns exclusive writable semantic verifiers; the accepted M5
train removed the four unassigned source-shape readers, while the aggregate
closure engine remains shared structural authority. Adding it as an exclusive
order-7 verifier would create false ownership and duplicate-subject pressure.

Admission verification passed the exact package suite, all 46 declarative
suites, 42 engine tests, both plan checks, lifecycle fixtures, graph freshness
at 230 Bash verifiers / 235 nodes / 989 edges / 231 components, and all 230
mixed entrypoints.

### Accepted M5-CP6 Source Closure

The former Cross-Platform source is now a 21-line non-normative index with one
title, two route headings, and seven canonical routes. The source-owned generic
fixture enforces its exact structure, 24-line bound, route resolution, 35
source-specific prohibited literals, generic non-authority language, all 20
frozen identifiers, derived corpus state, canonical owner, and Router absence.

M5-CP0 and its four registry edges are deleted. Native Loading, Native Release,
Platform Evidence, and Platform Target are independent declarative roots; Rust
Target retains only its true specialization dependency on Platform Target. All
five semantic suites are otherwise unchanged. F085 and parent source package
7 are closed without a replacement prerequisite, bespoke verifier, source
exception, preparation-inventory false owner, compatibility schema, or prior
source fallback.

Acceptance verification passed the seven-source aggregate, all five focused
owner suites, all 45 registered suites, 42 engine tests, package authority,
M5-CP0 absence, both plan checks, lifecycle fixtures, all five surviving source
readers, graph freshness at 230 Bash verifiers / 235 nodes / 989 edges / 231
components, and all 230 mixed entrypoints.
