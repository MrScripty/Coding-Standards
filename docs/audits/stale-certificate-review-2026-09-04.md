# Stale certificate review

Reviewed revision `53e750327c1f8410d3db278eb652e70df52ae118` through Engine
snapshot reads, the declared consumer graph, stored claims, and evidence-input
projections. All **51 existing certificates remain stale**. Every stored claim
was matched to its current subject and requirement; none was renewed.

The [subject inventory](stale-certificate-review-2026-09-04.evidence.json)
records all 51 comparisons, 445 incident relationship projections, selected
evidence suites, removed checks, and renewal requirements. This is a review of
certificate validity and the work needed for renewal, not a completed semantic
audit of every implementation consumer or a replacement coverage attestation.

## Findings

### F1 — High: receipt behavior is missing from the relevant coverage inputs

The new `tools/standards_analysis/standards_analysis/coverage_publication.py`
owns receipt construction and readback, exact evidence verification, historical
authorization, and publication binding. It has no explicit policy-consumer
relationship. Its only inclusion in a subject's transitive evidence inputs is
through `a1c-public-cutover` for `topic.dependencies.requirement-and-ownership`.
`tools/standards_engine/tests/test_coverage_publication.py` is absent from every
subject's declared evidence inputs.

In particular, neither file belongs to the declared input closure of
`topic.architecture.immutable-authority-closure`. Its selected suites are
`a1c-aggregate-replay`, `a1c-snapshot-lifecycle`, and `contract-authority-scope`;
their dependency closures do not include either file. A later receipt-only
implementation change therefore does not invalidate that subject through these
inputs. A repository-wide package check does not establish this policy link.

This omission was introduced by the publication implementation. Before renewing
the affected certificates, explicitly model receipt publication/readback as a
consumer of its actual policy owners and include the deciding evidence. Select
the smallest relevant relationships; making every certificate depend on every
source file would defeat dependency-local review. Verify invalidation with a
change to a selected input and preservation for an unrelated input.

### F2 — Medium: the oracle decision model cannot express legitimate narrower claims

`evaluation/standards-effectiveness/suites/evidence-oracle-boundaries.toml`
unconditionally rejects `generated-output` and `local-implementation` oracle
values. Its claim field distinguishes only `named` from `missing`; the declared
`external_contract` field does not affect any rule.

The current oracle policy distinguishes freshness, local consistency, and
external conformance. Local agreement can establish consistency while remaining
insufficient for external conformance. The current decision model cannot name
that difference. The existing negative fixtures cover inappropriate semantic
claims, but do not cover the legitimate narrower claim.

A scratch probe using the production predicate evaluator confirmed rejection
for both oracle values with both `external_contract=none` and `selected`;
the exact inputs/results are in the inventory. This is a limitation in the
modeled guidance, not evidence that the runtime verifier misexecutes its rules.

Before renewing `workflow.verification.evidence-oracle-boundary`, distinguish
the actual property claimed and add paired decisions for supported freshness
or consistency claims and unsupported semantic-conformance claims. Assertions
should compare structured decisions, not sentences. Changing only the external
contract flag would still leave the claimed property ambiguous.

### F3 — Medium: some graph evidence descriptions overstate the retained checks

The replay relationship manifest says `a1c-aggregate-replay` enforces immutable
AnalysisState replay and `a1c-snapshot-lifecycle` enforces exact capture/storage.
The latter suite currently runs a declarative decision table and path-presence
checks. It does not execute the real SQLite adapter or the publication
integration test. Similarly, the oracle relationship says its suite enforces
the policy and agent projections, but retained checks exercise a decision table
and the presence of consumer paths; they do not judge the prompts' meaning.

Forty-eight of the 51 subjects select suites affected by the phrase-check
removal. Removing those assertions was appropriate. Their old acceptance
rationales must now be reconciled with the narrower automated observations and
any actual manual or behavior evidence. Do not restore wording assertions or
count existing Python test files as executed tests. Name what each evidence
owner decides, and link/run the actual behavior evidence where the claim needs
it. The previous publication test result remains useful recorded evidence,
but its successful run does not repair missing graph relationships.

### F4 — Low: current graph descriptions retain obsolete Interface versions

The generated-contract suite describes a v12 public algebra, and
`policy-impact/topic.contracts.schemas.toml` describes rendering the v12 result
algebra. The Engine Interface is now version 23. These descriptions can mislead
a reviewer about the accepted consumer surface even when generated freshness
passes. Prefer the canonical contract reference where repeating a version adds
no useful meaning; verify actual operation/variant coverage separately.

## Renewal decisions by scope

| Current policy owners | Subjects | Review result and remaining obligation |
| --- | ---: | --- |
| Generated-contract profile and Router | 3 | Current routing/profile scope is distinguishable from IPC, persistence, and language binding. Reconcile routing and generated-consumer evidence with the current Interface. |
| Architecture, replay, and code design | 4 | Stable IDs survive the owner moves. Replay now distinguishes in-process inspection from cold replay and historical permission from current access. F1 prevents a complete replay closure claim. |
| Contracts and schemas | 7 | Current guidance distinguishes representation, semantic authority, version roles, invariant outcomes, and proof lifetime. Review receipt consumers and current generated/public behavior; resolve F3/F4. |
| Cross-platform and security | 2 | Canonical component ordering is supporting evidence. Renewal still needs claim-matched filesystem identity/containment review; Linux results or platform-name fixtures do not prove every real target. |
| Dependencies | 2 | The package-input closure includes the receipt implementation. This is ownership/dependency evidence, not a substitute for the missing replay relationship. Review current consumer declarations and retained conformance evidence. |
| Commit | 13 | Retained decision tables cover authority and lifecycle choices. Structural disposition records do not establish commit-message quality or current prompt meaning; record those consumer reviews separately. |
| Planning | 16 | Retained plan-contract and decision fixtures cover structure and modeled admission. Reconcile prompts/template with proportional planning, bounded systemic review, and actual acceptance claims. Graph completeness remains a review decision. |
| Verification and oracles | 4 | Ordinary regressions no longer require costly evidence admission. Resolve F2/F3, retaining the distinction between sampled decisions, real behavior, and semantic review. |

Two subjects changed semantic revision from 2 to 3:
`topic.architecture.immutable-authority-closure` and
`workflow.verification.acceptance-claims`. Their legacy unchanged-meaning
rationales cannot decide the new meaning. Nine subjects moved canonical owner;
their stable subject IDs correctly survive the moves. The other 49 subjects
preserve their semantic revision, which does not establish unchanged consumers
or sufficient evidence.

All 14 referenced historical evidence files are present. The inventory records
their bytes observed at the reviewed revision, not a claim that legacy schema-5
certificates pinned those bytes at their original review. Historical reviews
remain historical evidence; they cannot be silently upgraded to Engine receipts.

The three subjects with no removed phrase checks in their selected suite
closure are filesystem paths, filesystem containment, and planning projection
completeness. They still have changed consumer/evidence inputs and stale claims.
There is no basis to bulk-renew that smaller set either.

## Validation and disposition

Public Engine reads of the 14 current owners returned all 51 subjects as
`review-required`. Read-only production coverage compilation from the exact Git
archive agreed with every public requirement ID and reported zero current
claims. The stored-claim inventory matched all 51 legacy requirement IDs.
Production suite dependency projections established F1; the production predicate
evaluator established the F2 model limitation. No standards, graph declaration,
certificate, or Engine state was directly edited for this review.

The public `verify_repository` checkpoint passed all 271 suites and 858 checks
without refreshing generated inputs. Inventory consistency and staged whitespace
checks passed. These checks validate the review's mechanical observations and
repository consistency; they do not close the semantic findings above.

F1–F3 need correction or an explicit, supported narrowing of the relevant claim
before affected renewals. F4 belongs with that evidence-description correction.
After those changes, perform the actual consumer dispositions and policy audits,
commit their exact evidence, and publish supported claims through Engine audit
review, readiness-bound verification, and application. The outstanding downstream
pilots assess agent effectiveness; they are not a universal prerequisite for
every policy certificate.
