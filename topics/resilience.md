# Resilience

**Standards metadata**

- ID: `topic.resilience`
- Role: `topic`
- Level: `MUST`
- Applies when: A dependency, service, resource, or startup condition can fail and the product must choose whether to fail, retry, degrade, or remain unavailable.
- Does not apply when: No failure condition affects an operation, lifecycle, resource, or user-visible outcome.
- Requires: `core`, `workflow.verification`, `topic.contracts`
- Specializes: `none`
- Verification: Resilience decision fixtures plus affected startup, dependency, retry, degradation, and recovery tests.
- Canonical owner: `topics/resilience.md`

## Failure And Recovery Authority

Select one owner for the complete failure and recovery contract at each
applicable boundary. The contract names the dependency or resource, the
operation and lifecycle phase, criticality, retry or degradation semantics,
observable outcome, recovery authority, and evidence required to accept the
behavior. A failure category, retry count, timeout, or best-effort label is not
an independent policy authority.

Return typed `invalid` for contradictory criticality, recovery, or outcome
facts; return typed `unsupported` when a declared resilience mode is outside
the selected contract; and return typed `unavailable` when required
dependency, recovery, or evidence capability cannot be established. Do not
continue with an unowned failure, silently ignore it, or claim recovery from
logging alone.

## Failure Classification And Decision

Classify a failure from authoritative facts about the dependency, operation,
lifecycle phase, state ownership, selected degraded outcome, and available
recovery capability. Labels such as corrupt, unavailable, stale, external,
required, or optional describe evidence; they do not select a recovery action
by themselves.

Apply this decision order:

1. Establish whether the dependency is required or best-effort for the current
   operation and lifecycle phase.
2. Establish whether affected state is authoritative, disposable derived state,
   or unknown.
3. Select the declared terminal, degraded, retry, or reconstruction outcome.
4. Prove retry safety, reconstruction authority, and required evidence before
   executing that outcome.
5. Return the selected result or typed diagnostic without changing mechanisms.

## Criticality And Degradation

Classify a dependency as required or best-effort from the operation and
product contract. Required failures preserve the declared failure outcome;
best-effort behavior is valid only when the contract defines the degraded
semantics, user-visible impact, observability, and recovery obligations.
Startup checks and steady-state handling may differ only when the lifecycle
contract declares that distinction.

Do not turn an unavailable required dependency into success, substitute an
empty or stale value, skip a required startup check, or apply best-effort
handling because a default is convenient. A degraded result is not a generic
fallback; it is a selected contract outcome with evidence.

## Startup Resilience

Make startup decisions from the startup lifecycle contract rather than from a
universal dependency category. A required startup capability that cannot be
established prevents readiness with a typed diagnostic. A best-effort
capability permits startup only when the accepted contract defines the
degraded service surface, health state, user-visible impact, observability, and
later recovery authority.

Do not infer that databases and configuration are always required or that
caches, indexes, analytics, telemetry, and logging sinks are always optional.
Do not report readiness while a required capability is unavailable.

## Best-Effort Dependency Boundaries

A best-effort adapter returns the explicitly selected degraded result. It
preserves the distinction between absence, unavailable capability, invalid
state, unsupported behavior, and a successful value. Catching an arbitrary
failure and returning no value, an empty value, stale data, cached data,
partial output, or success is not a best-effort contract.

The adapter records health and recovery evidence without becoming the owner of
the dependency's authoritative state or the caller's operation semantics.

## Retry And Recovery

Retry only when the operation is eligible, the retry authority is selected,
the attempt and time budgets are bounded, and repeated execution is safe under
the operation's idempotency contract. Recovery may retry, reinitialize,
degrade, or fail according to the selected contract; it must not switch to an
alternate dependency or unbounded loop when the selected mechanism is missing.

Record attempts, terminal outcome, cancellation, and recovery evidence at the
owner that controls the operation. Typed diagnostics preserve the distinction
between failed, unavailable, unsupported, and successfully degraded outcomes.

## State Reconstruction

Delete, replace, seed, or rebuild state only when the Contracts owner proves
that the affected state is disposable derived state and identifies a complete
authoritative reconstruction source. Corrupt or unavailable authoritative
state remains intact for diagnosis or explicit recovery; it is not converted
to defaults or silently replaced.

Cold-start and lazy-rebuild behavior is valid only as a selected reconstruction
contract. A missing cache does not authorize stale reads, alternate stores, or
weaker evidence.

## Acceptance Evidence

Verification covers required and best-effort behavior at startup and runtime,
bounded retry and cancellation, degraded result shape, health transitions,
terminal diagnostics, reconstruction authority, and recovery. Availability
claims must match the service surface that remains valid during degradation.

## No Fallback

Missing facts or capability cannot select a default retry policy, timeout,
dependency, empty result, stale result, ignored error, alternate mechanism,
or silent degradation. Unknown recovery behavior remains a typed diagnostic.
