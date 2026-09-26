# Execution Ledger

## Admission

- Inspected current main and its retained CI source bundle; both bind `c4470f9e`.
- Source bundle ZIP SHA-256: `1905cc40e9bcbe3f076df3cfdb3e44aeadf89c2c111f8525e5c6e3ee285730d4`.
- Created isolated branch `implementation/agent-workflow-simplification`.
- Inspected Core, Router and applicable implementation, verification, proportionality,
  documentation, generated-contract/IPC, contract evolution and performance owners.
- Traced focused workflow/result producers, native Analysis work handles, detail
  paging, schema generation, tests and MCP consumers before changing the contract.
- Admitted the write set and acceptance in `plan.md`. Existing durable records and
  explicit review/publication remain with their current owners.

## Verification environment

The container currently supplies Python 3.13.5, not the project's declared
3.11/3.12 runtime. Local execution is diagnostic evidence only for that environment;
supported-runtime and configured-client qualification remain separate gates.

## Implementation checkpoint

The canonical contract is now interface 38; request 6/state 7 and all durable
handle formats are unchanged. Pending mutation views consume already-issued
native Analysis work through the shared paging owner. Compact status retains its
direct count projection. Full native outcomes remain supported. The old repeated
context is removed only from focused continuations and summary navigation.

The initial six new regressions passed (26.297 seconds) after the owner-generated
suite input manifest was refreshed. The registered checkpoint passed all 121
checks across 73 suites. Additional strict shape, no-domain-effect and byte-bound
regressions and the affected suites are running as diagnostic local evidence.
Instructions and the cold MCP consumer now use inline work and grouped decisions.
The real-client compatibility schema descriptions and MCP dual representation
remain unchanged.

## Completed local evidence and handoff

The full Engine suite completed in independent clones (381 tests,
0 skipped, no failures); the 50 focused and 26 final interface checks
also passed. Contract/compiler, Analysis, metadata, policy-impact and Verifier
implementation results are recorded in verification.md and the delivery logs.
Cold MCP traces improved from five calls to three for the same two decision
batches. Cross-version readback retained old Analysis and readiness handles
without store migration. Application route descriptions now directly recommend
existing grouped reads, independently of authoring skill loading.

Generated projections and the complete structural checkpoint were rechecked.
The scoped write set and pure implementation owner were reviewed internally.
Status remains Verifying because Q1 and independent external review remain open.
No normative text, application exposure, user state or remote Git was changed.

## Integration follow-up — 2026-09-26

- Applied the delivery patch with `git apply --check`, `git diff --check`, and
  no unrelated pre-existing worktree changes.
- Installed the locked Python 3.12.3 environment with the pinned
  `requirements.lock`; generated contract freshness, 54 contract tests, and
  repository verification (121 checks across 73 suites) passed.
- Re-ran the complete Engine suite from a disposable committed candidate after
  confirming the uncommitted-clone stale-input failure was fixture state; all
  381 tests passed. Focused runtime and interaction checks passed 29 tests.
- The local CLI reports Interface 38. The host-connected authoring MCP reports
  Interface 37 and `restart-required`; configured-client reconnect and
  independent external review remain open. No remote publication or user-store
  mutation was performed.
