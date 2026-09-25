# Execution Ledger

## Baseline and admission

The current branch was obtained as a GitHub Actions bundle at `2c406a8cbe0cecad6b4d83e1f431e74bb8618f16`; archive SHA-256 `0ed9c84aa7f00b5342aa534fd40e229d55bf913c52fa1e722688bcbcd48444d4`. Work is on an isolated local feature branch. Source confirms observation-only recovery at the unchanged target and loss of Git's diagnostic at Engine publication. No live proposal, readiness or host permissions were inspected or changed. The plan defines explicit completion and exact-candidate preservation before implementation.


## 2026-09-24 — Implementation and local qualification

Implemented interface-35 explicit recovery completion, shared exact candidate
construction/publication, current authorization and review checks, and bounded
Git command observations. Readiness, proposal, application and store formats
remain unchanged. The default recovery operation remains observational.

Focused recovery tests passed 14 cases. Repository Git passed 32 tests with one
root-only permission skip, and that case passed separately under an unprivileged
UID. The actual cold-MCP path passed failed apply, observation, same-application
completion, retry reconciliation and application readback with a real coverage
receipt and complete verifier. A distinct interface-34 admission was completed
by interface 35 without moving its expected main or replacing readiness/store.
An explicit changed-evidence transition remained blocked, preserving its target
and application. The final affected Engine subset passed 55 tests.

Metadata (43), policy impact (10), contracts (52, one existing interpreter skip),
analysis (114) and verifier (168) runs succeeded. Generated freshness and the
complete structural checkpoint were run separately. The report records initial
collection/version/fixture failures and their actual corrected evidence rather
than counting them as successful tests.

Local tests used Python 3.13.5 / rpds-py 2026.5.1, not the supported locked target.
No user store, real proposal or accepted branch was touched. Source acceptance
is not publication acceptance on the user's restricted host. R6 and the overall
plan remain verifying until the operator-qualified installation and live result
are established. Final packaging evidence is retained in verification.md and the
ZIP's checks directory.

## 2026-09-24 — Complete-checkout integration

Applied the package to the exact baseline and committed the source repair as
`5e7c04a8` under MrScripty. The supported Python 3.12.3 environment used locked
contract dependencies, including rpds-py 2026.6.3. Repository Git (32), focused
recovery (14), affected Engine tests (55), and the separate cold-process
publication test (1) passed. Contract projection freshness and both complete
structural verification paths passed 73 suites / 121 checks. The generated
suite-input manifest matched the supplied version.

The committed-head interface-34-to-35 probe completed the original admission.
The changed-evidence probe blocked the same application and preserved its target.
Only disposable repositories and stores were used. Operator-host qualification
and actual live recovery remain pending.
