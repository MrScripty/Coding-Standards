# Findings

## I1 — baseline proposal-analysis fixture (medium, resolved)

`test_analysis.AnalysisWorkflowTest.test_proposal_analysis_uses_one_projection_and_one_verified_base`
originally hardcoded accepted semantic revision 1/proposed 2. Both the candidate and a clean
Git clone of baseline `188beda1fa477d21d576c233dd8c7f4c4c267d23` return
`AUTHORING.INVALID_SEMANTIC_REVISION` before the test reaches its projection-count
assertions. Independent one-test baseline run:1 test, 1 failure, 1.397 s; candidate:
1 test, 1 failure, 1.606 s. At initial handoff head 4887b7af this source test was unchanged by issue3.

Owner: analysis fixture maintainers. Parent explicitly authorized this bounded
follow-up for PR #4. Disposition: resolved by deriving the accepted semantic
revision and its successor from the same immutable snapshot used for the proposal,
before the counting mocks. Policy existence, real proposal/analysis results and
both count assertions remain required. Validator and normative content unchanged.
The targeted case passed (3.748 s), all 23 analysis tests passed (113.275 s), and
the full serial Engine suite passed all 636 tests (2161.675 s). Independent fixture
review passed; see reports/fixture-review.md. Historical baseline failure evidence
above remains retained rather than relabeled as a baseline pass.

## Resolved review findings

Independent reviewer found and verified resolution of R1–R7: diagnostic field
binding, malformed-envelope coverage, measurement failure, normal retention loss,
report scope/bounds, pre-migration capability checks and residual private SQLite
content. See reports/independent-review.md for source-bound evidence.

Actual model/client traces are outside this task: synthetic process evidence does
not certify model intent or acquisition. No new model qualification is claimed.

## I2 — publication authentication (resolved)

The GitHub CLI reported an invalid configured `GH_TOKEN`, initially treated as a
publication blocker. A later explicitly authorized attempt through the existing
Git remote succeeded without inspecting/copying tokens or changing authentication.
Remote head 4887b7af was verified and the parent opened draft PR #4. The CLI failure
did not establish failure of the separate Git transport. Existing bundle and
checkout were preserved; subsequent publication uses the approved Git branch.
