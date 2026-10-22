# Application-exposure outcome

Updated 2026-10-22; original publication occurred on 2026-10-04.

## Published result

The33 application-exposure candidates have explicit dispositions:32 are now
qualified for application use; `workflow.standards-authoring` remains private
because it applies to library maintainers.

The Coding Standards MCP published the reviewed candidate to local `main`:

- Commit: `188beda1fa477d21d576c233dd8c7f4c4c267d23`.
- Applied proposal: `proposal:v1:800744d7-33d1-4b31-9a8e-bd66d2c9d3db`.
- Reviewed revision:
  `proposal-revision:sha256:9f0a8a377542d5372bf2c3db613a5c511693ca271e70c5b784e8290af5e14aa6`.
- Engine application:
  `application:sha256:5843ac2c62c36f4339c8a327fa832126f922ab50e92eda3a8c18fa16e67b8c6a`.

Following explicit user approval, this commit was also pushed to GitHub main
at https://github.com/MrScripty/Coding-Standards. A remote ref query confirmed
main at188beda1fa477d21d576c233dd8c7f4c4c267d23. Uncommitted workspace files
were excluded from the push. Subsequent checkout reconciliation and the separate
certificate status are recorded below.

The only normative prose change is the user-approved Rust baseline step:

> Establish the changed claim with adequate existing evidence or a construction
> guarantee, or add a focused Rust regression test when needed.

This restores Core and Verification's existing sufficient-evidence principle.
It introduces no new generic principle, test-harness mandate, or project
sandboxing requirement. The other31 approved module texts are unchanged.

The affected Baseline Rust Change scope is registered as
`profile.language.rust.baseline`, semantic revision1. Independent review of
all10 dispatched Rust specialists identified Rust Tooling as its sole direct
baseline consumer. Rust Tooling remains unchanged. The seven specialists outside
the original exposure selection remain unqualified for application use; their
bounded consumer review does not qualify their entire modules.

## Verification and review

The user-selected independent agent accepted the exact32-module candidate.
All32 native application previews succeeded, and accepted MCP readback from
the published commit confirms current qualification and exact content equality
with those previews. Required dependencies are qualified. Optional recipes retain
REFERENCE authority and do not enter Tooling's required-guidance traversal.
Maintenance workflow and provenance application previews remain unavailable.

The Engine returned `status: applied` after its required complete checkpoint.
The result contains a durable publication receipt and the target-ref observation;
it does not include individual test counts. No downstream CodeRabbit reproduction
or behavioral-effectiveness claim is made.

Evidence:

- [Independent material review](independent-review.md).
- [Independent corrected-candidate review](independent-rust-review.md).
- [Candidate validation](candidate-validation.md).
- [Application result](application-result.json).
- [Accepted readback](accepted-readback.json).

## Checkout discrepancy and reconciliation

The original Engine result reports `publication-checkout-observation.status: conflicted`.
Canonical `main` contains the published result, but the existing checkout/index
were left untouched because publication paths intersect pre-existing unpublished
work. All1538 tracked file byte states still match the task-start baseline.
Consequently the workspace Rust Markdown still contains the earlier sentence;
the accepted MCP standards contain the correction.

This is an actual checkout discrepancy, not a failed canonical publication or
an uncertain recovery state. No manual reset, stash, index, ref, or standards
file change was performed. Reconciling those pre-existing edits requires a
separate deliberate integration.

On 2026-10-22, the user explicitly authorized repository cleanup. The 51 verified
obsolete standards and metadata differences were restored to accepted `main`,
with a recovery copy retained outside the repository. The
[cleanup record](../../plans/authoring-publication-evidence/reports/checkout-reconciliation.md)
documents the source comparison. The original application result remains
unchanged as evidence of its publication-time checkout observation.

## Coverage certificate remains unpublished

The first proposal's coverage attestation was retained in its Analysis, but
accepted readback reports the new baseline subject as `review-required`.
Publishing an Engine certificate requires an explicit audit-policy-unit edit.

A certificate-only follow-up was created and independently accepted. Its
consumer and coverage obligations are resolved, but readiness was rejected:

- Proposal: `proposal:v1:b24452c8-9f63-4f8e-9e42-51a403e07ab7`.
- Revision:
  `proposal-revision:sha256:4cb48973a3daebc9162654c2665ce1d32a57a058f7064040b3bfc9792f48f0e0`.
- Resolved Analysis:
  `analysis:sha256:ff92fa3487afa24465a24b1c05a230b6d4521547f579a29c37598fd8fa6b4dd0`.
- Rejection: `COVERAGE.PUBLICATION_EVIDENCE_UNCOMMITTED`, outcome `unavailable`.
- Phase: `readiness-preflight`.
- Missing candidate evidence:
  `docs/proposals/application-exposure/independent-rust-review.md`.
- Expected digest:
  `sha256:998f863ef47520e7a3a7a31339c293e98fa8a92a299ebdd24c06c8fb27ebdcb1`.
- Engine next action: `include-reference-in-proposal`.

At the original readiness attempt, the frozen review and captured consumer
material existed as untracked workspace files; the certificate could not rely on
evidence absent from its destination Git candidate. The installed public
authoring edit surface had no operation to add
new arbitrary review-evidence files. Consumer registration only supports an
artifact already tracked in the original proposal revision. Substituting weaker
evidence or adding an application reference solely to bypass this constraint
would not preserve the intended review record.

The original MCP task stopped at that evidence-packaging capability gap.
The later user-authorized repository cleanup retains the frozen evidence in Git
alongside the implementation and historical records. It neither applies the
certificate nor changes the original proposal's captured base.

The follow-up remains unapplied. A subsequent Engine authoring task must use a
current base containing the frozen evidence, refresh the exact candidate review
and decisions, and publish its certificate through the supported workflow.
The32 exposure approvals and authorized Rust correction remain applied.

- [Independent certificate-only review](independent-coverage-review.md).
- [Exact readiness rejection](coverage-review-result.json).

## Separate principle follow-ups

The existing Library profile's new-test wording and the previously identified
fixture serialization restriction remain separate review opportunities. This
work does not modify or qualify those additional scopes.
