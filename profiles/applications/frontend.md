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

## Applicability Decision

Apply this profile when a change creates or alters a web or web-technology UI
projection, presentation-state owner, rendering lifecycle, user interaction,
frontend synchronization path, or frontend-specific evidence claim. Determine
applicability from the changed responsibility and observable behavior, not from
a product label, executable type, repository directory, or named container
technology.

A browser, embedded web view, desktop shell, or hybrid application is not
automatically in scope when the change has no frontend responsibility. A
frontend remains in scope when its UI mechanism is hosted outside a conventional
browser. Domain, persistence, transport, and native-host changes retain their
own owners even when a frontend consumes their results.

Missing responsibility or boundary facts are `unavailable`; contradictory
ownership is `invalid`; and a selected UI requirement that the supported
platform cannot represent is `unsupported`. Do not assume browser behavior,
copy a neighboring product profile, infer scope from Electron, Tauri, WebView,
or another framework name, or silently treat a cross-boundary change as
frontend-owned.

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

Select rendering from the authoritative state, required output, interaction,
lifecycle, platform capability, and evidence. Declarative bindings do not
become state authority, and imperative access does not authorize reconstruction
from the rendered tree. Isolate mechanism-owned mutation from declarative
ownership only when the selected renderer requires it, and prove cleanup and
reconciliation at that boundary.

Synchronize from authoritative state through the selected event, subscription,
query, or boundary mechanism. Polling is valid only when the source contract is
pull-based or no supported event mechanism satisfies the requirement. Its
owner, cadence, cancellation, stale-result handling, and terminal outcomes
must be explicit.

Event delivery, subscriptions, direct queries, and polling are alternatives
selected by the source and consumer contracts; none is a universal preference.
A pull-style FFI or message drain remains a boundary adapter and does not
authorize a second UI polling loop. The synchronization mechanism must preserve
ordering, duplicate, stale-result, cancellation, and unavailable-source
outcomes required by its owners.

Do not use a second UI store, DOM reads, global timer, copied response, or
periodic reconciliation as fallback for missing authority or synchronization.
Do not switch between declarative and imperative rendering, event and polling,
or push and pull sources when the selected mechanism is unavailable. Return
`invalid` for contradictory authority, unsafe mutation, stale application, or
incomplete lifecycle; `unsupported` for a valid requirement outside platform
capability; and `unavailable` for missing authority, source contract,
mechanism, lifecycle, or evidence.

Illustrative mechanisms are isolated in the
[Frontend mechanism recipes](../../reference/recipes/frontend.md).

## Lifecycle-Owned Frontend Work

For timers, polling, subscriptions, observers, animation callbacks, and other
work that can outlive one immediate call, identify the frontend owner, protected
state, invocation authority, start condition, completion, cancellation,
supersession, dependency change, teardown boundary, and terminal outcomes.
Concurrency owns generic work lifecycle; TypeScript Async owns TypeScript
invocation and result-application mechanisms.

Select a resource holder and cleanup trigger from the framework and lifecycle
contract. A ref, component state, field, closure, abort signal, generation
token, or owner object is a mechanism, not a default. Completion, dependency
change, unmount, shutdown, retry, and replacement require cleanup only when they
end or supersede the selected ownership interval.

Prevent duplicate active work and stale result application through proven
identity and lifecycle authority. Clearing a timer, returning from a callback,
or observing one successful update does not prove cancellation, terminal
classification, cleanup, or exclusion of a superseded result.

Missing owner, identity, lifecycle, cleanup capability, or evidence is
`unavailable`; contradictory ownership, duplicate work, stale application,
unobserved completion, or incomplete cleanup is `invalid`; and a valid
lifecycle unsupported by the selected mechanism is `unsupported`. Do not
fall back to a global timer, fixed cadence, ref holder, state holder, silent
stale-result discard, retry, detached work, or default success.

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
