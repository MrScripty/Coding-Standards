# Generic Directed Edge System Issues

| ID | Status | Finding | Owner | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- |
| GES-001 | resolved | Policy impact owned bespoke storage, reverse lookup, and query mechanics downstream of the needed neutral capability. | Generic edge recovery | Migrated to registered generic groups; deleted old query authority. | Milestone 2 acceptance |
| GES-002 | resolved | Suite dependency and metadata relation checks duplicated dependency closure or cycle mechanics. | Generic edge recovery | Adapted to generic groups and operations while retaining domain declarations and diagnostics. | Milestone 2 acceptance |
| GES-003 | deferred | The temporary Bash migration graph has specialized SCC, component, and wave semantics under a frozen schema. | Verification-engine migration | Do not modify; revisit only at zero-Bash deletion or a separately demonstrated current need. | Graph inventory |
| GES-004 | resolved | The Planning impact graph omitted a Planning-owned prompt, fixture, and suite. | Policy-impact adapter | Already corrected at the accepted base; migration must preserve all 24 edges and suite-owner closure. | Commit `7ae51ba` |
| GES-005 | resolved | Adapted suite and metadata providers were not part of the default repository query composition, so arbitrary-artifact discovery was incomplete. | Generic edge recovery | Registered named providers through downstream composition and proved cross-group discovery. | Repository composition tests and complete checkpoint |
| GES-006 | resolved | Selecting an unknown group for an existing artifact without registered edges returned a false-empty result. | Generic edge engine | Validate selected groups and traversal policy before unconnected-artifact empty handling. | Registry and CLI unknown-group tests |
| GES-007 | resolved | Recursive cycle detection and dependency ordering exceeded Python's recursion limit on valid long graphs. | Generic edge engine | Replaced recursive DFS with iterative color-state cycle detection and stable Kahn dependency ordering. | 1,500-node chain and cycle test |
| GES-008 | resolved | `preferred_order` ranked only DFS roots and did not control every available dependency tie. | Generic edge engine | Apply preferred rank through the ready-node priority queue at every topological step. | Preferred dependency-tie test |
