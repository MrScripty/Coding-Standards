# Implementation Workflow

**Standards metadata**

- ID: `workflow.implementation`
- Role: `workflow`
- Level: `MUST`
- Applies when: Source, tests, standards, configuration, or generated artifacts will change.
- Does not apply when: The task is read-only analysis.
- Requires: `core`
- Specializes: `none`
- Verification: Focused slice checks, staged-scope review, and objective acceptance.
- Canonical owner: `workflows/implementation.md`

## Before Editing

1. Inspect repository status and preserve unrelated work.
2. Identify one coherent behavior or contract change.
3. Declare the exact write set and acceptance evidence.
4. Resolve overlapping dirty work or ambiguous verification before editing.
5. Read routed standards and directly affected source context.

When a written plan governs the change, consume
[Planning's admission decision](planning.md#explicit-plan-admission). Bind the
task to one canonical repository-relative `plan.md` path and operation.
A human follow-up may reuse an unambiguous prior selection after current
repository state, plan lifecycle, and authority are checked. Obtain clarification
when that selection is missing or ambiguous. Machine interfaces retain their
explicit argument requirements.

Use the Concurrent Plan Integration profile's revision, stale-state,
compatibility, and reconciliation decisions when its actual applicability
conditions hold. Follow Planning's written-plan applicability: material sequencing,
independently owned contracts, migration, coordination, rollout, risk, or
acceptance complexity requires a plan when it cannot be held unambiguously in
the task. A bounded coherent change can state its exact write set inline.

## Slice Contract

Each slice must deliver one usable behavior, contract, or information-architecture
outcome; preserve the requested objective and canonical owners; provide the
declared outcomes when material facts cannot support a decision; include
focused regression or acceptance evidence; and leave coherent repository state.
Add compatibility, fallback, or duplicate-state mechanisms only for an actual
supported contract.

Keep a coherent change together. Split when separation materially improves
independent acceptance, risk containment, dependency ordering, conflict isolation,
rollback, or feedback. Add a directly affected file to the write set when the
objective, ownership, contract, risk, and acceptance meaning remain valid.
Record other relevant findings with severity, evidence, owner, and disposition.

Repair failed checks within the current slice while those decisions remain valid.
Replan when evidence changes them or shows that the slice cannot deliver its
outcome. For a shared invariant finding, bound the owner and reachable consumers
under [Planning](planning.md#systemic-finding-re-planning), disposition that
population, and resume at the supported decision boundary.

## Composed-Design Fidelity

Preserve the plan's admitted composition when its composed-design review applies.
Report observed caller knowledge, change propagation, or retained machinery that
contradicts the admission. Replan when that evidence changes the composition and
review the replacement against its current objective and acceptance.

## Editing

- Preserve unrelated changes.
- Update source and its focused evidence together.
- Regenerate derived artifacts from their source in the same slice.
- Remove superseded behavior once its replacement is accepted, with actual
  compatibility, retained-state, and cutover obligations dispositioned.
- Focus comments on non-obvious invariants, safety, and ownership.
- Establish explicit authority before destructive or permission-sensitive work.

## Disabled And Incomplete Behavior

Classify unavailable behavior before editing:

- remove deliberately unsupported capability from affected advertised and
  registered surfaces;
- represent temporary disablement explicitly at the owning boundary; or
- keep incomplete implementation unreachable from production consumers.

Temporary disablement identifies its owner, affected surfaces, reason, tracking
authority, re-enable or removal conditions, and a review or expiration trigger
when indefinite disablement is outside the product contract. Make that authority
discoverable to maintainers and affected consumers.

Keep flags, configuration, routes, commands, controls, and published capability
consistent with the selected lifecycle. Requested capability returns the owning
boundary's typed `unavailable`, `unsupported`, or `invalid` outcome when it
cannot be provided. Isolate test placeholders at the test boundary. Classify missing lifecycle ownership, tracking authority, or re-enable/removal
criteria as `unavailable` and resolve them before accepting the capability.

## Verification

Use [Verification](verification.md). Cover changed behavior and each affected
contract at its selected acceptance boundary and fidelity. Interpret build,
startup, and local checks within the properties they actually observe.

## Change-Description Evidence

Select reviewer and integrator context from affected risk, contracts, accepted
decisions, material alternatives, behavior, migration/operation consequences, and
Verification claims. Identify the owned artifact for each required fact and link
durable rationale.

Use the project's appropriate plan, change request, review, commit, issue, or
other owned artifact. Choose a review mechanism that can represent or link the
selected evidence. Require each item because it informs the affected decision;
keep routine context proportionate.

Classify contradictory evidence or ownership as `invalid`, missing required
context, rationale, evidence or owner as `unavailable`, and a mechanism unable
to convey the evidence as `unsupported`. Template completion proves only that
the template was completed.

## State And Findings

For an active plan, follow [Planning](planning.md). Keep objective, current
decisions, lifecycle, blockers, acceptance, and exactly one next slice current.
Update the ledger at accepted-slice boundaries and for material deviations or
verification results. Record findings in `issues.md`; replace superseded
decisions in current authority and preserve their history in the ledger.

Transition through `Implemented`, `Verifying`, and `Accepted` according to
the named evidence. Update planning artifacts when these facts change. Replan
for changed scope, ownership, objective, risk, or acceptance meaning.

Without an active plan, record out-of-scope issues in the normal repository
issue or review artifact.

## Commit Boundary

Follow [Commit](commit.md) for staging, branch/worktree applicability, integration,
history review, terminal lifecycle, cleanup, and rewrite authority. Implementation
owns the coherent slice. Preserve shared history and establish the explicit
authority required for history maintenance.
