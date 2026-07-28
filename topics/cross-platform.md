# Cross-Platform

**Standards metadata**

- ID: `topic.cross-platform`
- Role: `topic`
- Level: `MUST`
- Applies when: Supported platforms or filesystems differ in path construction, canonical identity, comparison, aliases, or test behavior.
- Does not apply when: The affected behavior has one declared platform and filesystem contract with no portable path boundary.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Filesystem-identity decision fixtures and checks on each supported filesystem family.
- Canonical owner: `topics/cross-platform.md`

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

Record the supported platform and filesystem families for the affected claim.
Exercise path construction and identity on each required family where behavior
differs. A simulated or single-filesystem check cannot satisfy a claim that
requires real behavior from another filesystem family.

Include spaces, alias paths, differing case behavior, canonical root equality,
and component-aware ancestry where applicable. Unknown filesystem semantics
produce an unresolved platform diagnostic rather than a guessed comparison.
