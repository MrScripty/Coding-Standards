# Plan: Generic Standards Verification Engine

**Plan status:** `Active`

**Current phase:** Milestone 5: Native Artifact Loading admission

**Next slice:** Audit and admit `M5-CP2` Native Artifact Release as the next
independent owner package.

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

**Status:** `Active`

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

**Status:** `Active`

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
  generated inference. It assigns admitted components to canonical owner,
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
- [ ] Convert transitive verifier calls into declared suite dependencies.
- [ ] Migrate platform-target, native-loading, release-artifact,
  platform-evidence, and Rust target-configuration suites while preserving
  owner-local semantics and whole-source route/prohibition coverage.
- [ ] Delete the five replaced scripts, close the Cross-Platform source in the
  parent plan's manifest order, and delete `M5-CP0` in the same closure wave.

**Acceptance gate:** Each dependency executes once; all five semantic suites'
decisions/dispositions/routes/no-fallback cases pass; no suite depends on
former-source headings; `F085` resolves; `M5-CP0` is absent after source
closure; and the complete mixed suite passes.

**Status:** `Active`

### Milestone 6: Exceptional Checks And Bash Retirement

**Goal:** Resolve the measured remainder without turning the engine into a
general-purpose programming language.

**Allowed write set:** bounded typed Python check modules/tests, suite
contracts, replaced scripts, inventory, launcher/complete-suite entrypoint,
documentation, and plan records.

**Tasks:**

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
