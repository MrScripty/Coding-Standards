# Milestone 3 Policy-Unit Coverage Bootstrap

## Claim Boundary

This report records the authored review used to bootstrap consumer-coverage
attestations for the 15 Planning and 13 Commit policy units accepted at semantic
revision 1. It makes one bounded claim: no additional applicable consumers were
identified within `audit-horizon.policy-impact-consumers` version 1 for the
exact current policy content and compiled relationships.

It does not claim that no consumer exists outside the registered horizon.

## Derived Requirement

The horizon resolves 856 typed members with digest
`sha256:e735b6b6f37b8107058eae2924660ba0d5695266282117a076033c0ec96d0c46`.
Membership comes from canonical modules and policy units, registered graph
sources, all 218 registered suites and their declared repository inputs, and
the supplemental policy-impact node catalog. Every member binds relevant
content or semantic state.

The audit did not use current policy-impact declarations as its membership
boundary. Relationship declarations were reviewed as the proposed coverage,
not as proof that the horizon was complete.

## Review Method

1. Reused the previously accepted bounded Planning audit of 24 consumers and
   Commit audit of 15 consumers as migration evidence, not as automatically
   generated policy-unit attestations.
2. Reviewed the 39-row semantic source inventory that maps every legacy
   module-level relationship to one or more coherent policy units. The mapping
   produces 126 policy-unit relationships and retains one exact disposition,
   rationale, locator assessment, and evidence owner for each legacy relation.
3. Searched every repository artifact in the independent horizon for the exact
   canonical module IDs and canonical document paths. This produced 35
   Planning candidates and 24 Commit candidates for manual classification.
4. Compared those candidates with the accepted consumer sets and the exact
   policy-unit relationship mapping. Former-source indexes, migration
   inventories, generated ownership tables, and historical decomposition
   evidence were classified as references to authority or historical evidence,
   not live consumers of the policy meaning.
5. Reviewed registered suite definitions separately. A suite owner field or a
   structural source reference did not create a semantic relationship. Suites
   whose accepted checks project Planning or Commit policy remain represented
   by explicit enforcement-suite relationships.
6. Retained previously reviewed consumers that do not contain a canonical ID or
   path literal, including templates and fixtures. Candidate search assisted
   review but did not define or infer relationship authority.

## Accepted Coverage

Planning retains exactly 24 consumer identities. Commit retains exactly 15.
Every one is represented by at least one policy-unit relationship, and every
one of the 28 source policy units has at least one outgoing relationship. When
several policy units reach one consumer, the relationships preserve every
selecting source and may later consolidate into one compatible consumer-review
obligation.

The exact semantic mapping is
[policy-impact-source-mapping.tsv](policy-impact-source-mapping.tsv). The
accepted compiler and graph cutover is recorded in
[milestone-3-policy-unit-source-cutover.md](milestone-3-policy-unit-source-cutover.md).
The earlier bounded consumer evidence remains available in the generic-edge
and Git branch lifecycle plans.

## Exclusions

No explicit horizon member was excluded from review. Artifacts classified as
non-consumers remain horizon members and continue to invalidate the coverage
view when their content changes. Their non-consumer disposition is a reviewed
semantic conclusion, not removal from the audit boundary.

## Attestation Decision

The exact revision-1 identity, locator, content, and outgoing relationship set
of each Planning and Commit policy unit was reviewed against the same horizon.
Each corresponding requirement may therefore receive a `complete`
repository-reviewed attestation citing this report. Attestation files do not
enter coverage-view identity, but they do enter the complete analysis snapshot
and stale any packet prepared before their commit.

Any change to a bound policy digest, relationship, applicability dependency,
horizon member fingerprint, provider contract, or identity contract produces a
new requirement and prevents these attestations from certifying the changed
view.
