# Milestone 3: Bound Authoring Contexts And Final Acceptance

The Engine reconstructs workflow state from one existing immutable revision,
analysis, or readiness handle. No new persistence, identity version, transport
session, or mutable current-context map was added. Association validation and
current-head checks live beside the Engine's native authoring lifecycle.

`propose` and `revise` compose creation/revision with analysis. Missing evidence,
owner decisions, rejection, and recovery stop progression. `review`, `apply`, and
`recover` remain explicit operations. `workflow_status` observes exact bound
state; `resume` deliberately selects the current proposal revision and returns
a draft context. Native authorization and atomic publication guards still apply.

## Observable Interaction Changes

| Scenario | Native/reference path | Focused path |
| --- | --- | --- |
| New proposal through initial analysis, with no snapshot supplied | Capture snapshot, create proposal, analyze revision: 3 calls | `propose`: 1 call |
| Revised proposal through analysis | Revise exact revision, analyze successor: 2 calls | `revise`: 1 call |
| Pending owner decision | Supply explicit submission to analysis | `resolve_workflow` with context and the same explicit submission; no decision is inferred |
| Ordinary lifecycle bookkeeping | Carry/select snapshot, proposal revision, analysis, readiness for different operations | Carry one returned `context`; detailed immutable identities remain inspectable |
| Stale proposal | Identify current head and explicitly select revision | Stale result advertises `resume`; resume returns current draft context without analyzing or reviewing |
| Interrupted application | Retain readiness; invoke native recovery separately | Same context advertises `recover`; another `apply` is refused |

Default discovery contains 15 focused tools, including inspection and historical
proposal reads. `--advanced` exposes all 32 generated native and focused tools.
Native Python and reference CLI operations retain their existing contracts.
The skill teaches explicit facts, authority, evidence, and continuation handling
using the focused tools; advanced administration is documented separately.

## Real Client Walkthrough

The official MCP Python SDK 1.29.1 connects over stdio and validates generated
output schemas. The repeatable harness is
`tools/standards_engine/tests/mcp_workflow_client.py`; its README instructions
keep the optional SDK in a separate environment from Engine dependencies.

The lifecycle walkthrough uses an isolated repository and two server processes:

1. Propose and analyze in one call; explicitly review using real repository
   evidence and three review acceptances.
2. Inject outcome-recording failure after native publication in a test-only
   launcher. Observe recovery-required and refusal of a second apply.
3. Restart the server, reconstruct the same readiness context, and recover.
   Assert that recovery does not publish again; read the accepted exact text.
4. Create and revise another proposal. Assert the old context is stale and
   cannot review; explicitly resume, analyze, review, and successfully apply
   through the normal publication path. Read the revised accepted text.

This complete walkthrough passes with the Engine on Python 3.11.14. The initial
publication/interruption/restart/recovery/stale walkthrough also passed on Python
3.12. A separate Python 3.12 pending-decision walkthrough demonstrates that early
review is refused, then supplies actual evidence and an explicit confirmed
impact disposition through `resolve_workflow` to complete the analysis.

These are actual SDK-client walkthroughs with assertions, not a model-driven
coding session. Earlier milestone SDK walkthroughs cover lookup, vocabulary,
compact reads, and interleaved snapshots. No personal client configuration was
changed. A7 is satisfied within this isolated client acceptance environment.

## Verification And Negative Evidence

- Six durable workflow tests passed on Python 3.12. The subsequently extended
  resolution and terminal-outcome cases were each rerun successfully.
- Invalid handle versions/IDs, mixed context fields, foreign repository records,
  stale revisions, missing authorization, and premature review are rejected.
- Invalid evidence is rejected without advancing context; an explicit
  requires-change disposition offers revision instead of review.
- Native analysis rejection retains the exact revision for inspection.
- Terminal native application and recovery outcomes are preserved directly;
  a regression asserts that secondary status reads cannot obscure them.
- Fresh native navigation, focused navigation, generated-contract, and MCP
  regressions pass on Python 3.12 (40 tests). The additional native readiness
  test exposed a stale consumer-disposition assumption, reproduced identically
  at milestone 2. After correcting its expectation to the actual coverage-only
  obligation, the readiness-composition regression passes. The focused
  navigation/generated-contract/MCP set also passes on Python 3.11 (33 tests).
- Contract compiler tests pass (20 tests). Generated projection checks, focused
  Ruff checks, skill validation, and whitespace checks pass.
- Both Engine environments use the repository's hash-locked dependencies.
  The Engine repository checkpoint passes: 73 suites and 121 checks. Verification
  input projections are refreshed through the Engine after staging new sources.

A4–A8 are satisfied, with fresh A1–A3 regressions. All three milestones are
accepted. Embeddings, semantic search, interpretation models, new fact semantics,
and remote publication remain outside this implementation.
