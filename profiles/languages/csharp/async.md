# C# Async Profile

**Standards metadata**

- ID: `profile.language.csharp.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: C# asynchronous code crosses an `await` boundary whose continuation scheduling, synchronization context, thread affinity, cancellation, or lifetime affects correctness.
- Does not apply when: No C# async mechanism changes or the operation is proven synchronous and immediate.
- Requires: `core`, `workflow.verification`, `topic.concurrency`
- Specializes: `topic.concurrency`
- Verification: C# continuation-affinity and lifecycle decisions plus focused runtime tests for every selected scheduling mechanism.
- Canonical owner: `profiles/languages/csharp/async.md`

## Inherit The Generic Lifecycle Contract

[Concurrency And Async Lifecycle](../../../topics/concurrency.md) owns work,
failure, cancellation, nonblocking execution, and shutdown. This profile owns
only C# continuation-scheduling mechanisms and evidence.

An `await`, `Task`, synchronization context, scheduler, or dispatcher does not
change the generic owner or permit detached work, discarded failure, ignored
cancellation, blocking waits, or state from a prior invocation.

## Select Continuation Scheduling From Affinity

Establish whether the continuation requires a specific synchronization
context, scheduler, thread, or dispatcher before selecting a mechanism.

Use context suppression such as `ConfigureAwait(false)` only when the selected
API supports it and the continuation contract proves that captured context is
not required. Preserve or explicitly dispatch to the required context when
continuation work has UI, engine, actor, or other thread-affinity obligations.

Library, service, handler, or application location alone does not prove either
decision. Do not apply context suppression globally, depend on implicit
capture, or add an alternate dispatcher as fallback.

## Preserve Invocation Isolation

Each invocation supplies its own inputs, cancellation, result destination, and
terminal outcome. A long-lived service or reused runtime may retain declared
shared resources, but it must not carry request inputs, synchronization
context, cancellation state, or result ownership from an earlier invocation.

## Typed Outcomes

Return the operation's typed `invalid`, `unsupported`, or `unavailable`
diagnostic when affinity requirements contradict the selected mechanism, the
API cannot provide the required scheduling behavior, or required affinity and
evidence are unknown. Preserve a more specific operation failure when one
exists.

Do not continue with context suppression, implicit capture, synchronous
blocking, detached work, alternate dispatch, or default success.

## Verification

Evidence must cover the selected continuation contract, including applicable:

- context-free continuation with supported context suppression;
- affinity-required continuation on or dispatched to the required context;
- failure and cancellation observation across the await boundary;
- repeated invocations with distinct inputs and cancellation;
- rejection of contradictory affinity and scheduling choices; and
- typed failure when required scheduling capability or evidence is absent.
