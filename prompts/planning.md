# Planning Prompt

Establish or revise an implementation direction under [Planning](../workflows/planning.md).
Begin with its discovery phase when material intent or design questions remain.
Create or revise a written plan only when Planning's applicability criteria require
one. Keep this operation within planning scope.

1. Read Core and route the task's actual facts through Router.
2. Establish the intended outcome and distinguish firm choices, preferences, and hypotheses. Follow [Discovery And Design](../workflows/planning/discovery.md) for unresolved intent, behavior, constraints, feasibility, or design questions. Keep the main agent responsive to the person while bounded research agents investigate independent questions; for substantial discovery, use a separate visual-document agent to maintain the provisional local HTML and CSS view.
3. Inspect repository state, affected code and contracts, and material technology or API assumptions. Compare meaningful alternatives when warranted, including changing the existing structure. Surface implied behavior and explain the proposed outcome, consequences, tradeoffs, and uncertainty back to the person before treating the direction as agreed.
4. Select observable acceptance claims from that understanding. Apply Planning's written-plan criteria and use the [Plan template](../templates/PLAN-TEMPLATE.md) when a written plan is needed. Keep provisional discovery separate from approved plan lifecycle and implementation authority.
5. Identify an early real observation for any external-interface or environment
   assumption that could invalidate the design. Separate that design decision
   from final acceptance, and name the owner/procedure for remaining evidence.
6. Discuss meaningful development and integration boundaries up front; link
   branch and merge choices to [Commit](../workflows/commit.md). When a written
   plan is required, select coherent milestones and slices. Split for material
   acceptance, risk, dependency, conflict, rollback, or feedback value.
7. Bind review to material content. When a written plan governs the work, record
   lifecycle changes with their causing outcome or evidence. Commit owns Git
   topology and commit boundaries.
8. Bound delegation, concurrency, and repository isolation by their actual
   applicability; preserve the owning workflows' authority and cleanup evidence.
9. Identify the deciding oracle for each claim. Use established dependencies
   for difficult semantics when they satisfy the affected requirements.
10. Record composed-design review applicability and, when applicable, the
    current Architecture-owned artifact probe. Review a material replacement anew.
11. Set replanning triggers for changed objective, ownership, contract, risk,
    sequencing, or acceptance meaning. Keep ordinary repairs inside a valid slice.
12. For systemic findings, bound the canonical owner and reachable consumers;
    record dispositions and a stopping condition under Planning.
13. When a written plan is required, put current decisions in the plan, findings
    in issues, and detailed evidence and history in their linked reports and
    ledger. Otherwise, retain the agreed outcome, consequential decisions, and
    acceptance path in the conversation or existing task record.

Keep current-format, identity, compatibility, migration, and allocation authority
with their actual owners. Follow the applicable Contracts and Architecture
requirements for independent change and invalidation.

Resolve missing or contradictory authoritative facts before admitting dependent
work. Continue bounded independent work where that uncertainty cannot change
its decisions.
