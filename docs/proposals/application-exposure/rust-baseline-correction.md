# Proposed Rust baseline correction

The independent exposure review found that this existing step:

> Add a focused Rust regression test.

requires a new test for every local library bug fix even when Core and
Verification accept adequate existing evidence or a construction guarantee.

Proposed replacement in `profile.language.rust`, Baseline Rust Change:

> Establish the changed claim with adequate existing evidence or a construction
> guarantee, or add a focused Rust regression test when needed.

This preserves regression evidence and Rust-specific mechanisms. It does not
create a new generic principle. The other baseline steps, including configured
Clippy checks, remain subject to their existing authority.

The base Rust profile and its three required dependents remain unqualified
until this normative wording issue is corrected, independently reviewed and
published through the Engine. The 28 other modules are being qualified
separately. The Standards Authoring workflow remains private to maintainers.

This is a reviewable proposed correction, not an applied standards edit.
