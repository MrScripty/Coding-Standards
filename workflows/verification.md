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

For an ordinary regression, identify the reachable failure, assert the observable
result at its owner, and run affected checks. Reuse an existing test or a
construction guarantee when it already proves the claim. A focused regression
test does not require a separate admission record or a seven-part cost review.

Before adding costly, overlapping, brittle, or architectural evidence machinery
(such as a new validator, verifier, integrity system, snapshot framework, or
custom test harness), establish:

- the reachable failure and its material consequence;
- the claim, proof boundary, and adequate independent or authoritative oracle;
- what types, construction, static analysis, a deeper Interface, existing
  evidence, normal failure, or trace-led diagnosis already establish;
- the mechanism's marginal deciding value after that overlap;
- its implementation, execution, review, and maintenance cost;
- why exact byte identity is required when the mechanism compares or hashes
  bytes; and
- the condition for retaining, reviewing, replacing, or removing it.

Admit permanent machinery only when it supplies material deciding value that
the less costly alternatives do not. Impossibility by construction may close a
claim without dynamic validation. A contained internal defect with an adequate
ordinary failure and diagnostic path may remain an engineering diagnosis
responsibility when no accepted claim or risk requires earlier detection or
recovery. The possibility that a value or artifact could be wrong is not by
itself evidence that a permanent mechanism is necessary.

Overlapping evidence is valid defense in depth only when it addresses an
independent reachable failure or supplies distinct deciding value worth its
lifecycle cost. Remove or replace a mechanism when its claim is no longer
required, the failure is no longer reachable, another proof subsumes it, its
oracle is no longer adequate, or its retained cost is no longer proportionate.
Do not preserve it from sunk cost, convention, existing registration, or the
absence of a recent observed failure.

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

## Quality Gates And Execution Location

Derive each blocking or advisory gate from a named acceptance claim, affected
risk, owned contract, and required environment. State what it proves, its blocking
authority, and conditions for changing or removing it. Required gates must pass.

Run a claim where its inputs, environment, authority, and result are available.
Local, hook, CI, dedicated-runner, release, and manual execution are locations;
evidence meaning comes from the observed property. Incremental or staged checks
prove their selected scope.

Classify contradictory gate/claim authority as `invalid`, missing claim,
environment, scope, or blocking authority as `unavailable`, and a required claim
beyond supported execution as `unsupported`. Retain the affected acceptance
claim as unsatisfied until adequate evidence is available.

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

Select the smallest complete claim set that directly proves the objective,
plus supporting checks for affected risks and contracts.

| Change shape | Typical required claims |
| --- | --- |
| Local deterministic bug | `focused` |
| Multiple in-process modules | `integration` |
| Serialized, generated, FFI, IPC, or public boundary | `contract`, plus the consuming path when behavior matters |
| Cross-process or deployed backend capability | `system` |
| User-visible workflow | `user-workflow`, plus affected contracts |
| Hardware-dependent user capability | `user-workflow` in `required-real` environment |
| Shipped application or library | `release-artifact`, plus behavior claims changed by release |

Select every direct claim the objective needs and keep unrelated claims outside
the acceptance set.

## Simplicity Evidence Boundary

Verification can establish the selected behavior, contract, failure, and risk
claims of a design. Passing tests, type checks, schemas, generated freshness,
coverage, mutation checks, or formal review does not establish that the composed
artifact is simple. A comparison fixture may supply simplicity evidence only
when it actually examines Interface knowledge, interleaving, representative
change Locality, independent evolution, or deletion results. Keep that design
evidence distinct from reliability evidence.

## Acceptance Paths And Boundaries

For each non-local claim, name the observable start, externally meaningful
result, real in-scope boundaries, authoritative producers and consumers, and
material environment facts. Select `integration`, `contract`, `system`, or
`user-workflow` evidence from that path.

A cross-boundary objective usually needs a path claim plus separate claims for
contracts whose representation or invariants can regress independently. Verify
internal hops separately when they own such a claim. The path evidence proves
only the boundaries actually traversed.

Resolve an external-interface or environment assumption that could invalidate
the design through the smallest adequate real observation before expanding
implementation around it. Continue independently useful work when the unavailable
observation cannot change its decisions. Keep design-selection evidence distinct
from final acceptance.

For consumer-visible behavior, exercise the real producer and consumer through
their relevant interface and observe the complete promised result. A preview
establishes its preview behavior; full consumption requires observation of full
consumption.

Start with the smallest path producing a useful objective-level result and add
focused evidence for risky branches and independent contracts. Broaden when the
objective, consumers, environment, scale, or failure boundaries require it.
Select test sequencing and suite organization from those needs.

Classify contradictory path, authority, or boundary facts as `invalid`; a
declared path outside supported capability as `unsupported`; and missing
required boundaries, consumers, environment, or results as `unavailable`.
Retain the claim as unsatisfied until its actual boundaries and fidelity are
observed.

## Disabled Behavior Claims

Derive claims from [Implementation's selected lifecycle](implementation.md#disabled-and-incomplete-behavior).

For deliberate removal, prove that affected advertised, registered, configured,
persisted, and user-visible surfaces cease promising the capability and return
the declared typed outcome. For temporary disablement, prove surface-state
consistency, boundary outcomes, and accepted tracking, review, and re-enable or
removal criteria. For incomplete behavior, prove isolation from production
consumers, including isolation of test placeholders.

Select evidence kinds and environments from the affected surfaces. Documentation,
configuration, tracking, and behavior observations each prove their own property.
Keep acceptance blocked while a required surface, lifecycle fact, outcome, or
direct behavior claim is missing or contradicted.

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

For interactive graphical acceptance, follow [GUI Smoke Evidence](verification/gui.md#gui-smoke-evidence).

## Evidence Oracle Boundaries

When a change creates a validator, negative fixture, property test, differential test, or other independent oracle, follow [Evidence Oracle Boundaries](verification/oracles.md#evidence-oracle-boundaries).

## Negative Fixture Isolation

When a change creates a validator, negative fixture, property test, differential test, or other independent oracle, follow [Negative Fixture Isolation](verification/oracles.md#negative-fixture-isolation).

## Property And Differential Evidence

When a change creates a validator, negative fixture, property test, differential test, or other independent oracle, follow [Property And Differential Evidence](verification/oracles.md#property-and-differential-evidence).

## Test Design

Design each focused check around one coherent observable claim or invariant.
Use the assertions needed to prove it. Separate claims when their setup,
diagnosis, ownership, or lifecycle differs.

Make setup, action, observation, and cleanup reviewable. Choose a structure
suited to the claim and add explicit phases or comments when needed for clarity.

Select real implementations or controlled substitutes from the boundary being
proved. A substitute is adequate when its modeled contract is the intended proof
target or the claim explicitly excludes the substituted real boundary.

Derive examples and edge conditions from the actual domain, invariants, prior
defects, failure modes, transitions, resource/numeric limits, and consumer contracts.
Missing applicable boundary evidence is `unavailable`; contradictory test and
contract facts are `invalid`.

Use property or generative evidence when the claim owns a meaningful input-domain
property and generation, shrinking, reproducibility, and oracles can preserve it.
Use examples for named scenarios. Preserve the asserted objective, applicable
input domain, and required observation while repairing tests.

## Test Data Authority And Lifecycle

Identify the contract owning each material test-data field, identity, relation,
transition, and validity rule. Construct the data required by the claim and make
material values/defaults reviewable. Choose construction mechanisms from the data
contract, setup cost, reuse, diagnosis, and repository tooling.

Own fixture identity and lifetime independently of the workflow that created it.
Choose sharing, construction, synchronization, transactions, namespaces, reset,
and cleanup from mutation, concurrency, ordering, resource cost, and the proved
boundary. Shared mutable data requires an explicit owner, scope, initial state,
transitions, synchronization, reset/disposal, and failure recovery, with evidence
that exercises that lifecycle.

Establish material preconditions explicitly through their owners. A reused
fixture carries its defined data contract; establish the receiving check's inputs
and claim context independently. Preserve stable identity when required and
allocate distinct identity when parallel or repeated execution could collide.

Classify contradictory data authority, identity, isolation, or lifecycle as
`invalid`, unsupported required construction/isolation as `unsupported`,
and missing material ownership, reset, cleanup, synchronization, or environment
facts as `unavailable`. Observe the selected lifecycle property before acceptance.

## Async Completion And Failure Evidence

Observe asynchronous work through the terminal state and externally meaningful
result selected by its owner and contract. Choose the observation mechanism
that proves the applicable completion, failure, cancellation, timeout, or
continued-operation claim, including required child work, cleanup, publication,
and failure handling.

Derive cases from the owned state machine, error contract, retry/backoff policy,
cancellation/timeout semantics, partial-result rules, idempotency/compensation,
and diagnostics. Verify every material applicable outcome at the selected boundary.

At service or process boundaries, assert the externally owned representation and
effects: status or typed error, response/event, committed or compensated state,
retry termination, cancellation propagation, bounded completion, and safe
diagnostic context as applicable.

Classify contradictory completion, timing, boundary or error facts as `invalid`,
required observations beyond supported runtime/platform/harness capability as
`unsupported`, and missing ownership, terminal state, timing authority, boundary
representation or diagnostics as `unavailable`. Keep local observations scoped
to their local claims.

## Test Placement And Naming

Place evidence where its owner, affected implementation, fixtures, environment,
and discovery tools make it findable and executable. Follow language, framework,
runner, and build conventions. Keep related evidence and fixtures discoverable
without duplicating policy or creating hidden test-only APIs. Record placement
decisions when repository structure and tooling cannot explain them.

Use stable scenario, observable-result/invariant, and differentiating-condition
vocabulary in check names, with syntax appropriate to the tool and language.

Classify contradictory ownership/discovery as `invalid`, unsupported required
placement as `unsupported`, and missing discovery/tooling/execution facts as
`unavailable`. Resolve these requirements before relying on evidence discovery.

## Coverage And Durable Evidence Records

Use coverage to identify unexamined paths in instrumented execution. Evaluate
line, branch, function, condition, mutation, path, or other coverage for a named
risk or claim. Select scope, instrumentation, threshold, baseline, and exclusions
from history, generated/unreachable-code authority, risk, tooling accuracy, and
decision cost. State how each threshold or exclusion affects acceptance.

Record enough durable context to understand, reproduce, and review evidence
when the check, code, fixture, command, result, and canonical contract cannot
supply it. Keep defect origin, invariant reasoning, fixture authority, environment,
and result interpretation with their owning evidence or linked artifact.

Classify contradictory metric/scope/authority/threshold/exclusion/evidence as
`invalid`, unsupported instrumentation as `unsupported`, and missing material
baseline, tooling, authority or reproduction context as `unavailable`. Accept
behavior and boundary claims through their required observations.

## Scheduling And Duration

Risk, cost, and available environments determine where and when evidence runs.
Do not assign universal durations or require a kind to run only in CI.

Projects may schedule fast supporting checks per edit or commit and expensive
claims at pre-push, pull request, dedicated-runner, release, or manual gates.
Scheduling never changes what the evidence proves.

## Supporting Gates And Claim-Directed Diagnosis

Classify supporting checks by the exact property they observe. Treat a check
as acceptance when that property is the named claim; otherwise retain its role
as a supporting gate.

When evidence fails, preserve the command, environment, output, timing, and
boundary context required to reproduce the failure. Form a bounded hypothesis
and select the next observation by authority, information gain, cost,
reversibility, and proximity to the claim. After correction, rerun affected
evidence and broaden to claims or contracts the correction could have changed.

Select diagnostics, traces, state inspection, focused probes, dependency source,
generated artifacts, installed declarations, version-matched official
documentation, history, or external references when their authority and expected
information justify them. Preserve the objective and validation contract.
Add production diagnostics when their owned operational claim warrants them.

Classify contradictory claim/evidence/environment/authority as `invalid`,
observations beyond supported tools or environment as `unsupported`, and
missing reproduction facts, authoritative information, access, or observation
paths as `unavailable`. State the unresolved decision and continue independent
work under the current slice.

## Evidence Under An Existing Failing Baseline

Use evidence that still reaches and distinguishes the changed behavior. When
an existing failure prevents that observation, repair the obstruction, provide
a focused discriminator, or retain the affected claim as unverified.

Identify where execution stops and which claims remain observable. Compare the
actual findings using their owned identities and scope. Unchanged failure counts,
names, or source locations alone do not prove that the affected result was tested.

Keep explicit debt dispositions separate from acceptance. Name an owner and
executable procedure for any remaining environment-qualified observation.

## Platform Evidence Coverage

When a claim spans supported targets or requires platform-specific evidence, follow [Platform Evidence Coverage](verification/platforms.md#platform-evidence-coverage).

## Unavailable Evidence

When a required environment, credential, platform, or operator is unavailable,
run independent supporting checks, record the unsatisfied claim and owner, set
acceptance to `blocked` or `partial`, and keep the plan `Blocked` or
`Verifying` as applicable. Name the executable procedure and conditions needed
to obtain the remaining evidence. Accept the objective when all required claims
are satisfied.

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
