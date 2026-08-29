# Plan: Active Fixture

**Plan status:** `Active`

**Current phase:** Milestone 0

**Next slice:** Implement the focused parser correction.

**Acceptance status:** `pending`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Reject empty identifiers.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Focused regression test rejects an empty identifier. | `contract` | `not-applicable` | `automated` | `pending` | `pending` |

## Binding Decisions

- Parser owns identifier validation.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: Parsing and identifier validation remain distinct but composed through one parser Interface.
- State, identity, value, time, policy, and mechanism: Identifier value policy is contained by the parser and introduces no state or time coupling.
- Caller and composition-root knowledge: Callers provide source text and do not know identifier-validation mechanics.
- Representative change paths and forced owners: Changing the empty-identifier rule changes only parser-owned validation and its focused evidence.
- Stable Interfaces versus hidden knowledge: The parser Interface hides identifier representation and validation ordering.
- Independent evolution, testing, failure, and replacement: The validation rule can be tested and replaced without changing callers.
- Necessary complexity and containment: The single validation branch is necessary and contained in the parser Module.
- Deletion and cumulative machinery result: No pass-through owner or duplicate verifier remains after the correction.

## Milestones

### Milestone 0: Parser

**Status:** `Active`

## Blockers

- `none`

## Re-Plan Triggers

- Validation is owned by a different boundary.

## Final Acceptance

- Objective evidence: `pending`
