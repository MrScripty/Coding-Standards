# Milestone 3 Coverage Identity Cutover

## Accepted Boundary

The cutover implements the accepted two-identity model without retaining the
legacy module audit mechanism. The commit and tree identities are recorded by
the accepting commit and its parent plan state.

## Authority Result

- `AnalysisSnapshot` binds the complete selected input closure, including the
  horizon declaration, attestation registry and sources, evidence, canonical
  metadata, relationship authority, suites, and registered suite inputs.
- `CoverageAuthorityView` binds one policy unit's semantic payload, outgoing
  relationship fingerprints, applicability dependencies, compiler provider
  contract, and the independent horizon. It excludes attestations,
  certificates, reports, packets, timestamps, dispositions, and storage-only
  provenance.
- `CoverageAuditRequirement` identity derives from the coverage view and does
  not include the complete snapshot recorded as provenance.
- Authored attestations bind exact requirements and evidence. Generated
  certificates bind the view, requirement, attestation, evidence, and contract
  versions; timestamps remain outside certificate identity.

The registered `audit-horizon.policy-impact-consumers` version 1 contains 856
typed, content-fingerprinted members. It derives from canonical modules and
policy units, graph-source registrations and manifests, every registered suite
and its declared repository inputs, and supplemental policy-impact nodes. The
node catalog is not its sole authority.

## Coverage Result

The reviewed bootstrap produced 28 current certificates:

- 15 Planning policy units, with no uncovered Planning subject.
- 13 Commit policy units, with no uncovered Commit subject.
- Zero certificates are inferred from absent relationships.
- `workflow.verification.acceptance-claims` remains uncovered and returns an
  unaudited result rather than successful empty impact.

An unrelated relationship change does not alter another policy unit's view.
A relationship placed under an attestation-named path still changes its source
view because projection uses typed artifact roles rather than directories.
Changing a registered suite input changes the horizon digest even when that
consumer is absent from policy-impact declarations and the node catalog.

## Removed Authority

The cutover deletes `policy-consumer-audits.toml` and removes `audit_catalog`,
compiler audit loading and matching, `audit_declaration`, `audited_owners`, the
old verifier coverage path, and superseded public contract definitions. No
compatibility loader or successful-empty fallback remains.

## Verification

- Graph engine: 35 tests passed.
- Applicability: 9 tests passed.
- Standards metadata: 15 tests passed.
- Policy impact: 7 tests passed.
- Standards graph: 2 tests passed.
- Standards analysis: 36 tests passed.
- Standards Engine: 15 tests passed.
- Standards verifier: 380 tests passed.
- Contract validation: 29 examples, 7 identity fixtures, 4 operation
  envelopes, and 109 definitions passed.
- Declarative verification: 218 of 218 suites passed.
- Focused policy semantic impact: 2 checks passed.
- Plan structure, policy-impact alias queries, and `git diff --check` passed.
- Complete mixed checkpoint: generated evidence, 218 declarative suites, and
  all 53 retained Bash checkers passed from the exact accepted write set.
