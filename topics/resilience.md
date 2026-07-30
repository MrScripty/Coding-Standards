# Resilience

**Standards metadata**

- ID: `topic.resilience`
- Role: `topic`
- Level: `MUST`
- Applies when: A dependency, service, resource, or startup condition can fail and the product must choose whether to fail, retry, degrade, or remain unavailable.
- Does not apply when: No failure condition affects an operation, lifecycle, resource, or user-visible outcome.
- Requires: `core`, `workflow.verification`
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
continue with an unowned failure,
silently ignore it, or claim recovery from logging alone.

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

## Retry And Recovery

Retry only when the operation is eligible, the retry authority is selected,
the attempt and time budgets are bounded, and repeated execution is safe under
the operation's idempotency contract. Recovery may retry, reinitialize,
degrade, or fail according to the selected contract; it must not switch to an
alternate dependency or unbounded loop when the selected mechanism is missing.

Record attempts, terminal outcome, cancellation, and recovery evidence at the
owner that controls the operation. Typed diagnostics preserve the distinction
between failed, unavailable, unsupported, and successfully degraded outcomes.

## No Fallback

Missing facts or capability cannot select a default retry policy, timeout,
dependency, empty result, stale result, ignored error, alternate mechanism,
or silent degradation. Unknown recovery behavior remains a typed diagnostic.
