# Build Workflow

**Standards metadata**

- ID: `workflow.build`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects or changes a build-time action, authoritative build input, produced or generated output, invalidation rule, build environment access, native build integration, or deterministic-build requirement.
- Does not apply when: The task only consumes an unchanged build artifact or runs an unchanged build procedure without changing its contract.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Build-action contract decisions plus affected input, output, invalidation, side-effect, environment, determinism, and consumer evidence.
- Canonical owner: `workflows/build.md`

## Build Authority

Authorize a build-time action from an owned artifact, consumer, target,
generation, dependency, or release contract. Identify the owner that may add,
change, or remove the action and the lifecycle phase in which it executes. A
build-system feature, existing script, ecosystem convention, successful build,
or convenience does not create authority.

Build owns the action contract, not the content contracts it consumes.
Contracts owns generated representation authority, Dependencies owns external
requirements, Cross-Platform owns target and capability facts, Security owns
untrusted authority and supply-chain risks, Release owns released artifacts and
reproducibility claims, and Tooling owns automation orchestration. Language and
build-system profiles express accepted decisions through supported mechanisms.

## Inputs, Outputs, And Side Effects

Name every authoritative input, produced output, consumer, permitted side
effect, and write boundary. Distinguish source inputs, generated intermediates,
final artifacts, diagnostics, caches, and metadata. An output path, environment
variable, compiler convention, or prior generated file cannot become authority.

Write only within the selected build output boundary unless another owner
explicitly authorizes a source change. Generated output follows the canonical
producer and consumer contract; do not hand-edit it, infer its source from the
output, or write into source merely because a tool supports that location.

## Invalidation And Incrementality

Derive rerun and invalidation inputs from every fact that can change the
observable output or required side effect. Include source, configuration,
environment, toolchain, dependency, target, and generator facts only when they
are material to the selected action.

Do not default to always rerun, never rerun, timestamps, directory-wide watches,
the current manifest, or a conventional directive list. A cache or incremental
result is valid only when its key and invalidation boundary cover all
authoritative inputs and exclude undeclared mutable state.

## Environment And External Effects

Declare required filesystem, process, environment, network, credential,
toolchain, compiler, and system-library access. Select build-time discovery only
when the accepted contract requires facts before artifact construction and the
result can be reproduced or intentionally qualified for the target claim.

Do not move runtime capability detection into the build, invoke a raw compiler,
access the network, inherit ambient environment state, or execute downloaded
content by convention. Missing required access or capability retains a typed
outcome; it does not authorize another command, dependency, detection phase, or
cached result.

## Determinism And Reproducibility

Derive determinism from the affected artifact and release claims. Control every
material nondeterministic input required by those claims, including time, paths,
ordering, locale, randomness, environment, network results, and tool versions.
Determinism of one generated file does not prove a reproducible released
artifact, and a pinned tool does not prove deterministic output.

Do not default to a timestamp variable, source-date convention, clean build,
lockfile, or byte-for-byte claim. When the required determinism cannot be
established, return the applicable typed outcome rather than relabeling the
artifact or accepting an unverified build.

## Typed Outcomes

Contradictory authority, input, output, consumer, side-effect, invalidation,
environment, target, or determinism facts are `invalid`. A well-formed action
outside supported build, platform, or toolchain capability is `unsupported`.
Missing authority, material input, output owner, consumer, invalidation fact,
access, capability, or evidence is `unavailable`.

Do not fall back to an existing script, conventional purpose, source-tree
output, broad rerun, raw compiler, runtime or build-time detection swap,
ambient environment, timestamp convention, minimal dependency set, successful
no-op, or default success.

## Verification

Evidence covers the accepted action and phase, authoritative inputs, produced
outputs and consumers, write boundary and side effects, invalidation behavior,
qualified environment and target, deterministic properties, typed failures,
and every changed producer-consumer path. Build success proves only that the
selected invocation exited successfully.
