# Tooling Workflow

**Standards metadata**

- ID: `workflow.tooling`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects, configures, schedules, or coordinates development tools or automation.
- Does not apply when: No development-tool selection, configuration, scheduling, or orchestration behavior changes.
- Requires: `core`, `workflow.implementation`, `workflow.verification`, `workflow.commit`
- Specializes: `none`
- Verification: Tool selection, hook orchestration, scheduling, cost, and persisted-artifact decision fixtures plus affected real automation evidence.
- Canonical owner: `workflows/tooling.md`

## Tooling Authority

Select and configure tooling from the repository's owned contracts, supported
environments, available capabilities, execution boundaries, cost constraints,
and required evidence. Tooling owns automation mechanism and orchestration. It
does not redefine what Verification evidence proves, what Implementation may
change, or what Commit permits in history.

Contradictory tool, authority, scope, or orchestration facts produce typed `invalid`.
A required capability or access that cannot be established produces typed `unavailable`.
A repository, platform, or toolchain that cannot implement the selected contract
produces typed `unsupported`. Do not continue with a conventional
tool, successful no-op, weaker check, or alternate execution path.

## Hook Selection And Configuration

Use a version-control hook only when its execution point, available inputs,
failure behavior, bypass authority, and operator feedback satisfy the selected
procedure. Choose the hook mechanism and configuration format from repository,
consumer, platform, dependency, and support facts.

Do not default to a hook product, hook stage, staged-file scope, parallel
execution, file glob, command, or installation mechanism. A hook transports a
selected check; running it before commit or push does not make its result an
acceptance claim or grant history-mutation authority.

## Scheduling And Cost

Schedule each selected check from its required environment, inputs, duration,
resource use, feedback needs, concurrency safety, and failure-reporting
contract. Interactive latency may justify an earlier focused check and a later
broader claim, but cost does not authorize weaker evidence or silent omission.

Do not infer a schedule from labels such as fast, local, pre-commit, pre-push,
CI, or release. If no schedule satisfies both the required claim and available
resources, return the applicable typed outcome.

## Editor And File Configuration

Select an editor-neutral configuration mechanism and each setting from the
repository's canonical formatting and encoding contracts, affected consumer
requirements, file-format semantics, generated-file authority, supported
platforms, and selected tool capabilities. Define the configuration's scope and
precedence where multiple mechanisms or nested files can apply.

EditorConfig is one possible transport for selected settings; its availability
does not make it the default. Do not default to spaces, indentation width, line
ending, character encoding, final-newline, trailing-whitespace, file-pattern,
or language-family settings. Do not copy a universal settings table when owned
files or consumers require different behavior.

Contradictory repository, consumer, or file-format requirements produce typed
`invalid`. Missing required scope, precedence, or authoritative setting facts
produce typed `unavailable`. A required setting that no supported mechanism can
represent produces typed `unsupported`; do not silently omit it or substitute a
conventional value.

## Persisted Artifact Checks

For a persisted or generated artifact, select validation from its canonical
producer-consumer contract, authoritative schema or shape, regeneration
authority, and required evidence. Scope optimization is allowed only when it
provably includes every affected artifact and dependency.

Do not default to staged paths, lightweight validation, deterministic
regeneration, or a later broader gate. Passing automation proves only the
declared check; it does not prove artifact acceptance or producer-consumer
compatibility unless Verification selected that exact claim.

## Lint Policy And Orchestration

Select lint purpose, rules, scope, severity mapping, automation, and schedule
from owned defect risks, security and type contracts, existing debt, affected
inputs, tool capability, execution cost, and required Verification claims.
Record how existing debt is distinguished from newly introduced violations and
who has authority to change that boundary.

Do not default to failing every warning, autofixing, changed-file scope,
tiered execution, CI execution, or a full audit. A lint result is a supporting
gate unless Verification selected the exact linted property as a claim.
Contradictory risk or debt policy is `invalid`; missing scope or severity
authority is `unavailable`; unsupported required analysis is `unsupported`.

## Formatting Policy And Orchestration

Select formatting authority, owned file scope, settings source, automation
points, mutation behavior, and check schedule from repository and consumer
contracts, generated-file authority, supported editors and tools, change
procedure, cost, and required Verification claims. Define formatter and linter
responsibilities by the properties each selected mechanism owns; resolve
overlap explicitly rather than relying on product pairing.

Do not default to format-on-save, editor mutation, CI checking, every-save or
pre-commit execution, Prettier, ESLint, a formatter/linter pair, or an
installation command. Automation that mutates files requires authority in the
active procedure and must expose resulting changes for review. A formatting
check proves only its selected formatting claim.

Contradictory formatting authorities or overlapping responsibilities are
`invalid`. Missing scope, settings authority, mutation authority, or schedule
facts are `unavailable`. Required formatting unsupported by selected tools is
`unsupported`; do not silently skip files, substitute conventional settings,
or treat unchanged command execution as proof.

## CI Orchestration And Scheduling

Select the CI dependency graph, execution groups, concurrency, cancellation,
failure aggregation, and reporting from required Verification claims, real data
and artifact dependencies, supported environments, resource limits, measured
cost, diagnostic value, and failure-isolation behavior. A dependency edge must
represent a required input, prerequisite claim, or explicit cost decision; a
shared label or blocking status does not create an edge.

Choose whether independent work continues after a failure by balancing the
value of additional evidence against its measured cost and resource impact.
Cancellation must identify which work becomes obsolete and must not hide a
required result. Reporting must preserve each required claim's outcome and
distinguish failed, unavailable, cancelled, and intentionally unselected work.

Do not default to GitHub Actions, parallel execution, fail-fast or aggregate
execution, a preflight/core/expensive tier model, a summary job, CI-local
commands, or cancellation of superseded runs. Provider syntax and job location
do not define claim dependencies or evidence meaning.

Contradictory claim, dependency, schedule, or cancellation facts are `invalid`.
Missing required dependency, cost, resource, or reporting facts are
`unavailable`. An orchestration contract that the selected provider or
environment cannot represent is `unsupported`; do not substitute a conventional
topology, skip the claim, weaken reporting, or silently serialize the work.

## Tool-Debt Governance

When a selected tool reports existing debt that cannot be resolved in the
current change, define the debt boundary from owned findings, affected scope,
stable identity, required claims, and explicit authority. Select the comparison
method, stored evidence, update procedure, blocking behavior, and retirement
condition so new or changed violations cannot be accepted accidentally.

Do not default to a committed snapshot, total-count comparison, changed-file
comparison, zero-debt threshold, named command, tier promotion, or temporary
non-blocking state. A debt boundary cannot weaken an independently required
Verification claim or convert unknown findings into accepted debt.

Contradictory debt and acceptance authority is `invalid`. Missing debt identity,
scope, baseline authority, update procedure, or retirement condition is
`unavailable`. A selected tool unable to distinguish governed debt from new
findings is `unsupported`; do not accept all findings, preserve an unverifiable
baseline, or infer a ratchet algorithm.

## Automation Cost And Operational Evidence

Optimize automation only from measured duration, resource consumption,
contention, transfer cost, cache behavior, and diagnostic needs while preserving
every required Verification claim and supported environment. Select caching,
timeouts, filtering, cancellation, artifact retention, and diagnostic transport
from authoritative inputs, invalidation boundaries, data sensitivity, provider
capability, and operational cost.

A cache must define its authoritative inputs, invalidation key, excluded mutable
state, trust boundary, and miss behavior. A timeout or filter must identify the
work it may omit and prove that required claims remain represented. Diagnostic
storage must define audience, retention, redaction, recursion prevention, and
secret-handling behavior.

Do not default to caching, cache contents or keys, lockfile commands, timeouts,
path filters, cancellation, artifact upload, retention periods, GitHub summaries,
diagnostic branches, or a provider. Optimization cannot replace evidence with a
successful cache hit, omit a required platform, hide a blocking failure, or
publish sensitive state.

Contradictory optimization, evidence, or data-handling facts are `invalid`.
Missing measurement, invalidation, omission, retention, or diagnostic authority
is `unavailable`. A provider unable to represent the selected safety and evidence
contract is `unsupported`; do not disable the claim, use stale state, select a
conventional cache, or silently discard diagnostics.
