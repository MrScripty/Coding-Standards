# Retirement of the last hand-listed metadata check

Reviewed revision `a5e8bf7ee4f29ba14826df1ce363bef13fbe2963`. This is the review
record supplied to the Engine's `maintain_evidence` operation for the retirement
below. It records what was checked before the retirement; it is not a coverage
attestation.

## Decision

On 2026-11-13 the repository owner decided to retire
`release-maintenance-policy/metadata-closure` and accepted that the coverage
certificates it invalidates are reissued afterwards, each after its own review.
Fifty-five sibling checks were retired on 2026-11-12; this one was held back
only because of that certificate effect.

## What is retired

| Item | Disposition |
| --- | --- |
| Check `release-maintenance-policy/metadata-closure` | Retired. It ran `metadata_graph` over a hand-typed list of 12 module paths. |
| Suite `release-maintenance-policy` | Retired by the Engine because it has no other check. |
| Registry entry for that suite | Removed with the suite. |
| Catalogue node `release-maintenance-policy` (`enforcement-suite`) | Removed with the suite. |

The suite required `release-reference-closure`, which stays registered with its
own checks. No registered suite requires `release-maintenance-policy`.

## Why the check is redundant

The check `canonical-corpus-metadata/canonical-corpus` validates every member of
`evaluation/standards-effectiveness/canonical-module-corpus.toml` through the same
`validate_module_metadata` call the retired check used.

- All 12 listed paths are among the 74 corpus members.
- Mutation test on a scratch copy of the reviewed revision: four defects
  (a `Requires` target that does not exist, a removed `Level` line, a wrong
  `Canonical owner` path, a `Specializes` target that does not exist) were
  introduced one at a time into each of the 12 modules, 48 mutations in all.
  The retired check failed 48 times. The whole-corpus check failed the same 48
  times with the same diagnostic code each time. No defect was reported by the
  retired check alone.

The retired check therefore could not fail for a reason the whole-corpus check
does not also report.

## Graph and certificate effect

- The removed node is neither the source nor the consumer of any policy-impact
  relationship, and no relationship names `suite:release-maintenance-policy` as
  its evidence owner. No relationship is removed or re-owned.
- The node catalogue digest is part of every coverage requirement. Removing a
  node changes all 53 requirement IDs, so the 16 certificates that were current
  at the reviewed revision become stale. The 8 certificates that were already
  stale stay stale.
- Stale certificates are left in place (`prune_stale_certificates` is `false`).
  A stale certificate is ignored when coverage is read; its policy unit reports
  `review-required` until a new certificate is published for it.

## Counts

| | Before | After |
| --- | ---: | ---: |
| Registered suites | 24 | 23 |
| Checks | 67 | 66 |
| Catalogue nodes | 122 | 121 |
| Certificates current / stale | 16 / 8 | 0 / 24 |

## Engine operation

`maintain_evidence` with this file as evidence, first with `apply: false` and
then with `apply: true`. Plan: `retire_checks` naming the one check; no suite,
input, description, relationship or consumer entries;
`replacement_evidence_owner` `review:consumer` (unused, because no relationship
names the retired suite). The Engine's candidate verification passed with 23
suites and 66 checks.
