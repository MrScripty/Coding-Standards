# Persisted State And Version Inventory

## Boundary

- Inventory base: commit `cb6abdb89afaa4fca25706cd42f621a8c762480f`,
  tree `24328086a11f9370a615ff62254de9aa1d825931`.
- Scope: public A1 contracts, snapshot/navigation/analysis handles, analysis
  state stores, coverage artifacts, and policy-impact provider identities.

## Retained State

No repository-tracked production analysis state or snapshot manifest exists.
The only tracked state-store uses are test-created temporary directories and
in-memory stores. The public Interface accepts caller-supplied handles, so old
well-formed handles still require an explicit outcome even though there is no
repository state corpus to convert.

Disposition: version 10 rejects version 9 snapshot, navigation, analysis, and
coverage handles or state as `unsupported`. Tests construct old values directly
and prove the rejection. No compatibility loader, dual reader, state relabeling,
or offline converter is admitted.

## Version Decisions

| Contract | Current | Replacement | Reason |
| --- | --- | --- | --- |
| Public interface/schema | 9 | 10 | Public operation closure and relationship inspection shape change. |
| Result projection | 1 | 2 | `RelationshipInspectionResult` replaces compiler internals with an operation-shaped semantic view. |
| Analysis contract/schema | 5/2 | 6/3 | Reprojection consumes the v2 provider and persisted state must reject the prior authority closure. |
| Snapshot/navigation/analysis handle and identity | 2 | 3 | Handles bind changed semantic contracts and must distinguish unsupported predecessor state. |
| Policy-impact authoring/catalog/kinds/provider | 1 | 2 | Typed artifact compatibility and one graph/semantic/coverage projection replace split ownership. |
| Coverage view/requirement/attestation/certificate | 1 | 2 | Provider, relationship IDs, catalog typing, and horizon inputs all change. |
| Coverage horizon provider | 2 | 3 | Membership and fingerprints consume the compiled typed catalog rather than a raw manifest. |
| Edge identity algorithm | 1 | 1 | Encoding and natural key do not change; relation changes naturally create replacement IDs. |
| Graph engine, applicability, metadata, evidence, authorization | unchanged | unchanged | Their represented semantics do not change in this slice. |

## Evidence Commands

The implementation candidate must rerun repository-tracked state discovery,
public version searches, generated contract freshness, direct old-version
rejection, and genuine fresh-process reconstruction. A shared in-memory store
or private authority injection is not cold-process evidence.
