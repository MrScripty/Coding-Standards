# Rust Cross-Platform Profile

**Standards metadata**

- ID: `profile.language.rust.cross-platform`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A Rust target contract, target triple, support claim, target-dependent source/build configuration, Rust-produced artifact, or target evidence obligation changes.
- Does not apply when: The Rust change neither changes nor relies on a target contract, target-specific capability, target-dependent mechanism, target artifact, or target evidence claim.
- Requires: `core`, `workflow.verification`, `topic.cross-platform`, `profile.language.rust`
- Specializes: `topic.cross-platform`, `profile.language.rust`
- Verification: Rust target/configuration decisions plus compile, link, package, integration, and runtime evidence selected by each declared target claim.
- Canonical owner: `profiles/languages/rust/cross-platform.md`

## Rust Target Contract

Consume the supported targets from the project, product, or release target
contract. For each Rust target triple, record the support claim, required
capabilities, produced artifacts, toolchain/linker requirements, deployment
conditions, and evidence needed to accept the claim. Target triples and support
levels are adopting-project facts, not generic Rust defaults.

A target absent from the selected contract is `unsupported`. Contradictory
target, artifact, or capability facts are `invalid`. Missing target,
toolchain, linker, artifact, deployment, or evidence facts are `unavailable`.
Do not relabel an unverified required target as best effort.

## Configuration And Placement

Select Rust `cfg`, build scripts, features, composition, and dispatch from the
declared target, toolchain, artifact, and deployment facts:

- use `cfg` when the selected artifact is compiled with target-specific Rust
  items or dependencies;
- use a build script only when build-time discovery or artifact construction is
  part of the declared build contract;
- use a feature only when the capability is a supported consumer selection,
  not as a substitute for an unknown target;
- use composition or dispatch when the deployed artifact selects among
  capabilities at startup or runtime; and
- combine mechanisms only when their ownership and precedence are explicit.

Keep target-specific mechanics outside domain behavior at the smallest
cohesive Rust boundary. A function, module, adapter, target-selected
implementation, or composed capability may be correct. No shared trait,
platform module, directory shape, or target-named file is universally
required.

Inline `cfg` is valid when the conditional item remains cohesive,
comprehensible, and locally verifiable. Extract it when separate ownership,
invariants, dependencies, unsafe reasoning, or tests make a boundary clearer.
Line counts, parameter counts, comment counts, and conditional-block counts do
not decide placement.

## Evidence By Claim

Match evidence to the accepted support claim:

- compilation proves that selected Rust items type-check for the target;
- linking proves that the declared linker and native dependencies produce the
  artifact;
- packaging proves the expected target artifact and metadata are assembled;
- integration proves selected components operate together in the qualified
  environment; and
- runtime evidence proves behavior on the real target or an explicitly
  accepted environment with equivalent semantics for that claim.

Target compilation does not prove linking, packaging, integration, or runtime
behavior. A host build, simulator, emulator, container, cross-compilation tool,
or hosted runner counts only for the claims the project contract explicitly
assigns to that environment. Record the evidence environment and unresolved
claims.

Return typed `invalid`, `unsupported`, or `unavailable` when the selected
target or its required evidence cannot be established.

## No Fallback

Missing target, toolchain, linker, artifact, capability, deployment, or
evidence facts cannot select:

- default target triples or support tiers;
- best-effort status for required behavior;
- a universal trait, module, directory, file, or inline-`cfg` threshold;
- a named build, cross-compilation, container, runner, simulator, or emulation
  tool;
- another target or configuration mechanism; or
- compile-only, simulated, host-only, or otherwise weaker evidence for a
  stronger claim.

Return the typed diagnostic for the selected contract without changing the
target claim or mechanism.
