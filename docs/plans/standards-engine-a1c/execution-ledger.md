# Standards Engine A1c Execution Ledger

## 2026-08-29 - Planning Workspace Created

- The user requested an A1c plan workspace while explicitly stating that the
  complete plan is not ready to be written.
- The workspace is `Blocked` rather than `Planned` because the accepted A1/A1b
  audit found no concrete external caller or retained-state requirement from
  which to select handle lifetime, persistence, compatibility, recovery, or
  object granularity.
- Current write authority is limited to this plan directory and one
  product-contract discovery report. No runtime, contract, generated artifact,
  fixture, suite, policy graph, normative standard, A1b deletion, or A2 change
  is authorized.
- Accepted A1b implementation
  `84412f22fa9fe082f089eaa347c30c23f185ffee` remains the behavioral and
  evidence baseline. The accepted audit supplies constraints and experiments,
  not a binding A1c architecture.
- Routed guidance: Core, Router, Implementation, Verification, Planning,
  Documentation, Architecture, Contracts, Dependencies, and the conditional
  Persistence boundary. Concurrent Plan Integration is not applicable to this
  serial planning workspace.
- The next planning step is A1C-001 product-fact discovery. Architecture
  comparison, prototypes, implementation milestones, and acceptance claims are
  deferred until those facts are explicit.

## 2026-08-29 - Discovery Scaffold Standards Review

- Review found that the initial `Blocked` lifecycle made the only authorized
  fact-discovery work unavailable. The plan and Milestone 0 are now `Planned`;
  A1C-001 and A1C-002 block architecture and implementation admission rather
  than the bounded work that resolves them.
- The former candidate treatment of the four public operations and explicit
  uncertainty is superseded. They are inherited A1c behavioral constraints
  from the accepted A1/A1b audit; discovery selects their internal composition
  and promised lifetime, not whether those behaviors exist.
- The former composed-design result is superseded by `not-applicable` for the
  discovery-only slice. The complete probe becomes applicable when a candidate
  composition exists.
- The earlier routing note conditionally selected Persistence before a durable
  crossing was known. Current Persistence applicability is `unresolved`
  pending A1C-001; no Persistence policy is selected or rejected by this
  correction.
- Acceptance evidence contracts now distinguish caller workflow, public and
  persisted contract inventory, multi-component experiments, composed-design
  review, and plan completeness. The issues register now records affected
  boundaries, fix/defer dispositions, and required verification.
- Runtime source, schema, generated artifacts, fixtures, suites, policy graph,
  normative standards, A1b behavior, and all A2 work remain outside the write
  set.

## 2026-08-29 - Planning-Path Generated-Evidence Replan

- Generated freshness exposed that the initial scaffold commit added four Git-
  indexed planning paths without regenerating the suite-input projection. Its
  repository-index digest changed from
  `sha256:e1f14e48c2c401861256e44cb2f1092c18d94e3f9c42591fe6d94df5d93d41b7`
  to
  `sha256:87ce6b28b1d88202e9c3991de7a233960701759eddad6b11a5e94e8d88bb6b7a`.
- `Superseded`: the initial decision that all generated artifacts were outside
  Milestone 0, because it omitted the existing projection mechanically derived
  from tracked-path membership.
- Replacement: admit only
  `evaluation/standards-effectiveness/generated/suite-inputs.json` and require
  registry, suite, file-input, input-use, and contract fields to remain
  identical. A1c runtime, suite behavior, coverage policy, and normative
  standards remain unchanged.
- A1b claim schema v4 resolves current coverage requirements from stable
  subjects, so this freshness repair does not require rewriting authored
  attestations. A1C-007 retains the separate product/design question of whether
  A1c should preserve global suite-input invalidation.
- Commit `36de9b23b51072e7488672bcb7ccd6ed6b5a53cd` is unpushed and owned only by
  `main`. The user explicitly authorized its rewrite after identifying its
  missing rationale body. The original tip is protected at
  `refs/recovery/pre-a1c-scaffold-rewrite-20260829` until the corrected boundary
  is verified.
- Regeneration changed only `repository_index.digest`; registry, suite,
  file-input, input-use, and contract fields remained identical. Generated
  freshness, plan structure, diff hygiene, the three focused suites, all
  registered declarative suites, and every retained Bash checker passed.
