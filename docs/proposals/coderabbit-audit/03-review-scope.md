# Proposal 3: Scope and completion of reviews used as gates

Status: saved through the Coding Standards MCP; `needs-action`, unreviewed and
unapplied.

## Purpose and effect

When a project chooses a review as a gate, distinguish completed review of an
identified source and scope from bot activity, command acknowledgements,
skipped review or an empty finding list. Preserve source mapping when carrying
a review into acceptance of a later revision.

The archive records bot activity on 139 of 150 PRs and completed code review on
45. A completed review may cover only one historical revision or bounded
range. These records support conditional scope guidance, not a requirement to
adopt CodeRabbit, a paid service or review on every edit.

Use the existing review artifact when it supplies the necessary facts. No
separate receipt format or universal full-file review requirement is introduced.

Evidence: [the ZIP coverage summary and source record](evidence.md).

## Proposed edits and placement

Add `Review Evidence Scope` to `workflow.tooling`, immediately before
`Tool-Debt Governance`. Register `workflow.tooling.review-evidence-scope` at
semantic revision 1 and add supporting provenance. Preserve the existing
Tool-Debt Governance policy and its semantic revision.

## Exact proposed wording

The following new section was read back from the immutable MCP candidate.
The submitted request includes the complete unchanged surrounding module.

## Review Evidence Scope

When a project relies on a human or automated review to satisfy a named gate,
establish the review's completion, exact source revision or range, examined
scope, and material exclusions. Use the existing review artifact when it supplies
those facts; a separate receipt is not required.

Before carrying that review into acceptance of another source revision, establish
how the reviewed source maps to the accepted source and which material changes
remain unreviewed. Review-only slices may contribute coverage when their source
mapping and examined scope establish the selected claim. Derive required
coverage and exclusions from that claim and the project's review authority.

Bot presence, summaries, command acknowledgements, skip notices, and an empty
finding list do not independently prove completed review of the required scope.
Thread resolution records discussion state; remediation acceptance requires the
evidence selected for the affected behavior.

Missing required completion or scope facts leaves the review claim `unavailable`;
contradictory scope or a false completion claim is `invalid`. Continue independent
checks while retaining any unsatisfied required review claim.

This rule applies only to a review the project has selected as a gate. It does
not require a provider, paid service, review on every edit, full-file coverage,
or treating every exclusion as a defect.

## MCP record and outstanding work

- Proposal: `proposal:v1:21e52eda-e849-4843-b2d5-f5d2a384e889`.
- Revision: `proposal-revision:sha256:2b0e0698fc06f3f73f1b0ddbe1ecb823fa4a519060a8a232c0847dd8aaccba27`.
- Analysis: `analysis:sha256:d71f07942517e0a99268717f52a9717ee103659a1d445e722eb6bdd8ffd4bdac`.
- Current analysis reports 5 pending obligations: consumer review for Rust
  tooling, TypeScript and the tooling recipes; coverage review for the new
  policy scope; and provenance impact review.
- Application exposure: `needs-review`.

These handles identify the saved draft. Complete the Engine's consumer,
coverage and material review before any later authorized application.
Historical review coverage was not revalidated against live PRs in this work.

[Submitted request](03-review-scope-request.json) ·
[MCP result](03-review-scope-result.json).
