# Milestone 4 Horizon Projection Replan

## Trigger

The reading-plan cutover added explicit `authority` classifications to the 27
existing non-module nodes. Node IDs, aliases, repository paths, graph groups,
graph edges, all 126 compiled policy-impact relationships, and compiled
semantics remained unchanged. Nevertheless, all 28 Planning and Commit coverage
requirements changed because horizon provider version 1 fingerprints the
complete node-catalog manifest as one opaque `edge-source-manifest`.

That invalidation is mechanically consistent with version 1 but broader than
the accepted `CoverageAuthorityView` contract, which binds only inputs capable
of changing consumer discovery.

## Accepted Correction

Explicit target authority remains canonical node metadata. Path and
relationship inference remain prohibited.

The complete node-catalog bytes remain in `AnalysisSnapshot` input closure, so
any classification change stales packets and navigation. Audit-horizon provider
version 2 compiles a narrower coverage fingerprint for this typed manifest:

- retain schema and source identity;
- retain node IDs, aliases, paths, suite bindings, and every metadata field
  except `authority`;
- retain every group field and edge field; and
- exclude exactly `nodes[].metadata.authority` as reading-only metadata.

The exclusion is structural and field-specific. Unknown future metadata is
retained and therefore conservatively invalidates coverage.

## Binding Sequence

1. Implement and test the provider-v2 projection.
2. Complete all reading-plan, schema, catalog, suite, graph-source, module, and
   policy-unit changes admitted by this slice.
3. Freeze the proposed horizon inputs.
4. Compare base `50043a5b` with the final proposed authority and record all 27
   node dispositions, topology, and 126 compiled semantic dispositions.
5. Generate the exact 28 current coverage requirement handles.
6. Obtain authorized `standards.review.audit` evidence over that exact
   horizon.
7. Renew Planning and Commit attestations once.
8. Compile certificates and run broad verification without further
   horizon-affecting edits.

The historical Milestone 3 bootstrap report and policy semantic revisions
remain unchanged.
