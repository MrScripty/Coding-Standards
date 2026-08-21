# Plan: Generic Standards Verification Engine

**Plan status:** `Active`

**Current phase:** Milestone 6 Bash retirement

**Next slice:** audit the fresh post-M6-I31 graph and select one owner-coherent
package without preselecting M6-I32

**Acceptance status:** `pending`

**Latest accepted slice:** M6-I31 replaced the row-40 decomposition checker
with one registered parent-plan suite.

**Latest admitted slice:** none

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

This file owns current verification-engine architecture, milestone state,
blockers, and the next authorized migration boundary. Accepted package history
belongs in the ledger, issues, reports, and canonical lifecycle manifests.

## Objective

Eliminate the Bash verification and helper surface in favor of one
maintainable declarative Python verification engine that runs repository-owned
suites once through a deterministic dependency graph, returns typed
diagnostics, and preserves exact ownership, disposition, no-fallback, and
evidence contracts.

## Objective Acceptance

| ID | Observable criterion | Status | Evidence |
| --- | --- | --- | --- |
| A1 | One documented command discovers and runs every registered suite once in dependency order. | `satisfied` | [Engine README](../../../tools/standards_verifier/README.md); current complete checkpoint |
| A2 | Strict configuration, containment, dependency, assertion, and typed-diagnostic tests pass. | `satisfied` | Engine self-tests and registered declarative suites |
| A3 | Required decision, text, table, metadata, migration, plan, route, and source-index contracts are represented without arbitrary command execution. | `partial` | Accepted assertion families and [architecture report](reports/architecture.md) |
| A4 | Each migrated suite removes its replaced Bash checker while preserving positive, negative, ownership, disposition, and no-fallback evidence. | `partial` | [Package manifest](../../../evaluation/standards-effectiveness/checker-migration-packages.tsv) and [edge dispositions](../../../evaluation/standards-effectiveness/executable-edge-dispositions.tsv) |
| A5 | Final inventory reports no Bash verifier, verification helper, or migration launcher. | `pending` | Current generated inventory still reports retained Bash checkers |
| A6 | The Python-only complete checkpoint passes and the temporary Bash reference model is absent. | `pending` | Milestones 6 and 7 |

## Scope

### In Scope

- A Python 3.11+ standard-library verification package and stable command.
- Strict TOML suite/registry contracts and TSV/Markdown evidence inputs.
- Deterministic dependency scheduling with each suite evaluated at most once.
- Typed text and JSON diagnostics with stable codes and source locations.
- Reusable bounded checks required by measured repository contracts.
- Incremental deletion of every Bash checker, verification helper, and
  temporary migration launcher.
- A frozen temporary inventory derived from remaining Bash scripts and deleted
  at zero-Bash closure.

### Out Of Scope

- Unrelated normative standards changes.
- A general-purpose expression language, arbitrary shell execution, `eval`,
  embedded configuration code, or compatibility parsing.
- Replacing downstream product verification with documentation checks.
- Third-party runtime dependencies or a second build toolchain.
- A permanent generalized standards graph, Bash AST, or ownership inferred
  from lexical topology.

## Constraints And Assumptions

- The engine owns mechanics; standards and fixtures own policy.
- Unknown keys, check kinds, operators, outcomes, paths, suite IDs, and
  dependencies are typed `invalid`, never ignored.
- Missing required files or capabilities are typed `unavailable`; unsupported
  capabilities are typed `unsupported`.
- Repository paths are normalized and contained; symlink resolution cannot
  escape the root.
- Suite dependencies are acyclic and execute once in stable order.
- Shared registry, engine contracts, package/edge manifests, generated
  artifacts, parent plan, and this plan integrate serially.
- A migrated checker and obsolete helper are deleted with their accepted
  replacement, not wrapped or retained as fallback.
- Custom algorithms must be typed, side-effect-free Python checks that are
  registered, directly tested, and owned.
- Current graph membership, references, counts, components, waves, and line
  totals are derived observations, not ownership or acceptance authority.
- The temporary graph schema remains frozen and is deleted wholesale at
  zero-Bash closure.

## Binding Decisions

| Decision | Binding direction | Evidence |
| --- | --- | --- |
| Runtime | Use Python 3.11+ standard library only. | [Architecture](reports/architecture.md#runtime-and-packaging) |
| Configuration | Use strict TOML composition with TSV/Markdown evidence. | [Architecture](reports/architecture.md#contract-model) |
| Ownership | Policy remains in standards and fixtures; engine checks expose bounded mechanics. | [Architecture](reports/architecture.md#ownership-boundary) |
| Security | Prohibit arbitrary commands, callbacks, embedded code, and compatibility schemas. | [Architecture](reports/architecture.md#security-and-no-fallback) |
| Migration | Migrate owner-coherent semantic packages and delete each replaced Bash path in the accepting slice. | [Package manifest](../../../evaluation/standards-effectiveness/checker-migration-packages.tsv) |
| Dependencies | Registered suite `requires` owns execution dependencies; lexical graph edges do not. | [Legacy reference boundary](reports/legacy-script-reference-model.md) |
| Temporary graph | Keep the current lexical reference model frozen as conservative deletion-lifecycle evidence and remove it at zero Bash. | [Legacy reference boundary](reports/legacy-script-reference-model.md) |
| Generated values | Derive mutable paths, counts, memberships, and relationships; store only explicit policy inputs and reviewed lifecycle authority. | [Count-authority report](reports/count-authority.md) |
| Numeric lifecycle | Whole-checker deletion derives candidate retirement from one accepted checker package; candidate mappings apply only when a numeric expression disappears while its checker remains live. | [Checker inventory](reports/checker-inventory.md) |
| Concurrency | Prepare admitted disjoint package-local work concurrently; integrate registry, manifests, graph, plans, and checkpoints serially. | [Checker inventory](reports/checker-inventory.md) |
| Parent boundary | The parent plan owns normative migration; this plan owns verification architecture and checker migration. | [Parent plan](../../../plans/standards-library-effectiveness-restructure-plan.md) |

## Current System

The canonical command is:

```bash
python3 tools/standards_verifier/verify.py --complete
```

Complete mode:

1. verifies generated migration evidence;
2. runs every registered declarative suite once in dependency order; and
3. fail-fast executes retained Bash checkers in deterministic inventory order.

At zero Bash, the same command becomes Python-only without an alternate mode or
fallback.

**Accepted boundary:** package records are accepted through M6-I31 at train
order 146.

**Current derived state:** 178 registered declarative suites, 94 retained Bash
checkers, 98 executable nodes, 616 conservative reference edges, and 98
components. These values are observations from generated evidence and do not
authorize package selection or ownership.

## Milestones

| Milestone | Outcome | Status | Current evidence or next work |
| --- | --- | --- | --- |
| 0 | Engine contract and migration authority | `Accepted` | [Architecture report](reports/architecture.md) |
| 1 | Executable kernel and first replaced checker | `Accepted` | [Engine README](../../../tools/standards_verifier/README.md) |
| 2 | Inventory and structural assertion families | `Accepted` | [Checker inventory](reports/checker-inventory.md) |
| 3 | Metadata, plan, migration, and shared evidence contracts | `Accepted` | Registered suites and engine tests |
| 4 | Standalone semantic-decision phase | `Superseded` | Decision migration proceeds through owner-coherent packages in Milestone 6 |
| 5 | Dependency graph and Cross-Platform closure | `Accepted` | Package and source-closure lifecycle records |
| 6 | Exceptional checks and Bash retirement | `Active` | Fresh graph review after accepted M6-I31 |
| 7 | Documentation and objective acceptance | `Planned` | Starts at zero-Bash closure |

### Milestone 6 Current State

**Goal:** replace or intentionally retire every remaining Bash verifier,
helper, and migration launcher without turning the engine into a general-purpose
programming language.

**Recovery dependency:** M6-I16 and the
[work proportionality and policy impact recovery](../work-proportionality-and-policy-impact/plan.md)
and the [generic edge-system recovery](../generic-edge-system/plan.md) are
accepted. The neutral graph capability and justified permanent consumers are
now upstream of the verifier. M6-I17 is accepted from fresh post-recovery
evidence. M6-I18 is accepted from fresh post-M6-I17 evidence; the frozen
temporary Bash graph schema remains unchanged.

**Next work:**

1. Audit the fresh post-M6-I31 graph and select one owner-coherent package from
   reviewed lifecycle and dependency evidence without preselecting M6-I32.
2. Select each subsequent owner-coherent package from reviewed lifecycle and
   dependency evidence.
3. Add another reusable primitive only when multiple coherent owners require it or
   one safety-critical invariant cannot otherwise be expressed clearly.
4. Prepare disjoint admitted suite/checker changes concurrently when their
   write sets and dependencies are frozen.
5. Integrate shared authority serially and run one complete checkpoint at each
   shared-contract or wave boundary.
6. Continue until no Bash verifier, helper, or launcher remains, then delete
   the temporary reference model.

**Acceptance gate:** exact inventory reports zero Bash verification paths; the
Python-only complete checkpoint passes; no wrapper, transitive Bash execution,
arbitrary command action, dual authority, compatibility representation, or
fallback remains.

## Evidence Index

| Authority | Canonical artifact |
| --- | --- |
| Accepted execution history | [Execution ledger](execution-ledger.md) |
| Findings and dispositions | [Issues](issues.md) |
| Engine architecture | [Architecture report](reports/architecture.md) |
| Current checker analysis | [Checker inventory](reports/checker-inventory.md) |
| Derived-value ownership | [Count-authority report](reports/count-authority.md) |
| Temporary lexical model boundary | [Legacy reference model](reports/legacy-script-reference-model.md) |
| Package lifecycle and exact write sets | [Checker migration packages](../../../evaluation/standards-effectiveness/checker-migration-packages.tsv) |
| Executable-edge lifecycle | [Executable edge dispositions](../../../evaluation/standards-effectiveness/executable-edge-dispositions.tsv) |
| Registered suite authority | [Suite registry](../../../evaluation/standards-effectiveness/suite-registry.toml) |
| Current generated observations | [Structure inventory](../../../evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv), [nodes](../../../evaluation/standards-effectiveness/generated/checker-dependency-nodes.tsv), [edges](../../../evaluation/standards-effectiveness/generated/checker-dependency-edges.tsv), and [components](../../../evaluation/standards-effectiveness/generated/checker-dependency-components.tsv) |
| Parent normative migration | [Standards restructure plan](../../../plans/standards-library-effectiveness-restructure-plan.md) |

## Blockers

- `none`

## Re-Plan Triggers

- Python 3.11+ cannot remain supported without unacceptable provisioning.
- A required invariant needs arbitrary command execution, dynamic code, or a
  policy-specific engine branch instead of a bounded reusable check.
- Strict TOML/TSV cannot represent a package legibly enough for semantic review.
- A migrated suite would lose negative, disposition, ownership, typed outcome,
  route, or source-closure evidence.
- Fresh incidence differs from admitted package/edge authority.
- Shared authority overlaps unrelated dirty files or concurrent write sets.
- Complete verification requires treating a removed checker as fallback.
- Package acceptance would retain a wrapper, Bash bridge, compatibility parser,
  inferred owner, false dependency, or dual authority.

## Concurrent Work

Package-local preparation may run concurrently only after owner, semantic
outcome, dependencies, exact write set, and verification contract are admitted.
Workers may edit only disjoint suite, fixture, and deleted-checker paths.

Registry, package and edge manifests, generated artifacts, READMEs, shared
helpers, engine contracts, plans, and acceptance checkpoints remain serial
integration-owner work.

## Final Acceptance

- Acceptance status: `pending`
- Deferred follow-ups: `none`
- Final status: `Active`
