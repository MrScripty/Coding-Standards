# Milestone 7 Security Checker Repair Re-plan

## Trigger

Final closure of `SECURITY-STANDARDS.md` cannot begin while verifiers use its
transitional headings or `HEAD` snapshots as evidence. The IPC verifier also
reads Architecture, Interop, and Security former sources, so assigning it to
the Security source package would conflict with later packages.

## Selected Design

Repair checker ownership through one dependency-ordered package graph before
Security source closure:

1. one serial cross-source IPC checker-infrastructure package;
2. three independently preparable owner-checker packages for input validation,
   validation-proof lifetime, and network transport; and
3. serial integration of the shared package followed by the three disjoint
   local packages and one complete-suite group gate.

The frozen package table is
`../../../../evaluation/standards-effectiveness/milestone-7-security-checker-repairs.tsv`. Each mutable checker has exactly one
write owner. Planning, findings, ledger, shared manifests, source files,
canonical standards, dispositions, generated artifacts, and closure fixtures
remain serial integration-owner files.

## Durable Evidence

Every repair preserves:

- canonical Contracts, Security, Concurrency, and IPC owner behavior;
- complete decision-fixture outcomes and typed `invalid`, `unsupported`,
  `unavailable`, overload, and incomplete outcomes where applicable;
- exact frozen identifier dispositions and owner metadata;
- canonical former-source routes that must remain in the final index; and
- negative evidence against unsafe casts, partial decoding, global validators,
  fixed validation and transport defaults, permissive decoding, and fallback.

The repairs replace only mutable source-shape evidence. Exact prohibited
literals are checked against the complete applicable former source instead of
a heading-delimited subsection. Required canonical routes are likewise checked
against the complete source. Canonical owner content and decision fixtures
remain the primary semantic authority.

## Package Contracts

### Cross-source IPC

`7.4c3hs1` exclusively owns
`verify-ipc-payload-validation.sh`. It removes heading-delimited Architecture,
Interop, and Security section extraction while retaining exact dispositions,
canonical owner semantics, required routes in all three sources, and
source-wide negative checks for the unsafe payload mechanisms the old section
checks rejected.

### Input Validation

`7.4c3hs2a` exclusively owns
`verify-input-validation-authority.sh`. It removes `HEAD` prefix/suffix
comparisons and the requirement for migration explanation terms. It retains
the input-authority route, source-wide prohibited legacy mechanisms, canonical
Security semantics, exact dispositions, and all typed decision cases.

### Validation-Proof Lifetime

`7.4c3hs2b` exclusively owns
`verify-validation-proof-lifetime.sh`. It removes `HEAD` region comparisons and
heading-delimited route extraction. It retains the Contracts route,
source-wide prohibited legacy guidance, canonical proof-lifetime semantics,
exact dispositions, and all typed decision cases.

### Network Transport

`7.4c3hs2c` exclusively owns
`verify-network-transport-policy.sh`. It removes heading-delimited extraction
and unrelated heading requirements. It retains every canonical Security,
Concurrency, Contracts, and IPC route, source-wide prohibited transport
defaults, exact dispositions, and all typed decision cases.

## Concurrency And Integration

The three `hs2` packages may be prepared concurrently in isolated worktrees
because their write sets do not overlap. The shared IPC package is integrated
first. The integration owner then applies the three local patches, verifies
their declared write sets and focused checkers, runs the Security closure
checker against the still-unchanged source, and runs one complete suite for the
integrated checker-repair group.

A prepared patch is not accepted evidence. No worker may edit shared planning
state or another package's checker. Any newly discovered shared checker,
semantic loss, broad prohibited literal, or required canonical owner change is
a re-plan trigger.

## No Fallback

The repair does not retain transitional headings, `HEAD` comparisons, old/new
branches, section-name aliases, permissive source exceptions, or weakened
semantic checks. The final Security package must pass with one pure index; a
checker cannot accept either the transitional source or the final source by
using compatibility logic.

## Ordered Execution

1. Integrate `7.4c3hs1` and run its focused checker.
2. Prepare `7.4c3hs2a`, `7.4c3hs2b`, and `7.4c3hs2c` concurrently.
3. Integrate the three disjoint patches and run every focused checker.
4. Run the current Security closure checker and complete verifier suite.
5. Mark `F084` resolved and begin `7.4c3.6` only after the group gate passes.
