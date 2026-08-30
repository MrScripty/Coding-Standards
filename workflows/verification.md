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

Before adding a permanent test, validator, verifier, integrity check, hash,
snapshot, contract, or other evidence mechanism, establish:

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
risk, owned contract, and required environment. Record what the gate proves,
its blocking authority, and the conditions for changing or removing it. A gate
must pass when its selected claim is required; no catalog of lint, type,
formatting, test, documentation, or traceability checks is universally
mandatory.

Execution location does not create an evidence hierarchy. Run the claim where
its required inputs, environment, authority, and observable result are
available, whether local, in a hook, in CI, on a dedicated runner, during
release verification, or through a recorded manual procedure. Incremental or
staged checks prove only their selected scope and cannot substitute for a
broader required claim.

Contradictory gate and claim authority is `invalid`. Missing claim, environment,
scope, or blocking authority is `unavailable`. A required claim outside
supported execution capability is `unsupported`; do not replace it with a
conventional gate list, CI execution, local success, a weaker check, or default
acceptance.

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
`user-workflow` evidence from that path. Repository suite labels such as unit,
integration, end-to-end, or vertical slice are organization mechanisms; they
do not establish evidence kind, environment fidelity, or acceptance.

A cross-boundary objective usually needs one path claim plus separate contract
claims for boundaries whose representation or invariants can regress
independently. The path claim proves only the boundaries it actually traverses.
Do not require assertions for every internal hop unless that hop owns a
separate claim, and do not infer complete-path behavior from isolated producer,
consumer, adapter, type, build, or startup results.

Start with the smallest path that produces a useful objective-level result,
then add focused evidence for risky branches and independently owned contracts.
This sequencing is a planning mechanism, not a universal requirement to write
one test first or to use one suite shape. Broaden the path when the objective,
consumers, environment, scaling behavior, or failure boundaries require it.

Contradictory path, authority, or boundary facts are `invalid`. A declared path
outside supported product or platform capability is `unsupported`. A missing
required boundary, consumer, environment, or observable result is
`unavailable`. Do not substitute a realistic simulation for required-real
evidence, a lower-fidelity suite for the selected claim, a successful build or
smoke, partial traversal, checklist completion, or default success.

## Disabled Behavior Claims

Derive acceptance claims from the lifecycle state selected by
[Implementation](implementation.md#disabled-and-incomplete-behavior).

For deliberate removal, prove that every affected advertised, registered,
configured, persisted, and user-visible surface no longer promises the
capability and that requests receive the declared typed outcome. For temporary
disablement, prove surface-state consistency, the owning boundary's typed
outcome, and the accepted tracking, review, and re-enable or removal criteria.
For incomplete behavior, prove it is unreachable from production consumers and
that any test-only placeholder remains isolated by the test boundary.

Select evidence kinds and environments from the affected surfaces. A focused
configuration check may prove one local state but cannot prove a public,
deployed, or user-visible surface. Documentation, a tracking issue, a feature
flag, or a workaround proves only its explicit claim and never substitutes for
observable disabled behavior.

Acceptance remains blocked when a required surface, lifecycle fact, typed
outcome, or direct behavior claim is missing or contradicted. Do not mark a
disabled capability accepted from checklist completion, issue existence,
documented intent, startup success, a production stub, or substitute behavior.

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

## Evidence Oracle Boundaries

For each acceptance claim, identify the observation mechanism and the exact
property it can decide. The expected property must come from authority
independent of the subject under test. Two projections that share one semantic
implementation can prove agreement with each other, but not conformance to an
external contract.

Keep these evidence boundaries explicit:

- deterministic generation proves freshness from the selected source, not
  semantic completeness;
- an exact literal proves literal identity only when literal identity is the
  contract;
- coordinated edits to a subject and a copied expectation do not provide an
  independent oracle; and
- mutation evidence proves detection of the sampled mutations, not complete
  detection outside the sampled domain.

When the required claim has no independent or otherwise authoritative oracle,
return `unavailable`. When the mechanism cannot decide the claimed property,
the evidence is `invalid`. Do not upgrade local agreement, freshness, parsing,
snapshot equality, or a passing harness into a stronger conformance claim.

## Negative Fixture Isolation

A negative fixture proves its intended failure only when every unrelated
precondition is valid and the observed result identifies the expected
diagnostic or failure point. Record the expected typed diagnostic and the
relevant complete message or structured fields when those details distinguish
the target failure from earlier validation failures.

Construct the fixture from a valid case by changing only the condition under
test where practical. A nonzero exit, thrown exception, generic rejection, or
substring match is insufficient when several validators can reject the same
input. If the fixture cannot reach the intended boundary, classify the
evidence as `invalid`; do not count incidental failure as acceptance.

## Property And Differential Evidence

Property, generative, mutation, and differential evidence must name:

- the property being tested;
- the generated or sampled input domain;
- the independent or authoritative oracle;
- the compared implementations or projections;
- reproducibility and shrinking behavior where applicable; and
- the unsupported or unexamined domain.

Comparison between local implementations proves consistency only unless an
independent authority establishes expected semantics. External conformance
claims require the selected specification, reference implementation, official
corpus, or another authority that is independent of the implementations being
compared. A sampled counterexample can disprove a universal claim; absence of
one does not prove completeness beyond the declared domain.

Return `unsupported` when the selected oracle or corpus does not cover a
well-formed required domain and `unavailable` when required authority or
reproducibility inputs cannot be obtained. Do not silently narrow the claim to
the cases a generator or local comparator happens to support.

## Test Design

Design each focused check around one coherent observable claim or invariant.
One check may need several assertions to prove that outcome; several claims may
need separate checks when their setup, failure diagnosis, ownership, or
lifecycles differ. Do not split or combine checks to satisfy a slogan about one
assertion or one behavior.

Structure setup, action, observation, and cleanup so the causal path and failed
criterion are reviewable. Arrange-Act-Assert, Given-When-Then, tables, state
machines, generators, or another structure are mechanisms selected from the
claim. Comments and explicit phases are required only when the test is not
otherwise clear.

Select real implementations, fakes, simulators, fixtures, mocks, or controlled
substitutes from the boundary being proved. A substitute is valid only when its
modeled contract is the intended proof target or the claim explicitly excludes
the real boundary. Do not use a mock to claim behavior of the mocked boundary,
and do not impose a universal real/fake/mock preference hierarchy.

Derive examples and edge conditions from the input domain, invariants, prior
defects, failure modes, state transitions, numeric or resource boundaries, and
consumer contracts. Empty, null, minimum, maximum, malformed, duplicate, and
failure inputs are not universal requirements when they are outside that
domain. Missing applicable boundary evidence is `unavailable`; contradictory
test and contract facts are `invalid`.

Use property-based or generative evidence when a property over a meaningful
input domain is the claim and generation, shrinking, reproducibility, and
oracles can preserve it. Example-based evidence remains valid for named
scenarios. Do not require property testing from an algorithm label, roundtrip,
inverse operation, or “all valid inputs” slogan without an owned property and
usable oracle.

Never weaken an assertion, narrow an input domain, replace the real objective
with substitute behavior, or accept successful execution as default success.

## Test Data Authority And Lifecycle

Identify the contract that owns each material test-data field, identity,
relationship, state transition, and validity rule. Construct only the data
needed by the claim while keeping material values and defaults reviewable.
Factories, builders, direct construction, generators, snapshots, seeded stores,
and external fixtures are mechanisms selected from the data contract, setup
cost, reuse, diagnosis, and repository tooling; none is a default hierarchy.

Define fixture identity and lifetime independently from the workflow or check
that first created it. Select immutable sharing, per-check construction, scoped
mutable sharing, transactions, namespaces, reset, cleanup, or another isolation
mechanism from mutation, concurrency, ordering, resource cost, and the proved
boundary. Shared mutable data is valid only when its owner, scope, synchronization,
initial state, transitions, reset or disposal, and failure recovery are explicit
and the selected evidence exercises that lifecycle.

Do not let a factory default, prior check, ambient database, clock, random seed,
process-global cache, external account, or persisted artifact silently supply a
material precondition. A reused fixture carries no originating check input or
claim context into another check. Preserve stable identity only when the claim
requires it, and allocate or derive distinct identity when parallel or repeated
execution could collide.

Contradictory data authority, identity, ownership, isolation, or lifecycle facts
are `invalid`. A required construction or isolation mechanism outside supported
repository or platform capability is `unsupported`. Missing material authority,
identity, reset, cleanup, synchronization, or environment facts are
`unavailable`. Do not substitute factory use, fresh allocation, transaction
rollback, cleanup success, test ordering, serial execution, or passing retries
for the required claim.

## Async Completion And Failure Evidence

Observe asynchronous work through the terminal state and externally meaningful
result selected by its owner and contract. Awaiting, joining, subscribing,
polling, callbacks, clocks, harness drains, and process observation are
mechanisms; use the one that proves completion, failure, cancellation, timeout,
or continued operation at the required boundary. Syntax that starts or awaits
work does not prove that child work, cleanup, publication, or failure handling
has completed.

Derive outcome cases from the owned state machine, error contract, retry and
backoff policy, cancellation and timeout semantics, partial-result rules,
idempotency or compensation behavior, and diagnostic channel. A success case
and a failure case are not a universal pair. Verify only applicable outcomes,
but do not omit a material terminal state or boundary because a lower-cost
focused check, build, startup, or generic exception assertion passed.

At a service or process boundary, assert the externally owned representation
and effects: status or typed error, response or event, committed or compensated
state, retry termination, cancellation propagation, bounded completion, and
safe diagnostic context as applicable. Internal exception types, mock call
counts, sleeps, or implementation callbacks prove only their explicit local
claims and cannot substitute for the selected boundary.

Contradictory completion, terminal-state, boundary, timing, or error-contract
facts are `invalid`. A required observation mechanism or outcome outside the
supported runtime, platform, or harness capability is `unsupported`. Missing
material completion ownership, terminal states, timing authority, boundary
representation, or diagnostic facts are `unavailable`. Do not fall back to
await syntax, happy-path completion, one generic failure, arbitrary sleeps,
test-runner exit, retry success, or weaker-boundary evidence.

## Test Placement And Naming

Place evidence where its owner, affected implementation, fixtures, environment
setup, and repository discovery tools make it findable and executable. The
selected boundary may be a source module, package, test root, contract fixture
area, system harness, or another repository-defined location. One repository
may use several placements when their ownership and execution contracts differ.

Follow required language, framework, runner, and build discovery conventions.
Within those constraints, keep related evidence and fixtures close enough that
maintainers can discover the claim and its owner without duplicating policy or
creating hidden test-only APIs. Document a placement decision only when it is
not recoverable from repository structure and tooling.

Name a check with the narrowest stable vocabulary that identifies its scenario,
observable result or invariant, and differentiating conditions. Names support
discovery and diagnosis; they do not need to encode every function, phase,
input, or expected value. Select syntax from the applicable tool and language.

Contradictory ownership or discovery requirements are `invalid`. Unsupported
runner or platform placement is `unsupported`. Missing ownership, discovery,
tooling, or execution facts are `unavailable`. Do not choose colocated,
mirrored-tree, hybrid, suite-level directories, README documentation, or a
`function_scenario_result` template as fallback.

## Coverage And Durable Evidence Records

Coverage reports where instrumented execution did or did not traverse code. It
is a diagnostic for finding unexamined paths and does not prove observable
behavior, boundary agreement, environment fidelity, assertion quality, or
objective acceptance by itself.

Use line, branch, function, condition, mutation, path, or other coverage only
when it helps evaluate a named risk or claim. Select scope, instrumentation,
threshold, baseline, and exclusions from repository history, generated and
unreachable-code authority, risk, tooling accuracy, and decision cost. Record
why a threshold or exclusion affects acceptance; do not infer quality from a
percentage or copy a conventional exclusion list.

Record the smallest durable context needed to understand, reproduce, and
review evidence when that context cannot be recovered from the check name,
code, fixture, command, result, or canonical contract. Useful context may
include the originating defect, non-obvious invariant, fixture shape authority,
material environment facts, or interpretation of a measured result. Put it at
the owning evidence or linked artifact rather than requiring an inline comment,
diagram, table, README section, or copied template.

Contradictory metric, scope, authority, threshold, exclusion, or evidence facts
are `invalid`. Unsupported instrumentation is `unsupported`. Missing material
baseline, tooling, authority, or reproduction context is `unavailable`. Do not
substitute high coverage, target attainment, documented intent, a fixture
diagram, or successful instrumentation for the required claim.

## Scheduling And Duration

Risk, cost, and available environments determine where and when evidence runs.
Do not assign universal durations or require a kind to run only in CI.

Projects may schedule fast supporting checks per edit or commit and expensive
claims at pre-push, pull request, dedicated-runner, release, or manual gates.
Scheduling never changes what the evidence proves.

## Supporting Gates And Claim-Directed Diagnosis

Classify every formatter, linter, static analysis, compilation, build, package,
startup, dev-server, runtime, source lookup, or documentation check by the exact
property it observes. Treat it as acceptance only when that property is itself
the named claim; otherwise it is a supporting gate and cannot replace focused,
contract, system, user-workflow, or release-artifact evidence.

When evidence fails or a claim remains unresolved, preserve the exact command,
environment, output, timing, and boundary context needed to reproduce it. Form
the smallest hypothesis consistent with those facts and select the next
observation by authority, information gain, cost, reversibility, and proximity
to the failed claim. Re-run affected evidence after correction and broaden only
to claims or contracts the correction could have changed.

Use compiler diagnostics, traces, logs, state inspection, focused probes,
dependency source, generated artifacts, installed declarations, official
version-matched documentation, repository history, or external references when
their authority and expected information justify them. No source order is
universal. Do not add production diagnostics, weaken validation, change the
objective, or repeatedly edit and retry merely to obtain a passing result.

Contradictory claim, evidence, environment, or authority facts are `invalid`.
An observation unavailable in the supported toolchain or environment is
`unsupported`. Missing reproduction facts, authoritative contract information,
required access, or a usable observation path is `unavailable`. Report the
typed diagnostic instead of falling back to a fixed layer order, compile/build/
launch loop, dev-server success, generic web search, checklist completion, or
default acceptance.

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
