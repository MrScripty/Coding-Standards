# Pull request draft

**Title:** feat(standards): clarify publication and preflight evidence

## Owning plan and milestone

- Plan: `docs/plans/authoring-publication-evidence/plan.md`
- Milestone: A1 — Explicit publication observations and early evidence failures
- Target: `main`; accepted base: `149ba317e9397519bc181a048ecf76aef129a69c`
- Repaired source candidate tested: `ecbf25cdcd8218b44e68b6adb359c7efaeea765d`
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

The branch starts from accepted `main` at
`149ba317e9397519bc181a048ecf76aef129a69c`. The local A1 gate passed on the
repaired source candidate. The plan remains `Verifying` until a successful
exact-head hosted run, the required Passeur review, and accepted main integration
are complete.
Pumas-Library acquisition/runtime plans are separate; Q1/AQ-HTTP is not ready and
is not an A1 dependency.

A1 excludes A2 evidence binding, durable evidence-bundle acquisition, reconciliation
writes, Pumas consumers, and migration of existing application/readiness persistence
formats.

## Ownership, persistence, security, and lifecycle

Repository Git owns fresh checkout/index observation and descriptor lifecycle;
Analysis owns evidence validation; the Engine owns publication projection. Durable
receipts and existing publication authorization remain authoritative. The change
does not alter request contract 6 or application/readiness persistence schemas and
requires no retained-state migration. Descriptor exhaustion, filesystem races, and
cancellation release observation resources. Application-facing diagnostics remain
bounded and redact private exception text. Readiness preflight rejects references
that publication will overwrite; final candidate validation remains intact.

## Validation

On integrated candidate `ecbf25cdcd8218b44e68b6adb359c7efaeea765d`, Python 3.12
with the hash-locked requirements, offline:

- The seven existing A1 modules (`test_repository`, `test_analysis`,
  `test_coverage_publication`, `test_agent_workflow`, `test_publication_recovery`,
  `test_registration_contract`, and `test_supporting_workflow`) plus five
  current-interface consumer modules (`test_capture_handoff_transport`,
  `test_consumer_publication`, `test_routing_fact_transport`,
  `test_runtime_identity`, and `test_schema_presentation`) passed **108 tests in
  427.181 seconds**. The five consumer modules independently passed 24 tests in
  165.995 seconds. The diagnostics regression retains valid bounded spaced,
  Unicode, and dot-prefixed repository references while preserving application
  redaction.
- `verify_repository(refresh_verification_inputs=true)` and the subsequent
  `refresh_verification_inputs=false` run each passed **73 suites and 121 checks**;
  refresh produced no manifest change. `tools/standards_verifier/verify.py
  --complete` passed all 73 suites with zero failures or blocked checks.
- `git diff --check` passed.

The suite exercises test-owned local Git repositories and controlled failure,
race, cancellation, readiness, and destination-overwrite cases. Mocked boundary
assertions are unit evidence, not evidence of real partial-clone or hosted-service
behavior. No live remote repository or hosted MCP publication was qualified.

## Independent review and outstanding acceptance

GPT-6.1 Sol high's read-only review of `f676cfaf` found two P2 gaps: unbounded
phase-specific evidence diagnostics and acceptance of evidence at paths publication
would overwrite. GPT-6.1 Sol medium repaired both in `01bb2d03`; Sol high's
read-only follow-up confirmed both findings closed and found no new actionable
issue. The regression tests bound diagnostics and reject overwritten evidence and
exclusions before readiness or candidate publication.

Earlier Standards Engine routing selected 30 applicable standards with no
unresolved questions; the resulting obligations were checked against the source.
GPT-6 Luna High's bounded spec/reference review found no remaining gap in the
reviewed A1 contracts. The required Passeur security/lifecycle review remains
outstanding because the available service is bound to Pumas-Library; no review was
sent through that unrelated repository context.

GPT-6.1 Sol high classified all nine failures on the earlier candidate's hosted
run as stale current-interface expectations, not intentional interface-45 client
fixtures. GPT-6.1 Sol medium changed exactly five installed-interface assertions
to 46 in the reviewed commit above; all other lifecycle, disclosure, and legacy
client checks remain intact. Sol High's read-only architecture review then found
that authoring diagnostics dropped otherwise valid spaced, Unicode, and
dot-prefixed evidence paths. Sol medium fixed the bounded authoring projection in
`e6da2e5f` with focused coverage for supported and unsafe paths and application
redaction; Sol High's follow-up confirmed closure with no further architecture
findings. The generated suite-input digests were refreshed and committed in
`ecbf25cd`.

Hosted run `36648831399` failed on the stale assertions after 612 tests and did not
reach its structural-verifier step. Prior exact PR-head run `36651259589` is for
`95b13802` and also failed on those stale assertions. Run `36653728027` is for
`6921489c` and remained in progress at the time of this report; it predates the
path-diagnostic fix and refreshed digests. A fresh successful exact-head hosted
run for the current candidate is pending. PR #2 remains draft. No merge is
requested or performed.
Maintainer-authorized main integration remains required before A1 is accepted and
A2 implementation begins.
