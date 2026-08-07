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
