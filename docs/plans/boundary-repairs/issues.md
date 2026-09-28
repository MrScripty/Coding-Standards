# Findings and dispositions

> **Current disposition (2026-09-27): Accepted.** The former environment and reviewer gates are resolved by the exact-source CI and independent review linked in the acceptance decision. All external observations are deferred as non-blocking; no production repair was required. See the [acceptance-owner decision](../typed-routing-edits/reports/acceptance-dispositions.md).

| ID | Boundary / owner | Disposition | Required evidence |
|---|---|---|---|
| F04 | Graph logical resolution | fix in B1 | Bare/path spellings independent of ambient filesystem |
| F05 | Engine -> SnapshotStore path admission | fix in B1 | Final symlink rejection and preservation through both entry points |
| F06 | Contracts -> domain integer representation | fix in B1 | Structural-family conformance, real proposal and no-effect negatives |
| F07 | Analysis evidence digest | fix in B1 | Common syntax cases across three representations, live byte rejection |
| F11 | CI selection | fix in B1 | Invoke all six existing direct package suites |
| F07a | Canonical Digest pattern admits final LF | fix in B1: maxLength 71; interface 44 | Shared corpus and independent validator/projection checks |
| V1 | Current discovery examples | corrected to interface 44, assertion retained | Final schema/contract tests |
| V2 | Local retained-state checker | corrected focused rejection path; original verdict preserved | Fresh-process retained-state rerun |
| E1 | Supported locked runtime | integration owner; pending | Existing CI with Python 3.12 and unchanged lock |
| E2 | Independent material review | integration owner; pending | Review exact patch and disposition findings |

F01–F03, F08–F10, F12–F16 remain outside the requested boundary repair. No caches,
maintenance policies, API redesign or historical documentation rewrite is added.

The Engine README opening was updated only for this release identity and its
boundary contract; broader historical-documentation cleanup remains deferred.
