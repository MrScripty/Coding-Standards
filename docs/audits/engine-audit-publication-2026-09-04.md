# Engine audit publication

The user selected Engine audit authority for future repository certificates.
This implements that choice following the
[publication prerequisite investigation](coverage-publication-prerequisites-2026-09-04.md).
It does not treat choosing an auditor as completing the outstanding policy reviews.

## Workflow

Interface version 23 adds `audit-policy-unit` to proposal edits. It names a
registered policy unit and a rationale, allowing an audit proposal without
changing standards text. An already-current certificate needs no renewal;
an unknown or retired unit cannot be certified through this edit.

The normal Analysis flow generates the exact coverage and consumer obligations.
The caller supplies the reviewed evidence and decisions, then obtains proposal
readiness. `verify_proposal` requires that readiness for coverage publication and
checks the candidate containing the receipt. Its result echoes the readiness.
Application independently reauthorizes the audit, checks destination evidence
and requirement identities, runs the complete candidate checkpoint, and uses
the existing local publication and recovery lifecycle.

Evidence must exist in the destination repository with the reviewed bytes.
The Engine reads uncaptured evidence from the exact destination Git revision;
it does not copy an uncommitted report into a certificate. A changed authority,
changed evidence, or changed destination requirement prevents publication.

## Retained authority

Attestation registry schema 3 adds an explicit `engine_sources` list. Registering
an Engine receipt admits its recorded Engine authority into repository coverage.
The receipt retains the original claim, Analysis ID, configured auditor contract,
authorization record, and exact authorization and revocation proof bytes. Primary
review evidence and exclusions retain their repository paths and reviewed digests.

A separate publication authorization binds the complete claim, original review
authorization, originating Analysis, and policy subject. Altering a rationale,
provenance, evidence reference, or exclusion makes that authorization inconsistent.
Either the review authorization or publication authorization can be revoked.

The configured Engine auditor authorizes both review and publication. Publication
first revalidates the original review authorization; it cannot silently switch auditors
or refresh a grant whose proof changed after review. Subsequent snapshot loading
validates the receipt's authorization identity and evidence bytes using repository
content, without requiring the original Engine database. The existing revocation
list can revoke the retained Engine authorization ID.

The actual issuer and principal are distinct from caller-supplied provenance text.
Coverage reads expose that retained authority alongside the requirement and status.
A portable receipt is a repository-trusted declaration with verified identities
and bytes; it is not an independently signed certificate or proof of semantic
review quality.

Legacy registry sources retain their existing formats and auditor identities.
No old claim is relabeled, converted, or automatically renewed. Obsolete Engine
receipts are ignored when their requirements no longer match; duplicate current
claims and inconsistent receipts are rejected. The new path does not require
admission from the historical documentation-cleanup auditor.

## Verification scope

The domain tests exercise receipt readback under an Engine principal different
from the legacy auditor; retained provenance; changed authority, requirement, and
evidence; revoked authorization; and tampered receipt authority. The publication
integration test exercises proposal creation, public resolution and review,
verification, changed-evidence rejection before publication, application recovery,
and coverage readback through a fresh database.

Existing policy certificates still require their actual semantic reviews. The
two downstream pilots still require repository and task selections.

Validation passed across 163 focused tests: 98 Analysis, 21 logical authoring,
20 contract, 14 generated Interface, nine rendering, and the full publication
integration test. The final integration run includes the complete-claim
publication binding. The public repository checkpoint passed all 271 suites /
858 checks; generated contract freshness, Ruff, and whitespace checks passed.
