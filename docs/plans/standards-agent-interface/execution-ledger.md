# Standards Agent Interface Execution Ledger

## 2026-09-05: Implementation Plan Created

**Outcome:** Planned direction recorded; implementation under this plan has not started.

**Request:** Improve focused navigation, explicit-fact discovery/explanations,
and context-bound authoring without embeddings or an interpretation model.

**Inspected evidence:**

- The working-tree MCP transport exposes 19 generated native operations through
  `AgentToolFacade`; it does not yet implement the focused experience.
- `StandardsEngine._route_value` already emits base/rule/dependency causes and
  unresolved questions. Router reads with `include_routing` already expose fact
  definitions. Those are reuse opportunities, not new semantic authority.
- The existing `read` projection includes complete related rows, prerequisites,
  specialization, policy summary, content, and continuations.
- The contract README identifies one JSON shape authority and generated native
  and agent-tool projections.
- The Planning Workflow was read through the Engine's MCP dispatch path against
  an accepted snapshot. The plan follows its current lifecycle/artifact model.

**Write set for this planning turn:** This plan directory and its entry in
`docs/plans/README.md`. Existing implementation changes and the unrelated
proportionality-routing prototype are retained.

**Verification:** Local plan structure, milestone/acceptance coverage, and
relative-link checks; no implementation acceptance claims are satisfied by
writing this plan.

**Commit:** None created by this planning turn.

## 2026-09-05: Milestone 1 Accepted

**Outcome:** Focused navigation and compact exact policy reads accepted.

**Evidence:** [Milestone 1](reports/milestone-1.md). A1/A2 are satisfied; A7 has
real-client navigation evidence and awaits authoring/recovery scenarios.

**Scope:** Included the previously implemented MCP transport and plan artifacts
as prerequisites. The unrelated proportionality-routing prototype is excluded.

**Deviation:** Corrected a test oracle that equated independent snapshot IDs;
production snapshot identity behavior was correct. No domain semantics changed.

**Commit subject:** `feat(standards-engine): add focused agent navigation tools`

## 2026-09-05: Milestone 2 Accepted

**Outcome:** Registered fact discovery and deterministic explanation projection
accepted. A3 is satisfied; no Router or fact semantics changed.

**Evidence:** [Milestone 2](reports/milestone-2.md), 32 passing tests and an
official MCP client walkthrough. Milestone 1 commit: `e9bac84f`.

**Commit subject:** `feat(standards-engine): expose routing facts and explanations`

## 2026-09-05: Milestone 3 Accepted

**Outcome:** One immutable context carries authoring state; Engine-derived
continuations preserve explicit review, exact application, and separate recovery.
All objective acceptance criteria are satisfied. No new context store or identity
version was necessary.

**Evidence:** [Milestone 3](reports/milestone-3.md), including real-client normal
publication, pending resolution, stale revision rejection, cold-process recovery,
and supported Python verification. Milestone 2 commit: `d97e1028`.

**Scope:** Default MCP discovery now exposes 15 focused operations; all 32 remain
available with `--advanced`. Skills use the focused surface. Personal client
configuration and the unrelated prototype remain untouched.

**Finding resolved:** Terminal application outcomes must survive projection even
when a later state read would fail. The wrapper preserves the native outcome
directly, with a regression assertion and real publication/recovery coverage.

**Commit subject:** `feat(standards-engine): bind authoring tools to immutable workflow context`

**Additional fixture correction:** A broadened native review regression failed
identically at Milestone 2 because it requested a nonexistent consumer
disposition. The accepted fixture has only an audit-coverage obligation. Corrected
the test to assert and resolve that obligation without changing production rules.

## 2026-09-05: Client Schema And Continuation Fixes

**Request:** Address hidden authoring schemas and unavailable continuation names
before returning to the separate effectiveness plan.

**Outcome:** Inline nonrecursive input schema references from canonical
contracts, preserving recursive validation. Engine-owned navigation projection
uses focused tool names. Default instructions and unknown-outcome guidance use
context-based recovery; advanced native operations retain readiness guidance.

**Evidence:** [Client follow-ups](reports/client-followups.md), 37 focused
regressions, 20 contract tests, Codex CLI 0.153.4 app-server schema consumption
and same-snapshot route/read, and the 73-suite / 121-check Engine checkpoint.
The local client check starts no model turn. This conversation needs a reconnect
to inspect its final model-visible declarations.

**Commit subject:** `fix(standards-engine): expose authoring schemas and focused continuations`

## 2026-09-05: Preserve Nested Authoring Contracts In Tool Descriptions

**Finding:** The live reconnect proved the inline fix was partial: outer
change-set fields appeared, but nested edits and evidence remained abbreviated
as `unknown`. Focused guidance and navigation continuations were confirmed.

**Change:** Emit the exact canonical input closure in affected authoring tool
descriptions, independently of client type rendering. No schema format, domain
identity, authorization, validation, or persistence contract changes.

**Evidence:** Exact-description schema regression and actual configured Codex
client preservation check; see [follow-up evidence](reports/client-followups.md).

**Commit subject:** `fix(standards-engine): retain nested input contracts in tool descriptions`
