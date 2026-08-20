# Active-Plan Consumer Inventory

## Purpose

Identify every executable consumer of the two active plans before historical
narration is removed. This report records the semantic review; the adjacent
[disposition table](active-plan-consumer-dispositions.tsv) records exact
consumer-level decisions.

## Method

The inventory was derived from current repository content:

- Python `tomllib` parsed every registered suite and selected checks whose
  nested `path` fields target either active plan;
- literal references in retained `verify-*.sh` entrypoints selected shell
  consumers and their plan aliases; and
- a repository search over Python, TOML, and shell executable surfaces checked
  that the selected consumer paths were complete.

The observed totals are reporting evidence, not maintained authority. Exact
coverage is the set equality between derived consumer paths and disposition
rows.

## Findings

- The current repository derives 145 direct executable consumers: 69 suite
  checks and 76 retained shell entrypoints.
- Every consumer targets
  `plans/standards-library-effectiveness-restructure-plan.md`.
- No executable consumer targets
  `docs/plans/standards-verification-engine/plan.md`.
- Every suite reference is a text assertion over accepted migration narration.
  These checks are separate from the suite's current owner, fixture,
  disposition, or package evidence.
- Every shell reference checks historical acceptance. Some also check obsolete
  next-slice narration or invoke the generic plan-structure checker from an
  unrelated owner verifier.
- The plan's current objective, decisions, scope, and milestone state are not
  required inputs to any owner behavior contract.

The active plan is therefore functioning as a historical verification database,
not merely carrying incidental history.

## Replacement Authorities

### Local Current Contract

Owner suites already verify the canonical standard, focused decisions,
fixtures, and exact dispositions. Their accepted-plan text check adds no current
behavior evidence. Remove that check. Keep historical execution evidence in the
execution ledger without making it an automated prerequisite.

### Canonical Migration Tables

Milestone decomposition checks already consume exact decomposition,
owner-validation, disposition, source-closure, and execution-train tables.
Those tables own the durable migration result. Remove accepted-plan and
next-slice narration checks; retain the ledger for audit history.

### Verification-Engine Package Table

The source-index implementation boundary is represented by accepted package
`M6-I9` in `checker-migration-packages.tsv`. That record and its package suite
own lifecycle status. The source-index behavior suite does not also need
`` `7.4c3v1` (`Accepted`) `` in the parent plan.

### Plan Structure

Plan structure remains a Planning-owned independent gate. Remove duplicated
invocations from unrelated shell owner checks and validate each active plan once
through the Planning verification surface.

## Migration Packages

| Package | Scope | Outcome | Ordering |
| --- | --- | --- | --- |
| `PPR-C1` | All declarative suite rows in the disposition table | Delete accepted-plan text checks while preserving every current owner, fixture, disposition, package, and decision check. | First |
| `PPR-C2` | All retained shell rows in the disposition table | Remove parent-plan variables, accepted-history assertions, obsolete next-slice assertions, and duplicated plan-structure calls while preserving non-plan behavior until each checker is migrated to Python. | After `PPR-C1` |

Both packages have one semantic outcome: active plan prose stops authorizing
historical acceptance. They are separated by representation and verification
contract, not by filename adjacency. Shared plan compaction remains a later
serial slice.

## No-Fallback Decision

The migration will not:

- copy accepted plan prose into another narrative file for checkers to search;
- introduce a generated compatibility plan;
- retain old checks against the ledger as a second current-behavior gate;
- infer package acceptance from timestamps or line order; or
- preserve parent-plan references until Bash retirement.

Current behavior uses current canonical evidence. Historical execution remains
available to humans through ledgers and reports. Migration lifecycle uses its
existing structured authority.

## Result

Every direct executable active-plan consumer has one disposition and one
replacement-authority class. No ownership conflict or missing authority was
found. `PPR-C1` can proceed after the Planning contract split so its suites no
longer enforce the universal transition protocol being corrected.
