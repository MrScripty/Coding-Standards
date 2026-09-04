# Milestone 2 Read, Related, And Inspect

## Outcome

Accepted the snapshot-bound typed navigation foundation for `read`, `related`,
and `inspect`. Router projection and the `route` request remain the sole next
slice; impact analysis remains outside this acceptance boundary.

## Implemented Contract

- `standards_engine` is the composition facade over `standards_metadata`,
  `standards_analysis`, `standards_graph`, and the repository-neutral graph
  engine. None of those packages imports the facade.
- Every request uses the exact immutable snapshot handle issued while opening
  the repository. A different handle returns `NAVIGATION.STALE_SNAPSHOT`.
- `read` accepts canonical module or registered policy-unit IDs. Canonical
  modules return whole-artifact scope; policy units return their exact resolved
  heading scope.
- `related` selects explicit named graph groups and direction. Transitive
  traversal delegates to the generic graph engine and retains its traversal
  restrictions and typed failures.
- `inspect` resolves snapshot, policy, relationship, and navigation handles.
  Repository paths and declaration locators appear only in explicit provenance
  inspection.
- Canonical module declarations and authored policy-unit declarations are
  distinct version-1 inspection variants. Stable registered edge identities
  use the separate `EdgeId` contract.
- Native malformed requests, unknown policies, unknown groups, forbidden
  traversal, retired identities, stale handles, and repository-path read
  attempts return typed rejection results without fallback lookup.

## Evidence

- Contract validation: 23 examples, seven identity fixtures, four operation
  envelopes, and 96 schema definitions passed.
- `standards_engine`: seven tests passed.
- `standards_analysis`: 17 tests passed.
- `standards_metadata`: seven tests passed.
- `standards_graph`: two tests passed.
- Generic graph engine: 35 tests passed.
- Standards verifier: 381 tests passed.
- Declarative verification: all 218 registered suites passed.
- Plan structure and `git diff --check` passed.

The complete mixed checkpoint remains reserved for the Milestone 2 shared
integration boundary after Router projection and typed route/read evidence.

## Remaining Limitation

The public `QueryRequest` schema includes `route`, but the Python facade does
not implement it yet. No claim is made that objective A3 or Milestone 2 is
complete until the accepted Router decision authority is mechanically
projected and exercised through the real typed query interface.
