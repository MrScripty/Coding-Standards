# Admitted-publication recovery: implementation and verification

**Source implementation:** complete. **Plan acceptance:** `Verifying`; the actual
operator host and preserved live application remain external. This report records
local source, Git, compiler, store and MCP evidence, not publication of the user's
standards or an independent external review.

## Baseline and unchanged authority

The complete source was recovered from the successful GitHub Actions artifact
for `MrScripty/Coding-Standards@2c406a8cbe0cecad6b4d83e1f431e74bb8618f16`.
Artifact SHA-256:
`0ed9c84aa7f00b5342aa534fd40e229d55bf913c52fa1e722688bcbcd48444d4`.
Its Git bundle reproduced the exact repository history. Development and all
publication/recovery experiments used owned local clones and temporary stores.

No external readiness, proposal, ref or database was accessed. The supplied
readiness ID is retained only as operator handoff information. The patch changes
runtime code, generated contracts, tests, technical documentation and its plan;
canonical standards, real registrations, reasoning/exposure declarations and
pending authoring skill content remain untouched. Package preservation checks
compare these paths against the exact source baseline.

## Implemented behavior

Interface 35 adds optional `action: observe | complete-publication` to focused
`recover` and native `recover_application`. Observation remains the default and
issues no Git writes. It may record a missing applied outcome when the exact
candidate is visible.

Explicit completion reuses the selected admitted application. It checks current
recovery and application authority, current proposal/readiness consistency and
review evidence, reconstructs through the same candidate/coverage-receipt owner
as ordinary apply, requires exact equality with the admitted commit, runs the
complete verifier, rechecks selection/head/permissions, validates the active
candidate, and performs one existing expected-old Git compare-and-swap. Failed
requirements preserve the selected application. A third target is not replaced.

An already-visible candidate or existing applied outcome is reconciled without
republishing. Failed outcome persistence after Git success remains recoverable.
A concurrent completion that establishes the same candidate is reconciled. A
candidate absent from the original repository after a failed import can be
reconstructed; recovery does not depend on leftover temporary clone files.

An unchanged target does not establish that publication never occurred. The new
action is an explicit authorization to re-establish the same candidate at the
expected base, not a historical exactly-once claim. No application selection,
readiness, proposal, analysis, snapshot or store format changed. No migration,
reset, permission override, lock removal, automatic retry or alternate old-code
implementation was introduced.

Repository Git now retains bounded command observations alongside its private
exception. Authoring diagnostics return command, exit status and a fixed matched
stderr phrase/classification. Arbitrary stderr, paths, URLs, credentials and
hook output do not enter the MCP result. Unrecognized messages stay unclassified.
Earlier stderr that was already discarded is not recreated.

## Environment

- Python 3.13.5; Linux x86-64; Git 2.47.3.
- jsonschema 4.26.0, referencing 0.37.0, attrs 26.1.0,
  jsonschema-specifications 2025.9.1, rpds-py 2026.5.1.
- The repository supports Python 3.11/3.12 and locks rpds-py 2026.6.3.
- Normal test execution was UID 0. The actual permission-denial test was also
  executed separately as unprivileged `nobody` against its own temporary repo.
- The optional MCP Python SDK was not installed. The system test used real
  JSON-RPC over stdin/stdout with a fresh actual MCP process for every call,
  checking text/structured result agreement and installed interface discovery.

These observations are complete for the named local environment. They do not
claim the supported locked deployment, the user's actual client, or the user's
likely sandbox error has been reproduced exactly.

## Evidence

| Check | Actual observation |
| --- | --- |
| Original Repository Git suite | 28 passed. |
| New regression before implementation | Explicit completion was unsupported in both generated request shapes; the real lock-failed application remained uncertain. Two test methods reproduced the missing contract and capability. |
| Focused recovery contract/lifecycle suite | 14 passed. Real Git/SQLite/proposal/candidate owners; the complete verifier is substituted for focused fault selection, so these are not standalone system acceptance. |
| Repository Git final suite | 32 run successfully; one root-only permission skip, separately executed and passed under an unprivileged UID. |
| Actual permission-denial case | 1 passed; a test-owned read-only ref directory rejected publication, retained main, reported permission denial, and allowed the same candidate after the test owner restored its own permissions. |
| Real cold-MCP recovery/publication | 1 passed, 103.340 seconds. Includes actual coverage attestation/receipt, full verification, failed lock write, observation, same-application completion, retry reconciliation and application readback. |
| Interface 34 admission → interface 35 completion | 1 passed, 106.006 seconds. Original main/readiness/application retained; current code/schema installed separately from accepted content; unchanged evidence revalidated; original candidate published through recovery. |
| Changed-evidence cross-edition case | 1 passed, 67.775 seconds; changed evidence blocks, the original application and target remain unchanged. |
| Existing affected Engine integration/workflow/generated/MCP tests | 55 passed, 216.403 seconds, with a fixed test baseline. |
| Metadata | 43 passed. |
| Policy impact | 10 passed. |
| Contracts | 52 run successfully, with one existing interpreter-dependent skip. |
| Analysis domain | 114 passed. |
| Verifier package | 168 passed. Intentional stale-manifest fixture messages appear in its output; the suite result is successful. |
| Complete structural checkpoint | 73 suites / 121 checks passed; final packaging rerun recorded in the ZIP. |
| Generated API projection | Fresh after owner-generated regeneration. |
| Syntax, scoped diff, preservation, patch round trip and ZIP integrity | Passed; final package records and exact hashes are supplied with the ZIP. |

The full Engine package was not rerun indiscriminately. The selected affected
Engine tests, new lifecycle cases and real MCP/edition-transition workflows
establish the named scope. The structural checkpoint does not replace these
functional observations or certify prose quality.

## Material corrections found during implementation

The first generated result attempted nested diagnostic objects where the owning
contract permits scalar detail fields; it was corrected to bounded scalar keys.
The workflow continuation contract also needed the new `action` input. Repeated
focused recovery initially rejected an already-applied readiness; it now returns
the existing applied outcome while repeat ordinary apply remains unavailable.

An initial system-test placement after the module's main guard prevented
collection. The method was moved into the test class, and the actual cold-MCP
workflow then executed and passed. An early structural run found the examples
file still declaring interface 34; its source declaration was corrected and
all generated inputs refreshed.

One initial 55-test affected-Engine run failed because this task advanced its
own temporary testing `main` while the class retained a snapshot of the previous
revision. The resulting target-stale rejection was correct. Final qualification
kept the baseline stable and reran the affected cases, rather than changing the
production readiness guard or counting the earlier run as green.

The first cross-edition probe used Engine README as all review evidence, then
changed that file during installation. Recovery correctly returned
`ANALYSIS.EVIDENCE_DIGEST_MISMATCH`, preserving the application and target. A
stable-evidence qualification succeeded; a separate explicit drift-rejection
probe tests the negative case. The repair preserves current evidence validation
instead of treating old acceptance as permission to ignore changed evidence.

## Review and operating limits

Source and generated differences were reviewed locally for ownership, data
preservation, action admission, failure semantics, disclosure and scope. No
independent external review was performed in this task; no such review is
claimed. The eight-part design admission remains in the plan.

The facade loads schemas from its configured repository root. Code and schema
installation must remain coherent while the real accepted ref stays at the
admitted expected target. A separate Python module path alone does not select
new schemas. A new process on a read-only host remains read-only.

The repair supplies a supported completion operation; it does not grant access
to a protected `.git` directory. An authorized writable host, unchanged/current
review evidence and the original stored application remain required. Confirm
the installed edition and permissions through the supported operations before
attempting the user's recovery. The action makes at most one publication attempt
per explicit request, and does not push a remote branch.

Catalog hot replacement, decision batching and general output pagination remain
separate product findings. Their omission does not prevent using the new
recovery action for the already-resolved application.

## Source basis

The baseline implementation is identified above. Relevant owners are
`tools/repository_git`, `standards_engine/engine.py`, `agent_workflow.py`, and the
canonical Engine contract. Git's expected-old update and reflog failure behavior
are documented in the official manual:
https://git-scm.com/docs/git-update-ref/2.46.0 . The implementation continues to
use that existing adapter rather than constructing a separate transaction
protocol.

See package `APPLY.md`, `manifest.json`, `checks/` and `qualification/` for the
integrator procedure, exact changed files, logs and the retained cross-edition
probe. Source implementation and user-host acceptance are separate claims.
