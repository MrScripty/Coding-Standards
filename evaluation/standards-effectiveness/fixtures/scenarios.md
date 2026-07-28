# Evaluation Scenarios

These fixtures are product-neutral. Expected routing names target roles rather
than final paths until Milestone 1 freezes the information architecture.

Every plan is expected to state objective, acceptance path, current phase,
exactly one next slice, binding decisions, blockers, re-plan triggers, and the
separate location for execution history.

## S1: Small Local Bug Fix

**Objective:** Correct an internal parser that accepts an empty identifier.

**Conditions:** One module, no public contract, no persistence, no UI, no
dependency change.

**Expected routing:** Core, implementation workflow, testing workflow, language
profile.

**Excluded:** Architecture patterns, release, frontend, interop, persistence,
launcher, accessibility, and cross-platform topics.

**Acceptance:** Focused regression test plus affected static checks.

**Prohibited errors:** Requiring a large plan, ADR, directory README, release
workflow, or full standards-tree read.

## S2: Cross-Layer Desktop Workflow

**Objective:** Add a user action whose policy and state live in the backend and
whose projection and interaction live in the frontend.

**Conditions:** Desktop shell bridges backend and web frontend; transport must
not own business policy.

**Expected routing:** Core; planning, implementation, and verification
workflows; desktop and frontend profiles; IPC/boundary, accessibility, and
security topics.

**Excluded:** Language bindings and release unless the contract is public or an
artifact will ship.

**Acceptance:** A real user workflow through UI, bridge, backend, state update,
and visible projection. Backend and frontend focused tests support but do not
replace it.

**Prohibited errors:** Business logic in the bridge, headless checks marked as
user acceptance, or duplicate policy owners.

## S3: Durable Background Worker

**Objective:** Process queued work across restart with bounded cancellation and
observable terminal outcomes.

**Conditions:** Durable state, concurrent execution, retries, shutdown, and
restart recovery.

**Expected routing:** Core; planning, implementation, and verification
workflows; service/worker profile; concurrency, persistence, diagnostics, and
security topics.

**Excluded:** Frontend, accessibility, bindings, and release absent explicit
conditions.

**Acceptance:** Integration test covers claim, execution, cancellation,
restart, retry, and terminal persistence using the real durable boundary.

**Prohibited errors:** Request scope presented as durable ownership, detached
untracked work, hidden retry fallback, or process-local state as authority.

## S4: Rust FFI Contract Change

**Objective:** Add a typed result to a Rust API exposed through generated host
bindings.

**Conditions:** Unsafe boundary, generated artifacts, host-language consumer,
and coordinated contract generation.

**Expected routing:** Core; planning, implementation, and verification
workflows; Rust and binding profiles; interop, unsafe, and contract topics.

**Excluded:** Frontend, launcher, and persistence unless independently present.

**Acceptance:** Rust contract tests, generated-artifact consistency, host
language tests, and one real cross-boundary consumer path.

**Prohibited errors:** Hand-edited generated output, stringly typed error
substitution, host-only smoke as native contract proof, or ambiguous owner.

## S5: Coordinated Persisted Schema Break

**Objective:** Replace a persisted schema whose producer and consumers are
released together.

**Conditions:** Existing stored data, coordinated deployment, explicit
migration window, no independent public consumer.

**Expected routing:** Core; planning, implementation, verification, and release
workflows; persistence and contract-evolution topics; language profile.

**Excluded:** Public compatibility profile unless independent consumers are
discovered.

**Acceptance:** Migration tests for supported prior data, rejection or typed
diagnostic for unsupported data, new-schema round trip, and release artifact
smoke.

**Prohibited errors:** Universal append-only evolution, compatibility shim
without a consumer, deleting authoritative data as fallback, or silent default.

## S6: Dependency And Release Update

**Objective:** Upgrade a shipped application's framework dependency and publish
the resulting release.

**Conditions:** Lockfile and build changes, security review, packaged artifact,
and downstream users.

**Expected routing:** Core; implementation, verification, and release
workflows; dependency and application profiles; security topic.

**Excluded:** Large architecture plan unless contracts or ownership change.

**Acceptance:** Dependency audit, affected tests, package build, clean-machine
artifact smoke, and release checklist.

**Prohibited errors:** Source-only success, unreviewed transitive risk, or
release smoke treated as full feature acceptance.

## S7: Hardware-Gated User Capability

**Objective:** Deliver an end-to-end feature requiring optional physical
hardware unavailable on ordinary CI runners.

**Conditions:** Device discovery, backend capability, UI workflow, explicit
unavailable diagnostics, and a manual or dedicated-runner acceptance gate.

**Expected routing:** Core; planning, implementation, verification, and release
workflows; application, frontend, and language profiles; hardware,
cross-platform, diagnostics, accessibility, and security topics.

**Excluded:** A requirement that every acceptance check finish in a universal
CI duration.

**Acceptance:** Focused and simulated checks in CI, plus recorded real-hardware
user-workflow acceptance before the capability is marked accepted.

**Prohibited errors:** Fake hardware fallback presented as real capability,
startup smoke as feature proof, skipped hardware acceptance without a visible
blocked state, or environment facts guessed by planning.
