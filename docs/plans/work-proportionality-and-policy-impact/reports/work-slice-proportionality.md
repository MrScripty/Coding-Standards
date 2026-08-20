# Work-Slice Proportionality Recovery

## Accepted Direction

One coherent implementation unit is one slice. Separation is justified only
when it materially improves independent acceptance, risk containment,
dependency ordering, conflict isolation, rollback, or feedback. File, layer,
line, diff, and commit counts do not determine slice count.

The bounded-local exclusion has precedence over written-plan triggers. Public,
generated, persistence, process, language, and user-interface boundaries are
review inputs, not automatic plan requirements. A written plan is selected for
material sequencing, independently owned contract, migration, coordination,
rollout, risk, or acceptance complexity.

Ordinary written-plan implementation consumes path, operation, lifecycle,
current-authority, and acceptance decisions. Revision, stale-state,
compatibility, and reconciliation decisions remain owned by the Concurrent Plan
Integration profile and are consumed only when Router applicability selects it.

## Consumer Review

[The exact disposition table](planning-consumer-dispositions.tsv) contains one
row for every artifact returned by the post-change `workflow.planning` reverse
impact query. It records whether the consumer was updated or reviewed without a
change, why, and which registered suite owns its evidence. No returned consumer
was classified as not applicable.

## Decision Evidence

The multi-output
[`work-slice-proportionality.tsv`](../../../../evaluation/standards-effectiveness/fixtures/planning/work-slice-proportionality.tsv)
fixture proves the required cases independently across plan selection, slice
selection, planning-artifact updates, concurrent-profile routing, and
concurrent-record consumption. Boundary and commit count are inputs but do not
independently change an outcome.
