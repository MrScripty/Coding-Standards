# CI Test Audit: Source Review and Diagnostic Evidence

**Review date:** September 29, 2026, America/Vancouver. GitHub timestamps below are UTC on September 30 where stated.

**Scope:** The user-supplied audit, its named source paths, their direct fixture consumers, the existing workflow, verification seams, and canonical planning/verification/performance/architecture policy. This is not a claim of a new exhaustive behavioral audit of the entire product.

## Source and Integrity

Reviewed branch head: `8260489e8e3ad6b7e170bbf7bd411bac90758abd`.

Actual tested PR merge commit: `fa7c4f9d5edee0a94baf6fff0ed29452ffaff7db`.

Tree for both: `c249e251efcf48ad13d4bfaf854cf496544bece7`.

Main/base: `149ba317e9397519bc181a048ecf76aef129a69c`.

The source came from GitHub run `36661745679`, artifact `11073664150`, named `engine-source-fa7c4f9d5edee0a94baf6fff0ed29452ffaff7db`. The downloaded ZIP digest matched GitHub's published `sha256:a0b764813c3ff94acfc40906d82d31fe1be5f05d385547607e3e30a893480f62`. Its only member was `source.bundle`. A local clone of that bundle was used for inspection and diagnostic probes; its source tree remained clean. No remote branch, workflow or production file was changed.

The workflow fetches `github.sha`, checks it out as `main`, records a bundle, installs the locked Python 3.12 environment, then invokes 13 unittest package groups and the complete verifier. See `.github/workflows/purpose-separated-engine.yml:25-83`. The PR-head SHA and actual checked-out merge SHA must both be retained in future timing evidence.

## Hosted Facts

| Run | Source | Outcome | Job duration | Verification step |
| --- | --- | --- | --- | --- |
| `36661745679` | PR head `8260489e`; tested merge `fa7c4f9d` | success | 45m46s | 45m35s |
| `36574954850` | main `149ba317` | failure | 43m14s | 43m03s |

Current successful job: `109717824822`, ubuntu-24.04. Verification ran from `2026-09-30T02:51:34Z` to `2026-09-30T03:37:09Z`. Source acquisition took two seconds, source upload two seconds and installation four seconds. The observed delay is not explained by those preparation steps.

The generic fetch action rejected the log endpoint, but the dedicated `fetch_workflow_job_logs` action subsequently recovered the complete decoded job log. Its sequential unittest summaries independently establish the following current-run figures:

| Package | Tests | unittest elapsed |
| --- | ---: | ---: |
| `standards_identity` | 16 | 0.162s |
| `standards_applicability` | 13 | 0.015s |
| `graph_engine` | 41 | 0.270s |
| `standards_graph` | 2 | 0.136s |
| `standards_snapshots` | 41 | 0.322s |
| `repository_git` | 52 | 5.715s |
| `review_evidence` | 49 | 4.501s |
| `standards_metadata` | 43 | 0.524s |
| `standards_policy_impact` | 10 | 0.596s |
| `standards_contracts` | 81 | 63.943s |
| `standards_analysis` | 125 | 1.597s |
| `standards_verifier` | 168 | 6.287s |
| `standards_engine` | 613 | 2,637.839s |

All 1,254 package tests report OK. The twelve non-Engine groups total 84.068s of reported test time; Engine accounts for approximately 96.4% of the 2,735-second verification step. The final structural result is `selected=73 passed=73 failed=0 blocked=0`. The timestamp interval between the Engine summary and final verifier output is approximately 8.5s; this is not separately instrumented process wall time.

The package totals make the priority clear: review-evidence's 441 setup processes are not the main hosted bottleneck because its entire 49-test package took only 4.501s. Contracts at 63.943s is a secondary contributor; the main investigation must identify the expensive bodies/setup within Engine's 2,637.839s. No per-test durations were emitted.

Retained: [hosted-baseline.json](hosted-baseline.json) and [selected exact job-log lines](hosted-job-log-excerpt.txt). The PR description's earlier 42m35s Engine / approximately 70s other-package figures refer to another run and are superseded here by current-run measurements.

The failed main run is useful history but is not a complete green baseline for performance acceptance. The supplied five-module 184.6-second result is a subset and cannot establish the cost of the current complete workflow.

## Findings and Dispositions

### F0 — Within-Engine attribution is missing despite clear package-level dominance

**Confirmed.** The workflow presents all 13 package commands plus the final verifier inside one large verification step. The recovered log identifies Engine as the 43m58s contributor, but does not identify individual expensive tests or setup phases. Native duration reporting and command-level timing can expose the relevant costs without changing test frameworks. Python 3.12 supports `unittest --durations N`; `0` reports every recorded test duration. Command wall time remains necessary for class/module setup and process overhead.

**Disposition:** M0. Preserve the required-check identity and all commands; collect source/environment identity and success/failure artifacts. Do not infer a particular test bottleneck solely from a static call count.

### F1 — Repository setup is repeated and has two inconsistent material contracts

**Confirmed, with a broader consumer inventory.** `test_analysis.py:151-230` clones with `--no-hardlinks`, enumerates tracked paths, removes obsolete tracked destination files, overlays current tracked content, stages it, commits if needed and selects main. `test_agent_workflow.py:22-38` performs a separate clone and overlays only three contract files. That second route can intentionally or accidentally combine committed corpus material and uncommitted contract material.

The complete bounded scan found 35 actual call expressions: 21 full-overlay calls and 14 `prepare_repository` calls. All are in Engine test/support files; several are standalone trace/MCP helpers, so a scan of only `test_*.py` misses them. The machine-readable inventory is [fixture-call-sites.json](fixture-call-sites.json). The original audit's approximate count is directionally right but should not be used as the number of runtime fixture constructions.

Existing fixture regression: `test_fixture_worktree.py:12-40` deliberately tests a staged deletion, staged addition, modified tracked bytes and excluded untracked file. Any seed or clean-source fast path must retain that contract. Cache-by-root or HEAD-only capture would be incorrect for dirty-source callers.

**Disposition:** M1. Consolidate the material owner, preserve intentional skew as explicit input, then retain only measured reuse. Independent Git/index/store state remains per consumer. A prepared seed is not automatically worthwhile for class fixtures that already initialize once.

### F2 — Review-evidence setup creates unnecessary Git prerequisites

**Confirmed.** `test_cli.py:20-49` issues nine Git commands per `setUp`. `test_repair_boundaries.py:15-19` reuses that setup by assigning methods from `PacketBuildTests`. There are 49 tests across these classes, hence 441 baseline setup commands, before test-body Git commands.

Examples without a Git-history requirement include ZIP traversal/duplicate validation (`test_cli.py:242`), portable-name checks (`test_repair_boundaries.py:33`), ZIP namespace validation (`:220`), descriptor lifecycle (`:304`) and linear namespace-work counting (`:320`). The duplicate-key portion of the request test at `test_cli.py:331` can also be isolated. That request test has other repository-dependent assertions, so it should not simply be moved wholesale.

**Disposition:** M2. Separate pure/filesystem setup from real Git integration. Preserve actual worktree/common-Git-directory, promisor, replace-ref, binary-diff, configuration and source-preservation evidence. The hosted package took only 4.501s, so this is useful bounded cleanup, not the explanation for the 43m58s Engine cost.

### F3 — Publication tests repeat complete verification

**Confirmed.** `test_coverage_publication.py:59-61` performs repository verification, `:440-449` performs reviewed preview verification, and `:463` applies through the real final verifier. The unreviewed preview at `:148-151` rejects before verification and is not another full verifier run. `test_analysis.py:476-478` separately exercises a real preview before real apply.

Production seam: `standards_engine/engine.py:736-754` owns repository verification; `:773-838` owns private-candidate preview; `:1483-1487` performs final application verification. Both preview and apply use `_application_verifier`, which is already replaceable in tests.

**Disposition:** M2. Use a narrow substitute only for duplicated preview orchestration within the large apply scenario. Keep a real coverage-aware preview and real final verification. Do not remove generated-input preparation just because repository verification is redundant: establish the required bytes through the existing producer, then retain the needed verification elsewhere. Preserve evidence changes after review, fresh authorization and cold consumers.

### F4 — Warm-cache publication is a full manual replay, not recursion

**Confirmed.** `test_process_reuse.py:391-410` calls `SupportingWorkflowTest.setUpClass`, replaces its authoring/application facades, invokes its full test method and calls its teardown. The full supporting scenario performs coordinated publication and a provenance-only revision (`test_supporting_workflow.py:79-143`). It is intentional repeated execution and has a hidden class-lifecycle dependency; it does not discover or recursively launch the suite.

Engine discovery in the review environment collected 613 unique test IDs, with no duplicate IDs or loader errors. The retained inventory does not count the manually invoked test body as another discovered ID; eliminating it therefore requires claim-level evidence mapping, not merely a stable test count.

**Disposition:** M2. Extract ordinary fixture actions and make the warm test directly assert reuse, purpose isolation, current/historical material and publication invalidation. Retain any unique provenance-cache claim. The detailed integration scenario keeps its original provenance/history coverage.

### F5 — Recovery setup is expensive, but its verification is already substituted

**Confirmed qualification to the optimization.** `test_publication_recovery.py:38-66` makes a fresh repository, opens an authoring facade, substitutes `_application_verifier`, proposes and reviews, locks main and attempts publication for each recovery test.

**Disposition:** Profile the repeated scenario construction. Factoring it into a helper is not a speedup by itself. Share only suitable initial material; keep fresh real proposal/readiness and mutation state. Do not copy path-bound admitted SQLite records or authorization into a different fixture root. Preserve independent recovery negatives and true fresh-process evidence elsewhere.

### F6 — Routing scenarios reload unchanged inputs

**Confirmed.** `standards_analysis/tests/test_routing.py:87-107` loads the canonical modules and router projection for every `route_task` call. Some tests invoke that helper several times. Other tests explicitly verify target drift or directory/recording/frozen source behavior and must keep their fresh inputs.

**Disposition:** Scoped read-only reuse within the unchanged scenario group, fresh fact bindings/results for every call. Its measured local contribution is small; the entire hosted Analysis package took only 1.597s. It is not a primary explanation for a 45-minute run.

### F7 — Coverage and digest assertions are weaker than their claimed result

**Confirmed.** `test_workflow_presentation.py:281-289` only runs the coverage-summary part when current corpus-derived work happens to contain a coverage attestation. An ordinary green run can bypass that intended assertion. It also compares two production projections; a controlled expected summary should independently state the result.

`test_coverage_publication.py:336-379` constructs changed bytes but both observed-digest assertions accept any value beginning `sha256:`. Compute the changed-byte digest independently and require exact equality at both the domain and outward diagnostic layers. Retain the earlier no-authorization assertion and diagnostic phase/material fields.

The adjacent presentation retry test at `:236-248` skips empty sections. Audit its claimed scope: populate all claimed sections or name the populated-section limitation. This is a bounded neighboring oracle review, not proof of another production defect.

**Disposition:** M0. Controlled wrong values should demonstrate that the strengthened checks reject the intended fault.

### F8 — Standalone compiler invocation omits two tests

**Confirmed.** `standards_contracts/tests/test_compiler.py:206-207` invokes `unittest.main()` before `OperationVariantTest` is declared at `:210-240`.

A nonexecuting collection probe found seven methods visible at the direct main guard, versus nine after full module import. The two missing methods belong to `OperationVariantTest`. This does not omit tests from the current GitHub discovery command. A bounded AST scan of the repository's test modules found no other later test class after a main guard.

**Disposition:** M0. Move the guard to the end; run both entrypoints and confirm both method identities. This is a local-invocation correctness fix, not a CI speed optimization.

## Local Diagnostic Results and Limits

Environment: Linux container, CPython 3.13.5, Git 2.47.3, jsonschema 4.26.0, rpds-py 2026.5.1. This is not the supported hash-locked Python 3.12 CI environment. The following observations locate work and validate source interpretation; they do not establish hosted performance improvement or full acceptance.

| Observation | Result |
| --- | --- |
| Full-overlay helper, three ordinary clean-source constructions | 0.600s, 0.540s, 0.639s |
| Three-contract-overlay helper, three constructions | 0.247s, 0.321s, 0.331s |
| Profiled full-overlay construction | 1,524 `copy2` calls, six Git subprocess calls, 0.931s profiled total |
| Analysis routing module | 11 tests passed in 0.750s |
| Review-evidence package | 49 tests passed in 15.326s |
| Engine collection | 613 unique IDs, zero loader errors |
| Compiler collection probe | seven direct-visible methods, nine imported methods; no body execution by this probe |
| Source status after probes | clean |

Ordinary helper timings exclude temporary-directory disposal after the measured function returns and include no claim of cold filesystem caches. A future seed comparison must include its complete lifecycle cost. Profiled timings include instrumentation overhead.

An initial combined shell invocation reached its local execution limit while beginning standalone compiler tests; it yielded no complete compiler result. A first collection probe lacked the standalone script-directory import path and was corrected. Neither attempt is counted as acceptance. The successful final collection probe is retained as collection-only evidence. The complete 613-test Engine suite was not rerun, and no optimized implementation was benchmarked.

Retained evidence: [local-diagnostics.json](local-diagnostics.json), [tracked-fixture-profile.txt](tracked-fixture-profile.txt), [routing-tests.log](routing-tests.log), [review-evidence-tests.log](review-evidence-tests.log), [compiler-discovery.json](compiler-discovery.json), [engine-test-inventory.json](engine-test-inventory.json), [fixture-call-sites.json](fixture-call-sites.json).

## Canonical Standards Applied

`workflows/planning.md` and `templates/PLAN-TEMPLATE.md` own plan lifecycle, artifacts, one next slice, write sets, claims and the composed-design probe. `workflows/verification.md`, especially Test Design, Test Data Authority and Lifecycle, Evidence and Oracles, Scheduling and Duration, and Claim-Directed Diagnosis, owns evidence fidelity and fixture preconditions. `topics/performance.md` owns workload, environment, variability, budget and comparison authority. `topics/architecture.md` owns test support responsibility and the composed-design/deletion probes. The existing authoring-publication-evidence, immutable-work-reuse, storage-lifecycle and targeted-test-strengthening plans provide constraints that this test-only effort must preserve.

Version-matched external references used for mechanism checks:

```text
https://docs.python.org/3.12/library/unittest.html
https://git-scm.com/docs/git-clone
```

Git's local-clone documentation distinguishes copying objects, local hardlinks and shared-object alternates. The proposed initial fixture design does not broadly remove `--no-hardlinks` or introduce alternates merely for speed.
