# Milestone 3 Change Classification And Graph Union

## Outcome

The first Milestone 3 slice is accepted. `standards_analysis` now validates and
classifies modification, addition, and removal descriptors against immutable
accepted and proposed policy-unit corpora, returns the exact graph seeds and
named groups required by the accepted impact contract, and traverses their
deterministic accepted/proposed union through the generic graph engine.

## Classification

- Modification requires one stable active ID in both corpora, unchanged
  ownership, locator, lifecycle, and accepted semantic revision.
- Equal source representations classify as `unchanged`.
- Changed representation with equal structure classifies only as
  `representation-only-candidate`; it is not semantic proof.
- Changed structure without an exact semantic overlay remains
  `possibly-semantically-changed` and `unresolved`.
- An exact overlay binds the accepted revision, next proposed revision, and
  proposed structural digest before classification as `semantically-changed`.
- Addition requires an unused ID, active proposed unit, initial revision 1,
  no predecessor lifecycle, and an exact semantic overlay.
- Removal requires an active accepted unit and an exact permanent proposed
  tombstone binding the retired accepted semantic revision.

Move, split, and merge are representable by the canonical enum but return the
explicit `CHANGE.UNSUPPORTED_KIND` outcome in this slice. Their lifecycle
semantics remain unimplemented rather than partially inferred.

## Graph Selection

- Modification seeds the stable policy ID in both graphs and selects only
  `policy-impact`.
- Addition seeds the proposed policy ID and its canonically derived owner
  module and selects proposed `policy-impact`, `standards-requires`, and
  `standards-specializes`.
- Removal seeds the accepted policy ID and selects only accepted
  `policy-impact`.

The Python group map is mechanically compared with the canonical interface
schema.

## Graph Union

- A node-only provider projects active policy units, aliases, and tombstones
  from accepted policy-unit authority. It declares no edges or groups.
- Callers supply immutable accepted and proposed `EdgeRegistry` views; the
  analyzer does not locate manifests or own graph storage.
- Every seed traverses only its selected group and direction. Transitivity is
  taken from the registered group contract rather than reimplemented.
- Candidate identity is the stable edge ID. Exact accepted and proposed traces
  retain seed, selected group, path nodes, path edges, relation, complete group
  membership, metadata, and declaration provenance.
- An edge present in both snapshots remains one candidate with both traces.
  Removed and added edges therefore remain visible in the same deterministic
  result.
- Unknown seeds, groups, or incompatible traversal produce typed analysis
  failure; they are not interpreted as empty impact.

This slice does not generate obligations, evaluate edge applicability, certify
empty impact, or create a second graph representation.

## Negative Evidence

Tests reject descriptor cardinality errors, owner mismatches, identity or
locator changes disguised as modification, direct accepted-revision mutation,
semantic-overlay revision or digest mismatch, missing addition overlays,
retired-ID reuse, missing or mismatched removal tombstones, duplicate policy
claims, orphan overlays, premature lifecycle changes, unknown graph seeds or
groups, and selection outside declared named groups.

## Verification

- 40 `standards_analysis` tests passed.
- 12 `standards_engine` tests passed.
- Seven neutral metadata, two standards-graph, and 35 generic graph tests
  passed.
- 381 standards-verifier tests passed.
- The canonical contract passed 23 examples, seven identity fixtures, four
  operation envelopes, and 96 definitions.
- All 218 registered declarative suites passed.
- Python compilation with bytecode redirected outside the repository and
  `git diff --check` passed.

The complete mixed checkpoint remains reserved for a shared integration or
milestone boundary; this package-local slice did not change registry,
generated, verifier, or retained-Bash authority.

## Replan Boundary

The next obligation slice cannot consume the current explanatory applicability
strings as typed expressions. The accepted trigger and options are recorded in
[the policy-impact applicability replan](milestone-3-policy-impact-applicability-replan.md).
No obligation, audit, packet, or lifecycle implementation is admitted until
that authority decision is accepted.
