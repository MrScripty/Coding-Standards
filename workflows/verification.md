# Verification Workflow

**Standards metadata**

- ID: `workflow.verification`
- Role: `workflow`
- Level: `MUST`
- Applies when: A behavior, contract, artifact, or standards change requires evidence.
- Does not apply when: The task is read-only and makes no acceptance claim.
- Requires: `core`
- Specializes: `none`
- Verification: Acceptance-claim fixtures and objective-level evidence review.
- Canonical owner: `workflows/verification.md`

## Acceptance Is A Set Of Claims

Name the observable claims that must be true before implementation. Each claim
has three independent dimensions:

1. evidence kind;
2. required environment; and
3. execution mode.

An objective may require several claims. Evidence satisfies only the claim it
actually proves. Do not compare unrelated kinds as one scalar hierarchy.

## Evidence Kinds

| Kind | Claim proved |
| --- | --- |
| `focused` | One local behavior or invariant in its canonical owner. |
| `integration` | Multiple components collaborate correctly through their real in-scope interfaces. |
| `contract` | A producer and consumer agree on a serialized, generated, FFI, IPC, persisted, or public contract. |
| `system` | A capability works through its real process, service, or deployment boundaries. |
| `user-workflow` | A user action reaches the externally visible result through the real interaction path. |
| `release-artifact` | The built, packaged, installed, or published artifact has the named property. |

Kinds describe different proof targets. A contract check does not prove a user
workflow. A system check does not prove packaging. A release startup smoke does
not prove feature behavior unless the smoke procedure actually performs and
asserts that feature workflow.

Static analysis, formatting, linting, compilation, and build checks are
supporting gates unless the objective is specifically the property they prove.

## Environment Qualification

Each claim names one environment requirement:

| Environment | Meaning |
| --- | --- |
| `not-applicable` | The claim is deterministic and has no material environment dependency. |
| `simulated` | A controlled substitute is the intended proof target. |
| `representative` | The claim requires a supported environment representative of real use. |
| `required-real` | Named hardware, platform, service, credential, or deployment facts must be present. |

Simulation proves only its modeled contract. It cannot satisfy a
`required-real` claim.

## Execution Mode

Each claim names one mode:

| Mode | Meaning |
| --- | --- |
| `automated` | A repeatable tool or test produces the evidence. |
| `manual` | A named operator procedure produces recorded evidence. |
| `either` | Either mode is acceptable for this claim. |

Manual execution is not stronger than automation. Use it when human perception,
physical interaction, or unavailable automation is part of the acceptance
criterion. Record the procedure, environment, result, and operator or evidence
owner.

## Selecting Claims

Select the smallest complete claim set that directly proves the objective, plus
supporting checks for affected risks and contracts.

| Change shape | Typical required claims |
| --- | --- |
| Local deterministic bug | `focused` |
| Multiple in-process modules | `integration` |
| Serialized, generated, FFI, IPC, or public boundary | `contract`, plus the consuming path when behavior matters |
| Cross-process or deployed backend capability | `system` |
| User-visible workflow | `user-workflow`, plus affected contracts |
| Hardware-dependent user capability | `user-workflow` in `required-real` environment |
| Shipped application or library | `release-artifact`, plus behavior claims changed by the release |

Do not require an unrelated high-cost claim. Do not omit a direct claim because
a cheaper supporting gate passed.

## Smoke Checks

A smoke check proves only its explicit narrow assertions, such as:

- an artifact installs;
- a process starts and remains healthy for a bounded observation;
- a library loads from its package; or
- one named minimal operation succeeds.

Label the smoke by evidence kind and asserted behavior. Startup alone is usually
`release-artifact` evidence and never substitutes for `system` or
`user-workflow` behavior.

### GUI Smoke Evidence

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

## Test Design

- Assert observable behavior, not implementation trivia.
- Include the failure mode or boundary invariant that could regress.
- Keep fixtures deterministic and isolate shared mutable or durable resources.
- Do not weaken an assertion to match an incorrect implementation.
- Avoid mocks when the objective is the behavior of the mocked boundary.
- Use the repository's established test placement and naming convention unless
  that convention prevents the selected evidence.

Detailed test organization remains in
[TESTING-STANDARDS.md](../TESTING-STANDARDS.md). This workflow is canonical for
claim selection and acceptance; the testing document owns test-design
techniques.

## Scheduling And Duration

Risk, cost, and available environments determine where and when evidence runs.
Do not assign universal durations or require a kind to run only in CI.

Projects may schedule fast supporting checks per edit or commit and expensive
claims at pre-push, pull request, dedicated-runner, release, or manual gates.
Scheduling never changes what the evidence proves.

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

## Unavailable Evidence

If a required environment, credential, platform, or operator is unavailable:

- run independent supporting checks;
- record the unsatisfied claim and owner;
- set acceptance to `blocked` or `partial`;
- keep plan status `Blocked` or `Verifying` as applicable; and
- do not mark the objective accepted.

Do not invent fallback evidence or infer environment facts.

## Reporting

For each required claim record:

- stable claim identifier and observable criterion;
- evidence kind, environment, and execution mode;
- command or procedure;
- `pending`, `blocked`, or `satisfied`;
- evidence location and environment facts when material; and
- unresolved risk.

Detailed logs belong in CI artifacts, reports, or an execution ledger, not the
active plan or commit message.
