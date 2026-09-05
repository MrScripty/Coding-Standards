# Coverage publication prerequisites

The user subsequently selected Engine audit authority. The
[publication implementation](engine-audit-publication-2026-09-04.md) records that
decision and the resulting Engine workflow; the investigation below explains
the prerequisites.

Investigation of the [coverage publication gap](standards-coverage-followup-2026-09-04.md)
found two evidence-integrity issues that must be addressed before persisting
new reviews.

## Exclusions need verified evidence

The Engine's `coverage-attestation` resolution passed the main `evidence` list
to its configured authorization adapter, which resolves exact bytes and checks
their digests. It copied `explicit_exclusions` into the immutable claim without
resolving those references. A claim could therefore contain an exclusion whose
digest did not match its file.

Resolution now passes both lists to the adapter. A mismatched exclusion produces
`ANALYSIS.EVIDENCE_DIGEST_MISMATCH` without recording a new Analysis state. Valid
exclusions remain distinct from primary evidence in the stored claim. Repository
coverage loading uses the same complete evidence set for authorization.

## Repository certificates need retained digests

Repository attestation schema 5 stores evidence paths. When loading a current
claim, the repository computes new digests from the files at those paths. The
stored record does not identify the bytes originally reviewed. Changes to an
evidence report outside the requirement's dependency horizon can consequently
leave a claim current while substituting different evidence bytes.

Schema 6 adds exact references for both evidence and exclusions. Each reference
contains the path ID, SHA-256 digest, and `repository-content` provider version
`1`. Loading a current claim checks the retained digest against the actual bytes.
An unsupported provider, malformed reference, or changed evidence is rejected.
Claims still need the current requirement ID and the configured auditor;
pinned bytes alone are not approval.

Schema 5 remains readable for the existing records and historical snapshots.
No existing claim was converted, renewed, or assigned a newly calculated digest.
The actual authorized review must supply the references used for publication.

## Auditor decision needed for publication

The repository currently recognizes
`standards.review.audit:user-authorized:documentation-cleanup`, with archived
documentation-cleanup authorization evidence. The local Engine instead operates
as `principal.standards-engine.local` under its configured authorization adapter.
Copying a local review into the current repository format would either be
rejected or require falsely attributing it to the historical auditor.

Two viable ownership choices remain:

| Choice | Publication behavior |
| --- | --- |
| Engine audit authority | Bind publication to the Engine's configured auditor and retain that authority with the reviewed claim for future snapshots. |
| Separate repository auditor | Require the configured repository auditor to authorize admission of an Engine review; retain both the original review provenance and repository admission authority. |

The user selected Engine audit authority after this investigation. Neither
choice may rewrite the review's evidence, provenance, or requirement identity.
After that decision, publication should consume the immutable reviewed claim,
recheck its exact destination requirement and evidence, and use the existing
verified candidate, local publication, and recovery lifecycle. It should not
introduce caller-authored certificate files or an independent Git publication
path.

## Validation

All 97 Analysis tests passed, including schema-6 readback, changed primary and
exclusion evidence, stale requirements, and unsupported providers. A public
Engine resolution regression also passed: bad exclusion bytes are rejected
without a state write, and valid primary and exclusion references reach the
configured authorizer together.

The public `verify_repository` operation refreshed derived suite inputs and
passed all 271 suites / 858 checks. Ruff and whitespace checks passed.
