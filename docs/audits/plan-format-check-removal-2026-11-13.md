# Removal of the plan-format checks

Reviewed revision `a5e8bf7ee4f29ba14826df1ce363bef13fbe2963` with the
metadata-check retirement of the same date applied. This is the review record
supplied to the Engine operations named below. It records what was checked
before the removal; it is not a coverage attestation.

## Decision

On 2026-11-13 the repository owner decided that the plan template is a guide
and that the layout of a plan is not something to verify, so the plan-format
checks are removed. Under the owner's rule for weak checks (repair a check
that is at fault; remove a check for something there is no reason to check)
this is a removal: the checks work as written, but what they check is not a
requirement.

`templates/PLAN-TEMPLATE.md`, the planning prompts and the Planning policy
text are kept. Historical records under `docs/archive/`, `docs/audits/` and
`docs/proposals/` are not changed.

## What the checks observed

Suite `planning-consolidation` held 19 checks, all of type `plan_contract`.
Each ran the plan-layout validator on one sample plan under
`evaluation/standards-effectiveness/fixtures/plans/`: 4 samples had to be
accepted and 15 had to be rejected with a fixed message.

- No check ran the validator on a real plan. The validator had two callers:
  this suite and its own unit test, which read the same 19 samples.
- Run by hand on this repository's own plans at the reviewed revision, the
  validator rejects 25 of the 28 `plan.md` files under `docs/plans/` (16 of
  them for having no `## Objective` heading) and 1 of the 20 under
  `docs/archive/plans/`. Nothing reported this, because nothing ran it.

The suite therefore showed that the validator agreed with its samples. It did
not show that any plan in use followed the template.

## What is removed, and how

| Part | Items | Operation |
| --- | --- | --- |
| Registry | The 19 checks, suite `planning-consolidation`, its registry entry, its `enforcement-suite` catalogue node, and the 4 relationships that name it | Engine `maintain_evidence`, `retire_suites` |
| Validator | `checks/plan_contract.py`, its unit test, its registration and its README row in `tools/standards_verifier/` | Ordinary code commit |
| Samples | The 19 files under `fixtures/plans/` | Engine `maintain_evidence`, `retire_inputs` |

The samples are retired after the validator code so that the validator's unit
test, which reads them, never runs without them.

## Relationships

Four relationships named the suite as both consumer and evidence owner. They
are removed with its node. No other relationship names `suite:planning-consolidation`,
so no evidence owner is replaced.

| Source policy unit | Relationships before | After |
| --- | ---: | ---: |
| `workflow.planning.active-plan-fields` | 4 | 3 |
| `workflow.planning.lifecycle-authority` | 7 | 6 |
| `topic.architecture.composed-design-admission` | 9 | 8 |
| `workflow.commit.per-commit-boundary` | 4 | 3 |

Each unit keeps its template, prompt, documentation and normative consumers,
all owned by consumer review. Policy-impact relationships 356 to 352.

## Certificates

All 24 certificates are already stale after the metadata-check retirement.
Two of them, for `workflow.planning.active-plan-fields` and
`workflow.planning.lifecycle-authority`, cite the retired suite file as
evidence. A stale certificate is ignored when coverage is read and its evidence
is not resolved, so both stay loadable. They are left in place
(`prune_stale_certificates` is `false`) until a reissue replaces them.

## Statements this makes untrue

- `workflows/planning.md`, metadata line `Verification: Active-plan structure
  fixtures and objective-level acceptance review.`
- `evaluation/standards-effectiveness/verification-guide.md`, which lists
  `plan records` among what the checkpoint checks.
- `tools/standards_verifier/README.md`, the `plan_contract` row of the
  check-kind table. This row is removed with the validator code.

The first two can only be corrected through the Engine's standards-authoring
workflow. That correction is prepared as a separate change so that it can be
accepted or rejected on its own. `workflows/planning.md` also says that
automated verification may inspect current plan structure. That sentence
grants a permission and does not say a check exists, so it stays true.

## Counts

| | Before | After |
| --- | ---: | ---: |
| Registered suites | 23 | 22 |
| Checks | 66 | 47 |
| Catalogue nodes | 121 | 120 |
| Policy-impact relationships | 356 | 352 |
| Sample plans | 19 | 0 |
