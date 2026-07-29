# Milestone 7 Accelerated Execution Re-plan

## Purpose

This report accelerates the remaining Milestone 7 migration without weakening
its ownership, disposition, dependency, no-fallback, or acceptance controls. It
supplements the immutable execution train; it does not replace or rewrite that
coverage authority.

At acceptance of `7.4b8k`, 570 frozen identifiers remain in 43 pending logical clusters.
Repeating one bespoke checker and one separately reconsidered planning decision
per cluster would add process and maintenance cost without improving semantic
review. Finding `F070` records that re-plan trigger.

## Scope

This planning slice may change only:

- this report and its acceleration manifest and checker;
- the evaluation index, findings, active plan, and execution ledger.

It changes no normative or legacy standard, disposition, immutable-train row,
decomposition overlay, generated artifact, owner map, router, metadata,
dependency declaration, decision fixture, configuration, lockfile, or
downstream repository.

## Preserved Invariants

Acceleration cannot weaken these gates:

1. Every legacy identifier receives exactly one final disposition.
2. Every retained rule has one canonical owner.
3. Dependencies remain acyclic and generic policy precedes specialization.
4. Replaced legacy text cannot remain competing authority.
5. Unsafe defaults and fallbacks require negative regression evidence.
6. Shared contracts, routing, metadata, generated artifacts, dispositions,
   plans, and ledgers integrate serially.
7. Complete fail-fast verification runs for shared-contract or checker-
   infrastructure changes and at every immutable-train wave checkpoint.
8. Final source closure, downstream pilots, and manual semantic review remain
   required.

No risk class permits compatibility copies, alternate behavior, guessed
ownership, weaker evidence, or implicit fallback.

## Risk Classes

| Class | Use | Minimum evidence |
| --- | --- | --- |
| `mechanical` | Link/index closure or bounded non-normative movement with no policy decision. | Exact disposition, link, index-purity, and whitespace checks. |
| `consolidation` | Equivalent rules move to one accepted owner without changing the observable contract. | Owner-focused fixture plus metadata and legacy-replacement checks. |
| `refinement` | Broad defaults, overlaps, or mixed mechanisms require a corrected semantic contract. | Positive and negative semantic decisions plus affected owner checks. |
| `safety-critical` | Validation, panic, lifecycle, persistence, unsafe, or authority behavior can lose safety or state. | Small contract slice, typed-failure cases, negative fallback cases, and dependency review. |
| `new-owner-design` | A missing canonical module must be established before rules can populate it. | Useful owner contract, applicability/exclusions, metadata, routing, overlap review, and focused decisions. |

Risk classification selects evidence; it does not override owner, dependency,
or semantic cohesion.

## Package Contract

The
[acceleration manifest](milestone-7-accelerated-packages.tsv)
maps every pending immutable-train row to one of 39 packages. A package may
contain more than one row only when all rows share:

- one canonical owner;
- one observable semantic outcome;
- one prerequisite set;
- one risk class and verification family;
- no unresolved ownership dispute; and
- no intermediate state with competing authority.

The only multi-row packages are:

- `P08`, the two C# concurrency rows;
- `P19`, the two thin implementation-prompt rows; and
- `P30` and `P32`, two contiguous non-normative architecture-pattern
  reference rows each.

Adjacency alone never authorizes batching. A package also cannot cross an
intervening train row because that would violate contiguous-prefix progress.
The manifest is an execution contract, not normative policy or migration
bookkeeping authority. Exact ID coverage and cursor state remain derived from
the immutable train and dispositions.

## Verification Architecture

Recurring invariants will move incrementally to reusable, table-driven
validators:

1. `decision-table` validates required and prohibited outcomes, typed
   diagnostics, and no-fallback cases.
2. `owner-contract` validates useful new-owner metadata, applicability,
   exclusions, prerequisites, routing, and overlap.
3. `migration-structure` validates exact dispositions, canonical owner,
   legacy replacement, links, and bounded source closure.
4. `custom-semantic` is allowed only when the package records an invariant
   that the reusable engines cannot express.

Existing focused checkers remain authoritative until an affected package moves
their invariant to a reusable engine. There is no wholesale checker rewrite.
Conversion occurs only when a checker blocks authorized work, duplicates the
new engine materially, or the active package needs the same invariant.

The next slice, `7.4b8m`, establishes and self-tests the reusable
`decision-table` engine against the active `STD-0804` through `STD-0809`
package. It changes checker infrastructure only. Normative row-5 implementation
follows after that gate passes.

## Verification Matrix

| Change | Required verification |
| --- | --- |
| Reference or example move | Dispositions, links, index purity, exact scope, whitespace. |
| Existing-owner consolidation | Owner decision suite, metadata, legacy replacement, exact scope. |
| New canonical owner | Focused decisions, routing, metadata, dependency graph, ownership checks, complete suite. |
| Shared Core, workflow, router, or contract change | Affected owner suites and complete fail-fast suite. |
| Checker infrastructure | Checker self-tests and complete fail-fast suite. |
| Package or wave checkpoint | Package-focused checks; complete fail-fast suite at the declared wave gate. |

Commands that aggregate checkers must use `set -euo pipefail`; loop completion
cannot mask an earlier failure.

## Missing-Owner Sequence

Thirteen canonical owners are still missing. They are established in
dependency order as useful minimum modules, never empty stubs:

1. `topics/resilience.md`
2. `topics/dependencies.md`
3. `workflows/tooling.md`
4. `profiles/applications/launcher.md`
5. `profiles/languages/rust/api.md`
6. `profiles/languages/rust/dependencies.md`
7. `profiles/languages/rust/release.md`
8. `profiles/languages/rust/tooling.md`
9. `topics/accessibility.md`
10. `topics/diagnostics.md`
11. `profiles/boundaries/persistence.md`
12. `profiles/applications/frontend.md`
13. `reference/patterns/architecture.md`

Each owner-creation package freezes purpose, applicability, exclusions,
prerequisites, precedence, semantic outcome, candidate IDs, fixture family,
shared-file effects, and escalation conditions before normative movement.
Later population is consolidation work only when that contract remains valid.

## Parallel Work

`isolated-draft` packages may be analyzed or drafted concurrently only when
they use separate worktrees, owner files, legacy sections, and fixture paths.
They may not edit the active plan, ledger, findings, dispositions, immutable
train, router, metadata schema, generated artifacts, shared fixtures, or
another package's source.

One serial integration owner:

1. verifies the declared write set;
2. performs semantic review;
3. integrates packages in dependency and train order;
4. updates dispositions and shared records once;
5. performs mechanical review; and
6. runs affected and checkpoint verification.

`serial-only` packages cannot be delegated because their canonical owner or
integration surface is shared.

## Review Separation

Semantic review answers whether ownership, applicability, contract outcomes,
typed failures, evidence, and dependencies are correct. Mechanical review
answers whether dispositions, links, metadata, generated inventories, legacy
purity, and the actual write set agree.

Both reviews are required. Passing mechanical checks cannot accept an
incorrect policy, and semantic approval cannot waive exact migration
bookkeeping.

## Source Closure

After all substantive identifiers in a legacy source are disposed, one bounded
source-closure package may replace remaining introductions, navigation,
examples, and duplicated summaries with a non-normative index. Closure remains
blocked while any active rule or executable fallback remains.

The final `7.4c` milestone still owns global legacy-index review, disposition
closure, and duplication verification after the immutable remainder reaches
zero.

## Execution Sequence

For each remaining wave:

1. Confirm clean status and accepted dependencies.
2. Read the immutable row and acceleration package contract.
3. Re-plan only if evidence invalidates owner, dependency, scope, semantic
   outcome, or acceptance.
4. Perform semantic review before editing.
5. Implement one coherent package with focused fixtures.
6. Integrate shared artifacts serially.
7. Perform mechanical review and exact-scope review.
8. Run focused checks and the risk-matrix checkpoint.
9. Update the plan, findings, and ledger once.
10. Create one atomic conventional commit.
11. Bulk-close an exhausted legacy source only through its declared closure
    package.

The acceleration path preserves:

```text
Immutable coverage
  -> exact package contract
  -> focused semantic evidence
  -> serial shared integration
  -> exact dispositions
  -> fail-fast wave verification
```

## Acceptance

This re-plan is accepted when:

- all 43 pending train rows appear exactly once in the manifest;
- the rows map to 39 owner-, outcome-, and train-coherent packages;
- all 13 missing owners have one dependency-ordered creation package;
- package enums, owners, train waves, and wave gates match their authorities;
- no completed train row or normative artifact changes;
- the active plan names only the reusable-verifier foundation for the active
  row as the next slice; and
- focused planning checks and the complete fail-fast checker suite pass.
