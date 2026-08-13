# Plan: Generic Standards Verification Engine

**Plan status:** `Active`

**Current phase:** Milestone 6: M6-U0 semantic-wave preflight

**Next slice:** preflight the twelve owner-separated semantic candidates and
admit only owner-coherent packages whose native declarative suites preserve
their exact evidence contracts.

**Acceptance status:** `pending`

**Latest accepted slice:** M6-I1 Python complete checkpoint. Eight focused
tests, all 214 engine tests, all 137 declarative suites, and the Python complete
checkpoint over 139 retained Bash verifiers pass.

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Count-authority recovery:**
[reports/count-authority.md](reports/count-authority.md)

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

**Status:** `Accepted`

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

**M6-L3 result:** the registered `release-workflow-foundation` suite
preserves the five-row release/changelog two-output decision, ten exact
inventory/disposition rows, direct Release metadata closure, canonical
workflow sections and Router route, and negative evidence against former
headings and implicit version/changelog defaults. The Bash checker, both helper
edges, and its exact row-35 dependency are absent. Row-35 passes at 22
dependencies / 20 direct route dependencies / 33 consumers. All 97 declarative
suites and graph freshness at 179 Bash verifiers / 184 nodes / 902 edges / 180
components pass. Forty-three metadata-helper consumers remain; no source,
fixture, engine, helper, schema, or unrelated lifecycle record changed. The
mixed checkpoint remains deferred to M6-L-W1.

**M6-L4 result:** the registered `rust-dependency-owner-contract` suite
preserves 14 typed mechanism decisions, direct Rust Dependency metadata
closure, canonical profile policy and Router/index routes, and the exact
`STD-0731` parent-index disposition. The Bash checker, both helper edges, its
row-35 dependency, and its classified README-consumer record are absent.
Row-35 passes at 21 dependencies / 19 direct route dependencies / 32 consumers.
All 98 declarative suites and graph freshness at 178 Bash verifiers / 183 nodes
/ 895 edges / 179 components pass. Forty-two metadata-helper consumers remain;
no source, fixture, engine, helper, schema, or unrelated lifecycle record
changed. The mixed checkpoint remains deferred to M6-L-W1.

**M6-L5 result:** the registered `rust-release-owner-contract` suite
preserves 16 typed mechanism decisions, direct Rust Release/reference metadata
closure, canonical profile/reference policy and Router/index routes, and the
exact `STD-0810` parent-index disposition. The Bash checker, both helper
edges, its row-35 dependency, and its classified README-consumer record are
absent. Row-35 passes at 20 dependencies / 18 direct route dependencies / 31
consumers. All 99 declarative suites and graph freshness at 177 Bash verifiers
/ 182 nodes / 888 edges / 178 components pass. Forty-one metadata-helper
consumers remain; no source, fixture, engine, helper, schema, or unrelated
lifecycle record changed. The mixed checkpoint remains deferred to M6-L-W1.

**M6-L6 result:** the registered `rust-tooling-owner-contract` suite
preserves 16 typed mechanism decisions, direct Rust Tooling/reference metadata
closure, canonical profile/reference policy and Router/index routes, and the
exact `STD-0831` parent-index disposition. The Bash checker, both helper
edges, its row-35 dependency, and its classified README-consumer record are
absent. Row-35 passes at 19 dependencies / 17 direct route dependencies / 30
consumers. All 100 declarative suites and graph freshness at 176 Bash verifiers
/ 181 nodes / 881 edges / 177 components pass. Forty metadata-helper consumers
remain; no source, fixture, engine, helper, schema, or unrelated lifecycle
record changed. The mixed checkpoint remains deferred to M6-L-W1.

**M6-L7 and M6-L-W1 result:** the registered
`rust-dependency-candidate-inspection` suite preserves the 14-row typed
inspection decision, direct Rust Dependency metadata closure, canonical
generic/profile/reference policy, legacy-index routing and prohibitions, and
the exact `STD-0732` through `STD-0734` dispositions. The Bash checker, both
helper edges, and its classified README-consumer record are absent. Its
source-preparation authority transferred directly from the removed `checker:`
subject to the registered `suite:` subject without dual authority. Row-35
passes at 19 dependencies / 17 direct route dependencies / 29 consumers;
source preparation passes at 8 packages / 9 unique subjects. All 101
declarative suites and graph freshness at 175 Bash verifiers / 180 nodes / 874
edges / 176 components pass. The one M6-L-W1 closing mixed checkpoint passed
all 175 remaining Bash entrypoints. Thirty-nine metadata-helper consumers
remain; no source, fixture, engine, helper, schema, or unrelated lifecycle
record changed. No later package is admitted; a fresh graph and ownership
audit is required before implementation continues.

#### M6-M1 Through M6-M3 Low-Coupling Semantic Wave

**Goal:** Replace the three remaining metadata-helper consumers that have no
executable callers and whose only non-metadata executable outputs are
independently owned historical decomposition or lifecycle gates.

**Admission evidence:** the fresh 175-verifier graph contains 39 metadata-helper
consumers. Seven have no executable callers. Rust Async Blocking and Mutex,
Rust Async Cancellation and Observability, and Rust Interop Memory call only
the metadata helper plus retained decomposition/lifecycle checkers. The other
four caller-free consumers depend on active semantic checkers across multiple
owners and remain unadmitted.

| Package | Owner | Direct contract | Independent gates | Lifecycle transfer |
| --- | --- | --- | --- | --- |
| M6-M1 | Rust Async profile | 18 typed blocking/synchronization decisions and two exact dispositions | Rust Async decomposition and trust/lifecycle re-plan | remove one row-35 consumer |
| M6-M2 | Rust Async profile | 20 typed cancellation/observation decisions and two exact dispositions | Rust Async decomposition and trust/lifecycle re-plan | remove one row-35 consumer |
| M6-M3 | Rust Interop profile | 22 typed foreign-memory decisions and five exact dispositions | F022/F023 decomposition | remove one row-35 dependency and consumer |

**Declarative contract:** existing decision, metadata-graph, exact-row/table,
and text checks preserve all three behaviors. M6-M3 applies source-wide
prohibitions to the non-normative legacy Rust Interop index for executable
examples and unsafe mechanism defaults. This is a reviewed conservative
strengthening of the Bash check's former moved-section range: a legacy index
cannot regain normative mechanism text in another section. It does not freeze
the canonical Interop or Language Bindings owners. No engine, fixture, policy
source, legacy source, helper, compatibility schema, wrapper, command action,
heading-range alias, or fallback is admitted.

**Edge contract:** metadata calls use direct native metadata assertions while
the shared helper remains independently owned. Decomposition and trust calls
are migration-lifecycle gates, not semantic policy prerequisites; each remains
an independently executable checker and runs as an affected package gate. No
suite duplicates those lifecycle contracts or retains a Bash invocation.

**Lifecycle contract:** M6-M1 and M6-M2 each remove one exact row-35 consumer
record. M6-M3 removes one exact dependency and consumer record. Fixed counts
reconcile under the existing schemas from 19 dependencies / 17 direct route
dependencies / 29 consumers to 18 / 16 / 26 after the complete wave. Any
schema, allowed-value, owner, or interpretation change is a re-plan trigger.

**Concurrency and integration:** M6-M1, M6-M2, and M6-M3 suite/checker paths
are disjoint and may be prepared in isolated worktrees. Fixtures, canonical and
legacy sources, engine, helper, registry, README, package/edge manifests,
lifecycle inventories/checkers, generated graph, and plans remain read-only to
package authors and serial integration-owner work.

**Verification:** each package runs its focused dependency closure, package and
edge authority, affected retained lifecycle gates, row-35/root audit, all
declarative suites, graph freshness, both plan checks, route/removal/diff, and
read-only evidence. The mixed Bash suite runs once after M6-M3 closes M6-M-W1.
A source, fixture, engine, helper, schema, router, lifecycle-meaning, or shared
edge-contract change requires an immediate checkpoint instead.

**Re-plan triggers:** stop if a candidate gains an executable caller; an
independent gate proves to be semantic policy authority; existing primitives
cannot preserve typed outcomes, exact dispositions, or no-legacy evidence; a
fixture or source must change; lifecycle rows cannot transfer exactly; package
paths overlap outside serial integration files; or a shared contract must
change.

**M6-M1 result:** the registered `rust-async-blocking-mutex` suite preserves
the 18-case typed blocking/synchronization decision, exact `STD-0722` and
`STD-0723` inventory and dispositions, direct Rust Async metadata closure,
canonical profile policy, legacy-index headings, and negative evidence against
named runtime/mutex defaults. The Bash checker and all six classified edges
are absent; Rust Async decomposition and trust/lifecycle re-plan remain
independent executable gates. Row-35 passes at 19 dependencies / 17 direct
route dependencies / 28 consumers. All 102 declarative suites and graph
freshness at 174 Bash verifiers / 179 nodes / 876 edges / 175 components pass.
Thirty-eight metadata-helper consumers remain; no source, fixture, engine,
helper, schema, or unrelated lifecycle record changed. The mixed checkpoint
remains deferred to M6-M-W1.

**M6-M2 result:** the registered `rust-async-cancellation-observability` suite
preserves the 20-case typed cancellation/observation decision, exact
`STD-0724` and `STD-0725` inventory and dispositions, direct Rust Async
metadata closure, canonical profile policy, resolved finding and accepted-plan
evidence, legacy-index headings, and negative evidence against assumed
cancellation, destruction-only cleanup, leaf ownership, and tool defaults.
The Bash checker and all six classified edges are absent; Rust Async
decomposition and trust/lifecycle re-plan remain independent executable gates.
Row-35 passes at 19 dependencies / 17 direct route dependencies / 27 consumers.
All 103 declarative suites and graph freshness at 173 Bash verifiers / 178
nodes / 866 edges / 174 components pass. Thirty-seven metadata-helper
consumers remain; no source, fixture, engine, helper, schema, or unrelated
lifecycle record changed. The mixed checkpoint remains deferred to M6-M-W1.

**M6-M3 result:** the registered `rust-interop-memory` suite preserves the
22-case typed foreign-memory decision, exact `STD-0752` through `STD-0756`
inventory and dispositions, direct Rust Interop metadata closure, canonical
profile and Rust-index routing evidence, and negative evidence against
executable examples and unsafe mechanism defaults anywhere in the
non-normative legacy index. The source-wide prohibition is the accepted
no-legacy strengthening from VE040; no heading-range alias or compatibility
checker was added. The Bash checker and all four classified edges are absent;
F022/F023 decomposition remains an independent executable gate. Row-35 passes
at 18 dependencies / 16 direct route dependencies / 26 consumers. All 104
declarative suites and graph freshness at 172 Bash verifiers / 177 nodes / 857
edges / 173 components pass. Thirty-six metadata-helper consumers remain; no
source, fixture, engine, helper, schema, or unrelated lifecycle record changed.
The M6-M-W1 closing mixed checkpoint passed all 172 remaining Bash entrypoints.
The wave is closed with no later package admitted; a fresh graph and ownership
audit is required before implementation continues.

#### M6-N Inbound-Caller Edge-Authority Re-plan Trigger

**Status:** `Accepted`

The fresh graph audit selected two shallow semantic candidates. Contract HTTP
Outcome Projection owns 24 typed decisions and four exact dispositions, calls
only the metadata helper, and is invoked by row-33 decomposition. Persistence
Owner Contract owns 19 typed decisions and one exact disposition, calls only
the metadata helper, and is invoked by row-32 decomposition. Persistence also
owns one exact row-35 direct-route dependency. Existing decision, table, text,
and metadata assertions can preserve both semantic contracts without source,
fixture, schema, helper, or compatibility changes.

The audit discovered that the generic `edge_dispositions` assertion freezes
only executable edges whose source is the package checker. It does not require
rows for executable edges whose target is that checker. Consequently, an
accepted package could delete its checker while a retained caller still names
the missing path; graph freshness would retain a dangling target node, but the
typed package contract would not reject it. A separate removed-path scan is
useful defense-in-depth but is not canonical package authority. Implementing
M6-N1 or M6-N2 under the current contract would therefore violate exact edge
ownership and the no-legacy/no-bridge rule.

**Option 1 - Exact incident-edge authority (`Recommended`):** extend the
existing generic assertion from exact outgoing-edge coverage to exact incident
coverage. Determine direction from the package subject and each row's existing
`source`/`target` fields; do not version, duplicate, or add a compatibility
manifest. For an inbound `independent-gate` row, the retained caller endpoint
is the typed checker replacement; accepted state requires the checker source
and every incident edge to be absent. Add focused positive and negative tests
for omitted inbound edges, fabricated inbound edges, wrong retained endpoint,
accepted dangling references, and unaffected historical outbound rows. Accept
this shared M6-EDGE-2 contract with engine, declarative, graph, plan, and mixed
checkpoints before admitting M6-N1 or M6-N2. Choose this to establish one
reusable authority model for the many remaining caller-connected packages.

**Option 2 - Atomic caller-and-child package trains:** migrate each row
decomposition checker and its semantic child as separate, dependency-ordered
packages in one wave so no dangling edge exists between commits. This avoids an
immediate engine change but expands each semantic package into migration-owner
work, requires classification of every other row-checker call, and still leaves
the generic package contract unable to detect future incoming-edge omissions.
Choose this only if caller review proves the row checker itself should now be
retired and all of its remaining dependencies can be represented without
cross-owner coupling.

**Option 3 - Defer caller-connected packages:** leave M6-N1 and M6-N2
unchanged and audit S1 routing or the Rust Binding dependency train. This
preserves current evidence but does not resolve the incoming-edge gap; S1 needs
shared route/link/budget capability and Rust Binding requires larger semantic
provider closures. Choose this only if shared edge-contract work cannot be
reviewed now.

Bespoke package scans, retaining deleted checker wrappers, invoking Python
suites from Bash callers, silently dropping row-32/row-33 calls, weakening
graph freshness, or treating all callers as one owner are invalid options.
Option 1 is selected. No semantic package is admitted until M6-EDGE-2 passes.

#### Slice M6-EDGE-2: Exact Incident-Edge Authority

**Status:** `Accepted`

**Goal:** make package authority cover every executable graph edge incident to
the package checker, preventing both undeclared prerequisites and retained
callers that reference a deleted checker.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/checks/edge_dispositions.py`
- `tools/standards_verifier/tests/test_edge_dispositions.py`
- `tools/standards_verifier/README.md`
- this child plan, its ledger, issue register, and checker-inventory report
- the parent standards-library restructure plan

Package manifests, edge rows, suite registry/configuration, generated graph,
canonical and legacy standards, semantic fixtures/checkers, helpers, schemas,
lockfiles, and workflow artifacts remain read-only.

**Canonical contract:** preserve the existing manifest header and infer edge
direction from whether the package checker equals `source` or `target`. Exact
identity is `(edge_type, source, target)`. An admitted `edge-dispositions`
package must declare every current incident executable edge once and no absent
edge. An admitted `edge-free` package must have no incident executable edge.
Accepted packages retain historical rows only when their checker and every
incident graph edge are absent.

For `independent-gate` and `external-owned-artifact`, replacement evidence must
equal the retained endpoint opposite the package checker. Existing outbound
rows therefore remain valid; inbound retained callers use the same typed
contract without a new disposition, schema version, compatibility parser, or
direction default. A row that contains neither package endpoint is invalid.

**Focused evidence:** preserve every current outbound and edge-free test, then
add positive inbound retained-gate coverage and typed negative coverage for an
omitted inbound edge, fabricated/absent inbound row, wrong retained endpoint,
accepted dangling inbound edge, and edge-free package with an inbound edge.
No test may rely only on a removed-path scan.

**Acceptance gate:** focused edge-disposition tests, all engine tests, Python
compilation, the registered edge contract, all declarative suites, graph
freshness, both plan checks, diff/whitespace validation, and one complete mixed
Bash checkpoint pass. Any manifest/schema rewrite, accepted historical-row
change, graph-generation change, owner inference, arbitrary execution, or
failure requiring a package-specific exception is a re-plan trigger.

**Outcome:** The generic assertion now indexes every executable edge under
both endpoints and compares exact `(edge_type, source, target)` identities.
Direction is inferred from the existing package-checker endpoint, retained
checker or artifact evidence names the opposite endpoint, and accepted or
edge-free packages reject dangling inbound callers. No schema version,
compatibility parser, package-specific exception, removed-path substitute, or
legacy execution bridge was added.

**Verification:** all 27 focused edge-disposition tests and all 99 engine tests
pass; Python compilation passes with an isolated bytecode cache; the registered
edge contract and all 104 declarative suites pass; graph freshness remains 172
Bash verifiers / 177 nodes / 857 edges / 173 components; both plan checks and
diff integrity pass; and the complete mixed 172-entrypoint checkpoint exits
zero.

#### M6-N-W1 Lifecycle-Caller Wave Admission

**Status:** `Accepted`

The unchanged graph confirms exactly four executable incident edges for each
candidate. Both checkers have outbound `executable_reference` and
`helper_dependency` edges to `check-metadata.sh`. Row 33 has inbound
`executable_reference` and `verifier_dependency` edges to Contract HTTP
Outcome; row 32 has the same two inbound edges to Persistence Owner. The
Persistence row-35 inventory reference is non-executable lifecycle data and is
transferred separately.

M6-N1 and M6-N2 are admitted in serial train order 69 and 70. Package manifests
declare every exact incident edge with direction inferred from the existing
source/target endpoints. The row checkers remain independently owned migration
evidence; implementation removes only their semantic-child invocation after a
registered suite becomes canonical. No caller wrapper, Bash-to-Python bridge,
duplicate suite invocation, package-specific scan, source fallback, fixture
rewrite, schema change, or compatibility mode is permitted.

Shared manifests, registry, README, generated graph, and plan records remain
serial integration-owner work. The semantic suites/checkers and row-33/row-32
callers have disjoint package write sets, but M6-N2 follows M6-N1 so package
state and shared records never conflict. Canonical standards, semantic fixtures,
metadata helper, engine code, schemas, lockfiles, and workflow artifacts remain
read-only for the full wave.

**Admission verification:** package projection and exact incident-edge
authority pass for both admitted rows. Serial inventory regeneration preserves
172 Bash verifiers / 177 nodes / 173 components and records 869 edges; the 12
new non-executable `contract_reference` edges are generated references from the
three shared package-authority artifacts to the four newly named checker/caller
paths, not semantic prerequisites or executable fallbacks.

**Wave outcome:** M6-N1 and M6-N2 are accepted in frozen order. Their registered
suites replace both semantic Bash authorities, row 33 and row 32 retain only
independent decomposition/lifecycle evidence, and row 35 no longer inventories
the deleted Persistence checker. No caller wrapper, Python bridge, duplicate
suite invocation, source fallback, fixture rewrite, or compatibility path
remains.

**Wave verification:** all 106 declarative suites, focused package and exact
incident-edge authority, affected row-32 and row-35 lifecycle checkers,
removed-path and graph-freshness checks, and the complete mixed checkpoint over
all 170 surviving Bash entrypoints pass. The accepted graph has 175 nodes, 854
edges, and 171 components.

#### Slice M6-N1: Contract HTTP Outcome Projection

**Status:** `Accepted`

**Package state:** `accepted`

**Goal:** replace the Bash checker with one registered Contracts-owned suite
that preserves all 24 typed outcome-projection decisions, four exact
dispositions, canonical protocol-outcome authority, non-normative HTTP recipe
evidence, former architecture-index closure, metadata relations, and negative
evidence against guessed status/envelope defaults.

**Allowed write set:** package and edge manifests, package expected rows, suite
registry, `suites/contract-http-outcome-projection.toml`, the deleted Contract
HTTP checker, row-33 decomposition checker, verification README, generated
checker inventories, and serial child/parent plan records. Everything else is
read-only.

**Caller transfer:** register and pass the semantic suite before removing the
single Contract HTTP child invocation from row 33. Row 33 continues to prove
its eight-ID/two-child decomposition, owner validation, plan history, adapter
proof, complete dispositions, and execution-train lifecycle. Accepted package
state requires the deleted checker and all four incident graph edges to be
absent.

**Acceptance gate:** focused suite, affected row-33 checker, package and exact
incident-edge authority, all declarative suites, graph freshness, both plan
checks, removed paths, README route, source/fixture/helper/engine/schema
read-only proof, and diff integrity pass. The mixed checkpoint is deferred to
M6-N-W1 closure.

**Outcome:** one registered seven-check suite now owns the 24 typed decisions,
four exact dispositions, metadata closure, canonical and reference policy, and
former architecture-index closure. The Bash checker and row-33 invocation are
removed; row 33 continues to pass its independent decomposition, adapter,
disposition, plan, and execution-train evidence. No Python bridge, wrapper,
duplicate invocation, source/fixture rewrite, or compatibility path remains.

**Verification:** focused suite, retained row-33 checker, package authority,
and exact incident-edge authority pass. Regenerated inventory records 171 Bash
verifiers / 176 nodes / 862 edges / 172 components, and metadata-helper
consumers fall from 36 to 35. All-wave declarative, plan, diff, read-only, and
removed-path gates remain required before this package commit; the mixed gate
remains deferred to M6-N-W1 closure.

#### Slice M6-N2: Persistence Owner Contract

**Status:** `Accepted`

**Package state:** `accepted`

**Goal:** replace the Bash checker with one registered Persistence-owned suite
that preserves all 19 typed owner decisions, the exact `STD-0106` disposition,
canonical and reference evidence, Router and architecture routes, metadata
relations, and negative evidence against nearby weaker-store fallback.

**Allowed write set:** package and edge manifests, package expected rows, suite
registry, `suites/persistence-owner-contract.toml`, the deleted Persistence
checker, row-32 decomposition checker, row-35 dependency inventory and checker,
verification README, generated checker inventories, and serial child/parent
plan records. Everything else is read-only.

**Caller and lifecycle transfer:** register and pass the semantic suite before
removing the single Persistence child invocation from row 32. Row 32 continues
to prove its 13-ID/three-child decomposition, owner validation, plan history,
durable-mutation and migration-execution children, exact disposition, and
execution train. Remove the deleted checker from row-35 dependency data and
reconcile exact counts from 18/16/26 to 17/15/26 without changing the lifecycle
schema. Accepted package state requires the deleted checker and all four
incident executable edges to be absent.

**Acceptance gate:** focused suite, affected row-32 and row-35 checkers,
package and exact incident-edge authority, all declarative suites, graph
freshness, both plan checks, removed paths, README route,
source/fixture/helper/engine/schema read-only proof, diff integrity, and one
complete mixed Bash checkpoint pass at M6-N-W1 closure. Any additional caller,
semantic prerequisite, lifecycle owner, or required reusable assertion is a
re-plan trigger.

**Outcome:** one registered eight-check Persistence suite now owns all 19 typed
owner decisions, the exact `STD-0106` disposition, metadata closure, canonical
and reference policy, and Router and architecture routes. The Bash checker and
row-32 invocation are absent; row 32 retains its 13-ID/three-child lifecycle
authority. Row 35 now freezes 17 total and 15 direct-route dependencies while
preserving 26 classified README consumers. No weaker-store fallback, wrapper,
bridge, duplicate execution, or compatibility authority remains.

**Verification:** the focused eight-check suite, row-32 and row-35 lifecycle
checkers, package authority, and exact incident-edge authority pass. All 106
declarative suites pass. Fresh generated inventory records 170 Bash verifiers,
175 nodes, 854 edges, and 171 components; 34 metadata-helper consumers remain.
Removed-path proof, graph freshness, diff integrity, and the complete mixed
170-entrypoint M6-N-W1 checkpoint pass.

#### Post-M6-N-W1 Candidate Re-plan Trigger

**Status:** `Accepted`

The clean accepted graph contains 34 metadata-helper consumers. The shallowest
candidate that uses only existing declarative primitives is Release Procedure,
but it is not independently deletable: Release Binding Generation invokes it
as a semantic prerequisite. Binding Generation itself has no executable caller
and invokes only Release Procedure plus the independently owned row-8 lifecycle
gate. Deleting Release Procedure alone, silently dropping that invocation, or
temporarily retaining dual Bash/declarative authority would violate exact
incident-edge ownership and the no-bridge/no-fallback rule.

S1 Routing is also shallow, with one metadata dependency and one inbound root
README audit caller, but its contract additionally proves exact routed module
identity, repository-local Markdown link closure, and an aggregate routed-line
ratio against generated summary data. The current engine has no generic link
closure or aggregate budget assertion. Approximating those checks with required
text would weaken evidence. The caller-free Rust Binding leaves are deeper and
depend on Rust Binding conversions/wire/runtime, Concurrency, Interop, Rust
Async, and lifecycle owners; combining that closure now would cross unresolved
semantic ownership.

**Option 1 - Dependency-closed Release pair (`Recommended`):** admit Release
Procedure and Release Binding Generation as one serial two-package wave and
implement them atomically after admission. Create two registered suites using
existing decision, table, metadata, and text assertions; make Binding
Generation explicitly require Release Procedure. Freeze all Release Procedure
metadata and inbound Binding Generation edges, all Binding Generation
Release/row-8 edges, the row-35 consumer transfer, exact removed paths, and one
closing mixed checkpoint. Choose this for the fastest standards-compliant
progress without shared engine work or implicit dependency loss.

**Option 2 - Generic routing capabilities before S1:** design separate typed,
side-effect-free Python assertions for repository-local Markdown link closure
and aggregate line-budget comparison, with focused positive and negative tests.
Accept that shared engine contract with opening and closing checkpoints, then
admit S1 and transfer the root README audit caller explicitly. Choose this when
improving reusable routing/documentation verification is more important than
immediate Bash reduction. Do not add an S1-specific callback or arbitrary
command action.

**Option 3 - Rust Binding dependency train:** first decompose the remaining
Rust Binding graph into owner-local prerequisite waves, then migrate the
caller-free error, callback, enum, and event leaves only after their semantic
providers are registered suites. Choose this when completing the Rust Binding
family is the priority and the larger multi-owner planning cost is accepted.
Do not combine Concurrency, Interop, Rust Async, wire, runtime, and lifecycle
authority into one package merely because the leaves share a profile.

**Re-plan gate:** select one option and record its exact package train before
implementation. Any proposal that drops a semantic call, preserves a Bash
wrapper, introduces dual authority, weakens S1 link/budget evidence, or merges
unresolved owners is rejected rather than treated as a fallback.

**Decision:** Option 2 is selected. M6-RC1 establishes generic routing evidence
before S1 is admitted. Release Procedure and the Rust Binding train remain
unchanged and unadmitted.

#### M6-RC1: Routing Evidence Primitives

**Status:** `Accepted`

**Goal:** add two independent, typed, side-effect-free declarative assertions
that preserve S1's currently unrepresentable local-link and routed-context
budget evidence without embedding S1 policy in the engine.

**`markdown_links` contract:** accepts exactly `id`, `type`, and one non-empty,
duplicate-free `paths` list. It reads each contained UTF-8 file, recognizes the
same inline Markdown destination form as the current S1 checker, skips only
`http://`, `https://`, and `mailto:` destinations, strips a fragment before
resolution, treats a fragment-only destination as the containing file, and
requires every remaining target to exist relative to the containing document.
Absolute targets, parent or symlink escape, malformed configuration, and
invalid UTF-8 are typed invalid; missing source or target evidence is typed
unavailable. It does not fetch URLs, validate anchors, normalize or decode
destinations, parse reference-style links, infer files, or execute commands.

**`line_budget` contract:** accepts exactly `id`, `type`, a non-empty unique
`paths` list, `baseline_path`, `baseline_key`, `maximum_numerator`, and
`maximum_denominator`. Both ratio values are positive integers. It counts raw
newline bytes across the explicit contained files, reads one exact
`metric<TAB>value` table with a unique requested key and positive decimal
integer value, and requires
`observed * maximum_denominator < baseline * maximum_numerator`. Equality is a
failure. Missing files or key evidence are typed unavailable; malformed tables,
duplicates, invalid integers, unsafe paths, and invalid ratios are typed
invalid. It supports no expression language, inferred metric, default ratio,
unit conversion, command action, or normalization.

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/checks/__init__.py`;
- `tools/standards_verifier/standards_verifier/checks/markdown_links.py`;
- `tools/standards_verifier/standards_verifier/checks/line_budget.py`;
- `tools/standards_verifier/tests/test_routing_checks.py`;
- `tools/standards_verifier/README.md`;
- `docs/plans/standards-verification-engine/reports/architecture.md`;
- this plan, execution ledger, issues, checker-inventory report, and parent
  plan.

S1 checker, fixture, root README audit, lifecycle data, suites, registry,
package/edge manifests, generated graph, standards sources, helpers, schemas,
lockfiles, and workflow artifacts remain read-only. S1 may consume the
capabilities only after M6-RC1 acceptance in a separately admitted package.

**Focused evidence:** cover valid nested local links, allowed external links,
fragment-only and file-plus-fragment targets, missing targets, absolute/parent/
symlink escape, missing sources, invalid UTF-8, empty/duplicate paths, and
unknown fields. Cover a passing strict line ratio, equality and exceeded-budget
failures, raw newline counting, malformed header/rows, duplicate or missing
metrics, non-positive/non-decimal values, missing/escaping inputs, invalid
ratios, empty/duplicate paths, and unknown fields. Diagnostics must retain
stable `CONFIG.*`, `PATH.*`, `INPUT.*`, and assertion-specific codes.

**Acceptance gate:** focused routing tests, all engine tests, Python
compilation, all declarative suites, graph freshness, both plan checks,
diff/read-only evidence, and a complete mixed closing checkpoint pass. Any need
for Markdown AST dependencies, network access, anchor policy, arbitrary
expressions, S1-specific branches, weaker text approximation, or changes
outside the allowed write set is a re-plan trigger.

**Admission evidence:** the clean opening baseline passes all 99 engine tests,
all 106 declarative suites, graph freshness at 170 Bash verifiers / 175 nodes /
854 edges / 171 components, both plan checks, diff integrity, and all 170 mixed
Bash entrypoints. No engine, test, documentation, suite, registry, checker,
fixture, source, helper, manifest, generated artifact, schema, or lockfile
changed during admission.

#### M6-RC1 Closing-Checkpoint Integrity Re-plan Trigger

**Status:** `Accepted`

Implementation of the two admitted generic assertions is complete and passes
24 focused routing tests, all 123 engine tests, Python compilation, all 106
declarative suites, graph freshness at 170 Bash verifiers / 175 nodes / 854
edges / 171 components, both plan checks, and diff integrity. M6-RC1 is not
accepted because the canonical fail-fast mixed checkpoint is not green.

The first failure is
`evaluation/standards-effectiveness/verify-milestone-7-row-46-decomposition.sh`:
it requires the live README-consumer manifest to contain 33 rows, while the
accepted manifest and its owning root audit contain 26. Three other failing
entrypoints call row 46; the other 166 entrypoints pass. The row-46 contract
already proves the retained Rust profile consumer's exact classification and
calls the root README audit, so its hard-coded mutable total duplicates current
manifest authority. Its 33-to-34 statement is valid historical activation
evidence, not a valid invariant for a manifest that decreases as Bash consumers
are migrated.

The earlier M6-N-W1 and M6-RC1 opening mixed-checkpoint claims were produced by
an ad hoc loop that did not fail fast and could return the final checker's
success after an intermediate failure. Those claims are superseded for current
acceptance purposes. The repository-owned
`evaluation/standards-effectiveness/run-complete-suite.sh` is the only accepted
mixed-checkpoint entrypoint for this recovery and later slices.

**Option 1 - Restore single current-state authority (`Recommended`):** admit one
bounded lifecycle repair that removes the row-46 hard-coded live total, retains
its exact Rust profile consumer/classification proof, preserves the historical
33-to-34 activation statement, and makes the decomposition explicit that the
root README audit owns current manifest completeness and count. Add focused
negative evidence for a missing or misclassified retained consumer, run row 46
and its three callers, then run the canonical complete-suite launcher. Choose
this to eliminate duplicated mutable authority without weakening historical or
current evidence.

**Option 2 - Rebase row 46 to 26:** change the hard-coded total and narrative to
the current count. This is the smallest textual patch, but every later consumer
migration would require another unrelated row-46 edit. Choose it only if row 46
is intentionally made a current-manifest co-owner; that conflicts with the
repository's single-owner and maintainability goals and is not recommended.

**Option 3 - Add immutable historical consumer evidence:** preserve an exact
34-row acceptance snapshot owned by row 46 and validate the historical
transition against that artifact, while leaving the live 26-row manifest to the
root audit. Choose this only if exact historical consumer membership is a
required audit product. It adds a new fixture and lifecycle contract that the
current objective does not otherwise require.

**Rejected:** accepting M6-RC1 with a waived mixed gate, keeping the non-failing
ad hoc loop, dropping row-46 caller evidence, or adding a compatibility path.
Select and admit one repair before editing row-46 lifecycle files or accepting
the shared engine change.

**Decision:** Option 1 is selected and broadened into the VE043 count-authority
recovery. Mutable aggregate membership and cardinality are derived from
canonical evidence. Exact finite contracts use row/key projections, historical
snapshots retain exact identities, structural zero/one multiplicity remains a
valid operator, and named policy thresholds remain policy data. Scalar totals
must not duplicate a mutable manifest, generated inventory, or package set.
The measured taxonomy and execution sequence are in the
[count-authority report](reports/count-authority.md).

##### VE043-R1: Baseline Authority Repair

**Status:** `Accepted`

**Goal:** restore a trustworthy fail-fast baseline and accept the already
implemented M6-RC1 capability without preserving any mutable README total as a
literal.

**Allowed write set:** the existing M6-RC1 implementation and documentation
set; `verify-root-readme-consumer-audit.sh`;
`verify-milestone-7-row-35-decomposition.sh`;
`verify-milestone-7-row-46-decomposition.sh`; row-35 and row-46 decomposition
documents; this plan, ledger, issues, count-authority and checker-inventory
reports, and parent plan. README manifests, row 45, suites, registry, package
and edge manifests, generated artifacts, standards sources, schemas, helpers,
lockfiles, and workflows remain read-only.

**Required behavior:**

- root audit retains exact observed-versus-manifest path equality, schema,
  classification domains, special identities, and prohibitions; it removes the
  literal 26 and derives its report count from the observed set;
- row 35 removes literal dependency totals 17/15/1/1 and consumer total 26,
  retains exact schema/domain/unique/path evidence, replaces category
  multiplicity with exact special-path identities where semantics require one,
  delegates consumer completeness to the root audit, and derives report totals;
- row 46 removes literal 33, retains the exact Rust profile consumer and
  classification, preserves 33-to-34 as historical activation evidence, and
  delegates current completeness to the root audit; and
- no manifest row, classification, caller, historical identity, or no-fallback
  assertion changes.

**Verification:** shell syntax; focused root audit, rows 35, 45, and 46, and the
three row-46 Rust callers; static absence of the removed mutable literals in the
three repaired checkers; 24 routing tests; all engine tests; Python compilation;
all declarative suites; graph freshness; both plan checks; diff/read-only proof;
and `evaluation/standards-effectiveness/run-complete-suite.sh`. The canonical
runner's pass jointly closes VE043-R1 and M6-RC1 because the M6-RC1
implementation was already present but unaccepted when the baseline defect was
found. This bounded integration is not precedent for combining unrelated
future slices.

##### VE043-E1: Count-Safe Engine Contract

**Status:** `Accepted`

After VE043-R1 and M6-RC1 acceptance, remove `row_count` from the strict table
schema and reject it as unknown with no compatibility parsing. Remove all eight
live uses; preserve seven through their existing exact projections and add one
exact GUI smoke case-key projection. In the same owner-coherent shared engine
package, add the bounded `reference_inventory` assertion specified by the
count-authority report, its focused tests, and engine documentation. No glob,
regex, command, shell parser, callback, inferred candidate set, normalization,
or policy-specific behavior is allowed.

**Allowed write set:** table parser and tests; one new registered
`reference_inventory` check and focused test module; the eight named suite
files in the count-authority report; engine README and architecture report;
this plan, ledger, issues, count-authority and checker-inventory reports, and
parent plan. Registry, manifests, generated artifacts, Bash checkers, standards
sources, fixtures other than the GUI case projection's existing suite data,
lockfiles, and workflows remain read-only.

**Acceptance:** focused schema-removal and reference-inventory tests, all engine
tests, Python compilation, all declarative suites, graph freshness, both plan
checks, diff/read-only proof, and one canonical fail-fast complete-suite
checkpoint pass.

**Acceptance evidence:** 15 focused schema and inventory tests, all 138 engine
tests, Python compilation, all 106 declarative suites, fresh generated evidence
at 170 verifiers / 175 nodes / 855 edges / 171 components, both plan checks,
diff integrity, and all 170 canonical mixed entrypoints pass. `row_count` is
rejected as unknown, all eight suites retain exact membership evidence, and
the generic assertion has no compatibility parser, inferred candidate set, or
policy-specific fallback.

##### VE043-R1 Generated-Artifact Re-plan Trigger

**Status:** `Accepted`

The focused R1 checkers pass, as do all 24 M6-RC1 routing tests and all 123
engine tests. The declarative launcher stops at generated-inventory freshness.
The committed VE043 plan adds documentation references to the three repaired
checker paths, and R1's required exact computed-consumer identity adds a new
executable reference from row 35 to `verify-commit-authority.sh`. The current
generated structure inventory and dependency graph therefore cannot remain
read-only while R1 also requires exact graph freshness. Preserving checker line
counts does not resolve these changed inbound relationships.

**Option 1 - Reconcile generated evidence atomically (`Recommended`):** add the
generated checker structure inventory and three dependency-graph TSVs to R1's
bounded write set, regenerate them once from the accepted implementation, and
review the exact diff. This follows VE018, keeps generated evidence truthful,
and creates no second authority or fallback.

**Option 2 - Obscure references to preserve the old graph:** rewrite plan and
checker text so exact checker basenames are assembled indirectly or omitted.
This can avoid measured reference edges, but makes ownership evidence less
legible and causes the graph to under-report an intentional executable
reference. It is not recommended.

**Option 3 - Change graph collection semantics:** exclude active plans or
comparison-only checker identities from generated inbound evidence. This is a
shared engine contract change requiring new classification semantics, tests,
and a separate checkpoint. Choose it only if the repository decides those
references should never be graph evidence; it is disproportionate to R1.

**Rejected:** waive freshness, hand-edit only selected generated rows, remove
the exact identity assertion, or split regeneration into a stale intermediate
commit. Select and admit one option before changing generated artifacts or
running the canonical complete-suite acceptance gate.

**Decision:** Option 1 is selected. Add
`generated/checker-structure-inventory.tsv`,
`generated/checker-dependency-nodes.tsv`,
`generated/checker-dependency-edges.tsv`, and
`generated/checker-dependency-components.tsv` beneath the standards-
effectiveness evaluation directory to VE043-R1's bounded write set. These
files are regenerated together by the canonical generator and reviewed as
derived evidence; no hand-edited row, graph-semantic change, or fallback is
authorized.

**Acceptance evidence:** the canonical generator produces a fresh 170-verifier
/ 175-node / 855-edge / 171-component graph. Exact review shows one intentional
executable-reference edge and its derived node/component updates plus plan-
documentation inbound evidence. Focused R1 checks, 24 routing tests, all 123
engine tests, Python compilation, all 106 declarative suites, both plan checks,
diff integrity, and all 170 canonical mixed entrypoints pass.

##### VE043-A1 And VE043-P1: Audit And Package Admission

**Status:** `Planned`

Classify the machine-generated numeric-comparison baseline as mutable aggregate,
declared finite contract, historical snapshot, structural multiplicity, or
policy threshold. Candidate paths, expressions, source locations, fingerprints,
owners, standard dispositions, progress, and all totals are derived rather than
restated in reviewed data. Confirmed mutable aggregates migrate to set/relation
evidence in their owner packages. Do not build a Bash-expression parser for
scripts scheduled for deletion.

After `reference_inventory` acceptance, audit the exact incident-edge and owner
closure of the root README consumer checker and rows 35, 45, and 46. The former
assumption that these paths could enter one dependency-closed owner package is
superseded by the VE043-P1 owner-closure trigger below. No checker may be deleted
while a Bash caller remains, no Python-through-Bash bridge may be introduced,
and declarative and Bash authority may not coexist for the same behavior.

##### VE043-A1 Candidate-Authority Re-plan Trigger

**Status:** `Accepted`

The recorded total of 359 broad numeric-comparison candidates has no frozen
candidate artifact, extraction contract, baseline revision, or exact path-level
rows. Repository and commit-history inspection finds only the aggregate claim.
The queue therefore cannot be reproduced or classified exactly, and retaining
359 as its authority would repeat the mutable-count defect VE043 exists to
remove. No owner file or candidate disposition has been changed.

**Option 1 - Reconstruct the undocumented historical scan:** infer likely
regular expressions until they reproduce 359, freeze those results, and then
classify them. This may preserve the historical number but cannot prove it
reconstructs the original candidate semantics. Choose it only if matching the
historical observation is itself required; it is not recommended.

**Option 2 - Freeze a generated verifier-scoped audit snapshot
(`Recommended`):** treat 359 as non-authoritative historical context. Enumerate
the current canonical Bash verifier paths from generated inventory and apply
one documented conservative lexical extraction contract. Machine-generate an
immutable baseline containing candidate identity, path, exact expression,
occurrence/source diagnostics, and fingerprint. Derive its cardinality. Keep a
separate reviewed decision layer containing only generated candidate identity
and one semantic taxonomy class. Resolve owners from canonical
ownership/package records, map normal dispositions from the taxonomy, and
derive progress from baseline, current
inventory, and accepted package evidence. This provides complete current scope
without manually maintaining observed facts or inferring semantic meaning.

**Option 3 - Defer global inventory to owner-package audits:** remove the broad
queue claim and inspect numeric authority only when each owner package is
admitted. This minimizes up-front work but cannot prove repository-wide audit
coverage and makes cross-owner consistency harder to review. Choose it only if
the global completeness objective is intentionally dropped.

**Option 4 - Build a shell AST or expression parser:** parse all checker
expressions and infer candidate semantics mechanically. This could broaden
syntax coverage, but semantic count ownership still requires review and the
parser would exist mainly for Bash scheduled for deletion. It conflicts with
the admitted no-parser boundary and is rejected.

**Decision:** Option 2 is selected with generated-fact and reviewed-decision
authority separated. Candidate rows and counts are never hand-authored. The
reviewed layer states only irreducible semantic class; it does not duplicate
path, location, expression, fingerprint, owner, standard disposition, package,
progress, or total. Exact candidate-ID
coverage, class domain, and exception absence are verified mechanically.

##### VE043-A1 Derived Audit Admission

**Status:** `Accepted`

The selected recovery executes in three serial, independently verified slices:

1. **VE043-A1-G1 generated baseline (`Accepted`):** add a deterministic Python lexical
   collector under the existing verifier inventory boundary, focused tests, a
   write/check entrypoint, and one machine-generated immutable candidate TSV.
   Its rows derive from canonical Bash verifier inventory and contain stable
   content-based identity plus review diagnostics. The historical 359 is not an
   expected value. The generated file is never hand-edited.
2. **VE043-A1-C1 semantic coverage:** add one reviewed decision table containing
   only candidate identity and taxonomy class.
   Require exact one-to-one coverage of the generated baseline and derive the
   normal migration action from the taxonomy. Owner is intentionally outside
   the C1 schema. Missing, duplicate, and unknown-class outcomes are typed
   diagnostics.
3. **VE043-A1-L1 lifecycle guard:** compare current derived candidates with the
   immutable baseline and accepted package evidence. Reject a new candidate or
   an unexplained disappearance; accept disappearance only through an accepted
   migration package that explicitly names its canonical owner. Missing or
   ambiguous package-owner authority is typed `unavailable` or `invalid` rather
   than inferred. Retain the baseline and decisions as historical audit evidence
   while deriving current progress and all report totals.

**G1 allowed write set:**
`tools/standards_verifier/standards_verifier/numeric_audit.py`;
`tools/standards_verifier/generate_numeric_audit.py`; focused inventory/audit
tests in `tools/standards_verifier/tests/test_numeric_audit.py`;
`tools/standards_verifier/README.md`;
`evaluation/standards-effectiveness/generated/numeric-comparison-candidates.tsv`;
architecture and count-authority reports; and serial plan/issue/ledger records.
The existing mutable inventory and dependency-graph implementation and
artifacts; classification, owner, package, edge, suite, and registry data; Bash
verifiers; standards sources; lockfiles; and workflows remain read-only.

**G1 acceptance:** deterministic output from the same source state; exact
canonical verifier scope; unique content-based candidate identities; contained
UTF-8 paths; conservative documented lexical coverage; derived reporting only;
positive and negative tests for malformed, duplicate, unavailable, escaping,
and invalid UTF-8 evidence; Python compilation; all engine tests; generated
dependency freshness; both plan checks; diff integrity; and one shared-contract
complete-suite checkpoint. G1 does not classify candidates or edit an owner.

**G1 acceptance evidence:** the fixed lexical contract machine-generates 708
candidate rows from all 170 canonical Bash verifiers; this observed cardinality
is diagnostic and is not stored as an expected value. All 14 focused audit
tests and all 152 engine tests pass, Python compilation succeeds, the baseline
write is idempotent and its check is byte-exact, all 106 declarative suites
pass, existing graph evidence remains fresh at 170 verifiers / 175 nodes / 855
edges / 171 components, and all 170 canonical mixed entrypoints pass. The
snapshot has no semantic, owner, disposition, package, progress, or expected-
count field, and no file outside the G1 write set changed.

**No-fallback rule:** no expected candidate count, manually authored candidate
fact, wildcard owner, inferred taxonomy class, heuristic default, compatibility
manifest, source annotation, shell parser, Python-through-Bash bridge, or
silent drift is allowed. Mechanical suggestions may be reported but never own
semantic classification.

##### VE043-A1-C1 Owner-Join Re-plan Trigger

**Status:** `Accepted`

C1 preflight proves that canonical package evidence cannot currently derive an
owner for baseline candidates. The generated baseline has candidate rows in
124 current verifier paths. The package manifest has 68 checker subjects, all
already migrated, and exact path-set intersection with the 124 current paths is
empty. README dependency evidence classifies dependency shape but does not name
semantic owner. Rule-owner maps own standards identifiers, not verifier paths.
The graph owns executable relationships, not policy ownership. These are
derived preflight observations, not expected totals.

**Option 1 - Defer owner resolution to package admission (`Recommended`):** C1
records exact semantic-class coverage only. The taxonomy derives the standard
action, but owner remains intentionally unresolved until a checker migration
package is admitted through existing owner review. L1 joins candidate
disappearance to that accepted package and its canonical owner. This keeps C1
globally complete without creating a second checker-owner authority or
premature owner decisions.

**Option 2 - Establish a canonical current-checker owner manifest:** review all
current candidate-bearing verifier paths now and create one owner mapping before
C1. This makes owner available early, but duplicates ownership that package
admission must later state and creates a large mutable mapping for Bash being
deleted. Choose it only if current-checker ownership is required independently
of migration; it is not recommended.

**Option 3 - Infer owner from names, references, graph edges, or standards
content:** compute likely owners mechanically. These signals are not ownership
contracts and can be multi-owner or infrastructural. This violates explicit
ownership and no-inference rules and is rejected.

**Option 4 - Block C1 until every remaining package is admitted:** obtain owner
coverage first through package planning, then classify candidates. This avoids
new owner authority but serializes the global audit behind the entire migration
train and prevents count-authority findings from informing package design.
Choose it only if owner-at-classification is mandatory.

**Recommended admission boundary:** select Option 1, remove owner from C1
acceptance, retain exact candidate-ID/class coverage and taxonomy-derived
standard action, and make accepted package owner a required L1 disappearance
join. The reviewed C1 table still contains only candidate identity, semantic
class. No owner manifest, inferred owner, exception field, package edit, checker
edit, or standards-owner edit is authorized in C1.

**Decision:** Option 1 is selected. C1 is a read-only semantic audit and does
not exercise modification or acceptance authority. It uses the existing generic
`table` and `relation` assertions to require the exact two-column decision
schema, the closed five-class taxonomy domain, unique candidate identities, and
set equality with the generated baseline. The reviewed table does not restate
candidate facts or contain owner, action, package, progress, or total fields.
The taxonomy remains the authority for standard action. L1, not C1, requires an
accepted package and explicit canonical owner before candidate disappearance.

**C1 allowed write set:**
`evaluation/standards-effectiveness/numeric-comparison-decisions.tsv`;
`evaluation/standards-effectiveness/suites/numeric-comparison-classification.toml`;
`evaluation/standards-effectiveness/suite-registry.toml`; engine documentation;
count-authority and architecture reports; and serial plan, issue, and ledger
records. Python engine implementation, generated baseline and graph artifacts,
package/edge manifests, Bash verifiers, standards sources, lockfiles, and
workflows remain read-only.

**C1 acceptance:** every generated candidate identity occurs exactly once in
the reviewed table; every class is one of `mutable-aggregate`,
`declared-finite-contract`, `historical-snapshot`, `structural-multiplicity`, or
`policy-threshold`; no exception artifact is admitted; the registered
declarative suite passes with focused positive and negative assertion evidence;
all declarative suites, both plan checks, generated graph freshness, Python
compilation, engine tests, and diff integrity pass. C1 does not authorize a
checker or owner edit.

##### VE043-A1-C1 Exception-Schema Re-plan Trigger

**Status:** `Accepted`

Preflight of the generic table contract shows that the admitted optional
`exception_rationale` column would be empty on every normal row. The existing
`table` assertion can require values to be non-empty or belong to a non-empty
literal domain, but cannot require a field to remain empty unless a separately
admitted exception exists. Keeping the column would therefore repeat empty data
without mechanically enforcing its authority. Adding a bespoke numeric check or
a generic conditional-empty primitive used only here would increase engine
surface before evidence demonstrates a reusable need.

**Option 1 - Keep the three-column table and add an empty-field primitive:**
enforce that rationale is empty for current rows and later extend the contract
for admitted exceptions. This is mechanically strong but adds a new primitive
for one anticipated use and conflicts with the capability-admission threshold.

**Option 2 - Keep the three-column table with manual review only:** retain the
blank column and inspect it outside the engine. This is concise to implement but
leaves accepted evidence less strict than its declared contract and is
rejected.

**Option 3 - Use a two-column classification table and admit exceptions only
when observed (`Recommended`):** C1 records exactly `candidate_id` and
`semantic_class`. If review finds a candidate that cannot use the five-class
taxonomy, stop and admit a separate exception artifact and its exact candidate
join before recording the exception. This removes repeated empty values, needs
no new assertion, and prevents hypothetical exceptions from weakening current
coverage.

**Option 4 - Require rationale on every row:** this makes every classification
self-describing but duplicates source evidence and taxonomy meaning across the
entire baseline. It adds review and maintenance cost without increasing
authority and is rejected.

**Recommended boundary:** select Option 3 and change C1 acceptance to an exact
two-column table. Absence of an exception artifact means no exception is
admitted, not that a default rationale applies. Discovery of a real exception
is a typed re-plan trigger; it cannot be represented through an unknown class,
free-form fallback, or silently non-empty field.

**Decision:** Option 3 is selected. C1 has exactly `candidate_id` and
`semantic_class` columns. No exception artifact, sentinel class, rationale
field, default, or conditional-empty primitive exists. If semantic review finds
a candidate outside the five-class taxonomy, classification stops and a new
plan admission must define the exception artifact, exact candidate join,
authority, and verification before any exception is recorded.

##### VE043-A1-C1 Taxonomy-Precedence Re-plan Trigger

**Status:** `Accepted`

The first bounded semantic-review batch proves that the five taxonomy rows are
not yet a mutually exclusive decision procedure. A historical fixture count of
one can satisfy both historical snapshot and structural multiplicity. A count
of an explicitly listed set can appear to be either a declared finite contract
or mutable aggregate. Header framing (`NR > 1`), schema arity (`NF != 5`), and
status/sentinel comparisons are finite structural contracts but are not named
by the current declared-row/key wording. Classifying these by reviewer habit or
numeric shape would create an unrecorded fallback and non-reproducible evidence.

**Option 1 - Add an authority-first precedence procedure (`Recommended`):**
retain the five class identifiers, broaden declared finite contract to include
explicit schema framing, arity, fixed identity, and status protocol, and select
in order: policy-owned threshold; immutable historical evidence; explicit
finite contract; zero/one presence or uniqueness multiplicity; otherwise
current mutable aggregate. Require the selected class to be determined from
the number's authoritative purpose, not syntax. This keeps the compact schema
and gives every overlap one canonical result.

**Option 2 - Add structural framing and status classes:** create separate
classes for schema/header ordinals and protocol sentinels. This is more
descriptive but expands the taxonomy around Bash mechanisms rather than
migration action; all finite structural contracts still derive from explicit
schema or protocol authority.

**Option 3 - Permit several classes per candidate:** record every applicable
semantic tag. This preserves overlap information but complicates exact coverage,
action derivation, package grouping, and lifecycle joins without evidence that
multiple actions are needed.

**Option 4 - Keep the current table and use reviewer judgment:** choose whichever
class seems most useful for each overlap. This leaves precedence implicit and
is rejected as non-reproducible authority.

**Recommended boundary:** select Option 1 and make the precedence procedure
canonical beside the taxonomy. The procedure refines class applicability but
does not derive a class mechanically. C1 remains explicit per-candidate review;
the engine verifies only exact identity coverage and the closed class domain.
If a candidate still lacks one result after precedence, it triggers the already
admitted exception re-plan rather than receiving a default.

**Decision:** Option 1 is selected with positive-evidence enforcement. Review
tests classes in precedence order, but a class is selected only when its own
authority condition is established. `mutable-aggregate` is not an `otherwise`
default; it requires evidence that the literal summarizes a changing current
inventory. If no class has positive evidence, review stops for the admitted
exception re-plan. The procedure records one semantic decision and does not
infer it from a literal, operator, filename, or graph relationship.

##### VE043-A1-C1 Semantic Coverage Acceptance

**Status:** `Accepted`

Every generated candidate identity has one explicit reviewed semantic class in
`numeric-comparison-decisions.tsv`. The registered
`numeric-comparison-classification` suite enforces the exact two-column schema,
closed five-class domain, unique candidate identity, and candidate-ID set
equality with the immutable generated baseline. The table contains no path,
expression, owner, action, package, progress, count, rationale, or exception
field.

The focused suite and four focused positive/negative generic table and relation
tests pass. All 152 engine tests, Python compilation, all 107 registered
declarative suites, generated graph and numeric-audit freshness, both plan
checks, and diff integrity pass. No engine, generated artifact, Bash checker,
owner, package, standards source, lockfile, or workflow changed.

**No-fallback result:** every class was selected through the accepted
authority-first procedure. No syntax classifier, default class, inferred owner,
exception sentinel, compatibility schema, or duplicate candidate fact was
introduced. L1 remains responsible for proving that any future candidate
disappearance joins an accepted package and its explicit canonical owner.

##### VE043-A1-L1 Live-Derivation Capability Re-plan Trigger

**Status:** `Accepted`

L1 preflight proves that the admitted evidence exists but the current engine
cannot express its lifecycle. The immutable baseline contains derived candidate
identity and checker path, C1 covers every baseline identity, and the migration
package table supplies unique checker subjects, explicit owners, and reviewed
state. The current baseline spans 124 candidate-bearing checker paths, while 68
checker packages are accepted under 29 explicit owner values; these are derived
review observations, not expected totals.

The generic `relation` assertion reads two committed tables and can prove static
set equality, but it cannot obtain the current candidate set from the canonical
collector or authorize a set difference through a third table. Conversely,
`generate_numeric_audit.py --check` requires the committed immutable baseline
to equal the current live scan byte-for-byte. Its first authorized checker
retirement would therefore be reported as stale even when an accepted package
explicitly owns that retirement. Keeping both behaviors would make historical
baseline and current inventory competing authorities.

**Option 1 - Admit one typed numeric-audit lifecycle check (`Recommended`):**
add a side-effect-free Python assertion that reuses `collect_candidates` and
reads the immutable baseline, C1 decisions, and existing package table through
strict contained schemas. It rejects every current identity absent from the
baseline. For each baseline identity absent from current derivation, it requires
the baseline checker itself to be absent from canonical current inventory and
an exact unique package subject `checker:<baseline checker>` whose state is
`accepted` and whose owner is non-empty. Missing authority is typed
`unavailable`; duplicate, ambiguous, malformed, still-live-checker, and new-
candidate evidence is typed `invalid`. It derives current, missing, and
completed totals only for diagnostics. The strict byte-equality check is removed
or made to use this same lifecycle implementation atomically, so there is one
freshness authority. This qualifies under the custom-capability rule because a
safety-critical no-unexplained-disappearance invariant cannot otherwise be
expressed clearly.

**Option 2 - Generate and commit a second current-candidate artifact:** retain
the immutable baseline, regenerate a separate current snapshot after every
checker package, and add generated lifecycle rows for package joins. This can be
made exact, but it adds update ordering, generated churn, and another freshness
gate while still requiring custom logic to derive and validate conditional
package authority. Choose it only if a reviewable current snapshot is required
independently; no such requirement is established.

**Option 3 - Extend generic relations with executable source adapters or
callbacks:** allow relation sides to invoke the numeric collector and perform
conditional joins. This could generalize live derivation, but it introduces an
executable configuration surface and a broad abstraction without a second
coherent consumer. It conflicts with the engine's no-callback and capability-
admission boundaries and is rejected.

**Option 4 - Rewrite the baseline and C1 after every accepted package:** make
the historical baseline represent only current candidates. This avoids a new
assertion but destroys accepted audit evidence, forces semantic re-review churn,
and makes an unexplained disappearance indistinguishable from a routine
refresh. It violates L1's immutable-history objective and is rejected.

**Recommended admission boundary:** select Option 1 with no generalized live-
source plugin. The check may know the numeric candidate contract and package
subject prefix, but policy remains in the immutable baseline, explicit C1
decisions, and accepted package rows. It must not infer package or owner from a
name, graph edge, standards route, source text, or classifier. It must not write
current rows, expected counts, progress, owner mappings, or compatibility data.

**Decision:** Option 1 is selected. L1 will add one typed, side-effect-free
Python lifecycle check that reuses canonical candidate collection. The check
owns mechanics only: baseline and C1 records remain immutable evidence, and the
existing migration-package row remains the sole package/owner authority. A
missing candidate is valid only when its checker is absent from canonical live
inventory and exactly one accepted checker-package row supplies a non-empty
owner. The old strict current-versus-baseline byte-equality check must be removed
or delegate to the same lifecycle implementation in this slice; dual freshness
authority is prohibited.

**Proposed implementation write set:** numeric-audit and check-dispatch modules;
one focused lifecycle-check module; focused numeric lifecycle tests; the
numeric-classification suite and registry only if registration structure
requires it; engine documentation; count-authority and architecture reports;
and serial plan, issue, and ledger records. The immutable baseline, C1 decision
table, package manifest, generated graph, Bash checkers, standards sources,
lockfiles, and workflows remain read-only.

**Proposed acceptance:** focused positive evidence plus negative cases for new
identity, unexplained missing identity, missing package, ambiguous package,
non-accepted package, empty owner, and a candidate removed while its checker
remains live; all engine tests; Python compilation; all declarative suites;
generated graph freshness; both plan checks; diff integrity; and one shared-
contract complete-suite checkpoint. The byte-equality freshness path must not
remain as competing authority.

##### VE043-A1-L1 Lifecycle Acceptance

**Status:** `Accepted`

The registered numeric-classification suite now includes one typed
`numeric_audit_lifecycle` check. It reads the exact immutable baseline, C1
decisions, and package schemas, derives canonical live checker inventory and
current candidates in-process, rejects every new identity, rejects candidate
removal from a still-live checker, and authorizes retired-checker candidates
only through one exact accepted checker-package row with a non-empty owner.
Missing package or owner authority is typed `unavailable`; malformed,
ambiguous, non-accepted, and unexplained evidence is typed `invalid`.

The former numeric `--check` byte-equality mode and `check_snapshot` API are
removed. Baseline creation remains write-once and immutable, while the
registered lifecycle check is the sole current-state authority. No current
snapshot, expected total, progress field, owner map, callback, relation adapter,
Bash bridge, inferred package, inferred owner, or compatibility path remains.

Twelve focused lifecycle tests and 13 baseline collector/writer tests pass. All
163 engine tests, Python compilation, all 107 registered declarative suites,
the focused three-check repository suite, generated inventory/graph freshness
at 170 verifiers / 175 nodes / 855 edges / 171 components, both plan checks,
diff integrity, and all 170 canonical mixed entrypoints pass. Baseline, C1,
package, graph, checker, standards, lockfile, and workflow evidence is unchanged.

##### VE043-P1 Owner-Closure Re-plan Trigger

**Status:** `Accepted`

The read-only incident-edge audit invalidates P1's one-package assumption. The
four named checkers do not form one dependency-closed owner-coherent unit:

- row 35 is a singleton generated component, but it executes Commit Authority,
  Contract Ownership, the execution train, root-index closure, root README
  audit, and root-router evidence and dynamically executes transitive contract
  consumers;
- row 45 is in a generated two-checker strongly connected component with
  Language Index Closure and also executes Language Profile Routing, the root
  README audit, root-router evidence, and the execution train;
- row 46 is in a generated four-checker strongly connected component with Rust
  Adoption Notes Retirement, Rust Index Closure, and Rust Profile Authority
  Closure, while also executing independently owned Rust API, Rust Async, Rust
  Tooling, Rust Unsafe, language-routing, root-audit, and execution-train
  checks; and
- the root README audit is a separate infrastructure checker with inbound
  executable references from root-index, language-index, rows 35/45/46, and
  Rust profile closure and outbound checks of Commit Authority, language-index,
  root-index, root-router, and unadmitted S1 routing.

None of the four named checkers or the reciprocal language/Rust closure
checkers has a canonical migration-package row. The immutable numeric baseline
currently associates 27 candidates with row 35, nine with row 45, 11 with row
46, and eight with the root audit; these are derived audit observations, not
expected counts. A single package would therefore either cross policy owners,
preserve nested Bash orchestration, duplicate authority, or silently omit
incident edges and prerequisites. All are prohibited.

**Option 1 - Ordered owner-coherent package train (`Recommended`):** replace P1
with a decomposition stage that freezes one canonical owner, responsibility
set, exact incident-edge closure, declarative dependency, allowed write set,
and retirement condition for each package. Keep root README/routing
infrastructure, Language Index closure, Rust profile/index closure, and
Milestone 7 lifecycle evidence as separate semantic owners. Include discovered
root-index and S1 prerequisites in the train rather than hiding them, and
transfer each executable caller edge only when its callee's registered suite is
accepted. Integrate shared registry, package, graph, README, and plan changes
serially. This preserves exact authority while allowing bounded owner packages.

**Option 2 - One atomic transitive-closure wave:** migrate every named checker,
reciprocal component member, inbound caller, and prerequisite together. This
can eliminate dangling calls in one state transition, but it creates a broad
cross-owner write set with several independently changing contracts and weakens
reviewability. Choose it only if later evidence proves the contracts cannot be
separated without an invalid intermediate state; current evidence does not.

**Option 3 - Retain the orchestration checkers while migrating semantic
leaves:** register owner suites but keep rows 35/45/46 and the root audit as
long-lived Bash integration gates. This minimizes immediate graph edits, but it
retains repeated transitive Bash execution and delays the engine-only objective.
It is valid only for a checker proven to own a durable independent integration
contract, not as a compatibility bridge or default.

**Option 4 - Reviewed retirement of historical-only checks:** delete a checker
without replacement only after exact evidence proves every observable contract
is historical bookkeeping already owned by accepted declarative suites and no
caller remains. This may apply to individual lifecycle assertions during the
Option 1 train, but cannot retire the four candidates as a group: the root audit
still owns live dynamic inventory and route checks, and the row checkers still
own migration evidence.

**Recommendation:** select Option 1. Its first slice is read-only P1-D1
decomposition: produce an exact responsibility/owner/edge matrix and an ordered
package train, then stop if any behavior lacks one canonical owner or any
intermediate state requires dual authority. No package is admitted by this
trigger record.

**Decision:** Option 1 is selected. P1-D1 must classify every observable
responsibility of the candidate checkers, resolve its canonical owner from
existing standards and migration authority, record exact incident edges and
available declarative coverage, and define the retirement condition for each
proposed package. The resulting train must be dependency ordered and keep
shared registry, package, edge, README, graph, and plan integration serial. P1-D1
is read-only with respect to executable and package authority and admits no
checker migration by itself.

**No-fallback rule:** do not infer owner from graph adjacency, checker name, or
file location; do not preserve a Bash caller around a migrated suite; do not
invoke Python through Bash; do not combine owners to reduce package count; and
do not treat absence from a proposed package as retirement authority.

**Trigger write set:** this plan, the parent plan, issues, count-authority
report, and canonical execution ledger only. Checkers, suites, fixtures,
registry, package and edge manifests, generated graph, numeric evidence,
standards sources, lockfiles, and workflows remain read-only.

##### VE043-P1-D1 Owner Decomposition And VE045 Capability Re-plan

**P1-D1 status:** `Accepted`

P1-D1 separates conservative graph references from executable behavior. The
generated `executable_reference` edge means a shell or Python source contains a
checker basename; `verifier_dependency` means the dependency extractor matched
a quoted verifier path. Neither edge proves invocation by itself. Exact script
review therefore owns whether a reference executes, inspects, or merely names
another checker, while all generated incident edges remain lifecycle evidence
that must be dispositioned before deletion.

The ordered package train is:

| Order | Package responsibility | Canonical owner | Existing coverage | Required transfer |
| --- | --- | --- | --- | --- |
| 1 | S1 routed vertical slice | `migration.parent-plan` | metadata graph, text, Markdown links, line budget | remove its root-consumer classification row |
| 2 | row-35 migration lifecycle | `migration.parent-plan` | table, relation, reference inventory, text | retain only unique lifecycle evidence; remove nested checker execution |
| 3 | root index closure | `STANDARDS-ROUTER.md` | table, relation, text | move root purity here; remove nested root-audit/router execution |
| 4 | language index closure | `STANDARDS-ROUTER.md` | table, relation, text | remove row-45 duplicate semantic checks and invocation |
| 5 | row-45 migration lifecycle | `migration.parent-plan` | table, relation, text | retain lifecycle evidence only |
| 6 | Rust adoption-notes retirement | `migration.parent-plan` | table and text | remove duplicate retirement checks and calls from Rust index/row 46 |
| 7 | Rust migration-index closure | `profiles/languages/rust/README.md` | table, relation, text | remove duplicate index checks and invocation from row 46 |
| 8 | Rust profile authority closure | `profiles/languages/rust/README.md` | metadata graph, Markdown links, text | remove duplicate profile checks and invocation from row 46 |
| 9 | row-46 migration lifecycle | `migration.parent-plan` | table, relation, text | retain lifecycle evidence only; remove nested checker execution |
| 10 | root README consumer inventory | `verification-engine.migration` | reference inventory, table, relation, text | migrate remaining dynamic Bash-consumer evidence after group callers are gone |

Every package receives its own checker subject, owner, exact incident-edge
rows, suite, write set, and acceptance. Semantic transfer may edit a surviving
caller only to remove the transferred invocation or duplicate assertion. It may
not move that caller's remaining lifecycle authority. Shared registry, package,
edge, README-consumer, generated graph, and plan integration stays serial;
independent suite/fixture preparation may be isolated after capability
acceptance.

**VE045 status:** `Accepted`

Before VE045, the train could not preserve all observable contracts through the
existing engine checks. Root, language, and Rust migration indexes each require
an exact ordered Markdown heading set plus a distinct explicit maximum line
threshold. Required and prohibited text does not prove exact heading order or
exclude additional headings, while `exact_text` would freeze unrelated prose.
Rust adoption retirement also requires the former authority path itself to
remain absent; empty table projections prove corpus state but cannot prove
filesystem absence.

**Option 1 - Two narrow generic checks (`Recommended`):** add
`markdown_structure` with one contained UTF-8 path, exact ordered Markdown
headings, and one positive maximum-line threshold; add `absent_paths` with one
non-empty unique contained path list that succeeds only when every path is
absent. Both are typed, side-effect-free, directly tested, and policy-neutral.
The three index owners justify the structure primitive, and removed-authority
non-reappearance justifies the absence primitive as a safety-critical
invariant. Implement them as a shared-contract slice before package 1.

**Option 2 - Freeze complete index files with `exact_text`:** preserve exact
headings and line limits by snapshotting all bytes and add only `absent_paths`.
This uses less engine code but turns unrelated prose and link edits into
verification-contract changes, increasing churn and moving authority from the
owned semantic constraints to whole-file snapshots. Choose it only if the
index files are intentionally immutable; they are not.

**Option 3 - Use required/prohibited text and table absence only:** avoid engine
work by checking known headings as literals and proving the retired artifact is
absent from corpus tables. This cannot reject extra/reordered headings, an
over-budget index, or a reappearing untracked file. It is a lower-fidelity
fallback and is rejected.

**Option 4 - Add package-specific Python checks:** implement the missing logic
inside S1, root, language, and Rust package checks. This preserves behavior but
duplicates common mechanics, increases custom surface, and conflicts with the
generic-engine objective. It is rejected unless generic contracts cannot
express an observed invariant.

**Recommendation:** select Option 1. The capability slice may touch only the
two check modules, check registration, one focused test module, engine and
architecture documentation, and serial plan records. Package suites, fixtures,
registry, package/edge manifests, generated evidence, Bash checkers, standards
sources, lockfiles, and workflows remain read-only until the shared-contract
checkpoint passes.

**Decision:** Option 1 is selected. Implement the two policy-neutral checks as
one shared-engine contract, prove their positive and typed-negative behavior,
and run the complete shared-contract checkpoint before any P1 admission. Do
not add whole-file snapshots, substring or corpus-only approximations,
package-specific implementations, Bash bridges, callbacks, or inferred
defaults.

**Capability acceptance:** focused positive and typed negative tests for exact
heading order, extra/missing headings, threshold equality/excess, invalid UTF-8,
missing/escaping/symlink paths, malformed configuration, present forbidden
paths, and absent paths; all engine tests; Python compilation; all declarative
suites; generated graph freshness; both plan checks; diff integrity; and one
canonical complete-suite checkpoint.

**Acceptance evidence:** 16 focused file-contract tests and all 179 engine tests
pass; Python compilation succeeds; all 107 declarative suites pass; generated
evidence is fresh at 170 Bash verifiers, 175 nodes, 855 edges, and 171
components; both plan checks and diff integrity pass; and all 170 canonical
mixed checker entrypoints pass. No package authority or legacy checker changed.

##### M6-P1 S1 Routing Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 71.

The clean preflight proves that the current S1 contract is fully expressible by
existing generic engine checks. One `metadata_graph` assertion validates the
six selected modules as a closed graph; six owner-local `text` assertions bind
each selected path to its exact module ID; `markdown_links` validates local
destinations; `line_budget` preserves the strict `observed * 4 < baseline`
contract against `normative_and_derived_lines`; and one root `text` assertion
prohibits `Read each document`. The legacy checker passes at 1,074 selected
newline bytes against the current derived 11,066-line baseline, and an
independent read-only engine preflight passes every proposed generic assertion.

The generated graph has three executable incident edges: an inbound basename
identity assertion from the root README consumer audit and outbound
`executable_reference` and `helper_dependency` edges to `check-metadata.sh`.
All three have exact typed dispositions. The retained root audit remains an
independent gate after its obsolete S1-only identity assertion is removed; the
metadata helper remains an independently owned artifact for other consumers.
The fourth incident edge is a non-executable `contract_reference` from the
README-consumer manifest. Implementation removes that obsolete classification
row and the matching root-audit category/assertion; it is not treated as a
runtime call or an executable-edge disposition.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/s1-routing.toml`; the deleted
`verify-s1-routing.sh` and its private
`fixtures/routing/s1-rust-library.expected`; README-consumer manifest and root
consumer audit; verification README; all four generated checker artifacts; this
plan; checker-inventory report; canonical evaluation ledger; and parent plan.
Canonical standards sources, metadata helper, engine code and tests, schemas,
numeric evidence, unrelated suites/fixtures/checkers, lockfiles, generated
build output, and workflows remain read-only.

**No-fallback rule:** register and pass the declarative suite before deleting
the Bash checker. Do not retain the fixture, wrapper, nested invocation,
duplicate root-purity assertion, Bash-to-Python bridge, package-specific check,
whole-file snapshot, inferred module set, alternate line baseline, or silent
consumer-row removal. Any additional incident edge, consumer, routed behavior,
or required engine capability is a re-plan trigger.

**Acceptance gate:** focused S1 suite; retained root consumer audit; package and
exact incident-edge authority; all declarative suites; removed checker and
fixture paths; README route; graph freshness; both plan checks; exact read-only
source/helper/engine/schema evidence; diff integrity; and the deferred
`M6-P-W1` mixed checkpoint at the bounded P1 wave boundary.

**Admission verification:** current S1 and the complete proposed generic
assertion set pass; package projection and exact executable-edge authority
pass; all 107 registered declarative suites pass; generated evidence is fresh
at 170 Bash verifiers / 175 nodes / 859 edges / 171 components; exact generated
review shows only four new contract references from package and edge authority;
both plan checks and diff integrity pass.

**Acceptance evidence:** the registered ten-check S1 suite passes exact
path-to-ID bindings, metadata closure, local links, strict context ratio, and
root routing boundary. The Bash checker and private fixture are absent. The
root consumer audit derives and passes 25 remaining consumers after the obsolete
classification and S1-only assertion are removed; row 35 passes with the same
derived inventory. Package and edge authority prove the checker and all three
executable incident edges are absent. All 108 declarative suites pass; generated
evidence is fresh at 169 Bash verifiers / 174 nodes / 852 edges / 170
components; shell syntax and removed-path evidence pass. Canonical standards,
metadata helper, engine, tests, schemas, numeric evidence, lockfiles, build
output, and workflows are unchanged. The mixed Bash checkpoint remains
explicitly deferred to `M6-P-W1`.

##### M6-P2 Row-35 Lifecycle Package

**Status:** `Accepted`

**Package state:** `accepted` at train order 72.

Exact script review separates row 35's unique lifecycle evidence from nested
execution. The unique contract is: two ordered execution-decomposition rows
covering `STD-0001` through `STD-0006`; six exact owner/disposition rows;
reviewed README-dependency classifications and live evidence paths; four exact
transitive Contract Ownership callers; required decomposition headings and
no-fallback statements; exact row-35 execution-train and package-gate records;
and three historical parent-plan acceptance markers. Current dependency,
consumer, and caller totals are derived reports and are not expected values.

The declarative suite uses exact `table` projections for finite lifecycle
membership and fields, `reference_inventory` for contained evidence and caller
membership, and newline-bounded `text` assertions for direct invocation and
decomposition/parent-plan evidence. One exact caller-selection suffix derives
the four current caller paths from canonical live checker inventory after the
row-35 source is removed; per-caller newline-bounded assertions preserve the
two accepted shell variable forms without regex, command execution, or parser
inference.

The generated graph has ten executable incident edges, all outbound to six
retained independent gates: Commit Authority, Contract Ownership, execution
train, root index closure, root README consumer audit, and root Router evidence.
All ten receive exact `independent-gate` dispositions. Four additional checker
executions are loaded dynamically from the transitive-caller manifest and do
not appear as row-35 graph edges; the suite preserves their exact membership and
invocation lines while removing their nested execution. Generated package
contract references remain lifecycle evidence only.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/milestone-7-row-35-decomposition.toml`; the
deleted row-35 checker; verification README; all four generated checker
artifacts; this plan; checker-inventory report; canonical evaluation ledger;
and parent plan. Every lifecycle TSV/Markdown input, all four dynamic callers,
all six retained gate checkers, standards sources, engine code/tests, schemas,
numeric evidence, unrelated suites/fixtures/checkers, lockfiles, build output,
and workflows remain read-only.

**No-fallback rule:** register and pass the suite before deleting the checker.
Do not execute a retained checker from Python or Bash, preserve a wrapper,
infer invocation from graph shape, copy mutable counts, add a caller snapshot,
rewrite lifecycle evidence, duplicate another owner's semantic assertions, or
retain Bash and declarative authority together. Any missing exact table/text
representation, additional incident edge, caller form, or changed lifecycle
owner is a re-plan trigger.

**Acceptance gate:** focused row-35 suite; package and exact incident-edge
authority; all declarative suites; removed checker path; README route; graph
freshness; both plan checks; exact read-only lifecycle/caller/gate/source/engine
evidence; diff integrity; and the deferred `M6-P-W1` mixed checkpoint.

**Admission verification:** the current row-35 checker passes; package
projection and all ten exact incident-edge dispositions pass; all 108
declarative suites pass; generated evidence is fresh at 169 Bash verifiers /
174 nodes / 857 edges / 170 components and adds only five non-executable
contract references from package/edge authority; both plan checks and diff
integrity pass.

**Implementation:** the registered 14-check suite now owns the exact finite
decomposition, owner/disposition, execution-train, accelerated-package, report,
and parent-plan decisions. It validates all open README-dependency paths and
derives the exact four transitive callers from canonical generated checker
inventory, then proves each caller's newline-bounded invocation without
executing it. The Bash checker is deleted, and all ten incident-edge states
transition with the package to `accepted`.

**Acceptance verification:** the focused suite, package authority, and exact
incident-edge authority pass; all 109 declarative suites pass; the retired path
and generated-inventory row are absent; generated evidence is fresh at 168
Bash verifiers / 173 nodes / 850 edges / 169 components; both plan checks and
diff integrity pass. Every lifecycle TSV/Markdown input, all four callers, all
six retained gates, standards sources, engine code/tests, schemas, numeric
evidence, lockfiles, build output, and workflows remain unchanged. The mixed
Bash checkpoint remains deferred to `M6-P-W1`.

**No-fallback rule:** do not replace exact structure with substring checks,
replace absent-path evidence with table absence, freeze whole files for
convenience, infer invocation from graph edge type, or retain a custom or Bash
implementation beside the generic checks.

##### M6-P3 Root Index Closure Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 73.

Exact review freezes the root index's unique contract: the four ordered README
headings and 32-line ceiling; six exact resource/target/role rows and live
repository-local links; explicit entrypoint, routing-diagnostic, resource, and
license statements; exact prohibited legacy catalog, template, customization,
license-paraphrase, and closure text; and exact dispositions for `STD-0001`
through `STD-0006`. Resource and disposition totals are finite membership
decisions, not separately copied expected counts.

The suite can express this contract with existing `markdown_structure`,
`markdown_links`, `table`, and newline-bounded `text` checks. It requires no
engine extension, command, regex, callback, whole-file snapshot, inferred
default, or changed standards source. `README.md`, the resource fixture, and
consolidation dispositions remain read-only evidence.

The checker has five executable incident edges. Its two calls to the root
README audit and root Router evidence, plus their two verifier-dependency edges,
are retained `independent-gate` relationships. The inbound root-audit identity
assertion follows the accepted M6-P1 transfer: remove the obsolete
`root-closure-verifier` manifest row and exact Bash identity assertion while the
audit remains independently owned. Do not turn either retained gate into a
suite dependency or duplicate its remaining semantics.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/root-index-closure.toml`; the deleted root
index checker; verification README; README-consumer manifest; root README audit
checker; all four generated checker artifacts; this plan; checker-inventory
report; canonical evaluation ledger; and parent plan. Root README, Router,
resource fixture, dispositions, retained Router evidence checker, all other
checkers/suites/fixtures, engine code/tests, schemas, numeric evidence,
lockfiles, build output, and workflows remain read-only.

**No-fallback rule:** register and pass the exact suite before deleting the
checker. Do not retain a wrapper, nested execution, obsolete consumer identity,
duplicate root-purity assertion, alternate route evidence, Bash-to-Python
bridge, copied mutable count, or weaker substring approximation. Any additional
incident edge, unmatched root-index assertion, changed canonical owner, or
required engine behavior is a re-plan trigger.

**Acceptance gate:** focused root-index suite; retained root audit; package and
all five exact incident-edge rows; all declarative suites; removed checker and
consumer-row proof; README route; graph freshness; both plan checks; exact
read-only source/fixture/disposition/gate/engine evidence; diff integrity; and
the deferred `M6-P-W1` mixed checkpoint.

**Admission verification:** the current root-index checker and its retained
Router/audit gates pass; package projection and all five exact incident-edge
rows pass; all 109 declarative suites pass; generated evidence is fresh at 168
Bash verifiers / 173 nodes / 852 edges / 169 components and adds only two
contract references; diff integrity passes.

**Acceptance evidence:** the registered five-check suite passes exact root
heading order and line ceiling, six resource identities/roles and live links,
the routing boundary and legacy-authority prohibitions, and six exact
dispositions. The Bash checker is absent. The retained root audit passes with
24 derived consumers after its obsolete root-closure identity is removed, and
root Router evidence still passes independently. M6-P3 and all five historical
incident-edge rows are accepted; the two affected M6-P2 rows now point to the
registered suite using the accepted VE046 independent-gate form without a
registry dependency. All 110 declarative suites pass; generated evidence is
fresh at 167 Bash verifiers / 172 nodes / 843 edges / 168 components; removed
paths, both plan checks, read-only boundaries, and diff integrity pass. The
mixed Bash checkpoint remains deferred to `M6-P-W1`.

##### M6-P4 Language Index Closure Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 74.

Exact review freezes the Language Index contract: the two ordered headings and
14-line ceiling; live links; required non-normative navigation, Router,
applicability, Rust-profile, diagnostic, and no-fallback statements; prohibited
legacy catalog and policy text; exact owner-map membership for `STD-0704` and
`STD-0705`; their exact index dispositions; exact row-45 owner-validation
outcomes; and the Router owner metadata plus Language Profiles heading.

An isolated worktree probe passed the proposed seven-check suite using existing
`markdown_structure`, `markdown_links`, `text`, and `table` checks. The suite
has `requires = []`. It needs no engine extension, callback, command, expected
mutable total, whole-file snapshot, inferred owner, or changed standards
source. `languages/README.md`, the owner map, dispositions, row-45 owner
validation, Router, and retained route gates remain read-only evidence.

The checker has eleven executable incident edges. Its four calls and matching
dependency edges retain Language Profile Routing, row-45 lifecycle, root
consumer audit, and root Router evidence as independent gates. The inbound
row-45 call and dependency plus the inbound root-audit identity are duplicate
lifecycle mechanisms to remove while both callers retain their remaining
authority. The consumer-manifest contract reference is removed with the
obsolete `language-index-closure` row; it is not reclassified as executable
authority. No retained gate becomes a suite dependency.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/language-index-closure.toml`; the deleted
Language Index checker; verification README; README-consumer manifest; root
README audit checker; row-45 lifecycle checker; all four generated checker
artifacts; this plan; checker-inventory report; canonical evaluation ledger;
and parent plan. Language Index, Router, owner map, dispositions, row-45 source
records, retained route/audit checkers outside the exact duplicate transfer,
all other suites/fixtures, engine code/tests, schemas, numeric evidence,
lockfiles, build output, and workflows remain read-only.

**No-fallback rule:** register and pass the exact suite before deleting the
checker. Remove nested execution, the two-checker cycle, obsolete consumer
identity, and duplicate row-45 assertions in the same acceptance slice. Do not
retain a wrapper, add a registry dependency, copy mutable counts, infer owner
or applicability from links, weaken exact projections to substring evidence,
or preserve Bash as alternate authority.

**Acceptance gate:** focused Language Index suite; retained Language Profile,
row-45, root audit, and root Router gates; package and all eleven exact edge
rows; all declarative suites; removed checker/consumer/caller proof; graph
freshness; both plan checks; exact read-only evidence; diff integrity; and the
deferred `M6-P-W1` mixed checkpoint.

**Admission verification:** the isolated seven-check suite probe and current
Language Index/row-45 checkers pass. Package projection and all eleven exact
edge rows pass; all 110 declarative suites pass; generated evidence is fresh at
167 Bash verifiers / 172 nodes / 850 edges / 168 components; both plan checks
and diff integrity pass. Any additional incident edge, unrepresentable
assertion, changed owner, required engine behavior, or failure of a retained
gate is a re-plan trigger.

**Joint acceptance evidence:** the registered seven-check suite passes and the
Language Index Bash checker is absent. M6-P4 and all eleven owner-local edge
rows are accepted; its four cycle rows use the registered row-45 suite as
independent evidence with no dependency. The obsolete consumer row and audit
classification are absent, and the retained audit derives 23 consumers.

##### M6-P5 Row-45 Lifecycle Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 75.

Exact owner review reduces row 45 to migration lifecycle authority: one exact
execution-train row, one exact P37 accelerated-package row, the bounded row-45
decomposition record, and three accepted parent-plan claims. Language Index
content, Router metadata, owner-map/disposition outcomes, and README-consumer
identity belong to M6-P4 and are not duplicated by M6-P5.

An isolated worktree probe passed the proposed four-check suite using existing
`table` and `text` checks. It has `requires = []` and executes no retained
checker. No engine extension, callback, command, mutable count, inferred owner,
or changed lifecycle input is required.

Generated evidence records twelve executable incident edges: two directions
of the Language Index cycle plus row-45 calls to Language Profile Routing, the
execution train, root consumer audit, and root Router evidence, each represented
as an executable reference and verifier dependency. M6-P5 owns all twelve
historical dispositions from the row-45 endpoint. The four cycle rows also
appear under M6-P4 from its separately owned endpoint; this is explicit
owner-local accountability, not one merged package or duplicated suite
behavior. During joint acceptance, cycle evidence transitions to the opposite
registered suite while retained gates remain checker-backed independent gates.

**Allowed implementation write set:** M6-P4's admitted write set plus package
and edge manifests; package projection; suite registry;
`suites/milestone-7-row-45-decomposition.toml`; deletion of the row-45 checker;
verification README; all four generated checker artifacts; this plan, issue
register, checker-inventory report, canonical evaluation ledger, and parent
plan. Execution train, accelerated packages, decomposition record, Language
Index, Router, owner map, dispositions, row-45 owner validation, retained gates,
engine, schemas, numeric baseline/classification, lockfiles, build output, and
workflows remain read-only.

**Joint no-fallback rule:** M6-P4 and M6-P5 retain separate owners, suites,
diagnostics, and package rows but share one atomic acceptance commit. Register
and pass both suites before deleting either checker. Delete both Bash checkers,
remove obsolete consumer/audit identity, accept both packages and all 23
owner-local edge rows, and prove numeric lifecycle from each absent checker and
its own accepted package. Do not add partial-candidate waivers, merge owners,
create suite dependencies, retain wrappers, disguise numeric expressions, or
leave either package half accepted.

**Admission verification:** the isolated four-check suite, current row-45 and
Language Index checkers, package projection, and all M6-P4/P5 edge rows pass;
all 110 declarative suites pass; generated evidence is fresh at 167 Bash
verifiers / 172 nodes / 850 edges / 168 components. Both plan checks and diff
integrity pass.

**Joint acceptance evidence:** the registered four-check suite passes and the
row-45 Bash checker is absent. M6-P5 and all twelve owner-local edge rows are
accepted; its four cycle rows use the registered Language Index suite as
independent evidence with no dependency. Numeric lifecycle passes by deriving
both absent checker subjects from their separately owned accepted packages.
All 112 declarative suites pass; generated evidence is fresh at 165 Bash
verifiers / 170 nodes / 824 edges / 167 components. Canonical standards,
ownership/disposition/lifecycle records, numeric baseline and engine remain
byte-identical to the captured implementation boundary. The mixed checkpoint
remains deferred to `M6-P-W1`.

##### VE047 Language Index Numeric-Lifecycle Re-plan

**Status:** `Accepted`; Option 3 implemented.

The M6-P4 implementation probe passed its seven-check suite, four retained
gates, package authority, and all eleven edge rows after deleting the Language
Index checker and transferring duplicate audit/row-45 identity assertions.
`numeric-comparison-classification` then returned
`ASSERT.NUMERIC_LIFECYCLE_CHECKER_STILL_LIVE` for row 45. Exact comparison with
the immutable baseline shows one vanished candidate: the row-45 `-eq 1`
assertion that the README-consumer manifest contains exactly one Language Index
Bash checker row. M6-P4 must remove that obsolete row and assertion, but row 45
remains live under the admitted package boundary.

The failed implementation was fully reversed to clean admission commit
`e64890d`. M6-P4 remains `admitted`; no suite, registry, checker, consumer,
edge/package state, generated artifact, standards source, evidence table,
engine, schema, numeric baseline, lockfile, build output, or workflow change
remains.

**Option 1 - Add partial live-checker candidate retirement:** extend numeric
lifecycle with explicit per-candidate retirement authority joined to an
accepted package or edge transfer. This can represent the immediate edit but
creates a second lifecycle manifest and broadens mutation authority for every
live checker. It is justified only if row 45 must remain Bash after M6-P4 and is
not recommended while its own declarative retirement is already planned.

**Option 2 - Preserve or rewrite the numeric assertion:** keep an `-eq 1`
comparison against another row, retain the obsolete consumer identity, or
change syntax to evade candidate collection. This would preserve false
authority or game verification and is prohibited.

**Option 3 - Admit M6-P5 and close the owner-separated SCC atomically
(`Recommended`):** retain separate M6-P4 (`STANDARDS-ROUTER.md`) and M6-P5
(`migration.parent-plan`) packages and suites, but integrate both checker
retirements in one commit. M6-P5 declaratively preserves row-45 lifecycle and
removes its nested execution. Both Bash checkers then become absent with one
accepted explicitly owned package each, satisfying the existing derived
numeric lifecycle without a per-candidate waiver. Shared registry, package,
edge, generated graph, README/audit, and plan files remain serial.

**Option 4 - Broaden M6-P4 to own row 45:** delete both checkers under one
package. This crosses canonical owners, conflicts with P1-D1, and obscures
separate diagnostics and acceptance. It is rejected.

**Recommendation:** select Option 3. Before executable work, preflight and admit
M6-P5 with exact row-45 behavior, all incident edges not already dispositioned
by M6-P4, a bounded write set, and a joint SCC acceptance condition. Verify the
two suites before deletion; then delete both Bash checkers, transfer obsolete
consumer/caller identities, accept both packages and edge rows, and prove
numeric lifecycle from absent checker plus accepted owner evidence. Do not add
numeric exceptions, duplicate shared edge rows, false suite dependencies,
wrappers, syntax evasions, or cross-owner suite authority.

**Decision:** Option 3 is selected. M6-P5 is admitted at train order 75 after
its four-check suite passed in isolation. M6-P4 and M6-P5 remain separate
canonical-owner packages and must transition to accepted together in one SCC
closure commit. Existing numeric lifecycle remains unchanged and must pass from
the two absent checker paths plus their accepted package owners.

**Acceptance:** both owner-separated packages transitioned to accepted in one
commit after both suites passed. Both Bash checkers, the cycle, and obsolete
consumer identity are absent. Numeric lifecycle passes unchanged; no waiver,
merged owner, false dependency, wrapper, syntax evasion, or fallback remains.

##### VE048 Rust Four-Checker Lifecycle Re-plan

**Status:** `Accepted`; Option 1 is implemented through staged admissions and
one atomic acceptance.

Read-only preflight of P1 package 6 found that Rust adoption-notes retirement
is not an independently removable leaf. The generated graph places it in one
four-member strongly connected component with Rust migration-index closure,
Rust profile authority closure, and row-46 lifecycle. The members invoke one
another, row 46 requires all three checker paths to remain executable, and
Rust index closure also invokes adoption retirement. Removing or partially
editing only package 6 would therefore leave a dangling caller, preserve a
checker stub, or remove immutable numeric candidates from still-live checkers.

The component crosses two canonical owners but not four semantic contracts:

| Package | Checker subject | Canonical owner | Declarative responsibility |
| --- | --- | --- | --- |
| M6-P6 | `checker:evaluation/standards-effectiveness/verify-rust-adoption-notes-retirement.sh` | `migration.parent-plan` | retired path, corpus absence, frozen historical metrics, and route absence |
| M6-P7 | `checker:evaluation/standards-effectiveness/verify-rust-index-closure.sh` | `profiles/languages/rust/README.md` | migration-index structure, four exact dispositions, and no legacy authority |
| M6-P8 | `checker:evaluation/standards-effectiveness/verify-rust-profile-authority-closure.sh` | `profiles/languages/rust/README.md` | canonical profile metadata, specialized routes, typed diagnostics, and no legacy authority |
| M6-P9 | `checker:evaluation/standards-effectiveness/verify-milestone-7-row-46-decomposition.sh` | `migration.parent-plan` | row-46 execution, package, decomposition, disposition, and accepted-plan lifecycle |

**Option 1 - Separate packages with atomic SCC acceptance (`Recommended` and
selected):** preflight and admit M6-P6 through M6-P9 separately, preserving one
checker subject, canonical owner, suite, diagnostics, exact incident-edge
projection, and bounded write set per package. Do not implement any member
until all four admissions pass. Then register and verify the four suites before
deleting all four Bash checkers and accepting all package and owner-local edge
rows in one commit. Internal historical edges point to the opposite registered
suite as `independent-gate` evidence and create no registry dependency unless
preflight proves a real semantic prerequisite. Existing absent-checker plus
accepted-package lifecycle authority must explain every retired numeric
candidate without changing the engine or immutable baseline.

**Option 2 - Sequential acceptance with partial live-checker lifecycle
authority:** introduce explicit candidate-retirement records so one member can
be edited or deleted while other SCC members remain live. This creates mutable
per-candidate bookkeeping and additional authorization paths despite a bounded
component already being known. It is rejected.

**Option 3 - Preserve wrappers or checker stubs:** keep executable paths that
delegate to suites until later packages migrate. This is a compatibility
fallback, retains dual authority, and is prohibited.

**Option 4 - Merge the component into one cross-owner package or suite:** make
one acceptance unit own all four contracts. This obscures diagnostics and
canonical ownership and conflicts with P1-D1. It is rejected.

**Selected execution sequence:** admit M6-P6, M6-P7, M6-P8, and M6-P9 in that
order through plan-only package/edge authority updates and focused isolated
suite probes. Admissions derive edge and numeric identities from canonical
inventories rather than declaring aggregate counts. After all four packages
are admitted, one serial implementation may add/register their separate
suites, remove duplicate consumer identity, delete all four Bash paths, accept
all four packages and their owner-local edge rows, regenerate graph evidence,
and run focused suites, numeric lifecycle, removed-path, package/edge,
declarative-all, graph-freshness, plan, and diff checks. The mixed Bash
checkpoint remains the already declared `M6-P-W1` wave boundary.

**No-fallback rule:** no package may own another package's semantic contract;
no suite dependency may be inferred from the obsolete Bash cycle; no wrapper,
stub, candidate waiver, syntax evasion, duplicate authority, hand-maintained
aggregate count, or sequential partial implementation is permitted. A failed
isolated suite probe, an unrepresentable assertion, a real cross-suite semantic
dependency, a dirty authority file, or inability to close all four members in
one accepted state is a new re-plan trigger.

##### M6-P6 Rust Adoption-Notes Retirement Acceptance

**Status:** `Accepted`

**Package state:** `accepted` at train order 76.

The isolated five-check suite proves the retired adoption-notes path is absent,
the canonical six-column live corpus contains no matching path, frozen metrics
retain the one exact historical row, and neither the legacy Rust index nor the
Router names the retired route. It uses existing `absent_paths`, `table`, and
`text` assertions with `requires = []`; no engine extension, compatibility
schema, inferred count, callback, command, or source change is needed.

M6-P6 owns the adoption-retirement contract only. Exact generated evidence
projects every incident relationship from the canonical graph: row 46 and Rust
index call adoption retirement, while adoption retirement calls row 46 and
Rust profile closure. Each executable relationship has matching reference and
verifier-dependency authority. During admission, every row points to its live
opposite checker as `independent-gate` evidence. Atomic acceptance must replace
those internal checker identities with the opposite registered suite without
creating registry dependencies.

**Allowed implementation write set:** the four package/edge/registry authority
files; `suites/rust-adoption-notes-retirement.toml`; all four Rust SCC Bash
checkers solely for their jointly accepted deletion and duplicate-call removal;
verification README; all four generated graph artifacts; this plan; issue and
inventory reports; canonical evaluation ledger; and parent plan. The retired
path, corpus, frozen metrics, Rust index, Router, numeric baseline, engine,
schemas, all unrelated suites and fixtures, lockfiles, build output, and
workflows remain read-only.

**Acceptance gate:** M6-P7 through M6-P9 admitted; all four isolated suites
pass before deletion; all four packages and their exact owner-local edge rows
accept in one commit; numeric lifecycle derives every missing candidate from
the four absent checker subjects and accepted explicit owners; removed paths,
all declarative suites, graph freshness, plan checks, read-only hashes, and diff
integrity pass. The mixed checkpoint remains deferred to `M6-P-W1`.

**Admission evidence:** corrected isolated suite passes all five checks. The
current adoption, index, profile, and row-46 checkers pass; package projection
and exact edge authority pass; all declarative suites, graph freshness, both
plan checks, read-only hashes, and diff integrity must close this admission.
Any added incident edge, changed source contract, required suite dependency,
or failed future isolated suite is a re-plan trigger.

**Acceptance evidence:** the registered five-check suite passes with no
dependencies and the Bash checker is absent. Package and exact owner-local edge
authority are accepted atomically with M6-P7 through M6-P9; internal historical
edges use registered-suite independent-gate evidence without creating registry
dependencies. Numeric lifecycle, removed-path proof, all 116 declarative
suites, and fresh generated evidence at 161 Bash verifiers / 166 nodes / 781
edges / 166 components pass. Canonical Rust sources, frozen history, Router,
engine, schemas, and numeric baseline remain unchanged.

##### M6-P7 Rust Migration-Index Closure Acceptance

**Status:** `Accepted`

**Package state:** `accepted` at train order 77.

The isolated dependency-free four-check suite preserves the complete two-
heading Rust migration-index structure and explicit line ceiling, exact
`STD-0827` through `STD-0830` owner-map membership, their exact two `index` and
two `split` dispositions, required typed routing diagnostics, and prohibited
legacy catalog and policy authority. Existing `markdown_structure`, `table`,
and `text` assertions represent the contract without source edits, mutable
counts, snapshots, callbacks, commands, or engine changes.

M6-P7 owns only the Rust migration-index contract. Exact graph projection
records row 46 calling Rust index and Rust index calling row 46, adoption
retirement, and Rust profile closure in both generated edge views. Each row
uses the live opposite checker as independent evidence during admission. The
future atomic acceptance must use the opposite registered suites without
turning obsolete Bash calls into suite dependencies.

**Allowed implementation write set:** the same serial SCC integration files
frozen by VE048 and M6-P6, plus `suites/rust-index-closure.toml`. Canonical Rust
index content, owner map, dispositions, profile, Router, adoption evidence,
numeric baseline, engine, schemas, unrelated suites and fixtures, lockfiles,
build output, and workflows remain read-only.

**Acceptance gate:** M6-P8/M6-P9 admitted; all four suites pass before deletion;
all packages and owner-local edges accept atomically; numeric lifecycle,
removed paths, all declarative suites, graph freshness, both plan checks,
read-only hashes, and diff integrity pass. `M6-P-W1` remains the mixed wave
checkpoint.

**Admission evidence:** the isolated suite passes all four checks. Current SCC
checkers, package and exact edge authority, all declarative suites, graph
freshness, plan checks, read-only hashes, and diff integrity must close this
admission. New semantics, changed ownership, or a required dependency triggers
re-plan.

**Acceptance evidence:** the registered four-check suite passes with no
dependencies and the Bash checker is absent. Its exact package and owner-local
edge rows accepted in the same four-member transition. Rust index structure,
owner-map membership, dispositions, and no-legacy authority remain canonical;
no wrapper, suite dependency, source edit, or fallback was introduced.

##### M6-P8 Rust Profile Authority Closure Acceptance

**Status:** `Accepted`

**Package state:** `accepted` at train order 78.

The isolated dependency-free three-check suite preserves canonical Rust profile
metadata and dependency validity, all ten specialized profile links, typed
`unavailable`, `invalid`, and `unsupported` diagnostics, and explicit
prohibition of legacy Rust authority and inferred mechanism defaults. Existing
`metadata_graph`, `markdown_links`, and `text` assertions represent the owner
contract without source edits, snapshots, callbacks, commands, engine changes,
or nested checker execution.

M6-P8 owns only the Rust profile boundary. Exact graph projection records the
three inbound SCC callers, reciprocal row-46 call, and six retained outbound
gates in both generated edge views. The retained Rust API, async, tooling,
unsafe, language-profile-routing, and root-audit checkers remain independently
owned; the old profile checker's orchestration does not transfer their
semantics or create declarative suite dependencies.

**Allowed implementation write set:** the serial SCC integration files frozen
by VE048; `suites/rust-profile-authority-closure.toml`; and the README-consumer
manifest/root-audit files needed to remove the obsolete Bash-consumer identity.
Canonical Rust profile content, specialized profiles, Router, adoption and
index evidence, numeric baseline, retained independent checkers, engine,
schemas, unrelated suites and fixtures, lockfiles, build output, and workflows
remain read-only.

**Acceptance gate:** M6-P9 admitted; all four suites pass before deletion; all
packages and owner-local edges accept atomically; obsolete README-consumer
identity is removed without weakening the root audit; numeric lifecycle,
removed paths, all declarative suites, graph freshness, both plan checks,
read-only hashes, and diff integrity pass. `M6-P-W1` remains the mixed wave
checkpoint.

**Admission evidence:** the isolated suite passes all three checks and has no
dependencies. Current SCC and retained outbound checkers, package and exact
edge authority, all declarative suites, graph freshness, plan checks, read-only
hashes, and diff integrity must close this admission. New profile semantics,
changed owner boundaries, an undeclared incident edge, or a required suite
dependency is a re-plan trigger.

Admission closed with package and exact incident-edge authority passing, all
112 registered declarative suites passing, all four current SCC checkers
passing, numeric lifecycle passing, and generated evidence fresh at 165 Bash
verifiers / 170 nodes / 838 edges / 167 components. Both plan checks, frozen
profile/consumer/routing hashes, and diff integrity also pass. The mixed Bash
suite remains intentionally deferred to `M6-P-W1`.

**Acceptance evidence:** the registered three-check suite passes with no
dependencies and the Bash checker plus its obsolete README-consumer identity
are absent. The root audit derives 22 remaining consumers. Exact package and
edge authority preserve retained API, async, tooling, unsafe, language-routing,
and root-audit checks as independently checker-backed gates. Canonical profile
content and specialized owners remain unchanged.

##### M6-P9 Row-46 Lifecycle Acceptance

**Status:** `Accepted`

**Package state:** `accepted` at train order 79.

The isolated dependency-free seven-check suite preserves exact row-46 execution
and P38 package records, the four unique owner-validation rows, set-equal owner
map and disposition lineage, the decomposition contract, and accepted parent-
plan claims. Existing `table`, `relation`, and `text` assertions derive closure
from canonical tables without aggregate counts, source duplication, callbacks,
commands, engine changes, or nested checker execution.

M6-P9 owns only migration lifecycle. It does not reassert Rust profile, index,
adoption-retirement, API, async, tooling, unsafe, language-routing, root-audit,
or execution-train semantics. Exact graph projection records three inbound SCC
calls and ten outbound gates in both generated views. Every opposite checker
remains independent evidence during admission; the obsolete Bash SCC creates no
declarative dependency.

**Allowed implementation write set:** the serial SCC integration files frozen
by VE048, all four proposed suites and checker paths, registry/package/edge
authority, obsolete README-consumer identity and its root audit, verification
README, derived graph artifacts, numeric lifecycle evidence only through its
existing derivation, and serial plan/report/ledger files. Canonical standards,
owner-validation and decomposition records, train/package/disposition/owner-map
tables, retained independent checkers, engine, schemas, unrelated suites and
fixtures, lockfiles, build output, and workflows remain read-only.

**Acceptance gate:** copy and register all four already-proved suites with empty
dependency lists; prove them before deletion; remove the obsolete profile
consumer identity; delete all four Bash paths; transition M6-P6 through M6-P9
and all owner-local rows to accepted with internal evidence rewritten to the
opposite registered suites; then pass focused suites, numeric lifecycle,
removed paths, package/edge authority, all declarative suites, graph freshness,
both plan checks, frozen read-only hashes, and diff integrity. The mixed Bash
suite runs once at `M6-P-W1` after atomic acceptance.

**Admission evidence:** the isolated suite passes all seven checks and has no
dependencies. Current SCC and retained gates, package and exact edge authority,
all declarative suites, graph freshness, plan checks, frozen lifecycle hashes,
and diff integrity must close this admission. A suite requiring another SCC
suite, an undeclared incident edge, inability to remove all four checkers, or a
required edit outside the frozen atomic write set is a re-plan trigger.

Admission closed with package and exact incident-edge authority passing, all
112 registered declarative suites passing, all four current SCC checkers and
the retained language-routing/root-audit/execution-train gates passing, numeric
lifecycle passing, and generated evidence fresh at 165 Bash verifiers / 170
nodes / 838 edges / 167 components. Both plan checks, frozen lifecycle hashes,
and diff integrity also pass. Regeneration was byte-identical because prior SCC
admissions already referenced every affected checker path. The mixed Bash suite
remains intentionally deferred to `M6-P-W1`.

**Acceptance evidence:** all four registered suites pass with empty dependency
lists and all four Bash checkers are absent. All four package rows and 62
owner-local edge rows accepted atomically; every internal historical edge names
the opposite registered suite as independent evidence, while retained gates
remain checker-backed. Package/edge authority, numeric lifecycle, all 116
declarative suites, graph freshness at 161 Bash verifiers / 166 nodes / 781
edges / 166 components, and removed-path proof pass. The subsequent `M6-P-W1`
checkpoint passes all 161 remaining Bash entrypoints.

##### M6-P-W1 P1 Wave Checkpoint

**Status:** `Accepted`

The canonical fail-fast mixed checkpoint passes all 161 remaining Bash
entrypoints after M6-P1 through M6-P9 acceptance. It includes all 116 registered
declarative suites and confirms that retained owner, lifecycle, routing,
disposition, source-closure, and migration gates remain green after removal of
the four Rust SCC members.

No later package is admitted. The next action is a read-only fresh-graph and
ownership audit. Any proposed package must derive its canonical owner, semantic
contract, exact incident edges, dependencies, write set, and verification gates
from current evidence before admission; stale pre-P1 graph shape is not
authority.

##### VE049 Post-P1 Owner-Wave Decomposition

**Status:** `Accepted`; Option 2 selected for staged admission, concurrent local
preparation, and serial integration.

The fresh post-P1 graph has 161 Bash verifiers, five helpers, 781 edges, 166
singleton components, and no cycles. Forty-eight verifiers have no executable
callers, but only the temporary declarative launcher and historical security
re-plan checker are executable-edge-free. The launcher remains required by the
current complete-suite convention. The security checker still owns four cross-
owner package records and a live IPC-checker identity. Neither is an admissible
semantic leaf.

Four disjoint caller-free candidates have bounded unique contracts:

| Package | Checker subject | Canonical owner | Unique contract | Current nested relationships |
| --- | --- | --- | --- | --- |
| `M6-Q1` | `checker:evaluation/standards-effectiveness/verify-rust-tooling-criterion.sh` | `profiles/languages/rust/tooling.md` | sixteen Criterion adapter decisions, canonical/profile/reference boundaries, one exact `STD-0834` split | no executable edge; four accepted historical independent-gate rows must transfer to the registered suite |
| `M6-Q2` | `checker:evaluation/standards-effectiveness/verify-accessibility-evidence-closure.sh` | `topics/accessibility.md` | thirteen evidence decisions, canonical/reference/legacy boundaries, four exact dispositions, accepted lifecycle claims | Accessibility Media remains an independently owned gate, not evidence-closure semantics |
| `M6-Q3` | `checker:evaluation/standards-effectiveness/verify-architecture-population.sh` | `migration.parent-plan` | legacy-index route purity, exact `STD-0137` through `STD-0147` population, accepted population lifecycle | Architecture Owner and row-15 lifecycle remain independent gates |
| `M6-Q4` | `checker:evaluation/standards-effectiveness/verify-coding-dependency-route.sh` | `STANDARDS-ROUTER.md` | one non-normative Coding index route, one exact `STD-0157` index disposition, accepted route lifecycle | Dependencies Owner and row-15 lifecycle remain independent gates |

Graph topology does not establish these owners. Q1 and Q2 are the canonical
semantic owners named by their standards metadata. Q3 owns migration population
closure rather than Architecture policy. Q4 owns route/index closure rather
than Dependencies policy. Nested Bash execution is orchestration evidence and
does not become a suite dependency unless an isolated semantic preflight proves
that the candidate's own result cannot be evaluated without the callee result.

**Concurrency contract:** each package receives its own suite TOML, retained
fixture paths, deleted checker path, and focused probe. These local paths may be
prepared in separate worktrees only after that package is individually
admitted. Registry, package and edge manifests, package projection, README,
generated graph, plans, ledgers, reports, and lifecycle consumer records are
serial integration-owner files. Prepared patches are proposals, not accepted
authority, and must be rebased and revalidated against the current integration
revision.

**Selected order:** preflight and admit Q1 first because it has no executable
edge and exercises accepted checker-to-suite independent-gate transfer. Then
preflight Q2, Q3, and Q4 independently. If all four isolated suites pass with
existing primitives and no real cross-suite dependency, their local suite and
checker paths may be prepared concurrently. Integrate one package at a time in
Q1 through Q4 order, regenerate exact graph evidence after each deletion, and
run one mixed checkpoint at `M6-Q-W1`.

**No-fallback rule:** do not merge owners, copy callee semantics, infer suite
dependencies from nested Bash calls, retain wrappers, preserve checker paths as
aliases, create per-edge waivers, or encode mutable aggregate counts. Existing
declarative assertions must preserve each unique contract at equal or greater
fidelity. A missing primitive, changed canonical source, additional incident
edge, disputed owner, non-disjoint local write set, true dependency on an
unmigrated suite, or required shared-contract change is a new re-plan trigger.

**Planning write set:** this plan, child and canonical ledgers, issue and
checker-inventory reports, parent plan, and the four generated graph artifacts
whose reference edges derive from plan text. Checker, fixture, suite, registry,
package, edge, README, standards, engine, schema, baseline, lockfile, build
output, and workflow authority remain unchanged.

**Planning verification:** current four candidate checkers and all named
retained gates; generated inventory freshness; all declarative suites; both
plan checks; exact graph-diff review; and diff integrity. Package-specific
admission gates are frozen only after isolated suite probes.

##### M6-Q1 Rust Tooling Criterion Package Admission

**Status:** `Active`; implementation is authorized after VE053.

**Package state:** `accepted` at train order 80.

An isolated dependency-free suite proves the complete Criterion contract with
existing generic assertions. One `decision` check reproduces all sixteen
fixture outcomes with typed invalid, unavailable, unsupported, and allow
results. Three `text` checks preserve the canonical profile, reference recipe,
and former-source boundary. One exact `table` projection proves the single
`STD-0834` split without relying on a copied count. The probe and the live Bash
checker both pass, and the temporary registry and suite were removed after the
comparison.

The current generated graph has no executable incident edge for the Q1
checker, so the package uses explicit `edge-free` authority and must have no
edge-disposition row. Its only current graph edge is a `contract_reference`
from the accepted historical edge manifest. Four accepted M6-P8 and M6-P9
`independent-gate` rows still use `checker:` evidence for Q1. Implementation
must transfer those rows to `suite:rust-tooling-criterion` after registration;
that evidence transition creates no registry dependency.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/rust-tooling-criterion.toml`; the deleted
`verify-rust-tooling-criterion.sh`; all four generated checker artifacts; this
plan; child ledger; issues; checker-inventory report; canonical evaluation
ledger; and parent plan. The Criterion fixture, canonical profile, reference
recipe, former source, consolidation dispositions, all retained gates, other
suites/checkers, verification README, engine code/tests, schemas, numeric
evidence, lockfiles, build output, and workflows remain read-only.

**No-fallback rule:** register and pass the five-check suite before deleting
the Bash checker. Do not retain a wrapper, Bash-to-Python bridge, duplicate
fixture, copied count, alternate Criterion defaults, whole-file snapshot,
package-specific assertion, false `requires` dependency, or checker-backed
historical evidence after deletion. Any new executable incident edge, changed
source contract, missing generic capability, or inability to transfer all four
historical rows is a re-plan trigger.

**Acceptance gate:** focused Q1 suite; live checker equivalence before deletion;
package projection and edge-free authority; exact four-row historical evidence
transfer; all declarative suites; removed checker path; graph freshness; both
plan checks; exact read-only source/fixture/disposition evidence; diff
integrity; and the deferred `M6-Q-W1` mixed checkpoint.

**Admission verification:** the disposable five-check suite and live checker
both pass all sixteen decisions and the exact disposition. The package
projection, edge-free contract, all 116 registered declarative suites, fresh
161-verifier / 166-node / 783-edge / 166-component graph, both plan checks, and
diff integrity pass. No suite, registry entry, edge row, checker, fixture,
standards source, engine, schema, numeric evidence, lockfile, build output, or
workflow authority changed.

**Acceptance evidence:** the dependency-free five-check suite is registered
and passes all sixteen decisions, source boundaries, and exact `STD-0834`
disposition. The Bash checker is absent. Four accepted M6-P8/P9 historical
independent-gate rows retain immutable checker lineage while naming
`suite:rust-tooling-criterion` and its exact suite path as evidence; no registry
dependency was added. Package/edge authority, all declarative suites, graph
freshness, both plan checks, removed-path and read-only-source proof, and diff
integrity pass. The mixed checkpoint remains deferred to `M6-Q-W1`.

##### M6-Q2 Accessibility Evidence Closure Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 81.

An isolated dependency-free suite proves the complete evidence-closure contract
with seven generic checks. One `decision` check reproduces all thirteen fixture
outcomes with typed invalid, unavailable, unsupported, and allow results. Two
`text` checks preserve canonical Accessibility evidence claims and the
non-normative legacy lint reference. `markdown_headings` derives every
level-two legacy-index heading and requires `Migrated` on each without a count
or copied inventory. A second legacy-index text check prohibits the three old
mechanism literals. One exact table projection proves `STD-0023` through
`STD-0026`, and one text check preserves the two accepted lifecycle claims.
The disposable suite and live Bash checker both pass; temporary files were
removed.

The current generated graph has exactly two executable incident edges for Q2,
both from the Q2 checker to `verify-accessibility-media.sh`: one
`executable_reference` and one `verifier_dependency`. Isolated preflight proves
Accessibility Media is a separately owned integration gate, not an input to
Q2's decision result. Both rows therefore use `independent-gate` with exact
retained checker evidence. Q2 declares no registry dependency and copies no
media semantics.

**Allowed implementation write set:** package and edge manifests; package
projection; suite registry; `suites/accessibility-evidence-closure.toml`; the
deleted `verify-accessibility-evidence-closure.sh`; all four generated checker
artifacts; this plan; child ledger; issues; checker-inventory report; canonical
evaluation ledger; and parent plan. The Accessibility decision fixture,
canonical owner, reference recipe, legacy index, consolidation dispositions,
parent-plan lifecycle claims, Accessibility Media checker and evidence, all
other suites/checkers, verification README, engine code/tests, schemas, numeric
evidence, lockfiles, build output, and workflows remain read-only.

**No-fallback rule:** register and pass the seven-check suite before deleting
the Bash checker. Do not retain a wrapper or Bash bridge, copy Accessibility
Media behavior, add a false `requires` dependency, duplicate the decision
fixture, copy a heading inventory or count, freeze the whole index, weaken the
legacy prohibition, create package-specific code, infer outcomes, or retain the
deleted checker as evidence. Any changed source contract, additional incident
edge, missing generic capability, unavailable retained media gate, or inability
to preserve exact typed outcomes is a re-plan trigger.

**Acceptance gate:** focused Q2 suite; live checker equivalence before deletion;
package projection and exact two-row edge authority; retained Accessibility
Media gate without a registry dependency; all declarative suites; removed
checker path; graph freshness; both plan checks; exact read-only
source/fixture/disposition/lifecycle evidence; diff integrity; and the deferred
`M6-Q-W1` mixed checkpoint.

**Admission verification:** the disposable seven-check suite and live checker
both pass all thirteen decisions, source boundaries, heading policy, four exact
dispositions, and lifecycle claims. Package projection and exact edge authority
pass against the current graph. No permanent suite, registry entry, checker,
fixture, standards source, engine, schema, numeric evidence, lockfile, build
output, or workflow changed.

**Acceptance evidence:** the dependency-free seven-check suite is registered
and passes thirteen typed decisions, source boundaries, derived heading policy,
four exact dispositions, and accepted lifecycle claims. The Bash checker is
absent. Both historical Accessibility Media edges remain independent and
checker-backed without a registry dependency. Numeric lifecycle derives the
retired symbolic candidate from the unchanged reviewed baseline and Q2's
accepted explicit owner; no baseline or decision row changed. Package/edge
authority, retained media, all declarative suites, graph freshness, both plan
checks, removed-path/read-only-source proof, and diff integrity pass. The mixed
checkpoint remains deferred to `M6-Q-W1`.

##### M6-Q3 Architecture Population Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 82.

An isolated dependency-free suite proves Q3's complete migration-population
contract with four generic checks. One text check preserves the Architecture
route in `CODING-STANDARDS.md`; a second prohibits the six retired architecture
headings and mechanism literals. One exact table projection proves
`STD-0137` through `STD-0147` without a copied count, and one text check
preserves accepted `7.4b8be` and `7.4b8bf` lifecycle claims. The disposable
suite and live Bash checker both pass; temporary files were removed.

The current generated graph has exactly four executable incident edges for Q3:
an `executable_reference` and `verifier_dependency` to Architecture Owner, and
the same pair to row-15 decomposition. Isolated preflight proves both are
separately owned integration gates, not inputs to Q3's route, prohibition,
disposition, or lifecycle result. All four rows therefore use
`independent-gate` with exact retained checker evidence. Q3 declares no
registry dependency and copies neither callee's behavior.

**Allowed implementation write set:** the exact `M6-Q3` row in
`checker-migration-packages.tsv`, verified by the registered
`checker-migration-packages` projection suite, is the sole file-level scope
authority. Canonical standards, consolidation dispositions, parent-plan
lifecycle claims, retained Architecture Owner and row-15 gate behavior, all
unlisted suites/checkers, fixtures, engine code/tests, schemas, numeric
evidence, lockfiles, build output, and workflows remain semantically excluded.

**No-fallback rule:** register and pass the four-check suite before deleting
the Bash checker. Do not retain a wrapper or Bash bridge, copy either retained
gate, add false `requires` dependencies, duplicate disposition evidence, use an
aggregate count, freeze unrelated source bytes, infer lifecycle state, create
package-specific code, or retain the deleted checker as evidence. Any changed
source contract, additional incident edge, missing generic capability,
unavailable retained gate, or inability to preserve exact disposition and
lifecycle evidence is a re-plan trigger.

**Acceptance gate:** focused Q3 suite; live checker equivalence before deletion;
package projection and exact four-row edge authority; both retained gates
without registry dependencies; all declarative suites; removed checker path;
graph freshness; both plan checks; exact read-only source/disposition/lifecycle
evidence; diff integrity; and the deferred `M6-Q-W1` mixed checkpoint.

**Admission verification:** the disposable four-check suite and live checker
both pass route, prohibition, eleven-disposition, and lifecycle evidence.
Package projection and exact edge authority pass against the current graph. No
permanent suite, registry entry, checker, standards source, fixture, engine,
schema, numeric evidence, lockfile, build output, or workflow changed.

**Acceptance evidence:** the dependency-free four-check suite is registered
and passes the Architecture route, source-wide retired-literal prohibitions,
eleven exact dispositions, and accepted lifecycle claims. The Bash checker is
absent and the README names only the registered suite as the current
entrypoint. All four historical Architecture Owner and row-15 edges remain
independent and checker-backed without registry dependencies or copied
behavior. Package/edge authority, retained gates, all declarative suites,
graph freshness, both plan checks, removed-path/README/read-only-source proof,
and diff integrity pass. The mixed checkpoint remains deferred to `M6-Q-W1`.

##### VE051 Q3 README Authority Re-plan

**Status:** `Accepted`; Option 1 selected and Q3 shared integration has not
started.

Fresh-base proposal reconstruction found a shared consumer omitted from Q3's
admitted write set. The standards-effectiveness README names the current Bash
checker as the entrypoint proving Architecture population. Deleting that
checker would leave stale documented authority. Editing the README under the
current package would exceed exact admission. The proposal worktree changed
only its permitted suite and checker paths; no shared implementation authority
was changed.

**Option 1 - Re-admit Q3 with the README (`Recommended`):** add the README to
Q3's exact implementation write set and add `readme-route` to its verification
contract. During one atomic acceptance, replace the obsolete Bash-entrypoint
sentence with the registered `architecture-population` suite and the evidence
it derives. Register and pass the suite before checker deletion, then prove the
README contains the suite identity and no deleted checker path. This is one
owner-coherent Architecture-population outcome; the README remains a mechanical
projection rather than a second semantic owner. It matches the accepted M3-DT1
recovery precedent and creates no intermediate invalid state.

**Option 2 - Serial README prerequisite:** admit a separate documentation-only
transition that changes the README before Q3 acceptance, then make Q3 depend on
it. Choose this only if the README has concurrent edits or needs an independent
review owner. Otherwise it creates an avoidable interval in which documentation
names an unregistered suite and adds lifecycle ceremony without separating a
real concern.

**Option 3 - Defer Q3 and the Q wave:** leave Q3 admitted but unavailable and
pause Q3/Q4 integration until README authority can be resolved. This preserves
the frozen serial order and avoids unauthorized edits, but does not advance the
migration. Skipping to Q4 would violate the accepted Q1-through-Q4 integration
order and is not part of this option.

Retaining the Bash checker, adding a wrapper or alias, deleting it while the
README remains stale, changing the README outside package authority, weakening
removed-path verification, or treating the stale reference as non-authoritative
noise are not valid options. Selection must update package manifest and
projection, plan/ledger/report authority, exact write set, and verification
contract before Q3 implementation resumes.

**Selected recovery:** Option 1. Q3 is re-admitted with the README in its exact
write set, `VE051` in its prerequisite authority, and `readme-route` in its
verification contract. The implementation must register and pass
`architecture-population`, replace only the obsolete README entrypoint
projection, delete the Bash checker, and prove both the suite route and removed
path in one atomic acceptance. No implementation file changed during
re-admission.

##### VE052 Q3 Duplicated Scope Authority Re-plan

**Status:** `Accepted`; Option 1 selected and Q3 integration is authorized.

Post-re-admission implementation review found that Q3's prose “Allowed
implementation write set” still classifies the verification README as
read-only, while the canonical package manifest and its checked projection now
include that README. The Q-wave freeze declares the manifest to be the source
for the exact write set, but contradictory plan prose still creates an
ambiguous authorization boundary. Editing the README would violate one
statement; not editing it would violate accepted VE051. The reconstructed Q3
proposal remains isolated and no shared implementation edit was made.

**Option 1 - Derive scope from the package manifest (`Recommended`):** replace
Q3's copied file enumeration with a direct pointer to the canonical `M6-Q3`
manifest row and retain only concise semantic exclusions/invariants in prose.
Require package-projection verification to prove the machine-readable row.
Then resume Q3 implementation under that single exact scope authority. This
removes the drift mechanism, keeps the plan legible, and follows the freeze's
existing declaration that package values are not copied into another
machine-readable authority.

**Option 2 - Patch both copies:** add the README to Q3's prose list and remove
it from the read-only sentence. This is the smallest textual repair and leaves
all current validators unchanged, but preserves two manually synchronized
scope descriptions and can reproduce the same failure during later
re-admission.

**Option 3 - Separate generated plan projection:** generate Q3's prose scope
from the package manifest and verify freshness. Choose this only if reviewers
need a full file list inline in every package section. It eliminates manual
drift but adds generator/template ownership and churn that are not justified
for the current plan because the checked manifest already provides the exact
list.

Silently preferring one authority, editing the README under contradictory
scope, dropping the accepted README change, weakening exact package
projection, or adding a wrapper/alias is invalid. Selection must resolve the
duplicate authority before Q3 implementation resumes.

**Selected recovery:** Option 1. Q3's copied file enumeration is removed. The
checked `M6-Q3` package row is the sole exact write-set authority, while this
plan retains only semantic exclusions that constrain how authorized files may
change. No generator or second scope projection is added. Q3 may resume only
after the package projection passes against the current manifest.

##### M6-Q4 Coding Dependencies Route Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 83.

An isolated dependency-free suite proves Q4's complete route-closure contract
with three generic checks. One text check preserves the dependency-route heading
and canonical Dependencies destination while prohibiting the retired
`DEPENDENCY-STANDARDS.md` route throughout the non-normative Coding index. This
is conservatively stronger than the Bash check's section-local prohibition and
cannot authorize legacy policy. One exact table projection proves the
`STD-0157` index disposition, and one text check preserves accepted `7.4b8bi`
and `7.4b9s` lifecycle claims. The disposable suite and live Bash checker both
pass; temporary files were removed.

The current generated graph has exactly four executable incident edges for Q4:
an `executable_reference` and `verifier_dependency` to Dependencies Owner, and
the same pair to row-15 decomposition. Isolated preflight proves both are
separately owned integration gates, not inputs to Q4's route, prohibition,
disposition, or lifecycle result. All four rows therefore use
`independent-gate` with exact retained checker evidence. Q4 declares no
registry dependency and copies neither callee's behavior.

**Allowed implementation write set:** the exact `M6-Q4` row in
`checker-migration-packages.tsv`, verified by the registered
`checker-migration-packages` projection suite, is the sole file-level scope
authority. Canonical standards, consolidation dispositions, parent-plan
lifecycle claims, retained Dependencies Owner and row-15 gate behavior, all
unlisted suites/checkers, fixtures, engine code/tests, schemas, numeric
evidence, lockfiles, build output, and workflows remain semantically excluded.

**No-fallback rule:** register and pass the three-check suite before deleting
the Bash checker. Do not retain a wrapper or Bash bridge, copy either retained
gate, add false `requires` dependencies, reintroduce a section parser, weaken
the whole-index legacy-source prohibition, duplicate disposition evidence, use
an aggregate count, infer lifecycle state, create package-specific code, or
retain the deleted checker as evidence. Any changed source contract,
additional incident edge, missing generic capability, unavailable retained
gate, or inability to preserve exact disposition and lifecycle evidence is a
re-plan trigger.

**Acceptance gate:** focused Q4 suite; live checker equivalence before deletion;
package projection and exact four-row edge authority; both retained gates
without registry dependencies; all declarative suites; removed checker path;
graph freshness; both plan checks; exact read-only source/disposition/lifecycle
evidence; diff integrity; and the deferred `M6-Q-W1` mixed checkpoint.

**Admission verification:** the disposable three-check suite and live checker
both pass route, conservative prohibition, exact disposition, and lifecycle
evidence. Package projection and exact edge authority pass against the current
graph. No permanent suite, registry entry, checker, standards source, fixture,
engine, schema, numeric evidence, lockfile, build output, or workflow changed.

**Acceptance evidence:** the registered dependency-free three-check suite
passes the Coding dependency route, whole-index retired-source prohibition,
exact `STD-0157` disposition, and accepted lifecycle claims. The Bash checker
is absent. All four historical Dependencies Owner and row-15 edges remain
independent and checker-backed without registry dependencies or copied
behavior. Package/edge authority, retained gates, all declarative suites,
graph freshness, both plan checks, removed-path/read-only-source proof, and
diff integrity pass. The closing mixed checkpoint is next at `M6-Q-W1`.

##### VE053 Q4 Scope Authority Consistency Re-plan

**Status:** `Accepted`; Option 1 selected and Q4 integration is authorized.

Post-Q3 review found that Q4's active package section still copies its exact
file-level write set into prose. It currently matches the canonical package
row, so no present scope contradiction exists. However, VE052 established the
manifest-derived design specifically to remove manual scope drift, and Q4 is
the next active package governed by the same Q-wave freeze. Implementing Q4
under the older duplicated representation would knowingly retain inconsistent
procedure and recreate the failure mechanism just removed from Q3.

**Option 1 - Apply manifest-derived scope to Q4 (`Recommended`):** replace
Q4's copied file enumeration with a pointer to the checked `M6-Q4` manifest row
and retain semantic exclusions only. Do not alter the already admitted row.
Verify package projection, then resume the prepared proposal. This gives the
remaining active Q-wave work one scope authority without touching accepted
historical package sections.

**Option 2 - One-time Q4 exception:** retain the matching prose list and
implement Q4. This is immediately valid because no contradiction exists, but
it leaves adjacent active Q packages under different scope models and depends
on reviewers manually proving synchronization.

**Option 3 - Refactor every package section:** convert all active and accepted
package prose to manifest-derived scope before Q4. This creates broad
consistency, but expands a local integration prerequisite into historical plan
cleanup with large review cost and no additional Q4 semantic evidence.

Silently treating Q4 as exempt, changing its manifest scope without admission,
editing outside the checked row, or introducing generated/copy authority is
invalid. Selection must be recorded before Q4 implementation resumes.

**Selected recovery:** Option 1. Q4's copied file enumeration is removed. The
checked `M6-Q4` package row is the sole exact write-set authority, while this
plan retains only semantic exclusions that constrain how authorized files may
change. No generator, exception, or second scope projection is added. Q4 may
resume only after the package projection passes against the current manifest.

##### M6-Q-W1 Q-Wave Checkpoint

**Status:** `Accepted`

The canonical fail-fast mixed checkpoint passes all 157 surviving Bash
entrypoints after Q1 through Q4 acceptance. The run includes all 120 registered
declarative suites and confirms that retained owner, lifecycle, routing,
disposition, source-closure, and migration gates remain green after the four
Q-wave checker retirements.

No later package is admitted. The next action is a read-only fresh graph and
ownership audit. Any proposed package must derive its canonical owner,
semantic contract, exact incident edges, dependencies, write set, and
verification gates from current evidence before admission; stale pre-Q-wave
graph shape is not authority.

##### VE054 Post-Q Package-Selection Re-plan

**Status:** `Accepted`; Option 1 selected for bounded owner-first continuation.

The fresh accepted graph contains 157 Bash verifiers, 162 nodes, 773 edges,
and 162 components. Forty-six verifiers have no executable caller, but only
two are also free of verifier dependencies: the declarative-suite bridge and
the Milestone 7 Security checker-repair replan gate. Both are infrastructure
or recovery gates, not ordinary semantic leaves. Graph topology therefore
cannot safely choose the next migration.

The smallest viable semantic candidate is the 19-line Accessibility Media
checker. Its canonical owner is `topics/accessibility.md`; its call to
Accessibility Name/Input is a separately owned gate; and two accepted Q2 edge
records retain the Media checker as historical independent-gate evidence. A
valid package must preserve the 13 typed decisions, canonical/reference/legacy
boundaries, three exact dispositions, and accepted lifecycle claim, then
transfer those two historical evidence values to the registered Media suite
without declaring a dependency.

Short row-decomposition candidates are not interchangeable with Media. Rows
25 and 27 project Implementation lifecycle; rows 32 and 33 preserve
Persistence and Contracts decomposition while accepted N-wave records retain
their checker paths as independent lifecycle evidence. Their final package
owner and evidence-transfer model must be decided explicitly before they can
form a concurrent wave. Generated Command Security and Release Build are also
caller-free, but the standards-effectiveness README names them and their
retained row gates remain separate owners, so they require serial README
projection and exact edge treatment.

**Option 1 - Bounded owner-first continuation (`Recommended`):** preflight and
admit Accessibility Media as the next single owner-coherent package. Freeze its
exact suite contract, two historical evidence transfers, retained Name/Input
gate, write set, and verification before implementation. In parallel only at
the planning/proposal level, classify row-lifecycle candidates by canonical
owner for a later wave. This advances executable retirement without letting an
unresolved lifecycle model contaminate the package.

**Option 2 - Freeze a multi-owner staged wave first:** perform read-only
semantic preflight for Accessibility Media, Generated Command Security,
Release Build, and selected lifecycle rows; admit each separately; then prepare
disjoint local suites concurrently and integrate shared registry, edge,
README, graph, and planning authority serially. This can increase throughput,
but requires resolving every lifecycle owner and README consumer before any
implementation starts.

**Option 3 - Resolve lifecycle-checker ownership first:** defer ordinary
semantic packages and define whether row-decomposition evidence is owned by
the migration parent, the destination domain, or an explicit split between
projection and domain gates. Then freeze and migrate the repeated row family
as separately owned packages. This offers the largest later batching gain but
adds an architecture prerequisite and leaves the already clear Media package
idle.

**Option 4 - Add a new generic engine capability first:** derive a common
decomposition assertion only if isolated suite probes prove current text,
table, relation, and Markdown checks cannot preserve the repeated row
contracts. No current evidence demonstrates such a capability gap, so choosing
this now risks package-specific overengineering.

Inferring owner from graph proximity, deleting either infrastructure gate as a
semantic leaf, merging owners for batch size, retaining a Bash wrapper,
declaring false suite dependencies, leaving historical checker evidence stale,
or editing README projections outside an admitted write set is invalid.

**Selected recovery:** Option 1. Accessibility Media receives isolated
semantic preflight as the next bounded owner-coherent candidate. Admission must
freeze its exact suite contract, two accepted Q2 historical evidence
transfers, retained Accessibility Name/Input gate, write set, and verification
contract before implementation. Lifecycle-row classification remains separate
planning work and cannot broaden or block this package unless preflight finds a
real shared dependency or ownership conflict.

##### M6-R1 Accessibility Media Package Admission

**Status:** `Accepted`

**Package state:** `accepted` at train order 84.

Disposable preflight proved that one dependency-free suite with six generic
checks preserves all thirteen typed decisions, canonical Accessibility media
rules, non-normative web mechanisms, exact `STD-0020` through `STD-0022`
dispositions, and accepted `7.4b18f` lifecycle evidence. The live Bash checker
and the disposable suite both pass. The temporary suite and registry were
removed after proof.

The package intentionally refines the legacy boundary. The Bash checker
prohibited `<img` only in the migrated Media section; the declarative suite
prohibits `<img` across `ACCESSIBILITY-STANDARDS.md`. That file is a migrated
navigation surface and must not regain HTML media mechanisms in any section.
This conservative source-wide prohibition cannot authorize old behavior and
requires no section parser, copied heading range, exception, or compatibility
path.

The generated graph has exactly two outgoing executable edges from Media to
Accessibility Name/Input: one `executable_reference` and one
`verifier_dependency`. Both are admitted as `independent-gate` evidence.
Name/Input remains checker-backed, separately executed, and absent from Media's
registry dependencies. The two accepted Q2 rows that currently retain the
Media checker must transfer atomically to `suite:accessibility-media` and its
registered suite path when M6-R1 is accepted.

The checked `M6-R1` package manifest row is the sole exact file-level write-set
authority. Semantically, implementation may register the proved suite, delete
only the Media Bash checker, accept its package and incident edges, transfer
only the two Q2 historical evidence records, regenerate the four graph
artifacts, and update the listed planning records. Standards sources, fixtures,
dispositions, lifecycle claims, the Name/Input checker, README, engine,
schemas, numeric evidence, lockfiles, outputs, and workflows remain read-only.

**No-fallback rule:** register and pass the six-check suite before checker
deletion. Do not retain a wrapper or bridge, add a suite dependency on
Name/Input, copy Name/Input behavior, preserve checker evidence after deletion,
weaken the source-wide legacy prohibition, add a section parser or package-
specific assertion, infer a default, or create dual checker/suite authority.

**Acceptance gate:** focused suite; exact package projection and incident-edge
authority; two Q2 historical evidence transfers; retained independent
Name/Input gate; source-wide legacy-index purity; graph freshness; all
declarative suites; removed checker path; exact read-only source, fixture,
disposition, and lifecycle evidence; both plan checks; diff integrity; and the
complete mixed suite because accepted shared edge evidence changes.

**Admission verification:** the disposable six-check suite and live Bash
checker pass; current graph evidence proves exactly two owner-local incident
edges; the package projection and admitted edge rows are machine-readable.
No permanent suite, registry, checker, source, fixture, engine, schema,
lifecycle, numeric, lockfile, output, or workflow authority changed.

**Acceptance result:** the dependency-free six-check suite is registered and
passes; the Bash checker is absent; both Q2 historical rows now retain exact
`suite:accessibility-media` evidence; and both Name/Input rows remain accepted
checker-backed independent gates without a registry dependency. The authorized
source-wide legacy-index prohibition passes. Package projection, edge
authority, all declarative suites, generated graph freshness, plan checks,
read-only source evidence, diff integrity, and the complete mixed suite pass.
The fresh graph contains 156 Bash verifiers, 161 nodes, 771 edges, and 161
components. No later package is admitted.

##### VE055 Parent-Owned Row-Family Preflight

**Status:** `Active`; Option 4 selected for bounded family architecture and
representability proof.

The fresh post-M6-R1 graph contains 156 Bash verifiers, 161 nodes, 771 edges,
and 161 components. Rows 29 through 31 already demonstrate that historical
row-decomposition contracts can use existing generic table and text
assertions under `migration.parent-plan`. Rows 20 through 28 and 32 through 34
remain Bash-backed, but they are not one mechanically identical contract:
their child cardinality, owner projections, disposition evidence, accepted
claims, reports, and independent domain-gate sets differ.

The ownership boundary is frozen as follows:

- `migration.parent-plan` owns historical decomposition identity, expected
  owner projection, execution order, disposition lineage, and accepted
  migration-lifecycle evidence;
- canonical domain modules own current policy behavior and remain the only
  normative owners of that behavior;
- a domain verifier remains an independent package or wave gate unless the
  declarative row suite consumes its result as a true prerequisite;
- accepted historical checker evidence transfers directly to the registered
  row suite with `suite:<registered-id>` and does not create a suite
  dependency;
- counts, cardinalities, owner totals, and other mechanical values are derived
  from checked rows and projections. Configuration may state semantic
  identities and exact expected sets, but may not duplicate their lengths as
  count authority.

Before any family package is admitted, three disposable contained suites must
probe the structural range of the remaining rows:

| Probe | Structural role | Required proof |
| --- | --- | --- |
| row 24 | one owner and one child | exact decomposition, owner map, execution-train identity, disposition lineage, accepted claims, and separately executed full-review and train gates |
| row 25 | one child with complex planning/concurrency/recovery narration | exact decomposition and owner projection, required report semantics and accepted claims, plus separately executed planning, implementation-entrypoint, and train gates |
| row 34 | six children across Frontend, TypeScript, and Accessibility domains | exact per-child owner/lifecycle projection, report and accepted claims, plus all separately owned domain gates and the train gate |

Each probe uses the current generic assertion vocabulary and a disposable
contained registry. It may read the live row evidence and run the live Bash
checker for comparison, but it may not add a permanent suite, alter the shared
registry, edit the engine or schemas, change evidence, admit a package, or
delete a checker. Temporary probe files are removed after execution.

An engine capability is authorized for design only when at least two probes
expose the same invariant that cannot be represented exactly by current
generic checks. A row-specific assertion, copied Bash algorithm, arbitrary
command action, wrapper, compatibility schema, false dependency, or weakened
projection is invalid. If all probes are representable, the next planning
slice classifies rows 20 through 28 and 32 through 34 into owner-local packages
and bounded concurrent preparation waves with serial shared-authority
integration.

**Probe write set:** temporary contained suite and registry files outside the
repository plus these six serial planning records for results. Canonical
standards, evidence, fixtures, suites, registry, checkers, package/edge state,
generated graph, engine, schemas, lockfiles, outputs, and workflows remain
read-only.

**Re-plan triggers:** a repeated unrepresentable invariant in at least two
probes; evidence requiring a different canonical owner; a true domain-suite
dependency; conflicting historical evidence authority; or a required edit
outside the frozen probe write set. One exceptional row does not authorize a
family-wide engine abstraction.

##### VE055 Probe Result And Remaining-Row Classification

**Status:** Accepted; no engine capability added and no package admitted.

Disposable suites for rows 24, 25, and 34 pass 16 existing generic checks in
total. Their live Bash checkers also pass with every independent domain gate.
The probes derive cardinality from exact row and identifier projections and
require no copied counts, custom assertion, schema change, command action, or
weakened evidence. The initial row-24 probe used incorrect owner-map column
names and failed with typed TABLE.HEADER_CONTRACT; correcting the disposable
configuration to the exact live header passed without engine change.

The remaining rows are classified by evidence and edge shape:

| Class | Rows | Boundary |
| --- | --- | --- |
| Rust source lifecycle | 20-23 | rows 20-22 depend only on the execution-train gate; row 23 also retains Rust no-std closure independently |
| Process and template lifecycle | 24-27 | each retains execution-train plus its Planning, Implementation, or template-projection gate |
| Application-boundary lifecycle | 28, 32-34 | row 28 has an inbound Accessibility caller; rows 32 and 33 require accepted historical evidence transfer; row 34 retains six Frontend/TypeScript/Accessibility domain gates |

Rows 20 through 22 form the first bounded preparation wave:

| Package | Historical subject | Local result | Independent gate |
| --- | --- | --- | --- |
| M6-S1 | row 20 Rust API decomposition | dependency-free milestone-7-row-20-decomposition suite replaces its Bash checker | execution train |
| M6-S2 | row 21 Rust dependency decomposition | dependency-free milestone-7-row-21-decomposition suite replaces its Bash checker | execution train |
| M6-S3 | row 22 Rust release decomposition | dependency-free milestone-7-row-22-decomposition suite replaces its Bash checker | execution train |

All three packages are owned by migration.parent-plan; the Rust profiles in
their evidence remain canonical domain owners and are not transferred into the
suite owner. Local suite/checker paths are disjoint and may be prepared
concurrently after admission. Registry, package/edge authority, generated
graph, plans, and ledgers remain serial integration-owner files.

**Preflight result:** Accepted. Disposable suites pass 22 existing generic
checks, all three live checkers pass, and execution train passes independently.
No permanent probe artifact or engine capability was added.

**Admission gate:** each disposable suite must preserve exact decomposition
rows and identifier sets, owner validation, reports, execution-train owner,
accepted plan claims, dispositions or source-closure evidence, and any
repository-path existence checks from its Bash checker. Each live checker and
the execution-train gate must pass independently. A missing generic invariant,
new incident edge, stale source, conflicting owner, or required permanent edit
is a re-plan trigger.

##### VE057 Positive Path-State Capability Trigger

**Status:** Accepted through VE057 and VE058; M6-S preflight resumed.

Row 22 required content-neutral proof that the Rust release profile and recipe
paths exist. The former generic checks could not express that exact contract.
The accepted `path_state` contract now preserves this evidence without content
or relationship authority.

This is a recurring generic invariant, not a row-specific exception. Eleven
surviving Bash verifiers contain positive path-existence checks, including
Milestone 7 rows 13 through 15, 18, 22 through 23, and 40 through 44. The
Option 4 threshold is therefore met.

**Option 1 - Unified strict path-state assertion (Recommended):** replace
absent_paths with one path_state assertion containing explicit nonempty
present and/or absent path sets. Present paths use contained -e semantics: the
resolved target may be a file or directory, but must exist; a missing or broken
target is typed unavailable. Absent paths reject every filesystem entry,
including broken symlinks, as typed invalid. Reject unknown fields, empty
configurations, duplicate paths, overlap between states, absolute paths,
parent traversal, and symlink escape. Migrate the sole registered absent_paths
consumer atomically and delete the old parser, model, and tests so no legacy
assertion remains.

**Option 2 - Add a separate required-paths assertion:** preserve absent_paths
and add its positive counterpart. This is a smaller immediate diff but
duplicates containment, path-list validation, diagnostics, tests, and future
maintenance across two concepts.

**Option 3 - Infer existence through a content-bearing check:** use text,
exact_text, Markdown links, or reference inventory. This is invalid for row 22
because it silently strengthens existence into unrelated content or
relationship authority.

**Option 4 - Remove positive existence evidence:** omit the Bash checks because
other suites currently consume the files. This is invalid because incidental
consumers do not transfer row-22 ownership and may disappear independently.

The recommended shared-contract slice may edit only the path-state check
module, check dispatcher, focused tests, the sole registered absent-path suite,
engine documentation or architecture records that enumerate assertion kinds,
and these six serial planning records. It cannot edit row suites, registry,
row checkers, standards, evidence fixtures, package/edge state, generated
graph, lockfiles, outputs, or workflows.

**Acceptance gate:** positive file and directory; symlink to contained target;
missing and broken target; absent file, directory, symlink, and broken symlink;
duplicate, overlap, empty, unknown-field, absolute, traversal, and symlink-
escape cases; migrated existing absence consumer; all engine tests; all
declarative suites; removed absent_paths scan; both plan checks; diff
integrity; and complete mixed suite because the shared assertion contract
changes.

Any inability to preserve both states without compatibility parsing, any
second registered absence representation, or any required policy-specific
path behavior is a new re-plan trigger.

**Selected recovery:** Option 1. One strict `path_state` assertion replaces
`absent_paths` atomically. It accepts explicit `present` and/or `absent`
sets, requires at least one nonempty set, derives all cardinality, rejects
duplicates and cross-state overlap, and uses repository-contained filesystem
state without content interpretation. The retired `absent_paths` type becomes
unknown immediately; no alias, translation, fallback parser, or dual suite
representation is permitted.

The sole registered absence consumer changes to `path_state` in the same
implementation commit that deletes the old module and tests. Active engine
documentation and architecture references change to the new contract;
historical accepted plan records remain historical evidence and are not
rewritten as if the old contract never existed.

##### VE058 Shared Containment Helper Trigger

**Status:** Accepted with VE057 in canonical shared-contract implementation.

Focused VE057 implementation passes 26 file-contract tests, all 193 engine
tests, its migrated consumer, and all 121 declarative suites. Review found a
maintenance and security-ownership conflict before acceptance: current
`contained_file` combines repository containment with mandatory existing
regular-file validation, while `path_state` must resolve contained paths that
may be missing, directories, or broken symlinks. The proposal therefore
duplicates absolute/traversal/symlink-escape logic in a second module.

**Option 1 - Extract one shared contained-path resolver (Recommended):** add a
private or module-level `contained_path` helper in the existing paths module.
It validates nonempty repository-relative syntax and resolved containment,
accepting a declared existence requirement. Existing `contained_file` calls
that helper with existence required, then retains its regular-file check and
existing diagnostics. `path_state` calls the shared resolver without requiring
existence and applies only its present/absent semantics. Add focused helper
tests for missing, directory, valid symlink, broken symlink, traversal, and
escape behavior. This creates one containment owner and no compatibility path.

**Option 2 - Keep bounded duplication:** accept the current standalone
resolver inside `path_state`. This avoids modifying shared paths code but
creates two security-sensitive containment implementations that can drift.

**Option 3 - Broaden `contained_file` with optional type and existence flags:**
reuse the public helper by adding several modes. This minimizes functions but
makes a file-specific API conditional, weakens its name, and increases the
chance existing callers select a permissive mode.

**Option 4 - Resolve lexical paths only in `path_state`:** avoid shared helper
work and reject only absolute/traversal syntax. This is invalid because
symlinks could escape repository authority.

The recommended implementation may additionally edit
`tools/standards_verifier/standards_verifier/paths.py` and its focused tests.
It must preserve every existing `contained_file` outcome and caller, expose
no compatibility parser, and keep path-state configuration unchanged. The
complete mixed gate remains required at shared-contract acceptance.

**Selected recovery:** Option 1. Add one `contained_path` resolver in the
existing paths module as the sole repository-containment and symlink-escape
authority. It validates a nonempty repository-relative path and returns the
contained candidate without imposing file type. Existing `contained_file`
delegates to it, then preserves its current existence, regular-file, diagnostic,
and exit-code behavior. `path_state` delegates to the same resolver and owns
only present/absent state semantics.

The implementation must prove all existing `contained_file` callers remain
unchanged and add direct resolver coverage. It may not add mode flags to
`contained_file`, expose a permissive fallback, retain a private duplicate,
or change VE057 configuration.

Acceptance returned the validated lexical candidate after checking resolved
containment so broken symlinks remain observable to `path_state`. Focused,
engine, declarative, and all 156 mixed checkers pass.

##### M6-S1 Through M6-S3 Admission

**Status:** Admitted at train orders 85 through 87.

The accepted preflight uses seven generic checks for row 20, seven for row 21,
and eight for row 22. Exact table relations connect decomposition identities
to owner validation and canonical dispositions; no copied numeric count owns
cardinality. Row 22 uses `path_state` for its two canonical paths.

Each package owns `migration.parent-plan` historical evidence and one local
suite/checker replacement. Rust profiles remain canonical domain owners.
Every row checker has exactly two outgoing incident edges to execution train,
and all six are admitted as independent gates rather than suite dependencies.

Implementation proceeds serially as M6-S1, M6-S2, then M6-S3. Each accepting
slice registers and passes the dependency-free suite before deleting its Bash
checker, changes only that package and its two edge records to accepted,
regenerates the graph, proves source/evidence files unchanged, and updates the
six serial records. The mixed Bash checkpoint runs after M6-S3 as M6-S-W1.

**No-fallback rule:** no wrapper, Bash bridge, checker alias, copied
execution-train behavior, false registry dependency, compatibility parser,
or owner transfer is permitted. A changed incident edge, stale evidence,
unrepresentable contract, or required edit outside the admitted write set is a
re-plan trigger.

##### M6-T1 Row 24 Admission

**Status:** Accepted at train order 88.

The fresh pre-admission graph contains 153 Bash verifiers, 158 nodes, 765
edges, and 158 components. Row 24 is the smallest remaining caller-free parent-owned
package: three Planning index identities, one child, no historical checker
evidence, and no canonical standards movement. Its disposable probe already
passed seven existing generic checks after strict correction of a malformed
owner-map header.

M6-T1 will register one dependency-free suite preserving exact decomposition
identity, owner-validation and disposition lineage, report semantics, the
derived Planning entrypoint owner-map decision, execution-train owner, and
accepted plan claims. The full-review prompt entrypoint and execution train
remain independently owned gates. The exact graph exposes four incident
edges, one executable-reference and one verifier-dependency edge for each
gate; all four are admitted without registry dependencies.

Implementation must register and pass the suite before deleting the Bash
checker, accept only M6-T1 and its four edge records, regenerate the graph,
prove source and evidence files unchanged, and update the serial records. No
wrapper, Bash bridge, copied helper behavior, false dependency, owner transfer,
compatibility parser, hardcoded cardinality, or legacy authority is permitted.
A changed incident edge, stale evidence, unrepresentable contract, or required
edit outside the admitted write set is a re-plan trigger.

Admission regeneration adds four reference-only authority edges from the
package and edge manifests. The resulting graph has 153 Bash verifiers, 158
nodes, 769 edges, and 158 components; executable caller and gate topology is
unchanged.

Acceptance registers the dependency-free seven-check suite and deletes the
Bash checker. All four former gate edges are accepted as independent lifecycle
evidence. The regenerated graph contains 152 Bash verifiers, 157 nodes, 762
edges, and 157 components. The full-review prompt and execution train pass
independently, all 125 declarative suites and the complete mixed suite of 152
checkers pass, and no legacy execution path remains.

##### M6-T2 Row 27 Admission

**Status:** Accepted at train order 89.

The fresh post-M6-T1 graph contains 152 Bash verifiers, 157 nodes, 762 edges,
and 157 components. Among caller-free rows 23 and 25 through 27, row 27 is the
smallest complete package: one Implementation-owned child, eleven index
identities, no historical checker-evidence transfer, and two independent
gates. Row 23 retains twelve children and Rust no-std closure; row 25 has three
gates and complex recovery evidence; row 26 contains twenty-nine identities.

A disposable dependency-free suite passes six existing generic checks:
decomposition identity, identity relation, disposition lineage, report
semantics, execution-train identity, and accepted plan claims. The live row
checker, review-template projection, and execution train pass independently.
No engine capability, schema, copied cardinality, or permanent probe artifact
is needed.

M6-T2 has four exact incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. Implementation must register
and pass the suite before deleting the checker, accept only M6-T2 and those
four edges, regenerate the graph, prove source/evidence unchanged, and update
the serial records. Wrappers, Bash bridges, false dependencies, owner transfer,
compatibility parsing, and retained legacy authority are prohibited. Changed
edge identity, stale evidence, an unrepresentable contract, or an edit outside
the admitted write set is a re-plan trigger.

Admission regeneration adds four reference-only authority edges. The resulting
graph has 152 Bash verifiers, 157 nodes, 766 edges, and 157 components;
executable caller and independent-gate topology is unchanged.

Acceptance registers the dependency-free six-check suite and deletes the Bash
checker. All four former gate edges are accepted as independent lifecycle
evidence. The regenerated graph contains 151 Bash verifiers, 156 nodes, 759
edges, and 156 components. The review-template projection and execution train
pass independently, all 126 declarative suites and the complete mixed suite of
151 checkers pass, and no legacy execution path remains.

##### M6-T3 Row 25 Admission

**Status:** Accepted at train order 90.

The fresh post-M6-T2 graph contains 151 Bash verifiers, 156 nodes, 759 edges,
and 156 components. Caller-free rows 23, 25, and 26 remain. Row 25 is the
smallest complete package: one Implementation-owned child, seven index
identities, and three independently owned gates. Row 23 retains twelve
children plus Rust no-std source closure; row 26 retains twenty-nine identities
plus plan-template projection.

The accepted VE055 representability result was revalidated against current
evidence. A disposable dependency-free suite passes six generic checks: exact
decomposition projection, decomposition-to-owner identity,
owner-to-disposition lineage, planning/concurrency/recovery report semantics,
execution-train identity, and accepted plan claims. The live row checker,
planning admission, implementation entrypoint, and execution train pass
independently. Temporary files were removed. No engine capability, schema,
copied cardinality, owner transfer, or permanent probe artifact is needed.

M6-T3 has six exact incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. Implementation must register
and pass the dependency-free suite before deleting the checker, accept only
M6-T3 and those six edges, regenerate the graph, prove decomposition,
owner-validation, disposition, report, execution-train, workflow, prompt, and
fixture evidence unchanged, and update the serial records. Wrappers, Bash
bridges, false dependencies, compatibility parsing, inferred plan selection,
and retained legacy authority are prohibited. Changed edge identity, stale or
ambiguous lifecycle evidence, an unrepresentable semantic invariant, or a
required edit outside the admitted write set is a re-plan trigger.

Admission regeneration adds five unique reference-only contract edges. The six
typed incident edges already exist in executable topology, and execution train
is already a target of the shared edge manifest, so the derived graph has 151
Bash verifiers, 156 nodes, 764 edges, and 156 components. Executable caller and
independent-gate topology is unchanged.

Acceptance registers the dependency-free six-check suite and deletes the Bash
checker. All six former gate edges are accepted as independent lifecycle
evidence. The regenerated graph contains 150 Bash verifiers, 155 nodes, 755
edges, and 155 components. Planning admission, implementation entrypoint, and
execution train pass independently; all 127 declarative suites and the complete
mixed suite of 150 checkers pass. Protected decomposition, owner-validation,
disposition, report, execution-train, workflow, prompt, and fixture evidence is
byte-identical to admission, and no legacy execution path remains.

##### M6-T4 Row 26 Admission

**Status:** Accepted at train order 91.

The fresh post-M6-T3 graph contains 150 Bash verifiers, 155 nodes, 755 edges,
and 155 components. Row 26 is the smallest complete caller-free parent-owned
package: one Planning-owned child, twenty-nine index identities, no historical
checker-evidence transfer, and two independent gates. Row 23 retains twelve
children and Rust no-std source closure.

A disposable dependency-free suite passes six generic checks: exact
decomposition projection, decomposition-to-owner identity,
owner-to-disposition lineage, report and no-compatibility semantics,
execution-train identity, and accepted plan claims. Its first strict run
correctly rejected two inverted or line-crossing text expectations; correcting
the disposable configuration to the report's exact literals passed without
editing source evidence or weakening the assertion. The live row checker,
plan-template projection, and execution train pass independently. No engine
capability, schema, copied cardinality, owner transfer, or permanent probe
artifact is needed.

M6-T4 has four exact incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. Implementation must register
and pass the dependency-free suite before deleting the checker, accept only
M6-T4 and those four edges, regenerate the graph, prove decomposition,
owner-validation, disposition, report, execution-train, template, workflow,
and projection-fixture evidence unchanged, and update the serial records.
Wrappers, Bash bridges, false dependencies, compatibility parsing, fixed-count
authority, and retained legacy execution are prohibited. Changed edge identity,
stale evidence, an unrepresentable semantic invariant, or a required edit
outside the admitted write set is a re-plan trigger.

Admission regeneration derives four unique reference-only contract edges. The
four typed incident edges already exist in executable topology, and execution
train is already a shared manifest target, so the graph has 150 Bash verifiers,
155 nodes, 759 edges, and 155 components. Executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check suite before
deleting the Bash checker. Both former gates remain independent through four
accepted edge records. The regenerated graph contains 149 Bash verifiers, 154
nodes, 752 edges, and 154 components. The focused suite, package and edge
authority, plan-template projection, execution train, all 128 declarative
suites, complete mixed suite of 149 checkers, graph freshness, removed-path,
plan, and diff checks pass. Protected decomposition, owner-validation,
disposition, report, execution-train, template, workflow, and fixture evidence
is byte-identical to admission; no wrapper, fallback, or legacy execution path
remains.

##### M6-T5 Row 33 Admission

**Status:** Accepted at train order 92.

The fresh post-M6-T4 graph contains 149 Bash verifiers, 154 nodes, 752 edges,
and 154 components. Caller-free row 33 is the smallest complete remaining
parent-owned package: two Contracts-owned children, eight exact identities,
one HTTP-adapter gate, and execution train. Row 32 has thirteen identities and
two Persistence gates; row 23 spans twelve children plus Rust no-std source
closure; row 34 retains six Frontend-family gates.

A corrected disposable dependency-free suite passes six generic checks: exact
two-child decomposition, decomposition-to-owner identity,
owner-to-disposition lineage, report and typed no-fallback semantics,
execution-train identity, and accepted plan claims. Its first strict run
correctly rejected an overbroad right-side source filter; narrowing the probe
to the eight row-derived identities passed without editing source evidence or
weakening the relation. The live row checker, HTTP-adapter proof, and execution
train pass independently. No engine or schema change is needed.

M6-T5 has four exact outgoing incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. Two accepted M6-N1 rows
retain immutable row-33-to-Contract-HTTP edge lineage but currently use the
live row-33 checker as evidence. Implementation must first register and pass
the row-33 suite, then atomically change only those two evidence representations
to `suite:milestone-7-row-33-decomposition` and its exact registered TOML path.
This is the accepted VE046 independent-gate lifecycle; it adds no registry
dependency and does not change M6-N1 edge identity, owner, disposition,
rationale, or accepted state.

Implementation must accept only M6-T5 and its four edges, perform the exact
two-row M6-N1 evidence transfer, regenerate the graph, prove decomposition,
owner-validation, disposition, report, execution-train, plan, and adapter
evidence unchanged, and update the serial records. Wrappers, Bash bridges,
false `suite-requires` dependencies, compatibility parsing, copied counts,
owner transfer, mutated historical endpoints, and retained legacy execution
are prohibited. Changed incident identity, an evidence transfer beyond those
two rows, stale source evidence, an unrepresentable invariant, or a required
edit outside the admitted write set is a re-plan trigger.

Admission regeneration derives one unique reference-only contract edge for the
newly named HTTP-adapter gate, so the graph has 149 Bash verifiers, 154 nodes,
753 edges, and 154 components. Existing M6-N1 shared references already name
row 33; executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check row-33 suite
before deleting the Bash checker. Four M6-T5 edge records remain independent,
and the two accepted M6-N1 rows retain immutable historical endpoints while
their evidence representation transitions exactly to the registered row-33
suite under VE046. The regenerated graph contains 148 Bash verifiers, 153
nodes, 746 edges, and 153 components. The focused suite, package and edge
authority, HTTP-adapter proof, execution train, all 129 declarative suites,
complete mixed suite of 148 checkers, graph freshness, removed-path, plan, and
diff checks pass. Protected decomposition, owner-validation, disposition,
report, execution-train, adapter, fixture, Contracts, HTTP-reference, and
legacy-index evidence is byte-identical to admission; no wrapper, false
dependency, fallback, compatibility path, or legacy execution remains.
The focused suite, package and edge authority, Rust `no_std` closure and
execution-train gates, all 133 declarative suites, and the complete mixed suite
of 144 checkers pass. Graph freshness, removal, both plan, protected-hash, and
diff checks also pass. A fresh graph and ownership audit is next.

##### M6-T6 Row 32 Admission

**Status:** Admitted at train order 93.

The fresh post-M6-T5 graph contains 148 Bash verifiers, 153 nodes, 746 edges,
and 153 components. Caller-free row 32 is the smallest complete remaining
parent-owned package: three Persistence-owned children, thirteen exact
identities, durable-mutation and migration-execution gates, and execution-train
integrity. Row 23 spans twelve children plus Rust no-std source closure, while
row 34 retains six Frontend-family gates across multiple owners.

A disposable dependency-free suite passes six generic checks: exact
three-child decomposition, decomposition-to-owner identity,
owner-to-disposition lineage, report and typed no-fallback semantics,
execution-train identity, and accepted plan claims. The live row checker,
durable-mutation proof, migration-execution proof, and execution train pass
independently. The first probe invocation correctly rejected a suite file used
as a registry; a disposable one-entry registry then passed the unchanged suite
through the supported CLI. No engine, schema, or source-evidence change is
needed.

M6-T6 has six exact outgoing incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. Two accepted M6-N2 rows
retain immutable row-32-to-Persistence-owner edge lineage but currently use
the live row-32 checker as evidence. Implementation must first register and
pass the row-32 suite, then atomically change only those two evidence
representations to `suite:milestone-7-row-32-decomposition` and its exact
registered TOML path. This is the accepted VE046 independent-gate lifecycle;
it adds no registry dependency and does not change M6-N2 edge identity, owner,
disposition, rationale, or accepted state.

Implementation may change only the admitted 15-path write set. It must accept
only M6-T6 and its six edges, perform the exact two-row M6-N2 evidence transfer,
regenerate the graph, prove decomposition, owner-validation, disposition,
report, execution-train, plan, durable-mutation, and migration-execution
evidence unchanged, and update the serial records. Wrappers, Bash bridges,
false `suite-requires` dependencies, compatibility parsing, copied counts,
owner transfer, mutated historical endpoints, and retained legacy execution
are prohibited. Changed incident identity, an evidence transfer beyond those
two rows, stale source evidence, an unrepresentable invariant, or a required
edit outside the admitted write set is a re-plan trigger.

Admission regeneration derives exactly two reference-only contract edges from
the new package declaration. The graph contains 148 Bash verifiers, 153 nodes,
748 edges, and 153 components; executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check row-32 suite
before deleting the Bash checker. Six M6-T6 edge records remain independent,
and the two accepted M6-N2 rows retain immutable historical endpoints while
their evidence representation transitions exactly to the registered row-32
suite under VE046. The regenerated graph contains 147 Bash verifiers, 152
nodes, 739 edges, and 152 components. Protected decomposition,
owner-validation, disposition, report, execution-train, Persistence gates,
fixtures, profile, reference, and legacy-index evidence is byte-identical to
admission. No wrapper, false dependency, fallback, compatibility path, or
legacy execution remains. The focused suite, package and edge authority, all
three independent gates, all 130 declarative suites, complete mixed suite of
147 checkers, graph freshness, removed-path, plan, hash, and diff checks pass.

##### M6-T7 Row 38 Admission

**Status:** Admitted at train order 94.

The fresh post-M6-T6 graph contains 147 Bash verifiers, 152 nodes, 739 edges,
and 152 components. Auditing every caller-free lifecycle checker selects row
38 as the smallest complete package: one Documentation-owned identity, one
exact merge-duplicate disposition, directory-README closure, and execution
train. Rows 6 and 23 also have two gates but broader multi-identity and
multi-child contracts; rows 34, 36, 37, and 47 have larger gate sets.

A corrected disposable dependency-free suite passes six generic checks:
decomposition, exact owner validation, disposition lineage, report and typed
no-fallback semantics, execution-train identity, and accepted plan state. Its
first run rejected a required phrase split across a Markdown line boundary;
using the exact contiguous policy phrase passed without editing protected
evidence. The live checker and both independent gates pass. No engine or schema
change is needed.

M6-T7 has four exact outgoing incident edges, one executable-reference and one
verifier-dependency edge to each independent gate. There are no historical
caller-evidence rows to transfer. Implementation may change only the admitted
15-path write set; it must register and pass the replacement before deleting
the Bash checker, accept only M6-T7 and its four edges, regenerate the graph,
and prove row, disposition, Documentation gate, train, policy, and legacy-index
evidence unchanged. Legacy restoration, row-47 ownership, wrappers, Bash
bridges, false dependencies, compatibility parsing, copied counts, owner
transfer, and fallback are prohibited. Changed incident identity, new source
gaps, an unrepresentable invariant, or a required edit outside the write set is
a re-plan trigger.

Admission regeneration derives four reference-only package edges. The graph
contains 147 Bash verifiers, 152 nodes, 743 edges, and 152 components;
executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check row-38 suite
before deleting the Bash checker. Four M6-T7 edge records remain independent.
The regenerated graph contains 146 Bash verifiers, 151 nodes, 736 edges, and
151 components. Protected row, owner-validation, disposition, report,
accelerated-package, execution-train, Documentation closure, source-gap,
policy, and legacy-index evidence is byte-identical to admission. No legacy
restoration, row-47 ownership, wrapper, false dependency, fallback,
compatibility path, or legacy execution remains. The focused suite, package
and edge authority, both independent gates, all 131 declarative suites,
complete mixed suite of 146 checkers, graph freshness, removal, plan, hash, and
diff checks pass.

##### M6-T8 Row 6 Admission

**Status:** Admitted at train order 95.

The fresh post-M6-T7 graph contains 146 Bash verifiers, 151 nodes, 736 edges,
and 151 components. Row 6 and row 23 are caller-free with two independent gates;
row 6 is smaller at six identities across three owner-coherent children, while
row 23 spans twelve children plus source closure. Other caller-free rows retain
larger gate sets.

A disposable dependency-free suite passes six generic checks: exact ordered
decomposition, decomposition-to-disposition owner lineage, exact disposition
kinds, report and no-fallback semantics, execution-train identity, and accepted
plan state. It derives ownership directly from existing decomposition edges and
does not add a redundant owner-validation table. The live checker, accelerated
execution, and execution train pass independently; no engine or schema change
is needed.

M6-T8 has four exact outgoing incident edges to those two independent gates and
no historical caller-evidence rows. Implementation may change only the admitted
15 paths. It must register and pass the suite before deleting Bash, accept only
M6-T8 and its four edges, regenerate the graph, and prove decomposition,
dispositions, report, acceleration, train, findings, owner policies, fixtures,
and legacy source unchanged. Mandatory Strategy, guessed artifact identities,
fixed platform matrices, weaker evidence, wrappers, false dependencies,
compatibility parsing, copied counts, duplicate ownership, and fallback are
prohibited. Changed incidence, unrepresentable semantics, or an edit outside
the write set is a re-plan trigger.

Admission regeneration derives four reference-only package edges. The graph
contains 146 Bash verifiers, 151 nodes, 740 edges, and 151 components;
executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check row-6 suite
before deleting the Bash checker. Four M6-T8 edge records remain independent.
The regenerated graph contains 145 Bash verifiers, 150 nodes, 733 edges, and
150 components. Protected decomposition, dispositions, report, acceleration,
train, findings, owner policies, fixtures, and legacy source evidence is
byte-identical to admission. No duplicate owner authority, mandatory Strategy,
guessed artifact identity, fixed platform matrix, weaker evidence, wrapper,
false dependency, fallback, compatibility path, or legacy execution remains.
The focused suite, package and edge authority, accelerated-execution and
execution-train gates, all 132 declarative suites, and the complete mixed suite
of 145 checkers pass. Graph freshness, removal, both plan, protected-hash, and
diff checks also pass. A fresh graph and ownership audit is next.

##### M6-T9 Row 23 Admission

**Status:** Admitted at train order 96.

The fresh post-M6-T8 graph contains 145 Bash verifiers, 150 nodes, 733 edges,
and 150 components. Its remaining caller-free lifecycle packages are rows 23,
34, 36, 37, and 47, with respectively two, seven, five, nine, and four
independent gates. Row 23 therefore has the smallest gate surface. It covers
twelve ordered identities, while the other candidates retain broader domain
gate sets.

A disposable dependency-free suite passes six generic checks: exact ordered
decomposition, exact decomposition-to-owner identities, owner and disposition
lineage, report and no-fallback semantics, execution-train identity, and all
fourteen accepted plan claims. Its owner relation preserves the canonical
exceptions for `STD-0839` and `STD-0842`; it neither infers ownership from
prose nor adds another owner record. The live checker, Rust `no_std` closure,
and execution train pass independently. No engine or schema change is needed.

M6-T9 has four exact outgoing incident edges to those two independent gates and
no historical caller-evidence rows. Implementation may change only the admitted
15 paths. It must register and pass the suite before deleting Bash, accept only
M6-T9 and its four edges, regenerate the graph, and prove decomposition, owner
validation, dispositions, train, package, gate, findings, Rust Tooling, Rust
Cross-Platform, Verification, legacy-source, and corpus evidence unchanged.
Generic claim ownership, commands, products, workspace assumptions, test or
lint defaults, target or feature defaults, wrappers, false dependencies,
compatibility parsing, copied counts, duplicate ownership, and fallback remain
prohibited. Changed incidence, unrepresentable semantics, protected evidence
mutation, or an edit outside the write set is a re-plan trigger.

Admission regeneration derives four reference-only package edges. The graph
contains 145 Bash verifiers, 150 nodes, 737 edges, and 150 components;
executable topology is unchanged.

Acceptance registers and passes the dependency-free six-check row-23 suite
before deleting the Bash checker. Four M6-T9 edge records remain independent.
The regenerated graph contains 144 Bash verifiers, 149 nodes, 730 edges, and
149 components. Protected decomposition, owner validation, dispositions,
train, package, gate, findings, Rust Tooling, Rust Cross-Platform,
Verification, legacy-source, and corpus evidence is byte-identical to
admission. No generic policy transfer, command or product default, workspace,
test, lint, target, or feature default, duplicate ownership, wrapper, false
dependency, fallback, compatibility path, or legacy execution remains.

##### M6-T10 Row 47 Admission

**Status:** Admitted at train order 97.

The fresh post-M6-T9 graph contains 144 Bash verifiers, 149 nodes, 730 edges,
and 149 components. Rows 47, 36, 34, and 37 are the remaining caller-free
lifecycle packages with four, five, seven, and nine independent gates. Row 47
therefore has the smallest gate surface.

A disposable dependency-free suite passes eleven generic checks covering exact
train and package identity, owner-table validity, inventory-derived identity
completeness, owner-map and disposition lineage, decomposition report, corpus
classification, workflow and derived-template state, and accepted plan claims.
Identity completeness is derived by set equality with the generated section
inventory. Outcome labels must be nonempty, but neither the eighteen identities
nor eleven outcome labels are represented as copied counts. The live checker
and all four gates pass independently; no engine or schema change is needed.

M6-T10 has eight exact incident-edge rows for four independently retained
gates and no historical caller-evidence rows. Implementation is limited to the
admitted 15 paths. It must pass the permanent suite before deleting Bash,
accept only M6-T10 and its edges, regenerate the graph, and prove train,
package, owner-validation, dispositions, section inventory, owner map, corpus,
template, Documentation workflow, all four gates, and findings unchanged.
Universal README applicability, fixed headings, invented facts, placeholder
defaults, copied cardinalities, wrappers, false dependencies, duplicate
authority, compatibility parsing, and fallback are prohibited. Changed
incidence, unrepresentable semantics, protected evidence mutation, or an edit
outside the write set is a re-plan trigger.

Admission regeneration records 144 Bash verifiers, 149 nodes, 736 edges, and
149 components. Eight typed disposition rows produce six net graph edges after
set-valued deduplication; executable topology is unchanged.

Acceptance registers and passes the dependency-free eleven-check row-47 suite
before deleting the Bash checker. Eight M6-T10 edge records remain independent.
The regenerated graph contains 143 Bash verifiers, 148 nodes, 725 edges, and
148 components. Protected train, package, owner-validation, dispositions,
section inventory, owner map, corpus, template, Documentation workflow, gate,
and findings evidence is byte-identical to admission. No copied cardinality,
universal README applicability, fixed heading list, invented fact, placeholder
default, wrapper, false dependency, duplicate authority, compatibility path,
fallback, or legacy execution remains.
The focused suite, package and edge authority, all four independent gates, all
134 declarative suites, and the complete mixed suite of 143 checkers pass.
Graph freshness, removal, both plan, protected-hash, and diff checks also pass.
A fresh graph and ownership audit is next.

##### M6-T11 Row 36 Admission

**Status:** Admitted at train order 98.

The fresh post-M6-T10 graph contains 143 Bash verifiers, 148 nodes, 725 edges,
and 148 components. Row 36 is caller-free and has five independently retained
gates: Architecture Pattern Reference, Layered Pattern, Monorepo Pattern, Data
Authority, and execution-train integrity. No historical caller-evidence
transfer applies.

After M6-E1 introduced the native `inclusion` assertion, a disposable
dependency-free suite passes eight checks. It proves the four exact row-36
decomposition records, derives identity equality with owner validation,
validates nonempty unique owner records, and proves every row-36 owner record is
contained in the source-wide canonical disposition table. The inclusion uses
projected records and a source filter only; it copies neither the nineteen
identifiers nor their count. Report semantics, immutable train identity,
package state, and six accepted plan claims also pass. The live checker and all
five gates pass independently.

M6-T11 has ten exact incident-edge rows for those five gates. Implementation is
limited to the admitted write set. It must register and pass the permanent
suite before deleting Bash, accept only M6-T11 and its edge rows, regenerate
the graph, and prove all decomposition, owner, disposition, report, train,
package, gate, and plan evidence. A wrapper, Bash callback, inferred member
list, copied cardinality, equality fallback, alias, compatibility path, false
dependency, or protected-source mutation is prohibited. Changed incidence,
unrepresentable semantics, protected evidence mutation, or an edit outside the
write set is a re-plan trigger.

Admission regeneration records 143 Bash verifiers, 148 nodes, 732 edges, and
148 components. Ten typed disposition rows produce seven net graph edges after
set-valued deduplication; executable topology is unchanged.

Acceptance registers and passes the dependency-free eight-check row-36 suite
before deleting the Bash checker. Ten M6-T11 edge records remain independent.
The regenerated graph contains 142 Bash verifiers, 147 nodes, 719 edges, and
147 components. Protected decomposition, owner validation, dispositions,
report, train, package, Architecture gate, plan, and inclusion evidence remains
unchanged. No copied identity or cardinality, inferred member list, wrapper,
Bash callback, relation alias, equality fallback, false dependency,
compatibility path, duplicate authority, fallback, or legacy execution remains.
The focused suite, package and edge authority, all five independent gates, all
135 declarative suites, and the complete mixed suite of 142 checkers pass.
Graph freshness, removal, both plan, engine, and diff checks also pass. A fresh
graph and ownership audit is next.

##### M6-T12 Row 34 Admission

**Status:** Admitted at train order 99.

The fresh post-M6-T11 graph contains 142 Bash verifiers, 147 nodes, 719 edges,
and 147 components. Rows 34 and 37 are caller-free lifecycle candidates with
seven and nine independent gates, so row 34 is the smallest remaining surface.
It has no historical caller-evidence transfer and requires no engine change.

A disposable dependency-free suite passes eight generic checks. It validates
the six exact owner-aligned decomposition records, derives complete identity
equality with owner validation, validates owner and disposition domains, and
proves exact disposition lineage against the complete Frontend legacy-source
set. Report, immutable train, P28 package, and seven accepted plan claims also
pass. Neither the sixteen identities nor their cardinality is copied into a
filter. The live checker and Frontend Applicability, Lifecycle Work, Rendering
Synchronization, Source Closure, Testing Lineage, TypeScript Tooling, and
execution-train gates pass independently.

M6-T12 has fourteen exact incident-edge rows for those seven gates. The
acceptance write set is frozen in the package manifest. Implementation must
register and pass the permanent suite before deleting Bash, accept only M6-T12
and its edges, regenerate the graph, and preserve all decomposition, owner,
disposition, report, train, package, gate, and plan evidence. Copied identities
or counts, wrappers, Bash callbacks, inferred filters, false dependencies,
compatibility paths, duplicate authority, and fallback are prohibited. Changed
incidence, unrepresentable semantics, protected evidence mutation, or an edit
outside the write set is a re-plan trigger.

Admission regeneration records 142 Bash verifiers, 147 nodes, 728 edges, and
147 components. Fourteen typed disposition rows produce nine net graph edges
after set-valued deduplication; executable topology is unchanged.

Acceptance registers and passes the dependency-free eight-check row-34 suite
before deleting the Bash checker. Fourteen M6-T12 edge records remain
independent. The regenerated graph contains 141 Bash verifiers, 146 nodes, 711
edges, and 146 components. Protected decomposition, owner validation,
dispositions, report, train, P28 package, Frontend gate, and plan evidence is
unchanged. No copied identity or cardinality, inferred filter, wrapper, Bash
callback, false dependency, compatibility path, duplicate authority, fallback,
or legacy execution remains. The focused suite, package and edge authority, all
seven independent gates, all 136 declarative suites, and the complete mixed
suite of 141 checkers pass. Graph freshness, removal, both plan, and diff checks
also pass. A fresh graph and ownership audit is next.

##### M6-T13 Row 37 Admission

**Status:** Admitted at train order 100.

The fresh post-M6-T12 graph contains 141 Bash verifiers, 146 nodes, 711 edges,
and 146 components. Row 37 is the last caller-free lifecycle candidate. Its
nine incident gates are independently owned, and migration requires neither an
engine change nor historical evidence transfer.

A disposable dependency-free suite passes eight native checks. It validates
the four exact decomposition-child semantics, derives identity lineage from
the existing decomposition table, validates owner domains, and proves those
records are included in the source-wide Architecture dispositions. It also
validates report text, immutable train row 37, exact P30 membership consisting
of rows 36 and 37, and the accepted plan claims. The immutable train correctly
retains row 37's historical `missing` owner state; current owner existence is
derived independently by the execution-train gate from row 36's sole
`missing-to-exists` transition. The probe does not reinterpret or overwrite
either fact. The live checker and all nine independent gates pass.

M6-T13 has eighteen exact incident-edge rows for Architecture composition-root,
directory-template, durable-workflow, owner-contract, pattern-reference,
Frontend owner-contract, Frontend view-model, Resilience owner-contract, and
execution-train gates. Admission regeneration records 141 Bash verifiers, 146
nodes, 720 edges, and 146 components; executable topology is unchanged.

The acceptance write set is frozen in the package manifest. Implementation
must register and pass the permanent suite before deleting Bash, accept only
M6-T13 and its edge rows, regenerate the graph, and preserve decomposition,
owner, disposition, report, train, P30 package, gate, and plan evidence. Copied
identities or counts, historical-state reinterpretation, inferred filters,
wrappers, Bash callbacks, false dependencies, compatibility paths, duplicate
authority, and fallback are prohibited. Changed incidence, unrepresentable
semantics, protected evidence mutation, or an edit outside the write set is a
re-plan trigger.

Acceptance registers and passes the dependency-free eight-check row-37 suite
before deleting the Bash checker. Eighteen M6-T13 edge records remain accepted
independent-gate evidence. The regenerated graph contains 140 Bash verifiers,
145 nodes, 699 edges, and 145 components. Protected decomposition, owner,
disposition, report, immutable train, P30 package, gate, and plan evidence is
unchanged. Historical owner state remains distinct from current existence
evidence. No copied identity or cardinality, historical-state reinterpretation,
inferred filter, wrapper, Bash callback, false dependency, compatibility path,
duplicate authority, fallback, or legacy execution remains. The focused suite,
package and edge authority, all nine independent gates, all 137 declarative
suites, and the complete mixed suite of 140 checkers pass. Graph freshness,
removal, both plan, and diff checks also pass. A fresh graph and ownership audit
is next.

##### M6-I1 Python Complete-Checkpoint Transition

**Status:** Accepted at train order 101.

The fresh post-M6-T13 graph contains 140 Bash verifiers, 145 nodes, 699 edges,
and 145 acyclic components. Fourteen verifiers have neither executable callers
nor verifier dependencies. Two are infrastructure or recovery authorities:
`verify-declarative-suites.sh` is a temporary Python launcher, while
`verify-milestone-7-security-checker-repair-replan.sh` validates semantic
migration evidence. They are not one owner-coherent package.

Inspection also finds that deleting only `verify-declarative-suites.sh` would
leave `run-complete-suite.sh` as the canonical Bash orchestrator. M6-I1
therefore replaces both shell entrypoints atomically with one explicit
`python3 tools/standards_verifier/verify.py --complete` interface. Complete mode
checks generated graph freshness, runs every registered declarative suite once
in dependency order, and then fail-fast executes every retained canonical Bash
verifier in deterministic inventory order. It accepts no checker path or
command from configuration, uses no shell evaluation, and naturally becomes a
Python-only checkpoint when the retained Bash inventory reaches zero.

The CLI must return typed invalid or unavailable diagnostics for conflicting
selection/format options, stale generated evidence, an unavailable retained
checker, or a nonzero retained-checker result. A declarative failure prevents
retained-checker execution. Focused tests must prove deterministic order,
fail-fast behavior, empty retained inventory, unavailable and failed checker
diagnostics, and option conflicts. Existing `--all`, `--suite`, `--list`, and
text/JSON declarative behavior remains unchanged.

M6-I1 is an explicit edge-free refinement package. Admission regeneration
records 140 Bash verifiers, 145 nodes, 701 edges, and 145 components; the two
new edges are package-contract references and executable topology is unchanged.
Acceptance must delete both shell entrypoints in the same commit that makes the
Python command canonical. No wrapper, shell callback, arbitrary command action,
configuration executable, compatibility alias, skipped freshness gate, ignored
checker failure, or fallback entrypoint may remain.

The checked package manifest is the sole exact file-level write-set authority.
Acceptance requires focused checkpoint tests, all engine tests, graph
freshness, all declarative suites, both removed paths, both plan checks, exact
read-only standards/suite/fixture/registry evidence, diff integrity, and one
successful `--complete` invocation over the retained inventory. A required
registry/schema change, policy-bearing engine branch, executable path from
configuration, inability to preserve fail-fast output, or edit outside the
manifest is a re-plan trigger.

Acceptance implements the admitted three-phase command without changing the
suite registry or schema. Generated evidence is checked before suite loading;
all declarative suites then execute once through the existing dependency graph;
only after those phases pass does the command derive and fail-fast execute the
retained Bash inventory. Eight focused checkpoint tests and all 214 engine
tests pass. Both Bash orchestration entrypoints are deleted with no wrapper,
alias, configuration command, skipped failure, or fallback. Regeneration
records 139 retained Bash verifiers, 144 nodes, 699 edges, and 144 acyclic
components. The focused package and edge-free suites, all 137 declarative
suites, the Python complete checkpoint over all 139 retained Bash verifiers,
graph freshness, both plan checks, removed-path checks, exact read-only
evidence, and diff integrity pass.

##### M6-I2 Security Repair Evidence Separation

**Status:** Planned after the semantic wave; not admitted.

The 71-line security-repair checker is not launcher infrastructure. It owns the
exact four-package repair inventory, serial/parallel preparation split,
preserved-evidence contract, selected-design report, and accepted parent-plan
claims. It requires a separately admitted `migration.parent-plan` declarative
suite after a disposable representability probe. M6-I1 may not delete, wrap,
invoke specially, reinterpret, or absorb this evidence.

##### M6-U0 Concurrent Semantic Preparation Wave

**Status:** Planned; package preflight follows M6-I1 acceptance.

Twelve caller-free, dependency-free semantic gates remain suitable for
owner-separated preflight. They form candidate preparation lanes, not one
cross-owner package:

| Lane | Candidate gates | Semantic owner boundary |
| --- | --- | --- |
| Contracts | HTTP adapter proof | Contracts policy and HTTP recipe evidence |
| Frontend | Applicability; lifecycle work; TypeScript tooling | Frontend profile, generic lifecycle owner, and TypeScript/Tooling specializations remain distinct within separately admitted packages |
| Persistence | Durable mutation; migration execution | Persistence boundary profile with two separate observable contracts |
| Planning and prompts | Planning admission; plan implementation entrypoint; full-review prompt | Planning workflow and versioned prompt projections remain separately owned |
| Templates | Plan template; review template | Planning and Implementation template projections remain separate packages |
| Rust | `no_std` closure | Rust Cross-Platform capability with Tooling and recipe evidence |

For every candidate, disposable native-suite preflight must derive exact
decisions, text/projection evidence, dispositions, and historical
independent-gate transfers. Preflight freezes one package owner, suite ID,
local write set, semantic outcome, prerequisites, and focused verification
contract. No package is admitted merely because graph incidence is zero.

After admission, package-local suites and checker deletions may be prepared
concurrently in isolated worktrees. Each worker owns only its suite path and
deleted checker path, starts from the same frozen canonical revision, changes
no shared authority, and reports a commit plus focused evidence. The suite
registry, package and edge manifests, historical evidence transfers, generated
graph, plans, ledgers, READMEs, and wave checkpoint remain serial integration-
owner files. Integration applies prepared local commits in admitted train
order, updates shared authority once per contiguous group, runs focused checks
after each package, and runs `--complete` once at the wave boundary.

A repeated unrepresentable invariant, overlapping local write sets, conflicting
owner, true cross-suite dependency, shared fixture mutation, stale historical
evidence, or required normative-source change is a re-plan trigger. Combining
owners for throughput, parallel shared-manifest edits, a Bash bridge, false
suite dependency, compatibility route, or fallback is prohibited.

##### M6-Q0 Concurrent Preparation And Serial Integration Freeze

**Status:** `Accepted`

All four Q packages are individually admitted and their local write sets are
disjoint. The admitted package manifest remains the source for package owner,
semantic outcome, prerequisites, verification contract, suite path, and
deleted checker path. This freeze does not copy those values into another
machine-readable authority.

Each proposal starts from the canonical revision containing this accepted
freeze and may change only its package-local suite path and delete its admitted
checker path:

| Proposal | Package-local write set |
| --- | --- |
| `M6-Q1` | `evaluation/standards-effectiveness/suites/rust-tooling-criterion.toml`; delete `evaluation/standards-effectiveness/verify-rust-tooling-criterion.sh` |
| `M6-Q2` | `evaluation/standards-effectiveness/suites/accessibility-evidence-closure.toml`; delete `evaluation/standards-effectiveness/verify-accessibility-evidence-closure.sh` |
| `M6-Q3` | `evaluation/standards-effectiveness/suites/architecture-population.toml`; delete `evaluation/standards-effectiveness/verify-architecture-population.sh` |
| `M6-Q4` | `evaluation/standards-effectiveness/suites/coding-dependency-route.toml`; delete `evaluation/standards-effectiveness/verify-coding-dependency-route.sh` |

Local preparation may run concurrently in isolated worktrees. A local commit
is a proposal only: it cannot edit the registry, package or edge manifests,
package projection, README, generated graph, active plans, ledgers, reports,
fixtures, canonical standards, lifecycle records, engine, schemas, numeric
evidence, lockfiles, build output, or workflows. It cannot claim package
acceptance. Each proposal must prove its suite through a disposable contained
registry, preserve the admitted read-only source/fixture contract, and return
its commit identity, exact diff, and focused result to the integration owner.

The integration owner applies proposals serially in Q1, Q2, Q3, then Q4 order.
Immediately before each integration it compares the current plan admission and
proposal base, rebases or reconstructs the proposal from fresh state when
stale, and confirms that no package-local or shared-authority write overlaps.
The accepting commit registers and passes the suite before deleting the Bash
checker, changes that package and its exact edge dispositions to accepted,
reconciles any admitted historical checker evidence to the registered suite,
updates shared plans/ledgers/reports, regenerates the graph, and proves the
removed path. Focused package, authority, retained independent-gate, all-
declarative, graph-freshness, plan, read-only-source, and diff checks run for
each integration. The mixed Bash checkpoint runs once after Q4 at `M6-Q-W1`.

**No-fallback rule:** prepared or integrated work cannot retain a wrapper,
Bash bridge, checker alias, dual suite/checker authority, copied callee
semantics, inferred dependency, package-specific engine branch, or compatibility
representation. A stale base, changed semantic source, changed fixture,
additional incident edge, failed local suite, overlapping write set, required
shared capability, or inability to register before deletion is a re-plan
trigger rather than authority to merge, retry automatically, or fall back.

**Acceptance evidence:** Q1 through Q4 are admitted; their suite and checker
paths are pairwise disjoint; shared authority is explicitly serial; proposal
and integration verification are separated; integration order and the wave
checkpoint are fixed; both plan structure checks pass; and no source, fixture,
suite, registry, checker, engine, schema, generated artifact, lockfile, build
output, or workflow changes in this planning slice.

##### VE050 Level-Selected Markdown Heading Policy Re-plan

**Status:** `Accepted`; Option 1 is implemented and Q2 preflight may resume.

Q2 preflight proves that its decision table, canonical and reference text,
exact dispositions, and accepted lifecycle claims fit existing generic
assertions. The remaining Bash rule selects every level-two heading in
`ACCESSIBILITY-STANDARDS.md` and rejects any selected heading that does not
contain `Migrated`. The engine has exact-heading plus mandatory-line-limit
`markdown_structure`, whole-file `exact_text`, and unstructured literal `text`,
but no assertion for a property over a structurally selected heading set.

**Option 1 - Generic level-selected heading policy (`Recommended`):** add a
separate `markdown_headings` assertion that parses ATX headings, selects one
declared level, requires at least one selected heading, and applies configured
literal requirements or prohibitions to every selected heading. It returns
typed configuration/input/assertion diagnostics and has focused positive and
negative tests. This preserves Q2 exactly without regex, heading inventories,
line limits, whole-file snapshots, callbacks, or package-specific code and is
reusable for other derived indexes.

**Option 2 - Exact `markdown_structure` inventory:** list the four current
headings and add a positive maximum-line value. This passes current content but
freezes heading membership and introduces unrelated count authority. Future
valid migrated sections or prose growth would require suite churn, so this is
not recommended.

**Option 3 - Whole-file `exact_text`:** freeze the current short index bytes.
This is deterministic but turns every prose, wrapping, or route edit into Q2
authority and duplicates content rather than describing the closure invariant.
It is not recommended.

**Option 4 - Defer Q2 and retain Bash:** continue Q3/Q4 while leaving Q2
unadmitted. This preserves current behavior but violates the selected Q-wave
ordering and leaves the generic capability gap unresolved; it is appropriate
only if heading-policy ownership is explicitly deferred to a later engine wave.

**No-fallback boundary at capability acceptance:** Q2 was not yet admitted. Do
not encode a magic line
limit, copy the current heading list, freeze the complete file, weaken the rule
to known prohibited headings, invoke Bash from Python, keep a compatibility
wrapper, or create an Accessibility-specific assertion. Engine/shared-contract
work requires its own capability slice and mixed checkpoint before Q2 resumes.

**Accepted implementation:** the generic `markdown_headings` check selects ATX
headings outside fenced code blocks at one explicit level, rejects an empty
selection, and applies every configured required and prohibited literal to
every selected heading. Configuration is strict; paths are contained; missing
or invalid UTF-8 input and per-line assertion failures are typed. It exposes no
regular-expression configuration, count, copied inventory, callback, command,
normalizer, inferred level, compatibility representation, or Bash fallback.

**Acceptance evidence:** 24 focused file-contract tests, all 191 engine tests,
Python byte-compilation, an isolated real-corpus Q2 proof against
`ACCESSIBILITY-STANDARDS.md`, the live Accessibility evidence-closure checker,
and the complete mixed Bash checkpoint passed. Q2's suite, registry entry,
package, edge rows, checker, fixture, standards sources, and generated graph
remain unchanged for the next isolated admission slice.

##### VE046 Independent-Gate Evidence Lifecycle Re-plan

**Status:** `Accepted`; Option 1 is implemented and M6-P3 may resume from its
clean admission boundary.

The focused root-index suite and transferred root audit both passed during the
aborted implementation, but exact edge authority returned
`INPUT.UNAVAILABLE`. Two accepted M6-P2 historical `independent-gate` rows name
`verify-root-index-closure.sh` as their retained checker evidence. M6-P3 must
delete that checker, yet the current edge contract accepts only
`checker:<path>` evidence for an independent gate. It cannot name the canonical
replacement suite without falsely declaring `suite-requires`.

**Option 1 - Tagged independent-gate evidence (`Recommended`):** retain the
single semantic disposition `independent-gate`, but permit exactly two explicit
replacement variants: `checker:<contained-path>` for a live Bash gate and
`suite:<registered-id>` for a migrated declarative gate. Validate checker
evidence exactly as today; validate suite identity and registered suite path
without requiring or synthesizing a registry dependency. Add focused accepted-
history transition, missing suite, malformed tag, and false-dependency
regressions. This models the same independent gate across representations with
no compatibility bridge or inferred default.

**Option 2 - New `independent-suite` disposition:** add a separate disposition
with `suite:<registered-id>` evidence. This is explicit, but duplicates the
independent-gate concept and forces disposition churn whenever a gate changes
implementation. Choose it only if checker-backed and suite-backed independent
gates later acquire different scheduling semantics; current evidence shows no
such distinction.

**Option 3 - Convert the M6-P2 rows to `suite-requires`:** register a dependency
from the row-35 lifecycle suite to root-index closure. This would satisfy the
current schema but invent runtime ordering and semantic dependence that exact
review rejected. It is a no-fallback violation and is not recommended.

**Option 4 - Point historical evidence at M6-P3 or waive evidence existence:**
record only package lineage or allow the deleted checker path to remain as
nominal evidence. Neither proves the current independent gate is registered
and executable; both weaken acceptance and are rejected.

**Accepted decision and implementation:** Option 1 retains one semantic
`independent-gate` disposition with two explicit representation tags. A live
gate uses `checker:<contained-path>`. A migrated gate uses
`suite:<registered-id>`, whose evidence must equal the suite's exact registered
path. The suite form neither requires nor synthesizes a registry dependency;
`suite-requires` remains reserved for an actual registered `requires` edge.
The validator does not infer representation, ownership, or dependency from
graph shape, syntax, or registry topology.

Focused coverage proves an accepted historical gate can transition to a suite
with an empty dependency list and rejects unknown suite IDs, mismatched
evidence paths, and dependency-expression syntax. Existing checker-backed and
`suite-requires` behavior remains strict. Verification passes 31 focused edge
tests, all 183 engine tests, Python compilation, all 109 declarative suites,
fresh graph evidence at 168 Bash verifiers / 173 nodes / 852 edges / 169
components, and the complete mixed checkpoint. No M6-P2 row or M6-P3
implementation file changed in the capability slice. M6-P3 acceptance may now
atomically convert the two affected M6-P2 historical rows to explicit suite
evidence while accepting its own five rows.

**Tasks:**

- [x] Generate exact dependency closures before package admission; a package
  must include or already have declarative versions of every semantic
  prerequisite and every Bash caller that would otherwise reference a deleted
  verifier.
- [x] Admit non-overlapping owner-coherent packages per accelerated wave only
  where their owner, dependency set, semantic decision, fixture family, and
  verification contract are frozen; bound size by semantic review and
  write-set overlap rather than an arbitrary package count.
- [x] Permit concurrent package preparation only in isolated worktrees with
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
