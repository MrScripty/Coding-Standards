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
  cancellation cleanup. Keep reconciliation writes and evidence bundle acquisition
  for later milestones.
- Replace the supporting-workflow test's dependency on accepted Security exposure
  with a test-owned unexposed standard.

## Validation

- Repository Git observer tests: 31 passed.
- Analysis tests: 21 passed.
- A1 acceptance modules: 30 passed.
- Direct and warm-cache supporting-workflow cases: 2 passed.
- Repository verification: 73 suites, 121 checks passed.
- `git diff --check` passed.

## Review notes

GPT-6 Astra architecture and Standards reviews and GPT-6 Luna Spec review found no
remaining findings after follow-up. Passeur review remains pending because the
available Pumas and Tuldok services are bound to unrelated repositories; no review
was sent to either wrong project. Hosted exact-candidate CI has not been run.

The branch is prepared locally and has not been pushed. This draft does not request
merge approval or change the separately dirty main checkout.
