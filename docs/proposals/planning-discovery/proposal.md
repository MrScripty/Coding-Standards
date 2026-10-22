# Planning Discovery Standards Proposal

**Status:** Applied through the Standards Engine to local `main`, commit `dcc56f26e884ade260770beceba2501d3746200d`.

**Date:** 1 October 2026

This proposal makes conversational discovery the opening phase of Planning when material intent or design questions remain. The agent develops an understanding of the intended behavior with the person, investigates what can change the design, compares meaningful alternatives, and explains the emerging direction before converting it into implementation work.

Substantial discovery depends on how much shared understanding must be developed and revised together. It uses bounded concurrent research and a separate writer for an evolving local HTML and CSS document when those capabilities are available. Planning retains implementation-plan lifecycle and admission authority; Architecture, Code Design, Contracts, Verification, Commit, and concurrent integration retain their existing ownership.

The wording below is a retained proposal record of the Engine's accepted content. The canonical standards are published in the commit above. The [source draft](source-draft.txt) and [intent and review record](intent-and-review.txt) preserve the original recommendation, the user's subsequent definition, the accepted corrections, and the evidence limits.

## Proposed Changes

1. Expand Planning applicability to material intent and design uncertainty, add discovery before written-plan criteria, preserve provisional artifact status, and discuss meaningful development boundaries.
2. Add `workflow.planning.discovery` at `workflows/planning/discovery.md`, with Planning as its required owner.
3. Add a conditional discovery entry to Implementation's Before Editing procedure.
4. Register discovery in the executable Router vocabulary and rules, with its row in Conditional Details and a corresponding Planning selection condition.
5. Update the Planning Prompt to enter discovery and keep instructions about plan milestones, lifecycle, and artifact placement conditional on a required written plan.

The candidate also includes policy registrations, explicit semantic revisions, identified consumer relationships, decision provenance, and proposed application exposure. It preserves the current implementation-plan states and admission operations.

## Planning Changes

### Applicability

Replace the two applicability fields in `workflows/planning.md`:

```markdown
- Applies when: Material uncertainty about intended behavior or design must be resolved, or work requires sequencing, shared decisions, migration, delegation, or acceptance across multiple boundaries.
- Does not apply when: A bounded local change has a clear agreed outcome, an obvious write set, a regression check, and an acceptance path, with no material uncertainty that could change those decisions.
```

### Discovery Opening

Insert this section immediately before When A Written Plan Is Required:

```markdown
## Discovery Before Implementation Planning

Begin with the intended outcome and the facts needed to choose a suitable design. When material intent, behavior, constraints, or design choices remain unresolved, use [Discovery And Design](planning/discovery.md) before writing the implementation plan. Discovery is the opening phase of this workflow; it is not an approved implementation direction.

Use an adaptive conversation supported by bounded investigation. Establish what the person is trying to achieve, distinguish firm requirements from suggestions and hypotheses, inspect current behavior and technical feasibility, and make consequential alternatives and implied behavior visible. Explain the emerging design back to the person before converting it into implementation work.

Do not treat a suggested mechanism, the current code, or the first plausible architecture as the objective. Apply the routed standards to the actual design decisions; a plan that merely lists standards does not establish that its design meets them.

Keep the effort proportionate. A small, clear task may need only a brief exchange and a concise explanation. Do not manufacture uncertainty, a questionnaire, a written plan, or an approval ceremony when the outcome and acceptance path are already clear. Conversely, the bounded-local exclusion does not apply merely because a proposed patch is small when its intended behavior remains materially unclear.

For substantial discovery, keep the main agent available for conversation while research agents investigate independent questions and a separate visual-document agent maintains the local shared picture. Follow the detailed procedure for ownership, unavailable capabilities, and the transition to canonical planning artifacts.
```

### Written Plan Criteria

Resolve material uncertainty before applying the bounded-local written-plan exclusion. Preserve the existing coordination triggers:

```markdown
## When A Written Plan Is Required

After resolving material intent and design uncertainty through discovery, apply
the bounded-local exclusion before the written-plan triggers. A change
with a clear objective, exact write set, regression check, and acceptance path
may proceed directly even when it touches a public, generated, persistence,
process, language, or user-interface boundary. State its write set inline; an
exact write set does not require a plan artifact.

Create a written plan when the change introduces material sequencing,
independently owned contract, migration, coordination, rollout, risk, or
acceptance complexity that must remain stable during implementation. A boundary
or file category alone does not satisfy this condition. Parallel work requires
a plan only when ownership, dependency, integration, or stale-state coordination
is material.
```

### Provisional Artifacts And Lifecycle

Add the provisional-artifact clarification before the existing lifecycle table:

```markdown
## Lifecycle

Discovery notes, candidate designs, and visual documents are provisional and do not acquire Planned status by being written. Planned continues to mean approved direction. Do not authorize implementation from a discovery artifact or add a discovery state to the implementation-plan lifecycle solely to store a discussion.

| State | Meaning |
| --- | --- |
| `Planned` | Approved direction; implementation has not started. |
| `Active` | The current phase or slice is being implemented. |
| `Blocked` | A named dependency or required fact prevents progress. |
| `Implemented` | Source work is complete; objective acceptance is pending. |
| `Verifying` | Objective-level acceptance is running or awaiting environment. |
| `Accepted` | The named acceptance evidence passed. |
| `Deferred` | Work is intentionally excluded with owner and revisit trigger. |
| `Superseded` | A newer binding decision or plan replaces this item. |

`Implemented` is not complete. `Accepted` requires every objective acceptance
claim to be satisfied.

Exactly one current phase is identified. Multiple independent milestones may be
implemented, but the active plan still names one next integration slice.
```

### Development And Integration Boundaries

Append these paragraphs to Repository Isolation In Written Plans. Commit continues to own the mechanisms:

```markdown
Discuss material development and integration boundaries before implementation. Explain what coherent outcome each boundary makes visible or reviewable, what evidence supports it, and which findings would reopen the design. Where branches or merges serve that purpose, identify their intended role and integration points using Commit's [Branch And Worktree Applicability](commit.md#branch-and-worktree-applicability),
[Governed Branch Context](commit.md#governed-branch-context), and
[Integration Mechanism Selection](commit.md#integration-mechanism-selection) rules.

These boundaries provide visibility into development and useful opportunities to reconsider direction. They do not require a branch per milestone, a merge per slice, a fixed commit count, or a particular history topology. If one serial change provides sufficient visibility and acceptance, say so. Commit retains authority over the actual branch, worktree, merge, history, and cleanup mechanics.
```

## Discovery Procedure

Create `workflows/planning/discovery.md` with this complete proposed content. The substantial-discovery definition and assessment sentence reproduce the user's wording verbatim.

```markdown
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
```

## Implementation Entry

Replace the Before Editing section of `workflows/implementation.md` with the following. Its new conditional link makes discovery reachable through an ordinary implementation request:

```markdown
## Before Editing

1. Inspect repository status and preserve unrelated work.
2. Identify one coherent behavior or contract change.
3. Declare the exact write set and acceptance evidence.
4. Resolve overlapping dirty work or ambiguous verification before editing.
5. Read routed standards and directly affected source context.

Before choosing implementation work, resolve material uncertainty about intended
behavior, constraints, feasibility, or design through Planning's
[Discovery And Design](planning/discovery.md). A small proposed patch does not
establish a clear outcome. Discovery may conclude with a bounded change and an
inline write set; it does not itself require a written plan or authorize
implementation.

When a written plan governs the change, consume
[Planning's admission decision](planning.md#explicit-plan-admission). Bind the
task to one canonical repository-relative `plan.md` path and operation.
A human follow-up may reuse an unambiguous prior selection after current
repository state, plan lifecycle, and authority are checked. Obtain clarification
when that selection is missing or ambiguous. Machine interfaces retain their
explicit argument requirements.

Use the Concurrent Plan Integration profile's revision, stale-state,
compatibility, and reconciliation decisions when its actual applicability
conditions hold. Follow Planning's written-plan applicability: material sequencing,
independently owned contracts, migration, coordination, rollout, risk, or
acceptance complexity requires a plan when it cannot be held unambiguously in
the task. A bounded coherent change can state its exact write set inline.
```

## Router Selection

Replace the Routing Procedure section in `STANDARDS-ROUTER.md`:

```markdown
## Routing Procedure

1. State the requested outcome and affected artifact.
2. Select workflow modules for the activities being performed. Include Planning
   and its discovery detail when material intent or design uncertainty remains,
   even when the proposed implementation is bounded. Keep ordinary uncertainty
   reduction separate when the intended behavior and design are already clear.
3. Select application, boundary, and language profiles from actual repository
   facts.
4. Select topics only when the concern is affected.
5. Follow each selected module's `Requires` metadata.
6. Confirm common exclusions.
7. If a required fact is unknown, report unresolved routing instead of
   selecting a convenient default.
```

Replace the Planning selection condition in Workflow Selection and add the discovery row to Conditional Details:

```markdown
| Condition | Select |
| --- | --- |
| Resolve material uncertainty about intended behavior or design, or coordinate material sequencing, migration, rollout, risk, or acceptance complexity | [Planning Workflow](workflows/planning.md) |
| Material user-intent, behavior, constraint, feasibility, or design uncertainty must be resolved before implementation planning or material replanning | [Discovery And Design](workflows/planning/discovery.md) |
```

Add `workflow.planning.discovery` to the existing `routing.details` enum set at semantic revision 4, preserving the other values. Add the corresponding conditional rule and extend Planning's rule to include that detail. The Engine owns the Markdown and executable projections together.

The new discovery rule tests whether `routing.details` contains `workflow.planning.discovery`. Planning is selected when `routing.activities` contains `planning` or that discovery detail is selected. The new procedure requires Planning, preserving its prerequisite closure. Ordinary `uncertainty-reduction` does not automatically select discovery.

## Planning Prompt

Replace `prompts/planning.md` with:

```markdown
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
```

## Candidate Verification

The current Engine candidate passed exact readback checks for the user's two sentences, all eight discovery sections, Planning's lifecycle table and explicit admission procedure, the concurrent integration boundary, Implementation's discovery entry, conditional prompt instructions, registered routing, and the requested Conditional Details placement.

Five initial route probes passed against the submitted wording:

| Supplied scenario facts | Planning selected | Discovery selected |
| --- | --- | --- |
| Clear bounded repair | No | No |
| Isolated API research with otherwise settled direction | No | No |
| Small feature with material uncertainty | Yes | Yes |
| Discovery detail without a planning activity | Yes | Yes |
| Large implementation with settled direction | Yes | No |

Each probe uses explicit supplied facts. They verify route selection and required closure; they do not prove that an agent will infer those facts correctly or conduct the intended conversation. No probe selected concurrent plan integration merely from research participation.

The initial [verification record](verification.json) and [candidate content](candidate-content.json) preserve the submitted readback. The final [candidate verification](reports/candidate-verification.json) records nine application checks and all sixteen discussion scenarios, with their explicit limits. [Accepted application verification](reports/accepted-application-verification.json) confirms all five adopted artifacts and the complete seven-module required closure through the application-purpose Interface after publication.

## Application Result

The exact reviewed revision `13906993f25ac027f2a6be4e9a9aac531b30bad56d3acbb64afa163ab093737a` resolved all 61 obligations before acceptance:

| Completed work | Count |
| --- | --- |
| Consumer reviews | 30 |
| Coverage audits | 18 |
| Supporting content impact reviews | 10 |
| Whole artifact normative impact dispositions | 3 |

The initial [pending work record](pending-work.json) preserves the earlier 55-obligation draft. Independent review identified thirteen additional semantic relationships for discovery handoff and Planning lifecycle/isolation consumers; those declarations produced the final 61-obligation inventory. The [resolution request](resolution-request.json) preserves every final evidence-backed disposition and audit claim.

The [independent Standards review](reports/standards-final-review.md), [independent Spec review](reports/spec-final-review.md), and [application and consumer review](reports/application-and-consumer-review.md) accepted the exact revised content and scoped relationships. All eighteen proposal policy units have current Engine audit receipts in accepted authority. Other library coverage is outside those scoped claims; the unchanged Verification acceptance-paths receipt now requires renewal because its reviewed consumer content changed.

The required scenarios in the [intent and review record](intent-and-review.txt) cover a clear repair, a suggested mechanism masking another need, isolated difficult research, coupled questions in a small feature, a large settled implementation, changing answers, challenged decisions, implied guarantees, stale findings, unavailable capabilities, read-only research, provisional authority, discovery-only prompt use, detail-only routing, and development boundaries.

The Engine's complete verification checkpoint passed before publication. Static prose review and routing checks establish their stated properties; actual downstream tasks are still needed to establish improved discovery behavior. The preexisting unreviewed concurrent-integration application profile retains its previous qualification boundary.

The [application result](application-result.json) records the applied commit, durable publication receipt, accepted readback and checkout observation. The Engine published local `main` while preserving all 82 preexisting staged paths, unchanged index bytes and unchanged working files. The checkout remains at predecessor content with nine overlapping publication paths classified as conflicted; it was not refreshed. Remote publication is outside this application.

The [proposal state](proposal-state.json) preserves the applied workflow handles. [The initial request](request.json), [placement correction](placement-revision-request.json), [coverage publication request](coverage-publication-request.json), [consumer correction](consumer-revision-request.json), [review request](review-request.json), and [apply request](apply-request.json) preserve the exact submitted inputs.
