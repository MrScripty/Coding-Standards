# A1c Final Acceptance

**Status:** `accepted`

**Product implementation:** `0911c079054185abca8ffe6973d26cdee34dedf7`

**Platform harness and Linux evidence:** `1c9da36507e28806cde72d50c3acf60e020e7d24`

## Accepted Scope

A1c is accepted for Linux on CPython 3.11 and 3.12. Windows and macOS are not
accepted or advertised as supported platforms. Their future promotion requires
real environment-qualified execution of the retained provider-neutral harness.

Cross-engine stored-state compatibility remains deferred until feature
completeness. A2 authoring remains outside A1c and requires separate planning
and admission.

## Claims

| Claim | Result | Evidence |
| --- | --- | --- |
| A1C-A1 generated v12 Interface and external schema semantics | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A2 immutable traced snapshot closure | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A3 aggregate lifecycle and transaction behavior | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A4 cold deterministic analysis and child inspection | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A5 dependency-local coverage identity | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A6 atomic A1b removal and migration closure | satisfied | [Milestone 5 cutover evidence](a1c-cutover-evidence.md) |
| A1C-A7 real Linux CPython 3.11/3.12 system behavior | satisfied | [Platform evidence](a1c-platform-evidence.md) |
| A1C-A8 eight agent-facing workflows and handle transfer | satisfied | [Platform evidence](a1c-platform-evidence.md) |

## Verification

- Provider-neutral CLI producer and consumer passed on real Linux x86_64 with
  CPython 3.11.14 and 3.12.3.
- Focused harness regressions passed on both supported Python versions.
- All 24 Standards Engine and 433 Standards Verifier tests passed.
- Generated contract and repository verification projections were fresh.
- All 227 declarative suites and all 53 retained Bash checkers passed.
- Plan structure, lifecycle fixtures, Ruff, staged diff hygiene, migration
  absence, coverage/certificate equality, and repository cleanliness passed.

No A1b compatibility implementation, product fallback, platform-specific
identity, provider workflow, binary store, or A2 behavior was added.
