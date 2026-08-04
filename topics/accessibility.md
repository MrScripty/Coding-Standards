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
