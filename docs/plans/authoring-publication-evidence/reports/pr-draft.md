# Pull request draft

**Title:** feat(standards): clarify publication and preflight evidence

## Summary

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
  Keep reconciliation writes and evidence bundle acquisition for later milestones.
- Replace the supporting-workflow test's dependency on accepted Security exposure
  with a test-owned unexposed standard.

## Validation

- Before the final review repair, Repository Git observer tests: 31 passed;
  Analysis tests: 21 passed; A1 acceptance modules: 30 passed; direct and
  warm-cache supporting-workflow cases: 2 passed; Repository verification: 73
  suites, 121 checks passed.
- The final local-only target-read regression and adjacent recovery assertion
  passed: 2 tests in 9.977 seconds.
- One post-repair combined run encountered stale suite-input digests for
  `engine.py` in temporary fixture repositories. The integration owner refreshed
  the generated suite-input manifest; the full post-refresh acceptance rerun is
  pending.
- `git diff --check` passed for the source repair.

## Review notes

GPT-6 Astra architecture and Standards reviews and GPT-6 Luna Spec review found no
remaining findings after follow-up. The final Astra review found one local-only
target-read omission and one plan-state sequencing error. The target read is fixed
in `7d8904a9`; the plan now keeps A1 in final verification and defers A2 until A1
is accepted and merged. A second final architecture review is pending. Passeur
review remains pending because its available service is bound to Pumas-Library;
no review was sent to that unrelated project.

Draft PR [#2](https://github.com/MrScripty/Coding-Standards/pull/2) is open against
`main` at `149ba317e9397519bc181a048ecf76aef129a69c`. The published head is still
`78a69fbb`; the local A1 branch includes the reviewed repair at `7d8904a9` and
awaits its push. Hosted run `36646667390` is for the older `78a69fbb` head and is
not candidate evidence for `7d8904a9`. The PR remains draft; no merge is requested
or performed, and the separately dirty main checkout is unchanged.
