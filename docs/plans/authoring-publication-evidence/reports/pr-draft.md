# Pull request draft

**Title:** feat(standards): clarify publication and preflight evidence

## Owning plan and milestone

- Plan: `docs/plans/authoring-publication-evidence/plan.md`
- Milestone: A1 — Explicit publication observations and early evidence failures
- Target: `main`; accepted base: `149ba317e9397519bc181a048ecf76aef129a69c`
- Local candidate tested: `033dde3623a6bd917d3def5c75b9c748d6cd4f27`
- Draft PR: [#2](https://github.com/MrScripty/Coding-Standards/pull/2)

## Intended outcome

- Report durable publication receipts separately from fresh, read-only target,
  worktree, and index observations across apply, recovery, and later status.
- Preflight destination evidence before readiness, preserve final evidence and
  authorization checks, and expose bounded authoring diagnostics with application
  redaction.
- Coordinate interface 46, result projection 8, generated consumers, and exact
  interface 45 client-upgrade dispositions while retaining request contract 6 and
  application/readiness persistence schemas.
- Make publication observation own descriptor exhaustion, path/root races, and
  cancellation cleanup, including a local-only read of the canonical target ref.
- Keep reconciliation writes and evidence bundle acquisition for later milestones.

## Prerequisites and exclusions

The branch starts from accepted `main` at `149ba317e9397519bc181a048ecf76aef129a69c`.
A1 adds no dependency on the unaccepted Pumas coordinated plans or acquisition
contract. It does not implement A2 evidence bindings, durable evidence-bundle
acquisition, reconciliation writes, a Pumas consumer, or a migration of existing
application/readiness persistence formats.

## Ownership, persistence, security, and lifecycle

Repository Git owns fresh checkout/index observation and descriptor lifecycle;
the Engine owns publication projection; Analysis owns evidence validation. Durable
receipts and existing authorization remain the publication authority. The change
does not alter request contract 6 or application/readiness persistence schemas and
requires no retained-state migration. Descriptor exhaustion, filesystem races, and
cancellation release observation resources. Application-facing diagnostics remain
bounded and redact private exception text.

## Validation

On the committed source candidate `033dde3623a6bd917d3def5c75b9c748d6cd4f27`,
Python 3.12 with the hash-locked requirements, offline:

- The complete A1 acceptance command ran seven modules (`test_repository`,
  `test_analysis`, `test_coverage_publication`, `test_agent_workflow`,
  `test_publication_recovery`, `test_registration_contract`, and
  `test_supporting_workflow`): **83 tests passed in 264.677 seconds**.
- `verify_repository(refresh_verification_inputs=False)`: **73 suites and 121
  checks passed**.
- `git diff --check` passed.

The suite exercises test-owned temporary Git repositories and controlled failure,
race, and cancellation cases. It does not qualify a live remote repository or live
MCP publication. Mocked boundary assertions are unit evidence, not real partial
clone or hosted-service evidence. Exact-candidate hosted CI is pending for the
updated PR head; run `36646667390` and CodeRabbit status applied only to the older
`78a69fbb` head.

## Independent review and outstanding acceptance

GPT-6 Astra Medium's final read-only architecture review of candidate `033dde36`
reported no actionable findings. It confirmed the earlier local-only target-read
finding and premature A2 sequencing finding are resolved. The reviewer noted that
the regression for `local_only=True` is mocked boundary evidence and does not by
itself demonstrate real partial-clone behavior.

Earlier Standards Engine routing selected 30 applicable standards with no
unresolved questions; the result was checked against the implemented obligations.
GPT-6 Luna High completed bounded spec/reference discovery and found no remaining
gap in the reviewed A1 contracts. The independent Passeur security/lifecycle review
remains outstanding: the available Passeur service is bound to Pumas-Library, so
no Coding-Standards review was submitted through that unrelated repository context.

PR #2 remains draft. Its published head must be updated to the tested A1 source
candidate before exact-head hosted checks can qualify. No merge is requested or
performed. Maintainer-authorized integration to `main` remains required before A1
is accepted and A2 implementation begins.
