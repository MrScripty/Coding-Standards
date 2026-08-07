# Generic Standards Verification Engine Execution Ledger

## 2026-08-07 - Re-plan Trigger And Baseline

- Operation: `start`
- Prior revision: `160ea4f5`
- Trigger: the requested objective expanded from repairing four
  Cross-Platform Bash checkers to designing and building one generic engine
  that replaces most bespoke scripts.
- Repository state: Coding-Standards clean; Pantograph has two unrelated user
  proposal changes and is outside this plan's write set.
- Measured baseline: 274 `verify-*.sh` scripts, 290 fixture files, 166 verifier
  scripts containing verifier/helper invocations, 43 scripts using `sed`, and
  13 scripts using the existing decision-table helper.
- Toolchain evidence: the repository has no Python, Cargo, Go, or Node project
  manifest; the current environment provides Python 3.12.3 and Rust 1.92.0.
- Decision: select a Python 3.11+ standard-library engine, declare its
  capability contract explicitly, prohibit runtime packages and arbitrary
  commands, and migrate in owner-bounded waves.
- No-fallback result: no checker or source was edited; the blocked
  Cross-Platform source remains unchanged pending the new engine contract.
- Next slice: accept Milestone 0 planning authority, then implement Milestone
  1's executable kernel and replace the Build owner checker.

## 2026-08-07 - Milestone 0 Contract Accepted

- Outcome: accepted one engine architecture, runtime/dependency decision,
  no-fallback boundary, migration sequence, and parent-plan delegation.
- Verification: the canonical plan-structure checker passed for both the new
  plan and the parent standards-restructure plan; link/identity scans and
  `git diff --check` passed.
- Scope: planning authority only. No standard, verifier, fixture, disposition,
  generated artifact, source index, configuration, or lockfile changed.
- Next slice: implement the strict kernel, register Build owner behavior, and
  delete `verify-build-owner-contract.sh`.

## 2026-08-07 - Milestone 1 Target Re-plan

- Trigger: deletion preflight found `verify-build-owner-contract.sh` in the
  frozen row-35 README dependency audit. Its owning verifier requires all 33
  paths to exist, so deleting Build alone would invalidate shared historical
  evidence and retaining a wrapper would violate the no-legacy contract.
- Decision: keep shared row-35 migration authority unchanged in the kernel
  slice. Replace `verify-rust-test-style.sh`, a measured leaf with no inbound
  script, manifest, plan, or documentation reference.
- Preserved behavior: 16 typed test-style decisions; Verification and Rust
  recipe text; rejection of old mandatory test naming; and exact `STD-0839`
  disposition.
- No-fallback result: the unaccepted Build declarative draft is not retained,
  and no Build wrapper, path alias, or historical-manifest exception is added.
- Deferred owner: Milestone 3 must migrate historical checker-identity audits
  when it replaces shared migration contracts.
