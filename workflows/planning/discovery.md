# Discovery And Design

**Standards metadata**

- ID: `workflow.planning.discovery`
- Role: `workflow`
- Level: `MUST`
- Applies when: Material uncertainty about user intent, behavior, constraints, feasibility, or design must be resolved before implementation planning or material replanning.
- Does not apply when: The intended outcome and applicable design decisions are already clear and supported; a brief confirmation may still be useful.
- Requires: `workflow.planning`
- Specializes: `none`
- Verification: Focused decision fixtures and review of whether discovery produces a challengeable, evidence-backed direction without granting implementation authority.
- Canonical owner: `workflows/planning/discovery.md`

## When Discovery Is Substantial

Discovery is substantial when resolving a material decision requires developing and revising a shared understanding across multiple questions, alternatives, or constraints. A decision is material when its answer could change the intended behavior, design direction, scope, or acceptance criteria.

Assess this as the discussion develops. When answers materially change other open questions or earlier design choices, use the substantial-discovery procedure.

## Discover The Intended Outcome

Start from the person, caller, or workflow the change serves and the result they need. Ask what a suggested mechanism is meant to enable or prevent. Establish whether it is a firm choice, a preference, an example, or a hypothesis to investigate; do not silently weaken an explicit requirement or promote a suggestion into one.

Choose questions from the current uncertainty and adapt them as answers and evidence arrive. Use concrete examples, boundary cases, failure situations, and counterexamples to reveal missing invariants. Ask what would make a technically correct implementation wrong for the intended use. Reconcile contradictory answers rather than selecting whichever is easiest to implement.

Keep these kinds of information distinguishable, in whatever concise representation serves the discussion:

- User intent: the desired outcome, supported workflows, and behavior that must or must not occur
- Observed behavior: what the current system demonstrably does, with relevant evidence
- External constraints: limitations or obligations imposed by the environment, interfaces, supported consumers, or other authorities
- Preferences: negotiable priorities whose strength and tradeoffs are understood
- Hypotheses: unverified beliefs about needs, behavior, feasibility, or an approach
- Decisions: choices made by the appropriate person or owner, with their scope and material reasons

These distinctions do not require six documents or a fixed schema. Keep open questions visible without making the person supply implementation details the agent can investigate.

## Investigate What Can Change The Design

Inspect the relevant code, contracts, callers, tests, and operating conditions. Identify what is observed, what is promised, and what is merely an incumbent implementation choice. Existing code is changeable: consider refactoring, replacement, consolidation, or deletion when that better serves the intended outcome, subject to actual compatibility and lifecycle obligations.

Verify material technology and API assumptions using the relevant version and authoritative documentation, plus a bounded real observation when required by [Planning's acceptance guidance](../planning.md#acceptance-claims). Report what the evidence establishes, what remains unknown, and which design decision it can change. Do not expand implementation around an untested assumption that could invalidate it.

## Compare Meaningful Alternatives

When the design is not obvious, compare materially different approaches against the same intended outcomes and constraints. Include a simpler approach, a change to the existing structure, or declining an unnecessary guarantee when any is credible. Do not create decorative alternatives or assume that the current design, a fashionable mechanism, or the smallest diff must win.

Consider the consequences relevant to the task: usability for people and software agents; responsibility and state ownership; lifecycle and failure behavior; resource use; likely changes; inherent and introduced complexity; and demonstrated opportunities for reuse. Explain what each approach makes easier or harder and where the evidence is weak. Select only relevant criteria and apply the canonical [Architecture](../../topics/architecture.md),
[Code Design](../../topics/code-design.md), [Contracts](../../topics/contracts.md),
and other routed requirements rather than duplicating their tests here.

Surface behavior implied by an approach during the discussion. Examples include new retention, recovery, compatibility, permissions, background work, or operating obligations. Distinguish behavior necessary to meet the agreed intent from an optional extension. A useful consequence is not automatically a requested requirement; bring consequential additions to the person before including them as committed plan scope.

## Keep The Main Agent In The Conversation

The main agent owns the conversation, synthesis, and understanding of what is agreed. It stays responsive while research proceeds, including when the person is speaking by voice. It should ask the next useful question, explain findings, and explore implications without making the person wait for unrelated investigations.

For substantial discovery with independent research questions, delegate bounded investigations concurrently. Give each research agent its question, relevant current intent and decisions, evidence expected, scope limits, and the finding or uncertainty that ends the investigation. Apply [Planning's Concurrent Work ownership rules](../planning.md#concurrent-work); read-only research does not gain implementation or integration authority.

Research agents return useful findings promptly, with sources, limits, and implications for the current design. They do not wait to produce a comprehensive report when an earlier finding would change the conversation. The main agent need not wait for every agent before discussing a usable result. Block only the decision that genuinely depends on missing evidence and continue independent discussion or work.

When direction changes, tell affected agents what changed. Reconcile results against the current intent before using them; an accurate finding about an abandoned direction may no longer support the decision. Bring findings that challenge an agreed decision back to the person rather than silently redefining the agreement.

If concurrent agents are unavailable or cannot operate independently, state the limitation and use bounded serial investigation while preserving conversational continuity as far as the environment permits. Do not claim concurrency that did not occur. Do not create branches, worktrees, or a concurrent-integration protocol merely because research agents participate.

## Maintain A Local Visual Document

For substantial discovery, assign a separate visual-document agent as the single writer of an evolving local HTML and CSS document. Maintain it during the discussion so the person can inspect and challenge the current understanding, rather than receiving a polished visualization only after the decisions are made.

The main agent supplies the current synthesis, evidence, open questions, and decision status. The visual-document agent turns that into a readable, attractive shared picture and updates it when meaningful information changes. Research agents report to the main agent; they do not independently rewrite the shared design or its agreed status.

Choose the presentation for the domain and the question. Use workflows, interaction examples, state or ownership views, comparisons, sketches, or other visual forms where they clarify the design. Show the relevant intended behavior, candidate alternatives, evidence, unresolved questions, decisions, and tradeoffs. A universal architecture diagram, fixed dashboard, or mandatory set of panels is not required.

Make proposed, agreed, uncertain, and superseded material visibly distinguishable. State the document's provisional purpose and current update context. Preserve enough source links and rationale to make consequential claims traceable, without reproducing the entire research record. Do not make a visual look settled merely because its layout is complete.

The main agent owns synthesis and the record of human decisions. The visual-document agent may clarify presentation but must return substantive ambiguity or disagreement for resolution. Findings that would change an agreed design must be discussed with the person before the visual represents that change as agreed. After a direction change, reconcile or retire stale alternatives and evidence visibly.

Keep the document local unless publication or sharing is separately authorized. It must remain useful to review without introducing a hosted service, backend, or persistent orchestration system solely for discovery.

A small, clear task may use a concise inline explanation instead of a separate visual artifact. If a visual-document agent is unavailable, state that limitation and have the main agent maintain the local document serially when feasible. If the environment cannot create or display local HTML, provide a reviewable text or supported visual equivalent and identify the limitation. The fallback does not justify claiming that a live visual document exists.

## Preserve One Source Of Decision Authority

During discovery, the visual is a provisional discussion aid, not an implementation plan or an independent decision maker. Once an implementation plan or durable ADR owns a decision, make the visual derive from or link to that canonical source and label any remaining proposals separately. Reconcile disagreements at the owning source; do not maintain competing authoritative versions in the visual and plan.

Retain or retire the visual according to its continuing review value. Keeping it does not create a new mandatory artifact lifecycle or require every future plan change to produce a separately authored visual narrative.

## Explain Back And Enter Planning

Before finalizing an implementation plan, explain the proposed direction in terms the person can challenge. Cover the intended behavior and representative workflow, important invariants, material consequences that were not explicit in the original request, the selected tradeoffs, and unresolved uncertainty. Explain why the approach serves the underlying need and where evidence or a changed assumption would cause reconsideration.

Invite correction on those consequential points. Use the existing conversation and explicit decisions; do not demand ritual approval of facts already settled or impose a fixed questionnaire. Resolve material misunderstandings before presenting the direction as agreed. When the person is unavailable, preserve the uncertain point and continue only work whose decisions it cannot change.

If writing the plan reveals a material new design choice or consequence, return it to the conversation before finalizing. Do not silently resolve it in plan prose or present the addition as previously agreed.

Apply [Planning's written-plan criteria](../planning.md#when-a-written-plan-is-required) after this discovery. If a written plan is needed, transfer the agreed outcome, constraints, decisions, acceptance claims, and meaningful development boundaries into its canonical fields. Keep detailed evidence in linked reports and durable architecture decisions in their owning ADRs. Do not turn the whole conversation into plan narration or promote tentative visual content into binding decisions.

The plan explains how its actual design satisfies applicable standards. Link to the canonical requirements and record the decisions and evidence they caused; copying a standards checklist is not a substitute for applying it. Preserve [Planning's explicit plan admission and implementation authorization
rules](../planning.md#explicit-plan-admission).

Discovery ends when the intended behavior and chosen approach are sufficiently understood to plan or perform the bounded change, and remaining uncertainty has an explicit disposition. Do not require complete knowledge of every possible future use. Reopen the relevant discussion when new evidence changes intent, authority, scope, design, risk, or acceptance meaning.
