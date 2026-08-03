# Milestone 7 Row 25 Implementation Prompt Decomposition

## Owner Contract

`workflows/implementation.md` is the sole projection owner for the versioned
implementation prompt. Frozen snapshot sections establish identifier lineage
only; they do not override current canonical workflow authority.

Planning owns active-plan state, findings, delegation, and re-planning;
Verification owns evidence and acceptance; Commit owns staged review and commit
procedure. The prompt routes through Implementation and cannot copy those
contracts, preserve a legacy checklist, or act as a second router.

## Exact Dispositions

`STD-0852` through `STD-0858` receive exact `index` dispositions to
`workflows/implementation.md`. No normative movement is required because the
useful snapshot semantics already exist in canonical workflows.

## Ordered Children

1. `25.1`: replace the tracked checklist with one thin, versioned,
   path-neutral Implementation entrypoint; record seven exact dispositions and
   focused positive and negative projection evidence.

The prompt, dispositions, focused fixtures/checker, plan, ledger, and affected
shared cursor assertions are the only allowed implementation write set.

## Re-plan Triggers

Stop if snapshot lineage must be regenerated, the prompt needs an independent
lifecycle or generation system, copied canonical procedure must remain, one
identifier needs multiple dispositions, or implementation requires files
outside the approved write set.
