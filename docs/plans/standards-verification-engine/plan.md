# Plan: Generic Standards Verification Engine

**Plan status:** `Active`

**Current phase:** Milestone 6: M6-L1 through M6-L7 leaf wave

**Next slice:** Implement admitted M6-L3 Release Workflow Foundation through
fast package and lifecycle-transfer gates. M6-L4 through M6-L7 remain admitted
and read-only.

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Eliminate the Bash verification and helper surface in favor of one
maintainable, declarative Python verification engine that runs repository-owned
suites once through a deterministic dependency graph, returns typed
diagnostics, and preserves the standards migration's exact ownership,
disposition, no-fallback, and evidence contracts.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | One documented command discovers and runs every registered declarative suite once in dependency order. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A2 | Strict configuration, path containment, dependency, assertion, and typed-diagnostic self-tests pass. | `focused` | `not-applicable` | `automated` | `pending` | pending |
| A3 | Decision, text, table, metadata, migration, plan, and source-index contracts needed by the current repository are represented without arbitrary command execution. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A4 | Migrated suites delete their replaced Bash checkers in the same accepted slice and preserve positive, negative, ownership, disposition, and no-fallback evidence. | `integration` | `not-applicable` | `automated` | `pending` | pending |
| A5 | Final inventory proves every Bash verifier, verification helper, and migration launcher is deleted after its behavior is migrated or intentionally retired with reviewed evidence. | `contract` | `not-applicable` | `automated` | `pending` | pending |
| A6 | The final Python engine-only suite passes through a documented Python entrypoint; the former Bash and repeated transitive checker graphs are absent. | `system` | `not-applicable` | `automated` | `pending` | pending |

## Scope

### In Scope

- A Python 3.11+ standard-library verification package and one stable generic
  launcher for the migration period.
- Strict TOML suite/registry contracts and TSV/Markdown assertion inputs.
- Deterministic dependency scheduling with each suite evaluated at most once.
- Typed text and JSON diagnostics with stable codes and source locations.
- Reusable text, decision, table, metadata, disposition, plan, route, and
  source-index checks required by measured checker inventory.
- Incremental removal of every Bash checker, verification helper, and temporary
  migration launcher.
- A generated migration inventory derived from registered and remaining
  checkers.

### Out Of Scope

- Normative standards policy changes unrelated to verification mechanics.
- A general-purpose expression language, arbitrary shell execution, `eval`,
  embedded Python from configuration, or compatibility parsing for old suite
  schemas.
- Copying or depending on another repository's orchestration design.
- Replacing real downstream product verification with documentation checks.
- Installing Python, third-party packages, or a second build toolchain.

## Constraints And Assumptions

### Constraints

- The engine owns mechanics only; standards and fixture data own policy.
- Unknown keys, assertion kinds, operators, diagnostic outcomes, paths, suite
  IDs, or dependencies are typed `invalid`, never ignored.
- Missing required files or the declared Python capability are typed
  `unavailable`; unsupported requested engine capabilities are typed
  `unsupported`.
- Repository paths are relative, normalized, and contained beneath the selected
  repository root. Symlink resolution cannot escape that root.
- Suite dependencies form an acyclic graph and execute once in stable order.
- Shared registry, engine contracts, parent plan, and migration inventory remain
  serial integration-owner files.
- A migrated checker and its old helper path are removed, not wrapped or kept as
  fallback.
- A genuinely custom algorithm remains eligible only as a typed,
  side-effect-free Python check registered through the engine; Bash is not an
  exceptional-check representation.

### Assumptions

- Python 3.11 or newer is a supportable verification dependency because it
  provides strict TOML parsing in the standard library; Milestone 1 validates
  and documents this requirement before it is relied on broadly.
- Most current checks decompose into reusable assertions plus ordered decision
  rules; the inventory milestone measures exceptions before plugin design.
- One stable Bash launcher is acceptable only as a process entrypoint while the
  repository's complete-suite convention still discovers `verify-*.sh`; it
  contains no policy or fallback behavior and is removed when that convention
  is replaced.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Implement the engine as a Python 3.11+ standard-library package with no runtime package dependencies. | This plan | [Architecture report](reports/architecture.md#runtime-and-packaging) | Repeated Bash/AWK/rg implementations |
| Use strict TOML for suite composition and TSV/Markdown for repository evidence. | This plan | [Architecture report](reports/architecture.md#contract-model) | Per-script argument and parsing conventions |
| Keep policy in standards and fixtures; the engine exposes bounded assertion primitives and ordered decision predicates. | This plan | [Architecture report](reports/architecture.md#ownership-boundary) | Policy embedded in shell control flow |
| Prohibit arbitrary commands and compatibility schemas in declarative suites. | This plan | [Architecture report](reports/architecture.md#security-and-no-fallback) | Shell-command check actions and old/new parser branches |
| Migrate by semantic family, deleting each replaced checker in the accepting slice. | This plan | [Architecture report](reports/architecture.md#migration-sequence) | Indefinite dual execution |
| Retire all Bash verifiers, verification helpers, and the migration launcher; represent exceptional algorithms only as registered typed Python checks. | This plan | [Architecture report](reports/architecture.md#extension-rule) | Bounded exceptional Bash adapters |
| Add bounded table, relation, and acceptance-claim checks from measured recurring contracts; do not add query strings, arbitrary transforms, or policy-specific callbacks. | This plan | 219 remaining scripts use AWK, 198 validate row shape, 165 collect projections, 83 count rows, 58 declare expected projections, and 109 compare lineage/owner/disposition data. | Per-script AWK/mapfile/sort pipelines |
| Derive coupled-checker migration order from one exact typed graph manifest with explicit unresolved targets, strongly connected components, condensation dependencies, and separately reviewed owner/risk/write-set classifications. | Integration owner | [Checker inventory report](reports/checker-inventory.md#coupled-graph-resolution) | Leaf-only selection and filename-adjacent batching |
| Keep the parent standards restructure plan authoritative for normative migration and this child plan authoritative for checker-engine architecture and migration. | Integration owner | Parent-plan delegation | `7.4c3hcp` bespoke Cross-Platform repair assumption |
| Resolve `F085` through one temporary whole-source route/prohibition contract followed by dependency-ordered owner suites and same-wave contract retirement at source closure. | Verification-engine migration mechanics | Cross-Platform `F085` dependency audit | Heading-range evidence, cross-owner replacement suites, and one oversized atomic closure wave |
| Preserve exact Bash evidence with one strict generic `exact_text` assertion over contained raw UTF-8 bytes and inline expected content. | Verification-engine assertion mechanics | M5-CP4+5 exact-evidence audit and accepted VE021 Option 1 | Literal-only weakening, expected-file mirrors, opaque hashes, normalization, wrappers, and source-specific callbacks |
| Accelerate the remainder through dependency-closed owner packages prepared concurrently and integrated serially in waves, with focused package checks and one complete-suite wave gate. | Verification-engine migration mechanics | Post-M5 graph audit: 69 inbound-free verifiers, including owner families whose outbound Bash prerequisites prevent naive leaf deletion | Per-script full-suite ceremony, filename-adjacent batching, cross-owner suites, Bash bridges, and duplicated prerequisite evidence |

## Simplicity And Ownership Review

- Independent concepts: suite registry, scheduling, assertion evaluation,
  diagnostics, repository evidence, and migration bookkeeping.
- Intentional coupling: assertion configurations name evidence paths and stable
  diagnostic expectations; suite dependencies name only required prerequisite
  suites.
- Accidental coupling risk: document headings, shell exit behavior, child
  script invocation, fixture layout, or mutable migration narration becoming
  hidden assertion authority.
- Policy/state/lifecycle owners: standards and fixtures own policy; suite TOML
  owns selected assertions; the engine owns execution and diagnostics; this
  plan owns migration lifecycle.
- Future changes that should remain independent: adding an assertion kind,
  adding a policy suite, changing human-readable output, and changing a
  standard's semantics.

## Milestones

### Milestone 0: Contract And Migration Authority

**Goal:** Establish one approved engine boundary, dependency decision, parent
delegation, migration sequence, and acceptance model before source changes.

**Allowed write set:**

- `docs/plans/standards-verification-engine/plan.md`
- `docs/plans/standards-verification-engine/execution-ledger.md`
- `docs/plans/standards-verification-engine/issues.md`
- `docs/plans/standards-verification-engine/reports/architecture.md`
- `plans/standards-library-effectiveness-restructure-plan.md`
- `evaluation/standards-effectiveness/findings.md`

**Tasks:**

- [x] Record measured checker topology and the selected runtime.
- [x] Freeze engine ownership, no-fallback rules, migration waves, and gates.
- [x] Delegate checker modernization from the parent migration plan.

**Acceptance gate:** Current plan structure passes, parent blocker names this
plan, and staged review contains only planning authority.

**Status:** `Accepted`

### Milestone 1: Executable Kernel And First Replaced Checker

**Goal:** Deliver a strict executable engine that replaces one complete,
representative and independently removable leaf checker without a wrapper or
policy loss.

**Allowed write set:**

- `tools/standards_verifier/**`
- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/rust-test-style.toml`
- `evaluation/standards-effectiveness/verify-declarative-suites.sh`
- `evaluation/standards-effectiveness/verify-rust-test-style.sh` (delete)
- this plan, ledger, and issues

**Tasks:**

- [x] Implement strict registry/config loading, repository path containment,
  acyclic once-only scheduling, typed diagnostics, text assertions, and ordered
  decision-table rules.
- [x] Add malformed-contract, path-escape, cycle, decision, diagnostic, and
  scheduling self-tests.
- [x] Register and run the Rust test-style suite.
- [x] Delete the replaced Rust test-style Bash checker.

**Acceptance gate:** Engine self-tests and negative fixtures pass; direct and
launcher execution pass; removed-checker scan passes; complete mixed suite
passes once.

**Status:** `Accepted`

### Milestone 2: Inventory And Structural Assertion Families

**Goal:** Derive an exact migration inventory and replace low-risk leaf scripts
that use only text, route, heading, table-shape, count, and exact-row checks.

**Allowed write set:** engine assertion modules/tests, suite contracts,
generated checker inventory source/generator/output, replaced leaf scripts,
and plan records selected per slice.

**Tasks:**

- [x] Generate and continuously verify exact structural checker inventory.
- [x] Migrate accepted Rust Tooling package `M2-P1` and remove its eight leaf
  scripts without changing engine source.
- [x] Migrate accepted Rust Release package `M2-P2` and remove its five leaf
  scripts without changing engine source.
- [x] Migrate accepted Tooling policy package `M2-P3` and remove its five leaf
  scripts without changing engine source.
- [x] Migrate accepted Rust API package `M2-P4` and remove its four leaf scripts
  without changing engine source.
- [x] Migrate accepted Rust Dependency package `M2-P5` and remove its four leaf
  scripts without changing engine source.
- [x] Migrate accepted Tooling reference package `M2-P6` and remove its two leaf
  scripts without changing engine source.
- [x] Migrate accepted TypeScript static-analysis package `M2-P7` and remove its
  leaf script without changing engine source.
- [x] Migrate accepted Verification quality-gate package `M2-P8` and remove its
  leaf script without changing engine source.
- [x] Add strict table header, row-width, count, non-empty, literal-domain,
  uniqueness, bounded-predicate projection, split, and ordering assertions;
  migrate `M2-S1` as the first complete consumer.
- [ ] Classify every checker by assertion family, inbound dependency, owner,
  risk, and migration disposition.
- [ ] Add strict table, Markdown heading/route, exact-row/set/order, and count
  assertions from observed requirements.
- [ ] Migrate coherent leaf packages and remove their scripts.
- [x] Migrate `M3-DT1` Language Binding Surface Contract and remove its Bash
  checker plus redundant schema and observed-outcome mirrors.
- [x] Migrate `M3-DT2` Rust Binding Contract Discovery and remove its Bash
  checker plus redundant schema and observed-outcome mirrors.
- [x] Migrate `M3-DT3` Binding Artifact Composition and remove its Bash checker
  plus redundant schema and observed-outcome mirrors.

**Acceptance gate:** Inventory coverage is exact; each package's focused suites
and complete mixed suite pass; no migrated behavior has two authorities.

**Status:** `Accepted`

#### Package M2-P2: Rust Release Leaf Consolidation

**Status:** `Accepted`

**Owner:** `profile.language.rust.release`

**Risk:** `consolidation`

**Allowed write set:**

- `evaluation/standards-effectiveness/suite-registry.toml`
- five suite contracts named in the checker-inventory report
- the five corresponding Bash checkers (delete only)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- this plan, ledger, issues, and checker-inventory report
- parent plan reconciliation after package acceptance

**Preserved contract:** 78 ordered typed decisions, required canonical profile,
reference, and former-source route evidence, five prohibited legacy defaults,
and exact dispositions `STD-0811` through `STD-0819`.

**Exclusions:** `verify-rust-release-evidence.sh` remains frozen by the source
package preparation contract; `verify-rust-release-owner-contract.sh` remains
frozen by row-35 identity contracts and depends on the shared metadata helper.
Both move only with Milestone 3's shared-contract migration.

**No-fallback rule:** implement with existing strict text and ordered-decision
checks, delete all five replaced scripts in the same slice, and add no wrapper,
source alias, compatibility schema, or owner-specific engine branch.

**Acceptance evidence:** 13 engine/inventory tests passed; all 14 registered
suites passed 70 checks directly and through the migration launcher; generated
inventory is fresh at 261 Bash entrypoints; all five deleted-path executable
and contract scans passed; and the complete 261-entrypoint mixed suite passed.

#### Package M2-P3: Tooling Policy Consolidation

**Status:** `Accepted`

**Owner:** `workflow.tooling`

**Risk:** `consolidation`

**Allowed write set:**

- `evaluation/standards-effectiveness/suite-registry.toml`
- five suite contracts named in the checker-inventory report
- the five corresponding Bash checkers (delete only)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- this plan, ledger, issues, and checker-inventory report
- parent plan reconciliation after package acceptance

**Preserved contract:** 60 ordered typed decisions; canonical Tooling workflow,
Tooling reference, and former-source route evidence; 11 prohibited legacy
defaults; and 13 exact dispositions across `STD-0666`, `STD-0673` through
`STD-0675`, `STD-0681` through `STD-0683`, `STD-0686`, `STD-0687`, and
`STD-0689` through `STD-0692`.

**Exclusions:** Tooling owner-contract and reference-recipe checkers remain
frozen by row-35 contracts. Tooling CI workflow reference and tool-setup
reference belong to the Tooling reference owner; TypeScript static analysis and
Verification quality gates belong to different canonical owners.

**No-fallback rule:** implement with existing strict text and ordered-decision
checks, delete all five replaced scripts in the same slice, and add no wrapper,
source alias, compatibility schema, or owner-specific engine branch.

**Acceptance evidence:** 13 engine/inventory tests passed; all 19 registered
suites passed 93 checks directly and through the migration launcher; generated
inventory is fresh at 256 Bash entrypoints; all five deleted-path executable
and contract scans passed; and the complete 256-entrypoint mixed suite passed.

#### Package M2-P4: Rust API Leaf Consolidation

**Status:** `Accepted`

**Owner:** `profile.language.rust.api`

**Risk:** `consolidation`

**Allowed write set:**

- `evaluation/standards-effectiveness/suite-registry.toml`
- four suite contracts named in the checker-inventory report
- the four corresponding Bash checkers (delete only)
- `evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv`
- this plan, ledger, issues, and checker-inventory report
- parent plan reconciliation after package acceptance

**Preserved contract:** 65 ordered typed decisions; canonical Rust API and
former-source route evidence; legacy architecture, failure, feature, and
validation default prohibitions; and exact dispositions `STD-0707` through
`STD-0712` plus `STD-0715`.

**Exclusions:** `verify-rust-api-owner-contract.sh` has executable and frozen
row-35 inbound references and depends on shared metadata verification.
`verify-rust-api-rustdoc.sh` is frozen by source-package preparation. Both
remain assigned to shared-contract Milestone 3.

**No-fallback rule:** implement with existing strict text and ordered-decision
checks, delete all four replaced scripts in the same slice, and add no wrapper,
source alias, compatibility schema, or owner-specific engine branch.

**Acceptance evidence:** 13 engine/inventory tests passed; all 23 registered
suites passed 109 checks directly and through the migration launcher; generated
inventory is fresh at 252 Bash entrypoints; all four deleted-path executable
and contract scans passed; and the complete 252-entrypoint mixed suite passed.

#### Package M2-P5: Rust Dependency Leaf Consolidation

**Status:** `Accepted`

**Owner:** `profile.language.rust.dependencies`

**Risk:** `consolidation`

**Allowed write set:** registry; four suite contracts named in the inventory
report; the four corresponding Bash checkers (delete only); generated checker
inventory; child plan records; and parent reconciliation after acceptance.

**Preserved contract:** 53 ordered typed decisions; canonical Rust Dependency,
Rust API, reference, and former-source evidence; legacy feature, graph,
workspace, and audit defaults; and all 14 exact dispositions `STD-0735` through
`STD-0748`.

**Exclusions:** adjacent Rust Dependency owner/source-closure checks have
executable or frozen-contract inbound references or shared-helper dependencies
and remain assigned to Milestone 3.

**No-fallback rule:** use existing strict text and ordered-decision checks,
delete all four replaced scripts atomically, and add no wrapper, compatibility
schema, source alias, or owner-specific engine branch.

**Acceptance evidence:** 13 self-tests; 27 suites and 130 checks; fresh
248-entrypoint inventory; removed-path scans; and complete mixed suite passed.

**Approved deviation:** implementation and serial integration records appear as
two adjacent commits because a delegated worker advanced `main` directly. The
maintainer approved retaining that history; no behavior or verification gate
was omitted.

#### Package M2-P6: Tooling Reference Consolidation

**Status:** `Accepted`

**Owner:** `reference/recipes/tooling.md`

**Risk:** `consolidation`

**Allowed write set:** registry; `tool-setup-reference.toml` and
`tooling-ci-workflow-reference.toml`; their two Bash checkers (delete only);
generated inventory; child plan records; and parent reconciliation.

**Preserved contract:** ten typed setup-reference decisions, canonical
non-normative setup and complete CI examples, former-source routes and
prohibitions, and exact move dispositions `STD-0693`, `STD-0694`, `STD-0701`,
and `STD-0702`.

**No-fallback rule:** use existing text and ordered-decision checks, delete both
scripts atomically, and add no wrapper, compatibility schema, or engine branch.

**Acceptance evidence:** 13 self-tests; 29 suites/137 checks; fresh 246-record
inventory; removed-path scans; and complete mixed suite passed.

#### Package M2-P7: TypeScript Static Analysis

**Status:** `Accepted`

**Owner:** `profile.language.typescript`

**Allowed write set:** registry, one suite TOML, its Bash checker deletion,
generated inventory, and plan records.

**Preserved contract:** ten typed decisions, canonical TypeScript and Tooling
reference text, former-source prohibitions, and split dispositions `STD-0677`
through `STD-0680`. Existing text/decision primitives suffice; no wrapper or
engine change is authorized.

**Acceptance evidence:** 13 self-tests; 30 suites/142 checks; fresh 245-record
inventory; removed-path scans; and complete mixed suite passed.

#### Package M2-P8: Verification Quality Gates

**Status:** `Accepted`

**Owner:** `workflow.verification`

**Allowed write set:** registry, one suite TOML, its Bash checker deletion,
generated inventory, and plan records.

**Preserved contract:** eleven typed decisions, canonical Verification text,
former-source prohibition, and refine dispositions `STD-0688` and `STD-0695`.
Existing text/decision primitives suffice; no wrapper or engine change is
authorized.

**Acceptance evidence:** 13 self-tests; 31 suites/146 checks; fresh 244-record
inventory; removed-path scans; and complete mixed suite passed.

### Structural And Shared-Contract Replan

**Status:** `Accepted`

The seven dependency-free leaves remaining after `M2-P8` are not one coherent
package:

| Package | Owner | Contract | Disposition |
| --- | --- | --- | --- |
| `M2-S1` Dependency audit lineage | `topics.dependencies` | decision, canonical text, exact disposition projection, accepted plan marker | Accepted with the first strict table consumer. |
| `M2-P9` Implementation change evidence | `workflow.implementation` | decision, canonical/reference text, exact split disposition | Accepted with existing checks after `M2-S1`. |
| `M3-C1` Acceptance claims | `workflow.verification` | canonical claim grammar and required-to-observed set satisfaction | Implement as one typed shared contract, then update its README invocation. |
| `M3-S1` F018 decomposition | parent migration plan | strict map, exact IDs/order, inventory/disposition relations, accepted lifecycle state | Accepted after relation checks; obsolete planned-state branches removed. |
| `M3-S2` Row 19 decomposition and owner validation | parent migration plan | strict tables, exact/expanded projections, uniqueness, counts, canonical report and accepted plan state | Accepted as one owner-coherent two-script package. |
| `M6-L1` Declarative-suite launcher | verification engine | inventory freshness plus complete Python execution | Retain only until the complete-suite convention changes; replace, do not wrap. |

The shared contract is bounded as follows:

- `table` reads one contained UTF-8 TSV file, requires an exact unique header
  and exact row widths, and may assert row count, non-empty columns, literal
  domains, unique column keys, and deterministic projections.
- A projection may use the existing bounded field predicates, select named
  columns, optionally split one selected field by one literal delimiter, and
  compare source order or lexical order with explicit expected rows. It cannot
  execute expressions, coerce types, interpolate variables, or mutate data.
- `relation` compares named projections from two strict table inputs for exact
  ordered or set equality. Both sides remain independently contained and
  validated; missing inputs are typed `unavailable` and malformed or unequal
  relations are typed `invalid`.
- `acceptance_claims` owns the canonical `kind@environment@mode` grammar and
  required-to-observed set satisfaction. `either` matches only the same kind
  and environment with explicit `automated` or `manual`; no evidence kind or
  environment implication is inferred.
- Common predicate parsing moves to one engine module shared by `decision`,
  `table`, and `relation`. There is one strict schema and no old/new parser.

Each primitive requires positive, mismatch, malformed-input, unknown-field,
missing-input, path-containment, and stable-diagnostic tests before a consumer
script is deleted. Engine and registry files remain serial. After a primitive
is accepted, disjoint suite packages may be prepared concurrently but are
integrated one at a time with fresh-revision admission.

#### Package M2-S1: Table Assertions And Dependency Audit Lineage

**Status:** `Accepted`

**Owner:** engine mechanics and `topics.dependencies`

**Preserved contract:** twelve ordered audit-lineage decisions, canonical
Dependencies and former-source text, exact `STD-0699`/`STD-0700` disposition
projection, and accepted `7.4b9r` lifecycle state.

**Acceptance evidence:** 19 engine/inventory tests; focused suite passed five
checks; all 32 suites passed 151 checks directly and through the launcher;
fresh 243-record inventory, removed-path scan, diff integrity, and complete
mixed suite passed.

**No-fallback result:** predicates have one shared parser; the table schema is
strict; the old Bash checker is deleted; no command action, expression string,
compatibility parser, source alias, or policy-specific callback exists.

#### Package M2-P9: Implementation Change Evidence

**Status:** `Accepted`

**Owner:** `workflow.implementation`

**Preserved contract:** thirteen ordered decisions, canonical
change-description evidence, exact `STD-0698` split disposition,
non-normative pull-request recipe projection, and former-source prohibitions.

**Acceptance evidence:** 19 engine/inventory tests; focused suite passed five
checks; all 33 suites passed 156 checks directly and through the launcher;
fresh 242-record inventory, removed-path scan, diff integrity, and complete
mixed suite passed.

**No-fallback result:** existing checks express the complete behavior; the old
Bash checker is deleted and no engine branch, wrapper, alias, or weaker
evidence path was introduced.

### Milestone 3: Shared Metadata, Plan, And Migration Contracts

**Goal:** Replace shared Bash parsers for metadata graphs, plan lifecycle,
dispositions, ownership, and source-index closure with typed engine checks.

**Allowed write set:** affected engine modules/tests, declarative suites and
fixtures, replaced shared helpers/checkers, migration inventory, and plan
records selected per slice.

**Tasks:**

- [ ] Implement metadata uniqueness/dependency/cycle and canonical-owner checks.
- [x] Implement canonical acceptance-claim grammar and exact set-satisfaction
  checks; migrate `M3-C1` as the first complete consumer.
- [ ] Implement remaining plan lifecycle checks.
- [ ] Implement exact disposition/owner-map and source-index closure checks.
- [ ] Delete superseded generic Bash engines and their wrappers atomically.

**Acceptance gate:** Existing positive and negative fixture families pass via
the engine; old helpers and compatibility paths are absent; complete mixed
suite passes at every shared-contract slice.

**Status:** `Accepted`

#### Package M3-C1: Canonical Acceptance Claims

**Status:** `Accepted`

**Owner:** engine mechanics and `workflow.verification`

**Preserved contract:** seven canonical scenarios, exact
`kind@environment@mode` grammar, separate kind and environment identity, and
same-kind/same-environment `either` satisfaction by explicit automated or
manual evidence only.

**Acceptance evidence:** 25 engine/inventory tests; focused suite passed;
all 34 suites passed 157 checks directly and through the launcher; fresh
241-record inventory, removed-path and README scans, diff integrity, and
complete mixed suite passed.

**No-fallback result:** configuration declares the allowed kind and environment
domains; the engine infers no hierarchy, substitution, or environment
equivalence; the Bash checker is deleted and its README invocation is replaced
by the focused Python command.

#### Package M3-S1: Relations And F018 Decomposition

**Status:** `Accepted`

**Owner:** engine mechanics and parent migration plan

**Preserved contract:** exact fourteen-row slice map, IDs and source order,
unique slice/order and ID keys, source-inventory agreement, final disposition
agreement, report evidence, and accepted `7.4b2a`/`7.4b2b`/`7.4b2c` lifecycle.

**Acceptance evidence:** 31 engine/inventory tests; focused suite passed five
checks; all 35 suites passed 162 checks directly and through the launcher;
fresh 240-record inventory, removed-path and report/README scans, diff
integrity, and complete mixed suite passed.

**No-fallback result:** relation sides use contained strict TSV inputs, bounded
predicates, named projections, optional one-field splitting, and ordered or
unique-set equality only. Transitional planned states, the Bash checker, and
its historical command references are removed.

#### Package M3-S2: Row 19 Structure

**Status:** `Accepted`

**Owner:** parent migration plan

**Preserved contract:** 18 exact Row 19 children, 50 expanded IDs, strict
ten-column execution rows, exact split-boundary projections, strict 50-row
owner validation, unique IDs, bounded owner/action domains, both report
contracts, all accepted plan markers, and canonical Tooling owner/reference
presence.

**Acceptance evidence:** 31 engine/inventory tests; focused suite passed eight
checks; all 36 suites passed 170 checks directly and through the launcher;
fresh 238-record inventory, two removed-path scans, diff integrity, and
complete mixed suite passed.

**No-fallback result:** both Bash checkers are deleted and their frozen ledger
references now name the registered suite. No engine change, transitional owner
state, compatibility path, or weaker projection was introduced.

#### Coupled Graph Replan Trigger

**Status:** `Accepted`

After `M3-S2`, the only dependency-free Bash entrypoint is the temporary
`verify-declarative-suites.sh` launcher. Of 238 remaining Bash entrypoints, 138
have executable inbound references, 72 have frozen-contract references, 44
have both, 166 invoke verifiers, and 84 invoke helpers. The 237 non-launcher
entries therefore require dependency-ordered shared-contract migration or
authorized frozen-reference reconciliation; they cannot be admitted as leaf
packages under the completed sequence.

#### Coupled Graph Resolution

The selected resolution is a graph-manifest, helper-first dependency train.
Structural generation and semantic migration authority remain separate:

- `checker-dependency-nodes.tsv` records every current Bash verifier and every
  named helper target, whether each target resolves, structural degree, and a
  deterministic strongly connected component identity.
- `checker-dependency-edges.tsv` records one exact typed edge per executable
  reference, frozen-contract reference, verifier invocation, or helper
  invocation. Documentation references remain inventory evidence but do not
  constrain migration order.
- `checker-dependency-components.tsv` records component membership,
  condensation dependencies, inbound component references, cyclic state, and
  deterministic topological wave. A cycle is evidence to migrate one coherent
  component or re-plan its ownership; it is not broken by wrappers.
- `checker-migration-packages.tsv` is reviewed planning authority rather than
  generated inference. It assigns stable checker or source subjects to owner,
  risk, semantic outcome, exact write set, prerequisite packages, verification
  contract, and lifecycle state.

Generation must fail with a typed diagnostic for an ambiguous helper basename,
an invocation target absent from the repository, a malformed generated
artifact, or stale output. It must not infer canonical owner, semantic risk,
package cohesion, or migration disposition from names, paths, or graph shape.

Helper-family migration proceeds in ascending shared-contract blast radius:

1. decision-table consumers;
2. source-index closure and decision-traceability consumers;
3. plan-structure consumers;
4. metadata graph consumers;
5. verifier hubs and frozen historical identity packages in condensation order.

Each accepted package removes the complete replaced Bash authority and its
direct invocation edges. Shared registry, engine, generated graph artifacts,
package manifest, and plans remain serial. Disjoint package analysis and suite
construction may proceed concurrently only after package rows are accepted.
The temporary launcher remains until `M6-L1` replaces the complete-suite
convention.

#### Package M3-G1: Exact Checker Dependency Graph

**Status:** `Accepted`

**Owner:** verification-engine migration mechanics

**Allowed write set:** inventory/graph generator modules and focused tests,
generated structure and dependency graph TSVs, the temporary launcher's
freshness gate, engine documentation, this plan, ledger, issues, checker
inventory report, and parent-plan delegated state.

**Observable outcome:** one deterministic command writes or verifies an exact
repository-contained graph whose typed nodes, edges, components, unresolved
targets, and condensation waves agree with all current checker sources and
frozen references.

**No-fallback rule:** do not treat missing targets as leaves, collapse edge
types, infer semantic ownership, retain stale output, execute graph nodes, or
use a Bash graph adapter. The existing structure inventory remains generated
by the same Python authority and may be replaced by a coherent combined
generator only if its freshness contract is preserved atomically.

**Acceptance gate:** positive, cycle, unresolved-target, ambiguous-target,
stale-output, and deterministic-order tests pass; generated artifacts are
fresh; current graph counts are reconciled; direct engine and temporary
launcher runs pass; complete mixed verification runs because generator and
launcher contracts are shared.

**Re-plan condition:** stop before helper migration if exact components cross
multiple semantic owners, frozen contracts cannot be assigned to one owning
package, or helper behavior needs an unbounded expression/command mechanism.

**Acceptance evidence:** 37 engine/inventory/graph tests passed; generation and
freshness checks produced 243 resolved nodes, 1,045 typed edges, 239 components,
and 11 condensation waves; all 36 suites/170 checks and all 238 complete-suite
checker entrypoints passed. Five helpers are acyclic wave-zero nodes. Two bounded
verifier SCCs are reserved as coherent later packages. The refined path-shaped
dependency rule removed seven false dependencies caused by quoted evidence
strings without removing their typed executable-reference edges. Empty component
list fields use explicit `-` values and pass whitespace verification.

**No-fallback result:** unresolved and ambiguous targets are typed failures;
malformed and stale graph artifacts are rejected; generated artifacts are
excluded from graph inputs; no owner, risk, cohesion, or disposition is
inferred; and the launcher remains unchanged.

#### Package M3-P1: Reviewed Migration Package Authority

**Status:** `Accepted`

**Owner:** verification-engine migration mechanics

**Allowed write set:** the reviewed package manifest, its declarative contract
suite and shared registry row, generated structure/dependency artifacts, this
plan, ledger, issues, checker inventory report, and parent-plan delegated state.
Helper and consumer source is excluded.

**Observable outcome:** the manifest admits exactly one bounded implementation
package: `M3-DT1`, component `component-0085`, owned by the canonical Language
Bindings profile. Its exact write set, prerequisite, verification contract,
risk, semantic outcome, and lifecycle state are machine checked.

**Decision-table family evidence:** the helper has 13 direct consumers across
multiple semantic owners. Five consumer components currently have no dependency
callers or executable/frozen references. The remaining consumers are blocked by
inbound verifier chains; the helper self-test has a 44-verifier transitive
inbound closure through the accelerated-execution checker. Graph shape therefore
does not authorize one 1,199-line cross-owner migration package.

**Acceptance evidence:** the focused package-authority suite passed its one
check; all 37 declarative suites/171 checks, 37 engine tests, Python compilation,
plan structure, generated freshness at 243 nodes/1,047 edges/239 components,
whitespace integrity, and all 238 complete-suite checkers passed.

**No-fallback result:** `M3-DT1` must remove the complete Bash authority and its
schema/observed mirror rather than invoke Python from Bash or retain a wrapper.
No other component is admitted by proximity, basename, shared helper use, or
generated wave. Shared registry, graph artifacts, manifest, and plans remain
serial integration-owner files.

**Re-plan trigger:** if `component-0085` contains semantics outside the bounded
decision, text, table, and relation checks already supported by the engine, stop
rather than add command execution, retain the checker, or weaken evidence.

#### M3-DT1 Documentation Scope Re-plan Trigger

**Status:** `Accepted`

Pre-implementation review found that the standards-effectiveness README names
the current Bash entrypoint. The admitted write set omitted that shared
documentation file. Deleting the entrypoint would therefore leave a stale
documented authority, while editing the README would violate exact package
admission. The attempted source changes were restored before integration.

**Option 1 - Expand the same package (`Recommended`):** re-admit `M3-DT1` with
the README in its exact write set, replace the obsolete entrypoint reference
with the canonical suite and retained decisions fixture, and add the README to
removed-path verification. This is one owner-coherent outcome with one extra
mechanical projection file and no intermediate competing authority.

**Option 2 - Documentation prerequisite:** admit a serial mechanical package
that updates the README first, then keep the consumer replacement as a dependent
package. Choose this only if the README has concurrent changes or requires an
independent reviewer; otherwise it creates an avoidable intermediate reference
to a suite that is not yet registered.

**Option 3 - Defer and select another leaf:** leave `M3-DT1` admitted but blocked
and analyze another inbound-free decision consumer. Choose this only if README
ownership is disputed. It preserves safety but does not resolve the stale
reference or advance this component.

Retaining the Bash checker, adding a wrapper, deleting without documentation
reconciliation, or weakening the removed-path scan are not valid options.

**Selected resolution:** Option 1. The re-admitted package includes the
standards-effectiveness README in its exact write set and adds an explicit
removed-path gate to its verification contract. The implementation slice must
replace the README's Bash-entrypoint projection with the registered suite and
retained decisions fixture in the same atomic outcome. No intermediate
documentation authority or compatibility entrypoint is authorized.

#### Package M3-DT1: Language Binding Surface Contract

**Status:** `Accepted`

**Owner:** `profile.boundary.language-bindings`

**Observable outcome:** one registered five-check suite derives all 19 surface
decisions from strict domains and ordered predicates, preserves exact canonical
profile, former-source, inventory, and disposition evidence, and retains typed
invalid and unavailable outcomes without implicit export defaults.

**Acceptance evidence:** the focused suite passed five checks; all 38
declarative suites/176 checks and 37 engine tests passed; Python compilation
passed with bytecode directed outside the read-only worktree; graph freshness
reports 237 Bash verifiers, 242 nodes, 1,039 edges, and 238 components. The
removed-path scan finds obsolete paths only in the accepted package's frozen
write-set history, and all 237 mixed checker entrypoints passed.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
were deleted, the README now projects the registered suite and retained
decisions fixture, and no Bash wrapper, transitive checker call, dual outcome
authority, stale operational reference, or default-success path remains.

#### M3-DT2 Package Admission: Rust Binding Contract Discovery

**Status:** `Accepted`

**Owner:** verification-engine migration mechanics

**Selected package:** post-`M3-DT1` graph review found four inbound-free direct
decision consumers. Rust Binding Contract Discovery is the smallest
owner-coherent candidate not coupled to unresolved source closure: 72 Bash
lines, one Rust profile owner, 13 strict decisions, one exact disposition, and
one README projection. Its current identity is `component-0183`.

**Deferred candidates:** Platform Evidence Coverage is nominally smaller, but
it and Native Artifact Loading are governed by unresolved Cross-Platform
source-shape finding `F085`; they remain reserved for Milestone 5. Binding
Artifact Composition is independently eligible but larger and follows this
package in reviewed risk order.

**Exact package outcome:** `M3-DT2` includes the replacement suite, obsolete
checker/schema/observed authorities, README projection, shared registry and
package authority, generated graph artifacts, and serial plan records. The
decisions fixture remains canonical input and is not rewritten.

**Acceptance evidence:** the two-row package-authority suite passed; all 38
declarative suites/176 checks, 37 engine tests, Python compilation, both plan
structure checks, diff integrity, graph freshness at 237 Bash verifiers/242
nodes/1,041 edges/238 components, and all 237 mixed checker entrypoints passed.

**No-fallback result:** no graph-derived ownership, Cross-Platform scope
shortcut, omitted documentation, Bash wrapper, compatibility authority, or
alternate discovery mechanism is admitted.

#### Package M3-DT2: Rust Binding Contract Discovery

**Status:** `Accepted`

**Owner:** `profile.language.rust.language-bindings`

**Observable outcome:** one registered five-check suite derives all 13 Rust
discovery decisions from strict domains and ordered predicates, preserves the
canonical Rust profile, former-source route/prohibitions, one exact
disposition, and both accepted parent markers, and distinguishes no-discovery,
invalid, unsupported, and unavailable outcomes.

**Acceptance evidence:** the focused suite passed five checks; all 39
declarative suites/181 checks, 37 engine tests, Python compilation, graph
freshness at 236 Bash verifiers/241 nodes/1,031 edges/237 components, removed
operational-path scanning, diff integrity, and all 236 mixed checker
entrypoints passed.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
were deleted, the README now projects the registered suite and retained
decisions fixture, and no wrapper, transitive checker call, universal version,
package-version substitution, alternate discovery, or default-success path
remains.

#### M3-DT3 Package Admission: Binding Artifact Composition

**Status:** `Accepted`

**Owner:** verification-engine migration mechanics

**Selected package:** `component-0024` remains inbound-free after `M3-DT2` and
has one Release owner, 75 Bash lines, 23 strict decisions, four exact
dispositions, one accepted parent marker, and one README projection. It has no
frozen identity or unresolved source-closure dependency.

**Exact package outcome:** `M3-DT3` includes the replacement suite, obsolete
checker/schema/observed authorities, README projection, shared registry and
package authority, generated graph artifacts, and serial plan records. The
decisions fixture remains canonical input and is not rewritten.

**Acceptance evidence:** the three-row package-authority suite passed; all 39
declarative suites/181 checks, 37 engine tests, Python compilation, both plan
structure checks, diff integrity, graph freshness at 236 Bash verifiers/241
nodes/1,033 edges/237 components, and all 236 mixed checker entrypoints passed.

**No-fallback result:** no fixed artifact count, package/bundle default,
framework or example identity, internal-input publication, graph-derived owner,
omitted documentation, Bash wrapper, or compatibility authority is admitted.

#### Package M3-DT3: Binding Artifact Composition

**Status:** `Accepted`

**Owner:** `workflow.release`

**Observable outcome:** one registered five-check suite derives all 23 artifact
composition decisions from strict domains and ordered predicates, preserves the
Release owner, former-source route/prohibitions, four exact dispositions, and
the accepted parent marker, and returns typed invalid or unavailable outcomes
without fixed artifact/package defaults.

**Acceptance evidence:** the focused suite passed five checks; all 40
declarative suites/186 checks, 37 engine tests, Python compilation, graph
freshness at 235 Bash verifiers/240 nodes/1,023 edges/236 components, removed
operational-path scanning, diff integrity, and all 235 mixed checker
entrypoints passed.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
were deleted, the README now projects the registered suite and retained
decisions fixture, and no wrapper, transitive checker call, fixed composition,
framework/example identity, internal-input publication, or default-success path
remains.

#### Cross-Platform F085 Re-plan Decision

**Status:** `Accepted`

After `M3-DT3`, every remaining inbound-free decision-table consumer is within
the Cross-Platform source-shape boundary. Native Artifact Loading, Native
Artifact Release, Platform Evidence Coverage, and Platform Target Policy derive
former-source evidence from legacy heading ranges that must disappear when
`CROSS-PLATFORM-STANDARDS.md` closes. Their canonical semantics belong to
Cross-Platform, Release, and Verification owners, so one ordinary package would
either cross owners or leave transitional heading authority.

**Option 1 - Shared closure prerequisite plus owner packages (`Recommended`):**
create one bounded migration-only source-closure contract that proves exact
source-wide routes and prohibited legacy text without heading-range aliases.
Then admit dependency-ordered owner-coherent suites for Cross-Platform, Release,
and Verification, integrate shared registry/graph changes serially, close the
legacy source, and retire the migration-only contract in the same closure wave.
Choose this when owner boundaries and reviewable thin slices must both remain
explicit.

**Option 2 - Coordinated atomic closure wave:** freeze separate owner subpackages
but integrate all four checker replacements and legacy-source closure in one
atomic wave checkpoint. Choose this only if no valid intermediate legacy index
state exists; it reduces transitional state but creates a much larger review and
rollback surface.

**Option 3 - Defer F085 and resolve other caller chains:** leave all four
Cross-Platform source-shape checkers intact and continue with graph packages
outside this source. Choose this if source-closure ownership is unavailable; it
preserves safety but delays Milestone 5 and helper retirement.

Heading aliases, compatibility sections, source exceptions, one cross-owner
semantic suite, weaker whole-file checks, or deleting scripts before their
replacement evidence exists are not valid options.

**Selected option:** Option 1. `M5-CP0` establishes one migration-owned,
non-normative whole-source contract over the complete
`CROSS-PLATFORM-STANDARDS.md` index. It proves the exact canonical routes and
source-wide prohibited legacy defaults without using section delimiters. It
does not own Cross-Platform, Release, Verification, or Rust policy and cannot
survive source closure.

**Dependency audit refinement:** Platform Target Policy has two live callers,
Native Artifact Loading and Rust Target Configuration. The owner-coherent
replacement train is therefore:

1. `M5-CP0` whole-source migration prerequisite;
2. `M5-CP1` Native Artifact Loading (`topic.cross-platform`);
3. `M5-CP2` Native Artifact Release (`workflow.release`);
4. `M5-CP3` Platform Evidence Coverage (`workflow.verification`);
5. `M5-CP4` Rust Target Configuration
   (`profile.language.rust.cross-platform`);
6. `M5-CP5` Platform Target Policy (`topic.cross-platform`); and
7. `M5-CP6` Cross-Platform source closure and `M5-CP0` retirement.

Each semantic package preserves its own decisions, exact dispositions,
canonical owner evidence, typed outcomes, routes, and prohibited defaults.
Suite dependencies replace transitive checker calls only when both endpoints
have accepted declarative owners. Shared registry, graph, source-closure, and
plan integration remains serial. Package order may advance independent
inbound-free `M5-CP1` through `M5-CP3` in any reviewed order, but `M5-CP4` and
`M5-CP1` must both be accepted before `M5-CP5`, and `M5-CP6` cannot begin until
all five semantic replacements are accepted.

**Retirement condition:** `M5-CP0` is deleted in `M5-CP6` after the final
Cross-Platform index shape, all exact routes/prohibitions, all dispositions,
and all replacement suites pass together. It must not become a permanent
source exception, policy owner, compatibility schema, or duplicate assertion
authority.

#### M5-CP0 Package Admission: Whole-Source Prerequisite

**Status:** `Accepted`

**Owner:** verification-engine migration source closure

**Observable outcome:** one registered text-only suite scans all of
`CROSS-PLATFORM-STANDARDS.md` and requires the complete canonical route set
while prohibiting the union of former platform-target, native-loading,
native-release, and platform-evidence defaults. It asserts no heading, policy
decision, disposition, or canonical-owner prose.

**Exact implementation write set:**

- `evaluation/standards-effectiveness/suite-registry.toml`;
- `evaluation/standards-effectiveness/suites/cross-platform-source-closure-prerequisite.toml`;
- the migration-package manifest and its validating suite;
- generated checker structure/dependency node/edge/component inventories;
- this plan, ledger, issues, checker-inventory report, and parent plan.

`CROSS-PLATFORM-STANDARDS.md`, all semantic fixtures, all five semantic Bash
checkers, canonical standards, README projections, engine source, lockfiles,
and source-closure manifests are excluded.

**Required routes:** platform-support Cross-Platform topic, Standards Router,
filesystem Cross-Platform topic, Security containment, native-artifact-loading
Cross-Platform topic, Release artifact plan, and Verification platform-evidence
coverage.

**Required prohibitions:** the exact union of fixed target/tier/Strategy/layout,
fixed native extension/embedding/loading, fixed OS filename/class-local release,
and fixed runner/schedule/fail-fast evidence defaults checked by the four
current source slices.

**No-fallback rule:** use the existing whole-file `text` assertion. Do not add
an engine primitive, source heading, compatibility fixture/schema, source
exception, policy assertion, alternate route, or Bash wrapper. The source must
remain unchanged during implementation.

**Acceptance gate:** the focused suite, all declarative suites, engine tests,
Python compilation, package-authority suite, graph freshness, source-unchanged
proof from the admission commit, diff integrity, and the complete mixed suite
pass before the package becomes accepted.

**Acceptance evidence:** the focused package-authority suite passed; all 40
declarative suites/186 checks, 37 engine tests, Python compilation, both
plan-structure checks, graph freshness at 235 Bash verifiers/240 nodes/1,023
edges/236 components, source immutability, diff integrity, and all 235 mixed
checker entrypoints passed.

#### Package M5-CP0: Whole-Source Prerequisite

**Status:** `Accepted`

**Owner:** verification-engine migration source closure

**Observable outcome:** one registered text-only suite scans the complete
Cross-Platform legacy index for seven canonical routes and 24 prohibited
former defaults without asserting a heading, semantic decision, disposition,
or canonical-owner rule.

**No-fallback result:** the implementation uses the existing text assertion;
the legacy source, five semantic checkers, canonical standards, engine,
README, and closure manifests are unchanged. No wrapper, source exception,
compatibility schema, alternate route, policy callback, or duplicate semantic
authority exists.

**Retirement:** this suite remains temporary and must be deleted in `M5-CP6`
with source closure after `M5-CP1` through `M5-CP5` are accepted.

**Acceptance evidence:** the focused suite and package-authority suite passed;
all 41 declarative suites/187 checks, 37 engine tests, Python compilation, both
plan-structure checks, graph freshness at 235 Bash verifiers/240 nodes/1,023
edges/236 components, admission-to-implementation source immutability, diff
integrity, and all 235 mixed checker entrypoints passed.

#### Cross-Platform Dependency-Semantics Re-plan Trigger

**Status:** `Accepted`

The `M5-CP1` audit found that Native Artifact Loading invokes Platform Target
Policy, while Rust Target Configuration also invokes Platform Target Policy.
The engine intentionally permits dependencies only on registered declarative
suites. Replacing a caller before classifying that invocation could silently
drop focused prerequisite coverage. Replacing the callee first would break its
two Bash callers or require prohibited dual semantic authority, a wrapper, or
an external-command dependency.

The same scripts also invoke migration lifecycle and broad integration checks
such as Row 6 decomposition, the execution train, independent-trust evidence,
and filesystem containment. Treating every historical nested invocation as a
permanent semantic dependency would reproduce the Bash process graph and could
expand one package into an unbounded transitive closure. Treating every call as
redundant without review could weaken focused evidence.

**Option 1 - Classify dependency semantics before package admission
(`Recommended`):** for every outbound call in `M5-CP1`, `M5-CP4`, and
`M5-CP5`, record whether the callee supplies an owner-required semantic
precondition or an independent migration/integration gate. Convert only true
semantic prerequisites into registered suite dependencies. Preserve
integration gates through package and wave acceptance, not nested suite
execution. Admit each caller only when its own decisions, owner evidence,
dispositions, routes, typed outcomes, and negative cases form a complete
focused contract. Choose this to preserve thin owner packages and remove
accidental orchestration coupling without weakening evidence.

**Option 2 - Atomic connected semantic replacement:** replace Native Artifact
Loading, Rust Target Configuration, and Platform Target Policy together as
three owner-coherent declarative suites, with dependencies frozen before the
wave. Migration/integration calls still require classification, but the
Platform Target caller edge cannot create an intermediate state. Choose this
when review proves Platform Target is a mandatory focused prerequisite for
both callers. This has a larger write, review, verification, and rollback
surface.

**Option 3 - Defer the connected chain:** migrate independent Native Release
and Platform Evidence packages first, leaving Native Loading, Rust Target, and
Platform Target unchanged until dependency semantics are resolved. Choose
this only if the semantic owner review is unavailable; it preserves current
coverage but delays source closure and does not resolve the architectural
question.

External Bash dependencies, arbitrary command actions, wrapper suites,
retaining a semantic Bash checker beside its declarative replacement,
duplicating Platform Target policy in caller suites, or dropping nested calls
without a recorded ownership classification are invalid options.

**Selected option:** Option 1. Every outbound call in the connected chain has
the following frozen disposition:

| Caller package | Current callee | Classification | Declarative treatment |
| --- | --- | --- | --- |
| `M5-CP1` Native Loading | `check-decision-table.sh` | replacement mechanics | Native Loading owns one strict decision check; no dependency |
| `M5-CP1` Native Loading | Platform Target Policy | owner-umbrella integration gate | no suite dependency; Native Loading's target field and typed outcomes remain complete; Platform Target remains an independently selected suite/checker |
| `M5-CP1` Native Loading | Row 6 decomposition | migration lifecycle gate | package/wave acceptance only |
| `M5-CP1` Native Loading | execution train | migration lifecycle gate | package/wave acceptance only |
| `M5-CP4` Rust Target | metadata helper | repository structural gate | package/wave acceptance only |
| `M5-CP4` Rust Target | Platform Target Policy | semantic specialization prerequisite | declare `platform-target-policy` in `requires` |
| `M5-CP4` Rust Target | independent-trust re-plan | migration lifecycle gate | package/wave acceptance only |
| `M5-CP5` Platform Target | metadata helper | repository structural gate | package/wave acceptance only |
| `M5-CP5` Platform Target | filesystem containment | adjacent-owner integration gate | package/wave acceptance only; filesystem authorization is outside `STD-0280` through `STD-0288` |
| `M5-CP5` Platform Target | independent-trust re-plan | migration lifecycle gate | package/wave acceptance only |

Native Loading is independently admissible because its decision contract
directly owns declared target, unsupported target, unknown target, capability,
and evidence outcomes. Invoking the broader same-owner Platform Target checker
does not supply a missing Native Loading rule. `M5-CP1`, `M5-CP2`, `M5-CP3`,
and `M5-CP5` require temporary `M5-CP0` while they read the Cross-Platform
former source.

Rust Target is a genuine specialization: its metadata explicitly requires and
specializes `topic.cross-platform`. To avoid either a missing dependency or
dual authority, `M5-CP4` and `M5-CP5` form one atomic integration wave with two
separate owner suites. Platform Target is registered first; Rust Target
declares it in `requires`; both Bash checkers are deleted in the same commit.
This atomic pair is not a cross-owner semantic suite and does not duplicate
generic policy in the Rust suite.

**Revised train:** `M5-CP1`, `M5-CP2`, and `M5-CP3` remain independently
reviewable packages after `M5-CP0`; `M5-CP4+5` is the bounded connected
generic/Rust dependency wave; `M5-CP6` closes the source and retires `M5-CP0`.

#### M5-CP1 Package Admission: Native Artifact Loading

**Status:** `Accepted`

**Owner:** `topic.cross-platform`

**Observable outcome:** one registered Native Loading suite depends on
`cross-platform-source-closure-prerequisite`, derives all 23 loading decisions
through strict domains and ordered typed outcomes, preserves the canonical
Native Artifact Loading section, two exact dispositions, and accepted lineage,
and contains no former-source heading assertion.

**Exact implementation write set:**

- migration-package manifest and validating suite;
- suite registry and
  `suites/native-artifact-loading.toml`;
- obsolete `verify-native-artifact-loading.sh`,
  `native-artifact-loading-schema.tsv`, and
  `native-artifact-loading-observed.tsv` for deletion;
- standards-effectiveness README projection;
- generated checker structure/dependency inventories; and
- this plan, ledger, issues, inventory report, and parent plan.

The canonical decisions fixture, `CROSS-PLATFORM-STANDARDS.md`,
`topics/cross-platform.md`, Platform Target checker, engine source, findings,
historical ledger, source-closure manifests, lockfiles, and all unrelated
fixtures are excluded.

**Dependency contract:** `M5-CP0` is the only suite dependency. Platform
Target remains an independently selected integration gate under the accepted
VE016 classification; Row 6 and execution-train evidence remain package/wave
gates and are not nested dependencies.

**No-fallback rule:** retain no Bash wrapper, schema compatibility parser,
observed-outcome mirror, heading alias, duplicated Platform Target policy,
alternate loader/artifact, ambient identity, guessed filename, embedded copy,
or default-success path.

**Acceptance gate:** focused dependency-order execution, package authority, all
declarative suites, 37 engine tests, Python compilation, graph freshness,
removed-path scanning, source immutability, both plan checks, diff integrity,
and the complete mixed suite pass before implementation is accepted.

**Admission evidence:** the focused package-authority suite passed; all 41
declarative suites/187 checks, 37 engine tests, Python compilation, both
plan-structure checks, graph freshness at 235 Bash verifiers/240 nodes/1,025
edges/236 components, source and semantic-input immutability, diff integrity,
and all 235 mixed checker entrypoints passed.

#### Package M5-CP1: Native Artifact Loading

**Status:** `Accepted`

**Owner:** `topic.cross-platform`

**Observable outcome:** one registered five-check suite depends on `M5-CP0`,
derives 23 ordered loading decisions, preserves canonical policy, two exact
dispositions, accepted lineage, and README projection, and executes the
temporary whole-source prerequisite once before focused Native Loading checks.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
are deleted. No Platform Target duplication, wrapper, heading range,
compatibility input, alternate loader/artifact, ambient identity, guessed
filename, embedded copy, or default-success path remains.

**Verification:** focused dependency execution passed `2` suites / `6` checks;
all `42` declarative suites, `37` engine tests, Python compilation, package
authority, removed-path scans, protected-input immutability, both plan checks,
diff integrity, and all `234` mixed checker entrypoints passed. The regenerated
graph contains `234` Bash verifiers, `239` nodes, `1,015` edges, and `235`
components.

#### M5-CP2 Package Admission: Native Artifact Release

**Status:** `Accepted`

**Owner:** `workflow.release`

**Observable outcome:** one registered Native Artifact Release suite depends on
`cross-platform-source-closure-prerequisite`, derives all 19 release identity
and consumer-information decisions through strict domains and ordered typed
outcomes, preserves the canonical Artifact Plan text, two exact dispositions,
accepted lineage, and README projection, and contains no former-source heading
assertion.

**Exact implementation write set:**

- migration-package manifest and validating suite;
- suite registry and `suites/native-artifact-release.toml`;
- obsolete `verify-native-artifact-release.sh`,
  `native-artifact-schema.tsv`, and `native-artifact-observed.tsv` for deletion;
- standards-effectiveness README projection;
- generated checker structure/dependency inventories; and
- this plan, ledger, issues, inventory report, and parent plan.

The retained `native-artifact-decisions.tsv`,
`CROSS-PLATFORM-STANDARDS.md`, `workflows/release.md`, Release Artifact Policy
checker, engine source, findings, historical ledger, source-closure manifests,
lockfiles, and all unrelated fixtures are excluded.

**Dependency contract:** temporary `M5-CP0` is the only suite dependency.
Release Artifact Policy independently owns `STD-0543` through `STD-0551` and is
an owner-umbrella integration gate under VE017; Row 6 and execution-train
evidence remain package/wave gates and are not nested dependencies.

**No-fallback rule:** retain no Bash wrapper, schema compatibility parser,
observed-outcome mirror, heading alias, duplicated Release Artifact policy,
OS-name filename default, class-local installation prose, ambient package,
alternate artifact, incomplete publication, or default-success path.

**Acceptance gate:** focused dependency-order execution, package authority, all
declarative suites, 37 engine tests, Python compilation, graph freshness,
removed-path scanning, source and semantic-input immutability, both plan checks,
diff integrity, and the complete mixed suite pass before implementation is
accepted.

**Admission identity:** the stable package subject is
`checker:evaluation/standards-effectiveness/verify-native-artifact-release.sh`.
Current `component-0137` is non-authoritative graph snapshot evidence. The
accepted VE018 recovery prevents ordinal reuse from changing package identity.

**Admission evidence:** focused package authority and all 42 declarative suites
passed; 37 engine tests, Python compilation, both plan checks, protected-input
immutability, and diff integrity passed. The admission graph is fresh at 234
Bash verifiers, 239 nodes, 1,017 edges, and 235 components; all 234 mixed
checker entrypoints passed.

#### Package M5-CP2: Native Artifact Release

**Status:** `Accepted`

**Owner:** `workflow.release`

**Observable outcome:** one registered five-check suite depends on M5-CP0,
derives 19 ordered native release decisions, preserves canonical Artifact Plan
policy, two exact dispositions, accepted lineage, and README projection, and
executes the temporary whole-source prerequisite once before focused checks.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
are deleted. No broader Release Artifact Policy duplication, wrapper, heading
range, compatibility input, OS filename default, class-local installation
prose, ambient package, alternate artifact, incomplete publication, or default
success remains.

**Verification:** focused dependency execution passed 2 suites / 6 checks; all
43 declarative suites, 37 engine tests, Python compilation, package authority,
removed-path scans, protected-input immutability, both plan checks, diff
integrity, and all 233 mixed checker entrypoints passed. The regenerated graph
contains 233 Bash verifiers, 238 nodes, 1,007 edges, and 234 components.

#### M5-CP3 Package Admission: Platform Evidence Coverage

**Status:** `Accepted`

**Owner:** `workflow.verification`

**Observable outcome:** one registered Platform Evidence Coverage suite depends
on `cross-platform-source-closure-prerequisite`, derives all 21 support,
coverage, environment, scheduling, orchestration, and fallback decisions
through strict domains and ordered typed outcomes, preserves canonical
Verification text, two exact dispositions, accepted lineage, and README
projection, and contains no former-source heading assertion.

**Exact implementation write set:**

- migration-package manifest and validating suite;
- suite registry and `suites/platform-evidence-coverage.toml`;
- obsolete `verify-platform-evidence-coverage.sh`,
  `platform-evidence-schema.tsv`, and `platform-evidence-observed.tsv` for
  deletion;
- standards-effectiveness README projection;
- generated checker structure/dependency inventories; and
- this plan, ledger, issues, inventory report, and parent plan.

The retained `platform-evidence-decisions.tsv`,
`CROSS-PLATFORM-STANDARDS.md`, `workflows/verification.md`, Verification
Ownership checker, engine source, findings, historical ledger, source-closure
manifests, lockfiles, and all unrelated fixtures are excluded.

**Dependency contract:** temporary `M5-CP0` is the only suite dependency.
Verification Ownership is a same-owner integration gate under VE019; Row 6 and
execution-train evidence remain package/wave gates and are not nested
dependencies. The decision-table helper supplies replacement mechanics only.

**No-fallback rule:** retain no Bash wrapper, schema compatibility parser,
observed-outcome mirror, heading alias, duplicated Verification Ownership
policy, default target set, current-platform substitution, weakened required
support, provider-matrix inference, fixed trigger/fail-fast default, simulated
environment substitution, or default-success path.

**Acceptance gate:** focused dependency-order execution, package authority, all
declarative suites, 37 engine tests, Python compilation, graph freshness,
removed-path scanning, source and semantic-input immutability, both plan
checks, diff integrity, and the complete mixed suite pass before implementation
is accepted.

**Admission identity:** the stable package subject is
`checker:evaluation/standards-effectiveness/verify-platform-evidence-coverage.sh`.
Current `component-0148` is non-authoritative graph snapshot evidence.

**Admission evidence:** focused package authority and all 43 declarative suites
passed; 37 engine tests, Python compilation, both plan checks, protected-input
immutability, and diff integrity passed. The admission graph is fresh at 233
Bash verifiers, 238 nodes, 1,009 edges, and 234 components; all 233 mixed
checker entrypoints passed.

#### Package M5-CP3: Platform Evidence Coverage

**Status:** `Accepted`

**Owner:** `workflow.verification`

**Observable outcome:** one registered five-check suite depends on M5-CP0,
derives 21 ordered platform-evidence decisions, preserves canonical
Verification policy, two exact dispositions, accepted lineage, and README
projection, and executes the temporary whole-source prerequisite once before
focused checks.

**No-fallback result:** the Bash checker and redundant schema/observed mirrors
are deleted. No Verification Ownership duplication, wrapper, heading range,
compatibility input, default target set, current-platform or simulated-
environment substitution, weakened support, provider inference, fixed
orchestration, or default success remains.

**Verification:** focused dependency execution passed 2 suites / 6 checks; all
44 declarative suites, 37 engine tests, Python compilation, package authority,
removed-path scans, protected-input immutability, both plan checks, diff
integrity, and all 232 mixed checker entrypoints passed. The regenerated graph
contains 232 Bash verifiers, 237 nodes, 999 edges, and 233 components.

#### Source-Closure Verifier-Subject Re-plan Trigger

**Status:** `Accepted`

The M5-CP4+5 audit confirmed the accepted semantic dependency direction:
Platform Target is the generic prerequisite and Rust Target is its
specialization. It also found that the Rust Target Bash path remains live
migration authority in three places outside the admitted wave:

- the root-README dependency inventory requires the path to exist;
- the root-README consumer inventory and audit require it as one of 34 exact
  Bash consumers and one of two negative-purity consumers; and
- source-closure preparation assigns that exact Bash checker as the exclusive
  writable verifier for package `7.4c3.20`.

Deleting the checker under the current plan would invalidate accepted source-
closure and concurrency contracts. Retaining it beside a declarative suite,
adding a wrapper, or weakening exact inventories would violate the engine
plan's no-legacy and no-fallback rules.

**Option 1 - Canonical typed verifier subjects (`Recommended`):** replace the
source-preparation manifest's path-only `writable_checkers` field with exact
typed `writable_verifiers` subjects. Rewrite every existing value atomically as
`checker:<repository-path>`, admit `suite:<repository-path>` as the only other
kind, require existence and uniqueness by kind, and reject untyped or unknown
subjects. During M5-CP4+5, replace the Rust package's checker subject with the
new Rust Target suite subject in the same commit. Remove the retired checker
from the Bash-only README inventories and update their exact counts and
negative-purity set. Choose this to preserve exclusive future source-closure
ownership, concurrent preparation boundaries, and one canonical verifier
without compatibility parsing.

**Option 2 - Defer the connected wave to Rust source closure:** leave both Bash
checkers and all current inventories unchanged until package `7.4c3.20` can
replace the Rust checker, register both suites, and reconcile source-closure
authority in one manifest-ordered wave. Choose this when changing shared
preparation contracts now is riskier than delaying Cross-Platform closure. It
preserves current evidence but postpones M5-CP4+5 and M5-CP6.

**Option 3 - Expand the wave through contiguous source closure:** execute every
pending source package required to reach manifest order 20, then integrate
M5-CP4+5 with Rust Cross-Platform source closure. Choose this only when those
earlier source packages are already prepared and independently accepted for
integration. It preserves serial source order but creates a substantially
larger verification and rollback surface.

Untyped alternate paths, dual checker/suite entries, wrapper checkers, source-
package ownership removal, count exceptions, and out-of-order source closure
are invalid options.

**Recommendation:** select Option 1 in a dedicated shared-contract slice, run
the complete suite, then re-audit and admit M5-CP4+5 against the resulting
typed verifier authority.

**Selected option:** Option 1. Source preparation now owns exact typed
`checker:` and `suite:` verifier subjects. All nine existing subjects were
rewritten atomically as `checker:` values; the validator rejects untyped,
unknown, missing, symlink, duplicate-subject, and duplicate-path entries
without a compatibility branch. No source package, verifier path, semantic
evidence, or acceptance order changed.

**Acceptance result:** focused source-preparation and aggregate source-closure
checks passed for eight packages and nine exclusive verifier subjects. All 44
declarative suites, 37 engine tests, Python compilation, graph freshness at
232 Bash verifiers / 237 nodes / 999 edges / 233 components, both plan checks,
diff integrity, and all 232 mixed checker entrypoints passed.

**Trigger evidence:** both plan checks, all 44 declarative suites, graph
freshness at 232 Bash verifiers / 237 nodes / 999 edges / 233 components, diff
integrity, and all 232 mixed checker entrypoints passed with no implementation
or policy changes.

#### Rust Migration-Index Exact-Evidence Decision

**Status:** `Accepted`

The clean-tree M5-CP4+5 re-audit confirmed that the typed Rust verifier subject
can transfer atomically and identified every live Bash-only inventory update:
the dependency inventory falls from 33 to 32 rows, the README-consumer
inventory falls from 34 to 33 rows, negative-purity ownership becomes
`verify-s1-routing.sh` only, and the row-35, row-46, and root-consumer validators
must update their exact current counts. Historical row-35 and row-46 prose
remains immutable evidence of the transitions accepted at those milestones.

The Rust Target checker also enforces the seven-line
`languages/rust/RUST-CROSS-PLATFORM-STANDARDS.md` migration index with
byte-for-byte `diff`. The Python engine's text check supports required and
prohibited literals only. Replacing the exact comparison with those literals
would permit additional unreviewed or normative prose and would weaken
accepted evidence. Keeping the Bash checker, adding a wrapper, or creating an
expected-file mirror would preserve prohibited duplicate authority.

**Option 1 - Generic exact-text assertion (`Recommended`):** add one bounded
`exact_text` check kind with strict keys `id`, `type`, `path`, and `expected`.
Resolve the path through the existing contained regular-file contract, encode
the inline expected TOML string as UTF-8, compare raw bytes without newline or
whitespace normalization, and return one stable mismatch diagnostic. Add
focused pass, mismatch, missing-input, path-escape, and unknown-field tests.
The Rust suite then owns its seven-line expected index inline; no fixture
mirror, policy callback, command execution, compatibility schema, hash-only
oracle, or normalization fallback is introduced. Choose this for the smallest
reviewable extension that preserves the accepted invariant exactly.

**Option 2 - Generic source-index purity assertion:** define a reusable typed
Markdown index contract that permits only an approved title, route links, and
bounded non-normative routing prose while prohibiting normative sections and
unrecognized content. Choose this when multiple pending source indexes are
ready to migrate together and semantic index purity should replace byte
identity. This requires a separate grammar, fixtures over all selected index
shapes, owner review of the refined invariant, and a larger engine/API surface
before M5-CP4+5 can be admitted.

**Option 3 - Defer the connected wave to source closure:** retain both Bash
checkers and postpone M5-CP4+5 until manifest-order package `7.4c3.20` can use
the source-index closure engine selected for Milestone 7. Choose this when no
engine primitive should be added for one current consumer. It preserves exact
evidence but delays both suites and cannot migrate Platform Target alone
because the Rust checker directly invokes it.

Required/prohibited literals alone, an opaque content hash, an expected-file
mirror, a Bash or Python wrapper, partial generic/Rust migration, compatibility
parsing, or dropping exact index evidence are invalid options.

**Decision:** Option 1 is accepted as a dedicated shared-engine slice. The
implementation must use strict keys `id`, `type`, `path`, and `expected`, the
existing contained regular-file resolver, inline TOML UTF-8 content, and a raw
byte comparison without normalization. Focused tests must cover pass,
mismatch, missing input, path escape, and unknown fields. After the complete
suite passes, admit and implement M5-CP4+5 with no engine changes in the
package commit.

**Trigger evidence:** the audit was read-only after commit `d95e4e9`; no source,
checker, fixture, registry, suite, engine, README inventory, migration manifest,
or generated artifact changed before this re-plan record. Both plan checks, all
44 declarative suites, graph freshness at 232 Bash verifiers / 237 nodes / 999
edges / 233 components, diff integrity, and all 232 mixed checker entrypoints
passed.

#### M5-CP4+5 Package Admission: Platform And Rust Target Policy

**Status:** `Accepted`

**Owners:** `topic.cross-platform` and
`profile.language.rust.cross-platform`

**Observable outcome:** two separately registered owner suites replace the
connected Bash pair atomically. Platform Target derives 25 decisions and nine
exact generic dispositions while requiring temporary M5-CP0. Rust Target
derives 30 decisions and five exact specialization dispositions, requires
Platform Target, and preserves the seven-line migration index through the
accepted raw-byte `exact_text` assertion.

**Exact implementation write set:**

- migration-package manifest and validating suite;
- suite registry and `suites/platform-target-policy.toml` plus
  `suites/rust-target-configuration.toml`;
- `verify-platform-target-policy.sh` and
  `verify-rust-target-configuration.sh` for deletion;
- standards-effectiveness README projection;
- source-package preparation subject transfer;
- row-35 README dependency and consumer manifests;
- root README consumer audit plus row-35 and row-46 current-count validators;
- generated checker structure/dependency inventories; and
- this plan, ledger, issues, inventory report, and parent plan.

The retained decision fixtures, `CROSS-PLATFORM-STANDARDS.md`,
`languages/rust/RUST-CROSS-PLATFORM-STANDARDS.md`, canonical Cross-Platform and
Rust profiles, Router, root README, findings, historical reports, engine source,
lockfiles, and all unrelated fixtures are excluded.

**Dependency contract:** register Platform before Rust. Platform requires only
`cross-platform-source-closure-prerequisite`; Rust requires only
`platform-target-policy`. Metadata, filesystem containment, independent-trust,
row-35, row-46, and root-consumer checks remain integration gates rather than
suite dependencies.

**Lifecycle contract:** remove the Rust checker from the Bash-only dependency
and consumer manifests, reduce their current counts from 33/34 to 32/33,
reduce negative-purity ownership to `verify-s1-routing.sh`, and transfer source
package `7.4c3.20` from its `checker:` subject to
`suite:evaluation/standards-effectiveness/suites/rust-target-configuration.toml`
in the same implementation commit. Historical transition prose remains
unchanged.

**No-fallback rule:** retain no Bash wrapper, checker-to-suite bridge, dual
subject, literal-only index evidence, expected-file mirror, heading alias,
fixed target list, best-effort support, Strategy/Factory requirement,
universal layout, runtime/compile-only substitution, stub, silent omission,
alternate target/mechanism, named tool, weaker evidence, or default success.

**Acceptance gate:** focused dependency-order execution, exact package
authority, all declarative suites and engine tests, Python compilation, graph
freshness, removed-path and lifecycle scans, source/profile/fixture
immutability, both plan checks, diff integrity, and the complete mixed suite
pass before implementation is accepted.

**Admission identity:** package row 8 is stable Platform checker subject
`M5-CP5`; row 9 is stable Rust checker subject `M5-CP4`. The manifest records
Platform before Rust because semantic dependency order, not numeric package
suffix, controls execution. Both rows are admitted and share one bounded
atomic implementation write set.

**Admission evidence:** the focused package suite, all 44 declarative suites,
all 42 engine tests, both plan checks, plan lifecycle fixtures, diff integrity,
and all 232 mixed entrypoints passed. The regenerated admission graph is fresh
at 232 Bash verifiers, 237 nodes, 1,009 edges, and 233 components.

#### Package M5-CP4+5: Platform And Rust Target Policy

**Status:** `Accepted`

**Owners:** `topic.cross-platform` and
`profile.language.rust.cross-platform`

**Observable outcome:** Platform Target is one six-check suite requiring
temporary M5-CP0; Rust Target is one ten-check specialization suite requiring
Platform. Focused selection executes three suites once and preserves 55 typed
decisions, 14 exact dispositions, canonical owner/routing evidence, accepted
lineage, source-wide negative evidence, and byte-for-byte Rust migration-index
content.

**Lifecycle result:** both Bash checkers are deleted. Source package
`7.4c3.20` now owns the Rust suite subject; Bash-only README dependency and
consumer manifests contain 32 and 33 rows; S1 is the sole negative-purity
consumer; and row-35, row-46, and root-consumer validators enforce the new
current state. Historical transition prose remains unchanged.

**No-fallback result:** no wrapper, Bash bridge, dual subject, compatibility
schema, expected-file mirror, heading alias, policy duplication, fixed target
or support default, universal layout, substitute tool/environment, alternate
target/mechanism, weaker evidence, silent omission, stub, or default-success
path remains.

**Verification:** focused dependency execution passed three suites / 17
checks; exact package, source-preparation, root-consumer, row-35, and row-46
authority passed; all 46 declarative suites, 42 engine tests, Python
compilation, protected-input immutability, both plan checks, plan lifecycle
fixtures, removed-path scans, diff integrity, and all 230 mixed entrypoints
passed. The regenerated graph contains 230 Bash verifiers, 235 nodes, 989
edges, and 231 components.

#### M5-CP6 Cross-Platform Source-Closure Admission

**Status:** `Accepted`

**Owner:** verification-engine migration source closure, integrated with parent
source package `7.4c3.7`

**Observable outcome:** manifest-order source 7 becomes a concise
non-normative index, its corpus row becomes `derived`, the existing generic
source-index engine verifies its exact heading, routes, prohibited authority,
20 frozen identifiers, canonical owner, and Router exclusion, and temporary
M5-CP0 is absent after the same commit. The four former M5-CP0 consumers become
independent roots; Rust Target continues to depend only on Platform Target.

**Exact implementation write set:** `CROSS-PLATFORM-STANDARDS.md`; its corpus
row; a new `fixtures/source-closure/cross-platform/` contract, heading, route,
and prohibition set; the suite registry; deletion of the temporary M5-CP0
suite; the migration-package manifest and exact projection; `F085`; generated
checker graph artifacts; the parent execution ledger and plan; and this child
plan's ledger, issues, and inventory report.

Canonical topics, workflows, profiles, decision fixtures, dispositions,
rule-owner map, Router, final source manifest, generic source-closure engine and
aggregate, source-preparation inventory, README, engine source/tests,
configuration, lockfiles, and unrelated historical evidence are excluded.
Order 7 does not enter the frozen preparation inventory: accepted delegated
M5 packages replaced the unassigned source-shape checkers that caused its
absence, and the generic aggregate is shared structural authority rather than
an exclusive writable semantic verifier.

**Preserved semantics:** exact dispositions `STD-0280` through `STD-0299`;
Cross-Platform platform-support, filesystem, and native-loading routes;
Security containment; Release artifact identity and consumer information;
Verification target evidence; Router-selected specialization; all owner-local
typed outcomes and prohibited fixed targets, mechanisms, layouts, loaders,
artifact names, and CI schedules.

**No-fallback rule:** do not retain transitional headings, old source prose,
M5-CP0, a replacement prerequisite suite, source exceptions, compatibility
schemas, alternate routes, duplicated semantic assertions, fixed defaults, or
permissive index wording. Missing or inapplicable routes return the Router's
typed diagnostic instead of prior source wording.

**Acceptance gate:** focused generic source closure; focused Platform/Rust,
Native Loading, Native Release, and Platform Evidence suites; exact proof that
M5-CP0 and all four dependency edges are absent; package authority; all
declarative suites and engine tests; corpus-derived and F085-resolved state;
graph freshness; both plan checks; diff integrity; and the complete mixed suite.

**Admission evidence:** exact package authority, all 46 declarative suites, all
42 engine tests, both plan checks, lifecycle fixtures, Python compilation,
graph freshness at 230 Bash verifiers / 235 nodes / 989 edges / 231 components,
diff integrity, and all 230 mixed entrypoints passed.

**Implementation result:** the 51-line transitional source is now a 21-line
index with one title, two route headings, seven canonical routes, no former
policy headings, and no fixed target, mechanism, loader, artifact, or CI
defaults. The corpus row is `derived`; the generic aggregate verifies seven
closed sources and 20 Cross-Platform identifiers; all four temporary dependency
edges and the M5-CP0 suite are absent. F085 is resolved without adding order 7
to the frozen preparation inventory or creating replacement authority.

**No-fallback result:** semantic owner suites remain unchanged and independent;
Rust Target still requires only Platform Target. There is no legacy source
selection, transitional heading, M5-CP0 alias, replacement prerequisite,
bespoke verifier, source exception, compatibility schema, alternate route,
duplicated semantic evidence, permissive wording, or prior-source fallback.

**Acceptance evidence:** the generic aggregate passed seven registered source
closures, including Cross-Platform with seven routes and 20 frozen IDs. All
five owner suites, all 45 registered suites, 42 engine tests, Python
compilation, package authority, M5-CP0 absence, both plan checks, lifecycle
fixtures, five surviving global/historical source readers, graph freshness at
230 Bash verifiers / 235 nodes / 989 edges / 231 components, diff integrity,
and all 230 mixed entrypoints passed.

#### Migration-Package Stable-Identity Re-plan Trigger

**Status:** `Accepted`

The package manifest requires exact unique subjects, but its `components`
column stores generated strongly connected component ordinals. Deleting one
checker renumbers later components, so the same ordinal can identify unrelated
packages at different admissions. Relaxing uniqueness would hide overlapping
ownership; rewriting accepted rows to current ordinals would falsify their
admission evidence.

Admission plan and ledger references also participate in the generated
dependency inventory. Therefore graph regeneration is an admission-boundary
write, not only an implementation-boundary write.

**Option 1 - Stable source subject plus snapshot evidence (`Recommended`):**
replace `components` with a unique stable `subject` such as
`checker:evaluation/standards-effectiveness/verify-native-artifact-release.sh`
or `source:CROSS-PLATFORM-STANDARDS.md`. Keep generated component ordinal and
baseline commit in reports as non-authoritative admission evidence. Migrate all
accepted manifest rows atomically, retain unique package and subject checks,
and include generated graph artifacts in admission write sets. Choose this for
durable ownership, legible history, and exact overlap prevention.

**Option 2 - Commit-qualified component snapshot:** store
`component-0137@<baseline-commit>` as the unique subject. This preserves the
exact historical graph observation but makes package identity opaque, couples
planning authority to graph numbering, and requires lookup through old graph
artifacts to discover the checker. Choose only when historical SCC identity is
itself the reviewed subject.

**Option 3 - Separate stable subject and graph snapshot columns:** add a unique
source `subject` plus explicit `graph_component` and `graph_baseline` columns.
This retains structured snapshot evidence in the manifest but expands every
row and duplicates information already available in reports and commits.
Choose when automated historical graph correlation is a demonstrated need.

Dropping subject uniqueness, using current ordinals to rewrite accepted rows,
adding arbitrary suffixes, or exempting admission changes from graph freshness
are invalid options.

**Selected option:** Option 1. The manifest's `subject` column uses typed,
repository-relative checker paths or source identities. Accepted rows retain
their original reviewed subject after checker deletion. Both `package_id` and
`subject` remain unique. Generated component ordinal and baseline commit remain
report evidence only, and generated graph artifacts are part of every admission
boundary whose references affect graph freshness.

**Recovery write set:** package manifest and validator, generated structure and
dependency graph artifacts, this plan, ledger, issues, inventory report, and
parent plan. Semantic policy, checkers, fixtures, registry, README, engine
source, lockfiles, and unrelated migration authority are excluded.

**Acceptance gate:** focused package authority, all declarative suites, 37
engine tests, Python compilation, graph freshness, both plan checks, protected-
input immutability, diff integrity, and the complete mixed suite.

**Acceptance evidence:** package authority and all 42 declarative suites
passed; 37 engine tests, Python compilation, both plan checks, protected-input
immutability, and diff integrity passed. The regenerated graph is fresh at 234
Bash verifiers, 239 nodes, 1,015 edges, and 235 components; all 234 mixed
checker entrypoints passed.

### Milestone 4: Semantic Decision Migration

**Goal:** Move repeated policy decision derivation from shell branches into
strict ordered declarative predicates without embedding policy in engine code.

**Allowed write set:** decision assertion modules/tests, decision suite
contracts, affected existing fixtures, replaced semantic scripts, inventory,
and plan records selected per package.

**Tasks:**

- [ ] Support bounded `all`, `any`, `not`, equality, membership, and explicit
  default outcomes with strict field/domain validation.
- [ ] Migrate same-owner decision packages in risk order.
- [ ] Record computations that cannot be expressed without unsafe or opaque
  configuration as exceptional candidates rather than expanding the DSL by
  default.

**Acceptance gate:** Positive, negative, typed-outcome, and no-fallback cases
match existing accepted behavior; package scripts are removed; complete mixed
suite passes at package boundaries.

**Status:** `Planned`

### Milestone 5: Dependency Graph And Cross-Platform Unblock

**Goal:** Replace repeated transitive shell invocation with suite dependencies
and resolve `F085` through durable canonical evidence rather than former-source
headings.

**Allowed write set:** registry/dependency contracts, the temporary
whole-source contract, affected Cross-Platform/Release/Verification/Rust suites,
the five obsolete semantic scripts, source-closure fixtures and source only
after checker migration, generated graph artifacts, README projections, parent
migration records, and this plan's records. Every package freezes a narrower
exact write set before implementation.

**Tasks:**

- [x] Establish and verify `M5-CP0` without changing normative policy or the
  legacy source.
- [x] Add and verify the strict generic `exact_text` assertion required by the
  Rust migration-index contract.
- [x] Convert transitive verifier calls into declared suite dependencies.
- [x] Migrate platform-target, native-loading, release-artifact,
  platform-evidence, and Rust target-configuration suites while preserving
  owner-local semantics and whole-source route/prohibition coverage.
- [x] Delete the five replaced scripts, close the Cross-Platform source in the
  parent plan's manifest order, and delete `M5-CP0` in the same closure wave.

**Acceptance gate:** Each dependency executes once; all five semantic suites'
decisions/dispositions/routes/no-fallback cases pass; no suite depends on
former-source headings; `F085` resolves; `M5-CP0` is absent after source
closure; and the complete mixed suite passes.

**Status:** `Accepted`

### Milestone 6: Exceptional Checks And Bash Retirement

**Goal:** Resolve the measured remainder without turning the engine into a
general-purpose programming language.

**Allowed write set:** bounded typed Python check modules/tests, suite
contracts, replaced scripts, inventory, launcher/complete-suite entrypoint,
documentation, and plan records.

#### Wave 1 Admission: Four Caller-Free Owner Packages

**Status:** `Accepted`

**Graph basis:** the fresh post-M5 graph contains 230 Bash verifiers, 235
nodes, 989 edges, and 231 components. Corrected column-8 analysis identifies
caller-free scripts; nine are also prerequisite-free. Migration infrastructure
and pending source-package authorities are excluded from this first wave.

**Admitted packages:** `M6-W1-BUILD` owns Build's 16-row decision contract and
canonical routes; `M6-W1-DOC-TRACE` owns Documentation's 14-row traceability
decision contract, two exact dispositions, policy/reference split, and legacy
negative evidence; `M6-W1-TOOLING` owns Tooling's 12-row decision contract, 14
exact dispositions, owner evidence, and Router route; and
`M6-W1-TOOLING-REF` owns the non-normative Tooling recipe contract, 14 exact
dispositions, legacy-source route evidence, and negative defaults.

Each script has zero executable callers and zero verifier/helper prerequisites.
The four owners and suite paths are distinct. Their existing decision fixtures
remain read-only inputs; no engine primitive, policy, disposition, source
index, Router, metadata, configuration, or compatibility schema changes.

**VE023 correction:** the Tooling reference script asserts 14 distinct exact
dispositions but prints a stale success count of 12. The suite freezes all 14
actual rows. Preserving the incorrect message as authority, dropping two rows,
or adding a compatibility expectation is prohibited.

**Shared serial integration:** register four separate suites; update exact
package authority; remove Build, Tooling owner, and Tooling reference from the
root-README dependency inventory; change its exact count from 32 to 29 in the
row-35 verifier and its root-route subtype from 30 to 27; delete the four
scripts; regenerate the checker graph; update plan records. Documentation
traceability has no root-README lifecycle entry. The transitive/computed
subtypes remain 1/1 and the consumer inventory remains exactly 33.

**No-fallback rule:** do not retain wrappers, Bash bridges, duplicated suite
dependencies, inferred decisions, partial disposition sets, default tools,
default build behavior, default documentation paths, normative recipe examples,
weaker negative evidence, or silent success.

**Acceptance gate:** each focused suite, all 45 pre-wave suites, 42 engine
tests, exact package authority, root-consumer/row-35 lifecycle checks at 29/33,
removed-path scans, graph freshness, both plan checks, diff integrity, and one
complete mixed-suite wave gate pass.

**Admission verification:** exact package authority, all 45 registered suites,
42 engine tests, Python compilation, both plan checks, lifecycle fixtures,
graph freshness at 230 Bash verifiers / 235 nodes / 997 edges / 231
components, diff integrity, and all 230 mixed entrypoints passed.

**Implementation:** four independent declarative suites now own the Build,
Documentation traceability, Tooling owner, and Tooling reference contracts.
The four Bash checkers are deleted without wrappers or bridges. Package rows
are accepted; three root-README dependency rows are removed; row 35 now freezes
29 total dependencies, 27 root-route dependencies, unchanged 1/1
transitive/computed dependencies, and 33 consumers. VE023 is resolved by
enforcing all 14 Tooling-reference dispositions; VE024 records the bounded
subtype-count reconciliation omitted from admission prose.

**Focused verification:** all four focused replacements and package authority
passed; all 49 registered suites passed; all 42 engine tests and Python
compilation passed; row-35 lifecycle passed at 29/27/1/1/33; no executable or
lifecycle references to the four deleted paths remain; admission fixtures,
owners, routes, dispositions, references, and former source are unchanged; and
the regenerated graph is fresh at 226 Bash verifiers / 231 nodes / 986 edges /
227 components.

**Wave acceptance:** all 226 surviving mixed entrypoints passed. Wave 1 is
accepted with four Bash verifiers removed and no compatibility execution path.

#### Wave 2 Admission: Three Rust Source-Preparation Owners

**Status:** `Accepted`

**Graph basis:** the fresh post-Wave-1 graph contains 226 Bash verifiers, 231
nodes, 986 edges, and 227 components. After excluding the declarative launcher
and historical security re-plan checker, its only caller-free,
prerequisite-free semantic roots are Rust API Rustdoc, Rust dependency build
cost, and Rust release evidence.

**Admitted packages:** `M6-W2-RUST-API-RUSTDOC` owns 18 Rustdoc decisions, one
exact disposition, Rust API mechanism evidence, and the closed Rust API source
index; `M6-W2-RUST-DEP-BUILD-COST` owns 14 decisions, three exact dispositions,
generic/Rust/reference evidence, and the closed Rust Dependency source index;
and `M6-W2-RUST-RELEASE-EVIDENCE` owns 17 decisions, one exact disposition,
Rust release/reference evidence, and the closed Rust Release source index.

Each script has zero executable callers and zero verifier/helper prerequisites.
All mechanics fit existing strict decision and text assertions. The three suite
paths and owners are distinct. No engine primitive, policy, fixture,
disposition, source index, Router, metadata, configuration, or compatibility
schema changes are allowed.

**Typed subject transfer:** source-package preparation order 18 changes its one
Rust API checker subject to `suite:.../rust-api-rustdoc.toml`; order 21 changes
only the Rust dependency build-cost subject and retains the independent
candidate-inspection checker; order 24 changes its one Rust Release subject to
`suite:.../rust-release-evidence.toml`. The inventory remains eight packages
and nine exclusive typed subjects. No wrapper, missing path, duplicate subject,
or checker/suite dual identity is permitted.

**No-fallback rule:** do not retain Bash bridges, wrappers, duplicated suite
dependencies, inferred decisions, partial dispositions, fixed build-cost
thresholds, every-release command defaults, Rustdoc checklists, weaker source
closure, compatibility parsing, or silent success.

**Acceptance gate:** each focused suite, all 49 pre-wave suites, 42 engine
tests, exact package authority, exact source-package transfer at 8/9,
admission-source immutability, removed-path scans, graph freshness, both plan
checks, diff integrity, and one complete mixed-suite wave gate pass.

**Admission verification:** exact package authority, all 49 registered suites,
42 engine tests, Python compilation, source-package preparation at eight
packages / nine exclusive subjects, both plan checks, graph freshness at 226
Bash verifiers / 231 nodes / 992 edges / 227 components, diff integrity, and
all 226 mixed entrypoints passed.

**Implementation:** three independent declarative suites now own Rust API
Rustdoc, Rust dependency build-cost, and Rust release-evidence verification.
The three Bash checkers are deleted without wrappers or bridges. Package rows
are accepted, and source-package orders 18, 21, and 24 transfer directly to
suite subjects while retaining candidate inspection at order 21 and preserving
eight packages / nine exclusive subjects.

**Deviation:** admission named decision and text mechanics. Implementation uses
the already accepted generic `exact_text` assertion for each complete short
source index, strictly preserving every byte instead of reproducing weaker
line-count, route-substring, and heading-absence approximations. VE025 records
this evidence strengthening; no engine, policy, source, or compatibility change
was required.

**Focused verification:** all three replacements and package authority passed;
all 52 registered suites passed; all 42 engine tests and Python compilation
passed; source-package preparation passed at 8/9; no live reference to the
three deleted paths remains; admission policies, references, source indexes,
fixtures, and dispositions are unchanged; and the regenerated graph is fresh
at 223 Bash verifiers / 228 nodes / 983 edges / 224 components. The complete
mixed-suite wave gate passed all 223 surviving entrypoints, accepting Wave 2
without a compatibility execution path.

#### Post-Wave-2 Re-Plan Trigger: Executable Edge Semantics

**Status:** `Accepted`

The fresh graph has 223 Bash verifiers, 228 nodes, 983 edges, and 224
components. Its only caller-free and prerequisite-free roots are the
declarative-suite launcher and a historical security re-plan checker. Every
remaining semantic leaf executes another path.

Those edges are not one semantic category. They include shared generic helpers,
historical lifecycle/decomposition gates, owner-local semantic prerequisites,
and an external owned template command. The largest shared targets have 53,
16, 14, and 64 Bash callers. Treating all edges as semantic suite dependencies
would force oversized cross-owner waves; deleting leaves without a disposition
would violate VE022; retaining wrappers or Bash-to-Python bridges is prohibited.

**Option 1 - Typed executable-edge disposition contract (recommended):** add
one exact manifest and declarative table contract that classifies every edge a
wave removes as `native-engine`, `independent-gate`, `suite-requires`,
`same-owner-package`, `external-owned-artifact`, or `invalid`. Require the
target, owner, rationale, replacement evidence, and package identity. Migrate
owner packages only after every removed edge has one disposition. This enables
parallel owner preparation, preserves true dependencies, retires historical
coupling explicitly, and prevents both giant waves and one-off exceptions.

**Option 2 - Shared-prerequisite closure waves:** migrate a shared prerequisite
and every Bash caller atomically, then express retained semantics with suite
dependencies. This preserves the executable graph literally but creates large
cross-owner write sets, serial integration pressure, and difficult review. It
is appropriate only if audit proves most callers genuinely require the same
semantic contract.

**Option 3 - Owner-family waves with local edge review:** migrate one complete
owner chain at a time and document external-edge treatment inside each package.
This can start quickly for chains such as Accessibility, but repeats taxonomy
and review decisions, weakens global completeness evidence, and risks
inconsistent treatment of the same shared target.

**Rejected option:** wrappers, Bash bridges, dual checker/suite identities,
silent dependency deletion, implicit full-suite reliance, or one-off engine
callbacks preserve legacy execution or hide semantics and remain prohibited.

**Accepted decision:** Option 1. Implement one generic Python assertion over a
typed TSV manifest. Every package checker source must have exact outgoing-edge
coverage before deletion. `admitted` rows must name current executable edges;
`accepted` rows must name removed edges. Package and edge states must agree.
`native-engine`, `independent-gate`, `suite-requires`, `same-owner-package`, and
`external-owned-artifact` rows require typed replacement evidence;
`invalid/unresolved` blocks acceptance. Paths remain contained, keys unique,
and wrappers, bridges, implicit deletion, and duplicate authority prohibited.

**Acceleration model:** classify high-fan-out shared targets once, then admit
many disjoint owner packages in one wave. Package authors own only their suite,
fixture, deleted checker, and edge rows. Shared edge manifest, package manifest,
registry, generated graph, and plans integrate serially. A wave may remove many
scripts when their owners and edge dispositions are independent; batch size is
bounded by semantic review and write-set overlap, not an arbitrary script count.

#### Slice M6-EDGE-1: Generic Edge-Disposition Assertion

**Status:** `Accepted`

**Allowed write set:** one Python check module, check parser registration,
focused engine tests/fixtures, one declarative contract suite, suite registry,
edge manifest/schema fixture, engine documentation, generated graph artifacts,
and plan records.

**No-fallback rule:** no arbitrary command execution, Bash checker, bridge,
graph-derived default disposition, inferred owner, wildcard acceptance,
unresolved accepted row, or missing-path exception.

**Acceptance gate:** focused positive and negative engine tests prove malformed
schema, duplicate edges, package mismatch, incomplete outgoing coverage,
missing admitted edges, present accepted edges, unresolved acceptance, invalid
replacement evidence, and path containment fail with typed diagnostics. The
contract suite, all declarative suites, graph freshness, both plan checks, and
the complete mixed suite pass.

**Implementation:** the strict `edge_dispositions` check joins one exact TSV
manifest to package authority, the generated graph, and the suite registry.
Packages opt in explicitly. Their complete outgoing `executable_reference`,
`helper_dependency`, and `verifier_dependency` sets must match while admitted;
accepted packages retain historical rows only after their checker and graph
edges are absent. Edge identity includes type so coincident dependency and
reference edges cannot collapse.

Replacement evidence is executable rather than nominal: native assertions
name a registered package-owned suite and existing check ID; suite requirements
name an actual registry `requires` edge whose source suite is package-owned;
retained checker and external-artifact paths equal the edge target; same-owner
packages resolve through package authority; and unresolved rows cannot be
accepted. All paths remain contained and no replacement is executed.

**Deviation:** the first implementation draft checked only replacement path
existence. Semantic review found that fabricated assertion IDs or unproved
suite dependencies could pass. VE027 records the pre-acceptance correction to
registered assertion identity and actual registry-edge evidence. This
strengthens the accepted contract without changing its objective or adding a
fallback.

**Verification:** all 15 focused edge tests and all 57 engine tests passed;
all 53 registered suites passed; Python compilation, graph freshness at 223
Bash verifiers / 228 nodes / 983 edges / 224 components, both plan checks, and
diff integrity passed; and the complete mixed gate passed all 223 entrypoints.
No Bash checker, generated graph artifact, policy source, wrapper, bridge, or
compatibility path changed.

#### Slice M6-EDGE-2: Accelerated Multi-Owner Wave

**Status:** `Accepted`

After M6-EDGE-1 acceptance, classify high-reuse helper and historical-gate
edges, select disjoint owner packages, and migrate them in one integrated wave.
True semantic dependencies become suite `requires`; generic helper behavior
uses native engine assertions; historical gates remain independently
registered; same-owner chains migrate together; external artifacts retain an
explicit owner. Exact edge rows transition from `admitted` to `accepted` with
their checker deletion.

**Acceptance gate:** every removed checker has exact package and edge coverage;
all focused suites and typed edge checks pass; no unresolved row, wrapper,
bridge, or live deleted-path reference remains; one complete wave gate passes.

##### Wave 3 Admission: Six Independent Owners

**Status:** `Accepted`

**Packages:** `M6-W3-CONTRACT-BOUNDARY`, `M6-W3-CORE-CONSTANTS`,
`M6-W3-DISABLED-BEHAVIOR`, `M6-W3-LICENSING`, `M6-W3-PERFORMANCE`, and
`M6-W3-TYPESCRIPT-OWNER`.

**Frozen behavior:** 93 decision cases and 24 exact dispositions across
Contracts, Core constants, disabled-behavior verification, Licensing,
Performance, and TypeScript. Existing canonical owner, router, legacy-source
prohibition, accepted-plan, and disposition evidence remains unchanged.

**Edge contract:** every checker is inbound-free and has exactly two outgoing
typed edges to
`evaluation/standards-effectiveness/verify-milestone-7-row-15-decomposition.sh`:
one `executable_reference` and one `verifier_dependency`. All 12 rows are
`independent-gate` because row 15 proves historical migration lifecycle rather
than any package's semantic policy. It remains independently discovered and is
not copied, wrapped, inferred, or converted into a suite dependency.

**Implementation write set:** six new suite TOMLs, six deleted checker paths,
the unchanged decision fixtures as read-only evidence, package and edge
manifests, registry, package contract, the standards-effectiveness README for
the Core checker route, row-35 dependency fixture and checker for three frozen
README identities, generated graph artifacts, and this plan's records.

**Lifecycle reconciliation:** deleting Licensing, Performance, and TypeScript
owner checkers removes three root-route rows. Row 35 changes from 29 to 26
dependencies and from 27 to 24 direct root-route assertions; its transitive and
computed counts remain 1/1 and its consumer inventory remains 33.

**No-fallback rule:** no policy, fixture, disposition, canonical source,
metadata, Router, source package, engine, compatibility schema, wrapper,
bridge, alternate checker identity, inferred decision, weaker evidence, or
silent success may be added or changed.

**Implementation gate:** each suite must reproduce its exact decision outcomes,
positive and negative canonical text, exact dispositions, and route/source
closure. Package and edge rows transition together to `accepted`; all six
checkers and every live reference to them are absent; the row-15 gate remains;
focused suites, both authority contracts, 57 engine tests, all declarative
suites, row-35 lifecycle, graph freshness, both plan checks, diff integrity,
and one complete mixed gate pass.

**Implementation:** six separate declarative suites now own Contracts boundary
proof, Core constants, disabled-behavior claims, Licensing, Performance, and
TypeScript owner policy. They preserve all 93 frozen decisions, 24 exact
dispositions, canonical routes and owners, former-source prohibitions, and
accepted-plan evidence using existing strict engine primitives. All six Bash
checkers are deleted without wrappers, bridges, aliases, alternate identities,
or duplicated policy.

The six package rows and all 12 historical edge rows transitioned together to
`accepted`. Row 15 remains an independently discovered historical lifecycle
gate and is not a suite dependency. Row 35 now owns 26 Bash dependencies: 24
direct root-route assertions plus the unchanged one transitive and one computed
assertion; its consumer inventory remains 33.

**Verification:** all six focused suites, package authority, edge authority,
row-35 lifecycle, all 57 engine tests, and all 59 declarative suites passed.
Graph freshness passed at 217 Bash verifiers / 222 nodes / 969 edges / 218
components. Diff integrity and the complete mixed gate passed all 217 surviving
entrypoints. No policy, decision fixture, disposition, canonical source,
metadata, Router, source-package authority, engine, compatibility schema, or
fallback path changed.

##### Wave 4 Admission: Testing Evidence Family

**Status:** `Active`

**Packages:** 13 separate packages for acceptance paths, async evidence,
concurrency consolidation, coverage documentation, test-data lifecycle,
focused design, supporting-gate diagnosis, language-binding evidence,
organization, performance evidence, persisted contract artifacts, resilience
replay, and Testing source closure.

**Frozen behavior:** 187 typed decision cases, eight exact source-index routes,
and 101 exact dispositions across Verification, Concurrency, Language Bindings,
Performance, Contracts, Resilience, and the Testing former source. Canonical
owner text, legacy-source prohibitions, and accepted-plan evidence remain
unchanged.

**Boundary:** all 13 sources are executable-inbound-free, contract-inbound-free,
and helper-free. Frontend testing evidence is excluded because Frontend testing
lineage still calls it; neither member of that active caller chain changes.
None of the admitted sources is a row-35 identity, source-package subject, or
README checker route.

**Edge contract:** every admitted checker has exactly one executable reference
and one verifier dependency to the row-18 decomposition checker. All 26 rows
are `independent-gate`: row 18 proves historical Testing migration lifecycle,
remains independently discovered, and is not semantic policy for any package.

**Implementation write set:** 13 new suite TOMLs, 13 deleted checker paths,
unchanged fixtures as read-only evidence, package and edge manifests, registry,
package contract, generated graph artifacts, and this plan's serial records.

**No-fallback rule:** no policy, fixture, disposition, canonical source,
metadata, Router, row-18 checker, Frontend caller chain, engine, compatibility
schema, wrapper, bridge, alias, inferred decision, weaker evidence, or silent
success may be added or changed.

**Admission verification:** package and edge authority, all 57 engine tests,
all 59 declarative suites, graph freshness at 217 Bash verifiers / 222 nodes /
1,009 edges / 218 components, both plan checks, diff integrity, and all 217
mixed entrypoints passed.

**Implementation:** 13 registered declarative suites now own the complete
testing-family behavior. They preserve 187 typed decisions, eight exact Testing
index routes, 101 exact dispositions, canonical owner text, legacy-source
prohibitions, and accepted-plan evidence. All 13 Bash paths are deleted; their
package rows and all 26 historical edge rows transitioned together to
`accepted`. Row 18 remains independently discovered, and the Frontend testing
caller chain remains unchanged.

VE029 records one strict evidence refinement: the Testing source suite rejects
Markdown checkbox tokens anywhere rather than only line-start checklist syntax.
This removes more residual checklist authority without changing policy,
fixtures, the source, or the engine.

**Implementation verification:** all 13 focused suites plus package and edge
authority passed; all 57 engine tests and all 72 declarative suites passed;
graph freshness passed at 204 Bash verifiers / 209 nodes / 944 edges / 205
components; diff integrity and the complete mixed checkpoint passed all 204
surviving entrypoints.

##### Wave 5 Admission: Contract And Lifecycle Leaves

**Status:** `Accepted`

**Packages:** Contract invariants, Core code discipline, Core simplicity,
disabled implementation lifecycle, and Resilience failure boundaries.

**Frozen behavior:** 69 typed decisions and 26 exact dispositions across
Contracts, Core, Implementation, and Resilience, including canonical routes,
legacy-source prohibitions, and accepted-plan evidence.

**Edge contract:** all five sources are executable-inbound-free,
contract-inbound-free, and helper-free. Four have one row-15 reference and
dependency; Core simplicity additionally has one execution-train reference and
dependency. All 12 rows are `independent-gate` historical lifecycle evidence.

**Implementation write set:** five new suite TOMLs, five deleted checker paths,
unchanged fixtures as read-only evidence, two README checker-to-suite routes,
package and edge manifests, registry, package contract, generated graph
artifacts, and serial plan records.

**No-fallback rule:** no policy, fixture, disposition, canonical source,
metadata, Router, row-15 checker, execution train, engine, compatibility schema,
wrapper, bridge, alias, inferred decision, weaker evidence, or silent success
may be added or changed.

**Admission verification:** package and edge authority, all 57 engine tests,
all 72 declarative suites, graph freshness at 204 Bash verifiers / 209 nodes /
960 edges / 205 components, both plan checks, diff integrity, and all 204 mixed
entrypoints passed.

**Implementation gate:** five focused suites, package and edge authority, 57
engine tests, all declarative suites, graph freshness, README route closure,
both plan checks, diff integrity, and one complete mixed checkpoint pass.

**Implementation gate:** each suite preserves its complete typed decisions,
exact routes or dispositions, positive and negative canonical text, legacy
source closure, and accepted-plan claims. Package and edge rows transition
together to `accepted`; all five checker paths and live references are absent;
focused suites, package and edge authority, 57 engine tests, all declarative
suites, graph freshness, both plan checks, diff integrity, and one complete
mixed checkpoint pass.

**Implementation summary:** Five registered declarative suites now replace the
five admitted Bash checkers and preserve all 69 typed decisions and 26 exact
dispositions. The Core simplicity and Resilience README routes name canonical
suite identities. All 12 row-15 and execution-train edges remain independent
historical lifecycle gates; no false suite dependency, wrapper, bridge, alias,
compatibility schema, inferred decision, or weaker evidence was introduced.

**Implementation verification:** all five focused suites plus package and edge
authority passed; all 57 engine tests and all 77 declarative suites passed;
graph freshness passed at 199 Bash verifiers / 204 nodes / 933 edges / 200
components; diff integrity and the complete mixed checkpoint passed all 199
surviving entrypoints.

##### Post-Wave-5 Re-Plan: Explicit Edge-Free Packages

**Status:** `Accepted`

The fresh graph exposes a connected ten-checker wave whose six semantic child
checkers have exactly zero outgoing executable edges. Omitting edge-contract
participation would weaken explicit package proof; inventing manifest rows
would falsify the generated graph; and treating semantic dependencies as
independent gates would violate the no-fallback rule.

**Decision:** extend the existing generic edge assertion with a configured
`edge-free` token. Every newly admitted checker package must use exactly one of
`edge-dispositions` or `edge-free`. Edge-free packages prohibit disposition
rows, require zero generated executable edges, require their checker while
admitted, and require checker absence when accepted. Edge packages retain the
existing exact non-empty historical manifest contract.

**Allowed write set:** the generic edge check, focused tests, its declarative
configuration, engine documentation, this plan and ledger, issues and inventory
report, and the parent plan. No package, policy, fixture, checker, registry,
generated graph, compatibility schema, wrapper, bridge, or alias may change.

**Acceptance gate:** focused mode, edge-presence, row-presence, admitted-source,
and accepted-source tests; all engine tests and declarative suites; graph
freshness; both plan checks; diff integrity; and one complete mixed checkpoint.

**No-fallback rule:** no inferred edge-free state, empty edge-disposition mode,
fabricated edge, optional participation, historical-row deletion, package
exception, or silent success.

**Verification:** all 20 focused edge tests and all 62 engine tests passed; all
77 declarative suites passed; graph freshness remained 199 Bash verifiers /
204 nodes / 933 edges / 200 components; both plan checks and diff integrity
passed; and the complete mixed checkpoint passed all 199 entrypoints.

##### Wave 6 Admission: Connected Contracts, Diagnostics, And Verification

**Status:** `Accepted`

**Packages:** ten checker packages form four owner-coherent closures: Contracts
planning boundary plus row 29; Contracts artifact selection and semantic
preservation plus row 30; Diagnostics owner and activity context plus row 31;
and Verification ownership plus GUI smoke evidence.

**Frozen behavior:** 69 typed decisions and 18 exact dispositions, exact row
29/30/31 decomposition and owner-validation projections, canonical Contracts,
Diagnostics, and Verification evidence, legacy mechanism prohibitions, Router
and reference routes, and accepted parent-plan claims.

**Package modes:** the six semantic child packages are explicitly `edge-free`.
The three row packages and GUI smoke package classify all 24 current executable
reference and verifier-dependency rows. Six same-owner relationships must
become registered `suite-requires` edges at acceptance; execution train,
Launcher population, row 14, and their duplicate graph edge kinds remain six
independent historical gates.

**Shared serial integration:** register ten separate suites; replace GUI smoke
and Verification owner README routes; replace the Diagnostics owner checker
identity in row 35 with its suite identity; reconcile row-35 dependency and
direct-route totals from 26/24 to 25/23 while preserving transitive/computed
counts at 1/1 and consumers at 33; accept package and edge state together;
delete ten checkers; regenerate the graph; and update serial plan records.

**Implementation write set:** ten suite TOMLs and ten deleted checker paths;
unchanged fixtures, decomposition, owner-validation, disposition, and canonical
policy files as read-only evidence; registry, package and edge manifests,
package contract, README, row-35 dependency data and checker, generated graph,
and serial plan records.

**No-fallback rule:** no policy, fixture, disposition, canonical source,
metadata, Router, execution train, Launcher population, row 14, engine,
compatibility schema, wrapper, bridge, alias, duplicate authority, inferred
outcome, false independent gate, or weaker evidence may be added or changed.

**Acceptance gate:** ten focused suites, package and edge authority, exact six
registry dependencies, README and row-35 lifecycle closure, all engine tests
and declarative suites, graph freshness, both plan checks, diff integrity, and
one complete mixed checkpoint after all ten Bash paths are absent.

**Admission verification:** package and edge authority, all 62 engine tests,
all 77 declarative suites, graph freshness at 199 Bash verifiers / 204 nodes /
965 edges / 200 components, both plan checks, diff integrity, and all 199 mixed
entrypoints pass before implementation.

**Implementation:** four disjoint owner closures produced ten registered
declarative suites. Row 29 requires Contract Planning Boundary; row 30 requires
Contract Artifact Selection and Contract Semantic Preservation; row 31
requires Diagnostics Owner Contract and Diagnostics Activity Context; and GUI
Smoke Evidence requires Verification Ownership. All six relationships are
real registry dependencies, while execution train, Launcher population, and
row 14 remain independently registered lifecycle gates.

The two README routes now name suite identities. The Bash-only row-35
Diagnostics identity is removed, with dependency/direct-route counts accepted
at 25/23 and transitive/computed/consumer counts preserved at 1/1/33. All ten
Bash paths are absent; package and edge state transitioned atomically to
`accepted`; no wrapper, alias, bridge, compatibility schema, or alternate
execution path remains.

**Deviation:** the generic text primitive rejects the two former
Contracts duplicate-heading literals anywhere, while the deleted Bash checks
anchored them at line start. This conservative check cannot make invalid
duplicate authority valid and avoids a policy-specific regex primitive. It is
recorded as VE032. A bulk state edit briefly duplicated the package
state-domain value; focused typed validation rejected it before acceptance,
and the domain remains exactly `admitted | accepted | blocked`. Final plan
review also found Wave 3 still labeled `Active` despite its accepted
implementation and evidence; VE033 records the bookkeeping correction to
`Accepted`.

**Verification:** all 12 focused replacement/authority suites, all 62 engine
tests, all 87 declarative suites, row-35 lifecycle, graph freshness, both plan
checks, and diff integrity passed. The regenerated graph contains 189 Bash
verifiers / 194 nodes / 910 edges / 190 components. The complete mixed
checkpoint passed all 189 surviving entrypoints.

##### M6-K1 Re-Plan: Module Metadata Graph

**Decision status:** `Accepted`

**Package status:** `Accepted`

The metadata audit found that the canonical schema advertised module IDs or
rule IDs in `Specializes`, while every live specialization names a module, the
Bash validator resolves only modules, and no canonical current-rule identity
registry exists. The generated `STD-*` owner map is migration bookkeeping for
legacy sections and cannot authorize current rule-level precedence.

**Decision:** `Specializes` is module-level in the current schema. It names
canonical module IDs whose generic obligations remain authoritative while a
selected profile supplies narrower mechanisms. It does not grant blanket
override authority. Rule-level specialization is unsupported until a future
version introduces namespaced stable rule IDs, canonical ownership, routing,
and cycle semantics through a separately admitted plan.

`Requires` is an inclusion edge and `Specializes` is a precedence edge. Each
target must resolve to exactly one selected module; only profiles may declare
specialization. Reject self-edges, duplicate IDs, malformed lists, unresolved
targets, relation cycles, and cycles in the combined relation graph with typed
diagnostics. Do not infer rule targets, consult the legacy owner map, or fall
back from an unresolved specialization to prose or file order.

**Exact grammar:** all nine metadata fields occur exactly once as line-oriented
Markdown entries. Symbolic fields (`ID`, `Role`, `Level`, and
`Canonical owner`) contain exactly one backticked token. Relation fields
(`Requires` and `Specializes`) contain individually backticked module IDs
separated by commas and optional surrounding ASCII spaces, or exactly the
single token `none`; empty, duplicate, unquoted, or mixed-`none` items are
invalid. Prose fields (`Applies when`, `Does not apply when`, and
`Verification`) preserve their complete non-empty Markdown value, including
embedded inline code, without global backtick removal or outer-code
normalization. Module IDs retain the lowercase dot-separated grammar.
Canonical owner is a normalized repository-relative path equal to the
declaring file.

**Proposed first implementation boundary:** add one side-effect-free typed
Python check and focused tests; add specialization and combined-cycle fixtures
missing from the Bash corpus; register one declarative metadata fixture suite;
migrate and delete only `verify-metadata-fixtures.sh`. The shared
`check-metadata.sh` and its 52 semantic consumers remain unchanged until later
exact owner-coherent waves. Migrated suites may not execute the helper through
a bridge, wrapper, alias, or command action.

**Proposed implementation write set:** metadata schema and information
architecture wording; metadata fixtures; metadata check module, parser
registration, and focused engine tests; metadata suite and registry; fixture
checker deletion; package, edge, generated graph, README, plan, issue, report,
and ledger integration artifacts required by the admitted package. Canonical
modules, legacy owner maps, the shared helper, its 52 consumers, unrelated
suites, lockfiles, and configuration remain unchanged.

**Admission gate:** freeze one package subject for the fixture checker, classify
every current executable edge, name exact replacement evidence, and pass
package/edge authority, graph freshness, engine tests, declarative suites, both
plan checks, diff integrity, and the complete mixed checkpoint with no policy,
fixture, engine, registry, generated graph, or Bash deletion beyond admission
bookkeeping.

**Admission:** package `M6-K1` exclusively owns the fixture-checker subject and
the proposed implementation write set. Its exact current executable-reference
and helper-dependency edges both target the shared metadata helper and are
classified as a retained external-owned artifact for 52 later consumers. The
helper is not replacement execution for the new suite and remains excluded from
this package's write set.

**Admission evidence:** package and edge authority passed with one admitted
package and two exact retained-artifact edges; all 62 engine tests and all 87
declarative suites passed; graph freshness passed at 189 Bash verifiers / 194
nodes / 914 edges / 190 components; both plan checks and diff integrity passed;
and the complete mixed checkpoint passed all 189 entrypoints.

**VE036 re-plan decision:** the strict implementation passed all 20 focused
engine tests, then a read-only audit of all 57 live canonical modules found
`reference/recipes/diagnostics.md` declares `Level: ADVISORY`. The schema,
information architecture, legacy metadata helper, and new primitive permit
only `REFERENCE` for a `reference` module. This is isolated existing corpus
non-compliance, not replacement drift.

Resolve the defect first as a separate Diagnostics-owned correction. Its exact
implementation write set is `reference/recipes/diagnostics.md`, the existing
`diagnostics-owner-contract` and `diagnostics-activity-context` suite files,
this plan, its issue register, metadata audit, execution ledger, and the parent
plan cursor. Change only the level token and add exact positive level evidence
to both suites that already consume the reference. Verify both owner suites,
the legacy metadata helper over the reference's complete dependency closure,
all declarative suites, plan structure, graph freshness, and diff integrity.
No metadata schema, helper, fixture, engine, registry, package manifest,
generated graph source, canonical Diagnostics policy, or unrelated reference
content may change. This correction neither broadens nor accepts M6-K1.

The paused M6-K1 source and test work remains isolated until this prerequisite
is committed. Afterward restore it, preserve this decision, rerun the 57-module
audit, and continue the admitted implementation. Do not add `ADVISORY`, accept
both values, omit the invalid module, normalize it silently, or merge the
cross-owner correction into the metadata-kernel package.

**VE036 acceptance:** `reference/recipes/diagnostics.md` now uses the canonical
`REFERENCE` level, and both existing Diagnostics suites assert that exact
metadata token. The owner suites and legacy metadata helper over Core,
Verification, Contracts, Diagnostics, and the reference dependency closure
pass. No schema, helper, engine, registry, package, fixture, canonical
Diagnostics policy, or unrelated reference content changed. M6-K1 remains
admitted and resumes only after this correction's atomic commit.

**Implementation result:** the engine now has one side-effect-free
`metadata_graph` check with mutually exclusive direct-graph and exact
fixture-corpus modes. It preserves prose, enforces field-specific symbolic and
relation grammar, validates canonical owner and role/level contracts, resolves
module relations exactly, and reports self-edges plus `Requires`,
`Specializes`, and combined cycles with typed diagnostics. Twenty focused tests
and nineteen registered corpus cases cover positive workflow/profile graphs
and every admitted negative behavior.

The canonical schema and information architecture now define module-level
specialization without blanket override authority. The registered
`metadata-fixtures` suite replaces the deleted fixture checker directly; it
does not execute the shared metadata helper. The helper and all 52 semantic
consumers remain unchanged for later owner-coherent migration. Package and edge
authority pass with M6-K1 accepted and its two historical helper edges absent
from the regenerated graph.

**Acceptance evidence:** the focused metadata suite, package and edge
authority, all 82 engine tests, all 88 declarative suites, strict validation of
all 57 live canonical modules, graph freshness at 188 Bash verifiers / 193
nodes / 909 edges / 189 components, both plan checks, removed-path proof, diff
integrity, and all 188 mixed entrypoints pass. The package is accepted and the
fixture checker is absent.

**Implementation gate after admission:** focused parser/graph tests cover every
typed diagnostic; the positive corpus and every negative fixture pass through
the registered suite; package and edge authority prove the deleted checker has
one native replacement and no unresolved edge; all engine tests and
declarative suites, graph freshness, both plan checks, diff integrity, and one
complete mixed checkpoint pass.

**Re-plan triggers:** stop if a live rule-level target exists; a canonical rule
registry is required; module-only semantics would weaken a profile contract;
combined-cycle rejection invalidates an intended current graph; exact grammar
cannot represent current metadata; or the first package must edit a semantic
consumer of `check-metadata.sh`.

##### M6-K2: Release Reference Closure

**Package status:** `Accepted`

The post-kernel graph has 52 remaining metadata-helper consumers. Twenty have
zero executable inbound callers. `verify-release-reference-closure.sh` is the
smallest owner-coherent candidate: it has zero executable inbound callers,
zero contract references, one node in an acyclic component, and only the
metadata helper as an executable dependency.

**Owner and behavior:** `reference/recipes/releases.md` owns the non-normative
Release Recipe closure. The checker proves exact frozen inventory IDs
`STD-0541` and `STD-0542`, exact move dispositions and rationales, the complete
selected metadata graph through Core, Verification, Contracts, Release, and
the recipe, required workflow/recipe/index links, non-normative recipe wording,
and the complete concise legacy Release index with no residual policy or
executable recipe authority.

**Declarative replacement:** use existing `table` checks for exact inventory
and disposition projections, one direct `metadata_graph` check for the selected
module graph, `text` checks for canonical links and recipe wording, and
`exact_text` for the complete legacy index. No new engine primitive, fixture,
canonical source edit, schema change, regex approximation, helper call, command
action, wrapper, alias, compatibility path, or fallback is admitted.

**Exact implementation write set:** package and edge manifests, suite registry,
package authority suite, new `release-reference-closure` suite, deleted checker,
evaluation README route, generated checker graph artifacts, this plan, its
ledger/issues/inventory report, and the parent-plan cursor. Core, Verification,
Contracts, Release Workflow, Release Recipe, legacy Release index, frozen
section inventory, consolidation dispositions, helper, other consumers, engine,
fixtures, lockfiles, and unrelated files are read-only evidence.

**Edge disposition:** both exact current edges target the shared metadata
helper and remain classified as a retained external-owned artifact. The new
suite validates metadata natively and does not execute the helper. Accepted
state requires the checker and both graph edges to be absent while the helper
remains for other owners.

**Admission evidence:** package `M6-K2` and its two exact helper edges are
admitted. Implementation may begin only after package/edge authority, graph
freshness, both plan checks, declarative suites, diff integrity, and the mixed
checkpoint pass with no implementation file changed.

**Re-plan triggers:** stop if exact legacy-index bytes conflict with an intended
current index; the two frozen identifiers or dispositions do not match their
accepted source ownership; a canonical source must change; another executable
or contract inbound edge exists; or existing primitives cannot preserve one of
the checker's observable claims without weakening it.

**Implementation result:** the registered `release-reference-closure` suite
uses six side-effect-free checks for exact frozen inventory and dispositions,
the complete direct metadata graph, canonical recipe and workflow evidence,
and the byte-exact legacy Release index. It does not execute the retained
metadata helper. The Bash checker is deleted, both historical helper edges are
accepted and absent, and package authority records one canonical declarative
replacement without a wrapper, alias, compatibility path, or fallback.

**Acceptance evidence:** the focused six-check suite, package and edge
authority, all 89 declarative suites, graph freshness at 187 Bash verifiers /
192 nodes / 907 edges / 188 components, both plan checks, README route,
removed-path proof, diff integrity, and all 187 mixed entrypoints pass.
Canonical sources, frozen inventory and dispositions, helper, engine, fixtures,
and the other 51 helper consumers remained unchanged.

##### M6-K3: Release Recovery Policy

**Package status:** `Accepted`

The post-M6-K2 graph has 51 remaining metadata-helper consumers. Five have zero
executable inbound callers and zero contract references; all are Release-owned
and depend only on the helper. `verify-release-recovery-policy.sh` is the
smallest at 113 lines and forms one acyclic owner-local component.

**Owner and behavior:** `workflows/release.md` owns recovery and withdrawal.
The checker proves the six-row all-required recovery decision, exact frozen
inventory IDs `STD-0577` through `STD-0581`, exact move dispositions and
rationales, the Core/Verification/Contracts/Release metadata graph, required
recovery rules and typed diagnostics, removal of provider/registry/branch/
patch-version/consensus/changelog defaults, and non-authoritative legacy-index
routing.

**Declarative replacement:** use the existing `decision` primitive for the
explicit Boolean contract, `table` projections for exact inventory and
dispositions, one direct `metadata_graph`, and `text` for canonical and
removed workflow rules. Register `release-reference-closure` as a suite
dependency so its stronger byte-exact legacy-index proof replaces the old
checker's weaker route and heading assertions without duplicated authority.
No new primitive, fixture, source edit, helper call, regex approximation,
wrapper, alias, compatibility path, command action, or fallback is admitted.

**Exact implementation write set:** package and edge manifests, suite registry,
package authority suite, new `release-recovery-policy` suite, deleted checker,
evaluation README route, generated checker graph artifacts, this plan, its
ledger/issues/inventory report, and the parent-plan cursor. The recovery
fixture, Core, Verification, Contracts, Release Workflow, legacy Release
index, frozen inventory, dispositions, accepted Release Reference suite,
helper, other consumers, engine, lockfiles, and unrelated files are read-only.

**Edge disposition:** both exact current edges target the shared metadata
helper and remain a retained external-owned artifact. The replacement suite
validates metadata natively and depends only on the registered declarative
Release Reference suite. Accepted state requires the checker and both helper
edges to be absent while the helper remains for other owners.

**Admission evidence:** package M6-K3 and both exact helper edges are admitted.
Implementation begins only after package/edge authority, graph freshness, both
plan checks, all declarative suites, diff integrity, and the complete mixed
checkpoint pass with no implementation file changed.

**Re-plan triggers:** stop if the Boolean fixture cannot be represented exactly;
the five frozen identifiers or dispositions disagree with their accepted
owners; a canonical source or fixture must change; another executable or
contract inbound edge exists; the suite dependency creates a cycle or competing
legacy authority; or existing primitives would weaken an observable claim.

**Implementation result:** the registered `release-recovery-policy` suite
uses one exact Boolean decision, exact inventory and disposition projections,
one direct metadata graph, and canonical/removed workflow text. Its registered
dependency executes the accepted byte-exact Release legacy-index proof once.
The suite does not call the metadata helper. The Bash checker and both helper
edges are absent, with no wrapper, alias, compatibility path, command action,
duplicated legacy authority, or fallback.

**Acceptance evidence:** the focused dependency closure, package and edge
authority, all 90 declarative suites, graph freshness at 186 Bash verifiers /
191 nodes / 905 edges / 187 components, both plan checks, README route,
removed-path proof, read-only-source proof, and diff integrity pass. The mixed
Bash checkpoint is intentionally deferred to M6-K-W1 closure under VE037;
commit `4a39062` supplies the wave's passing 187-entrypoint opening baseline.
Canonical and legacy sources, the recovery fixture, frozen inventory and
dispositions, helper, engine, accepted dependency suite, and the other 50
helper consumers remained unchanged.

##### VE037: Wave-Scoped Mixed Bash Checkpoints

**Status:** `Accepted`

The acceleration contract already requires focused verification per package
and one complete mixed suite per integrated wave or shared-contract change.
Package rows continued to require `complete-suite`, causing each admission and
implementation to spend roughly nine minutes re-executing the same transitive
Bash closures. That stale row-level ceremony is removed for M6-K-W1 and future
waves; accepted historical evidence is not rewritten.

Every package still requires its focused registered dependency closure,
package/edge authority, all declarative suites, graph freshness, both plan
checks, route/removal/diff evidence, and exact read-only-source proof. Run a
surviving Bash checker between wave checkpoints only when generated executable
or contract edges prove that changed package evidence reaches it. Run the full
mixed suite once at wave closure and immediately around shared engine, helper,
launcher, metadata-schema, edge-contract, or routing-contract changes.

M6-K-W1 opens from commit `4a39062`, whose admitted state passed all 187 mixed
entrypoints. It contains M6-K3 and no more than the four other currently
inbound-safe Release-owned helper consumers. Close the wave after those
packages, or earlier if an inbound edge, ownership conflict, shared-contract
change, unexpected retained-Bash consumer, or focused/declarative failure
appears. The closing checkpoint validates the integrated deletions once.

##### M6-K4 Through M6-K7: Release Wave Remainder

**Package status:** `M6-K4 and M6-K5 Accepted; M6-K6 and M6-K7 Admitted`

##### M6-DM1: Multi-Output Decision Contract

**Package status:** `Accepted`

**Trigger:** M6-K6 owns one five-row scenario matrix with three independently
typed outputs: SBOM, checksum, and lockfile. The current generic `decision`
check requires one configured expected column at the end of the table. It
cannot evaluate the first two outputs without duplicating the fixture,
collapsing outputs into a combined string, weakening them to snapshot rows, or
changing the engine. M6-K6's admitted contract prohibits those substitutions
and requires typed unavailable for unresolved lockfile ownership.

**Decision:** extend the canonical `decision` check with one mutually exclusive
multi-output form. It requires an exact ordered `input_columns` list and at
least two `[[checks.outputs]]` entries. Each output declares exactly `column`,
`default`, and one or more ordered `rules`. The table header must equal `case`,
then the declared inputs, then the declared output columns. Domains must still
cover every column exactly. Output columns are unique, cannot be predicate
inputs, and each default and rule outcome must belong to that output's domain.
Every output is evaluated independently in declaration order and mismatch
diagnostics identify both case and output column.

The existing single-output form remains the canonical compact representation
for one output and retains its exact schema and final-column contract. A check
must use exactly one form; mixed forms, inferred inputs, one-entry multi-output
forms, output-to-output predicates, duplicate inputs/outputs, unlisted columns,
empty rules, unknown keys, and malformed domains are typed invalid. There is no
schema fallback, topic callback, executable action, fixture normalization, or
implicit output derivation.

**Implementation write set:**

- `tools/standards_verifier/standards_verifier/checks/decision.py`;
- `tools/standards_verifier/tests/test_engine.py`;
- `tools/standards_verifier/README.md`;
- `docs/plans/standards-verification-engine/reports/architecture.md`;
- this plan, ledger, issues, inventory report, and parent plan.

All suites, fixtures, registry entries, standards sources, checker/package/edge
manifests, generated inventories, Bash files, helper files, lockfiles, and
unrelated engine modules remain read-only. M6-K6 consumes the accepted
capability in a later package commit; M6-DM1 does not alter policy evidence or
delete a checker.

**Focused evidence:** add pass coverage with three outputs including a typed
unavailable result; independent mismatch diagnostics naming the output;
single-output regression coverage; mixed-form, one-output, duplicate-column,
header-order, undeclared-predicate, default-domain, and rule-domain rejection;
and existing missing/path/domain/row diagnostics. Run focused and complete
engine tests, all declarative suites, compilation, graph freshness, both plan
checks, diff/read-only evidence, and the mixed checkpoint immediately before
and after this shared-contract implementation. Resume M6-K6 fast package gates
only after M6-DM1 acceptance.

**No-fallback rule:** do not split or copy the artifact fixture, encode a
combined output, use expected output columns as rule inputs, retain Bash as an
alternate evaluator, silently select one output, or weaken semantic decisions
to exact-row snapshots.

**Admission evidence:** all 92 declarative suites, graph freshness at 184 Bash
verifiers / 189 nodes / 907 edges / 185 components, both plan checks, diff
integrity, and the complete 184-entrypoint mixed opening checkpoint pass. No
engine, test, documentation contract, suite, fixture, registry, policy,
checker, helper, manifest, or generated graph file changed during admission.

**Acceptance evidence:** the canonical `decision` primitive now parses one
multi-output matrix once, validates exact declared inputs and output contracts,
isolates every output's predicates/default/rules, and emits output-specific
mismatch diagnostics. Ten focused multi-output cases plus all existing tests
pass for 92 engine tests total. All 92 declarative suites, Python compilation,
graph freshness at 184 Bash verifiers / 189 nodes / 907 edges / 185 components,
both plan checks, diff/read-only evidence, and all 184 closing mixed entrypoints
pass. No suite, fixture, registry, policy, checker, helper, package/edge
manifest, generated graph, lockfile, or unrelated engine module changed.

After M6-K3, Maintenance, Pipeline, Artifact, and Publication remain separate
acyclic one-node components with zero executable inbound callers, zero contract
references, and only the shared metadata helper dependency. They share the
Release Workflow owner, direct metadata closure, accepted byte-exact legacy
index dependency, read-only source set, package gates, and M6-K-W1 checkpoint,
but retain separate semantic contracts and atomic implementation commits.

| Package | Direct contract | Frozen IDs | Special behavior |
| --- | --- | --- | --- |
| M6-K4 Maintenance | six-row all-required maintenance/channel decision | `STD-0561` through `STD-0565` | removes fixed branches, durations, channel names, and feature-flag defaults |
| M6-K5 Pipeline | six-row all-required authenticated handoff decision | `STD-0552` through `STD-0560` | preserves three exact removals and removes provider workflow/target defaults |
| M6-K6 Artifact | five-row SBOM/checksum/lockfile decisions | `STD-0543` through `STD-0551` | three decision checks; unresolved resolution ownership is typed unavailable |
| M6-K7 Publication | six-row all-required publication decision | `STD-0566` through `STD-0574` | preserves move/merge/remove dispositions and removes hosted-product examples |

**Declarative replacements:** every suite uses exact decision domains and
outcomes, exact inventory and disposition projections, direct
`metadata_graph`, and canonical/removed workflow text. Each registers
`release-reference-closure` as its sole suite dependency for stronger
byte-exact legacy-index evidence. No fixture, primitive, engine branch,
canonical source, legacy source, helper call, regex approximation, wrapper,
alias, compatibility path, command action, or fallback is admitted.

**Write ownership:** each package owns only its new suite and deleted checker.
Package/edge manifests, registry, package authority, README, generated graph,
this plan/ledger/issues/report, and parent cursor remain serial integration
files. All four fixtures; Core, Verification, Contracts, Release Workflow and
legacy Release index; frozen inventory/dispositions; accepted suites; helper;
engine; other consumers; lockfiles; and unrelated files are read-only.

**Edge and verification contract:** each package admits exactly one executable
reference and one helper dependency to the retained external-owned metadata
helper. Implement M6-K4, K5, K6, then K7. For each, run focused dependency
closure, package/edge authority, all declarative suites, graph and plan checks,
route/removal/diff/read-only evidence, and any graph-proven affected retained
Bash checker. Run the mixed Bash suite once after M6-K7 closes M6-K-W1.

**Re-plan triggers:** stop if any inbound or cross-package edge appears; owner
semantics overlap rather than compose; exact fixtures/IDs/dispositions cannot
be represented; Artifact cannot preserve typed unresolved ownership; a source,
fixture, engine, helper, or accepted suite must change; or a retained Bash
consumer is affected but absent from package verification.

**M6-K4 result:** the registered `release-maintenance-policy` suite preserves
the six-row decision, five exact IDs/dispositions, direct metadata closure,
canonical maintenance/channel rules, and removed defaults, with the accepted
byte-exact index dependency. The checker and both helper edges are absent.
Focused dependency closure, package/edge authority, all 91 declarative suites,
graph freshness at 185 Bash verifiers / 190 nodes / 912 edges / 186 components,
both plan checks, route/removal/diff/read-only evidence pass. The mixed
checkpoint remains deferred to M6-K-W1 closure.

**M6-K5 result:** the registered `release-pipeline-policy` suite preserves the
six-row authenticated immutable handoff decision, nine exact IDs and
dispositions, direct metadata closure, required-artifact failure behavior,
least-privilege publication handoff, and removed provider trigger/matrix
recipes, with the accepted byte-exact index dependency. The checker and both
helper edges are absent. Focused dependency closure, package/edge authority,
all 92 declarative suites, graph freshness at 184 Bash verifiers / 189 nodes /
907 edges / 185 components, both plan checks, route/removal/diff/read-only
evidence pass. The mixed checkpoint remains deferred to M6-K-W1 closure.

**M6-K6 result:** the registered `release-artifact-policy` suite parses the
single five-row matrix once and preserves independent SBOM, checksum, and
lockfile outcomes, including typed unavailable when lockfile ownership cannot
be resolved. It also preserves nine exact IDs/dispositions, direct metadata
closure, canonical artifact/reproducibility policy, and removed legacy
defaults through the accepted byte-exact index dependency. The checker and
both helper edges are absent. Focused dependency closure, package/edge
authority, all 93 declarative suites, graph freshness at 183 Bash verifiers /
188 nodes / 902 edges / 184 components, both plan checks, and
route/removal/diff/read-only evidence pass. Forty-seven helper consumers
remain; the mixed checkpoint remains deferred to M6-K-W1 closure.

**M6-K7 and M6-K-W1 result:** the registered
`release-publication-policy` suite preserves the six-row all-required
publication decision, nine exact move/merge/remove dispositions, direct
metadata closure, canonical provider-neutral presentation, and removal of
hosted-service/product defaults through the accepted byte-exact index
dependency. The checker and both helper edges are absent. Focused dependency
closure, package/edge authority, all 94 declarative suites, graph freshness at
182 Bash verifiers / 187 nodes / 897 edges / 183 components, both plan checks,
and route/removal/diff/read-only evidence pass. The one M6-K-W1 closing mixed
checkpoint passed all 182 remaining Bash entrypoints. Forty-six metadata-helper
consumers remain. No later package is admitted; a fresh dependency and
ownership audit is required before implementation continues.

#### M6-L1 Through M6-L7 Inbound-Free Leaf Wave

**Goal:** Replace the seven remaining metadata-helper consumers that have zero
executable inbound callers and zero non-metadata executable dependencies while
preserving their independent owners, exact lifecycle evidence, and one bounded
wave checkpoint.

**Admission evidence:** the fresh graph contains 46 metadata-helper consumers.
Exactly seven are executable leaves after excluding the helper: Documentation
Changelog, Documentation Reference, Release Workflow Foundation, Rust
Dependency Owner, Rust Release Owner, Rust Tooling Owner, and Rust Dependency
Candidate Inspection. Each has only the metadata helper as executable output.
All seven are named by frozen lifecycle inventories but none is an executable
prerequisite of another checker.

| Package | Owner | Direct contract | Lifecycle transfer |
| --- | --- | --- | --- |
| M6-L1 | Release Workflow | 16 exact changelog dispositions and canonical changelog policy | remove one row-35 dependency |
| M6-L2 | Documentation Reference | 24 exact reference dispositions and non-normative recipe boundary | remove one row-35 dependency |
| M6-L3 | Release Workflow | release/changelog two-output decision and ten exact dispositions | remove one row-35 dependency |
| M6-L4 | Rust Dependency profile | 14 typed mechanism decisions and one exact index disposition | remove row-35 dependency and consumer rows |
| M6-L5 | Rust Release profile | 16 typed mechanism decisions and one exact index disposition | remove row-35 dependency and consumer rows |
| M6-L6 | Rust Tooling profile | 16 typed mechanism decisions and one exact index disposition | remove row-35 dependency and consumer rows |
| M6-L7 | Rust Dependency profile | 14 typed inspection decisions and three exact dispositions | remove one row-35 consumer and replace one source-preparation checker subject with suite evidence |

**Declarative contract:** existing decision, multi-output decision, table,
metadata-graph, and text checks represent all seven behaviors. No engine,
fixture, canonical source, legacy source, helper, compatibility schema,
wrapper, command action, regex approximation, or fallback is admitted.

**Lifecycle contract:** removing a checker also removes its exact row-35
dependency/consumer records and updates only the fixed counts and diagnostics
that describe those records. M6-L7 replaces its source-preparation
`checker:` subject with its registered `suite:` subject. These are
data-lifecycle reconciliations under the existing schema, not schema or
semantic changes. Any required change to allowed values, columns, ownership,
or interpretation is a shared-contract re-plan trigger.

**Concurrency and integration:** package authors may prepare only their
exclusive suite and checker paths in isolated worktrees. Fixtures, policy,
engine, helper, and shared lifecycle files remain read-only to package authors.
The integration owner applies registry, README, package/edge authority,
row-35/source-preparation reconciliation, generated graph, and plan records
serially in M6-L1 through M6-L7 order.

**Verification:** each package runs its focused dependency closure, package and
edge authority, affected row-35/root-audit/source-preparation checks, all
declarative suites, graph freshness, both plan checks, route/removal/diff and
read-only evidence. The mixed Bash suite runs once after M6-L7 closes
M6-L-W1. A schema, helper, engine, router, or lifecycle-meaning change requires
an immediate shared-contract checkpoint instead.

**Re-plan triggers:** stop if a candidate gains an executable caller or
non-metadata dependency; exact lifecycle rows cannot be removed with the
checker; a fixture or source must change; existing primitives cannot preserve
typed outcomes or exact evidence; package paths overlap outside serial
integration files; M6-L7 cannot transfer source-preparation authority directly
to a registered suite; or a lifecycle schema/meaning change is required.

**M6-L1 result:** the registered `documentation-changelog-closure` suite
preserves 16 exact inventory/disposition rows, direct Release metadata closure,
all canonical changelog requirements, the three-route Documentation index, and
negative evidence against seven former headings plus fixed-format/stale
examples. The Bash checker, both helper edges, and its exact row-35 dependency
are absent. Row-35 reconciliation passes at 24 dependencies / 22 direct route
dependencies / 33 consumers. All 95 declarative suites and graph freshness at
181 Bash verifiers / 186 nodes / 914 edges / 182 components pass. Forty-five
metadata-helper consumers remain; the mixed checkpoint remains deferred to
M6-L-W1.

**M6-L2 result:** the registered `documentation-reference` suite preserves
24 exact inventory/reference-disposition rows, native metadata closure, the
non-normative recipe boundary, legacy routing, and negative evidence against
blanket API, table-alignment, algorithm-template, and former-section rules.
The Bash checker, both helper edges, and its exact row-35 dependency are
absent. Row-35 passes at 23 dependencies / 21 direct route dependencies / 33
consumers. All 96 declarative suites and graph freshness at 180 Bash verifiers
/ 185 nodes / 908 edges / 181 components pass. Forty-four metadata-helper
consumers remain; the mixed checkpoint remains deferred to M6-L-W1.

**Tasks:**

- [x] Generate exact dependency closures before package admission; a package
  must include or already have declarative versions of every semantic
  prerequisite and every Bash caller that would otherwise reference a deleted
  verifier.
- [x] Admit non-overlapping owner-coherent packages per accelerated wave only
  where their owner, dependency set, semantic decision, fixture family, and
  verification contract are frozen; bound size by semantic review and
  write-set overlap rather than an arbitrary package count.
- [ ] Permit concurrent package preparation only in isolated worktrees with
  disjoint suite, fixture, and deleted-checker paths; keep registry, package
  manifest, README, generated graph, and plan integration serial.
- [x] Run focused verification for every package and the complete suite once at
  each integrated wave boundary or shared-contract change.
- [ ] Review each exception for a missing reusable primitive, bad test design,
  historical-only assertion, or genuinely custom algorithm.
- [ ] Add reusable primitives only when at least two coherent owners require
  them or one safety-critical invariant cannot otherwise be expressed clearly.
- [ ] Keep any custom check typed, side-effect-free, implemented in Python,
  registered, directly tested, and owned.
- [ ] Remove every Bash verifier and verification helper after its accepted
  replacement or reviewed retirement.
- [ ] Replace and delete the Bash migration launcher with the final Python
  engine command.

**Acceptance gate:** Exact inventory reports zero Bash verifiers, verification
helpers, or launchers; the Python engine-only full suite passes; no transitive
execution graph, arbitrary command action, or duplicate authority remains.

**Status:** `Planned`

### Milestone 7: Documentation And Objective Acceptance

**Goal:** Make suite authoring, focused execution, diagnostics, and maintenance
clear, then prove the objective against the final repository.

**Allowed write set:** engine documentation/examples, final inventory/report,
this plan/ledger/issues, and parent migration references.

**Tasks:**

- [ ] Document dependency satisfaction, suite schema, assertion catalog,
  diagnostics, focused execution, and extension criteria.
- [ ] Compare final script count, process graph, runtime, and maintenance
  surface with the baseline.
- [ ] Run every objective acceptance claim and record residual limitations.

**Acceptance gate:** A1-A6 are satisfied with linked evidence and both plans
identify one current verification authority.

**Status:** `Planned`

## Blockers

- `none`

## Re-Plan Triggers

- Python 3.11+ cannot be declared and satisfied in supported verification
  environments without adding an unacceptable provisioning or release burden.
- A required invariant needs arbitrary command execution, dynamic code, or a
  policy-specific engine branch rather than a bounded reusable check.
- Migration evidence shows TOML/TSV cannot represent suites legibly enough for
  maintainers to review policy and outcomes.
- A migrated suite loses accepted negative, disposition, ownership, typed
  outcome, route, or source-closure evidence.
- Engine or registry work overlaps an unrelated dirty shared-authority file.
- The complete mixed suite cannot run without treating a removed checker as a
  compatibility fallback.

## Concurrent Work

| Owner | Primary write set | Adjacent write set | Forbidden/shared | Output/report | Integration order |
| --- | --- | --- | --- | --- | --- |
| Assertion-family analyst | Read-only checker/fixture families | none | Engine, registry, plans, inventory | Proposed family map | Before inventory integration |
| Suite package author | One frozen suite/config/fixture package | Its replaced checker | Engine, registry, plans, shared helpers | Patch plus behavior/evidence report | After required primitives |
| Engine integration owner | Engine, registry, inventory, plans | Shared helpers and launcher | none | Accepted serial transition | Dependency order |

Parallel package work requires frozen configuration schema, non-overlapping
suite/checker/fixture paths, no shared dependency change, and fresh revision
admission. Shared contracts and registry integration remain serial.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Active`
