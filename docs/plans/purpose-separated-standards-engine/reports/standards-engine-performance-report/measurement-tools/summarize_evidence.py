"""Summarize measured artifacts without treating partial/failed cases as acceptance."""
from pathlib import Path
import csv,json,statistics,subprocess,time
W=Path('/mnt/data/engine-performance');E=W/'evidence';D=Path('/mnt/data/standards-engine-performance-report');D.mkdir(exist_ok=True)
def lines(path):
    result=[]
    for line in path.read_text().splitlines():
        try: result.append(json.loads(line))
        except json.JSONDecodeError: pass
    return result
ops=lines(E/'operations/operations.jsonl')
def group(name):
    return [r for r in ops if r['operation'].split('.',1)[1]==name]
def fmt(values):return (statistics.median(values),min(values),max(values))
# Individual repeated read/reopen entries remain in CSV; aggregate summary names their n.
with (D/'operation-baseline.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['operation','n','median_wall_s','min_wall_s','max_wall_s','median_cpu_s','execution_scope'])
    for name in dict.fromkeys(r['operation'].split('.',1)[1] for r in ops):
        rs=group(name);w.writerow([name,len(rs),*fmt([r['wall_s'] for r in rs]),statistics.median(r['cpu_s'] for r in rs),'isolated serial; three sweeps; same Python process except Engine/facade reopen'])
observations=[]
for path in sorted(E.glob('*.jsonl')):
    if not (path.name.startswith(('test_','qualified_')) or path.name in {'per-test-full.jsonl','slow-case-isolated.jsonl'}):continue
    lane=('isolated serial initial partial run' if path.name=='per-test-full.jsonl' else 'isolated serial slow-case reproduction' if path.name=='slow-case-isolated.jsonl' else 'disposable-main fixture qualification rerun; concurrent campaign' if path.name.startswith('qualified_') else 'isolated stores/checkouts; concurrent module campaign')
    for row in lines(path):
        if row.get('event')=='end':observations.append({**row,'lane':lane,'source_log':path.name})
with (D/'per-test-baseline.csv').open('w',newline='') as f:
    fields=['test','status','wall_s','cpu_s','setup_s','body_s','teardown_s','lane','source_log','content_id_calls','content_id_inclusive_s','compile_calls','compile_inclusive_s','proposal_projection_calls']
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for row in observations:
        spans=row.get('spans',{});get=lambda name,key:spans.get(name,{}).get(key,'')
        out={key:row.get(key,'') for key in fields};out.update(content_id_calls=get('SnapshotModule._content_id','calls'),content_id_inclusive_s=get('SnapshotModule._content_id','inclusive_s'),compile_calls=get('StandardsEngine._compile','calls'),compile_inclusive_s=get('StandardsEngine._compile','inclusive_s'),proposal_projection_calls=get('StandardsEngine._proposal_projection','calls'));w.writerow(out)
latest={}
# Prefer completed fixture-qualified reruns for the consolidated disposition, while retaining every attempt.
for row in observations:
    prev=latest.get(row['test'])
    if prev is None or row['source_log'].startswith('qualified_'):latest[row['test']]=row
counts={s:sum(r['status']==s for r in latest.values()) for s in ['pass','skip','error','failure']}
summary={'observed_distinct_tests':len(latest),'attempts':len(observations),'consolidated_statuses':counts,'per_test_is_not_one_serial_suite_run':True,'scheduler_complete':(E/'parallel-summary.json').exists(),'followup_complete':(E/'followup/measurements.json').exists(),'longest_completed':[{k:r.get(k) for k in ['test','wall_s','cpu_s','status','lane','source_log']} for r in sorted(latest.values(),key=lambda r:r['wall_s'],reverse=True)[:15]],'failures':[{k:r.get(k) for k in ['test','status','source_log','wall_s']} for r in latest.values() if r['status'] in {'failure','error'}]}
(D/'baseline-summary.json').write_text(json.dumps(summary,indent=2))
body='''# Standards Engine performance evidence

**Revision:** `8750761133b66297a2bfac4e495fd1c8a893b96a`  
**Branch examined:** `implementation/purpose-separated-standards-engine`  
**Date:** 2026-09-23  
**Status:** supporting measurements and design evidence, not installed acceptance or an optimized-candidate result.

## What was and was not accessed

The requested `/media/jeremy/.../Coding-Standards` path is not mounted in this environment. The remote branch was read through the GitHub connector; the exact published revision was reconstructed with Git CLI from the supplied full source bundle and incremental implementation bundle. The source reconstruction retains original local `main` at `366c1d9`. A disposable benchmark clone places the candidate on its own local `main`, following the documented pre-merge qualification procedure. None of these operations changes the user's repository, Codex configuration, or installed/archived store.

All instrumentation resides outside the source tree. Wrappers record elapsed time, CPU time and call counts and then invoke the original functions. No candidate optimization, rewritten source function, weakened assertion, skipped integrity gate, altered lockfile, or normative-content change was used. Tests that intentionally create/edit synthetic repositories continue doing so in their own temporary directories.

## Evidence classes and environment

| Class | What it establishes |
| --- | --- |
| User-reported | 32.5-second representative platform test, 11.5-second capture, roughly 10-second analysis sequence and 1.7-second calls; 4.6 MB store. Not independently reproduced on the user's machine. |
| Local operation measurement | Three isolated serial sweeps on the exact published source; operation timing and internal inclusive spans. |
| Local test measurement | Individual unmodified Engine tests with wall/CPU/phase timing and Python stack samples; split runs and concurrency are identified per row. |
| External CI record | Existing Python 3.12 locked-environment run for this SHA; not a newly executed run. |
| Profile / memory diagnostic | Mechanism attribution and retained-allocation estimate; profiling overhead is not the unprofiled latency baseline. |
| Cost model / target | Hypothetical savings and proposed budgets in the design, explicitly not measured candidate performance. |

The local environment is CPython 3.13.5, Linux 6.18.44, AMD EPYC 9V74, five visible logical CPUs with a four-CPU cgroup quota, approximately 6.24 GB available container memory allocation, no swap, and overlay-backed `/mnt/data` and `/tmp`. Git is 2.47.3. This is outside the project's supported Python 3.11/3.12 range. Installed `jsonschema` 4.26.0, `referencing` 0.37.0, `attrs` 26.1.0 and `jsonschema-specifications` 2025.9.1 match the inspected lock; installed `rpds-py` 2026.5.1 differs from pinned 2026.6.3. No claim of exact locked-environment acceptance is made.

The machine's filesystem page cache was not forcibly cleared. “Fresh process” below means a new interpreter or MCP process, not cold physical storage. The three operation sweeps were isolated from the test campaign; later per-module tests used separate checkouts/stores concurrently. Concurrency can inflate those per-test wall times and they are not serial production latency percentiles. Parent `process_time` excludes child-process CPU.

## Per-operation baseline

Raw observations are in `evidence/operations/operations.jsonl`; [operation-baseline.csv](operation-baseline.csv) contains individual operation-group medians and ranges. The following table combines repeated reads where appropriate.

| Operation | Samples | Median seconds | Minimum–maximum seconds |
| --- | ---: | ---: | ---: |
'''
selected=[('Engine open, new store',group('engine_open_new')),('Facade/interface construction',group('facade_construct')),('Create snapshot',group('create_snapshot')),('Explicit policy read',[r for r in ops if '.query_read_' in r['operation']]),('Policy inspection',group('inspect_policy')),('Route with explicit snapshot',group('route_explicit')),('Prepare, same snapshot in both roles',group('prepare_same_snapshot')),('Resolve submission',group('resolve')),('Analysis inspection',group('inspect_analysis')),('Snapshot inspection',group('inspect_snapshot')),('Reopen existing store',[r for r in ops if r['operation'].split('.',1)[1] in ['reopen_0','reopen_1']]),('Read after Engine reopen',[r for r in ops if '.reopened_query_' in r['operation']])]
for label,rs in selected:
    med,lo,hi=fmt([r['wall_s'] for r in rs]);body+=f'| {label} | {len(rs)} | {med:.4f} | {lo:.4f}–{hi:.4f} |\n'
body+='''
The operation workload uses an authoring Engine and explicit snapshot IDs. Preparation supplies the same snapshot as both accepted and proposed material, then exercises an existing test-authorizer evidence disposition. The external benchmark submits **current Analysis request version 6**. It is a valid current-contract benchmark, not a claim that the unchanged repository platform round-trip test passes.

Each captured corpus contains **434 files and 3,708,028 raw bytes**. The temporary database is **4,558,848 bytes** (1,113 × 4,096-byte pages). No archived 240 MB database participates. The aggregate read median is descriptive for nine reads across three sweeps; this sample is too small to establish a reliable p95/p99.

### Read and analysis attribution

A representative read is approximately 2.9 seconds: approximately 0.011 seconds in SQLite content loading, 2.54 seconds in the loading layer's content-identity work, and 0.32 seconds in full compilation. The direct long-test instrumentation independently times `SnapshotModule._content_id`, confirming that attribution. Removing only compilation would therefore retain approximately 89% of current read cost.

Same-snapshot `prepare` loads/verifies/compiles that snapshot **twice**; its median is 5.994 seconds. `resolve` evaluates pre- and post-submission states and loads/verifies/compiles the same material **four** times; its median is 12.120 seconds. The pure analysis evaluations themselves total approximately 0.047 seconds in the representative resolve. Keeping those two evaluations is necessary; reconstructing their unchanged inputs four times is the optimization opportunity.

Analysis inspection is approximately 0.006 seconds and snapshot inspection approximately 0.0006 seconds. A generic statement that every inspection is slow would be inaccurate: policy-child inspection takes the compiled-snapshot path, while these simpler inspections do not.

### Capture attribution

The representative capture has **1,137 Git-backed source reads for 434 distinct paths**, expanding to **6,134 object requests for 524 distinct repository/OID/type combinations**. There are 6,135 Git commands including the accepted-branch resolution. `_object` starts one `git cat-file --batch` process per requested object; it does not retain a batch process between requests.

The median Git-command span is approximately 11.34 seconds. First full compilation over Git-backed recording takes approximately 12.24 seconds. The required second fresh compilation over frozen content takes approximately 0.315 seconds. Remaining capture time includes exact content-ID generation and SQLite publication. These are nested spans: first-compilation time already includes the Git spans.

Thus the intentional second compile is not the dominant 11.5–15-second capture cost. Repeated commit/tree/blob retrieval and process setup account for most observed capture latency. The count ratio suggests 91.5% duplicate object fetches, but unique-object timing has not been isolated; the projected capture speedup remains a cost model.

## Long-case identification

The isolated test `test_agent_workflow.AgentWorkflowTest.test_normative_proposal_stops_at_real_pending_work` completed successfully with:

| Observation | Measured value |
| --- | ---: |
| Test body wall time | 119.854 seconds |
| Test parent-process CPU | 116.387 seconds |
| Entire one-test runner, including class setup/import work | 137.863 seconds |
| Content identity calls | 32 |
| Content identity inclusive time | 86.127 seconds |
| Full compiles | 52 |
| Compilation inclusive time | 18.528 seconds |
| Proposal projections | 21 |
| Projected-input validation calls | 10 |
| Resolve operations | 3 |

Identity accounts for about 71.9% and compilation about 15.5% of the body. Proposal-projection spans include those costs and are not additive. All three in-body stack samples (approximately 27, 72 and 117 seconds) were inside identity integer/byte encoding. The last sample traces `resolve_workflow → resolve → _evaluate → _validate_projected_inputs → _proposal_projection → load_content → _content_id`.

This identifies a reproducible roughly two-minute **case**, including a late duplicate projection, and shows that it is doing CPU work rather than waiting on a SQLite lock. The user's original unnamed two-minute case cannot be conclusively matched to this test. Other long cases are listed below; the original terminal output/test ID would be needed to identify which one the user saw.

## Per-test campaign and qualifications

'''
body+=f"The consolidated campaign currently records **{len(latest)} distinct completed tests**, with {counts['pass']} passing, {counts['skip']} skipped, {counts['error']} errors and {counts['failure']} failures across split runs. There are {len(observations)} recorded attempts, including qualification reruns. These are per-test observations, not a claim of one clean serial full-suite run. The full table is [per-test-baseline.csv](per-test-baseline.csv).\n\n"
body+='''The initial serial diagnostic run completed 13 tests and then ended while emitting a native `faulthandler` diagnostic during the next test. Its exit cause was not captured; cgroup OOM/pid-exhaustion counters did not identify a cause. This is not classified as a production crash or as the user's original incident. The continuation used a non-terminating Python-thread stack sampler instead, and the suspected slow test was rerun in isolation.

The remaining cases ran in isolated module checkouts/stores with up to three module processes. A separate one-process fixture-qualification rerun overlapped part of that campaign, making the maximum four test runners. The source revision and file bytes remained the same. Class-fixture costs and imports are included in each runner summary, outside individual test-body timing; sums of test rows are not a serial suite elapsed time.

Four initial cases using nested repository clones failed because nested `git clone` copied the checked-out feature branch but did not create its own local `main`. The parent benchmark clone did have candidate-local `main`. This is a fixture/checkout precondition, distinct from the Engine's correct accepted-main lookup. Those cases are rerun with an otherwise identical disposable source clone **checked out on local `main`**, so nested clones meet their assumed precondition. All failed attempts remain in the raw evidence and CSV.

### Longest completed case observations

| Test | Seconds | CPU seconds | Result | Scope |
| --- | ---: | ---: | --- | --- |
'''
for r in sorted(latest.values(),key=lambda r:r['wall_s'],reverse=True)[:10]:
    body+=f"| `{r['test']}` | {r['wall_s']:.3f} | {r.get('cpu_s',0):.3f} | {r['status']} | {r['lane']} |\n"
body+='''
### Existing CI record, separate environment

The existing GitHub Actions job **107298850681**, run **35895666852**, used this exact SHA with Python 3.12 and the complete hash-pinned dependency installation, including `rpds-py` 2026.6.3. Its log reports:

| Suite | Tests | Seconds | Result |
| --- | ---: | ---: | --- |
| Metadata | 31 | 0.350 | OK |
| Policy impact | 10 | 0.431 | OK |
| Contracts | 23 | 26.270 | OK |
| Analysis domain | 100 | 1.413 | OK |
| Verifier | 156 | 5.491 | OK |
| Engine | 157 | 2,946.090 | One error |

The Engine run took **49.10 minutes**. Its dots are buffered and supply no per-test times, so they cannot identify a two-minute case. The one error is `test_closed_store_round_trip_uses_public_operations`: `platform_harness.py` constructs Analysis request version 5 while the supported interface requires version 6. Preparation returns `INTERFACE.INVALID_ARGUMENTS`; the subsequent final structural command was not reached because the workflow uses fail-fast shell execution. This is a caller-conformance issue, not evidence that accepting version 5 would be an optimization.

The CI execution is independently useful because it demonstrates a long complete Engine run in the supported locked environment. It is not numerically interchangeable with this container's interpreter, hardware, resource limits, concurrency or per-test instrumentation.

Primary run: https://github.com/MrScripty/Coding-Standards/actions/runs/35895666852  
Job: https://github.com/MrScripty/Coding-Standards/actions/runs/35895666852/job/107298850681

## Additional slow paths

The coordinated supporting-content publication test completed in **839.065 seconds** during the concurrent campaign (617.979 seconds parent CPU), with **130 content-ID computations**, **278 compiles**, and **71 proposal projections**. Its identity span total was 380.130 seconds and its compilation span total 272.510 seconds. The compilation figure also includes Git-backed captures, so it cannot be read as 272 seconds of pure compiler CPU. This test deliberately crosses multiple captures, reviews, publication and historical-read boundaries. Its total counts are amplification evidence, not authority to eliminate all those checks or to promise a proportional whole-suite speedup.

The evidence-maintenance preview/overlap/apply test took **170.094 seconds** but only 27.812 seconds of parent CPU. Samples at approximately 43 and 133 seconds were inside per-file Git object subprocess work; a sample at approximately 88 seconds was waiting for a required Python package-verification child process. This is a distinct slow path, not evidence of a database deadlock. Capture-only caching would not accelerate its bulk revision read unless the bounded verified Git reader is reused there as well. The required verifier execution remains intact.

## Profiler and memory observations

A compiler-only `cProfile` observation records about 6.25 million calls and 1.467 seconds of profiled execution, versus about 0.32 seconds in the unprofiled operation baseline. Its cumulative hot path is coverage/suite-input identity generation, including approximately 68,954 `_encode_string` calls and 2.46 million `ord` calls. The profiler's timings include instrumentation overhead and are used for attribution, not latency targets.

A one-compilation `tracemalloc` observation records 3,649,110 additional retained bytes and 3,985,733 peak additional bytes. It excludes imports and the existing captured byte objects. Adding 3,708,028 raw capture bytes gives about 7.36 MB of representative retained material, supporting a two-entry cache design investigation, not proving a universal bound. Baseline process peak RSS includes other imports and identity-encoding temporaries; it must not be represented as cache size.

'''
follow=E/'followup/measurements.json'
if follow.exists():
    rows=json.loads(follow.read_text());body+='''### Additional isolated identity and transport observations

These runs begin after both test controllers finish, with no concurrent test runners. Fresh CLI and MCP calls use a consistent closed-store copy and current explicit snapshot. The hand-driven MCP test exercises actual stdio initialization, tool listing and calls, not the official SDK or configured Codex client.

| Observation | Seconds | Interpretation |
| --- | ---: | --- |
'''
    for row in rows:
        body+=f"| `{row['operation']}` | {row['wall_s']:.4f} | {'Mechanism-only; not a replacement hash contract' if row['operation'].startswith('sha256_') else 'Existing implementation'} |\n"
else:body+='Additional isolated identity and transport measurements are pending in the live working report. Final delivery requires their explicit measured or unavailable disposition.\n'
body+='''
## Conclusions supported by measurement

The dominant repeated-read cost is exact content-ID serialization/rehashing, rather than SQLite I/O. The dominant capture cost is repeated verified Git-object subprocess work. Repeated immutable material/projection derivation amplifies both mechanisms in authoring workflows. The fixed frozen replay pass is small relative to current Git-backed capture and remains necessary. A compiled cache alone has much less benefit than the phrase “recompile each call” suggests.

The archived 240 MB store, a deadlock, a 30/60/120-second timeout, network delay, or a specific Python-version regression has not been established as the cause of the user's original pause. The observed slow case is CPU-bound. SQLite write contention, large-store integrity-check growth, filesystem-cold behavior, a larger-than-budget cache population, optimized-candidate performance and configured-client behavior remain separate unmeasured claims.

## Reproduction and source integrity

See [README.md](README.md) for the isolated-checkout procedure and measurement commands. External harnesses are supplied under `measurement-tools/`. They measure the existing implementation; they are not proposed production code. All operation and test raw records retain status and scope. Supported-environment acceptance requires rerunning with the declared Python interpreter, exact lock and the actual required client.

Source integrity and branch/head observations are recorded in `evidence/source-integrity.json`. The design report is [design.md](design.md). No runtime optimization, standards edit, commit, remote push or PR is part of this task.
'''
(D/'evidence.md').write_text(body)
print(json.dumps(summary,indent=2))
