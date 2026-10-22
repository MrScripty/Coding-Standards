# Certificate retirement review

## Observed obstruction

The first refinement request was rejected before proposal creation with
`ANALYSIS.EVIDENCE_DIGEST_MISMATCH`. Both supplied evidence references matched
their actual bytes. A diagnostic replay in a disposable clone identified an
existing Engine-issued certificate pinning the whole `workflows/verification.md`
file as review evidence. The proposed unrelated paragraphs changed its digest
while the certificate's policy requirement stayed current.

Inspection identified three such registered certificates, for:

- `topic.concurrency.cessation-of-effects`;
- `topic.security.untrusted-execution-selection`; and
- `topic.security.untrusted-execution.authority`.

The maintainer explicitly selected adding narrowly scoped certificate retirement
to the Engine, then applying the refinements. The exact subject/requirement
selections and individual rationales are retained in
[retirement-plan.json](retirement-plan.json). Existing receipt bytes remain in
Git history; retirement supplies no replacement attestation or claim of coverage.

## Implementation and independent review

Interface 48 adds optional `retire_engine_certificates` selections to the existing
evidence-maintenance plan. Each selection requires a subject, requirement digest
and rationale. The Engine rejects unknown, duplicate or ambiguous identities
before writes. The existing authorization, exact revision, preview, candidate
verification and guarded-write procedure remains applicable. Only the selected
Engine-issued receipt files and registry entries are retired; normative policies,
registered subjects, consumers and unselected certificates remain intact.

Two independent review agents inspected the frozen implementation diff SHA-256
`3f7b11699834bafc972f84b931aa3fa618434a32398e20e3cd268cf19b679caf`:

- `/root/refinement_standards_review`: no correctness, security or contract
  findings from static review; requested retaining exact selections and reasons.
- `/root/refinement_spec_review`: no scope or correctness findings; confirmed
  canonical and generated schema agreement by static inspection.

These are static reviews, not runtime qualification. Existing interface-version
assertions were updated; no new tests were added or separately run. The actual
maintenance preview/application and Engine checkpoint supply their own results.

## Standards review

The independently reviewed standards candidate is request V3, SHA-256
`af3fa0b7256cda0e6408a0f562e1c5c6775ba0cc66cbd68a0ab6986343731c69`.
Review corrected an overbroad Proportionality ownership sentence and an
implementation-only return path for acceptance work. It added explicit consumer
relationships for Commit, Tooling, GUI smoke and the two Router fixture consumers.
Both reviewers reported no remaining findings within the inspected scope.
The bounded consumer search does not prove all possible consumers were found.

Review covered the source audit's semantic cases using existing evidence for
unchanged portions and a focused recheck of corrections. It does not demonstrate
downstream behavioral improvement or replace the Engine's proposal obligations,
exact application preview, review and application checks.
