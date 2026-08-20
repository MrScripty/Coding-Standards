# Generic Directed Edge System Execution Ledger

## 2026-08-20: Plan Construction And Admission

- Plan path: `docs/plans/generic-edge-system/plan.md`.
- Operation: `start`.
- Accepted base: `7ae51ba996827cbf35cb6a5d73476b9eeb724437`.
- Preconditions: canonical `main` was clean; M6-I16 was accepted in both active
  plans and the package manifest; M6-I17 was not admitted; and no active shared
  write set overlapped the graph engine, verifier, registry, Planning, or
  generated authority used by this recovery.
- Coordination: stale detached worktrees were left untouched. Their dirty Bash
  checker experiments do not authorize or overlap this recovery's write set.
- Discovery: no neutral graph owner exists. Policy impact, suite dependencies,
  and metadata dependencies duplicate permanent graph mechanics; the temporary
  Bash graph remains frozen and deferred.
- Evidence: the graph inventory records 14 exact dispositions and the accepted
  pre-migration query records all 24 Planning consumers.
- Validation: this plan and both parent active plans passed plan-structure
  checks in the `Planned` state; `git diff --check` passed.
- Result: Milestone 1 is the only admitted implementation slice. M6-I17 and
  temporary migration graph changes remain unauthorized.

## 2026-08-20: Neutral Graph Engine Foundation

- Operation: `continue`.
- Boundary: `tools/graph_engine/` owns only neutral models, errors, registered
  sources, alias resolution, immutable indexes, queries, and traversal.
- Authority: stable edge and group IDs are explicit; incoming, outgoing,
  incident, edge-to-group, and group-to-edge indexes are derived in memory.
- Sources: strict TOML manifests register through a strict source registry;
  deterministic providers register through the Python protocol. Unregistered
  manifests and providers contribute nothing.
- Safety: path-like aliases must resolve to contained artifacts; symlink and
  repository escape, contradictory aliases, dangling endpoints, invalid group
  membership, and mismatched provider provenance are rejected.
- Traversal: exact-edge and named-group traversal require explicit direction;
  transitive traversal is denied unless the selected group permits it; cycles
  terminate deterministically with explanatory paths and provenance.
- Verification: all 28 graph-engine tests passed, covering the 22 required core
  behaviors; bytecode compilation passed; the package import scan found no
  downstream dependency; the plan structure and `git diff --check` passed.
- Result: Milestone 1 is accepted. Milestone 2 is the only active slice.
