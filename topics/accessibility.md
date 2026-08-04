# Accessibility

**Standards metadata**

- ID: `topic.accessibility`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes a user-facing task, interaction, content, control, status, notification, or accessibility claim.
- Does not apply when: The change has no user-facing behavior or accessibility claim and cannot affect access to a supported user task.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Accessibility contract decision fixtures plus claim-matched evidence for the selected users, tasks, platforms, modalities, capabilities, and conformance obligations.
- Canonical owner: `topics/accessibility.md`

## Accessibility Authority

Accessibility owns the outcomes required for supported users to perceive,
understand, navigate, operate, and receive the results of user-facing behavior.
Define those outcomes from the product contract and affected user tasks before
selecting an interface mechanism.

An accessibility contract identifies the supported users and tasks, relevant
content and controls, supported platforms, required interaction and perception
modalities, available assistive capabilities, selected conformance obligations,
and evidence needed to establish the claim. Do not infer that contract from the
current interface technology, one input method, one assistive technology, or a
general statement that the interface is accessible.

## Outcome And Modality Selection

Select required outcomes and modalities from actual user, product, platform,
and regulatory or organizational obligations. Visual, auditory, tactile,
pointer, keyboard, switch, voice, and programmatic access are possible contract
dimensions, not a universal checklist. Support for one modality does not prove
equivalent access through another.

An external accessibility standard or conformance level applies only when the
project contract selects its authority, scope, version, target platform, and
evidence obligations. Do not silently select, upgrade, weaken, or substitute an
external standard when those facts are absent.

## Semantic Meaning And Role

Expose each user-facing element's purpose, role, relationships, value, state,
availability, and change through every modality required by the accepted
contract. Derive that meaning from the user task and observable behavior, not
from appearance, event-handler name, current widget, or implementation type.

Use a platform-native mechanism when it satisfies the complete selected
meaning, modality, state, feedback, and lifecycle contract. A native mechanism
is preferred only on that evidence; semantic markup, an accessibility API role,
or a conventional control is not a universal mechanism and does not prove the
outcome by itself.

## Action And Navigation Outcomes

Classify an interaction by its user-visible result. An action changes
application state or performs an operation. Navigation changes the user's
location or active destination. A control that can do both declares the
conditions, resulting state, destination, feedback, and required modalities
for each outcome.

Do not select action or navigation semantics from visual styling, click
handling, a URL-shaped value, or an incumbent element. Do not substitute one
outcome for the other when the required platform mechanism is unavailable.

## Custom Interaction Outcomes

A custom interaction is permitted only when supported mechanisms cannot satisfy
the accepted task and its implementation covers the complete selected role,
state, value, relationships, activation, modalities, feedback, focus or
position lifecycle, cancellation, and failure outcomes.

Support through one event, input method, visual state, role declaration, or
assistive mechanism does not prove another modality or the complete custom
interaction. Missing required capability or evidence is a typed outcome, not
authority to omit behavior or emulate a nearby control incompletely.

## Input Modality Equivalence

For every required modality, define how a user reaches, identifies, activates,
adjusts, cancels, and receives feedback from the interaction. Preserve task
order, state effects, and failure outcomes across modalities where the contract
requires equivalent access. Support through pointer activation, a click event,
or one native control does not establish another input modality.

Keyboard, switch, voice, touch, pointer, and programmatic interaction are
selected capabilities, not mutual substitutes or universal requirements. When
a required modality cannot be supported or established, return its typed
outcome instead of omitting it or treating another modality as sufficient.

## Focus Visibility And Authority

When the selected interaction model has an active position or focus concept,
assign authority for its current target and make that target perceivable through
the required modalities and states. Visibility must remain distinguishable in
the supported environment and must not depend only on color, pointer hover, or
an implementation-specific default unless the accepted contract proves it.

Removing, hiding, or moving focus is valid only as part of an owned transition
that preserves task continuity and feedback. Styling, browser defaults, or a
successful focus API call alone do not prove visibility or correct authority.

## Focus Lifecycle

For composite, transient, modal, or dynamically replaced interactions, define
the initial target, movement boundaries, active-order behavior, dismissal and
cancellation, restoration destination, target removal, nested interaction, and
failure outcomes from the user task and supported platform.

A fixed trap, first-control target, Escape binding, return-to-trigger rule, or
DOM-presence check is a possible mechanism, not a generic lifecycle contract.
If the authoritative target no longer exists, resolve the next target through
the selected task lifecycle or return a typed diagnostic; do not silently lose
or guess focus.

## Names And Descriptions

Provide each user-facing control, region, status, and task-relevant item a name
or description sufficient to distinguish its purpose, scope, current target,
and effect through every required modality. Names remain stable enough for task
continuity and update when the represented purpose or state changes.

Visible text, hidden text, platform naming APIs, associated content, and
generated descriptions are mechanisms. A role, icon, position, implementation
identifier, or generated default does not independently establish a meaningful
name. Do not expose internal detail as a substitute for user-task meaning.

## Input Relationships And Instructions

For user input, expose the relationship among the input, its purpose, name,
instructions, units or format, constraints, current value, validation state,
errors, and recovery action through the required modalities. Preserve those
relationships when layout, state, content, or validation changes.

Visual proximity, placeholder content, color, field order, or one assistive
projection does not prove the relationship. If required naming, instruction,
state, or error capability is missing, return a typed outcome rather than
accepting an unlabeled or ambiguously associated input.

## Media Meaning And Classification

Classify media, imagery, icons, animation, audio, and visual or auditory effects
from the meaning and function they contribute to the user task in context.
Informative media contributes content, status, identity, instruction, or
function. Decorative media contributes no task-relevant meaning after the
surrounding context and supported modalities are considered.

Classification is an owned content decision, not a property of file type,
component name, placement, repetition, visual subtlety, or library convention.
Re-evaluate it when content, context, state, or function changes.

## Equivalent Media Outcomes

For informative or functional media, provide the selected users an equivalent
task outcome through every required modality, preserving relevant meaning,
state, timing, controls, and change notification. For decorative media, prevent
the mechanism from introducing misleading or redundant meaning where the
selected platform supports that projection.

Alternate text, captions, transcripts, descriptions, hidden semantics, visible
labels, and adjacent content are mechanisms selected from the media and task
contract. An empty string, filename, icon-library default, nearby visual text,
or successful API attribute does not independently prove classification or
equivalence.

## Accessibility Evidence Claims

Define evidence from each accepted accessibility outcome, affected users and
tasks, supported platforms and modalities, relevant states, failure paths, and
conformance obligations. Select automated, manual, assistive-technology, user,
inspection, or combined evidence only for the claims each method can establish.

Tooling selects and orchestrates lint products, rules, severity, scope, commands,
and schedules. Verification owns evidence kind, environment, execution, and
acceptance meaning. Accessibility owns the user-access claim those systems
consume. A configured plugin, named rule set, zero lint findings, CI execution,
or successful command does not prove a broader accessibility outcome.

## Responsibility Boundaries

Accessibility owns required user-access outcomes and conformance obligations.
Application, frontend, language, and framework profiles own concrete semantic,
interaction, rendering, platform, and assistive-technology mechanisms. Tooling
owns selected lint and automation execution. Verification owns the evidence
plan and acceptance claim. Documentation records durable accessibility
contracts and decisions when they cannot be recovered from implementation and
evidence.

A mechanism such as semantic markup, an accessibility API, keyboard handling,
focus management, captions, alternate text, automated linting, or a manual
assistive-technology check is evidence or implementation only for the outcomes
its selected contract covers. No mechanism, tool, browser, framework, input
method, assistive technology, or passing check independently defines or proves
the complete accessibility contract.

## Typed Outcomes

Return typed `invalid` for contradictory users, tasks, modalities, conformance,
or authority requirements. Return typed `unsupported` when a valid required
outcome cannot be provided by the selected product or supported platform.
Return typed `unavailable` when required users, tasks, platform facts,
capabilities, conformance authority, or claim-matched evidence cannot be
established.

Do not continue by assuming a web interface, a particular external standard,
one input modality, one assistive technology, a conventional lint configuration,
weaker evidence, omitted behavior, or default success.

## Verification

Evidence covers the selected users and tasks, supported platforms, required
modalities and capabilities, applicable conformance obligations, successful and
unsuccessful outcomes, and any mechanism-specific claims. Automated checks,
manual review, assistive-technology exercises, and user evaluation prove only
their declared scope; select and combine them from the accepted claim.
