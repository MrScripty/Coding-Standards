# Review of the Planning verification-line correction

Reviewed revision `2c2138ae204491c60437207cc0dfe38e3bf06fc3`. This is the review
evidence for one proposed standards change. The change is offered separately
from the plan-format check removal so that it can be accepted or rejected on
its own. It is not a coverage attestation.

## The change

| Target | Before | After |
| --- | --- | --- |
| `workflows/planning.md`, metadata line 12 | `Verification: Active-plan structure fixtures and objective-level acceptance review.` | `Verification: Objective-level acceptance review.` |
| `evaluation/standards-effectiveness/verification-guide.md`, line 10 | `metadata, routes, navigation links, plan records, consumer graph structure,` | `metadata, routes, navigation links, consumer graph structure,` |
| Application approval of `workflow.planning` | Bound to the content before this change | Bound to the content after this change |

## Why

The [plan-format check removal](plan-format-check-removal-2026-11-13.md)
retired the checks, the validator and the sample plans. Both sentences still
said those checks exist. Each edit removes only the part that is no longer
true. The remaining words of each sentence are unchanged.

## What was checked

Candidate content

- The candidate `workflows/planning.md` has SHA-256
  `6b728ad32fbabdd203a3c09586251d0b7b5edd5bc465807e2d312c0f45c832f7` and
  differs from the accepted file in line 12 only. The candidate verification
  guide has SHA-256
  `1a0f5b737ed69102d6da76c0cc007f224dc5bef36180f0f7c8a00cb1b0a61361` and
  differs in line 10 only.
- The Engine's analysis of the candidate reports no changed policy unit. The
  eight registered policy units of `workflow.planning` keep their text,
  headings and semantic revisions.
- The Engine's proposal verification of the candidate passed with 22 suites
  and 47 checks.

The Planning metadata line

- `Verification` is a prose metadata field. The metadata loader requires it to
  be present; no routing rule, relationship, check or generated inventory reads
  its wording.
- The old sentence is copied nowhere outside historical records under
  `docs/plans/` and `docs/proposals/`, which are not changed.
- The remaining clause is still true. The module still requires objective
  acceptance claims with matching evidence before a plan is `Accepted`.
- Fifteen relationships name `workflow.planning` as a normative consumer of
  other policy units. None of those policies concerns how the module itself is
  verified, so none needs a consumer change.

The verification guide

- After the validator removal the Verifier README lists eight check kinds.
  They cover metadata (`metadata_graph`), routes (`metadata_route`),
  navigation links (`markdown_targets`, `markdown_links`,
  `markdown_link_coverage`), the consumer graph (`policy_impact`), generated
  contracts (`contract_projection`) and package boundaries
  (`python_package_contract`). The guide's corrected list names exactly these
  six subjects.
- Two relationships name the guide as a documentation projection, both from
  Commit policy units. The corrected sentence is not about commits, so neither
  relationship is affected.
- The guide has no application approval before or after.

Application delivery

- Without a new approval, an application read of the candidate
  `workflow.planning` is labelled `changed-since-review`. No other approved
  target changes label.
- The only difference from the previously approved content is the one metadata
  line above, so the change set approves the candidate content. With the
  approval, the candidate read is labelled `current`.
- Two other targets, `prompts/implement-plan.md` and
  `templates/PLAN-TEMPLATE.md`, were already labelled `changed-since-review`
  before this work. This change does not touch them.

## Not changed, and why

`workflows/planning.md` also says that automated verification may inspect
current plan structure and current authority. That sentence permits such a
check and does not say one exists, so it remains true and is left as it is.

## Limits

This review covers the two sentences and their direct readers. It does not
review the rest of the Planning workflow, and it does not decide whether a
plan's structure should be verified in some other way later.
