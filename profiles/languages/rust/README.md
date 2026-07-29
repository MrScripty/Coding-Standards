# Rust Language Profile

**Standards metadata**

- ID: `profile.language.rust`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust source, Cargo metadata, or Rust-generated artifacts change.
- Does not apply when: No Rust-owned artifact changes.
- Requires: `core`
- Specializes: `none`
- Verification: Affected Cargo formatting, lint, build, and test commands pass.
- Canonical owner: `profiles/languages/rust/README.md`

This profile owns Rust mechanisms. Cross-language policy remains in Core,
workflows, application profiles, boundary profiles, and topics.

## Baseline Rust Change

For a local library bug fix:

1. Use the existing crate and workspace ownership boundaries.
2. Add a focused Rust regression test.
3. Run formatting for affected Rust files or the workspace.
4. Run Clippy for the affected package/targets with repository-configured
   warnings.
5. Run the focused test and affected package tests.
6. Run broader workspace checks only when shared contracts or workspace wiring
   changed.

Do not require `--all-features` when declared features are mutually exclusive.
Test default, no-default, individual, and explicitly supported combinations
according to the crate's feature contract.

## Rust Invariants

- Prefer validated types and checked conversions at boundaries.
- Route async API and suspension-boundary selection through the
  [Rust Async profile](async.md).
- Route Rust target selection, configuration placement, and target evidence
  through the [Rust Cross-Platform profile](cross-platform.md).
- Give async runtimes and spawned tasks explicit lifecycle owners.
- Do not hold synchronous guards across `.await`.
- Deny unsafe by default and route legitimate unsafe work through the
  [Rust Unsafe profile](unsafe.md).
- Route raw foreign memory, checked dimensions, and callback borrows through
  the [Rust Interop profile](interop.md).
- Route untrusted dimensions, counts, offsets, strides, and lengths through
  the [Rust Security profile](security.md) before arithmetic or resource use.
- Route Rust host representations and cross-language conversions through the
  [Rust Language Binding profile](language-bindings.md).
- Keep generated bindings derived and test both native and host sides when that
  boundary changes.

## Detailed Guidance During Migration

The current Rust documents remain canonical for specialized rules not stated
here:

- [API](../../../languages/rust/RUST-API-STANDARDS.md)
- [Remaining Async mechanisms](../../../languages/rust/RUST-ASYNC-STANDARDS.md#runtime-boundaries)
- [Dependencies](../../../languages/rust/RUST-DEPENDENCY-STANDARDS.md)
- [Release](../../../languages/rust/RUST-RELEASE-STANDARDS.md)
- [Remaining security guidance](../../../languages/rust/RUST-SECURITY-STANDARDS.md)
- [Tooling](../../../languages/rust/RUST-TOOLING-STANDARDS.md)

If a legacy Rust rule conflicts with this profile for a moved rule, this
profile is canonical. Conflicts in unmoved specialized rules must be reported
rather than resolved by convenience.
