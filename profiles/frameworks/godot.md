# Godot Framework Profile

**Standards metadata**

- ID: `profile.framework.godot`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Godot objects, nodes, scene-tree operations, signals, resources, or engine APIs cross thread, async, deferred-dispatch, or object-lifetime boundaries.
- Does not apply when: No Godot-owned mechanism changes or the operation is proven to remain within one valid engine-owned context and lifetime.
- Requires: `core`, `workflow.verification`, `topic.concurrency`
- Specializes: `topic.concurrency`
- Verification: Godot affinity, dispatch ownership, and point-of-use lifetime decisions plus focused engine tests for every selected mechanism.
- Canonical owner: `profiles/frameworks/godot.md`

## Inherit The Generic Lifecycle Contract

[Concurrency And Async Lifecycle](../../topics/concurrency.md) owns work,
failure, cancellation, nonblocking execution, and shutdown. This profile owns
only Godot thread-affinity, dispatch, object-lifetime, and engine-mechanism
specialization.

Godot callbacks, deferred calls, signals, tasks, and object references do not
permit detached work, discarded failure, ignored cancellation, or state from
an earlier invocation to authorize a later one.

## Establish Engine Affinity

Identify which operations require the main thread, scene-tree ownership, a
render or physics phase, or another engine context before selecting a
mechanism. Execute directly only when the current context satisfies that
contract.

When dispatch is required, select a mechanism whose ordering, argument
lifetime, cancellation, completion, and failure behavior satisfy the
operation. `CallDeferred`, a callable, a dispatcher, or another engine API is
a mechanism, not universal proof. Do not use an alternate dispatcher or
fire-and-forget deferred call when required completion cannot be observed.

## Prove Object Lifetime At Use

Establish authority for every Godot object at the point where the engine
operation uses it. `GodotObject.IsInstanceValid` can contribute a local
validity observation, but a check before an await, queue, callback, or deferred
boundary does not prove later validity.

Use an ownership, reference, identity, revalidation, or engine-provided
mechanism that closes the check-to-use gap for the selected operation. Do not
carry a node reference, validity result, cancellation state, or result owner
from one workflow or invocation into an unrelated one.

## Typed Outcomes

Return the operation's typed `invalid`, `unsupported`, or `unavailable`
diagnostic when affinity contradicts execution, the selected dispatch cannot
provide required lifecycle evidence, the object is invalid at use, or required
context and lifetime facts are unknown. Preserve a more specific engine
failure when one exists.

Do not continue with off-thread engine access, stale validity, detached
deferred work, alternate dispatch, stale object references, or default
success.

## Verification

Evidence must cover the selected mechanism, including applicable:

- direct execution in the required engine context;
- ordered dispatch with observed completion and failure;
- object destruction before and after an async or deferred boundary;
- point-of-use identity and validity proof;
- repeated invocations with distinct objects and cancellation;
- rejection of off-thread access and check-then-use gaps; and
- typed failure when affinity, dispatch, lifetime, or evidence is absent.
