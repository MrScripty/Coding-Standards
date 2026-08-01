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

## Persisted Artifact Checks

For a persisted or generated artifact, select validation from its canonical
producer-consumer contract, authoritative schema or shape, regeneration
authority, and required evidence. Scope optimization is allowed only when it
provably includes every affected artifact and dependency.

Do not default to staged paths, lightweight validation, deterministic
regeneration, or a later broader gate. Passing automation proves only the
declared check; it does not prove artifact acceptance or producer-consumer
compatibility unless Verification selected that exact claim.
