# Performance core increment — implementation and evidence

**Status:** implemented; local supporting verification complete. Supported-environment and independently reviewed performance acceptance remain unclaimed.

**Branch:** `implementation/purpose-separated-standards-engine`
**Input revision:** `90a3c8f13f517ad1dc32342fa10a4f1af181ed81`
**Scope:** the first increment of the [performance design](standards-engine-performance-report/design.md), authorized for implementation after that report was imported.

## Result and boundary

This change implements exact-format Identity-v2 acceleration, bounded operation-scoped reuse of verified Git objects, and explicit immutable-material reuse within native analysis operations. It retains the two independent capture compiles, captured path closure and semantic-signature comparisons, accepted-main selection, purpose-qualified projection, current authorization, live snapshot lifecycle checks, proposal-revision binding, publication verification/CAS, and observation-only recovery.

The source checkout's local `main` remains `366c1d90a24bbfb50973f62b155a5f3396c0f107`. The user's checkout, installed configuration and database were unavailable and were not modified. Disposable qualification clones deliberately establish their own accepted `main` at the candidate. The fixed-corpus benchmark instead keeps its disposable `main` at the input revision while loading the changed implementation, so baseline and candidate capture exactly the same inputs.

Normative standards, examples and prompts intended for ordinary standards use, policy declarations, public interface schemas, generated public models, dependency locks and version domains remain unchanged. The generated verification-input manifest is refreshed through the existing Engine operation. The existing accepted purpose-separation plan is not relabeled or reopened by this implementation report.

## Implementation ownership

| Owner | Change | Retained guarantee |
| --- | --- | --- |
| `standards_identity/encoding.py` | Construct validated path frames once; use exact byte-domain integer tokens and segment-based Unicode escaping/validation. | Identical Identity-v2 canonical preimages, scalar validation, arbitrary-size integer handling, domain/length framing and IDs. Full durable-load hashing still runs. |
| `repository_git` | Add a single-owner `RevisionReadSession`; use bounded LRU reuse of fully verified immutable object bytes at an exact revision. | Existing object header/type/length/framing/hash validation on each miss; path/mode/gitlink interpretation on each read; no failure caching. |
| Engine capture/evidence composition | Own and close a read session for each exact-revision bulk read. | Resolve accepted main once. Close the live reader before independent frozen replay. Mutable-source recording semantics remain unchanged. |
| Engine analysis | Pass a private `_EvaluationMaterials` value through prepare, prior-decision validation, resolution and provider-driven reevaluation. | Separate decision evaluations and fresh lifecycle/revision/authorization observations; one verified input per distinct root within the operation. |
| Logical authoring | Borrow an already compiled base only when it owns the exact supplied frozen source; reuse the exact proposal projection during validation. | Changed candidates still compile fully. Internal proof is not a public request or authorization input. |

The helper holds no response, authorization grant, provider result, mutable proposal-head decision, readiness or publication state. It is passed explicitly and expires with the owning operation. Focused workflow preflight and composed native operations retain separate barriers; the implementation does not stretch reuse over every nested public call. Publication and recovery continue to acquire their existing current observations.

The Git session retains at most 8 MiB of payload and 1,024 entries, with zero bounds supporting verified uncached operation. Keys include the configured repository, OID, expected type and hash algorithm. Valid oversized entries and evictions use normal verified reads. Close clears the cache and rejects subsequent reads. The session contains no long-lived subprocess; each Git command retains the existing bounded lifecycle. These are implementation-local retention settings, not generic standards or an RSS promise.

Cross-call compiled caches, persisted caches, selective compilation, a second graph/store, MCP lifetime changes, SQLite policy changes and additional compatibility paths remain outside this increment. Measured explicit MCP reads are about 1.1 seconds without those mechanisms; their extra state is deferred rather than assumed necessary.

## Paired operation measurements

Measurements use the same host, interpreter, dependencies, captured corpus and operation sequence before and after the change. They are local supporting results, not a supported-platform release claim. The final candidate sweeps ran after the other long campaigns completed. There are three independent operation sweeps; each contains three explicit reads. The sample establishes medians/ranges, not p95 or p99. Baseline then candidate execution is sequential rather than a randomized crossover, and wall-time variability remains an environmental limitation.

Both executable variants capture **434 files / 3,708,262 bytes** into **4,558,848-byte temporary SQLite databases**. Neither uses the archived 240 MB store. [Raw baseline](performance-core-evidence/baseline-operations.jsonl), [raw candidate](performance-core-evidence/candidate-operations.jsonl), and [comparison CSV including ranges](performance-core-evidence/comparison.csv) preserve the observations.

| Operation | Samples before / after | Baseline median | Candidate median | Speedup | Latency reduction |
| --- | ---: | ---: | ---: | ---: | ---: |
| `snapshot_capture` | 3 / 3 | 15.020 s | 2.529 s | 5.94× | 83.2% |
| `explicit_policy_read` | 9 / 9 | 3.059 s | 0.815 s | 3.75× | 73.4% |
| `policy_inspection` | 3 / 3 | 3.016 s | 0.808 s | 3.73× | 73.2% |
| `explicit_route` | 3 / 3 | 3.111 s | 0.991 s | 3.14× | 68.1% |
| `prepare_same_snapshot` | 3 / 3 | 6.243 s | 0.828 s | 7.54× | 86.7% |
| `resolve_same_snapshot` | 3 / 3 | 12.358 s | 0.851 s | 14.53× | 93.1% |
| `reopened_policy_read` | 6 / 6 | 2.978 s | 0.877 s | 3.40× | 70.6% |
| `identity_complete_identity` | 5 / 5 | 2.572 s | 0.592 s | 4.34× | 77.0% |
| `cold_cli_read` | 3 / 3 | 5.178 s | 3.122 s | 1.66× | 39.7% |
| `mcp_explicit_read` | 6 / 6 | 3.275 s | 1.095 s | 2.99× | 66.6% |
| `mcp_implicit_capture_read` | 1 / 1 | 18.180 s | 3.582 s | 5.08× | 80.3% |

The single implicit-capture transport observation is labeled as a single sample, not a stable median distribution. Cold CLI reads include Python/import/interface construction; explicit native reads start with an existing facade. MCP measurements include two separate server processes, three explicit reads per process, and normal per-call Engine/store opening. MCP startup itself remains approximately 1.6 seconds; it was not optimized. Existing-store opening remains approximately 4–5 ms.

### Integrity and work-count evidence

| Observation | Baseline | Candidate |
| --- | ---: | ---: |
| Capture logical source reads / unique paths | 1,137 / 434 | 1,137 / 434 |
| Capture fully verified Git object fetches / unique keys | 6,134 / 524 | 524 / 524 |
| Total Git commands in representative capture | 6,135 | 525 |
| Independent live and frozen full compiles | 2 | 2 |
| Same-snapshot prepare content loads / compiles | 2 / 2 | 1 / 1 |
| Same-snapshot resolve content loads / compiles | 4 / 4 | 1 / 1 |
| Resolve decision evaluations | 2 | 2 |

The full 3.71 MB capture produces the same **13,031,223 encoded bytes**, encoded digest `73cbb95660b04a89dd8fd5f11adb8cadd99f4651ec6836fbd75720bdc8084bc0`, and content ID `snapshot-content:sha256:e95df9fd7e1c346706c40733ef93b39f87a6a29e50fad8fcb993a99fc1f10582` in both implementations. [Primitive baseline](performance-core-evidence/baseline-primitives.json) and [primitive candidate](performance-core-evidence/candidate-primitives.json) each contain five observations. The optimized full identity median is 23.0% of baseline, meeting the design's local one-quarter target.

The capture cache peaked at **3,744,707 payload bytes and 524 entries**, below both budgets, and reported zero retained payload/entries after close. This measures cache-owned payload and entry count, not full process memory; captured source bytes may remain held independently because replay requires them. Whole-process RSS and allocation traces are not used to claim an independent memory speedup.

Cold CLI full-result hashes and explicit MCP result hashes match their respective baseline outputs byte-for-byte after canonical result serialization. No retained cross-call cache is needed for those results. Explicit reopen reads and the existing cold-process tests establish that these gains do not depend on an originating Engine instance.

## Long-test reproduction

`test_agent_workflow.AgentWorkflowTest.test_normative_proposal_stops_at_real_pending_work` passed before and after with its original assertions:

| Metric | Fresh baseline | Candidate |
| --- | ---: | ---: |
| Test body wall time | 116.120 s | 17.719 s |
| Content-identity computations | 32 | 10 |
| Full compiles | 52 | 18 |
| Proposal projections | 21 | 9 |
| Stored revision reads | 24 | 32 |

The extra cheap revision observations retain current authority while expensive immutable derivation falls. Identity work decreased from 83.129 s to 6.294 s in this test. Inclusive parent/child spans overlap and are not additive. [Baseline log](performance-core-evidence/baseline-long.jsonl) and [candidate campaign](performance-core-evidence/full-engine.jsonl) contain the detailed traces.

This workflow comparison uses each revision's candidate-derived fixture corpus, unlike the fixed-corpus operation benchmark. Candidate test timing comes from the Engine campaign rather than a randomized repeated single-test study. It is a directly observed improvement for that named case, not a claim of a uniform whole-suite speedup or proof of the identity of an earlier unnamed pause.

## Functional verification

The complete Engine population contains **166 distinct tests**. The initial full campaign produced 162 passes and four fixture errors/failures. Investigation showed that two disposable-clone helpers inherited the feature branch name and never established a local accepted `main`. The repair creates `main` only in those disposable candidate repositories. Production accepted-main selection and every behavior assertion remain unchanged.

The four cases subsequently passed on the repaired candidate, including actual topology publication, exact-candidate verification and cold readback, coverage publication/interruption recovery, and snapshot reads after worktree changes. Thus all 166 have successful evidence **across the full campaign and the four reruns**; this is not represented as one clean full-suite command. The initial errors remain visible in [full-engine.log](performance-core-evidence/full-engine.log), and corrections in [fixture-reruns.log](performance-core-evidence/fixture-reruns.log) and [per-test disposition](performance-core-evidence/per-test-disposition.csv).

All changed production Python ASTs match the full-run candidate. The only subsequent Python changes are the two Engine fixture repairs and an additional real SHA-256/object-limit Repository Git test, which passed in its complete final package run. Final implementation/test ASTs match the tested source; [tested-source.json](performance-core-evidence/tested-source.json) records this comparison and file digests. The full run and fixture reruns overlapped during part of execution, so their elapsed totals are not treated as a clean sequential suite benchmark. The final operation and transport sweeps started after both completed.

New regressions prove exact scalar/byte/Unicode framing, one frame construction per input path, cache disabling/eviction/oversized behavior, missing/corrupt objects, gitlink repository isolation, real SHA-256 Git repositories, read-session close semantics, same/distinct snapshot handling, pre/post decision evaluation, fresh denial/authorization, quarantine during authorization, independent capture compiles, and borrowed-projection ownership. Existing purpose, hidden-intermediary, unsupported capture, publication, stale-state and cold-recovery tests retain their assertions.

Supporting packages ran separately:

| Package | Tests run | Result |
| --- | ---: | --- |
| `graph_engine` | 37 | Passed |
| `repository_git` | 16 | Passed |
| `standards_analysis` | 100 | Passed |
| `standards_applicability` | 12 | Passed |
| `standards_contracts` | 23 | Passed; 1 interpreter-dependent skip |
| `standards_graph` | 2 | Passed |
| `standards_identity` | 11 | Passed |
| `standards_metadata` | 31 | Passed |
| `standards_policy_impact` | 10 | Passed |
| `standards_snapshots` | 23 | Passed |
| `standards_verifier` | 156 | Passed |

The 421 package-test invocations include one existing interpreter-dependent skip in Contracts. The structural checkpoint separately reports **73 suites / 121 checks passed**; it is not substituted for behavioral tests. No installed formatter/linter result or independently delegated review is claimed. Review of the changed call sites, invariants and test differences was performed in this implementation session.

## Environment and acceptance limits

[Environment evidence](performance-core-evidence/environment.json): Python **3.13.5**, Git **2.47.3**, SQLite **3.46.1**, Linux **6.18.44**, four-CPU cgroup quota and 4 GiB memory limit. Python is outside the repository's supported 3.11/3.12 range; local `rpds-py 2026.5.1` differs from pinned `2026.6.3`. Other recorded dependency versions match their lock. Dependencies and support declarations were preserved.

The required remaining qualification is a clean complete suite in the supported locked environment, plus the configured official SDK/client lane and independent review before claiming this increment fully qualified for the installed system. The real stdio/CLI measurements here are stronger than mocks but do not substitute for the official configured client. No performance threshold was used to kill otherwise-correct application work.

The local targets for capture, explicit reads, full identity cost, same-snapshot preparation/resolution and the named long test were met. New supported-host measurements should establish their absolute deployment budgets rather than copy these local numbers. Existing main/store cutover and unfinished-work dispositions remain the installation owner's responsibility; this increment adds no store conversion or new persisted/public version.

## Reproduction

Use isolated clones and disposable stores only. Preserve the actual user branch, main and installed store. Obtain a baseline checkout at the input revision and a second checkout with this implementation. For a fixed-corpus comparison, make the disposable local main in both clones identify the input revision; run the candidate executable code without moving that benchmark main. For full functional qualification, the disposable candidate main must identify the tested candidate, matching the installed-candidate contract.

Run `measurement-tools/measure_operations.py` in the adjacent original performance report with `--repo`, a new `--output` directory and `--samples 3` for each executable. It produces the input store and snapshot handles used by the two supplemental [primitive](performance-core-evidence/measure_primitives.py) and [transport](performance-core-evidence/measure_transport.py) probes. Give those probes an explicitly selected disposable store/snapshot; the transport probe additionally requires `--confirm-disposable`. Their output paths retain the raw results. The original `timed_suite.py` script records per-test bodies, setup/teardown, counters and overlapping spans; preserve both failures and rerun results.

In the supported locked interpreter, run the eleven package discovery commands under `tools/<package>/tests` and `unittest discover -s tools/standards_engine/tests`; use `PYTHONPATH=.:tools/standards_verifier` where required. Run the separate Engine `verify_repository` checkpoint and inspect its actual `verification.passed` result. The publication tests use real disposable Git and SQLite state.

## Retained scope decision

The measured first increment solves the large redundant work without a new cross-call cache or changing transport/storage lifetime. Keep those larger options deferred. Residual latency is now primarily ordinary full content verification, compiler and process/interface construction; only a subsequent measured requirement should admit extra retained state. The original design/evidence remain historical inputs, while this report records the implementation and its observed limits.
