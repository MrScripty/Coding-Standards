# Authoring Guide: Positive Guidance and Decision Provenance

**Guide revision:** 1
**Status:** Proposed content migration; implementation is gated on the code plan's acceptance
**Prepared:** September 23, 2026
**Repository baseline inspected:** `MrScripty/Coding-Standards@366c1d90a24bbfb50973f62b155a5f3396c0f107`
**Required predecessor:** [Purpose-Separated Standards Engine implementation plan](../plans/purpose-separated-standards-engine/plan.md)
**Audience:** Standards authors and reviewers; authoring-only material
**Normative status:** This guide proposes changes. It is not an already-published replacement for Core, Router, or their owned requirements.

## 1. Purpose and sequencing

Use the accepted Engine to turn the standards into concise, affirmative, broadly applicable operational guidance. Keep implementation examples supplementary and retrieve them only when relevant. Preserve the evidence and reasoning behind standards in revision-bound decision provenance available to standards authors and reviewers.

The sequence is **code capability → code acceptance → Engine-mediated content migration → real-world effectiveness evaluation**. The code plan may use this guide's prospective practices as its user-approved task contract without first editing the published standards. This guide begins execution only after the Engine can perform all required content operations and enforce the agreed purpose boundary.

There is one standards authority. Application and authoring interfaces provide different views of that authority, not competing versions of the rules.

The intended improvement is to devote ordinary agent context to correct actions, useful conditions, and positive examples. Whether that improves model behavior is evaluated in downstream work. Content filtering can control what the Engine supplies; it does not establish that a model never considers a behavior, erases prior context, or changes its training memory.

## 2. Content classes and authoring responsibilities

| Content | What it owns | Normal use |
| --- | --- | --- |
| Operational standard | Applicable requirements, correct decisions/actions, preserved invariants, meaningful exceptions, and acceptance conditions. | Included when the actual task makes it applicable and its application exposure has been reviewed. |
| Supplementary reference | A correct implementation example or explanatory aid for a selected language, framework, environment, or technical condition. | Optional, specifically retrieved; it adds no normative obligations. |
| Operational prompt or template | A convenient projection of selected workflow requirements and links to their canonical owners. | Included only after its wording and dependencies are reviewed; it is not a second policy authority. |
| Decision provenance | Origin, evidence, assumptions, alternatives, historical failures, trade-offs, uncertainty, and reconsideration conditions. | Available to standards authors/reviewers; excluded from application reading. |

Exposure and normative role are separate. A normative authoring workflow may be relevant only to standards maintainers. A reference document may still be unsuitable for ordinary use if it contains historical failure narratives. A read-only standards review may need authoring provenance, while a code review in an adopting project generally needs operational standards.

The operational rule must be sufficient to apply correctly. Essential preconditions, exclusions, severity, authorization, and failure behavior remain available to the applying agent. Historical reasons for selecting them are the material moved to provenance.

## 3. Prospective generic practices

These identifiers are guide-local labels for planning and review. Reuse actual canonical policy IDs when editing the corpus; the labels do not create another standards registry.

### G1 — Generality follows technical conditions, not the motivating project

Write rules around a general responsibility, invariant, decision, or evidence need. Select applicability from observable conditions such as shared mutation, external contracts, durable state, or user-visible behavior.

Use a motivating project as evidence for the rule's reasoning. Keep its repository name, vendor choices, incidental dimensions, particular bug, and file layout in authoring provenance or a clearly scoped reference. A requirement should remain meaningful after those details are removed.

Where the existing rule already covers the situation, improve its wording, routing, or supplementary help rather than creating a duplicate. A conditional language or boundary profile is appropriate only when it owns a real specialization; broad applicability does not require every rule to apply to every project.

**Editorial test:** Can an unrelated project with the same relevant technical condition apply the requirement without knowing the original incident?

### G2 — Express the correct decision and preserve its force

Prefer direct formulations that state the condition, required action, preserved property, and completion criterion. Use concrete verbs and the owning concern's vocabulary. Keep mandatory obligations mandatory and conditional recommendations conditional.

For example, a generic operational direction can be expressed as:

> Retain ownership of asynchronous work through its required completion, cleanup, and result publication.

This is candidate policy language, not a framework recipe. A demonstration of how to satisfy it in a specific runtime belongs in a separate reference.

Positive language is not a lexical rule. Factual exclusions, protocol-defined negative outcomes, exact external quotations when necessary, and logically essential boundaries may remain. Review meaning rather than counting words such as “not,” “never,” or “unless.” A grammatical rewrite that drops an exception or weakens authorization is a substantive defect.

Avoid replacing a precise restriction with vague encouragement. Express the allowed decision space clearly enough that the agent can choose a correct action without reconstructing a catalog of rejected approaches.

### G3 — Separate application knowledge from maintenance reasoning

Place historical failure narratives, rejected approaches, comparative arguments, and the origin of a standard in its decision provenance. Retain correct examples in separately classified reference material. Keep ordinary rule bodies focused on what an applying agent needs now.

The graph associates these records with their actual owners. Prerequisite relationships select required guidance; supplementary relationships provide optional help; provenance relationships support authoring review. A descriptive association does not create a reading prerequisite or a normative dependency.

Application selection includes a complete required closure or identifies the missing qualification. Detailed reads remain purpose-qualified. A positive title does not make an otherwise mixed document ready for application exposure.

### G4 — Retain one owner across guidance, prompts, templates, and examples

Each requirement has one canonical owner. Operational prompts and templates route to it and include only the procedure context needed to use it. Supplementary examples demonstrate the owner's contract without adding unsupported requirements.

When changing a standard, inspect the declared affected consumer relationships and update the material consumers in the same coherent content change. Distinguish an incomplete relationship inventory from proof that no consumer exists. Add a missing semantic relationship explicitly after review; hyperlinks alone are not evidence of semantic ownership.

Allow reference content to be specific while keeping its relationship to the generic rule clear. A reference must state the conditions and scope of the example and preserve the required lifecycle, failure, and evidence semantics.

### G5 — Obtain decisive evidence where it can change implementation

Refine existing planning/verification guidance, rather than introducing a second end-to-end requirement:

> Resolve an external-interface or environment assumption that could invalidate the design through the smallest adequate real observation before expanding implementation around it. Continue bounded independently useful work when the unavailable observation cannot change that work's decisions.

Distinguish the observation needed to select a design from the evidence needed to accept the final outcome. Name the owner and executable procedure for a remaining environment-qualified claim. Hardware, credentials, and vendor services are required only when the actual claim depends on them.

For consumer-visible behavior, identify the real producer and consumer and prove the required result through their relevant interface. A preview can establish preview behavior; complete consumption requires evidence of the complete consumer result. Specific format, size, framework, and tool examples remain in references.

### G6 — Keep ordinary repairs inside the current decision boundary

Clarify the existing replanning trigger:

> Repair failed checks within the current slice while its objective, ownership, contract, risk, and acceptance meaning remain valid. Replan when the evidence changes those decisions or shows that the admitted slice cannot deliver its outcome.

A failed test is evidence to interpret, not automatically a new design process. A new file inside an already bounded owner does not itself change the objective. When a finding reveals a shared invariant problem, inspect the affected owner and reachable consumers; finish that inspection when the decision-relevant population has concrete dispositions.

Clarify human–agent task binding separately from machine API arguments. A follow-up may reuse an unambiguous plan selection after current repository state is checked. Machine interfaces retain their explicitly declared argument requirements. This is a substantive policy clarification and must be reviewed as such, rather than described as wording-only cleanup.

### G7 — Match effort and evidence to the actual decision

Build on existing Development Proportionality and Verification guidance:

> Reuse an established mechanism when it satisfies the affected requirements. Reconsider it when evidence identifies a material mismatch in behavior, ownership, safety, compatibility, or cost.

Investigate a named uncertainty with a named decision and stopping condition. Prefer reversible implementation when it is the least costly adequate way to resolve the uncertainty. Record durable reasoning in proportion to its consequence.

Clarify evidence under an existing failing baseline:

> Use evidence that still reaches and distinguishes the changed behavior. When an existing failure prevents that observation, repair the obstruction, supply a focused discriminator, or retain the affected claim as unverified.

Preserve explicit debt dispositions while distinguishing them from acceptance. Unchanged failure counts, names, or source locations are not substitutes for a test that can observe the affected result. Generalize this rule across runners and languages; concrete test-framework demonstrations belong in references.

### G8 — Evolve contracts toward the best supported design

Express compatibility as a consequence of actual consumer and state requirements:

> Select one supported contract that satisfies the current product and deployment needs. Replace superseded contracts when the new design provides a better implementation or user experience, with explicit cutover and retained-state dispositions.

For this repository change, the owner has chosen no backward-compatibility maintenance. That is a project-specific compatibility decision recorded in the implementation plan, not a universal rule requiring every adopting project to break its contracts.

Generic standards should continue to protect actual retained data, recovery obligations, coordinated deployment, and explicit authority. Removing compatibility code and preserving historical bytes are compatible actions. User authorization to replace an API does not authorize unrelated data destruction or rewriting shared history.

### G9 — Treat provenance and effectiveness as evidence with limits

Record what supports a rule and how far that support extends. Separate observations, external requirements, experiments, engineering inference, and owner-selected preferences. An owner's preference can establish a selected design objective without proving that objective improves model behavior.

A new rationale is maintained against the rule revision it actually supports. A factual correction or evidence update can change provenance without changing operational meaning. A material change to a rule or its assumptions receives a corresponding review of the reasoning.

Use the existing effectiveness work to evaluate the resulting guidance in actual tasks. Internal graph validity and prose-review completion establish their named properties, not downstream effectiveness.

## 4. Decision-provenance authoring guide

Write a concise reviewable record rather than reconstructing an imagined historical narrative. Use the Engine's accepted schema and optional fields; the following is a content checklist, not an additional serialization contract.

| Question | Record when material |
| --- | --- |
| What property or decision does this rule protect? | Intended outcome and the technical conditions that activate it. |
| Why was this direction selected? | The rationale and its decision-relevant evidence. |
| What is the basis of the account? | Documented original reasoning, reconstructed history, current justification, or unrecorded origin. |
| How strong and broad is the support? | Observation/inference/requirement/preference distinctions, assumptions, uncertainty, and scope limits. |
| Which alternatives mattered? | Relevant alternatives and accepted trade-offs, including negative examples where informative. |
| What would change the decision? | Reconsideration conditions or later evidence that could justify refinement, replacement, or retirement. |

Preserve precise source attribution when evidence exists. For an external source, record its identity, version/date where meaningful, the property it supports, and a bounded retained excerpt or local evidence artifact when necessary. A URL alone is not a preserved observation. Respect confidentiality and content rights when recording supporting material.

For an older rule with unknown origins, explicitly record the gap. A current review may justify retaining the rule, but label that justification as current rather than claiming it was the original reason.

Keep rejected examples out of application-visible references. Authors and reviewers may use them to establish preservation of constraints and the adequacy of a rewrite. Ordinary application agents receive the resulting operational rule, not the editing debate.

Provenance records do not silently define exceptions. If a condition changes how an agent must apply the rule, that condition belongs in operational guidance or its declared applicability.

## 5. Engine-only migration procedure

### H0 — Confirm the code-to-content handoff

Begin after code claims C1–C10 are accepted. Verify the actual installed purpose-specific catalog and supported versions. Use an authoring-configured client for maintenance. Exercise the handoff's tested operation map; this guide does not invent commands that are not yet implemented.

Required capabilities are complete module/metadata revision, scoped policy revision with stable identities, reference creation/revision, registered prompt/template editing, provenance maintenance, explicit exposure approval/withdrawal, relationship updates, and coherent reviewed publication. Verify a whole-module rewrite preserves or explicitly dispositions existing policy-unit scopes and previously unmapped content.

The handoff also exercises explicit policy-unit registration within an existing standard, both for a module with no registered units and for an owner with established units. Prove registration together with an optional whole-module rewrite, consumer relationships and provenance through reviewed publication and cold readback. Registration preserves existing identities and requires the real coverage dispositions. The [registration correction plan](../plans/existing-policy-registration/plan.md) owns the code capability and its acceptance; a schema entry alone does not satisfy this handoff.

A missing necessary content operation returns to the code workstream as a bounded implementation gap. It is not a reason to bypass the Engine and edit canonical files directly.

H0 also verifies proposal-local registration of tracked fixture and documentation
consumers for policy scopes created in that draft. Use canonical candidate IDs
for their relationships. Registered Markdown skill references are eligible for
controlled authoring without granting source-code edit access. Inspect candidate
application content with authoring `preview_application`, bound to an exact
revision; ordinary application `query_proposal` is intentionally unavailable.
This preview applies the same exposure and dependency checks but does not publish
or certify the content. Refresh the running MCP process and client catalog, then
check the installed interface and these operation schemas before continuing.

### H1 — Inventory one coherent migration boundary

Read the actual canonical owner, its rule scopes, metadata, dependencies, and current exposure state through the Engine. Traverse the relevant declared consumer and support relationships. Identify materially affected prompts, templates, references, routing facts/descriptions, and existing evidence owners.

Inventory all text returned by the selected application view, not merely its principal rule paragraphs. This includes tables, headings, applicability wording, notes, examples, footnotes, and local links. Whole-module eligibility requires reviewing the whole returned module; a clean scoped rule does not establish that the rest of its parent is ready.

Record current meaning and classify the work as wording-only preservation, structural separation with preserved meaning, or substantive policy change. Keep evidence gaps explicit. Stop inventory when the affected owner and reachable consumers have sufficient dispositions for the current change; do not enumerate unrelated projects or the whole repository by default.

### H2 — Prepare the smallest complete content change

Use the existing authoring workflow to revise the operational body, extract reasoning into provenance, and create or revise relevant positive references. Include affected registered prompts/templates and real semantic relationships. Preserve stable policy identities; update heading/locator representation through the Engine. Record intended semantic preservation or the explicit substantive revision.

Review operational rules for preconditions, authorization, lifecycle, failure behavior, exception scope, and acceptance. For meaning-preserving edits, compare those obligations before and after. For substantive edits, state the newly selected behavior and why it is justified.

The Engine generates repository projections and technical bindings. Authors provide the content and semantic decisions, not file paths, copied digests, or manually edited generated outputs.

### H3 — Review the exact candidate and its two views

Obtain an independent material review using the relevant provenance. Confirm generality, directive clarity, sufficient operational meaning, and accurate evidence. Review declaration changes and downstream consumers against the actual graph; a successful graph compile proves structure, not complete discovery or sound policy.

Then inspect what an application client will receive from the candidate using the accepted Engine's validation/testing path. Check complete dependency availability, positive example selection, prompt/template consistency, and separation of authoring-only material. Keep draft content in the authoring workflow until publication.

Approve exposure only for the exact reviewed content and its applicable metadata. A record's presence in a proposal is not application publication. If a content change makes earlier exposure stale, reapprove the new exact content or explicitly withdraw that module and disposition affected routes.

Repair wording or implementation details within the admitted meaning without reopening the entire design. A changed obligation, applicability decision, or exposure contract receives a material re-review.

### H4 — Publish coherently and verify readback

Publish through the existing review/apply workflow. Use its returned continuation for interrupted or uncertain publication. Read the accepted result through both authoring and application interfaces and verify the intended content and relationship behavior.

A consumer path becomes application-ready when every required member is qualified. Optional examples may be omitted until ready. A missing required module remains explicit; partial traversal does not become complete acceptance.

Preserve the historical rationale and original source revision in authoring provenance without retaining a second active negative formulation as policy. References, prompts, and templates consume their canonical owner rather than restating an alternative authority.

### H5 — Continue by owner and evaluate effectiveness

Start with Core, application-relevant Router/fact wording, and the smallest real task's actual prerequisite closure. This creates one usable application path. Continue in owner-coherent groups selected from actual downstream needs; do not require a rewrite of the entire library before proving the first useful path.

Keep authoring-only workflows and historical reports separate. The complete graph and authoring view can remain richer than any application view.

Use the two independent downstream pilots already planned in the effectiveness effort. Prefer unrelated task domains or substantially different technical conditions so the result does not merely fit the motivating repository. Use fresh contexts, comparable model/tool/environment settings, and a reviewer who evaluates the actual artifacts.

Measure accepted behavior, escaped and review-found defects, repair/intervention effort, unnecessary artifacts, and total task cost. Record reading/context size as an explanatory measure, not a quality verdict. Where inexpensive and informative, distinguish positive wording from rationale removal in the comparison. Otherwise describe the measured change as the combined presentation effect. Small pilots provide directional evidence, not a universal cognitive claim.

## 6. Priority and ownership of the intended edits

Review the current owners first; merge improvements into them rather than creating parallel policies.

| Concern | Existing owner to examine | Intended disposition |
| --- | --- | --- |
| Generic direction and positive wording | Core and applicable topic/workflow owners | Preserve obligations; clarify the correct action and move maintenance reasoning. |
| Early real observation and complete consumption | Planning and Verification | Refine timing and decision relevance; reuse existing path/claim guidance. |
| Ordinary repair versus replanning | Planning and Implementation | Make the distinction explicit and update affected prompts/templates coherently. |
| Prior plan selection versus API admission | Planning, Implementation, operational prompts | Separate conversational task binding from explicit machine argument contracts. |
| Existing failing baselines | Verification and Tooling | Clarify whether the evidence still reaches the changed behavior. |
| Conventional mechanisms and proportional effort | Development Proportionality, Tooling, and Core | Replace repeated catalogs of prohibited defaults with conditional reuse and reconsideration rules. |
| Supplementary implementation help | Existing reference owners and selected profiles | Add positively framed examples only when a concrete applicability need exists. |
| Reasoning provenance and purpose selection | Appropriate standards-authoring guidance, Engine content classification, and actual graph declarations | Record genuine reasoning and keep maintenance discovery separate from application prerequisites. |
| Effectiveness | Existing standards-effectiveness effort | Complete pilots and concision review using real outcomes. |

The inspected publication still has mixed maintenance instructions in `prompts/implement-plan.md`; include that surface when revising its owning workflows. The current implementation supports `revise-standard` and other logical edits, but the code plan adds the missing complete supporting-content and exposure workflow. These are specific migration facts, not generic requirements to place into Core.

## 7. Meaning-preservation and content acceptance

A migrated owner is accepted when all applicable claims below are satisfied. Record evidence once in its normal authoring/review records; this checklist is not a new global certification system.

| Claim | Required evidence |
| --- | --- |
| Generic applicability | An independent reader can apply the rule to an unrelated project with the same material conditions. Project-specific history stays in provenance or references. |
| Operational sufficiency | The rewritten rule preserves or explicitly revises its obligation strength, preconditions, exclusions, authorization, failure/lifecycle semantics, and acceptance condition. |
| Positive direction | The normal reading path predominantly supplies correct actions and useful conditions; a lexical ban is not used as the oracle. |
| Separation | Application readback includes only reviewed operational content and selected references/aids. Authoring can retrieve the associated reasoning. |
| Reasoning accuracy | Sources and inference are distinguished; unrecorded history remains explicit; a rationale-only correction does not invent policy change. |
| Graph fidelity | Dependencies, specialization, descriptive support, and actual impact relationships retain their distinct meanings. Missing coverage is not represented as completeness. |
| Consumer coherence | Related prompts, templates, examples, routing wording, and generated projections agree with their canonical owner. |
| Publication integrity | The accepted view matches the exact reviewed candidate; stale bindings and partial publication follow the Engine's declared outcomes. |

The runtime structural checkpoint remains useful, but semantic review and downstream behavior remain independent evidence. Tests of the Engine's exposure mechanism do not certify the migrated prose; prose review does not certify all downstream code.

## 8. Completion and continuing maintenance

Content migration completion means the selected published scope has operationally sufficient positive guidance, relevant supplementary examples, truthful available provenance, coherent consumer projections, and a complete qualified application reading path. Remaining unreviewed modules are named and excluded from claims of corpus-wide readiness.

Complete the effectiveness effort separately when its pilot and review claims are satisfied. A mechanically complete migration can still need wording refinement after real use; such refinement follows the same Engine workflow and evidence boundaries.

For later work, maintain provenance when the reason, supporting evidence, or applicable assumptions materially change. Reuse unchanged reasoning when review confirms it still applies. Keep routine formatting and implementation choices inexpensive. Retire superseded operational text from current authority while preserving useful history in the authoring view.

**This guide changes standards content only after code acceptance. It does not authorize runtime rewrites, direct canonical-file edits, or claims that the migration has already occurred.**

## Source and decision basis

Repository observations use the inspected commit above:

- `tools/standards_engine/README.md` and `contracts/README.md`: existing typed navigation, logical authoring, snapshots, and publication.
- `tools/standards_engine/standards_engine/logical_authoring.py`: current standard, policy-unit, routing, and relationship edit forms.
- `tools/standards_policy_impact/README.md` and `contracts/policy-impact-authoring-v2.toml`: distinct relationship semantics and declared coverage limits.
- `CORE-STANDARDS.md`, `workflows/planning.md`, `workflows/implementation.md`, `workflows/verification.md`, `workflows/development-proportionality.md`, `workflows/tooling.md`: current owners for the proposed refinements.
- `prompts/implement-plan.md` and `templates/PLAN-TEMPLATE.md`: operational consumers requiring coordinated editorial treatment.
- `docs/plans/standards-library-effectiveness/plan.md`: existing downstream-pilot and final-review work.

The positive-context objective, authoring-only reasoning boundary, code-before-content sequencing, and this implementation's compatibility choice come from the user's instructions in this conversation. Their behavioral effectiveness remains a proposition for evaluation, not a historical fact established by this guide.
