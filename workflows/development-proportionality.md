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

Development effort must be proportionate to decision-relevant uncertainty and
the consequence it can prevent. Reuse an established mechanism that satisfies
the affected requirements. Reconsider it for an evidenced mismatch in behavior,
ownership, safety, compatibility, or cost.

Once the design satisfies the admitted product contract and applicable standards,
prefer the smallest reversible production implementation unless a named unresolved
issue threatens an irreversible or high-consequence outcome. Keep investigation
cost within the plausible rework or consequence it can prevent. Quantify more
closely when the measurement could change the decision and costs less than the
reversible action.

This workflow owns the next development action. Architecture owns design admission;
Verification owns claims and evidence value; Planning owns sequencing and plan
maintenance. Preserve the user's explicit design choices and admitted contract.

## Development Decision

Identify the current contract, design conformance, exact uncertainty, decision it
could change, consequence of error, reversibility, and least costly adequate method.
Choose one outcome:

### Implement

Choose `implement` when the design satisfies the contract and standards and
implementation is reversible without a plausible high-consequence outcome.
Implementation can itself be the cheapest reliable observation.

### Investigate

Choose `investigate` when a bounded investigation can resolve a missing fact
preventing a conforming design.

For an already conforming design, investigate only when the uncertainty could
change the current decision, error could cause irreversible/high-consequence
harm or implementation would plausibly cost more, and the investigation has
a named decision, adequate method, and observable stopping condition.

### Defer And Implement

Choose `defer-and-implement` when a valid concern cannot change the current
admitted decision. Preserve a durable follow-up when Planning or issue management
requires it.

### Blocked

Choose `blocked` when missing authority, information, or external state prevents
implementation from satisfying the contract or standards. State the missing
requirement precisely. Keep decision-changing unknown facts `unavailable` and
contradictory facts `invalid` under the applicable diagnostic contract.

## Investigation Admission

Before an investigation delays implementation, name its uncertainty, affected
decision, plausible consequence prevented, cost comparison with implementation,
least costly adequate method, and stopping condition.

Absent that basis, continue reversible implementation of an already conforming
design. End the investigation at its stopping condition and return to the
Development Decision. Evaluate adjacent uncertainty on its own decision relevance.

## Boundary And Stopping Rules

Expand or block the slice for findings that invalidate its product contract,
demonstrate a standards violation in its design, or materially change the
reversibility or consequence assessment.

Keep review within the admitted decision boundary. After required contract and
standards checks pass, require further evidence only for a newly established
decision-relevant claim or risk.

## Handoff

- `implement`: proceed through Implementation and selected Verification.
- `investigate`: answer one bounded question and reconsider the development decision.
- `defer-and-implement`: proceed with the admitted slice and its required follow-up.
- `blocked`: identify the missing authority, information, or external-state change.
