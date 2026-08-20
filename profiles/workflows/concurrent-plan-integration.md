# Concurrent Plan Integration Profile

**Standards metadata**

- ID: `profile.workflow.concurrent-plan-integration`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Two or more proposals may be prepared from the same mutable plan revision before integration and correctness depends on detecting intervening plan or shared-authority change.
- Does not apply when: Work is serial, read-only, non-authorizing, cannot become stale, or has one current-state integration owner with no outstanding proposals.
- Requires: `core`, `workflow.planning`, `workflow.verification`
- Specializes: `workflow.planning`
- Verification: Concurrent proposal applicability, exclusion, stale-state, conflict, dependency, unsupported-mechanism, and no-fallback decision fixtures.
- Canonical owner: `profiles/workflows/concurrent-plan-integration.md`

## Applicability

Apply this profile only when all of these facts hold:

- at least two proposals can remain outstanding before integration;
- those proposals were prepared from the same mutable plan revision;
- plan or declared shared-authority state can change before integration; and
- integrating from stale admission facts could change correctness.

Do not apply it to serial work by several participants, read-only investigations,
delegated reports that cannot authorize changes, independent work whose
admission facts cannot become stale, or one integration owner working from
current state with no outstanding proposals.

Missing applicability facts are `unavailable`. Contradictory applicability or
authority is `invalid`. Do not infer applicability from participant count,
agent use, worktree count, file disjointness, or repository size.

## Proposal Contract

Each outstanding proposal records:

- the selected plan path and explicit operation;
- the admitted plan revision using one supported revision mechanism;
- the responsible actor;
- affected scope and bounded write set;
- prerequisite proposal identities or `none`;
- intended semantic outcome and resulting plan state;
- verification contract; and
- designated serial integration owner.

When a proposal uses a branch or worktree, also record its source branch,
target branch, visibility, and cleanup handoff. Do not require a branch or
worktree merely because this profile applies; Commit owns the isolation and
integration-mechanism decision.

Actor identity records responsibility and does not confer plan, resource, or
integration ownership. Empty, absent, and `none` remain distinct where the
selected representation gives them different meanings.

## Revision And Compatibility Checks

Compare the proposal's admitted revision with current plan authority immediately
before its first shared-authority mutation and immediately before authoritative
integration. A mismatch is semantically `stale`; do not silently retry, merge,
overwrite, rebase, or select the latest state.

Before integration, confirm prerequisites, affected scopes, write-set
compatibility, semantic outcomes, verification contracts, and shared-authority
ownership. Classify overlap or contradictory outcomes as `conflicting`, unmet
prerequisites as `dependency-blocked`, missing required facts as `unavailable`,
malformed or contradictory authority as `invalid`, and an unavailable selected
revision mechanism as `unsupported`.

These classifications are semantic. Tools may encode them as typed values;
manual workflows may record explicit labels. A serialized sum type is not
required.

After a stale proposal receives fresh admission, Commit may authorize rebasing
a complete private, unshared branch, followed by conflict resolution, complete
affected reverification, and fast-forward integration. Fresh admission is the
authority; a stale mismatch itself never authorizes rebase or another recovery
mechanism.

## Serial Integration And Reconciliation

One designated integration owner serially changes active plans, ledgers,
routers, shared contracts, lockfiles, generated artifacts, and other declared
shared authority. Disjoint files alone do not prove compatible outcomes.

The integration owner selects the least history-transforming accepted
mechanism through Commit, records replacement lineage when selective
cherry-pick or reconstruction is required, records each proposal's terminal
classification, and hands off only predeclared cleanup of owned task resources.
Separate worktrees provide isolation; they do not confer ownership, preserve
durable evidence, or require cherry-pick integration.

When integration is partial or evidence disagrees with state, stop normal
admission. From fresh current state, record what integrated, what did not, the
observed revision, the selected recovery outcome and authority, intended result,
and verification contract. Verify that result and issue a new admission for any
remaining work. Do not choose recovery from timestamps, file precedence,
apparent completeness, or a failed proposal's old admission.

## Mechanism Boundary

This profile requires a revision mechanism with compare-before-integrate
semantics; it does not prescribe hashes, framing, database versions, object
identifiers, repository identities, or storage. The selected mechanism must be
available to every participating writer and must distinguish the admitted state
from changed current state.

If an adopting standard mandates a concrete machine representation, its
constructor, validator, prompts, templates, fixtures, and executable support
must agree before that representation becomes mandatory. The
[revision mechanism recipe](../../reference/recipes/concurrent-plan-integration.md)
is illustrative and non-normative.

Do not add reservations, leases, queues, heartbeats, scheduling, state-only
commits, recovery journals, transaction managers, duplicate execution, or
persistent coordination as fallback. Such mechanisms require measured need and
their own routed owners.
