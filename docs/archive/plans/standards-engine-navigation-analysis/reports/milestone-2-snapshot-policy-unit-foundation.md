# Milestone 2 Snapshot And Policy-Unit Foundation

## Decision

Accept the snapshot and policy-unit foundation as the first Milestone 2 slice.
It establishes immutable input identity and stable policy-unit authority without
adding navigation, Router projection, semantic analysis, or repository writes.

## Implemented Boundary

- `tools/standards_analysis/` owns canonical serialization, snapshot
  compilation, policy-unit loading, and neutral analysis failures.
- Clean Git identity uses the Git tree while commit identity remains
  provenance. Declared scope, exclusions, and submodule state are explicit.
- Dirty Git and non-Git sources use deterministic manifests. Explicitly scoped
  ignored files remain inputs; unrelated untracked files outside scope do not.
- Symlinks are recorded without traversal. Reading through an escaping symlink
  ancestor is rejected.
- Dirty gitlinks and nested repositories bind nested snapshot handles; Git
  administrative data is not traversed as source content.
- The policy-unit registry is explicit. Module paths derive from
  `standards_metadata`; sidecars do not copy path, alias, membership, Requires,
  or Specializes authority.
- Representation digest, structural digest, and accepted semantic revision are
  separate values. Structural equality is not semantic acceptance.
- Active identities, aliases, locators, tombstones, predecessors, and
  successors are globally checked for conflicts and reciprocal lifecycle links.

## Scope Disposition

| Surface | Disposition | Reason |
| --- | --- | --- |
| Canonical standards and Router | reviewed-no-change | This slice creates read-only identity foundations and changes no policy or routing decision. |
| Generic graph engine | reviewed-no-change | No new graph operation or edge authority is required. |
| Standards verifier | reviewed-no-change | The analyzer is independent and no verifier execution path imports it yet. |
| Policy-unit authority | updated | Added one registered source and one exact accepted policy-unit identity. |
| A1 plan and ledger | updated | Current authority advances to the next bounded Milestone 2 slice. |

## Verification

- `python3 -m unittest discover -s tools/standards_analysis/tests`: 17 passed.
- `python3 -m unittest discover -s tools/standards_metadata/tests`: 7 passed.
- `python3 -m unittest discover -s tools/standards_verifier/tests`: 381 passed.
- `python3 -m unittest discover -s tools/graph_engine/tests`: 35 passed.
- `python3 tools/standards_engine/contracts/validate_contracts.py`: 22 examples,
  7 identities, 4 operation envelopes, and 94 definitions passed.
- `python3 tools/standards_verifier/verify.py --all`: 218 of 218 suites passed.
- `git diff --check`: passed.

The mixed checkpoint is deferred to the Milestone 2 shared integration gate.
No existing runtime consumer changed in this package-local foundation slice.
