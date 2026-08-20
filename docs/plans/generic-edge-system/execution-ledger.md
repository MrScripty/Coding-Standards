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

## 2026-08-20: Milestone 2 Generic Dependency Refinement

- Discovery: the accepted registry provides traversal but not a direct cycle
  witness or dependency-first order. Adapting suite and metadata dependencies
  without those operations would preserve duplicate downstream DFS logic.
- Decision: extend the active slice's exact write set with generic deterministic
  cycle detection and dependency ordering, then require both domain adapters to
  consume those operations.
- Scope effect: no objective, owner, migration disposition, domain schema, or
  temporary graph authority changes. The refinement is part of the already
  admitted permanent-dependency adaptation.

## 2026-08-20: Repository Composition Re-Plan

- Finding: policy impact was available through the default generic query, but
  suite and metadata providers were instantiated only by verifier consumers.
  Their local registries passed adapter tests while the repository query could
  not report those groups for an arbitrary artifact.
- Impact: this violates the objective's one-query discovery contract even
  though storage, traversal, and adapter behavior are individually correct.
  Milestone 2 and objective acceptance were therefore reopened before commit.
- Decision: extend explicit source registration to accept caller-supplied,
  named deterministic providers. Keep provider construction in one downstream
  repository composition root; inject the completed registry into the neutral
  CLI so the graph engine imports no consumer.
- Required proof: the canonical query must list policy, suite, and metadata
  groups together and resolve incident edges from logical IDs and paths. An
  unregistered or unavailable provider must fail neutrally rather than being
  scanned, inferred, or skipped.

## 2026-08-20: Downstream Migration And Objective Acceptance

- Policy impact now loads from the registered generic edge source as the
  `policy-impact` and `semantic` groups. Policy validation, allowed relations,
  applicability, evidence ownership, audited coverage, and typed diagnostics
  remain downstream adapter responsibilities.
- The source registry explicitly names the policy manifest and deterministic
  suite and metadata providers. `tools/query_edges.py` is the sole canonical
  repository command and injects downstream provider composition into the
  neutral CLI; the graph engine imports no consumer.
- The canonical command reports six groups. `workflow.implementation` exposes
  policy and metadata edges together; `concurrent-plan-integration` exposes
  policy and suite-dependency edges through both suite ID and path aliases.
- The obsolete policy graph query, policy CLI, and manifest-only graph command
  were deleted. There is no alternate schema, reverse index, compatibility
  representation, inferred provider, or fallback lookup.
- Planning has 24 canonical outgoing policy-impact edges. Queries by
  `workflow.planning` and `workflows/planning.md` returned the same exact edge
  identities, including the full-review prompt, fixture, and suite.
- Exact review dispositions cover all 24 Planning consumers. The repository
  inventory retains the frozen temporary Bash graph and specialized lifecycle
  assertions under explicit deferred or retained dispositions.
- Verification passed: 32 graph-engine tests, 323 standards-verifier tests,
  164 registered declarative suites, generated-evidence freshness, affected
  plan and link checks, exact alias/disposition comparisons, `git diff
  --check`, and the complete checkpoint with 109 retained Bash verifiers.
- Result: both milestones and the generic-edge objective are accepted. Parent
  verification work resumes with a fresh graph audit; M6-I17 remains
  unselected and unadmitted.
