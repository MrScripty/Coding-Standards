# Platform Verification

**Standards metadata**

- ID: `workflow.verification.platforms`
- Role: `workflow`
- Level: `MUST`
- Applies when: A claim spans supported targets or requires platform-specific evidence.
- Does not apply when: The claim has no target-specific behavior or supported-platform evidence obligation.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/verification/platforms.md`

## Platform Evidence Coverage

For each declared platform-support claim, record every required target or
environment and map it to the evidence kind, environment qualification,
execution mode, and observed result that prove that claim. Required behavior
must be evidenced on every target whose real behavior is part of the support
contract. A build, simulation, or result from one target does not prove
different target behavior.

Best-effort and unsupported targets remain explicit and cannot satisfy a
required target entry. A best-effort failure may leave the required claim
accepted only when the support contract makes that target genuinely optional
and the result is still recorded.

Select local hooks, push or review checks, hosted or self-managed runners,
provider matrices, dedicated hardware, release gates, and manual procedures
from risk, cost, target availability, credentials, and release facts.
Failure fan-out and early termination are orchestration decisions; neither
`fail-fast` setting is universal. Different environments may use different
commands when they prove the same declared claim.

If any required target result is missing, failed, or blocked, acceptance
remains blocked. Contradictory support/evidence mappings are invalid, an
explicitly unsupported target is unsupported, and missing support, target,
environment, scheduling, or orchestration facts are unavailable.

Do not infer Linux and Windows, substitute current-platform compilation,
weaken a required target to best-effort, copy a provider matrix, or impose a
fixed pre-commit, pre-push, push, or pull-request schedule as fallback.
