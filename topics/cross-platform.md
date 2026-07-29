# Cross-Platform

**Standards metadata**

- ID: `topic.cross-platform`
- Role: `topic`
- Level: `MUST`
- Applies when: Supported targets differ in capability, build or deployment selection, platform behavior, filesystem identity, or required evidence.
- Does not apply when: The affected behavior has one declared target contract and no platform-dependent behavior or portable boundary.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Platform-target and filesystem-identity decision fixtures plus evidence on each target required by the selected claim.
- Canonical owner: `topics/cross-platform.md`

## Platform Support Contract

Declare supported targets in the project, product, or release contract. For
each target, define the support claim, required behavior, unavailable or
unsupported capabilities, artifact/build requirements, and evidence needed to
accept the claim. Product target names and support tiers are project facts, not
generic defaults.

A required behavior must retain its declared semantics on every target covered
by the claim. An intentionally optional capability is distinct from an
unimplemented required capability. Return typed `invalid` for contradictory
target facts, `unsupported` when the declared target or capability is outside
the supported contract, and `unavailable` when required target, build,
deployment, capability, or evidence facts cannot be established.

## Platform Behavior Isolation

Keep platform selection and platform-specific mechanics outside domain
behavior. Choose the smallest cohesive boundary that preserves the domain
contract and follows the language and architecture: a function, module,
adapter, injected capability, build-selected implementation, or another
explicit boundary may be correct.

Select compile-time, runtime, composition, and dispatch mechanisms from the
language, toolchain, artifact, and deployment contract. File and module
boundaries follow cohesion and language conventions. No Strategy/Factory,
runtime detection, compile-time condition, or one-file-per-platform layout is
universally required.

Platform-specific code may return a typed unsupported or unavailable outcome
when the selected contract permits it. A stub, log message, false result,
silent omission, or alternate implementation is not graceful degradation
unless an explicit product contract defines that result as semantically valid.

Language-specific target syntax, build mechanisms, and target verification
belong to the selected language profile. Use the
[Standards Router](../STANDARDS-ROUTER.md) to select it.

### No Fallback

Missing target, support, capability, build, deployment, or evidence facts
cannot choose a default platform list, support tier, Strategy/Factory, runtime
detection, compile-time condition, file layout, stub, silent omission,
alternate mechanism, or weaker evidence.

## Filesystem Paths

Use path APIs that preserve platform components. Do not construct paths with
hard-coded separators or recover components by splitting display strings.
Spaces and other valid platform path characters remain ordinary path data, not
shell or parsing syntax.

## Display, Lexical, And Canonical Forms

Keep these concepts distinct:

- display form is presentation for a user or log;
- lexical normalization resolves syntax such as redundant separators and
  `.` components without proving filesystem identity; and
- canonical identity resolves the filesystem object and aliases according to
  the platform contract.

Tests compare the form used by the behavior under test. Code that canonicalizes
or resolves real paths needs canonical expectations; display-only behavior
must not force canonical presentation.

## Comparison

Compare path components using the selected platform and filesystem contract.
Do not use raw string prefix as equality, ancestry, or containment. Do not
apply one universal case-folding or Unicode-normalization rule merely from an
operating-system name; mounted filesystems and platform-managed aliases can
have different identity behavior.

Account for temp directories, symlinked workspaces, mounted volumes, and
platform aliases such as two display paths resolving to one object. When an
untrusted path authorizes an operation, apply
[Filesystem Containment](security.md#filesystem-containment) in addition to
these identity rules.

## Verification

Platform-target checks cover single and multiple declared targets, mechanism
selection, cohesive isolation, semantic optionality, typed outcomes, and the
evidence environment required by each support claim.

Record the supported platform and filesystem families for the affected claim.
Exercise path construction and identity on each required family where behavior
differs. A simulated or single-filesystem check cannot satisfy a claim that
requires real behavior from another filesystem family.

Include spaces, alias paths, differing case behavior, canonical root equality,
and component-aware ancestry where applicable. Unknown filesystem semantics
produce an unresolved platform diagnostic rather than a guessed comparison.
