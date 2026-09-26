# Workflow detail material reuse — implementation and evidence

**Status:** implemented; local scope verification and consumer measurements are
recorded below. Full-suite baseline failures and supported installed qualification
remain explicit. This is not acceptance of the entire standards migration.

**Base:** `8fef41d18c524c7ac6a1a16f242cc3f549c791a2` (`main`, interface 37).

**Branch:** `performance/workflow-detail-material-reuse`.

## Scope and design

The latest baseline already constructs compact status summaries directly and
supports adaptive whole-record detail pages with explicit oversized-record
retrieval. The remaining measured problem is draft replay within those detail
reads: their evaluation previously omitted the existing operation-material scope.

The Engine entrypoint now creates `ProposalMaterials` with a context manager and
passes it to `workflow_presentation.details`. That function obtains evaluation
inputs through the existing `_evaluation_materials` owner, then performs the
ordinary evaluation. Only these two production functions change. The existing
cache, compiler, Analysis evaluator, public decorator, store, authorization and
publication/recovery implementations are unchanged.

Every request still reads and validates the actual stored Analysis and required
revision, verifies captured content, and observes lifecycle. An eligible exact
proposal projection may be reused; no evaluation or returned page is retained.
Snapshot-backed Analysis uses the same existing input selection, including its
separate proposed snapshot where applicable. The operation ends with scope
cleanup on success, rejection or exception. Public reentry creates another scope.

Cache-disabled, evicted and restarted consumers reconstruct normally. A newer
proposal head does not replace the exact historical Analysis. Review, physical
candidate verification, application and recovery retain their independent full
replay paths. Capture retains its recorded/frozen passes and closure checks.

Interface 37 is unchanged: pages bind the complete observed section, preserve
record order and contents, adapt to the compact byte bound, and return an explicit
full-detail retry for one oversized record. The implementation leaves section-wide
projection, hashing and size calculation intact. It does not add another cache,
change compact mutation-result construction, rewrite standards or tune SQLite.

## Standards consistency

The current Core and executable Router selected Performance, Implementation,
Verification, Development Proportionality, Architecture/immutable replay,
Contracts/evolution/protocols, Library, Persistence, IPC, Security, Code Design,
Commit, Documentation and the relevant oracle/platform guidance. The read-only
routing inputs/result are retained in the delivery evidence. No normative content
or registered operational guidance was edited.

One existing mechanism supplies the missing integration; a new retention owner or
proof framework is unnecessary. The bounded claim is faster repeated detail reads
of the same immutable draft with equivalent complete outputs and failures. Current
history and independent acceptance checks retain their owners. Tests use actual
Git/SQLite and generated interfaces; benchmark fixtures are synthetic standards,
not approvals of real standards. The source comparison names the exact production
functions and hashes. It does not infer simplicity from test counts.

## Measurements

| Actual MCP operation | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| First detail page in a new process | 2.925 s | 2.980 s | 0.98x |
| Next page of the same draft | 2.685 s | 0.253 s | 10.63x |
| Repeat the first page | 2.700 s | 0.252 s | 10.73x |
| Oversized compact request (expected rejection) | 2.733 s | 0.258 s | 10.59x |
| Explicit complete-record retry | 2.733 s | 0.262 s | 10.44x |

Ranges (baseline / candidate), three observations per cell:

- First detail page in a new process: 2.918–2.928 s / 2.930–3.150 s.
- Next page of the same draft: 2.682–2.722 s / 0.247–0.254 s.
- Repeat the first page: 2.699–2.701 s / 0.252–0.257 s.
- Oversized compact request (expected rejection): 2.721–2.765 s / 0.250–0.274 s.
- Explicit complete-record retry: 2.674–2.735 s / 0.253–0.264 s.

Startup plus the complete five-request sequence took a median **14.429 s before and 4.694 s after**, a 67.5% reduction. Each total is formed per sequence before aggregation.

The fixed corpus has **473 files / 4,191,784 bytes**, with a twelve-change-set stored proposal. Its content ID is `snapshot-content:sha256:9629d84fa50bc10bd3524ff7cb8fa14ad17e7eb05bce1c881b1ee91b3ca0aa29`. Both implementations used this same original accepted fixture, with pending and completed historical Analyses for the same proposal revision.

[Raw stdio observations](performance-detail-reuse/stdio-comparison.json), [comparison CSV](performance-detail-reuse/comparison.csv), [sequence totals](performance-detail-reuse/sequence-totals.json) and [resource environment](performance-detail-reuse/resource-environment.json) retain exact source/workload bindings and measurement limits. The candidate was measured as a staged working tree; production hashes, not its then-unchanged HEAD alone, identify the executed implementation.


The comparison uses actual newline-delimited MCP subprocesses, one fixed persisted
baseline workload, and the same executable/dependencies/host on each side. Three
new-server sequences per implementation alternate run order. Each begins cold,
then reads another page, repeats the first page, observes an oversized compact
rejection and follows its explicit full retry. Every domain result matches the
baseline oracle exactly; both text and structured MCP encodings agree. Process
identity metadata is intentionally not part of historical-result equality.

Preparation and original snapshot capture are outside operation timings; process
startup is recorded separately. No package-test process ran during paired timing.
These small samples establish local medians/ranges, not tail latency, a full-suite
speedup or configured Codex performance. A warm result does not satisfy a cold-start
claim. The two methods use one installed supported contract, not legacy modes.

The separate attribution probe found twelve manifest refreshes per baseline warm
page versus zero after integration, with one complete durable-content load and one
fresh evaluation on every request in both implementations. The new regression
asserts those counts and actual stored-revision reads. Counting wraps existing
boundaries without substituting the compiler recipe used for cache eligibility.

## Verification and baseline findings

| Execution | Result |
| --- | --- |
| Complete serial Engine discovery | 372 tests: 368 passed, 3 failures and 1 error; every failing case reproduced on unchanged baseline. |
| Eleven supporting package suites | 518 tests: 516 passed and two environment-dependent skips; no failure/error. |
| Final focused reuse suite | All 12 passed. |
| New replay-count regression on unchanged baseline | Fails as intended: 12 manifest refreshes across three four-edit draft reads instead of zero. |
| Structural checkpoint before qualification | 73 suites / 121 checks passed, separately from tests. |

The combined discovered population is **890 tests: 884 passed, four baseline failures/errors and two skips**. This is not an all-green full-suite claim. Supporting packages ran in separate processes during the early Engine run; these are correctness results, not paired suite timings.

After the full run, the new replay assertion was changed from Mock.assert_not_called to the equivalent call-count equality so a failure does not print the entire captured corpus. All twelve new tests were then rerun on the final code. The benchmark driver also gained explicit source hashes. Production bytes remained unchanged. The final source and generated manifest receive another structural checkpoint after report publication; the archived post-commit evidence records its result.

The four baseline findings are:

| Existing test | Reproduced cause |
| --- | --- |
| `test_analysis.AnalysisWorkflowTest.test_coverage_exclusions_require_exact_evidence_before_resolution` | StopIteration while selecting coverage-attestation from fixture output; the expected work is absent in the current corpus. |
| `test_analysis.AnalysisWorkflowTest.test_proposal_analysis_derives_inputs_and_replays_exact_revision` | Hard-coded semantic transition 1 to 2 for a policy whose accepted revision is already 2; AUTHORING.INVALID_SEMANTIC_REVISION. |
| `test_navigation.NavigationTest.test_proposal_query_projects_every_request_from_an_exact_revision` | The same obsolete hard-coded policy revision transition; AUTHORING.INVALID_SEMANTIC_REVISION. |
| `test_process_reuse.ProcessReuseTest.test_real_stdio_restarts_read_the_same_retained_snapshot` | The assertion compares full MCP envelopes from fresh servers, including intentionally different runtime instance IDs. |

[Verification inventory](performance-detail-reuse/verification.json) and [baseline dispositions](performance-detail-reuse/baseline-failures.json) identify exact commands and results. Completed command logs are retained under the archive’s `evidence/` directory; preliminary fixture setup and interrupted invocations are not counted as passing tests. The original baseline-counter failure produced a redundant full-argument dump; its hash and the complete bounded-diagnostic rerun are recorded instead of bundling megabytes of repeated corpus text.


The twelve new tests cover exact warm/cold page equality, one durable load and
fresh evaluation per call, disabled/evicted retention, oversized explicit retry,
contiguous paging, unchanged durable Analysis, stale historical revisions,
quarantine/purge, actual content and revision corruption, lifecycle changes after
input acquisition, reentrant independent scopes, exception cleanup, snapshot-backed
Analysis, application-purpose denial, invalid paging and result-mutation isolation.
The existing presentation tests preserve every section, integer representation,
Unicode JSON sizing, continuation boundaries and cold oversized-record transport.

Baseline failures are not relabeled as passes and no assertions were removed.
The exact old-fixture failures are independently reproduced on unchanged baseline
source and retained for separate maintenance. Their code and owning semantics are
outside this change. Required current-path evidence is still exercised directly;
this disposition is not a blanket exclusion of failing tests.

## Environment and handoff

Execution used isolated CPython 3.13.5, Git 2.47.3 and the recorded core dependency
versions. The project supports CPython 3.11/3.12; local `rpds-py` 2026.5.1 differs
from locked 2026.6.3. Optional rich-environment packages were excluded from both
benchmark sides. The lock and support declarations are unchanged. Root execution
prevents the unprivileged POSIX permission case; the supported-runtime dependency
check is also skipped by its existing condition.

The official SDK, configured Codex installation and an independent reviewer were
unavailable. Supported locked qualification, relevant installed-client behavior
and independent review remain separate gates. Full-suite baseline failures also
remain unresolved. Successful raw stdio and real repository tests are evidence of
their actual boundaries, not substitutes for those gates.

The source was recovered from the exact Actions Git bundle and verified against
its archive hash. All commits use Git CLI on the dedicated local branch. Original
local `main` remains at the baseline; the user's live checkout, databases, archived
proposals and client configuration were neither accessed nor changed. Runtime
schemas, persisted contracts, normative files and previous optimizations remain
byte-identical. The archive manifest records the final commit/tree and file hashes.

Use one route in the archive's `APPLY.md`. On a newer or divergent main, review and
port the small implementation rather than overwrite later work; refresh generated
verification inputs from that actual combined tree. Restart the MCP process after
installing the changed code. Interface edition and operation catalog remain 37.

## Reproduction

Use a complete baseline and candidate checkout plus the supported locked Python.
The fixture directory must be new. The driver creates only disposable fixture state
and writes the selected measurement output:

```bash
SCRIPT=/absolute/candidate/docs/plans/engine-routing-review-ux/reports/performance-detail-reuse/measure_details.py
python "$SCRIPT" --baseline /absolute/baseline --fixture /tmp/detail-fixture --prepare
python "$SCRIPT" --baseline /absolute/baseline --candidate /absolute/candidate \
  --fixture /tmp/detail-fixture --output /tmp/details.json --repeats 3
PYTHONPATH=. python -m unittest tools.standards_engine.tests.test_workflow_detail_reuse -v
PYTHONPATH=. python -m unittest tools.standards_engine.tests.test_workflow_presentation -v
```

The delivery includes commands and logs for the complete Engine and supporting
package runs and all baseline controls. Structural verification is separate from
functional tests. The paired measurement supplies claim evidence, not an arbitrary
wall-clock assertion embedded in an ordinary regression test.
