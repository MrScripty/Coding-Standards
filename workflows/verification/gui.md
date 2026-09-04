# GUI Verification

**Standards metadata**

- ID: `workflow.verification.gui`
- Role: `workflow`
- Level: `MUST`
- Applies when: A graphical user workflow requires smoke evidence.
- Does not apply when: No graphical workflow claim is affected.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: GUI smoke decisions and the real affected interaction path.
- Canonical owner: `workflows/verification/gui.md`

## GUI Smoke Evidence

When a smoke procedure launches a GUI or desktop runtime, qualify the claim
against the environment and execution mode that materially affect startup.
Record applicable display or session capability, sandbox policy, graphics
capability, shared-memory or equivalent resource constraints, state isolation,
and bounded process-lifecycle behavior. Select mechanisms only after these
facts and the supported target contract are known.

CI-specific display servers, software rendering, sandbox flags, resource
limits, or process wrappers are valid only when the selected smoke environment
requires them and the procedure records their effect on the claim. Keep a
verification-only procedure separate from normal interactive startup when
their runtime contracts differ. Do not silently weaken the user runtime,
inherit an operator desktop session, or choose a conventional virtual display,
graphics mode, sandbox setting, shared-memory workaround, or timeout.

The application launcher may expose and transport the selected procedure, but
Verification owns its evidence kind, environment qualification, execution
mode, assertions, and acceptance result. A local reproduction is supporting
evidence unless its environment satisfies the same material facts. Undeclared
runner behavior, missing required capability, premature exit, failed
assertions, or an environment mismatch blocks the claim with the applicable
typed diagnostic; it does not fall back to startup-only evidence, another
environment, or default success.
