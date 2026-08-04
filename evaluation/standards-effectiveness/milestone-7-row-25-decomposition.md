# Milestone 7 Row 25 Implementation Prompt Decomposition

## Owner Contract

`workflows/implementation.md` is the sole projection owner for the versioned
implementation prompt. Frozen snapshot sections establish identifier lineage
only; they do not override current canonical workflow authority.

Planning owns active-plan state, findings, delegation, and re-planning;
Verification owns evidence and acceptance; Commit owns staged review and commit
procedure. The prompt routes through Implementation and cannot copy those
contracts, preserve a legacy checklist, or act as a second router.

## Exact Dispositions

`STD-0852` through `STD-0858` receive exact `index` dispositions to
`workflows/implementation.md`. No normative movement is required because the
useful snapshot semantics already exist in canonical workflows.

## Ordered Children

1. `25.1a`: establish Planning-owned `start`, `continue`, and `verify`
   admission plus explicit repository-relative plan identity consumed by
   Implementation, with focused no-inference evidence.
2. `25.1b`: replace the tracked checklist with one thin, versioned,
   path-neutral Implementation entrypoint; record seven exact dispositions and
   focused positive and negative projection evidence.

Child `25.1a` may touch Planning, Implementation, its focused fixtures/checker,
plan, and ledger. Child `25.1b` may touch the prompt, dispositions, focused
fixtures/checker, plan, ledger, and affected shared cursor assertions.

## Child 25.1 Plan Identity Replan

The invocation must supply one explicit repository-relative `plan.md` path.
Implementation owns identity presence and plan semantics. Security owns path
resolution, canonicalization, traversal and symlink-escape rejection,
containment, and validation/use safety. Cross-Platform applies conditionally
when filesystem representation affects resolution. Planning owns plan
structure, implementable lifecycle state, linked artifact consistency, and
exactly one next slice.

Missing identity is Implementation `unavailable`; contradictory identity is
Implementation `invalid`; traversal or repository escape is Security `invalid`;
missing root or resolution facts are Security `unavailable`; unsupported
filesystem mechanics are Security `unsupported`; invalid plan structure is
Planning `invalid`, and missing required plan facts are Planning `unavailable`.

Implementation links to these owners and does not copy their algorithms. Do not
scan for an active plan, select by filesystem order or recency, infer a
conventional path, use conversation history as authority, or create a
repository-global pointer. A future default-selection mechanism requires
downstream evidence and a separate replan.

## Child 25.1 Lifecycle Admission Replan

The invocation supplies one explicit operation. Planning owns admission:

- `start` accepts only `Planned` and transitions it to `Active`;
- `continue` accepts only `Active` and preserves that state; and
- `verify` accepts `Implemented` or `Verifying` and transitions
  `Implemented` to `Verifying` when verification begins.

`Blocked` is `unavailable` with its blocker. `Deferred` is `unavailable` until
its revisit authority activates it. `Accepted` and `Superseded` are `invalid`
for execution; a known replacement is diagnostic context only. Missing or
inferred operation is `unavailable`, and a state/operation mismatch is
`invalid`. The presence of a next slice does not grant execution authority.

Implementation transports the explicit operation and consumes Planning's
decision without copying this admission table. The accepted transition and its
ledger update occur in the same coherent slice.

## Child 25.1 Concurrent Admission Replan

Admission includes an explicit expected revision of the selected plan.
Planning owns the decision against that revision; Concurrency owns stale-read
and conditional-transition semantics. The serial integration owner alone may
change shared plan and ledger state. Delegated workers receive read-only plan
context and cannot advance lifecycle state.

Before transition or next-slice advancement, compare the authoritative current
revision with the admitted revision and apply the state change only when they
match. A mismatch is `invalid` stale admission and requires rereading the plan
and obtaining a new decision. Do not retry the old operation automatically.
This contract protects plan-state mutation; it does not reserve external
resources or authorize overlapping write sets.

Independent transitions may be planned or implemented concurrently only when
each has an admitted transition envelope and their exact scopes, bounded write
sets, dependencies, semantic outcomes, and verification contracts are
compatible. Overlap, contradictory outcomes, unmet dependencies, changed base
state, or missing compatibility facts reject admission with typed diagnostics.
Compatible concurrent preparation does not grant authority to integrate shared
state; plan, ledger, router, shared contracts, lockfiles, generated artifacts,
and other declared shared authority remain serial integration-owner writes.

Do not introduce lock files, reservations, leases, queues, heartbeats,
scheduler infrastructure, state-only Git commits, duplicate execution with
later reconciliation, or optimistic conflict acceptance as fallback. A future
reservation protocol requires measured downstream contention and a separate
replan; it is not implied by this admission contract.

## Child 25.1 Admission Revision Representation Replan

Planning owns a versioned `planning-admission-v1` digest over authoritative
current state: the selected repository-relative `plan.md` and its linked
repository-relative `issues.md`. `execution-ledger.md` remains append-only
evidence written with an accepted transition; it cannot independently
authorize admission and is not digest input.

Construct the digest from stable path ordering, an explicit presence marker,
the exact path bytes, unambiguous length-delimited framing, and exact artifact
bytes. The supported implementing environment selects a cryptographic digest
algorithm and records it with the scheme identifier. Do not normalize newlines,
use timestamps or filesystem metadata, depend on Git identity, omit a required
artifact, or infer an issues path.

A missing required artifact or digest input is `unavailable`; malformed or
contradictory framing, scheme, algorithm, or identity is `invalid`; an
unavailable supported cryptographic or conditional-update mechanism is
`unsupported`. Digest mismatch is stale `invalid` and is never retried
automatically. The digest identifies compared state but does not itself make
replacement atomic.

## Child 25.1 Transition Envelope Replan

Planning owns deterministic `planning-transition-v1` identity for each proposed
transition. Its length-delimited digest input contains the scheme identifier,
canonical repository-relative plan path, explicit operation, proposing actor,
prior `planning-admission-v1`, exact affected scope and bounded write set,
ordered prerequisite transition identities, intended semantic outcome and plan
state, intended resulting `planning-admission-v1`, and required verification
contract. Paths, sets, and dependency identities use one documented canonical
ordering; absent and empty values remain distinguishable. The implementing
environment records the supported cryptographic digest algorithm.

The actor identifies responsibility and evidence; it does not own the plan,
runtime resources, or shared integration authority. The envelope contains no
workflow input, mutable execution context, inferred defaults, timestamps,
filesystem metadata, or conversation state. Missing required facts are
`unavailable`; malformed identity, framing, ordering, operation, scope, or
outcome is `invalid`; an unavailable supported digest mechanism is
`unsupported`.

Concurrency owns compatibility decisions between admitted envelopes. Disjoint
write sets alone are insufficient: transitions must also have compatible
semantic outcomes, satisfied dependencies, unchanged admitted bases, and no
shared-authority conflict. A compatible decision permits bounded preparation
or implementation only. It never bypasses either revision gate or the serial
integration owner. Conflicts return typed affected scopes, transition
identities, and failed invariants; they are not merged, reordered, retried, or
resolved by latest-wins behavior.

Reconciliation receives a separate deterministic identity that references the
failed `planning-transition-v1`, observed inconsistent revisions, explicitly
selected remedy, current expected revision, intended result, authority, and
verification contract. It cannot reuse or mutate the failed identity. Neither
transition nor reconciliation identity creates a reservation or persistent
coordination lifecycle.

## Child 25.1 Revision-Checked Serial Integration Replan

The designated serial integration owner performs two revision gates: compare
`planning-admission-v1` immediately before mutating or staging the transition,
and compare it again immediately before commit or other authoritative
integration. This is optimistic integration validation, not atomic filesystem
or multi-file compare-and-swap.

The coherent staged transition contains the admitted operation, resulting plan
state, corresponding ledger evidence, any required issue-state change, and the
prior and resulting revision identities. Implementation owns those coherent
edits; Commit owns staged-scope and pre-integration review; Planning owns the
transition; Concurrency owns stale-decision rejection.

A mismatch at either gate is stale `invalid`: discard the admission decision,
reread authoritative state, and request new admission. Do not overwrite,
automatically retry, merge stale state, or apply latest-wins behavior.
Intermediate local disagreement is not accepted state and cannot be
integrated. This contract does not claim to prevent non-cooperating local edits.

## Child 25.1 Revision Evidence Replan

`execution-ledger.md` is the canonical, append-only owner for transition
evidence and remains outside `planning-admission-v1`. Each accepted transition
records the explicit operation, prior revision, resulting revision, resulting
plan state, resulting next-slice identity, integration owner, and applicable
integration evidence. A historical ledger entry never authorizes admission.

After preparing resulting `plan.md` and `issues.md`, compute their resulting
digest, write both revisions into the ledger entry, perform the pre-integration
gate against authoritative prior state, and integrate the coherent state and
evidence change. Post-integration verification recomputes the digest and must
match the recorded result before the transition is accepted.

Do not place a digest field in either digest input, exclude selected fields,
create a transition manifest, or make commit metadata the evidence owner.
Failure to integrate ledger evidence with the state change leaves the
transition unaccepted and requires explicit repair or re-evaluation; do not
report success from the state files alone.

## Child 25.1 Partial Integration Recovery Replan

When current `planning-admission-v1` does not match the applicable recorded
result, or transition evidence is missing, malformed, duplicated, or
contradictory, normal `start`, `continue`, and `verify` admission is
`unavailable`. Report the affected artifact paths, observed revisions, and
failed invariant. Do not execute work under the disputed transition.

The serial integration owner must explicitly select `complete-transition`,
`restore-prior-state`, or `supersede-transition`, provide exact candidate state
and the expected current revision, and pass the normal pre-mutation and
pre-integration gates. Recovery never reuses the original admission
automatically and never selects a remedy from timestamps, file precedence, or
apparent completeness.

Append reconciliation evidence identifying the failed transition evidence,
observed inconsistent state, selected remedy and authority, current and
resulting revisions, and verification result. Recompute the resulting digest
and confirm ledger agreement before clearing the diagnostic. Normal work
resumes only through a new explicit admission operation and revision.

Do not automatically roll back or complete, declare state-file-wins or
ledger-wins, delete contradictory evidence, select latest timestamps, or report
success while artifacts disagree. No recovery journal, transaction manager, or
new persistent lifecycle state is introduced.

## Re-plan Triggers

Stop if transition evidence cannot identify the applicable transition
unambiguously, compatibility cannot be decided from bounded canonical facts,
actor identity would confer resource or integration ownership, concurrent
admission requires a reservation or persistent coordination lifecycle,
authoritative integration cannot provide both revision gates, plan identity
requires repository-global mutable state, snapshot lineage must be regenerated,
the prompt needs an independent
lifecycle or generation system, copied canonical procedure must remain, one
identifier needs multiple dispositions, or implementation requires files
outside the approved write set.
