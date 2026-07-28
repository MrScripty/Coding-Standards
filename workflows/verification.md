# Verification Workflow

**Standards metadata**

- ID: `workflow.verification`
- Role: `workflow`
- Level: `MUST`
- Applies when: A behavior, contract, artifact, or standards change requires evidence.
- Does not apply when: The task is read-only and makes no acceptance claim.
- Requires: `core`
- Specializes: `none`
- Verification: The routed scenario names evidence at the same fidelity as its objective.
- Canonical owner: `workflows/verification.md`

## Select Evidence From The Objective

Name the acceptance criterion before implementation. Select the lowest-cost
evidence that directly proves it, plus supporting checks for affected contracts.

| Change shape | Minimum direct evidence |
| --- | --- |
| Local deterministic bug | Focused regression test |
| Multiple in-process modules | Integration test through their real interface |
| Serialized, generated, FFI, IPC, or public contract | Producer and consumer contract test |
| Cross-process or full backend capability | System test through real boundaries |
| User-visible workflow | User interaction through UI to visible result |
| Hardware/environment-dependent capability | Recorded real-environment acceptance |
| Shipped artifact | Built artifact smoke on a representative clean environment |

These levels are not interchangeable. Supporting unit tests or startup smoke
cannot close a user-workflow criterion.

## Small Local Bug Fix

For the S1 Rust library parser defect:

1. Add a regression test that demonstrates the invalid empty identifier.
2. Implement the smallest correction in the parser's canonical owner.
3. Run the focused test.
4. Run affected Rust formatting, lint, type/build, and package tests selected by
   the Rust profile.
5. Do not route unrelated E2E, release, UI, launcher, interop, or persistence
   checks.

## Test Design

- Assert observable behavior, not implementation trivia.
- Include the failure mode or boundary invariant that could regress.
- Keep fixtures deterministic and isolate shared mutable or durable resources.
- Do not weaken an assertion to match an incorrect implementation.
- Avoid mocks when the objective is the behavior of the mocked boundary.
- Use the repository's established test placement and naming convention unless
  that convention prevents the selected evidence.

Detailed test organization remains in
[TESTING-STANDARDS.md](../TESTING-STANDARDS.md) until Milestone 4 completes its
migration. This workflow is canonical for evidence selection and acceptance
fidelity.

## Unavailable Evidence

If required hardware, credentials, platform, or environment is unavailable:

- run independent lower-level checks;
- record the missing acceptance criterion and owner;
- keep status `Verifying` or `Blocked`; and
- do not mark the objective accepted.

Simulation is valid evidence only for the contract it actually models.

## Reporting

Record:

- criterion and verification level;
- command or procedure;
- pass, fail, blocked, or not applicable;
- environment when material; and
- unresolved risk.

Detailed logs belong in CI artifacts, reports, or an execution ledger, not the
active plan or commit message.
