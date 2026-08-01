# Performance

**Standards metadata**

- ID: `topic.performance`
- Role: `topic`
- Level: `MUST`
- Applies when: A task changes a performance claim, budget, measurement, optimization, benchmark, resource-use behavior, or performance-sensitive implementation.
- Does not apply when: The task makes no performance or resource-use claim and does not change a measured performance-sensitive path.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Performance claim, measurement, optimization, benchmark, and regression decision fixtures plus claim-matched measurements in the required environment.
- Canonical owner: `topics/performance.md`

## Performance Claim Authority

Name the owned performance claim before selecting an optimization. The claim
identifies the operation or workflow, metric, workload, budget or comparison,
environment, variability policy, and consumer impact. Latency, throughput,
memory, energy, startup, frame time, and capacity are distinct claims.

A hot-path label, call frequency, allocation, algorithm class, profiler sample,
or benchmark result is evidence about a claim; it does not independently
authorize an implementation change.

## Measurement Contract

Measure the relevant workload in an environment representative of the claim.
Record inputs, data scale and distribution, warm-up or steady-state conditions,
runtime and build configuration, hardware or resource constraints, sample
method, variability, and baseline. Control only factors material to the claim.

Use profiling to locate contributing work when the claim and available tooling
make profiling informative. Profiling before every change is not universal,
and a profile does not prove an end-to-end budget or regression by itself.

Do not substitute a debug build, synthetic microbenchmark, single sample,
different device, stale baseline, or unrelated workload when the required
measurement is unavailable.

## Optimization Decision

Optimize when evidence shows the owned claim is unsatisfied or materially at
risk and the proposed change addresses a measured contributor. Evaluate the
effect on correctness, maintainability, resource use, other performance
claims, and operational complexity.

Allocation avoidance, pooling, caching, batching, precomputation, parallelism,
specialization, and lower-level representations are mechanisms, not defaults.
Code that runs at startup may still own a startup claim; code in a loop may be
irrelevant to the limiting claim. Readability does not automatically block or
authorize an optimization.

Retain the simplest implementation that satisfies the accepted claim and its
other contracts. Remove or revise an optimization when representative evidence
shows it no longer provides the intended value or its tradeoffs are no longer
accepted.

## Benchmarks And Regression Evidence

A benchmark names the claim it supports and preserves the material measurement
contract. Use a microbenchmark for an isolated mechanism claim and a broader
integration or user-workflow measurement for an end-to-end claim. Neither is a
universal substitute for the other.

Regression thresholds account for expected variability and decision cost.
Select absolute budgets, relative comparisons, statistical tests, trend
analysis, or another method from the claim. Do not require one duration,
percent threshold, benchmark framework, CI schedule, sample count, or target
machine for every project.

Documentation records durable claim, tradeoff, and reproduction facts that
cannot be recovered from the code and evidence. Do not require a copied
performance comment template or treat documentation as measurement.

## Performance Test Evidence

Select the benchmark or test harness from the owned claim, workload, required
environment, and measurement capability. An ecosystem harness may improve
repeatability, but its use does not establish that the workload, metric,
baseline, budget, or environment is authoritative. A unit-test clock around one
invocation does not prove an end-to-end latency, throughput, capacity, memory,
energy, startup, or frame-time claim unless its measurement contract covers
that claim.

A performance budget names its authority, consumer impact, workload, metric,
environment, and variability policy. Derive a threshold from that contract; do
not copy a duration, percentage, sample count, machine, CI cadence, or benchmark
tool from an example. Compare the candidate with the applicable baseline or
budget and preserve correctness and resource-tradeoff evidence.

When a representative environment, reliable measurement capability,
authoritative budget, or applicable baseline is unavailable, return
`unavailable`. Do not pass a weaker microbenchmark, nearby device, debug build,
single timing sample, or successful harness execution as the required result.

## Typed Outcomes

Contradictory metric, budget, workload, environment, or authority facts are
`invalid`. A declared claim or mechanism outside supported product or platform
capability is `unsupported`. Missing baseline, representative environment,
measurement capability, budget authority, or required evidence is
`unavailable`.

Do not continue with a guessed budget, conventional threshold, alternate
workload, stale benchmark, nearby device, allocation ban, hot-loop assumption,
weaker evidence, undocumented comparison, or default success.

## Verification

Evidence covers the accepted workload and environment, baseline and candidate,
variability policy, claimed improvement or budget, correctness and resource
tradeoffs, and negative or unsupported cases. Re-run the narrowest complete
claim after implementation and retain evidence according to its decision and
regression value.
