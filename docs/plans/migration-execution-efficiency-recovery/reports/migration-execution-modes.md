# Migration Execution Modes

## Purpose

This report defines how the remaining Bash-retirement work applies the
repository's proportional slicing policy. It specializes the active migration
procedure; it does not change generic Planning or create a second package
lifecycle authority.

## Selection Contract

| Mode | Select when | Integration and verification |
| --- | --- | --- |
| `serial-coherent` | One low-risk package has no outstanding proposal; owner, consumers, dependencies, and complete write set are current; no shared contract or re-plan trigger is involved. | Record the final accepted package and implementation in one coherent commit. Run focused final-state, mutation or negative, package, edge, removal, and freshness evidence. |
| `pre-admitted` | The proposal can become stale, ownership or consumers remain unresolved, safety risk needs independent review, or a shared decision must be frozen before implementation. | Accept admission separately, refresh stale facts before integration, then run the package's focused acceptance evidence. |
| `owner-wave` | An ordered set shares one canonical owner, dependency set, semantic outcome, verification family, and compatible integration sequence. | Record one bounded wave admission, run focused evidence per member, integrate shared files serially, and run one complete mixed checkpoint at wave close. |
| `shared-contract` | Work changes engine mechanics, schemas, Router authority, shared verification behavior, or another cross-owner contract. | Use separate admission and acceptance, affected contract tests, and the complete mixed checkpoint. |

Mode selection is evidence-driven. File count, line count, commit cadence, and
elapsed time do not select a mode. Fresh evidence may escalate a mode; reducing
ceremony alone cannot downgrade one.

## Invariants

Every mode preserves:

- one canonical package record and exact executable-edge dispositions;
- complete replacement of the Bash path without a wrapper or fallback;
- owner-specific positive and negative or mutation evidence;
- source-removal and generated-freshness checks;
- explicit treatment of current callers and dependencies;
- serial integration of registry, manifests, generated evidence, and plans;
- a blocked result when required evidence is unavailable or invalid.

The package manifest remains lifecycle authority. This procedure does not add a
second execution-state table or rewrite accepted historical package rows.

## Scenario Review

| Scenario | Selected mode | Reason | Checkpoint |
| --- | --- | --- | --- |
| One owner-local checker with known consumers and no pending proposal | `serial-coherent` | The complete bounded outcome can be reviewed and accepted together. | Focused final-state evidence only |
| A checker exposes an unrecorded transitive caller during verification | `pre-admitted` | Consumer authority and the write set require an independently accepted re-plan. | Focused evidence after fresh admission; mixed checkpoint only if it closes a wave |
| Several equivalent owner-local checkers use the same assertion family | `owner-wave` | One semantic decision and dependency contract can be reviewed once without hiding member evidence. | Focused per member, one mixed checkpoint at close |
| Two adjacent checkers have different owners or mutation contracts | Separate modes/packages | Adjacency does not establish one coherent acceptance unit. | According to each selected mode |
| A package needs a new reusable assertion kind | `shared-contract` | Engine behavior affects more than one package and requires cross-owner acceptance. | Complete mixed checkpoint |
| Multiple proposals can be prepared from the same mutable package authority | `pre-admitted` | Admission facts can become stale before serial integration. | Focused acceptance plus the applicable wave boundary |
| A documentation-only correction to current migration procedure | One coherent recovery milestone | It changes current authority but not verifier behavior or Bash execution. | Affected plan/package/suite checks; no mixed checkpoint solely for commit cadence |

## M6-I44 Boundary

M6-I44 is not converted retroactively to `serial-coherent`. It already exposed
VE086 after admission: a hidden row-35 transitive consumer changes its write set
and acceptance contract. It therefore remains `pre-admitted` and blocked until
fresh re-admission resolves that consumer. No later package is selected by this
report.
