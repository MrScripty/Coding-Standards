# TypeScript Async Profile

**Standards metadata**

- ID: `profile.language.typescript.async`
- Role: `profile`
- Level: `PROFILE`
- Applies when: TypeScript asynchronous operations can overlap, be superseded, mutate shared or visible state, or require cancellation and terminal-result ownership.
- Does not apply when: No TypeScript async mechanism changes or execution is proven sequential with no operation outliving its immediate caller.
- Requires: `core`, `workflow.verification`, `topic.concurrency`, `profile.language.typescript`
- Specializes: `topic.concurrency`
- Verification: TypeScript invocation-authority, cancellation, completion, and state-application decisions plus focused tests for the selected mechanism.
- Canonical owner: `profiles/languages/typescript/async.md`

## Inherit The Generic Lifecycle Contract

[Concurrency And Async Lifecycle](../../../topics/concurrency.md) owns work,
failure, cancellation, nonblocking execution, and shutdown. This profile owns
only TypeScript mechanisms for identifying the current invocation, classifying
superseded completion, and controlling result application.

A `Promise`, generation token, request identifier, or `AbortSignal` does not
permit detached work, discarded failure, ignored cancellation, or state from
one invocation to become input or output authority for another.

## Establish Current-Invocation Authority

When operations can overlap, select an explicit owner and mechanism that can
prove which invocation may mutate current state. Valid mechanisms can include
a scope-owned generation token, cancellation signal, serialized owner, or
another mechanism whose lifetime and comparison contract are verified.

Do not select a process-global counter, one example request identifier, or
silent stale-result discard as universal policy. The mechanism must be scoped
to the state it protects and must not wrap, collide, leak across owners, or
carry inputs from an earlier invocation.

## Classify Every Completion

Observe every started operation's success, failure, cancellation, or
superseded result. A superseded completion must not mutate current state, but
it still has an explicit terminal classification owned by the operation's
lifecycle owner.

Propagate cancellation when it remains part of the operation contract. When
the underlying operation cannot be cancelled, continue to observe its
completion and classify it without applying a superseded result. Do not treat
an early `return`, ignored promise, or omitted callback as completion evidence.

## Typed Outcomes

Return the operation's typed `invalid`, `unsupported`, or `unavailable`
diagnostic when invocation authority contradicts result application, the
selected mechanism cannot provide required cancellation or identity, or
required ownership and evidence are unknown. Preserve a more specific
operation failure when one exists.

Do not continue with a process-global counter, stale state mutation, ignored
completion, ignored cancellation, alternate mechanism, or default success.

## Verification

Evidence must cover the selected mechanism, including applicable:

- overlapping invocations with only the current result applied;
- explicit success, failure, cancellation, and superseded classifications;
- scoped authority across multiple independent owners;
- repeated operations with distinct inputs and cancellation;
- rejection of stale mutation and process-global authority; and
- typed failure when identity, cancellation, ownership, or evidence is absent.
