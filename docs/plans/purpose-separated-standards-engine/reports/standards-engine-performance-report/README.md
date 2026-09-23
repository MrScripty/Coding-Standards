# Standards Engine performance design and evidence

This package contains analysis, a proposed design, raw measurement evidence, and external measurement scripts. It contains **no production implementation patch**. The source branch and normative standards are unchanged.

## Read the reports

- [Recommended design and verification plan](design.md)
- [Measured evidence and limitations](evidence.md)
- [Per-test timing table](per-test-baseline.csv): every completed attempt, including failed initial attempts and qualified reruns.
- [Per-operation timing table](operation-baseline.csv)
- [Machine-readable summary](baseline-summary.json)

The baseline is the published branch `implementation/purpose-separated-standards-engine` at `8750761133b66297a2bfac4e495fd1c8a893b96a`. The user's local checkout and installed database were not accessible. The reports distinguish local supporting measurements, the user's reported timings, existing CI results, and unmeasured design targets.

## Reproduce on the supported environment

Use a disposable clone and an evidence directory outside the source tree. The commands below deliberately change only the disposable clone's `main`, not the real accepted branch. They also check out that local main because some existing tests create nested clones that assume their checked-out branch is named main.

```bash
SOURCE='/media/jeremy/OrangeCream/Linux Software/repos/owned/developer-tooling/Coding-Standards'
WORK="$(mktemp -d)"
OUT="$WORK/evidence"
mkdir -p "$OUT"
git clone --local --no-hardlinks \
  --branch implementation/purpose-separated-standards-engine \
  "$SOURCE" "$WORK/repo"
git -C "$WORK/repo" checkout -B main \
  8750761133b66297a2bfac4e495fd1c8a893b96a

# Select the existing supported 3.11/3.12 environment installed from the exact lock.
PY='/absolute/path/to/locked-engine-environment/bin/python'
REPORT='/absolute/path/to/standards-engine-performance-report'
export PYTHONDONTWRITEBYTECODE=1

"$PY" "$REPORT/measurement-tools/run_timed_suite.py" \
  --repo "$WORK/repo" --output "$OUT/engine-tests.jsonl"

"$PY" "$REPORT/measurement-tools/measure_operations.py" \
  --repo "$WORK/repo" --output "$OUT/operations" --samples 3 --profile

"$PY" "$REPORT/measurement-tools/measure_followup.py" \
  --repo "$WORK/repo" --evidence "$OUT"
```

Run these commands serially for isolated latency comparison. The submitted report's complete per-test population was assembled from split runs, with explicitly labeled concurrent module timing; it is not represented as a serial full-suite latency measurement. Increase independent paired repetitions when establishing candidate regression thresholds; the report's three operation sweeps do not establish a tail-latency SLA.

The unchanged platform harness at this revision submits Analysis request version 5 to the version-6 interface and therefore fails. The standalone operation benchmark constructs valid version-6 requests; it does not repair or bypass that test. Keep this failure visible until a separately authorized harness-conformance repair is made.

`run_timed_suite.py` times setup, body, teardown and selected original method calls, and uses a Python-thread sampler to capture long-case stacks without terminating the test. It preserves test assertions and call behavior. The optional `--test` or `--pattern` selects a narrower measurement. The scripts assume the measured branch's actual methods; revalidate instrumentation when applying them to later implementations.

`measure_followup.py` reuses a fully closed disposable store created by the operation script. It measures existing identity framing/encoding, fresh-process CLI reads, hand-driven MCP stdio calls, and two concurrent readers. Its SHA-256-only probe is attribution evidence, never a replacement content-ID contract. Fresh processes do not imply that physical filesystem caches were flushed. Official MCP SDK and configured Codex acceptance remain separate from this protocol-level measurement.

## Evidence contents

`evidence/operations/operations.jsonl` holds nested inclusive and exclusive span accounting. `evidence/*test*.jsonl`, `evidence/test_*.jsonl`, and `evidence/qualified_*.jsonl` hold test start/end records, statuses and stack observations. Associated stderr files retain failures. `evidence/ci-baseline.json` transcribes the relevant existing CI log results and names their primary source. `evidence/environment.json` and `evidence/source-integrity.json` record the local execution boundary.

Binary SQLite stores, repository copies, private installed state and Git bundles are intentionally absent from this report package. Reproduction creates its own disposable stores. Text profiler summaries are provided instead of requiring profiler tooling to open binary profiles. `SHA256SUMS` covers the packaged reports, observations and measurement tools.

The original orchestration scripts are also included to explain campaign provenance, but contain the report-generation environment's `/mnt/data/engine-performance` paths. The three commands above are the portable measurement entrypoints; the orchestration scripts are not required for reproduction.
