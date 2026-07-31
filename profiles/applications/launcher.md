# Launcher Application Profile

**Standards metadata**

- ID: `profile.application.launcher`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A repository entrypoint exposes application lifecycle, build, install, verification, release, or operator actions through a command-line launcher.
- Does not apply when: No launcher or launcher-visible action changes.
- Requires: `core`, `workflow.verification`, `topic.resilience`
- Specializes: `none`
- Verification: Launcher action-selection, delegation, argument, process-lifecycle, and outcome-preservation decisions plus focused command-boundary tests.
- Canonical owner: `profiles/applications/launcher.md`

## Launcher Authority

A launcher is a command adapter between an operator or automation caller and
canonical repository procedures. It owns:

- action discovery and selection;
- action-specific argument decoding and validation;
- environment and process setup declared by the action contract;
- delegation to the selected procedure;
- signal, cancellation, and child-process lifecycle handling; and
- preservation of the delegated procedure's terminal outcome.

It does not own application business logic, dependency selection, build or
release semantics, verification acceptance, frontend projection, or transport
policy. Invoke the canonical owner for those concerns rather than reproducing
its logic in the launcher.

## Select Actions From Declared Capabilities

Expose only actions backed by declared repository capabilities and selected
procedures. Action names, required actions, argument schemas, target identity,
and passthrough support come from the application contract; they are not a
universal fixed flag set.

Decode exactly one action when the interface requires one. Reject unknown,
ambiguous, contradictory, or malformed input with a typed diagnostic. Do not
accept positional or passthrough arguments unless the selected action declares
their schema and destination.

An inapplicable action is omitted or returns its declared typed
`unsupported` outcome. Do not add a successful no-op, guessed target, raw
toolchain command, or alternate action as fallback.

## Delegate Without Upgrading Evidence

Build, install, test, performance, smoke, release, and run actions delegate to
their canonical procedures. Preserve their exit status, diagnostics,
artifacts, and evidence classification.

A launcher invocation does not turn startup into a user workflow, a smoke
check into end-to-end evidence, or a successful command into proof beyond the
delegated procedure's acceptance claim. Missing required procedure or evidence
is a typed `unavailable` outcome.

## Own Process And State Boundaries

Select process replacement, child supervision, bounded execution, signal
forwarding, and cancellation from the action lifecycle contract. `exec`,
background processes, timeouts, and process groups are mechanisms, not
universal defaults.

State isolation, host-state access, environment mutation, and cleanup must be
declared by the action contract. A launcher must not carry temporary paths,
credentials, request inputs, cancellation, or result ownership from one
invocation into another.

## Typed Outcomes

Return typed `invalid`, `unsupported`, or `unavailable` diagnostics for
malformed action input, unsupported capability, missing procedure or target,
and unavailable lifecycle or evidence requirements. Preserve more specific
delegated failures.

Do not continue through a guessed action, alternate command, implicit install,
successful no-op, weakened runtime mode, discarded child failure, stale state,
or default success.

## Verification

Evidence must cover applicable:

- each declared action and its argument schema;
- unknown, ambiguous, malformed, and unsupported actions;
- exact delegation and outcome preservation;
- signal, cancellation, timeout, and child failure behavior;
- isolated and explicitly authorized host-state modes;
- repeated invocations without state carry-forward; and
- rejection when procedure, target, lifecycle, or evidence is unavailable.
