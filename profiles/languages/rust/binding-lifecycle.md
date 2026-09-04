# Rust Binding Events And Runtime Lifecycle

**Standards metadata**

- ID: `profile.language.rust.binding-lifecycle`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust bindings adapt events, callback tasks, runtime handles, or executors.
- Does not apply when: The binding changes only synchronous value representation without event, task, runtime, or executor ownership.
- Requires: `profile.language.rust.language-bindings`
- Specializes: `profile.language.rust.language-bindings`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `profiles/languages/rust/binding-lifecycle.md`

## Host Event Delivery

Select the host event-delivery contract before implementing the Rust adapter.
The contract defines:

- the event representation and supported variants;
- provider or registration authority under the Interop callback contract;
- push, pull, stream, or another declared delivery mode;
- ordering, capacity, backpressure, and overflow or retention behavior;
- delivery-failure, cancellation, and shutdown outcomes; and
- callback thread, re-entrancy, and input-lifetime requirements.

The adapter bridges that selected contract without moving host behavior into
the core. Push and pull are peer contract choices; neither is a preference or
fallback for the other. A retained provider, registration, buffer, runtime, or
host handle does not authorize carrying an earlier event, cancellation,
result, or failure state into a later delivery.

When buffering is selected, capacity and overflow or retention behavior are
governed by the operation contract. Overflow is observable through the
selected typed outcome or declared event semantics. Do not retain events
without a bound or discard them silently. When direct callback or message
delivery is selected, invoke host-controlled behavior only on an authorized
thread and outside synchronization guards.

Inline delivery remains scoped to the current invocation. Work that may
outlive delivery uses
[Concurrency work ownership](../../../topics/concurrency.md#own-work-failure-and-cancellation)
for failure observation, cancellation, and shutdown. Foreign registration,
in-flight callback, unregistration, and release obligations remain governed by
the [Interop event-registration contract](../../boundaries/interop.md#event-registration-lifecycle).

Preserve provider and host delivery failures. Return `invalid` when adapter
facts contradict the selected contract, `unsupported` when a well-formed event
or delivery mode is outside it, `unavailable` when required registration,
thread, delivery, buffering, or host capability cannot be established before
delivery, and the selected typed incomplete outcome when an active delivery or
shutdown obligation cannot be resolved.

Do not substitute push for pull or pull for push, create an alternate runtime,
detach callback-created work, retry on an arbitrary thread, carry prior event
state forward, drop events silently, or report default success.
## Host Callback Task Adaptation

Select the host callback-task contract before a Rust adapter asks host code to
perform work. The contract defines:

- supported task identities and checked input and output representations;
- callback authority, thread, re-entrancy, and input lifetime;
- synchronous or asynchronous completion and correlation identity;
- admission, capacity, cancellation, deadline, and shutdown obligations; and
- host failure, incomplete completion, duplicate response, and late response
  outcomes.

The core may define a binding-neutral port when host execution is a domain
capability, but the adapter owns host representation and invocation mechanics.
Neither generated host code nor the adapter owns domain behavior. Capture the
current validated task snapshot, release synchronization guards, and then
invoke host-controlled behavior.

Each invocation has fresh task identity, input, cancellation, result, and
failure state. A retained callback, host process, runtime, model, or adapter
does not authorize carrying state from an earlier invocation. Match each
response to the selected correlation contract and resolve terminal completion
once. Preserve the contract-selected outcome for late or duplicate completion
after cancellation or another terminal result.

Inline completion remains scoped to the invocation. Asynchronous work that may
outlive it consumes the composition-owned runtime capability and is registered
with the selected Rust Async and Concurrency lifecycle owner before submission.
That owner observes success, failure, panic, cancellation, and shutdown. The
adapter does not synchronously drive async work, create an alternate runtime,
or detach work to satisfy the callback.

Convert task input, output, and host failures through checked binding
representations. Preserve host task failure and cancellation. Return `invalid`
for malformed input, output, correlation, or contradictory callback facts,
`unsupported` when a well-formed task is outside the selected host contract,
`unavailable` when required callback, runtime, admission, conversion, or result
delivery capability cannot be obtained, and the selected typed incomplete
outcome when accepted work cannot reach an observed terminal state.

Do not install a no-op executor, replace callbacks with snapshot polling or
result injection, use generic/default task output, reinterpret failure as
unsupported delegation, carry prior invocation state forward, or report
default success.
## Handle And Runtime Adaptation

Distinguish a host-visible handle from runtime and task lifecycle. A foreign
handle owns only its declared adapter or domain-object reference. Releasing the
last host handle releases that reference; it does not grant runtime shutdown
authority unless the composition owner separately assigns that authority.

When host adaptation needs asynchronous execution, also select the
[Rust Async profile](async.md). Consume the runtime capability supplied by the
application's composition owner. The capability may remain loaded and shared
across calls or workflow runs without making a binding object, request, task,
or requesting workflow its owner.

Each call creates fresh input, cancellation, result, and failure state. Runtime
reuse never carries any of that request-scoped state into later calls. A
persistence or keep-alive request is lifecycle/scheduling input, not ownership
transfer and not authority to retain the requesting workflow's state.

Expose a host-compatible asynchronous result when work remains scoped to the
call. Work that may outlive the call is registered with the selected lifecycle
owner before submission, and its terminal outcome remains observable through
that owner. The adapter does not synchronously drive an asynchronous runtime,
create an embedded or alternate runtime, or detach work to satisfy a host call.

Return typed `unsupported` or `unavailable` when the selected runtime,
host-async, task-registration, or result-delivery capability cannot be
provided.
## Explicit Executor Delegation

A composite executor defines the exact typed `unsupported` outcome that makes
an operation eligible for one selected next executor. Pass only the current
call's already validated input. Successful local completion is terminal.

Validation, execution, cancellation, resource, lifecycle, and unavailable
capability outcomes remain their original terminal outcomes. Do not
reinterpret them as unsupported. If the selected next executor or its required
capability cannot be obtained, return typed `unavailable`.

Delegated work remains scoped to the current call or is registered with the
selected lifecycle owner before it can outlive that call. Runtime persistence
does not authorize another delegation attempt or retention of the call's
input.
