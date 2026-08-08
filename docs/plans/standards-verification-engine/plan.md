# Plan: Generic Standards Verification Engine

**Plan status:** `Active`

**Current phase:** Milestone 2: Shared Structural Assertion Foundation

**Next slice:** Implement `M2-S1`: strict table assertions with Dependency audit
lineage as the first complete consumer.

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
| Keep the parent standards restructure plan authoritative for normative migration and this child plan authoritative for checker-engine architecture and migration. | Integration owner | Parent-plan delegation | `7.4c3hcp` bespoke Cross-Platform repair assumption |

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
- [ ] Classify every checker by assertion family, inbound dependency, owner,
  risk, and migration disposition.
- [ ] Add strict table, Markdown heading/route, exact-row/set/order, and count
  assertions from observed requirements.
- [ ] Migrate coherent leaf packages and remove their scripts.

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
| `M2-S1` Dependency audit lineage | `topics.dependencies` | decision, canonical text, exact disposition projection, accepted plan marker | Implement with the first strict table consumer. |
| `M2-P9` Implementation change evidence | `workflow.implementation` | decision, canonical/reference text, exact split disposition | Migrate with existing checks after `M2-S1`. |
| `M3-C1` Acceptance claims | `workflow.verification` | canonical claim grammar and required-to-observed set satisfaction | Implement as one typed shared contract, then update its README invocation. |
| `M3-S1` F018 decomposition | parent migration plan | strict map, exact IDs/order, inventory/disposition relations, accepted lifecycle state | Implement after relation checks; remove obsolete planned-state branches. |
| `M3-S2` Row 19 decomposition and owner validation | parent migration plan | strict tables, exact/expanded projections, uniqueness, counts, canonical report and accepted plan state | Migrate as one owner-coherent two-script package. |
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

### Milestone 3: Shared Metadata, Plan, And Migration Contracts

**Goal:** Replace shared Bash parsers for metadata graphs, plan lifecycle,
dispositions, ownership, and source-index closure with typed engine checks.

**Allowed write set:** affected engine modules/tests, declarative suites and
fixtures, replaced shared helpers/checkers, migration inventory, and plan
records selected per slice.

**Tasks:**

- [ ] Implement metadata uniqueness/dependency/cycle and canonical-owner checks.
- [ ] Implement plan lifecycle and acceptance-claim checks.
- [ ] Implement exact disposition/owner-map and source-index closure checks.
- [ ] Delete superseded generic Bash engines and their wrappers atomically.

**Acceptance gate:** Existing positive and negative fixture families pass via
the engine; old helpers and compatibility paths are absent; complete mixed
suite passes at every shared-contract slice.

**Status:** `Planned`

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

**Allowed write set:** registry/dependency contracts, affected Cross-Platform
suites, the four obsolete Cross-Platform scripts, source-closure fixtures and
source only after checker migration, parent migration records, and this plan.

**Tasks:**

- [ ] Convert transitive verifier calls into declared suite dependencies.
- [ ] Migrate platform-target, native-loading, release-artifact, and
  platform-evidence suites with source-wide route/prohibition assertions.
- [ ] Delete the four replaced scripts and close the Cross-Platform source in
  the parent plan's manifest order.

**Acceptance gate:** Each dependency executes once; all Cross-Platform
decisions/dispositions/routes/no-fallback cases pass; `F085` resolves; source
closure and complete mixed suite pass.

**Status:** `Planned`

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
