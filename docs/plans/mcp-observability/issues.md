# Findings

## I1 — baseline proposal-analysis fixture (medium, deferred)

`test_analysis.AnalysisWorkflowTest.test_proposal_analysis_uses_one_projection_and_one_verified_base`
hardcodes accepted semantic revision1/proposed2. Both the candidate and a clean
Git clone of baseline `188beda1fa477d21d576c233dd8c7f4c4c267d23` return
`AUTHORING.INVALID_SEMANTIC_REVISION` before the test reaches its projection-count
assertions. Independent one-test baseline run:1 test,1 failure,1.397s; candidate:
1 test,1 failure,1.606s. This source test is unchanged by issue3.

Owner: existing analysis test/standards-content maintainers. Disposition: defer
outside the recorder write set; do not edit normative standards or weaken the
validator. Revisit when maintaining this fixture against accepted policy revision.
Required evidence: bind the test to the actual immutable accepted policy revision,
then verify its intended projection-count claim. Full suite results remain visible;
this is not labeled a successful complete Engine run.

## Resolved review findings

Independent reviewer found and verified resolution of R1–R7: diagnostic field
binding, malformed-envelope coverage, measurement failure, normal retention loss,
report scope/bounds, pre-migration capability checks and residual private SQLite
content. See reports/independent-review.md for source-bound evidence.

Actual model/client traces are outside this task: synthetic process evidence does
not certify model intent or acquisition. No new model qualification is claimed.
