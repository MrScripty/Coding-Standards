# Frontend Application Profile

**Standards metadata**

- ID: `profile.application.frontend`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A web or web-technology user interface, component, rendering path, interaction, frontend state projection, or frontend test changes.
- Does not apply when: No user-interface projection, interaction, frontend state, or frontend-owned evidence changes.
- Requires: `core`, `workflow.verification`, `topic.contracts`, `topic.accessibility`
- Specializes: `topic.contracts`, `topic.accessibility`
- Verification: Frontend authority, projection, synchronization, interaction, accessibility, and evidence decision fixtures plus affected component and real-browser evidence.
- Canonical owner: `profiles/applications/frontend.md`

## Projection Authority

A frontend projects canonical application and domain state into a user
interface and translates user interaction into declared actions. It owns
presentation state, rendering lifecycle, interaction adaptation, and
frontend-specific evidence. It does not own domain behavior, persistence,
transport, runtime decoding, or accessibility policy.

Select the authoritative state and action contract before selecting a
framework mechanism. Independently produced input requires Contracts-owned
runtime proof before it becomes frontend state. Do not infer domain authority
from the rendered tree, duplicate backend rules in components, or treat a
TypeScript type as runtime proof.

## Rendering And Synchronization

Prefer declarative projection when the selected framework can express the
required output and lifecycle. Direct DOM, canvas, WebGL, native-widget, or
other imperative access is valid when the interaction or rendering contract
requires it and ownership, cleanup, and synchronization are explicit.

Synchronize from authoritative state through the selected event, subscription,
query, or boundary mechanism. Polling is valid only when the source contract is
pull-based or no supported event mechanism satisfies the requirement. Its
owner, cadence, cancellation, stale-result handling, and terminal outcomes
must be explicit.

Do not use a second UI store, DOM reads, global timer, copied response, or
periodic reconciliation as fallback for missing authority or synchronization.

## Interaction And Accessibility

Project every supported interaction through declared action and state
transitions. Select pointer, keyboard, focus, gesture, and assistive-technology
mechanisms from the component and Accessibility contracts. Visual behavior
alone is not interaction proof.

An unsupported interaction or platform capability returns the declared
`unsupported` outcome. Contradictory ownership, inaccessible required
interaction, or ambiguous action mapping is `invalid`. Missing authoritative
state, decoder, lifecycle, capability evidence, or required browser evidence
is `unavailable`.

Do not silently omit an applicable interaction, install an inert control,
substitute a pointer-only path, or report success from a visual snapshot.

## Evidence

Use the narrowest evidence that proves the changed claim:

- pure projection and state transitions may use deterministic component tests;
- user-visible semantics require role, name, state, and interaction evidence;
- geometry, focus, pointer capture, browser APIs, rendering engines, and
  embedded controls require evidence in an environment that implements them;
- backend-to-frontend flows require evidence through the real contract and
  projection boundaries.

Selectors and simulation tools are mechanisms. Choose them from the behavior
under test and do not treat a preferred query API, synthetic event, DOM shim,
snapshot, or component mount as universal evidence.

Select interaction evidence from the user-observable contract. Semantic
controls require accessible role, name, state, focus, keyboard, and activation
evidence for every applicable interaction path. Embedded controls inside
draggable, pannable, zoomable, or canvas-style containers also require pointer
capture and release, focus and escape, and parent-gesture conflict evidence.
A selector or event-dispatch API is not evidence unless its semantics match the
claim.

Browser geometry, layout, pointer capture, focus transfer, rendering-engine,
and browser-API claims require a representative browser environment. Pure
geometry functions may be proved deterministically, but mocked rectangles or a
DOM shim do not prove browser integration. If the required environment is not
available, report `unavailable` instead of substituting component success.

Polling, timers, subscriptions, observers, and other lifecycle-owned work
require evidence that completion, dependency change, retry, cancellation, and
unmount release the resource, prevent duplicate work, and exclude stale
results. A successful update does not prove cleanup.

## Typed Outcomes

Preserve typed `invalid`, `unsupported`, and `unavailable` outcomes through the
UI contract. A presentation layer may map them to declared user-facing states,
but must not convert them to stale content, empty success, guessed defaults,
silent omission, or an alternate interaction.

Evidence covers successful projection, invalid input, unsupported
capabilities, unavailable dependencies, lifecycle cleanup, repeated
invocations without state carry-forward, and the real environment for claims
that component-level simulation cannot prove.
