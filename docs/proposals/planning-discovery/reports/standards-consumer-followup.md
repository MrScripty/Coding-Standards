# Bounded Consumer Follow-up

Examined Engine revision `proposal-revision:sha256:9421465aaed112d9538bc6fd3f3bdb7a52bfe37e84f1f9ab05ff56f11b385990`, preserving the original independent review. Additional missing relationships concern newly registered Planning scopes; this audit does not repair unrelated existing graph gaps.

| Source policy | Consumer and scope | Relationship | Actual consumption |
| --- | --- | --- | --- |
| `workflow.planning.lifecycle-authority` | `workflow.planning.discovery` / Preserve One Source Of Decision Authority | normative-consumer | Visual remains provisional, with canonical plan authority governing agreed decisions. |
| Same | `templates/PLAN-TEMPLATE.md` / whole artifact | template-projection | Plan, milestone, and final status fields use Planning lifecycle states. |
| Same | `workflow.implementation` / State And Findings | normative-consumer | Uses Implemented, Verifying, and Accepted evidence transitions. |
| Same | `prompts/implement-plan.md` / whole artifact | prompt-projection | Checks plan lifecycle before reusing admission selection. |
| Same | `profile.workflow.concurrent-plan-integration` / Proposal Contract | normative-consumer | Records the intended resulting plan state under Planning authority. |
| Same | `planning-consolidation` / whole suite | enforcement-suite-projection | Enforces the lifecycle vocabulary, unfinished milestone states, and Accepted acceptance constraints. |
| `workflow.planning.repository-isolation` | `templates/PLAN-TEMPLATE.md` / Repository Isolation | template-projection | Projects conditional isolation fields, owner/terminal context, and plan-created worktree evidence. |
| Same | `prompts/implement-plan.md` / whole artifact | prompt-projection | Applies material isolation and retains the governed cleanup handoff. |
| Same | `profile.workflow.concurrent-plan-integration` / Proposal Contract | normative-consumer | Conditional branch/worktree source, target, visibility, and cleanup handoff. |

Isolation relationships preserve Commit's ownership of mechanisms and cleanup authority; they concern Planning's governed context and handoff.

Planning's **Acceptance Claims**, **Concurrent Work**, **Artifact Model**, and **Concurrent Integration Routing** have no registered policy-unit scope in this candidate. Their direct consumption must be disclosed as outside the registered-unit coverage audit; do not invent policy IDs or claim their normative content was removed.

Inspected registered Architecture authority/composed-design admission, Code Design simplicity/complection, and Contracts equality/invariant/proof-lifetime scopes. Discovery's conditional instruction to apply routed standards does not reproduce those specific tests. Broad hyperlinks and similar vocabulary alone justify no additional relationships.

Evidence: exact candidate reads of these consumers and `policy-impact` declarations; accepted-base `planning-consolidation.toml`, `plan_contract.py`, and `test_plan_contract.py`, including invalid-three-state and Accepted-state checks. The three handoff relationships identified in the first report remain required. Final revised graph confirmation is pending.
