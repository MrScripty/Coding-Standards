# Admitted Publication Recovery

**Plan status:** `Verifying`
**Acceptance status:** `pending`
**Current phase:** Source implementation and supported Python 3.12 local qualification complete; operator-host qualification remains pending.
**Next slice:** Install current code and schemas without advancing the admitted target; verify the supported locked host, then use the original readiness to observe and explicitly complete the preserved application.
**Canonical plan:** `docs/plans/admitted-publication-recovery/plan.md`; operation: `verify` the installed handoff.
**Source baseline:** `MrScripty/Coding-Standards@2c406a8cbe0cecad6b4d83e1f431e74bb8618f16`.
**Composed-design review:** `applicable`; recorded below.
**Execution ledger:** [execution-ledger.md](execution-ledger.md).
**Issues:** [issues.md](issues.md).
**Report:** [verification.md](verification.md).

## Objective And Scope

An authorized author can finish an already-admitted application after its Git publication failed while the canonical target remains at the admitted expected revision. Preserve the readiness, proposal revision, selected application, exact candidate, review evidence, and existing store. Give the author bounded diagnostic observations sufficient to distinguish permission, read-only filesystem, lock, and other Git failures without returning arbitrary stderr content.

This code repair leaves standards, actual policy declarations, application exposure, and the user's proposal database unchanged. It does not publish the user's draft or alter the host sandbox. The reported readiness is external; only disposable repositories and stores are used here.

## Authority And Routed Standards

Apply Core and Router with Implementation, Planning, Verification, Development Proportionality, Documentation, and Commit; Library, Persistence, IPC and Generated Contract profiles; Contracts, Resilience, Diagnostics, Security, Architecture/replay and verification-oracle guidance. The prospective positive-guidance guide supplies the agreed generic, affirmative, proportional code/content separation. Examples and incident-specific identities stay in tests or maintenance records.

Preserve generic Git operations in Repository Git, immutable intent and outcome records in Authoring, integration and authorization in Engine, workflow projection in Agent Workflow, and wire shape in the canonical contract. Use existing established mechanisms and one complete behavior slice. No compatibility branch, database migration, retry daemon, new receipt store or graph change is required.

## Binding Decisions

### Explicit recovery action

Add `action: observe | complete-publication` to focused `recover` and native `recover_application`. Omission selects `observe` because safe read/receipt reconciliation remains a useful operation in its own right. The host's authoring purpose and current capability checks remain authoritative.

`observe` retains existing behavior: a selected durable applied outcome is returned; observing the exact admitted candidate can persist the applied outcome; observing the expected base or a third revision leaves recovery required. Observation issues no Git writes.

`complete-publication` may write only after observing the expected base. It requires current recovery and application authorization, current proposal/readiness consistency, reconstruction from the original frozen proposal and reviewed evidence, equality of reconstructed commit identity with the admitted candidate, fresh complete verification, active-candidate validation, and renewed admission/authorization checks at the publication boundary. Publication uses the existing expected-old Git compare-and-swap. A third revision stays untouched; an already-visible candidate is reconciled rather than republished.

An unchanged target is not evidence that publication never happened. Explicit completion authorizes re-establishing the same candidate at that exact expected target, including an unknown prior history. This contract does not promise historical exactly-once side effects or infer intent from elapsed time. Each request makes at most one publication attempt.

### Shared construction and publication

Extract the existing pure candidate-file preparation and complete-verification handling sufficiently to reuse them for apply and completion. Reconstruct deterministically even when the failed fetch imported no candidate object. Retain existing coverage receipt generation and current evidence validation. Compare the resulting candidate with the persisted admitted OID; changed reconstruction is a blocked recovery, not a new application or an implicit substitution.

Keep one selected application. Finish its outcome through existing Authoring storage. If outcome persistence fails after Git succeeds, the next observe reconciles the same candidate. If another completion wins the compare-and-swap, observation of the same candidate can finish the same outcome. Competing different revisions remain protected.

### Diagnostics

Repository Git owns command identity, exit status and an allowlisted observation derived from stderr. Retain full command error data only inside the existing private exception boundary. Engine authoring outputs include bounded operation/code/exit-status/reason and recognized fixed stderr phrases, not arbitrary filenames, URLs, credentials or hook output. Unknown text is explicitly unclassified. A recognized phrase is evidence of Git's error, not proof of the broader host configuration.

Application-purpose interfaces continue to reject publication and recovery before accessing authoring data. The error from an old process cannot be reconstructed retrospectively; a fresh failure supplies new diagnostics. No automatic permission probe, escalation or host modification is part of this fix.

### Compatibility And Operator Cutover

Bump only the public interface edition to 35 and regenerate its models/tool catalog. Existing snapshots, readiness, applications, store formats and semantic identities retain their formats. Replace actual current code consumers coherently; no old-code fallback is added.

The installed implementation can be updated independently from its accepted content branch. Keep the real target at the admitted expected revision; advancing it merely to install this repair would create a legitimate divergence. Use a Git-writable, operator-authorized host for the same repository/store. Restart the server and reconnect; interface discovery does not upgrade a running process. Preserve the exact readiness handle and use supported workflow status/recover operations. No manual ref update or database repair is authorized by this plan.

## Exact Write Set

- `tools/repository_git/repository_git/{__init__,errors,repository}.py`: structured bounded command observations and preservation across expected-target failures.
- `tools/repository_git/tests/test_repository.py`: real lock failure, diagnostics, unchanged target and later success.
- `tools/standards_engine/standards_engine/{engine,agent_workflow}.py`: shared candidate/verification/publication behavior and explicit recovery completion.
- `tools/standards_engine/contracts/{a1-contract.schema.json,a1-interface.toml,examples/a1-examples.json}` and their owning generated outputs: action and bounded diagnostic results; interface 35.
- A new `tools/standards_engine/tests/test_publication_recovery.py` and directly affected existing workflow/transport/version assertions.
- `tools/repository_git/README.md`, `tools/standards_engine/{README.md,PURPOSE-SEPARATION.md,contracts/README.md}`: current technical behavior and operator handoff. Real standards and the pending authoring skill content stay unchanged.
- The generated suite-input manifest via its owning generator, this plan directory, and package integration instructions outside the repository.

## Milestone R1 — Complete Admitted Recovery

**Status:** `Verifying`.
**Goal:** A failed publication is completed through public recovery without re-admission or substitution.
**Write set:** The exact owners listed above.
**Gate:** Focused failure/authorization tests, Repository Git tests, real compiler and durable-store recovery, generated freshness, and real MCP failure/observe/completion/readback pass. Baseline and unavailable-environment evidence are reported separately.

## Acceptance Claims

| ID | Claim | Evidence kind | Environment | Mode | Status |
| --- | --- | --- | --- | --- | --- |
| R1 | Observation preserves unresolved admission and performs no Git write; explicit completion uses the same candidate/application. | integration | representative local Git/SQLite | automated | passed |
| R2 | Divergence, stale readiness, missing authority, candidate mismatch, failed verification and failed writes retain the intent without replacing content or issuing false success. | focused + integration | deterministic fault cases with real owners | automated | passed |
| R3 | Publication uses expected-target CAS, preserves diagnostic meaning, bounds disclosure, and reconciles lost success or outcome persistence. | integration | real Git plus targeted failure injection | automated | passed |
| R4 | Actual MCP schema, focused workflow, process replacement and application readback agree with native behavior. | system | real local processes/Git/SQLite | automated | passed |
| R5 | Existing affected suites, generated artifacts and complete structural checkpoint remain coherent; normative/source data outside scope are preserved. | contract + review | complete checkout | automated | passed |
| R6 | The operator's supported locked environment and preserved live application can use the installed repaired server. | user-workflow | required-real operator host | either | pending |

Source delivery can finish with R6 explicitly pending. It cannot claim the user's publication succeeded. Available Python/dependency versions are recorded before testing. Failures that prevent a test reaching the affected behavior provide no evidence for that claim; repair or report them rather than compare failure counts.

## Composed-Design Admission

1. **Independent concerns:** Git owns bounded commands and CAS; Authoring owns immutable admission/outcome; Engine owns current permission and integration; workflow owns continuation; schema owns representation.
2. **State, identity, value, time, policy and mechanism:** Readiness and application identities remain durable; current target is a live observation; historical authority is not current permission; time cannot prove completion.
3. **Caller and composition knowledge:** Callers retain a readiness and choose an explicit action. They supply no candidate bytes, Git paths, expected target overrides or replacement application.
4. **Representative change paths:** A diagnostic update changes its producer and typed projection; candidate construction is shared by first application and recovery; store and graph semantics stay independent.
5. **Stable interfaces and hidden knowledge:** The existing Git adapter still validates issued active candidates. Engine performs all orchestration through declared owners; generated contracts remain derived.
6. **Independent evolution and failure:** A failed write leaves the selected application; a failed outcome receipt is reconciled by observation; denied authorization preserves intent without granting writes.
7. **Deletion results:** Removing explicit completion leaves the current dead end; omitting exact candidate comparison permits substituted publication; omitting fresh permission permits stale authority. A new database, retry worker, per-attempt durable journal or broad diagnostic platform contributes no necessary value here.
8. **Necessary complexity:** One explicit action plus reuse of existing construction and CAS supplies the deciding capability. No repository-specific rule, fixed test-count target or unrelated process redesign drives it.

## Blockers And Replan Triggers

The user's Git-writable host and actual store are unavailable here. The downloaded source is complete and local integration passed on supported Python 3.12 with locked dependencies. Replan only if exact candidate replay cannot reconstruct the admitted identity, existing records cannot preserve required authority, or the selected completion promise needs additional persistent state. Keep catalog hot reload and 84-decision response overhead as separate findings.
