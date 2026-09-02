# Development Proportionality Workflow

**Standards metadata**

- ID: `workflow.development-proportionality`
- Role: `workflow`
- Level: `MUST`
- Applies when: Development work is being planned, or an additional prototype, design investigation, evidence cycle, review, or re-plan could delay implementation.
- Does not apply when: Work is read-only and makes neither an implementation decision nor a development-sequencing decision.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Development-decision fixtures and metadata-route closure.
- Canonical owner: `workflows/development-proportionality.md`

Development effort must remain proportionate to the decision-relevant
uncertainty and the consequence it can prevent. Once the current design
satisfies the admitted product contract and applicable standards, prefer the
smallest reversible production implementation over further design
investigation unless a named unresolved issue threatens an irreversible or
high-consequence outcome.

Do not spend more effort reducing uncertainty than the plausible rework or
consequence that effort can prevent. This is a qualitative decision unless a
closer measurement could plausibly change the outcome and is cheaper than
taking the reversible action. Do not create measurement or review machinery
merely to justify continuing investigation.

This workflow owns whether the next development action is `implement`,
`investigate`, `defer-and-implement`, or `blocked`. It does not replace:

- Architecture's admission and machinery tests;
- Verification's claim, evidence-value, and evidence-budget decisions;
- Planning's sequencing and plan-maintenance rules; or
- the user's explicit design choices and admitted product contract.

## Development Decision

Identify only the facts needed for the current decision:

1. the admitted product contract for the current slice;
2. whether the current design satisfies that contract and the applicable
   standards;
3. the exact unresolved uncertainty;
4. the current implementation decision that its answer could change;
5. the plausible consequence of making that decision incorrectly now;
6. whether the production implementation is reversible; and
7. the least costly adequate way to resolve the uncertainty.

Choose exactly one outcome:

### Implement

Choose `implement` when the design satisfies the current product contract and
applicable standards, and implementation is reversible without a plausible
high-consequence outcome. Implementation is itself admissible evidence when
it is the cheapest reliable way to expose the remaining uncertainty.

### Investigate

Choose `investigate` when the current design does not yet satisfy the admitted
contract but a bounded investigation can resolve the missing design fact.

When the design already satisfies the contract, choose `investigate` only when
all of the following are true:

- the uncertainty could change the current implementation decision;
- getting the decision wrong could cause an irreversible or high-consequence
  outcome, or implementation-first is plausibly more costly than a bounded
  investigation; and
- the investigation has a named decision, the least costly adequate method,
  and an observable stopping condition.

### Defer And Implement

Choose `defer-and-implement` when a concern is valid but cannot change the
current admitted decision. Preserve it only when the applicable Planning or
issue-management workflow requires a durable follow-up.

### Blocked

Choose `blocked` only when implementation cannot satisfy the current product
contract or an applicable standard without missing authority, information, or
an external-state change. Report the missing requirement precisely.

Unknown or contradictory facts that can change the outcome are `unavailable`
or `invalid`; do not replace them with a convenient default.

## Investigation Admission

Every prototype, design review, evidence cycle, or re-plan that would delay
implementation must name:

- the uncertainty being reduced;
- the decision its result could change;
- the plausible consequence prevented;
- why implementation-first is not the cheaper adequate test;
- the least costly adequate method; and
- an observable stopping condition.

If an item is absent, the investigation must not block a reversible
implementation whose design already satisfies the admitted contract and
applicable standards. An admitted investigation ends when its stopping
condition is met; discovering adjacent uncertainty does not automatically
renew it.

## Boundary And Stopping Rules

An adjacent finding may expand or block the current slice only when it:

- invalidates the admitted product contract;
- demonstrates a standards violation in the current design; or
- materially changes the reversibility or consequence assessment.

Keep review findings within the admitted decision boundary. After the required
contract and standards checks pass, do not create new evidence obligations
merely because another investigation could produce more confidence.

A completed investigation returns to the Development Decision. It does not
authorize another investigation by itself.

## Handoff

- `implement` hands the admitted slice to Implementation and its selected
  Verification.
- `investigate` hands one bounded question to the cheapest adequate method,
  then returns to the Development Decision.
- `defer-and-implement` leaves the admitted slice unchanged.
- `blocked` reports the missing authority, information, or external-state
  change.
