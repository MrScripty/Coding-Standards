# Plan: Blocked Fixture

**Plan status:** `Blocked`

**Current phase:** Hardware acceptance

**Next slice:** Run the user workflow on the required device.

**Acceptance status:** `blocked`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Deliver a hardware-backed user capability.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Recorded real-device workflow succeeds. | `user-workflow` | `required-device` | `manual` | `blocked` | `pending` |

## Binding Decisions

- Simulation cannot accept the hardware objective.

## Milestones

### Milestone 0: Headless path

**Status:** `Implemented`

### Milestone 1: Hardware path

**Status:** `Blocked`

## Blockers

- Required device is unavailable.

## Re-Plan Triggers

- Supported hardware contract changes.

## Final Acceptance

- Objective evidence: `pending`
