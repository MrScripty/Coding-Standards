# Tooling Workflow

**Standards metadata**

- ID: `workflow.tooling`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects, configures, schedules, or coordinates development tools or automation.
- Does not apply when: No development-tool selection, configuration, scheduling, or orchestration behavior changes.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Tool selection, hook orchestration, scheduling, cost, and persisted-artifact decision fixtures plus affected real automation evidence.
- Canonical owner: `workflows/tooling.md`

## Tooling Authority

Select tooling from owned repository contracts, supported environments, available
capabilities, execution boundaries, cost constraints, and required evidence.
Reuse an established mechanism when it satisfies the affected requirements.
Reconsider it when evidence identifies a material mismatch in behavior,
ownership, safety, compatibility, or cost.

Tooling owns automation and orchestration. Verification owns what evidence
proves, Implementation owns the permitted change, and Commit owns history.
For routine reversible choices, use adequate repository conventions within
existing authority and record material departures proportionately.

Classify contradictory authority, scope, or orchestration facts as `invalid`;
missing required capabilities or access as `unavailable`; and a selected
contract beyond supported tools or environments as `unsupported`. State
development uncertainty in prose under Core; machine interfaces retain their
declared diagnostics. Resolve the affected requirement before relying on its result.

## Hook Selection And Configuration

Use a version-control hook when its execution point, inputs, failure behavior,
bypass authority, and operator feedback satisfy the selected procedure. Choose
the mechanism, configuration, stage, scope, concurrency, commands, and
installation from actual repository, consumer, platform, and support facts.
Treat its result according to the Verification claim and retain Commit's
separate history authority.

## Scheduling And Cost

Schedule checks from their required environment, inputs, duration, resource use,
feedback needs, concurrency safety, and failure-reporting contract. Interactive
latency can justify an early focused check and a later broader claim. Preserve
the required evidence at the selected schedule. If available resources cannot
satisfy the claim, report the applicable diagnostic and retain it as unsatisfied.

## Editor And File Configuration

Select an editor-neutral mechanism, settings, scope, and precedence from the
canonical formatting and encoding contracts, file semantics, consumer needs,
generated-file authority, supported platforms, and tools.

For ordinary new source files, SHOULD use UTF-8, a final newline, and the
language formatter's conventional layout. Preserve an adequate existing
convention. Use shared editor configuration when several editors need the same
settings, and let the language formatter own its formatting responsibility.

Preserve significant whitespace, binary/generated content, required encodings,
and protocol line endings. Scope exceptions to affected files and verify actual
consumer readability. Keep normalization within the authorized change. Investigate
missing material consumer requirements; routine formatting choices use the
stated defaults within existing authority.

## Persisted Artifact Checks

Validate persisted or generated artifacts against their producer-consumer
contract, authoritative schema or shape, regeneration authority, and selected
Verification claims. Scope optimization must include every affected artifact
and dependency. Interpret success only within the check's declared proof target.

## Lint Policy And Orchestration

Select lint purpose, rules, scope, severity, automation, and schedule from owned
defect risks, security/type contracts, existing debt, affected inputs, capability,
cost, and required claims. Identify governed debt and the authority to change
its boundary. Lint supplies a supporting gate unless its property is itself
the selected acceptance claim. Resolve contradictory risk/debt policy, missing
scope/severity authority, and unsupported analysis through the declared outcomes.

## Formatting Policy And Orchestration

Define the formatting authority, file scope, settings source, automation points,
mutation behavior, and schedule from repository and consumer contracts, generated
authority, supported editors/tools, cost, and the change procedure. Assign
formatter and linter responsibilities by their owned properties and resolve
overlap explicitly. Automated mutation requires authority in the active procedure
and a reviewable diff. Formatting success proves its selected formatting claim.

Report contradictory authorities as `invalid`, missing settings, scope,
mutation, or schedule authority as `unavailable`, and required formatting
beyond the selected tools as `unsupported`.

## CI Orchestration And Scheduling

Select dependencies, execution groups, concurrency, cancellation, failure
aggregation, and reporting from required claims, real input/artifact dependencies,
supported environments, resource limits, measured cost, and diagnostic needs.
Each dependency edge represents a required input, prerequisite claim, or explicit
cost decision.

Continue independent work after failure when its evidence value justifies the
cost and resource impact. Cancellation identifies obsolete work and preserves
visibility of required results. Report each claim as failed, unavailable,
cancelled, intentionally unselected, or satisfied according to its actual outcome.

Resolve contradictory dependency/schedule/cancellation facts, missing cost,
resource or reporting facts, and provider limitations through the declared
diagnostics before relying on the orchestration.

## Tool-Debt Governance

When existing debt remains outside the current repair, record its owned findings,
affected scope, stable identity, required claims, and explicit authority. Select
the comparison, stored evidence, update procedure, blocking behavior, and retirement
condition so that new or changed violations remain distinguishable.
Classify every finding against the authorized debt boundary. Keep new, changed,
or unclassified findings outside accepted debt until explicitly dispositioned;
preserve each independently required acceptance claim.

Apply [Verification](verification.md#evidence-under-an-existing-failing-baseline)
to determine whether evidence still reaches the changed behavior. A debt
disposition records retained findings; acceptance requires evidence for the
affected claim. If a tool cannot distinguish governed debt from new findings,
report `unsupported`. Keep missing identity, scope, baseline, update or retirement
authority `unavailable`, and contradictory debt/acceptance authority `invalid`.

## Automation Cost And Operational Evidence

Optimize from measured duration, resource consumption, contention, transfer cost,
cache behavior, and diagnostic needs while preserving every required claim and
supported environment.

A cache defines authoritative inputs, invalidation key, excluded mutable state,
trust boundary, and miss behavior. A timeout or filter identifies potentially
omitted work and demonstrates continued representation of required claims.
Diagnostic storage defines audience, retention, redaction, recursion prevention,
and secret handling.

Select mechanisms from those facts and provider capability. Preserve required
observations and blocking failures, use authoritative current state, and restrict
disclosure to the intended audience. Resolve contradictions as `invalid`,
missing measurements or authority as `unavailable`, and unsupported provider
contracts as `unsupported`.
