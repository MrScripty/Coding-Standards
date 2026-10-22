# 2 → 4 → 3 acceptance reconciliation — 2026-09-29

This record separates exact-source verification, reviewer recommendation, and
acceptance-owner disposition. It does not change any plan's acceptance status.

| Priority | Exact source and evidence | Independent review | Owner disposition |
| --- | --- | --- | --- |
| 2 — routing-fact ergonomics | Accepted source, supported CI, live observation, and review are already recorded in its plan. | Favorable external review already recorded. | `Accepted` in its existing plan; no reopening. |
| 4 — review-evidence packaging | Candidate `91ceb0fe`; existing workflow `36509340996` reports a completed/successful Engine job. Local F1–F4 and F4-C1 evidence, including an offline recipient packet, is retained. The first packet explicitly lacks a raw CI log. | [Independent candidate review](../../review-evidence-packaging/reports/final-candidate-review.md) finds no blocker and recommends owner review. | `Verifying` / partial in the existing plan. The owner has not recorded P-A8 acceptance; this report does not supply that decision. |
| 3 — targeted test strengthening | Candidate `39d55dc3` is present on remote GitHub. Local T-A1–T-A5 and affected Python 3.12 tests are recorded. A successful hosted locked run for this exact commit has not been retrieved here. | [Independent candidate review](../../targeted-test-strengthening/reports/final-candidate-review.md) finds no blocker and recommends owner review. | `Verifying` / partial in the existing plan. T-A6 exact-candidate CI and the owner's T-A7 disposition remain open. |

The connected GitHub Actions lookup by commit returns only PR-triggered runs,
so an empty list for `39d55dc3` is not evidence that push CI failed or did not
run. The local GitHub CLI token is invalid and this sandbox cannot resolve the
GitHub API host. The owner has no run ID available. A directly retrieved
job/source record, or a new exact-candidate run under the supported workflow,
is needed to qualify the push candidate. Do not reuse packaging's successful
baseline run as test-candidate CI.

The reviewer recommendations above are read-only judgments. The acceptance
owner must compare the exact CI material with each plan's claim and record the
decision in that plan. Until then the 2 → 4 → 3 sequence is not closed and the
Milestone 8 pilots receive no A3 acceptance credit. The bounded
[pilot admission](milestone-8-pilot-admission.md) can be prepared independently.
